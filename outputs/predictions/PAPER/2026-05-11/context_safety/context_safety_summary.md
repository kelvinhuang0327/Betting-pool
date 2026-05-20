# P12 Context Safety Audit Summary

Generated: 2026-05-11T07:01:51.056493+00:00

## Overall Statistics

| Metric | Count |
|--------|-------|
| Total files audited | 234 |
| PREGAME_SAFE | 109 |
| POSTGAME_RISK | 76 |
| UNKNOWN | 49 |
| Usable (safe) | 109 |
| Unsafe | 76 |

## Safety Recommendation

CAUTION: 76 file(s) have postgame leakage risk. Exclude from pregame feature pipeline. Risky files: ['data/derived/odds_snapshots_2026-04-29.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase48_p0_v1.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase50_p0_injected_v1.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase52_sp_context_v1.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase52_sp_injected_v1.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase54_sp_safe_coeff_v1.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl', 'data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_injected_v1.jsonl', 'data/wbc_backend/reports/performance_monitor.jsonl', 'data/wbc_backend/reports/postgame_results.jsonl', 'data/wbc_backend/reports/prediction_registry.jsonl', 'data/wbc_backend/reports/prediction_registry_replay.jsonl', 'data/mlb_2025/mlb-2025-asplayed.csv', 'data/derived/manifest_dry_run_summary_2026-04-29.json', 'data/derived/model_output_contract_validation_summary_2026-04-29.json', 'data/derived/model_output_contract_validation_summary_6q_2026-04-30.json', 'data/derived/model_output_contract_validation_summary_6r_2026-04-30.json', 'data/derived/model_output_contract_validation_summary_6s_2026-04-30.json', 'data/fixtures/mlb_current_source_sample_20260507.json', 'data/wbc_backend/artifacts/continuous_learning_state.json', 'data/wbc_backend/artifacts/improvement_log.json', 'data/wbc_backend/artifacts/retrainer_state.json', 'data/wbc_backend/artifacts/v3_research_cycle.json', 'data/wbc_backend/market_validation.json', 'data/wbc_backend/portfolio_risk.json', 'data/wbc_backend/reports/clv_validation_records_6u_summary_2026-04-30.json', 'data/wbc_backend/reports/market_support_performance_summary.json', 'data/wbc_backend/reports/mlb_alpha_discovery_report.json', 'data/wbc_backend/reports/mlb_alpha_discovery_report_test.json', 'data/wbc_backend/reports/mlb_alpha_discovery_report_test_blocked.json', 'data/wbc_backend/reports/mlb_decision_optimization_report.json', 'data/wbc_backend/reports/mlb_model_rebuild_report.json', 'data/wbc_backend/reports/mlb_regime_feature_redesign_report.json', 'data/wbc_backend/reports/mlb_regime_paper_report.json', 'data/wbc_backend/reports/optimization_readiness_latest.json', 'data/wbc_backend/tune_results_top10.json', 'data/wbc_backend/walkforward_summary.json', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_73855ccb.jsonl', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_calibrated_candidate_d5fb827f.jsonl', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_f8695fec.jsonl', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_oof_calibrated_ed059d96.jsonl', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p10_feature_candidat_edaddde1.jsonl', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl', 'outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p9_repaired_oof_663d9bc7.jsonl', 'outputs/predictions/PAPER/__pytest_p8_deep_diag__/bad_source.csv', 'outputs/predictions/PAPER/__pytest_p8_deep_diag__/oof_model.csv', 'outputs/predictions/PAPER/__pytest_p8_deep_diag__/raw_model.csv', 'outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_oof.json', 'outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_raw.json', 'outputs/predictions/PAPER/2026-05-11/model_probability_audit.json', 'outputs/predictions/PAPER/__pytest_p8_deep_diag__/model_deep_diagnostics_oof.json', 'outputs/predictions/PAPER/__pytest_p8_deep_diag__/model_deep_diagnostics_raw.json', 'outputs/replay/replay_default_validation_ci_verification_report.json', 'reports/mlb_paper_betting_ledger.jsonl', 'reports/mlb_paper_betting_reviewed_snapshot_20250701.jsonl', 'reports/mlb_paper_betting_reviewed_snapshot_20260507.jsonl', 'reports/metrics_ssot_phase67_72_inventory_20260507.json', 'reports/mlb_current_source_probe_20260507.json', 'reports/mlb_daily_advisory_dry_run_20250701.json', 'reports/mlb_daily_advisory_dry_run_20260507.json', 'reports/mlb_daily_scheduler_manifest_20250701.json', 'reports/mlb_daily_scheduler_manifest_20260507.json', 'reports/mlb_live_source_plan_20260507.json', 'reports/mlb_postgame_review_20250701.json', 'reports/mlb_postgame_review_20260507.json', 'reports/phase53_sp_coefficient_calibration_2026-05-05.json', 'reports/phase55_sp_vs_bullpen_diagnosis_2026-05-05.json', 'reports/phase59_real_bullpen_boxscore_acquisition_20260506.json', 'reports/phase64_granular_bullpen_attribution_20260506.json', 'reports/phase64b_full_season_bullpen_ingestion_and_attribution_20260506.json', 'reports/phase65_sp_fatigue_attribution_20260506.json', 'reports/phase66_market_microstructure_failure_attribution_20260506.json', 'reports/phase67_context_failure_attribution_20260506.json', 'reports/phase68_model_architecture_ensemble_failure_audit_20260506.json', 'reports/phase71_market_dominance_model_derisk_audit_20260507.json']

## Per-File Audit

| File | Type | Rows | Status | Reasons |
|------|------|------|--------|---------|
| tsl_odds_history.jsonl | jsonl | 2001 | UNKNOWN | no_clear_temporal_keywords |
| team_alias_map_2026-04-29.csv | csv | 66 | UNKNOWN | no_clear_temporal_keywords |
| 2026-03-14_KOR_DOM_poisson_matrix.csv | csv | 13 | UNKNOWN | no_clear_temporal_keywords |
| 2026-03-14_USA_CAN_poisson_matrix.csv | csv | 13 | UNKNOWN | no_clear_temporal_keywords |
| 2026-03-15_PUR_ITA_poisson_matrix.csv | csv | 13 | UNKNOWN | no_clear_temporal_keywords |
| 2026-03-15_VEN_JPN_poisson_matrix.csv | csv | 13 | UNKNOWN | no_clear_temporal_keywords |
| test_cache_key_123.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| test_expired_key.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| tsl_dedup_state.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| prediction_timestamp_evidence_summary_2026-04-29.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| learning_state.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| mlb-2025-asplayed.csv.metadata.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| mlb_odds_2025_real.csv.metadata.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| odds_capture_schedule.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| tsl_fetch_status.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| tsl_frontend_probe.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| tsl_odds_snapshot.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| wbc_2026_authoritative_snapshot.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| wbc_2026_live_scores.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| wbc_all_players_realtime.json | json_array | 21 | UNKNOWN | no_clear_temporal_keywords |
| clv_activation_preview_2026-05-01.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| gate_blend_search.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| gate_coverage_gaps.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| mlb_odds_source_audit.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| prediction_registry_6t_summary_2026-04-30.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| wbc_hitting_stats_2026.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| wbc_pitching_stats_2026.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| wbc_players_2025_stats.json | json_array | 20 | UNKNOWN | no_clear_temporal_keywords |
| wbc_players_2026.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| mlb_feature_candidate_probabilities.jsonl | jsonl | 2402 | UNKNOWN | no_clear_temporal_keywords |
| mlb_feature_candidate_probabilities.jsonl | jsonl | 2402 | UNKNOWN | no_clear_temporal_keywords |
| mlb_model_probabilities.jsonl | jsonl | 1476 | UNKNOWN | no_clear_temporal_keywords |
| mlb_feature_candidate_probabilities.jsonl | jsonl | 2402 | UNKNOWN | no_clear_temporal_keywords |
| mlb_feature_candidate_probabilities.jsonl | jsonl | 2402 | UNKNOWN | no_clear_temporal_keywords |
| mlb_feature_candidate_probabilities.jsonl | jsonl | 2402 | UNKNOWN | no_clear_temporal_keywords |
| calibration_candidate_evaluation.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| model_join_integrity_audit.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| model_probability_segment_audit.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| model_worst_segments.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| oof_calibration_evaluation.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| oof_calibration_folds.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| model_join_integrity_audit.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| model_worst_segments.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| replay_default_validation_report.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| phase64b_bullpen_relief_appearances_20260506.jsonl | jsonl | 0 | UNKNOWN | file_empty_or_unreadable |
| phase54_safe_sp_stability_audit_2026-05-05.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| phase59_pre_heavy_favorite_local_calibration_2026-05-06.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| phase64b_full_season_ingestion_summary_20260506.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| phase70_strong_home_favorite_underconfidence_audit_20260507.json | json_object | 1 | UNKNOWN | no_clear_temporal_keywords |
| future_model_predictions_dry_run_2026-04-29.jsonl | jsonl | 2080 | PREGAME_SAFE | pregame_keywords_present: ['odds_snapshot_ref'] |
| match_identity_bridge_2026-04-29.jsonl | jsonl | 383 | PREGAME_SAFE | postgame_keyword_columns: ['postgame_game_id']; pregame_keywords_present: ['odds_raw_match_ids'] |
| model_outputs_2026-04-29.jsonl | jsonl | 2986 | PREGAME_SAFE | pregame_keywords_present: ['odds_snapshot_ref', 'training_window_id'] |
| model_outputs_6q_dry_run_2026-04-30.jsonl | jsonl | 30 | PREGAME_SAFE | pregame_keywords_present: ['odds_snapshot_ref', 'odds_snapshot_time_utc', 'training_window_id'] |
| model_outputs_6r_future_2026-04-30.jsonl | jsonl | 10 | PREGAME_SAFE | pregame_keywords_present: ['odds_snapshot_ref', 'training_window_id'] |
| model_outputs_6s_future_2026-04-30.jsonl | jsonl | 14 | PREGAME_SAFE | pregame_keywords_present: ['market_odds_at_prediction', 'odds_snapshot_ref', 'odds_snapshot_alignment_status', 'odds_sna |
| mlb_2025_bullpen_features_phase56.jsonl | jsonl | 2025 | PREGAME_SAFE | pregame_keywords_present: ['away_bullpen_recent_era_proxy', 'away_bullpen_fatigue_7d', 'home_bullpen_fatigue_7d', 'bullp |
| mlb_2025_starting_pitcher_features_phase52.jsonl | jsonl | 2025 | PREGAME_SAFE | pregame_keywords_present: ['home_probable_pitcher_name', 'away_probable_pitcher_name'] |
| bullpen_usage_3d.jsonl | jsonl | 2430 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_usage_last_3d_home', 'bullpen_usage_last_3d_away'] |
| injury_rest.jsonl | jsonl | 2430 | PREGAME_SAFE | pregame_keywords_present: ['injury_report.away_inactive', 'rest_days_home', 'rest_days_away', 'injury_report', 'injury_r |
| lineups.jsonl | jsonl | 2430 | PREGAME_SAFE | pregame_keywords_present: ['confirmed_home_lineup', 'confirmed_away_starter', 'confirmed_away_lineup', 'confirmed_home_s |
| odds_timeline.jsonl | jsonl | 2979 | PREGAME_SAFE | postgame_keyword_columns: ['external_closing_away_ml', 'closing_home_ml', 'closing_ts', 'closing_source', 'external_clos |
| weather_wind.jsonl | jsonl | 2430 | PREGAME_SAFE | pregame_keywords_present: ['park_factors.turf_type', 'wind', 'wind.wind_kmh_avg', 'weather.weather_code_mode', 'weather. |
| bullpen_usage_3d.jsonl | jsonl | 2370 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_usage_last_3d_home', 'bullpen_usage_last_3d_away'] |
| confirmed_lineups.jsonl | jsonl | 2370 | PREGAME_SAFE | pregame_keywords_present: ['confirmed_home_lineup', 'confirmed_away_starter', 'confirmed_away_lineup', 'confirmed_home_s |
| injury_rest.jsonl | jsonl | 2370 | PREGAME_SAFE | pregame_keywords_present: ['injury_report.away_inactive', 'rest_days_home', 'rest_days_away', 'injury_report', 'injury_r |
| odds_timeline.jsonl | jsonl | 2398 | PREGAME_SAFE | postgame_keyword_columns: ['closing_home_ml', 'closing_away_ml']; pregame_keywords_present: ['odds_history'] |
| odds_timeline_canonical.jsonl | jsonl | 2430 | PREGAME_SAFE | postgame_keyword_columns: ['closing_home_ml', 'closing_ts', 'closing_away_ml']; pregame_keywords_present: ['latest_prega |
| weather_cache.jsonl | jsonl | 2050 | PREGAME_SAFE | pregame_keywords_present: ['weather_payload.wind_kmh_avg', 'weather_payload.provider', 'weather_payload.weather_code_mod |
| weather_wind.jsonl | jsonl | 2370 | PREGAME_SAFE | pregame_keywords_present: ['park_factors.turf_type', 'wind', 'wind.wind_kmh_avg', 'weather.temp_c_avg', 'weather'] |
| clv_validation_records_6u_2026-04-30.before_phase29_2026-05-01.jsonl | jsonl | 14 | PREGAME_SAFE | postgame_keyword_columns: ['closing_odds_source', 'closing_implied_probability', 'closing_odds', 'closing_odds_time_utc' |
| clv_validation_records_6u_2026-04-30.jsonl | jsonl | 14 | PREGAME_SAFE | postgame_keyword_columns: ['closing_odds_source', 'closing_ts', 'closing_implied_probability', 'closing_odds', 'closing_ |
| prediction_registry_6t_2026-04-30.jsonl | jsonl | 14 | PREGAME_SAFE | pregame_keywords_present: ['market_odds_at_prediction', 'odds_snapshot_ref', 'odds_snapshot_alignment_status', 'odds_sna |
| tsl_spring2026_canonical.jsonl | jsonl | 38 | PREGAME_SAFE | postgame_keyword_columns: ['closing_home_ml', 'closing_ts', 'closing_away_ml']; pregame_keywords_present: ['latest_prega |
| mlb_odds_2025_real.csv | csv | 2430 | PREGAME_SAFE | postgame_keyword_columns: ['Home Score', 'Away Score']; pregame_keywords_present: ['Away Starter', 'Home RL Spread', 'Ho |
| external_closing_state.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['last_attempt_ts'] |
| calibration_compare.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['platt.summary.logloss', 'isotonic.summary.logloss']; pregame_keywords_present: ['isotonic.od |
| model_artifacts.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['odds_band_stats.roi.other', 'odds_band_stats.bets.other', 'odds_band_stats.bets.1.81-2.10',  |
| 2026-03-14_KOR_DOM_poisson_summary.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['b_win_9', 'a_win_9']; pregame_keywords_present: ['starters.away_sp.name', 'starters.away_sp. |
| 2026-03-14_USA_CAN_poisson_summary.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['b_win_9', 'a_win_9']; pregame_keywords_present: ['starters.away_sp.name', 'starters.away_sp. |
| 2026-03-15_PUR_ITA_poisson_summary.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['b_win_9', 'a_win_9']; pregame_keywords_present: ['starters.away_sp.name', 'starters.away_sp. |
| 2026-03-15_VEN_JPN_poisson_summary.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['b_win_9', 'a_win_9']; pregame_keywords_present: ['starters.away_sp.name', 'starters.away_sp. |
| gate_validation_evidence.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['final_decision', 'missing_actual_detail', 'n_missing_actual']; pregame_keywords_present: ['n |
| mlb_2025_odds_timeline_qa_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['acceptance_gate.closing_only_coverage_gte_80pct', 'missing_by_timepoint.closing', 'closing_o |
| mlb_calibration_baseline_snapshot_2026-04-25.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['metrics.candidate.small_edge.logloss', 'metrics.delta.favorites.logloss_vs_favorites', 'metr |
| mlb_data_health_report_sample.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['availability_pct.closing_line_home', 'availability_pct.closing_line_away']; pregame_keywords |
| mlb_decision_quality_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['summary.clv_source_counts.closing_fallback', 'summary.label_counts.BAD_BET_LOSS', 'summary.l |
| mlb_decision_quality_report_test.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['summary.clv_source_counts.closing_fallback', 'summary.label_counts.BAD_BET_LOSS', 'summary.l |
| mlb_feed_qa_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['strict_validation_recovery.after.availability_pct.closing_line_away', 'strict_validation_rec |
| mlb_model_family_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['moneyline_research.logloss', 'moneyline_strict.logloss', 'f5_moneyline.logloss', 'team_total |
| mlb_odds_timeline_audit_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['context_summary.same_opening_closing', 'source_summary.closing_home_ml_canonical', 'tsl_spri |
| mlb_odds_timeline_qa_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['qa.availability.closing_rate', 'build_summary.games_with_closing', 'qa.availability.closing_ |
| mlb_paper_tracking_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['overall_strict_metrics.strict_only_logloss', 'monthly_tracking.prior_month.strict_only_loglo |
| mlb_paper_tracking_report_test.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['overall_strict_metrics.strict_only_logloss', 'monthly_tracking.prior_month.strict_only_loglo |
| mlb_paper_tracking_report_tmp.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['overall_strict_metrics.strict_only_logloss', 'monthly_tracking.prior_month.strict_only_loglo |
| mlb_pregame_coverage_report.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['totals.postgame_records']; pregame_keywords_present: ['pregame_coverage.multi_snapshot_rate' |
| mlb_universe_alignment_report.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['providers_ready.the_odds_api'] |
| mlb_weather_scale_report.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['weather_batch_efficiency.cache_misses', 'weather_batch_efficiency.cache_hits', 'weather_batc |
| optimization_ops_report_2026-04-30_1017.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_1328.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_1401.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_1403.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_1424.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_1426.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_1438.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['scheduler_runs']; pregame_keywords_present: ['window'] |
| optimization_ops_report_2026-04-30_2137.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['closing_availability.stale_candidates', 'closing_availability.source_refresh_blocked_reason' |
| tsl_timeline_research_asset.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['timeline_tier_breakdown.closing_only_1_pregame', 'games_with_actual_line_movement']; pregame |
| wbc_quarterfinal_starters_2026.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['games.2026-03-14_USA_CAN.home_sp.era', 'games.2026-03-15_VEN_JPN.away_sp.era', 'games.2026-0 |
| wbc_verified_overrides.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['games.A06.starter_source_urls', 'games.C06.starter_source_urls', 'games.D01.starter_source_u |
| mlb_independent_features.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['recent_win_rate_delta', 'home_recent_win_rate', 'source_trace.win_rate_lookback', 'away_rece |
| mlb_independent_features.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['recent_win_rate_delta', 'home_recent_win_rate', 'source_trace.win_rate_lookback', 'away_rece |
| mlb_repaired_model_probabilities.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| mlb_independent_features.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['recent_win_rate_delta', 'home_recent_win_rate', 'source_trace.win_rate_lookback', 'away_rece |
| mlb_independent_features.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['recent_win_rate_delta', 'home_recent_win_rate', 'source_trace.win_rate_lookback', 'away_rece |
| mlb_independent_features.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['recent_win_rate_delta', 'home_recent_win_rate', 'source_trace.win_rate_lookback', 'away_rece |
| mlb_repaired_model_probabilities.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| mlb_repaired_model_probabilities.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| mlb_repaired_model_probabilities.jsonl | jsonl | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| 2026-05-11-AWY-HOM-824441.jsonl | jsonl | 1 | PREGAME_SAFE | pregame_keywords_present: ['tsl_decimal_odds'] |
| 2026-05-11-LAA-CLE-824441.jsonl | jsonl | 1 | PREGAME_SAFE | pregame_keywords_present: ['tsl_decimal_odds'] |
| mlb_odds_with_feature_candidate_probabilities.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_independent_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_calibrated_probabilities.csv | csv | 2430 | PREGAME_SAFE | postgame_keyword_columns: ['Home Score', 'Away Score']; pregame_keywords_present: ['Away Starter', 'Home RL Spread', 'Ho |
| mlb_odds_with_feature_candidate_probabilities.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_independent_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_model_probabilities.csv | csv | 2430 | PREGAME_SAFE | postgame_keyword_columns: ['Home Score', 'Away Score']; pregame_keywords_present: ['Away Starter', 'Home RL Spread', 'Ho |
| mlb_odds_with_oof_calibrated_probabilities.csv | csv | 1951 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_repaired_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| mlb_odds_with_feature_candidate_probabilities.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_independent_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_feature_candidate_probabilities.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_independent_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_feature_candidate_probabilities.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_independent_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['indep_away_recent_win_rate', 'win_rate_delta', 'indep_recent_win_rate_delta', 'Home Score',  |
| mlb_odds_with_repaired_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| mlb_odds_with_repaired_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| mlb_odds_with_repaired_features.csv | csv | 2402 | PREGAME_SAFE | postgame_keyword_columns: ['win_rate_delta', 'Home Score', 'Away Score', 'recent_win_rate_home', 'recent_win_rate_away'] |
| independent_feature_coverage.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['coverage_by_feature.away_recent_win_rate.hit', 'coverage_by_feature.home_recent_win_rate.pct |
| independent_feature_coverage.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['coverage_by_feature.away_recent_win_rate.hit', 'coverage_by_feature.home_recent_win_rate.pct |
| repaired_feature_metadata.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_join_miss_count', 'rest_join_hit_count', 'rest_join_miss_count', 'bullpen_join_hit_c |
| independent_feature_coverage.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['coverage_by_feature.away_recent_win_rate.hit', 'coverage_by_feature.home_recent_win_rate.pct |
| independent_feature_coverage.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['coverage_by_feature.away_recent_win_rate.hit', 'coverage_by_feature.home_recent_win_rate.pct |
| independent_feature_coverage.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['coverage_by_feature.away_recent_win_rate.hit', 'coverage_by_feature.home_recent_win_rate.pct |
| repaired_feature_metadata.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_join_miss_count', 'rest_join_hit_count', 'rest_join_miss_count', 'bullpen_join_hit_c |
| repaired_feature_metadata.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_join_miss_count', 'rest_join_hit_count', 'rest_join_miss_count', 'bullpen_join_hit_c |
| repaired_feature_metadata.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_join_miss_count', 'rest_join_hit_count', 'rest_join_miss_count', 'bullpen_join_hit_c |
| phase63_bullpen_relief_appearances_20260506.jsonl | jsonl | 26 | PREGAME_SAFE | pregame_keywords_present: ['starter_flag'] |
| phase63_bullpen_ssot_features_20260506.jsonl | jsonl | 4 | PREGAME_SAFE | pregame_keywords_present: ['pit_window_map.reliever_back_to_back_count', 'pit_window_map.high_leverage_reliever_workload |
| phase64b_bullpen_ssot_features_20260506.jsonl | jsonl | 4694 | PREGAME_SAFE | pregame_keywords_present: ['bullpen_usage_last_5d', 'bullpen_usage_last_1d', 'bullpen_usage_last_3d'] |
| phase44_market_blend_paper_tracking_2026-05-05.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['phase43_evidence.segment_value.odds_bucket', 'segment_summary.odds_bucket'] |
| phase49_feature_repair_evaluation_2026-05-05.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['delta_metrics.delta_log_loss', 'baseline_metrics.log_loss', 'market_metrics.log_loss', 'phas |
| phase50_p0_feature_injection_2026-05-05.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['delta_log_loss', 'baseline_log_loss', 'phase50_log_loss']; pregame_keywords_present: ['segme |
| phase52_sp_feature_injection_2026-05-05.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['delta_log_loss', 'baseline_log_loss', 'phase52_log_loss']; pregame_keywords_present: ['segme |
| phase56_bullpen_feature_evaluation_2026-05-05.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['evaluation.phase56_metrics.log_loss', 'evaluation.baseline_metrics.log_loss', 'evaluation.ma |
| phase60_bullpen_feature_decomposition_20260506.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['oof_summary.fold_win_rate_deltas', 'negative_control.real_win_rate_delta_heavy_fav']; pregam |
| phase62_bullpen_granular_source_selection_20260506.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['ingestion_proof.errors', 'ingestion_proof.closer_candidates', 'ingestion_proof.total_pitcher |
| phase63_statsapi_bullpen_granular_ingestion_20260506.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['ingestion_summary.starters'] |
| phase69_calibration_objective_redesign_counterfactual_20260507.json | json_object | 1 | PREGAME_SAFE | postgame_keyword_columns: ['counterfactual_metrics']; pregame_keywords_present: ['oof_split.eval_windows', 'oof_split.tr |
| phase72_market_derisk_guard_proposal_20260507.json | json_object | 1 | PREGAME_SAFE | pregame_keywords_present: ['p71_evidence.windows_market_superior'] |
| odds_snapshots_2026-04-29.jsonl | jsonl | 28941 | POSTGAME_RISK | outcome_columns_present: ['raw_outcome_name'] |
| mlb_2025_per_game_predictions.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase48_p0_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase50_p0_injected_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase52_sp_context_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase52_sp_injected_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase54_sp_safe_coeff_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| mlb_2025_per_game_predictions_phase56_sp_bullpen_injected_v1.jsonl | jsonl | 2025 | POSTGAME_RISK | outcome_columns_present: ['home_win'] |
| performance_monitor.jsonl | jsonl | 8141 | POSTGAME_RISK | postgame_keyword_columns: ['actual']; no_pregame_keywords_found |
| postgame_results.jsonl | jsonl | 49 | POSTGAME_RISK | outcome_columns_present: ['actual_result.total_runs', 'evaluation.home_win_log_loss', 'actual_result.home_win', 'actual_ |
| prediction_registry.jsonl | jsonl | 66 | POSTGAME_RISK | outcome_columns_present: ['game_output.away_win_prob', 'prediction.confidence_score', 'decision_report.real_edge_score', |
| prediction_registry_replay.jsonl | jsonl | 40 | POSTGAME_RISK | outcome_columns_present: ['prediction.home_win_prob', 'prediction.away_win_prob', 'prediction.confidence_score', 'predic |
| mlb-2025-asplayed.csv | csv | 2430 | POSTGAME_RISK | outcome_columns_present: ['Winner', 'away_score', 'winner', 'home_score', 'home_win'] |
| manifest_dry_run_summary_2026-04-29.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['aggregate_gate_results.A2_league_coverage', 'aggregate_gate_results.A1_sample_sufficiency', ' |
| model_output_contract_validation_summary_2026-04-29.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results |
| model_output_contract_validation_summary_6q_2026-04-30.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results |
| model_output_contract_validation_summary_6r_2026-04-30.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results |
| model_output_contract_validation_summary_6s_2026-04-30.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results |
| mlb_current_source_sample_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['fixture_metadata.coverage_summary.result_games'] |
| continuous_learning_state.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['recent_brier_scores'] |
| improvement_log.json | json_array | 1 | POSTGAME_RISK | outcome_columns_present: ['training_metrics.xgboost.brier_score', 'training_metrics.stacking.brier_score', 'training_met |
| retrainer_state.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['performances.baseline.brier_scores', 'performances.elo.brier_scores', 'performances.bayesian. |
| v3_research_cycle.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['phase_results'] |
| market_validation.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['ML.logloss', 'OU.logloss', 'RL.logloss']; no_pregame_keywords_found |
| portfolio_risk.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['consecutive_losses']; no_pregame_keywords_found |
| clv_validation_records_6u_summary_2026-04-30.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['stats.pending_closing']; no_pregame_keywords_found |
| market_support_performance_summary.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['groups.tsl_direct.winner_accuracy', 'groups.tsl_direct.avg_total_score_error'] |
| mlb_alpha_discovery_report.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['strict_results'] |
| mlb_alpha_discovery_report_test.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['strict_results'] |
| mlb_alpha_discovery_report_test_blocked.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['strict_results'] |
| mlb_decision_optimization_report.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['calibration_metrics_before_after.isotonic.logloss', 'strict_optimized_metrics.logloss', 'str |
| mlb_model_rebuild_report.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['regime_segmentation_results'] |
| mlb_regime_feature_redesign_report.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.calibra |
| mlb_regime_paper_report.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['regime_specific_model_results'] |
| optimization_readiness_latest.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['closing_availability.invalid_same_snapshot', 'closing_availability.invalid_before_prediction |
| tune_results_top10.json | json_array | 10 | POSTGAME_RISK | postgame_keyword_columns: ['logloss', 'score']; no_pregame_keywords_found |
| walkforward_summary.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['logloss']; no_pregame_keywords_found |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_73855ccb.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_calibrated_candidate_d5fb827f.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_f8695fec.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_oof_calibrated_ed059d96.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p10_feature_candidat_edaddde1.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p9_repaired_oof_663d9bc7.jsonl | jsonl | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score'] |
| bad_source.csv | csv | 1 | POSTGAME_RISK | postgame_keyword_columns: ['Home Score', 'Away Score']; no_pregame_keywords_found |
| oof_model.csv | csv | 20 | POSTGAME_RISK | postgame_keyword_columns: ['Home Score', 'Away Score']; no_pregame_keywords_found |
| raw_model.csv | csv | 20 | POSTGAME_RISK | postgame_keyword_columns: ['Home Score', 'Away Score']; no_pregame_keywords_found |
| model_deep_diagnostics_oof.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_on |
| model_deep_diagnostics_raw.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_on |
| model_probability_audit.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score', 'orientation_checks.home_win_rate_when_model_gt_0_5', 'orientation_checks |
| model_deep_diagnostics_oof.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_on |
| model_deep_diagnostics_raw.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_on |
| replay_default_validation_ci_verification_report.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['local_fixture_results.overall', 'local_fixture_results.aligned', 'local_fixture_results.misma |
| mlb_paper_betting_ledger.jsonl | jsonl | 13 | POSTGAME_RISK | outcome_columns_present: ['result_status', 'realized_outcome'] |
| mlb_paper_betting_reviewed_snapshot_20250701.jsonl | jsonl | 7 | POSTGAME_RISK | outcome_columns_present: ['result_status', 'realized_outcome'] |
| mlb_paper_betting_reviewed_snapshot_20260507.jsonl | jsonl | 13 | POSTGAME_RISK | outcome_columns_present: ['result_status', 'realized_outcome'] |
| metrics_ssot_phase67_72_inventory_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['phase_scan_results'] |
| mlb_current_source_probe_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['market_coverage.result_available', 'source_health.result_games'] |
| mlb_daily_advisory_dry_run_20250701.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['review_summary.pending_result_count', 'market_coverage_matrix_summary.result_available'] |
| mlb_daily_advisory_dry_run_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['review_summary.pending_result_count', 'market_coverage_matrix_summary.result_available'] |
| mlb_daily_scheduler_manifest_20250701.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_score'] |
| mlb_daily_scheduler_manifest_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['brier_score'] |
| mlb_live_source_plan_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['contracts.result_source_contract.governance_flags.paper_only', 'contracts.result_source_contr |
| mlb_postgame_review_20250701.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'rev |
| mlb_postgame_review_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'rev |
| phase53_sp_coefficient_calibration_2026-05-05.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['coefficient_grid_results'] |
| phase55_sp_vs_bullpen_diagnosis_2026-05-05.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['bullpen_diagnosis.bullpen_missing_score', 'functional_form_results'] |
| phase59_real_bullpen_boxscore_acquisition_20260506.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['heavy_fav_signal.home_win_rate', 'high_conf_signal.home_win_rate'] |
| phase64_granular_bullpen_attribution_20260506.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['oof_results'] |
| phase64b_full_season_bullpen_ingestion_and_attribution_20260506.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['oof_results'] |
| phase65_sp_fatigue_attribution_20260506.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['oof_results'] |
| phase66_market_microstructure_failure_attribution_20260506.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['oof_results'] |
| phase67_context_failure_attribution_20260506.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['oof_results'] |
| phase68_model_architecture_ensemble_failure_audit_20260506.json | json_object | 1 | POSTGAME_RISK | postgame_keyword_columns: ['model_band_75_plus.fav_win_rate', 'high_conf_metrics.fav_win_rate', 'model_band_60_65.fav_wi |
| phase71_market_dominance_model_derisk_audit_20260507.json | json_object | 1 | POSTGAME_RISK | outcome_columns_present: ['split_market_results', 'sp_fip_attribution.sp_fip_vs_outcome_residual_corr'] |

## Risk Files (detail)

### odds_snapshots_2026-04-29.jsonl

- Path: `data/derived/odds_snapshots_2026-04-29.jsonl`
- Rows: 28941
- Outcome columns: ['raw_outcome_name']
- Postgame keyword hits: ['raw_outcome_name']
- Reasons: ["outcome_columns_present: ['raw_outcome_name']"]

### mlb_2025_per_game_predictions.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase48_p0_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase48_p0_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase50_p0_injected_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase50_p0_injected_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase52_sp_context_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase52_sp_context_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase52_sp_injected_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase52_sp_injected_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase54_sp_safe_coeff_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase54_sp_safe_coeff_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### mlb_2025_per_game_predictions_phase56_sp_bullpen_injected_v1.jsonl

- Path: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_injected_v1.jsonl`
- Rows: 2025
- Outcome columns: ['home_win']
- Postgame keyword hits: ['home_win']
- Reasons: ["outcome_columns_present: ['home_win']"]

### performance_monitor.jsonl

- Path: `data/wbc_backend/reports/performance_monitor.jsonl`
- Rows: 8141
- Outcome columns: []
- Postgame keyword hits: ['actual']
- Reasons: ["postgame_keyword_columns: ['actual']", 'no_pregame_keywords_found']

### postgame_results.jsonl

- Path: `data/wbc_backend/reports/postgame_results.jsonl`
- Rows: 49
- Outcome columns: ['actual_result.total_runs', 'evaluation.home_win_log_loss', 'actual_result.home_win', 'actual_result.home_score', 'evaluation.predicted_home_win', 'prediction_summary.predicted_away_win_prob', 'prediction_summary.predicted_away_score', 'prediction_summary.predicted_home_score', 'actual_result', 'evaluation.winner_correct', 'actual_result.away_score', 'evaluation.home_win_brier', 'prediction_summary.predicted_home_win_prob']
- Postgame keyword hits: ['actual_result.total_runs', 'evaluation.score_error_total_abs', 'evaluation.score_error_home_abs', 'evaluation.home_win_log_loss', 'actual_result.home_win', 'evaluation.predicted_total_runs', 'actual_result.home_score', 'evaluation.predicted_home_win', 'evaluation.actual_total_runs', 'prediction_summary.predicted_away_win_prob']
- Reasons: ["outcome_columns_present: ['actual_result.total_runs', 'evaluation.home_win_log_loss', 'actual_result.home_win', 'actual_result.home_score', 'evaluation.predicted_home_win', 'prediction_summary.predicted_away_win_prob', 'prediction_summary.predicted_away_score', 'prediction_summary.predicted_home_score', 'actual_result', 'evaluation.winner_correct', 'actual_result.away_score', 'evaluation.home_win_brier', 'prediction_summary.predicted_home_win_prob']"]

### prediction_registry.jsonl

- Path: `data/wbc_backend/reports/prediction_registry.jsonl`
- Rows: 66
- Outcome columns: ['game_output.away_win_prob', 'prediction.confidence_score', 'decision_report.real_edge_score', 'game_output.home_win_prob', 'game_output.predicted_away_score', 'game_output.market_bias_score', 'prediction.away_win_prob', 'prediction.market_bias_score', 'simulation.away_win_prob', 'prediction.sub_model_results', 'prediction.home_win_prob', 'decision_report.edge_score', 'decision_report.fake_move_score', 'game_output.predicted_home_score', 'simulation.home_win_prob', 'decision_report.execution_risk_score']
- Postgame keyword hits: ['deployment_gate.walkforward_summary.logloss', 'game_output.away_win_prob', 'simulation.score_distribution.6-4', 'simulation.score_distribution.3-4', 'simulation.score_distribution.2-4', 'simulation.mean_total_runs', 'prediction.expected_home_runs', 'prediction.confidence_score', 'simulation.score_distribution.2-1', 'decision_report.real_edge_score']
- Reasons: ["outcome_columns_present: ['game_output.away_win_prob', 'prediction.confidence_score', 'decision_report.real_edge_score', 'game_output.home_win_prob', 'game_output.predicted_away_score', 'game_output.market_bias_score', 'prediction.away_win_prob', 'prediction.market_bias_score', 'simulation.away_win_prob', 'prediction.sub_model_results', 'prediction.home_win_prob', 'decision_report.edge_score', 'decision_report.fake_move_score', 'game_output.predicted_home_score', 'simulation.home_win_prob', 'decision_report.execution_risk_score']"]

### prediction_registry_replay.jsonl

- Path: `data/wbc_backend/reports/prediction_registry_replay.jsonl`
- Rows: 40
- Outcome columns: ['prediction.home_win_prob', 'prediction.away_win_prob', 'prediction.confidence_score', 'prediction.sub_model_results']
- Postgame keyword hits: ['prediction.home_win_prob', 'prediction.expected_away_runs', 'prediction.away_win_prob', 'prediction.expected_home_runs', 'prediction.confidence_score', 'prediction.sub_model_results']
- Reasons: ["outcome_columns_present: ['prediction.home_win_prob', 'prediction.away_win_prob', 'prediction.confidence_score', 'prediction.sub_model_results']"]

### mlb-2025-asplayed.csv

- Path: `data/mlb_2025/mlb-2025-asplayed.csv`
- Rows: 2430
- Outcome columns: ['Winner', 'away_score', 'winner', 'home_score', 'home_win']
- Postgame keyword hits: ['Winner', 'away_score', 'winner', 'Home Score', 'home_score', 'Away Score', 'home_win']
- Reasons: ["outcome_columns_present: ['Winner', 'away_score', 'winner', 'home_score', 'home_win']"]

### manifest_dry_run_summary_2026-04-29.json

- Path: `data/derived/manifest_dry_run_summary_2026-04-29.json`
- Rows: 1
- Outcome columns: ['aggregate_gate_results.A2_league_coverage', 'aggregate_gate_results.A1_sample_sufficiency', 'aggregate_gate_results.A3_market_coverage.markets_present', 'aggregate_gate_results', 'aggregate_gate_results.A3_market_coverage', 'aggregate_gate_results.A3_market_coverage.pass', 'aggregate_gate_results.A1_sample_sufficiency.note', 'aggregate_gate_results.A1_sample_sufficiency.current', 'aggregate_gate_results.A1_sample_sufficiency.target', 'aggregate_gate_results.A2_league_coverage.pass', 'aggregate_gate_results.A2_league_coverage.bridge_ready_leagues', 'aggregate_gate_results.A1_sample_sufficiency.pass']
- Postgame keyword hits: ['aggregate_gate_results.A2_league_coverage', 'aggregate_gate_results.A1_sample_sufficiency', 'aggregate_gate_results.A3_market_coverage.markets_present', 'aggregate_gate_results', 'aggregate_gate_results.A3_market_coverage', 'aggregate_gate_results.A3_market_coverage.pass', 'aggregate_gate_results.A1_sample_sufficiency.note', 'aggregate_gate_results.A1_sample_sufficiency.current', 'opening_closing_pairs', 'aggregate_gate_results.A1_sample_sufficiency.target']
- Reasons: ["outcome_columns_present: ['aggregate_gate_results.A2_league_coverage', 'aggregate_gate_results.A1_sample_sufficiency', 'aggregate_gate_results.A3_market_coverage.markets_present', 'aggregate_gate_results', 'aggregate_gate_results.A3_market_coverage', 'aggregate_gate_results.A3_market_coverage.pass', 'aggregate_gate_results.A1_sample_sufficiency.note', 'aggregate_gate_results.A1_sample_sufficiency.current', 'aggregate_gate_results.A1_sample_sufficiency.target', 'aggregate_gate_results.A2_league_coverage.pass', 'aggregate_gate_results.A2_league_coverage.bridge_ready_leagues', 'aggregate_gate_results.A1_sample_sufficiency.pass']"]

### model_output_contract_validation_summary_2026-04-29.json

- Path: `data/derived/model_output_contract_validation_summary_2026-04-29.json`
- Rows: 1
- Outcome columns: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']
- Postgame keyword hits: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass']
- Reasons: ["outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']"]

### model_output_contract_validation_summary_6q_2026-04-30.json

- Path: `data/derived/model_output_contract_validation_summary_6q_2026-04-30.json`
- Rows: 1
- Outcome columns: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']
- Postgame keyword hits: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass']
- Reasons: ["outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']"]

### model_output_contract_validation_summary_6r_2026-04-30.json

- Path: `data/derived/model_output_contract_validation_summary_6r_2026-04-30.json`
- Rows: 1
- Outcome columns: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']
- Postgame keyword hits: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass']
- Reasons: ["outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']"]

### model_output_contract_validation_summary_6s_2026-04-30.json

- Path: `data/derived/model_output_contract_validation_summary_6s_2026-04-30.json`
- Rows: 1
- Outcome columns: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']
- Postgame keyword hits: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass']
- Reasons: ["outcome_columns_present: ['gate_results.M10.pass_pct', 'gate_results.M4.pass_pct', 'gate_results.M1.pass', 'gate_results.M9.block', 'gate_results.M4.fail', 'gate_results.M9.pass_pct', 'gate_results.M4', 'gate_results.M3.pass', 'gate_results.M5.total_rows', 'gate_results.M4.pass', 'gate_results.M2', 'gate_results.M11', 'gate_results.M5.block', 'gate_results.M11.block', 'gate_results.M12.block', 'gate_results.M8.pass_pct', 'gate_results.M5.fail', 'gate_results.M9.pass', 'gate_results.M13.pass', 'gate_results.M3.total_rows', 'gate_results.M9.fail', 'gate_results.M12.pass', 'gate_results.M13.fail', 'gate_results.M8.block', 'gate_results.M11.pass', 'gate_results.M11.total_rows', 'gate_results.M3.fail', 'gate_results.M13.total_rows', 'gate_results.M3.pass_pct', 'gate_results.M1.total_rows', 'gate_results.M9.total_rows', 'gate_results.M12', 'gate_results.M7.fail', 'gate_results.M2.fail', 'gate_results.M10.fail', 'gate_results.M2.pass_pct', 'gate_results.M10', 'gate_results.M2.pass', 'gate_results.M7.total_rows', 'gate_results.M10.block', 'gate_results.M7.block', 'gate_results.M7', 'gate_results.M2.block', 'gate_results.M12.pass_pct', 'gate_results.M3.block', 'gate_results.M5.pass_pct', 'gate_results.M13.block', 'gate_results.M5.pass', 'gate_results.M9', 'gate_results.M6', 'gate_results.M11.pass_pct', 'gate_results.M8.pass', 'gate_results.M12.total_rows', 'gate_results.M6.pass_pct', 'gate_results.M3', 'gate_results.M1.fail', 'gate_results.M4.total_rows', 'gate_results.M13.pass_pct', 'gate_results.M11.fail', 'gate_results.M8.total_rows', 'gate_results.M6.fail', 'gate_results.M10.total_rows', 'gate_results.M10.pass', 'gate_results.M2.total_rows', 'gate_results.M12.fail', 'gate_results.M8.fail', 'gate_results.M1.pass_pct', 'gate_results.M1', 'gate_results.M7.pass', 'gate_results.M1.block', 'gate_results.M6.pass', 'gate_results', 'gate_results.M13', 'gate_results.M4.block', 'gate_results.M6.block', 'gate_results.M6.total_rows', 'gate_results.M8', 'gate_results.M5', 'gate_results.M7.pass_pct']"]

### mlb_current_source_sample_20260507.json

- Path: `data/fixtures/mlb_current_source_sample_20260507.json`
- Rows: 1
- Outcome columns: ['fixture_metadata.coverage_summary.result_games']
- Postgame keyword hits: ['fixture_metadata.coverage_summary.result_games']
- Reasons: ["outcome_columns_present: ['fixture_metadata.coverage_summary.result_games']"]

### continuous_learning_state.json

- Path: `data/wbc_backend/artifacts/continuous_learning_state.json`
- Rows: 1
- Outcome columns: ['recent_brier_scores']
- Postgame keyword hits: ['recent_brier_scores']
- Reasons: ["outcome_columns_present: ['recent_brier_scores']"]

### improvement_log.json

- Path: `data/wbc_backend/artifacts/improvement_log.json`
- Rows: 1
- Outcome columns: ['training_metrics.xgboost.brier_score', 'training_metrics.stacking.brier_score', 'training_metrics.neural_net.brier_score', 'training_metrics.lightgbm.brier_score']
- Postgame keyword hits: ['training_metrics.xgboost.brier_score', 'training_metrics.lightgbm.logloss', 'training_metrics.neural_net.logloss', 'training_metrics.stacking.brier_score', 'training_metrics.neural_net.brier_score', 'training_metrics.xgboost.logloss', 'training_metrics.stacking.logloss', 'training_metrics.lightgbm.brier_score']
- Reasons: ["outcome_columns_present: ['training_metrics.xgboost.brier_score', 'training_metrics.stacking.brier_score', 'training_metrics.neural_net.brier_score', 'training_metrics.lightgbm.brier_score']"]

### retrainer_state.json

- Path: `data/wbc_backend/artifacts/retrainer_state.json`
- Rows: 1
- Outcome columns: ['performances.baseline.brier_scores', 'performances.elo.brier_scores', 'performances.bayesian.brier_scores', 'performances.neural_net.brier_scores', 'performances.real_gbm_stack.brier_scores', 'performances.poisson.brier_scores']
- Postgame keyword hits: ['performances.poisson.log_losses', 'performances.baseline.brier_scores', 'performances.elo.brier_scores', 'performances.bayesian.brier_scores', 'performances.neural_net.brier_scores', 'performances.neural_net.actuals', 'performances.real_gbm_stack.brier_scores', 'performances.real_gbm_stack.log_losses', 'performances.elo.actuals', 'performances.poisson.actuals']
- Reasons: ["outcome_columns_present: ['performances.baseline.brier_scores', 'performances.elo.brier_scores', 'performances.bayesian.brier_scores', 'performances.neural_net.brier_scores', 'performances.real_gbm_stack.brier_scores', 'performances.poisson.brier_scores']"]

### v3_research_cycle.json

- Path: `data/wbc_backend/artifacts/v3_research_cycle.json`
- Rows: 1
- Outcome columns: ['phase_results']
- Postgame keyword hits: ['phase_results']
- Reasons: ["outcome_columns_present: ['phase_results']"]

### market_validation.json

- Path: `data/wbc_backend/market_validation.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['ML.logloss', 'OU.logloss', 'RL.logloss']
- Reasons: ["postgame_keyword_columns: ['ML.logloss', 'OU.logloss', 'RL.logloss']", 'no_pregame_keywords_found']

### portfolio_risk.json

- Path: `data/wbc_backend/portfolio_risk.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['consecutive_losses']
- Reasons: ["postgame_keyword_columns: ['consecutive_losses']", 'no_pregame_keywords_found']

### clv_validation_records_6u_summary_2026-04-30.json

- Path: `data/wbc_backend/reports/clv_validation_records_6u_summary_2026-04-30.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['stats.pending_closing']
- Reasons: ["postgame_keyword_columns: ['stats.pending_closing']", 'no_pregame_keywords_found']

### market_support_performance_summary.json

- Path: `data/wbc_backend/reports/market_support_performance_summary.json`
- Rows: 1
- Outcome columns: ['groups.tsl_direct.winner_accuracy', 'groups.tsl_direct.avg_total_score_error']
- Postgame keyword hits: ['groups.tsl_direct.winner_accuracy', 'groups.tsl_direct.avg_total_score_error', 'groups.tsl_direct.avg_log_loss']
- Reasons: ["outcome_columns_present: ['groups.tsl_direct.winner_accuracy', 'groups.tsl_direct.avg_total_score_error']"]

### mlb_alpha_discovery_report.json

- Path: `data/wbc_backend/reports/mlb_alpha_discovery_report.json`
- Rows: 1
- Outcome columns: ['strict_results']
- Postgame keyword hits: ['final_verdict', 'strict_results', 'production_gap_map.odds_tier_summary.closing_coverage_rate', 'production_gap_map.odds_tier_summary.closing_only', 'data_tier_summary.closing_only_games']
- Reasons: ["outcome_columns_present: ['strict_results']"]

### mlb_alpha_discovery_report_test.json

- Path: `data/wbc_backend/reports/mlb_alpha_discovery_report_test.json`
- Rows: 1
- Outcome columns: ['strict_results']
- Postgame keyword hits: ['final_verdict', 'data_tier_summary.closing_only_games', 'strict_results', 'production_gap_map.odds_tier_summary.closing_coverage_rate', 'production_gap_map.odds_tier_summary.closing_only']
- Reasons: ["outcome_columns_present: ['strict_results']"]

### mlb_alpha_discovery_report_test_blocked.json

- Path: `data/wbc_backend/reports/mlb_alpha_discovery_report_test_blocked.json`
- Rows: 1
- Outcome columns: ['strict_results']
- Postgame keyword hits: ['final_verdict', 'data_tier_summary.closing_only_games', 'strict_results', 'production_gap_map.odds_tier_summary.closing_coverage_rate', 'production_gap_map.odds_tier_summary.closing_only']
- Reasons: ["outcome_columns_present: ['strict_results']"]

### mlb_decision_optimization_report.json

- Path: `data/wbc_backend/reports/mlb_decision_optimization_report.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['calibration_metrics_before_after.isotonic.logloss', 'strict_optimized_metrics.logloss', 'strict_optimized_metrics.win_rate', 'calibration_metrics_before_after.platt.logloss', 'calibration_metrics_before_after.raw.logloss', 'research_baseline_metrics.logloss', 'strict_baseline_metrics.logloss']
- Reasons: ["postgame_keyword_columns: ['calibration_metrics_before_after.isotonic.logloss', 'strict_optimized_metrics.logloss', 'strict_optimized_metrics.win_rate', 'calibration_metrics_before_after.platt.logloss', 'calibration_metrics_before_after.raw.logloss', 'research_baseline_metrics.logloss', 'strict_baseline_metrics.logloss']", 'no_pregame_keywords_found']

### mlb_model_rebuild_report.json

- Path: `data/wbc_backend/reports/mlb_model_rebuild_report.json`
- Rows: 1
- Outcome columns: ['regime_segmentation_results']
- Postgame keyword hits: ['regime_segmentation_results', 'final_diagnosis']
- Reasons: ["outcome_columns_present: ['regime_segmentation_results']"]

### mlb_regime_feature_redesign_report.json

- Path: `data/wbc_backend/reports/mlb_regime_feature_redesign_report.json`
- Rows: 1
- Outcome columns: ['strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_ablation', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.clv', 'strict_only_results_after_redesign.weak_starter_mismatch', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.brier', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.n_games', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.n_bets', 'strict_only_results_after_redesign.small_edge.final_metrics', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.brier', 'strict_only_results_after_redesign.small_edge.selected_feature_count', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.calibration_curve', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.roi', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.brier', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.logloss', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.n_bets', 'strict_only_results_after_redesign', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.roi', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.n_bets', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.roi', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.clv', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.clv', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.verdict', 'strict_only_results_after_redesign.small_edge.final_metrics.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.logloss', 'strict_only_results_after_redesign.small_edge.selected_features', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.win_rate', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.calibration', 'strict_only_results_after_redesign.small_edge.final_metrics.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.roi', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.fold_roi_std', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.brier', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.calibration_curve', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.fold_roi_std', 'strict_only_results_after_redesign.small_edge.final_metrics.n_games', 'strict_only_results_after_redesign.small_edge.final_metrics.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_features', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.logloss', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.roi', 'strict_only_results_after_redesign.small_edge.final_selected_calibration', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw', 'strict_only_results_after_redesign.small_edge.final_metrics.brier', 'strict_only_results_after_redesign.small_edge.final_metrics.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.n_games', 'strict_only_results_after_redesign.small_edge.calibration_comparison', 'strict_only_results_after_redesign.small_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.roi', 'strict_only_results_after_redesign.small_edge.selected_ablation', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_feature_count', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.fold_roi_std', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.clv', 'strict_only_results_after_redesign.small_edge.verdict', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.calibration_curve', 'strict_only_results_after_redesign.small_edge.final_metrics.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.final_selected_calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.logloss', 'strict_only_results_after_redesign.small_edge.final_metrics.avg_abs_edge', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.avg_abs_edge', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.avg_abs_edge', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.n_games', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.fold_roi_std', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.n_bets', 'strict_only_results_after_redesign.small_edge.final_metrics.n_bets', 'strict_only_results_after_redesign.small_edge.final_metrics.logloss']
- Postgame keyword hits: ['strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_ablation', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.avg_abs_edge']
- Reasons: ["outcome_columns_present: ['strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_ablation', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.clv', 'strict_only_results_after_redesign.weak_starter_mismatch', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.brier', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.n_games', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.n_bets', 'strict_only_results_after_redesign.small_edge.final_metrics', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.brier', 'strict_only_results_after_redesign.small_edge.selected_feature_count', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.calibration_curve', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.roi', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.brier', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.logloss', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.n_bets', 'strict_only_results_after_redesign', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.roi', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.n_bets', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.roi', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.clv', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.clv', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.verdict', 'strict_only_results_after_redesign.small_edge.final_metrics.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.logloss', 'strict_only_results_after_redesign.small_edge.selected_features', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.win_rate', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.calibration', 'strict_only_results_after_redesign.small_edge.final_metrics.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.roi', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.fold_roi_std', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.brier', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.calibration_curve', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.fold_roi_std', 'strict_only_results_after_redesign.small_edge.final_metrics.n_games', 'strict_only_results_after_redesign.small_edge.final_metrics.roi', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_features', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.logloss', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.avg_abs_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.roi', 'strict_only_results_after_redesign.small_edge.final_selected_calibration', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw', 'strict_only_results_after_redesign.small_edge.final_metrics.brier', 'strict_only_results_after_redesign.small_edge.final_metrics.win_rate', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt', 'strict_only_results_after_redesign.small_edge.calibration_comparison.platt.n_bets', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.n_games', 'strict_only_results_after_redesign.small_edge.calibration_comparison', 'strict_only_results_after_redesign.small_edge', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.brier', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.roi', 'strict_only_results_after_redesign.small_edge.selected_ablation', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.selected_feature_count', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.clv', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.fold_roi_std', 'strict_only_results_after_redesign.small_edge.calibration_comparison.raw.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.win_rate', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.clv', 'strict_only_results_after_redesign.small_edge.verdict', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.logloss', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.calibration_curve', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.calibration_curve', 'strict_only_results_after_redesign.small_edge.final_metrics.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.isotonic.fold_roi_std', 'strict_only_results_after_redesign.weak_starter_mismatch.final_selected_calibration', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.logloss', 'strict_only_results_after_redesign.small_edge.final_metrics.avg_abs_edge', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.avg_abs_edge', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.raw.avg_abs_edge', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.n_games', 'strict_only_results_after_redesign.small_edge.best_ablation_metrics_raw.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.final_metrics.n_games', 'strict_only_results_after_redesign.weak_starter_mismatch.calibration_comparison.platt.fold_roi_std', 'strict_only_results_after_redesign.small_edge.calibration_comparison.isotonic.calibration', 'strict_only_results_after_redesign.weak_starter_mismatch.best_ablation_metrics_raw.n_bets', 'strict_only_results_after_redesign.small_edge.final_metrics.n_bets', 'strict_only_results_after_redesign.small_edge.final_metrics.logloss']"]

### mlb_regime_paper_report.json

- Path: `data/wbc_backend/reports/mlb_regime_paper_report.json`
- Rows: 1
- Outcome columns: ['regime_specific_model_results']
- Postgame keyword hits: ['regime_specific_model_results']
- Reasons: ["outcome_columns_present: ['regime_specific_model_results']"]

### optimization_readiness_latest.json

- Path: `data/wbc_backend/reports/optimization_readiness_latest.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['closing_availability.invalid_same_snapshot', 'closing_availability.invalid_before_prediction', 'closing_availability.consecutive_no_improvement', 'closing_availability.recommended_escalation_action', 'closing_availability.ready_to_upgrade', 'phase7.stale_closing_rejected', 'closing_availability.next_closing_action', 'closing_availability.last_refresh_action', 'closing_availability.manual_review_required', 'closing_availability.escalation_recommended']
- Reasons: ["postgame_keyword_columns: ['closing_availability.invalid_same_snapshot', 'closing_availability.invalid_before_prediction', 'closing_availability.consecutive_no_improvement', 'closing_availability.recommended_escalation_action', 'closing_availability.ready_to_upgrade', 'phase7.stale_closing_rejected', 'closing_availability.next_closing_action', 'closing_availability.last_refresh_action', 'closing_availability.manual_review_required', 'closing_availability.escalation_recommended', 'closing_availability.source_refresh_blocked_reason', 'closing_availability.last_refresh_improved', 'closing_availability.recommended_refresh_tsl', 'closing_availability.missing_all_sources', 'safe_work.closing_monitor_due', 'closing_availability.refresh_task_due', 'closing_availability.computed_total', 'closing_availability.stale_candidates', 'phase6.clv_pending_closing', 'closing_availability.recommended_refresh_external', 'closing_availability', 'closing_availability.pending_total', 'closing_availability.last_refresh_task', 'closing_availability.next_refresh_action', 'closing_availability.available']", 'no_pregame_keywords_found']

### tune_results_top10.json

- Path: `data/wbc_backend/tune_results_top10.json`
- Rows: 10
- Outcome columns: []
- Postgame keyword hits: ['logloss', 'score']
- Reasons: ["postgame_keyword_columns: ['logloss', 'score']", 'no_pregame_keywords_found']

### walkforward_summary.json

- Path: `data/wbc_backend/walkforward_summary.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['logloss']
- Reasons: ["postgame_keyword_columns: ['logloss']", 'no_pregame_keywords_found']

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_73855ccb.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_73855ccb.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_calibrated_candidate_d5fb827f.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_calibrated_candidate_d5fb827f.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_f8695fec.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_f8695fec.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_oof_calibrated_ed059d96.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_oof_calibrated_ed059d96.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p10_feature_candidat_edaddde1.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p10_feature_candidat_edaddde1.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### 2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p9_repaired_oof_663d9bc7.jsonl

- Path: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p9_repaired_oof_663d9bc7.jsonl`
- Rows: 1
- Outcome columns: ['brier_skill_score']
- Postgame keyword hits: ['brier_skill_score']
- Reasons: ["outcome_columns_present: ['brier_skill_score']"]

### bad_source.csv

- Path: `outputs/predictions/PAPER/__pytest_p8_deep_diag__/bad_source.csv`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['Home Score', 'Away Score']
- Reasons: ["postgame_keyword_columns: ['Home Score', 'Away Score']", 'no_pregame_keywords_found']

### oof_model.csv

- Path: `outputs/predictions/PAPER/__pytest_p8_deep_diag__/oof_model.csv`
- Rows: 20
- Outcome columns: []
- Postgame keyword hits: ['Home Score', 'Away Score']
- Reasons: ["postgame_keyword_columns: ['Home Score', 'Away Score']", 'no_pregame_keywords_found']

### raw_model.csv

- Path: `outputs/predictions/PAPER/__pytest_p8_deep_diag__/raw_model.csv`
- Rows: 20
- Outcome columns: []
- Postgame keyword hits: ['Home Score', 'Away Score']
- Reasons: ["postgame_keyword_columns: ['Home Score', 'Away Score']", 'no_pregame_keywords_found']

### model_deep_diagnostics_oof.json

- Path: `outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_oof.json`
- Rows: 1
- Outcome columns: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Postgame keyword hits: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Reasons: ["outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']"]

### model_deep_diagnostics_raw.json

- Path: `outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_raw.json`
- Rows: 1
- Outcome columns: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Postgame keyword hits: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Reasons: ["outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']"]

### model_probability_audit.json

- Path: `outputs/predictions/PAPER/2026-05-11/model_probability_audit.json`
- Rows: 1
- Outcome columns: ['brier_skill_score', 'orientation_checks.home_win_rate_when_model_gt_0_5', 'orientation_checks.home_win_rate_when_model_lt_0_5', 'avg_outcome', 'missing_outcome_count', 'orientation_checks.avg_model_prob_when_home_wins']
- Postgame keyword hits: ['brier_skill_score', 'orientation_checks.home_win_rate_when_model_gt_0_5', 'orientation_checks.home_win_rate_when_model_lt_0_5', 'avg_outcome', 'missing_outcome_count', 'orientation_checks.avg_model_prob_when_home_wins']
- Reasons: ["outcome_columns_present: ['brier_skill_score', 'orientation_checks.home_win_rate_when_model_gt_0_5', 'orientation_checks.home_win_rate_when_model_lt_0_5', 'avg_outcome', 'missing_outcome_count', 'orientation_checks.avg_model_prob_when_home_wins']"]

### model_deep_diagnostics_oof.json

- Path: `outputs/predictions/PAPER/__pytest_p8_deep_diag__/model_deep_diagnostics_oof.json`
- Rows: 1
- Outcome columns: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Postgame keyword hits: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Reasons: ["outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']"]

### model_deep_diagnostics_raw.json

- Path: `outputs/predictions/PAPER/__pytest_p8_deep_diag__/model_deep_diagnostics_raw.json`
- Rows: 1
- Outcome columns: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Postgame keyword hits: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']
- Reasons: ["outcome_columns_present: ['brier_skill_score', 'outcome_diagnostics.outcome_null_count', 'outcome_diagnostics.outcome_one_count', 'outcome_diagnostics.outcome_balance', 'outcome_diagnostics', 'outcome_diagnostics.outcome_zero_count', 'avg_home_win_rate']"]

### replay_default_validation_ci_verification_report.json

- Path: `outputs/replay/replay_default_validation_ci_verification_report.json`
- Rows: 1
- Outcome columns: ['local_fixture_results.overall', 'local_fixture_results.aligned', 'local_fixture_results.mismatch', 'local_fixture_results', 'browser_lane_result', 'local_fixture_results.multi_state', 'local_fixture_results.browser']
- Postgame keyword hits: ['local_fixture_results.overall', 'local_fixture_results.aligned', 'local_fixture_results.mismatch', 'local_fixture_results', 'browser_lane_result', 'local_fixture_results.multi_state', 'local_fixture_results.browser']
- Reasons: ["outcome_columns_present: ['local_fixture_results.overall', 'local_fixture_results.aligned', 'local_fixture_results.mismatch', 'local_fixture_results', 'browser_lane_result', 'local_fixture_results.multi_state', 'local_fixture_results.browser']"]

### mlb_paper_betting_ledger.jsonl

- Path: `reports/mlb_paper_betting_ledger.jsonl`
- Rows: 13
- Outcome columns: ['result_status', 'realized_outcome']
- Postgame keyword hits: ['paper_profit_loss_units', 'result_status', 'closing_market_prob', 'realized_outcome']
- Reasons: ["outcome_columns_present: ['result_status', 'realized_outcome']"]

### mlb_paper_betting_reviewed_snapshot_20250701.jsonl

- Path: `reports/mlb_paper_betting_reviewed_snapshot_20250701.jsonl`
- Rows: 7
- Outcome columns: ['result_status', 'realized_outcome']
- Postgame keyword hits: ['paper_profit_loss_units', 'result_status', 'realized_outcome']
- Reasons: ["outcome_columns_present: ['result_status', 'realized_outcome']"]

### mlb_paper_betting_reviewed_snapshot_20260507.jsonl

- Path: `reports/mlb_paper_betting_reviewed_snapshot_20260507.jsonl`
- Rows: 13
- Outcome columns: ['result_status', 'realized_outcome']
- Postgame keyword hits: ['paper_profit_loss_units', 'result_status', 'realized_outcome']
- Reasons: ["outcome_columns_present: ['result_status', 'realized_outcome']"]

### metrics_ssot_phase67_72_inventory_20260507.json

- Path: `reports/metrics_ssot_phase67_72_inventory_20260507.json`
- Rows: 1
- Outcome columns: ['phase_scan_results']
- Postgame keyword hits: ['phase_scan_results']
- Reasons: ["outcome_columns_present: ['phase_scan_results']"]

### mlb_current_source_probe_20260507.json

- Path: `reports/mlb_current_source_probe_20260507.json`
- Rows: 1
- Outcome columns: ['market_coverage.result_available', 'source_health.result_games']
- Postgame keyword hits: ['market_coverage.result_available', 'market_coverage.closing_market_available', 'source_health.result_games']
- Reasons: ["outcome_columns_present: ['market_coverage.result_available', 'source_health.result_games']"]

### mlb_daily_advisory_dry_run_20250701.json

- Path: `reports/mlb_daily_advisory_dry_run_20250701.json`
- Rows: 1
- Outcome columns: ['review_summary.pending_result_count', 'market_coverage_matrix_summary.result_available']
- Postgame keyword hits: ['review_summary.pending_result_count', 'review_summary.win_loss_push_summary.lost', 'actual_date_used', 'market_coverage_matrix_summary.result_available', 'review_summary.win_loss_push_summary.push', 'actual_today_schedule_unavailable', 'review_summary.win_loss_push_summary.unknown', 'review_summary.win_loss_push_summary', 'market_coverage_matrix_summary.closing_market_available', 'review_summary.win_loss_push_summary.won']
- Reasons: ["outcome_columns_present: ['review_summary.pending_result_count', 'market_coverage_matrix_summary.result_available']"]

### mlb_daily_advisory_dry_run_20260507.json

- Path: `reports/mlb_daily_advisory_dry_run_20260507.json`
- Rows: 1
- Outcome columns: ['review_summary.pending_result_count', 'market_coverage_matrix_summary.result_available']
- Postgame keyword hits: ['review_summary.pending_result_count', 'review_summary.win_loss_push_summary.lost', 'actual_date_used', 'market_coverage_matrix_summary.result_available', 'review_summary.win_loss_push_summary.push', 'actual_today_schedule_unavailable', 'review_summary.win_loss_push_summary.unknown', 'review_summary.win_loss_push_summary', 'market_coverage_matrix_summary.closing_market_available', 'review_summary.win_loss_push_summary.won']
- Reasons: ["outcome_columns_present: ['review_summary.pending_result_count', 'market_coverage_matrix_summary.result_available']"]

### mlb_daily_scheduler_manifest_20250701.json

- Path: `reports/mlb_daily_scheduler_manifest_20250701.json`
- Rows: 1
- Outcome columns: ['brier_score']
- Postgame keyword hits: ['postgame_warnings', 'postgame_failure_reason', 'brier_score', 'postgame_review_status']
- Reasons: ["outcome_columns_present: ['brier_score']"]

### mlb_daily_scheduler_manifest_20260507.json

- Path: `reports/mlb_daily_scheduler_manifest_20260507.json`
- Rows: 1
- Outcome columns: ['brier_score']
- Postgame keyword hits: ['postgame_warnings', 'postgame_failure_reason', 'brier_score', 'postgame_review_status']
- Reasons: ["outcome_columns_present: ['brier_score']"]

### mlb_live_source_plan_20260507.json

- Path: `reports/mlb_live_source_plan_20260507.json`
- Rows: 1
- Outcome columns: ['contracts.result_source_contract.governance_flags.paper_only', 'contracts.result_source_contract.fallback_behavior', 'contracts.result_source_contract.governance_flags.human_review_required_for_cancelled', 'source_candidate_summary.result_candidates', 'contracts.result_source_contract.governance_flags.no_auto_result_fabrication', 'contracts.result_source_contract.allowed_missing_fields', 'contracts.result_source_contract.governance_flags.no_real_bet', 'contracts.result_source_contract.unavailable_behavior', 'contracts.result_source_contract.freshness_sla_minutes', 'contracts.result_source_contract.governance_flags.human_review_required_for_suspended', 'contracts.result_source_contract.governance_flags', 'contracts.result_source_contract.validation_rules', 'contracts.result_source_contract.contract_id', 'contracts.result_source_contract.optional_fields', 'contracts.result_source_contract.required_fields', 'contracts.result_source_contract']
- Postgame keyword hits: ['contracts.odds_source_contract.normalization_contract.closing_line_available', 'contracts.result_source_contract.governance_flags.paper_only', 'contracts.result_source_contract.fallback_behavior', 'contracts.result_source_contract.governance_flags.human_review_required_for_cancelled', 'source_candidate_summary.result_candidates', 'contracts.result_source_contract.governance_flags.no_auto_result_fabrication', 'contracts.result_source_contract.allowed_missing_fields', 'odds_normalization_contract.output_fields.closing_line_available', 'contracts.odds_source_contract.governance_flags.no_closing_line_exploitation', 'contracts.result_source_contract.governance_flags.no_real_bet']
- Reasons: ["outcome_columns_present: ['contracts.result_source_contract.governance_flags.paper_only', 'contracts.result_source_contract.fallback_behavior', 'contracts.result_source_contract.governance_flags.human_review_required_for_cancelled', 'source_candidate_summary.result_candidates', 'contracts.result_source_contract.governance_flags.no_auto_result_fabrication', 'contracts.result_source_contract.allowed_missing_fields', 'contracts.result_source_contract.governance_flags.no_real_bet', 'contracts.result_source_contract.unavailable_behavior', 'contracts.result_source_contract.freshness_sla_minutes', 'contracts.result_source_contract.governance_flags.human_review_required_for_suspended', 'contracts.result_source_contract.governance_flags', 'contracts.result_source_contract.validation_rules', 'contracts.result_source_contract.contract_id', 'contracts.result_source_contract.optional_fields', 'contracts.result_source_contract.required_fields', 'contracts.result_source_contract']"]

### mlb_postgame_review_20250701.json

- Path: `reports/mlb_postgame_review_20250701.json`
- Rows: 1
- Outcome columns: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'review_summary.pending_results']
- Postgame keyword hits: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'review_summary.pending_results']
- Reasons: ["outcome_columns_present: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'review_summary.pending_results']"]

### mlb_postgame_review_20260507.json

- Path: `reports/mlb_postgame_review_20260507.json`
- Rows: 1
- Outcome columns: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'review_summary.pending_results']
- Postgame keyword hits: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'review_summary.pending_results']
- Reasons: ["outcome_columns_present: ['review_summary.brier_score', 'review_summary.matched_results', 'total_result_snapshots', 'review_summary.pending_results']"]

### phase53_sp_coefficient_calibration_2026-05-05.json

- Path: `reports/phase53_sp_coefficient_calibration_2026-05-05.json`
- Rows: 1
- Outcome columns: ['coefficient_grid_results']
- Postgame keyword hits: ['coefficient_grid_results']
- Reasons: ["outcome_columns_present: ['coefficient_grid_results']"]

### phase55_sp_vs_bullpen_diagnosis_2026-05-05.json

- Path: `reports/phase55_sp_vs_bullpen_diagnosis_2026-05-05.json`
- Rows: 1
- Outcome columns: ['bullpen_diagnosis.bullpen_missing_score', 'functional_form_results']
- Postgame keyword hits: ['bullpen_diagnosis.bullpen_missing_score', 'functional_form_results']
- Reasons: ["outcome_columns_present: ['bullpen_diagnosis.bullpen_missing_score', 'functional_form_results']"]

### phase59_real_bullpen_boxscore_acquisition_20260506.json

- Path: `reports/phase59_real_bullpen_boxscore_acquisition_20260506.json`
- Rows: 1
- Outcome columns: ['heavy_fav_signal.home_win_rate', 'high_conf_signal.home_win_rate']
- Postgame keyword hits: ['heavy_fav_signal.home_win_rate', 'heavy_fav_signal.fatigue_win_rate_delta', 'high_conf_signal.fatigue_win_rate_delta', 'high_conf_signal.rested_fav_win_rate', 'high_conf_signal.home_win_rate', 'heavy_fav_signal.rested_fav_win_rate', 'heavy_fav_signal.tired_fav_win_rate', 'high_conf_signal.tired_fav_win_rate']
- Reasons: ["outcome_columns_present: ['heavy_fav_signal.home_win_rate', 'high_conf_signal.home_win_rate']"]

### phase64_granular_bullpen_attribution_20260506.json

- Path: `reports/phase64_granular_bullpen_attribution_20260506.json`
- Rows: 1
- Outcome columns: ['oof_results']
- Postgame keyword hits: ['phase60_baseline_replication.heavy_fav_bucket_attribution.win_rate_high', 'oof_results', 'phase60_baseline_replication.heavy_fav_bucket_attribution.win_rate_low', 'phase60_baseline_replication.heavy_fav_bucket_attribution.win_rate_delta']
- Reasons: ["outcome_columns_present: ['oof_results']"]

### phase64b_full_season_bullpen_ingestion_and_attribution_20260506.json

- Path: `reports/phase64b_full_season_bullpen_ingestion_and_attribution_20260506.json`
- Rows: 1
- Outcome columns: ['oof_results']
- Postgame keyword hits: ['phase60_baseline_replication.heavy_fav_bucket_attribution.win_rate_high', 'oof_results', 'phase60_baseline_replication.heavy_fav_win_rate', 'phase60_baseline_replication.heavy_fav_bucket_attribution.win_rate_low', 'phase60_baseline_replication.heavy_fav_bucket_attribution.win_rate_delta']
- Reasons: ["outcome_columns_present: ['oof_results']"]

### phase65_sp_fatigue_attribution_20260506.json

- Path: `reports/phase65_sp_fatigue_attribution_20260506.json`
- Rows: 1
- Outcome columns: ['oof_results']
- Postgame keyword hits: ['oof_results']
- Reasons: ["outcome_columns_present: ['oof_results']"]

### phase66_market_microstructure_failure_attribution_20260506.json

- Path: `reports/phase66_market_microstructure_failure_attribution_20260506.json`
- Rows: 1
- Outcome columns: ['oof_results']
- Postgame keyword hits: ['extreme_fav_metrics.win_rate', 'heavy_fav_metrics.win_rate', 'high_conf_metrics.fav_win_rate', 'oof_results', 'all_metrics.win_rate', 'phase45_failure_metrics.fav_win_rate', 'phase45_failure_metrics.win_rate', 'high_conf_metrics.win_rate', 'all_metrics.fav_win_rate', 'heavy_fav_metrics.fav_win_rate']
- Reasons: ["outcome_columns_present: ['oof_results']"]

### phase67_context_failure_attribution_20260506.json

- Path: `reports/phase67_context_failure_attribution_20260506.json`
- Rows: 1
- Outcome columns: ['oof_results']
- Postgame keyword hits: ['heavy_fav_metrics.win_rate', 'high_conf_metrics.fav_win_rate', 'oof_results', 'all_metrics.win_rate', 'phase45_failure_metrics.fav_win_rate', 'phase45_failure_metrics.win_rate', 'high_conf_metrics.win_rate', 'all_metrics.fav_win_rate', 'heavy_fav_metrics.fav_win_rate']
- Reasons: ["outcome_columns_present: ['oof_results']"]

### phase68_model_architecture_ensemble_failure_audit_20260506.json

- Path: `reports/phase68_model_architecture_ensemble_failure_audit_20260506.json`
- Rows: 1
- Outcome columns: []
- Postgame keyword hits: ['model_band_75_plus.fav_win_rate', 'high_conf_metrics.fav_win_rate', 'model_band_60_65.fav_win_rate', 'phase45_failure_metrics.fav_win_rate', 'model_band_70_75.fav_win_rate', 'all_metrics.fav_win_rate', 'heavy_fav_metrics.fav_win_rate', 'extreme_fav_metrics.fav_win_rate', 'model_band_65_70.fav_win_rate']
- Reasons: ["postgame_keyword_columns: ['model_band_75_plus.fav_win_rate', 'high_conf_metrics.fav_win_rate', 'model_band_60_65.fav_win_rate', 'phase45_failure_metrics.fav_win_rate', 'model_band_70_75.fav_win_rate', 'all_metrics.fav_win_rate', 'heavy_fav_metrics.fav_win_rate', 'extreme_fav_metrics.fav_win_rate', 'model_band_65_70.fav_win_rate']", 'no_pregame_keywords_found']

### phase71_market_dominance_model_derisk_audit_20260507.json

- Path: `reports/phase71_market_dominance_model_derisk_audit_20260507.json`
- Rows: 1
- Outcome columns: ['split_market_results', 'sp_fip_attribution.sp_fip_vs_outcome_residual_corr']
- Postgame keyword hits: ['split_market_results', 'sp_fip_attribution.sp_fip_vs_outcome_residual_corr']
- Reasons: ["outcome_columns_present: ['split_market_results', 'sp_fip_attribution.sp_fip_vs_outcome_residual_corr']"]


---
paper_only: true
production_enablement_attempted: false