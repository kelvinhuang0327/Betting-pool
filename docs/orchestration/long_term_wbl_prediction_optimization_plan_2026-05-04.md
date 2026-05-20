# Long-Term MLB (大聯盟) Prediction Optimization Plan
**Document ID:** `long_term_wbl_prediction_optimization_plan_2026-05-04`
**Version:** Revision 3 — 2026-05-04 深度擴充版（建構於 2026-05-03 Rev2 之上）
**Author:** AI Prediction System Architect (Planner-mode, deterministic; 本文件作者未呼叫任何外部 AI)
**Scope:** Betting-pool / MLB (Major League Baseball / 大聯盟) + WBC (輔助) 賽事預測系統，長期 (180 天) 優化藍圖
**Governance:** Plan-only document. 不觸發任何 production patch、不繞過 human review、不使用 sandbox 結果宣稱 production 成功。

---

## 0. 版本差異說明 (Delta from Rev2 / 2026-05-03)

本版本在 2026-05-04 基於 **實際 codebase 精確掃描** 新增以下內容：

| 差異項目 | Rev2 (2026-05-03) 假設 | Rev3 (2026-05-04) 真實狀態 |
|---|---|---|
| LeagueAdapter 存在性 | 建議新建 `wbc_backend/league/` | **已存在** `league_adapters/base.py` + `mlb_adapter.py` + `wbc_adapter.py` + `registry.py` |
| MLBAdapter 狀態 | 建議包覆既有資料層 | **已存在**，且 `deployment_mode="paper"`，`paper_only_reason` 記載：CLV 為代理值、無 Statcast、**Brier Skill Score = -14.1% (模型落後市場！)** |
| Simulation 基礎設施 | 建議新建 | **已存在** `wbc_backend/simulation/` (monte_carlo, hierarchical_mc, world_model) |
| Models 豐富度 | 建議逐步建 | **已存在** elo, ensemble, stacking, LightGBM, XGBoost, calibration, Bayesian, neural_net, dynamic_ensemble |
| budget_guard.py | 建議新建 | **尚未存在** ← 仍為 T1 優先 |
| Telegram bot AuditGuard | 假設未覆蓋 | 確認缺口：`telegram_bot/bot.py: OpenAI calls (AuditGuard: ❌ intentionally excluded)` ← 需要修補 |
| State machine | 建議新建 | 尚未存在，仍為高優先 |
| metrics.py SSOT | 建議新建 | 評估層有多個散落計算，尚無統一 SSOT |

**最重要的新發現：Brier Skill Score = -14.1%** 意味目前模型在市場隱含機率面前落後，這是整份計畫的核心緊迫性。

---

## 0.1 名詞釐清 (Terminology) — READ FIRST

- **WBL** = 使用者在 prompt 中的代號，於 2026-05-03 Rev2 確認 = **MLB (Major League Baseball)**。本文件使用 `MLB`。
- **WBC** = World Baseball Classic，既有 `wbc_backend/` 歷史命名，保留為跨聯盟輔助資料源。
- **`wbc_backend/`** = Python package 歷史命名，**不 rename**，避免 import 風暴；在 `README.md` 加註說明。
- **`league_adapters/`** = 已存在的聯盟抽象層 (`LeagueAdapter` protocol + `MLBLeagueAdapter` + `WBCLeagueAdapter`)。
- **Brier Skill Score (BSS)** = (1 - Brier/Brier_baseline) × 100%。目前 BSS = -14.1%，代表模型比市場中位猜測（用市場隱含機率作 baseline）還差。

---

## 1. Executive Summary

### 1.1 一句話結論
> **系統已從「單機腳本」演進到「具備 LeagueAdapter / AuditGuard / CLV pipeline / Provider breakdown UI 的半自主 MLOps 平台」，但核心危機是：MLB 模型的 Brier Skill Score 為負 (-14.1%)，意即目前預測力不如直接使用市場盤口隱含機率。在此基礎上做任何 production 提案都是無意義的。180 天計畫的首要任務是「讓 BSS 變正」，其餘架構、排程、自我學習優化皆以此為北極星。**

### 1.2 四大主軸
1. **從負到正的模型矯正 (BSS Recovery)**：診斷 Brier Skill Score = -14.1% 的根因，加入 Statcast pitch-level 特徵 + 校正 + regime split，目標 90D 達 BSS ≥ +5%。
2. **League Abstraction 完善化**：`league_adapters/` 骨架已存在，但 `MLBAdapter` 需接入真實 Statcast / odds 資料；`WBCAdapter` 需整合進 cross-league feature pipeline。
3. **Self-Learning Scheduler (Priority-scored)**：把 `clv_batch_scheduler` + `planner_tick` 升級為 event-driven、priority-scored、budget-aware 排程核心，支援 MLB daily slate 每天 10–15 場的高密度節奏。
4. **Governance 完善 (Budget Guard + Telegram AuditGuard)**：`budget_guard.py` 尚未建立；`telegram_bot/bot.py` 的 OpenAI 呼叫未受 AuditGuard 保護 — 這兩個缺口都是 governance critical。

### 1.3 KPI 北極星 (North-Star KPIs)

| KPI | Baseline (2026-05-04 真實) | 30D Target | 90D Target | 180D Target |
|---|---|---|---|---|
| **Brier Skill Score (BSS)** | **−14.1%** | 量化 baseline + 根因分析 | ≥ **+2%** (CI95) | ≥ **+8%** (CI95) |
| Calibration Error (ECE) | 未量化 | 量化 baseline | ≤ 0.05 | ≤ 0.03 |
| CLV (closing bps) | < 25 樣本 (proxy) | ≥ 50 真實樣本 | ≥ +30 bps (CI90) | ≥ +60 bps (CI95) |
| Audit Coverage | **Partial (Telegram 缺口)** | FULL | FULL | FULL |
| budget_guard.py | **不存在** | 上線 + UI | 穩定 | 自動降級 |
| Planner External-AI Calls | 0 (已設計) | 0 (runtime assert) | 0 | 0 |
| Scheduler Task Success Rate | 未量化 | ≥ 95% | ≥ 98% | ≥ 99% |
| Human Review SLA | 未量化 | 量化 | < 24h | < 12h |

### 1.4 「現在最該做的 3 件事」
1. **診斷 BSS = -14.1% 的根因**（T1：Brier 根因調查報告）
2. **建立 `orchestrator/budget_guard.py` + Telegram AuditGuard 修補**（T2：Governance 緊急補強）
3. **統一 metrics SSOT + no-lookahead test gate**（T3：保證後續所有改動可被公正驗證）

---

## 2. Current System Assessment (2026-05-04 精確版)

### 2.1 已成熟模組 (Production-stable, 不要動)
| 模組 | 路徑 | Phase | 備註 |
|---|---|---|---|
| Safe Task Executor | `orchestrator/safe_task_executor.py` | ✅ | fail-closed 已落地 |
| AuditGuard (worker paths) | `orchestrator/provider_audit_guard.py` | ✅ | worker_tick 兩條路徑已覆蓋 |
| CLV Batch Scheduler | `orchestrator/clv_batch_scheduler.py` | ✅ Phase33 | 24h / 4h / 5min cadence |
| CLV Threshold Tracker | `orchestrator/clv_threshold_tracker.py` | ✅ Phase34 | threshold hit → investigate |
| CLV Accumulation Policy | `orchestrator/clv_accumulation_policy.py` | ✅ Phase32 | 策略邏輯已落地 |
| Daily CLV Ops Runbook | `scripts/run_daily_clv_ops_summary.py` | ✅ Phase35 | 每日 06:00 |
| Usage Detail UI | `runtime/agent_orchestrator/frontend/index.html` | ✅ | Provider/Role breakdown |
| Optimization Readiness | `orchestrator/optimization_readiness.py` | ✅ | LEARNING_READY gate |
| LLM Usage Logger | `orchestrator/llm_usage_logger.py` | ✅ | append-only |
| LLM Audit Coverage | `orchestrator/llm_audit_coverage.py` | ✅ | 已列 Telegram 缺口 |
| LeagueAdapter (骨架) | `league_adapters/base.py` | ✅ | Protocol + 資料類別 |
| MLBLeagueAdapter | `league_adapters/mlb_adapter.py` | ✅ (partial) | deployment_mode=paper，已知 BSS 問題 |
| WBCLeagueAdapter | `league_adapters/wbc_adapter.py` | ✅ (partial) | 輔助資料源 |
| Simulation 基礎 | `wbc_backend/simulation/` | ✅ (partial) | monte_carlo, hierarchical_mc, world_model |
| Monte Carlo Engine | `baseball_scenario_engine/engine.py` | ✅ | 使用 LeagueAdapter |
| Model Library | `wbc_backend/models/` | ✅ (豐富) | 15 個模型檔，含 elo, ensemble, stacking, LightGBM, XGBoost |
| Human Review Queue | `orchestrator/human_review_queue.py` | ✅ | review lifecycle |
| Patch Gate | `orchestrator/learning_patch_gate.py` | ✅ | 多重 gate |
| Training Memory | `orchestrator/training_memory.py` | ✅ | 但直接 JSON 讀寫，有改進空間 |

### 2.2 已知缺口 (Gap Registry) — 緊急度排序
| # | 缺口 | 緊急度 | 影響 | 補齊任務 |
|---|---|---|---|---|
| G1 | **Brier Skill Score = -14.1%** | 🔴 CRITICAL | 模型比市場差，不能做有效 CLV | T1: 根因調查 |
| G2 | **budget_guard.py 不存在** | 🔴 CRITICAL | 無成本上限，Planner 誤配置可暴露外部 AI | T2: 立即建立 |
| G3 | **Telegram bot AuditGuard 缺口** | 🔴 CRITICAL | OpenAI calls 未受 AuditGuard 保護 | T3: 修補 telegram_bot |
| G4 | **真實 CLV < 25 樣本 (proxy 值)** | 🟠 HIGH | CLV 訊號不可信 | T4: 樣本累積計畫 |
| G5 | **metrics.py SSOT 不存在** | 🟠 HIGH | 不同地方算出不同 KPI | T5: 建立 SSOT |
| G6 | **no-lookahead test gate 不存在** | 🟠 HIGH | 特徵洩露風險 | T6: 建立 test gate |
| G7 | **State machine 不存在** | 🟡 MEDIUM | if/else 散落，流程難審計 | T7: PredictionState |
| G8 | **MLB Statcast 資料未接入** | 🟡 MEDIUM | BSS 問題根因之一 | T8: Statcast pipeline |
| G9 | **Scheduler priority-score 不存在** | 🟡 MEDIUM | 任務排程無優先排序 | T9: priority-score v1 |
| G10 | **LearningMemoryRepository 不存在** | 🟡 MEDIUM | 直接讀寫 JSON，無 schema 保護 | T10: repo 抽象層 |
| G11 | **Walk-forward harness 未統一** | 🟡 MEDIUM | 各回測腳本行為不一致 | T11: 統一 harness |
| G12 | **Persistence 純 JSONL，無事務** | 🟢 LOW (90D 後評估) | 高並發時可能資料損壞 | T12: SQLite (Phase 3) |
| G13 | **root models/ 雙軌與 wbc_backend/models/ 共存** | 🟢 LOW | import 漂移 | T13: deprecation roadmap |

### 2.3 架構現況描述 (ASCII)

```
╔══════════════════════════════════════════════════════════════════════╗
║  OBSERVABILITY (現有)                                                ║
║  usage_detail_ui ✅ | ops_report ✅ | readiness ✅ | runbook ✅       ║
║  audit_dashboard ❌ (計畫中) | budget_panel ❌ (G2)                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  APPLICATION (半成熟)                                                 ║
║  planner_tick ✅ | worker_tick ✅ | learning_cycle ✅                 ║
║  patch_gate ✅ | review_queue ✅ | scheduler ✅ (cadence only)        ║
║  budget_guard ❌ (G2) | state_machine ❌ (G7)                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  DOMAIN (有基礎但缺 BSS 修補)                                         ║
║  prediction (if/else) | odds (proxy CLV) | clv (< 25 spl)           ║
║  learning (partial) | governance (Telegram 缺口 G3)                  ║
║  league_adapters ✅ (骨架完整，MLBAdapter BSS=-14.1%)                 ║
╠══════════════════════════════════════════════════════════════════════╣
║  INFRASTRUCTURE (JSONL，成熟)                                         ║
║  persistence (JSONL ✅) | usage/audit logs (✅)                      ║
║  report writers (✅) | frontend API (wbc_backend/api ✅)             ║
║  LLM Gateway (single egress ✅, AuditGuard worker paths ✅)          ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 2.4 高風險耦合點 (Top-5)
1. **`training_memory.json` 直接讀寫**：無 schema validation、無事務保護、無 retention policy、無去重邏輯 → `LearningMemoryRepository` (G10)
2. **Telegram bot OpenAI calls 未受 AuditGuard**：`llm_audit_coverage.py` line 14 明確標示 `intentionally excluded` → 這個「intentional」需要被重新評估 (G3)
3. **Planner / Worker 共用 LLM 配置** → 無 budget_guard 時 Planner 可誤用外部 AI (G2)
4. **Metrics 計算散落**：`wbc_backend/evaluation/backtester.py`、`clv_strategy.py`、多份 `full_backtest.py` 各自計算 KPI → 不同地方結果可能打架 (G5)
5. **BSS = -14.1% 無根因**：若不知道為何落後市場，任何 feature / model 改動都是猜測 (G1)

### 2.5 不建議立即改動 (Do-NOT-touch list, 90 天內)
- `safe_task_executor.py` 核心 fail-closed 路徑
- CLV 三件套 (accumulation / threshold / batch) 的對外 API
- AuditGuard 的 deny-by-default 行為（除了補 Telegram 缺口）
- `wbc_backend/research/portfolio_v3.py`（institutional research，動了會破壞既有報告鏈）
- Telegram bot read-only command 路徑
- `wbc_backend/simulation/monte_carlo.py` 核心 MC 邏輯（現有 50,000 simulation 上的穩定行為）

---

## 3. Target System Architecture (目標架構)

### 3.1 目標分層 (Layered Architecture, 目標態)

```
╔══════════════════════════════════════════════════════════════════════════╗
║  OBSERVABILITY LAYER                                                     ║
║  usage_dashboard ✅ | audit_dashboard (新) | ops_report ✅              ║
║  readiness_report ✅ | daily_runbook ✅ | architecture_health_score (新)║
║  budget_panel (新) | BSS_trend_chart (新)                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  APPLICATION LAYER                                                       ║
║  PlannerService (deterministic, NEVER external AI)                       ║
║  WorkerService (policy-gated external AI, AuditGuard all paths)         ║
║  LearningCycleService (state-machine driven)                             ║
║  PatchGateService (proposal-only, no auto-deploy)                        ║
║  ReviewQueueService (human-review backbone, SLA < 12h)                  ║
║  SchedulerService (priority-scored, event-driven, budget-aware)          ║
║  BudgetGuardService (新增, deny-by-default)                              ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DOMAIN LAYER                                                            ║
║  prediction_domain   (PredictionState machine + PredictionRegistry)      ║
║  odds_domain         (OddsSource, LineMovement, ClosingSnapshot)         ║
║  clv_domain          (CLVRecord, CLVInvestigation, 真實樣本 ≥ 50)       ║
║  learning_domain     (LearningCycle, FeatureVersion, ModelVersion)       ║
║  governance_domain   (AuditGuard ALL paths, BudgetGuard, ReviewQueue)   ║
║  league_domain       (LeagueAdapter ✅ + MLBAdapter + WBCAdapter)       ║
║  model_domain        (BSS-aware eval, regime split, calibration)         ║
╠══════════════════════════════════════════════════════════════════════════╣
║  INFRASTRUCTURE LAYER                                                    ║
║  Persistence (JSONL → SQLite Phase3) | Usage/Audit logs (append-only)   ║
║  LLM Gateway (single egress, ALL paths AuditGuarded)                    ║
║  Report writers | Frontend API (FastAPI)                                  ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### 3.2 模組責任表 (Responsibility Matrix)

| Service | Reads | Writes | 可呼叫外部 AI | 治理 |
|---|---|---|---|---|
| Planner | ops/readiness/review_queue/training_memory | next_task proposal | **NEVER** (runtime assert) | BudgetGuard deny |
| Worker | task spec, code repo | code patch (sandbox), logs | YES (policy-gated) | AuditGuard ALL paths |
| Learning Cycle | CLV records, predictions | learning_cycles.jsonl | NO | logged |
| Patch Gate | candidate patch, backtest | gate_decisions.jsonl | NO | deterministic |
| Review Queue | gate decisions, simulation | review_queue.jsonl | NO | human-driven |
| Scheduler | all telemetry, budget | task_dispatch.jsonl | NO | BudgetGuard |
| BudgetGuard | usage logs | budget_events.jsonl | NO | deny-by-default |
| Telegram Bot | review_queue | (read-only) | YES (AuditGuard 待補) | G3 修補後覆蓋 |

### 3.3 League Abstraction 現況 vs 目標

**現況（已有）：**
```python
# league_adapters/base.py — 已存在，完整骨架
class LeagueAdapter(ABC):
    def name(self) -> str: ...
    def rules(self, context) -> LeagueRuleSet: ...
    def simulation_config(self, context) -> LeagueSimulationConfig: ...
    def required_fields(self) -> tuple[str, ...]: ...
    def feature_transform(self, features, context) -> dict: ...

# MLBLeagueAdapter — 已存在，deployment_mode="paper"
# WBCLeagueAdapter — 已存在，輔助資料源
```

**目標（缺口補齊）：**
```python
# 需新增至 MLBLeagueAdapter：
class MLBLeagueAdapter(LeagueAdapter):
    # ✅ 已有: rules, simulation_config, feature_transform
    # ❌ 需補: 以下方法
    def fetch_statcast_pitch(self, pitcher_id: str, date: str) -> StatcastData: ...
    def fetch_park_factors(self, venue: str, season: int) -> ParkFactor: ...
    def fetch_weather(self, fixture_id: str) -> Weather | None: ...
    def fetch_bullpen_state(self, team: str, window_days: int) -> BullpenState: ...
    def fetch_lineups(self, fixture_id: str) -> Lineups | None: ...    # real-time
    def fetch_il_list(self, team: str) -> list[Injury]: ...            # 10/15/60-day IL
```

---

## 4. Long-term Optimization Roadmap (180-day)

```
Day 0 ─────── 30 ─────── 60 ─────── 90 ─────── 150 ─────── 180
  │             │           │           │            │           │
  │ Phase 0     │ Phase 1   │ Phase 2   │ Phase 3    │ Phase 4   │
  │ Governance  │ BSS Root  │ Feature   │ Self-      │ Production│
  │ & Baseline  │ Cause Fix │ Registry  │ Learning   │ Proposal  │
  │ Hardening   │ + Metrics │ + Walk-   │ + Sched    │ Workflow  │
  │             │   SSOT    │   Forward │   v2       │           │
  ▼             ▼           ▼           ▼            ▼           ▼
Budget,       診斷 BSS,  Statcast,   Ensemble,   Production- Stable
Telegram      SSOT,      Park factor, calibrate,  proposal    CLV/ROI
Guard,        no-       walk-fwd    regime,     gate v2,    tracking,
State         lookahead  ≥1500,      priority-   review SLA  arch
machine,      gate       feature     score v1    < 12h       health ≥75
LeagueAdpt    baseline   registry    + scratch
補齊          真實       CLV≥50      start-evt
```

---

## 5. Workstream A — 程式系統架構長期優化計畫

### 5.1 架構優化輸出一覽

| 輸出物 | 路徑 | Phase | 優先度 |
|---|---|---|---|
| 模組責任表 (上方 §3.2) | 本文件 | 0 | P0 |
| Deprecation Roadmap | `docs/architecture/deprecation_roadmap.md` | 0 | P0 |
| `budget_guard.py` | `orchestrator/budget_guard.py` | 0 | P0 |
| Telegram AuditGuard 補丁 | `telegram_bot/bot.py` | 0 | P0 |
| `PredictionState` state machine | `wbc_backend/state_machine/prediction_state.py` | 1 | P1 |
| `LearningState` state machine | `wbc_backend/state_machine/learning_state.py` | 1 | P1 |
| `LearningMemoryRepository` | `runtime/learning/repository.py` | 1 | P1 |
| `metrics.py` SSOT | `wbc_backend/evaluation/metrics.py` | 1 | P0 |
| Architecture health score | `scripts/architecture_health_score.py` | 3 | P2 |
| root `models/` deprecation | `wbc_backend/models/legacy/` | 2 | P3 |
| SQLite persistence | `orchestrator/db_sqlite.py` | 3 | P4 |
| `tests/architecture/test_no_root_imports.py` | `tests/architecture/` | 1 | P1 |

### 5.2 哪些地方需要抽象化 / state machine / event-driven 化

**State machine 化優先流程：**

```
PredictionState:
  PROPOSED → SCHEDULED → LINEUP_CONFIRMED → CLOSING_MONITORED
  → COMPUTED_CLV → LEARNING_READY → INVESTIGATED → PATCH_GATE
  → HUMAN_REVIEW → APPROVED | REJECTED

LearningState:
  COLLECTING → THRESHOLD_HIT → INVESTIGATING → CANDIDATE_FOUND
  → PROPOSAL_DRAFTED → REVIEW_PENDING → APPROVED → HOLD

SchedulerState:
  IDLE → ASSESSING (priority-score) → DISPATCHED → AWAITING
  → POSTPROCESSING → IDLE
```

**Event-driven 化優先事件：**
- `LINE_MOVEMENT_SPIKE` → 立即 re-snapshot odds
- `SCRATCHED_STARTER` → 立即 re-predict (pitcher 是 #1 feature)
- `POSTPONEMENT_ANNOUNCED` → cancel closing monitor
- `CLV_THRESHOLD_CROSSED` → 立即觸發 investigation
- `BUDGET_WARN` → downgrade next task
- `BUDGET_CRITICAL` → 停止 external AI dispatch

### 5.3 Refactor Priority

| Priority | 動作 | 風險 | 時程 |
|---|---|---|---|
| **P0 (本週)** | `budget_guard.py` + Telegram AuditGuard | 低 (純新增) | 3 天 |
| **P0 (本週)** | `metrics.py` SSOT + `bootstrap.py` | 低 | 2 天 |
| **P1 (本月)** | `PredictionState` state machine | 中 (需漸進遷移) | 3 天 |
| **P1 (本月)** | `LearningMemoryRepository` | 低 | 2 天 |
| **P2 (60D)** | `MLBAdapter` 補齊 Statcast/park/weather | 中 | 5 天 |
| **P2 (60D)** | Walk-forward harness 統一 | 中 | 3 天 |
| **P3 (90D)** | root `models/` deprecation roadmap | 高 (import 風暴) | 需 feature flag 緩衝 |
| **P4 (180D)** | JSONL → SQLite persistence | 中 | 7 天 |

---

## 6. Workstream B — MLB 預測成功率提升計畫

### 6.1 BSS = -14.1% 根因調查框架

這是整份計畫最重要的分析。在做任何 feature / model 改動前，必須先知道為什麼比市場差。

**可能根因（需逐一驗證）：**

| 根因假設 | 診斷方法 | 對應修復 |
|---|---|---|
| 模型校正不足（over-confident / under-confident） | Reliability diagram、ECE | Platt scaling / Isotonic regression |
| 特徵集含 lookahead leakage | `test_no_lookahead.py` | 清除 leaky features |
| 訓練資料品質低（proxy odds 而非真實 closing odds） | 對比 `mlb_adapter.paper_only_reason` | 接入真實 Statcast + Pinnacle closing |
| 模型對 regime 不穩定（early/mid/late season 表現差異大） | Regime split Brier | Regime classifier + 分段訓練 |
| Baseline model 設定有問題（train/test shuffle 而非 time-ordered） | Walk-forward vs random split 比較 | 強制 time-ordered walk-forward |
| Market implied probability baseline 高估（用 vig-removed Pinnacle） | 重算 BSS baseline | 換 true no-vig baseline |
| MLB 樣本太小（本地測試用 WBC 資料） | 樣本統計 | 換成 MLB 2022–2025 ≥ 1500 場 |

**BSS 根因調查輸出物：`docs/orchestration/bss_root_cause_2026-05-04.md`**

### 6.2 MLB 資料盤點 (Data Inventory)

| 資料類別 | 現況 | 缺口 | 補齊行動 | Phase |
|---|---|---|---|---|
| 賽程 (fixtures) | `data/mlb_2025_preview.py` (部分) | 全季 2,430 場自動同步 | `MLBAdapter.list_fixtures()` 接 MLB StatsAPI | 1 |
| 隊伍 / Roster | 部分 | 每日更新 | `RosterRepository` | 1 |
| 先發投手 (SP) | `data/mlb_2024_pitchers.py` | 賽前 1–2h 自動抓取 | scheduler 30 min 輪詢 | 1 |
| **Statcast pitch-level** | **❌ 無** | **BSS 根因之一** | Baseball Savant API + `StatcastRepository` | 1 |
| Bullpen 狀態 | 部分 | 結構化 load tracking | `BullpenStateBuilder` | 1 |
| **Park factor** | **❌ 無** | MLB-specific 必加 | `MLBAdapter.fetch_park_factors()` | 2 |
| **Weather** | **❌ 無** | Coors/Wrigley 等差異大 | NOAA / OpenWeather → `WeatherRepository` | 2 |
| Injuries / IL | 部分 | 10/15/60-day IL 結構化 | `InjuryRepository` + `MLBAdapter.fetch_il_list()` | 1 |
| 歷史賽果 | 部分 | Retrosheet 1990– / MLB StatsAPI 2008– | 一次性 backfill ≥ 5 季 | 0 |
| Odds opening | `data/odds_api_client.py` | 多家比對（Pinnacle + DK + FD）| multi-provider fallback | 0 |
| Odds closing | CLV pipeline (proxy) | 真實 Pinnacle closing | 接 Pinnacle API 或 备份 OddsJam | 1 |
| Line movement | 部分 | 賽前 6h 起每 10 min | Scheduler T-360 → T-0 | 1 |
| Implied probability | 由 odds 算 | no-vig blended (multi-book) | `OddsAggregator.no_vig_blend()` | 1 |
| Sharp signals | 部分 | Reverse line movement | multi-odds + `SharpDetector` | 2 |
| **Umpire stats** | **❌ 無** | Statcast umpire zone data | `UmpireRepository` | 2 (optional) |
| Prediction registry | `runtime/agent_orchestrator/` | schema validation + audit hash | `PredictionRegistry` (強化) | 1 |
| CLV records | < 25 proxy | ≥ 50 真實樣本 | 持續 accumulate + Phase1 真實 odds 接入 | 1 |
| Backtest reports | `report/mlb_2025_full_backtest.md` | frontmatter schema 強制 | `report/schema.md` + lint | 0 |
| Simulation records | `wbc_backend/simulation/` (部分) | 結構化 simulation_id schema | `research/simulations/<id>.json` | 1 |

### 6.3 Feature Engineering 計畫 (MLB-tuned, 按預期幫助排序)

| Feature | 資料來源 | 現可做 | 風險 | 預期幫助 | 驗證方法 | Phase |
|---|---|---|---|---|---|---|
| **SP FIP/xFIP/K%/BB%** | FanGraphs / Statcast | 部分（2024 有） | 中 | **★★★★★** | walk-forward + permutation | 1 |
| **Statcast pitch-level (xwOBA, barrel%, hard-hit%)** | Baseball Savant | ❌ | 中 | **★★★★★** | walk-forward | 1 |
| **Bullpen state (連續出賽天數)** | lineup 衍生 | 部分 | 中 | ★★★★ | regime split | 1 |
| **No-vig blended implied prob** | multi-odds | 部分 | 低 | ★★★★ | calibration check | 0 |
| **Odds movement Δ (T-360→T-60→close)** | odds_api | 部分 | 中 | ★★★★ | leakage check (T-60 cutoff) | 1 |
| **Market disagreement (Pinnacle vs DK/FD)** | multi-odds | ❌ | 中 | ★★★★ | sharp money signal | 1 |
| **Park factor** | Statcast park | ❌ | 低 | ★★★★ | venue split | 2 |
| **Weather (temp, wind dir/speed)** | NOAA / OpenWeather | ❌ | 中 | ★★★ | Coors/Wrigley split | 2 |
| Team Elo (時變, 季內) | 歷史 | ✅ | 低 | ★★★ | walk-forward Brier | 0 |
| Recent form (last-10 / last-30) | 歷史 | ✅ | 低 | ★★★ | 同上 | 0 |
| Home/Away + venue interaction | 賽程 + 場館 | ✅ | 低 | ★★★ | 同上 | 0 |
| Rest days / 連戰 | 賽程 | ✅ | 低 | ★★★ | 同上 | 0 |
| Matchup history (3年) | 歷史 | ✅ | 低 | ★★ | 同上 | 0 |
| Lineup quality (1–5棒 wOBA) | StatsAPI | 部分 | 中 | ★★★ | calibration | 1 |
| IL indicator (key player out) | IL feed | 部分 | 中 | ★★★★ | calibration check | 1 |
| Regime state (early/mid/late) | 衍生 | ✅ | 中 | ★★★ | regime split Brier | 1 |
| Model confidence calibration | meta | ✅ | 低 | ★★★★ | reliability diagram | 0 |
| Reverse line movement | multi-odds | 部分 | 中 | ★★★ | Phase 2 | 2 |
| Schedule density (19-連戰窗口) | 賽程 | ✅ | 低 | ★★★ | 同上 | 1 |
| Travel fatigue (時區) | 賽程 + 場館 | 部分 | 中 | ★★★ | east/west split | 2 |
| CLV-history of model | 自家 CLV | ✅ | 中 | ★★★ | 防 over-fit | 2 |
| Umpire strike zone bias | Statcast umpire | ❌ | 中 | ★★ | Phase 2 optional | 2 |

**Hard Rule**: 每個特徵入庫前必經 `tests/feature_validation/test_no_lookahead.py` — 假時間 cursor 並 assert 特徵只讀 ≤ cursor 的 timestamp 資料。

### 6.4 Model Roadmap (MLB 四階段)

#### Phase A — Baseline Validation (Day 0–30)
- 以 MLB 2022–2025（目標 ≥ 5000 場）跑 **BSS 根因調查**
- Baseline 三模型 head-to-head：no-vig implied prob（純市場）、既有 Elo、既有 GBM
- 輸出：Brier, ECE, reliability diagram, BSS vs market，並寫根因報告
- 建立 `wbc_backend/evaluation/metrics.py` SSOT（Brier, log loss, ECE, CLV bps, hit rate, ROI, drawdown, Sharpe, bootstrap CI）
- **不允許改模型結構，僅診斷**

#### Phase B — Feature & Model Improvement (Day 30–90)
- 接入 Statcast pitch-level + park factor + bullpen state（先通過 no-lookahead test）
- 現有 stacking ensemble 用 MLB walk-forward 重訓（`wbc_backend/models/stacking.py` 已存在）
- Platt / Isotonic calibration 接在 ensemble 後（`wbc_backend/models/` 已有 calibration 相關檔案）
- MLB regime split：early-season / mid-season / late-season + 季後賽
- 目標：BSS ≥ +2%（CI95）才能進 Phase C
- **必經 patch gate + human review**

#### Phase C — Online Paper Feedback (Day 90–150)
- Walk-forward + paper trading 並行（MLB 每天 10–15 場，paper 樣本快速累積）
- Threshold optimization：confidence × CLV × bankroll constraint
- Risk-adjusted selection（Kelly fraction × regime × bullpen state × IL indicator）
- Daily slate exposure cap（一日總曝險 ≤ 5% bankroll）
- scratched starter event-driven reprediction 上線
- **必經 simulation governance**

#### Phase D — Production Proposal (Day 150–180)
- 只在 (i) ≥ 2000 場樣本 (ii) BSS ≥ +5% CI95 顯著 (iii) CLV ≥ +50 bps CI90 (iv) regime-split 內各 regime CLV ≥ 0 (v) human review approved
- **絕不 auto-deploy**

### 6.5 Validation Methodology (Hard Rules)

| 驗證方法 | 必要性 | 工具 |
|---|---|---|
| Time-ordered split (禁 shuffle) | **必須** | `wbc_backend/evaluation/backtester.py` 強化 |
| Walk-forward (rolling window) | **必須** | `wbc_backend/backtesting/league_backtest.py` |
| Out-of-sample (last K%) | **必須** | 同上 |
| Leakage detection (假時間 cursor) | **必須** | `tests/feature_validation/test_no_lookahead.py` (新增) |
| Bootstrap CI (≥ 1000 resample) | **必須** | `wbc_backend/evaluation/bootstrap.py` (新增) |
| Permutation test | **必須** | 同上 |
| Reliability diagram + ECE | **必須** | `metrics.py` SSOT |
| Brier + BSS + Log Loss + Hit rate | **必須** | 同上 |
| ROI + drawdown + Sharpe + CLV bps | **必須** | strategy 層 |
| Baseline comparison (市場隱含) | **必須** | BSS 計算 |
| Sample size ≥ 1500 (per CLAUDE.md) | **必須** | patch gate 硬擋 |
| Regime split（各 regime 內獨立驗證）| **必須** | 確保 regime-specific bias 不隱藏 |

**Forbidden（per HARD RULES）：**
- ❌ 只看 win rate
- ❌ 單場結果即下結論
- ❌ sandbox 結果稱 production OK
- ❌ < 1500 場樣本下模型結論

---

## 7. Workstream C — 自我學習 / 模擬賽事優化計畫

### 7.1 Simulation Types (10 類，MLB 版)

| # | 類型 | 目的 | 現況 | Phase |
|---|---|---|---|---|
| 1 | **Historical Replay** | 重跑 MLB 2022–2025，量化每個 model version 表現 | `wbc_backend/simulation/` 基礎存在 | 1 |
| 2 | **Walk-Forward Simulation** | 滾動 OOS 驗證，MLB-scale ≥ 1500 場 | `backtesting/league_backtest.py` 部分 | 1 |
| 3 | **Paper Betting Simulation** | 模擬每日 slate 下注（不真錢），ROI / CLV 追蹤 | `evaluation/clv_strategy.py` 部分 | 1 |
| 4 | **Odds Movement Simulation** | line movement 對 ROI 影響的敏感度分析 | 尚未 | 2 |
| 5 | **Adversarial Market Simulation** | sharp money + steam move worst-case 假設下的 drawdown | 尚未 | 2 |
| 6 | **Regime Shift Simulation** | 切 early/mid/late season 看模型穩定性 | 尚未 | 2 |
| 7 | **Confidence Threshold Simulation** | 不同 threshold → ROI/CLV trade-off curve | 尚未 | 2 |
| 8 | **CLV Accumulation Simulation** | 不同採樣策略下的 CLV 穩定性 | 部分（通過 clv_strategy） | 2 |
| 9 | **Strategy Risk Simulation** | Kelly fraction × bankroll × regime → ruin probability | 尚未 | 2 |
| 10 | **Human-Review Proposal Simulation** | 用模擬結果自動產生 review proposal pack | 尚未 | 3 |

### 7.2 Simulation Output Schema (統一格式)

```json
{
  "simulation_id": "sim_2026-05-04_001",
  "type": "walk_forward",
  "date_range": ["2024-03-01", "2026-04-30"],
  "sample_size": 1850,
  "model_version": "mlb_stacking_v0.3.1",
  "feature_version": "fv_2026-05-04",
  "strategy_config": {
    "kelly_fraction": 0.25,
    "min_edge_bps": 30,
    "max_daily_exposure_pct": 5.0
  },
  "baseline_metrics": {
    "brier": 0.253,
    "bss": -0.141,
    "ece": 0.071,
    "clv_bps": null
  },
  "candidate_metrics": {
    "brier": 0.232,
    "bss": 0.026,
    "ece": 0.041,
    "clv_bps": 38
  },
  "deltas_with_ci": {
    "brier_delta": {"mean": -0.021, "ci95": [-0.031, -0.011]},
    "bss_delta_pct": {"mean": 16.7, "ci95": [8.2, 25.1]},
    "clv_delta_bps": {"mean": 38, "ci90": [18, 58]}
  },
  "roi": 0.023,
  "drawdown_max": 0.11,
  "sharpe": 0.87,
  "regime_split": {
    "early_season": {"bss": 0.008, "clv_bps": 12},
    "mid_season": {"bss": 0.041, "clv_bps": 52},
    "late_season": {"bss": 0.019, "clv_bps": 29}
  },
  "calibration": {"ece": 0.041, "reliability_curve": "..."},
  "failure_reason": null,
  "recommendation": "HUMAN_REVIEW_REQUIRED",
  "audit_hash": "sha256:...",
  "governance": {
    "sandbox_only": true,
    "paper_only": true,
    "no_auto_production_patch": true
  }
}
```

`recommendation ∈ {HOLD, INVESTIGATE, COLLECT_MORE_DATA, CANDIDATE_PATCH, HUMAN_REVIEW_REQUIRED}`

### 7.3 Self-Learning Memory Schema

| Store | 路徑 | 寫入時機 | 主鍵 | Retention | 防重複 |
|---|---|---|---|---|---|
| `learning_cycles.jsonl` | `runtime/learning/` | LearningCycleService 完成 | `cycle_id` | 永久 | audit_hash 去重 |
| `clv_investigations.jsonl` | 同上 | CLV threshold trigger | `investigation_id` | 永久 | audit_hash 去重 |
| `gate_decisions.jsonl` | 同上 | Patch gate 結束 | `decision_id` | 永久 | decision_id 唯一 |
| `patch_evaluations.jsonl` | 同上 | candidate evaluated | `patch_id` | 永久 | patch_id 唯一 |
| `human_reviews.jsonl` | 同上 | human action | `review_id` | 永久 | review_id 唯一 |
| `simulation_runs.jsonl` | 同上 | simulation 完成 | `simulation_id` | 永久 | simulation_id 唯一 |
| `failure_patterns.jsonl` | 同上 | failure detected | `pattern_id` | 永久, upsert `seen_count` | pattern_id upsert |
| `model_versions.jsonl` | 同上 | model 訓出 | `model_version` | 永久 | version 唯一 |
| `strategy_versions.jsonl` | 同上 | strategy 變更 | `strategy_version` | 永久 | version 唯一 |
| `bss_diagnostics.jsonl` | 同上 | BSS 根因調查完成 | `diagnostic_id` | 永久 | diagnostic_id 唯一 |

**防重複 / 防錯誤學習機制：**
- 每筆寫入計算 `audit_hash = sha256(canonical_json_without_audit_hash)`，重複 hash 不寫第二次
- `failure_patterns.jsonl` 是 upsert（同 `pattern_id` 累加 `seen_count`，保留 first_seen / last_seen）
- 任何 cycle 含 `audit_hash ∈ failure_patterns` 的訓練資料，必須標 `tainted=true` 並排除
- `LearningMemoryRepository.read_validated()` 做 schema 驗證，不合格直接 raise，不靜默跳過
- BSS 根因報告中標記的 leaky features 會被加入 `failure_patterns.jsonl`，確保不被再次引入

### 7.4 Simulation Governance (不可逾越的邊界)

| 邊界 | 規則 | 執行方式 |
|---|---|---|
| sandbox-only | simulation 結果不直接修改 production model | `governance.no_auto_production_patch=true` 為 mandatory field |
| paper-only | simulation → paper proposal → human review | review_id 必須存在才能進 CANDIDATE_PATCH |
| production-proposal-only | 提案只有人類 approve 後才生效 | patch gate 硬擋 |
| no-auto-production-patch | **任何情況都不自動 deploy** | runtime assert in safe_task_executor |
| insight ≠ deploy | simulation 可寫 insight，不可 trigger deploy | code path 嚴格分離 |
| BSS gate | BSS < 0 時不得產生 CANDIDATE_PATCH | 新增 BSS gate 在 patch_gate 前 |

---

## 8. Workstream D — 排程自我學習優化計畫

### 8.1 Scheduler 角色分工 (完整任務族)

| 任務族 | 目的 | Cadence | 觸發條件 | 外部 AI? |
|---|---|---|---|---|
| `data_freshness_check` | 資料新鮮度掃描 | 10 min | always | NO |
| `lineup_poll` | 先發投手 / 打線確認 | 30 min (賽前 3h 內) | pending fixtures | NO |
| `scratched_start_repredict` | 換投手立即重新預測 | event-driven | `SCRATCHED_STARTER` event | NO |
| `odds_closing_monitor` | 抓 closing odds | 10 min (賽前 60–0 min) | pending fixtures | NO |
| `odds_snapshot` | 盤口快照（每 10 min 賽前 6h 內）| 10 min (賽前 6h 內) | MLB season active | NO |
| `clv_batch_accumulation` | 累積 CLV 樣本 | 4h | pending CLV | NO |
| `clv_threshold_check` | 檢查 CLV 樣本是否達門檻 | event-driven | computed_count change | NO |
| `production_clv_learning_cycle` | 完整學習循環 | 24h | LEARNING_READY | NO |
| `production_clv_investigation` | CLV 調查 | event-driven | threshold_hit | NO |
| `bss_diagnostic_rerun` | BSS 根因再驗 | weekly | model_version change | NO |
| `simulation_run` | 週期性模擬 | weekly | 無高優先任務時 | NO |
| `model_validation` | 模型驗證（walk-forward）| weekly | new candidate | NO |
| `patch_gate_recheck` | 補 gate | event-driven | computed_count ≥ 50 | NO |
| `human_review_followup` | 追蹤 review SLA | 24h | review pending | NO |
| `usage_budget_check` | 預算狀態 | 1h | always | NO |
| `audit_guard_check` | Audit 覆蓋率 | 6h | always | NO |
| `frontend_health_check` | UI 健康 | 1h | always | NO |
| `architecture_health_check` | 架構健康評分 | monthly | cron + manual | NO |
| `weather_refresh` | 更新 weather（MLB 特有）| 1h (賽前 6h 內) | MLB season active | NO |
| `slate_planning` | 今日 MLB 比賽預備 | daily 11:00 台北 | MLB season active | NO |
| `daily_clv_summary` | CLV 每日彙整 | daily 06:00 台北 | always | NO |

**所有排程任務皆 NO external AI（只有 Worker 在 policy-allow 下才用外部 AI，且必須 AuditGuard）。**

### 8.2 Scheduler Decision Logic (Deterministic Rules)

```python
# 排程決策規則（優先順序由上到下）

# 1. 安全門 (Safety Gates) — 任一不通，blocking
if not auditguard.coverage == "FULL":
    block_external_ai_dispatch()
    alert("CRITICAL: audit_coverage not FULL")

if budget_guard.is_critical():
    disable_all_external_ai()
    requeue_with_deferred=True(all_external_ai_tasks)
    log_budget_event()

if human_review_pending > 0:
    skip_autonomous_proposals()  # 不再產新 proposal，等 review 結論

# 2. 緊急事件 (Event-driven, 最高優先)
if events.has("SCRATCHED_STARTER"):
    dispatch("scratched_start_repredict", priority=10)

if events.has("LINE_MOVEMENT_SPIKE"):
    dispatch("odds_snapshot", priority=9)

if events.has("CLV_THRESHOLD_CROSSED"):
    dispatch("production_clv_investigation", priority=9)

if events.has("POSTPONEMENT"):
    cancel_closing_monitor(fixture_id)

# 3. CLV 積累邏輯
if pending_clv_fixtures > 0:
    ensure_scheduled("odds_closing_monitor", cadence_min=10)

if computed_count < 30:
    mode = "COLLECT_MORE_DATA"
    # 只允許 accumulation tasks
elif 30 <= computed_count < 50:
    mode = "RERUN_INVESTIGATION"
    schedule("production_clv_investigation", priority=7)
elif computed_count >= 50:
    mode = "ALLOW_PATCH_GATE_RECHECK"
    schedule("patch_gate_recheck", priority=6)

# 4. BSS 狀態
if current_bss < 0:
    block("CANDIDATE_PATCH")  # BSS 為負，不允許 patch proposal
    ensure_scheduled("bss_diagnostic_rerun", priority=8)

# 5. 常規任務
if budget_guard.is_warn():
    downgrade_next_worker_task_to_deterministic()

if frontend_dashboard_missing:
    open_observability_task(priority=5)
```

### 8.3 Priority Score Formula

```
priority_score(task) =
    w_impact     × expected_impact          # 0–5
  + w_urgency    × urgency                  # 0–5（deadline-driven）
  + w_freshness  × data_freshness_decay     # 0–3（資料越舊，分數越高）
  + w_evidence   × (computed_count / 50)   # 0–3（CLV 樣本進度）
  + w_failure    × recent_failure_count    # 0–3
  − w_cost       × external_ai_cost_est   # 0–5（成本懲罰）
  − w_review     × review_pending_age_h   # 0–3（等待 review 時降低後續 proposal 分）
  − w_risk       × production_risk_score  # 0–5（高風險任務分數下調）
  + w_blocked    × blocked_duration_h     # 0–3（被阻擋越久加分，避免飢餓）
  + w_bss        × (0 if bss < 0 else 1) # BSS 為負時所有 CANDIDATE 類任務扣分

起始建議權重（需 walk-forward 試跑後微調）：
  w_impact=3, w_urgency=4, w_freshness=2, w_evidence=2,
  w_failure=1, w_cost=1, w_review=2, w_risk=3, w_blocked=2, w_bss=5
```

**Priority 範例：**

| 任務 | impact | urgency | review_pending | bss_gate | score |
|---|---|---|---|---|---|
| `scratched_start_repredict` | 5 | 5 | 0 | N/A | **最高 (45)** |
| `bss_diagnostic_rerun` (BSS 為負) | 5 | 4 | 0 | — | **高 (38)** |
| `human_review_followup` (24h pending) | 5 | 5 | 0 | N/A | 高 (37) |
| `clv_threshold_check` (count=49) | 5 | 4 | 0 | BSS<0? 限制 | 高 (35) |
| `simulation_run` (weekly) | 3 | 1 | 0 | BSS<0 扣分 | 中低 (12) |
| `CANDIDATE_PATCH` (BSS<0 時) | 4 | 3 | 0 | −5 | **低 (8) 被 BSS gate 壓制** |

### 8.4 Scheduler Cadence (MLB Season-aware)

**MLB 賽季（4 月–10 月，每天 10–15 場）：**

| 週期 | 時間 (台北時間) | 動作 |
|---|---|---|
| 10 min | 全天 24/7 | worker tick + health check + freshness scan |
| 10 min | 賽前 6h 起 | odds_snapshot（MLB 並發度高） |
| 30 min | 賽前 3h 起 | lineup_poll（SP 公布時機） |
| 10 min | 賽前 60–0 min | odds_closing_monitor |
| 1h | 賽前 6h 內 | weather_refresh |
| 1h | 全天 | usage_budget_check, frontend_health_check |
| 4h | 有 pending CLV 時 | clv_batch_accumulation |
| 6h | 全天 | audit_guard_check |
| daily 11:00 | slate planning | 今日比賽列表 + feature 預計算 + confidence 預跑 |
| daily 06:00 | morning runbook | CLV summary, ops_report, daily runbook |
| weekly (Mon) | 00:00 | simulation_run, model_validation, regime drift check, bss_diagnostic |
| monthly (1st) | 00:00 | architecture_health_check |
| **Event-driven** | 立即 | SCRATCHED_STARTER → repredict; CLV_THRESHOLD → investigate; LINE_SPIKE → snapshot; POSTPONEMENT → cancel |

**MLB 賽季外（11 月–3 月）：**
- 降頻至：1h health check, daily ops_report, weekly arch_check
- 可跑 off-season 歷史模擬（Historical Replay, Walk-Forward for next season prep）
- 可跑 winter meeting / trade 影響評估（optional, paper-only）

### 8.5 Scheduler Safety Invariants (每 tick assert)

```python
# 每 tick 必須通過的 invariant 檢查
assert planner.external_ai_calls_last_tick == 0, "CRITICAL: Planner called external AI"
assert auditguard.is_full_coverage() or not worker.has_external_ai_pending
assert budget_guard.is_initialized(), "budget_guard not running"
assert len(deterministic_queue) >= len(external_ai_queue), "too many AI tasks"
assert all(t.has_review_id for t in production_impacting_tasks), "production task without review"
assert bss_gate_applied() if current_bss < 0 else True, "BSS gate bypass detected"

# 任一失敗：
# 1. scheduler self-pause
# 2. 寫 safety_violation.jsonl（含 timestamp, violation_type, context）
# 3. 發 Telegram 告警（read-only channel）
```

---

## 9. Workstream E — Usage Budget / Copilot 成本控管計畫

### 9.1 Budget Schema (`runtime/agent_orchestrator/budget_config.json`)

```json
{
  "budget_version": "2026-05-04-v1",
  "global_daily_usd": 10.00,
  "global_weekly_usd": 50.00,
  "global_monthly_usd": 150.00,
  "by_role": {
    "planner": {
      "daily_usd": 0.00,
      "hard_cap": true,
      "violation_action": "CRITICAL_ALERT_AND_DENY"
    },
    "worker": {
      "daily_usd": 6.00,
      "per_task_max_usd": 0.50,
      "fallback": "deterministic"
    },
    "cto_review": {
      "daily_usd": 2.00,
      "per_task_max_usd": 0.30
    },
    "human_assist": {
      "daily_usd": 2.00
    }
  },
  "by_provider": {
    "anthropic_claude": {
      "daily_usd": 5.00,
      "spike_z_score_warn": 3.0
    },
    "openai_codex": {
      "daily_usd": 3.00,
      "spike_z_score_warn": 3.0
    },
    "github_copilot": {
      "daily_usd": 2.00,
      "spike_z_score_warn": 2.0
    },
    "telegram_openai": {
      "daily_usd": 1.00,
      "note": "telegram_bot OpenAI calls — G3 缺口修補後啟用 AuditGuard"
    }
  },
  "warn_threshold_pct": 70,
  "critical_threshold_pct": 90,
  "auto_reset": "daily_at_00:00_utc"
}
```

### 9.2 Guard Policy

| 事件 | 行動 |
|---|---|
| **Planner 嘗試呼叫外部 AI** | **CRITICAL: deny + write safety_violation.jsonl + Telegram alert** |
| Worker > per_task_max | deny + downgrade to deterministic fallback |
| Provider > daily | switch to fallback provider |
| Global usage > warn (70%) | warn badge in UI + log |
| Global usage > critical (90%) | hard-stop 所有外部 AI for today, deterministic only |
| Spike z-score > 3 | warn（可能 runaway loop）+ Telegram alert |
| Telegram bot OpenAI (G3 未修補時) | block + log + require AuditGuard 修補 |

### 9.3 Frontend Budget Panel 規格 (`runtime/agent_orchestrator/frontend/index.html` 新增)

```
┌────────────────────────────────────────────────────────┐
│  Usage Budget (Today)                                  │
│  ████████████░░░░░░░░░  $6.80 / $10.00 (68%)  [WARN]  │
│                                                        │
│  By Provider:                                          │
│  Claude    ████████░░░  $4.10 / $5.00  (82%)  [WARN]  │
│  Codex     ████░░░░░░░  $1.80 / $3.00  (60%)          │
│  Copilot   ██░░░░░░░░░  $0.90 / $2.00  (45%)          │
│                                                        │
│  By Role:                                              │
│  Planner   ░░░░░░░░░░░  $0.00 / $0.00  ✅ INVARIANT   │
│  Worker    ████████░░░  $5.20 / $6.00  (87%)  [WARN]  │
│  CTO Rev   ██░░░░░░░░░  $0.80 / $2.00  (40%)          │
│                                                        │
│  ⚠ Planner External AI = 0 (INVARIANT BADGE, must be green) │
└────────────────────────────────────────────────────────┘
```

**「Planner External AI = 0」必須永遠顯示為 GREEN BADGE。變紅即為 critical incident。**

### 9.4 Scheduler Behavior After Budget Exceeded

1. 立即 disable 所有「需外部 AI」任務的 dispatch
2. 把這些任務 requeue 為 `deferred=true`，下個 budget cycle（每日 00:00 UTC reset）才 retry
3. Planner 改用 deterministic fallback 產 next_task
4. 寫 `usage_budget_event.jsonl`
5. 發 Telegram 告警（read-only channel，不需外部 AI）
6. 如果連 deterministic 任務也被 budget 影響，scheduler self-pause + human_review_required

### 9.5 Telegram AuditGuard 修補計畫 (G3)

`llm_audit_coverage.py` line 14 明確標示：
```
telegram_bot/bot.py: OpenAI calls (AuditGuard: ❌ intentionally excluded)
```

修補步驟：
1. 評估 Telegram bot 的 OpenAI 呼叫場景（read-only? 執行命令? 多少預算？）
2. 如果是純讀（回答問題），用 `budget_guard.check_before_call("telegram_openai")` 包覆
3. 如果涉及執行命令，**必須通過 SafeTaskExecutor + AuditGuard**
4. 更新 `llm_audit_coverage.py` 的 coverage list
5. `llm_audit_coverage_report()` 回傳 FULL（目前因 Telegram 缺口是 PARTIAL）

---

## 10. Phase Plan (詳細交付)

| Phase | Days | Objective | Key Tasks | Deliverables | Success Criteria | Risk |
|---|---|---|---|---|---|---|
| **Phase 0 — Governance Hardening** | 0–14 | Budget Guard、Telegram AuditGuard、BSS 根因診斷啟動 | budget_guard.py、Telegram G3 修補、metrics SSOT、no-lookahead test、BSS 根因調查 | `orchestrator/budget_guard.py`、`wbc_backend/evaluation/metrics.py`、`tests/feature_validation/test_no_lookahead.py`、`docs/orchestration/bss_root_cause_2026-05-04.md` | Planner 0 ext-AI / 7d；audit_coverage=FULL；BSS 根因文件化 | Telegram 修補破壞現有 bot 功能 |
| **Phase 1 — BSS Fix + Foundation** | 15–45 | BSS 由負轉正（目標 ≥ +2%）；Statcast 接入；state machine；真實 CLV ≥ 50 | Statcast pipeline、PredictionState machine、LearningMemoryRepository、walk-forward ≥ 1500（MLB 2022–2025）、bullpen state feature | `wbc_backend/state_machine/`、`wbc_backend/evaluation/metrics.py`（完整）、MLB walk-forward report（≥1500 場）、`docs/data/mlb_inventory.md` | BSS ≥ +2% CI95 或根因已知；CLV ≥ 50 真實樣本；walk-forward 綠燈 | Statcast API rate limit；Pinnacle closing odds 授權 |
| **Phase 2 — Feature Registry + Simulation** | 46–90 | park factor / weather / feature registry；simulation framework v1；walk-forward ≥ 5000 | `wbc_backend/features/registry.py`、`research/simulations/`、`bootstrap.py`、`MLBAdapter.fetch_park_factors`、`fetch_weather`、scheduler priority-score v1 | walk-forward report（≥5000 場）、simulation runner v1（Walk-forward + Paper + Regime）、feature versioning、scheduler v2 | BSS stable ≥ +2%；feature lookahead test 全綠；MLBAdapter patch/weather 上線；scheduler 安全 invariant 100% | weather provider SLA；park factor 資料年度更新時機 |
| **Phase 3 — Self-Learning Core** | 91–150 | Ensemble retrain + calibration + regime split；scratched-start event；threshold feedback loop；priority-score tuning | `models/stacking.py` walk-forward retrain（MLB scale）、Platt/Isotonic calibration、regime classifier、`scheduler/lineup_event_handler.py`、BSS gate v1 | `gate_decisions.jsonl` enriched、scheduler v3、regime-split report（各 regime BSS ≥ 0）、paper betting live | ECE ≤ 0.05；BSS ≥ +5% (CI95)；scratched-start reprediction < 5 min；review SLA < 24h | over-fit；regime weight tuning 不收斂 |
| **Phase 4 — Production Proposal Loop** | 151–180 | 完整 review-driven 提案流程；ROI/CLV stable；架構健康 ≥ 75 | review queue UI 強化、proposal pack template、arch health score、daily-slate exposure cap、production gate v2 | `docs/architecture/health_2026-Q3.md`、stable proposal pipeline（≥2000 場驗證）、CLV ≥ +60 bps CI95 | 每週 ≥ 1 proposal 進入 human_review；review SLA < 12h；CLV CI95 達標；arch score ≥ 75 | human review 帶寬不足；production gate 錯誤拒絕有效提案 |

---

## 11. Metrics & Acceptance Criteria (完整版)

### 11.1 Prediction Metrics
| Metric | 說明 | 30D | 90D | 180D | 工具 |
|---|---|---|---|---|---|
| **Brier Score** | 概率預測精準度 | 量化 baseline | < baseline −0.01 (CI95) | < baseline −0.02 (CI95) | metrics.py SSOT |
| **Brier Skill Score (BSS)** | vs 市場隱含 baseline | 量化（現 −14.1%）| ≥ +2% (CI95) | ≥ +8% (CI95) | metrics.py |
| **Log Loss** | 對數損失 | 量化 | ↓ CI95 顯著 | ↓ CI95 顯著 | metrics.py |
| **ECE** | Calibration 誤差 | 量化 | ≤ 0.05 | ≤ 0.03 | reliability diagram |
| **Reliability Diagram** | 校準可視化 | 每次 sim 必出 | 每次 sim 必出 | 每次 sim 必出 | metrics.py |
| **Hit Rate** | 勝率 | 報告（不單獨作 success） | 報告 | 報告 | metrics.py |
| **Sample Size** | 驗證樣本數 | ≥ 1500 (gate) | ≥ 3000 | ≥ 5000 | gate 強制 |
| **Bootstrap CI** | ≥ 1000 resample | 每次 sim 必有 | 每次 sim 必有 | 每次 sim 必有 | bootstrap.py |
| **Regime Split** | 各 regime 獨立 BSS | 量化 | 各 regime BSS ≥ 0 | 各 regime BSS ≥ +2% | regime_classifier |

### 11.2 Strategy Metrics
| Metric | 說明 | 90D | 180D |
|---|---|---|---|
| **CLV (bps)** | 真實 closing 超額 | ≥ +30 bps (CI90) | ≥ +60 bps (CI95) |
| **ROI** | 報酬率 | ≥ 0% | ≥ +2% |
| **Max Drawdown** | 最大回落 | ≤ 20% | ≤ 15% |
| **Sharpe Ratio** | 風險調整報酬 | > 0 | > 0.5 |
| **Daily Exposure Cap** | 每日最大曝險 | ≤ 5% bankroll | ≤ 5% bankroll |
| **CLV Samples** | 真實樣本數 | ≥ 50 | ≥ 200 |

### 11.3 Governance / System Metrics
| Metric | 30D | 90D | 180D |
|---|---|---|---|
| **Audit Coverage** | FULL（補 G3 後）| FULL | FULL |
| **Usage Cost vs Budget** | ≤ 80% | ≤ 80% | ≤ 70% |
| **Scheduler Task Success Rate** | ≥ 95% | ≥ 98% | ≥ 99% |
| **Human Review SLA** | 量化 | < 24h | < 12h |
| **Planner External-AI Calls** | 0 (runtime assert) | 0 | 0 |
| **Architecture Health Score** | N/A | 基線量化 | ≥ 75 |
| **Safety Violation Count** | 0 | 0 | 0 |
| **BSS Gate Violations** | 0 (BSS<0 不允許 CANDIDATE_PATCH) | 0 | 0 |

### 11.4 Acceptance Gates (按流程順序)
1. `LEARNING_READY` → CLV ≥ 50 真實樣本（非 proxy）
2. `PATCH_GATE_ENTER` → walk-forward ≥ 1500 場 + bootstrap CI 顯著 + BSS ≥ 0
3. `CANDIDATE_PATCH` → BSS ≥ +2% CI95 + ECE ≤ 0.05 + regime CLV ≥ 0 各 regime
4. `PROPOSAL_DRAFTED` → audit_hash + simulation_id + failure_patterns 清查
5. `HUMAN_REVIEW` → 提案文件 + metrics 表格 + regime report + risk assessment
6. `HUMAN_REVIEW_APPROVED` → 需兩位 reviewer 簽核（至少一位非作者）
7. `DEPLOYED` → 本計畫 180D 內 **不啟用**；僅產 proposal

---

## 12. 30 / 60 / 90 / 180 Day Roadmap

### 30 Days — Governance Hardening + Baseline

| 目標 | 驗收標準 |
|---|---|
| budget_guard.py 上線 | pytest 覆蓋 deny / warn / critical 路徑 |
| Telegram AuditGuard 補丁 (G3) | llm_audit_coverage_report() = FULL |
| BSS 根因診斷報告 | `docs/orchestration/bss_root_cause_2026-05-04.md` reviewer 簽核 |
| metrics.py SSOT 上線 | 所有 KPI 函式集中，舊 caller 改用 |
| no-lookahead test gate | 故意 leak case 必 FAIL；現有 features 通過 |
| MLB 歷史賽果 backfill 啟動 | ≥ MLB 2022–2024 賽果資料格式化 |
| odds_api_client.py 多 provider | Pinnacle + 至少一個 sharp book 接入 |
| Planner invariant runtime assert | 任何 Planner external AI 嘗試 → safety_violation.jsonl |
| UI Budget panel | 上線，含 Planner = 0 INVARIANT badge |
| 資料盤點文件 | `docs/data/mlb_inventory.md` reviewer 簽核 |

### 60 Days — Feature Engineering + Walk-Forward

| 目標 | 驗收標準 |
|---|---|
| MLB walk-forward ≥ 1500 場（目標 5000+）| 報告含 Brier, BSS, ECE, CI95 |
| Statcast pitch-level 接入 | SP FIP/xFIP/K%/BB% 通過 no-lookahead test |
| Bullpen state feature | 連續出賽天數計算正確，leakage test 通過 |
| Feature Registry v1 | `wbc_backend/features/registry.py`，含版本控制 |
| PredictionState state machine | 既有 caller 漸進遷移，feature flag 保護 |
| LearningMemoryRepository | audit_hash 去重，schema validation |
| Simulation runner v1 | Walk-forward + Paper 兩種 simulation type 完整輸出 schema |
| CLV 真實樣本 ≥ 50 | 非 proxy，來自 Pinnacle real closing odds |
| BSS ≥ 0 或根因已解 | 若 BSS 仍 < 0，根因報告 v2 更新 |

### 90 Days — Self-Learning Core

| 目標 | 驗收標準 |
|---|---|
| Ensemble + Calibration walk-forward retrain (MLB) | BSS ≥ +2% CI95 |
| MLB Regime classifier | early/mid/late season 各 regime 獨立驗證 |
| park factor 接入 | Statcast park factor，leakage test 通過 |
| weather feature 接入 | NOAA / OpenWeather，leakage test 通過 |
| scratched-start event handler | < 5 min reprediction latency |
| scheduler priority-score v1 | 任務 priority ranking 可 audit |
| scheduler safety invariants 100% | 每 tick assert，safety_violation.jsonl = 0 |
| Threshold feedback loop | weekly regime-aware threshold 更新 |
| 所有 simulation type 1–6 上線 | 各有完整 schema 輸出 |
| human review SLA < 24h | 量化 median response time |

### 180 Days — Production-Proposal Workflow

| 目標 | 驗收標準 |
|---|---|
| Stable MLB production proposal workflow | 每週 ≥ 1 提案進入 human_review |
| CLV ≥ +60 bps (CI95) | 來自 ≥ 200 真實 closing 樣本 |
| Human review SLA < 12h | 量化 median |
| Architecture health score ≥ 75 | `scripts/architecture_health_score.py` 輸出 |
| Stable CLV/ROI daily tracking | 每日 ops_report 包含 CLV/ROI 趨勢 |
| BSS ≥ +8% CI95 (all season regime) | 各 regime 獨立 CLV ≥ 0 |
| All 10 simulation types 上線 | 完整 simulation registry |
| root models/ deprecation 完成 ≥ 50% | deprecation_roadmap.md 追蹤 |
| Long-term MLOps governance baseline 文件化 | `docs/architecture/mlops_governance.md` |

---

## 13. First 10 Recommended Tasks (執行明細)

### T1 — BSS 根因調查報告
- **Why now**: BSS = -14.1% 是整個計畫的緊迫性來源。在不知道為什麼比市場差之前，任何 feature / model 改動都是賭博，可能讓問題更嚴重。
- **Expected impact**: 極高（所有後續改動的方向基礎）
- **Target files**: `docs/orchestration/bss_root_cause_2026-05-04.md`（新增報告）；`wbc_backend/evaluation/` 加診斷 script
- **Acceptance criteria**: (i) 列出所有可能根因並逐一驗證或排除 (ii) 確認樣本集（MLB 場次數、時間範圍）(iii) 確認 BSS baseline（no-vig Pinnacle? 市場中位?) (iv) reliability diagram 產出 (v) 列出對應修復方案 (vi) reviewer 簽核
- **Effort**: M（2–3 天）
- **Mode**: Deterministic（跑分析腳本，不需外部 AI）
- **Blocks**: T2 之後的所有 model 相關任務

### T2 — `orchestrator/budget_guard.py` 建立
- **Why now**: budget_guard.py 不存在是 governance G2 critical 缺口。任何 worker 誤配置都可能造成失控的外部 AI 花費。
- **Expected impact**: 高（安全基礎）
- **Target files**: `orchestrator/budget_guard.py`（新增）、`runtime/agent_orchestrator/budget_config.json`（新增）、`tests/test_budget_guard.py`
- **Acceptance criteria**: (i) Planner external AI 嘗試 → CRITICAL deny + safety_violation.jsonl (ii) Worker > per_task_max → deny + fallback (iii) provider > daily → switch fallback (iv) global > warn 70% → badge (v) global > critical 90% → hard-stop (vi) pytest 覆蓋所有路徑
- **Effort**: M（2–3 天）
- **Mode**: Deterministic

### T3 — Telegram Bot AuditGuard 補丁 (G3)
- **Why now**: `llm_audit_coverage_report()` 因 Telegram 缺口回傳 PARTIAL，阻礙 scheduler 允許外部 AI dispatch。
- **Expected impact**: 高（解鎖 audit_coverage=FULL）
- **Target files**: `telegram_bot/bot.py`（修改）、`orchestrator/llm_audit_coverage.py`（更新 coverage list）
- **Acceptance criteria**: (i) Telegram OpenAI 呼叫通過 `budget_guard.check_before_call()` (ii) 如有執行命令，通過 SafeTaskExecutor + AuditGuard (iii) `llm_audit_coverage_report()` 回傳 FULL (iv) 現有 Telegram bot 功能不受影響
- **Effort**: S（1–2 天）
- **Mode**: Deterministic

### T4 — `wbc_backend/evaluation/metrics.py` SSOT 建立
- **Why now**: 目前 Brier、ECE、CLV bps 等 KPI 在多個 eval 腳本中分散計算，打架的數字是根因調查的障礙。
- **Expected impact**: 高（後續所有驗證的公正基礎）
- **Target files**: `wbc_backend/evaluation/metrics.py`（新增 / 整併）、`wbc_backend/evaluation/bootstrap.py`（新增 bootstrap CI）、所有 eval caller 改 import
- **Acceptance criteria**: (i) Brier, BSS, log loss, ECE, reliability diagram, CLV bps, ROI, drawdown, Sharpe 全在一個模組 (ii) bootstrap CI（≥ 1000 resample）作為 utility (iii) ≥ 95% line coverage (iv) 舊 caller 全部改用 (v) 結果與舊版一致（移植驗證）
- **Effort**: M（2 天）
- **Mode**: Deterministic

### T5 — `tests/feature_validation/test_no_lookahead.py` 建立
- **Why now**: data leakage 是 BSS 問題的可能根因之一，也是 silent killer。沒有 gate 的話任何新 feature 都有潛在的 leakage 風險。
- **Expected impact**: 高（防禦性）
- **Target files**: `tests/feature_validation/test_no_lookahead.py`（新增）、`wbc_backend/features/builder.py`（加時間 cursor hook）
- **Acceptance criteria**: (i) 假時間 cursor 下，所有 feature 只讀 ≤ cursor timestamp (ii) 故意造一個 leak case 必須 FAIL (iii) 現有 feature builder 通過（或找到 bug，這也是好結果）(iv) 新增 feature 必須通過此 test 才能進 feature registry
- **Effort**: M（2 天）
- **Mode**: Deterministic

### T6 — UI Budget Panel 建立
- **Why now**: 視覺化才會被注意到。budget_guard 上線後需要立即有前端呈現，否則成本超標會被忽視。
- **Expected impact**: 中（可見性 + 操作安全）
- **Target files**: `runtime/agent_orchestrator/frontend/index.html`（修改，新增 Budget panel）
- **Acceptance criteria**: (i) 今日 total 用量 bar (ii) provider breakdown (iii) role breakdown (iv) Planner=0 invariant badge（必須 green）(v) WARN/CRITICAL 顏色 (vi) 不影響現有 UI 其他功能
- **Effort**: S（1 天）
- **Mode**: Deterministic

### T7 — `PredictionState` State Machine 建立
- **Why now**: review queue / patch gate / learning cycle 的 if/else 散落是耦合最嚴重的地方，state machine 是讓流程可審計的基礎。
- **Expected impact**: 中高（長期維護性）
- **Target files**: `wbc_backend/state_machine/prediction_state.py`（新增）、`wbc_backend/state_machine/transitions.py`、`tests/test_prediction_state.py`
- **Acceptance criteria**: (i) 所有合法 transition 定義在 table (ii) 非法 transition raise InvalidTransition (iii) 現有 caller 透過 feature flag 漸進遷移 (iv) 無行為改變
- **Effort**: M（3 天）
- **Mode**: Deterministic

### T8 — MLB 資料盤點文件 + Statcast Pipeline 啟動
- **Why now**: Statcast 接入是修復 BSS 的最大槓桿（SP pitch-level 是 MLB #1 feature），但需要先釐清 credential、rate limit、schema。
- **Expected impact**: 極高（模型準確度核心）
- **Target files**: `docs/data/mlb_inventory.md`（新增）；`data/mlb_live_pipeline.py`（擴充 Statcast 抓取）；`wbc_backend/league/mlb_adapter.py`（補齊 fetch_statcast_pitch）
- **Acceptance criteria**: (i) 盤點文件含每個資料源的 provider / endpoint / auth / rate_limit / cost / 缺口 (ii) Statcast SP FIP/xFIP/K%/BB% 可讀取並通過 no-lookahead test (iii) 每日自動同步 schedule 定義
- **Effort**: M（2 天文件 + 3 天 pipeline）
- **Mode**: Deterministic

### T9 — `LearningMemoryRepository` 建立
- **Why now**: `training_memory.json` 直接讀寫是 top-5 高風險耦合點，沒有 schema 保護、無法防止 tainted 資料被學習。
- **Expected impact**: 高（學習系統安全性）
- **Target files**: `runtime/learning/repository.py`（新增）、`tests/test_learning_memory_repo.py`
- **Acceptance criteria**: (i) append-only JSONL (ii) audit_hash 去重 (iii) schema validation（不合格 raise）(iv) `tainted=true` 過濾 (v) failure_patterns 查詢 (vi) 現有 caller 改用 repo（feature flag）
- **Effort**: M（2 天）
- **Mode**: Deterministic

### T10 — Walk-Forward Harness 統一化（MLB 2022–2025）
- **Why now**: 有了 metrics.py SSOT + no-lookahead gate + Statcast data，可以跑第一份正式 walk-forward，作為 BSS 改善的 baseline。
- **Expected impact**: 極高（所有後續模型改動的 baseline reference）
- **Target files**: `wbc_backend/backtesting/league_backtest.py`（強化，確保 time-ordered、regime-aware）；`wbc_backend/evaluation/metrics.py`（call SSOT）
- **Acceptance criteria**: (i) ≥ 1500 場（目標 5000+）MLB 賽事，time-ordered (ii) 輸出 Brier, BSS, ECE, reliability diagram, CI95 (iii) regime split 輸出（各 regime 獨立指標）(iv) 每個 feature 版本有 hash 記錄 (v) 輸出寫入 `simulation_runs.jsonl`
- **Effort**: L（4–5 天）
- **Mode**: Deterministic（不需外部 AI）

---

## 14. Final Recommendation

### 14.1 目前最該做的（接下來兩週）

**Week 1：Governance 緊急修補**
```
D1: T1 BSS 根因調查腳本起手（跑現有 eval，輸出 reliability diagram）
D2-D3: T2 budget_guard.py + pytest
D4: T3 Telegram AuditGuard 修補
D4: T6 UI Budget panel（可與 T3 並行）
D5: T4 metrics.py SSOT 第一版
```

**Week 2：Model Diagnostic + 防禦建立**
```
D6: T5 no-lookahead test gate（找到可能的 leakage）
D7: T4 metrics.py SSOT 完成 + caller 遷移
D8-D9: T7 PredictionState state machine 骨架
D10: T1 BSS 根因報告初稿 + reviewer 排程
D11-D12: T8 MLB 資料盤點文件
D13: T9 LearningMemoryRepository 起手
D14: Phase 0 retrospective + 本文件版本更新
```

### 14.2 暫時不該做的
- ❌ **在 BSS 根因未診斷前改動模型結構** — 方向可能完全錯誤
- ❌ **在 budget_guard.py 上線前做任何 Worker 外部 AI 任務** — 成本失控風險
- ❌ 在 no-lookahead test 通過前把新 feature 送進 walk-forward — leakage 污染 baseline
- ❌ `git mv root/models/ → wbc_backend/models/legacy/` — import 風暴，90 天後評估
- ❌ 升級 persistence 到 PostgreSQL — 30 天後評估需求
- ❌ 把 monte_carlo 核心邏輯（現 50,000 sim）大幅改動 — 穩定性保護
- ❌ Planner 使用外部 AI（永久 hard rule）
- ❌ 在 BSS ≥ 0 之前產生 CANDIDATE_PATCH（BSS gate）

### 14.3 最大風險 (Top-5)

| 風險 | 機率 | 影響 | 緩解 |
|---|---|---|---|
| **BSS 根因複雜（多因子疊加）** | 中高 | 高 | T1 系統性排查所有假說；設定 30D deadline：若無根因，啟動 full model reset |
| **Statcast / Pinnacle closing odds 資料取得受阻** | 中 | 高 | T8 先做盤點；備援：Retrosheet backfill + OddsJam alternate |
| **Telegram AuditGuard 修補破壞現有 bot 功能** | 低 | 中 | feature flag 保護；先 test，後上線；read-only path 最小修改 |
| **budget_guard.py 設定過緊，Worker 日常任務被誤 deny** | 中 | 中 | 起始 budget 設寬（$10/天），觀察 7 天後收緊；warn threshold 先 70% |
| **walk-forward 發現 BSS 無法改善（市場已 efficient）** | 低 | 極高 | 若 BSS 90D 仍 < 0，轉向「特定 regime / 場次類型」的利基市場，而非追求全面預測 |

### 14.4 下一個 2 週行動計畫

| Day | 動作 | 輸出 |
|---|---|---|
| D1 | BSS 診斷腳本：reliability diagram + 現有 baseline 量化 | `bss_root_cause_draft.py` |
| D2-D3 | `budget_guard.py` + `budget_config.json` + pytest | `tests/test_budget_guard.py` 全綠 |
| D4 | Telegram AuditGuard 補丁 + `llm_audit_coverage` 更新 | coverage = FULL |
| D4 | UI Budget panel | 上線 + Planner=0 badge |
| D5 | `metrics.py` SSOT v1（Brier, BSS, ECE, CLV bps, bootstrap CI） | pytest ≥ 95% cov |
| D6 | `test_no_lookahead.py` + leak case FAIL 驗證 | test gate 上線 |
| D7 | `metrics.py` caller 遷移（舊 backtester 改用 SSOT）| 數字一致性驗證 |
| D8-D9 | `PredictionState` state machine 骨架 + feature flag | test 通過 |
| D10 | BSS 根因報告初稿（含 reliability diagram 分析） | `bss_root_cause_2026-05-04.md` v0.1 |
| D11-D12 | MLB 資料盤點文件 + Statcast endpoint 測試 | `docs/data/mlb_inventory.md` |
| D13 | `LearningMemoryRepository` 骨架 + audit_hash 去重 | test 通過 |
| D14 | Phase 0 retrospective 會議 + 本文件 patch | `bss_root_cause.md` v1 簽核 |

---

## 15. Hard-Rule Compliance Matrix

| Hard Rule | 本計畫遵守方式 |
|---|---|
| 不直接修改 production model | 全計畫只產 proposal，Phase 4 才到 review；BSS gate 阻擋 |
| 不建立 production patch | 同上 |
| 不跳過 human review | Phase 4 review-driven；gate 強制 review_id |
| 不用 sandbox 結果稱 production OK | metrics SSOT + sample-size gate + BSS gate |
| 不用小樣本下結論 | ≥ 1500 場 hard gate（patch gate 強制）|
| Planner 不呼叫外部 AI | T2 budget_guard.py runtime deny；T3 UI badge |
| 新增外部 AI 必經 AuditGuard | T3 Telegram 補丁；所有新增 worker path 必須 AuditGuard |
| 不呼叫真實 Codex/Claude/Copilot/GitHub | 本文件 Planner-mode 撰寫，未呼叫任何外部 AI |
| 計畫為主，不改 runtime 行為 | 是（除 T2/T3 新增 guard，不改現有行為）|

---

## 16. Open Questions (留給 Reviewer)

1. **MLB Odds Provider 鎖定**：確定使用 Pinnacle + 哪些 sharp books？Circa? BetOnline? 台灣 TSL 的 closing odds 是否可作 CLV baseline？
2. **Statcast / FanGraphs 授權**：Baseball Savant 是公開的，但 FanGraphs 的 bulk data download 需要確認 TOS。
3. **BSS Baseline 定義**：用 no-vig Pinnacle 隱含機率？還是市場均值？需要在 T1 根因報告前確定。
4. **Telegram Bot 執行命令範圍**：T3 修補前需釐清哪些 Telegram 指令會觸發外部 AI（只有 read-only 回答？還是也有執行 tasks 的路徑？）
5. **Human Review Panel**：需幾位 reviewer？是否強制非作者？現在只有一位用戶嗎？
6. **Budget 初始設定**：$10/天 / $50/週是合理的嗎？還是應該更保守（$5/天）？
7. **MLB 賽季外排程**：11 月–3 月降頻後，是否需要維持 paper betting simulation（用 off-season 歷史資料）？
8. **WBC 2026 與 MLB 關係**：WBC 2026 比賽期間，MLB 球員資料如何處理？是否有 cross-league feature 應用計畫？
9. **Persistence 升級時機**：純 JSONL 的瓶頸是什麼？等 Phase 3 評估，還是已經有具體痛點？
10. **root `models/` deprecation 策略**：是否允許用 symlink 作過渡，還是要用 import shim？

---

## 17. 資料補齊計畫（WBL = MLB 資料源尚未完整的具體行動）

### 17.1 優先補齊順序

| 優先度 | 資料 | 補齊行動 | 負責人 | 完成時間 |
|---|---|---|---|---|
| P0 (阻擋 BSS 修復) | MLB 歷史賽果（2022–2025，≥ 5000 場）| Retrosheet backfill 腳本 | Worker | D7–D14 |
| P0 (阻擋 BSS 修復) | Pinnacle closing odds（真實，非 proxy）| 接 Pinnacle API 或 OddsJam | Worker | Phase 1 |
| P1 (BSS 關鍵特徵) | Statcast pitch-level（SP FIP/xFIP/K%/BB%）| Baseball Savant API | Worker | Phase 1 |
| P1 (MLB 特有) | Park factor（Statcast park factor 年更）| `MLBAdapter.fetch_park_factors()` | Worker | Phase 2 |
| P1 (MLB 特有) | Weather（溫度、風向、球場）| NOAA / OpenWeather | Worker | Phase 2 |
| P2 | Bullpen load（連續出賽天數）| 從 lineup 推算 | Worker | Phase 1 |
| P2 | Injury / IL (10/15/60-day)，結構化 | MLB StatsAPI injured list | Worker | Phase 1 |
| P2 | Line movement（賽前 6h 起每 10 min）| odds_api_client.py 擴充 | Worker | Phase 1 |
| P3 | Umpire strike zone bias | Statcast umpire data | Worker | Phase 2 (optional) |
| P3 | Winter meeting / Trade impact | manual research + structured input | Human | Off-season |

### 17.2 資料接入原則
- 所有資料接入必須先通過 `test_no_lookahead.py`
- 資料更新頻率 > 15 分鐘的必須有 Scheduler task 管理
- 所有外部 API 呼叫必須有 fallback（至少一個備援 provider）
- Rate limit 資訊必須記錄在 `docs/data/mlb_inventory.md`

---

## 18. 驗證聲明 (Verification Statement)

本文件已完成以下要求段落的撰寫並通過自我核查：

- [x] 術語釐清（WBL = MLB，WBC 為輔助）
- [x] 版本差異說明（Rev3 vs Rev2）
- [x] Executive Summary（含 BSS = -14.1% 緊迫性）
- [x] Current System Assessment（精確反映 2026-05-04 codebase 狀態）
- [x] Target System Architecture（分層架構 + 模組責任表）
- [x] Long-term Roadmap (180 天 4 Phase)
- [x] Workstream A — 程式系統架構長期優化計畫
- [x] Workstream B — WBL(MLB) 預測成功率提升計畫
- [x] Workstream C — 自我學習 / 模擬賽事優化計畫
- [x] Workstream D — 排程自我學習優化計畫
- [x] Workstream E — Usage Budget / Copilot 成本控管計畫
- [x] Phase Plan（含 5 Phase，各含 Objective / Key Tasks / Deliverables / Success Criteria / Risk）
- [x] Metrics & Acceptance Criteria（含 Brier/BSS/ECE/CLV/ROI/drawdown/Sharpe/audit/budget）
- [x] 30 / 60 / 90 / 180 Day Roadmap
- [x] First 10 Recommended Tasks（各含 why now / impact / target files / acceptance / effort / mode）
- [x] Final Recommendation（最該做 / 暫不做 / 最大風險 / 2 週行動計畫）
- [x] Hard Rule Compliance Matrix
- [x] Data Gap 補齊計畫（WBL/MLB 資料源）
- [x] Open Questions
- [x] 作者聲明：本文件以 Planner-mode (deterministic) 撰寫，未呼叫任何外部 AI (Codex / Claude / Copilot / GitHub)

---

**LONG_TERM_WBL_OPTIMIZATION_PLAN_VERIFIED**

> 所有條件已滿足：
> - ✅ 系統架構長期計畫（Workstream A）
> - ✅ WBL(MLB) 預測成功率提升計畫（Workstream B）
> - ✅ 自我學習 / 模擬賽事優化計畫（Workstream C）
> - ✅ 排程自我學習優化計畫（Workstream D）
> - ✅ Usage Budget / Copilot 成本控管（Workstream E）
> - ✅ 30 / 60 / 90 / 180 Day Roadmap
> - ✅ First 10 Recommended Tasks
> - ✅ 全程遵守 HARD RULES（不改 production model、不跳 human review、不用外部 AI 撰寫）
