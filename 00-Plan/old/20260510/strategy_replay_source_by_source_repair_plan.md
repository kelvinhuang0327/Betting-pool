# Strategy Replay Source-by-Source Repair Plan

Date: 2026-05-10
Status: Read-only repair analysis
Scope: Historical Strategy Replay readiness blockers only

## Conclusion

The historical blocker is still real and still structural:

- `strategy_id` cannot be safely repaired from any historical source discovered in this workspace.
- `lifecycle_state_at_prediction_time` cannot be safely repaired from any historical source discovered in this workspace.
- `actual_result` can be safely repaired for only the rows that have an exact match in `data/wbc_backend/reports/postgame_results.jsonl`.

That means the historical set cannot reach `UI_MVP_READY` from the available sources alone. The best outcome from a safe repair pass is a partial `actual_result` backfill, while the two identity fields remain blocked.

## Sources Reviewed

- `data/wbc_backend/reports/prediction_registry.jsonl`
- `data/wbc_backend/reports/postgame_results.jsonl`
- `wbc_backend/reporting/strategy_replay_instrumentation.py`
- `wbc_backend/reporting/strategy_replay_backfill_plan.py`
- `scripts/check_strategy_replay_readiness.py`
- `scripts/export_strategy_replay_backfill_candidates.py`
- `scripts/review_strategy_replay_backfill_candidates.py`
- `00-BettingPlan/20260510/strategy_replay_historical_data_coverage_audit.md`
- `00-BettingPlan/20260510/strategy_replay_end_to_end_gate_map.md`

## Field-Level Classification

| Field | Classification | Evidence | Safe Repair Path |
|---|---|---|---|
| `strategy_id` | `SOURCE_NOT_FOUND` | The historical prediction registry rows do not carry a strategy identifier, and no alternate source in the current workspace exposes one for these 66 rows. The instrumentation helper only knows how to read `strategy_id` if it already exists in the record or a nested request/decision payload. | None available from current historical sources. Keep blocked. |
| `lifecycle_state_at_prediction_time` | `SOURCE_NOT_FOUND` | The historical prediction registry rows do not carry a lifecycle snapshot, and no alternate source in the current workspace exposes a trustworthy historical lifecycle state for these rows. The helper can only snapshot from present-tense lifecycle fields when they exist. | None available from current historical sources. Keep blocked. |
| `actual_result` | `SAFE_TO_REPAIR` for matched rows, `SOURCE_NOT_FOUND` for unmatched rows | `postgame_results.jsonl` provides actual outcomes for a subset of games. A direct join by `game_id` succeeds for 17 of the 66 historical prediction rows. The remaining 49 historical prediction rows have no matching outcome row in the available postgame source. | Backfill only the 17 exact matches. Leave the other 49 rows unchanged. |
| `canonical_outcome_key` | `ALREADY_PRESENT` | The historical export and diagnostics show this field is already present for all 66 rows. | No repair needed. |

## Repair Decision Rules

### `strategy_id`

- Do not infer from `game_id`, `teams`, `request`, or downstream model output.
- Do not promote any fallback label, team code, or market label to a strategy identity.
- Do not synthesize a surrogate strategy id from file names or row order.

Decision: remain blocked until a real historical source is found.

### `lifecycle_state_at_prediction_time`

- Do not infer from current state, postgame state, or any later-stage evaluation artifact.
- Do not derive from model confidence, result quality, or gate status.
- Do not reuse the live snapshot state as a historical substitute.

Decision: remain blocked until a real historical lifecycle snapshot is found.

### `actual_result`

- Exact `game_id` match against `data/wbc_backend/reports/postgame_results.jsonl` is acceptable.
- The join must be exact and deterministic.
- Rows without a matching postgame record stay untouched.

Decision: safe to backfill only the 17 exact matches.

## Impact Summary

- Total historical prediction rows: 66
- Rows with exact `actual_result` join available: 17
- Rows still missing `actual_result` after safe join: 49
- Rows missing `strategy_id`: 66
- Rows missing `lifecycle_state_at_prediction_time`: 66
- Rows already carrying `canonical_outcome_key`: 66

## Readiness Effect

Even after a safe `actual_result` repair pass, the historical dataset still cannot satisfy the readiness gate because the two critical identity fields are absent across the full historical set.

Result:

- `BACKFILL_REQUIRED` remains the correct readiness level.
- `UI_MVP_READY` is not reachable from current historical sources alone.
- Production migration remains blocked.

## Recommended Next Step

If the goal is to move readiness forward without violating provenance rules, the next safe action is to produce a narrow repair candidate list for the 17 joinable `actual_result` rows only, with the remaining 49 rows explicitly marked as `NO_MATCH`.

If the goal is to unblock `strategy_id` or `lifecycle_state_at_prediction_time`, a new authoritative source must be introduced before any repair is attempted.
