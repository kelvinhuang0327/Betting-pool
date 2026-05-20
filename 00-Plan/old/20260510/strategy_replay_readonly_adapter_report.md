# Strategy Replay Read-Only Adapter Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only adapter implemented, no production DB writes

## What Was Implemented

- A read-only adapter module at [wbc_backend/reporting/strategy_replay_adapter.py](wbc_backend/reporting/strategy_replay_adapter.py) with pure helpers to load JSONL entries, build outcome lookups, adapt prediction rows to the replay contract, build replay rows, and summarize row readiness.
- An updated dry-run preview CLI at [scripts/preview_strategy_replay_backfill.py](scripts/preview_strategy_replay_backfill.py) that accepts explicit `--prediction-registry` and `--postgame-outcomes` paths, still prints `DRY_RUN_ONLY`, and stays non-writing.
- Fixture-based adapter tests at [tests/test_strategy_replay_adapter.py](tests/test_strategy_replay_adapter.py) covering JSONL loading, canonical outcome joins, missing outcome flags, missing strategy_id preservation, missing lifecycle flags, and no DB access.

## What Was Not Implemented

- No frontend page.
- No production DB schema migration.
- No production DB writes.
- No strategy mining.
- No betting recommendation changes.
- No bankroll optimization changes.
- No CI / branch protection changes.
- No replay-default-validation changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_adapter.py](wbc_backend/reporting/strategy_replay_adapter.py)
- [scripts/preview_strategy_replay_backfill.py](scripts/preview_strategy_replay_backfill.py)
- [tests/test_strategy_replay_history_contract.py](tests/test_strategy_replay_history_contract.py)
- [tests/test_strategy_replay_adapter.py](tests/test_strategy_replay_adapter.py)
- [00-BettingPlan/20260510/strategy_replay_readonly_adapter_report.md](00-BettingPlan/20260510/strategy_replay_readonly_adapter_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py -q`
- `./.venv/bin/python scripts/preview_strategy_replay_backfill.py`

## PASS / FAIL

- PASS: targeted contract and adapter tests returned 38 passed.
- PASS: dry-run preview CLI prints `DRY_RUN_ONLY` and summary counts.
- PASS: no production DB access is introduced by the adapter path.
- FAIL: the user-facing Strategy Historical Replay UI still cannot start, because the adapter is read-only and the canonical production replay store is not yet wired.

## Can API Endpoint Work Start?

Yes. The read-only adapter is now sufficient for the next worker slice to start wiring a read-only API endpoint or service layer around the replay contract.

## Can UI Work Start?

Not yet. The UI should wait until the API endpoint is wired to real replay rows backed by the read-only adapter and validated against production data samples.

## Remaining Blockers Before UI

1. Canonical per-strategy history is still not fully persisted in production.
2. lifecycle_state_at_prediction_time still needs upstream persistence or backfilled inference for historical rows.
3. The actual outcome join key still needs broader validation against real historical rows.
4. The adapter currently normalizes and flags missing data, but it does not solve the upstream storage gap.

## Next Worker Agent Prompt

Implement a read-only API service layer that consumes the adapter output, applies pagination/sort/filter parameters, and returns the strategy replay rows without touching production DB state.

P3_STRATEGY_REPLAY_READONLY_ADAPTER_READY
