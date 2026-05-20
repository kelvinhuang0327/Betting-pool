# Strategy Replay Minimum Backfill Instrumentation Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only instrumentation and backfill plan implemented, no production DB writes

## What Was Implemented

- A pure instrumentation module at [wbc_backend/reporting/strategy_replay_instrumentation.py](wbc_backend/reporting/strategy_replay_instrumentation.py) that resolves strategy identity, snapshots lifecycle state, builds canonical outcome keys, and prepares backfill candidates without mutating source records.
- A pure backfill-plan module at [wbc_backend/reporting/strategy_replay_backfill_plan.py](wbc_backend/reporting/strategy_replay_backfill_plan.py) that classifies replay gaps into P0, P1, and P2 priorities and summarizes next actions.
- An updated readiness diagnostic at [scripts/check_strategy_replay_readiness.py](scripts/check_strategy_replay_readiness.py) that now prints backfill gap counts for P0, P1, and P2.
- Fixture-based coverage at [tests/test_strategy_replay_instrumentation.py](tests/test_strategy_replay_instrumentation.py) and [tests/test_strategy_replay_backfill_plan.py](tests/test_strategy_replay_backfill_plan.py) for canonical-key fallback detection, lifecycle snapshots, validation behavior, and priority classification.

## What Was Not Implemented

- No frontend page.
- No production DB schema migration.
- No production DB writes.
- No CI / branch protection changes.
- No betting recommendation logic change.
- No bankroll optimization.
- No strategy mining.
- No production replay write path.

## Files Changed

- [wbc_backend/reporting/strategy_replay_instrumentation.py](wbc_backend/reporting/strategy_replay_instrumentation.py)
- [wbc_backend/reporting/strategy_replay_backfill_plan.py](wbc_backend/reporting/strategy_replay_backfill_plan.py)
- [scripts/check_strategy_replay_readiness.py](scripts/check_strategy_replay_readiness.py)
- [tests/test_strategy_replay_instrumentation.py](tests/test_strategy_replay_instrumentation.py)
- [tests/test_strategy_replay_backfill_plan.py](tests/test_strategy_replay_backfill_plan.py)
- [00-BettingPlan/20260510/strategy_replay_minimum_backfill_instrumentation_report.md](00-BettingPlan/20260510/strategy_replay_minimum_backfill_instrumentation_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: targeted replay suites returned 77 passed.
- PASS: readiness diagnostics now report `backfill_required_count`, `p0_gap_count`, `p1_gap_count`, and `p2_gap_count`.
- PASS: canonical-outcome fallback is now explicit instead of being treated as a production-ready join.
- FAIL: the UI cannot start yet, because the current data still needs upstream instrumentation or historical backfill to eliminate P0 blockers.

## Current Readiness Level

`BACKFILL_REQUIRED`

This remains the correct gate state for Betting-pool today. The repository now has the instrumentation and planning surface needed to make the remaining gaps visible and actionable, but it still does not have a canonical production replay store.

## Remaining Blockers Before UI

1. `strategy_id` is still missing in some historical replay rows.
2. `lifecycle_state_at_prediction_time` is still missing in some historical replay rows.
3. `canonical_outcome_key` still falls back to `game_id` in some rows and should not be treated as canonical production data.
4. `actual_result` still depends on downstream joins rather than a fully persisted replay store.
5. The UI should remain blocked until the readiness gate reaches `UI_MVP_READY`.

## Next Worker Prompt

Implement the smallest safe historical backfill or write-time instrumentation step that removes the remaining P0 gaps, then rerun the readiness diagnostic to verify whether the gate can move toward `UI_MVP_READY`.

P6_STRATEGY_REPLAY_MINIMUM_BACKFILL_INSTRUMENTATION_READY
