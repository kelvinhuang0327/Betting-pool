# Phase 6M — Prediction Time Alignment Design

**Date**: 2026-04-29
**Phase**: 6M (Documentation / Alignment Design Only — No Model Changes, No Predictions, No Commit)
**Status**: PHASE_6M_TIMING_ALIGNMENT_DESIGN_VERIFIED
**Predecessor**: Phase 6L — `PHASE_6L_ML_ADAPTER_PARTIALLY_VERIFIED`
**Contract Schema Version**: 6j-1.0

---

## 1. Executive Summary

Phase 6L emitted 2,986 model output rows (1,493 MLB games × 2 ML selections) that
pass structural validation (M1–M5, M7–M12 gates on real rows) but fail the M6
`TIMING_VALID` gate universally because `prediction_time_utc = null` and
`feature_cutoff_time_utc = null` on every row.

This document diagnoses why M6 fails, catalogs all timestamp evidence available in
the codebase, evaluates five timestamp alignment options, and recommends a safe
implementation path that does **not** backfill fabricated timestamps.

**Primary finding**: The existing 2,986 rows represent a historical reconstruction
of the 2025 MLB season (games dated 2025-04-24 through 2025-09-28) produced by a
paper-only report generated on 2026-04-24 — approximately 11 months after the earliest
game date. No pre-match prediction inference ever occurred. There is no safe Option A
or Option C timestamp recovery for these rows. The correct disposition is:

- **Option E**: Preserve existing rows as contract-shaped, non-CLV-usable historical
  adapter output with explicit quality flags.
- **Option B**: Require future model pipelines to record `prediction_time_utc` natively
  at inference time.

No fake timestamps will be backfilled. No existing data files are modified.

---

## 2. Evidence Read

| File | Status | Key Finding |
|------|--------|-------------|
| `docs/orchestration/phase6l_ml_model_output_adapter_report_2026-04-29.md` | ✅ Read | Confirms `prediction_time_utc = null` on all 2,986 rows; `PREDICTION_TIME_MISSING` flag; `clv_usable = false` on all rows |
| `data/derived/model_outputs_2026-04-29.jsonl` | ✅ Read (sample) | 2,986 rows; `prediction_time_utc: null`; `feature_cutoff_time_utc: null`; `match_time_utc` approximate; file mtime Apr 30 00:32 local |
| `docs/orchestration/phase6k_model_output_contract_validator_report_2026-04-29.md` | ✅ Read | M6 `TIMING_VALID`: 0/2,086 pass (dry-run); real rows not yet gated on M6 via validator |
| `data/derived/model_output_contract_validation_summary_2026-04-29.json` | ✅ Read | `run_timestamp_utc: 2026-04-29T16:32:17Z`; M6 pass=0/2,080 for dry-run rows |
| `docs/orchestration/phase6j_model_output_contract_design_2026-04-29.md` | ✅ Read | M6 rules: T1 `prediction_time_utc < match_time_utc`; T2 `feature_cutoff_time_utc <= prediction_time_utc`; T3 training window end < prediction_time_utc |
| `data/wbc_backend/reports/mlb_decision_quality_report.json` | ✅ Read | `generated_at: 2026-04-24T08:27:30.528058Z`; per-game rows have no timestamp fields; status `UNAVAILABLE_SINGLE_SNAPSHOT`; mode `PAPER_ONLY` |
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ✅ Read (sample) | Has `snapshot_time_utc`; covers TSL/WBC/unknown_league only — zero MLB 2025 rows |
| `data/derived/match_identity_bridge_2026-04-29.jsonl` | ✅ Read (via Phase 6L) | 383 rows; all `unknown_league`; no MLB rows |
| `data/derived/team_alias_map_2026-04-29.csv` | ✅ Read (via Phase 6L) | 67 rows; KBO/NPB Chinese team names; no MLB timing data |
| `config/settings.py` | ✅ Read (via Phase 6J) | `EV_STRONG=0.07`, `EV_MEDIUM=0.03`, `KELLY_FRACTION=0.15`; no timestamp config |
| `strategy/risk_control.py` | ✅ Read (via Phase 6J) | `RiskStatus` enum; no prediction timing fields |
| `logs/daemon_heartbeat.jsonl` | ✅ Read | Odds capture heartbeat only; timestamps from 2026-04-17 onward; **no prediction/model inference events** |
| `logs/runtime_events.jsonl` | ✅ Read | Snapshot monitoring cycles (2026-04-18); **no model inference events** |
| `logs/odds_capture.log` | ✅ Read | Odds capture events only |
| `logs/odds_capture_error.log` | ✅ Read | Odds capture errors only |
| `data/wbc_backend/reports/mlb_pregame_coverage_report.json` | ✅ Read | `generated_at: 2026-03-20T08:08:19Z`; MLB scope; per-game rows have `game_time_utc` (match time) only — no prediction timestamps |

### Missing Evidence

| File | Status | Impact on M6 Recovery |
|------|--------|----------------------|
| `data/derived/model_output_contract_validation_summary_2026-04-29.json` for real rows | Validation ran against dry-run only | M6 gate results for real 2,986 rows not in summary |
| Any scheduler/orchestrator job log recording model inference run | **ABSENT** | Option C (scheduler log recovery) cannot be pursued |
| `prediction_time_utc` in any per-game row of `mlb_decision_quality_report.json` | **ABSENT** | Source has no timing data at any granularity below report level |
| MLB 2025 odds snapshots with `snapshot_time_utc` | **ABSENT** (TSL covers WBC/unknown only) | `odds_snapshot_ref` cannot be resolved; `implied_probability_at_prediction` cannot be derived |

---

## 3. Current Timing Evidence Inventory

| Evidence Source | Has `prediction_time_utc`? | Has `generated_at` / `run_timestamp`? | Has `feature_cutoff`? | Has `match_time`? | Safe for M6? | Notes |
|---|:---:|:---:|:---:|:---:|:---:|---|
| `model_outputs_2026-04-29.jsonl` (Phase 6L) | ❌ null | ❌ no | ❌ null | ✅ approximate | ❌ | All timing fields null; flags `PREDICTION_TIME_MISSING`, `MATCH_TIME_UTC_APPROXIMATE` |
| `mlb_decision_quality_report.json` (source) | ❌ absent | ✅ `2026-04-24T08:27:30Z` | ❌ absent | ❌ per game: absent | ❌ | Report `generated_at` is 2026-04-24 — ~11 months AFTER 2025-season games; `PAPER_ONLY` status; no CLV |
| `mlb_pregame_coverage_report.json` | ❌ absent | ✅ `2026-03-20T08:08:19Z` | ❌ absent | ✅ per game UTC | ❌ | Match times only; no prediction times; covers future 2026 games, not 2025 MLB dataset |
| `model_output_contract_validation_summary_2026-04-29.json` | ❌ absent | ✅ `2026-04-29T16:32:17Z` | ❌ absent | ❌ absent | ❌ | Validator run timestamp is a processing artifact, not a prediction timestamp |
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ❌ absent | ❌ absent | ❌ absent | ✅ `match_time_utc` | ❌ | `snapshot_time_utc` present but covers WBC/TSL/unknown_league only — no MLB 2025 rows |
| `logs/daemon_heartbeat.jsonl` | ❌ absent | ✅ per event | ❌ absent | ❌ absent | ❌ | Odds capture events only; no model/prediction events |
| `logs/runtime_events.jsonl` | ❌ absent | ✅ per event | ❌ absent | ❌ absent | ❌ | Snapshot monitoring only; no model inference events |
| File mtime — `model_outputs_2026-04-29.jsonl` | ❌ | ✅ Apr 30 00:32 local | ❌ | ❌ | ❌ | mtime is adapter script run time; games are 2025 season; mtime is post-season by ~7 months minimum |
| File mtime — `mlb_decision_quality_report.json` | ❌ | ✅ Apr 24 16:27 local | ❌ | ❌ | ❌ | Report generated 2026-04-24; earliest game 2025-04-24; 365 days post-match — leakage risk maximum |

**Inventory Conclusion**: No timing evidence in the codebase is both pre-match and
attributable to a genuine model inference run against the 2025 MLB dataset.
Every available timestamp post-dates all or most of the games being tracked.
Option A (report generation timestamp) and Option C (scheduler log) are both
infeasible for the existing 2,986 rows.

---

## 4. M6 Timing Gate Diagnosis

### 4.1 Gate Definition (from Phase 6J §7)

M6 `TIMING_VALID` requires all three timing rules to pass:

| Rule | Condition | Failure Mode |
|------|-----------|-------------|
| T1 | `prediction_time_utc < match_time_utc` | Either field is null → cannot evaluate |
| T2 | `feature_cutoff_time_utc <= prediction_time_utc` | Either field is null → cannot evaluate |
| T3 | Training window end date < `prediction_time_utc` | `UNKNOWN_TRAINING_WINDOW` flag → cannot evaluate |

### 4.2 Why M6 Fails for All 2,986 Rows

**Root cause**: `prediction_time_utc = null` on every row in
`model_outputs_2026-04-29.jsonl`. This makes T1, T2, and T3 unevaluable.

Cascade effects:

1. **T1 cannot be evaluated** — null `prediction_time_utc` cannot be compared to
   `match_time_utc`. Even if `match_time_utc` is present (approximate), comparison
   requires a non-null left operand.

2. **T2 cannot be evaluated** — `feature_cutoff_time_utc = null` compounds the T1
   failure. Both sides of the inequality are null.

3. **T3 cannot be evaluated** — `training_window_id = UNKNOWN_TRAINING_WINDOW` means
   the training window end date is indeterminate. Even with a known `prediction_time_utc`,
   T3 would remain unverifiable.

4. **`clv_usable` remains false** — the CLV usability flag in Phase 6J contract
   requires M6 to pass before `clv_usable` can be set to `true`. Zero rows qualify.

5. **`odds_snapshot_ref = null`** — without a pre-match odds snapshot reference,
   `implied_probability_at_prediction` cannot be computed, and CLV measurement
   is structurally impossible regardless of timing.

### 4.3 Historical Context Amplifying Risk

The 2,986 rows span games from 2025-04-24 to 2025-09-28 (full 2025 MLB regular
season). The source report (`mlb_decision_quality_report.json`) was generated on
2026-04-24 — approximately 365 days after the first game and 208 days after the
last game. This is a retrospective paper-tracking analysis, not a real-time
pre-match prediction pipeline. There was no prediction inference run prior to
game time for these rows. The timing gap is structural, not incidental.

---

## 5. Alignment Options

### Option A — Use Report Generation Timestamp

Use `mlb_decision_quality_report.json` → `report_header.generated_at`
(`2026-04-24T08:27:30.528058Z`) as a surrogate `prediction_time_utc`.

**Pros**:
- Value is available and unambiguous.
- Represents the exact moment the analysis report was produced.

**Cons**:
- `2026-04-24T08:27:30Z` is 365+ days after the earliest game (2025-04-24).
  T1 (`prediction_time_utc < match_time_utc`) would fail for every single row.
- Setting this as `prediction_time_utc` would not pass M6; it would merely replace
  a null failure with an explicit post-match failure.
- Creates false provenance: implies inference occurred in 2026 for 2025 games.
- Would add `PREDICTION_TIME_AFTER_MATCH` quality flag to all rows.
- Adversarially misleading for CLV analysis.

**Verdict**: **Reject**. The report generation timestamp is demonstrably
post-match for the entire 2025 MLB dataset. Using it would corrupt provenance
without passing M6.

---

### Option B — Add Explicit Prediction Timestamp to Future Model Pipeline (Preferred)

Require all future model inference pipelines to record `prediction_time_utc`
natively at the moment of inference and emit it into every output row.

**Pros**:
- Safest provenance: timestamp is recorded at the point of truth.
- Satisfies leakage guard: inference time is known and verifiable.
- Clean contract: no reconstruction, no inference, no approximation.
- Enables T1, T2, T3 to be evaluated on forward-looking rows.
- Compatible with future CLV measurement.

**Cons**:
- Requires model pipeline modification (future work, not this phase).
- Cannot fix the existing 2,986 historical adapter rows immediately.
- The existing rows will remain `clv_usable = false` until a real inference
  pipeline is in place.

**Verdict**: **Accept as primary path.** All future model output pipelines must
emit `prediction_time_utc` at inference time. This is a non-negotiable contract
requirement for any row to become CLV-usable.

---

### Option C — Reconstruct from Scheduler / Job Logs

Use available orchestrator or job logs to infer when the prediction report was
generated or when a model inference run was triggered.

**Investigation result**:
- `logs/daemon_heartbeat.jsonl`: contains only odds capture heartbeats. No entries
  related to model inference, prediction pipeline, or report generation.
- `logs/runtime_events.jsonl`: contains snapshot monitoring cycle events only.
- `logs/odds_capture.log` / `logs/odds_capture_error.log`: odds capture operations only.
- `logs/activation_loop_log.jsonl`, `logs/settlement_run_log.jsonl`: unrelated
  lifecycle events; no model inference records.
- No orchestrator task log records any prediction run for the MLB 2025 dataset.

**Evidence verdict**: Log evidence is absent. No scheduler log captures the time
at which `mlb_decision_quality_report.json` was generated or when any model
inference occurred against the 2025 MLB dataset.

Even if logs were present, the report `generated_at = 2026-04-24T08:27:30Z`
confirms the report was produced 365+ days post-match. Recovering this timestamp
via logs would yield the same Option A failure: the reconstructed time would still
be post-match.

**Verdict**: **Reject for existing rows.** Log evidence is absent, and any
recoverable timestamp would be post-match by construction. Option C remains
a documented future path for genuine real-time inference pipelines with log
instrumentation.

---

### Option D — Use Fixed Pre-Match Offset

Set `prediction_time_utc = match_time_utc - N hours` for some fixed offset N.

**Analysis**:
- Manufactures a timestamp with no empirical basis.
- There is no evidence that inference occurred N hours before any game.
- Passes M6 mechanically while creating false provenance.
- CLV computed against a fabricated prediction time has no statistical meaning.
- Violates the leakage guard's core principle: temporal isolation must be
  verified, not assumed.
- Would add `PREDICTION_TIME_INFERRED` + `PREDICTION_TIME_LOW_CONFIDENCE` flags
  but no flag can rehabilitate a fabricated timestamp for CLV purposes.

**Verdict**: **Reject unconditionally.**

> ⛔ Do not backfill fake timestamps. Option D is permanently excluded from
> consideration for any row in this pipeline.

---

### Option E — Keep Rows Non-CLV-Usable Until Future Capture (Safe Fallback)

Retain all 2,986 existing rows with `prediction_time_utc = null`,
`clv_usable = false`, and `PREDICTION_TIME_MISSING` quality flag. Treat these rows
as contract-shaped historical adapter output that documents the model's probability
distribution over the 2025 MLB season, without asserting any timing provenance.

**Pros**:
- Honest: no fabrication, no reconstruction, no leakage risk.
- Rows remain structurally valid under M1–M5, M7–M12 (except M6).
- Quality flags accurately describe the dataset's limitations.
- Preserves the dataset for non-CLV uses (model calibration audit, historical
  ROI simulation with explicit caveats, structural testing).
- Consistent with the report's own `PAPER_ONLY` / `SANDBOX_ONLY` designation.

**Cons**:
- CLV measurement remains unavailable for these rows indefinitely.
- M6 continues to fail; `clv_usable = false` persists.

**Verdict**: **Accept as correct fallback.** The 2,986 historical adapter rows
will remain non-CLV-usable. This is the honest disposition for a paper-tracking
retrospective dataset.

---

## 6. Recommended Path

### 6.1 Decision

| Priority | Option | Status | Action |
|----------|--------|--------|--------|
| Primary | **Option B** | ✅ Accepted | Implement native `prediction_time_utc` capture in future model pipelines |
| Fallback | **Option E** | ✅ Accepted | Existing 2,986 rows remain `clv_usable = false`; no modification |
| Conditional | **Option C** | ⚠️ Not available now | Revisit only if future real-time pipelines add log instrumentation; requires pre-match evidence |
| Rejected | **Option A** | ❌ Rejected | Report generation timestamp is post-match; does not pass M6 |
| Rejected | **Option D** | ❌ Rejected | Fabricated timestamp; prohibited unconditionally |

### 6.2 Explicit Constraint

> **Do not backfill fake timestamps.**
>
> No value shall be written to `prediction_time_utc` for any existing row in
> `model_outputs_2026-04-29.jsonl` unless that value can be traced to an actual
> model inference event that occurred prior to the corresponding `match_time_utc`.
> The absence of a valid `prediction_time_utc` is not a defect to be patched;
> it is an accurate characterization of the current dataset.

### 6.3 Disposition of Existing 2,986 Rows

The existing adapter output is retained as-is with the following interpretation:

- **Purpose**: Historical model probability reconstruction for paper-tracking audit.
- **CLV status**: Not usable. `clv_usable = false` is correct and intentional.
- **M6 status**: Expected failure. M6 will pass only for rows from future
  real-time pipelines with native inference timestamp capture.
- **Modification policy**: Do not modify `model_outputs_2026-04-29.jsonl`.

---

## 7. Timestamp Contract Addendum

This section extends the Phase 6J contract schema with timestamp provenance fields
required for M6 gate evaluation and CLV eligibility.

### 7.1 New Fields

| Field | Type | Nullable | Description |
|-------|------|:--------:|-------------|
| `prediction_time_utc` | ISO8601 | YES (pending) | UTC timestamp when model inference was executed for this row. Must be strictly before `match_time_utc`. Set to null when timing is unknown; M6 fails if null. |
| `feature_cutoff_time_utc` | ISO8601 | YES (pending) | Latest timestamp of any feature input used during inference. Must be ≤ `prediction_time_utc`. May equal `prediction_time_utc` for adapters without feature-level timestamp resolution. |
| `prediction_time_source` | enum | NO | Source/method used to establish `prediction_time_utc`. See §7.2. Must not be `UNKNOWN` for CLV-usable rows. |
| `prediction_time_confidence` | enum | NO | Confidence level for the `prediction_time_utc` value. See §7.3. |
| `prediction_time_quality_flags` | list[str] | NO | Zero or more quality flags describing timing data issues. See §7.4. |

### 7.2 `prediction_time_source` Enum

| Value | Description | CLV Eligible? |
|-------|-------------|:-------------:|
| `MODEL_INFERENCE_RUNTIME` | Timestamp recorded by the model pipeline at the moment of inference execution. Native, authoritative. | ✅ Yes |
| `SCHEDULER_RUN_LOG` | Timestamp recovered from an orchestrator/scheduler job log that records when the inference job was triggered. Must be verifiably pre-match. | ⚠️ Conditional |
| `REPORT_METADATA` | Timestamp derived from a report's `generated_at` field. Acceptable only if the report was generated pre-match and provenance is recorded. | ⚠️ Conditional |
| `FILE_METADATA_LOW_CONFIDENCE` | Timestamp derived from file system modification time (`mtime`). Low confidence; subject to file copy, rsync, or clock drift errors. | ❌ No |
| `UNKNOWN` | Prediction time cannot be determined from any available evidence. | ❌ No |

> **Note for existing rows**: The current 2,986 adapter rows have
> `prediction_time_source` not yet set; the correct value is `UNKNOWN` since
> no valid source can be identified. Rows with `prediction_time_source = UNKNOWN`
> must have `clv_usable = false`.

### 7.3 `prediction_time_confidence` Enum

| Value | Description |
|-------|-------------|
| `HIGH` | Timestamp is native to the inference pipeline; millisecond precision; reliable. |
| `MEDIUM` | Timestamp recovered from a trusted job log; second-level precision; pre-match status verified. |
| `LOW` | Timestamp approximated from secondary metadata; may have minute-level uncertainty. |
| `NONE` | Timestamp is absent or cannot be assessed. |

### 7.4 `prediction_time_quality_flags` Enum Values

| Flag | Meaning |
|------|---------|
| `PREDICTION_TIME_MISSING` | `prediction_time_utc` is null. M6 will fail. |
| `PREDICTION_TIME_INFERRED` | Timestamp was not recorded natively; it was inferred from secondary evidence. |
| `PREDICTION_TIME_LOW_CONFIDENCE` | Timestamp has low provenance confidence (e.g., file mtime, approximate offset). |
| `PREDICTION_TIME_AFTER_MATCH` | `prediction_time_utc >= match_time_utc`. Hard leakage violation. M6 must fail. |
| `FEATURE_CUTOFF_MISSING` | `feature_cutoff_time_utc` is null. T2 cannot be evaluated. |
| `FEATURE_CUTOFF_AFTER_PREDICTION` | `feature_cutoff_time_utc > prediction_time_utc`. Feature leakage detected. Hard fail. |
| `HISTORICAL_TIMESTAMP_RECOVERY` | Prediction time was recovered from historical evidence (logs, metadata) rather than recorded at inference time. Treat as `LOW` or `MEDIUM` confidence. |

### 7.5 Field Co-Constraints

```
IF prediction_time_source == UNKNOWN:
    clv_usable MUST be false
    prediction_time_quality_flags MUST include PREDICTION_TIME_MISSING

IF PREDICTION_TIME_AFTER_MATCH in prediction_time_quality_flags:
    clv_usable MUST be false
    M6 gate MUST fail (hard)

IF FEATURE_CUTOFF_AFTER_PREDICTION in prediction_time_quality_flags:
    clv_usable MUST be false
    M6 gate MUST fail (hard)

IF prediction_time_source == FILE_METADATA_LOW_CONFIDENCE:
    clv_usable MUST be false (file mtime is never safe for CLV)

IF prediction_time_source == MODEL_INFERENCE_RUNTIME AND confidence == HIGH:
    prediction_time_quality_flags SHOULD be empty
    Row is eligible for M6 gate evaluation
```

---

## 8. M6 Acceptance Criteria

The following conditions must ALL be satisfied for an output row to pass M6
`TIMING_VALID` and become eligible for `clv_usable = true`:

| # | Criterion | Evaluation |
|---|-----------|-----------|
| 1 | `prediction_time_utc` is present (not null) | `prediction_time_utc IS NOT NULL` |
| 2 | `match_time_utc` is present (not null or approximate-only) | `match_time_utc IS NOT NULL` |
| 3 | `feature_cutoff_time_utc` is present, or is explicitly justified as equal to `prediction_time_utc` for historical adapter rows without feature-level timestamps | `feature_cutoff_time_utc IS NOT NULL OR feature_cutoff_justified = true` |
| 4 | Prediction precedes match | `prediction_time_utc < match_time_utc` (strict) |
| 5 | Feature cutoff does not exceed prediction time | `feature_cutoff_time_utc <= prediction_time_utc` |
| 6 | `prediction_time_source` is not `UNKNOWN` | `prediction_time_source != UNKNOWN` |
| 7 | No high-risk timing quality flags present | `PREDICTION_TIME_AFTER_MATCH` and `FEATURE_CUTOFF_AFTER_PREDICTION` absent |
| 8 | `odds_snapshot_ref` is present (for CLV measurement, not strictly for M6 pass) | Required for `expected_value` computation; M6 can pass without it but CLV record generation requires it |

### 8.1 M6 Gate Levels

| Level | Condition | Action |
|-------|-----------|--------|
| **PASS** | All criteria 1–7 met | Row eligible for CLV measurement; `clv_usable = true` allowed |
| **WARN** | Criteria 1–7 met but `prediction_time_confidence = LOW` | Row technically passes M6; must be flagged with `PREDICTION_TIME_LOW_CONFIDENCE`; CLV results marked as low-confidence |
| **FAIL** | Any of criteria 1–7 not met | Row fails M6; `clv_usable = false` enforced |
| **HARD_FAIL** | `PREDICTION_TIME_AFTER_MATCH` or `FEATURE_CUTOFF_AFTER_PREDICTION` detected | Row fails M6; row must not be promoted; flag for quarantine review |

---

## 9. Implementation Roadmap

### Phase 6N — Prediction Timestamp Evidence Scanner

**Goal**: Implement a read-only scanner that inspects available logs, reports, and
metadata files to determine whether any pre-match timestamp evidence exists for the
current `model_outputs_2026-04-29.jsonl` rows. Produce an evidence report and
summary JSON. Do not modify any output files.

**Scope**: Evidence scanning only. No timestamp backfill.

**Expected outcome**: Confirm that Option C (scheduler log recovery) is infeasible
for existing rows due to absent log evidence, and document this conclusion formally.

---

### Phase 6O — ML Adapter Timestamp Attachment (If Evidence Exists)

**Prerequisite**: Phase 6N must confirm that verifiable, pre-match timestamp evidence
exists. If Phase 6N returns `NO_PRE_MATCH_EVIDENCE`, Phase 6O is skipped.

**Goal**: If Phase 6N finds valid pre-match evidence (e.g., a newly discovered log
not covered in Phase 6N), update the ML adapter to attach `prediction_time_utc` with
appropriate quality flags (`prediction_time_source`, `prediction_time_confidence`,
`prediction_time_quality_flags`) to qualifying rows.

**Constraint**: Do not write `prediction_time_utc` for any row where evidence is
post-match. Do not use Option D offsets.

---

### Phase 6P — Odds Snapshot Reference Alignment

**Goal**: Resolve `odds_snapshot_ref` for qualifying rows by building a lookup from
`data/derived/odds_snapshots_2026-04-29.jsonl` to model output rows via
`canonical_match_id` and `market_key`. Currently infeasible for MLB 2025 rows
because no MLB odds snapshots exist in the derived dataset.

**Dependency**: Requires MLB odds data source. Currently absent.

---

### Phase 6Q — Registry Conversion for ML-Only Rows

**Goal**: Promote model output rows that pass all gates (M1–M12) into the prediction
registry. Currently zero rows qualify due to M6 failure.

**Dependency**: Phase 6N/6O must resolve timing; Phase 6P must resolve odds reference.
For future real-time rows: Phase 6N/6O/6P may be bypassed if the inference pipeline
natively records all required fields.

---

### Phase 6R — CLV Record Generation

**Goal**: Generate CLV records by joining prediction registry entries with closing odds.
Only rows that pass all contract gates (including M6) and have `odds_snapshot_ref`
resolved are eligible.

**Dependency**: Phase 6Q must promote at least one row to registry. This phase will
not run until the full gate chain is satisfied.

---

## 10. Next Prompt

The following prompt is ready to copy for Phase 6N:

---

```text
# TASK: BETTING-POOL ORCHESTRATION PHASE 6N — PREDICTION TIMESTAMP EVIDENCE SCANNER

Follow AI system rules.

GOAL:
Implement a read-only evidence scanner that inspects all available logs, report
metadata, and file timestamps to determine whether any pre-match timestamp evidence
exists for the rows in `data/derived/model_outputs_2026-04-29.jsonl`.

Produce an evidence report and summary JSON. Do not modify any existing files.
Do not backfill timestamps. Do not generate predictions.

---

# CONTEXT

Phase 6M concluded:
- `prediction_time_utc = null` on all 2,986 model output rows
- Option A (report generation timestamp) is rejected: `generated_at = 2026-04-24`
  is post-match for all 2025 MLB games
- Option C (scheduler log recovery) is preliminary-rejected: no prediction events
  found in daemon_heartbeat.jsonl or runtime_events.jsonl
- Option E (keep rows non-CLV-usable) is the current fallback
- Option B (native inference timestamp) is the primary future path

Phase 6N must formally confirm or deny whether any pre-match evidence exists.

---

# STRICT SCOPE

Allowed:
1. Read all files in `logs/`
2. Read `data/wbc_backend/reports/*.json` for any timestamp metadata
3. Read `data/derived/*.jsonl` and `*.json` for metadata timestamps
4. Read `scripts/build_ml_model_outputs.py` for any embedded timestamp logic
5. Read git log for file creation / modification timestamps (read-only)
6. Create one evidence report: `docs/orchestration/phase6n_timestamp_evidence_report_2026-04-29.md`
7. Create one summary JSON: `data/derived/timestamp_evidence_summary_2026-04-29.json`

Forbidden:
1. Do not modify `model_outputs_2026-04-29.jsonl`
2. Do not modify any adapter script
3. Do not modify any model code
4. Do not backfill `prediction_time_utc` for any row
5. Do not generate new predictions
6. Do not call external APIs
7. Do not create orchestrator tasks
8. Do not run formal CLV validation
9. Do not commit

---

# REQUIRED ANALYSIS

1. Scan all log files for prediction/model/inference events
2. Extract all `generated_at` / `run_timestamp` / `created_at` fields from all
   report and derived files
3. For each timestamp found, determine:
   a. Is it pre-match relative to the game dates (2025-04-24..2025-09-28)?
   b. Can it be attributed to a model inference run?
   c. What is its `prediction_time_source` classification?
4. Produce a structured evidence table
5. State a clear decision: `PRE_MATCH_EVIDENCE_FOUND` or `NO_PRE_MATCH_EVIDENCE`
6. If `PRE_MATCH_EVIDENCE_FOUND`: describe which rows can receive `prediction_time_utc`
   and with what confidence
7. If `NO_PRE_MATCH_EVIDENCE`: confirm Option E (rows remain non-CLV-usable) and
   document Phase 6O as skipped

---

# REQUIRED OUTPUT FILES

- `docs/orchestration/phase6n_timestamp_evidence_report_2026-04-29.md`
- `data/derived/timestamp_evidence_summary_2026-04-29.json`

---

# ACCEPTANCE CRITERIA

PHASE_6N_EVIDENCE_SCAN_COMPLETE if:
1. All log files scanned
2. Evidence table is present
3. Decision is stated: PRE_MATCH_EVIDENCE_FOUND or NO_PRE_MATCH_EVIDENCE
4. No model_outputs modified
5. No timestamps backfilled
6. Contamination count (lottery domain terms) = 0
```

---

## 11. Scope Confirmation

The following constraints were observed throughout this phase:

| Constraint | Status |
|---|---|
| Source data modified | ❌ No |
| `model_outputs_2026-04-29.jsonl` modified | ❌ No |
| Model code modified | ❌ No |
| Crawler modified | ❌ No |
| DB or migrations modified | ❌ No |
| External APIs called | ❌ No |
| Orchestrator tasks created | ❌ No |
| Formal CLV validation run | ❌ No |
| Git commit made | ❌ No |
| Predictions generated | ❌ No |
| Adapter script modified | ❌ No |
| Fake timestamps written | ❌ No |

**Output produced**: One documentation file only.
`docs/orchestration/phase6m_prediction_time_alignment_design_2026-04-29.md`

---

*Phase 6M — Prediction Time Alignment Design — PHASE_6M_TIMING_ALIGNMENT_DESIGN_VERIFIED*
