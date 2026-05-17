# P40D Main Behind-Origin Review
**Date:** 2026-05-16  
**paper_only:** True | **production_ready:** False

---

## The Divergence Problem

Local `main` and `origin/main` have **diverged** from a common ancestor:

```
034f772  (merge-base — last shared commit)
    │
    ├── origin/main path: e765b3b  "chore: publish replay default validation workflow (#1)"
    │
    └── local main path:  [38 orchestrator commits] → 10a08a1
```

A `git push origin main` will be **rejected** because `e765b3b` exists on `origin/main` but not on local `main`. Git treats this as a non-fast-forward situation.

**`--force` push is FORBIDDEN** by hard rules.

---

## The Origin-Only Commit

| Field | Value |
|-------|-------|
| SHA | `e765b3b` |
| Message | `chore: publish replay default validation workflow (#1)` |
| Files | 9 files, 966 insertions |
| Author | GitHub PR merge |
| Content | `.github/workflows/replay_default_validation.yml` + replay validation scripts and reports |

### Files in `e765b3b`

| File | Type |
|------|------|
| `.github/workflows/replay_default_validation.yml` | CI workflow |
| `outputs/replay/replay_default_validation_ci_rerun_inspector_report.md` | Report |
| `outputs/replay/replay_default_validation_ci_verification_report.json` | Report |
| `outputs/replay/replay_default_validation_ci_verification_report.md` | Report |
| `outputs/replay/replay_default_validation_pr_readiness_audit.md` | Report |
| `outputs/replay/replay_default_validation_report.html` | Report |
| `outputs/replay/replay_default_validation_report.json` | Report |
| `outputs/replay/replay_default_validation_report.md` | Report |
| `scripts/run_replay_default_validation.py` | Script (560 lines) |

This commit is a legitimate PR merge (GitHub PR #1). It added the replay default validation CI/CD pipeline. It does NOT conflict with the orchestrator work in local `main`.

---

## Resolution Options

### Option A — Merge `origin/main` into local `main` (Recommended)

Integrate the 1 remote commit into local history via a merge commit.

```bash
git fetch origin
git merge origin/main --no-ff -m "Merge origin/main: integrate replay validation workflow"
# Resolve any conflicts (unlikely — disjoint files)
git push origin main
```

**Result:** Local `main` includes all 38 orchestrator commits + `e765b3b` + 1 new merge commit → total 40 commits on `origin/main`.

**Pros:** Preserves full history. No rebasing. Explicit merge record.  
**Cons:** Adds a merge commit. History is slightly non-linear.  
**Conflict risk:** LOW — `e765b3b` touches `.github/`, `outputs/replay/`, `scripts/run_replay_default_validation.py`. Local `main` orchestrator work is in `orchestrator/`, `wbc_backend/`, etc. Minimal overlap expected.  
**Signal required:** `YES: push main to origin`

### Option B — Rebase local `main` onto `origin/main`

Rebase all 38 orchestrator commits on top of `e765b3b`.

```bash
git rebase origin/main
git push origin main
```

**Result:** Clean linear history. All 38 commits replayed after `e765b3b`.  
**Pros:** Cleanest history.  
**Cons:** Rewrites 38 commit SHAs — any branches derived from local `main` (including `codex/consolidate-p13-clean-20260516`) would need to be rebased too. High operational risk.  
**Signal required:** `YES: push main to origin` + explicit CTO approval for rebase

### Option C — Push `--force` (FORBIDDEN)

`git push --force origin main`

**FORBIDDEN** by hard rules. Not an option.

### Option D — Leave As-Is (Current State)

Keep local `main` diverged. Branch is available on GitHub without a PR. Consolidation branch is on remote.

**Pros:** Zero risk. No action needed.  
**Cons:** PR will always show a messy 41-commit diff until resolved.

---

## Recommendation

**Option A (merge `origin/main` → local `main` → push)** is the safest path:

1. `git fetch origin` (already done)
2. `git merge origin/main --no-ff` — merge the 1-commit replay workflow into local main
3. Check conflicts (expected: none)
4. `git push origin main` — fast-forward on remote

The merge commit will integrate `e765b3b` cleanly. After push, `origin/main` = local `main` = all 38 orchestrator commits + replay workflow commit.

**After main sync, PR from consolidation branch will show only 3 clean commits.**

---

## Does This Block Main Push?

| Factor | Block? |
|--------|--------|
| Diverged history (non-fast-forward) | ⚠️ YES — blocks direct push; solvable via merge (Option A) |
| Forbidden files in 38 commits | ✅ NO — forbidden audit passed |
| Origin-only commit (`e765b3b`) content | ✅ NO conflict expected |
| CTO decision required | ✅ YES — explicit YES needed |

---

## CTO Decision Required

To proceed, CTO must send:

```
YES: push main to origin
```

Agent will then:
1. Run `git merge origin/main --no-ff`
2. Verify no conflicts
3. Run final forbidden scan on merged state
4. `git push origin main`
5. Verify `git rev-parse origin/main` equals new local `main`

---

## Acceptance Marker

`P40D_MAIN_BEHIND_ORIGIN_REVIEW_COMPLETE_20260516`
