# Strategy Replay Artifact Drift Source Trace Report

Date: 2026-05-10
Status: Read-only trace completed
Marker: P23_STRATEGY_REPLAY_ARTIFACT_DRIFT_SOURCE_TRACE_READY

## 1. Executive Summary

The P22B artifact-drift finding is not reproducible on the current fixture files.

Current evidence shows:
- `fixture_prediction_registry_before_actual_result_apply.jsonl` is byte-equivalent to the live `data/wbc_backend/reports/prediction_registry.jsonl` for the same rows.
- `fixture_prediction_registry_after_actual_result_apply.jsonl` differs from the before fixture only by `actual_result` patches.
- `artifact_feature_counts` did **not** change between before and after fixtures.
- The apply helper and write plan both only authorize `actual_result`.

Conclusion:
- The current P21 fixture apply result is trustworthy.
- The earlier P22B mixed-delta conclusion should be superseded.
- No clean re-output fixture was needed.

Readiness:
- BACKFILL_REQUIRED
- UI can start = false
- production migration can start = false

## 2. Reproduced Result

Exact recomputed delta between the two fixture files:
- before rows: 66
- after rows: 66
- changed rows: 17
- unchanged rows: 49
- added rows: 0
- removed rows: 0
- rows with only `actual_result` changed: 17
- rows with only `artifact_feature_counts` changed: 0
- rows with both changed: 0
- rows with other fields changed: 0

Changed row indices:
- 3, 12, 16, 21, 27, 28, 34, 35, 41, 42, 49, 50, 56, 57, 63, 64, 65

Changed game_ids:
- B06, B06, B06, B06, B06, C09, B06, C09, B06, C09, B06, C09, B06, C09, B06, C09, C09

## 3. Source Trace Findings

The apply path is clean and narrow:
- `scripts/apply_strategy_replay_backfill_write_plan_fixture.py` loads rows and the write plan, then delegates to `apply_write_plan_to_rows()`.
- `wbc_backend/reporting/strategy_replay_backfill_apply.py` deep-copies each row before patching.
- `_apply_patch_to_row()` only iterates through `approved_fields` and only copies values from `proposed_values`.
- Unknown fields are preserved because the helper patches only the approved fields on a copied row.

The write plan is also pure:
- The P20 write plan contains 17 items.
- Every item has `approved_fields: ["actual_result"]`.
- No item includes `artifact_feature_counts`.
- No item includes deployment gate patches.
- Every item is `dry_run_only: true`.

The fixture source is stable:
- `before` fixture equals the live `prediction_registry.jsonl` exactly for the covered rows.
- `after` fixture equals `before` when `actual_result` is stripped.
- `postgame_results.jsonl` matches every filled `actual_result` in the `after` fixture.

No evidence was found that the fixture apply process mixed in newer prediction rows, model artifacts, or registry regeneration output.

## 4. Root Cause Classification

`UNKNOWN_REQUIRES_MANUAL_REVIEW`

Reason:
- The current repo state does not reproduce the P22B drift claim.
- There is no code-path evidence that the apply helper touched `artifact_feature_counts`.
- There is no write-plan evidence that `artifact_feature_counts` was ever requested.
- The most likely explanation is that the earlier P22B drift report was a stale or incorrect audit artifact, not a real fixture mutation.

## 5. Write Plan Purity Check

Verified against `00-BettingPlan/20260510/strategy_replay_safe_actual_result_write_plan.json`:
- exactly 17 items: yes
- every `proposed_patch` contains only `actual_result`: yes
- no `artifact_feature_counts` in the write plan: yes
- no deployment gate patch in the write plan: yes
- no model artifact metadata patch in the write plan: yes
- every item `dry_run_only = true`: yes

## 6. Apply Helper Safety Check

Verified against `wbc_backend/reporting/strategy_replay_backfill_apply.py`:
- patches only approved fields: yes
- preserves unknown fields: yes
- mutates input rows in place: no, it deep-copies rows first
- can alter nested `deployment_gate` fields accidentally: no evidence of that in the helper
- matches rows by candidate/source tokens, not by model artifact metadata: yes

Verdict:
- The helper is safe for the approved actual-result-only fixture apply.

## 7. Contamination Check

Is the after fixture contaminated?
- No.

Evidence:
- `before_equals_registry = true`
- `before_equals_registry_without_actual_result = true`
- `after_equals_before_without_actual_result = true`
- `artifact_feature_counts_after` remained split only between the existing 32 and 37 values already present in the same row set, with no before/after delta.
- The only row-level delta between before and after is `actual_result`.

## 8. Clean Fixture Output

A clean recomputed fixture output was not created.

Reason:
- The current after fixture is already clean with respect to the approved apply scope.
- No repair of the fixture file was required.

## 9. Corrected Before/After Delta

Corrected delta for the current files:
- `actual_result` changed count: 17
- `artifact_feature_counts` changed count: 0
- other fields changed count: 0

## 10. Impact on P21 Conclusion

P21 remains valid.

The P21 apply report stating that the fixture-only apply changes `actual_result` only is supported by the current files and should not be corrected.

The P22B mixed-delta conclusion should be superseded.

## 11. Impact on Readiness

Readiness remains:
- BACKFILL_REQUIRED

Why:
- strategy_id remains missing
- lifecycle_state_at_prediction_time remains missing
- the fixture apply does not resolve the gating fields that block UI and migration readiness

## 12. UI / Production Verdict

- UI can start = false
- production migration can start = false

## 13. Recommended Next Phase

Treat the current P21 fixture apply as the authoritative fixture-only actual-result backfill result.

If further investigation is needed, trace the provenance of the earlier P22B audit output itself, not the fixture apply path.

## 14. Next Worker Agent Prompt

Audit the earlier P22B analysis artifact and determine why it reported artifact_feature_counts drift even though the current fixture files reproduce as actual_result-only changes.

## 15. Required Conclusions

- Did the P20 write plan include artifact_feature_counts? No.
- Did the apply helper mutate artifact_feature_counts? No.
- Was the after fixture generated from the correct before fixture? Yes.
- Is the P21 after fixture trustworthy? Yes.
- Should P21 be corrected / superseded? P21 should remain; P22B should be superseded.
- Does readiness remain BACKFILL_REQUIRED? Yes.
- Can UI start? No.
- Can production migration start? No.

## Validation Marker

P23_STRATEGY_REPLAY_ARTIFACT_DRIFT_SOURCE_TRACE_READY
