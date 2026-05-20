# Long-Term MLB (大聯盟) Prediction Optimization Plan

> **Superseded notice — 2026-05-15 CTO update:** This roadmap is preserved as historical context. The current roadmap is `00-BettingPlan/roadmap/betting_roadmap_20260515_mlb_product_plan.md`, marker `CTO_BETTING_ROADMAP_V7_MLB_PRODUCT_PLAN_20260515_READY`. Use the 2026-05-15 version for next-phase planning because the project now has an explicit single-repo consolidation requirement and a product-level focus on MLB betting recommendations plus strategy simulation optimization.

**Document ID:** `long_term_wbl_prediction_optimization_plan_2026-05-03` **Date:** 2026-05-03 (Revision 3 — CTO alignment update 2026-05-07) **Author:** AI Prediction System Architect (Planner-mode, deterministic; no external AI was called to author this plan) **Scope:** Betting-pool / MLB (Major League Baseball) 賽事預測系統，長期 (180 天) 優化藍圖 **Governance:** Plan-only document. 不觸發任何 production patch、不繞過 human review、不使用 sandbox 結果宣稱 production 成功。

---

## 0A. CTO Alignment Update — 2026-05-07

### 0A.1 Roadmap 對齊度判斷

原 roadmap 的 180 天方向仍成立：MLB domain abstraction、metrics / validation SSOT、scheduler governance、usage budget guard 都仍是中長期必要建設。但 2026-05-06 的每日總結與 Phase59-68 artifacts 已經把短期問題收斂到 heavy_favorite / high_confidence failure，因此「今天」不應再優先做泛架構 P0，而應先完成 Phase69 paper-only counterfactual，確認 model architecture / probability shaping / calibration objective 是否真的是瓶頸。

### 0A.2 與原 roadmap 的主要落差

| 原 roadmap 排序 | 實際進度 / 證據 | CTO 調整 |
| :---- | :---- | :---- |
| 先做 `LeagueAdapter` / `MLBAdapter` | 系統已完成 Phase59-68 root-cause 排查，且 2025 prediction artifact 已有 2025 場可用樣本 | `LeagueAdapter` 下修為 P1，本日 P0 改做 Phase69 |
| 先建立 walk-forward / Brier / ECE baseline | Phase68 已有 2025 場 baseline：all blend Brier 0.243419、ECE 0.025784；heavy_fav n=60、blend BSS vs market = -0.003264 | baseline 不再是空白，下一步是 calibration objective counterfactual |
| Feature backlog 中 bullpen / SP / market / context 仍靠前 | Phase64B/65/66/67 已分別判定 bullpen、SP fatigue、market microstructure、context 暫時不 promising 或 overfit risk | 這四條 feature-family patch route 降級為 P2 / data-only，不進 patch gate |
| Usage Budget Guard 是 Phase0 P0 | 仍重要，但本輪主要風險是錯誤模型 patch，不是外部 AI 成本 | Budget Guard 保留 P1，不能阻塞 Phase69 deterministic paper-only work |

### 0A.3 目前系統狀態 Snapshot

- 最新有效 artifact：`data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`，共 2025 場。
- Phase68 gate：`CALIBRATION_OBJECTIVE_REDESIGN_PROMISING`。
- Phase68 找到實際架構來源：`models/stacking_model.py` 中 `away_wp * 0.9` favorite sharpening、`logit / 0.85` confidence sharpening、`steam * 0.25` market double-incorporation risk。
- 已降級路線：bullpen granular、SP fatigue、market microstructure、context feature-family patch。
- 測試狀態：Phase68 172/172 PASS；Phase67+68 347/347 PASS；full regression 3853 passed / 31 failed / 15 skipped，其中 31 failed 目前歸類為既有無關 tech debt。
- 不可越線：不得 production patch、不得修改 production model、不得調整 production market_blend alpha、不得用 in-sample calibration 宣稱成功。

### 0A.4 Reordered P0 / P1 / P2

| Priority | 新排序 | 原因 | Done 條件 |
| :---- | :---- | :---- | :---- |
| **P0 — Today** | Phase69 Calibration Objective Redesign Counterfactual | Phase68 已將 failure 收斂到 calibration objective / probability shaping；這是當前最短的決策路徑 | 產出 Phase69 module / runner / tests / JSON / report，gate 明確指向 Phase70 或停止 patch search |
| **P0 — Guardrail** | 隔離 full regression 31 failed 為獨立 tech debt，不混入 Phase69 判讀 | 避免把既有失敗誤判成 Phase69 regression | Phase69 targeted tests + Phase67/68 regression pass；full suite failure list 另列 |
| **P1 — This Week** | Phase70 gate 設計（依 Phase69 結論選 calibration objective / probability shaping / ensemble weighting / abstention guard） | Phase69 若 promising，下一步仍只能 paper-only patch gate | Phase70 prompt / acceptance gate / no-production policy 完成 |
| **P1 — This Week** | Metrics SSOT / bootstrap / ECE shared utility 收斂 | Phase69/70 會重複使用 Brier、BSS、ECE、bootstrap CI | 新增或整併 shared metrics，caller 不再各算各的 |
| **P1 — This Week** | Budget Guard + Planner external-AI invariant | 原 roadmap governance 仍正確，只是不應阻塞 Phase69 | planner external AI = 0 runtime assertion；budget warn/critical path 有測試 |
| **P2 — Later** | `LeagueAdapter` / `MLBAdapter` / `WBCAdapter` 架構化 | 中長期正確，但今天不是 heavy_fav failure 的最快解 | 不改行為地包覆現有資料與 rule engine |
| **P2 — Later** | Bullpen 1d/5d/B2B/closer、lineup/travel/key batter、opening line / line movement 補資料 | 目前 DATA_LIMITED 或 not promising，不應變成 patch route | 只做 ingestion / coverage，不宣稱模型提升 |

### 0A.5 今日最應聚焦的系統優化方向

今天唯一主線：**Phase69 — paper-only calibration objective redesign counterfactual**。目標不是修 production，而是用 PIT-safe / OOF / rolling monthly validation 判斷 `logit/0.85`、`away_wp*0.9`、OOF isotonic / Platt、confidence-band abstention 是否真的改善 Brier / BSS / ECE，並決定 Phase70 是否值得開 gate。

### 0A.6 Latest Worker Task Prompt

```text
你是 Betting-pool MLB 系統的 Worker Agent。

任務名稱：
Phase 69 — Calibration Objective Redesign Counterfactual with OOF / PIT-safe Validation

日期：
2026-05-07

背景：
Phase59-68 已完成 heavy_favorite / high_confidence failure root-cause 排查。
Bullpen granular、SP fatigue、market microstructure、context feature-family patch 路線已分別被降級為 not promising、OVERFIT_RISK 或 DATA_LIMITED。
Phase68 gate = CALIBRATION_OBJECTIVE_REDESIGN_PROMISING。
Phase68 已定位 probable causes：
- `models/stacking_model.py` 內 `away_wp * 0.9` favorite sharpening
- `models/stacking_model.py` 內 `logit / 0.85` confidence sharpening
- `steam * 0.25` 可能造成 market signal double incorporation

任務目的：
建立 paper-only counterfactual，評估 calibration objective / probability shaping / ensemble output 是否值得進入 Phase70 paper-only patch gate。不得建立 production patch。

核心要求：
1. 不修改 production model。
2. 不調整 production market_blend alpha。
3. 不覆蓋 production prediction JSONL。
4. 不用 in-sample fit-and-evaluate。
5. calibration training data 必須嚴格早於 evaluation data。
6. 盤點 prediction generation / model_home_prob / market_home_prob_no_vig / blend_home_prob / ensemble / calibration artifacts。
7. 明確記錄所使用 artifacts、audit_hash、coverage 與選用理由。
8. 至少比較 variants：
   - original_baseline
   - remove_logit_sharpening
   - remove_away_damping
   - remove_both
   - OOF isotonic calibration
   - OOF Platt calibration
   - confidence-band abstention diagnostic
9. segmentation 至少包含：
   - all games
   - heavy_favorite prob >= 0.70
   - high_confidence prob >= 0.75
   - extreme_favorite prob >= 0.80
   - model_prob 0.60-0.65
   - model_prob 0.65-0.70
   - model_prob 0.70-0.75
   - model_prob 0.75+
   - Phase45 failure segment
10. metrics 至少包含：
   - Brier
   - BSS
   - ECE
   - bucket-level ECE
   - heavy_favorite ECE
   - high_confidence BSS
   - calibration residual
   - win-rate by confidence band
   - market-only vs model-only vs blend comparison
   - bootstrap CI
11. negative controls 至少包含：
   - shuffled probability band
   - random confidence assignment
   - irrelevant bucket split
12. 若 negative control 也顯著，必須標記 OVERFIT_RISK。
13. abstention / no-bet guard 只允許 diagnostic，不可宣稱 ROI success。
14. report 必須明確判斷是否值得進 Phase70：
   - calibration objective patch gate
   - probability shaping removal gate
   - ensemble weighting gate
   - abstention guard gate
   - 或停止 patch search

輸出檔案：
- `orchestrator/phase69_calibration_objective_redesign_counterfactual.py`
- `scripts/run_phase69_calibration_objective_redesign_counterfactual.py`
- `tests/test_phase69_calibration_objective_redesign_counterfactual.py`
- `reports/phase69_calibration_objective_redesign_counterfactual_20260507.json`
- `00-BettingPlan/20260507/phase69_calibration_objective_redesign_counterfactual_report_20260507.md`

Gate 結論七選一：
- `CALIBRATION_OBJECTIVE_PATCH_PROMISING`
- `PROBABILITY_SHAPING_REMOVAL_PROMISING`
- `ENSEMBLE_WEIGHTING_REPAIR_PROMISING`
- `ABSTENTION_GUARD_PROMISING`
- `OVERFIT_RISK`
- `DATA_LIMITED`
- `CALIBRATION_OBJECTIVE_NOT_PROMISING`

驗收條件：
- 所有新增 tests 通過
- Phase67 / Phase68 targeted regression 不破壞
- candidate_patch_created = false
- production_modified = false
- alpha_modified = false
- report 明確說明 Phase70 是否值得進行

完成標記：
`PHASE_69_CALIBRATION_OBJECTIVE_REDESIGN_COUNTERFACTUAL_VERIFIED`
```

---

## 0\. 名詞釐清 (Terminology Disambiguation) — READ FIRST

### 0.1 「WBL」= MLB 大聯盟 (Major League Baseball)

使用者於 review 中確認：本系統的目標賽事為 **MLB (Major League Baseball / 大聯盟)**。原 prompt 中的 `WBL` 應視為 **MLB 的本地代號**，文件統一改用 `MLB`。

### 0.2 Codebase 已存在的 MLB 資產 (這是好消息)

盤點結果，repo 已有 MLB 基礎：

- `data/mlb_2024_pitchers.py` — 2024 投手資料抓取  
- `data/mlb_2025_preview.py` — 2025 賽季 preview 資料  
- `report/mlb_2025_full_backtest.md` — 2025 完整回測報告  
- `docs/mlb_2025_historical_odds_timeline_asset_spec.md` — odds timeline 規格  
- 既有 odds pipeline (`data/odds_api_client.py`)、CLV pipeline、Kelly / risk control 模組均可直接套用。

代表 MLB 的「資料層 \+ 回測層」並非 0；**本計畫的任務是把這些資產正規化、結構化、納入 governance**，而不是從零打造。

### 0.3 為什麼 MLB 比 WBC 更好做

| 條件 | WBC | MLB | 對計畫的影響 |
| :---- | :---- | :---- | :---- |
| 場次數 / 季 | 數十場 | **2,430 場 regular season \+ 季後賽** | 1500 樣本 hard gate 容易達標 |
| 資料源成熟度 | 有限 | **MLB StatsAPI、Baseball Savant、Retrosheet、FanGraphs** 公開 | 特徵工程成本大幅下降 |
| 盤口流動性 | 低 | **極高 (Pinnacle/Circa 為 sharp 標竿)** | CLV 訊號乾淨，sharp money 偵測有效 |
| Park / weather 影響 | 小（賽會制） | **顯著 (尤其 Coors / Fenway 等)** | park factor、weather feature 必加 |
| 投手 matchup | 中 | **極強訊號 (starting pitcher 是 \#1 feature)** | 改變 feature 排序 |
| 賽季時間範圍 | 集中在 3 月 | **3 月底–10 月，每天 10–15 場** | 排程器需處理 daily slate |
| 樣本年數 | 有限 | **可回溯 10+ 年** | walk-forward 訓練視窗充足 |

### 0.4 與 WBC 的關係（不要丟掉）

WBC 既有實作 (`wbc_backend/`) 仍然有價值，**改成 MLB 的「pre-season tournament 視窗」**——MLB 球員在 WBC 出賽會影響 spring training，可作 MLB 開季預測的輔助資訊。建議在 League abstraction 中：

- 主 adapter：`MLBAdapter` (新)，由現有 `mlb_*` 資料層升級而來  
- 輔 adapter：`WBCAdapter`（保留，包覆既有 `wbc_backend/`），主要供 MLB 球員傷況 / 表現 跨資料庫使用

### 0.5 Action Item — Phase 0 Day 1

- 建立 `docs/glossary/league_codes.md`：明確標註 `MLB = Major League Baseball (主要預測對象)`、`WBC = World Baseball Classic (輔助資料源 / 既有資產)`  
- `wbc_backend/` 的 layer name 維持不動（避免大規模 rename 觸發 import 風暴），但在 README 內加註「`wbc_backend` 是歷史命名；目標 league \= MLB，WBC 為輔助」

---

## 1\. Executive Summary

### 1.1 一句話結論

**目前系統已從「單機跑模型」演進到「具備治理、Audit、CLV pipeline 的半自主 MLOps」階段，且 codebase 已具備 MLB 2024/2025 基礎資料與回測；但仍困在三大缺口：(a) MLB 領域邏輯未被抽成 League adapter、root vs `wbc_backend/` 雙軌未收斂、(b) MLB 全季規模 (2,430 場/年) 的 walk-forward / 校準 / CLV 樣本未系統化驗證、(c) 排程器決策仍偏 procedural、未對 daily-slate 的高密度賽程做 priority-driven 排程。本計畫以 180 天分四階段，把系統推進到「可重複、可審計、可自我學習」的 MLB production-proposal-ready 狀態，且全程不違反 fail-closed governance。**

### 1.2 三大主軸 (Top-3 thrusts)

1. **MLB Domain & League Abstraction**：把現有 `mlb_*` 資料零件 \+ `wbc_backend/` rule\_engine 抽成 `MLBAdapter`（主）+ `WBCAdapter`（輔），完成 root `models/`、`strategy/` 的 deprecation roadmap。  
2. **Statistical Rigor Loop (MLB-scale)**：利用 MLB 高樣本優勢，在 CLV accumulation → investigation → patch-gate-recheck 之上，加上強制 walk-forward / OOS / bootstrap CI / calibration / regime split 的 audit-trailed 驗證鏈；目標是「每週 walk-forward 跑 ≥ 1500 樣本」常態化。  
3. **Self-Learning Scheduler (Daily-Slate aware)**：把現在的 `clv_batch_scheduler` \+ `planner_tick` 升級成 priority-scored、event-driven、budget-aware 的排程核心；MLB 每天 10–15 場意味 closing monitor 並發度與 odds-snapshot 頻率都需提升。Planner 永遠 deterministic，Worker 在 policy-allow 下才動用外部 AI。

### 1.3 KPI 北極星 (North-Star KPIs)

| KPI | Baseline (今日推估) | 30D Target | 90D Target | 180D Target |
| :---- | :---- | :---- | :---- | :---- |
| Brier Score (head-to-head) | 未量化 | 量化 baseline | \< baseline − 0.005 (CI 95%) | \< baseline − 0.015 (CI 95%) |
| Calibration Error (ECE) | 未量化 | 量化 baseline | ≤ 0.05 | ≤ 0.03 |
| CLV (closing-price-value, 平均 bps) | \< 25 樣本 | ≥ 50 樣本 | ≥ \+50 bps (CI 90%) | ≥ \+80 bps (CI 95%) |
| Audit Coverage (external AI calls audited) | 部分 | FULL | FULL | FULL |
| Human Review SLA (median resp time) | 未量化 | 量化 | \< 24h | \< 12h |
| Planner External-AI Calls | 應為 0 | 0 (assert) | 0 | 0 |
| Scheduler Task Success Rate | 未量化 | ≥ 95% | ≥ 98% | ≥ 99% |
| Usage Cost vs Budget | 未限額 | 訂出限額 | ≤ 80% budget | ≤ 70% budget |

### 1.4 「現在最該做的 3 件事」

1. **執行 Phase69 paper-only calibration objective redesign counterfactual**：針對 `logit/0.85`、`away_wp*0.9`、OOF isotonic / Platt、abstention diagnostic 做 PIT-safe / OOF 驗證，決定 Phase70 是否值得開 gate。  
2. **把 Phase59-68 已降級的 feature-family 路線鎖住**：bullpen、SP fatigue、market microstructure、context 暫時只允許 data / diagnostic work，不進 production patch gate。  
3. **保留 governance / architecture 建設為本週 P1**：Budget Guard、Planner external-AI invariant、Metrics SSOT 仍要做，但不阻塞 Phase69 的 deterministic paper-only work。

---

## 2\. Current System Assessment

### 2.1 已成熟模組 (Production-ready, 不要動)

| 模組 | 路徑 | 狀態 | 備註 |
| :---- | :---- | :---- | :---- |
| Safe Task Executor | `orchestrator/safe_task_executor.py` | 成熟 | fail-closed 已落地 |
| CLV Batch Scheduler | `orchestrator/clv_batch_scheduler.py` | 成熟 | Phase33 已驗收 |
| CLV Threshold Tracker | `orchestrator/clv_threshold_tracker.py` | 成熟 | Phase34 已驗收 |
| CLV Accumulation Policy | `orchestrator/clv_accumulation_policy.py` | 成熟 | Phase32 已驗收 |
| Daily CLV Ops Runbook | `scripts/run_daily_clv_ops_summary.py` | 成熟 | Phase35 已驗收 |
| Usage Detail UI | `runtime/agent_orchestrator/frontend/index.html` | 成熟 | Provider breakdown 已落地 |
| Optimization Readiness | `orchestrator/optimization_readiness.py` | 成熟 | LEARNING\_READY gate |
| Pipeline Backtest Runner | `wbc_backend/backtest/runner.py` | 成熟 | walk-forward 基礎 |

### 2.2 過於耦合 / 應該拆分 (Refactor backlog)

| 痛點 | 位置 | 風險 | 建議動作 |
| :---- | :---- | :---- | :---- |
| 雙軌 `models/` vs `wbc_backend/models/` | repo root \+ `wbc_backend/` | import 漂移、版本不一致 | 進入 Workstream A.2 — Deprecation Roadmap |
| 雙軌 `strategy/` vs `wbc_backend/strategy/` | repo root \+ `wbc_backend/` | 策略邏輯散落 | 同上，先建 import-shim，再逐檔搬 |
| `main.py` vs `scripts/run_mode.py` vs `wbc_backend/run.py` | 三處 entry-point | 行為不一致 | 統一到 `wbc_backend/run.py`，其餘變 thin wrapper |
| WBC 領域邏輯散落於 `wbc_backend/pipeline/wbc_rule_engine.py` | 強耦合 League (WBC) | 無法支援 MLB / NPB / KBO | 抽 `LeagueRuleEngineProtocol`，MLB 為主 adapter |
| Self-improve 流程在 `wbc_backend/optimization/self_improve.py` 直接寫狀態 | 無 patch-gate | 容易跳過 review | 改寫成「produce proposal only」 |
| Telegram bot 手動觸發指令 | `telegram_bot/bot.py` | 缺 audit | 通過 SafeTaskExecutor |

### 2.3 應該 state-machine / event-driven 化的流程

1. **Prediction Lifecycle**：`PROPOSED → SCHEDULED → CLOSING_MONITORED → COMPUTED_CLV → LEARNING_READY → INVESTIGATED → PATCH_GATE → HUMAN_REVIEW → APPROVED/REJECTED`。目前散落在多個檔案的 if/else 應抽成 `PredictionState` enum \+ transition table。  
2. **Learning Cycle**：`COLLECTING → THRESHOLD_HIT → INVESTIGATING → CANDIDATE_FOUND → PROPOSAL_DRAFTED → REVIEW_PENDING → APPROVED → DEPLOYED`。  
3. **Scheduler Tick**：`IDLE → ASSESSING → DISPATCHED → AWAITING → POSTPROCESSING`，並把 priority-score 放在 `ASSESSING` 階段算。

### 2.4 高風險耦合點 (Top-5 risk)

1. **`runtime/agent_orchestrator/training_memory.json` 直接讀寫** — 無 schema 驗證、無 retention policy、無 lock。  
2. **CLV pipeline 與 odds source 直連** — 切換盤口提供者代價高。  
3. **Planner 與 Worker 共用相同 LLM client 配置** — 萬一 misconfig，Planner 會打外部 AI（critical incident）。  
4. **Audit Guard 只覆蓋已知通道** — 新增第三方呼叫時容易漏接。  
5. **回測 / paper / production 的 metric 計算分散在多份 script** — 同一 KPI 在不同地方算法不同。

### 2.5 不建議立即改動 (Do-NOT-touch list, 至少 90 天內)

- `safe_task_executor.py` 的核心 fail-closed 路徑  
- CLV 三件套（accumulation / threshold / batch scheduler）的對外 API  
- `wbc_backend/research/portfolio_v3.py`（institutional research 邏輯，動了會破壞既有報告鏈）  
- AuditGuard 的 deny-by-default 行為  
- Telegram bot 的 read-only command 路徑

---

## 3\. Target System Architecture

### 3.1 目標分層 (Layered Architecture, ASCII)

\+--------------------------------------------------------------------+

| OBSERVABILITY LAYER                                                |

|  \- usage\_dashboard (frontend/index.html, 已有)                     |

|  \- audit\_dashboard (新增)                                          |

|  \- ops\_report  (orchestrator/optimization\_ops\_report.py, 已有)     |

|  \- readiness\_report (orchestrator/optimization\_readiness.py, 已有) |

|  \- daily\_runbook (scripts/run\_daily\_clv\_ops\_summary.py, 已有)      |

|  \- architecture\_health\_score (新增, 季度跑)                        |

\+--------------------------------------------------------------------+

| APPLICATION LAYER                                                  |

|  \- PlannerService    (deterministic only, 嚴禁外部 AI)              |

|  \- WorkerService     (policy-gated 外部 AI)                         |

|  \- LearningCycleService (state-machine)                             |

|  \- PatchGateService  (proposal-only, no auto-deploy)                |

|  \- ReviewQueueService (human-review backbone)                       |

|  \- SchedulerService  (priority-scored, event-driven)                |

\+--------------------------------------------------------------------+

| DOMAIN LAYER                                                        |

|  \- prediction\_domain  (PredictionState, PredictionRegistry)         |

|  \- odds\_domain        (OddsSource, LineMovement, ClosingSnapshot)   |

|  \- clv\_domain         (CLVRecord, CLVInvestigation)                 |

|  \- learning\_domain    (LearningCycle, FeatureVersion, ModelVersion) |

|  \- governance\_domain  (AuditGuard, BudgetGuard, ReviewQueue)        |

|  \- league\_domain      (LeagueAdapter: MLB(主) | WBC(輔) | …, 新增)  |

\+--------------------------------------------------------------------+

| INFRASTRUCTURE LAYER                                                |

|  \- Persistence (JSONL → SQLite/Postgres，分階段)                    |

|  \- Usage / Audit logs (append-only, hash-chained)                  |

|  \- Report writers (md / json / pdf 輸出)                           |

|  \- Frontend API (FastAPI, 已有 wbc\_backend/api/app.py)              |

|  \- LLM Gateway (single egress, AuditGuard 強制覆蓋)                 |

\+--------------------------------------------------------------------+

### 3.2 模組責任表 (Responsibility Matrix)

| Service | Reads | Writes | 可呼叫外部 AI | Governance |
| :---- | :---- | :---- | :---- | :---- |
| Planner | training\_memory, ops\_report, readiness, review queue | next\_task proposal | **NEVER** | deterministic assertion |
| Worker | task spec, code repo | code patch (sandbox), logs | YES (policy-gated) | AuditGuard 必經 |
| Learning Cycle | CLV records, predictions | learning\_cycles.jsonl | NO (deterministic) | logged |
| Patch Gate | candidate patch, backtest reports | gate\_decisions.jsonl | NO | deterministic |
| Review Queue | gate decisions, simulation results | review\_queue.jsonl | NO | human-driven |
| Scheduler | all telemetry | task\_dispatch.jsonl | NO | budget-aware |
| Frontend | reports, telemetry | (read-only) | NO | n/a |

### 3.3 League Abstraction (新增的核心抽象)

class LeagueAdapter(Protocol):

    code: str  \# "MLB" | "WBC" | ...

    def list\_fixtures(self, season: str) \-\> list\[Fixture\]: ...

    def fetch\_results(self, fixture\_id: str) \-\> Result | None: ...

    def fetch\_odds\_open(self, fixture\_id: str) \-\> OddsSnapshot: ...

    def fetch\_odds\_closing(self, fixture\_id: str) \-\> OddsSnapshot: ...

    def fetch\_lineups(self, fixture\_id: str) \-\> Lineups | None: ...      \# MLB: 含先發投手

    def fetch\_injuries(self, team: str) \-\> list\[Injury\]: ...             \# MLB: IL 名單

    def fetch\_park\_factors(self, venue: str) \-\> ParkFactor: ...          \# MLB-specific

    def fetch\_weather(self, fixture\_id: str) \-\> Weather | None: ...      \# MLB-specific

    def league\_specific\_rules(self) \-\> RuleSet: ...

- **`MLBAdapter`** (主，新增)：包覆 `data/mlb_2024_pitchers.py`、`data/mlb_2025_preview.py`、`data/odds_api_client.py`、MLB StatsAPI / Baseball Savant；落腳 `wbc_backend/league/mlb_adapter.py`（檔名沿用 `wbc_backend` package，避免大規模搬遷）。  
- **`WBCAdapter`** (輔，重構)：把 `wbc_backend/pipeline/wbc_rule_engine.py` 包成 adapter，主要供「MLB 球員 WBC 出賽紀錄 → spring training/開季表現」的 cross-league feature 使用。  
- 後續若要支援 NPB / KBO / CPBL，只需新增 adapter，不再改 application layer。

---

## 4\. Long-term Optimization Roadmap (180-day)

Day 0 ──────── 30 ──────── 60 ──────── 90 ──────── 180

   │            │            │            │           │

   │ Phase 0    │ Phase 1    │ Phase 2    │ Phase 3   │

   │ Stabilize  │ Foundation │ Validation │ Self-Learn│

   │            │            │            │           │

   ▼            ▼            ▼            ▼           ▼

 Audit/        MLB data     Walk-fwd     Ensemble    Production-

 Budget        normalization on MLB      \+calibrate, proposal

 Guard,        \+LeagueAdpt, ≥1500 smp,   regime,     workflow,

 Glossary,     CLV ≥50,     feature      threshold   stable CLV

 Planner       Brier/ECE    registry,    feedback    ROI loop,

 invariant     baseline     simulation   loop        arch audit

              (MLB \+WBC                  on MLB

              cross-link)                daily slate

每階段詳細任務見 §10 Phase Plan。

---

## 5\. Workstream A — Program / System Architecture

### 5.1 Goal

把雙軌（root vs `wbc_backend/`）收斂成單一 canonical layer，並引入 League abstraction 與 state-machine 化 lifecycle。

### 5.2 Deliverables

- `docs/architecture/target_layered_architecture_v1.md`（含本文件 §3 之擴充版）  
- `wbc_backend/league/` 新模組：`base.py`、`mlb_adapter.py`（主，Phase 1 完成）、`wbc_adapter.py`（輔，Phase 1 重構既有 rule\_engine）  
- `wbc_backend/state_machine/`：`prediction_state.py`、`learning_state.py`、`scheduler_state.py`  
- `docs/architecture/deprecation_roadmap.md`：列出 root `models/`、`strategy/` 每個檔案的搬遷對應  
- `tests/architecture/test_no_root_imports.py`：驗證新代碼不再 import root `models/`  
- `scripts/architecture_health_score.py`：按月跑

### 5.3 Refactor Priority (按可動順序)

1. **P0** — `wbc_backend/league/base.py` 介面 \+ `WBCAdapter` 包覆現有 rule\_engine（**不改行為**）  
2. **P1** — `state_machine/prediction_state.py` 取代散落的 if/else  
3. **P2** — Entry-point 收斂，`main.py` 改成 thin shim  
4. **P3** — root `models/` 搬至 `wbc_backend/models/legacy/`，再逐檔升級  
5. **P4** — root `strategy/` 同上  
6. **P5** — Persistence 從 JSONL 升級到 SQLite (90 天後再評估)

### 5.4 Architecture Anti-patterns (要主動消除)

- 無條件 `from models import …`：應一律走 `wbc_backend.models`  
- 直接讀寫 `runtime/agent_orchestrator/training_memory.json`：應透過 `LearningMemoryRepository`  
- 多份 KPI 計算函式：應抽成 `wbc_backend/evaluation/metrics.py` 的 single source of truth  
- 在 if/else 內寫 transition logic：應走 state machine  
- 在 worker 程式碼裡硬編 LLM provider name：應走 `LLMGateway`

---

## 6\. Workstream B — MLB Prediction Accuracy Improvement

### 6.1 Data Inventory & Gap Plan (MLB-centric)

| 資料類別 | 現況 | 目標 (MLB) | 缺口 | 補齊行動 |
| :---- | :---- | :---- | :---- | :---- |
| 賽程 (fixtures) | `data/mlb_2025_preview.py` (部分) | MLB StatsAPI 全季 (2,430+ 場) | 自動每日同步 | `MLBAdapter.list_fixtures(season)` |
| 隊伍 / 30 隊 Roster | 部分 | MLB StatsAPI `roster/` endpoint | 需正規 schema | `RosterRepository` 統一寫入 |
| 球員統計 | `data/mlb_2024_pitchers.py` | Baseball Savant (Statcast)、FanGraphs (FIP/xFIP/SIERA) | 未自動化抓取 | `PlayerStatsRepository` \+ 每日同步 |
| 先發投手 (lineup) | 部分 | MLB **賽前 1–2h 公布**，是 \#1 訊號 | 需 high-frequency 抓取 | scheduler 每 30 min 賽前抓 |
| Injuries / IL | `wbc/adjustments.py` 部分 | MLB IL (10/15/60 day) feeds | 結構化 | `InjuryRepository` |
| 歷史賽果 | 部分 | Retrosheet 1990– / MLB StatsAPI 2008– | 至少回填 5 季 | 一次性 backfill 任務 |
| Odds opening | `data/odds_api_client.py` | The Odds API / Pinnacle / Circa | 多家比對 | 多 provider fallback \+ spread 計算 |
| Odds closing | CLV pipeline 已有 | 同上 \+ Pinnacle close 為 sharp 標竿 | 樣本累積 | 持續 accumulate (90D ≥ 50\) |
| Line movement | 部分 | high-frequency snapshot (賽前 6h 起每 10 min) | 不足 | Scheduler T-360 → T-0，每 10 min |
| Implied probability | 由 odds 算 | no-vig blended (multi-book) | 多書合成 | `OddsAggregator.no_vig_blend()` |
| Sharp / liquidity | `strategy/sharp_detector.py` | reverse line movement、steam moves | 需 multi-book | Phase 2 入 feature |
| Prediction registry | `runtime/agent_orchestrator/` | 強化 schema \+ audit hash | 需正規化 | `PredictionRegistry` repo |
| CLV records | 已有 | 90D ≥ 50 樣本，180D ≥ 200 | 樣本量 | 持續 accumulate |
| Backtest reports | `report/mlb_2025_full_backtest.md` 已有 | frontmatter schema 強制 | 多版本散落 | `report/schema.md` \+ lint |
| Live results | 部分 | MLB GUMBO live feed | 缺 streaming | Phase 3，可選 |
| **Park factor** | 無 | Statcast park factor (年更) | **MLB-only 必加** | `MLBAdapter.fetch_park_factors` |
| **Weather** | 無 | NOAA / OpenWeather | **MLB-only 必加 (Coors / Wrigley wind 等)** | `MLBAdapter.fetch_weather` |
| **Umpire** | 無 | Statcast umpire stats | MLB optional, Phase 2 | `UmpireRepository` |
| **Bullpen 狀態** | 無 | 連續出賽天數、近期負荷 | MLB-only | `BullpenStateBuilder` (從 lineup 推) |

### 6.2 Feature Engineering Backlog (MLB-tuned)

評分 1–5；MLB 上 **starting pitcher / bullpen / park / weather** 的權重比 WBC 高很多，下表已調整排序。

| Feature | 來源 | 現可做 | 風險 | 期望幫助 | 驗證 |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Starting pitcher matchup (FIP, xFIP, K/9, BB/9, HR/9)** | FanGraphs / Statcast | 部分 | 中 | **高 (5)** | walk-forward \+ permutation |
| **Statcast pitch-level (xwOBA, barrel%, hard-hit%)** | Baseball Savant | ❌ → ✅ Phase 1 | 中 | **高 (5)** | walk-forward |
| **Bullpen state (連續出賽、累積投球)** | lineup 衍生 | 部分 | 中 | 高 (4) | regime split (high-leverage) |
| **Park factor (場館 × 賽季)** | Statcast park factor | ✅ | 低 | 高 (4) | calibration check |
| **Weather (溫度、風向風速)** | NOAA / OpenWeather | ❌ → Phase 2 | 中 | 中 (3) | Coors/Wrigley split |
| Team Elo (時變, 季內) | 歷史 | ✅ | 低 | 中 (3) | walk-forward Brier |
| Recent form (last-10 / last-30 weighted) | 歷史 | ✅ | 低 | 中 (3) | 同上 |
| Home/Away \+ venue interaction | 賽程 \+ 場館 | ✅ | 低 | 中 (3) | 同上 |
| Rest days / 連戰 / 休息日 | 賽程 | ✅ | 低 | 中 (3) | 同上 |
| Matchup history (隊對隊 last-3y) | 歷史 | ✅ | 低 | 中 (2) | 同上 |
| Lineup quality (打序 1–5 棒 wOBA) | StatsAPI lineups | 部分 | 中 | 中 (3) | calibration |
| Injury / IL indicator (key player) | IL feed | 部分 | 中 | 高 (4) | calibration check |
| Odds movement Δ (T-360 → T-60 → close) | odds\_api | 部分 | 中 | 高 (4) | leakage check (T-60 cutoff) |
| Market disagreement (Pinnacle vs DK/FD) | multi-odds | ❌ → ✅ Phase 1 | 中 | 高 (4) | sharp money signal |
| Reverse line movement (sharp signal) | multi-odds | 部分 | 中 | 中 (3) | Phase 2 |
| No-vig blended implied prob | odds | ✅ | 低 | 高 (4) | calibration |
| CLV-history of model | 自家 CLV | ✅ | 中 | 中 (3) | 防 over-fit |
| Regime state (early / mid / late season; pitcher-heavy / hitter-heavy) | regime\_classifier | ✅ | 中 | 中 (3) | regime split |
| Model confidence calibration | meta | ✅ | 低 | 高 (4) | reliability diagram |
| Volatility / model disagreement | 多模型分歧 | ✅ | 中 | 中 (3) | Brier Decomposition |
| Schedule density (背靠背、19 連戰窗口) | 賽程 | ✅ | 低 | 中 (3) | 同上 |
| Travel / fatigue (時區、跨海岸) | 賽程 \+ 場館位置 | 部分 | 中 | 中 (3) | east-coast → west-coast split |
| Umpire bias (strike zone) | Statcast umpire | ❌ → Phase 2 | 中 | 低 (2) | Phase 2 |

**Hard rule**: 每個特徵入庫前必經 `tests/feature_validation/test_no_lookahead.py` — 假時間 cursor 並 assert 特徵在 cursor 之前的所有 timestamp 才能被讀取。

### 6.3 Model Roadmap (MLB)

#### Phase A — Baseline Validation (Day 0–30)

- 用 MLB 2022–2025 資料跑 baseline 三家 head-to-head：Elo、LR (with no-vig prior)、現有 GBM (`models/gradient_boosting.py`)  
- 樣本 ≥ 1500（MLB regular season 一個半月就足量）  
- 校正 sanity：Brier, log loss, ECE, reliability diagram  
- 寫 `wbc_backend/evaluation/metrics.py` single source of truth  
- **不允許**改模型結構

#### Phase B — Ensemble & Regime (Day 30–90)

- Stacking ensemble (`models/stacking_model.py` 已存在，需用 MLB 全季資料 walk-forward 重訓)  
- Calibration model (Platt / Isotonic) 接在 ensemble 後  
- MLB regime split：early-season (3–4 月，small sample noisy) / mid-season (5–8 月) / late-season \+ 季後賽 (9–10 月)  
- 另一切法：pitcher-dominant matchup vs hitter-dominant  
- Pitcher-aware sub-model：先發投手變更 (scratched start) → 重新預測  
- CLV-aware loss：在 paper bet 上以 CLV bps 為 secondary objective  
- **必經 patch gate \+ human review**

#### Phase C — Online Paper Feedback (Day 90–150)

- Walk-forward \+ paper trading 並行（MLB daily slate 10–15 場，paper sample 累積快）  
- Threshold optimization：confidence × CLV × bankroll constraint × parlay-vs-single  
- Risk-adjusted selection (Kelly fraction × regime × bullpen state)  
- Daily slate exposure cap (e.g. 一日總曝險 ≤ 5% bankroll)  
- **必經 simulation governance**

#### Phase D — Production Proposal (Day 150–180)

- 只在 (i) ≥ **2000** 樣本 (MLB 容易達標) (ii) Brier 下降 CI 95% 顯著 (iii) CLV ≥ \+50 bps CI 90% 顯著 (iv) 通過 regime stability test (各 regime 內單獨 CLV ≥ 0\) (v) human review approved → 發 production proposal  
- **絕不 auto-deploy**

### 6.4 Validation Methodology (Hard rules)

| 檢驗 | 必須 | 工具 |
| :---- | :---- | :---- |
| Time-ordered split (no shuffle) | YES | `wbc_backend/optimization/dataset.py` 強化 |
| Walk-forward (rolling) | YES | `models/walkforward.py` |
| Out-of-sample (last K %) | YES | 同上 |
| Leakage detection (假時間 cursor) | YES | `tests/feature_validation/` 新增 |
| Bootstrap CI (≥ 1000 resample) | YES | `wbc_backend/evaluation/bootstrap.py` 新增 |
| Permutation test | YES | 同上 |
| Calibration (ECE, reliability) | YES | 同 metrics.py |
| Brier \+ Log Loss \+ Hit rate | YES | 同上 |
| ROI \+ drawdown \+ Sharpe | YES | strategy 層 |
| Baseline comparison | YES | 強制 |
| Sample size ≥ 1500 (per CLAUDE.md) | YES | gate 強制 |

**Forbidden** (per HARD RULES)：

- 只看 win rate  
- 單場結果即下結論  
- 用 sandbox 結果稱 production OK  
- 用 \< 1500 樣本下模型結論

---

## 7\. Workstream C — Self-Learning / Simulation Optimization

### 7.1 Simulation Types (10 類)

| \# | 類型 | 目的 | 輸入 | 輸出 |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Historical Replay | 重跑舊資料看 model 行為 | season slice | metrics |
| 2 | Walk-Forward | 滾動 OOS 驗證 | features \+ labels | walk-forward report |
| 3 | Paper Betting | 模擬下注 (不真錢) | predictions \+ odds | ROI/CLV |
| 4 | Odds Movement | 模擬 line movement 對 ROI 影響 | odds timeline | sensitivity |
| 5 | Adversarial Market | sharp money 假設下的 worst-case | shock scenarios | drawdown |
| 6 | Regime Shift | 切 regime 看模型穩定性 | regime labels | regime-split metrics |
| 7 | Confidence Threshold | 不同 threshold → ROI/CLV trade-off | predictions | curve |
| 8 | CLV Accumulation | 不同採樣策略下的 CLV stability | CLV records | distribution |
| 9 | Strategy Risk | Kelly fraction × bankroll × regime | strategy config | ruin prob |
| 10 | Human-Review Proposal | 用模擬結果產生 review proposal | candidate patch | proposal pack |

### 7.2 Simulation Output Schema (`research/simulations/<simulation_id>.json`)

{

  "simulation\_id": "sim\_2026-05-03\_001",

  "type": "walk\_forward",

  "date\_range": \["2024-03-01", "2026-04-30"\],

  "sample\_size": 1850,

  "model\_version": "ensemble\_v0.3.1",

  "feature\_version": "fv\_2026-04-28",

  "strategy\_config": {"kelly\_fraction": 0.25, "min\_edge\_bps": 30},

  "baseline\_metrics": {"brier": 0.241, "ece": 0.052, "clv\_bps": 18},

  "candidate\_metrics": {"brier": 0.232, "ece": 0.041, "clv\_bps": 47},

  "deltas\_with\_ci": {

    "brier\_delta": {"mean": \-0.009, "ci95": \[-0.014, \-0.004\]},

    "clv\_delta\_bps": {"mean": 29, "ci90": \[12, 46\]}

  },

  "drawdown\_max": 0.12,

  "sharpe": 0.93,

  "calibration": {"reliability\_curve": "...", "ece": 0.041},

  "failure\_reason": null,

  "recommendation": "HUMAN\_REVIEW\_REQUIRED",

  "audit\_hash": "sha256:..."

}

`recommendation ∈ {HOLD, INVESTIGATE, COLLECT_MORE_DATA, CANDIDATE_PATCH, HUMAN_REVIEW_REQUIRED}`。

### 7.3 Self-Learning Memory Schema

| Store | 路徑 | 寫入時機 | 主鍵 | Retention |
| :---- | :---- | :---- | :---- | :---- |
| `learning_cycles.jsonl` | `runtime/learning/` | LearningCycleService 完成 | `cycle_id` | 永久 |
| `clv_investigations.jsonl` | 同上 | CLV threshold trigger | `investigation_id` | 永久 |
| `gate_decisions.jsonl` | 同上 | Patch gate 結束 | `decision_id` | 永久 |
| `patch_evaluations.jsonl` | 同上 | candidate evaluated | `patch_id` | 永久 |
| `human_reviews.jsonl` | 同上 | human action | `review_id` | 永久 |
| `simulation_runs.jsonl` | 同上 | simulation 完成 | `simulation_id` | 永久 |
| `failure_patterns.jsonl` | 同上 | failure detected | `pattern_id` \+ `seen_count` | 永久, 去重 |
| `model_versions.jsonl` | 同上 | model 訓出 | `model_version` | 永久 |
| `strategy_versions.jsonl` | 同上 | strategy 變更 | `strategy_version` | 永久 |

#### 防重複 / 防錯誤學習

- 每筆寫入計算 `audit_hash = sha256(canonical_json - audit_hash)`，重複 hash 不寫第二次  
- `failure_patterns.jsonl` 是 upsert（同 `pattern_id` 累加 `seen_count`）  
- 學習層讀記憶時必經 `LearningMemoryRepository.read_validated(...)`，schema 不合直接 raise  
- 任何 cycle 在訓練資料中包含 `audit_hash` ∈ `failure_patterns` 時，必須 mark `tainted=true` 並排除

### 7.4 Simulation Governance

| 邊界 | 規則 |
| :---- | :---- |
| sandbox-only | 所有 simulation 不直接寫 production model |
| paper-only | simulation → paper proposal → human review |
| production-proposal-only | 通過 review 才能升級 |
| no-auto-production-patch | 任何情況都不自動 deploy |
| insight ≠ deploy | simulation 可寫 insight，不可 trigger deploy |

---

## 8\. Workstream D — Scheduler Self-Learning Optimization

### 8.1 任務族 (Task Families)

| Family | 目的 | 預設 cadence | 觸發條件 |
| :---- | :---- | :---- | :---- |
| `data_freshness_check` | 資料新鮮度 | 10 min | always |
| `odds_closing_monitor` | 抓 closing | 賽前 60–0 min | pending fixtures |
| `clv_batch_accumulation` | 累積 CLV | 4h | pending |
| `clv_threshold_check` | 檢查門檻 | event-driven | computed\_count change |
| `production_clv_learning_cycle` | 學習循環 | 24h | LEARNING\_READY |
| `production_clv_investigation` | 調查 | event-driven | threshold hit |
| `simulation_run` | 跑模擬 | weekly | 無高優先 task |
| `model_validation` | 模型驗證 | weekly | new candidate |
| `patch_gate_recheck` | 補跑門檻 | event-driven | computed\_count ≥ 50 |
| `human_review_followup` | 追蹤 review | 24h | review pending |
| `usage_budget_check` | 預算檢查 | 1h | always |
| `audit_guard_check` | Audit 健康 | 6h | always |
| `frontend_health_check` | UI 健康 | 1h | always |
| `architecture_health_check` | 架構健康 | monthly | manual \+ cron |

### 8.2 Decision Logic (deterministic rules)

if usage\_budget\_exceeded:           downgrade external AI calls \+ alert

if audit\_coverage \!= FULL:          block external AI dispatch

if human\_review\_pending \> 0:        no autonomous proposal follow-up

if pending\_clv \> 0:                 prioritize odds\_closing\_monitor

if computed\_count \< 30:             COLLECT\_MORE\_DATA (only)

elif 30 \<= computed\_count \< 50:     rerun investigation, no patch gate

elif computed\_count \>= 50:          allow patch\_gate\_recheck

if frontend\_dashboard\_missing:      open observability task (P1)

### 8.3 Priority Score Formula

priority\_score \=

    w\_impact     \* expected\_impact            \# 0..5

  \+ w\_urgency    \* urgency                    \# 0..5 (deadline-driven)

  \+ w\_freshness  \* data\_freshness\_decay       \# 0..3

  \+ w\_evidence   \* evidence\_threshold\_progress \# 0..3 (CLV samples / 50\)

  \+ w\_failure    \* recent\_failure\_count       \# 0..3

  − w\_cost       \* external\_ai\_cost\_estimate  \# 0..5

  − w\_review     \* human\_review\_pending\_age   \# 0..3

  − w\_risk       \* production\_risk\_score      \# 0..5

  \+ w\_blocked    \* blocked\_duration\_hours     \# 0..3

建議起始權重 `w_*`（皆需 walk-forward 試跑後再調）： `w_impact=3, w_urgency=4, w_freshness=2, w_evidence=2, w_failure=1, w_cost=1, w_review=2, w_risk=3, w_blocked=2`。

#### Ranking Example

| Task | impact | urgency | cost | review\_pending | score |
| :---- | :---- | :---- | :---- | :---- | :---- |
| `clv_threshold_check` (computed\_count=49) | 5 | 4 | 0 | 0 | 高 |
| `production_clv_learning_cycle` | 4 | 2 | 0 | 1 (penalty) | 中 |
| `simulation_run` (weekly) | 3 | 1 | 1 | 0 | 中低 |
| `human_review_followup` (24h pending) | 5 | 5 | 0 | 0 | 最高 |
| Worker external-AI bug-fix | 3 | 3 | 4 | 0 | 中 (cost penalty) |

### 8.4 Scheduler Cadence (MLB-tuned)

MLB daily slate 通常 10–15 場、賽程從台北時間早上 7 點到隔日早上 5 點，scheduler 必須 **24/7 active during season**。

| 週期 | 動作 |
| :---- | :---- |
| 10 min | worker tick \+ health check \+ freshness scan |
| 10 min | **odds snapshot (賽前 6h 內各場)** — MLB 並發度高，10 min 更積極 |
| 30 min | **lineup detection** (MLB 賽前 1–2h 公布，scratched start 立即觸發 reprediction) |
| 20 min | closing monitor (賽前 30–0 min) |
| 1 h | usage budget check, frontend health, weather refresh |
| 4 h | fast CLV batch check if pending |
| 6 h | audit guard self-test |
| daily (台北時間 11:00) | **slate planning**：列出今日 MLB 比賽、預跑 features、預計算 confidence |
| daily (台北時間 隔日 06:00) | CLV accumulation summary, ops report, runbook |
| weekly (週一) | simulation\_run, model\_validation, regime drift check |
| monthly | architecture\_health\_score |
| event-driven | threshold crossing, scratched start, postponement (rain), human review state change |

### 8.5 Scheduler Safety Invariants (assert each tick)

1. `assert not planner.invoked_external_ai_in_last_tick`  
2. `assert auditguard.coverage == "FULL" before allowing external-AI`  
3. `assert deterministic_tasks scheduled ≥ external_ai_tasks`  
4. `assert budget_remaining_today > 0 or external_ai_disabled`  
5. `assert no production-impacting task without review_id reference`

任一條 fail：scheduler 必須 self-pause 並寫 `safety_violation.jsonl`。

---

## 9\. Workstream E — Usage Budget / Copilot Cost Governance

### 9.1 Budget Schema

{

  "budget\_version": "2026-05-03-v1",

  "global\_daily\_usd": 10.00,

  "global\_weekly\_usd": 50.00,

  "by\_role": {

    "planner":  {"daily\_usd": 0.00, "hard\_cap": true},

    "worker":   {"daily\_usd":  6.00},

    "cto\_review": {"daily\_usd": 2.00},

    "human\_assist": {"daily\_usd": 2.00}

  },

  "by\_provider": {

    "anthropic":     {"daily\_usd": 5.00},

    "openai\_codex":  {"daily\_usd": 3.00},

    "github\_copilot":{"daily\_usd": 2.00}

  },

  "per\_task\_max\_usd": 0.50,

  "warn\_threshold\_pct": 70,

  "critical\_threshold\_pct": 90,

  "spike\_z\_score\_warn": 3.0

}

### 9.2 Guard Policy

| Event | Action |
| :---- | :---- |
| Planner external-AI attempt | **CRITICAL**, deny \+ alert \+ write `safety_violation.jsonl` |
| Worker \> per\_task\_max | deny \+ downgrade to deterministic fallback |
| Provider \> daily | switch to fallback provider |
| Global \> warn\_threshold | warn in usage dashboard |
| Global \> critical | hard-stop external AI for the day, deterministic only |
| Spike z-score \> 3 | warn (might indicate runaway loop) |

### 9.3 Frontend Card Requirement

`runtime/agent_orchestrator/frontend/index.html` 增加 `Usage Budget` panel：

- 今日總用量 / budget bar  
- 各 provider breakdown（沿用既有）  
- 各 role breakdown  
- 警告徽章（warn / critical）  
- "Planner external AI \= 0" 永遠顯示為 invariant 標誌（紅燈一亮即 incident）

### 9.4 Scheduler Behavior After Budget Exceeded

1. 立即 disable 所有「需外部 AI」任務的 dispatch  
2. 把這些任務 requeue 為 `deferred=true`，下個 budget cycle 才 retry  
3. Planner 改用 deterministic fallback 產 next task  
4. 寫 `usage_budget_event.jsonl`  
5. 發通知 (Telegram bot read-only channel)

---

## 10\. Phase Plan (詳細交付)

> 2026-05-07 CTO update：下表保留 180 天 long-term phase plan；短期執行排序以 §0A.4 為準。Phase69 / Phase70 是插入在 Phase 0/1 之前的 evidence-driven detour，用來決定是否值得進 calibration / probability shaping paper-only patch gate。

| Phase | Days | Objective | Key Tasks | Deliverables | Success Criteria | Risk |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Phase 0 — Stabilize** | 0–14 | Audit/Budget Guard 上線、MLB/WBC 術語釐清、Planner invariant assert | Glossary、Budget Schema、Planner external-AI assertion、`safety_violation.jsonl`、UI Budget panel | `docs/glossary/league_codes.md`、`orchestrator/budget_guard.py`、UI patch | Planner 0 ext-AI hits / 7d；UI 上線；Glossary review pass | UI cycle 干擾使用者 |
| **Phase 1 — Foundation** | 15–45 | LeagueAdapter 介面、`MLBAdapter` 包覆既有 mlb 資料、CLV ≥ 50 累積、Brier/ECE baseline (MLB 2022–2025) | `wbc_backend/league/`、metrics SSOT、`MLBAdapter` 抓取、PredictionState enum | `wbc_backend/league/{base,mlb_adapter,wbc_adapter}.py`、`wbc_backend/evaluation/metrics.py`、`docs/data/mlb_inventory.md` | CLV ≥ 50；ECE baseline 文件化；MLB walk-forward sample ≥ 1500；no behavior change | MLB StatsAPI / Statcast rate limit |
| **Phase 2 — Validation** | 46–90 | Walk-forward 全面化、Feature Registry (含 starting pitcher / park / weather)、Simulation Framework | `wbc_backend/features/registry.py`、`research/simulations/`、`wbc_backend/evaluation/bootstrap.py`、`MLBAdapter.fetch_park_factors`/`fetch_weather` | walk-forward report (≥1500 樣本)、simulation runner v1、feature versioning | Brier ↓ CI95 顯著；feature lookahead test 全綠；MLB pitcher-feature 上線 | weather provider SLA |
| **Phase 3 — Self-Learning** | 91–150 | Ensemble \+ Calibration \+ Regime (early/mid/late MLB season) \+ 排程 priority-scored、threshold feedback loop、scratched-start reprediction | `models/ensemble.py` walk-forward retrain、`models/calibration.py`、`scheduler/priority.py`、`scheduler/lineup_event_handler.py` | `gate_decisions.jsonl` enriched、scheduler v2 | ECE ≤ 0.05；scheduler safety invariants 100%；scratched-start 自動 re-predict | over-fit、weight tuning 不收斂 |
| **Phase 4 — Production-Proposal Loop** | 151–180 | 完整 review-driven 提案流程、ROI/CLV stable on MLB daily slate、architecture audit | review queue UI、proposal pack、arch health score、daily-slate exposure cap | `docs/architecture/health_2026-Q3.md`、stable proposal pipeline | CLV ≥ \+50 bps CI90 (MLB 全季)；review SLA \< 12h；regime-split CLV ≥ 0 | human review 帶寬不足 |

---

## 11\. Metrics & Acceptance Criteria

### 11.1 Prediction Metrics (model layer)

- **Brier score**: 必跑、CI95 報告、目標 90D −0.005、180D −0.015  
- **Log loss**: 同上  
- **ECE (Calibration)**: 90D ≤ 0.05、180D ≤ 0.03  
- **Reliability diagram**: 每次 simulation 必出  
- **Hit rate**: 報告但不單獨作為 success  
- **Sample size**: ≥ 1500 (硬門檻)，Bootstrap ≥ 1000 resample

### 11.2 Strategy Metrics

- **CLV bps**: 90D ≥ \+50 (CI90)、180D ≥ \+80 (CI95)  
- **ROI**: 報告，並要求 ≥ 0 才能 propose  
- **Max drawdown**: ≤ 20% bankroll  
- **Sharpe**: 報告

### 11.3 Governance / System Metrics

- **Audit coverage**: FULL，缺一即 critical  
- **Usage cost vs budget**: ≤ 70% (180D)  
- **Scheduler task success rate**: ≥ 99% (180D)  
- **Human review pending**: median age \< 12h  
- **Planner external-AI calls**: 0 (never)  
- **Architecture health score**: 0–100，180D ≥ 75

### 11.4 Acceptance Gates

1. `LEARNING_READY` → 必須 ≥ 50 CLV 樣本  
2. `PATCH_GATE_RECHECK` → 必須 walk-forward \+ bootstrap CI 顯著  
3. `PROPOSAL_DRAFTED` → 必須 audit hash \+ simulation\_id  
4. `HUMAN_REVIEW_APPROVED` → 必須兩位 reviewer 簽核（至少一位非作者）  
5. `DEPLOYED` (production) → 本計畫期內 **不啟用**，僅產 proposal

---

## 12\. 30 / 60 / 90 / 180 Day Roadmap (Crisp View)

### 30 Days — Stabilize \+ Foundation kickoff

- Glossary（MLB 為主、WBC 為輔）落地  
- Budget Guard \+ UI panel 上線  
- Planner external-AI invariant assertion \+ alert  
- `LeagueAdapter` 介面 \+ `MLBAdapter`（主）/ `WBCAdapter`（輔）包覆  
- CLV daily monitoring runbook 強化（已有 Phase35 基礎）  
- MLB 資料源盤點文件 (`docs/data/mlb_inventory.md`)  
- `wbc_backend/evaluation/metrics.py` SSOT  
- Scheduler health check task

### 60 Days — Validation

- Walk-forward 全 model family 用 MLB 2022–2025 跑過（樣本 ≥ 1500，目標 5000+）  
- Feature registry \+ lookahead test gate  
- 加入 MLB 核心特徵：starting pitcher、park factor、bullpen state  
- Simulation framework v1（10 種 simulation type 至少 3 種上線：Walk-forward / Paper / Threshold）  
- First production paper-learning loop on MLB daily slate（不 deploy）  
- CLV samples ≥ 50（MLB 高頻容易達標）

### 90 Days — Self-learning core

- Ensemble \+ Calibration \+ MLB regime classifier (early/mid/late season) 進入 walk-forward 結果  
- Threshold-based feedback loop（每週滾動）  
- Scheduler priority-score v1 上線，含 lineup-event-driven re-prediction  
- Brier ↓ CI95 顯著  
- Weather feature 接上 (Phase 2 末端)

### 180 Days — Robust governance

- Stable MLB production proposal workflow  
- Human-review-assisted model governance  
- Robust CLV / ROI tracking \+ daily-slate drawdown caps  
- Automated architecture health scoring  
- Long-term MLOps governance baseline  
- WBC 資產作為跨聯盟 feature（spring training 預測 MLB 開季）已可選用

---

## 13\. Prioritized Backlog (Top 25\)

> 2026-05-07 CTO override：本表是原 180 天 backlog。今日與本週的實際 P0/P1/P2 已在 §0A.4 重新排序；在 Phase69 完成前，不啟動新的 feature-family patch route。

| Rank | Item | Workstream | Effort | Deterministic? |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Glossary `league_codes.md` (MLB 主 / WBC 輔) | A | XS | YES |
| 2 | Budget Guard schema \+ `orchestrator/budget_guard.py` | E | M | YES |
| 3 | Planner external-AI invariant assertion | E | S | YES |
| 4 | UI Budget panel \+ critical badge | E | S | YES |
| 5 | `wbc_backend/league/base.py` \+ `MLBAdapter` 包覆既有 mlb 資料 | A | M | YES |
| 6 | `wbc_backend/evaluation/metrics.py` SSOT | A/B | M | YES |
| 7 | `tests/feature_validation/test_no_lookahead.py` | B | M | YES |
| 8 | MLB Data Inventory doc (`docs/data/mlb_inventory.md`) | B | S | YES |
| 9 | `PredictionState` state machine | A | M | YES |
| 10 | `LearningMemoryRepository` (取代直接 JSON 讀寫) | A/C | M | YES |
| 11 | Walk-forward harness 統一化 (用 MLB 2022–2025) | B | L | YES |
| 12 | Feature Registry \+ versioning | B | M | YES |
| 13 | Bootstrap CI utility | B | S | YES |
| 14 | Simulation runner v1 (Walk-forward \+ Paper, MLB daily slate) | C | L | YES |
| 15 | `failure_patterns.jsonl` 防重複學習 | C | M | YES |
| 16 | Scheduler priority-score v1 | D | M | YES |
| 17 | Scheduler safety invariants assertion | D | S | YES |
| 18 | Audit dashboard (frontend) | A/E | M | YES |
| 19 | Starting pitcher feature builder（MLB \#1 訊號） | B | M | YES |
| 20 | Park factor \+ Statcast park 資料接入 | B | M | YES |
| 21 | Bullpen state feature builder | B | M | YES |
| 22 | Lineup-event-driven re-prediction (scratched start) | D | M | YES |
| 23 | Ensemble walk-forward retrain on MLB | B | L | YES |
| 24 | Calibration (Platt/Isotonic) on MLB | B | M | YES |
| 25 | MLB Regime classifier (early/mid/late) | B | M | YES |
| 26 | Weather feature 接 NOAA / OpenWeather | B | L | YES |
| 27 | Patch gate enrichment \+ audit hash | C | M | YES |
| 28 | Review queue SLA tracker | A | S | YES |
| 29 | Architecture health score script | A | M | YES |
| 30 | `WBCAdapter` 重構為 cross-league 輔助資料源 | A | S | YES |

---

## 14\. First 10 Recommended Tasks (執行明細)

> 2026-05-07 CTO override：以下 T1-T10 保留為 governance / architecture backlog，但不再是今日開工順序。今日第一個執行 prompt 見 §0A.6。

### T1 — Glossary `league_codes.md`（MLB 為主、WBC 為輔）

- **Why now**: 整份計畫的命名歧義來源；codebase 上的 `wbc_backend/` 是歷史命名，但目標 league 是 MLB，需要明文記錄  
- **Expected impact**: 高（避免 architecture wrong-direction）  
- **Target files**: `docs/glossary/league_codes.md`（新增）；`README.md`（加註）  
- **Acceptance**: 文件含 (i) MLB \= Major League Baseball (primary target) (ii) WBC \= World Baseball Classic (auxiliary, cross-league feature) (iii) `wbc_backend/` package 為歷史命名說明，不會 rename (iv) 使用者於 review meeting 簽核  
- **Effort**: XS（\< 0.5 day）  
- **Mode**: Deterministic, planner-authored

### T2 — Budget Guard

- **Why now**: 沒有 guard 之前任何 worker bug 都可能燒錢  
- **Expected impact**: 高  
- **Target files**: `orchestrator/budget_guard.py`（新增）、`runtime/agent_orchestrator/budget_config.json`、`tests/test_budget_guard.py`  
- **Acceptance**: pytest 覆蓋 deny path、warn/critical 觸發、provider fallback；planner external-AI assertion 一被觸發即寫 `safety_violation.jsonl`  
- **Effort**: M（2–3 day）  
- **Mode**: Deterministic

### T3 — Planner External-AI Invariant

- **Why now**: hard rule 要求，但目前無 runtime assertion  
- **Expected impact**: 高（governance）  
- **Target files**: `orchestrator/planner_tick.py`、`orchestrator/budget_guard.py`、`tests/test_planner_invariant.py`  
- **Acceptance**: 任何 planner code path 上 assert `provider != external`；測試模擬 misconfig 必觸發 critical  
- **Effort**: S（1 day）  
- **Mode**: Deterministic

### T4 — UI Budget Panel

- **Why now**: 視覺化才會被注意到  
- **Expected impact**: 中高  
- **Target files**: `runtime/agent_orchestrator/frontend/index.html`  
- **Acceptance**: 顯示 daily/weekly bar、provider/role breakdown、Planner=0 invariant badge、warn/critical 顏色  
- **Effort**: S（1 day）  
- **Mode**: Deterministic

### T5 — `LeagueAdapter` 骨架 \+ `MLBAdapter`（主） \+ `WBCAdapter`（輔）包覆

- **Why now**: 未來所有資料 / 規則 / odds 都要走這層；MLB 是主預測對象，WBC 是輔助  
- **Expected impact**: 高（架構基石）  
- **Target files**: `wbc_backend/league/base.py`（新增）、`wbc_backend/league/mlb_adapter.py`（新增，包覆 `data/mlb_2024_pitchers.py`、`data/mlb_2025_preview.py`、`data/odds_api_client.py`）、`wbc_backend/league/wbc_adapter.py`（新增，包覆 `wbc_backend/pipeline/wbc_rule_engine.py`）、`tests/architecture/test_league_adapter.py`  
- **Acceptance**: (i) 既有 MLB 與 WBC pipeline 行為不變 (ii) `LeagueAdapter` Protocol 完整 (iii) `MLBAdapter` 至少實作 `list_fixtures` / `fetch_results` / `fetch_odds_open` / `fetch_odds_closing` / `fetch_lineups` / `fetch_park_factors` (iv) test 強制 import 路徑、禁止跨 adapter 直接 import 對方資料源  
- **Effort**: M（3 day）  
- **Mode**: Deterministic

### T6 — Metrics SSOT

- **Why now**: 多份 KPI 計算分散造成數字打架  
- **Expected impact**: 高  
- **Target files**: `wbc_backend/evaluation/metrics.py`（新增 / 整併）、`wbc_backend/evaluation/bootstrap.py`、所有 caller import  
- **Acceptance**: Brier、Log loss、ECE、reliability、CLV bps 一處實作；測試 ≥ 95% line cov  
- **Effort**: M（2 day）  
- **Mode**: Deterministic

### T7 — `test_no_lookahead.py`

- **Why now**: data leakage 是模型 silent killer  
- **Expected impact**: 高  
- **Target files**: `tests/feature_validation/test_no_lookahead.py`、`wbc_backend/features/builder.py`（加 hooks）  
- **Acceptance**: 假時間 cursor 下，所有 feature 只能讀 ≤ cursor 的時間戳；故意造一個 leak case 必須 fail  
- **Effort**: M（2 day）  
- **Mode**: Deterministic

### T8 — MLB Data Inventory Doc

- **Why now**: 確認所有 MLB 資料管線（StatsAPI / Statcast / FanGraphs / Odds API）的可得性、SLA、rate limit、credential 狀態，是後續所有 feature 工程的前置  
- **Expected impact**: 高  
- **Target files**: `docs/data/mlb_inventory.md`  
- **Acceptance**: 對齊 §6.1 表格；每個 slot 列出 (i) provider / endpoint (ii) auth / credential 來源 (iii) 抓取頻率 / rate limit (iv) cost (v) 既有 codebase 中對應檔案 (vi) 缺口 (vii) Phase 落點  
- **Effort**: S（1 day, 文件）  
- **Mode**: Deterministic

### T9 — `PredictionState` State Machine

- **Why now**: 解耦 if/else，後續 review queue / patch gate 都要靠它  
- **Expected impact**: 中高  
- **Target files**: `wbc_backend/state_machine/prediction_state.py`、`wbc_backend/state_machine/transitions.py`、`tests/test_prediction_state.py`  
- **Acceptance**: 所有 transition table 化；非法 transition raise；既有 caller 漸進改 (feature flag)  
- **Effort**: M（3 day）  
- **Mode**: Deterministic

### T10 — `LearningMemoryRepository`

- **Why now**: 直接讀寫 `training_memory.json` 是高風險耦合  
- **Expected impact**: 高  
- **Target files**: `runtime/learning/repository.py`（新增）、`tests/test_learning_memory_repo.py`  
- **Acceptance**: schema validation、append-only、audit hash、ducplication detection；既有 caller 改用 repo（feature flag）  
- **Effort**: M（2 day）  
- **Mode**: Deterministic

---

## 15\. Final Recommendation

### 15.1 目前最該做的（接下來兩週）

1. **Phase69 先行**：執行 calibration objective redesign counterfactual，針對 `logit/0.85`、`away_wp*0.9`、OOF isotonic / Platt、abstention diagnostic 做 PIT-safe / OOF 驗證。  
   理由：Phase59-68 已把問題收斂到 model architecture / probability shaping；這比泛架構工作更接近當前 failure 的決策點。  
2. **Phase70 只在 Phase69 promising 時開 gate**：依 Phase69 結論選 calibration objective、probability shaping removal、ensemble weighting 或 abstention guard 的 paper-only patch gate。  
   理由：避免在 feature-family 路線已降級後又開新 patch search。  
3. **治理鏈改為本週 P1**：Budget Guard、Planner external-AI invariant、Metrics SSOT 仍需做，但排在 Phase69 後。  
   理由：這些是長期安全基礎，不應阻塞 deterministic paper-only counterfactual。

### 15.2 暫時不該做的

- ❌ 改動 production model（hard rule）  
- ❌ 將 Phase69 counterfactual 結果直接套進 production  
- ❌ 重啟 bullpen / SP fatigue / market / context feature-family patch gate  
- ❌ 在 sample \< 1500 時調整 ensemble 結構  
- ❌ 把 root `models/` / `strategy/` 直接 `git mv`（會炸掉 import）  
- ❌ 升級 persistence 到 Postgres（90 天後再評估）  
- ❌ 上線新 simulation type（先把 walk-forward / paper 兩種做穩）  
- ❌ 把 Planner 換成 LLM-driven（永久 hard rule）

### 15.3 最大風險 (Top-3)

1. **counterfactual 重建誤差** — Phase56 artifact 有 final probabilities，但 individual sub-model probabilities 不完整，移除 `logit/0.85` / `away_wp*0.9` 可能需要重跑或近似重建。緩解：Phase69 必須記錄 artifact alignment、coverage 與 DATA_LIMITED 條件。  
2. **calibration overfit** — Phase59-Pre+ 已證明 local isotonic / Platt 不能直接視為解法。緩解：Phase69 強制 OOF / rolling monthly / PIT-safe，不允許 in-sample fit-and-evaluate。  
3. **full regression 噪音污染判讀** — 目前 full suite 仍有 31 個既有 failed。緩解：Phase69 以新增 tests + Phase67/68 targeted regression 為主，31 failed 獨立列 tech debt。

### 15.4 下一個兩週行動計畫

| Day | Action | Owner | Output |
| :---- | :---- | :---- | :---- |
| D1 | Phase69 module / runner / report skeleton | Worker | `phase69_calibration_objective_redesign_counterfactual.py` |
| D2 | variants + segmentation + metrics implementation | Worker | JSON diagnostic draft |
| D3 | OOF / PIT-safe calibration + negative controls | Worker | tests + report sections |
| D4 | Phase67/68 targeted regression + CTO readout | Worker / CTO | Phase69 gate conclusion |
| D5 | Phase70 prompt only if Phase69 promising | CTO | Phase70 paper-only gate prompt |
| D6-D7 | Metrics SSOT extraction from Phase69/68 reused utilities | Worker | shared metrics tests |
| D8-D9 | Budget Guard + Planner external-AI invariant | Worker | budget/invariant tests |
| D10 | full regression 31 failed triage | Worker | tech debt report |
| D11-D12 | LeagueAdapter skeleton only if Phase69 path is not blocked | Worker | no-behavior-change adapter |
| D13 | roadmap v1.1 alignment review | CTO | updated roadmap |
| D14 | Phase0/Phase69 retrospective | All | retrospective notes |

---

## 16\. Hard-Rule Compliance Matrix

| Hard Rule | 本計畫遵守方式 |
| :---- | :---- |
| 不直接修改 production model | 全計畫只產 proposal，T11+ 才到 review |
| 不建立 production patch | 同上 |
| 不跳過 human review | Phase 4 才開 review-driven loop |
| 不用 sandbox 結果稱 production OK | metrics SSOT \+ sample-size gate |
| 不用小樣本下結論 | ≥ 1500 樣本 hard gate |
| Planner 不呼叫外部 AI | T3 runtime assertion |
| 新增外部 AI 必經 AuditGuard | Workstream E \+ scheduler invariant |
| 不呼叫真實 Codex/Claude/Copilot/GitHub | 本文件作者為 deterministic planner，完全未呼叫 |
| 計畫為主，不改 runtime 行為 | 是 |

---

## 17\. Open Questions (留給使用者 / Reviewer)

1. ~~WBL 真實對應到哪個聯盟？~~ **已釐清：MLB**  
2. MLB 主要 odds provider 鎖定哪幾家？(建議 Pinnacle \+ Circa \+ DK \+ FD，至少 3 家做 spread)  
3. Statcast / FanGraphs API key 是否已申請？credential 收容方式？  
4. 預算上限要設多少？（§9.1 的 `10/50/USD` 只是建議起點）  
5. Human review 由幾人 panel 簽核？兩人是否強制非作者？  
6. Telegram bot 是否要用作 review 通知 channel？  
7. Persistence 升級 SQLite/Postgres 的時點 — 90 天後評估還是 60 天？  
8. 是否允許 weekly simulation\_run 進入下一個 cycle 的 training data？（目前預設：否，僅做 insight）  
9. MLB 賽季外（11–2 月）排程如何降頻？是否做 winter meeting 期間的 trade impact 模擬？  
10. WBC 資產（既有 wbc\_backend/）要保留多少？建議：保留 \+ 重構為 cross-league feature，不刪除

---

## 18\. Verification Statement

本文件已涵蓋所有要求段落，並通過下列自我檢查：

- [x] Executive Summary  
- [x] Current System Assessment  
- [x] Target Architecture  
- [x] Long-term Roadmap  
- [x] Phase Plan (含表格 \+ 風險)  
- [x] Workstream A — System Architecture  
- [x] Workstream B — Prediction Accuracy  
- [x] Workstream C — Self-learning / Simulation  
- [x] Workstream D — Scheduler self-learning  
- [x] Workstream E — Usage Budget / Cost Governance  
- [x] Metrics \+ Acceptance Criteria  
- [x] 30 / 60 / 90 / 180-day Roadmap  
- [x] Prioritized Backlog  
- [x] First 10 Recommended Tasks（含 acceptance criteria 與 deterministic/LLM 標註）  
- [x] Final Recommendation  
- [x] Hard-rule compliance matrix  
- [x] WBL 名詞釐清（已確認 \= MLB 大聯盟；計畫已 MLB-tuned）

---

**LONG\_TERM\_WBL\_OPTIMIZATION\_PLAN\_VERIFIED**  
這份長期計畫品質不錯，而且方向有對齊你目前的系統狀態。可以判定：

LONG_TERM_WBL_OPTIMIZATION_PLAN_VERIFIED ✅

但我會建議你不要直接照單全收全部同時開做，而是把它收斂成下一階段的執行主線。這份計畫已經釐清 WBL 其實是 MLB，並指出目前 repo 已有 data/mlb_2024_pitchers.py、data/mlb_2025_preview.py、report/mlb_2025_full_backtest.md、docs/mlb_2025_historical_odds_timeline_asset_spec.md 等 MLB 基礎資產，所以不是從零開始，而是要把 MLB 資料層、回測層、CLV 與治理流程正規化。

我對這份計畫的判斷

最有價值的部分是這三條主線：

主線	判斷
MLB / WBC 名詞釐清	很重要，必須先做
LeagueAdapter / MLBAdapter	正確，但不要一開始大規模搬檔
Usage Budget Guard	應該優先，因為你已經遇到 Copilot 用量過高

這份文件裡也正確指出，Planner 必須永遠 deterministic，Worker 才能在 policy allow 下使用外部 AI，且所有外部 AI / GitHub 呼叫都要經過 AuditGuard。這跟你目前的 Provider Safety / Usage Detail UI / Audit Guard 主線一致。

但有幾個地方要修正或保守看待

第一，文件把「CLV ≥ 50」跟「LEARNING_READY」混在一起的風險要注意。你目前系統已經在 Phase 29 後達成 LEARNING_READY，因為 production CLV 已有 14 筆 COMPUTED；但 patch gate 或 production proposal 才需要更高樣本，例如 50 或 1500。建議文字改成：

LEARNING_READY：>= 1 production COMPUTED CLV 可啟動 paper learning
PATCH_GATE_RECHECK：>= 50 production COMPUTED CLV
MODEL_EFFECTIVENESS_CLAIM：>= 1500 OOS / walk-forward samples

第二，1500 樣本 hard gate 適合模型有效性宣稱與 walk-forward 結論，但不適合每一個小功能都卡 1500。否則 daily CLV learning 會被卡死。應該分層：

14 筆：只能 observation / investigation
50 筆：可 patch gate recheck
500 筆：可 regime 初步分析
1500 筆：可宣稱模型改動有效性

第三，Budget Schema 用 USD 估算可以當設計，但 Copilot / Claude Code 的額度常常不是單純 USD 模型，所以要同時追：

calls
premium_requests
input_tokens
output_tokens
cached_tokens
rate_limit_hit
blocked_attempts
provider-specific quota text

也就是不要只做 daily_usd，要做「quota unit」混合治理。

我建議下一步不要直接做 T5 LeagueAdapter

雖然計畫把 T5 LeagueAdapter 排得很前面，但以你目前痛點來看，最優先應該是：

Phase 36 — Usage Budget Guard / Copilot Cost Control

原因是你剛剛才補完 Usage Detail UI，也確認 Copilot / Claude 使用量需要被看見。下一步應該讓系統「超量時自動控管」，而不是只顯示。

下一個可以給 Agent 的 prompt
# ROLE
You are a senior AI usage-governance and orchestrator safety engineer.

# OBJECTIVE
Implement Phase 36: Usage Budget Guard / Copilot Cost Control.

The long-term MLB optimization plan is complete and recommends Usage Budget Guard as the immediate governance priority.

Current state:
- Usage logging exists.
- AuditGuard exists.
- Usage Detail UI exists.
- Frontend shows Planner / Worker / CTO usage and provider breakdown.
- Browser runtime verification passed.
- Worker currently shows Copilot-Daemon / Claude usage.
- Planner external attempts are blocked.

Now implement deterministic usage budget controls so excessive Copilot / Claude / Codex / GitHub usage is warned, throttled, or blocked.

---

# GOAL

Create a budget guard that answers:

1. How much usage occurred today / last 24h / all-time?
2. Which role consumed usage?
3. Which provider consumed usage?
4. Did any role or provider exceed warning threshold?
5. Did any role or provider exceed hard cap?
6. Should Worker external AI be allowed, throttled, or disabled?
7. Should Planner / CTO external attempts be treated as critical?
8. Should scheduler downgrade to deterministic safe tasks?

---

# TASK 1 — Budget config

Create:

runtime/agent_orchestrator/usage_budget_config.json

Default schema:

{
  "version": "2026-05-03-v1",
  "enabled": true,
  "window": "24h",
  "roles": {
    "planner": {
      "max_allowed_external_calls": 0,
      "severity_on_any_allowed": "CRITICAL",
      "hard_cap": true
    },
    "cto": {
      "max_allowed_external_calls": 0,
      "severity_on_any_allowed": "CRITICAL",
      "hard_cap": true
    },
    "worker": {
      "warn_calls": 20,
      "critical_calls": 40,
      "hard_cap_calls": 60
    }
  },
  "providers": {
    "github-copilot": {
      "warn_calls": 20,
      "critical_calls": 40,
      "hard_cap_calls": 60
    },
    "claude": {
      "warn_calls": 10,
      "critical_calls": 20,
      "hard_cap_calls": 30
    },
    "codex": {
      "warn_calls": 5,
      "critical_calls": 10,
      "hard_cap_calls": 15
    }
  },
  "tokens": {
    "warn_input_tokens": 3000000,
    "critical_input_tokens": 6000000,
    "hard_cap_input_tokens": 9000000
  },
  "blocked_attempts": {
    "warn": 5,
    "critical": 10
  }
}

Do not use USD only. Track calls, tokens, blocked attempts, premium requests, rate limit events.

---

# TASK 2 — Budget evaluator

Create:

orchestrator/usage_budget_guard.py

Implement:

load_budget_config()
evaluate_usage_budget(hours=24)
is_provider_allowed(role, provider)
get_budget_summary()

Return:

{
  "budget_status": "OK|WARN|CRITICAL|HARD_CAP",
  "roles": {...},
  "providers": {...},
  "tokens": {...},
  "warnings": [...],
  "critical_alerts": [...],
  "hard_cap_triggered": true/false,
  "recommended_scheduler_mode": "NORMAL|DETERMINISTIC_ONLY|PAUSE_EXTERNAL_AI",
  "allowed_external_providers": [...]
}

Rules:
- Planner allowed external call > 0 = CRITICAL.
- Planner external attempt blocked > 0 = WARN.
- CTO allowed external call > 0 = CRITICAL.
- Worker over warn_calls = WARN.
- Worker over critical_calls = CRITICAL.
- Provider over hard cap = HARD_CAP.
- Any rate_limit_hit = WARN or CRITICAL depending provider.
- If HARD_CAP, external Worker calls are not allowed.

---

# TASK 3 — Integrate with ProviderFactory / execution policy

Before Worker external AI dispatch:

1. Check existing ProviderFactory / execution_policy.
2. Check usage_budget_guard.is_provider_allowed(role, provider).
3. If budget guard denies:
   - do not execute subprocess
   - write audit BLOCKED
   - write usage blocked record
   - reason = USAGE_BUDGET_HARD_CAP
   - scheduler should prefer deterministic safe task

Do not weaken existing AuditGuard.

---

# TASK 4 — Scheduler integration

In planner_tick / scheduler decision:

If budget_status = HARD_CAP:
- do not create external-AI-required tasks.
- prefer deterministic tasks:
  - clv_batch_accumulation
  - clv_threshold_check
  - production_clv_investigation
  - usage_budget_check
  - audit_guard_check
  - frontend_health_check

If budget_status = CRITICAL:
- allow only high-priority external Worker tasks if explicitly policy-allowed.
- otherwise defer.

If budget_status = WARN:
- show warning but do not block.

---

# TASK 5 — Frontend / Decision Card integration

Add Usage Budget section to:

- ops_decision_card.py
- runtime/agent_orchestrator/frontend/index.html
- /api/orchestrator/summary if needed

Show:

## Usage Budget

- Budget status
- Worker calls today / threshold
- Copilot-Daemon calls today / threshold
- Claude calls today / threshold
- Planner allowed external calls
- CTO allowed external calls
- blocked attempts
- token usage
- recommended scheduler mode

Warnings:
- ⚠️ Copilot usage high
- ⚠️ Claude usage high
- 🚨 Planner external AI allowed call detected
- 🚨 Usage hard cap reached — external AI paused

---

# TASK 6 — CLI

Create:

scripts/usage_budget_check.py

Commands:

python3 scripts/usage_budget_check.py --hours 24
python3 scripts/usage_budget_check.py --json
python3 scripts/usage_budget_check.py --provider github-copilot
python3 scripts/usage_budget_check.py --role worker

---

# TASK 7 — Tests

Add tests:

1. Planner allowed external call => CRITICAL.
2. Planner blocked attempts => WARN.
3. Worker below threshold => OK.
4. Worker over warn => WARN.
5. Worker over critical => CRITICAL.
6. Provider hard cap => HARD_CAP.
7. hard cap blocks Worker subprocess.
8. blocked by budget writes audit BLOCKED.
9. blocked by budget writes usage blocked record.
10. scheduler chooses deterministic-only mode under hard cap.
11. Decision Card renders Usage Budget.
12. Frontend renders Usage Budget section.
13. malformed config falls back safely.
14. missing config creates default config.
15. No real Codex / Claude / Copilot / GitHub call occurs in tests.

---

# HARD RULES

- Do not call real external AI.
- Do not reset usage logs.
- Do not hide usage records.
- Do not weaken AuditGuard.
- Do not allow Planner external AI.
- Do not block deterministic safe tasks.
- Do not use USD-only budgeting.
- Do not mutate production model.

# SUCCESS CRITERIA

Return final status:

PHASE_36_USAGE_BUDGET_GUARD_VERIFIED

Only if:
- budget config exists
- budget evaluator works
- Worker external calls can be blocked by hard cap
- Planner / CTO external calls are critical
- Decision Card / UI show budget status
- tests pass

我會把 Phase 36 放在所有模型優化之前，因為這是你目前實際遇到的痛點：Copilot / Claude 用量可見，但尚未被治理。
