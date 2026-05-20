# Strategy Replay UI Mock-Data Contract

Marker: `P40_STRATEGY_REPLAY_UI_MOCK_DATA_SPEC_GATE_READY`

## Purpose
This contract defines a non-production, read-only UI mock-data/spec mode for Strategy Replay. It is a design aid only and does not authorize production launch, runtime enablement, or production migration.

## Allowed Mode
- `UI_MOCK_DATA_SPEC_ONLY`
- production UI launch = `false`
- source = fixture/mock only
- readiness level = `BACKFILL_REQUIRED` or `MOCK_DATA_ONLY`

## Required Safety Labels
- `Mock-data/spec-only. Not production UI.`
- `No production migration has been executed.`
- `Historical strategy identity remains blocked unless explicit metadata source is accepted.`

## Table Columns
The UI table should expose only read-only replay fields:
- `strategy_id`
- `strategy_name`
- `game_id`
- `prediction_timestamp`
- `lifecycle_state_at_prediction_time`
- `current_lifecycle_state`
- `actual_result`
- `data_quality_flags`
- `replay_metadata_version`
- `prediction.home_win_prob`
- `prediction.away_win_prob`
- `prediction.expected_home_runs`
- `prediction.expected_away_runs`
- `prediction.confidence_score`
- `prediction.market_bias_score`
- `prediction.x_factors`
- `prediction.diagnostics.regime`
- `source_mode`
- `row_status`

## Filter Definitions
Supported filters mirror the read-only service/query contract and remain non-mutating:
- `strategy_id`
- `lifecycle_state`
- `date_from`
- `date_to`
- `market_type`
- `settlement_status`
- `sort_by`
- `sort_dir`
- `page`
- `page_size`
- `data_quality_flag`
- `source_mode`

## Sort Keys
- `prediction_timestamp`
- `strategy_id`
- `lifecycle_state_at_prediction_time`
- `market_type`
- `settlement_status`
- `game_id`

## Pagination Shape
```json
{
  "page": 1,
  "page_size": 25,
  "total_rows": 3,
  "total_pages": 1
}
```

## Detail Drawer Fields
- explicit strategy identity fields
- lifecycle state snapshot fields
- raw prediction block
- actual result block
- replay metadata version
- quality flags
- source references
- warnings
- disabled actions

## Quality Badges
- `FIXTURE_ONLY`
- `MOCK_DATA_SPEC_ONLY`
- `BACKFILL_REQUIRED`
- `MISSING_ACTUAL_RESULT`
- `CANONICAL_OUTCOME_KEY_FALLBACK_TO_GAME_ID`
- `NO_PRODUCTION_LAUNCH`

## Disabled Actions
- `PRODUCTION_LAUNCH`
- `RUNTIME_PRODUCTION_ENABLEMENT`
- `PRODUCTION_MIGRATION`
- `PRODUCTION_DB_WRITE`
- `HISTORICAL_REGISTRY_MUTATION`
- `HISTORICAL_IDENTITY_REPAIR`

## Blocked Production Actions
- production UI launch
- runtime production enablement
- production migration
- production DB writes
- historical registry mutation
- historical identity repair

## API Response Shape
The mock API response must include:
- `mode`
- `production_ui`
- `ui_mode`
- `source_mode`
- `readiness_level`
- `warnings`
- `disabled_actions`
- `filters`
- `pagination`
- `rows`
- `empty_state`
- `error_state`
- `quality_badges`
- `detail_drawer_fields`
- `final_marker`

## Empty State
When no rows are present, the UI should show:
- mock-data/spec-only notice
- a callout explaining that this is not production UI
- a reminder that historical strategy identity remains blocked until an explicit source is accepted

## Error State
When the mock payload fails validation, the UI should show:
- a contract validation error
- a blocked production launch notice
- the required safety labels above

## Required Warnings
The payload must carry these exact warnings:
- `Mock-data/spec-only. Not production UI.`
- `No production migration has been executed.`
- `Historical strategy identity remains blocked unless explicit metadata source is accepted.`

## Final Notes
This package is intentionally non-production. It can support design, QA, and contract review, but it must not be repurposed as a launch signal.
