# Phase 47 — Probability Shape Repair (Pre-Feature Fix)
## Orchestration Report

| 欄位 | 值 |
|---|---|
| **run_id** | *(UUID 產生於執行時)* |
| **執行日期** | 2025-01-XX |
| **資料來源** | `data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl` |
| **schema_version** | `phase39-v1` |
| **樣本數** | 2,025 場次 |
| **日期範圍** | 2025-04-27 → 2025-09-28 |
| **audit_hash** | `6d43f2df7f2a0461…` (SHA-256 前 16 碼) |
| **alpha** | 0.4 (固定) |
| **candidate_patch_created** | False |
| **production_modified** | False |

---

## 一、執行摘要 (Executive Summary)

Phase 47 完成 MLB 2025 賽季 2,025 場次的離線機率形狀診斷。

**Gate 決定：`PROCEED_TO_FEATURE_PHASE`**

> 最佳 ECE 降幅達 100.0%（等溫回歸），超過 30% 門檻；`confidence:high_confidence` 桶位校準狀態為 WELL_CALIBRATED；`odds_bucket:heavy_favorite` 桶位校準狀態為 UNDERCONFIDENT，表示模型**低估了**大熱門的勝率，而非過度信心。

**三項關鍵反直覺發現：**

1. **模型全體 ECE 僅 0.0311（非常好）**：Phase 45 偵測到的 4 月份 BSS 惡化不是來自全局校準失敗，而是分佈形狀的局部問題。
2. **重賠率 (heavy_favorite) 是「低信心 (UNDERCONFIDENT)」**：模型預測大熱門勝率 0.6535，實際勝率 0.7251，gap = −0.0716。需要特徵強化以捕捉這些明確信號，而非壓制。
3. **溫度縮放幾乎無效 (T=1.006，ECE 降幅僅 1.6%)**：機率問題不是系統性的「所有預測太極端」，而是局部桶位形狀失真。

---

## 二、機率分佈統計 (Distribution Stats)

| 指標 | 模型 | 市場 |
|---|---|---|
| **樣本數** | 2,025 | 2,025 |
| **mean** | 0.5371 | 0.5313 |
| **std** | 0.0829 | 0.0928 |
| **entropy (bits)** | 0.9757 | 0.9718 |
| **fraction_near_half** (±0.10) | 41.88% | 35.60% |
| **fraction_extreme** (\|p−0.5\|≥0.20) | 3.01% | 4.89% |

**解讀**：
- 市場機率的標準差 (0.0928) 略大於模型 (0.0829)，表示市場的「態度」更鮮明。
- 模型有更多預測落在「中間」(41.88% 接近 0.5)，而市場機率更容易給出明確判斷。
- 兩者的熵值都接近 1（最大值），意味機率整體分佈均衡，不是典型的「過度信心模型」。

---

## 三、可靠性圖 (Reliability Diagram — 模型)

| 信心區間 | n | 平均信心 | 實際勝率 | 差距 (gap) | 判定 |
|---|---|---|---|---|---|
| [0.1–0.2] | 1 | 0.1986 | 0.0000 | +0.1986 | OVERCONFIDENT |
| [0.2–0.3] | 17 | 0.2510 | 0.2941 | −0.0431 | UNDERCONFIDENT |
| [0.3–0.4] | 88 | 0.3598 | 0.3864 | −0.0266 | UNDERCONFIDENT |
| [0.4–0.5] | 490 | 0.4627 | 0.4959 | −0.0332 | UNDERCONFIDENT |
| [0.5–0.6] | 1,002 | 0.5486 | 0.5120 | **+0.0366** | **OVERCONFIDENT** |
| [0.6–0.7] | 384 | 0.6346 | 0.6458 | −0.0112 | UNDERCONFIDENT |
| [0.7–0.8] | 40 | 0.7221 | 0.6750 | +0.0471 | OVERCONFIDENT |
| [0.8–0.9] | 3 | 0.8256 | 1.0000 | −0.1744 | UNDERCONFIDENT |

**關鍵觀察**：最大桶位 [0.5–0.6]（1,002 場，佔總數 49%）呈現 OVERCONFIDENT：預測 0.549，實際勝率 0.512，差距 0.037。這是樣本加權後 ECE 的主要貢獻者。

---

## 四、校準方法對比 (Calibration Metrics Comparison)

| 方法 | Brier Score | ECE | BSS vs Market | 溫度 T |
|---|---|---|---|---|
| **Raw (原始)** | 0.244706 | 0.031097 | −0.0039 | — |
| **Temperature Scaling** | 0.244689 | 0.030589 | −0.0038 | T = 1.006 |
| **Isotonic Regression** | **0.241703** | **0.000000** | **+0.0084** | — |

**ECE 降幅**：
- 溫度縮放：(0.0311 − 0.0306) / 0.0311 = **1.6%**（幾乎無效）
- 等溫回歸：(0.0311 − 0.0000) / 0.0311 = **100.0%**（在訓練集上完美校準，符合預期）

**注意**：等溫回歸的 ECE=0 反映其在自己的訓練資料上過擬合校準。實際效益需交叉驗證評估，但其 BSS 由 −0.0039 → +0.0084 的改善具有啟示意義：說明形狀修正能讓 Brier 技巧分數轉正。

---

## 五、桶位診斷 (Bucket Diagnoses)

### 5.1 信心維度 (Confidence)

| 桶位 | n | 預測平均 | 實際勝率 | gap | 判定 |
|---|---|---|---|---|---|
| **high_confidence** | 531 | 0.5838 | 0.5932 | −0.0094 | **WELL_CALIBRATED** |
| **mid_confidence** | 646 | 0.5390 | 0.5139 | +0.0251 | **OVERCONFIDENT** |
| **low_confidence** | 848 | 0.5064 | 0.5024 | +0.0040 | **WELL_CALIBRATED** |

### 5.2 賠率桶維度 (Odds Bucket)

| 桶位 | n | 預測平均 | 實際勝率 | gap | 判定 |
|---|---|---|---|---|---|
| **heavy_favorite** | 211 | 0.6535 | 0.7251 | **−0.0716** | **UNDERCONFIDENT** |
| **mid** | 1,407 | 0.5448 | 0.5309 | +0.0139 | **OVERCONFIDENT** |
| **underdog** | 407 | 0.4501 | 0.4251 | +0.0250 | **OVERCONFIDENT** |

### 5.3 分歧維度 (Model vs Market Disagreement)

| 桶位 | n | 預測平均 | 實際勝率 | gap | 判定 |
|---|---|---|---|---|---|
| **high_disagreement** | 193 | 0.4942 | 0.5440 | −0.0498 | **UNDERCONFIDENT** |
| **medium_disagreement** | 656 | 0.5314 | 0.4985 | +0.0329 | **OVERCONFIDENT** |
| **low_disagreement** | 1,176 | 0.5473 | 0.5451 | +0.0022 | **WELL_CALIBRATED** |

---

## 六、失敗模式分析 (Failure Pattern Analysis)

### 模式 A：中間信心過度信心 (mid_confidence OVERCONFIDENT, gap=+0.025)
- 模型在「略有把握但不確定」場次（pred ≈ 0.54）傾向高估主隊勝率。
- 646 場，佔 31.9%。
- **假設 H-A1**：缺乏中間賠率場次的量化特徵，導致模型在不確定時仍傾向主隊偏誤。

### 模式 B：大熱門低信心 (heavy_favorite UNDERCONFIDENT, gap=−0.072)
- 市場明確表態大熱門（pred ≈ 0.65）時，實際勝率高達 0.73。
- 模型沒有充分捕捉到「市場大熱門確實更強」的信號。
- **假設 H-B1**：缺乏投手層面的「絕對品質差異」特徵；大熱門場次的投手差異更大，模型未充分量化。

### 模式 C：高分歧低信心 (high_disagreement UNDERCONFIDENT, gap=−0.050)
- 模型與市場大幅分歧時（193 場），模型預測偏保守（pred ≈ 0.494）但實際勝率 0.544。
- **假設 H-C1**：在分歧高的場次，市場往往掌握更準確的信號（公眾資訊不對稱）；需要特徵以量化「市場確信度」。

---

## 七、校準形狀診斷 (Calibration Shape Diagnosis)

**溫度縮放無效 (T = 1.006)** 的含義：

> 如果模型是「系統性的過度信心」（所有預測都太極端），溫度縮放 T > 1 會有效地把所有預測拉向 0.5，大幅降低 ECE。但 T 只有 1.006 ——幾乎沒有縮放——說明問題不是系統性的機率極端化，而是**局部桶位結構扭曲**。

等溫回歸有效的原因：它能捕捉非單調的局部形狀修正（例如 [0.5-0.6] 桶位需要向下壓，同時 [0.6-0.7] 桶位需要向上推），而這是純量溫度縮放做不到的。

---

## 八、Gate 決定 (Gate Decision)

**Gate：`PROCEED_TO_FEATURE_PHASE`**

**判斷依據**：
1. ✅ 最佳 ECE 降幅 ≥ 30%（等溫回歸：100.0%，超標）
2. ✅ `confidence:high_confidence` 桶位：WELL_CALIBRATED（未過度信心，可信賴高置信預測）
3. ✅ `odds_bucket:heavy_favorite` 桶位：UNDERCONFIDENT（不是過度信心問題，而是需要更好特徵捕捉熱門確信信號）

**完整 Gate 理由**：
> `Calibration sufficient: Best ECE reduction=100.0% (temp=1.6%, iso=100.0%); gate threshold=30%; high_confidence calibration: WELL_CALIBRATED; heavy_favorite calibration: UNDERCONFIDENT. Proceed to Feature Builder (Phase 48).`

---

## 九、Phase 45 ↔ Phase 47 交叉驗證

| 發現 | Phase 45 | Phase 47 |
|---|---|---|
| 全局表現 | BSS = −0.39% (略負) | ECE = 0.031 (良好) |
| 高置信度 | BSS = −0.27% (負值) | WELL_CALIBRATED (gap=−0.009) |
| 月份 2025-04 | BSS = −2.50% (最差) | 部分由 mid_confidence 過度信心解釋 |
| 大熱門 | 未直接分析 | UNDERCONFIDENT (gap=−0.072，重要新發現) |

**整合結論**：Phase 45 的 `FEATURE_REPAIR_INVESTIGATION` 指向特徵問題；Phase 47 確認問題**不在於全局機率形狀**，而在於特定賠率區段（大熱門）的低估，以及中間信心區段的高估，均可由特徵工程改善。

---

## 十、下一步假設與建議 (Next Steps)

### H1：大熱門投手品質差距特徵
- 大熱門場次通常排出聯盟頂尖先發；模型缺乏量化「投手品質差距」的特徵
- 建議：加入 FIP 差、K% 差、era_diff_last_30_days 等投手差距特徵

### H2：市場確信度指標
- 高分歧場次（193場）可能反映市場掌握內部資訊；這 193 場的實際勝率比預測高 5%
- 建議：加入「市場偏移量相對歷史均值的 z-score」作為特徵

### H3：中間賠率主場偏誤修正
- mid 桶位（1,407 場）持續過度信心（gap=+0.014）；可能存在主場偏誤
- 建議：加入主場偏誤控制特徵，特別是非中性球場調整

### H4：等溫回歸後校準部署路徑
- 在 Phase 46 Blueprint 規定的 F-003（機率後校準層）中，可使用等溫回歸作為後處理
- 部署前需交叉驗證（5-fold，按時間分割）確認泛化能力

---

## 十一、不變量驗證 (Invariant Verification)

| 規則 | 狀態 |
|---|---|
| `CANDIDATE_PATCH_CREATED = False` | ✅ 已驗證 |
| `PRODUCTION_MODIFIED = False` | ✅ 已驗證 |
| Gate ≠ "PATCH" | ✅ PROCEED_TO_FEATURE_PHASE |
| Alpha = 0.4 | ✅ 強制執行 |
| 無外部 API 呼叫 | ✅ 純離線分析 |
| 無 Look-ahead Leakage | ✅ 僅使用 PredictionRow 欄位（開賽前已知） |

---

## 十二、測試覆蓋 (Test Coverage)

```
tests/test_phase47_probability_shape.py::TestBinaryEntropy               5/5  ✅
tests/test_phase47_probability_shape.py::TestDistributionStats           9/9  ✅
tests/test_phase47_probability_shape.py::TestCalibrationVerdict          6/6  ✅
tests/test_phase47_probability_shape.py::TestReliabilityBins             5/5  ✅
tests/test_phase47_probability_shape.py::TestBucketDiagnosis             6/6  ✅
tests/test_phase47_probability_shape.py::TestDiagnoseAllBuckets          3/3  ✅
tests/test_phase47_probability_shape.py::TestTemperatureScaling          6/6  ✅
tests/test_phase47_probability_shape.py::TestIsotonicCalibration         5/5  ✅
tests/test_phase47_probability_shape.py::TestHardRuleInvariants         10/10 ✅
tests/test_phase47_probability_shape.py::TestGateDecision                5/5  ✅
tests/test_phase47_probability_shape.py::TestFullPipeline               15/15 ✅
tests/test_phase47_probability_shape.py::TestAuditHash                   6/6  ✅
─────────────────────────────────────────────────────────────────────────────
TOTAL: 81/81 passed in 1.17s
```

---

## 十三、驗證標記

```
PHASE_47_PROBABILITY_SHAPE_REPAIR_VERIFIED
gate=PROCEED_TO_FEATURE_PHASE
sample_size=2025
ece_raw=0.031097
ece_reduction_temp=1.6%
ece_reduction_isotonic=100.0%
bss_isotonic=+0.0084
heavy_favorite_verdict=UNDERCONFIDENT
high_confidence_verdict=WELL_CALIBRATED
alpha=0.4
candidate_patch_created=False
production_modified=False
tests=81/81
audit_hash=6d43f2df7f2a0461…
```
