# Active Task: P224-A PR #49 Merge Closeout With Post-Merge Smoke

## Status

`AUTHORIZED_IN_CEO_THREAD_20260702_PENDING_EXECUTION`

Owner 的明確 merge 授權文字（"I explicitly authorize P224-A PR #49 merge closeout only"）
已出現在 2026-07-02 CEO 審查串。依「授權不跨任務繼承」規則，worker 執行串必須自帶
同等授權文字；缺授權 → STOP。

## Supersedes

取代 P204-PREDICTION-PROVENANCE-HARDENING（2026-06-14，plan-only）。該任務目標已被
P205-A provenance fail-closed 實作（已 merge）吸收，standalone inventory 不再是優先。

## Background（2026-07-02 CEO 實測）

- `origin/main` = `59b5aea`：PR #46（P219-C markdown determinism guard，mergedAt
  2026-07-02T06:29:52Z）在 PR #48（P223-A）之後合併，僅 +54 行
  `tests/test_p219a_historical_feature_baseline_evaluation.py`。
- P216–P223 historical artifact chain 已全部在 main。
- PR #49（P224-A）：OPEN、非 draft、target main、head `1e1b91e`、`MERGEABLE`、
  CI `replay-default-validation` PASS；因 PR #46 後合而 `BEHIND`
  （4 behind / 1 ahead，與 main 新 commit 無檔案交集）。
- P224-A 結論：`NO_DERIVATION_WINDOW_LEAKAGE_DETECTED`；Baseline A/B
  committed=recomputed（0.250000 / 0.312500）；16/16 row-level match。
- `git worktree list`：無任何 worktree 佔用 `main`，主目錄 `git checkout main` 可行。

## Goal

把 PR #49 合併進 main、完成 post-merge smoke、記錄 merge commit 與 P224 artifact
SHA256。不做任何其他變更。

## Allowed Changes

- GitHub 標準方式 merge PR #49。
- 若且唯若 GitHub 因 branch-out-of-date 規則拒絕 merge：允許執行一次 GitHub
  「Update branch」（merge main into PR branch），等 CI 綠後再 merge。此為唯一允許的
  額外 commit；不得 rebase / force-push。
- 本地 `git checkout main` + `git pull --ff-only origin main`（僅同步）。
- 重跑 P224 builder 覆寫 `report/p224a_*.{json,md}`（determinism 驗證；應與 committed
  版本 bit-identical，若有 diff → STOP 報告，不得 commit）。
- `/tmp` 或 scratchpad 下的 SHA 記錄檔。

## Forbidden Changes

- 不得建立 repair commit、不得 revert、不得 push 其他 commit。
- 不得動 P216–P223 artifacts、依賴檔（requirements / pyproject / CI config）。
- 不得動 unrelated dirty/untracked files，已知清單（staging 亦禁止）：
  - `00-Plan/roadmap/roadmap.md`、`CEO-Decision.md`、`active_task.md`（2026-07-02 CEO 已改，未 commit）
  - `00-Plan/roadmap/SHARED_AGENT_BOOTSTRAP.md`、`TASK_TEMPLATES.md`、`agent_bootstrap/`（untracked）
  - `report/mlb_prediction_workflow_*`（4 檔）、`scripts/run_mlb_prediction_workflow_snapshot.py`、
    `tests/test_mlb_product_workflow_snapshot.py`、`wbc_backend/recommendation/mlb_product_workflow_snapshot.py`
  - `report/p199_*`、`report/p202*`（untracked 歷史 audit）
  - `data/`、`logs/`、`runtime/` 下所有 dirty 檔
- 不得 remote data fetch（git/gh 操作除外）、不得 pybaseball、不得 model training、
  不得產 future predictions、不得 DB writes。
- 不得繼續 P225 / model / prediction 工作（需另行 Owner 授權）。

## Phase 0 Verification

1. `cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool`
2. 確認執行串內含 Owner merge 授權文字。
3. `git fetch origin --prune`；記錄 `origin/main` SHA（預期 `59b5aea` 或其後；若 main
   又移動，重驗 PR #49 changed files 仍恰為 4 檔且與新 commit 無檔案交集，否則 STOP）。
4. `gh pr view 49 --json state,isDraft,mergeable,mergeStateStatus,headRefOid`：
   OPEN、非 draft、`MERGEABLE`、head `1e1b91e`（或 update-branch 後的新 head）。
5. `gh pr view 49 --json files`：恰為 4 檔 —
   `scripts/build_pit_feature_contract_leakage_audit.py`、
   `tests/test_p224a_pit_feature_contract_leakage_audit.py`、
   `report/p224a_pit_feature_contract_leakage_audit.json`、
   `report/p224a_pit_feature_contract_leakage_audit.md`。
6. `gh pr checks 49` 全 pass。
7. `git status --short` 記錄 dirty inventory（預期＝Forbidden 清單所列；出現未知項 → STOP）。
8. `git diff --cached --name-status` 必須為空。

## STOP Conditions

- 執行串內無 Owner 授權文字。
- PR checks 非全綠；changed files ≠ 4 檔 whitelist；與 main 新 commit 有檔案交集。
- Update-branch 之後 CI 未綠。
- merge / smoke 會觸及 unrelated dirty/untracked files。
- post-merge smoke 任一步 FAIL（記錄證據後 STOP；不得自行 repair）。

## Post-Merge Smoke（Test Commands）

1. `git checkout main && git pull --ff-only origin main`；記錄 merge commit hash；
   確認 local main == origin/main。
2. `export PYTHONPATH="$PWD"; python3 scripts/build_pit_feature_contract_leakage_audit.py`
3. `shasum -a 256 report/p224a_pit_feature_contract_leakage_audit.json report/p224a_pit_feature_contract_leakage_audit.md > /tmp/p224a_sha_run1.txt`
4. 重跑 builder → `/tmp/p224a_sha_run2.txt`；`diff -u /tmp/p224a_sha_run1.txt /tmp/p224a_sha_run2.txt` 必須為空。
5. `git diff -- report/p224a_pit_feature_contract_leakage_audit.json report/p224a_pit_feature_contract_leakage_audit.md` 必須為空（rebuild 與 committed bit-identical）。
6. `.venv/bin/python -m pytest -q tests/test_p224a_pit_feature_contract_leakage_audit.py tests/test_p223a_historical_evaluation_evidence_index.py tests/test_p221a_historical_time_split_baseline_evaluation.py tests/test_p219a_historical_feature_baseline_evaluation.py`
7. `git diff --check`
8. 確認無依賴 diff、無 P216–P223 artifact diff。
9. `git status --short`（dirty inventory 與 Phase 0 記錄一致）。

## Acceptance Criteria

- PR #49 merged；local main == origin/main；merge commit hash 記錄。
- P224 JSON/MD SHA256 記錄；two-run determinism diff 空；rebuild 與 committed bit-identical。
- P224 / P223 / P221 / P219A tests PASS；`git diff --check` PASS。
- 無依賴變更、無 P216–P223 artifact 修改、無 unrelated files 觸及。
- 無 remote data fetch（git/gh 除外）、無 pybaseball、無 model training、
  無 future predictions、無 DB writes。
- 未繼續 P225 / model / prediction 工作。

## Evidence / Report Output Location

- 回報於任務串本文：merge commit、artifact SHA256、test 輸出、git status 前後對照、
  final classification。不新增 repo 檔案。

## Required Completion Check

1. Completed: yes/no
2. Tests: PASS / FAIL / NOT RUN
3. Only remaining blocker
4. Modified files
5. staged / commit / push status
6. Allowed to proceed next: yes/no
7. Final Classification

## Final Classification

- 成功：`P224A_MERGED_POST_MERGE_SMOKE_PASS`
- 失敗 / 中止：`P224A_MERGE_BLOCKED`（附證據）

## Queued Next（不在本任務範圍；各需 Owner 一句話授權）

1. **P225-W**：MLB prediction workflow snapshot 8 檔入版控（新 branch + PR + CI +
   review；含釐清 2026 快照版本標示 `p84b_diagnostic_baseline_v1` 的語意）。
2. **P226**：Run line / Total 機率模型 + paper 回測（per-market Brier / acc / ROI 報告，
   防洩漏 time-split，paper-only 標示）。
