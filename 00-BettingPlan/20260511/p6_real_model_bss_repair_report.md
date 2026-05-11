# P6 Real Model BSS Repair Report

**任務代號**: P6 Real Model Underperformance Audit & Calibration Repair  
**產出日期**: 2026-05-11  
**完成標記**: `P6_REAL_MODEL_BSS_REPAIR_READY`

---

## 1. 執行摘要

P6 任務針對 P5 產出的真實模型機率進行品質審計，發現系統性主場機率高估偏差，並實作 bin-level 校準修復。在樣本內測試中，BSS 從 -0.0333 改善至 -0.0068（delta +0.0265），ECE 從 0.0595 降至 0.0004。但由於這是**樣本內校準候選**，仍無法通過 BSS 正值閘，系統正確標記為 `BLOCKED_NEGATIVE_BSS`，**不可投入生產環境**。

---

## 2. 輸入 Artifact

| 項目 | 路徑 |
|------|------|
| 模型機率 CSV (P5) | `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv` |
| 輸入總行數 | 2,430 rows |
| 有 model_prob_home 行數 | 1,341 rows (55.2%) |
| 缺少 model_prob_home 行數 | 1,089 rows (44.8%) |
| 所有行 Status=Final | ✅ |
| 所有行有 Home/Away ML | ✅ |

---

## 3. 審計結果 (Task 2 + Task 3)

### 3.1 核心指標

| 指標 | 數值 |
|------|------|
| Brier Score (模型) | 0.2552 |
| Brier Score (市場) | 0.2470 |
| **Brier Skill Score (BSS)** | **-0.0333** |
| ECE (Expected Calibration Error) | 0.0595 |
| avg_model_prob | 0.5661 |
| avg_market_prob | 0.5181 |
| avg_outcome (實際主場勝率) | 0.5227 |
| 主場機率高估偏差 | **+4.8 pp** (model 比 market 高) |

### 3.2 根本原因

模型系統性高估主場勝率：`avg_model_prob = 0.566` 對比 `avg_market_prob = 0.518`，偏差達 **4.8 個百分點**。即使主場方向性正確（高 model_prob 時主場勝率確實更高：0.536 vs 0.475），仍因機率過度樂觀導致 Brier 分數劣於市場基準，BSS 為負值。

### 3.3 方向性檢查

| 檢查項目 | 值 |
|---------|-----|
| 主場勝率 (model > 0.5 時) | 0.5364 |
| 主場勝率 (model < 0.5 時) | 0.4747 |
| 平均 model_prob（主場勝） | 0.5708 |
| 平均 model_prob（主場負） | 0.5609 |

**方向性正確**：模型確實能區分主客場勝負，但機率數值過度偏高，壓縮了分數提升空間。

---

## 4. 校準修復 (Task 4 + Task 5)

### 4.1 方法

- **方法**: Equal-width bin calibration (等寬分箱)
- **分箱數**: n_bins=10，min_bin_size=30
- **稀疏分箱處理**: < min_bin_size 樣本時，與全局勝率加權混合
- **空分箱處理**: 使用全局勝率

### 4.2 校準前後比較

| 指標 | 原始 | 校準後 (樣本內) | 變化 |
|------|------|----------------|------|
| BSS | -0.0333 | **-0.0068** | +0.0265 ↑ |
| ECE | 0.0595 | **0.0004** | -0.0591 ↑ |
| 可用行數 | 1,341 | 1,341 | = |

### 4.3 評估建議

**建議**: `KEEP_BLOCKED`  
**理由**: 雖然樣本內 BSS 改善顯著，但這是**同一資料集的樣本內校準**，校準本身即是對訓練資料擬合。若要解除封鎖，必須通過 Out-of-Fold (OOF) 或 Walk-Forward 驗證，確認校準效果在未見資料上可複製。

> ⚠️ **in-sample calibration candidate — not production deployable unless OOF validated**

---

## 5. 模擬結果比較 (Task 9)

| 策略 | BSS | ECE | 下注次數 | ROI | Gate |
|------|-----|-----|---------|-----|------|
| `moneyline_edge_threshold_v0` (P5, 原始) | -0.01877 | 0.03629 | — | — | BLOCKED_NEGATIVE_BSS |
| `moneyline_edge_threshold_v0_calibrated_candidate` (P6, 樣本內) | **-0.0038** | **0.0123** | 686 | 2.33% | BLOCKED_NEGATIVE_BSS |

**重要**：模擬 ROI=2.33% 是基於樣本內校準機率計算，**具有強烈的過擬合疑慮**，不能解讀為真實獲利能力。

---

## 6. 閘控建議結果 (Task 10)

- **策略**: `moneyline_edge_threshold_v0_calibrated_candidate`
- **閘狀態**: `BLOCKED_NEGATIVE_BSS`
- **允許投注**: ❌ False
- **校準警告**: 已在 source_trace 中記錄 `calibration_warning`
- **輸出位置**: `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

---

## 7. 新增模組清單

| 模組 | 功能 |
|------|------|
| `wbc_backend/prediction/mlb_model_probability_audit.py` | 機率品質審計：BSS、ECE、方向性、分段診斷 |
| `wbc_backend/prediction/mlb_probability_calibration_repair.py` | 等寬分箱校準、評估、樣本內警告 |
| `scripts/run_mlb_model_probability_audit_repair.py` | CLI 串接審計+修復+評估管線 |

### 7.1 Strategy Simulator 更新 (Task 6)

`wbc_backend/simulation/strategy_simulator.py` 新增：
- `calibrated_model_row_count` 計數器
- source_trace 新增 `calibrated_model_count` 欄位
- `probability_source_mode = "calibrated_model"` 分類模式
- `calibration_warning` 欄位（calibrated_model_count > 0 時自動附加）

---

## 8. 測試覆蓋

| 測試檔案 | 測試數 |
|---------|--------|
| `tests/test_mlb_model_probability_audit.py` | 16 |
| `tests/test_mlb_probability_calibration_repair.py` | 14 |
| `tests/test_run_mlb_model_probability_audit_repair.py` | 8 (含 2 real-data skip) |
| 含 P1-P5 回歸 | 216 tests total (全部通過) |

---

## 9. P6 Artifact 位置

| Artifact | 路徑 |
|---------|------|
| 審計 JSON | `outputs/predictions/PAPER/2026-05-11/model_probability_audit.json` |
| 分段審計 JSON | `outputs/predictions/PAPER/2026-05-11/model_probability_segment_audit.json` |
| 校準 CSV | `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_calibrated_probabilities.csv` |
| 評估 JSON | `outputs/predictions/PAPER/2026-05-11/calibration_candidate_evaluation.json` |
| 審計修復摘要 | `outputs/predictions/PAPER/2026-05-11/p6_audit_repair_summary.md` |
| 校準模擬 JSONL | `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_calibrated_candidate_d5fb827f.jsonl` |

---

## 10. 成功標準驗證

| 成功標準 | 狀態 |
|---------|------|
| BSS 審計完成，數值準確 | ✅ BSS=-0.0333 |
| 根本原因識別（主場偏差）| ✅ +4.8pp 偏差 |
| 校準修復模組實作 | ✅ bin calibration |
| 樣本內警告正確標記 | ✅ in_sample_warning 存在 |
| 校準候選 BSS 改善 | ✅ -0.0333 → -0.0068 |
| 閘仍為 BLOCKED | ✅ KEEP_BLOCKED |
| 模擬 source_trace 含校準警告 | ✅ calibration_warning 欄位 |
| 所有 P1-P5 測試通過 | ✅ 216/216 passed |

---

## 11. 下一步：P7 Out-of-Fold 驗證

P6 發現：等寬分箱校準在**樣本內**表現良好（BSS -0.0333 → -0.0068），但必須通過**Out-of-Fold 驗證**才能確認校準效果的泛化能力。

P7 任務定義：
- 將 1,341 個有效行分成 K 折（建議 K=5）
- 每折以「其餘 K-1 折訓練校準映射 → 在目標折評估」
- 計算 OOF BSS、OOF ECE
- 若 OOF BSS > 0：升級為生產候選，解除 KEEP_BLOCKED
- 若 OOF BSS ≤ 0：確認 P6 校準無法泛化，維持 BLOCKED

---

`P6_REAL_MODEL_BSS_REPAIR_READY`
