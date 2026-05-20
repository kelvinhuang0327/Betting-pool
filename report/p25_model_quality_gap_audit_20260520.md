# P25 模型品質差距稽核報告

**Phase**: P25 — Model Quality Gap Audit  
**Date**: 2026-05-20  
**Verdict**: `MODEL_QUALITY_INSUFFICIENT`  
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 執行摘要

從 MLB walkforward 驗證（N=2188 場）、WBC gate validation（N=40 場）、校準比較三個維度評估模型品質。結論：**MLB 模型辨別能力近乎隨機，WBC 樣本過小無法可靠驗證，兩者均不足以支撐正 CLV 的持續產生。**

---

## 一、MLB Walkforward 驗證

**資料來源**：`data/wbc_backend/walkforward_summary.json`（N=2188 場）

| 指標 | 數值 | 基準 | 評估 |
|---|---|---|---|
| Brier Score | **0.2487** | 隨機 = 0.25 | ⚠️ 幾乎與隨機相同（delta = -0.0013）|
| Log Loss | 0.6910 | 隨機 ≈ 0.693 | ⚠️ 近乎隨機 |
| ML Hit Rate | **46.25%** | 盈虧平衡 = 50% | 🔴 低於 50%，比擲硬幣更差 |
| ML ROI | **-1.11%** | ≥ 0 才有意義 | 🔴 負收益 |
| OU ROI | **-12.18%** | ≥ 0 | 🔴 大小分強烈負值 |

**關鍵問題**：在 2188 場中，ML hit rate = 46.25% 意味著模型預測方向錯誤的頻率高於正確。這不是小樣本波動 — 在 N=1626 次 ML 賭注中，統計顯著性明確。

---

## 二、WBC Gate Validation

**資料來源**：`data/wbc_backend/reports/gate_validation_evidence.json`（N=40 場）

| 指標 | 數值 |
|---|---|
| Ensemble Brier | **0.1415** |
| 可評估場次 | **40** |

**分析**：
- 0.1415 表面上看起來比 MLB（0.2487）好很多，也明顯優於隨機基準（0.25）
- **但 N=40 太小**：在 N=40 下，Brier 的 95% 信賴區間約為 ±0.04，即 [0.10, 0.18]
- 40 場的樣本選擇性偏差（Selection Bias）：哪些場次被認定為「可評估」可能本身就代表市場穩定的比賽，導致 Brier 偏低
- **結論**：WBC ensemble Brier=0.1415 是積極訊號，但不足以作為生產驗證依據。需要 ≥1500 場次的回測（依照 CLAUDE.md 規範）

---

## 三、校準比較

**資料來源**：`data/wbc_backend/calibration_compare.json`

| 方法 | Brier | Log Loss | ECE | ML ROI | ML Hit Rate |
|---|---|---|---|---|---|
| Platt | 0.24840 | 0.69038 | **3.52%** | -0.85% | 46.44% |
| Isotonic | 0.25035 | 0.73093 | 4.40% | +1.80% | 48.03% |

**分析**：
- ECE（Expected Calibration Error）在 3.52%-4.40% 之間 — **校準品質本身是可接受的**（業界通常以 5% 為門檻）
- 問題不在校準（calibration），而在**辨別能力（discrimination）**
- Isotonic ROI = +1.80% 看似正面，但這是校準訓練集的 in-sample 結果，底層 Brier=0.2504 仍是近乎隨機
- 兩種校準方法的 ML hit rate 均 < 50%，不存在可靠的出樣 edge

---

## 四、模型輸出契約合規

**資料來源**：`data/derived/model_output_contract_validation_summary_2026-04-29.json`

| 門控 | Pass Rate |
|---|---|
| M1 | **0%** |
| M5 | **0%** |
| M6 | **0%** |
| M13 | **0%** |
| M10 | 36.8% |
| M2/M3/M4/M7-M12 | 100% |

**缺失的 7 個時間戳欄位**：
1. `feature_cutoff_source`
2. `model_output_written_at_utc`
3. `prediction_run_completed_at_utc`
4. `data_freshness_label`
5. `feature_lookback_days`
6. `model_version_tag`
7. `training_end_date`

**影響**：
- 缺少 `feature_cutoff_source` → 無法驗證特徵截止時間是否早於預測目標，Data Leakage 審計不可能完成
- 缺少 `training_end_date` → 無法確認 Walk-forward 分界正確
- 缺少 `model_version_tag` → 無法追蹤哪個模型版本產生哪組預測結果

---

## 五、差距彙總

| 差距 | 嚴重度 | 需要行動 |
|---|---|---|
| Brier ≈ 隨機（0.2487 vs 0.25） | 🔴 CRITICAL | 重新設計特徵工程 |
| ML hit rate < 50%（46.25%） | 🔴 CRITICAL | 回測重新驗證（≥1500 場）|
| WBC 樣本不足（N=40） | 🟠 HIGH | 累積 WBC 歷史數據（WBC 2026+ 賽季）|
| 7 個時間戳欄位缺失 | 🟠 HIGH | 補齊 model output schema |
| OU ROI = -12.2% | 🟡 MEDIUM | 大小分特徵需重新評估 |
| OE 市場無資訊含量 | 🟡 LOW | 排除 OE 出 CLV 彙總統計 |

---

## 六、研究方向（不得作為生產提案）

1. **特徵洩漏檢查**：hit_rate < 50% 可能意味著存在反向特徵（標籤洩漏或特徵方向錯誤），需逐一稽核特徵來源
2. **WBC 專屬模型**：MLB 與 WBC 賽制/球員/主場效應差異大，需獨立訓練，目前 WBC 樣本量不足，需等待更多賽季數據
3. **MLB 模型重訓**：若 Brier 持續 ≈ 0.25，考慮更強特徵集（投手疲勞、對戰 matchup 歷史、天氣）
4. **契約合規**：補齊 7 個時間戳欄位後才可進行任何 Data Leakage 審計

> ⚠️ 以上均為研究方向，**所有方向需通過 backtest ≥1500 場的驗證後才允許提案**

---

## 七、約束確認

- ✅ `paper_only=true`，無生產提案
- ✅ 不替換 `fixed_edge_5pct` champion
- ✅ 不做任何盈利聲明
- ✅ 模型改進僅為 research direction，不得推進至 production

---

*Artifact*: `data/paper_recommendations/p25_model_quality_gap_audit_20260520.json`
