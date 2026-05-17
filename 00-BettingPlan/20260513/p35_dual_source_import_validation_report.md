# P35 Dual Source Import Validation Report

**Phase**: P35 — Dual Source Import Validation
**Date**: 2026-05-13
**Marker**: `P35_DUAL_SOURCE_IMPORT_VALIDATION_BLOCKED`
**Gate Result**: `P35_BLOCKED_ODDS_LICENSE_NOT_APPROVED`
**Exit Code**: 1 (BLOCKED)
**PAPER_ONLY**: True
**PRODUCTION_READY**: False

---

## 1. Objective

Validate whether two data sources — (A) historical market odds and (B) out-of-fold model predictions — can be imported and joined for 2024 MLB back-testing, without violating data licensing constraints or introducing look-ahead leakage.

---

## 2. Phase Prerequisites

| Prerequisite | Status |
|---|---|
| P34 `dual_source_acquisition_plan_ready` marker | ✅ Verified |
| P34 output dir `data/mlb_2024/processed/p34_dual_source_acquisition/` | ✅ Exists |
| P32 game log `mlb_2024_game_identity_outcomes_joined.csv` | ✅ Exists |
| `PAPER_ONLY=True`, `PRODUCTION_READY=False` in contract | ✅ Enforced |

---

## 3. Odds License Validation

**Source Options Loaded from P34**: 6 providers evaluated
**Approval Record**: Not provided (no `--odds-approval-record` argument)

| Check | Result |
|---|---|
| Manual approval record present | ❌ Not provided |
| Required approval fields present | N/A — no record |
| `allowed_use` in permitted values | N/A — no record |
| Schema template valid | ✅ All 11 required columns present |
| Scraping instructions | ❌ Forbidden — ToS must be approved before any download |

**Checklist items**: 12 items generated (includes source-specific ToS review steps)

**Outcome**: `LICENSE_BLOCKED_NOT_APPROVED`

**Blocker**: "Odds license is not approved. No odds may be downloaded until explicit approval record is provided."

---

## 4. Prediction Rebuild Feasibility

The existing pipeline is WBC/2025 format, not 2024 Retrosheet format.

| Component | Found |
|---|---|
| Feature pipeline candidates | ✅ 16 files |
| Model training candidates | ✅ 18 files |
| OOF generation candidates | ✅ 87 files |
| Leakage guard (temporal separation) | ✅ Present (`walk_forward_logistic.py`) |
| Time-aware split pattern | ✅ Present |
| **2024 Retrosheet format adapter** | ❌ **MISSING** |

**Feasibility Status**: `FEASIBILITY_BLOCKED_ADAPTER_MISSING`

**Key Finding**: `wbc_backend/models/walk_forward_logistic.py` uses `DefaultFeatures = ["indep_recent_win_rate_delta", "indep_starter_era_delta"]` — WBC/2025 column format. No adapter mapping P32 Retrosheet columns to these features exists.

**Note**: This is `FEASIBILITY_BLOCKED_ADAPTER_MISSING` (acceptable for P35), not `FEASIBILITY_BLOCKED_PIPELINE_MISSING`. The adapter gap will be addressed in P36.

---

## 5. Gate Priority Evaluation

| Priority | Condition | Met? | Gate Triggered |
|---|---|---|---|
| 1 | `production_ready=True` or `paper_only=False` | ❌ No | — |
| 2 | `odds_license_status == LICENSE_BLOCKED_NOT_APPROVED` | ✅ **Yes** | **`P35_BLOCKED_ODDS_LICENSE_NOT_APPROVED`** |
| 3 | `odds_source_status == "source_not_provided"` | N/A (stopped at 2) | — |
| 4 | `feature_pipeline_status == "not_found"` | N/A | — |
| 5 | Feasibility pipeline/leakage blocked | N/A | — |
| 6 | All clear | N/A | — |

**Final Gate**: `P35_BLOCKED_ODDS_LICENSE_NOT_APPROVED`

---

## 6. Validator Specs Written

| File | Status |
|---|---|
| `odds_import_validator_spec.json` | ✅ Written — 11 required columns, global rules include `no_outcome_derived_odds`, `no_scraping` |
| `prediction_import_validator_spec.json` | ✅ Written — 9 required columns, `generated_without_y_true` must be True, `no_y_true_derived_predictions` global rule |

Both specs: `paper_only=True`, `production_ready=False`

---

## 7. Output Artifacts

Location: `data/mlb_2024/processed/p35_dual_source_import_validation/`

| File | Description |
|---|---|
| `p35_gate_result.json` | Gate decision + blocker reason |
| `odds_license_validation.json` | Full odds license validation record |
| `prediction_rebuild_feasibility.json` | Prediction rebuild feasibility analysis |
| `dual_source_validation_summary.json` | Combined validation summary |
| `dual_source_validation_summary.md` | Human-readable summary |
| `odds_import_validator_spec.json` | Odds import column/rule spec |
| `prediction_import_validator_spec.json` | Prediction import column/rule spec |

---

## 8. Test Coverage

| Test File | Tests |
|---|---|
| `test_p35_dual_source_import_validation_contract.py` | 25 |
| `test_p35_odds_license_provenance_validator.py` | 26 |
| `test_p35_prediction_rebuild_feasibility_auditor.py` | 22 |
| `test_p35_import_validator_skeletons.py` | 22 |
| `test_p35_dual_source_validation_builder.py` | 22 |
| `test_run_p35_dual_source_import_validation.py` | 9 |
| **Total P35** | **108 passed** |

**Cumulative** (P31–P35): 567 + 108 = **675 passing tests**

---

## 9. Determinism Verification

Two independent runs (different temp output directories) produced identical:
- `gate`: `P35_BLOCKED_ODDS_LICENSE_NOT_APPROVED`
- `paper_only`: True
- `production_ready`: False
- `season`: 2024
- `blocker_reason`: (identical)

Excluded from comparison: `generated_at`, `output_dir`, `artifacts`

**Result**: ✅ `Determinism check PASSED`

---

## 10. Security & Leakage Guards

- **No HTTP scraping**: script contains no `requests.get`, `urllib.request`, `BeautifulSoup`
- **Data isolation**: prediction rebuild feasibility verifies `generated_without_y_true=True` constraint in all specs
- **Contract enforcement**: `PAPER_ONLY=True` and `PRODUCTION_READY=False` hardcoded; script exits 2 if contract violated
- **Raw game log guard**: `data/mlb_2024/raw/gl2024.txt` never staged or committed

---

## 11. Known Gaps (Deferred to P36)

1. **Odds acquisition approval**: Must obtain written approval from chosen provider before downloading any data
2. **2024 format adapter**: A Retrosheet → WBC-feature-pipeline adapter must be built in P36
3. **OOF prediction rebuild**: Requires P36 to implement the adapter; existing pipeline is WBC/2025 only

---

## 12. Path to P36

To unblock P36:
1. Select one of the 6 odds source options from P34
2. Obtain written ToS approval → record in `approval_record.json`
3. Build `p36_retrosheet_feature_adapter.py` mapping P32 columns to prediction feature format
4. Re-run P35 with `--odds-approval-record approval_record.json`
5. If gate = `P35_DUAL_SOURCE_IMPORT_VALIDATION_READY`, proceed to P36

---

## 13. Summary

> **P35 is BLOCKED pending odds license approval.**
>
> The validation infrastructure is complete and fully functional. All 7 output artifacts were produced, 108 tests pass, and the determinism check passed. The block is administrative (no approval record), not technical. The prediction rebuild pipeline exists but lacks a 2024-format adapter — this is the expected state and is deferred to P36.

**`P35_DUAL_SOURCE_IMPORT_VALIDATION_BLOCKED`**
