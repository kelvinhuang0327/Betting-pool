# Strategy Replay UI Mock-Only Interaction Flow

Marker: `P41_STRATEGY_REPLAY_UI_MOCK_ONLY_WIREFRAME_SPEC_READY`

## 1. Initial Load
1. Load the mock-only page.
2. Read the P40 fixture payload.
3. Render the warning banner, readiness panel, filter panel, table, and footer.
4. Show the mode label `UI_MOCK_DATA_SPEC_ONLY`.

### Initial load rules
- No production API call is allowed.
- No runtime production enablement request is allowed.
- No migration request is allowed.
- If the mock payload is unavailable, the error state is shown instead of any production fallback.

## 2. Filter Changes
1. User changes one or more filters.
2. The page re-applies the local mock dataset slice.
3. The table and pagination update.

### Filter change rules
- Filters are read-only.
- Filters must never change production state.
- Changing filters must not hide the warning banner.
- Changing filters must not hide readiness blockers.

## 3. Sort Changes
1. User changes the sort key or direction.
2. The mock rows are re-ordered locally.
3. Table headers reflect the active sort.

### Sort rules
- Default sort remains `prediction_timestamp desc`.
- Sorting is local and non-mutating.
- Sorting must not trigger any production endpoint call.

## 4. Page Changes
1. User navigates to another page.
2. The page updates the mock pagination state.
3. Rows are re-sliced from the fixture payload.

### Pagination rules
- Default page size is `25`.
- Page changes must not request production data.
- Page changes must keep the warning banner and blocker panel visible.

## 5. Row Selection
1. User selects a row.
2. The detail drawer opens with the selected row content.
3. The selected row remains highlighted.

### Row selection rules
- Row selection is read-only.
- Row selection does not open any production editing surface.
- Row selection does not reveal any launch control.

## 6. Detail Drawer Open / Close
1. A selected row opens the drawer.
2. The drawer shows identity, lifecycle, prediction, actual result, warnings, and disabled actions.
3. The drawer closes when the user dismisses it.

### Drawer rules
- Drawer content must be sourced from the mock payload only.
- Closing the drawer must not clear the table selection state unless the implementation explicitly chooses to do so for mock-only UX.
- The drawer must never expose production-enable controls.

## 7. Warning Banner Behavior
- The banner is visible on every state.
- The banner is not dismissible.
- The banner copy stays unchanged unless the contract changes.
- The banner remains visible when filters, sort, pagination, or drawer state changes.

## 8. Disabled Production Actions Behavior
1. User sees disabled actions in the drawer or action surface.
2. Hover/click explains that the action is blocked.
3. No request is sent.

### Disabled-action rules
- `PRODUCTION_LAUNCH` remains blocked.
- `RUNTIME_PRODUCTION_ENABLEMENT` remains blocked.
- `PRODUCTION_MIGRATION` remains blocked.
- `PRODUCTION_DB_WRITE` remains blocked.
- `HISTORICAL_REGISTRY_MUTATION` remains blocked.
- `HISTORICAL_IDENTITY_REPAIR` remains blocked.

## 9. Error Handling
If the mock contract fails validation or the payload cannot be parsed:
1. Show the error state.
2. Keep the banner visible.
3. Keep the blocker panel visible.
4. Do not fall back to production data.

### Error handling rules
- Contract failure is a UI error, not a production launch signal.
- Validation failure must be legible.
- The page must remain read-only even in error mode.

## 10. Mock-Data Refresh Behavior
1. The mock payload may be refreshed by replacing the fixture file.
2. The page may re-render after a local refresh.
3. The updated mock data must still obey the contract.

### Refresh rules
- Refresh means local fixture refresh only.
- Refresh does not mean production sync.
- Refresh must not change readiness from blocked to production-ready.

## 11. No Production API Call Guarantee
The page must guarantee the following:
- No production read API calls.
- No production write API calls.
- No migration API calls.
- No runtime enablement calls.
- No DB access from the UI layer.

If a future frontend implementation introduces data fetching, it must remain fixture-only or mock-only for this mode.

## 12. Interaction Summary
This interaction flow is intentionally shallow: load, inspect, filter, sort, paginate, open drawer, close drawer, and inspect blockers.

It never crosses into production enablement, production migration, or historical mutation.
