# Active Task: Dirty Tree Cleanup Policy / Classification After PR #4 Merge

## 任務名稱

Dirty Tree Cleanup Policy / Classification Plan After PR #4 Merge

## 背景

PR #4 已 merge，local `main` 與 `origin/main` 均同步到 `9a0ddc205b3f6b6cb4499dc214391bd4d886db2d`。P122-P140 governance chain 已進入 `main`，但目前 working tree 仍有大量既有 dirty / untracked files。

使用者已重申 Betting 專案核心目標：

1. 聚焦 MLB 賽事，依台灣運彩可投注市場產生賽前預測策略與 paper-only 投注建議候選。
2. 支援既有預測策略回測、模擬勝敗比分、策略學習，並根據預測成功率調整最佳策略。

在 dirty tree 未分類前，不應啟動 P141 或任何會修改 source / data / runtime 的任務。

## 目標

產出 read-only dirty tree classification report，逐項分類目前 modified / untracked files，並提出 cleanup policy。此任務只做分類與建議，不修改、不刪除、不還原、不 stash、不 stage、不 commit。

## 允許行為

- 讀取 repo 狀態與 git 狀態。
- 讀取 modified / untracked file metadata、路徑、diff、大小與用途線索。
- 產出一份分類報告。
- 必要時讀取 roadmap / active task / handoff / report 檔案做分類依據。

## 允許修改範圍

- `report/dirty_tree_cleanup_policy_20260603.md`

若需要其他輸出檔，必須 STOP 並回報需要修正 scope。

## 禁止行為

- 不得 restore、reset、clean、delete、stash。
- 不得 stage、commit、push、merge、rebase、checkout、建立 branch。
- 不得修改 source code、data、runtime、logs、outputs、reports 以外的新報告檔。
- 不得呼叫 live / paid odds API。
- 不得產生真實投注建議、EV、CLV、Kelly 倉位、stake/profit 或 production readiness 宣稱。
- 不得刪除 release branch。

## Phase 0 Verification

開始前必須確認：

1. `pwd`
2. `git rev-parse --show-toplevel`
3. `git branch --show-current`
4. `git rev-parse --git-dir`
5. `git rev-parse HEAD`
6. `git rev-parse origin/main`
7. `git status --short`
8. 確認目前 repo 是 `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
9. 確認 branch 是 `main`
10. 確認 git-dir 是 `.git`
11. 確認 no staged files；若已有 staged files，STOP

## STOP Conditions

若以下任一成立，立即 STOP：

- repo 不是 canonical repo。
- branch 不是 `main`。
- git-dir 不是 `.git`。
- HEAD 與 `origin/main` 不一致，且任務未授權處理同步。
- 任務開始前已有 staged files。
- 需要修改 `report/dirty_tree_cleanup_policy_20260603.md` 以外的檔案。
- 需要 restore/delete/stash/stage/commit/push/branch 操作。
- 需要讀取 secrets 或 `.env`。
- 需要 live / paid API call。
- dirty files 中出現無法只靠 read-only 分類判斷且會影響安全結論的重大未知變更。

## 分類要求

報告需至少包含下列分類：

- roadmap / governance file
- report / planning artifact
- data output / derived artifact
- runtime / log / cache
- generated test output
- probe / scratch script
- source code candidate
- unknown / requires human decision

每個分類需列：

- path
- git status code
- why classified this way
- risk level: low / medium / high
- recommended action: keep / review / ignore / restore candidate / delete candidate / unknown
- whether safe to stage: yes / no / needs explicit authorization

## 驗收標準

- 報告涵蓋所有 `git status --short` entries。
- 報告清楚分離 runtime/cache/generated 與 roadmap/governance/source/report 類檔案。
- 報告明確標示哪些檔案可安全忽略、哪些需要使用者決策。
- 沒有任何 cleanup action 被實際執行。
- 沒有任何 staged files。
- 沒有任何 branch / commit / push 操作。

## 測試指令

本任務不需要 pytest。測試狀態應標記為 NOT RUN。

建議 verification commands：

- `git status --short`
- `git diff --name-only`
- `git ls-files --others --exclude-standard`
- `git diff --stat`

## 輸出報告位置

`report/dirty_tree_cleanup_policy_20260603.md`

## Required Completion Check

最後回報必須包含：

1. 是否真的完成
2. 測試結果 PASS / FAIL / NOT RUN
3. 仍卡住的唯一問題
4. 修改檔案清單
5. staged / commit / push 狀態
6. 是否允許進入下一輪
7. Final Classification

## Final Classification

預期分類：

`DIRTY_TREE_CLEANUP_POLICY_READY_READ_ONLY`

若任務因 STOP condition 卡住：

`DIRTY_TREE_CLEANUP_POLICY_BLOCKED`
