# Betting-pool Roadmap v6 — Single Repo Consolidation + MLB Betting Product Plan

> **Superseded notice — 2026-05-15 CTO update:** Use `00-BettingPlan/roadmap/betting_roadmap_20260515_mlb_product_plan.md` as the current active roadmap. The 2026-05-14 version remains valid for single-repo governance, but v7 reorders execution around the two product goals: MLB betting recommendations and strategy simulation optimization.

**Date:** 2026-05-14  
**Owner:** CTO agent  
**Current user directive:** Long-term canonical workspace must be `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`; do not create additional Betting-pool repos. Consolidate useful code back into `Betting-pool`, then retire extra worktrees/folders only after verification.  
**Supersedes:** `betting_roadmap_20260513.md`, `betting_roadmap_20260513_v4_cto_RESCUED.md`, `betting_roadmap_20260513_v5_ceo.md`, and any document that defines `Betting-pool-p13` as the long-term canonical repo.  
**Current implementation source branch/worktree:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`, latest inspected commit `5775588 docs(betting): finalize P1.5 research odds fixture-only review`.  
**Operating mode:** `PAPER_ONLY=true`, `production_ready=false`.

---

## 1. CTO Decision

The previous p13 governance decision solved an immediate stale-worktree problem, but it conflicts with the user's current repo-management requirement. The new CTO decision is:

> **`Betting-pool` becomes the single canonical local repo. `Betting-pool-p13` is a temporary source worktree/branch to merge back. `Betting-pool-preserve-2026-05-11` and `Betting-pool-publication` are candidates for retirement only after diff verification and user-approved deletion.**

The product focus remains unchanged:

1. **MLB game prediction to Taiwan Sports Lottery recommendation**  
   Moneyline PAPER pipeline exists; next value is multi-season reliability and TSL market expansion.

2. **Strategy simulation optimization**  
   Strategy policy must be optimized by replay/simulation evidence before recommendations are trusted.

---

## 2. Workspace Inventory

| Path | Role after this roadmap | Observed state | Action |
|---|---|---|---|
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | **Target canonical repo** | `main`, ahead 38 / behind 1, dirty worktree with many existing data/report changes | Clean/stabilize enough to merge p13; do not create new repo. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13` | Temporary source worktree | git worktree on `p13-clean`; 34 commits ahead of `main`; latest P1.5 commit `5775588` | Merge/cherry-pick back into `Betting-pool`, then remove worktree after verification. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-preserve-2026-05-11` | Preservation snapshot | no `.git`; 225 MB | Keep read-only until merge verification; delete only after user approval. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-publication` | Publication worktree | git worktree branch `p1/replay-default-validation-publication`; small legacy/publication subset | Diff against main and p13; retire if no unique code remains. |

Deletion rule: **do not delete any directory until the merge-back validation report says `RETIREMENT_READY` and the user explicitly approves deletion.**

---

## 3. Current Product Implementation Status

### Axis A — MLB prediction to TSL-style betting recommendations

| Capability | Status | Evidence |
|---|---:|---|
| 2025 moneyline OOF model | PAPER ready | P13 walk-forward logistic, OOF BSS positive but thin. |
| Historical odds-aware simulation | PAPER ready | P15 joined 1,575 / 1,577 rows. |
| Risk-aware recommendation gate | PAPER ready | P16.6 produced 324 eligible rows with P18 policy. |
| Settlement and daily paper summary | PAPER ready | P19/P17 replay settled 171 W / 153 L; P20 ready with 0 unsettled. |
| Multi-day backfill | PAPER ready but sparse | P21 ready; missing dates explicit. |
| Stability certification | Blocked | P28: 324 active < 1,500; P29 best relaxed policy = 563. |
| 2024 game identity/outcome spine | Partial | P32 processed game logs exist in p13 branch; raw logs remain uncommitted/guarded. |
| 2024 OOF prediction source | Blocked | P33/P35: no verified prediction source; adapter missing. |
| 2024 real odds source | Blocked | P37.5 and P1.5 conclude no real-data local join certification. |
| TSL multi-market coverage | Not built | Moneyline only; HDC/OU/F5/odd-even/team total need schema and labels. |

### Axis B — strategy simulation optimization

| Capability | Status | Evidence |
|---|---:|---|
| Basic strategy simulation | Ready | P14/P15. |
| Risk repair / policy search | Ready on 2025 sample | P18 searched 400 candidates; selected conservative capped Kelly. |
| Ledger P/L | Ready on 2025 sample | P17 replay after P19 identity repair. |
| Expanded sample optimization | Blocked | Requires 2024 joined prediction + odds/proxy data. |
| Real CLV validation | Deferred | Requires licensed/live snapshots; not available. |

---

## 4. P1.5 Research Odds Review Status

P1.5 is now closed as **fixture-only**, not real-data ready.

| Item | Result |
|---|---|
| Commit in source worktree | `5775588 docs(betting): finalize P1.5 research odds fixture-only review` |
| Marker set | `RESEARCH_ODDS_MANUAL_REVIEW_AUDIT_20260513_READY`, `FIXTURE_ONLY_SMOKE_ALLOWED_20260513`, `FIXTURE_ONLY_DATA_STRUCTURE_READY_20260513`, `FIXTURE_ONLY_JOIN_SMOKE_READY`, `RESEARCH_ODDS_P15_LICENSE_JOIN_UPDATE_20260513_READY` |
| Raw guard | No staged `data/research_odds/*.csv`; no local-only raw data committed |
| Real data join certification | **Not achieved** |
| Current classification | `FIXTURE_ONLY_JOIN_SMOKE_READY` |

Conclusion: P1.5 validates structure only. It does **not** unblock model edge claims, real odds replay, or production readiness.

---

## 5. Roadmap Alignment Gaps

1. **Old p13/v5 roadmap conflicts with repo governance**  
   It says `Betting-pool-p13` is canonical. The user now requires `Betting-pool` as the single canonical repo. This roadmap supersedes that.

2. **P37.5/P1.5 are governance blockers, not product milestones**  
   They protect licensing and data provenance, but do not improve prediction quality or strategy evidence by themselves.

3. **P38A was correctly identified but still not implemented**  
   The most useful engineering task remains the 2024 Retrosheet pregame-safe adapter + OOF rebuild.

4. **The system is still moneyline-only**  
   This does not fully satisfy the user goal of recommendations across Taiwan Sports Lottery betting items.

5. **Sample wall is still the central model/strategy blocker**  
   324 active entries cannot support a credible production proposal. Multi-season joined input remains mandatory.

---

## 6. Reordered P0-P10

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | **Single Repo Consolidation Gate** | Repo governance | Merge p13 code/docs/tests back into `/Betting-pool`; stop using extra Betting-pool worktrees as canonical. | p13 branch merged/cherry-picked or equivalent diff applied to `Betting-pool`; no raw/local-only data included; tests smoke pass; retirement list produced. |
| **P1** | **Dirty Worktree Triage for Betting-pool main** | Repo governance | Separate existing main dirty changes into keep/ignore/review buckets before merge. | `git status` categorized; no user data lost; merge can proceed without overwriting unrelated edits. |
| **P2** | **P38A Runtime: 2024 Retrosheet Feature Adapter + OOF Rebuild** | Prediction | Build pregame-safe 2024 features and OOF probabilities. | `p_oof` for 2024 rows, leakage audit, Brier/ECE/BSS, deterministic tests. |
| **P3** | **Research Odds Real-Data Procurement Decision** | Data | Decide Kaggle purchase/manual download vs no real-data path; AusSportsBetting remains blocked unless ToS confirmed. | Either approved local-only real-data sample exists, or blocker remains explicit. |
| **P4** | **2024 Joined Input Certification** | Prediction + data | Join 2024 OOF predictions with licensed/research odds or explicitly certify fixture-only blocker. | Join coverage and provenance report; no look-ahead fields; no fake real-data readiness. |
| **P5** | **Multi-Season True-Date Replay** | Strategy | Run 2024+2025 replay once joined input exists. | Active entries target >= 1,500 or honest blocker; identity-settled ledger. |
| **P6** | **Strategy Optimization v2** | Strategy | Re-run policy grid on expanded sample. | Drawdown, Sharpe, bootstrap CI, exposure, turnover, and hit rate all reported. |
| **P7** | **Recommendation Gate v2 + Ledger Closure** | Product | Issue moneyline paper recommendations from v2 model/policy. | Recommendation rows carry risk profile; ledger closes with 0 unsettled where outcomes exist. |
| **P8** | **TSL Market Taxonomy + Schema Pack** | Product | Add formal support for HDC, OU, F5, odd/even, team total schemas. | Market contracts, labels, odds fields, and blocked-state semantics committed. |
| **P9** | **Run Line + Totals PAPER Prototype** | Product | First non-moneyline paper prototypes. | HDC/OU paper-only models/simulators with no-lookahead validation. |
| **P10** | **Production Proposal Gate** | Governance | Only after paper + source + risk evidence. | Human approval, licensed/live odds path, rollback/no-bet fail-safe, multi-day monitoring. |

---

## 7. Immediate Execution Plan

### Next 24 hours

1. **Produce merge-back manifest from p13 to Betting-pool**  
   Use `git diff --name-status main..p13-clean` and classify:
   - code/tests/scripts: merge candidate
   - docs/reports: merge candidate
   - processed research artifacts: review candidate
   - raw/local-only/output/runtime/db: reject

2. **Triage main dirty worktree**  
   Current `Betting-pool/main` has many modified data/report files and deletions. Do not merge over it blindly.

3. **Create a merge dry-run branch in the existing repo only**  
   Branch name should be under existing repo, e.g. `codex/consolidate-p13-into-main`. This is a branch, not a new repo.

### Next 72 hours

1. Apply/cherry-pick p13 commits into the consolidation branch.
2. Run smoke tests for P13-P21 and P31-P37/P1.5 scopes.
3. Confirm no raw odds, `outputs/`, `runtime/`, DB, or local-only files enter tracked diff.
4. Produce `RETIREMENT_READY` / `RETIREMENT_BLOCKED` report for `p13`, `preserve`, and `publication`.

### Next 7 days

1. Finish P38A runtime implementation in `Betting-pool`.
2. Decide real-data odds procurement path.
3. Certify 2024 joined input if odds source clears.
4. Re-run multi-season replay and strategy optimization.

---

## 8. Stop Rules

- Do not delete `Betting-pool-p13`, `Betting-pool-preserve-2026-05-11`, or `Betting-pool-publication` until after merge-back validation and explicit user approval.
- Do not create another `Betting-pool*` directory.
- Do not claim `JOIN_CERT_RESEARCH_ODDS_READY`; P1.5 is fixture-only.
- Do not commit raw odds, `data/research_odds/local_only/`, `data/mlb_2024/raw/`, `outputs/`, `runtime/`, or DB files.
- Do not touch live betting or production writes.

---

## 9. Marker

`CTO_BETTING_ROADMAP_V6_SINGLE_REPO_CONSOLIDATION_20260514_READY`
