# Strategy Replay Backfill and Instrumentation Skeleton Report

Date: 2026-05-10
Repo: Betting-pool
Status: Skeleton implementation only, no production DB writes

## What Was Implemented

- A pure normalization module at [wbc_backend/reporting/strategy_replay_history.py](wbc_backend/reporting/strategy_replay_history.py) for replay row construction, lifecycle normalization, settlement derivation, data-quality flagging, and structural validation.
- A fixture-based contract test file at [tests/test_strategy_replay_history_contract.py](tests/test_strategy_replay_history_contract.py) covering win/loss/push, missing strategy_id, missing lifecycle state at prediction time, missing actual outcome, unstable outcome join key, known lifecycle states, unknown lifecycle normalization, and no production DB access.
- A dry-run backfill preview CLI at [scripts/preview_strategy_replay_backfill.py](scripts/preview_strategy_replay_backfill.py) that prints `DRY_RUN_ONLY` and summary counts without writing anything.

## What Was Not Implemented

- No frontend page.
- No DB schema migration.
- No production DB writes.
- No CI / branch protection change.
- No betting recommendation logic change.
- No strategy mining.
- No bankroll optimization.
- No production replay execution.

## Files Changed

- [wbc_backend/reporting/strategy_replay_history.py](wbc_backend/reporting/strategy_replay_history.py)
- [tests/test_strategy_replay_history_contract.py](tests/test_strategy_replay_history_contract.py)
- [scripts/preview_strategy_replay_backfill.py](scripts/preview_strategy_replay_backfill.py)
- [00-BettingPlan/20260510/strategy_replay_backfill_instrumentation_skeleton_report.md](00-BettingPlan/20260510/strategy_replay_backfill_instrumentation_skeleton_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py -q`

## PASS / FAIL

- PASS: `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py -q` returned 29 passed.
- PASS: dry-run preview is non-writing and emits `DRY_RUN_ONLY`.
- FAIL: the user-facing MVP UI cannot start yet, because the contract skeleton does not backfill historical production data and the canonical replay store is still missing.

## Can MVP UI Start Now?

No. The contract skeleton is ready for the next worker slice, but the user-facing UI still needs backfill and instrumentation integration before it can show complete historical strategy replay rows.

## Remaining Blockers Before UI

1. Canonical per-strategy history is still not persisted in production.
2. Historical lifecycle state at prediction time still needs upstream instrumentation or backfill alignment.
3. The actual outcome join key still needs stabilization across historical data.
4. The UI should not be built until the contract rows are testable against real backfilled records.

## Next Worker Agent Prompt

Implement the next safe slice: wire the replay contract into a read-only backfill adapter that can consume existing registry and postgame rows, emit canonical replay rows, and validate join completeness without writing to production storage.

P2_STRATEGY_REPLAY_BACKFILL_INSTRUMENTATION_SKELETON_READY
