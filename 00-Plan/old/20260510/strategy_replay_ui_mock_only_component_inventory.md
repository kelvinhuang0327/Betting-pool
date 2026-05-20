# Strategy Replay UI Mock-Only Component Inventory

Marker: `P41_STRATEGY_REPLAY_UI_MOCK_ONLY_WIREFRAME_SPEC_READY`

## 1. StrategyReplayMockPage
**Purpose:** Top-level page shell for the mock-only Strategy Replay view.

**Inputs:** P40 mock payload, derived filters, readiness summary, warning text, mock mode label.

**Outputs / Events:** Renders table, banner, blocker panel, drawer, and footer; delegates user events to child components.

**Blocked production behavior:** Must never mount a production launch flow or a runtime enablement flow.

**Test notes:** Verify the page renders even when the payload has `BACKFILL_REQUIRED` and that the banner copy is always visible.

## 2. ProductionBlockedBanner
**Purpose:** Persistent warning banner explaining the page is mock-only.

**Inputs:** Required warning text, mode label, blocked-action summary.

**Outputs / Events:** None beyond visibility state.

**Blocked production behavior:** The banner must not be dismissible and must never be replaced by a launch-success message.

**Test notes:** Assert the required banner strings are always present.

## 3. ReplayReadinessPanel
**Purpose:** Summarize readiness and blocker state in a visible panel.

**Inputs:** Readiness level, production UI status, runtime enablement status, migration status, blocker list.

**Outputs / Events:** None; informational only.

**Blocked production behavior:** Must show blocked state clearly and never imply approval.

**Test notes:** Check that `production UI can start = false`, `runtime production enablement can start = false`, and `production migration can start = false` are displayed.

## 4. ReplayFilterPanel
**Purpose:** Read-only controls for filtering and sorting mock rows.

**Inputs:** Filter values, available sort keys, pagination defaults.

**Outputs / Events:** Emits filter-change, sort-change, and page-size-change events.

**Blocked production behavior:** Filter changes must never mutate production data or trigger production requests.

**Test notes:** Ensure filter and sort changes only affect local mock state.

## 5. ReplayMockTable
**Purpose:** Display the mock replay rows in a read-only table.

**Inputs:** Mock rows, active sort, paging slice, visible badge state.

**Outputs / Events:** Emits row-select events.

**Blocked production behavior:** No edit controls, no production launch controls, no migration controls.

**Test notes:** Assert required columns are present and row selection opens the drawer only.

## 6. ReplayQualityBadge
**Purpose:** Show row-level and page-level data quality states.

**Inputs:** Badge list from the mock payload, row `data_quality_flags`.

**Outputs / Events:** None.

**Blocked production behavior:** Badges must not be styled as approval or success indicators.

**Test notes:** Verify `FIXTURE_ONLY`, `MOCK_DATA_SPEC_ONLY`, `BACKFILL_REQUIRED`, and `NO_PRODUCTION_LAUNCH` can appear.

## 7. ReplayDetailDrawer
**Purpose:** Show richer row details for one selected replay row.

**Inputs:** Selected row, required detail fields, warnings, disabled actions.

**Outputs / Events:** Close drawer, maybe switch selected row.

**Blocked production behavior:** Must not contain a production-enable action or an approval action.

**Test notes:** Verify the drawer contains identity, lifecycle, prediction, actual result, warnings, and disabled actions.

## 8. ReplayDisabledActionNotice
**Purpose:** Explain why production actions are unavailable in mock-only mode.

**Inputs:** Disabled action list and reason text.

**Outputs / Events:** None.

**Blocked production behavior:** Must not enable any action on click.

**Test notes:** Validate the required disabled action names are rendered and explained.

## 9. ReplayPagination
**Purpose:** Navigate mock rows across pages.

**Inputs:** Current page, page size, total rows, total pages.

**Outputs / Events:** Page-change and page-size-change events.

**Blocked production behavior:** Pagination must remain local and read-only.

**Test notes:** Verify page changes recalculate only the view slice, not the source data.

## 10. ReplayEmptyState
**Purpose:** Explain the empty mock-only dataset state.

**Inputs:** Empty-state title and copy.

**Outputs / Events:** None.

**Blocked production behavior:** Must never suggest the page is ready for production launch.

**Test notes:** Check required empty-state text is visible.

## 11. ReplayErrorState
**Purpose:** Show contract validation or payload parsing failures.

**Inputs:** Error title and blocked copy.

**Outputs / Events:** None.

**Blocked production behavior:** Must not fall back to production data or production UI state.

**Test notes:** Check required error-state copy is visible and production launch remains blocked.
