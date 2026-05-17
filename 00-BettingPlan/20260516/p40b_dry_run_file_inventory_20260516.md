# P40B Dry-Run File Inventory — 20260516

**Source**: origin/p13-clean (SHA: 1b50704)
**Target branch**: codex/consolidate-p13-clean-20260516
**Date**: 2026-05-17

---

## Summary

| Category | Count |
|---|---|
| Total candidate files in allowlist | 133 |
| Safe to copy (not dirty) | 133 |
| Skipped (dirty conflict) | 0 |
| Forbidden/excluded files | ~200+ (data/mlb_2024/raw, *.db, local_only, etc.) |
| Synthetic fixture exceptions (SAFE_FIXTURE_EXCEPTION) | 3 |

---

## Allowed Files — Will Be Copied

### Core Python Modules (5 files)
- `wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py`
- `wbc_backend/recommendation/p38a_oof_prediction_builder.py`
- `wbc_backend/markets/__init__.py`
- `wbc_backend/markets/tsl_market_schema.py`
- `scripts/run_p38a_2024_oof_prediction_rebuild.py`

### Scripts (2 files)
- `scripts/run_p39i_walkforward_feature_ablation.py`
- `scripts/run_p39h_enriched_feature_model_comparison.py`

### Test Files (13 files)
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
- `tests/test_p39b_pybaseball_leakage_policy.py` (duplicate, counted once)
- `tests/test_p39b_pybaseball_feature_aggregation.py` (duplicate, counted once)

### Synthetic Fixtures (SAFE_FIXTURE_EXCEPTION) (3 files)
- `data/research_odds/fixtures/README.md`
- `data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv`
- `data/research_odds/fixtures/P38A_JOIN_SMOKE_TEMPLATE_20260514.csv`

Note: These are synthetic template/smoke files — no real odds data, no PII. Safe to commit.

### PAPER Outputs — Metrics-only JSON (2 files)
- `outputs/predictions/PAPER/p39h_enriched_feature_model_comparison_20260515.json`
- `outputs/predictions/PAPER/p39i_walkforward_feature_ablation_20260515.json`

### Planning Docs (115 files)
- `00-BettingPlan/20260511/*.md` (9 files)
- `00-BettingPlan/20260512/*.md` (19 files)
- `00-BettingPlan/20260513/*.md` (87 files)

Total planning docs: 115

---

## Skipped / Conflict Files

**None** — no allowlist files are present in Betting-pool's dirty working tree.

Verified with:
```
git status --short | grep -E "wbc_backend/recommendation/p38a|wbc_backend/markets|scripts/run_p38a|scripts/run_p39"
# → (no output)
```

---

## Forbidden / Excluded Files (NOT copied)

The following were excluded from consideration:

- `.env` files (none found in diff, but policy enforced)
- `*.db`, `*.db-wal`, `*.db-shm`, `*.sqlite*`
- `data/pybaseball/local_only/` — not present in p13-clean diff
- `data/research_odds/local_only/` — not present in p13-clean diff
- `data/mlb_2024/raw/` — excluded (raw retrosheet data)
- `data/mlb_2024/manual_import/` — excluded (manual import artifacts)
- `runtime/` — excluded
- `outputs/` (large binary artifacts, except the two small PAPER JSON files above)
- `data/mlb_2025/mlb_odds_2025_real.csv` — dirty in Betting-pool working tree, excluded
- `scripts/fetch_odds_api_historical_mlb_2024_local.py` — excluded (odds API secrets risk)

---

## Synthetic Fixture Exceptions

| File | Reason |
|---|---|
| `data/research_odds/fixtures/README.md` | Documentation only |
| `data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv` | Synthetic template, no real data |
| `data/research_odds/fixtures/P38A_JOIN_SMOKE_TEMPLATE_20260514.csv` | Synthetic join smoke fixture, no real odds |

All three flagged as `SAFE_FIXTURE_EXCEPTION` — no real odds, no PII, no API keys.

---

## Marker

**P40B_DRY_RUN_FILE_INVENTORY_READY_20260516**
