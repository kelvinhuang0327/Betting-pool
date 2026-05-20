# Strategy Replay End-to-End Gate Map

Date: 2026-05-10
Repo: Betting-pool
Scope: Betting-pool only
Status: Consolidated handoff document for Strategy Replay P0–P14

## Executive Summary

Current readiness level: `BACKFILL_REQUIRED`.

UI can start now: no. The post-staging gate exists, but repository readiness still fails the completeness gate, so UI remains blocked.

Production migration can start now: no. The small-batch gate, staging runner, and post-staging recheck all remain read-only / staging-only, and production execution is still explicitly blocked.

production migration blocked: yes.

Allowed mode now: read-only diagnostics and staging/fixture-only simulation. If and only if a future post-staging gate passes, the only UI mode that may be considered is `FRONTEND_SPEC_MOCK_DATA`.

## P0–P14 Completion Matrix

| Phase | Phase Name | Implemented Files | Tests Added | Validation Result | Marker | Current Limitation |
|---|---|---|---|---|---|---|
| P0 | Page discovery and contract | [strategy_replay_page_discovery_and_contract.md](strategy_replay_page_discovery_and_contract.md), [strategy_replay_mvp_contract.md](strategy_replay_mvp_contract.md) | Discovery / contract planning only | Discovery showed the page contract could not be fully satisfied from current data alone | none | No canonical per-strategy history store; current data is game-level, not strategy-level |
| P1 | Backfill instrumentation skeleton | [wbc_backend/reporting/strategy_replay_history.py](../../wbc_backend/reporting/strategy_replay_history.py), [tests/test_strategy_replay_history_contract.py](../../tests/test_strategy_replay_history_contract.py), [scripts/preview_strategy_replay_backfill.py](../../scripts/preview_strategy_replay_backfill.py) | Contract tests for win/loss/push, missing fields, join stability, and no DB access | `29 passed` in the skeleton slice | `DRY_RUN_ONLY` | Historical replay still incomplete; no production backfill |
| P2 | Read-only adapter | [wbc_backend/reporting/strategy_replay_adapter.py](../../wbc_backend/reporting/strategy_replay_adapter.py), [tests/test_strategy_replay_adapter.py](../../tests/test_strategy_replay_adapter.py), [scripts/preview_strategy_replay_backfill.py](../../scripts/preview_strategy_replay_backfill.py) | Adapter coverage for JSONL loading, canonical joins, missing flags, and no DB access | `38 passed` | `DRY_RUN_ONLY` | Read-only adapter does not solve upstream storage gaps |
| P3 | Read-only API skeleton | [wbc_backend/reporting/strategy_replay_service.py](../../wbc_backend/reporting/strategy_replay_service.py), [orchestrator/api.py](../../orchestrator/api.py), [tests/test_strategy_replay_service.py](../../tests/test_strategy_replay_service.py) | Service tests for query parsing, filters, sorting, pagination, response metadata | `49 passed` | `READ_ONLY` / read-only route | API skeleton is not production-hardened and still depends on incomplete replay data |
| P4 | Data readiness gate | [wbc_backend/reporting/strategy_replay_readiness.py](../../wbc_backend/reporting/strategy_replay_readiness.py), [scripts/check_strategy_replay_readiness.py](../../scripts/check_strategy_replay_readiness.py), [tests/test_strategy_replay_readiness.py](../../tests/test_strategy_replay_readiness.py) | Readiness classification, blocker output, and diagnostics tests | `54 passed`, diagnostics still report `BACKFILL_REQUIRED` | `READ_ONLY_DIAGNOSTIC` | Readiness remains blocked by missing historical completeness |
| P5 | Minimum backfill instrumentation | [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py), [wbc_backend/reporting/strategy_replay_backfill_plan.py](../../wbc_backend/reporting/strategy_replay_backfill_plan.py), [tests/test_strategy_replay_instrumentation.py](../../tests/test_strategy_replay_instrumentation.py), [tests/test_strategy_replay_backfill_plan.py](../../tests/test_strategy_replay_backfill_plan.py) | Priority classification and gap-count coverage | `77 passed`, diagnostic still `BACKFILL_REQUIRED` | backfill gap counts in readiness output | P0 blockers still exist in historical rows |
| P6 | Prediction write-path instrumentation | [wbc_backend/domain/schemas.py](../../wbc_backend/domain/schemas.py), [wbc_backend/reporting/prediction_registry.py](../../wbc_backend/reporting/prediction_registry.py), [tests/test_strategy_replay_prediction_instrumentation_write_path.py](../../tests/test_strategy_replay_prediction_instrumentation_write_path.py) | Future-write replay metadata persistence checks | targeted regression suite passed in the P7 slice; historical state unchanged | replay metadata on writes | Fixes future writes only; historical rows still need backfill |
| P7 | Historical backfill candidate export | [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py), [scripts/export_strategy_replay_backfill_candidates.py](../../scripts/export_strategy_replay_backfill_candidates.py), [tests/test_strategy_replay_backfill_candidate_export.py](../../tests/test_strategy_replay_backfill_candidate_export.py) | Export marker / no-mutation / inferred-vs-unsafe field checks | read-only export validation passed, readiness still `BACKFILL_REQUIRED` | `READ_ONLY_BACKFILL_EXPORT` | Export is safe, but auto-write-back is not yet safe for all rows |
| P8 | Backfill review workflow | [wbc_backend/reporting/strategy_replay_backfill_review.py](../../wbc_backend/reporting/strategy_replay_backfill_review.py), [scripts/review_strategy_replay_backfill_candidates.py](../../scripts/review_strategy_replay_backfill_candidates.py), [tests/test_strategy_replay_backfill_review.py](../../tests/test_strategy_replay_backfill_review.py), [00-BettingPlan/20260510/strategy_replay_backfill_approval_manifest.example.json](strategy_replay_backfill_approval_manifest.example.json) | Manifest validation, write-ready classification, and review CLI tests | read-only review validation passed, migration still blocked by default | `READ_ONLY_BACKFILL_REVIEW` | Approval is required; P0 gaps remain unresolved |
| P9 | Approved write-plan flow | [wbc_backend/reporting/strategy_replay_backfill_write_plan.py](../../wbc_backend/reporting/strategy_replay_backfill_write_plan.py), [scripts/build_strategy_replay_backfill_write_plan.py](../../scripts/build_strategy_replay_backfill_write_plan.py), [tests/test_strategy_replay_backfill_write_plan.py](../../tests/test_strategy_replay_backfill_write_plan.py) | Dry-run plan generation and no-mutation tests | dry-run plan validation passed, production execution still blocked | `DRY_RUN_BACKFILL_WRITE_PLAN` | A plan exists, but it is not execution authorization |
| P10 | Fixture-only backfill apply | [wbc_backend/reporting/strategy_replay_backfill_apply.py](../../wbc_backend/reporting/strategy_replay_backfill_apply.py), [scripts/apply_strategy_replay_backfill_write_plan_fixture.py](../../scripts/apply_strategy_replay_backfill_write_plan_fixture.py), [tests/test_strategy_replay_backfill_apply_fixture.py](../../tests/test_strategy_replay_backfill_apply_fixture.py) | Fixture apply semantics, same-path refusal, and no-mutation tests | fixture-only application passed, real historical rows untouched | `FIXTURE_ONLY_BACKFILL_APPLY` | Only proves fixture semantics; production migration remains forbidden |
| P11 | Small-batch migration gate | [wbc_backend/reporting/strategy_replay_migration_gate.py](../../wbc_backend/reporting/strategy_replay_migration_gate.py), [scripts/build_strategy_replay_migration_gate_checklist.py](../../scripts/build_strategy_replay_migration_gate_checklist.py), [tests/test_strategy_replay_migration_gate.py](../../tests/test_strategy_replay_migration_gate.py) | Gate denial, manifest approval, rollback, and UI blocking tests | gate validation passed, default denial preserved | `READ_ONLY_MIGRATION_GATE_CHECKLIST` | Migration is not allowed without explicit approval and complete checks |
| P12 | Staging / fixture migration runner | [wbc_backend/reporting/strategy_replay_staging_migration_runner.py](../../wbc_backend/reporting/strategy_replay_staging_migration_runner.py), [scripts/run_strategy_replay_staging_migration.py](../../scripts/run_strategy_replay_staging_migration.py), [tests/test_strategy_replay_staging_migration_runner.py](../../tests/test_strategy_replay_staging_migration_runner.py) | Staging-only success, production refusal, and immutability tests | staging / fixture runner passed, production mode refused | `STAGING_ONLY_MIGRATION_RUNNER` | Only staging / fixture simulation exists; no production execution |
| P13 | Post-staging readiness recheck | [wbc_backend/reporting/strategy_replay_post_staging_readiness.py](../../wbc_backend/reporting/strategy_replay_post_staging_readiness.py), [scripts/check_strategy_replay_post_staging_readiness.py](../../scripts/check_strategy_replay_post_staging_readiness.py), [tests/test_strategy_replay_post_staging_readiness.py](../../tests/test_strategy_replay_post_staging_readiness.py) | UI unlock, production-write blocking, zero-applied blocking, no-write-default tests | post-staging recheck passed; current repo readiness still blocks UI | `POST_STAGING_READINESS_RECHECK` | UI unlock only becomes eligible if readiness actually reaches `UI_MVP_READY` |
| P14 | End-to-end readiness handoff | This document | No new tests required for documentation-only consolidation | documentation consolidation complete | `P14_STRATEGY_REPLAY_POST_STAGING_READINESS_RECHECK_READY` | The gate chain is still blocked by `BACKFILL_REQUIRED` |

## End-to-End Gate Chain

1. Candidate export: read-only export of historical replay candidates from prediction registry and postgame outcomes.
2. Review gate: classify candidates as review-required, auto-approvable, or write-ready only when the manifest explicitly approves them.
3. Approval manifest: only explicit approvals can move fallback-only or optional candidates toward a write plan.
4. Dry-run write plan: build a dry-run approved plan, but do not execute production writes.
5. Fixture-only apply: verify the plan against copied fixture rows only.
6. Small-batch migration gate: require approval validity, write-plan readiness, fixture apply results, rollback plan, human approval, and UI gating.
7. Staging / fixture-only runner: execute only in staging or fixture mode, never in production mode.
8. Post-staging readiness recheck: combine staged output with readiness classification and determine whether UI spec work may start.
9. UI unlock gate: only if readiness reaches `UI_MVP_READY` and staging output remains safe may `FRONTEND_SPEC_MOCK_DATA` be considered.

## Current Blockers

- Readiness remains `BACKFILL_REQUIRED`.
- Production UI is blocked.
- Production migration is blocked.
- Real historical backfill has still not been executed.
- `actual_result`, `strategy_id`, and `lifecycle_state_at_prediction_time` coverage still may require approved backfill or upstream instrumentation.
- Canonical outcome joins still need stabilization rather than relying on inferred fallback semantics.

## Allowed Next Actions

- Use the read-only diagnostics and reports to keep validating gap closure.
- Use the staging / fixture-only runner only behind the P12 gate.
- Use the post-staging recheck only after staging output exists and only to decide whether frontend spec / mock-data mode can be considered.
- Require an approval manifest before any write-plan item becomes write-ready.
- Keep the UI blocked until the readiness gate actually reaches `UI_MVP_READY`.

## Explicitly Forbidden Actions

- Production migration.
- In-place historical registry mutation.
- Production UI launch.
- Bypassing the approval manifest.
- Bypassing the readiness gate.
- Claiming production readiness before the data completeness blockers are closed.

## Recommended Next Phase

Recommended phase: P16C Historical Data Coverage Audit.

Why this is the best next step:

- The repository is still blocked by `BACKFILL_REQUIRED`, so the limiting factor is historical completeness, not UI polish.
- P16A Frontend Spec / Mock Data Mode is only sensible after post-staging output proves the gate can actually unlock UI work.
- P16B Staging Small-Batch Trial With Approved Fixture Manifest is useful, but it depends on the same historical data quality being trustworthy enough to justify a real trial batch.
- A coverage audit is the safest way to target the remaining gaps in `strategy_id`, `lifecycle_state_at_prediction_time`, canonical join stability, and `actual_result` before any broader UI or migration expansion.

## Next Worker Agent Prompt

Copy-paste this as the next prompt:

```text
You are Betting-pool's next Strategy Replay worker.

Mission: perform P16C Historical Data Coverage Audit for the Strategy Replay flow inside /Users/kelvin/Kelvin-WorkSpace/Betting-pool only.

Constraints:
- documentation or read-only analysis only unless a file edit is strictly necessary
- do not touch LotteryNew, Stock, Novel, number-pattern-research, or unrelated H6/DB lane work
- no production DB writes
- no historical registry mutation
- no migration execution
- no frontend implementation
- no CI or branch protection changes
- no betting recommendation logic changes

Goal:
- audit the remaining historical coverage gaps that keep readiness at BACKFILL_REQUIRED
- identify exactly which historical sources still miss strategy_id, lifecycle_state_at_prediction_time, canonical_outcome_key stability, and actual_result coverage
- produce a short action plan that keeps UI blocked until UI_MVP_READY is actually reached

Required outputs:
- a read-only coverage summary
- a gap list ranked by severity
- the next safe slice to implement after the audit
- explicit confirmation that production UI and production migration are still blocked

Use the existing Strategy Replay reports under 00-BettingPlan/20260510/ as the source of truth.
```

P15_STRATEGY_REPLAY_END_TO_END_GATE_MAP_READY