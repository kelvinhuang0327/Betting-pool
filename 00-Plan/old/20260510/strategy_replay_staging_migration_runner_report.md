# Strategy Replay Staging-Only Migration Runner Report

Date: 2026-05-10
Repo: Betting-pool
Status: Staging-only / fixture-only runner skeleton implemented; no migration executed

## What Was Implemented

- A pure staging-only runner helper at [wbc_backend/reporting/strategy_replay_staging_migration_runner.py](wbc_backend/reporting/strategy_replay_staging_migration_runner.py) that validates P12 gate state, refuses production mode, refuses missing human approval or rollback plan, preserves input rows, and returns a staging-only result summary.
- A staging-only CLI at [scripts/run_strategy_replay_staging_migration.py](scripts/run_strategy_replay_staging_migration.py) that prints `STAGING_ONLY_MIGRATION_RUNNER`, requires explicit paths, refuses same input/output paths, and writes only to the explicit output path.
- Fixture-based regression coverage at [tests/test_strategy_replay_staging_migration_runner.py](tests/test_strategy_replay_staging_migration_runner.py) covering gate blocking, human approval blocking, rollback blocking, production-mode refusal, STAGING/FIXTURE success, input immutability, CLI marker output, same-path refusal, and no-production-access checks.

## What Was Not Implemented

- No production DB writes.
- No actual production migration execution.
- No mutation of real historical registry files in place.
- No frontend implementation.
- No CI changes.
- No branch protection changes.
- No replay-default-validation changes.
- No betting recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_migration_gate.py](wbc_backend/reporting/strategy_replay_migration_gate.py)
- [wbc_backend/reporting/strategy_replay_staging_migration_runner.py](wbc_backend/reporting/strategy_replay_staging_migration_runner.py)
- [scripts/run_strategy_replay_staging_migration.py](scripts/run_strategy_replay_staging_migration.py)
- [tests/test_strategy_replay_staging_migration_runner.py](tests/test_strategy_replay_staging_migration_runner.py)
- [00-BettingPlan/20260510/strategy_replay_staging_migration_runner_report.md](00-BettingPlan/20260510/strategy_replay_staging_migration_runner_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py tests/test_strategy_replay_backfill_apply_fixture.py tests/test_strategy_replay_migration_gate.py tests/test_strategy_replay_staging_migration_runner.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: the runner defaults to staging-only and refuses production mode.
- PASS: the runner refuses to run unless the P12 gate passes, human approval is true, and a rollback plan exists.
- PASS: STAGING and FIXTURE modes can run when the gate passes.
- PASS: input rows are not mutated.
- PASS: the CLI prints `STAGING_ONLY_MIGRATION_RUNNER`.
- PASS: the CLI refuses same input/output paths.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: actual production migration execution is not allowed because this is only a staging skeleton.

## Is Actual Migration Allowed?

No.

This runner only simulates staging or fixture execution behind the P12 gate. It does not authorize or execute production migration.

## Can UI Work Start?

No.

The readiness state still reports `BACKFILL_REQUIRED`, so UI remains blocked until post-migration diagnostics reach `UI_MVP_READY`.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. Post-migration diagnostics have not advanced readiness to `UI_MVP_READY`.

## Next Worker Prompt

Use the staging-only runner only after the P12 gate passes, and keep production execution blocked until a separate explicit migration authorization step is approved.

P13_STRATEGY_REPLAY_STAGING_MIGRATION_RUNNER_READY