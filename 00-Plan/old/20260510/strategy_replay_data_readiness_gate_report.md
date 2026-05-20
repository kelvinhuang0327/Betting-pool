# Strategy Replay Data Readiness Gate Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only readiness gate implemented, no production DB writes

## What Was Implemented

- A read-only readiness classifier at [wbc_backend/reporting/strategy_replay_readiness.py](wbc_backend/reporting/strategy_replay_readiness.py) with the requested readiness levels, blocker identification, and gap closure planning helpers.
- A dry-run readiness diagnostics script at [scripts/check_strategy_replay_readiness.py](scripts/check_strategy_replay_readiness.py) that prints `READ_ONLY_DIAGNOSTIC` and summary counts without writing anything.
- Fixture-based readiness tests at [tests/test_strategy_replay_readiness.py](tests/test_strategy_replay_readiness.py) covering zero rows, complete rows, missing field classifications, diagnostics output, and no DB access.

## What Was Not Implemented

- No frontend page.
- No production DB schema migration.
- No production DB writes.
- No CI / branch protection changes.
- No strategy mining.
- No bankroll optimization.
- No betting recommendation changes.
- No production readiness claim.

## Files Changed

- [wbc_backend/reporting/strategy_replay_readiness.py](wbc_backend/reporting/strategy_replay_readiness.py)
- [scripts/check_strategy_replay_readiness.py](scripts/check_strategy_replay_readiness.py)
- [tests/test_strategy_replay_readiness.py](tests/test_strategy_replay_readiness.py)
- [00-BettingPlan/20260510/strategy_replay_data_readiness_gate_report.md](00-BettingPlan/20260510/strategy_replay_data_readiness_gate_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: readiness tests returned 59 passed across the replay skeleton and readiness slices.
- PASS: diagnostics script prints `READ_ONLY_DIAGNOSTIC` and readiness details.
- PASS: no production DB access was added.
- FAIL: the UI cannot start yet, because the current data is still missing canonical production replay completeness.

## Current Readiness Level

`BACKFILL_REQUIRED`

This is the correct gate state for Betting-pool today because the current row contract can be classified, but the production replay store is still missing required historical completeness and canonical join stability.

## Can UI Work Start?

No. UI work should wait until the readiness gate moves to `UI_MVP_READY`.

## Blocker List

1. `strategy_id` is not guaranteed in historical production replay rows.
2. `lifecycle_state_at_prediction_time` is not fully instrumented across the real replay history.
3. `canonical_outcome_key` still needs stabilization for all supported rows, including fallback cases.
4. `actual_result` still depends on adapter-level joining instead of a canonical production replay store.
5. The existing API is still a skeleton and should not be treated as production-ready.

## Minimum Gap Closure Plan

1. Persist `strategy_id` on every replayable prediction record.
2. Persist `lifecycle_state_at_prediction_time` at prediction write time.
3. Normalize and persist a stable `canonical_outcome_key` for replay joins.
4. Backfill `actual_result` from the canonical postgame outcomes store.
5. Re-run the read-only diagnostics until the readiness gate reaches `UI_MVP_READY`.
6. Only then wire the UI to the validated read-only API contract.

## Next Worker Agent Prompt

Implement the minimum production replay store instrumentation or historical backfill process needed to eliminate the remaining missing-field blockers, then rerun the readiness diagnostic before attempting any UI work.

P5_STRATEGY_REPLAY_DATA_READINESS_GATE_READY
# Strategy Replay Data Readiness Gate Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only readiness gate implemented, no production DB writes

## What Was Implemented

- A read-only readiness classifier at [wbc_backend/reporting/strategy_replay_readiness.py](wbc_backend/reporting/strategy_replay_readiness.py) with the requested readiness levels, blocker identification, and gap closure planning helpers.
- A dry-run readiness diagnostics script at [scripts/check_strategy_replay_readiness.py](scripts/check_strategy_replay_readiness.py) that prints `READ_ONLY_DIAGNOSTIC` and summary counts without writing anything.
- Fixture-based readiness tests at [tests/test_strategy_replay_readiness.py](tests/test_strategy_replay_readiness.py) covering zero rows, complete rows, missing field classifications, diagnostics output, and no DB access.

## What Was Not Implemented

- No frontend page.
- No production DB schema migration.
- No production DB writes.
- No CI / branch protection changes.
- No strategy mining.
- No bankroll optimization.
- No betting recommendation changes.
- No production readiness claim.

## Files Changed

- [wbc_backend/reporting/strategy_replay_readiness.py](wbc_backend/reporting/strategy_replay_readiness.py)
- [scripts/check_strategy_replay_readiness.py](scripts/check_strategy_replay_readiness.py)
- [tests/test_strategy_replay_readiness.py](tests/test_strategy_replay_readiness.py)
- [00-BettingPlan/20260510/strategy_replay_data_readiness_gate_report.md](00-BettingPlan/20260510/strategy_replay_data_readiness_gate_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: readiness tests returned 54 passed across the replay skeleton and readiness slices.
- PASS: diagnostics script prints `READ_ONLY_DIAGNOSTIC` and readiness details.
- PASS: no production DB access was added.
- FAIL: the UI cannot start yet, because the current data is still missing canonical production replay completeness.

## Current Readiness Level

BACKFILL_REQUIRED

This is the correct gate state for Betting-pool today because the current row contract can be classified, but the production replay store is still missing required historical completeness.

## Can UI Work Start?

No. UI work should wait until the readiness gate moves to `UI_MVP_READY`.

## Blocker List

1. `strategy_id` is not guaranteed in historical production replay rows.
2. `lifecycle_state_at_prediction_time` is not fully instrumented across the real replay history.
3. `canonical_outcome_key` still needs stabilization for all supported rows.
4. `actual_result` still depends on adapter-level joining instead of a canonical production replay store.
5. The existing API is still a skeleton and should not be treated as production-ready.

## Minimum Gap Closure Plan

1. Persist `strategy_id` on every replayable prediction record.
2. Persist `lifecycle_state_at_prediction_time` at prediction write time.
3. Normalize and persist a stable `canonical_outcome_key` for replay joins.
4. Backfill `actual_result` from the canonical postgame outcomes store.
5. Re-run the read-only diagnostics until the readiness gate reaches `UI_MVP_READY`.
6. Only then wire the UI to the validated read-only API contract.

## Next Worker Agent Prompt

Implement the minimum production replay store instrumentation or historical backfill process needed to eliminate the remaining missing-field blockers, then rerun the readiness diagnostic before attempting any UI work.

P5_STRATEGY_REPLAY_DATA_READINESS_GATE_READY
