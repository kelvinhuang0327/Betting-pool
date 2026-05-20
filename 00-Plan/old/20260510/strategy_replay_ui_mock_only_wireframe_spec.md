# Strategy Replay UI Mock-Only Wireframe Spec

Marker: `P41_STRATEGY_REPLAY_UI_MOCK_ONLY_WIREFRAME_SPEC_READY`

## 1. Page Purpose
This page is a non-production, read-only Strategy Replay wireframe for design review, QA review, and contract review only.

It exists to help future frontend work follow the P40 mock-data/spec-only contract safely.

## 2. Allowed Mode
- Allowed mode: `UI_MOCK_DATA_SPEC_ONLY`
- Production UI launch: `false`
- Runtime production enablement: blocked
- Production migration: blocked

## 3. Production Warning Banner
The page must show a persistent banner at the top of the content area.

### Required banner copy
- `Mock-data/spec-only. Not production UI.`
- `No production migration has been executed.`
- `Historical strategy identity remains blocked unless explicit metadata source is accepted.`
- `Runtime production enablement is blocked.`

### Banner behavior
- Visible on every load.
- Not dismissible.
- Never replaced by a success or launch banner.
- If the page is empty or errored, the banner still remains visible.

## 4. Wireframe Layout

### Top-level structure
1. Header row with title, mock mode label, and readiness summary.
2. Persistent production warning banner.
3. Readiness / blocker panel.
4. Filter panel.
5. Replay table.
6. Pagination footer.
7. Non-production footer.

### Simple wireframe sketch
```text
┌────────────────────────────────────────────────────────────────────┐
│ Strategy Replay | MOCK DATA / SPEC ONLY | BACKFILL_REQUIRED        │
├────────────────────────────────────────────────────────────────────┤
│ WARNING: Mock-data/spec-only. Not production UI.                   │
│         No production migration has been executed.                 │
│         Historical strategy identity remains blocked...            │
│         Runtime production enablement is blocked.                  │
├────────────────────────────────────────────────────────────────────┤
│ Readiness / Blockers                                               │
├────────────────────────────────────────────────────────────────────┤
│ Filters                                                            │
├────────────────────────────────────────────────────────────────────┤
│ Table                                                              │
├────────────────────────────────────────────────────────────────────┤
│ Pagination                                                         │
├────────────────────────────────────────────────────────────────────┤
│ Non-production footer                                              │
└────────────────────────────────────────────────────────────────────┘
```

## 5. Table Layout
The table is read-only and must mirror the mock payload fields from P40.

### Primary columns
- `strategy_id`
- `strategy_name`
- `game_id`
- `prediction_timestamp`
- `lifecycle_state_at_prediction_time`
- `current_lifecycle_state`
- `actual_result`
- `data_quality_flags`
- `replay_metadata_version`

### Prediction subcolumns / grouped cells
- `prediction.home_win_prob`
- `prediction.away_win_prob`
- `prediction.expected_home_runs`
- `prediction.expected_away_runs`
- `prediction.confidence_score`
- `prediction.market_bias_score`
- `prediction.x_factors`
- `prediction.diagnostics.regime`

### Table behavior
- Default sort: `prediction_timestamp desc`.
- Table rows are selectable for detail viewing only.
- No inline editing.
- No launch, migrate, or production-enable action in the table.

## 6. Filter Panel Layout
The filter panel sits above the table and uses only read-only controls.

### Filters
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

### Filter panel behavior
- Changing a filter refreshes the mock dataset view only.
- Filters never create or mutate production records.
- Filter state can be reset to the P40 mock defaults.

## 7. Detail Drawer Layout
The detail drawer opens from a selected row and shows a richer replay snapshot.

### Drawer sections
1. Strategy identity section.
2. Lifecycle snapshot section.
3. Raw prediction block.
4. Actual result block.
5. Replay metadata version section.
6. Quality flags section.
7. Source references section.
8. Warnings section.
9. Disabled actions section.

### Drawer fields
- `strategy_id`
- `strategy_name`
- `game_id`
- `prediction_timestamp`
- `lifecycle_state_at_prediction_time`
- `current_lifecycle_state`
- `prediction`
- `actual_result`
- `data_quality_flags`
- `replay_metadata_version`
- `source_mode`
- `warnings`
- `disabled_actions`

## 8. Data-Quality Badges
The page must show quality badges near the header and within row details.

### Badges
- `FIXTURE_ONLY`
- `MOCK_DATA_SPEC_ONLY`
- `BACKFILL_REQUIRED`
- `MISSING_ACTUAL_RESULT`
- `CANONICAL_OUTCOME_KEY_FALLBACK_TO_GAME_ID`
- `NO_PRODUCTION_LAUNCH`

### Badge behavior
- Badges must be visually distinct from warning text.
- Badges must not imply production readiness.
- A row may show multiple badges at once.

## 9. Readiness / Blocker Panel
The readiness panel summarizes why the page is mock-only.

### Panel content
- Allowed mode
- Readiness level
- Production UI status
- Runtime production enablement status
- Production migration status
- Historical strategy identity blocker status

### Panel copy hints
- Show `BACKFILL_REQUIRED` prominently.
- Show `production UI can start = false`.
- Show `runtime production enablement can start = false`.
- Show `production migration can start = false`.

## 10. Empty State
If there are no rows, the UI must show the mock-only empty state.

### Required empty-state copy
- `Mock-data/spec-only. Not production UI.`
- `Historical strategy identity remains blocked unless explicit metadata source is accepted.`

### Empty-state behavior
- Keep the warning banner visible.
- Keep the readiness panel visible.
- Keep the filter panel visible.

## 11. Error State
If the mock payload fails validation, the UI must show a contract error state.

### Required error-state copy
- `Contract validation failed`
- `Mock-data/spec-only. Not production UI.`
- `No production migration has been executed.`

### Error-state behavior
- Do not fall back to production data.
- Do not hide the blocker panel.
- Do not show any launch controls.

## 12. Pagination Behavior
- Default page size: `25`.
- Pagination uses the P40 response envelope.
- The footer shows current page, page size, and total rows.
- Page changes refresh the mock dataset only.
- Pagination never triggers production calls.

## 13. Disabled Actions
The following actions must appear as disabled or unavailable:
- `PRODUCTION_LAUNCH`
- `RUNTIME_PRODUCTION_ENABLEMENT`
- `PRODUCTION_MIGRATION`
- `PRODUCTION_DB_WRITE`
- `HISTORICAL_REGISTRY_MUTATION`
- `HISTORICAL_IDENTITY_REPAIR`

### Disabled-action behavior
- Display the action name.
- Explain why it is disabled in mock-only mode.
- Never wire the action to a production endpoint.

## 14. Non-Production Footer
The footer must state that the page is a mock/spec aid only.

### Required footer copy
- `Mock-only design aid`
- `No production launch signal`
- `Read-only fixture-backed spec`

## 15. Acceptance Notes for Future Frontend Work
- Use the P40 payload as the only data source for this mode.
- Keep the production warning banner visible at all times.
- Keep disabled actions visibly disabled.
- Keep readiness and blocker information readable without opening the drawer.
