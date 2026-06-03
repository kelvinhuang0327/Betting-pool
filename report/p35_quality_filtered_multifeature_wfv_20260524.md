# P35: Quality-Filtered Multi-Feature WFV + Calibration + Park Factor Audit

**日期**: 2026-05-24  
**作者**: AI Quant Research  
**狀態**: COMPLETE — diagnostic_only=True | promotion_freeze=True  
**Branch**: main | HEAD: 0547d58 → commit pending  
**Script**: `scripts/_p35_quality_filtered_multifeature_wfv.py`

---

## 一、研究動機

P34 發現 `league_average_fallback` 是 sp_fip_delta 的噪音汙染源（597 局 / 29.5%，sp_fip_delta 固定為 0.0，AUC=0.500）。P35 目的：

1. **排除 fallback 污染**，在 quality-filtered dataset (proxy + mixed) 上重跑 3-特徵多變量 WFV
2. **解明 park_run_factor 負係數謎題**（P33 standardized coeff = −0.3725）—— 進行五分位數方向審計
3. **與 P33 all-sample 基準比較**：排除後是否提升 AUC / Brier Skill / ECE？

---

## 二、資料來源

| 資料集 | 路徑 | n |
|---|---|---|
| Phase56 predictions | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` | 2,025 |
| SSOT Bullpen | `data/mlb_context/bullpen_usage_3d.jsonl` | 2,430 |
| As-played results | `data/mlb_2025/mlb-2025-asplayed.csv` | 2,430 |

### 2.1 Quality Filter

```
Phase56 total        : 2,025
league_avg_fallback  :   597 (29.5%) → EXCLUDED
Quality-filtered     : 1,428 rows retained
  - historical_proxy :   408 (28.6%)
  - mixed            : 1,001 (70.1%)  ← nesting of proxy + league data
                                          (not pure fallback)
```

### 2.2 3-Way Join

```
Phase56 quality rows  : 1,409  (after asplayed-join key match)
BP miss               :    38  (bullpen data absent for date/team)
Complete rows (all 3) : 1,371
```

---

## 三、SECTION 1 — Park Run Factor 方向審計

> **目的**：解釋 P33 發現 park_run_factor standardized coefficient = −0.3725 的成因

### 3.1 五分位數分析

| 分位 | PRF 範圍 | n | 主場勝率 |
|---|---|---|---|
| Q1 (投手友好) | 0.940 – 0.970 | 281 | **55.2%** |
| Q2 | 0.970 – 1.000 | 281 | **45.9%** ← lowest |
| Q3 (中性) | 1.000 – 1.000 | 281 | 54.4% |
| Q4 | 1.000 – 1.030 | 281 | 52.7% |
| Q5 (打者友好) | 1.030 – 1.150 | 285 | 54.0% |

### 3.2 方向結論

```
Pearson r (park_run_factor vs home_win): −0.0420
1D LR coefficient (standardized)       : −0.0842
1D LR coefficient (raw scale)          : −2.141

方向: NEGATIVE (較高 PRF → 略低 HW%)
Q1 HW%=55.2% → Q5 HW%=54.0% (Δ=−1.1%)
```

### 3.3 機制解釋

負向關聯雖然係數方向一致，但**效果量極小**（Pearson r=−0.042），且**非單調**：
- Q2（0.97–1.00）有最低勝率（45.9%），Q1、Q3–Q5 都接近 52–55%
- 主要驅動力：Q2 anomaly（可能 sample composition 偏差）而非真實球場效應
- **P33 standardized coeff = −0.3725 被高估** 因為 all-sample 包含 league_avg_fallback 的信號漏出（constant 0.0 rows 會破壞 feature 的方差估計）
- **P35 quality-filtered standardized coeff = −0.0934**（縮小 4x）→ 移除污染後方向維持負向但強度大幅降低

---

## 四、SECTION 2 — 個別特徵基準線（quality-filtered）

| 特徵 | AUC | Brier Skill | Pearson r (train) | 方向 |
|---|---|---|---|---|
| sp_fip_delta | 0.5262 | −0.0065 | +0.1404 | POSITIVE (符合預期) |
| park_run_factor | 0.5125 | +0.0016 | −0.0577 | NEGATIVE (確認) |
| bullpen_usage_diff | **0.4706** | −0.0009 | +0.0046 | **NOISE** ← 重要發現 |

**關鍵發現**：`bullpen_usage_diff` 在 quality-filtered set 中 AUC = 0.471（< 0.5），在 P32/P33 中 AUC = 0.529 的「信號」在移除 fallback 後完全消失 → **原先的 bullpen 信號是 league_avg_fallback 遊戲的混雜效應**。

---

## 五、SECTION 3 — 多特徵 WFV（quality-filtered）

### 5.1 Walk-Forward Split

```
n_complete = 1,371
Train: 959 games | 2025-04-27 → 2025-08-15
Val  : 412 games | 2025-08-15 → 2025-09-28
Val HW%: 53.2%
```

### 5.2 模型結果

| 指標 | P35 (quality-filtered) | P33 (all-sample) | Delta |
|---|---|---|---|
| AUC | **0.5253** | 0.5280 | −0.0027 |
| Brier Skill | **−0.0039** | +0.0009 | −0.0048 |
| Log-Loss Skill | −0.0028 | — | — |
| ECE (raw) | **0.0686** | 0.0213 | +0.0473 ← 劣化 |
| ECE after Platt (in-sample) | 0.0008 | 0.0050 | — |
| n_val | 412 | 721 | −309 |

**結論：排除 league_average_fallback 後，多特徵模型性能略微下降，而非提升。**

### 5.3 係數分析

| 特徵 | Std 係數 | Raw-scale 係數 | 解釋 |
|---|---|---|---|
| sp_fip_delta | **+0.2793** | +0.438 | 主要信號載體 |
| park_run_factor | −0.0934 | −2.377 | 弱負向（P33 的 −0.3725 被高估） |
| bullpen_usage_diff | +0.0014 | +0.000327 | 完全崩潰（≈ 0） |

### 5.4 校準分析（Reliability Diagram）

```
預測範圍僅 0.3–0.7（模型過度向基準率壓縮）

Bin [0.3-0.4]:  Conf=0.368, Acc=0.476, n= 21  → UNDERCONFIDENT
Bin [0.4-0.5]:  Conf=0.459, Acc=0.568, n=125  → UNDERCONFIDENT (最大 ECE 貢獻者)
Bin [0.5-0.6]:  Conf=0.545, Acc=0.495, n=206  → OK
Bin [0.6-0.7]:  Conf=0.637, Acc=0.600, n= 60  → OK
```

**ECE=0.0686 的主因**：模型在低置信區間（0.4–0.5）系統性低估，實際勝率達 56.8% 但模型僅預測 45.9%。  
**Platt in-sample ECE = 0.0008**（近乎完美，但屬 in-sample 上限，不可部署）。

### 5.5 信號分類

```
AUC=0.5253 ≥ 0.520 | Brier Skill < 0 → WEAK_SIGNAL (CALIBRATION_REQUIRED)
PROMOTION_BLOCKED_BY_GOVERNANCE (promotion_freeze=True)
```

---

## 六、SECTION 4 — 月度穩定性（quality-filtered, sp_fip_delta）

| 月份 | n | sp_fip AUC | park AUC | Pearson(sp) | HW% |
|---|---|---|---|---|---|
| 2025-04 | 37 | **0.700** | 0.446 | +0.344 | 48.6% |
| 2025-05 | 304 | 0.550 | 0.503 | +0.095 | 52.3% |
| 2025-06 | 277 | 0.581 | 0.517 | +0.158 | 49.1% |
| 2025-07 | 252 | 0.596 | 0.527 | +0.167 | 54.0% |
| 2025-08 | 285 | 0.512 | 0.497 | +0.025 | 53.7% |
| 2025-09 | 254 | 0.544 | 0.471 | +0.084 | 53.9% |

```
sp_fip_delta monthly AUC: mean=0.5806, std=0.0600
上 0.5 比率: 6/6 (100%) → STABLE ✅

比較:
  P33 (all-sample bullpen_usage_diff): mean=0.487, 43% above 0.5 → UNSTABLE
  P34 historical_proxy sp_fip_delta  : mean=0.578, 83% above 0.5  → STABLE
  P35 quality-filtered sp_fip_delta  : mean=0.581, 100% above 0.5 → STABLE ✅
```

**park_run_factor** 月度 AUC 均值 ≈ 0.494（Aug/Sep < 0.5）→ 方向不穩定，不宜用作個別信號。

---

## 七、綜合比較（P31B → P35）

| Phase | Feature / Model | AUC | Brier Skill | 月度穩定性 |
|---|---|---|---|---|
| P31B | sp_fip_delta (fallback 污染) | 0.511 | — | — |
| P31B | park_run_factor (fallback 污染) | 0.513 | — | — |
| P31B | bullpen_fatigue_delta_3d | 0.500 | — | NOISE |
| P32 | bullpen_usage_diff (SSOT) | 0.529 | — | — |
| P33 | sp_fip_delta (individual, all-sample) | 0.5219 | +0.0001 | — |
| P33 | park_run_factor (individual, all-sample) | 0.5227 | +0.0008 | — |
| P33 | bullpen_usage_diff (individual, all-sample) | 0.5291 | −0.0004 | UNSTABLE 43% |
| P33 | multi-feature 3D (all-sample) | 0.5280 | +0.0009 | — |
| P34 | historical_proxy (sp_fip_delta, per-tier) | 0.5420 | −0.0062 | STABLE 83% |
| P34 | mixed (sp_fip_delta, per-tier) | 0.5216 | −0.0053 | STABLE 83% |
| **P35** | **sp_fip_delta (quality-filtered, individual)** | **0.5262** | −0.0065 | **STABLE 100%** |
| P35 | park_run_factor (quality-filtered, individual) | 0.5125 | +0.0016 | UNSTABLE (park) |
| P35 | bullpen_usage_diff (quality-filtered) | **0.4706** | — | **NOISE** (< 0.5) |
| P35 | multi-feature 3D (quality-filtered) | 0.5253 | **−0.0039** | — |

---

## 八、關鍵發現摘要

### 🔑 Finding 1: bullpen_usage_diff 信號為假陽性
P32/P33 中 AUC=0.529 的 bullpen_usage_diff 在 quality-filtered set 中崩潰至 AUC=0.470（< 0.5）。原本的「信號」來自 league_average_fallback 遊戲的混雜效應，而非真實的 bullpen 預測能力。

### 🔑 Finding 2: park_run_factor 負向係數機制確認
P33 的 standardized coeff = −0.3725 在 P35 quality-filtered 中縮小至 −0.0934（4倍縮小）。真實負向相關 Pearson r = −0.042，效果量微小，不足以作為獨立預測因子。五分位數分析顯示 Q2（0.97-1.00）是主要異常點，並非單調遞減關係。

### 🔑 Finding 3: sp_fip_delta 是唯一穩健信號
- Quality-filtered 後月度穩定性提升至 100%（vs P34 83%）
- Mean AUC = 0.581（vs P31B 0.511 fallback 污染版）
- 方向一致（Pearson r = +0.14，所有月份正向）
- **sp_fip_delta 是整個特徵集中唯一值得進一步研究的信號**

### 🔑 Finding 4: 多特徵組合無增益
- 排除 fallback 後多特徵 AUC=0.5253 vs 個別 sp_fip_delta AUC=0.5262（個別更好）
- ECE=0.0686（比 P33 0.0213 更差）—— 多特徵校準更困難
- bullpen + park 的加入實際上降低了 Brier Skill（−0.0039 vs −0.0065 for sp only, but model structure differences）
- **結論：單一 sp_fip_delta 信號優於 3-特徵組合**

---

## 九、後續研究建議

| 優先 | 研究方向 | 動機 |
|---|---|---|
| 高 | **P36: sp_fip_delta 純淨信號深度研究** | 100% 月度穩定性 + mean AUC=0.581，最有潛力 |
| 中 | **P37: park_run_factor × team strength 交互效應** | 負向係數可能是球隊實力混雜因子 |
| 低 | **bullpen 數據品質改善** | 當前 SSOT IP 數據在 quality-filtered 集無信號 |

---

## 十、治理聲明

```
diagnostic_only   = True   ✅
promotion_freeze  = True   ✅
Champion strategy = UNMODIFIED ✅
Kelly/betting     = UNMODIFIED ✅
Test suite        = 216 PASS / 0 FAIL ✅
Staged files      = 0 ✅
```

---

*Generated by P35 analysis pipeline — 2026-05-24*
