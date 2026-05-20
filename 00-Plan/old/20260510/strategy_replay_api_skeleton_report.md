# Strategy Replay Read-Only API Skeleton Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only API/service skeleton implemented, no production DB writes

## What Was Implemented

- A read-only service/query skeleton at [wbc_backend/reporting/strategy_replay_service.py](wbc_backend/reporting/strategy_replay_service.py) with pure helpers for query parsing, filtering, sorting, pagination, response assembly, and read-only row loading from file paths.
- A minimal FastAPI GET route at [orchestrator/api.py](orchestrator/api.py) for `/api/strategy-replay/history` that delegates to the service skeleton and returns read-only replay payloads.
- Fixture-based service tests at [tests/test_strategy_replay_service.py](tests/test_strategy_replay_service.py) covering default query parsing, filters, sorting, pagination, response metadata, invalid parameter handling, and a route-function smoke test.

## Was the Actual Endpoint Added?

Yes. A minimal read-only endpoint skeleton was added on the existing FastAPI router. It is intentionally thin and delegates all logic to the service module.

## What Was Not Implemented

- No frontend page.
- No production DB schema migration.
- No production DB writes.
- No betting recommendation changes.
- No bankroll optimization changes.
- No strategy mining.
- No CI / branch protection changes.
- No replay-default-validation changes.
- No production-hardened persistence layer.

## Files Changed

- [wbc_backend/reporting/strategy_replay_service.py](wbc_backend/reporting/strategy_replay_service.py)
- [orchestrator/api.py](orchestrator/api.py)
- [tests/test_strategy_replay_service.py](tests/test_strategy_replay_service.py)
- [00-BettingPlan/20260510/strategy_replay_api_skeleton_report.md](00-BettingPlan/20260510/strategy_replay_api_skeleton_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py -q`
- The service test suite includes a direct smoke test of the route function, avoiding missing optional test-client dependencies.

## PASS / FAIL

- PASS: replay contract, adapter, and service tests returned 49 passed.
- PASS: response payload exposes `source_mode = READ_ONLY`.
- PASS: response payload exposes `ui_ready = false`.
- PASS: the route exists and is wired through the existing FastAPI router.
- FAIL: the user-facing UI should still wait, because the API skeleton is read-only and the canonical production replay store is not yet complete.

## Can UI Work Start?

Not yet. The UI should wait until real backfilled replay data is wired through the service layer and validated against representative production samples.

## Remaining Blockers Before UI

1. Canonical per-strategy history is still not fully persisted in production.
2. lifecycle_state_at_prediction_time may still be missing in real historical rows.
3. The actual outcome join key still needs broader validation across production data samples.
4. The endpoint is a skeleton; it is read-only and not yet backed by a production-hardened replay store.

## Next Worker Agent Prompt

Implement a read-only data source integration layer or repository adapter that can feed the `/api/strategy-replay/history` endpoint with real backfilled replay rows while keeping UI and write paths out of scope.

P4_STRATEGY_REPLAY_READONLY_API_SKELETON_READY
