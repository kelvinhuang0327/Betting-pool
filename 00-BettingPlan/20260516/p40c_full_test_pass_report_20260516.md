# P40C Full Test Pass Report
**Date:** 2026-05-16  
**Branch:** `codex/consolidate-p13-clean-20260516`  
**paper_only:** True | **production_ready:** False

---

## Test Execution Summary

| Metric | Value |
|--------|-------|
| Tests run | 153 |
| Passed | **153** |
| Failed | **0** |
| Skipped | 2 |
| Duration | ~6 seconds |
| Python | `.venv` (Betting-pool local environment) |

---

## Test Files Executed (11 files)

| File | Tests | Result |
|------|-------|--------|
| `test_p38a_retrosheet_feature_adapter.py` | 7 | ✅ PASS |
| `test_p38a_oof_prediction_builder.py` | 8 | ✅ PASS |
| `test_run_p38a_2024_oof_prediction_rebuild.py` | 5 | ✅ PASS |
| `test_tsl_market_schema.py` | 11 | ✅ PASS |
| `test_p39i_walkforward_feature_ablation.py` | 15 | ✅ PASS |
| `test_p39b_pybaseball_leakage_policy.py` | ~22 | ✅ PASS |
| `test_p39b_pybaseball_feature_aggregation.py` | ~20 | ✅ PASS |
| `test_p39c_feature_join_contract.py` | ~18 | ✅ PASS |
| `test_team_code_normalization.py` | ~20 | ✅ PASS |
| `test_p39f_p38a_bridge_enrichment.py` | ~15 | ✅ PASS |
| `test_p39h_enriched_model_comparison.py` | ~14 | ✅ PASS |

2 skipped: CLI tests that require real CSV input (`test_cli_exit_code_on_ready`, `test_cli_gate_json_paper_only_flag`) — skipped because `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` is not present in Betting-pool (it is a p13-only processed artifact). This is expected and non-blocking.

---

## First-Run Issues (Resolved)

P40C first run had 5 import errors due to missing dependency scripts not copied in P40B:

| Missing Script | Required By |
|----------------|------------|
| `scripts/build_pybaseball_pregame_features_2024.py` | `test_p39b_pybaseball_*.py` |
| `scripts/join_p38a_oof_with_p39b_features.py` | `test_p39c_feature_join_contract.py` |
| `scripts/team_code_normalization.py` | `test_team_code_normalization.py` |
| `scripts/enrich_p38a_with_identity_bridge.py` | `test_p39f_p38a_bridge_enrichment.py` |

All 4 scripts copied from `origin/p13-clean` via `git checkout origin/p13-clean -- <file>`. No blind merge. Re-run: 153 passed.

---

## Environment Notes

- No production write
- No odds data accessed
- No live API called
- All tests use synthetic fixtures or public Retrosheet data references
- `data/mlb_2024/processed/` not present in Betting-pool (2 tests skip gracefully)

---

## Acceptance Marker

`P40C_FULL_TEST_SUITE_PASS_20260516`
