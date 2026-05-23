# Strategy Replay UI — Mock-Only Wireframe Spec

## Status

**Mock-data/spec-only. Not production UI.**

This document is a wireframe specification for the Strategy Replay UI in mock/spec-only mode.
No frontend implementation was created. No production API call is allowed.

## Warnings

- Mock-data/spec-only. Not production UI.
- No production migration has been executed.
- Historical strategy identity remains blocked unless explicit metadata source is accepted.
- Runtime production enablement is blocked.

## Scope

This spec covers the mock-only wireframe layout for the Strategy Replay feature.
The UI described here is strictly a design/spec artifact. It does not represent a live system.

## Production Gates

- production UI can start = false
- runtime production enablement can start = false
- production migration can start = false
- No production launch button is exposed in this spec.
- No migration button is exposed in this spec.

## Pages

### StrategyReplayMockPage

Top-level page wrapper. Displays `ProductionBlockedBanner` prominently.

### ProductionBlockedBanner

Persistent banner indicating production is blocked. Non-dismissible.
Text: "Mock-data/spec-only. Not production UI."

### ReplayReadinessPanel

Shows current readiness state. Always reads `MOCK_DATA_ONLY` in this spec.

### ReplayFilterPanel

Filter controls for strategy ID, lifecycle state, date range.
All actions in filter panel are read-only in mock mode.

### ReplayMockTable

Tabular display of mock replay rows.
Each row shows: strategy_id, lifecycle_state_at_prediction_time, game_id, prediction, actual_result.
`production_ready` column always shows `false`.

### ReplayQualityBadge

Badge component showing data quality flags per row.

### ReplayDetailDrawer

Side drawer showing full detail for a selected replay row.
No production action buttons are shown.

### ReplayDisabledActionNotice

Notice component displayed in place of production action buttons.
Text: "Production actions are disabled in mock/spec mode."

### ReplayPagination

Standard pagination for mock table rows.

### ReplayEmptyState

Empty state component shown when no rows match filters.

### ReplayErrorState

Error state component shown when mock data fails to load.
