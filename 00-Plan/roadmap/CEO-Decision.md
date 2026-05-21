# CEO Decision — P26G 後置二次審查與今日方向裁決

## 1. CEO Review Date

2026-05-21 Asia/Taipei

備註：
- [Confirmed] 環境日期為 2026-05-21。
- [Confirmed] 本輪 CEO 審查在 CTO 提交 P26G-to-P26H roadmap 更新後執行。
- [Confirmed] 昨日 (2026-05-20) CEO-Decision 為 `CEO_DECISION_PARTIALLY_APPROVED` (P23 reconciliation focus)，本日覆寫為 P26 系列現狀。

## 2. Reviewed Inputs

- [Confirmed] `00-Plan/roadmap/roadmap.md` (CTO 更新版，2026-05-21)
- [Confirmed] `00-Plan/roadmap/CTO-Analysis.md` (CTO 更新版，2026-05-21)
- [Confirmed] `data/paper_recommendations/p26g_coverage_recheck_post_p26f_20260521.json`
- [Confirmed] `report/p26g_coverage_recheck_post_p26f_20260521.md`
- [Confirmed] `00-BettingPlan/20260521/p26g_coverage_recheck_post_p26f_20260521.md`
- [Confirmed] `git log --oneline -8`：HEAD = `8a98f52 fix(p26f): force-save closing snapshots through dedup bypass`
- [Confirmed] `git status --short`：30+ dirty files，包含 raw feed (`tsl_odds_history.jsonl`) 與 runtime state
- [Confirmed] 用戶交接報告 + 兩大主軸補充 (MLB paper recommendation + 預測策略優化驗證)

未執行：
- [Confirmed] 本輪未 rerun pytest。
- [Confirmed] 本輪未修改 CTO-Analysis.md 與 roadmap.md。
- [Confirmed] 本輪未 commit 任何檔案。

## 3. Yesterday Work Value Assessment

| 項目 | 評估 | 標記 |
|---|---|---|
| P26F commit `8a98f52` (force_closing dedup bypass) | code-level 修復完成，runtime 已生效 | [Confirmed] 實質推進 |
| Daemon restart (PID 1715 → 15022) | 新 code 已載入；Cycle #1 完成 | [Confirmed] 必要動作但本身無系統成熟度提升 |
| `force_closing_snapshot=True` rows = 10 | 證明 P26F 機制 runtime 可寫入 | [Confirmed] 機制驗證型推進 |
| `dedup_bypassed=True` rows = 7 (交接寫 2，以 repo artifact 為準) | dedup bypass 實際發生 | [Confirmed] 但交接與 artifact 數字不一致為輕度治理風險 |
| 1 個 closing window snapshot 寫入 (gap=-0.53h) | 但缺對應 pregame | [Confirmed] 機制可用但未形成 pair |
| COMPLETE_PAIR 仍為 220，delta = 0 | **未推進 CLV 樣本** | [Confirmed] 核心 KPI 未動 |
| P25C bootstrap 正確 NOT RUN | 治理紀律維持 | [Confirmed] |
| P26G artifacts 已產出 (JSON/MD/BettingPlan) | 但 **untracked**，無 commit hash | [Risk] 交付未閉環 |
| Phase 8 full validation / forbidden scan | 交接未貼出結果 | [Unknown] |
| P26G artifact 自帶 `next_closing_candidates` (3469930.1, 3469931.1) 預計今日 +2 pair | 內建自動預測，CTO 未提及 | [Confirmed] 被低估的事實 |
| `data/tsl_odds_history.jsonl` 現為 2892 行 (P22 時為 2785) | daemon live feed 正常成長 | [Confirmed] 不可 commit |

結論：昨日成果屬「機制驗證型推進」(P26F runtime confirmed)，**未達**「CLV 樣本成熟度推進」(COMPLETE_PAIR 未變)。同時引入兩項 P0 級閉環項：(a) P26G artifact commit 未完成；(b) Phase 8 validation 結果未確認。

## 4. CTO Judgment Review

完全採納項：
- [Confirmed] P0 = P26G delivery closure + P26H pair formation monitor
- [Confirmed] P25C bootstrap 必須 >= 300 COMPLETE_PAIR 才啟動
- [Confirmed] 不重啟 daemon、不改 scheduler、不修 dedup、不手動補 snapshots
- [Confirmed] 不 stage raw feed (`tsl_odds_history.jsonl`) 與 runtime state 檔
- [Confirmed] champion `fixed_edge_5pct` 保留、promotion frozen、production proposal frozen

部分採納 / 修正項：
- [Inferred] CTO 將 P29/P30A model quality 完全降到 P6，**CEO 改為 P5**：CLV coverage 累積屬於數據自然累積問題，模型品質工作可在不依賴 CLV 樣本的軌道上並行（不衝突），但不可搶 P0/P1 資源。
- [Inferred] CTO P7「TSL Market Recommendation Contract」(主軸一) 排太後，**CEO 上拉至 P4**：用戶最後一段補充明確強調「先完成正式資料 CLV validation，再決定 paper recommendation pipeline 強化」，paper recommendation contract 設計可在 CLV 等待期間並行設計（不釋出投注）。
- [Risk] CTO 沒有指出 P26G artifact 內建 `next_closing_candidates` 與 `expected_new_pairs_today=2`。CEO 要求今日 P26H 必須驗證這兩個自動預測是否成真，作為機制是否真正工作的 ground truth。
- [Risk] CTO 接受了交接的 `dedup_bypassed=2`，但 repo artifact 顯示 = 7，CEO 要求 active_task 必須使用 repo artifact 為單一事實源並調和差異。

不採納項：
- 無。CTO 整體方向正確，僅優先序與 scope 細節需 CEO 補強。

最終判定：**CEO_DECISION_PARTIALLY_APPROVED**

## 5. Roadmap Gap Assessment

| Gap | 處理方式 |
|---|---|
| CTO 將兩大主軸隱含對齊但未顯式標註 | CEO P0-P10 表格內每行加註對齊「主軸一/主軸二/兩者皆是/治理」 |
| CTO 未指出 dedup_bypassed 交接/artifact 數字不一致 | active_task 強制使用 repo artifact 為單一事實源 |
| CTO 未要求驗證 `expected_new_pairs_today=2` | active_task 加入「next_closing_candidates pair 形成驗證」 |
| P26G dirty worktree 風險 (30+ 個 daemon/runtime/data dirty files) | active_task 強制 commit scope 白名單，禁止 stage raw feed |
| P29/P30A 過度降級 | CEO 上拉到 P5 (並行但不搶 P0/P1 資源) |
| Paper recommendation pipeline (主軸一) 過度降級 | CEO 上拉到 P4 (設計併行，無 release) |
| Phase 8 validation 結果在 P26G 缺失 | active_task 強制 rerun 並記錄實測值 |

## 6. CEO Priority Decision

| Priority | Phase | Track | Done condition | 對齊主軸 |
|---:|---|---|---|---|
| **P0** | P26G Delivery Closure + P26H Pair Formation Monitor | Data QA + Governance | P26G artifacts staged & committed (raw feed 排除)；force_closing rows 全部 match-level 分類；COMPLETE_PAIR before/after 記錄；`expected_new_pairs_today=2` ground-truth 驗證；Phase 8 targeted tests rerun | 主軸二前置 |
| **P1** | Missing-Pregame Root Cause Diagnostic | Data QA | 對每個 force_closing row 標註 missing_pregame / missing_closing / complete / ambiguous；分類「自然晚掛盤 vs pregame capture gap vs matching rule bug」 | 主軸二前置 |
| **P2** | Closing Cadence Impact Estimate (diagnostic-only) | Ops | 15-min vs 5-min expected coverage lift 估算；**不**修改 daemon interval 直到 CEO 明確授權 | 主軸二前置 |
| **P3** | P25C Bootstrap Gate (auto-trigger 預備) | Validation | COMPLETE_PAIR >=300 自動觸發條件文件化；當前 NOT RUN 因 220<300 | 主軸二 |
| **P4** | MLB → 台彩 Paper Recommendation 證據契約 (設計併行) | Product | moneyline / 不讓分 / 讓分 / 大小分 / 單雙 / 局數市場契約設計；**僅契約，無釋出**；每筆 paper_only=true | 主軸一 |
| **P5** | P29/P30A Real Orchestrator `w_market` Validation (並行非搶占) | Prediction | 在 P0/P1 完成且未消耗 P0/P1 資源的情況下推進；diagnostic-only | 主軸二 |
| **P6** | TSL CLV Data SSOT | Data governance | raw feed (`tsl_odds_history.jsonl`)、daemon state、artifact 三者嚴格分離 | 治理 |
| **P7** | P26 Runtime Validation Hygiene | QA | targeted tests + forbidden scan 結果均記錄為實測值 (非沿用報告) | 治理 |
| **P8** | Daily Paper Ops / Drift Monitor | Ops | COMPLETE_PAIR、force_closing rows、missing_pregame、Brier、ECE 每日追蹤 | 兩者皆是 |
| **P9** | Repo / PR Governance Gate | Engineering governance | canonical branch = main；不新增 repo/worktree/branch 除非 `YES: create...` | 治理 |
| **P10** | Production Proposal Gate | Governance | 永久 blocked，直到多季 evidence + live licensed data + fail-safe + monitoring + CEO 批准 | 治理 |

## 7. Today Focus Direction

**唯一執行方向**：**P0 — P26G Delivery Closure + P26H Pair Formation Monitor** (合一任務)

- 對應 phase：P0
- 重要性：
  1. P26G artifacts 已產出但 untracked，交付未閉環會讓下一輪 agent 重複驗證。
  2. P26F runtime 已 confirm，但 row-level 成功不等於 pair-level 成功；CLV 樣本是否真的會自然累積必須觀測。
  3. P26G JSON 自帶 `expected_new_pairs_today=2`，這是系統自動預測，必須驗證為 ground truth 或修正預測邏輯。
- 系統成熟度推進：
  1. row → match 級別的 observability 升級
  2. P26G artifact 治理閉環，避免重複工作
  3. 證實或否定「自然累積 2-7 天可達 300」的工程假設
- 預期收益：
  1. COMPLETE_PAIR 增長軌跡可被預測 (產出 burn-down curve)
  2. 若 expected_new_pairs_today 真的成真，可建立每日自動驗證模板
  3. 若失敗，可定位 pregame capture gap 真因
- 風險：
  1. 純監測動作，無模型/收益改變；不做才是更大風險。
  2. dirty worktree 中可能誤 stage raw feed → 必須 commit scope 白名單。
- 驗收標準：見 active_task.md。
- 是否採納 CTO：採納並加強（補上 next_candidates 驗證 + commit scope 白名單 + 兩大主軸對齊註記）。

## 8. Risks / Blind Spots

- [Risk] P26G 自宣告「2-7 days 可達 300」是工程估算，未經驗證；若 force_closing 連續 N 日仍無法形成 pair，需重新檢視 pregame capture 完整性。
- [Risk] dirty worktree 30+ 個 daemon/runtime/data 檔；commit scope 一定要用白名單，禁止 `git add .`。
- [Risk] 交接報告 `dedup_bypassed=2` vs repo artifact = 7 數字不一致，可能代表 user 觀測 timing 與 artifact 寫入 timing 不同；active_task 必須以 artifact 為單一事實源。
- [Risk] Phase 8 validation 結果在 P26G 缺失，若今日不 rerun，未來無法回溯。
- [Unknown] missing_pregame 真因：自然晚掛盤 / pregame capture gap / matching rule bug，三者 incident response 不同。
- [Risk] 15-min interval 估算屬 P2，若提前進入會搶 P0/P1 資源。
- [Risk] 兩大主軸 (MLB paper rec + 策略優化) 易被治理工作遮蔽；CEO 顯式保留 P4/P5 並行軌道但禁止搶 P0/P1。
- [Confirmed] `production_ready=false`，promotion / champion replacement / production proposal / live API / TSL crawler modification / profitability claim 全部 frozen。
- [Confirmed] 不啟動 P25C bootstrap (220 < 300)。
- [Risk] 若今日 P26H 顯示 expected_new_pairs_today 為 0 而非 2，代表 P26G 自我預測 broken，需即刻補一個 diagnostic 而非進入下一輪 P26I。

## 9. CEO Final Decision

**CEO_DECISION_PARTIALLY_APPROVED**

- 採納 CTO P0/P1/P2/P3 排序與 promotion / production / champion replacement 全面 freeze。
- 修正 P4/P5 對齊兩大主軸 (主軸一 paper rec 契約設計併行；主軸二 model quality 可並行但不搶 P0/P1)。
- 今日唯一執行方向 = P26G Delivery Closure + P26H Pair Formation Monitor（合一任務）。
- 強制 commit scope 白名單，禁止 stage raw feed (`tsl_odds_history.jsonl`)、daemon state、runtime output。
- 強制以 repo artifact 為 dedup_bypassed 等數字的單一事實源（artifact > 交接報告）。
- 強制驗證 `expected_new_pairs_today=2` ground truth。
- 明令禁止：optimizer promotion、champion replacement、production proposal、live odds API、TSL crawler modification、profitability claim、daemon restart、scheduler change、PR merge (除非顯式批准)、手動補造 snapshots、新增 repo/worktree/branch。
- `paper_only=true` 為所有產出強制 invariant。

## 10. 10 行內 CEO 摘要

1. P26F 已 commit (`8a98f52`)，runtime 確認生效。
2. force_closing rows = 10、dedup_bypassed = 7 (以 repo artifact 為準，非交接 2)。
3. COMPLETE_PAIR 仍為 220，delta = 0，P25C bootstrap 正確 NOT RUN。
4. P26G artifacts 已產出但 **未 commit**，交付未閉環。
5. P26G 自宣告今日預計 +2 pair (3469930.1, 3469931.1)，必須驗證。
6. 採納 CTO P0 = P26G closure + P26H pair monitor；P1 = missing-pregame diagnostic。
7. 修正：P29/P30A 上拉到 P5、主軸一 paper rec 契約設計上拉到 P4 (並行但不搶 P0/P1)。
8. 今日唯一任務：P26H Pair Formation Monitor + P26G Commit Closure。
9. 強制 commit 白名單；raw feed / daemon state / runtime output 禁止 stage。
10. Final classification = `CEO_DECISION_PARTIALLY_APPROVED`。
