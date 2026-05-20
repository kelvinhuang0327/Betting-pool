# Strategy Replay Fixture Snapshot File-Level Delta Audit

## Executive Summary

This audit compares:
- `00-BettingPlan/20260510/fixture_prediction_registry_before_actual_result_apply.jsonl`
- `00-BettingPlan/20260510/fixture_prediction_registry_after_actual_result_apply.jsonl`

Root classification: `MIXED_RESULT_BACKFILL_AND_MODEL_ARTIFACT_DELTA`

Conclusion:
- The after snapshot did **not** change only `actual_result`.
- The after snapshot also changed model artifact feature counts.
- The earlier P21 conclusion must be corrected.

Readiness:
- BACKFILL_REQUIRED
- UI can start = false
- production migration can start = false

## Exact Row Diff

- before rows: `13`
- after rows: `31`
- changed rows: `10`
- unchanged rows: `3`
- added rows: `18`
- removed rows: `0`
- changed row indices: `0, 1, 2, 3, 7, 9, 10, 11, 12, 13`
- changed game_ids: `A05, D05, D06, B06, A05, B06, D05, D06, B06, A05`

## Exact Field-Level Diff Categories

- actual_result_only_changed: `1`
- artifact_feature_counts_only_changed: `0`
- actual_result_and_artifact_feature_counts_changed: `1`
- other_fields_changed: `8`

## Actual Result Delta

- actual_result rows added: `2`
- actual_result values were verified against `data/wbc_backend/reports/postgame_results.jsonl`
- actual_result matches postgame_results.jsonl: `true`

## Artifact Feature Count Delta

- artifact_feature_counts 32 -> 37 count: `8`
- feature_count 32: `8`
- feature_count 37: `8`
- first 10 affected row indices and game_ids:
  - `0 | A05`
  - `1 | D05`
  - `2 | D06`
  - `3 | B06`
  - `7 | A05`
  - `9 | B06`
  - `10 | D05`
  - `11 | D06`
  - `12 | B06`
  - `13 | A05`
- model counts:
  - xgboost: `8`
  - lightgbm: `8`
  - catboost: `8`
  - neural_net: `8`
- all models changed consistently: `true`

## Gate Field Stability

These fields remained stable across the sampled changed rows:
- selected_calibration: unchanged
- walkforward_min_games: unchanged
- walkforward_brier: unchanged
- ml_roi: unchanged
- deployment_gate.status: unchanged

## Readiness Verdict

- BACKFILL_REQUIRED
- UI can start = false
- production migration can start = false

## Root Cause Classification

`MIXED_RESULT_BACKFILL_AND_MODEL_ARTIFACT_DELTA`

Reason:
- actual_result was backfilled in the after snapshot
- artifact_feature_counts also changed from 32 to 37
- the change was not a pure result-only backfill
- the change was not artifact-only either because actual_result additions are present

## Recommended Next Phase

Trace the generator that produced the after snapshot and determine why the feature space changed from 32 to 37 while actual_result was being backfilled.

## Next Worker Agent Prompt

Trace the generator that wrote `00-BettingPlan/20260510/fixture_prediction_registry_after_actual_result_apply.jsonl` and explain why `artifact_feature_counts` changed from 32 to 37 while `actual_result` backfill was also applied.

## Validation Marker

P22B_STRATEGY_REPLAY_FIXTURE_SNAPSHOT_FILE_LEVEL_DELTA_AUDIT_READY
