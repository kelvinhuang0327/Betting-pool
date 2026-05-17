# P13 → Betting-pool Merge Manifest
**Date:** 2026-05-16  
**Source:** `origin/p13-clean` (SHA: `1b50704`)  
**Target:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` (`main`, `e765b3b`)  
**Diff base:** `origin/main..origin/p13-clean` — **90 commits**, ~500+ files  
**paper_only:** True | **production_ready:** False

---

## Merge Strategy

> **Do NOT run `git merge origin/p13-clean` blindly.**  
> The p13-clean branch diverged from a different state of `main` (it branched from commit `e765b3b` but the canonical `Betting-pool/main` is `38 ahead, 1 behind` of origin/main with heavy dirty state).  
> Safe path: create a consolidation branch, selectively copy/cherry-pick by category.

---

## Category 1 — ALLOW: Code / Tests / Scripts

These files contain no secrets, no odds data, no generated artifacts. Safe to merge into canonical repo.

### `wbc_backend/` — New modules (P13–P38A/P39A-I)

| Subcategory | Count | Key files |
|-------------|-------|-----------|
| `wbc_backend/recommendation/p3*.py` | ~35 | P31–P37 recommendation pipeline |
| `wbc_backend/recommendation/p38a_*.py` | 2 | `p38a_retrosheet_feature_adapter.py`, `p38a_oof_prediction_builder.py` |
| `wbc_backend/markets/` | 2 | `__init__.py`, `tsl_market_schema.py` |
| `wbc_backend/features/p39b*.py` + related | ~5 | pybaseball feature core |
| `wbc_backend/simulation/p13_strategy_simulator.py` | 1 | Walk-forward simulator |
| `wbc_backend/simulation/p18_*.py` | 3 | Strategy policy grid + diagnostics |
| Other `wbc_backend/` updates | ~50 | research, strategy, reporting, scheduler |

### `scripts/` — New scripts

| File | Description |
|------|-------------|
| `scripts/run_p38a_2024_oof_prediction_rebuild.py` | P38A OOF prediction CLI |
| `scripts/run_p39i_walkforward_feature_ablation.py` | P39I walk-forward ablation CLI |
| `scripts/run_p39h_enriched_feature_model_comparison.py` | P39H model comparison CLI |
| `scripts/rebuild_ml_artifacts.py` | ML artifact rebuild |
| `scripts/run_postgame_sync.py` | Postgame sync |
| `scripts/run_mlb_backtest.py` | MLB backtest |
| Other scripts (~20) | Various build/run scripts |

### `tests/` — New and updated tests

| File | Description |
|------|-------------|
| `tests/test_p38a_retrosheet_feature_adapter.py` | P38A adapter (7 tests) |
| `tests/test_p38a_oof_prediction_builder.py` | P38A OOF builder (8 tests) |
| `tests/test_run_p38a_2024_oof_prediction_rebuild.py` | P38A CLI (5 tests) |
| `tests/test_tsl_market_schema.py` | TSL market schema (11 tests) |
| `tests/test_p39i_walkforward_feature_ablation.py` | P39I ablation (15 tests) |
| `tests/test_p39b_*.py`, `test_p39c_*.py`, etc. | P39A-H test suite |
| Other test updates (~30 files) | Institutional system, model, feature tests |

### `.github/` — Workflow updates

| File | Notes |
|------|-------|
| `.github/workflows/daily_update.yml` | Updated CI workflow |
| `.github/workflows/replay_default_validation.yml` | Replay validation CI |
| `.github/skills/analyze-wbc-betting/SKILL.md` | Skill definition |
| `.github/skills/update-wbc-data/SKILL.md` | Skill definition |

### `.gitignore` — Updated ignore rules

Safe to merge. Contains local_only/outputs/runtime ignore patterns.

---

## Category 2 — ALLOW WITH REVIEW: Docs / Planning

| Directory | Count | Notes |
|-----------|-------|-------|
| `00-BettingPlan/20260511/` | 10 docs | P0–P12 reports |
| `00-BettingPlan/20260512/` | 20 docs | P13–P30 reports |
| `00-BettingPlan/20260513/` | 50+ docs | P31–P39J docs, CTO gate, odds assessment |

All markdown — no secrets. Safe to merge.

---

## Category 3 — SAFE_FIXTURE_EXCEPTION: Synthetic Fixtures

| File | Status | Justification |
|------|--------|--------------|
| `data/research_odds/fixtures/README.md` | ✅ SAFE | Documentation only |
| `data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv` | ✅ SAFE_FIXTURE_EXCEPTION | Synthetic schema template, no real odds |
| `data/research_odds/fixtures/P38A_JOIN_SMOKE_TEMPLATE_20260514.csv` | ✅ SAFE_FIXTURE_EXCEPTION | 5 rows, `source_license_status: synthetic_no_license`, notes: "FIXTURE ONLY — dummy odds" |

These contain fabricated values for smoke-testing the schema contract. They do not represent real licensed odds. Allowed under the fixture exception.

---

## Category 4 — ALLOW WITH REVIEW: Processed MLB 2024 Data

| File | Status | Notes |
|------|--------|-------|
| `data/mlb_2024/processed/mlb_2024_game_identity.csv` | ✅ ALLOW | Retrosheet-derived public data |
| `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` | ✅ ALLOW | 2429 rows, Retrosheet public |
| `data/mlb_2024/processed/mlb_2024_game_outcomes.csv` | ✅ ALLOW | Retrosheet public |
| `data/mlb_2024/processed/mlb_2024_game_log_manifest.json` | ✅ ALLOW | Metadata only |
| `data/mlb_2024/processed/mlb_2024_game_log_summary.json` | ✅ ALLOW | Summary stats |
| `data/mlb_2024/processed/mlb_2024_retrosheet_provenance.json` | ✅ ALLOW | Provenance record |
| `data/mlb_2024/processed/p32_gate_result.json` | ✅ ALLOW | Gate result artifact |
| `data/mlb_2024/processed/p33_joined_input_gap/` | ⚠️ REVIEW | Gap analysis artifacts — no odds, but review size |
| `data/mlb_2024/processed/p34_dual_source_acquisition/` | ⚠️ REVIEW | Acquisition plan artifacts |
| `data/mlb_2024/processed/p35_*/`, `p36_*/`, `p37_*/` | ⚠️ REVIEW | Validation/approval artifacts |

---

## Category 5 — ALLOW WITH REVIEW: Outputs / PAPER predictions

| File | Status | Notes |
|------|--------|-------|
| `outputs/predictions/PAPER/p39h_enriched_feature_model_comparison_20260515.json` | ⚠️ REVIEW | Metrics-only JSON, no odds — likely safe |
| `outputs/predictions/PAPER/p39i_walkforward_feature_ablation_20260515.json` | ⚠️ REVIEW | Metrics-only JSON — likely safe |
| `outputs/replay/replay_default_validation_*.json` | ⚠️ REVIEW | CI replay artifacts |
| `outputs/predictions/PAPER/p38a_2024_oof/` | ⚠️ REVIEW | OOF prediction CSV — check size before committing |

---

## Category 6 — FORBIDDEN: Never Merge

| File / Pattern | Reason |
|----------------|--------|
| `data/pybaseball/local_only/*` | Raw Statcast data — local_only, gitignored |
| `data/research_odds/local_only/*` | Raw odds data — local_only, gitignored |
| `outputs/predictions/PAPER/2026-05-*/` | Daily generated outputs |
| `runtime/` | Orchestrator state, DB files |
| `*.db`, `*.db-wal`, `*.db-shm` | Binary DB files |
| `.env` | API secrets |
| `data/mlb_2024/raw/gl2024.txt` | Raw Retrosheet binary |
| `data/mlb_2024/manual_import/` | Manual import staging |

---

## Merge Execution Plan (Dry-Run — Not Yet Executed)

```bash
# 1. Create consolidation branch in Betting-pool
git checkout -b codex/consolidate-p13-clean-20260516

# 2. Add p13 remote temporarily
git remote add p13-source https://github.com/kelvinhuang0327/Betting-pool.git
git fetch p13-source p13-clean

# 3. Selectively copy safe files using git checkout
git checkout p13-source/p13-clean -- \
  wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py \
  wbc_backend/recommendation/p38a_oof_prediction_builder.py \
  wbc_backend/markets/__init__.py \
  wbc_backend/markets/tsl_market_schema.py \
  scripts/run_p38a_2024_oof_prediction_rebuild.py \
  scripts/run_p39i_walkforward_feature_ablation.py \
  tests/test_p38a_retrosheet_feature_adapter.py \
  tests/test_p38a_oof_prediction_builder.py \
  tests/test_tsl_market_schema.py \
  tests/test_p39i_walkforward_feature_ablation.py \
  # ... etc per Category 1/2/3 list above

# 4. Verify forbidden-file check
git diff --cached --name-only | grep -E "\.env|\.db|local_only|odds_real|raw"

# 5. Commit on consolidation branch (do NOT push to main yet)
git commit -m "chore: consolidate P38A/P39A-I code from p13-clean"
```

**Status: DRY-RUN ONLY — not executed this round.**
