# P40D PR #2 CI Gate + MLB Roadmap Realignment Report

**Date:** 2026-05-18  
**Owner:** CTO agent  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Branch observed:** `codex/main-sync-20260516`  
**Mode:** `PAPER_ONLY=true`, `NO_REAL_BET=true`, `production_ready=false`  
**Final classification:** `WAITING_FOR_USER_YES_GATE_PR2` + `DOCS_ROADMAP_UPDATED` + `ODDS_INPUT_NOT_READY`

---

## 1. 本輪目標

本輪不是新增模型或下注功能，而是做 CTO daily review：

1. 檢查 PR #2 main sync gate 與 CI 狀態。
2. 對齊目前 repo governance、roadmap、MLB prediction、TSL recommendation、strategy simulation 實作進度。
3. 重新排序下一階段 P0-P10，讓工作回到兩大主軸：MLB 賽事預測投注建議、策略模擬優化。
4. 直接更新 active roadmap，不新增 repo、不繞過 branch protection、不做 production write。

---

## 2. 已完成事項

| 項目 | 結果 |
|---|---|
| PR #2 狀態 | `OPEN`, `MERGEABLE`, `CLEAN` |
| Required CI | `replay-default-validation` 已 PASS |
| CI run | `actions/runs/25991240145`, job `76397636132` |
| Merge gate | 未 merge，因尚未收到 `YES: merge PR #2` |
| `origin/main` | 尚未更新，仍需 PR #2 merge 後才同步 |
| Roadmap | 已更新 active v8 roadmap，加入 2026-05-18 CTO execution update |
| New repo/worktree | 無新增 |
| Odds input check | `THE_ODDS_API_KEY` 不存在；`data/research_odds/local_only/` 不存在 |

---

## 3. 修改或產出的檔案

| 檔案 | 用途 |
|---|---|
| `00-BettingPlan/roadmap/betting_roadmap_20260516_p39j_odds_consolidation.md` | 更新 active roadmap，加入 v8.1 PR2 gate + MLB execution plan |
| `00-BettingPlan/20260518/p40d_pr2_ci_gate_and_mlb_roadmap_realignment_20260518.md` | 本輪 daily CTO 交接報告 |

---

## 4. 驗證結果 / 測試結果

### 4.1 GitHub PR / CI

```text
gh pr checks 2
replay-default-validation    pass    1m2s
```

```text
gh pr view 2
state=OPEN
mergeable=MERGEABLE
mergeStateStatus=CLEAN
head=codex/main-sync-20260516
base=main
headRefOid=16cd40ed6767231369c8a2fd9f02385779c39fb4
baseRefOid=e765b3bfe2279643942440731b9b8835b29c591d
```

### 4.2 Product / data readiness

| Check | Result | CTO interpretation |
|---|---|---|
| `.env` `THE_ODDS_API_KEY` | `KEY_NOT_FOUND_IN_ENV` | P3 odds API path blocked |
| `data/research_odds/local_only/*.csv` | `LOCAL_ONLY_DIR_NOT_FOUND` | P3 manual local-only path blocked |
| MLB decision quality report | `UNAVAILABLE_SINGLE_SNAPSHOT`, 1,493 rows | Benchmark only, not CLV evidence |
| Optimization report | 1,734 strict games; Platt Brier 0.2463 / ECE 0.0269; ROI sweeps negative | Calibration helps probability quality, but betting policy not profitable yet |
| TSL schema implementation | Not found as standalone module | Product market taxonomy is underbuilt |

---

## 5. 目前結論

PR #2 is ready from CI perspective but not authorized from governance perspective.

The next engineering action is not another model experiment. The correct order is:

1. Wait for explicit `YES: merge PR #2`.
2. Merge PR #2 through GitHub PR workflow.
3. Verify `origin/main`.
4. Re-check consolidation PR diff cleanliness.
5. In parallel after governance clears, implement TSL market taxonomy because it does not depend on odds data.

---

## 6. 尚未完成事項

| Item | Status | Required signal |
|---|---|---|
| PR #2 merge | Waiting | `YES: merge PR #2` |
| Consolidation PR | Deferred | PR #2 merged and `origin/main` verified |
| P3 odds unblock | Blocked | `KEY_READY` or `DATA_READY` |
| TSL market schema | Not implemented | Code + tests in canonical repo |
| Strategy optimization v2 | Blocked | Joined odds + prediction + settled result input |
| Production proposal | Not allowed | Multi-season evidence, live/licensed data, human approval |

---

## 7. 風險與不確定點

| Risk | Level | Note |
|---|---:|---|
| PR #2 not merged | Medium | CI passed, but `origin/main` remains stale until user approval |
| Dirty worktree | High | Large existing modified/untracked state; no destructive cleanup allowed |
| Consolidation PR diff pollution | Medium | Must re-check after PR #2 merge |
| Odds source absent | High | Blocks CLV, EV, Kelly realism, and strategy replay |
| TSL product scope under-modeled | Medium | README lists markets, but standalone schema/contract module is missing |
| Negative ROI sweeps | Medium | Probability calibration is improving, but policy selection still loses in historical test |

---

## 8. 建議今天優先處理方向

### P0 — PR #2 Merge Gate

Only after explicit authorization:

```text
YES: merge PR #2
```

Then execute:

```bash
gh pr merge 2 --merge
git fetch origin
git rev-parse origin/main
gh pr view 2 --json state,mergeCommit,url
```

### P1 — Consolidation PR Readiness

After PR #2 merge, re-check:

```bash
gh pr create --base main --head codex/consolidate-p13-clean-20260516
```

Only proceed if diff is clean and does not include main-sync commits.

### P2 — TSL Market Taxonomy

Implement the missing product contract:

```text
wbc_backend/markets/tsl_market_schema.py
tests/test_tsl_market_schema.py
```

Scope v1: all market definitions exist, but only moneyline is `is_paper_implemented=True`.

### P3 — Odds Input

Wait for one of:

```text
KEY_READY: The Odds API key is in .env as THE_ODDS_API_KEY
DATA_READY: I dropped a CSV to data/research_odds/local_only/
```

---

## 9. 下一輪可直接執行的 task prompt

```text
請作為 Senior Betting CTO / P40D PR #2 Merge Gate Agent，
在 /Users/kelvin/Kelvin-WorkSpace/Betting-pool 執行下一輪任務。

最高原則：
- 不新增 repo / worktree
- 不 force push
- 不 bypass branch protection
- 不 commit .env / API key / raw odds / local_only CSV
- 不做 production write
- 不做 live betting
- 只有收到 explicit YES: merge PR #2 才能 merge

TRACK 0 — Preflight:
git status --short
git branch --show-current
git fetch origin
gh pr view 2 --json number,url,state,headRefName,baseRefName,mergeable,mergeStateStatus,statusCheckRollup
gh pr checks 2

TRACK 1 — Merge gate:
若 CI pass 但沒有 YES: merge PR #2:
- 不 merge
- final classification = WAITING_FOR_USER_YES_GATE_PR2

若收到 YES: merge PR #2 且 CI pass:
gh pr merge 2 --merge

TRACK 2 — Post-merge verification:
git fetch origin
git rev-parse origin/main
gh pr view 2 --json state,mergeCommit,url
git log origin/main -1 --oneline

TRACK 3 — Consolidation readiness:
檢查 codex/consolidate-p13-clean-20260516 對 main 的 diff 是否乾淨。
產出 post-merge readiness report。

Final classification:
- WAITING_FOR_USER_YES_GATE_PR2
- PR2_MERGED_AND_POST_VERIFY_PASS
- PR2_CI_FAILED_REQUIRES_FIX
- BLOCKED_REPO_STATE_UNCLEAR
```

---

## 10. CTO Agent 10 行內摘要

```text
1. PR #2 CI 已 PASS，mergeStateStatus=CLEAN。
2. 尚未收到 YES: merge PR #2，所以沒有 merge。
3. origin/main 仍未更新，consolidation PR 必須繼續等待。
4. active roadmap 已更新為 2026-05-18 execution view。
5. 下一階段 P0 是 PR #2 merge gate，不是新模型。
6. P1 是 post-merge consolidation PR readiness。
7. P2 應提前做 TSL market taxonomy，因為它不依賴 odds。
8. P3 odds 仍 blocked：無 THE_ODDS_API_KEY，無 local_only CSV。
9. Strategy simulation v2 需要 odds join 後才能實質優化。
10. production_ready=false；no live betting；no edge claim。
```

`P40D_PR2_CI_PASS_WAITING_USER_MERGE_YES_ROADMAP_UPDATED_20260518`
