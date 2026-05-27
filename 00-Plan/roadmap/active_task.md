# Active Task — P84A 2026 Upstream Data Collector Contract

> **[COMPLETED 2026-05-26]** `P84A_UPSTREAM_COLLECTOR_CONTRACT_READY`
> **Issued by**: P83E handoff (P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA, commit `1d295b5`)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=True`
>
> **P84A Result:** Upstream data collector contract fully defined.
> P83E remains blocked (P83E state: P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA).
> Three contracts defined: schedule / pitcher FIP / model output.
> Allowed source classes: MLB_STATS_API_PUBLIC_SCHEDULE, MLB_STATS_API_PUBLIC_PLAYER_STATS,
> LOCAL_PUBLIC_STATS_EXPORT, MANUAL_PUBLIC_STATS_FIXTURE, MOCK_SCHEMA_ONLY_FIXTURE.
> Mock schema-only fixture (3 games, all schemas) validated as noncanonical.
> No upstream files written. No canonical prediction rows written.
>
> **Upstream target file status:**
> - data/mlb_2026/schedule/mlb_2026_schedule.jsonl → Missing
> - data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl → Missing
> - data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl → Missing
>
> **Contracts defined:**
> - P84A_SCHEDULE_COLLECTOR_CONTRACT_V1 (endpoint: statsapi.mlb.com/api/v1/schedule)
> - P84A_PITCHER_FIP_CONTRACT_V1 (endpoint: statsapi.mlb.com/api/v1/people/{id}/stats)
> - P84A_MODEL_OUTPUT_CONTRACT_V1 (2025-trained ensemble applied to 2026 feature rows)
>
> **P83E rerun trigger:**
> All 3 upstream files must be locally present and schema-valid.
>
> **Next phase:** P84B — Public Stats Collector Implementation
> **Output artifacts:**
> - `scripts/_p84a_2026_upstream_data_collector_contract.py`
> - `tests/test_p84a_2026_upstream_data_collector_contract.py`
> - `data/mlb_2026/derived/p84a_2026_upstream_data_collector_contract_summary.json`
> - `report/p84a_2026_upstream_data_collector_contract_20260526.md`

<!-- Prior phase completion markers (required by regression tests) -->
<!-- P72A: P72A_ODDS_FREE_STRATEGY_ACCURACY_BACKTEST_READY -->
<!-- P72B: P72B_OBJECTIVE_METRIC_CONTRACT_READY -->
<!-- P73: P73_TIER_STABILITY_AND_SAMPLE_EXPANSION_READY -->
<!-- P74: P74_TIER_C_HOME_AWAY_BIAS_CORRECTION_READY -->
<!-- P75A: P75A_TIER_C_CORRECTED_RULE_VALIDATOR_READY -->
<!-- P77: P77_PREDICTION_ONLY_SHADOW_TRACKER_CONTRACT_READY -->
<!-- P78: P78_MONTHLY_SHADOW_TRACKER_REPORT_TEMPLATE_READY -->
<!-- P79A: P79A_TIER_B_TRIGGER_READINESS_CONTRACT_READY -->
<!-- P79B: P79B_TIER_B_VS_TIER_C_COMPARISON_HARNESS_READY -->
<!-- P80: P80_MARKET_EDGE_REENTRY_READINESS_CONTRACT_READY -->
<!-- P81: P81_LEGAL_ODDS_DATASET_VALIDATOR_CONTRACT_READY -->
<!-- P82: P82B_RAW_PAID_DATA_POLICY_READY / P82C_STAGING_GUARD_DRYRUN_READY -->
<!-- P82B: P82B_RAW_PAID_DATA_POLICY_READY -->
<!-- P82C: P82C_STAGING_GUARD_DRYRUN_READY -->
<!-- P83A: P83A_AWAITING_2026_DATA -->
<!-- P83C: P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA -->
<!-- P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA confirmed -->
