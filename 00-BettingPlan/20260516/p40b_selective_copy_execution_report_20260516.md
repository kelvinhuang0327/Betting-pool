# P40B Selective Copy Execution Report — 20260516

**Source**: origin/p13-clean (SHA: 1b50704)
**Target branch**: codex/consolidate-p13-clean-20260516
**Date**: 2026-05-17

---

## Execution Method

Used `git checkout origin/p13-clean -- <file>` for each allowlisted file individually.
- No `git merge` executed
- No `git checkout origin/p13-clean -- .` (no wildcard whole-dir checkout)
- No `git checkout origin/p13-clean -- data/` (no whole data dir checkout)
- No `git checkout origin/p13-clean -- wbc_backend/` (no whole wbc_backend dir)

---

## Files Copied (138 total staged)

### Core Python Modules (7 files)
- `wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py`
- `wbc_backend/recommendation/p38a_oof_prediction_builder.py`
- `wbc_backend/markets/__init__.py`
- `wbc_backend/markets/tsl_market_schema.py`
- `scripts/run_p38a_2024_oof_prediction_rebuild.py`
- `scripts/run_p39i_walkforward_feature_ablation.py`
- `scripts/run_p39h_enriched_feature_model_comparison.py`

### Test Files (11 files)
- `tests/test_p38a_retrosheet_feature_adapter.py`
- `tests/test_p38a_oof_prediction_builder.py`
- `tests/test_run_p38a_2024_oof_prediction_rebuild.py`
- `tests/test_tsl_market_schema.py`
- `tests/test_p39i_walkforward_feature_ablation.py`
- `tests/test_p39h_enriched_model_comparison.py`
- `tests/test_p39b_pybaseball_leakage_policy.py`
- `tests/test_p39b_pybaseball_feature_aggregation.py`
- `tests/test_p39c_feature_join_contract.py`
- `tests/test_team_code_normalization.py`
- `tests/test_p39f_p38a_bridge_enrichment.py`

### Synthetic Fixtures — SAFE_FIXTURE_EXCEPTION (3 files)
- `data/research_odds/fixtures/README.md`
- `data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv`
- `data/research_odds/fixtures/P38A_JOIN_SMOKE_TEMPLATE_20260514.csv`

### PAPER Metrics-only JSON (2 files)
- `outputs/predictions/PAPER/p39h_enriched_feature_model_comparison_20260515.json`
- `outputs/predictions/PAPER/p39i_walkforward_feature_ablation_20260515.json`

### Planning Docs (115 files)
- `00-BettingPlan/20260511/*.md` — 12 files
- `00-BettingPlan/20260512/*.md` — 19 files
- `00-BettingPlan/20260513/*.md` — 84 files

---

## Dirty File Conflicts

**Zero conflicts** — no allowlisted files were present in Betting-pool's dirty working tree.

Verified:
```
git status --short | grep -E "wbc_backend/recommendation/p38a|wbc_backend/markets|scripts/run_p38a|scripts/run_p39"
# → (no output)
```

---

## Post-Copy Status Summary

```
git status --short | grep "^A " | wc -l
→ 138 staged files (all new additions)
```

All files staged as `A` (new additions), none as modifications/conflicts.

---

## Marker

**P40B_SELECTIVE_COPY_EXECUTED_20260516**
