# Strategy Replay Safe Actual Result Backfill Candidates Report

Date: 2026-05-10
Status: Read-only candidate export
Marker: P18_STRATEGY_REPLAY_SAFE_ACTUAL_RESULT_BACKFILL_CANDIDATES_READY

## What Was Exported

- Exported 17 Strategy Replay rows with a safe exact-match actual_result repair path.
- Export file: 00-BettingPlan/20260510/strategy_replay_safe_actual_result_backfill_candidates.jsonl
- Each candidate includes prediction_row_index, game_id, canonical_outcome_key, matched_outcome_source_ref, proposed_actual_result, confidence = HIGH, repairability = SAFE_TO_REPAIR, unsafe_to_infer_fields = [strategy_id, lifecycle_state_at_prediction_time], and a note that the row is still not UI_MVP_READY.

## Why These 17 Rows Are Safe

- The match is exact on game_id against data/wbc_backend/reports/postgame_results.jsonl.
- No inference is used for actual_result.
- The candidate set is read-only and does not mutate the historical registry.
- The export is suitable for review/approval workflow only.

## Why This Still Does Not Unlock UI

- strategy_id is still SOURCE_NOT_FOUND for all 66 historical rows.
- lifecycle_state_at_prediction_time is still SOURCE_NOT_FOUND for all 66 historical rows.
- The readiness gate therefore remains BACKFILL_REQUIRED.
- UI can start = false.

## Migration And UI Status

- production migration can start = false
- UI can start = false
- The safe actual_result repair list does not change the production or UI gates.

## Next Worker Prompt

Produce a review-only approval manifest for the 17 safe candidates, then keep the remaining 49 rows explicitly marked as NO_MATCH without inferring strategy_id or historical lifecycle state.
