# MLB Roadmap Problem Convergence Plan

**Document ID:** `mlb_roadmap_problem_convergence_plan_2026-05-04`
**Date:** 2026-05-04
**Phase:** 40
**Author:** AI Architect (Planner-mode, deterministic; no external AI called)
**Primary Source:** `00-Plan/betting_roadmapplan_20260504.md` (Revision 2 — WBL → MLB)
**Scope:** Betting-pool / MLB 預測系統 — 整合 Phase 36–39 完成工作，收斂 roadmap 至下一可執行序列
**Governance:** Plan-only document. 不觸發任何 production patch、不繞過 BSS Safety Gate、不呼叫外部 AI。

---

## 1. Executive Summary

### 1.1 系統現況一句話

Betting-pool MLB 預測系統已從「單機跑模型」演進至**治理成熟 (governance-mature)** 狀態：Usage Budget Guard 已上線（Phase 36）、Planner external-AI invariant 已驗收（Phase 36A）、BSS 負向根因已稽核（Phase 37）、資料清洗與校準修復預覽已完成（Phase 38）、per-game 預測機率持久化管線已建立（Phase 39）。

### 1.2 五個關鍵事實

| 事實 | 狀態 |
|------|------|
| MLB 為主要預測目標（WBC 為輔助） | ✅ 已確認（roadmap Revision 2） |
| BSS 為負值（-14.1% 報告值，Phase 38 清洗後 -15.61%） | 🔴 BLOCKED — BSS Safety Gate 鎖定 |
| Phase 39 修復 `RAW_MODEL_PROB_MISSING`，JSONL 管線已建立 | ✅ 完成（`persist_predictions=True`） |
| 下一個模型步驟為**校準修復**，非 ensemble 擴充 | ✅ 確認 |
| CANDIDATE_PATCH 繼續被 BSS Safety Gate 封鎖（BSS < 0） | 🔴 封鎖中 |

### 1.3 核心結論

> **系統已準備好進行校準修復（calibration repair）與指標整合（metrics consolidation），尚未具備模型擴充（ensemble）或生產部署（production deployment）的條件。**

校準修復需要先執行 `FullBacktestEngine(persist_predictions=True).run(records)` 產出 JSONL，再用 Phase 39 建立的 `recompute_metrics_from_rows()` 重新計算 Brier / BSS / ECE / log loss，最後才能驗證 BSS 是否恢復正值。在此之前，BSS Safety Gate 持續封鎖所有非調查類任務。

---

## 2. Source Roadmap Alignment

**基準文件：** `00-Plan/betting_roadmapplan_20260504.md`（下稱「主 roadmap」）

### 2.1 名詞釐清（§0）

| 主 roadmap 項目 | 現況 | 標記 |
|----------------|------|------|
| WBL → MLB 釐清（MLB 為主，WBC 為輔） | Phase 36–39 全部以 MLB 為作業目標 | ✅ DONE |
| `docs/glossary/league_codes.md` 建立 | 檔案尚未建立 | ⏳ STILL VALID |
| `wbc_backend/` package 歷史命名說明（不 rename） | README 尚未加註，但各 Phase 均遵守此原則 | ⏳ PARTIAL |

### 2.2 Current System Assessment（§2）

| 主 roadmap 評估項目 | 現況 | 標記 |
|--------------------|------|------|
| 成熟模組（SafeTaskExecutor、CLV 三件套、OptimizationReadiness 等） | 未動，保持成熟 | ✅ DONE |
| 雙軌 `models/` vs `wbc_backend/models/` — 需拆分 | 尚未整合 | ⏳ STILL VALID |
| `runtime/agent_orchestrator/training_memory.json` 直接讀寫風險 | 尚未修復 | ⏳ STILL VALID |
| 多份 KPI 計算分散（metrics SSOT 缺口） | Phase 39 建立 `recompute_metrics_from_rows()`，但全域 SSOT 尚未統一 | ⏳ PARTIAL |
| Planner 與 Worker 共用 LLM client 風險 | Phase 36A assertion 已部分緩解 | ⏳ PARTIAL |

### 2.3 Target System Architecture（§3）

| 主 roadmap 架構項目 | 現況 | 標記 |
|--------------------|------|------|
| League Domain（`LeagueAdapter` Protocol） | `wbc_backend/league/` 尚不存在 | ⏳ STILL VALID |
| `MLBAdapter`（主）/ `WBCAdapter`（輔） | 尚未建立 | ⏳ STILL VALID |
| `PredictionState` state machine | 尚未建立 | ⏳ STILL VALID |
| `LearningMemoryRepository` | 尚未建立 | ⏳ STILL VALID |
| Observability Layer（已有 usage dashboard） | 已有 frontend/index.html | ✅ PARTIAL |
| Application Layer services | 架構文件存在，但未全實作 | ⏳ STILL VALID |

### 2.4 Workstream A — Architecture

| 項目 | 優先級 | 現況 | 標記 |
|------|--------|------|------|
| LeagueAdapter 介面骨架 | P0 | 未建 | STILL VALID |
| MLBAdapter 包覆既有 mlb 資料 | P0 | 未建 | STILL VALID |
| WBCAdapter 重構為輔助 | P1 | 未建 | STILL VALID |
| PredictionState enum | P1 | 未建 | STILL VALID |
| Entry-point 收斂 | P2 | 未動 | DEFER |
| root models/ → wbc_backend/models/legacy/ | P3 | 未動 | DEFER |
| Persistence JSONL → SQLite | P5 | 未動 | DEFER（90D 後評估） |
| metrics.py SSOT | P0 | Phase 39 部分建立（prediction_persistence.py 內有 recompute_metrics_from_rows） | NEEDS REVISION |

### 2.5 Workstream B — MLB Prediction Accuracy

| 項目 | 現況 | 標記 |
|------|------|------|
| MLB 資料盤點（mlb_inventory.md） | 尚未建立 | STILL VALID |
| Starting pitcher features（MLB #1 訊號） | 未加入 | STILL VALID |
| Park factor 接入 | 未加入 | DEFER（Phase 2） |
| Bullpen state feature | 未加入 | DEFER（Phase 2） |
| Weather feature | 未加入 | DEFER（Phase 2） |
| walk-forward harness 統一 | `wbc_backend/evaluation/full_backtest.py` 有基礎，但非 MLB 全季標準化 | PARTIAL |
| Feature Registry + lookahead tests | 未建立 | STILL VALID |
| Bootstrap CI utility | 未建立 | STILL VALID |
| BSS < 0 根因（市場偏差 + 重複 + 校準不足） | Phase 37/38 已確認 | DONE |
| Calibration repair 實驗 | Phase 39 建立管線，但尚未執行校準 | **PARTIAL — 下一步** |
| Ensemble walk-forward | BSS 未正 → 禁止 | DEFER |

### 2.6 Workstream C — Simulation / Self-learning

| 項目 | 現況 | 標記 |
|------|------|------|
| Simulation runner v1（Walk-forward / Paper） | 未建 | STILL VALID |
| Self-learning memory schema（learning_cycles.jsonl 等） | `runtime/learning/` 部分存在 | PARTIAL |
| failure_patterns.jsonl 防重複學習 | 未建 | STILL VALID |
| 10 種 simulation 類型 | 未對齊 BSS/calibration 工作流 | NEEDS REVISION |
| Simulation governance boundaries | 文件定義，未落地斷言 | PARTIAL |

### 2.7 Workstream D — Scheduler Self-learning

| 項目 | 現況 | 標記 |
|------|------|------|
| Scheduler priority score formula | 文件定義，未實作 | STILL VALID |
| Scheduler safety invariants（5 條 assert） | 文件定義，未全部落地 | PARTIAL |
| Lineup-event-driven re-prediction（scratched start） | 未建 | DEFER（Phase 3） |
| MLB daily-slate cadence（10 min / 30 min / 1h 週期） | 未對齊實作 | STILL VALID |

### 2.8 Workstream E — Usage Budget / Copilot Governance

| 項目 | 現況 | 標記 |
|------|------|------|
| Budget Guard（Phase 36） | ✅ 已驗收 | DONE |
| Planner external-AI invariant（Phase 36A） | ✅ 已驗收 | DONE |
| UI Budget Panel | ✅ 已驗收（Phase 36） | DONE |
| AuditGuard ordering（Phase 36A） | ✅ 已驗收 | DONE |
| safety_violation.jsonl 機制 | 已實作（Phase 36） | DONE |

### 2.9 Phase Plan（§10）

| 主 roadmap Phase | 天數 | 對應現況 | 標記 |
|-----------------|------|---------|------|
| Phase 0 — Stabilize（Audit/Budget Guard） | D0–14 | Phase 36 / 36A 完成 Workstream E，但 Glossary 尚未建立 | PARTIAL |
| Phase 1 — Foundation（LeagueAdapter / MLB data / metrics） | D15–45 | 尚未開始 | STILL VALID（優先） |
| Phase 2 — Validation（Walk-forward / Feature Registry / Simulation） | D46–90 | 尚未開始 | STILL VALID |
| Phase 3 — Self-Learning（Ensemble / Calibration / Scheduler v2） | D91–150 | BSS 未正，ensemble 禁止 | DEFER 部分 |
| Phase 4 — Production Proposal Loop | D151–180 | BSS 未正，禁止 | DEFER |

### 2.10 First 10 Recommended Tasks（§14）

| 主 roadmap 任務 | Phase 36–39 後現況 | 優先級調整 |
|----------------|-------------------|-----------|
| T1: Glossary `league_codes.md` | 未建立 | 保留，下調至 P2（先做 SSOT + 校準） |
| T2: Budget Guard | Phase 36 已完成 | **DONE** |
| T3: Planner External-AI Invariant | Phase 36A 已完成 | **DONE** |
| T4: UI Budget Panel | Phase 36 已完成 | **DONE** |
| T5: LeagueAdapter + MLBAdapter + WBCAdapter | 未建立 | 保留 P1 |
| T6: Metrics SSOT | Phase 39 部分（prediction_persistence.py），全域未統一 | **提升為 P0** |
| T7: test_no_lookahead.py | 未建立 | 保留 P1 |
| T8: MLB Data Inventory | 未建立 | 保留 P1 |
| T9: PredictionState state machine | 未建立 | 保留 P2 |
| T10: LearningMemoryRepository | 未建立 | 保留 P2 |

---

## 3. Completed Work Since Roadmap

### Phase 36 — Usage Budget Guard ✅

**Tag:** `PHASE_36_USAGE_BUDGET_GUARD_VERIFIED`

| 交付項目 | 狀態 |
|----------|------|
| Budget config schema（`runtime/agent_orchestrator/budget_config.json`） | ✅ |
| Budget evaluator（`orchestrator/budget_guard.py`） | ✅ |
| Worker external call blocking（policy-gated） | ✅ |
| Decision Card / frontend Usage Budget panel（`frontend/index.html`） | ✅ |
| CLI（`scripts/run_usage_budget_check.py`） | ✅ |
| `tests/test_phase36_usage_budget_guard.py`（15 tests PASS） | ✅ |

**BSS 影響：** 無（governance 層，不觸碰模型）

### Phase 36A — Copilot Daemon CLI Compatibility ✅

**Tag:** `PHASE_36A_COPILOT_DAEMON_CLI_COMPAT_VERIFIED`

| 交付項目 | 狀態 |
|----------|------|
| Agent CLI mode（deterministic fallback） | ✅ |
| gpt-5-mini command wrapper | ✅ |
| Legacy fallback 路徑 | ✅ |
| AuditGuard ordering（deny-first）修正 | ✅ |

**BSS 影響：** 無（governance 層）

### Phase 37 — BSS Root Cause Audit ✅

**Tag:** `PHASE_37_MLB_BSS_NEGATIVE_ROOT_CAUSE_AUDIT_VERIFIED`

| 交付項目 | 狀態 |
|----------|------|
| BSS 原始值：-14.1%（報告）/ -15.5%（重算） | ✅ 稽核 |
| 根因確認：(1) 市場機率偏差、(2) 重複樣本、(3) 模型未校準 | ✅ 稽核 |
| BSS Safety Gate（`orchestrator/bss_safety_gate.py`） | ✅ |
| `BssSafetyResult`（fields: `bss`, `bss_negative`, `allowed`, `block_reason`, `recommendation`, `baseline`, `model_brier`, `task_kind`） | ✅ |
| `tests/test_phase37_mlb_bss_root_cause_audit.py`（24 tests PASS） | ✅ |

**關鍵發現：** `allowed=False`，`bss_negative=True` — 生產路徑持續封鎖

### Phase 38 — Data + Calibration Repair Preview ✅

**Tag:** `PHASE_38_MLB_BSS_DATA_CALIBRATION_REPAIR_VERIFIED`

| 交付項目 | 狀態 |
|----------|------|
| 重複樣本清洗（n_games: 2,400 → 清洗後） | ✅ |
| 清洗後 market_brier = 0.2419（vs 報告 0.2451） | ✅ |
| 清洗後 BSS = -15.61%（更差，確認模型本身問題） | ✅ |
| `RAW_MODEL_PROB_MISSING` 缺口識別 | ✅ |
| `scripts/run_phase38_mlb_bss_repair_preview.py` | ✅ |
| `tests/test_phase38_mlb_bss_repair_preview.py`（51 tests PASS） | ✅ |

**關鍵發現：** per-game model 機率從未持久化至磁碟 → 無法重算 Brier / ECE / log loss

### Phase 39 — Prediction Probability Persistence ✅

**Tag:** `PHASE_39_MLB_PREDICTION_PROBABILITY_PERSISTENCE_VERIFIED`

| 交付項目 | 狀態 |
|----------|------|
| `wbc_backend/evaluation/prediction_persistence.py`（`PredictionRow` schema `phase39-v1`） | ✅ |
| `FullBacktestEngine(persist_predictions=True)`（`wbc_backend/evaluation/full_backtest.py`） | ✅ |
| `DEFAULT_PREDICTIONS_PATH = data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl` | ✅ |
| `scripts/run_phase39_mlb_prediction_persistence_check.py`（CLI） | ✅ |
| `docs/orchestration/phase39_mlb_prediction_probability_persistence_report_2026-05-04.md` | ✅ |
| `tests/test_phase39_mlb_prediction_persistence.py`（46 tests PASS） | ✅ |

**關鍵發現：** JSONL 尚未生成（需手動執行完整 backtest run）；校準修復路徑已通暢但尚未執行

**JSONL 生成指令（非自動化，需要完整 MARL backtest）：**
```python
from data.mlb_data_loader import load_mlb_2025
from wbc_backend.evaluation.full_backtest import FullBacktestEngine

records = load_mlb_2025()
engine = FullBacktestEngine(persist_predictions=True)
report = engine.run(records)
# → data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl
```

**Combined test baseline：** 136/136 PASS（Phase 36:15 + Phase 37:24 + Phase 38:51 + Phase 39:46）

---

## 4. Current Blockers（優先順序）

### Blocker 1 — 校準修復尚未執行（關鍵路徑）

**優先級：** 🔴 P0

Phase 39 建立了 JSONL 寫出管線與 `recompute_metrics_from_rows()` 函數，但完整 backtest 尚未執行。`data/mlb_2025/derived/` 目錄不存在。沒有 per-game 機率行，就無法進行 Platt/Isotonic 校準實驗。

**解鎖條件：** 執行 `FullBacktestEngine(persist_predictions=True).run(records)` 並確認 JSONL ≥ 500 行。

### Blocker 2 — Metrics SSOT 未統一（影響所有後續驗證）

**優先級：** 🔴 P0

Brier / BSS / ECE / log loss 計算分散在至少三處：
- `wbc_backend/evaluation/prediction_persistence.py`（`recompute_metrics_from_rows`）
- `scripts/run_phase38_mlb_bss_repair_preview.py`（內嵌計算）
- `scripts/run_phase39_mlb_prediction_persistence_check.py`（獨立計算）

主 roadmap 已識別此問題（§5.4 Anti-patterns）。需建立 `wbc_backend/evaluation/metrics.py` 作為 SSOT，所有 caller 改 import。

### Blocker 3 — BSS 持續為負（封鎖生產路徑）

**優先級：** 🔴 P0（持續）

BSS 清洗後 -15.61%（`allowed=False`，`bss_negative=True`）。即使校準修復成功，仍需重跑 walk-forward 並確認 BSS ≥ 0 才能解鎖 CANDIDATE_PATCH。

**解鎖條件：** 校準後 BSS ≥ 0（walk-forward OOS，n ≥ 1500）。

### Blocker 4 — LeagueAdapter 能力缺口未稽核

**優先級：** 🟡 P1

`wbc_backend/league/` 目錄不存在。`MLBAdapter` 尚未建立。現有 `data/mlb_2024_pitchers.py`、`data/mlb_2025_preview.py`、`data/odds_api_client.py` 等 MLB 資產尚未被抽象化。LeagueAdapter 是主 roadmap §3.3 的架構基石。

### Blocker 5 — Feature repair 尚未開始

**優先級：** 🟡 P1

Starting pitcher（MLB #1 訊號）、park factor、bullpen state 均未加入特徵集。`tests/feature_validation/test_no_lookahead.py` 尚未建立。無 Feature Registry，無版本控制。

### Blocker 6 — Odds source 驗證未完成

**優先級：** 🟡 P1

`docs/data/mlb_inventory.md` 尚未建立。`data/odds_api_client.py` 存在，但多 provider 比對（Pinnacle / Circa / DK / FD）、rate limit、credential 狀態均未文件化。

### Blocker 7 — Scheduler priority score 未實作

**優先級：** 🟠 P2

主 roadmap §8.3 定義的 priority score 公式（8 個 weight 參數）文件化但未落地。Scheduler tick 的 5 條 safety invariant 只部分存在。

### Blocker 8 — Simulation framework 未對齊 BSS/校準工作流

**優先級：** 🟠 P2

主 roadmap §7.1 定義 10 種 simulation 類型，但目前 simulation runner 概念上存在卻未與 calibration workflow 對齊。需先完成校準修復，再啟動 simulation framework。

---

## 5. Roadmap Convergence Table

| Roadmap Item | 主 roadmap 原始優先級 | 當前狀態 | 決策 | 原因 | 下一 Phase |
|---|---|---|---|---|---|
| Glossary `league_codes.md` | Rank 1 (§13) | 未建立 | **Keep** | 命名歧義根源，低成本高影響 | Phase 40 Task 2 |
| Usage Budget Guard | Rank 2 (§13) | ✅ Phase 36 完成 | **Done** | 已驗收 | — |
| Planner external-AI invariant | Rank 3 (§13) | ✅ Phase 36A 完成 | **Done** | 已驗收 | — |
| UI Budget Panel | Rank 4 (§13) | ✅ Phase 36 完成 | **Done** | 已驗收 | — |
| LeagueAdapter / MLBAdapter | Rank 5 (§13) | 未建立 | **Keep** | 架構基石，BSS 封鎖中仍可並行 | Phase 41 |
| Metrics SSOT | Rank 6 (§13) | ⚠️ 部分（prediction_persistence.py） | **Keep / Merge** | 提升為 P0，Phase 39 的 recompute 函數合並入 metrics.py | Phase 40 Task 1 |
| No-lookahead tests | Rank 7 (§13) | 未建立 | **Keep** | Data leakage silent killer | Phase 41 |
| MLB Data Inventory | Rank 8 (§13) | 未建立 | **Keep** | 所有 feature 工程的前置 | Phase 41 |
| PredictionState state machine | Rank 9 (§13) | 未建立 | **Keep** | 解耦 if/else，Review Queue 前置 | Phase 42 |
| LearningMemoryRepository | Rank 10 (§13) | 未建立 | **Keep** | 高風險耦合點修復 | Phase 42 |
| Walk-forward harness | Rank 11 (§13) | ⚠️ 部分（full_backtest.py） | **Keep / Merge** | 需對齊 MLB 全季標準 | Phase 41 |
| Feature Registry | Rank 12 (§13) | 未建立 | **Keep** | Feature version control 必要 | Phase 41 |
| Bootstrap CI | Rank 13 (§13) | 未建立 | **Keep** | 需在校準驗證中使用 | Phase 40 |
| Simulation runner v1 | Rank 14 (§13) | 未建立 | **Keep** | 校準修復完成後啟動 | Phase 42 |
| Scheduler priority score | Rank 16 (§13) | 未實作 | **Defer** | 需先完成校準 + Metrics SSOT | Phase 43 |
| Starting pitcher features | Rank 19 (§13) | 未加入 | **Keep** | MLB #1 訊號，Phase 2 | Phase 41 |
| Park factor | Rank 20 (§13) | 未加入 | **Defer** | Phase 2，等 Feature Registry | Phase 42 |
| Bullpen state | Rank 21 (§13) | 未加入 | **Defer** | Phase 2，等 Feature Registry | Phase 42 |
| Calibration（Platt/Isotonic） | Rank 24 (§13) | ⚠️ 管線已建（Phase 39）但未執行 | **Keep — P0** | BSS 負值的直接修復路徑 | Phase 40 Task 2 |
| BSS Safety Gate | Phase 37 | ✅ 建立，`allowed=False` | **Keep** | 永遠有效直到 BSS ≥ 0 | 持續 |
| Prediction probability persistence | Phase 39 | ✅ 管線建立，JSONL 未生成 | **Keep — P0** | 校準修復的前置 | Phase 40 Task 2 |
| Ensemble（Phase B） | Rank 23 (§13) | BSS < 0 封鎖 | **Defer** | BSS < 0 時不允許 | Phase 43+ |
| Production proposal | Phase 4 | BSS < 0 封鎖 | **Defer** | 不允許 | Phase 44+ |
| Auto-tune betting thresholds | — | BSS < 0 封鎖 | **Drop（本階段）** | 校準前無效 | — |
| Persistence → SQLite | Rank 5 (§5.3) | 未動 | **Defer** | 90D 後評估 | Phase 44+ |

---

## 6. Corrected Priority Order

基於 Phase 36–39 完成工作與當前 blocker 分析，更新執行優先序：

### 調整後優先序（Top 10）

| 優先序 | 項目 | 原主 roadmap 順序 | 調整原因 |
|--------|------|------------------|---------|
| 1 | **Metrics SSOT（`wbc_backend/evaluation/metrics.py`）** | Rank 6 | BSS / ECE / Brier / log loss 在三處計算不一致；校準修復結果必須有 SSOT 才能驗證 |
| 2 | **校準修復實驗（使用 Phase 39 persisted predictions）** | Rank 24 | Phase 39 已建管線；校準是解鎖 BSS 正值的直接路徑 |
| 3 | **BSS 重算與 Safety Gate 驗證（from persisted rows）** | Phase 37 延伸 | 校準後必須重跑 walk-forward 確認 BSS ≥ 0 才能解鎖 |
| 4 | **LeagueAdapter 能力稽核（+MLBAdapter 骨架）** | Rank 5 | 架構基石；可與校準並行，不影響 BSS gate |
| 5 | **Odds source 驗證 / MLB Data Inventory** | Rank 8 | Feature 工程的前置；`mlb_inventory.md` |
| 6 | **Feature ablation（MARL proxy feature 貢獻分析）** | Rank 19–21 | 校準後確認哪些 feature 真正貢獻，避免雜訊 feature 影響校準 |
| 7 | **Market-only / rule-only / model 三路比較** | Phase A（§6.3） | 建立 Brier baseline 比較，確認模型相較市場的真實缺口 |
| 8 | **No-lookahead feature validation** | Rank 7 | Data leakage 是 silent killer；在加入 pitcher/park 特徵前必須強制 |
| 9 | **Walk-forward harness 統一（MLB 全季標準）** | Rank 11 | 校準修復後需要標準化的 walk-forward 流程 |
| 10 | **Simulation runner v1（校準 + feature ablation 適用）** | Rank 14 | 校準修復完成後，simulation 才有正確的機率輸入 |

### 為什麼 Ensemble、生產提案、自動 patch 不允許

**Ensemble（Phase B / Rank 23）：**
主 roadmap §6.3 Phase B 明確要求「必經 patch gate + human review」，且 Phase B 的前提是「Brier / ECE baseline 文件化」完成。目前 BSS = -15.61%，表示模型預測能力落後純市場機率；在此基礎上 ensemble 只會堆疊劣質信號，無法改善 BSS。

**Production proposal：**
主 roadmap §6.3 Phase D 要求五個門檻同時達標（≥ 2000 樣本、Brier CI95 下降、CLV ≥ +50 bps CI90、regime stability、human review）。目前 CLV 樣本 < 50，BSS 為負，五個門檻均不達標。

**CANDIDATE_PATCH / auto-patch：**
BSS Safety Gate（`orchestrator/bss_safety_gate.py`）設計即為此而生：`allowed=False` 時，所有非調查類任務均被封鎖。Phase 39 固化了此行為（46 tests PASS）。

---

## 7. Updated 30 / 60 / 90 / 180 Day Roadmap

> **參考基準：** 主 roadmap §12。以下為合併 Phase 36–39 完成工作後的修訂版。Day 0 = 2026-05-04。

### 30 Days（2026-05-04 → 2026-06-03）

**核心焦點：** Metrics 整合 + 校準修復 + BSS 重算 + LeagueAdapter 啟動 + MLB 盤點

| 交付物 | 對應 Phase |
|--------|-----------|
| `wbc_backend/evaluation/metrics.py` — Brier / BSS / ECE / log loss SSOT | Phase 40 |
| 執行 `FullBacktestEngine(persist_predictions=True)` → 生成 JSONL | Phase 40 |
| Calibration repair 實驗（Platt / Isotonic） | Phase 40 |
| 從 persisted rows 重算 BSS / ECE → 更新 Phase 37 / 38 / 39 報告 | Phase 40 |
| BSS Safety Gate 跨組件驗證（planner / patch gate） | Phase 40 |
| `docs/glossary/league_codes.md` | Phase 40 |
| `wbc_backend/league/base.py` — LeagueAdapter Protocol 骨架 | Phase 41 |
| `wbc_backend/league/mlb_adapter.py` — 包覆現有 mlb_* 資料 | Phase 41 |
| `docs/data/mlb_inventory.md` | Phase 41 |
| `tests/feature_validation/test_no_lookahead.py` | Phase 41 |
| 136 tests 繼續 PASS，不迴歸 | 持續 |

**封鎖狀態：** BSS Safety Gate 持續。若校準修復後 BSS ≥ 0，本週期末可申請解鎖審查。

### 60 Days（2026-06-03 → 2026-07-03）

**核心焦點：** Feature ablation + walk-forward 標準化 + simulation v1

| 交付物 | 對應 Phase |
|--------|-----------|
| MARL proxy feature ablation report | Phase 42 |
| Market-only / rule-only / model 三路 Brier 比較 | Phase 42 |
| Feature Registry + versioning（`wbc_backend/features/registry.py`） | Phase 42 |
| Bootstrap CI utility（`wbc_backend/evaluation/bootstrap.py`） | Phase 42 |
| Walk-forward harness 統一化（MLB 2022–2025，樣本 ≥ 1500） | Phase 42 |
| `PredictionState` state machine（`wbc_backend/state_machine/`） | Phase 42 |
| `LearningMemoryRepository`（取代直接讀寫 training_memory.json） | Phase 42 |
| Simulation runner v1（Walk-forward + Paper，MLB daily slate） | Phase 42 |
| Odds source 多 provider 比對（Pinnacle / Circa / DK / FD） | Phase 42 |

**前提：** BSS 需 ≥ 0（校準後）才允許執行 Walk-forward feature ablation 的 candidate 模型。

### 90 Days（2026-07-03 → 2026-08-02）

**核心焦點：** Feature repair + pitcher/park/bullpen + scheduler v1

| 交付物 | 對應 Phase |
|--------|-----------|
| Starting pitcher features（FIP / xFIP / K9 / BB9 / HR9） | Phase 43 |
| Park factor（Statcast，年更） | Phase 43 |
| Bullpen state feature builder | Phase 43 |
| Scheduler priority score v1（8 weight 公式落地） | Phase 43 |
| Scheduler safety invariants（5 條 assert） | Phase 43 |
| MLB Regime classifier（early / mid / late season） | Phase 43 |
| **Ensemble（前提：BSS ≥ 0 且 walk-forward 顯著）** | Phase 43（條件式） |

**條件式啟動：** Ensemble 僅在 BSS 持續 ≥ 0（walk-forward OOS ≥ 1500，CI95 顯著）才啟動。若未達標，本週期聚焦 feature repair。

### 180 Days（2026-08-02 → 2026-11-01）

**核心焦點：** Human-reviewed production proposal + 穩健 CLV/ROI + daily-slate governance

| 交付物 | 對應 Phase |
|--------|-----------|
| 完整 production proposal workflow（review queue + audit hash） | Phase 44 |
| 穩健 CLV / ROI tracking + daily-slate exposure cap | Phase 44 |
| Architecture health score script（季度跑） | Phase 44 |
| WBC adapter 重構為 cross-league 輔助（spring training → MLB 開季） | Phase 44 |
| Human Review SLA < 12h | Phase 44 |
| `CLV ≥ +50 bps CI90`（MLB 全季，180D 目標） | Phase 44 |

---

## 8. First 10 Execution Tasks

### Task 1 — Metrics SSOT（`wbc_backend/evaluation/metrics.py`）

**Why now：** BSS / ECE / Brier / log loss 目前在三個檔案內各自計算（`prediction_persistence.py`、`run_phase38_...py`、`run_phase39_...py`）。校準修復結果必須由同一個函數庫計算才有可比性。主 roadmap §5.4 明確列為 Anti-pattern 要消除。

**目標檔案：**
- `wbc_backend/evaluation/metrics.py`（新建）
- `wbc_backend/evaluation/prediction_persistence.py`（`recompute_metrics_from_rows` 改 import metrics.py）
- `scripts/run_phase38_mlb_bss_repair_preview.py`（caller 改用 metrics.py）
- `scripts/run_phase39_mlb_prediction_persistence_check.py`（caller 改用 metrics.py）

**預期輸出：**
- `brier_score(y_true, y_prob) → float`
- `log_loss_score(y_true, y_prob) → float`
- `expected_calibration_error(y_true, y_prob, n_bins=10) → float`
- `bss(model_brier, market_brier) → float`
- `reliability_curve(y_true, y_prob, n_bins=10) → dict`
- `compute_metrics_bundle(rows: list[PredictionRow]) → dict`

**測試：** `tests/test_metrics_ssot.py`（≥ 15 tests，含數值驗證、邊界條件、與 Phase 38/39 數字對齊）

**驗收標準：**
- 所有 caller 改用 `from wbc_backend.evaluation.metrics import ...`
- Phase 38 計算結果（model_brier=0.2796，market_brier=0.2451，BSS=-0.141）通過 metrics.py 重算
- Phase 39 `recompute_metrics_from_rows` 使用 metrics.py 計算
- 136 + N tests 全 PASS

**核准要求：** 無（純 deterministic 重構，不改演算法）
**Deterministic：** ✅

---

### Task 2 — 校準修復實驗（使用 Phase 39 Persisted Predictions）

**Why now：** Phase 38 確認根因為（1）市場機率偏差 + （2）重複樣本 + （3）模型未校準。Phase 39 建立了 JSONL 管線。校準修復是解鎖 BSS 正值的最直接路徑。

**目標檔案：**
- 執行腳本（新建）：`scripts/run_phase40_calibration_repair.py`
- 校準模組（新建）：`wbc_backend/evaluation/calibration.py`（Platt scaling / Isotonic regression）
- 輸出：`data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl`（需先執行 backtest）
- 輸出：`docs/orchestration/phase40_calibration_repair_report_YYYY-MM-DD.md`

**預期輸出：**
- Pre-calibration ECE、calibrated ECE、reliability diagram（before / after）
- Calibrated BSS（walk-forward OOS，n ≥ 500 驗證組，不得用同一 fold 校準與評估）
- `CalibrationResult` dataclass（schema_version, method, pre_ece, post_ece, pre_bss, post_bss, sample_size, n_bins, audit_hash）

**測試：** `tests/test_phase40_calibration_repair.py`（≥ 15 tests）

**驗收標準：**
- JSONL 存在且 ≥ 500 行
- 校準使用 cross-validation fold（不得 same-fold）
- 校準後 ECE 有所改善（不保證 < 0.08 — 依數據而定）
- BSS 重算結果寫入報告（即使仍為負值）
- BSS Safety Gate 繼續運作，`allowed` 依重算後 BSS 決定

**核准要求：** 需 human review（模型校準修改）
**Deterministic：** ✅（Platt / Isotonic 均 deterministic）

---

### Task 3 — 從 Persisted Rows 重算 BSS / ECE，更新報告

**Why now：** Phase 37 / 38 / 39 的報告基於不同資料版本和計算方式。Metrics SSOT 完成後，需統一重算並更新 SSOT 數字作為後續所有驗證的基準。

**目標檔案：**
- `scripts/run_phase40_metrics_recompute.py`（新建）
- 更新 `docs/orchestration/phase37_mlb_bss_negative_root_cause_audit_2026-05-04.md`（添加 SSOT 數字）
- 更新 `docs/orchestration/phase38_mlb_bss_data_calibration_repair_report_2026-05-04.md`（添加 SSOT 數字）
- 更新 `docs/orchestration/phase39_mlb_prediction_probability_persistence_report_2026-05-04.md`（添加 SSOT 數字）

**預期輸出：**
- `MetricsRecomputeResult`（from persisted rows，using metrics.py SSOT）
- 官方 SSOT 數字（model_brier / market_brier / BSS / ECE）作為 Phase 40 基準

**驗收標準：**
- 報告內 SSOT 數字與 `wbc_backend/evaluation/metrics.py` 計算結果一致
- BSS Safety Gate 使用更新後數字（若仍為負，`allowed=False`）

**核准要求：** 無（文件更新）
**Deterministic：** ✅

---

### Task 4 — BSS Safety Gate 跨組件驗證（Planner / Patch Gate）

**Why now：** Phase 37 建立了 BSS Safety Gate，但主 roadmap §8.2 要求 Planner / Worker / Scheduler 均受 Gate 保護。目前僅在 `orchestrator/bss_safety_gate.py` 實作，未確認 Planner tick 和 Patch Gate 是否都正確引用。

**目標檔案：**
- `orchestrator/bss_safety_gate.py`（驗證現有實作）
- `orchestrator/planner_tick.py`（確認呼叫 BSS Gate）
- `tests/test_phase40_bss_safety_gate_cross_component.py`（新建，≥ 10 tests）

**預期輸出：**
- 確認 Planner tick 在 `bss_negative=True` 時不允許非調查類任務
- 確認 Patch Gate 在 `bss_negative=True` 時不允許 CANDIDATE_PATCH
- `gate_decisions.jsonl` 有正確記錄

**驗收標準：**
- 模擬 BSS = -0.141：Planner 不發出非調查任務
- 模擬 BSS = +0.02：Planner 可發出調查任務（但仍需 walk-forward 驗證）
- 136 + N tests PASS

**核准要求：** 無
**Deterministic：** ✅

---

### Task 5 — LeagueAdapter 能力稽核（+ MLBAdapter 骨架）

**Why now：** 主 roadmap §3.3 + §5.1 將 `LeagueAdapter` 定為架構基石（Rank 5）。`wbc_backend/league/` 不存在。所有後續 MLB feature 工程都需要 `MLBAdapter` 介面。可與 Tasks 1–4 並行，不受 BSS 封鎖影響。

**目標檔案：**
- `wbc_backend/league/__init__.py`（新建）
- `wbc_backend/league/base.py`（LeagueAdapter Protocol，新建）
- `wbc_backend/league/mlb_adapter.py`（包覆 data/mlb_2024_pitchers.py、data/mlb_2025_preview.py、data/odds_api_client.py，新建）
- `wbc_backend/league/wbc_adapter.py`（包覆 wbc_backend/pipeline/wbc_rule_engine.py，新建）
- `tests/architecture/test_league_adapter.py`（新建）

**預期輸出：**
- `LeagueAdapter` Protocol（code, list_fixtures, fetch_results, fetch_odds_open, fetch_odds_closing, fetch_lineups, fetch_park_factors, fetch_weather, league_specific_rules）
- `MLBAdapter` 至少實作 list_fixtures / fetch_results / fetch_odds_open / fetch_odds_closing
- 既有 MLB + WBC pipeline 行為不變（wrapping，非改寫）
- 稽核報告：各 method 的實作狀態（已有 / 缺口 / 計劃）

**驗收標準：**
- Import 路徑測試通過
- 禁止 cross-adapter 直接 import 對方資料源
- 既有 14 項測試（Phase 36–39）繼續 PASS

**核准要求：** 無（純包覆，不改行為）
**Deterministic：** ✅

---

### Task 6 — MLB Data Inventory + Odds Source 驗證

**Why now：** 主 roadmap §6.1 的 MLB Data Inventory 表格（18 行資料類別）需要文件化，作為後續所有 feature 工程的前置。`docs/data/mlb_inventory.md` 不存在。主 roadmap §15.1 T8 要求 D10 完成。

**目標檔案：**
- `docs/data/mlb_inventory.md`（新建）
- `docs/glossary/league_codes.md`（新建）

**預期輸出（依主 roadmap §6.1 表格）：**
每個資料類別包含：
1. Provider / endpoint
2. Auth / credential 來源
3. 抓取頻率 / rate limit
4. Cost
5. 既有 codebase 對應檔案
6. 缺口說明
7. Phase 落點

**18 項資料類別：** 賽程、Roster、球員統計、先發投手、Injuries/IL、歷史賽果、Odds opening、Odds closing、Line movement、Implied probability、Sharp/liquidity、Prediction registry、CLV records、Backtest reports、Live results（可選）、Park factor、Weather、Umpire（可選）

**驗收標準：**
- 全部 18 項有文件化（即使是「未取得 / Phase N 計劃」）
- Odds provider 列出 ≥ 3 家比對基準
- Credential 狀態明確（已有 / 需申請 / 未知）

**核准要求：** 無（文件）
**Deterministic：** ✅

---

### Task 7 — MARL Proxy Feature Ablation 分析

**Why now：** Phase 38 清洗後 BSS = -15.61%，比原本更差，顯示模型特徵可能有問題（proxy features 可能引入雜訊）。在執行校準前需理解哪些 feature 真正貢獻，哪些是 MARL proxy 雜訊。

**前提：** JSONL 存在（Task 2 前置）

**目標檔案：**
- `scripts/run_phase40_feature_ablation.py`（新建）
- `wbc_backend/evaluation/feature_ablation.py`（新建）

**預期輸出：**
- 每個 feature 的 Brier contribution（leave-one-out 或 permutation）
- `FeatureAblationReport`（feature_name, brier_baseline, brier_without, delta, p_value）
- 建議移除 / 保留 / 深入調查的 feature 清單

**測試：** `tests/test_phase40_feature_ablation.py`（≥ 10 tests）

**驗收標準：**
- 使用 walk-forward split（不 shuffle）
- 每個 feature ablation 使用 ≥ 300 OOS 樣本
- 無 look-ahead（`test_no_lookahead.py` 通過）
- 報告生成並寫至 `docs/orchestration/`

**核准要求：** 無（分析，不改模型）
**Deterministic：** ✅

---

### Task 8 — Market-only / Rule-only / Model 三路比較

**Why now：** 主 roadmap §6.3 Phase A 要求 baseline 三家 head-to-head（Elo / LR / GBM）。更根本的問題：market 機率本身（去vig後）的 Brier 是 0.2419（Phase 38 cleaned）。模型的 Brier 是 0.2796。需要明確量化這個差距，並確認 rule-based 系統是否好於 market。

**目標檔案：**
- `scripts/run_phase40_baseline_comparison.py`（新建）
- `wbc_backend/evaluation/baseline_models.py`（新建）

**預期輸出：**
- `BaselineComparisonResult`（market_brier, rule_brier, model_brier, delta_model_vs_market, bss_model, bss_rule）
- Reliability diagram for all three
- 結論：哪條路線值得繼續投資

**驗收標準：**
- 使用相同 OOS 樣本集（不重疊訓練資料）
- n ≥ 1500（walk-forward）
- 報告含 CI95（Bootstrap）

**核准要求：** 無
**Deterministic：** ✅

---

### Task 9 — No-lookahead Feature Validation

**Why now：** Data leakage 是模型 silent killer。主 roadmap §6.2 明確要求「每個特徵入庫前必經 `tests/feature_validation/test_no_lookahead.py`」。尤其在加入 starting pitcher / park / bullpen 特徵前，必須先建立 leakage 防線。

**目標檔案：**
- `tests/feature_validation/__init__.py`（新建）
- `tests/feature_validation/test_no_lookahead.py`（新建）
- `wbc_backend/features/builder.py`（加 time-cursor hooks）

**預期輸出：**
- 假時間 cursor（`reference_dt`）機制
- 每個 feature 的 timestamp 必須 ≤ reference_dt
- 故意製造 1 個 leak case 必須 FAIL（regression guard）
- 所有現有 MARL feature 通過測試

**驗收標準：**
- Leak case 測試必須顯示 `FAIL`（預期失敗）
- 現有所有 feature 通過（無 leakage）
- 新 feature 加入前必須先通過此 gate

**核准要求：** 無
**Deterministic：** ✅

---

### Task 10 — Simulation Runner v1（校準 + Feature Ablation 適用）

**Why now：** 主 roadmap §7.1 定義 10 種 simulation 類型，目前無一完整實作。校準修復完成後，需要一個能對不同校準方法 / feature 組合進行系統化比較的 simulation runner。

**前提：** Task 1（Metrics SSOT）+ Task 2（JSONL 生成）完成

**目標檔案：**
- `research/simulations/__init__.py`（新建）
- `wbc_backend/simulation/runner.py`（新建）
- `wbc_backend/simulation/schemas.py`（新建，含 §7.2 的輸出 schema）

**預期輸出（v1 僅實作 3 種類型）：**
1. Walk-forward simulation（type 2）
2. Calibration comparison simulation（type 1 的變體）
3. Feature ablation simulation（type 6 的精簡版）

**驗收標準：**
- `SimulationResult` 輸出 schema（simulation_id, type, date_range, sample_size, baseline_metrics, candidate_metrics, deltas_with_ci, audit_hash）
- `recommendation ∈ {HOLD, INVESTIGATE, COLLECT_MORE_DATA, CANDIDATE_PATCH, HUMAN_REVIEW_REQUIRED}`
- Sandbox-only（不觸碰 production model）
- `insight ≠ deploy`（simulation 只寫 insight，不 trigger deploy）

**核准要求：** Human review 若 recommendation = CANDIDATE_PATCH
**Deterministic：** ✅

---

## 9. What Not To Do Yet

以下項目在 Phase 40 期間**明確禁止**：

### 模型層禁止

| 禁止事項 | 原因 |
|----------|------|
| ❌ 建立 Ensemble（Phase B） | BSS < 0；劣質信號疊加不改善 BSS |
| ❌ 建立 CANDIDATE_PATCH | BSS Safety Gate `allowed=False` |
| ❌ Production deployment | BSS < 0；review 門檻未達 |
| ❌ 自動調整 betting thresholds | 校準修復前 threshold 無效 |
| ❌ 用 sandbox 結果宣稱 production 成功 | Phase 39 report 已明確禁止 |
| ❌ Same-fold 校準與評估 | 會高估校準效果（數據洩漏） |

### 架構層禁止

| 禁止事項 | 原因 |
|----------|------|
| ❌ rename `wbc_backend/` | 會觸發大規模 import 風暴；主 roadmap §0.5 明確禁止 |
| ❌ 將 JSONL persistence 遷移至 SQLite/Postgres | 90D 後評估；現在改動增加不必要風險 |
| ❌ 新增付費外部 API（在 inventory 完成前） | Task 6 前置條件未達 |
| ❌ 直接 `git mv` root `models/` | 會破壞 import；需先建 import-shim |

### 治理層禁止

| 禁止事項 | 原因 |
|----------|------|
| ❌ Planner 呼叫外部 AI | Hard rule，Phase 36A assertion 已落地 |
| ❌ 繞過 BSS Safety Gate | Hard rule，Phase 37 已固化 |
| ❌ 以 < 1500 樣本下模型結論 | CLAUDE.md hard rule；patch gate 強制 |
| ❌ 跳過 human review（模型 / 策略變更） | Phase 4 才開 review-driven loop |

---

## 10. Final Recommendation

### 10.1 接下來兩週應做什麼

**Week 1（D1–D7）：**

| Day | 行動 | 輸出 |
|-----|------|------|
| D1 | Task 1：設計 `wbc_backend/evaluation/metrics.py` API | API 草稿 + 函數簽名 |
| D2 | Task 1：實作 metrics.py（5 個函數 + 測試） | `metrics.py` + `test_metrics_ssot.py` |
| D3 | Task 1：更新 prediction_persistence.py / Phase 38/39 scripts caller | 136 + N tests PASS |
| D4 | Task 6：`docs/glossary/league_codes.md` + `docs/data/mlb_inventory.md` 草稿 | 2 份文件 |
| D5 | Task 2 準備：執行 `FullBacktestEngine(persist_predictions=True).run(records)`（如資料可用） | JSONL 或錯誤報告 |
| D6 | Task 5：`wbc_backend/league/base.py` LeagueAdapter Protocol | Protocol 骨架 + tests |
| D7 | Task 5：`wbc_backend/league/mlb_adapter.py` 包覆既有 mlb 資料 | MLBAdapter v0.1 |

**Week 2（D8–D14）：**

| Day | 行動 | 輸出 |
|-----|------|------|
| D8 | Task 2：校準修復實驗（Platt scaling，若 JSONL 已有） | CalibrationResult |
| D9 | Task 2：校準修復實驗（Isotonic，比較） | 校準比較報告 |
| D10 | Task 3：從 persisted rows 重算 BSS / ECE，更新報告 | SSOT 數字更新 |
| D11 | Task 4：BSS Safety Gate 跨組件驗證 | `test_bss_safety_gate_cross_component.py` |
| D12 | Task 9：`tests/feature_validation/test_no_lookahead.py` | No-lookahead gate |
| D13 | 整合驗證：全部 tests PASS | Combined test run |
| D14 | Phase 40 retrospective + Phase 41 計劃 | Phase 40 驗收報告 |

### 10.2 下一個技術阻礙（Technical Blocker）

**JSONL 生成問題：** `data/mlb_data_loader.load_mlb_2025()` 返回的 records 需確認欄位與 `GameRecord` schema 對齊（`game_id`, `game_date`, `home_team`, `away_team`, `actual_home_win`, `market_home_prob`）。若資料缺少關鍵欄位，`FullBacktestEngine` 會生成空 JSONL，導致校準無法進行。

**解鎖動作：** 執行 backtest dry-run 確認 JSONL 行數 ≥ 500。

### 10.3 下一個模型阻礙（Model Blocker）

**BSS 持續為負（-15.61%）：** 校準修復能改善 ECE，但不保證能讓 BSS 轉正。BSS = 1 - model_brier / market_brier，若模型的 Brier 基本面就輸給市場，校準只能減少預測機率的偏差，無法補救模型特徵的預測力不足。

**評估方式：** 校準後，若 BSS 仍為負，需啟動 Task 7（Feature ablation）確認哪些 feature 拖累模型，再考慮 feature repair（Task 5 之後的 starting pitcher / park / bullpen 加入）。

### 10.4 下一個 Scheduler 阻礙（Scheduler Blocker）

**Priority score 未落地：** 主 roadmap §8.3 的 8 weight 公式需要 walk-forward 試跑才能調整權重。在 BSS 轉正、walk-forward 標準化完成前，priority score 的 `expected_impact` 參數無可靠估計值。

**解鎖條件：** Task 9（Metrics SSOT + walk-forward harness）完成後，才能用實際 Brier delta 標定 `w_impact`。

### 10.5 下一個治理阻礙（Governance Blocker）

**BSS Safety Gate 仍然是最大的治理決定：** Gate 設計正確（`allowed=False`），但目前沒有標準化的「Gate 解鎖申請流程」。若校準修復後 BSS 接近 0（例如 -0.01），需要有明確的審核流程決定是否進入下一階段，而非任意解鎖。

**解鎖動作：** Task 4（BSS Safety Gate 跨組件驗證）完成後，定義 Gate 解鎖申請文件模板。

### 10.6 最終結論

> **系統已準備好進行校準修復與指標整合，尚未具備模型擴充或生產部署的條件。**

具體而言：

- ✅ Governance 層：已成熟（Usage Budget Guard + Planner Invariant + BSS Safety Gate）
- ✅ Persistence 層：已建立（Phase 39 JSONL 管線）
- ⏳ Calibration 層：管線已建，修復實驗尚未執行 → **這是下一步**
- ⏳ Metrics 層：分散計算，需整合為 SSOT → **與校準並行**
- ⏳ Architecture 層：LeagueAdapter 尚未建立 → **校準後的 P1 工作**
- 🔴 Model 層：BSS < 0，封鎖所有 Ensemble / Production 操作
- 🔴 Strategy 層：CLV 樣本 < 50，封鎖所有 Production proposal

**下一個 14 天唯一的目標：讓 BSS Safety Gate 能基於校準後的實際數字運作。**

---

## Appendix A — 測試基準（Phase 40 開始前）

```
pytest tests/test_phase36_usage_budget_guard.py \
       tests/test_phase37_mlb_bss_root_cause_audit.py \
       tests/test_phase38_mlb_bss_repair_preview.py \
       tests/test_phase39_mlb_prediction_persistence.py
# → 136 passed（Phase 36:15 + Phase 37:24 + Phase 38:51 + Phase 39:46）
```

Phase 40 任何新測試加入後，此組合必須保持 PASS。

## Appendix B — BSS 數字時間線

| Phase | BSS | Model Brier | Market Brier | 資料 |
|-------|-----|------------|-------------|------|
| Phase 37（報告值） | -14.1% | 0.2796 | 0.2451 | n=2,400（含重複） |
| Phase 37（重算值） | -15.5% | 0.2796 | 0.2420 | 同上，不同計算路徑 |
| Phase 38（清洗後） | **-15.61%** | 0.2796 | 0.2419 | n=2,400（去重後） |
| Phase 39（持久化前） | N/A（JSONL 不存在） | N/A | N/A | per-game 機率未生成 |
| Phase 40 目標（校準後） | **TBD** | TBD（校準後應下降） | 0.2419 | n ≥ 500 walk-forward OOS |

## Appendix C — Hard Rule Compliance Matrix

| Hard Rule | 本文件遵守方式 |
|-----------|-------------|
| 不修改 runtime 行為 | 本文件為 plan-only，無 code 修改 |
| 不修改 production model | 全計畫只做 calibration 實驗（sandbox） |
| 不建立 CANDIDATE_PATCH | BSS < 0 繼續封鎖 |
| 不呼叫外部 API | 文件撰寫不需外部呼叫 |
| 不呼叫外部 LLM | 文件撰寫為 deterministic，不使用 LLM |
| 不繞過 BSS Safety Gate | Gate 狀態：`allowed=False`，持續 |
| 不用 sandbox 結果宣稱 production OK | 校準實驗結果只更新報告，不觸發 deploy |
| 不使用 stock roadmap 作為事實來源 | 全文以 `00-Plan/betting_roadmapplan_20260504.md` 為基準 |
| 使用 betting_roadmapplan_20260504.md 作為主 roadmap | ✅ 文件第一句即聲明 |

---

**PHASE_40_MLB_ROADMAP_PROBLEM_CONVERGENCE_VERIFIED**
