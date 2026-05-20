# Strategy Replay Metadata Registry Rollback Plan Draft

Date: 2026-05-10
Status: Draft / Not Executed

## Scope

This rollback plan covers the Strategy Replay metadata registry candidate path only. It does not modify historical prediction rows, and it does not authorize any production writes.

## Trigger Conditions

- production review rejects the candidate
- reviewer requests rollback before approval
- unexpected metadata write behavior appears in fixture or staging validation
- any production readiness claim is discovered before approval

## Rollback Owner

- Owner: `wbc_backend.reporting.strategy_registry`
- Reviewer: to be assigned during human review

## How to Disable Runtime Metadata Registry Path

- keep the registry draft out of runtime configuration
- keep `runtime_enabled = false`
- do not point runtime request builders at the draft artifact
- continue to load metadata only through the existing explicit test path when needed

## How to Revert to Non-Strict Metadata Injection

- call the runtime helper in non-strict mode only for read-only diagnostics
- avoid promoting the candidate draft to any production-facing registry path
- keep unresolved metadata returning empty kwargs rather than enabling writes

## How to Verify No Production Writes Occurred

- confirm the candidate draft is stored only under `00-BettingPlan/20260510/`
- confirm no production DB commands were run
- confirm the acceptance gate returned `accepted = false`
- confirm the runtime enablement flag remains false

## How to Verify Future Rows Stop Receiving Production Metadata

- confirm runtime production enablement remains false
- confirm no production registry source is mounted in runtime configuration
- run the explicit runtime metadata fixture test to ensure future-row injection remains fixture-only

## How to Preserve Audit Logs

- retain the candidate draft JSON
- retain the acceptance context draft JSON
- retain the evidence pack and review package reports
- retain test output in the workspace history

## Re-run Fixture Validation

- rerun `tests/test_strategy_replay_runtime_metadata_e2e_fixture.py`
- rerun the acceptance gate dry-run against the draft candidate after any review change

## Historical Backfill

No historical backfill rollback is needed because historical backfill remains disabled.
