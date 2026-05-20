# Strategy Replay Fixture-Only Backfill Apply Report

Date: 2026-05-10
Repo: Betting-pool
Status: Fixture-only apply flow implemented; no real historical data mutated

## What Was Implemented

- A pure fixture-only apply helper at [wbc_backend/reporting/strategy_replay_backfill_apply.py](wbc_backend/reporting/strategy_replay_backfill_apply.py) that loads fixture rows, applies approved write-plan fields in memory, and preserves unknown fields.
- A fixture-only CLI at [scripts/apply_strategy_replay_backfill_write_plan_fixture.py](scripts/apply_strategy_replay_backfill_write_plan_fixture.py) that prints `FIXTURE_ONLY_BACKFILL_APPLY`, accepts explicit input / write-plan / output paths, and refuses to run when input and output paths are the same.
- Fixture-backed regression coverage at [tests/test_strategy_replay_backfill_apply_fixture.py](tests/test_strategy_replay_backfill_apply_fixture.py) covering:
  - approved patches apply to matching fixture rows
  - unapproved fields are not patched
  - unknown fields are preserved
  - unmatched source refs are skipped
  - input rows are not mutated
  - CLI marker output and explicit output path writes
  - same-path refusal
  - no production DB access

## What Was Not Implemented

- No production DB writes.
- No actual migration execution.
- No historical registry file mutation in place.
- No schema migration.
- No frontend UI.
- No CI or branch protection changes.
- No betting model or recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_backfill_apply.py](wbc_backend/reporting/strategy_replay_backfill_apply.py)
- [scripts/apply_strategy_replay_backfill_write_plan_fixture.py](scripts/apply_strategy_replay_backfill_write_plan_fixture.py)
- [tests/test_strategy_replay_backfill_apply_fixture.py](tests/test_strategy_replay_backfill_apply_fixture.py)
- [00-BettingPlan/20260510/strategy_replay_fixture_backfill_apply_report.md](00-BettingPlan/20260510/strategy_replay_fixture_backfill_apply_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py tests/test_strategy_replay_backfill_apply_fixture.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: approved patches apply to matching fixture rows in memory.
- PASS: unapproved fields remain unchanged.
- PASS: unknown fields are preserved.
- PASS: unmatched source refs are skipped rather than failing the run.
- PASS: the CLI prints `FIXTURE_ONLY_BACKFILL_APPLY` and writes only to the explicit output path.
- PASS: same-path input/output is refused.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: actual migration execution is not allowed because this is a fixture-only simulation.

## Is Actual Migration Allowed?

No.

This step only proves apply semantics against temporary fixture files. It does not authorize or execute any production migration.

## Can UI Work Start?

No. UI work should remain blocked until the historical gaps are resolved and the readiness gate moves beyond `BACKFILL_REQUIRED`.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. No actual production migration has been executed.

## Next Worker Prompt

Use the fixture-only apply output to verify the final shape of an approved migration batch, then keep production migration blocked until a separate explicit execution step is approved.

P11_STRATEGY_REPLAY_FIXTURE_BACKFILL_APPLY_READY# Strategy Replay Fixture-Only Backfill Apply Report

Date: 2026-05-10
Repo: Betting-pool
Status: Fixture-only apply flow implemented; no real historical data mutated

## What Was Implemented

- A pure fixture-only apply helper at [wbc_backend/reporting/strategy_replay_backfill_apply.py](wbc_backend/reporting/strategy_replay_backfill_apply.py) that loads rows, applies approved write-plan fields in memory, and preserves unknown fields.
- A fixture-only CLI at [scripts/apply_strategy_replay_backfill_write_plan_fixture.py](scripts/apply_strategy_replay_backfill_write_plan_fixture.py) that prints `FIXTURE_ONLY_BACKFILL_APPLY`, accepts explicit input / write-plan / output paths, and refuses to run when input and output paths are the same.
- Fixture-backed regression coverage at [tests/test_strategy_replay_backfill_apply_fixture.py](tests/test_strategy_replay_backfill_apply_fixture.py) covering:
  - approved patches apply to matching fixture rows
  - unapproved fields are not patched
  - unknown fields are preserved
  - unmatched source refs are skipped
  - input rows are not mutated
  - CLI marker output and explicit output path writes
  - same-path refusal
  - no production DB access

## What Was Not Implemented

- No production DB writes.
- No actual migration execution.
- No historical registry file mutation in place.
- No schema migration.
- No frontend UI.
- No CI or branch protection changes.
- No betting model or recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_backfill_apply.py](wbc_backend/reporting/strategy_replay_backfill_apply.py)
- [scripts/apply_strategy_replay_backfill_write_plan_fixture.py](scripts/apply_strategy_replay_backfill_write_plan_fixture.py)
- [tests/test_strategy_replay_backfill_apply_fixture.py](tests/test_strategy_replay_backfill_apply_fixture.py)
- [00-BettingPlan/20260510/strategy_replay_fixture_backfill_apply_report.md](00-BettingPlan/20260510/strategy_replay_fixture_backfill_apply_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py tests/test_strategy_replay_backfill_apply_fixture.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: approved patches apply to matching fixture rows in memory.
- PASS: unapproved fields remain unchanged.
- PASS: unknown fields are preserved.
- PASS: unmatched source refs are skipped rather than failing the run.
- PASS: the CLI prints `FIXTURE_ONLY_BACKFILL_APPLY` and writes only to the explicit output path.
- PASS: same-path input/output is refused.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: actual migration execution is not allowed because this is a fixture-only simulation.

## Is Actual Migration Allowed?

No.

This step only proves apply semantics against temporary fixture files. It does not authorize or execute any production migration.

## Can UI Work Start?

No. UI work should remain blocked until the historical gaps are resolved and the readiness gate moves beyond `BACKFILL_REQUIRED`.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. No actual production migration has been executed.

## Next Worker Prompt

Use the fixture-only apply output to verify the final shape of an approved migration batch, then keep production migration blocked until a separate explicit execution step is approved.

P11_STRATEGY_REPLAY_FIXTURE_BACKFILL_APPLY_READY