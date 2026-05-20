# Strategy Replay Historical Backfill Candidate Export Report

Date: 2026-05-10
Repo: Betting-pool
Status: Read-only historical backfill candidate export implemented; no historical data mutated

## What Was Implemented

- A read-only export CLI at [scripts/export_strategy_replay_backfill_candidates.py](scripts/export_strategy_replay_backfill_candidates.py) that prints `READ_ONLY_BACKFILL_EXPORT`, accepts explicit prediction registry / postgame outcomes / output paths, and supports `jsonl` or `json` output.
- Pure export helpers in [wbc_backend/reporting/strategy_replay_instrumentation.py](wbc_backend/reporting/strategy_replay_instrumentation.py) that build historical backfill candidate rows without mutating source records.
- Candidate rows now preserve original source references and expose:
  - `proposed_strategy_id`
  - `proposed_lifecycle_state_at_prediction_time`
  - `proposed_canonical_outcome_key`
  - `proposed_actual_result`
  - `backfill_priority`
  - `backfill_reasons`
  - `inferred_fields`
  - `unsafe_to_infer_fields`
  - `data_quality_flags`
- Fixture-based coverage at [tests/test_strategy_replay_backfill_candidate_export.py](tests/test_strategy_replay_backfill_candidate_export.py) verifying:
  - the export marker is printed
  - output is written only to the explicit output path
  - input files are not mutated
  - missing `strategy_id` is unsafe to infer
  - missing `lifecycle_state_at_prediction_time` is unsafe to infer
  - canonical fallback via `game_id` is marked inferred
  - `actual_result` joins from the postgame outcome when available
  - missing `actual_result` is unsafe to infer
  - both `jsonl` and `json` formats work
  - the script has no production DB dependencies

## What Was Not Implemented

- No historical data backfill.
- No production DB writes.
- No schema migration.
- No frontend UI.
- No CI or branch protection changes.
- No betting model or recommendation logic changes.
- No automatic write-back of candidate rows into historical registry files.

## Files Changed

- [wbc_backend/reporting/strategy_replay_instrumentation.py](wbc_backend/reporting/strategy_replay_instrumentation.py)
- [scripts/export_strategy_replay_backfill_candidates.py](scripts/export_strategy_replay_backfill_candidates.py)
- [tests/test_strategy_replay_backfill_candidate_export.py](tests/test_strategy_replay_backfill_candidate_export.py)
- [00-BettingPlan/20260510/strategy_replay_historical_backfill_candidate_export_report.md](00-BettingPlan/20260510/strategy_replay_historical_backfill_candidate_export_report.md)

## Tests Run

- `./.venv/bin/python -m pytest tests/test_strategy_replay_history_contract.py tests/test_strategy_replay_adapter.py tests/test_strategy_replay_service.py tests/test_strategy_replay_readiness.py tests/test_strategy_replay_instrumentation.py tests/test_strategy_replay_backfill_plan.py tests/test_strategy_replay_prediction_instrumentation_write_path.py tests/test_strategy_replay_backfill_candidate_export.py -q`
- `./.venv/bin/python scripts/check_strategy_replay_readiness.py`

## PASS / FAIL

- PASS: the export CLI emits `READ_ONLY_BACKFILL_EXPORT` and writes only to the explicit output path.
- PASS: historical rows are not mutated in place.
- PASS: candidate export rows preserve original source references and separate inferred versus unsafe fields.
- PASS: `actual_result` joins from postgame outcomes when present.
- PASS: both JSONL and JSON output modes work.
- PASS: the replay readiness diagnostic still reports `BACKFILL_REQUIRED`.
- FAIL: historical backfill cannot be fully automated end-to-end yet, because P0 fields still require human review or upstream instrumentation before a write-back step.

## Can Historical Backfill Be Safely Automated?

Only partially.

The export step can be automated safely because it is read-only and preserves provenance. A direct automatic write-back of historical rows is not safe yet for rows that still miss `strategy_id`, `lifecycle_state_at_prediction_time`, or `actual_result`.

## Unsafe To Infer Fields

- `strategy_id`
- `lifecycle_state_at_prediction_time`
- `actual_result`
- `canonical_outcome_key` when the only available value is a `game_id` fallback; this should stay marked as inferred and treated as P1, not as canonical truth

## Current Readiness Level

`BACKFILL_REQUIRED`

This is still the correct gate state because the repository now has a safe export surface for historical candidates, but it does not yet have a fully automated historical write-back path.

## Can UI Work Start?

No. UI work should remain blocked until the historical completeness gaps are closed and readiness reaches `UI_MVP_READY`.

## Remaining Blockers Before UI

1. Some historical rows still miss `strategy_id`.
2. Some historical rows still miss `lifecycle_state_at_prediction_time`.
3. Some historical rows still need canonical join stabilization rather than game-id fallback.
4. Some historical rows still miss `actual_result` until postgame joins are available.
5. The replay page should stay blocked until the readiness gate moves beyond `BACKFILL_REQUIRED`.

## Next Worker Prompt

Use the exported candidate file as the review input for a minimal historical backfill pass, then rerun the read-only readiness diagnostic to confirm whether the gate can move closer to `UI_MVP_READY` without introducing unsafe inference.

P8_STRATEGY_REPLAY_HISTORICAL_BACKFILL_CANDIDATE_EXPORT_READY