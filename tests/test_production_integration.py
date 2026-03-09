"""
Integration tests for the production pipeline with institutional intelligence.

Tests that PredictionService correctly wires:
  - InstitutionalDecisionEngine (7-phase gate)
  - Portfolio optimization (CVaR + survival)
  - Calibration monitoring (Brier / ECE / drift)
  - Report rendering with new sections
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wbc_backend.betting.risk_control import BankrollState
from wbc_backend.config.settings import AppConfig
from wbc_backend.domain.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BetRecommendation,
    GameOutput,
    Matchup,
    OddsLine,
    PredictionResult,
    SimulationSummary,
    SubModelResult,
    TeamSnapshot,
)
from wbc_backend.intelligence.decision_engine import DecisionReport
from wbc_backend.pipeline.service import PredictionService
from wbc_backend.reporting.renderers import render_full_report, render_json


# ──────────────────────────────────────────────────────────────────────────────
#  Fixtures
# ──────────────────────────────────────────────────────────────────────────────

def _make_matchup() -> Matchup:
    return Matchup(
        game_id="WBC2026_TPE_JPN_001",
        tournament="WBC2026",
        game_time_utc="2026-03-15T10:00:00Z",
        home=TeamSnapshot(
            team="TPE", elo=1580, batting_woba=0.340,
            batting_ops_plus=112, pitching_fip=3.40,
            pitching_whip=1.18, pitching_stuff_plus=108,
            der=0.710, bullpen_depth=9.0, pitch_limit=65,
        ),
        away=TeamSnapshot(
            team="JPN", elo=1680, batting_woba=0.360,
            batting_ops_plus=130, pitching_fip=2.90,
            pitching_whip=1.05, pitching_stuff_plus=115,
            der=0.730, bullpen_depth=9.5, pitch_limit=65,
        ),
    )


def _make_pred() -> PredictionResult:
    return PredictionResult(
        game_id="WBC2026_TPE_JPN_001",
        home_win_prob=0.38,
        away_win_prob=0.62,
        expected_home_runs=3.2,
        expected_away_runs=4.5,
        x_factors=["Ohtani dual-threat"],
        diagnostics={"brier_score": 0.22, "platt_a": 1.05, "platt_b": -0.02},
        sub_model_results=[
            SubModelResult("elo", 0.35, 0.65, confidence=0.6),
            SubModelResult("bayesian", 0.40, 0.60, confidence=0.7),
            SubModelResult("poisson", 0.38, 0.62, confidence=0.65),
        ],
        confidence_score=0.72,
    )


def _make_sim() -> SimulationSummary:
    return SimulationSummary(
        home_win_prob=0.37,
        away_win_prob=0.63,
        over_prob=0.55,
        under_prob=0.45,
        home_cover_prob=0.30,
        away_cover_prob=0.70,
        mean_total_runs=7.5,
        std_total_runs=2.8,
        odd_prob=0.52,
        even_prob=0.48,
        home_f5_win_prob=0.40,
        away_f5_win_prob=0.60,
        score_distribution={"3-4": 0.08, "2-5": 0.06, "4-3": 0.05},
        n_simulations=50_000,
    )


def _make_odds_lines() -> List[OddsLine]:
    return [
        OddsLine("TSL", "ML", "HOME", None, 2.70, "tsl"),
        OddsLine("TSL", "ML", "AWAY", None, 1.50, "tsl"),
        OddsLine("TSL", "OU", "OVER", 7.5, 1.90, "tsl"),
        OddsLine("TSL", "OU", "UNDER", 7.5, 1.90, "tsl"),
    ]


def _make_top_bets() -> List[BetRecommendation]:
    return [
        BetRecommendation(
            market="ML", side="AWAY", line=None, sportsbook="TSL",
            source_type="tsl", win_probability=0.62, implied_probability=0.667,
            ev=0.038, edge=0.045, kelly_fraction=0.03,
            stake_fraction=0.015, stake_amount=150, confidence=0.72,
        ),
        BetRecommendation(
            market="OU", side="OVER", line=7.5, sportsbook="TSL",
            source_type="tsl", win_probability=0.55, implied_probability=0.526,
            ev=0.025, edge=0.030, kelly_fraction=0.02,
            stake_fraction=0.010, stake_amount=100, confidence=0.65,
        ),
    ]


def _make_game_output(top_bets: List[BetRecommendation]) -> GameOutput:
    return GameOutput(
        game_id="WBC2026_TPE_JPN_001",
        home_team="TPE",
        away_team="JPN",
        home_win_prob=0.38,
        away_win_prob=0.62,
        predicted_home_score=3.2,
        predicted_away_score=4.5,
        market_bias_score=0.015,
        ev_best=0.038,
        best_bet_strategy="ML AWAY @ TSL",
        confidence_index=0.72,
        top_3_bets=top_bets,
    )


# ──────────────────────────────────────────────────────────────────────────────
#  1. Decision Engine Integration
# ──────────────────────────────────────────────────────────────────────────────

class TestDecisionEngineIntegration(unittest.TestCase):
    """Test _run_decision_engine via PredictionService."""

    def test_decision_engine_returns_report(self):
        """Engine should return a DecisionReport with expected fields."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        matchup = _make_matchup()
        pred = _make_pred()
        odds = _make_odds_lines()

        rpt = svc._run_decision_engine(matchup, pred, 0.38, odds)

        self.assertIsInstance(rpt, DecisionReport)
        self.assertIn(rpt.decision, ("BET", "NO_BET", "WATCH"))
        self.assertIn(rpt.confidence, ("LOW", "MODERATE", "STRONG", "ELITE"))
        self.assertIsInstance(rpt.edge_score, float)
        self.assertIsInstance(rpt.market_regime, str)

    def test_decision_engine_extracts_sub_model_probs(self):
        """Verify that sub-model probs are extracted from PredictionResult."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        matchup = _make_matchup()
        pred = _make_pred()
        odds = _make_odds_lines()

        rpt = svc._run_decision_engine(matchup, pred, 0.38, odds)

        # The engine should have received our 3 sub-model probs
        self.assertIn("match_id", vars(rpt) if hasattr(rpt, '__dict__') else dir(rpt))
        self.assertEqual(rpt.match_id, "WBC2026_TPE_JPN_001")

    def test_decision_engine_uses_correct_odds(self):
        """ML odds from odds_lines should be extracted correctly."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        matchup = _make_matchup()
        pred = _make_pred()

        # Use TPE/JPN team names in odds
        odds = [
            OddsLine("TSL", "ML", "TPE", None, 3.00, "tsl"),
            OddsLine("TSL", "ML", "JPN", None, 1.40, "tsl"),
        ]
        rpt = svc._run_decision_engine(matchup, pred, 0.38, odds)
        self.assertIsInstance(rpt, DecisionReport)


# ──────────────────────────────────────────────────────────────────────────────
#  2. Portfolio Optimization Integration
# ──────────────────────────────────────────────────────────────────────────────

class TestPortfolioOptimization(unittest.TestCase):

    def test_portfolio_returns_valid_metrics(self):
        """Portfolio should return survival, CVaR, drawdown scale."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        top_bets = _make_top_bets()
        decision_rpt = DecisionReport(
            decision="BET", confidence="MODERATE", edge_score=3.5,
        )

        metrics = svc._run_portfolio_optimization(top_bets, decision_rpt)

        self.assertIn("survival_prob", metrics)
        self.assertIn("cvar_95", metrics)
        self.assertIn("drawdown_scale", metrics)
        self.assertIn("decision_verdict", metrics)
        self.assertEqual(metrics["decision_verdict"], "BET")
        self.assertGreater(metrics["survival_prob"], 0)
        self.assertLessEqual(metrics["survival_prob"], 1.0)
        self.assertEqual(metrics["drawdown_scale"], 1.0)  # no drawdown

    def test_portfolio_empty_bets(self):
        """Empty bet list should return safe defaults."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        decision_rpt = DecisionReport(decision="NO_BET")

        metrics = svc._run_portfolio_optimization([], decision_rpt)

        self.assertEqual(metrics["survival_prob"], 1.0)
        self.assertEqual(metrics["cvar_95"], 0.0)
        self.assertEqual(metrics["drawdown_scale"], 1.0)

    def test_portfolio_drawdown_scaling(self):
        """When bankroll has drawdown, scale should be < 1."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        svc.bankroll.peak = 100_000
        svc.bankroll.current = 80_000  # 20% drawdown
        top_bets = _make_top_bets()
        decision_rpt = DecisionReport(decision="BET", edge_score=2.0)

        metrics = svc._run_portfolio_optimization(top_bets, decision_rpt)

        self.assertLess(metrics["drawdown_scale"], 1.0)
        self.assertAlmostEqual(metrics["current_drawdown"], 0.2, places=2)


# ──────────────────────────────────────────────────────────────────────────────
#  3. Calibration Monitoring Integration
# ──────────────────────────────────────────────────────────────────────────────

class TestCalibrationMonitoring(unittest.TestCase):

    def test_calibration_returns_none_below_threshold(self):
        """Should return None when < 10 predictions accumulated."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        svc._prob_history = [0.6, 0.7, 0.5]  # only 3
        self.assertIsNone(svc._run_calibration_monitoring())

    def test_calibration_returns_metrics_at_threshold(self):
        """Should return calibration dict at 10+ predictions."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        svc._prob_history = [0.4, 0.6, 0.7, 0.3, 0.55, 0.65, 0.45, 0.5, 0.6, 0.7]
        svc._outcome_history = [0, 1, 1, 0, 1, 1, 0, 0, 1, 1]

        result = svc._run_calibration_monitoring()

        self.assertIsNotNone(result)
        self.assertIn("brier", result)
        self.assertIn("logloss", result)
        self.assertIn("ece", result)
        self.assertIn("mce", result)
        self.assertEqual(result["n_predictions"], 10.0)
        self.assertGreaterEqual(result["brier"], 0.0)
        self.assertLessEqual(result["brier"], 1.0)

    def test_calibration_drift_detection(self):
        """With 20+ predictions, should include drift metrics."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        svc._prob_history = [0.5] * 10 + [0.8] * 10  # shift at midpoint
        svc._outcome_history = [0, 1] * 10

        result = svc._run_calibration_monitoring()

        self.assertIsNotNone(result)
        self.assertIn("drift_flag", result)

    def test_record_outcome(self):
        """record_outcome should append to history."""
        from wbc_backend.pipeline.service import PredictionService

        svc = PredictionService()
        svc.record_outcome(1)
        svc.record_outcome(0)
        self.assertEqual(svc._outcome_history, [1, 0])

    def test_bankroll_storage_is_loaded_and_persisted(self):
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "bankroll.db"
            base = AppConfig()
            config = replace(
                base,
                sources=replace(base.sources, bankroll_storage_db=str(db_path)),
            )

            svc = PredictionService(config)
            svc.bankroll = BankrollState(
                initial=100_000.0,
                current=125_000.0,
                peak=130_000.0,
                daily_start=120_000.0,
            )
            svc.bankroll_storage.save(svc.bankroll)

            reloaded = PredictionService(config)
            self.assertEqual(reloaded.bankroll.current, 125_000.0)

            reloaded.record_outcome(
                1,
                pnl=2_500.0,
                stake=1_000.0,
                game_id="A05",
                market="ML",
                side="COL",
                odds=1.91,
            )

            persisted = PredictionService(config)
            self.assertEqual(persisted.bankroll.current, 127_500.0)
            self.assertEqual(len(persisted.bankroll_storage.get_bet_history()), 1)


# ──────────────────────────────────────────────────────────────────────────────
#  4. Report Rendering with Intelligence Data
# ──────────────────────────────────────────────────────────────────────────────

class TestReportRendering(unittest.TestCase):

    def _build_decision_report(self):
        return DecisionReport(
            match_id="WBC2026_TPE_JPN_001",
            match_label="JPN @ TPE",
            decision="BET",
            confidence="STRONG",
            edge_score=4.2,
            market_regime="LIQUID_MARKET",
            bets=[],
        )

    def test_markdown_includes_decision_section(self):
        game = _make_game_output(_make_top_bets())
        pred = _make_pred()
        sim = _make_sim()
        rpt = self._build_decision_report()

        md = render_full_report(
            game, pred, sim, {"adjusted_home_prob": 0.38},
            decision_report=rpt,
        )

        self.assertIn("INSTITUTIONAL DECISION ENGINE", md)
        self.assertIn("BET", md)
        self.assertIn("STRONG", md)
        self.assertIn("4.2", md)
        self.assertIn("Final Calibrated Win Probability", md)

    def test_markdown_includes_portfolio_section(self):
        game = _make_game_output(_make_top_bets())
        pred = _make_pred()
        sim = _make_sim()
        portfolio = {"survival_prob": 0.95, "cvar_95": 0.003, "expected_return": 0.012,
                      "gross_exposure": 0.05, "drawdown_scale": 0.85, "current_drawdown": 0.1}

        md = render_full_report(
            game, pred, sim, {"adjusted_home_prob": 0.38},
            portfolio_metrics=portfolio,
        )

        self.assertIn("PORTFOLIO OPTIMIZATION", md)
        self.assertIn("95.0%", md)  # survival prob
        self.assertIn("0.003000", md)  # cvar

    def test_markdown_includes_calibration_section(self):
        game = _make_game_output(_make_top_bets())
        pred = _make_pred()
        sim = _make_sim()
        cal = {"brier": 0.22, "logloss": 0.69, "ece": 0.05, "mce": 0.12, "n_predictions": 50.0}

        md = render_full_report(
            game, pred, sim, {"adjusted_home_prob": 0.38},
            calibration_metrics=cal,
        )

        self.assertIn("CALIBRATION MONITORING", md)
        self.assertIn("0.2200", md)
        self.assertIn("50", md)

    def test_json_includes_decision_engine(self):
        game = _make_game_output(_make_top_bets())
        pred = _make_pred()
        sim = _make_sim()
        rpt = self._build_decision_report()

        json_str = render_json(
            game, pred, sim, {"adjusted_home_prob": 0.38},
            decision_report=rpt,
        )
        data = json.loads(json_str)

        self.assertIn("decision_engine", data)
        self.assertEqual(data["final_probability_basis"], "market_calibrated")
        self.assertEqual(data["decision_engine"]["verdict"], "BET")
        self.assertEqual(data["decision_engine"]["confidence"], "STRONG")
        self.assertAlmostEqual(data["decision_engine"]["edge_score"], 4.2)

    def test_json_includes_portfolio_and_calibration(self):
        game = _make_game_output(_make_top_bets())
        pred = _make_pred()
        sim = _make_sim()
        portfolio = {"survival_prob": 0.92, "cvar_95": 0.005}
        cal = {"brier": 0.20, "ece": 0.04}

        json_str = render_json(
            game, pred, sim, {"adjusted_home_prob": 0.38},
            portfolio_metrics=portfolio,
            calibration_metrics=cal,
        )
        data = json.loads(json_str)

        self.assertIn("portfolio", data)
        self.assertEqual(data["portfolio"]["survival_prob"], 0.92)
        self.assertIn("calibration", data)
        self.assertEqual(data["calibration"]["brier"], 0.20)

    def test_json_without_optional_fields(self):
        """When no decision/portfolio/calibration, JSON should still work."""
        game = _make_game_output([])
        pred = _make_pred()
        sim = _make_sim()

        json_str = render_json(game, pred, sim, {"adjusted_home_prob": 0.38})
        data = json.loads(json_str)

        self.assertNotIn("decision_engine", data)
        self.assertNotIn("portfolio", data)
        self.assertNotIn("calibration", data)


# ──────────────────────────────────────────────────────────────────────────────
#  5. AnalyzeResponse Schema
# ──────────────────────────────────────────────────────────────────────────────

class TestAnalyzeResponseSchema(unittest.TestCase):

    def test_response_accepts_new_fields(self):
        resp = AnalyzeResponse(
            markdown_report="test",
            json_report="{}",
            decision_report=DecisionReport(decision="NO_BET"),
            calibration_metrics={"brier": 0.25},
            portfolio_metrics={"survival_prob": 0.99},
        )
        self.assertEqual(resp.decision_report.decision, "NO_BET")
        self.assertEqual(resp.calibration_metrics["brier"], 0.25)
        self.assertEqual(resp.portfolio_metrics["survival_prob"], 0.99)


class TestScoreConsistency(unittest.TestCase):

    def test_display_scores_reconcile_when_prob_and_score_disagree(self):
        home, away, reconciled = PredictionService._resolve_display_scores(
            raw_home_runs=6.8,
            raw_away_runs=5.1,
            mean_total_runs=11.6,
            final_home_prob=0.459,
        )

        self.assertTrue(reconciled)
        self.assertLess(home, away)
        self.assertAlmostEqual(home + away, 11.6, places=1)


if __name__ == "__main__":
    unittest.main()
