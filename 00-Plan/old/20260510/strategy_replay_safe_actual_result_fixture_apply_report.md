# Strategy Replay Safe Actual Result Fixture Apply Report

Date: 2026-05-10
Status: Fixture-only apply
Marker: P21_STRATEGY_REPLAY_SAFE_ACTUAL_RESULT_FIXTURE_APPLY_READY

## What Was Applied

- Applied the P20 dry-run write plan to a fixture copy only.
- Applied fields: actual_result
- Original registry remained untouched: data/wbc_backend/reports/prediction_registry.jsonl

## Fixture Paths

- Before fixture: 00-BettingPlan/20260510/fixture_prediction_registry_before_actual_result_apply.jsonl
- After fixture: 00-BettingPlan/20260510/fixture_prediction_registry_after_actual_result_apply.jsonl

## Apply Summary

- applied_count = 17
- skipped_count = 0
- unchanged_count = 49

## Readiness Before / After

- readiness_before = BACKFILL_REQUIRED
- readiness_after = BACKFILL_REQUIRED
- missing_strategy_id_before = 66
- missing_strategy_id_after = 66
- missing_lifecycle_state_at_prediction_time_before = 66
- missing_lifecycle_state_at_prediction_time_after = 66
- missing_actual_result_before = 49
- missing_actual_result_after = 49

## Why This Still Does Not Unlock UI

- strategy_id remains missing for 66/66 rows.
- lifecycle_state_at_prediction_time remains missing for 66/66 rows.
- The fixture-only apply changes actual_result only.
- The readiness gate therefore remains BACKFILL_REQUIRED.
- UI can start = false.

## Why Production Migration Still Cannot Start

- The apply was performed on a temporary fixture copy, not on the historical registry.
- No production DB write or migration execution occurred.
- The unresolved identity and lifecycle fields remain blocked.
- production migration can start = false

## Next Worker Prompt

Review the fixture-only actual_result delta, keep strategy_id and lifecycle_state_at_prediction_time blocked, and do not escalate this fixture result into production migration.
