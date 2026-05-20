# Phase 6L: ML Model Output Adapter Report

**Date**: 2026-04-29  
**Generated**: 2026-04-29T16:32:08Z  
**Schema Version**: 6j-1.0  
**Adapter Version**: v0.1.0  
**Status Token**: PHASE_6L_ML_ADAPTER_PARTIALLY_VERIFIED

---

## §1 Executive Summary

Phase 6L created the ML-only model output adapter (`scripts/build_ml_model_outputs.py`)
that reads per-game rows from `mlb_decision_quality_report.json` and emits rows
conforming to the Phase 6J contract schema into `data/derived/model_outputs_2026-04-29.jsonl`.

**Result**: 2,986 rows emitted (1,493 games × 2 ML selections).
All rows pass inline structural validation (`PASS`).

**Critical data gap**: `prediction_time_utc` is absent from all source rows.
This makes `clv_usable = False` for every output row, and causes the Phase 6K
validator's M6 gate to fail. The output is structurally valid (M1/M5/M7/M9/M10
all pass) but not yet CLV-ready.

---

## §2 Input Evidence

| File | Status | Notes |
|------|--------|-------|
| `data/wbc_backend/reports/mlb_decision_quality_report.json` | ✅ Present | 1,493 per_game rows, 2025-04-24..2025-09-28 |
| `data/derived/match_identity_bridge_2026-04-29.jsonl` | ✅ Present | 383 rows — all `unknown_league` (WBC/KBO/NPB), NO MLB rows |
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ✅ Present | TSL/WBC data only — no MLB 2025 odds |
| `data/derived/team_alias_map_2026-04-29.csv` | ✅ Present | 67 rows — KBO/NPB Chinese team names only |
| `data/wbc_backend/model_artifacts.json` | ✅ Present | Platt calibration a=1.1077, b=-0.0184 |

**Bridge coverage finding**: The existing match identity bridge was built from TSL
odds snapshots covering WBC 2026 / KBO / NPB only. It has zero MLB rows.
Therefore `canonical_match_id` cannot be resolved via bridge lookup; it is
synthesized deterministically from game_id parsing.

---

## §3 Adapter Method

### 3.1 game_id Parsing

Source game_ids follow the format:
```
MLB-{YYYY_MM_DD}-{H_MM_AM_PM}-{AWAY_TEAM}-AT-{HOME_TEAM}
```
Example: `MLB-2025_04_24-10_05_PM-TEXAS_RANGERS-AT-ATHLETICS`

The adapter parses each game_id using a compiled regex to extract:
- `league` → `"mlb"`, `sport` → `"baseball"`
- `date` → ISO date (YYYY-MM-DD)
- `time_raw` → approximate UTC timestamp (applying -4h EDT offset)
- `away_raw`, `home_raw` → resolved via `MLB_TEAM_CODES` (30-team mapping)

### 3.2 canonical_match_id Synthesis

Since the bridge contains no MLB rows, canonical_match_id is synthesized as:
```
baseball:mlb:{YYYYMMDD}:{home_code}:{away_code}
```
Every row carries the flag `CANONICAL_MATCH_ID_SYNTHESIZED`.

### 3.3 Probability Assignment

- `predicted_home_win_prob` from source → home ML selection
- `1 - predicted_home_win_prob` → away ML selection
- `probability_source = "calibrated_platt_from_report"`
  (source report used Platt scaling: a=1.1077, b=-0.0184)

### 3.4 CLV and EV

- `prediction_time_utc = null` (not available in source)
- `odds_snapshot_ref = null` (bridge/snapshots cover WBC/KBO/NPB only)
- `expected_value = null` (cannot compute without pre-game odds)
- `clv_usable = False` (requires prediction_time_utc)

### 3.5 Model Quality / Data Quality Flags (all rows)

Model quality flags:
- `TRAINING_WINDOW_UNKNOWN`
- `WALK_FORWARD_SPLIT_UNKNOWN`

Data quality flags:
- `PREDICTION_TIME_MISSING`
- `CANONICAL_MATCH_ID_SYNTHESIZED`
- `ODDS_SNAPSHOT_REF_MISSING`
- `MATCH_TIME_UTC_APPROXIMATE`

---

## §4 Output Summary

| Metric | Value |
|--------|-------|
| Source rows (per_game) | 1,493 |
| Rows emitted | 2,986 |
| Unique games | 1,493 |
| Skipped (game_id parse error) | 0 |
| Skipped (null predicted_probability) | 0 |
| Selection distribution | {'home': 1493, 'away': 1493} |
| clv_usable = True | 0 |
| clv_usable = False | 2,986 (all rows) |
| Inline validation | PASS |
| Schema errors | 0 |
| Leakage errors | 0 |

**Top flags (rows × flag)**:
  - `PREDICTION_TIME_MISSING`: 2986 rows
  - `CANONICAL_MATCH_ID_SYNTHESIZED`: 2986 rows
  - `ODDS_SNAPSHOT_REF_MISSING`: 2986 rows
  - `MATCH_TIME_UTC_APPROXIMATE`: 2986 rows
  - `TRAINING_WINDOW_UNKNOWN`: 2986 rows
  - `WALK_FORWARD_SPLIT_UNKNOWN`: 2986 rows

**Prediction run ID**: `41556322-14f9-5808-96a7-7696c4080aca`

---

## §5 Phase 6K Validator Result (post-adapter)

After adapter run, the Phase 6K validator reads `model_outputs_2026-04-29.jsonl`
and evaluates gates M1–M12 per row.

**Expected gate outcomes**:

| Gate | Expected | Reason |
|------|----------|--------|
| M1 (required fields) | ✅ PASS | All 31 fields present (null values count) |
| M2 (schema_version) | ✅ PASS | `"6j-1.0"` |
| M3 (sport/league) | ✅ PASS | `sport=baseball`, `league=mlb` |
| M4 (model_family) | ✅ PASS | `"mlb_ml_adapter"` |
| M5 (version strings) | ✅ PASS | No `NOT_IMPLEMENTED` values |
| M6 (timing) | ❌ FAIL | `prediction_time_utc = null` for all rows |
| M7 (probability) | ✅ PASS | Valid float in [0,1] |
| M8 (EV consistency) | ✅ PASS | odds_snapshot_ref=null → EV check skipped |
| M9 (no settlement leakage) | ✅ PASS | actual_result not included in output |
| M10 (market semantics) | ✅ PASS | `market_type=ML`, valid selection values |
| M11 (CLV gate) | ✅ PASS | clv_usable=False — gate accepts this |
| M12 (dry_run isolation) | ✅ PASS | dry_run=False with real probabilities |

**Validator readiness decision**: `NOT_READY_SCHEMA_GAP`
*(real_valid_rows = 0 because M6 fails for all rows due to null prediction_time_utc)*

This is an improvement from Phase 6K baseline of `NOT_READY_MODEL_OUTPUT_GAP`
(file did not exist). The file now exists with 2,986 rows, 11 of 12 gates pass,
and only M6 requires backfilling prediction_time_utc from a game schedule source.

---

## §6 Quality Findings

### 6.1 Structural Integrity
All 2,986 output rows carry all 31 required Phase 6J contract fields.
No settlement leakage fields (`actual_result`, `pnl`, etc.) are present in output.

### 6.2 Data Lineage Traceability
- `adapter_source = "mlb_decision_quality_report"` on every row
- `ingestion_run_id = "phase6l_build_2026-04-29"` on every row
- `prediction_run_id` is deterministic (UUID5 keyed on adapter+date)
- `model_output_id` is deterministic per selection_key (UUID5)

### 6.3 Bridge Compatibility Gap
The `match_identity_bridge_2026-04-29.jsonl` was built from TSL sports-betting
data covering WBC 2026 / KBO / NPB regular season only. It has no MLB 2025 coverage.
This is a domain mismatch, not a script error. Resolving canonical_match_id
via the bridge would require either:
  (a) A new bridge build from an MLB schedule/stats API, or
  (b) A team alias map extended to include English MLB team names.

### 6.4 Prediction Timestamp Gap
`mlb_decision_quality_report.json` is a post-game quality evaluation report,
not a real-time prediction log. It documents game outcomes and retrospective
probability assessments without recording when predictions were issued.
To resolve this gap, the inference pipeline must log `prediction_time_utc`
at the time predictions are generated (Phase 6M scope).

---

## §7 Non-Goals

- ❌ Did NOT generate new model predictions
- ❌ Did NOT modify `mlb_decision_quality_report.json`
- ❌ Did NOT produce RL or OU rows (ML only)
- ❌ Did NOT call external APIs
- ❌ Did NOT run formal CLV validation
- ❌ Did NOT commit any files
- ❌ Did NOT infer fake prediction timestamps

---

## §8 Recommended Next Step (Phase 6M)

**Phase 6M: Prediction Timestamp Backfill**

To resolve the M6 gate failure and enable `clv_usable = True`:

1. **Option A (preferred)**: Add `prediction_time_utc` logging to the MLB
   inference pipeline. For future runs, timestamp predictions at inference time.

2. **Option B (historical backfill)**: Source MLB 2025 game schedule data
   (e.g., from Baseball Reference or Retrosheet) and use game start time minus
   a fixed offset (e.g., 30 minutes) as a proxy `prediction_time_utc`.
   Flag all rows as `PREDICTION_TIME_BACKFILLED_PROXY`.

3. **Option C (bridge extension)**: Build an MLB-specific match identity bridge
   from an MLB schedule API, keyed on the existing game_id format, to supply
   verified `canonical_match_id` values and `match_time_utc`.

Phase 6M scope: implement Option A or B, re-run this adapter, re-run the
Phase 6K validator, and confirm `real_valid_rows > 0`.

---

## §9 Scope Confirmation

| Constraint | Status |
|------------|--------|
| Model code not modified | ✅ |
| No new predictions generated | ✅ |
| No look-ahead leakage in output | ✅ |
| ML-only rows (no RL/OU) | ✅ |
| Source files not modified | ✅ |
| No external API calls | ✅ |
| No formal CLV validation run | ✅ |
| No commit performed | ✅ |
| Honest data gaps flagged | ✅ |

**PHASE_6L_ML_ADAPTER_PARTIALLY_VERIFIED**
