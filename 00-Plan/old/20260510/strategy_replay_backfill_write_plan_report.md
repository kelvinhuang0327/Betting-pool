# Strategy Replay Approved Backfill Write-Plan Report

Date: 2026-05-10
Repo: Betting-pool
Status: Dry-run approved write-plan flow implemented; no migration executed

## What Was Implemented

- A pure approved write-plan helper at [wbc_backend/reporting/strategy_replay_backfill_write_plan.py](wbc_backend/reporting/strategy_replay_backfill_write_plan.py) that only accepts `WRITE_READY` candidates from the review workflow.
- A dry-run CLI at [scripts/build_strategy_replay_backfill_write_plan.py](scripts/build_strategy_replay_backfill_write_plan.py) that prints `DRY_RUN_BACKFILL_WRITE_PLAN`, accepts explicit candidates / approval manifest / output paths, and writes only to the requested output file.
- Fixture-based regression coverage at [tests/test_strategy_replay_backfill_write_plan.py](tests/test_strategy_replay_backfill_write_plan.py) covering:
  - unapproved candidates are rejected
  - approved P1 fallback candidates enter the write plan
  - P0 unsafe candidates without approved values are rejected
  - unknown candidate IDs are rejected
  - plan rows are dry-run only
  - CLI output is read-only and written only to the explicit output path
  - input candidates are not mutated
  - no production DB access

## What Was Not Implemented

- No production migration execution.
- No production DB writes.
- No historical file mutation in place.
- No schema migration.
- No frontend UI.
- No CI or branch protection changes.
- No betting model or recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_backfill_write_plan.py](wbc_backend/reporting/strategy_replay_backfill_write_plan.py)
- [scripts/build_strategy_replay_backfill_write_plan.py](scripts/build_strategy_replay_backfill_write_plan.py)
- [tests/test_strategy_replay_backfill_write_plan.py](tests/test_strategy_replay_backfill_write_plan.py)
- [00-BettingPlan/20260510/strategy_replay_backfill_write_plan_report.md](00-BettingPlan/20260510/strategy_replay_backfill_write_plan_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: the write-plan CLI prints `DRY_RUN_BACKFILL_WRITE_PLAN` and writes only to the explicit output path.
- PASS: only review-approved candidates enter the plan.
- PASS: unapproved and unsafe candidates are excluded.
- PASS: P1 fallback candidates can be included when explicitly approved.
- PASS: the plan is marked dry-run only.
- PASS: input candidates remain unchanged.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: production migration execution is not allowed yet because this is only a dry-run write-plan generator.

## Is Migration Execution Allowed?

No.

This workflow only prepares a dry-run write plan for approved candidates. Actual migration execution remains blocked by design and by the still-incomplete historical readiness state.

## Can UI Work Start?

No. UI work should remain blocked until the historical gaps are resolved and the readiness gate moves beyond `BACKFILL_REQUIRED`.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. No actual migration execution has been approved or run.

## Next Worker Prompt

Use the dry-run write plan output as the input to a manual migration review step, then keep migration execution blocked until the final historical write strategy is explicitly approved.

P10_STRATEGY_REPLAY_BACKFILL_WRITE_PLAN_READY# Strategy Replay Approved Backfill Write-Plan Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only approved write-plan flow implemented; no migration executed

## What Was Implemented

- A pure approved write-plan helper at [wbc_backend/reporting/strategy_replay_backfill_write_plan.py](wbc_backend/reporting/strategy_replay_backfill_write_plan.py) that only turns review-approved candidates into dry-run plan items.
- A dry-run CLI at [scripts/build_strategy_replay_backfill_write_plan.py](scripts/build_strategy_replay_backfill_write_plan.py) that prints `DRY_RUN_BACKFILL_WRITE_PLAN`, accepts explicit candidates / approval manifest / output paths, and writes only to the requested output file.
- A fixture-backed regression suite at [tests/test_strategy_replay_backfill_write_plan.py](tests/test_strategy_replay_backfill_write_plan.py) covering:
  - unapproved candidates are rejected
  - approved P1 fallback candidates enter the write plan
  - P0 unsafe candidates without approved values are rejected
  - unknown candidate IDs are rejected
  - write plan rows are dry-run only
  - CLI output is read-only and written only to the explicit output path
  - input candidates are not mutated
  - no production DB access

## What Was Not Implemented

- No production migration execution.
- No production DB writes.
- No historical file mutation in place.
- No schema migration.
- No frontend UI.
- No CI or branch protection changes.
- No betting model or recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_backfill_write_plan.py](wbc_backend/reporting/strategy_replay_backfill_write_plan.py)
- [scripts/build_strategy_replay_backfill_write_plan.py](scripts/build_strategy_replay_backfill_write_plan.py)
- [tests/test_strategy_replay_backfill_write_plan.py](tests/test_strategy_replay_backfill_write_plan.py)
- [00-BettingPlan/20260510/strategy_replay_backfill_write_plan_report.md](00-BettingPlan/20260510/strategy_replay_backfill_write_plan_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: the write-plan CLI prints `DRY_RUN_BACKFILL_WRITE_PLAN` and writes only to the explicit output path.
- PASS: only review-approved candidates enter the plan.
- PASS: unapproved and unsafe candidates are excluded.
- PASS: P1 fallback candidates can be included when explicitly approved.
- PASS: the plan is marked dry-run only.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: production migration execution is not allowed yet because this is only a dry-run write-plan generator.

## Is Migration Execution Allowed?

No.

This workflow only prepares the dry-run write plan for approved candidates. Actual migration execution remains blocked by design and by the still-incomplete historical readiness state.

## Can UI Work Start?

No. UI work should remain blocked until the historical gaps are resolved and the readiness gate moves beyond `BACKFILL_REQUIRED`.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. No actual migration execution has been approved or run.

## Next Worker Prompt

Use the dry-run write plan output as the input to a manual migration review step, then keep migration execution blocked until the final historical write strategy is explicitly approved.

P10_STRATEGY_REPLAY_BACKFILL_WRITE_PLAN_READY