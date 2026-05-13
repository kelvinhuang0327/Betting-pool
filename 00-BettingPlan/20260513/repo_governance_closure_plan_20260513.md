# Repo Governance Closure Plan — 2026-05-13

**Status:** ACTIVE  
**Author:** CEO/CTO Agent  
**Date:** 2026-05-13  
**Acceptance Marker:** REPO_GOVERNANCE_CLOSURE_PLAN_20260513_READY

---

## 2026-05-13 Repo Governance Correction

### Executive Summary

On 2026-05-13, a critical governance failure was identified: the CTO v4 roadmap
(`betting_roadmap_20260513.md`) was produced in the stale worktree
`/Users/kelvin/Kelvin-WorkSpace/Betting-pool` and was **never tracked in the
canonical repo**. This document formalizes the closure of that governance debt
and establishes the canonical repo policy going forward.

---

## 1. Canonical Repo Definition

| Role              | Path                                                          |
|-------------------|---------------------------------------------------------------|
| **Canonical Repo** | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`            |
| **Stale Repo**     | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`                 |
| **Remote**         | `https://github.com/kelvinhuang0327/Betting-pool.git`        |
| **Active Branch**  | `p13-clean`                                                   |

All new development, roadmaps, reports, and code changes MUST be committed to
`Betting-pool-p13` on branch `p13-clean`.

---

## 2. Stale Repo Policy

The following actions are **PROHIBITED** in `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`:

- ❌ 不得在 stale repo 新增 roadmap / report / code
- ❌ 不得從 stale repo 直接 commit
- ❌ 不得把 untracked roadmap 當作已納管成果
- ❌ 不得以 stale repo 的檔案路徑作為 canonical 參考
- ❌ 不得在 stale repo 執行 `git add` / `git commit` / `git push`

The stale repo may only be used for:
- ✅ READ-ONLY reference (diff comparison, body extraction)
- ✅ Rescue operations (copy body to canonical repo with RESCUED banner)

---

## 3. Rescue Evidence

| Item                          | Status         | Detail                                                        |
|-------------------------------|----------------|---------------------------------------------------------------|
| Rescue file created           | ✅ DONE         | `00-BettingPlan/roadmap/betting_roadmap_20260513_v4_cto_RESCUED.md` |
| Rescue banner present         | ✅ VERIFIED     | Header lines 1-3: RESCUED FROM STALE WORKTREE                |
| Body integrity diff           | ✅ CLEAN        | `RESCUED_V4_DIFF_CLEAN` — no contamination                   |
| Original file in stale repo   | ✅ READ-ONLY    | `/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260513.md` |

Rescue file banner (verified):
```
> ⚠️ RESCUED FROM STALE WORKTREE on 2026-05-13.
> Original location: Betting-pool/main (untracked).
> Superseded by betting_roadmap_20260513_v5_ceo.md.
```

---

## 4. Roadmap Succession Chain

| Version  | File                                              | Status      |
|----------|---------------------------------------------------|-------------|
| v4 (CTO) | `betting_roadmap_20260513_v4_cto_RESCUED.md`      | RESCUED / SUPERSEDED |
| v5 (CEO) | `betting_roadmap_20260513_v5_ceo.md`              | CANONICAL — next generation |

The v5 roadmap is the **authoritative planning document**. All agents must
reference v5 for priority ordering.

---

## 5. P37.6 Handling

Per CEO ruling on 2026-05-13:

- **Old status:** P37.6 Operator Action Packet was named P0 in engineering handoff doc.
- **New status:** P37.6 is **downgraded to a sub-task** of the repo-governance P0.
- **No standalone phase** for P37.6.
- Rationale: The governance failure (lost roadmap in stale worktree) must be
  resolved before any action packet can be reliably communicated.

---

## 6. Priority Ordering (Corrected)

| Priority | Item                                        | Source      |
|----------|---------------------------------------------|-------------|
| P0       | Repo Governance Closure + Canonicalization  | CEO ruling  |
| P0-sub   | P37.6 Operator Action Packet                | Downgraded  |
| P1       | Free-Source Odds Feasibility Spike          | CEO ruling  |
| P2       | P38A Retrosheet Feature Adapter + OOF Rebuild | After P1  |
| P3       | Licensed Odds Approval / Manual Import      | P37.5 path  |

---

## 7. Merge / Push Policy

| Action              | Policy                                                        |
|---------------------|---------------------------------------------------------------|
| `git add`           | Allowed in `Betting-pool-p13` only                           |
| `git commit`        | Allowed in `Betting-pool-p13` only                           |
| `git push`          | Must confirm branch + status + diff scope BEFORE pushing     |
| `git merge`         | Must wait for **explicit YES** from user before executing    |
| `git push --force`  | PROHIBITED without explicit written confirmation             |
| `git reset --hard`  | PROHIBITED without explicit written confirmation             |

---

## 8. Agent Handoff Rules

Any agent picking up this codebase MUST:

1. Verify CWD is `Betting-pool-p13` before any write operation.
2. Run `git branch --show-current` → expected: `p13-clean`.
3. Run `git status --short` → understand untracked files before adding.
4. Check that new files go into appropriate `00-BettingPlan/YYYYMMDD/` directories.
5. Never treat a file in `Betting-pool/` as already committed.
6. Reference roadmap version `v5_ceo` for priority ordering.

---

## 9. Acceptance Criteria

All of the following must be true before declaring TRACK 1 complete:

- [x] `repo_governance_closure_plan_20260513.md` exists in canonical repo
- [x] RESCUED file exists and diff is clean
- [x] Stale repo policy documented
- [x] P37.6 downgrade documented
- [x] v5 roadmap succession referenced
- [x] Merge/push policy documented

**Acceptance Marker:** REPO_GOVERNANCE_CLOSURE_PLAN_20260513_READY
