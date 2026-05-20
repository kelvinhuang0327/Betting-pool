# Replay Default Validation Required-Check Proposal

## Proposal Summary

`replay_default_validation` is now a credible candidate for a GitHub required check.

Evidence exists at three levels:

- PR/head validation passed before merge, including the browser lane in CI.
- Post-merge main observation round 1 passed on the merge commit.
- Post-merge main observation round 2 passed again on the same merge commit via manual `workflow_dispatch`.

This report proposes the check for governance review only. It does not change branch protection or required-check settings.

## Why This Is a Candidate Required Check

The workflow has now proven the following:

- It is visible and runnable on the branch and on `main`.
- It completes successfully in GitHub Actions on the merged commit.
- The browser lane is a true CI `PASS`, not a local-only `SKIP`.
- The same result repeated across two separate `main` observations, one push-triggered and one manual dispatch.

That combination is enough to treat the workflow as operationally stable and worthy of required-check consideration.

## Evidence Table

| Phase | Run ID | Trigger | Commit SHA | Status | Conclusion | Browser lane | Overall |
|---|---:|---|---|---|---|---|---|
| PR / head | `25601421342` | `pull_request` | `5edb650333bde9c8ced74b43b039549694a02afd` | `completed` | `success` | `PASS` in CI | `PASS` |
| Main round 1 | `25601450048` | `push` | `e765b3bfe2279643942440731b9b8835b29c591d` | `completed` | `success` | `PASS` in CI | `PASS` |
| Main round 2 | `25601589741` | `workflow_dispatch` | `e765b3bfe2279643942440731b9b8835b29c591d` | `completed` | `success` | `PASS` in CI | `PASS` |

## Expected GitHub Required Check Name

The required status check name expected to appear in branch protection is:

- `replay-default-validation`

This is the workflow/job name surfaced in GitHub Actions and in the PR check rollup.

## Risks of Making It Required Too Early

- A future runner, dependency, or browser-install regression could temporarily block merges if the check is required too soon.
- The workflow is currently validated on only two main-branch observations; that is strong, but not exhaustive.
- The workflow includes Playwright browser installation, so external runner or browser package changes could create intermittent false failures.
- If required-check policy is enabled before the team is comfortable with the noise profile, merges could be slowed by incidental infrastructure issues rather than replay logic problems.

## Rollback Plan

If enabling the required check causes false blocking, the rollback should be governance-only and reversible:

1. Temporarily remove `replay-default-validation` from the required checks list.
2. Re-run the workflow on `main` to confirm whether the failure is transient or persistent.
3. Inspect only the failing CI step logs and correct the smallest tooling or path issue if needed.
4. Re-add the required check only after the workflow is green again on `main`.

This plan avoids changing replay semantics and keeps the recovery surface limited to workflow governance and CI tooling.

## Recommended Governance Decision

The evidence is strong enough to propose the check for governance review now.

However, enactment should remain separate from proposal. A conservative posture is to prepare the required-check change request, but wait for explicit approval before updating branch protection.

## Proposal vs Enactment

- Proposal status: ready
- Enactment status: not authorized in this round
- Branch protection: unchanged
