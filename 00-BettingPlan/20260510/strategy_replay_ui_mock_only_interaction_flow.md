# Strategy Replay UI — Mock-Only Interaction Flow

## Status

**Mock-data/spec-only. Not production UI.**

This document describes the interaction flow for the Strategy Replay UI in mock/spec-only mode.

## Warnings

- Mock-data/spec-only. Not production UI.
- No production migration has been executed.
- Historical strategy identity remains blocked unless explicit metadata source is accepted.
- Runtime production enablement is blocked.
- No production API call is allowed.

## Flow Overview

All interactions in this spec are read-only and operate on fixture/mock data only.

### Step 1 — Page Load

User navigates to StrategyReplayMockPage.
`ProductionBlockedBanner` is rendered immediately.
`ReplayReadinessPanel` shows `MOCK_DATA_ONLY`.

### Step 2 — Filter

User applies filters via `ReplayFilterPanel`.
No production API call is allowed. Filters operate on local mock data.

### Step 3 — Table View

`ReplayMockTable` renders filtered mock rows.
`ReplayQualityBadge` shows data quality flags per row.
`ReplayDisabledActionNotice` appears where production actions would be shown.

### Step 4 — Detail Drawer

User clicks a row to open `ReplayDetailDrawer`.
Full mock row detail is shown. No production action buttons are present.
No production migration has been executed.

### Step 5 — Pagination

User pages through mock results using `ReplayPagination`.

### Empty State

If no rows match, `ReplayEmptyState` is shown.

### Error State

If mock data fails to load, `ReplayErrorState` is shown.

## Production Gate Checklist

- production UI can start = false
- runtime production enablement can start = false
- production migration can start = false
- No production launch button
- No migration button
