# Strategy Replay Backfill Review Workflow Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only review workflow implemented; no historical data mutated

## What Was Implemented

- A pure review workflow helper at [wbc_backend/reporting/strategy_replay_backfill_review.py](wbc_backend/reporting/strategy_replay_backfill_review.py) that loads backfill candidates, summarizes them, classifies review decisions, validates approval manifests, and builds a safe migration proposal.
- A read-only review CLI at [scripts/review_strategy_replay_backfill_candidates.py](scripts/review_strategy_replay_backfill_candidates.py) that prints `READ_ONLY_BACKFILL_REVIEW`, accepts candidates plus an optional approval manifest, and does not write any files.
- An approval manifest example at [00-BettingPlan/20260510/strategy_replay_backfill_approval_manifest.example.json](00-BettingPlan/20260510/strategy_replay_backfill_approval_manifest.example.json).
- Fixture-based regression coverage at [tests/test_strategy_replay_backfill_review.py](tests/test_strategy_replay_backfill_review.py) covering:
  - P0 unsafe candidates remain review required
  - P1 fallback-only candidates are not write-ready without a manifest
  - P1 fallback-only candidates can become write-ready with a valid manifest
  - P2 optional candidates can be auto-approvable but not write-ready without a manifest
  - unknown candidate references are rejected
  - missing manifest fields invalidate approval
  - the review CLI prints the required marker
  - no production DB access and no writes

## What Was Not Implemented

- No historical data backfill.
- No production DB writes.
- No schema migration.
- No frontend UI.
- No CI or branch protection changes.
- No betting model or recommendation logic changes.
- No automatic historical write-back.

## Files Changed

- [wbc_backend/reporting/strategy_replay_backfill_review.py](wbc_backend/reporting/strategy_replay_backfill_review.py)
- [scripts/review_strategy_replay_backfill_candidates.py](scripts/review_strategy_replay_backfill_candidates.py)
- [00-BettingPlan/20260510/strategy_replay_backfill_approval_manifest.example.json](00-BettingPlan/20260510/strategy_replay_backfill_approval_manifest.example.json)
- [tests/test_strategy_replay_backfill_review.py](tests/test_strategy_replay_backfill_review.py)
- [00-BettingPlan/20260510/strategy_replay_backfill_review_workflow_report.md](00-BettingPlan/20260510/strategy_replay_backfill_review_workflow_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py tests/test_strategy_replay_backfill_review.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: the review CLI prints `READ_ONLY_BACKFILL_REVIEW` and remains read-only.
- PASS: P0 candidates remain review required.
- PASS: P1 fallback-only candidates are only write-ready when a valid approval manifest explicitly allows them.
- PASS: P2 optional candidates can be auto-approvable without being write-ready.
- PASS: unknown manifest references are rejected.
- PASS: manifest field validation blocks incomplete approvals.
- PASS: the readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: migration is not allowed by default because the backfill set still contains unresolved historical gaps and approval is not complete.

## Is Migration Allowed?

Not yet.

The review gate only allows migration when the approval manifest is valid and every candidate targeted for migration is explicitly approved. The current historical set still has P0 gaps, so the safe default remains blocked.

## Can UI Work Start?

No. UI work should remain blocked until the readiness gate moves beyond `BACKFILL_REQUIRED` and the historical candidate set is safe to migrate.

## Remaining Blockers Before UI

1. Historical rows still miss `strategy_id`.
2. Historical rows still miss `lifecycle_state_at_prediction_time`.
3. Historical rows still need canonical join stabilization rather than game-id fallback.
4. Historical rows still miss `actual_result` until postgame joins are available.
5. The review gate is intentionally blocking migration until explicit approval manifests are present and valid.

## Next Worker Prompt

Use the review CLI output together with a signed approval manifest to decide which candidates can move into a minimal historical backfill write-back plan, then rerun the read-only readiness diagnostic before any migration attempt.

P9_STRATEGY_REPLAY_BACKFILL_REVIEW_WORKFLOW_READY