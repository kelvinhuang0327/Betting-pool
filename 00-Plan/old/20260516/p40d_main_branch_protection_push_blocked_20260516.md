# P40D Main Branch Protection — Direct Push Blocked
**Date:** 2026-05-16  
**paper_only:** True | **production_ready:** False

---

## What Happened

`git push origin main` was executed after a successful local merge (`066b787`) and rejected by GitHub:

```
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: - Required status check "replay-default-validation" is expected.
error: failed to push some refs to 'https://github.com/kelvinhuang0327/Betting-pool.git'
```

**No force push was attempted.** No `--force`, no `--force-with-lease`, no admin override.

---

## Branch Protection Rule

| Field | Value |
|-------|-------|
| Error code | `GH006` |
| Branch | `origin/main` |
| Required status check | `replay-default-validation` |
| Check added by | Commit `e765b3b` (`.github/workflows/replay_default_validation.yml`) |
| Protection enforcement | Mandatory — no bypass without admin action |

The `replay-default-validation` workflow was introduced by `e765b3b` ("chore: publish replay default validation workflow (#1)") — the same commit that local `main` was merging. The workflow defines a required status check that must pass before any ref can be pushed to `origin/main`.

---

## Current State

| Item | Value |
|------|-------|
| Local main HEAD | `51588d6` (41 commits ahead of origin/main) |
| origin/main | `e765b3b` (unchanged) |
| Behind | 0 (divergence resolved locally by `066b787` merge) |
| Merge quality | ✅ Zero conflicts, NO_STRICT_FORBIDDEN |
| origin/main updated | ❌ NO — protected branch blocked push |

---

## Why Force Push Is Not the Answer

- `--force` overrides the protection but violates the repo's safety policy
- Hard rules for this project forbid force push
- Even if permitted: force push skips CI, defeats the purpose of the protection rule
- The CI check `replay-default-validation` exists to validate changes before they land on `main`

---

## Correct Path: PR Workflow

To update `origin/main`, changes must go through a PR that passes CI:

```
1. Create branch: codex/main-sync-20260516 (from local main at 51588d6)
2. Push branch: git push origin codex/main-sync-20260516
3. Open PR: codex/main-sync-20260516 → main (on GitHub)
4. CI runs: replay-default-validation
5. If CI passes → merge PR → origin/main updates
```

This is the intended GitHub workflow for protected branches.

---

## No Action Required From CTO Beyond YES

The local work is clean and ready. The only remaining step is:
1. A PR branch is created and pushed (done in this round)
2. CTO says `YES: open PR for main sync to origin/main`
3. PR is opened, CI runs automatically

---

## Acceptance Marker

`P40D_MAIN_PUSH_BLOCKED_BY_BRANCH_PROTECTION_20260516`
