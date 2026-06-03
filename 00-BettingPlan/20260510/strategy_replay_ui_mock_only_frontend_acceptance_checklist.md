# Strategy Replay UI — Mock-Only Frontend Acceptance Checklist

## Status

**Mock-data/spec-only. Not production UI.**

This checklist confirms the mock-only UI spec package meets all acceptance criteria.

## Warnings

- Mock-data/spec-only. Not production UI.
- No production migration has been executed.
- Historical strategy identity remains blocked unless explicit metadata source is accepted.
- Runtime production enablement is blocked.

## Checklist

### Production Gate

- [ ] No production launch button
- [ ] No migration button
- [ ] production UI can start = false
- [ ] runtime production enablement can start = false
- [ ] production migration can start = false

### Mock Data Integrity

- [ ] All rows sourced from fixture/mock data only
- [ ] No production API call is allowed
- [ ] All `production_ready` flags in rows are `false`
- [ ] All `ui_mode` values in rows are `mock` or absent

### Component Presence

- [ ] StrategyReplayMockPage rendered
- [ ] ProductionBlockedBanner visible and non-dismissible
- [ ] ReplayReadinessPanel shows MOCK_DATA_ONLY
- [ ] ReplayFilterPanel read-only
- [ ] ReplayMockTable shows mock rows
- [ ] ReplayQualityBadge present per row
- [ ] ReplayDetailDrawer opens without production action buttons
- [ ] ReplayDisabledActionNotice replaces production action buttons
- [ ] ReplayPagination functional on mock data
- [ ] ReplayEmptyState shown when no rows match
- [ ] ReplayErrorState shown on mock load failure

## Acceptance Result

All production controls are absent. Mock-only UI spec is not production UI.
This spec may proceed to design review. No frontend implementation was created here.
