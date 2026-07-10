# CEO Decision — 2026-07-02（P216–P224 期 / 轉向實質預測工作流）

**Reviewer role**: CEO / Technical Decision Reviewer（CEO Agent Task2.0）
**Canonical repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
**Observed branch**: `task/p224a-pit-contract-leakage-audit` @ `1e1b91e`
**Mode**: `paper_only=true`, `production_ready=false`, `NO_REAL_BET=true`
**Supersedes**: CEO Decision 2026-05-28（P93 era，已標 STALE）。P94–P224 期間無正式 CEO 裁決，本文件補上並校正 roadmap 漂移。
**Final Classification**: `CEO_DECISION_APPROVED`

---

## 1. CEO Review Date

2026-07-02 Asia/Taipei

## 2. Reviewed Inputs

- [Confirmed] 工程交接報告（in-thread，P216→P224 全紀錄）＋ Owner 2026-07-01/02 方向指令。
- [Confirmed] git 實測：branch/HEAD 如上；staged=空；dirty inventory 與已知清單完全一致（無未知變更）；fetch 後 `origin/main`=`59b5aea`。
- [Confirmed] gh 實測：PR #49 OPEN / non-draft / base main / `MERGEABLE` / `BEHIND`；changed files 恰 4 檔 whitelist；CI `replay-default-validation` PASS。PR #46（P219-C guard）mergedAt 2026-07-02T06:29:52Z，僅 +54 行 `tests/test_p219a_historical_feature_baseline_evaluation.py`，與 P224 檔案無交集。
- [Confirmed] `report/p224a_pit_feature_contract_leakage_audit.md`：`NO_DERIVATION_WINDOW_LEAKAGE_DETECTED`、A/B committed=recomputed（0.250000 / 0.312500）、source hash 全 match、18 欄 PIT 分類（pregame_known 僅 3 欄）。
- [Confirmed] `report/mlb_prediction_workflow_snapshot.md`：重訓 / Moneyline paper / 2026 快照 / 市場覆蓋數字（見 §3）。
- [Confirmed] 本輪 read-only smoke：`test_mlb_product_workflow_snapshot` + `test_p224a_*` = **6 passed**。
- [Confirmed] roadmap.md（§0T, 2026-06-14）、CTO-Analysis.md（2026-06-14）、active_task.md（P204）＝全部過時 2.5 週。
- [Unknown] worktree 中另有多個 codex/claude detached worktree 的用途；不影響本裁決。

## 3. Work Value Assessment

**實質成熟度提升：**
- [Confirmed] MLB「重訓→預測→Moneyline 紙上下注→結果回填」工作流第一次端到端跑通：2025 test 972 場、best Brier `calibrated_elo_recent_form` 0.2460、best acc `retrained_team_history_smooth` 56.38%；paper 398 注 hit 51.26% / ROI +4.70%；2026 本地快照 828 筆、已附結果 acc 56.93%。這是核心目標①③的第一段可看結果，也是 Owner 要求的方向。
- [Confirmed] P224-A 是實質稽核（重算 metrics、零 delta、16/16 row match），非純文件。
- [Confirmed] P216–P223 chain：流程 / 證據價值為主，邊際價值遞減；fixture 僅 24 rows / 16 eval rows，屬 pitch-event 級流程骨架，不是 game-level 預測能力證據。

**表面性進度 / 缺口：**
- governance 三檔漂移 2.5 週（本次已校正）。
- [Confirmed] workflow snapshot 8 檔 untracked、未經 PR review —— 最大交付風險。
- paper ROI +4.70%（398 注）統計上不足以宣稱真實 edge；odds 來源為賽後單快照。
- [Confirmed] P224-A post-merge smoke NOT RUN（PR 未合）；full-repo regression NOT RUN。

## 4. CTO Judgment Review

**判定：部分採納（PARTIALLY ADOPTED）**
- 採納：PR #49 merge closeout 為第一優先（正確、Owner 授權文字已在串內、風險低）；claim boundary / 授權不繼承 / whitelist 紀律全數保留。
- 調整：handoff 隱含「繼續 artifact-only audit 鏈（P225+）」→ 降級為 on-demand；Owner 指令明確要實質預測結果。
- 調整：Fable5「model training NO-GO」限縮為 live transport / real betting / production activation / 新遠端資料來源；本機 historical paper-only 重訓由 Owner 指令解鎖（否則與 Owner 明示目標矛盾，且 P207A 與 workflow snapshot 已是既成事實）。
- 補漏：handoff 未預見 main 移動（PR #46 今晨合併致 PR #49 `BEHIND`）→ 已把 BEHIND 處理程序寫進 active_task.md。

## 5. Roadmap Gap Assessment

- [Confirmed] roadmap 停在 §0T（P203/P204），漏記 P205–P223 全部合併、P224 PR #49、workflow snapshot、Owner 方向指令 → 已以 §0U 校正（最小增量，保留歷史）。
- [Confirmed] active_task.md 停在 P204 plan-only（其目標已被 P205A 實作吸收）→ 已替換為 PR #49 merge closeout。
- [Confirmed] 缺 blocker 紀錄：workflow 檔案 untracked → 已列 P0-2。
- CTO-Analysis.md 同樣過時，但非 CEO 可寫檔案 → 留待下次 CTO 輪更新（記錄於此，不阻塞）。

## 6. CEO Priority Decision

- **P0-1**：PR #49 merge closeout + post-merge smoke（已授權，today）。
- **P0-2**：workflow snapshot 8 檔入版控（新 branch + PR）——`WAITING_FOR_USER_AUTHORIZATION`。
- **P1-1**：Run line / Total 機率模型 + paper 回測——`WAITING_FOR_USER_AUTHORIZATION`。
- **P1-2**：PIT-safe（pregame_known only）真實先發 / 近況特徵強化。
- **P2**：F5 資料缺口盤點；external historical closing odds 評估；model-heavy 前 full-repo regression。
- **P3–P10**：P225+ artifact-only 鏈（on-demand）；P219 residual（PR #46 guard 監控）；live / betting / production / Track B（STOP / HOLD / deferred）。

**Upgraded**：workflow 入版控（新列 P0-2）、run line / total 模型（P1-1）。
**Downgraded**：artifact-only 鏈擴充（P3+ on-demand）。
**Retired**：P204 provenance inventory（被 P205A 吸收）。
**Paused（不變）**：Track B、live transport、F5（待資料）。

## 7. Roadmap Changes Applied

- `roadmap.md`：header meta 更新（review date / observed branch / status / active marker）＋ 新增 §0U（現況真相、Fable5 界線調和、P0–P10、Today Focus）。§0T 以下全部保留為歷史。未重寫全檔。
- `active_task.md`：整檔替換為 P224-A PR #49 merge closeout（含 BEHIND 應變、更新後 dirty inventory、queued next）。
- `CEO-Decision.md`：本檔（整檔替換，前版已自標 STALE）。
- 未動 `CTO-Analysis.md`、source、data、runtime、bootstrap 檔。

## 8. Today Focus Direction

1. **PR #49 merge closeout**（phase P224；採納 CTO）— main 取得 PIT contract / leakage audit 主線證據。驗收：`P224A_MERGED_POST_MERGE_SMOKE_PASS`（merge commit + SHA256 + determinism diff 空 + P224/P223/P221/P219A tests PASS + `git diff --check` PASS + dirty inventory 前後一致）。風險：BEHIND 需 update-branch 時多一次 CI 等待。
2. **Workflow snapshot 入版控（P0-2）**（CEO 新增）— 消除 untracked 遺失風險、讓實質成果可 review 可重跑。驗收：新 branch + PR + CI green + 8 檔 SHA 記錄 + targeted tests PASS。等 Owner 授權。
3. **Run line / Total 機率模型（P1-1）**（採納 Owner 指令）— 台灣運彩主要市場不只停在 Moneyline。驗收：新增 report 含 per-market Brier / acc / paper ROI 表、防洩漏 time-split、paper-only 標示。等 Owner 授權。

## 9. Risks / Blind Spots

- [Confirmed] workflow snapshot 8 檔 untracked＝最高交付風險（遺失 / 誤 staging）。
- [Confirmed] 2026 快照預測版本標示 `p84b_diagnostic_baseline_v1`（診斷基線，非重訓最佳模型）→ P0-2 review 時必須釐清版本語意，避免「最佳模型在跑」的誤讀。
- [Confirmed] paper ROI 樣本不足以宣稱 edge；odds 為賽後單快照，禁止當賽前市場 / CLV 使用。
- [Confirmed] P219 nondeterminism root cause 未 isolate（residual；PR #46 guard test 監控）。
- [Inferred] 多 agent 並行下 main 可能再移動；active_task 已要求 worker fetch 後重驗 whitelist 無交集。
- [Unknown] PR #49 merge 是否受 up-to-date branch protection 阻擋（active_task 已定義唯一允許的 update-branch 程序）。

## 10. CEO Final Decision

核准：P0-1 立即執行（Owner merge 授權文字已在 2026-07-02 串內；worker 執行串需自帶）。P0-2 / P1-1 列隊，各需 Owner 一句話授權。artifact-only 鏈降級 on-demand。live / real betting / production / 新遠端資料維持 STOP / HOLD。本裁決未 stage / commit / push 任何檔案。

**Final Classification**: `CEO_DECISION_APPROVED`

## 11. CEO Summary（≤10 行）

1. [Confirmed] P205–P223 全部已進 main；main 今晨再收 PR #46 guard（`59b5aea`）。
2. [Confirmed] PR #49 OPEN / MERGEABLE / CI PASS / 4 檔 whitelist 正確，唯 `BEHIND`。
3. [Confirmed] P224-A 結論 `NO_DERIVATION_WINDOW_LEAKAGE_DETECTED`，重算零 delta。
4. [Confirmed] 實質工作流已跑通且數字已驗：Brier 0.2460 / acc 56.38% / paper ROI +4.70% / 2026 acc 56.93%。
5. [CEO] 部分採納 CTO：先合 PR #49；artifact-only 鏈降級；主線轉向預測實質工作。
6. [CEO] Fable5 NO-GO 限縮至 live / production / real-money；本機 paper 重訓解鎖。
7. [CEO] P0-2 workflow 入版控、P1-1 run line / total 模型，皆等 Owner 一句話授權。
8. [Risk] workflow 8 檔 untracked 是當前最大遺失風險。
9. [Boundary] paper-only / no live / no real bet / no production 不變。
10. 三檔已更新；未 stage / commit / push。
