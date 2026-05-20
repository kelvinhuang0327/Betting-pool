# Strategy Replay Post-Staging Readiness Recheck Report

Date: 2026-05-10
Repo: Betting-pool
Status: Post-staging readiness recheck gate implemented; no UI shipped

## What Was Implemented

- A pure post-staging readiness helper at [wbc_backend/reporting/strategy_replay_post_staging_readiness.py](wbc_backend/reporting/strategy_replay_post_staging_readiness.py) that combines staged rows with a staging result summary and decides whether UI MVP work can start.
- A read-only recheck CLI at [scripts/check_strategy_replay_post_staging_readiness.py](scripts/check_strategy_replay_post_staging_readiness.py) that prints `POST_STAGING_READINESS_RECHECK`, accepts staging output plus an optional staging result, and writes only to an explicit output path when provided.
- Fixture-based regression coverage at [tests/test_strategy_replay_post_staging_readiness.py](tests/test_strategy_replay_post_staging_readiness.py) covering backfill-blocked UI, UI_MVP_READY unlock into frontend spec/mock-data mode, production-write blocking, zero-applied-count blocking, missing-P0 blocking, CLI marker output, no-production-access, and no-write-default behavior.

## What Was Not Implemented

- No frontend implementation.
- No production UI.
- No production DB writes.
- No actual production migration execution.
- No mutation of real historical registry files in place.
- No CI changes.
- No branch protection changes.
- No replay-default-validation changes.
- No betting recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_post_staging_readiness.py](wbc_backend/reporting/strategy_replay_post_staging_readiness.py)
- [scripts/check_strategy_replay_post_staging_readiness.py](scripts/check_strategy_replay_post_staging_readiness.py)
- [tests/test_strategy_replay_post_staging_readiness.py](tests/test_strategy_replay_post_staging_readiness.py)
- [00-BettingPlan/20260510/strategy_replay_post_staging_readiness_report.md](00-BettingPlan/20260510/strategy_replay_post_staging_readiness_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py tests/test_strategy_replay_backfill_apply_fixture.py tests/test_strategy_replay_migration_gate.py tests/test_strategy_replay_staging_migration_runner.py tests/test_strategy_replay_post_staging_readiness.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: BACKFILL_REQUIRED keeps UI blocked.
- PASS: UI_MVP_READY with a valid staging result unlocks frontend spec/mock-data mode.
- PASS: production_write_allowed true blocks UI unlock.
- PASS: applied_count = 0 blocks UI unlock.
- PASS: missing P0 fields block UI unlock.
- PASS: the CLI prints `POST_STAGING_READINESS_RECHECK`.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: production UI is not allowed because post-staging unlock only enables frontend spec/mock-data mode, not production.

## Is UI Allowed To Start?

Only in frontend spec / mock-data mode when the staged rows are complete, the staging result is valid, source_mode remains `READ_ONLY`, and the readiness level reaches `UI_MVP_READY`.

Current repository readiness still reports `BACKFILL_REQUIRED`, so UI remains blocked right now.

## Allowed UI Mode

- `FRONTEND_SPEC_MOCK_DATA`

## Remaining Blockers Before Production UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. Post-staging checks have not yet reached a production UI release state.

## Next Worker Prompt

Use the post-staging recheck only after staging output is available, and keep production UI blocked until a separate explicit production-ready authorization step is approved.

P14_STRATEGY_REPLAY_POST_STAGING_READINESS_RECHECK_READY