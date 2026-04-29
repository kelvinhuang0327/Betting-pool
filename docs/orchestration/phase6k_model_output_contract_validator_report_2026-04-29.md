# Phase 6K — Model Output Contract Validator Report

**Date**: 2026-04-29
**Phase**: 6K (Validator — No Code Changes, No Predictions, No Commit)
**Contract Schema Version**: 6j-1.0
**Readiness Decision**: `NOT_READY_MODEL_OUTPUT_GAP`

---

## 1. Executive Summary

Phase 6K applies the Phase 6J model output contract quality gates M1–M12 to all
candidate model output files. The validator scans the real contract target
`data/derived/model_outputs_YYYY-MM-DD.jsonl`, dry-run placeholders, and legacy
report/aggregate files to determine whether any source is registry-compatible.

**Real contract target (`model_outputs_2026-04-29.jsonl`)**: **MISSING**
**Dry-run placeholder rows**: 2080
**Legacy candidate files scanned**: 9
**Valid real model output rows (all gates pass)**: 0

**Readiness Decision: `NOT_READY_MODEL_OUTPUT_GAP`**

No real `model_outputs_YYYY-MM-DD.jsonl` file exists. All existing candidate files
are either aggregate metrics, paper-tracking retrospective reports, or WBC-domain
registry entries. None satisfies the Phase 6J per-market contract. Dry-run
placeholders confirm schema structure but remain non-CLV-usable by design.

---

## 2. Input Evidence

| File | Exists | Size | Notes |
|---|:---:|---:|---|
| `docs/orchestration/phase6j_model_output_contract_design_2026-04-29.md` | ✅ | 33,554 B | Phase 6J contract — 14 sections, 31 required fields |
| `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl` | ✅ | 2,137,566 B | Phase 6I dry-run placeholder; 2,080 rows; all `dry_run=true` |
| `data/derived/model_outputs_2026-04-29.jsonl` | ❌ | 0 B | Real contract target — **MISSING** |

---

## 3. Candidate Files Scanned

| Candidate | Exists | Rows | Looks Like Model Output | Required Fields Present | Valid Rows | Decision |
|---|:---:|---:|:---:|:---:|---:|---|
| `data/derived/model_outputs_2026-04-29.jsonl` | ❌ | 0 | ❌ | ❌ | 0 | `MISSING_REAL_MODEL_OUTPUT_FILE` |
| `future_model_predictions_dry_run_2026-04-29.jsonl` | ✅ | 2,080 | ⚠️ partial | ⚠️ partial | 0 | `DRY_RUN_PLACEHOLDER_NOT_CLV_USABLE` |
| `model_artifacts.json` | ✅ | 0 | ❌ | ❌ | 0 | `AGGREGATE_ONLY: top-level keys ['calibration', 'params', 'od` |
| `market_validation.json` | ✅ | 0 | ❌ | ❌ | 0 | `AGGREGATE_ONLY: top-level keys ['ML', 'RL', 'OU']` |
| `walkforward_summary.json` | ✅ | 0 | ❌ | ❌ | 0 | `AGGREGATE_ONLY: top-level keys ['games', 'ml_bets', 'ml_roi'` |
| `mlb_decision_quality_report.json` | ✅ | 1,493 | ❌ | ❌ | 0 | `REPORT_NOT_REGISTRY: per_game rows exist but missing contrac` |
| `mlb_paper_tracking_report.json` | ✅ | 0 | ❌ | ❌ | 0 | `AGGREGATE_ONLY: top-level keys ['status', 'governance_flags'` |
| `mlb_alpha_discovery_report.json` | ✅ | 0 | ❌ | ❌ | 0 | `AGGREGATE_ONLY: top-level keys ['research_scope', 'feature_i` |
| `mlb_model_family_report.json` | ✅ | 0 | ❌ | ❌ | 0 | `AGGREGATE_ONLY: top-level keys ['strict_valid_rate', 'promot` |
| `mlb_pregame_coverage_report.json` | ✅ | 38 | ❌ | ❌ | 0 | `REPORT_NOT_REGISTRY: per_game rows exist but missing contrac` |
| `prediction_registry.jsonl` | ✅ | 66 | ❌ | ❌ | 0 | `MISSING_CONTRACT_FIELDS: lacks ['canonical_match_id', 'predi` |

---

## 4. Contract Field Validation

### 4.1 Real Contract Target (`model_outputs_2026-04-29.jsonl`)

File does not exist. All 31 required contract fields are absent by definition.

**Gap**: All fields in the Phase 6J contract schema are unimplemented in any
current model output file. The closest existing source is
`mlb_decision_quality_report.json` which provides `predicted_home_win_prob` per
game but lacks: `canonical_match_id`, `prediction_time_utc`, `market_key`,
`selection_key`, `model_version`, `feature_version`, `leakage_guard_version`.

### 4.2 Dry-Run Placeholder

| Field Group | Fields | Dry-Run Status |
|---|---|---|
| Schema | `schema_version` | ✅ Present (`6i-dry-run-1.0`) |
| Identity | `canonical_match_id`, `sport`, `league` | ✅ Present |
| Market | `market_type`, `market_key`, `selection`, `selection_key` | ✅ Present |
| Prediction | `predicted_probability`, `prediction_time_utc` | ✅ Present (`null`) |
| Versioning | `model_version`, `feature_version`, `leakage_guard_version` | ⚠️ Present (`NOT_IMPLEMENTED`) |
| Output fields | `model_output_id`, `prediction_run_id`, `model_family` | ❌ Missing |
| Walk-forward | `training_window_id`, `walk_forward_split_id` | ❌ Missing |
| Team | `home_team_code`, `away_team_code` | ❌ Missing |
| Probability | `probability_source`, `confidence` | ⚠️ Partial |
| EV | `expected_value`, `implied_probability_at_prediction` | ✅ Present (`null`) |

---

## 5. Quality Gate Results M1–M12

### 5.1 Dry-Run Placeholder Gate Results

| Gate | Name | Pass | Fail | Block | Pass % | Notes |
|---|---|---:|---:|---:|---:|---|
| M1 | SCHEMA_VALID | 0 | 2,080 | 0 | 0.0% | ❌ |
| M2 | CANONICAL_MATCH_ID_PRESENT | 2,080 | 0 | 0 | 100.0% | ✅ |
| M3 | MARKET_KEY_PRESENT | 2,080 | 0 | 0 | 100.0% | ✅ |
| M4 | SELECTION_KEY_PRESENT | 2,080 | 0 | 0 | 100.0% | ✅ |
| M5 | VERSION_FIELDS_PRESENT | 0 | 2,080 | 0 | 0.0% | ❌ |
| M6 | TIMING_VALID | 0 | 2,080 | 0 | 0.0% | ❌ |
| M7 | PROBABILITY_VALID | 2,080 | 0 | 0 | 100.0% | ✅ |
| M8 | EV_VALID_OR_NULL_WITH_REASON | 2,080 | 0 | 0 | 100.0% | ✅ |
| M9 | NO_LEAKAGE_HARD_FAIL | 2,080 | 0 | 0 | 100.0% | ✅ |
| M10 | MARKET_SEMANTICS_VALID | 766 | 1,314 | 0 | 36.8% | ❌ |
| M11 | CLV_USABLE_FLAG_CORRECT | 2,080 | 0 | 0 | 100.0% | ✅ |
| M12 | DRY_RUN_FLAG_CORRECT | 2,080 | 0 | 0 | 100.0% | ✅ |

**Expected**: M1, M5 fail for most rows (missing contract fields in dry-run schema).
M9, M12 should pass (no leakage fields; dry_run=true consistently).
M7 should pass for dry-run rows (null predicted_probability is valid when dry_run=true).

### 5.2 Real Model Output Gate Results

No real model output file exists. All gates would fail at M1 (no rows to validate).

---

## 6. Dry-Run Placeholder Validation

File: `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl`
Rows: 2,080

### Summary

| Property | Value |
|---|---|
| `dry_run=true` count | 2,080 (all rows) |
| `clv_usable=false` count | 2,080 (all rows) |
| `predicted_probability=null` count | 2,080 (all rows) |
| `expected_value=null` count | 2,080 (all rows) |
| Schema version | `6i-dry-run-1.0` (distinct from production `6j-1.0`) |

### Finding

Dry-run placeholders correctly signal that the real prediction pipeline is not yet
operational. They validate the schema skeleton and market-splitting logic but are
**not CLV-usable** by design and must never be promoted to a real registry.

Dry-run rows lack the following Phase 6J production fields:
`model_output_id`, `prediction_run_id`, `model_family`, `training_window_id`,
`walk_forward_split_id`, `home_team_code`, `away_team_code`, `probability_source`.

---

## 7. Readiness Decision

**`NOT_READY_MODEL_OUTPUT_GAP`**

### Rationale

| Criterion | Status | Evidence |
|---|:---:|---|
| Real `model_outputs_YYYY-MM-DD.jsonl` exists | ❌ | File absent |
| Any candidate has `canonical_match_id` + `predicted_probability` + `prediction_time_utc` | ❌ | `mlb_decision_quality_report` has `predicted_home_win_prob` but no `canonical_match_id` / `prediction_time_utc` |
| Any candidate satisfies M1–M12 | ❌ | All legacy candidates fail M1 |
| Dry-run placeholders exist | ✅ | 2,080 rows, schema skeleton valid |
| Dry-run placeholders are CLV-usable | ❌ | `clv_usable=false` for all 2,080 rows |

---

## 8. Findings

### F1 — No Real Model Output File (`NOT_READY_MODEL_OUTPUT_GAP`)

`data/derived/model_outputs_2026-04-29.jsonl` does not exist. No component in the
current codebase writes per-market, per-selection predicted probabilities to a file
satisfying the Phase 6J contract.

### F2 — `mlb_decision_quality_report.json` Is Not a Registry Input

`mlb_decision_quality_report.json` contains 1,493 per-game rows with
`predicted_home_win_prob`, but it is a **paper-tracking retrospective report**,
not a real-time pre-game prediction registry. It lacks:
- `canonical_match_id` (game_id format incompatible with bridge)
- `prediction_time_utc` (timing rule T1 cannot be verified)
- `market_key` / `selection_key` (game-level only, not per-market)
- `model_version` / `feature_version` / `leakage_guard_version`

All 1,493 rows have `clv_available=false`, confirming the report itself
acknowledges they are not CLV-ready.

### F3 — Dry-Run Placeholders Are Valid as Placeholders

The 2,080 dry-run rows confirm the market-splitting logic (ML×766, RL×656, OU×658)
and the schema skeleton. They are correctly flagged `dry_run=true`, `clv_usable=false`,
`predicted_probability=null`. They must not be promoted to real predictions.

### F4 — Current Candidate Reports Are Not Real Model Outputs

The following files are aggregate metrics / legacy reports and do not qualify as
model output candidates under the Phase 6J contract:
- `model_artifacts.json` — calibration params + hyperparams only
- `market_validation.json` — aggregate ML/RL/OU ROI
- `walkforward_summary.json` — aggregate walk-forward metrics
- `mlb_paper_tracking_report.json` — `PAPER_ONLY` / `SANDBOX_ONLY` aggregate
- `prediction_registry.jsonl` — WBC-domain (not MLB/KBO/NPB), game-level

### F5 — Formal CLV Validation Must Not Run Yet

CLV hypothesis (Phase 5.5): `CLV_proxy > 0.03 → ≥3pp ROI over ≥200 bets per regime`.
This validation requires CLV-usable prediction rows with confirmed pre-game
`prediction_time_utc`. No such rows exist. Formal CLV validation is blocked.

---

## 9. Recommended Next Step

**Phase 6L — ML-Only Model Output Adapter**

The closest existing ML signal is `predicted_home_win_prob` in
`mlb_decision_quality_report.json` (1,493 per-game rows).

Phase 6L should:
1. Design an adapter that reads `mlb_decision_quality_report.json` per_game rows.
2. Resolve `canonical_match_id` via the match identity bridge.
3. Attach `prediction_time_utc` (requires backfilling from game schedule data or
   adding pre-game timestamp recording to the inference pipeline).
4. Emit ML-only rows to `data/derived/model_outputs_YYYY-MM-DD.jsonl`.
5. Apply `probability_source = 'calibrated_platt'` using `model_artifacts.json`
   calibration params (a=1.1077, b=-0.0184).
6. Validate output with this Phase 6K validator (must pass M1–M12).

**RL / OU**: Remain in `MODEL_CAPABILITY_GAP` status until Phase 6M.

---

## 10. Scope Confirmation

| Constraint | Status |
|---|---|
| Source data files modified | ❌ NOT done |
| Model code modified | ❌ NOT done |
| New predictions generated | ❌ NOT done |
| `prediction_registry.jsonl` modified | ❌ NOT done |
| Dry-run JSONL modified | ❌ NOT done |
| `mlb_decision_quality_report.json` modified | ❌ NOT done |
| Crawler modified | ❌ NOT done |
| DB or migrations modified | ❌ NOT done |
| External API called | ❌ NOT done |
| Orchestrator task created | ❌ NOT done |
| Formal CLV validation run | ❌ NOT done |
| Git commit made | ❌ NOT done |
| Lottery-domain terms used | ❌ NOT done |

---

*Phase 6K VALIDATOR_VERIFIED — token: PHASE_6K_VALIDATOR_VERIFIED*