from __future__ import annotations

import os
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wbc_backend.betting.market import market_adjustment
from wbc_backend.config.settings import AppConfig
from wbc_backend.domain.schemas import AnalyzeRequest, Matchup, TeamSnapshot
from wbc_backend.ingestion.unified_loader import UnifiedDataLoader
from wbc_backend.pipeline.service import PredictionService


class TestWBCProfileLoader(unittest.TestCase):
    def test_loader_exposes_extended_wbc_profile_columns(self):
        loader = UnifiedDataLoader(AppConfig())
        df = loader.load_team_metrics().set_index("team")

        self.assertIn("runs_per_game", df.columns)
        self.assertIn("bullpen_era", df.columns)
        self.assertIn("roster_strength_index", df.columns)
        self.assertAlmostEqual(float(df.loc["PAN", "runs_per_game"]), 3.8, places=2)
        self.assertAlmostEqual(float(df.loc["CAN", "bullpen_era"]), 3.6, places=2)


class TestWBCLiveOddsAndMatchup(unittest.TestCase):
    def _make_service(self) -> PredictionService:
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        base = AppConfig()
        config = replace(
            base,
            sources=replace(
                base.sources,
                bankroll_storage_db=str(Path(td.name) / "bankroll.db"),
            ),
        )
        return PredictionService(config)

    def test_get_odds_rejects_seed_lines_for_live_predictions(self):
        svc = self._make_service()
        request = AnalyzeRequest(game_id="A06")
        matchup = Matchup(
            game_id="A06",
            tournament="WBC2026",
            game_time_utc="2026-03-09T00:00:00Z",
            home=TeamSnapshot("CAN", 1500, 0.32, 100, 3.8, 1.25, 100, 0.70, 8.0, 65),
            away=TeamSnapshot("PAN", 1500, 0.32, 100, 3.8, 1.25, 100, 0.70, 8.0, 65),
        )

        odds = svc._get_odds(request, matchup)

        self.assertEqual(odds, [])

    def test_build_matchup_hydrates_non_default_team_profile(self):
        svc = self._make_service()

        matchup = svc._build_matchup(AnalyzeRequest(game_id="A06"))

        self.assertAlmostEqual(matchup.home.runs_per_game, 4.8, places=2)
        self.assertAlmostEqual(matchup.away.runs_per_game, 3.8, places=2)
        self.assertEqual(matchup.home.sample_size, 152)
        self.assertAlmostEqual(matchup.away.roster_strength_index, 60.0, places=2)
        self.assertGreater(len(matchup.home_bullpen), 0)
        self.assertGreater(len(matchup.away_bullpen), 0)


class TestMarketFallbackBehavior(unittest.TestCase):
    def test_market_adjustment_leaves_model_prob_when_no_matching_odds(self):
        result = market_adjustment(0.6123, [], "CAN", "PAN")

        self.assertAlmostEqual(result["adjusted_home_prob"], 0.6123, places=4)
        self.assertAlmostEqual(result["market_implied_home"], 0.6123, places=4)
        self.assertEqual(result["market_weight_applied"], 0.0)
        self.assertEqual(result["model_weight_applied"], 1.0)


if __name__ == "__main__":
    unittest.main()
