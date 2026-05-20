# Betting-pool Roadmap v7 — Single Repo + MLB Recommendation / Simulation Plan

> **Superseded notice — 2026-05-16 CTO update:** Use `00-BettingPlan/roadmap/betting_roadmap_20260516_p39j_odds_consolidation.md` as the current active roadmap. v7 remains useful for the two product axes, but v8 reflects P38A completion, P39J remote push, the Statcast batting feature freeze, and the P3 odds input gate.

**Date:** 2026-05-15  
**Owner:** CTO agent  
**Current directive:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` is the single canonical repo target. Do not create additional `Betting-pool*` repos. Use `Betting-pool-p13` only as a temporary source worktree until its useful commits are merged back and verified.  
**Supersedes:** `betting_roadmap_20260514_single_repo_consolidation.md`, `betting_roadmap_20260513.md`, and older roadmaps where they conflict.  
**Operating mode:** `PAPER_ONLY=true`, `production_ready=false`, `NO_REAL_BET=true`.  
**Active marker:** `CTO_BETTING_ROADMAP_V7_MLB_PRODUCT_PLAN_20260515_READY`

---

## 1. CTO Decision

The roadmap must now be organized around the user's two product goals:

1. **MLB game prediction -> Taiwan Sports Lottery style betting recommendation**  
   Produce auditable pregame recommendation rows by market type. Current evidence supports paper-only moneyline flow; TSL market breadth is not complete.

2. **Strategy simulation optimization**  
   Optimize model/recommendation policy through replay and simulation evidence before any recommendation is trusted.

The next phase should not spend more time on generic roadmap churn. The highest-value move is to stabilize the single repo, then push the system toward a multi-season, auditable MLB paper recommendation loop.

---

## 2. Roadmap Alignment Assessment

| Source / report | Still valid | Gap / adjustment |
|---|---|---|
| 2026-05-04 long-term MLB roadmap | Long-term MLB direction, governance, calibration, scheduler, and `production_ready=false` discipline remain valid. | It is too broad for the current blocker. It predates the single-repo consolidation requirement and P1/P1.5 odds license findings. |
| 2026-05-13 P37.5 / odds approval report | Correctly blocks production odds import until licensed approval files exist. | It solved safe manual provisioning, not actual source acquisition. It does not unlock P38 by itself. |
| P1 research odds feasibility report `7ab0123` | Candidate inventory, license matrix, import contract, join skeleton are useful. | It is stale relative to P1.5. P1.5 concluded fixture-only, not real-data ready. |
| P1.5 fixture-only review `5775588` | Current truth for community/free odds: no real-data join readiness; fixture-only smoke allowed. | Must be merged back into `Betting-pool`; do not treat p13 as canonical. |
| 2026-05-14 single repo roadmap | Correct governance decision: `Betting-pool` is canonical and p13 is merge-back source. | Needs stronger product sequencing for MLB recommendations and strategy optimization. |

CTO conclusion: **v6 governance is correct but incomplete. v7 keeps single-repo consolidation as P0 and reorders the product work around MLB recommendations + simulation optimization.**

---

## 3. Current System Status

### 3.1 Repo / governance status

| Item | Status | CTO call |
|---|---|---|
| Canonical target | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | Keep as single canonical repo. |
| Source worktree | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean` | Temporary merge source only. |
| p13 latest useful evidence | `5775588 docs(betting): finalize P1.5 research odds fixture-only review` | Must be merged/cherry-picked back before p13 can be retired. |
| Main target state | `main...origin/main [ahead 38, behind 1]`, large dirty/untracked state | Blind merge is unsafe. Need triage branch inside existing repo. |
| Extra folders | `Betting-pool-preserve-2026-05-11`, `Betting-pool-publication` | Keep until retirement report and explicit user approval. |

### 3.2 Product axis A — MLB prediction -> betting recommendation

| Capability | Status | Evidence / blocker |
|---|---|---|
| MLB moneyline paper model | Partially ready | Multiple MLB model/probability scripts and tests exist in target tree, but many are dirty/untracked in `Betting-pool`. |
| Historical odds-aware simulation | Paper-ready on 2025 sample | P15 reports 1,575 / 1,577 odds join coverage and paper-only simulation. |
| Paper recommendation gate | Paper-ready on 2025 sample | P16/P18/P19/P20 family exists, but must be verified after merge-back. |
| Real / licensed 2024 odds | Blocked | P37.5 missing filled approval record and approved CSV; P1.5 says fixture-only. |
| 2024 OOF prediction source | Blocked / not implemented in canonical target | P38A remains the most important runtime blocker. |
| TSL market coverage | Incomplete | Moneyline exists; HDC, OU, F5, odd/even, team total require schema, labels, and validation. |
| Production recommendation | Not allowed | `production_ready=false`; no live betting; no model edge claim. |

### 3.3 Product axis B — strategy simulation optimization

| Capability | Status | Evidence / blocker |
|---|---|---|
| Simulation spine | Exists | `wbc_backend/simulation/*` and P14/P15 evidence. |
| Odds-aware strategy policy | Paper-ready but thin | P18/P19/P20 indicate risk repair and paper ledger, but active sample is too small. |
| Multi-season optimization | Blocked | Requires 2024 OOF predictions and licensed/research odds join. |
| CLV / live market validation | Deferred | Requires approved/live odds source and aligned snapshots. |
| Policy confidence | Not production-grade | Sample wall remains the dominant blocker. |

---

## 4. Key Blockers

1. **Repo blocker:** useful p13 work is not yet consolidated into `Betting-pool`; extra repos/worktrees create management risk.
2. **Dirty worktree blocker:** `Betting-pool/main` has large existing modified/untracked state, so merge-back must be controlled.
3. **Data license blocker:** no public odds source is approved for real local-only research ingestion; P1.5 is fixture-only.
4. **Production odds blocker:** P37.5 approval package exists, but real filled approval files do not.
5. **2024 prediction blocker:** no certified 2024 OOF prediction artifact exists in the canonical target.
6. **Sample-size blocker:** 2025-only paper entries are too thin for production proposal.
7. **Market breadth blocker:** current evidence is moneyline-first; Taiwan Sports Lottery market items are not fully modeled.
8. **Naming/architecture blocker:** `wbc_backend` remains historical naming while product target is MLB; rename is not needed now, but docs and adapters must prevent confusion.

---

## 5. Reordered P0-P10

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | Single Repo Consolidation Gate | Governance | Merge/cherry-pick useful p13 commits into `/Betting-pool` without creating another repo. | p13 P0-P1.5 docs/code/tests represented in `Betting-pool`; no raw/local-only/runtime/output/DB files; merge-back validation report complete. |
| **P1** | Dirty Worktree Triage | Governance | Categorize current `Betting-pool` dirty/untracked files before consolidation. | Keep / ignore / review buckets produced; unrelated user changes protected; no destructive cleanup. |
| **P2** | P38A 2024 OOF Prediction Rebuild | Prediction | Build Retrosheet/pregame-safe 2024 feature adapter and OOF probability artifact. | 2024 `p_model` rows produced with leakage audit, Brier/ECE/BSS, deterministic tests. |
| **P3** | Licensed / Research Odds Decision Gate | Data | Decide paid/manual licensed odds route vs fixture-only blocker; do not force public data. | Either approved local-only sample exists, or blocker remains explicit; no raw odds committed. |
| **P4** | 2024 Joined Input Certification | Prediction + data | Join 2024 OOF predictions with approved odds source or certify honest blocker. | Coverage report, unmatched/duplicate report, no look-ahead fields, provenance hash. |
| **P5** | Multi-Season True-Date Replay | Strategy | Run 2024+2025 paper replay with settled outcomes. | Active entries target >= 1,500 or honest blocker; ledger settlement quality report. |
| **P6** | Strategy Optimization v2 | Strategy | Re-run policy grid on expanded multi-season sample. | Edge threshold, Kelly cap, stake cap, drawdown, Sharpe, bootstrap CI, exposure, turnover reported. |
| **P7** | Recommendation Gate v2 | Product | Produce auditable moneyline paper recommendation rows from v2 policy. | Recommendation rows include market, selection, odds, p_model, p_market, edge, stake, risk reason, `paper_only=true`. |
| **P8** | TSL Market Taxonomy + Schema | Product | Define Taiwan Sports Lottery betting item contracts for HDC, OU, F5, odd/even, team total. | Market schemas, labels, odds fields, blocked-state semantics, fixture tests. |
| **P9** | Non-Moneyline Paper Prototypes | Product | Build first HDC/OU/F5/team-total paper-only models and simulators. | No-lookahead validation, sample coverage, separate market-specific gates. |
| **P10** | Production Proposal Gate | Governance | Only after multi-season paper evidence and licensed/live data path. | Human approval, live odds source, rollback/no-bet fail-safe, monitoring plan, `production_ready` review. |

Most worth optimizing next: **P0/P1 repository consolidation first, then P2/P4 multi-season evidence generation.** Without that, every model or market expansion result remains hard to trust and hard to maintain.

---

## 6. Practical Execution Plan

### Next 24 hours

1. Run controlled dirty-state inventory in `Betting-pool`.
2. Produce exact p13 commit/file merge list from `482c52e` through `5775588`.
3. Create an in-repo branch only, for example `codex/consolidate-p13-into-main`.
4. Cherry-pick or patch-apply p13 docs/code/tests while excluding forbidden paths.
5. Confirm P1/P1.5 markers exist in `Betting-pool`.

### Next 72 hours

1. Run targeted P13-P21 and P31-P37/P1.5 smoke tests where dependencies allow.
2. Produce `single_repo_retirement_readiness_20260515.md`.
3. Start P38A runtime work only after consolidation branch is stable.
4. Prepare odds decision packet: paid/licensed source, manual import path, or fixture-only blocker.

### Next 7 days

1. Complete P38A 2024 OOF prediction rebuild.
2. Certify or block 2024 joined input.
3. Run multi-season replay.
4. Re-run strategy policy optimization.
5. Start TSL market taxonomy pack, with non-moneyline prototypes kept paper-only.

---

## 7. Stop Rules

- Do not create another `Betting-pool*` repo.
- Do not delete `Betting-pool-p13`, `Betting-pool-preserve-2026-05-11`, or `Betting-pool-publication` until after validation and explicit user approval.
- Do not use `git reset --hard`, `git clean`, destructive checkout, or blind merge against current dirty `Betting-pool`.
- Do not commit raw odds, local-only odds, `outputs/`, `runtime/`, DB, `.db-wal`, `.db-shm`, or unapproved manual import files.
- Do not claim `JOIN_CERT_RESEARCH_ODDS_READY`; P1.5 is fixture-only.
- Do not claim model edge, production readiness, live TSL integration, or real betting readiness.

---

## 8. Next Task Prompt

```text
請作為 Betting-pool Single Repo Consolidation + MLB Product CTO Agent，
只使用 /Users/kelvin/Kelvin-WorkSpace/Betting-pool 作為目標 repo，
並只把 /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13 作為 temporary source worktree。

任務：
1. 在既有 Betting-pool repo 內建立 consolidation branch，不新增 repo。
2. 對 Betting-pool/main 的 dirty/untracked 狀態產出 keep/ignore/review 分類。
3. 盤點 p13-clean 從 P0 到 5775588 的可併回檔案。
4. 禁止納入 raw odds、local_only、outputs、runtime、DB、manual filled approval。
5. 將 P1/P1.5 docs、fixtures policy、P31-P37/P38A 前置 docs/code/tests 納入 dry-run branch。
6. 跑 targeted smoke tests；若依賴不足，明確標記 TESTS_BLOCKED_DEPENDENCY。
7. 產出 single_repo_retirement_readiness_20260515.md，結論只能是 RETIREMENT_READY 或 RETIREMENT_BLOCKED。

Final classification:
- SINGLE_REPO_CONSOLIDATION_DRY_RUN_READY
- SINGLE_REPO_CONSOLIDATION_BLOCKED_DIRTY_WORKTREE
- SINGLE_REPO_CONSOLIDATION_BLOCKED_TESTS
- DOCS_ONLY_ROADMAP_UPDATED
```

---

## 9. CTO 10-Line Summary

```text
1. Betting-pool is the only canonical repo target; no new repo is allowed.
2. Betting-pool-p13 is a temporary source worktree, not the long-term canonical repo.
3. P1 odds feasibility is superseded by P1.5 fixture-only status.
4. No real public odds source is approved for local research ingestion.
5. P37.5 approval package exists, but real approved odds files are still missing.
6. MLB moneyline paper flow exists, but sample size is too thin for production claims.
7. Strategy optimization is blocked by the same multi-season joined-input gap.
8. TSL market coverage is incomplete beyond moneyline.
9. The best next move is repo consolidation, then P38A 2024 OOF rebuild.
10. production_ready remains false; no live betting, no edge claim.
```

---

`CTO_BETTING_ROADMAP_V7_MLB_PRODUCT_PLAN_20260515_READY`
