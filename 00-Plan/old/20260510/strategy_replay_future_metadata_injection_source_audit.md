# Strategy Replay Future Metadata Injection Source Audit

Date: 2026-05-10
Marker: P26_STRATEGY_REPLAY_FUTURE_METADATA_INJECTION_SOURCE_AUDIT_READY
Status: Completed

## 1. Executive Summary

The current repository does not expose a trustworthy production source for future Strategy Replay metadata injection. `AnalyzeRequest` can carry the required fields, but the runtime callers are not populating them, and there is no strategy registry or lifecycle store in the current workspace that can safely backfill them automatically.

Current outcome:
- future `strategy_id` must be explicit
- future `strategy_name` must be explicit
- future `lifecycle_state_at_prediction_time` must be explicit
- `current_lifecycle_state` may be explicit, but it cannot replace the historical snapshot
- missing fields must remain flagged, not inferred
- UI can start = false
- production migration can start = false

## 2. Sources Inspected

Read-only sources inspected for this audit:
- [00-BettingPlan/20260510/strategy_replay_future_instrumentation_and_historical_repair_stop_report.md](strategy_replay_future_instrumentation_and_historical_repair_stop_report.md)
- [tests/test_strategy_replay_future_instrumentation_contract.py](../../tests/test_strategy_replay_future_instrumentation_contract.py)
- [wbc_backend/domain/schemas.py](../../wbc_backend/domain/schemas.py)
- [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py)
- [wbc_backend/reporting/prediction_registry.py](../../wbc_backend/reporting/prediction_registry.py)
- [wbc_backend/pipeline/service.py](../../wbc_backend/pipeline/service.py)
- [orchestrator/api.py](../../orchestrator/api.py)
- [wbc_backend/api/app.py](../../wbc_backend/api/app.py)
- [wbc_backend/run.py](../../wbc_backend/run.py)
- [examples/run_pipeline.py](../../examples/run_pipeline.py)
- [scripts/replay_build_registry.py](../../scripts/replay_build_registry.py)
- [tests/test_strategy_replay_prediction_instrumentation_write_path.py](../../tests/test_strategy_replay_prediction_instrumentation_write_path.py)

## 3. Current Metadata Coverage

### Schema coverage

`AnalyzeRequest` already has the right fields:
- `strategy_id`
- `strategy_name`
- `lifecycle_state_at_prediction_time`
- `current_lifecycle_state`
- `canonical_outcome_key`

This means the data contract can carry the metadata, but the contract alone is not a production source.

### Runtime caller coverage

Current runtime entrypoints build `AnalyzeRequest` without strategy metadata:
- [wbc_backend/api/app.py](../../wbc_backend/api/app.py) builds request with `game_id`, `line_total`, `line_spread_home`, and `force_retrain` only.
- [wbc_backend/run.py](../../wbc_backend/run.py) builds request with `game_id`, `line_total`, and `line_spread_home` only.
- [examples/run_pipeline.py](../../examples/run_pipeline.py) does the same.
- [scripts/replay_build_registry.py](../../scripts/replay_build_registry.py) also creates `AnalyzeRequest` without strategy metadata.

### Write path coverage

The write path already preserves explicit metadata when supplied:
- [wbc_backend/pipeline/service.py](../../wbc_backend/pipeline/service.py) passes the request into `append_prediction_record`.
- [wbc_backend/reporting/prediction_registry.py](../../wbc_backend/reporting/prediction_registry.py) writes the replay metadata payload returned by the instrumentation helper.
- [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py) preserves explicit identity and flags missing values.

### API / query coverage

[orchestrator/api.py](../../orchestrator/api.py) exposes `strategy_id` as a query parameter for the Strategy Replay history endpoint, but that is only a read/filter parameter. It is not a source for future prediction creation.

## 4. Safe Source Candidates

| Candidate | Classification | Reason |
|---|---|---|
| `AnalyzeRequest` schema fields | SAFE_SOURCE | The schema can carry explicit metadata without guessing. This is the correct container for the future-row contract. |
| `wbc_backend/api/app.py` request construction | NEEDS_NEW_SOURCE | It currently builds requests with only game/line inputs. Metadata can be injected here only after a real upstream source is added. |
| `wbc_backend/run.py` CLI request construction | NEEDS_NEW_SOURCE | Same issue as the API path: the request object exists, but the metadata source does not. |
| `current_lifecycle_state` request field | NEEDS_NEW_SOURCE | The field exists, but no production caller populates it yet. It cannot substitute for the historical snapshot. |
| `wbc_backend/pipeline/service.py` | SAFE_SOURCE for write preservation, not origin | The service can preserve what it receives, but it is not a trusted source of truth. |
| `wbc_backend/reporting/prediction_registry.py` | SAFE_SOURCE for persistence, not origin | It writes metadata forward, but does not create it. |

## 5. Unsafe Hints

| Hint | Classification | Why it is unsafe |
|---|---|---|
| `decision_report.execution_strategy = SINGLE_BOOK` | UNSAFE_HINT | Execution mode is not strategy identity. It is a weak behavioral label and must not become `strategy_id`. |
| `game_output.best_bet_strategy` | UNSAFE_HINT | It is a bet description / display string, not a stable strategy identifier. |
| `prediction.sub_model_results[].model_name` | UNSAFE_HINT | Model names describe ensemble components, not the strategy identity of the prediction row. |
| `orchestrator/api.py` history filter `strategy_id` | UNSAFE_HINT | This is a read-time query filter for replay history, not a write-time metadata source. |

## 6. Current Injection Trace

Current trace for a future prediction row:

1. The user or caller triggers `wbc_backend/api/app.py` or `wbc_backend/run.py`.
2. An `AnalyzeRequest` is created.
3. The request is passed into `PredictionService.analyze()`.
4. `PredictionService.analyze()` eventually calls `append_prediction_record()`.
5. `append_prediction_record()` forwards the request and replay payload to the registry writer.
6. `build_prediction_write_path_replay_metadata()` preserves explicit values and flags missing ones.

Current gap:
- step 1 does not supply strategy metadata
- therefore step 2 builds an incomplete request
- therefore the write path can only preserve missing values as flags

## 7. Required Injection Contract

Future-row requirements:
- `strategy_id` must be explicit
- `strategy_name` must be explicit
- `lifecycle_state_at_prediction_time` must be explicit
- `current_lifecycle_state` may be explicit but cannot replace the historical snapshot
- `canonical_outcome_key` must remain explicit or be safely derived from a stable game identifier only when clearly marked as a fallback
- missing fields must remain flagged, not inferred
- weak hints must never be promoted into identity

The future instrumentation contract already enforces this behavior in the write path.

## 8. Recommended Implementation Path

Recommended path: `P27D Stop Strategy Replay UI Until Metadata Source Exists`

Why:
- there is currently no trustworthy production source for future strategy metadata injection
- the request schema exists, but runtime callers do not populate the fields
- no strategy registry or lifecycle store exists in the current workspace to serve as an authoritative source
- pushing UI forward before the source exists would preserve incomplete rows and keep the replay contract ambiguous

Secondary follow-up once a source is chosen:
- `P27A API Request Metadata Injection Patch` can be used later to thread the explicit metadata into the request builders
- but that patch should wait until the upstream source is defined

## 9. Whether UI and Production Can Start

- UI can start = false
- production migration can start = false

Reason:
- future metadata injection is still source-bound, not source-complete
- the strategy replay page cannot claim a complete strategy contract until the runtime request path supplies explicit identity and lifecycle snapshot values

## 10. Files Changed

- [00-BettingPlan/20260510/strategy_replay_future_metadata_injection_source_audit.md](strategy_replay_future_metadata_injection_source_audit.md)

## 11. Tests Observed

No new code tests were required for this audit-only pass.

Observed contract coverage already exists in:
- [tests/test_strategy_replay_future_instrumentation_contract.py](../../tests/test_strategy_replay_future_instrumentation_contract.py)
- [tests/test_strategy_replay_prediction_instrumentation_write_path.py](../../tests/test_strategy_replay_prediction_instrumentation_write_path.py)

## 12. Next Worker Agent Prompt

Trace the production request builders in [wbc_backend/api/app.py](../../wbc_backend/api/app.py) and [wbc_backend/run.py](../../wbc_backend/run.py), then propose a concrete upstream source for `strategy_id`, `strategy_name`, and `lifecycle_state_at_prediction_time`. Do not implement a UI change until the source is explicit and reproducible.

## 13. Required Conclusions

- strategy_id
- strategy_name
- lifecycle_state_at_prediction_time
- SAFE_SOURCE
- UNSAFE_HINT
- future rows must carry explicit identity
- UI can start = false
- production migration can start = false

## Validation Marker

P26_STRATEGY_REPLAY_FUTURE_METADATA_INJECTION_SOURCE_AUDIT_READY
