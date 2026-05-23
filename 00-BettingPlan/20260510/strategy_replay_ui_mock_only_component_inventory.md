# Strategy Replay UI — Mock-Only Component Inventory

## Status

**Mock-data/spec-only. Not production UI.**

This document lists all UI components defined in the Strategy Replay mock/spec package.

## Component List

### StrategyReplayMockPage

Top-level page wrapper for the Strategy Replay mock UI.
Orchestrates all child components. Enforces mock-only mode throughout.

### ProductionBlockedBanner

Persistent banner displayed at the top of `StrategyReplayMockPage`.
Communicates that production is blocked and this is a mock/spec-only view.

### ReplayReadinessPanel

Panel showing the current readiness state of the replay system.
In mock mode, always displays `MOCK_DATA_ONLY`.

### ReplayFilterPanel

Filter controls for narrowing replay rows by strategy ID, lifecycle state, and date range.
Read-only in mock mode; no production API calls are made.

### ReplayMockTable

Tabular component displaying mock replay rows.
Columns: strategy_id, strategy_name, lifecycle_state_at_prediction_time, game_id, prediction, actual_result, data_quality_flags.

### ReplayQualityBadge

Badge displayed in each table row showing data quality flags.
Color-coded by severity. Mock data only.

### ReplayDetailDrawer

Side drawer opened when user clicks a table row.
Displays full detail for the selected mock replay record. No production action buttons.

### ReplayDisabledActionNotice

Notice rendered in place of production action buttons.
Explicitly states that production actions are disabled in mock mode.

### ReplayPagination

Standard pagination controls for the `ReplayMockTable`.

### ReplayEmptyState

Component shown when no mock rows match the current filters.

### ReplayErrorState

Component shown when the mock data fails to load or parse.
