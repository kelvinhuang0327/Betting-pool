# 🧬 Betting-pool: 量化研究平台核心規範 (Quant Platform Core)

本規範定義了策略從發想到部署的完整生命週期與統計校驗標準。

## 1. 策略生命週期 (Strategy Lifecycle)
所有策略必須遵循以下路徑，並產出對應 Artifacts：
**構思 → 模擬 → 回測 → 校驗 → 演化 → 集成 → 再評估**

| 階段 | 必要 Artifact |
| :--- | :--- |
| Idea | `strategy.yaml` |
| Simulation | `sim_result.json` |
| Backtest | `backtest_report.md` |
| Validation | `stat_test.txt` |
| Rejected | `rejected/{strategy_name}.json` |

## 2. 統計驗證標準 (Validation Standard)
- **數據量**: 必須覆蓋至少 **1500 場歷史賽事**。
- **三窗口驗證**: 必須同時滿足 150 場、500 場、1500 場的穩定獲利。
- **核心指標**:
  - ROI > Baseline
  - Sharpe Ratio > 0
  - p-value < 0.05
- **必測項目**: 排列檢定 (Permutation Test)、前進式樣本外測試 (Walk-forward testing)。

## 3. 策略評分公式 (Scoring)
```
Score = (ROI × Stability × Significance) ÷ Complexity
```
- **Stability**: 不同驗證窗口的一致性。
- **Significance**: -log10(p-value)。
- **Complexity**: 特徵數量 × 參數數量。

## 4. 數據治理與特徵工程
- **數據隔離**: 執行 `predict()` 時僅能接收預測時刻前的已知數據。
- **特徵存儲**: 複用特徵應存放在 `features/` (如 `frequency_features.py`)。
- **防過擬合**: 必須通過 K-fold 驗證與 Monte Carlo 模擬。

## 5. 失敗追蹤 (Fail but Record)
拒絕的策略嚴禁刪除，必須移動至 `rejected/` 並記錄：
- 失敗原因 (Failure Reason)
- 統計結果 (Statistical Results)
- 是否具備再測試條件 (Retest Conditions)
