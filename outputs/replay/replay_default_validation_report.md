# Replay Lifecycle Default Validation Report

Generated at: 2026-05-09T12:29:08.508307+00:00
Overall status: **PASS**

## Fixture Results

| Case | Expected | Actual | Validation | Details |
| --- | --- | --- | --- | --- |
| mismatch | BLOCKED | BLOCKED | PASS | upgraded=0; still_pending=1; lookup_by_canonical=0; lookup_by_snapshot_ref=0; reason=no_upgradeable_records |
| aligned | PASS | PASS | PASS | upgraded=1; still_pending=0; lookup_by_canonical=1; lookup_by_snapshot_ref=0 |
| multi-state | PASS | PASS | PASS | upgraded=2; still_pending=0; lookup_by_canonical=1; lookup_by_snapshot_ref=1 |

## Browser Lane

- Status: **SKIP**
- Reason: Playwright Python package is not installed in this environment.
- Detail: Local/browser tooling unavailable; keeping honest SKIP.

## Recommendation

Keep the browser lane optional until CI consistently installs Playwright + Chromium; once the workflow is stable, it can be promoted to required status.
