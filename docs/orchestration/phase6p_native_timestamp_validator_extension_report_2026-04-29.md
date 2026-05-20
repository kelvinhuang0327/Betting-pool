# Phase 6P — Native Timestamp Validator Extension Report

**Date**: 2026-04-29
**Phase**: 6P (Validator Extension — No Code Changes, No Predictions, No Commit)
**Schema Version (this phase)**: 6p-1.0
**Validator Extended**: `scripts/validate_model_output_contract.py`
**Readiness Decision**: `PARTIAL_READY_HISTORICAL_ROWS_BLOCKED`

---

## 1. Executive Summary

Phase 6P extends the Phase 6K model output contract validator
(`scripts/validate_model_output_contract.py`) to support the Phase 6O native timestamp
capture design (`docs/orchestration/phase6o_future_native_timestamp_capture_design_2026-04-29.md`).

**Extension scope (validator-only, no model/data/crawler changes):**

| Component | Change |
|---|---|
| New gate M13 | `M13_NATIVE_TIMESTAMP_CONTRACT` — all Phase 6O native fields present and valid |
| M6 extended | T4–T7 timestamp chain invariant checks (graceful skip when fields absent) |
| M9 extended | Disallowed `prediction_time_source` and hard-fail `timestamp_quality_flags` checks |
| M11 extended | Requires native timestamp compliance for `clv_usable=true` rows |
| `determine_readiness` | Returns `PARTIAL_READY_HISTORICAL_ROWS_BLOCKED` when M13 blocks all real rows |
| Summary JSON | 7 new native timestamp keys added |
| `schema_version` | Updated from `6k-1.0` to `6p-1.0` |

**Result**: All 2,986 historical rows (Phase 6L ML-adapter output) fail M13 — expected
because retrospective reconstruction cannot provide native runtime timestamps.
Readiness advances from `NOT_READY_SCHEMA_GAP` → `PARTIAL_READY_HISTORICAL_ROWS_BLOCKED`.

No source data, model code, prediction files, or crawler files were modified.

---

## 2. Input Evidence

| File | Status | Notes |
|---|:---:|---|
| `docs/orchestration/phase6o_future_native_timestamp_capture_design_2026-04-29.md` | ✅ | Phase 6O design — 14 sections, 6O schema spec, M13/M6/M9/M11 gate specs |
| `scripts/validate_model_output_contract.py` | ✅ | Phase 6K validator (M1–M12) — extended in this phase |
| `data/derived/model_outputs_2026-04-29.jsonl` | ✅ (unmodified) | 2,986 rows; schema `6j-1.0`; Phase 6L ML-adapter output |
| `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl` | ✅ (unmodified) | 2,080 dry-run placeholder rows |
| `data/derived/model_output_contract_validation_summary_2026-04-29.json` | ✅ updated | Updated by validator run; 7 new native timestamp keys |

---

## 3. Validator Extension Summary

### 3.1 New Constants Added

```python
NATIVE_TIMESTAMP_FIELDS: list[str] = [
    "prediction_run_started_at_utc",
    "prediction_run_completed_at_utc",
    "model_output_written_at_utc",
    "prediction_time_source",
    "feature_cutoff_source",
    "timestamp_capture_version",
    "timestamp_quality_flags",
]

ALLOWED_PREDICTION_TIME_SOURCES: list[str] = [
    "MODEL_INFERENCE_RUNTIME",
    "MODEL_OUTPUT_EMISSION_RUNTIME",
    "SCHEDULER_RUN_RUNTIME",
]

DISALLOWED_PREDICTION_TIME_SOURCES_FOR_CLV: list[str] = [
    "REPORT_METADATA",
    "FILE_METADATA_LOW_CONFIDENCE",
    "UNKNOWN",
]

HARD_FAIL_TIMESTAMP_QUALITY_FLAGS: list[str] = [
    "TIMESTAMP_MISSING",
    "TIMESTAMP_SOURCE_LOW_CONFIDENCE",
    "PREDICTION_TIME_AFTER_MATCH",
    "FEATURE_CUTOFF_AFTER_PREDICTION",
    "FEATURE_CUTOFF_AFTER_MATCH",
    "TIMESTAMP_CLOCK_DRIFT",
    "HISTORICAL_TIMESTAMP_RECOVERY",
    "ODDS_SNAPSHOT_AFTER_MATCH",
]
```

### 3.2 Schema Version Update

| Field | Before | After |
|---|---|---|
| `SCHEMA_VERSION` | `"6k-1.0"` | `"6p-1.0"` |
| `PHASE` | `"6K"` | `"6K/6P"` |

---

## 4. M13 Native Timestamp Contract Gate

### 4.1 Gate Definition

`gate_m13(row)` → `tuple[bool, list[str]]`

**Checks (in order):**

1. `prediction_run_started_at_utc` — must be present and non-null
2. `prediction_run_completed_at_utc` — must be present and non-null
3. `model_output_written_at_utc` — must be present and non-null
4. `prediction_time_source` — must be present and in `ALLOWED_PREDICTION_TIME_SOURCES`; must not be in `DISALLOWED_PREDICTION_TIME_SOURCES_FOR_CLV`
5. `feature_cutoff_source` — must be present and not `"UNKNOWN"`
6. `timestamp_capture_version` — must be a non-empty string
7. `timestamp_quality_flags` — must not contain any flag from `HARD_FAIL_TIMESTAMP_QUALITY_FLAGS`

**Backward compatibility**: M13 does not crash on rows missing native timestamp fields.
It collects all failures and returns the complete issue list, enabling downstream
classification of "missing fields" vs "invalid values".

### 4.2 M13 Results on Historical Rows

| Metric | Value |
|---|:---:|
| Real rows evaluated | 2,986 |
| M13 PASS | **0** |
| M13 FAIL | **2,986** |
| M13 Pass % | **0.0%** |
| Root cause | All 7 native timestamp fields absent from `"6j-1.0"` schema rows |

**Missing native timestamp fields** (all 2,986 rows):

| Field | Present in any row? |
|---|:---:|
| `prediction_run_started_at_utc` | ❌ |
| `prediction_run_completed_at_utc` | ❌ |
| `model_output_written_at_utc` | ❌ |
| `prediction_time_source` | ❌ |
| `feature_cutoff_source` | ❌ |
| `timestamp_capture_version` | ❌ |
| `timestamp_quality_flags` | ❌ |

**Root cause**: These rows were produced by the Phase 6L ML-only adapter
(`scripts/build_ml_model_outputs.py`) which performed retrospective reconstruction from
`mlb_decision_quality_report.json`. Retrospective reconstruction cannot supply native
runtime timestamps — they must be captured at prediction inference time (Phase 6Q+).

---

## 5. M6 / M9 / M11 Gate Extensions

### 5.1 M6 TIMING_VALID — T4–T7 Added

Four additional timestamp chain invariant checks. **All skip gracefully when native
timestamp fields are absent** (no crash, no additional failure for historical rows):

| Check | Invariant | Behavior when field absent |
|---|---|---|
| T4 | `prediction_run_started_at_utc` ≤ `prediction_time_utc` | Skip (fields not in row) |
| T5 | `prediction_time_utc` ≤ `prediction_run_completed_at_utc` | Skip |
| T6 | `model_output_written_at_utc` ≥ `prediction_time_utc` | Skip |
| T7 | `odds_snapshot_time_utc` ≤ `prediction_time_utc` | Skip |

**Impact on historical rows**: Zero additional failures from T4–T7 (all fields absent,
checks skipped). The existing T1/T2 failure (`prediction_time_utc=null`) accounts for all
2,986 M6 failures.

### 5.2 M9 NO_LEAKAGE_HARD_FAIL — Timestamp Source / Flag Checks Added

Three new checks appended to the existing M9 leakage chain:

| Check | Condition | Error code |
|---|---|---|
| Disallowed source | `prediction_time_source` in `DISALLOWED_PREDICTION_TIME_SOURCES_FOR_CLV` | `M9_FAIL_LEAKAGE: prediction_time_source=...` |
| Hard-fail flags | `timestamp_quality_flags` contains any `HARD_FAIL_TIMESTAMP_QUALITY_FLAGS` entry | `M9_FAIL_LEAKAGE: timestamp_quality_flags contains hard-fail flags` |
| Odds snapshot leakage | `odds_snapshot_time_utc > prediction_time_utc` | `M9_FAIL_LEAKAGE: odds_snapshot_time_utc > prediction_time_utc` |

**Impact on historical rows**: Zero additional failures from new M9 checks.
`prediction_time_source` is absent (not "REPORT_METADATA"), `timestamp_quality_flags`
is absent, `odds_snapshot_time_utc` is absent. All 2,986 rows still pass M9.

### 5.3 M11 CLV_USABLE_FLAG_CORRECT — Native Timestamp Requirement Added

For rows where `clv_usable=true`, `dry_run=false`, and `predicted_probability` is not null,
M11 now requires:

1. `prediction_time_source` must be in `ALLOWED_PREDICTION_TIME_SOURCES`
2. `timestamp_capture_version` must be a non-empty string
3. `timestamp_quality_flags` must not contain hard-fail flags

**Impact on historical rows**: Zero additional failures. All 2,986 historical rows have
`clv_usable=false`, so the new M11 branch is never entered.

---

## 6. Historical Row Compatibility

### 6.1 Gate Result Comparison (Real Rows — 2,986 total)

| Gate | Before Phase 6P | After Phase 6P | Delta |
|---|:---:|:---:|:---:|
| M1 SCHEMA_VALID | FAIL 2,986 | FAIL 2,986 | 0 |
| M2 CANONICAL_MATCH_ID_PRESENT | PASS 2,986 | PASS 2,986 | 0 |
| M3 MARKET_KEY_PRESENT | PASS 2,986 | PASS 2,986 | 0 |
| M4 SELECTION_KEY_PRESENT | PASS 2,986 | PASS 2,986 | 0 |
| M5 VERSION_FIELDS_PRESENT | PASS 2,986 | PASS 2,986 | 0 |
| M6 TIMING_VALID | FAIL 2,986 | FAIL 2,986 | 0 |
| M7 PROBABILITY_VALID | PASS 2,986 | PASS 2,986 | 0 |
| M8 EV_VALID_OR_NULL_WITH_REASON | PASS 2,986 | PASS 2,986 | 0 |
| M9 NO_LEAKAGE_HARD_FAIL | PASS 2,986 | PASS 2,986 | 0 |
| M10 MARKET_SEMANTICS_VALID | FAIL 2,220 | FAIL 2,220 | 0 |
| M11 CLV_USABLE_FLAG_CORRECT | PASS 2,986 | PASS 2,986 | 0 |
| M12 DRY_RUN_FLAG_CORRECT | PASS 2,986 | PASS 2,986 | 0 |
| M13 NATIVE_TIMESTAMP_CONTRACT | — (new) | FAIL 2,986 | +2,986 |

**No existing gate results were disturbed.** M13 is an additive gate and
the M6/M9/M11 extensions are backward-compatible (graceful skip when fields absent).

### 6.2 CLV-Usability Status

All 2,986 Phase 6L rows remain **not CLV-usable** (`clv_usable=false`). Phase 6P does
not backfill `prediction_time_utc`, native timestamp fields, or any other data.

---

## 7. Validation Results

### 7.1 Console Output (Phase 6P Validator Run)

```
======================================================================
Phase 6K — Model Output Contract Validator
======================================================================
  Run timestamp        : 2026-04-30T07:16:35Z
  Real candidate       : data/derived/model_outputs_2026-04-29.jsonl
    → exists           : True
    → rows             : 2986
    → valid rows       : 0
  Dry-run rows         : 2080
  Legacy candidates    : 9

  Gate Results (dry-run rows):
    M1  SCHEMA_VALID                       : FAIL (0/2080, 0.0%)
    M2  CANONICAL_MATCH_ID_PRESENT         : PASS (2080/2080, 100.0%)
    M3  MARKET_KEY_PRESENT                 : PASS (2080/2080, 100.0%)
    M4  SELECTION_KEY_PRESENT              : PASS (2080/2080, 100.0%)
    M5  VERSION_FIELDS_PRESENT             : FAIL (0/2080, 0.0%)
    M6  TIMING_VALID                       : FAIL (0/2080, 0.0%)
    M7  PROBABILITY_VALID                  : PASS (2080/2080, 100.0%)
    M8  EV_VALID_OR_NULL_WITH_REASON       : PASS (2080/2080, 100.0%)
    M9  NO_LEAKAGE_HARD_FAIL               : PASS (2080/2080, 100.0%)
    M10 MARKET_SEMANTICS_VALID             : FAIL (766/2080, 36.8%)
    M11 CLV_USABLE_FLAG_CORRECT            : PASS (2080/2080, 100.0%)
    M12 DRY_RUN_FLAG_CORRECT               : PASS (2080/2080, 100.0%)
    M13 NATIVE_TIMESTAMP_CONTRACT          : FAIL (0/2080, 0.0%)

  READINESS DECISION   : PARTIAL_READY_HISTORICAL_ROWS_BLOCKED
  M13 Native TS ready  : 0/2986 real rows
  Native TS missing    : ['feature_cutoff_source', 'model_output_written_at_utc',
                          'prediction_run_completed_at_utc', 'prediction_run_started_at_utc']...
======================================================================
```

### 7.2 Summary JSON New Keys

All 7 new native timestamp keys confirmed present in
`data/derived/model_output_contract_validation_summary_2026-04-29.json`:

| Key | Value |
|---|---|
| `native_timestamp_gate_enabled` | `true` |
| `m13_native_timestamp_contract` | `{total_rows: 2986, pass: 0, fail: 2986, block: 0, pass_pct: 0.0}` |
| `native_timestamp_ready_rows` | `0` |
| `native_timestamp_blocked_rows` | `2986` |
| `native_timestamp_missing_fields` | (all 7 NATIVE_TIMESTAMP_FIELDS) |
| `allowed_prediction_time_sources` | `["MODEL_INFERENCE_RUNTIME", "MODEL_OUTPUT_EMISSION_RUNTIME", "SCHEDULER_RUN_RUNTIME"]` |
| `disallowed_prediction_time_sources` | `["REPORT_METADATA", "FILE_METADATA_LOW_CONFIDENCE", "UNKNOWN"]` |

---

## 8. Readiness Decision

**`PARTIAL_READY_HISTORICAL_ROWS_BLOCKED`**

### Rationale

| Criterion | Status | Evidence |
|---|:---:|---|
| Real `model_outputs_2026-04-29.jsonl` exists | ✅ | 2,986 rows present |
| Real rows schema-valid (M1) | ❌ | All fail M1 (missing clv_usable, dry_run, other contract fields) |
| Real rows timing-valid (M6) | ❌ | `prediction_time_utc=null` on all rows (retrospective reconstruction) |
| Real rows CLV-usable | ❌ | `clv_usable=false` on all rows |
| M13 PASS for any real row | ❌ | All 7 native timestamp fields absent (historical rows cannot have runtime timestamps) |
| Validator supports M13 | ✅ | Implemented and running in this phase |
| Backward compatibility maintained | ✅ | M6/M9/M11 extensions skip gracefully; no existing gate results disturbed |
| Summary JSON includes 7 new keys | ✅ | Verified in `model_output_contract_validation_summary_2026-04-29.json` |

### Decision Progression

| Phase | Readiness |
|---|---|
| 6K | `NOT_READY_SCHEMA_GAP` |
| **6P** | **`PARTIAL_READY_HISTORICAL_ROWS_BLOCKED`** |
| 6Q (target) | `PARTIAL_READY_DRY_RUN_ONLY` (after native timestamp dry-run stub) |

---

## 9. Recommended Next Step

**Phase 6Q — Future Inference Timestamp Capture Stub / Dry-Run Adapter**

Phase 6Q should:

1. Design a native timestamp capture stub that fires at inference time (not reconstruction time).
2. Emit a dry-run row with all 7 native timestamp fields populated (`prediction_run_started_at_utc`,
   `prediction_run_completed_at_utc`, `model_output_written_at_utc`, `prediction_time_source`,
   `feature_cutoff_source`, `timestamp_capture_version`, `timestamp_quality_flags`).
3. Set `prediction_time_source = "MODEL_INFERENCE_RUNTIME"` and `timestamp_capture_version = "0.1.0"`.
4. Pass M13 on at least one dry-run row.
5. Validate with the Phase 6P extended validator — expect readiness `PARTIAL_READY_DRY_RUN_ONLY`.

Historical rows in `data/derived/model_outputs_2026-04-29.jsonl` must **not** be backfilled.
They remain in `PARTIAL_READY_HISTORICAL_ROWS_BLOCKED` status permanently.

---

## 10. Scope Confirmation

| Constraint | Status |
|---|---|
| `data/derived/model_outputs_2026-04-29.jsonl` modified | ❌ NOT done |
| `scripts/build_ml_model_outputs.py` modified | ❌ NOT done |
| `docs/orchestration/phase6l_ml_model_output_adapter_report_2026-04-29.md` modified | ❌ NOT done |
| Model code modified | ❌ NOT done |
| New predictions generated | ❌ NOT done |
| Crawler modified | ❌ NOT done |
| DB or migrations modified | ❌ NOT done |
| External API called | ❌ NOT done |
| Orchestrator task created | ❌ NOT done |
| Formal CLV validation run | ❌ NOT done |
| Git commit made | ❌ NOT done |
| Contamination terms used | ❌ NOT done |

---

*Phase 6P VALIDATOR_EXTENSION_VERIFIED — token: PHASE_6P_VALIDATOR_EXTENSION_VERIFIED*
