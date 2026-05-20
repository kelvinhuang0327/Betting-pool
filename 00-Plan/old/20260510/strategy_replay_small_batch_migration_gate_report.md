# Strategy Replay Small-Batch Migration Gate Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only small-batch migration gate implemented; no migration executed

## What Was Implemented

- A pure small-batch migration gate helper at [wbc_backend/reporting/strategy_replay_migration_gate.py](wbc_backend/reporting/strategy_replay_migration_gate.py) that evaluates approval validity, write-plan readiness, fixture apply results, rollback planning, human approval, and UI gating.
- A read-only checklist CLI at [scripts/build_strategy_replay_migration_gate_checklist.py](scripts/build_strategy_replay_migration_gate_checklist.py) that prints `READ_ONLY_MIGRATION_GATE_CHECKLIST` and writes only to an explicit output path when provided.
- Fixture-based regression coverage at [tests/test_strategy_replay_migration_gate.py](tests/test_strategy_replay_migration_gate.py) covering default denial, approval gating, skipped-count blocking, unresolved P0 blocking, rollback-plan blocking, UI blocking, CLI marker output, and no-production-access checks.

## What Was Not Implemented

- No production DB writes.
- No actual migration execution.
- No historical registry file mutation in place.
- No frontend implementation.
- No CI changes.
- No branch protection changes.
- No replay-default-validation changes.
- No betting recommendation logic changes.

## Files Changed

- [wbc_backend/reporting/strategy_replay_migration_gate.py](wbc_backend/reporting/strategy_replay_migration_gate.py)
- [scripts/build_strategy_replay_migration_gate_checklist.py](scripts/build_strategy_replay_migration_gate_checklist.py)
- [tests/test_strategy_replay_migration_gate.py](tests/test_strategy_replay_migration_gate.py)
- [00-BettingPlan/20260510/strategy_replay_small_batch_migration_gate_report.md](00-BettingPlan/20260510/strategy_replay_small_batch_migration_gate_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py tests/test_strategy_replay_backfill_write_plan.py tests/test_strategy_replay_backfill_apply_fixture.py tests/test_strategy_replay_migration_gate.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: the gate defaults to `migration_allowed = false`.
- PASS: valid manifest + write plan + fixture apply still do not allow migration without explicit human approval.
- PASS: explicit human approval can allow the small-batch gate when all checks pass.
- PASS: skipped planned items block the gate.
- PASS: unresolved P0 unsafe fields block the gate.
- PASS: a missing rollback plan blocks the gate.
- PASS: UI remains blocked while readiness is `BACKFILL_REQUIRED`.
- PASS: the checklist CLI prints `READ_ONLY_MIGRATION_GATE_CHECKLIST`.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: actual migration execution is not allowed because this is a read-only gate only.

## Is Actual Migration Allowed?

No.

This gate only defines the approval and verification rules for a future small-batch migration. It does not authorize execution by itself, and no migration was run.

## Can UI Work Start?

No.

The current readiness state still reports `BACKFILL_REQUIRED`, so UI must remain blocked until post-migration diagnostics reach `UI_MVP_READY`.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. Post-migration diagnostics have not advanced readiness to `UI_MVP_READY`.

## Next Worker Prompt

Use the migration gate checklist to approve only a tightly scoped batch after all read-only checks pass, then keep UI work blocked until the post-migration readiness diagnostic explicitly reaches `UI_MVP_READY`.

P12_STRATEGY_REPLAY_SMALL_BATCH_MIGRATION_GATE_READY