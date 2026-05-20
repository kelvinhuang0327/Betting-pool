# Strategy Replay Prediction Write Path Instrumentation Report

Date: 2026-05-10
Repo: Betting-pool
Status: Future prediction writes now carry replay metadata when the upstream request provides it; no backfill and no UI work

## What Was Implemented

- `AnalyzeRequest` now supports optional replay context fields in [wbc_backend/domain/schemas.py](wbc_backend/domain/schemas.py): `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, `current_lifecycle_state`, and `canonical_outcome_key`.
- `append_prediction_record()` now writes replay metadata into the prediction registry JSONL in [wbc_backend/reporting/prediction_registry.py](wbc_backend/reporting/prediction_registry.py).
- A pure write-path helper at [wbc_backend/reporting/strategy_replay_instrumentation.py](wbc_backend/reporting/strategy_replay_instrumentation.py) now resolves replay metadata for prediction writes without inventing missing values.
- The new write-path metadata includes `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, `current_lifecycle_state`, `canonical_outcome_key`, `canonical_outcome_key_source`, `canonical_outcome_key_used_fallback`, `replay_metadata_version`, `replay_instrumentation_source`, `replay_data_quality_flags`, and `replay_data_quality_flag_count`.
- Regression coverage at [tests/test_strategy_replay_prediction_instrumentation_write_path.py](tests/test_strategy_replay_prediction_instrumentation_write_path.py) now verifies:
  - supplied strategy / lifecycle / canonical fields are persisted
  - missing values are flagged instead of being invented
  - fallback canonical keys are flagged
  - legacy JSONL rows remain readable through the replay adapter

## What Was Not Implemented

- No historical backfill.
- No frontend UI.
- No registry migration.
- No production DB writes.
- No change to the public analysis API shape beyond optional compatibility fields.
- No readiness gate promotion yet.

## Files Changed

- [wbc_backend/domain/schemas.py](wbc_backend/domain/schemas.py)
- [wbc_backend/reporting/strategy_replay_instrumentation.py](wbc_backend/reporting/strategy_replay_instrumentation.py)
- [wbc_backend/reporting/prediction_registry.py](wbc_backend/reporting/prediction_registry.py)
- [tests/test_strategy_replay_prediction_instrumentation_write_path.py](tests/test_strategy_replay_prediction_instrumentation_write_path.py)
- [00-BettingPlan/20260510/strategy_replay_prediction_write_path_instrumentation_report.md](00-BettingPlan/20260510/strategy_replay_prediction_write_path_instrumentation_report.md)

## Tests Run

- `./.venv/bin/python -m pytest -q tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_deployment_gate_and_registry.py`

## PASS / FAIL

- PASS: future prediction registry writes now persist replay metadata when the caller supplies it.
- PASS: missing replay values are represented by explicit flags instead of being fabricated.
- PASS: legacy JSONL rows still load through the replay adapter.
- PASS: the existing registry/deployment gate regression file still passes.
- FAIL: readiness is still not `UI_MVP_READY` because this change only stops the gap from growing; it does not backfill historical rows.

## Current Readiness Level

`BACKFILL_REQUIRED`

This remains the correct gate state because future writes are now instrumented, but historical rows still need backfill before the replay page can be treated as complete.

## Can UI Work Start?

No. The UI should stay blocked until the backfill step closes the historical gaps and the readiness gate moves forward.

## Remaining Blockers Before UI

1. Historical registry rows still miss replay metadata.
2. `actual_result` still depends on downstream outcome joining.
3. The replay store is still not complete enough for MVP UI release.

## Next Worker Prompt

Implement the smallest safe historical backfill pass for replay metadata, then rerun the readiness diagnostic to confirm whether the gate can move beyond `BACKFILL_REQUIRED`.

P7_STRATEGY_REPLAY_PREDICTION_WRITE_PATH_INSTRUMENTATION_READY