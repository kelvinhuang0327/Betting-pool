# Strategy Replay Runtime Metadata Injection Patch Report

Date: 2026-05-10
Marker: P28B_STRATEGY_REPLAY_RUNTIME_METADATA_INJECTION_PATCH_READY
Status: Completed

## 1. Executive Summary

A future-only, explicit Strategy Replay runtime metadata injection path now exists. It loads only from a validated registry, resolves an explicit `strategy_id`, and passes the registry-backed `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, and `current_lifecycle_state` into `AnalyzeRequest` only when the metadata is resolved safely.

Current conclusions:
- runtime injection is explicit-only
- no historical rows were mutated
- unresolved metadata falls back to the existing missing-field path
- strict mode blocks unresolved or unsafe registry inputs
- the runtime path remains backward compatible when no registry is supplied

## 2. What Was Implemented

Implemented:
- [wbc_backend/reporting/strategy_replay_runtime_metadata.py](../../wbc_backend/reporting/strategy_replay_runtime_metadata.py)
- [wbc_backend/api/app.py](../../wbc_backend/api/app.py)
- [wbc_backend/run.py](../../wbc_backend/run.py)
- [examples/run_pipeline.py](../../examples/run_pipeline.py)
- [scripts/replay_build_registry.py](../../scripts/replay_build_registry.py)
- [tests/test_strategy_replay_runtime_metadata_injection.py](../../tests/test_strategy_replay_runtime_metadata_injection.py)

The runtime helper provides:
- `load_runtime_strategy_metadata_registry`
- `resolve_runtime_strategy_metadata`
- `build_analyze_request_replay_metadata`
- `validate_runtime_metadata_injection_inputs`
- `prepare_runtime_strategy_metadata_request_kwargs`

## 3. What Was Not Implemented

Not implemented:
- historical identity repair
- UI integration changes
- production data migration
- database writes for strategy metadata
- any inference from weak hints or query filters

## 4. Files Changed

- [wbc_backend/reporting/strategy_replay_runtime_metadata.py](../../wbc_backend/reporting/strategy_replay_runtime_metadata.py)
- [wbc_backend/api/app.py](../../wbc_backend/api/app.py)
- [wbc_backend/run.py](../../wbc_backend/run.py)
- [examples/run_pipeline.py](../../examples/run_pipeline.py)
- [scripts/replay_build_registry.py](../../scripts/replay_build_registry.py)
- [tests/test_strategy_replay_runtime_metadata_injection.py](../../tests/test_strategy_replay_runtime_metadata_injection.py)
- [00-BettingPlan/20260510/strategy_replay_runtime_metadata_injection_patch_report.md](strategy_replay_runtime_metadata_injection_patch_report.md)

## 5. Tests Run

Run:
- `./.venv/bin/python -m pytest -q tests/test_strategy_replay_runtime_metadata_injection.py`
- `./.venv/bin/python -m pytest -q tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_deployment_gate_and_registry.py`

Result:
- `19 passed`

## 6. PASS / FAIL Results

PASS:
- explicit registry resolution injects strategy metadata into `AnalyzeRequest`
- missing registry falls back to the existing missing-field path in non-strict mode
- strict mode blocks missing registry and unknown `strategy_id`
- invalid registry source hints such as `SINGLE_BOOK` and `best_bet_strategy` are rejected
- `allowed_for_future_writes = true` is required
- `allowed_for_historical_backfill = false` remains unchanged
- backward-compatible `AnalyzeRequest` creation still works without metadata
- no production DB access

FAIL:
- none in this slice

## 7. Whether Metadata Source Now Exists

Yes, for future runtime requests only.

The injection path is explicit and validated. It does not recover or repair historical strategy identity, and it does not invent metadata when the registry cannot be resolved.

## 8. Whether Runtime Injection Can Start

Yes, for future explicit registry-backed request builders.

The safe start condition is:
- explicit `strategy_id`
- explicit registry path or preloaded registry records
- validated registry entry with future-write permission

## 9. Whether UI Can Start

- UI can start = false

Reason:
- this patch only wires runtime request construction
- the UI stop gate remains a separate policy surface
- no UI flow was added or unlocked here

## 10. Whether Production Migration Can Start

- production migration can start = false

Reason:
- no historical mutation was performed
- no production registry source was introduced
- the patch is runtime-only and explicit-only

## 11. Remaining Blockers

- no UI integration change
- no production rollout decision
- no live registry ownership process
- no historical repair path

## 12. Recommended Next Phase

Recommended next phase: keep all future runtime calls on the explicit registry-backed path and leave historical repair blocked.

Why:
- the request builders now support explicit metadata injection
- the write path already persists those request fields
- the remaining risk is policy and ownership, not code plumbing

## 13. Next Worker Agent Prompt

If further work is needed, extend the explicit registry-backed path only where future request construction happens, and do not touch historical prediction rows.

## 14. Required Conclusions

- runtime injection is explicit-only
- no historical rows were mutated
- unresolved metadata falls back to the existing missing-field path
- strict mode blocks unresolved or unsafe registry inputs
- backward compatibility remains intact when no registry is supplied

## Validation Marker

P28B_STRATEGY_REPLAY_RUNTIME_METADATA_INJECTION_PATCH_READY
