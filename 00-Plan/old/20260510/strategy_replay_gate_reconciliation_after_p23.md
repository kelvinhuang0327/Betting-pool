# Strategy Replay Gate Reconciliation After P23

Date: 2026-05-10
Status: Read-only reconciliation completed
Marker: P24_STRATEGY_REPLAY_GATE_RECONCILIATION_AFTER_P23_READY

## 1. Executive Summary

The authoritative gate chain after P23 is now clear:

- P21 remains trustworthy.
- P22B is superseded.
- P23 is the controlling finding.
- The after fixture is trustworthy as actual_result-only fixture output.
- Artifact drift in the current fixture pair is not reproducible.
- Readiness remains `BACKFILL_REQUIRED`.
- UI remains blocked.
- Production migration remains blocked.

The remaining blockers are still the historical coverage gaps in `strategy_id` and `lifecycle_state_at_prediction_time`, not the approved actual-result backfill.

## 2. Supersession Statement

`P23_STRATEGY_REPLAY_ARTIFACT_DRIFT_SOURCE_TRACE_READY` is the controlling finding.

`P22B_STRATEGY_REPLAY_FIXTURE_SNAPSHOT_FILE_LEVEL_DELTA_AUDIT_READY` is superseded because its artifact-feature drift claim is not reproducible on the current fixture pair.

`P21_STRATEGY_REPLAY_SAFE_ACTUAL_RESULT_FIXTURE_APPLY_READY` remains valid because the current before/after fixture comparison still shows an actual-result-only apply path.

## 3. P21 / P22B / P23 Comparison

| Report | Status now | Core claim | Current judgment |
|---|---|---|---|
| P21 fixture apply report | Valid | Fixture-only apply changed `actual_result` only | Trusted |
| P22B file-level delta audit | Superseded | Claimed `artifact_feature_counts` drift plus actual_result backfill | Not reproducible on current fixtures |
| P23 artifact drift source trace | Controlling | Showed current fixture pair is actual_result-only and helper/write plan are pure | Authoritative |

Why P22B is superseded:
- The current fixture pair does not reproduce `artifact_feature_counts` drift.
- The current before fixture matches the live `prediction_registry.jsonl` rows.
- The current after fixture differs from before only by nested `actual_result` fields.
- The write plan only authorizes `actual_result`.
- The apply helper only patches approved fields on deep-copied rows.

## 4. Fixture Sanity Check Metrics

Recomputed on the current fixture pair:

- before rows: `66`
- after rows: `66`
- changed rows: `17`
- actual_result changed count: `17`
- artifact_feature_counts changed count: `0`
- deployment_gate changed count: `0`
- all changed rows only changed `actual_result`: `true`
- rows eligible for `UI_MVP_READY`: `0`

Row-level summary:
- changed row indices: `3, 12, 16, 21, 27, 28, 34, 35, 41, 42, 49, 50, 56, 57, 63, 64, 65`
- changed game_ids: `B06, B06, B06, B06, B06, C09, B06, C09, B06, C09, B06, C09, B06, C09, B06, C09, C09`

## 5. Remaining Blockers

From the historical coverage audit and the current fixture apply reports:

- `strategy_id` missing rows: `66`
- `lifecycle_state_at_prediction_time` missing rows: `66`
- `actual_result` missing rows before fixture apply: `66`
- `actual_result` missing rows after fixture apply: `49`
- readiness level: `BACKFILL_REQUIRED`

These are the true remaining blockers.

## 6. Corrected Current Gate Status

| Gate | Status | Evidence | Next action |
|---|---|---|---|
| Candidate export | complete | Read-only export and coverage audit reported 66 candidates, with no write-ready set | Keep as read-only source of truth |
| Approval manifest | complete | P20 manifest approved only `actual_result` | Keep unchanged |
| Dry-run write plan | complete | 17 items, every patch is `actual_result` only, all `dry_run_only = true` | No further action |
| Fixture apply | complete | 17 actual-result changes, 0 artifact-feature changes | Trust as actual-result-only fixture output |
| Artifact drift check | complete | P23 shows current fixture pair does not reproduce artifact drift | Supersede P22B |
| Readiness gate | blocked | `BACKFILL_REQUIRED` persists | Continue historical coverage work |
| UI unlock gate | blocked | `UI can start = false` | Do not start UI work |
| Production migration gate | blocked | `production migration can start = false` | Do not start production migration |

## 7. What Is Allowed Now

Allowed now:
- Read-only diagnostics and documentation.
- Historical coverage audits.
- Fixture-only validation and comparison.
- Further source tracing of missing historical identity fields.

## 8. What Is Forbidden Now

Forbidden now:
- Production DB writes.
- Historical registry mutation.
- Migration execution.
- Frontend implementation.
- Model retraining.
- Betting recommendation changes.
- CI changes.
- Production readiness claims.

## 9. Recommended Next Phase

Recommended next phase: `P25A Strategy Identity Source Recovery Audit`

Why:
- `strategy_id` is missing for `66/66` historical rows.
- `strategy_id` is mandatory for strategy grouping and UI readiness.
- Until strategy identity exists, lifecycle reconstruction and UI grouping remain weak.
- This is the highest-severity unresolved blocker after P23.

## 10. Next Worker Agent Prompt

Trace the source of historical `strategy_id` for the 66 Strategy Replay rows in `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` without mutating any data. Use the existing Strategy Replay reports and fixture JSONL files as the source of truth, and identify whether a trustworthy strategy identity source exists or whether a new authoritative source must be introduced.

## 11. Required Conclusions

- P23 is the controlling finding.
- P22B is superseded.
- P21 remains valid.
- artifact_feature_counts drift is not reproducible in the current fixture pair.
- after fixture is trustworthy as actual_result-only fixture output.
- readiness remains `BACKFILL_REQUIRED`.
- UI can start = false.
- production migration can start = false.
- the remaining blocker is `strategy_id` and `lifecycle_state_at_prediction_time` coverage.

## Validation Marker

P24_STRATEGY_REPLAY_GATE_RECONCILIATION_AFTER_P23_READY
