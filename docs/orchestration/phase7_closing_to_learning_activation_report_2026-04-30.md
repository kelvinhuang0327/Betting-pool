# Phase 7：Closing-to-Learning 啟動報告
**日期**: 2026-04-30  
**狀態**: ✅ VERIFIED — `PHASE_7_CLOSING_TO_LEARNING_ACTIVATION_VERIFIED`  
**測試**: 30/30 通過（Phase 7）；28/28 通過（Phase 6 迴歸）

---

## 1. 目標

Phase 7 的核心目標：**啟動從「市場收盤賠率」到「策略強化學習」的完整回饋迴路**。

- PENDING_CLOSING → COMPUTED 升級（有外部收盤資料時）
- 計算 CLV（Closing Line Value），記錄進訓練記憶
- Strategy tick 讀取 COMPUTED 紀錄，調整策略信心值

---

## 2. 架構變更

### 2.1 Scheduler（5 軌道）

| 軌道 | 名稱 | 間隔 |
|------|------|------|
| A | PlannerWorker | 動態 |
| B | PlannerWorker | 動態 |
| C | SimulationEngine | 30 min |
| D | StrategyTick | 5 min |
| **E** | **ClosingOddsMonitor** | **15 min** |

新增 `OrchestratorClosingMonitor` daemon thread，每 30 秒檢查一次是否到排程時間。  
可透過 DB 設定 `phase7_closing_monitor_enabled`（預設 "1"）與 `phase7_closing_monitor_interval_seconds` 動態控制。

### 2.2 closing_odds_monitor.py

**`_validate_closing_odds()` — 5 道驗證**：

| 驗證 | 規則 |
|------|------|
| 1 | `closing_ts > prediction_time_utc`（嚴格在預測之後） |
| 2 | `age_days ≤ 30`（收盤賠率不超過 30 天舊） |
| 3 | 研究情境允許未來日期（data pipeline 處理歷史賽事時放行） |
| 4 | `closing_ml ∈ [-3000, +3000]`（棒球賠率有效範圍） |
| 5 | **Same-snapshot guard**: `diff_seconds ≥ 60`（至少 60 秒差距，防資料滲透） |

升級後的 COMPUTED 紀錄新增欄位：
- `closing_odds_time_utc`（收盤時間 alias）
- `computed_at_utc`（計算時間 alias）
- `clv_value`（到 6 位小數）
- `closing_implied_probability`

狀態持久化至：`runtime/agent_orchestrator/closing_monitor_state.json`

### 2.3 strategy_tick.py — CLV 強化信號

在 Phase 6U 閘門通過後，若有 `eligible_for_reinforcement`:

```
avg_clv = mean(clv_value for all COMPUTED records)

if avg_clv > +0.010 → confidence_delta = +0.02  (positive)
elif avg_clv < -0.010 → confidence_delta = -0.02  (negative)  
else → confidence_delta = 0.0  (flat)

exposure_delta = 0.0  (CLV 不直接影響倉位大小)
```

強化訊號透過 `state["phase7_clv_reinforce"]` 持久化至 `strategy_state.json`。

### 2.4 training_memory.py — CLV 結果記錄

新增函數：
- `record_clv_outcome(prediction_id, clv_value, clv_direction, source, ...)`: 依 `prediction_id` 去重（最新覆蓋），最多保留 200 筆；**絕不觸碰** `consecutive_successes / consecutive_failures`
- `get_clv_outcomes(n=50)`: 取最後 n 筆
- `get_clv_outcome_summary()`: 回傳 `{total, positive_count, negative_count, flat_count, avg_clv, positive_rate}`

CLV 方向判定：
- `"positive"` → `clv_value > +0.005`
- `"negative"` → `clv_value < -0.005`
- `"flat"` → 其餘

### 2.5 ops_decision_card.py — Phase 7 可觀測性

新增 `compute_phase7_status()` 與渲染區塊：

```
📡 PHASE 7 CLOSING MONITOR
  last_run_at: ...
  computed_clv: N  pending_clv: M
  stale_closing_rejected: K
  learning_unlocked_count: L
  ► CLV_COMPUTED_READY_FOR_LEARNING / WAITING_FOR_MARKET_SETTLEMENT / BLOCKED_NO_VALID_CLOSING
```

---

## 3. 資料隔離保證

| 硬規則 | 實作 |
|--------|------|
| 不偽造收盤賠率 | Monitor 只讀外部資料，無 mock fallback |
| 不從預測快照計算 CLV | Same-snapshot guard：60 秒差距強制 |
| 不從 PENDING_CLOSING 強化策略 | `_load_computed_clv_records()` 僅讀 COMPUTED 行 |
| 不覆寫生產報告 | 輸出至獨立 out_path，原始檔案唯讀 |
| 不修改即時下注執行 | CLV 強化只改 confidence_delta，不影響 exposure |

---

## 4. 測試覆蓋（Phase 7）

| 情境 | 測試類 | 通過 |
|------|--------|------|
| Monitor 跳過已 COMPUTED 紀錄 | TestMonitorSkipsComputed | 3/3 |
| 有效外部收盤升級 | TestValidExternalClosingUpgrade | 4/4 |
| 過期收盤保持 PENDING | TestStaleClosingRemainsUnchanged | 2/2 |
| Same-snapshot 拒絕 | TestSameSnapshotRejection | 2/2 |
| 策略只強化 COMPUTED | TestStrategyReinforcesOnlyComputed | 6/6 |
| 訓練記憶 CLV 結果 | TestTrainingMemoryCLVOutcome | 4/4 |
| Decision Card Phase 7 | TestDecisionCardPhase7 | 3/3 |
| Monitor 冪等性 | TestMonitorIdempotency | 2/2 |
| 外部 vs TSL 優先權 | TestExternalClosingPriority | 3/3 |
| **成功標記** | test_phase7_closing_to_learning_activation_verified | 1/1 |
| **合計** | | **30/30** |

Phase 6 迴歸測試: **28/28** 通過（無退化）。

---

## 5. 現有資料狀態

`data/wbc_backend/reports/clv_validation_records_6u_2026-04-30.jsonl`：14 筆全為 PENDING_CLOSING。  
**實際升級為 COMPUTED 需要真實收盤賠率資料（外部 API 或 TSL 爬取）**，本期 Phase 7 完成管線基礎架構，收盤資料接入為後續 Phase 8 任務。

---

## 6. 已知限制與後續工作

1. **收盤賠率資料來源**：目前依賴 `tsl_odds_history.jsonl` 及外部 API；需定期爬取確保收盤時間點資料可用。
2. **研究情境未來日期**：驗證器在研究 / backtest 情境放行未來日期的收盤時間（以 debug log 標記），生產環境可透過設定收緊。
3. **CLV 強化門檻**：±0.010 為保守初值，待累積足夠樣本後可透過 Phase 8 Optuna 調整。

---

## 7. SUCCESS CRITERIA

```
PHASE_7_CLOSING_TO_LEARNING_ACTIVATION_VERIFIED
```
