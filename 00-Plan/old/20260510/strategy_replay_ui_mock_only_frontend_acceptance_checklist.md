# Strategy Replay UI Mock-Only Frontend Acceptance Checklist

Marker: `P41_STRATEGY_REPLAY_UI_MOCK_ONLY_WIREFRAME_SPEC_READY`

## Acceptance Checklist
- [ ] Uses mock payload only
- [ ] No production API calls
- [ ] No production launch button
- [ ] No migration button
- [ ] Warnings visible
- [ ] Disabled actions visible
- [ ] Mock mode label visible
- [ ] Data quality flags visible
- [ ] Readiness blockers visible
- [ ] production UI can start = false
- [ ] runtime production enablement can start = false
- [ ] production migration can start = false

## Required Visual Statements
- `Mock-data/spec-only. Not production UI.`
- `No production migration has been executed.`
- `Historical strategy identity remains blocked unless explicit metadata source is accepted.`
- `Runtime production enablement is blocked.`

## Scope Guard
- This checklist is for future mock-only frontend work.
- Passing this checklist does not authorize production UI.
- Passing this checklist does not authorize runtime production enablement.
- Passing this checklist does not authorize production migration.

## Review Notes
- The page must stay fixture-backed or mock-backed.
- The page must remain read-only.
- The page must remain a design/spec aid, not a launch signal.
