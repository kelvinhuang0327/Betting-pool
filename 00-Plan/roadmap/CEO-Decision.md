# CEO Decision — Context Hygiene Clean + 回到 P26K 二次審查與今日方向裁決

## PROJECT_CONTEXT_LOCK

```text
Project          = Betting-pool
Canonical Repo   = /Users/kelvin/Kelvin-WorkSpace/Betting-pool
Canonical Branch = main
Cross-Project Rule:
  若任何任務、檔案、commit 或 roadmap 屬於其他專案 (Stock-Prediction-System / P48 / P49 /
  golden fixture / paper simulation dry-run / Lottery)：
    STOP immediately
    Do NOT summarize as current project work
    Do NOT create artifacts for it
```

## 1. CEO Review Date

2026-05-23 Asia/Taipei

備註：
- [Confirmed] CTO 採用 2026-05-23 作為本輪 review date；CEO 沿用以保持一致。
- [Confirmed] 本輪 CEO 審查在 CTO 提交 Context Hygiene Clean roadmap 更新 (0D 章節) 後執行。
- [Confirmed] 前一輪 CEO-Decision (P26J 後置 PM session, 2026-05-21) 因跨專案對話混線事件後**部分過期**；本輪覆寫並整合 context hygiene。

## 2. Reviewed Inputs

- [Confirmed] `00-Plan/roadmap/roadmap.md` (CTO 更新版，含新 0D 章節，active marker = `CTO_CANONICAL_ROADMAP_CONTEXT_CLEAN_RETURN_TO_P26K_20260523`)
- [Confirmed] `00-Plan/roadmap/CTO-Analysis.md` (CTO 更新版，2026-05-23)
- [Confirmed] `data/paper_recommendations/p26j_*_rerun_20260521.json` (2 個)
- [Confirmed] `report/p26j_*_rerun_20260521.md` (2 個)
- [Confirmed] `00-BettingPlan/20260521/p26j_*.md`
- [Confirmed] `git log --oneline -10`：HEAD 仍 `0ccd06d`，無 P48/P49/Stock-Prediction 字樣
- [Confirmed] `git status --short`：64 dirty files (比 2026-05-21 PM 的 30+ 又多)；4 個 untracked `scripts/p26j_*.py`
- [Confirmed] grep contamination scan：未在 source content 找到 Stock/P48/P49 污染（除 roadmap governance guard 自身文字，屬 non-positive hit）
- [Confirmed] 用戶交接報告 + PROJECT_CONTEXT_LOCK 補充 + 兩大主軸補充

未執行：
- [Confirmed] 本輪未 rerun pytest。
- [Confirmed] 本輪未修改 CTO-Analysis.md 與 roadmap.md。
- [Confirmed] 本輪未 commit 任何檔案。
- [Confirmed] 本輪未對 untracked scripts 做任何 stage / remove 動作。

## 3. Yesterday Work Value Assessment

| 項目 | 評估 | 標記 |
|---|---|---|
| Context hygiene check 完成 (BETTING_CONTEXT_CLEAN) | **真實治理價值**：對話混線不等於 repo 污染，正式釐清避免錯誤救火 | [Confirmed] 治理推進 |
| `git log` 最近 10 筆 + grep `00-Plan/00-BettingPlan/report/data/paper_recommendations` | 結構化檢查，未發現 Stock 字樣 | [Confirmed] 證據級檢查 |
| CTO 新增 roadmap 0D 章節 + active marker 更新 | 把 context-lock 固化為 roadmap 一部分 | [Confirmed] 防複發機制建立 |
| HEAD 仍 `0ccd06d`，P26K 未執行 | 前一輪 CEO active_task 已寫好，但無 worker 進場執行 | [Confirmed] 任務未推進 |
| 4 個 untracked `scripts/p26j_*.py` 被列出 | 新風險面，**前輪未抓到** | [Risk][Confirmed] |
| 64 個 dirty files | 比 2026-05-21 多 30+，commit scope 風險升級 | [Risk][Confirmed] |
| CTO 將 Context-Lock 提到 P1、Untracked Scripts 提到 P2 | 方向正確但 CEO 需重新整合既有 P1 (COMPLETE_PAIR -1) | [Inferred] 需 CEO 整合 |
| 本輪未跑 tests | 不能宣稱 P26K 或 regression PASS | [Confirmed] |
| 對話層級混線真實發生 | 流程風險 [Confirmed]，repo 風險 [Refuted] | [Risk] |

結論：昨日成果為**治理成熟度真實推進**——把跨專案污染從「不確定的恐慌」變成「證據級的 clean classification」，並把 context-lock 固化進 roadmap。但**技術主線 (P26K) 仍未動**，且新增了 untracked scripts 風險與 dirty worktree 規模上升的次級風險。

## 4. CTO Judgment Review

完全採納項：
- [Confirmed] `BETTING_CONTEXT_CLEAN` classification 證據充分。
- [Confirmed] P0 維持 P26K Closing Fetch Trigger Root Cause Diagnostic。
- [Confirmed] 加入 PROJECT_CONTEXT_LOCK 機制（roadmap 0D + 每個 task prompt 必含）。
- [Confirmed] Untracked scripts 不可在 P26K artifact-only commit 中被誤 stage。
- [Confirmed] 不重啟 daemon、不改 scheduler/dedup/crawler、不 call live API、不手動補 snapshots。
- [Confirmed] champion `fixed_edge_5pct` 保留、promotion/production/champion replacement 全部 frozen。
- [Confirmed] 不直接修改 CEO-Decision.md / active_task.md (CTO scope 限制)。

部分採納 / 修正項：
- [Inferred] CTO 將 Context-Lock Preflight 排為**獨立 P1**，CEO 修正為**併入 P0 任務 Phase 0** (每個任務必跑 contamination grep)。理由：context-lock 是**橫向治理屬性**，每個任務都該帶，而不是一個獨立的優先項；獨立列會分散注意力。
- [Inferred] CTO 將 Untracked P26J Scripts 排為**獨立 P2**，CEO 修正為**併入 P0 任務 Phase 1** (untracked scripts inventory + classification + 不 stage)。理由：scripts 是 P26K commit scope 一定會碰到的，必須在同一輪內處理。
- [Risk] 我前一輪 PM session 將 COMPLETE_PAIR 220→219 下降 root cause 排為 P1；CTO 0D 沒明確處理。CEO **整合**：將 COMPLETE_PAIR -1 root cause 保留為 P26K 任務內 Phase 7 強制階段，不獨立列 P1。
- [Inferred] CEO 第一假設 (startup-only fetch architecture) 仍維持為 P26K Phase 3 第一驗證目標，CTO 未提但前輪已寫入。
- [Risk] CTO 將 paper recommendation 隱性壓在 P8，CEO 維持前輪上拉至 **P4** (主軸一契約設計併行，無釋出)。
- [Risk] dirty worktree 從 30+ 增至 64，**CEO 加上強制 `git status --short | wc -l` 數字 check**，若 >100 則需另行 CEO 授權才能繼續 commit。

不採納項：
- 無。CTO 整體方向正確，僅優先序層級需 CEO 重新整合避免分散。

最終判定：**CEO_DECISION_PARTIALLY_APPROVED**

## 5. Roadmap Gap Assessment

| Gap | 處理方式 |
|---|---|
| CTO 把 Context-Lock 排為獨立 P1 → 與技術主線分散 | CEO 改為「每個任務 Phase 0 必跑」橫向治理屬性 |
| CTO 把 Untracked Scripts 排為獨立 P2 → 與 P26K commit scope 衝突 | CEO 改為 P26K Phase 1 內處理，不獨立列 |
| CTO 未把前輪 CEO 補強的 COMPLETE_PAIR -1 root cause 顯式接入 | CEO 維持為 P26K Phase 7 強制階段 |
| CTO 未提 startup-only fetch hypothesis | CEO 維持為 P26K Phase 3 第一驗證 |
| CTO 0D 沒處理 dirty worktree 規模上升 (30+ → 64) | CEO 加入 `wc -l` 警戒線 (>100 需另行授權) |
| 兩大主軸 (paper rec + 策略優化) 在 CTO 未顯式排序 | CEO 維持 P4/P6 並行軌道 |
| 環境日期從 2026-05-21 跳到 2026-05-23 | CEO 接受 CTO 日期；artifact filename 仍用 20260521 (與 P26J chain 一致) 或新建 20260523 由 worker 判斷 |

## 6. CEO Priority Decision

| Priority | Phase | Track | Done condition | 對齊主軸 |
|---:|---|---|---|---|
| **P0** | P26K Closing Fetch Trigger Root Cause Diagnostic (read-only) + Context Hygiene + Untracked Scripts Inventory | Data QA + Observability + Governance | 一個明確 root cause classification (primary + secondary)；context-lock pre-flight PASS；4 個 untracked scripts 分類為 temporary/reusable/unknown 且**不 stage**；COMPLETE_PAIR -1 root cause 記錄；startup-only fetch hypothesis 驗證；P26J source-unavailable label retire；recommended_next_action enum 寫入 | 主軸二前置 |
| **P1** | Heartbeat-vs-Fetch Watchdog Design (design-only) | Observability design | 告警條件：`closing_window_active=true AND heartbeat=true AND fetched=false AND api_calls_today 未增加`；設計檔，無實作 | 治理 |
| **P2** | Scheduler/Quota/Next Trigger Decision Gate (post-P26K) | Ops governance | 依 P26K root cause + recommended_next_action 決定下一步；尚未啟動 | 主軸二 |
| **P3** | Bootstrap Gate Discipline (COMPLETE_PAIR >=300) | Validation | P25C bootstrap 維持 NOT RUN (219<300) | 主軸二 |
| **P4** | MLB → 台彩 Paper Recommendation 證據契約 (設計併行) | Product | moneyline / 讓分 / 大小分 / 單雙 / 局數市場契約設計；**僅契約，無釋出**；每筆 paper_only=true；不搶 P0 資源 | 主軸一 |
| **P5** | P26 Artifact SSOT Compression + P26 終結硬規則 | Governance | P26K 為 P26 階段終點；P26K 後不開 P26L 除非 root cause 明確要求 | 治理 |
| **P6** | P29/P30A Real Orchestrator Validation (並行非搶占) | Prediction | 在 P0 完成且不消耗 P0 資源情況下推進；diagnostic-only | 主軸二 |
| **P7** | P26 Runtime Validation Hygiene | QA | targeted tests + forbidden scan (含 Stock 字樣) 結果均記錄為實測值 | 治理 |
| **P8** | TSL CLV Data SSOT | Data governance | raw feed、daemon state、artifact 三者嚴格分離 | 治理 |
| **P9** | Repo / PR Governance Gate + Cross-Project Context Lock | Engineering governance | canonical branch=main；context-lock 每任務 Phase 0 必跑；commit 白名單 | 治理 |
| **P10** | Production Proposal Gate | Governance | 永久 blocked | 治理 |

## 7. Today Focus Direction

**唯一執行方向**：**P0 — P26K Closing Fetch Trigger Root Cause Diagnostic (read-only) + Context Hygiene + Untracked Scripts Inventory**（合一任務）

- 對應 phase：P0
- 重要性：
  1. P26J 證實 daemon 8 個 cycle 全 `fetched=false`，根因未知 → CLV 樣本永遠無法累積。
  2. `api_calls_today=2` 整天不變 + last 2 calls 在 02:07Z/02:09Z (P26G daemon restart 後)，**暗示 fetch 只在 startup 觸發**。
  3. COMPLETE_PAIR 220→**219** (-1) 必須在新 evidence 累積前釐清。
  4. P26J `TSL_SOURCE_UNAVAILABLE` 命名誤導，必須正式 retire。
  5. 跨專案污染風險真實發生於對話層，雖 repo clean，但每個 task 必須 context-lock pre-flight 防複發。
  6. 4 個 untracked `scripts/p26j_*.py` 與 64 個 dirty files 是 commit scope 高風險。
- 系統成熟度推進：
  1. 將「source unavailable」vacuous claim 拆成具體 root cause。
  2. 把 220→219 下降從 mystery 變成 documented。
  3. 把 context-lock 從事後救火變成事前防護。
  4. 把 untracked scripts boundary 明確化，避免被誤 stage 或誤刪。
  5. P26 階段收斂為單一 root cause chain。
- 預期收益：
  1. primary root cause + `recommended_next_action` enum → 下一輪可直接 CEO 授權對應動作。
  2. context-lock 機制成為跨任務不變式，降低多專案並行污染風險。
  3. 4 個 scripts 與 64 個 dirty files 都有明確處置決定。
- 風險：
  1. read-only，無模型/收益改變。
  2. dirty worktree 規模上升（30+→64），白名單 commit 風險升級 → CEO 加 `wc -l >100` 警戒線。
  3. untracked scripts 若被誤 stage 會污染 P26K 純診斷 commit。
- 驗收標準：見 active_task.md。
- 是否採納 CTO：採納大方向 + CEO 修正 (Context-Lock 與 Untracked Scripts 併入 P0 任務內處理，不獨立列 P1/P2)。

## 8. Risks / Blind Spots

- [Risk] 跨專案對話混線真實發生；雖 repo clean，但若下一輪 prompt 沒帶 PROJECT_CONTEXT_LOCK，agent 仍可能再混入 Stock 內容。
- [Risk] 4 個 untracked `scripts/p26j_*.py` 用途未知；若是 worker 自製分析工具，不該被誤 stage；若是必要工具，不該被忽略；CEO 強制 P26K 任務內**分類但不處置**（除非顯式授權）。
- [Risk] dirty worktree 從 30+ 升至 64；commit scope 越大越容易誤 stage；CEO 加 `wc -l >100` 警戒線。
- [Risk] CEO 第一假設「fetch 只在 daemon startup 觸發」若 confirmed，整個 daemon scheduler 架構需重設計，非小修。
- [Risk] COMPLETE_PAIR -1 若是新 evidence 反向 invalidate prior pair，CLV 樣本可信度需重評估。
- [Unknown] `api_calls_today=2` 是 hard quota / dedup / startup-only side effect，三選一。
- [Unknown] `next_trigger_minutes=null` 是 expected / bug / 配置缺失。
- [Unknown] `markets=[]` 真因 (source 真沒給 vs fetch 沒執行 client 自填空)。
- [Unknown] 環境日期跳到 2026-05-23 是 CTO review 日期還是真實環境日期；artifact filename 約定需 worker 自行決定。
- [Risk] 主軸一/二易被治理工作遮蔽；CEO 顯式 P4/P6 並行軌道但禁止搶占 P0。
- [Confirmed] `production_ready=false`，promotion/champion replacement/production proposal/live API/TSL crawler modification/profitability claim 全部 frozen。
- [Confirmed] P25C bootstrap NOT RUN (219<300)。
- [Inferred from report] 75 PASS / 0 FAIL 為 P26J 報告值未實測，P26K validation phase 必須 rerun。

## 9. CEO Final Decision

**CEO_DECISION_PARTIALLY_APPROVED**

- 採納 CTO Context Hygiene Clean 大方向 + P0 = P26K。
- 修正 CTO 把 Context-Lock 排為獨立 P1 → CEO 改為「每任務 Phase 0 必跑」橫向治理屬性，併入 P26K Phase 0。
- 修正 CTO 把 Untracked Scripts 排為獨立 P2 → CEO 改為 P26K Phase 1 內分類處理，不獨立列。
- 維持前輪 CEO 補強：startup-only hypothesis 為 P26K Phase 3 第一驗證；COMPLETE_PAIR -1 root cause 為 P26K Phase 7 強制階段；P26 終結硬規則；即使發現 bug 只記錄不修。
- 新增本輪：`PROJECT_CONTEXT_LOCK` 區塊強制；contamination grep 含 `P48|P49|Stock-Prediction|golden fixture|paper simulation dry-run`；dirty worktree `wc -l >100` 警戒線；untracked scripts 不 stage 不刪只分類；commit 白名單 forbidden pattern 加入 `scripts/p26j_`。
- 明令禁止：optimizer promotion、champion replacement、production proposal、live odds API、TSL crawler modification、daemon restart、scheduler/dedup/crawler code change、profitability claim、PR merge (除非顯式批准)、手動補造 snapshots、新增 repo/worktree/branch、開新 P26L (除非 root cause 明確要求)、納入 Stock-Prediction/P48/P49 內容、stage `scripts/p26j_*.py`、stage raw feed/daemon state/runtime output。
- `paper_only=true`、`diagnostic_only=true`、`read_only=true`、`context_hygiene=BETTING_CONTEXT_CLEAN` 為 P26K 所有產出強制 invariant。

## 10. 10 行內 CEO 摘要

1. Context Hygiene Check 完成：`BETTING_CONTEXT_CLEAN`，對話混線但 repo 無污染。
2. HEAD 仍 `0ccd06d`，P26K 仍未執行；前輪 active_task.md 仍 canonical (本輪僅補強)。
3. 4 個 untracked `scripts/p26j_*.py` + 64 個 dirty files (前輪 30+，已升級風險)。
4. 採納 CTO 0D Context Hygiene 大方向 + P0 = P26K。
5. 修正：Context-Lock 與 Untracked Scripts 併入 P0 任務內 (Phase 0/1)，不獨立列 P1/P2。
6. CEO 補強：PROJECT_CONTEXT_LOCK 區塊、contamination grep、dirty `wc -l >100` 警戒線、scripts 不 stage 不刪只分類。
7. 維持前輪：startup-only fetch hypothesis、COMPLETE_PAIR -1 必查、P26 終結硬規則、bug 只記錄不修。
8. 主軸一 paper rec 維持 P4 (設計併行)；主軸二後置 (bootstrap/optimizer) 今日不啟動。
9. 強制 read-only/白名單 commit/不准開 P26L/不准納入 Stock 內容/不准 stage scripts。
10. Final classification = `CEO_DECISION_PARTIALLY_APPROVED`。
