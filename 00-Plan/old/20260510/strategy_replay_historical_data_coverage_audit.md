# Strategy Replay Historical Data Coverage Audit

Date: 2026-05-10
Repo: Betting-pool
Scope: Read-only historical data coverage audit only
Status: Audit complete; readiness remains `BACKFILL_REQUIRED`

## What Was Audited

- The consolidated gate map at [strategy_replay_end_to_end_gate_map.md](strategy_replay_end_to_end_gate_map.md).
- The read-only readiness diagnostic at [scripts/check_strategy_replay_readiness.py](../../scripts/check_strategy_replay_readiness.py).
- The read-only candidate export at [scripts/export_strategy_replay_backfill_candidates.py](../../scripts/export_strategy_replay_backfill_candidates.py).
- The readiness and backfill helper implementations in [wbc_backend/reporting/strategy_replay_readiness.py](../../wbc_backend/reporting/strategy_replay_readiness.py), [wbc_backend/reporting/strategy_replay_backfill_plan.py](../../wbc_backend/reporting/strategy_replay_backfill_plan.py), and [wbc_backend/reporting/strategy_replay_instrumentation.py](../../wbc_backend/reporting/strategy_replay_instrumentation.py).
- The actual historical JSONL inputs at [data/wbc_backend/reports/prediction_registry.jsonl](../../data/wbc_backend/reports/prediction_registry.jsonl) and [data/wbc_backend/reports/postgame_results.jsonl](../../data/wbc_backend/reports/postgame_results.jsonl).
- The embedded sample replay rows in [scripts/preview_strategy_replay_backfill.py](../../scripts/preview_strategy_replay_backfill.py).

## Data Sources Found

| Source | Path | Notes |
|---|---|---|
| Prediction registry JSONL | [data/wbc_backend/reports/prediction_registry.jsonl](../../data/wbc_backend/reports/prediction_registry.jsonl) | 66 lines / 66 historical prediction rows |
| Postgame outcome JSONL | [data/wbc_backend/reports/postgame_results.jsonl](../../data/wbc_backend/reports/postgame_results.jsonl) | 49 lines / 49 outcome rows |
| Configured prediction registry path | [wbc_backend/config/settings.py](../../wbc_backend/config/settings.py) | `prediction_registry_jsonl` is configured to the same JSONL path above |
| Configured postgame outcome path | [wbc_backend/config/settings.py](../../wbc_backend/config/settings.py) | `postgame_results_jsonl` is configured to the same JSONL path above |
| Sample replay rows | [scripts/preview_strategy_replay_backfill.py](../../scripts/preview_strategy_replay_backfill.py) | Contains embedded sample rows for dry-run preview / diagnostics |

## Data Sources Not Found

- No dedicated fixture JSONL replay corpus was found beyond the embedded sample rows in [scripts/preview_strategy_replay_backfill.py](../../scripts/preview_strategy_replay_backfill.py).
- No separate historical backfill snapshot file was found that would already resolve the remaining P0 gaps.
- No production-hardened canonical replay store was found.

## Coverage Metrics

Read-only diagnostic against the actual JSONL inputs returned:

- total historical prediction rows: 66
- rows with strategy_id: 0
- rows missing strategy_id: 66
- rows with lifecycle_state_at_prediction_time: 0
- rows missing lifecycle_state_at_prediction_time: 66
- rows with canonical_outcome_key: 66
- rows using fallback outcome key only: 0
- rows missing actual_result: 49
- rows UI_MVP_READY eligible: 0
- P0 gap count: 66
- P1 gap count: 0
- P2 gap count: 0
- top unsafe_to_infer_fields:
  - strategy_id: 66
  - lifecycle_state_at_prediction_time: 66
  - actual_result: 49

Additional audit checks:

- `READ_ONLY_DIAGNOSTIC` still reports `BACKFILL_REQUIRED`.
- `READ_ONLY_BACKFILL_EXPORT` succeeded with 66 exported candidates.
- `READ_ONLY_BACKFILL_REVIEW` reported `review_required_count: 66`, `auto_approvable_count: 0`, `write_ready_count: 0`, and `migration_allowed: false`.
- The explicit fallback-only canonical key count in the exported candidate file was 0.

## Blocker Classification

### BLOCKER

- Missing `strategy_id` on every historical replay row prevents safe strategy grouping and filtering.
- Missing `lifecycle_state_at_prediction_time` on every historical replay row prevents historical truth from being reconstructed.
- Missing `actual_result` on 49 rows prevents settled replay output.
- Current readiness remains `BACKFILL_REQUIRED`, so the UI cannot start and production migration cannot start.

### IMPORTANT

- Canonical replay completeness is still incomplete because the real historical rows are not yet safely backfilled.
- The review gate has no write-ready candidates, so approval manifests cannot unlock a batch yet.
- The staging / fixture-only runner exists, but it still depends on historical completeness before it can become meaningful for UI work.

### OPTIONAL

- The read-only API skeleton, dry-run write-plan flow, and fixture-only apply semantics are already in place, but they do not block the current gap closure.

## Can Readiness Move Beyond BACKFILL_REQUIRED?

No.

The current repository data fails the P0 gate completely: all 66 historical rows are missing `strategy_id` and `lifecycle_state_at_prediction_time`, and 49 rows are still missing `actual_result`. That is enough to keep the readiness classifier at `BACKFILL_REQUIRED`.

## UI / Migration Decision

UI can start = false.

production migration can start = false.

Reason:

- The UI is still blocked by missing historical completeness and cannot safely move into `UI_MVP_READY`.
- Production migration is still blocked by design, and the historical rows are not yet safe to write back.

## Recommended Next Phase

Recommended phase: P16C Historical Data Coverage Audit.

Why:

- The dominant blocker is still historical completeness, not UI implementation.
- The audit shows there are no write-ready candidates yet, so staging or frontend work would be premature.
- The next useful slice is to continue source-by-source coverage analysis until the team can identify a safe, smallest historical repair path for `strategy_id`, `lifecycle_state_at_prediction_time`, and `actual_result`.

## Next Worker Agent Prompt

Copy-paste this as the next prompt:

```text
You are Betting-pool's next Strategy Replay worker.

Mission: continue the read-only historical coverage audit for Strategy Replay inside /Users/kelvin/Kelvin-WorkSpace/Betting-pool only.

Constraints:
- read-only analysis only unless a file edit is strictly necessary
- do not touch LotteryNew, Stock, Novel, number-pattern-research, or unrelated H6/DB lane work
- no production DB writes
- no historical registry mutation
- no migration execution
- no frontend implementation
- no CI or branch protection changes
- no betting recommendation logic changes

Goal:
- identify the smallest safe historical repair path for the rows missing strategy_id, lifecycle_state_at_prediction_time, and actual_result
- keep UI blocked until readiness actually reaches UI_MVP_READY
- keep production migration blocked until a separate explicit execution authorization exists

Required outputs:
- a source-by-source coverage breakdown
- a minimal repair plan ranked by severity
- explicit confirmation that UI can start = false and production migration can start = false

Use the actual JSONL inputs and the existing read-only helper modules as the source of truth.
```

P16C_STRATEGY_REPLAY_HISTORICAL_DATA_COVERAGE_AUDIT_READY