"""
Enhanced Prediction Pipeline Service — Full Orchestration

Ties together:
  1. Data validation
  2. Feature engineering
  3. Model ensemble prediction
  4. Monte Carlo simulation
  5. Market calibration
  6. Bet optimization
  7. Institutional decision engine (7-phase intelligence)
  8. Portfolio optimization (CVaR / correlation-adjusted Kelly)
  9. Calibration monitoring (Brier / ECE / drift)
  10. Report generation
"""
from __future__ import annotations

from dataclasses import replace
import logging
from typing import cast

from wbc_backend.betting.market import market_adjustment
from wbc_backend.betting.optimizer import build_true_probs, find_top_bets
from wbc_backend.betting.portfolio_risk import (
    BetProposal,
    PortfolioRiskManager,
    compute_risk_of_ruin,
)
from wbc_backend.betting.bankroll_storage_v3 import BankrollStorageV3
from wbc_backend.betting.risk_control import BankrollState, update_bankroll
from wbc_backend.config.settings import AppConfig
from wbc_backend.data.validator import auto_fetch_missing_data, validate_dataset
from wbc_backend.data.wbc_verification import (
    WBCDataVerificationError,
    WBCAuthoritativeSnapshot,
    hydrate_matchup_from_snapshot,
    verify_game_artifact,
    verify_matchup,
)
from wbc_backend.domain.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BetRecommendation,
    GameOutput,
    Matchup,
    OddsLine,
    PitcherSnapshot,
    PredictionResult,
    TeamSnapshot,
)
from wbc_backend.features.advanced import build_advanced_features
from wbc_backend.optimization.continuous_learning import ContinuousLearningSystem
from wbc_backend.intelligence.decision_engine import (
    InstitutionalDecisionEngine,
    DecisionReport,
)
from wbc_backend.models.ensemble import predict_matchup
from wbc_backend.models.dynamic_ensemble import record_outcome as record_ensemble_outcome
from wbc_backend.pipeline.wbc_rule_engine import apply_wbc_rules
from wbc_backend.pipeline.deployment_gate import (
    evaluate_deployment_gate,
)
from wbc_backend.reporting.prediction_registry import append_prediction_record
from wbc_backend.reporting.renderers import render_full_report, render_json
from wbc_backend.simulation.monte_carlo import run_monte_carlo

logger = logging.getLogger(__name__)


def _normalize_player_name(name: str) -> str:
    return "".join(ch for ch in str(name).lower() if ch.isalnum())


class PredictionService:
    """
    Main prediction service — zero-intervention automated pipeline.

    Call flow:
      1. validate data → auto-patch if needed
      2. load matchup data
      3. run ensemble prediction
      4. apply WBC rules
      5. run Monte Carlo simulation (50K+)
      6. market calibration
      7. find top 3 bets
      8. institutional decision engine (7-phase gate)
      9. portfolio optimization (CVaR)
      10. calibration monitoring
      11. generate report
    """

    def __init__(self, config: AppConfig | None = None):
        self.config = config or AppConfig()
        self.bankroll_storage = BankrollStorageV3(
            self.config.sources.bankroll_storage_db,
        )
        self.bankroll = self.bankroll_storage.load()
        if self.bankroll.initial <= 0:
            self.bankroll = BankrollState(
                initial=self.config.bankroll.initial_bankroll,
                current=self.config.bankroll.initial_bankroll,
                peak=self.config.bankroll.initial_bankroll,
                daily_start=self.config.bankroll.initial_bankroll,
            )
            self.bankroll_storage.save(self.bankroll)
        # Institutional Decision Engine
        self.decision_engine = InstitutionalDecisionEngine(
            bankroll=self.bankroll.current,
        )
        self.portfolio_risk = PortfolioRiskManager(initial_bankroll=self.bankroll.current)
        self.continuous_learning = ContinuousLearningSystem()
        # Calibration tracking
        self._prob_history: list[float] = []
        self._outcome_history: list[int] = []
        self._last_sub_model_results = []
        self._last_tournament = "WBC"
        self._last_round_name = "Pool"

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Run the full prediction pipeline for a game."""
        logger.info("=" * 70)
        logger.info("🎯 ANALYZING GAME: %s", request.game_id)
        logger.info("=" * 70)

        # ── 1. Data Validation ───────────────────────────
        logger.info("[STEP 1] Validating data completeness...")
        validation = validate_dataset("MLB_2025", self.config)
        if not validation.is_valid:
            logger.info("[STEP 1] Data incomplete (%.1f%%), auto-fetching...",
                       validation.completeness_pct * 100)
            validation = auto_fetch_missing_data("MLB_2025", self.config)
        logger.info("[STEP 1] Data validation: completeness=%.1f%%, valid=%s",
                   validation.completeness_pct * 100, validation.is_valid)

        logger.info("[STEP 1B] Evaluating deployment gate...")
        deployment_gate = evaluate_deployment_gate(self.config)
        deployment_gate.ensure_ready()
        logger.info(
            "[STEP 1B] Deployment gate ready: calibration=%s, wf_brier=%.4f",
            deployment_gate.selected_calibration,
            float(deployment_gate.walkforward_summary.get("brier", 0.0)),
        )

        # ── 2. Build Matchup ─────────────────────────────
        logger.info("[STEP 2] Building matchup data...")
        matchup = self._build_matchup(request)
        verification = verify_matchup(
            matchup,
            self.config.sources.wbc_authoritative_snapshot_json,
        )
        verification.ensure_verified()
        logger.info(
            "[STEP 2] WBC data verified: %s (warnings=%d)",
            verification.canonical_game_id or matchup.game_id,
            sum(1 for issue in verification.issues if issue.severity != "ERROR"),
        )

        # ── 3. Advanced Features ─────────────────────────
        logger.info("[STEP 3] Computing advanced features...")
        adv_features = build_advanced_features(matchup)
        logger.info("[STEP 3] Features: fatigue_diff=%.3f, matchup_diff=%.3f, "
                   "bullpen_stress_diff=%.3f, clutch_diff=%.3f",
                   adv_features.feature_dict.get("sp_fatigue_diff", 0),
                   adv_features.feature_dict.get("matchup_edge_diff", 0),
                   adv_features.feature_dict.get("bullpen_stress_diff", 0),
                   adv_features.feature_dict.get("clutch_diff", 0))

        # ── 4. Ensemble Prediction ───────────────────────
        logger.info("[STEP 4] Running hybrid ensemble prediction...")
        pred = predict_matchup(matchup, self.config.model)
        if verification.used_fallback_lineup:
            pred.confidence_score *= 0.85
            pred.x_factors.append("Previous-game lineup fallback applied")
        logger.info("[STEP 4] Raw prediction: home=%.3f, away=%.3f, "
                   "score=%s %.1f - %s %.1f",
                   pred.home_win_prob, pred.away_win_prob,
                   matchup.home.team, pred.expected_home_runs,
                   matchup.away.team, pred.expected_away_runs)
        self._last_sub_model_results = list(pred.sub_model_results or [])
        self._last_tournament = matchup.tournament
        self._last_round_name = matchup.round_name

        # ── 5. WBC Rules ─────────────────────────────────
        if matchup.tournament.upper().startswith("WBC"):
            logger.info("[STEP 5] Applying WBC rule adjustments...")
            pred, notes, _ = apply_wbc_rules(matchup, pred)
            for note in notes:
                logger.info("[STEP 5] %s", note)

        # ── 6. Monte Carlo (50K) ─────────────────────────
        logger.info("[STEP 6] Running Monte Carlo simulation (%d sims)...",
                   self.config.model.mc_simulations)
        sim = run_monte_carlo(
            pred,
            line_total=request.line_total,
            line_spread_home=request.line_spread_home,
            simulations=self.config.model.mc_simulations,
            home_sp_fatigue=adv_features.home_sp_fatigue,
            away_sp_fatigue=adv_features.away_sp_fatigue,
            home_bullpen_stress=adv_features.home_bullpen_stress,
            away_bullpen_stress=adv_features.away_bullpen_stress,
        )
        logger.info("[STEP 6] MC result: home_wp=%.3f, over=%.3f, "
                   "mean_total=%.1f, odd=%.3f",
                   sim.home_win_prob, sim.over_prob,
                   sim.mean_total_runs, sim.odd_prob)

        # ── 7. Market Calibration ────────────────────────
        logger.info("[STEP 7] Running market calibration...")
        odds_lines = self._get_odds(request, matchup)
        if not odds_lines:
            pred.x_factors.append("No verified live odds available; market calibration skipped")
        market_result = market_adjustment(
            pred.home_win_prob,
            odds_lines,
            matchup.home.team,
            matchup.away.team,
            self.config.market,
        )
        adjusted_home_prob = market_result["adjusted_home_prob"]
        pred.market_bias_score = market_result["market_bias_score"]
        logger.info("[STEP 7] Market: model=%.3f → adjusted=%.3f, bias=%.3f, steams=%d",
                   pred.home_win_prob, adjusted_home_prob,
                   pred.market_bias_score, market_result["n_steam_moves"])

        # ── 8. Build true probabilities ──────────────────
        true_probs = build_true_probs(
            matchup.home.team, matchup.away.team,
            adjusted_home_prob, sim,
        )

        # ── 9. Find Top 3 Bets ──────────────────────────
        logger.info("[STEP 8] Finding top EV bets...")
        top_bets = find_top_bets(
            odds_lines, true_probs,
            matchup.home.team, matchup.away.team,
            pred.confidence_score, self.config, self.bankroll,
        )

        # ── 10. Institutional Decision Engine (7-Phase) ──
        logger.info("[STEP 9] Running institutional decision engine...")
        decision_rpt = self._run_decision_engine(
            matchup, pred, adjusted_home_prob, odds_lines,
        )
        logger.info("[STEP 9] Decision: %s (%s) — edge=%.1f, regime=%s",
                   decision_rpt.decision, decision_rpt.confidence,
                   decision_rpt.edge_score, decision_rpt.market_regime)

        # ── 11. Portfolio Optimization ───────────────────
        logger.info("[STEP 10] Running portfolio optimization...")
        portfolio_metrics = self._run_portfolio_optimization(top_bets, decision_rpt, matchup)
        logger.info("[STEP 10] Portfolio: survival=%.1f%%, cvar=%.4f",
                   portfolio_metrics.get("survival_prob", 0) * 100,
                   portfolio_metrics.get("cvar_95", 0))

        # ── 12. Calibration Monitoring ───────────────────
        logger.info("[STEP 11] Calibration monitoring...")
        self._prob_history.append(adjusted_home_prob)
        calibration_metrics = self._run_calibration_monitoring()
        if calibration_metrics:
            logger.info("[STEP 11] Brier=%.4f, ECE=%.4f, drift=%s",
                       calibration_metrics.get("brier", 0),
                       calibration_metrics.get("ece", 0),
                       "YES" if calibration_metrics.get("drift_flag", 0) > 0 else "no")

        # ── 10. Build GameOutput ─────────────────────────
        best_bet_desc = ""
        best_ev = 0.0
        if top_bets:
            best = top_bets[0]
            best_bet_desc = f"{best.market} {best.side}"
            if best.line is not None:
                best_bet_desc += f" ({best.line:+.1f})"
            best_bet_desc += f" @ {best.sportsbook}"
            best_ev = best.ev

        display_home_score, display_away_score, reconciled = self._resolve_display_scores(
            raw_home_runs=pred.expected_home_runs,
            raw_away_runs=pred.expected_away_runs,
            mean_total_runs=sim.mean_total_runs,
            final_home_prob=adjusted_home_prob,
        )
        if reconciled:
            pred.x_factors.append("Display score reconciled to final win-probability direction")

        game_output = GameOutput(
            game_id=request.game_id,
            home_team=matchup.home.team,
            away_team=matchup.away.team,
            home_win_prob=round(adjusted_home_prob, 4),
            away_win_prob=round(1 - adjusted_home_prob, 4),
            predicted_home_score=display_home_score,
            predicted_away_score=display_away_score,
            market_bias_score=pred.market_bias_score,
            ev_best=round(best_ev, 4),
            best_bet_strategy=best_bet_desc,
            confidence_index=pred.confidence_score,
            top_3_bets=top_bets,
        )

        # ── 13. Generate Reports ─────────────────────────
        markdown = render_full_report(
            game_output, pred, sim, market_result, adv_features,
            decision_report=decision_rpt,
            calibration_metrics=calibration_metrics,
            portfolio_metrics=portfolio_metrics,
        )
        json_report = render_json(
            game_output, pred, sim, market_result,
            decision_report=decision_rpt,
            calibration_metrics=calibration_metrics,
            portfolio_metrics=portfolio_metrics,
        )

        logger.info("=" * 70)
        logger.info("✅ ANALYSIS COMPLETE: %s", request.game_id)
        logger.info("=" * 70)

        append_prediction_record(
            config=self.config,
            request=request,
            matchup=matchup,
            verification=verification,
            deployment_gate=deployment_gate,
            game_output=game_output,
            pred=pred,
            sim=sim,
            top_bets=top_bets,
            decision_report=decision_rpt,
            calibration_metrics=calibration_metrics,
            portfolio_metrics=portfolio_metrics,
        )

        return AnalyzeResponse(
            game_output=game_output,
            markdown_report=markdown,
            json_report=json_report,
            decision_report=decision_rpt,
            calibration_metrics=calibration_metrics,
            portfolio_metrics=portfolio_metrics,
            deployment_gate_report=deployment_gate.to_dict(),
        )

    @staticmethod
    def _resolve_display_scores(
        raw_home_runs: float,
        raw_away_runs: float,
        mean_total_runs: float,
        final_home_prob: float,
    ) -> tuple[float, float, bool]:
        raw_diff = raw_home_runs - raw_away_runs
        final_diff = (final_home_prob * 2.0) - 1.0
        total = mean_total_runs if mean_total_runs > 0 else max(0.0, raw_home_runs + raw_away_runs)

        if raw_diff == 0 or final_diff == 0 or raw_diff * final_diff >= 0:
            return round(raw_home_runs, 2), round(raw_away_runs, 2), False

        home_runs = max(0.0, total * final_home_prob)
        away_runs = max(0.0, total - home_runs)
        return round(home_runs, 2), round(away_runs, 2), True

    def _build_matchup(self, request: AnalyzeRequest) -> Matchup:  # NOSONAR  # noqa: C901
        """
        Build a Matchup from the request.

        WBC schedule / starters / lineups are sourced from the authoritative
        local snapshot. If the game is missing or not verified there, analysis
        must stop.
        """
        from wbc_backend.ingestion.providers import WBCDataProvider

        provider = WBCDataProvider(self.config)
        schedule_df = provider.load_wbc_2026_live()
        snapshot_repo = WBCAuthoritativeSnapshot(
            self.config.sources.wbc_authoritative_snapshot_json,
        )
        snapshot_game = snapshot_repo.find_game(request.game_id)
        precheck = verify_game_artifact(
            game_id=request.game_id,
            expected_home=None,
            expected_away=None,
            expected_game_time=None,
            expected_home_sp=None,
            expected_away_sp=None,
            expected_home_lineup=None,
            expected_away_lineup=None,
            snapshot_path=self.config.sources.wbc_authoritative_snapshot_json,
        )
        if precheck.blocking and not precheck.used_fallback_lineup:
            precheck.ensure_verified()
        elif precheck.blocking:
            issue_summary = "; ".join(issue.message for issue in precheck.issues) or "fallback verification warning"
            logger.warning(
                "Proceeding with fallback authoritative snapshot for %s: %s",
                request.game_id,
                issue_summary,
            )

        # Find the game
        row = None
        for _, r in schedule_df.iterrows():
            aliases = {
                str(r.get("game_id", "")).upper(),
                *[part.strip().upper() for part in str(r.get("aliases", "")).split(",") if part.strip()],
            }
            if request.game_id.upper() in aliases:
                row = r
                break

        if row is None:
            raise WBCDataVerificationError(precheck)

        # Build team snapshots from provider data
        from wbc_backend.ingestion.unified_loader import UnifiedDataLoader
        from wbc_backend.cleaning.preprocess import clean_team_metrics
        loader = UnifiedDataLoader(self.config)

        try:
            metrics = clean_team_metrics(loader.load_team_metrics())
            lookup = metrics.set_index("team")
            pitcher_profiles = loader.load_wbc_pitcher_profiles()

            home_code = row["home"]
            away_code = row["away"]

            def _coalesce(primary, fallback, default):
                for value in (primary, fallback):
                    if value is None:
                        continue
                    if value != value:
                        continue
                    return value
                return default

            def _team(code, row_data, prefix):
                if code in lookup.index:
                    m = lookup.loc[code]
                    return TeamSnapshot(
                        team=code,
                        elo=float(_coalesce(m.get("elo"), None, 1500.0)),
                        batting_woba=float(_coalesce(m.get("woba"), None, 0.320)),
                        batting_ops_plus=float(_coalesce(m.get("ops_plus"), None, 100.0)),
                        pitching_fip=float(_coalesce(m.get("fip"), None, 3.80)),
                        pitching_whip=float(_coalesce(m.get("whip"), None, 1.25)),
                        pitching_stuff_plus=float(_coalesce(m.get("stuff_plus"), None, 100.0)),
                        der=float(_coalesce(m.get("der"), None, 0.700)),
                        bullpen_depth=float(_coalesce(m.get("bullpen_depth"), None, 8.0)),
                        pitch_limit=int(_coalesce(row_data.get(f"{prefix}_pitch_limit"), None, 65)),
                        bullpen_era=float(_coalesce(m.get("bullpen_era"), row_data.get(f"{prefix}_bullpen_era"), 3.50)),
                        bullpen_pitches_3d=int(_coalesce(m.get("bullpen_pitches_3d"), row_data.get(f"{prefix}_bullpen_pitches_3d"), 0)),
                        runs_per_game=float(_coalesce(m.get("runs_per_game"), row_data.get(f"{prefix}_runs_per_game"), 4.5)),
                        runs_allowed_per_game=float(_coalesce(m.get("runs_allowed_per_game"), row_data.get(f"{prefix}_runs_allowed_per_game"), 4.5)),
                        clutch_woba=float(_coalesce(m.get("clutch_woba"), row_data.get(f"{prefix}_clutch_woba"), 0.320)),
                        roster_strength_index=float(_coalesce(m.get("roster_strength_index"), row_data.get(f"{prefix}_roster_strength_index"), 80.0)),
                        missing_core_batter=bool(_coalesce(row_data.get(f"{prefix}_missing_core_batter"), None, False)),
                        ace_pitch_count_limited=bool(_coalesce(row_data.get(f"{prefix}_ace_limited"), None, False)),
                        top50_stars=int(_coalesce(m.get("top50_stars"), row_data.get(f"{prefix}_top50_stars"), 0)),
                        sample_size=int(_coalesce(m.get("sample_size"), row_data.get(f"{prefix}_sample_size"), 120)),
                        league_prior_strength=float(_coalesce(m.get("league_prior_strength"), row_data.get(f"{prefix}_league_prior_strength"), 0.0)),
                        win_pct_last_10=float(_coalesce(m.get("win_pct_last_10"), row_data.get(f"{prefix}_win_pct_last_10"), 0.5)),
                        rest_days=int(_coalesce(m.get("rest_days"), row_data.get(f"{prefix}_rest_days"), 1)),
                    )
                else:
                    return TeamSnapshot(
                        team=code, elo=1500, batting_woba=0.320,
                        batting_ops_plus=100, pitching_fip=3.80,
                        pitching_whip=1.25, pitching_stuff_plus=100,
                        der=0.700, bullpen_depth=8.0, pitch_limit=65,
                    )

            matchup = Matchup(
                game_id=row["game_id"],
                tournament=row.get("tournament", "WBC2026"),
                game_time_utc=row["game_time_utc"],
                home=_team(home_code, row, "home"),
                away=_team(away_code, row, "away"),
                venue=str(row.get("venue", "")),
                round_name=str(row.get("round_name", "Pool")),
                neutral_site=bool(row.get("neutral_site", True)),
                weather=str(row.get("weather", "dome")),
                umpire_id=str(row.get("umpire_id", "generic_avg")),
                elevation_m=float(row.get("elevation_m", 0.0)),
                temp_f=float(row.get("temp_f", 72.0)),
                humidity_pct=float(row.get("humidity_pct", 0.50)),
                wind_speed_mph=float(row.get("wind_speed_mph", 0.0)),
                wind_direction=str(row.get("wind_direction", "none")),
                is_dome=bool(row.get("is_dome", False)),
            )
            matchup = hydrate_matchup_from_snapshot(matchup, snapshot_game or {})
            matchup.home_sp = self._enrich_pitcher_snapshot(matchup.home_sp, matchup.home.team, pitcher_profiles)
            matchup.away_sp = self._enrich_pitcher_snapshot(matchup.away_sp, matchup.away.team, pitcher_profiles)
            matchup.home_bullpen = self._build_bullpen(matchup.home.team, matchup.home_sp, pitcher_profiles)
            matchup.away_bullpen = self._build_bullpen(matchup.away.team, matchup.away_sp, pitcher_profiles)
            return matchup

        except Exception as e:
            logger.error("Failed to build verified matchup for %s: %s", request.game_id, e)
            raise

    def _get_odds(self, request: AnalyzeRequest, matchup: Matchup) -> list[OddsLine]:
        """Get odds lines for the matchup."""
        from wbc_backend.ingestion.unified_loader import UnifiedDataLoader

        loader = UnifiedDataLoader(self.config)
        odds_map = loader.load_wbc_seed_odds()
        for key in (matchup.game_id, request.game_id, str(request.game_id).upper(), str(matchup.game_id).upper()):
            if key in odds_map:
                lines = list(odds_map[key])
                if self.config.sources.allow_seed_odds_for_live_predictions:
                    return lines
                non_seed = [line for line in lines if line.source_type != "seed"]
                if not non_seed and lines:
                    logger.warning(
                        "Ignoring %d seed odds lines for %s; live predictions require real market data",
                        len(lines),
                        key,
                    )
                return non_seed
        return []

    @staticmethod
    def _profile_to_pitcher(profile: dict[str, float]) -> PitcherSnapshot:
        return PitcherSnapshot(
            name=str(profile["name"]),
            team=str(profile.get("team", "")),
            era=float(profile.get("era", 3.80)),
            fip=float(profile.get("fip", 3.90)),
            whip=float(profile.get("whip", 1.25)),
            k_per_9=float(profile.get("k_per_9", 8.5)),
            bb_per_9=float(profile.get("bb_per_9", 3.0)),
            stuff_plus=float(profile.get("stuff_plus", 100.0)),
            ip_last_30=float(profile.get("ip_last_30", 20.0)),
            era_last_3=float(profile.get("era_last_3", profile.get("era", 3.80))),
            pitch_count_last_3d=int(profile.get("pitch_count_last_3d", 0)),
            fastball_velo=float(profile.get("fastball_velo", 93.0)),
            high_leverage_era=float(profile.get("high_leverage_era", profile.get("era", 3.80))),
            role=str(profile.get("role", "SP")),
            pitch_mix=dict(profile.get("pitch_mix", {}) or {}),
            recent_fastball_velos=[float(v) for v in profile.get("recent_fastball_velos", []) or []],
            career_fastball_velo=float(profile.get("career_fastball_velo", profile.get("fastball_velo", 93.0))),
            woba_vs_left=float(profile.get("woba_vs_left", 0.320)),
            woba_vs_right=float(profile.get("woba_vs_right", 0.320)),
            innings_last_14d=float(profile.get("innings_last_14d", 0.0)),
            season_avg_innings_per_14d=float(profile.get("season_avg_innings_per_14d", 0.0)),
            recent_spin_rate=float(profile.get("recent_spin_rate", 0.0)),
            career_spin_rate_mean=float(profile.get("career_spin_rate_mean", 0.0)),
            career_spin_rate_std=float(profile.get("career_spin_rate_std", 0.0)),
        )

    def _enrich_pitcher_snapshot(
        self,
        pitcher: PitcherSnapshot | None,
        team_code: str,
        pitcher_profiles: dict[str, dict[str, dict[str, float]]],
    ) -> PitcherSnapshot | None:
        if pitcher is None:
            return None
        team_profiles = pitcher_profiles.get(team_code, {})
        profile = team_profiles.get(_normalize_player_name(pitcher.name))
        if not profile:
            return pitcher
        enriched = self._profile_to_pitcher(profile)
        return cast(
            PitcherSnapshot,
            replace(enriched, name=pitcher.name, team=team_code, role=pitcher.role or enriched.role),
        )

    def _build_bullpen(
        self,
        team_code: str,
        starter: PitcherSnapshot | None,
        pitcher_profiles: dict[str, dict[str, dict[str, float]]],
    ) -> list[PitcherSnapshot]:
        team_profiles = pitcher_profiles.get(team_code, {})
        starter_name = _normalize_player_name(starter.name) if starter else ""
        relievers = []
        fallback = []
        for name_key, profile in team_profiles.items():
            if name_key == starter_name:
                continue
            pitcher = self._profile_to_pitcher(profile)
            if pitcher.role in {"RP", "PB"}:
                relievers.append(pitcher)
            else:
                fallback.append(pitcher)
        return relievers or fallback

    # ── Institutional Intelligence Integration ───────────────────────────

    def _run_decision_engine(  # NOSONAR
        self,
        matchup: Matchup,
        pred: PredictionResult,
        adjusted_home_prob: float,
        odds_lines: list[OddsLine],
    ) -> DecisionReport:
        """Run the 7-phase institutional decision engine."""
        # Extract sub-model probabilities from diagnostics
        sub_model_probs: dict[str, float] = {}
        if pred.sub_model_results:
            for sr in pred.sub_model_results:
                sub_model_probs[sr.model_name] = sr.home_win_prob

        # Find ML odds
        odds_home = 2.0
        odds_away = 1.85
        for o in odds_lines:
            if o.market == "ML":
                if o.side == matchup.home.team or o.side == "HOME":
                    odds_home = o.decimal_odds
                elif o.side == matchup.away.team or o.side == "AWAY":
                    odds_away = o.decimal_odds

        # Extract calibration params from diagnostics
        brier = pred.diagnostics.get("brier_score", 0.25) if pred.diagnostics else 0.25
        platt_a = pred.diagnostics.get("platt_a", 1.0) if pred.diagnostics else 1.0
        platt_b = pred.diagnostics.get("platt_b", 0.0) if pred.diagnostics else 0.0

        league = "WBC" if matchup.tournament.upper().startswith("WBC") else "MLB"

        report = self.decision_engine.analyze_match(
            match_id=matchup.game_id,
            match_label=f"{matchup.away.team} @ {matchup.home.team}",
            sub_model_probs=sub_model_probs,
            calibrated_prob=adjusted_home_prob,
            odds_home=odds_home,
            odds_away=odds_away,
            brier_score=brier,
            platt_a=platt_a,
            platt_b=platt_b,
            league=league,
        )
        return report

    def _run_portfolio_optimization(
        self,
        top_bets: list[BetRecommendation],
        decision_rpt: DecisionReport,
        matchup: Matchup | None = None,
    ) -> dict[str, float]:
        """Run portfolio-level risk optimization via Phase 7 portfolio_risk engine."""
        if not top_bets:
            return {"survival_prob": 1.0, "cvar_95": 0.0, "drawdown_scale": 1.0}

        # Keep portfolio risk state aligned with runtime bankroll snapshot.
        self.portfolio_risk.state.bankroll = float(self.bankroll.current)
        self.portfolio_risk.state.peak_bankroll = float(self.bankroll.peak)

        tournament = matchup.tournament if matchup else "WBC"
        round_name = matchup.round_name if matchup else "Pool"
        game_date = ""
        if matchup and getattr(matchup, "game_time_utc", ""):
            game_date = str(matchup.game_time_utc)[:10]

        proposals: list[BetProposal] = []
        for b in top_bets:
            proposals.append(BetProposal(
                game_id=f"{b.market}:{b.side}",
                market=b.market,
                side=b.side,
                win_prob=float(b.win_probability),
                odds=2.0 if b.implied_probability <= 0 else float(1.0 / b.implied_probability),
                ev=float(b.ev),
                edge=float(b.edge),
                individual_kelly=float(max(0.0, b.kelly_fraction)),
                confidence=float(b.confidence),
                tournament=tournament,
                game_date=game_date,
                group=round_name,
            ))

        sizing = self.portfolio_risk.size_portfolio(proposals)
        avg_stake = float(sum(p.stake_fraction for p in sizing.positions) / max(1, len(sizing.positions)))
        avg_prob = float(sum(p.bet.win_prob for p in sizing.positions) / max(1, len(sizing.positions)))
        avg_odds = float(sum(p.bet.odds for p in sizing.positions) / max(1, len(sizing.positions)))
        ruin_metrics = compute_risk_of_ruin(
            bankroll=self.portfolio_risk.state.bankroll,
            avg_bet_size=max(0.0001, avg_stake),
            win_rate=max(0.01, min(0.99, avg_prob)),
            avg_odds=max(1.01, avg_odds),
            ruin_threshold=0.10,
        )

        return {
            "survival_prob": round(max(0.0001, 1.0 - float(ruin_metrics.get("risk_of_ruin", 1.0))), 4),
            "cvar_95": round(-float(sizing.portfolio_variance), 6),
            "expected_return": round(float(sizing.expected_daily_return), 6),
            "gross_exposure": round(float(sizing.total_exposure), 4),
            "drawdown_scale": round(max(0.3, 1.0 - float(self.portfolio_risk.state.drawdown) * 2.0), 4),
            "current_drawdown": round(float(self.portfolio_risk.state.drawdown), 4),
            "decision_verdict": decision_rpt.decision,
            "edge_score": decision_rpt.edge_score,
            "risk_level": sizing.risk_level,
            "risk_of_ruin": float(ruin_metrics.get("risk_of_ruin", 1.0)),
        }

    def _run_calibration_monitoring(self) -> dict[str, float] | None:
        """Run calibration and drift detection on accumulated predictions."""
        if len(self._prob_history) < 10:
            return None

        from wbc_backend.research.infrastructure import (
            calibration_monitoring,
            drift_detection,
        )

        # Use stored outcomes (fill with 0.5-rounded proxy if no actuals yet)
        n = len(self._prob_history)
        if len(self._outcome_history) < n:
            # Pad with rounded probabilities as proxy until actuals arrive
            for i in range(len(self._outcome_history), n):
                self._outcome_history.append(int(self._prob_history[i] >= 0.5))

        cal = calibration_monitoring(self._prob_history, self._outcome_history)

        # Drift detection: compare first half vs second half
        drift_metrics: dict[str, float] = {}
        if n >= 20:
            mid = n // 2
            drift_metrics = drift_detection(
                self._prob_history[:mid],
                self._prob_history[mid:],
            )

        return {
            "brier": cal["brier"],
            "logloss": cal["logloss"],
            "ece": cal["ece"],
            "mce": cal["mce"],
            "n_predictions": float(n),
            **drift_metrics,
        }

    def record_outcome(  # NOSONAR
        self,
        actual_home_win: int,
        *,
        pnl: float = 0.0,
        stake: float = 0.0,
        game_id: str = "",
        market: str = "ML",
        side: str = "",
        odds: float = 0.0,
    ) -> None:
        """Record an actual game outcome for calibration tracking."""
        self._outcome_history.append(actual_home_win)

        if self._prob_history:
            try:
                cl_result = self.continuous_learning.process_game_result(
                    game_id=game_id or "unknown",
                    predicted_prob=float(self._prob_history[-1]),
                    actual_outcome=int(actual_home_win),
                    tournament="WBC",
                    round_name="Pool",
                    bet_pnl=float(pnl),
                )
                logger.info(
                    "[CONTINUOUS_LEARNING] game=%s status=%s actions=%s",
                    game_id or "unknown",
                    cl_result.get("system_status", "UNKNOWN"),
                    ",".join(cl_result.get("actions", [])) or "none",
                )
            except Exception as exc:
                logger.warning("Continuous learning update failed: %s", exc)

        # Update dynamic ensemble weights only after actual outcome is known.
        if game_id and self._prob_history:
            try:
                if self._last_sub_model_results:
                    record_ensemble_outcome(
                        sub_results=self._last_sub_model_results,
                        actual_home_win=int(actual_home_win),
                        tournament=self._last_tournament,
                        round_name=self._last_round_name,
                    )
            except Exception as exc:
                logger.warning("Dynamic ensemble outcome update failed: %s", exc)

        has_financial_update = stake > 0 or abs(pnl) > 1e-12
        if has_financial_update:
            update_bankroll(self.bankroll, pnl=pnl, stake=stake)
            if hasattr(self.decision_engine, "risk") and hasattr(self.decision_engine.risk, "state"):
                self.decision_engine.risk.state.current_bankroll = self.bankroll.current
                self.decision_engine.risk.state.peak_bankroll = max(
                    getattr(self.decision_engine.risk.state, "peak_bankroll", self.bankroll.peak),
                    self.bankroll.peak,
                )
            self.bankroll_storage.save(self.bankroll)
            if game_id:
                self.bankroll_storage.record_bet(
                    game_id=game_id,
                    market=market,
                    side=side,
                    odds=odds,
                    stake_pct=(stake / self.bankroll.current) if self.bankroll.current > 0 else 0.0,
                    stake_amount=stake,
                    pnl=pnl,
                    won=pnl >= 0,
                    bankroll_after=self.bankroll.current,
                    metadata={"actual_home_win": actual_home_win},
                )

        if has_financial_update:
            try:
                self.portfolio_risk.record_outcome(
                    game_id=game_id or "unknown",
                    pnl=float(pnl),
                    stake_amount=float(stake),
                )
            except Exception as exc:
                logger.warning("Portfolio risk outcome update failed: %s", exc)
