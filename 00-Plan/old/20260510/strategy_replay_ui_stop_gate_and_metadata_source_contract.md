# Strategy Replay UI Stop Gate and Metadata Source Contract

Date: 2026-05-10
Marker: P27D_STRATEGY_REPLAY_UI_STOP_GATE_AND_METADATA_SOURCE_CONTRACT_READY
Status: Completed

## 1. Executive Summary

Strategy Replay UI remains stopped. The repository still does not have a valid metadata source for future strategy identity injection, and historical repair has already been stopped. The UI cannot start until a trustworthy metadata source exists and the future write path proves it is writing explicit fields.

Current conclusions:
- UI can start = false
- production migration can start = false
- future rows must carry explicit identity
- metadata source does not currently exist
- SINGLE_BOOK is not strategy_id
- best_bet_strategy is not strategy_id
- current_lifecycle_state cannot infer lifecycle_state_at_prediction_time
- strategy_id query filter is not a write source

## 2. Current State

The source audits show the same pattern across the workspace:
- `AnalyzeRequest` can hold the required metadata.
- `wbc_backend/api/app.py`, `wbc_backend/run.py`, `examples/run_pipeline.py`, and `scripts/replay_build_registry.py` do not currently inject strategy metadata.
- `orchestrator/api.py` only exposes `strategy_id` as a history query filter.
- `wbc_backend/reporting/strategy_replay_instrumentation.py` preserves explicit metadata and rejects inference.
- historical repair is stopped.

## 3. Why UI Is Stopped

UI is stopped because Strategy Replay cannot claim a complete strategy contract without a real metadata source.

Blocking reasons:
- missing strategy_id source
- missing strategy_name source
- missing lifecycle_state_at_prediction_time source
- future rows are not yet proven to be written with explicit strategy metadata from a durable upstream source
- readiness is not `UI_MVP_READY`

## 4. Why Production Migration Is Stopped

Production migration is stopped for the same reason plus the readiness gate.

Blocking reasons:
- `BACKFILL_REQUIRED` remains the current readiness state
- future metadata injection is source-bound, not source-complete
- historical rows remain unattributed
- the repo does not contain a durable source that can safely own the required metadata

## 5. Metadata Source Contract

Required fields for any source that wants to feed Strategy Replay future writes:
- `source_id`
- `source_name`
- `provided_fields`
- `explicit_identity = true`
- `lifecycle_snapshot_time`
- `owner/module`
- `durability`
- `auditability`
- `allowed_for_future_writes`
- `allowed_for_historical_backfill = false` unless explicit evidence exists
- `failure_modes`
- `validation_rules`

Validation rules:
- `strategy_id` must be explicit
- `strategy_name` must be explicit
- `lifecycle_state_at_prediction_time` must be explicit
- `current_lifecycle_state` cannot replace `lifecycle_state_at_prediction_time`
- `SINGLE_BOOK` is an unsafe hint
- `best_bet_strategy` is an unsafe hint
- read/query filter `strategy_id` is not a write source

## 6. Unsafe Hints

These are not valid strategy identity sources:
- `decision_report.execution_strategy = SINGLE_BOOK`
- `game_output.best_bet_strategy`
- `prediction.sub_model_results[].model_name`
- `orchestrator/api.py` `strategy_id` query filter

## 7. Allowed Modes

Allowed modes are limited to read-only or explicit non-production mock/spec handling.

Examples:
- `HISTORICAL_UNATTRIBUTED_MODE`
- `UNATTRIBUTED_PREDICTION_AUDIT_MODE`
- `DATA_QUALITY_LIMITED_MODE`
- explicitly approved non-production mock-data/spec mode

## 8. Forbidden Modes

Forbidden modes:
- normal Strategy Replay UI launch
- production migration launch
- any mode that infers identity from weak hints
- any mode that uses `current_lifecycle_state` as a substitute for historical lifecycle snapshot
- any mode that treats query filters as write sources

## 9. Gate Decision Table

| Condition | UI can start | Production migration can start |
|---|---|---|
| Missing any explicit metadata source | false | false |
| Readiness = `BACKFILL_REQUIRED` | false | false |
| Explicit non-production mock-data mode approved, but readiness not `UI_MVP_READY` | true for mock-data only | false |
| All required metadata sources exist and readiness = `UI_MVP_READY` | true | true only if production-approved |

## 10. Required Next Implementation Options

1. `P28A Strategy Metadata Source Registry Skeleton`
2. `P28B Orchestrator Strategy Metadata Injection Patch`
3. `P28C Strategy Lifecycle Store Contract`
4. `P28D UI Mock-Data Spec Only`

Recommended default:
- `P28A Strategy Metadata Source Registry Skeleton`

Reason:
- before runtime injection can be patched, the repo needs a durable, auditable metadata source that explicitly owns `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, and `current_lifecycle_state`.

## 11. Recommended Next Phase

Continue to stop UI work until the metadata source contract exists and can be validated end-to-end. If a source is later introduced, use it to patch the runtime request builders before any UI work resumes.

## 12. Next Worker Agent Prompt

Define a concrete metadata source registry or lifecycle store contract for Strategy Replay, then map the runtime request builders to that source without inferring any identity fields and without touching historical registry files.

## 13. Required Conclusions

- UI can start = false
- production migration can start = false
- future rows must carry explicit identity
- metadata source does not currently exist
- SINGLE_BOOK is not strategy_id
- best_bet_strategy is not strategy_id
- current_lifecycle_state cannot infer lifecycle_state_at_prediction_time
- strategy_id query filter is not a write source

## Validation Marker

P27D_STRATEGY_REPLAY_UI_STOP_GATE_AND_METADATA_SOURCE_CONTRACT_READY
