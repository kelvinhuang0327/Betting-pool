# P28 Model Quality Baseline Audit
**Date**: 2026-05-20  
**Phase**: P28_MLB_MODEL_QUALITY_REPAIR  
**paper_only**: true | **diagnostic_only**: true

---

## 現有 Baseline 讀取

| 指標 | 數值 | 來源 |
|------|------|------|
| Walkforward Brier | **0.2487** | walkforward_summary.json |
| Walkforward log loss | 0.6910 | walkforward_summary.json |
| ML hit rate | **46.25%** | walkforward_summary.json |
| ECE | 0.0347 | walkforward_summary.json |
| Sample size | 2,188 games | walkforward_summary.json |
| Random baseline Brier | 0.2500 | 理論值（always predict 0.5） |
| Platt calibration Brier | 0.2484 | calibration_compare.json |
| Isotonic calibration Brier | 0.2503 | calibration_compare.json |

---

## 預測機率分布（N=1,493 games）

| 指標 | 數值 |
|------|------|
| Mean | 0.5642（輕微 home bias） |
| Std | 0.0955 |
| 0.45–0.55 concentration | 32.0% |
| > 0.60 count | 562（37.6%） |
| Min / Max | 0.1458 / 0.9163 |

---

## 校準審計

| 指標 | 狀態 |
|------|------|
| ECE | 0.0347（< 0.05 閾值，可接受） |
| Home bias | Mean=0.5642，MLB 實際主場勝率 ~54%（偏差 2.4pp） |
| Overconfidence | **否**（ECE 可接受） |
| Platt ECE | 0.0352（比 baseline 更差） |
| Isotonic ECE | 0.0440（更差） |
| AUC | **MISSING（artifacts 無此欄位）** |

---

## 辨別力審計

| 指標 | 狀態 |
|------|------|
| Hit rate | **46.25%**（低於 50%，選擇的 bets 輸給硬幣） |
| High-confidence reliability | 未知（AUC MISSING） |
| Market beat rate | 未知（CLV diagnostic = N/A） |

**ML hit rate 46.25% < 50%** 是嚴重警示，代表模型在選擇投注時更常錯。但這可能是因為 optimizer 在 edge > 0 時才投注，而被選中的 bets 是模型最高 edge（但市場已較準確）的情況。

---

## 當前模型特徵集（7個）

| # | 特徵 | 說明 |
|---|------|------|
| F1 | home_ml_p | 主場賠率隱含機率 |
| F2 | away_ml_p | 客場賠率隱含機率 |
| F3 | home_ml_p − away_ml_p | 機率差值 |
| F4 | ou | Over/Under 線 |
| F5 | starter_home_known | 主場先發已知（binary） |
| F6 | starter_away_known | 客場先發已知（binary） |
| F7 | home_bias | 常數 1.0 |

**根本問題**：7 個特徵幾乎等同於「重新輸出市場賠率」。模型學習的是近乎恆等映射（identity map）。

---

## Baseline 結論

**分類：`MODEL_RANDOM_LIKE` + `MODEL_DATA_LIMITED`**

1. Brier=0.2487 vs random=0.25：僅比隨機好 0.0013
2. 現有 7 個特徵中，6 個都是市場賠率衍生物
3. 無真實 alpha：沒有先發投手品質、打擊狀態、牛棚疲勞等訊號
4. Platt/Isotonic 校準均未改善（Platt Δ=-0.0003，Isotonic 更差）
5. 311 個 alpha_signals.py 特徵未被 walkforward 使用

---

## 可用但未使用的 CSV 欄位

| 欄位 | 說明 | 可加工特徵 |
|------|------|-----------|
| RL Home / RL Away | 讓分賠率 | 隱含機率（另一維度） |
| Over / Under | 大小盤賠率 | 大盤隱含機率 |
| Home / Away | 球隊名稱 | 滾動勝率（在訓練視窗內） |
| Date | 日期 | 賽季階段、星期幾 |

**沒有 pitcher ERA/FIP、batting wOBA 等真實 stat 特徵。**
