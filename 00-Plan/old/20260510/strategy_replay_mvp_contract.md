# Strategy Historical Replay MVP Contract

Date: 2026-05-10
Repo: Betting-pool
Status: MVP planning only, no production code changes
Scope: Betting-pool only

## Source Inputs

- Discovery report: [strategy_replay_page_discovery_and_contract.md](strategy_replay_page_discovery_and_contract.md)
- Roadmap reset: [docs/orchestration/mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md](../../docs/orchestration/mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md)

## 1. Executive Decision

The Strategy Historical Replay Page cannot be fully delivered from the current data surface alone.

Contract work can start immediately, but the user-facing MVP requires backfill and new instrumentation before it can faithfully show all strategies across all lifecycle states with per-period prediction vs actual rows.

### Decision split

- Start immediately: yes, for contract design, data model definition, endpoint contract, and UI spec.
- Ship the user-facing MVP immediately: no, not until the minimum backfill / instrumentation set is in place.

## 2. MVP Scope

The MVP is a read-only replay page that mirrors the current historical review list style, but is strategy-centered instead of game-centered.

### In scope

- Show all strategies regardless of lifecycle state.
- List one row per strategy-period replay record.
- Display prediction vs actual outcome for each period.
- Show historical lifecycle state at prediction time.
- Provide filters for strategy, lifecycle state, market type, and date range.
- Support pagination and deterministic sorting.
- Surface data-quality notes when joins are incomplete or inferred.

### Non-MVP scope

- Strategy creation or editing.
- Lifecycle transition admin UI.
- Automatic strategy mining.
- Betting recommendation logic changes.
- DB schema changes.
- CI / branch protection changes.
- Production replay execution.
- Export/download features.
- Cross-product expansion beyond the current betting-pool MVP contract.

## 3. Minimum Data Model

This is the minimum row shape required for the replay page.

| Field | Required for MVP | Source classification | Notes |
|---|---|---|---|
| strategy_id | Yes | New instrumentation | Stable identifier for grouping and filtering. |
| strategy_name | Yes | New instrumentation or backfill mapping | Human-readable label. |
| lifecycle_state_at_prediction_time | Yes | New instrumentation | Historical truth at the time the prediction was made. |
| current_lifecycle_state | Yes | Backfill from current state or optional live lookup | Secondary metadata only. |
| prediction_timestamp | Yes | Current available field if already stored, otherwise new instrumentation | Must be timezone-aware. |
| game_id / canonical outcome key | Yes | Requires stabilization | Primary replay-period join key. |
| market_type | Yes | Current available field | Examples: moneyline, run line, total, odd/even, first five, team total. |
| recommendation | Yes | Current available field | Keep current recommendation wording where possible. |
| confidence / edge | Optional | Current available field if present | Can be omitted until the upstream signal is reliable. |
| actual_result | Yes | Backfill from outcome storage | Joined settlement result. |
| hit_miss_push | Yes | Derived | Must be explicit, not inferred in the UI. |
| settlement_status | Yes | Backfill from outcome storage | Example values: WON, LOST, PUSH, VOID, PENDING. |
| notes / data_quality_flags | Yes | Derived | Join warnings, missing fields, fallback joins, stale data. |

### Optional for MVP

- model_version
- odds_snapshot_id
- predicted_probability
- closing_probability
- realized_profit_loss
- source_keys / trace metadata
- reviewer notes

## 4. Current Available Fields vs Gaps

### Currently available fields

The discovery pass confirmed the current system already has some row-level review data and prediction metadata:

- game_id
- game_date / date
- market_type
- recommendation
- paper_selection
- model_prob / market_prob in review output
- result_status
- realized_outcome
- review_status
- review_reason
- paper_profit_loss_units
- brier_component
- failure_tags
- recorded_at_utc in prediction registry records
- prediction, game_output, verification, market_support, and decision_report payloads in the registry

### Fields requiring backfill

- strategy_id
- strategy_name
- lifecycle_state_at_prediction_time
- canonical replay-period key for each strategy row
- stable actual outcome join key
- historical transition history for lifecycle state
- settlement_status normalized across historical rows

### Fields requiring new instrumentation

- strategy_id on every replayable prediction event
- lifecycle_state_at_prediction_time captured at write time
- canonical replay-period key captured consistently at write time
- source_keys / join provenance for traceability
- explicit data-quality flags for unresolved joins

### Fields that should remain optional for MVP

- confidence / edge, if not available from all strategies
- model_version, if not uniformly recorded yet
- realized_profit_loss, if settlement logic is incomplete
- closing lines or CLV metadata, if not yet stable
- reviewer notes, if not needed for the first page cut

## 5. Required Backfill Contract

Backfill is required before the user-facing MVP can be considered complete.

### Backfill contract goals

- Reconstruct historical strategy-period rows from existing prediction and outcome stores.
- Map each historical record to a canonical replay-period key.
- Attach lifecycle state as it existed at prediction time, not as it exists now.
- Preserve join provenance so unresolved matches remain visible as data-quality flags.

### Backfill minimum inputs

- Existing prediction registry rows.
- Existing postgame result rows.
- Any current lifecycle status source that can be used to infer current state.
- Any alias / normalization mapping needed to stabilize game or replay keys.

### Backfill minimum outputs

- One canonical replay row per strategy-period.
- Joined actual outcome payload.
- Normalized settlement status.
- Data-quality flags for missing or inferred fields.

### Backfill acceptance rule

If a historical row cannot be joined with high confidence, it must remain visible with a warning flag rather than being silently dropped or guessed.

## 6. Required API Endpoint Contract

The MVP should expose a read-only endpoint that serves the replay page.

### Proposed endpoint

`GET /api/strategy-replay`

### Query parameters

| Param | Type | Required | Behavior |
|---|---|---|---|
| strategy_id | string | no | Exact strategy filter. |
| lifecycle_state | string | no | Filter by lifecycle state at prediction time. |
| market_type | string | no | Filter by market type. |
| date_from | string | no | Inclusive lower bound, ISO date. |
| date_to | string | no | Inclusive upper bound, ISO date. |
| page | integer | no | Default 1. |
| page_size | integer | no | Default 25, max should be capped. |
| sort_by | string | no | Default prediction_timestamp desc. |
| sort_dir | string | no | asc or desc. |

### Response contract

```json
{
  "items": [
    {
      "period": "string",
      "strategy_id": "string",
      "strategy_name": "string",
      "lifecycle_state_at_prediction_time": "string",
      "current_lifecycle_state": "string",
      "prediction_timestamp": "string",
      "game_id": "string",
      "market_type": "string",
      "recommendation": "string",
      "confidence": 0.0,
      "actual_result": "string",
      "hit_miss_push": "string",
      "settlement_status": "string",
      "notes": "string",
      "data_quality_flags": ["string"]
    }
  ],
  "total": 0,
  "page": 1,
  "page_size": 25,
  "sort_by": "prediction_timestamp",
  "sort_dir": "desc",
  "filters": {}
}
```

### Contract rules

- Response must be stable and pagination-safe.
- Items must be sorted deterministically.
- Unresolved joins must not disappear.
- Missing optional fields must serialize as null, not as invented values.

## 7. Frontend Display Fields

The frontend should mirror the compact table style of the existing historical review list while shifting the subject from game review to strategy replay.

### Columns for MVP

- Period
- Strategy
- Lifecycle State
- Prediction Time
- Market
- Recommendation
- Confidence / Edge
- Actual Result
- Hit / Miss / Push
- Settlement Status
- Notes

### Display behavior

- Strategy and lifecycle state must be visually prominent.
- Notes should be compact and only expand when needed.
- Confidence / edge should be hidden if unavailable rather than filled with placeholder text.
- Data-quality warnings should be visually distinguishable from normal notes.

## 8. Filter Fields

### MVP filters

- strategy_id
- lifecycle_state
- market_type
- date_from
- date_to

### Optional later filters

- settlement_status
- hit_miss_push
- current_lifecycle_state
- data_quality_flags

## 9. Pagination and Sort Behavior

### Pagination

- Default page size: 25.
- Maximum page size: 100.
- Empty result sets must return total = 0 and an empty items array.
- Pagination must remain stable under sort order changes.

### Sort defaults

Primary default sort:

- prediction_timestamp desc

Secondary tie-breakers:

- strategy_id asc
- game_id asc

### Sort options for MVP

- prediction_timestamp
- strategy_id
- lifecycle_state_at_prediction_time
- market_type
- settlement_status

## 10. Validation Strategy

Validation must happen in layers.

### Layer 1: contract validation

- Confirm every API row can be serialized with the required fields.
- Confirm required filters work independently and in combination.
- Confirm pagination totals remain consistent across pages.

### Layer 2: backfill validation

- Spot-check a sample of historical rows against source records.
- Confirm current lifecycle state does not overwrite historical lifecycle_state_at_prediction_time.
- Confirm unresolved joins surface as warnings, not silent omissions.

### Layer 3: UI validation

- Confirm the page matches the existing historical review list density and readability.
- Confirm the user can sort, filter, and paginate without losing row context.
- Confirm rows with missing optional fields still render cleanly.

### Layer 4: data-quality validation

- Confirm the join key is stable across all supported historical rows.
- Confirm no strategy rows are dropped because lifecycle state is offline, rejected, or observation.
- Confirm duplicate rows are not produced for the same strategy-period key.

## 11. MVP Build Order

1. Define the canonical replay row contract.
2. Add backfill mapping from current prediction/result stores into that contract.
3. Add the read-only API endpoint.
4. Render the frontend table using the API contract.
5. Add validation around pagination, sort, and join completeness.

## 12. Minimum Acceptance Criteria

The MVP is complete only when all of the following are true:

- The page shows all strategies, regardless of lifecycle state.
- Each row shows prediction vs actual outcome for one replay period.
- Historical lifecycle state is captured at prediction time.
- The page matches the existing historical review list style closely enough to feel native.
- Unresolved joins are visible and flagged.
- Pagination and sorting are deterministic.

## 13. What the Worker Agent Should Do Next

Implement the replay contract in the smallest safe slice:

1. Add a canonical replay DTO / schema.
2. Add a backfill adapter from current prediction and postgame stores into that DTO.
3. Add the read-only API endpoint and paging/sort logic.
4. Render a compact table view with the MVP columns.
5. Add validation for join completeness, stable sorting, and missing-field handling.

Do not expand into strategy mining, recommendation logic, or production settlement behavior during this slice.

## 14. Final Position

This MVP can start immediately as a contract and backfill preparation effort, but it cannot be considered user-facing complete until the minimum backfill and instrumentation are in place.

That is the smallest executable path that still preserves the user requirement: show all strategies, preserve historical lifecycle state, and display per-period prediction vs actual outcome without pretending current data already supports more than it does.

P1_STRATEGY_REPLAY_MVP_CONTRACT_READY
