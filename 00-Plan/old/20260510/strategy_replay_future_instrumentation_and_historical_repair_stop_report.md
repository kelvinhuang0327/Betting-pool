# Strategy Replay Future Instrumentation and Historical Repair Stop Report

Date: 2026-05-10
Marker: P25E_STRATEGY_REPLAY_FUTURE_INSTRUMENTATION_AND_REPAIR_STOP_READY
Status: Completed

## 1. Executive Summary

Historical Strategy Replay identity repair is stopped. The current workspace does not contain a trustworthy historical source for `strategy_id` or `strategy_name`, and weak hints such as `decision_report.execution_strategy = SINGLE_BOOK` or `game_output.best_bet_strategy` must not be promoted into identity.

Future prediction rows are now explicitly instrumented to carry Strategy Replay metadata at write time, and missing identity or lifecycle fields remain visible as data-quality flags instead of being invented.

Current outcome:
- historical `strategy_id` repair stopped
- historical `strategy_name` repair stopped
- weak strategy hints are not valid identity
- future rows must carry explicit identity
- readiness remains `BACKFILL_REQUIRED` unless future rows meet contract
- UI can start = false
- production migration can start = false

## 2. Historical Repair Stop Decision

Historical repair stop policy:
- historical `strategy_id` repair is stopped
- historical `strategy_name` repair is stopped
- historical `lifecycle_state_at_prediction_time` repair remains blocked unless an explicit source is later found
- weak hints such as `SINGLE_BOOK` or `best_bet_strategy` must not be promoted into `strategy_id`
- historical rows may remain in limited replay mode only

The decision is based on the P25A recovery audit, which showed `SOURCE_NOT_FOUND` for `strategy_id` and `strategy_name` across all 66 historical rows.

## 3. Why Strategy Identity Remains SOURCE_NOT_FOUND

The repository does not provide a trustworthy historical identity source for the 66 historical rows.

Evidence:
- `data/wbc_backend/reports/prediction_registry.jsonl` has 66/66 rows with no `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, or `current_lifecycle_state` fields.
- `decision_report.execution_strategy` is always `SINGLE_BOOK`, which is an execution mode, not identity.
- `game_output.best_bet_strategy` is empty across the historical set.
- No authoritative strategy catalog or mapping table was found.
- The safe resolver in `wbc_backend/reporting/strategy_replay_instrumentation.py` only reads explicit fields and now keeps lifecycle state explicit-only.

Conclusion:
- `strategy_id` remains `SOURCE_NOT_FOUND`
- `strategy_name` remains `SOURCE_NOT_FOUND`

## 4. Future Instrumentation Contract

Future rows now have an explicit write-path contract in [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py) and [wbc_backend/reporting/prediction_registry.py](../../wbc_backend/reporting/prediction_registry.py).

Supported future-row fields:
- `strategy_id`
- `strategy_name`
- `lifecycle_state_at_prediction_time`
- `current_lifecycle_state`
- `canonical_outcome_key`
- `replay_metadata_version`
- `replay_instrumentation_source`
- `replay_data_quality_flags`

Contract behavior:
- explicit `strategy_id` is preserved
- explicit `strategy_name` is preserved
- explicit `lifecycle_state_at_prediction_time` is preserved
- missing `strategy_id` is flagged, not invented
- missing `strategy_name` is flagged, not invented
- missing `lifecycle_state_at_prediction_time` is flagged, not invented
- weak hints are not promoted to identity
- `replay_metadata_version` is written as `p7-1.0`
- `replay_instrumentation_source` is written as `wbc_backend.reporting.prediction_registry`

Important correction made in this task:
- `current_lifecycle_state` is no longer used to infer `lifecycle_state_at_prediction_time`
- historical lifecycle state remains explicit-only

## 5. Files Inspected

- [00-BettingPlan/20260510/strategy_replay_strategy_identity_source_recovery_audit.md](strategy_replay_strategy_identity_source_recovery_audit.md)
- [00-BettingPlan/20260510/strategy_replay_gate_reconciliation_after_p23.md](strategy_replay_gate_reconciliation_after_p23.md)
- [00-BettingPlan/20260510/strategy_replay_end_to_end_gate_map.md](strategy_replay_end_to_end_gate_map.md)
- [wbc_backend/domain/schemas.py](../../wbc_backend/domain/schemas.py)
- [wbc_backend/reporting/prediction_registry.py](../../wbc_backend/reporting/prediction_registry.py)
- [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py)
- [wbc_backend/pipeline/service.py](../../wbc_backend/pipeline/service.py)
- [wbc_backend/reporting/strategy_replay_service.py](../../wbc_backend/reporting/strategy_replay_service.py)
- [tests/test_strategy_replay_instrumentation.py](../../tests/test_strategy_replay_instrumentation.py)
- [tests/test_strategy_replay_prediction_instrumentation_write_path.py](../../tests/test_strategy_replay_prediction_instrumentation_write_path.py)
- [tests/test_strategy_replay_adapter.py](../../tests/test_strategy_replay_adapter.py)
- [tests/test_strategy_replay_readiness.py](../../tests/test_strategy_replay_readiness.py)

## 6. Files Changed

- [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py)
- [tests/test_strategy_replay_future_instrumentation_contract.py](../../tests/test_strategy_replay_future_instrumentation_contract.py)
- [00-BettingPlan/20260510/strategy_replay_future_instrumentation_and_historical_repair_stop_report.md](strategy_replay_future_instrumentation_and_historical_repair_stop_report.md)

## 7. Tests Added or Run

Added:
- [tests/test_strategy_replay_future_instrumentation_contract.py](../../tests/test_strategy_replay_future_instrumentation_contract.py)

Run:
- `./.venv/bin/python -m pytest tests/test_strategy_replay_future_instrumentation_contract.py -q`

Result:
- `4 passed`

## 8. PASS / FAIL Results

PASS:
- explicit future strategy identity is preserved
- missing strategy identity is flagged, not invented
- missing lifecycle state at prediction time is flagged, not invented
- weak hints are not promoted to identity
- legacy rows remain backward compatible through the read-only adapter path
- no production DB access

FAIL:
- none in this slice

## 9. Historical Limited-Mode Decision

Historical rows without `strategy_id` cannot be shown as normal Strategy Replay rows.

They may only be shown in a limited mode such as:
- `HISTORICAL_UNATTRIBUTED_MODE`
- `UNATTRIBUTED_PREDICTION_AUDIT_MODE`
- `DATA_QUALITY_LIMITED_MODE`

This mode is not `UI_MVP_READY`.
This mode cannot claim strategy lifecycle replay.
This mode can only support data-quality or prediction-result audit.

## 10. Impact on Readiness

Readiness remains `BACKFILL_REQUIRED`.

Why:
- historical `strategy_id` remains missing
- historical `strategy_name` remains missing
- historical `lifecycle_state_at_prediction_time` remains blocked
- future instrumentation is now explicit, but historical rows are still incomplete

## 11. UI and Production Verdict

- UI can start = false
- production migration can start = false

## 12. Recommended Next Phase

Recommended next phase: keep historical repair stopped and enforce the future write contract on all new prediction rows.

That means:
- keep historical rows in limited unattributed mode only
- require explicit `strategy_id`, `strategy_name`, and `lifecycle_state_at_prediction_time` for new replayable rows
- continue read-only validation until future rows consistently satisfy the contract

## 13. Next Worker Agent Prompt

Validate the live prediction entry points that call `append_prediction_record` and ensure every new prediction-producing path populates explicit `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, `current_lifecycle_state`, and `canonical_outcome_key`, while keeping historical rows in limited unattributed mode only.

## 14. Required Conclusions

- historical strategy_id repair stopped
- historical strategy_name repair stopped
- weak strategy hints are not valid identity
- future rows must carry explicit identity
- readiness remains BACKFILL_REQUIRED unless future rows meet contract
- UI can start = false
- production migration can start = false

## Validation Marker

P25E_STRATEGY_REPLAY_FUTURE_INSTRUMENTATION_AND_REPAIR_STOP_READY
