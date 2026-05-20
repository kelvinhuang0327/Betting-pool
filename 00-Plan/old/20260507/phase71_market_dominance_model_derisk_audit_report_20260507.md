# Phase 71 — Market Dominance and Model De-risk Audit
## 0.65–0.70 Strong Favorite Band

**日期**: 2026-05-07  
**版本**: `phase71_market_dominance_model_derisk_audit_v1`  
**資料集**: `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` (n=2025)  
**安全旗標**: `DIAGNOSTIC_ONLY=True` / `CANDIDATE_PATCH_CREATED=False` / `PRODUCTION_MODIFIED=False` / `ALPHA_MODIFIED=False`  
**ALPHA（凍結）**: 0.40  
**Phase 70 gate anchor**: `MARKET_ONLY_SUPERIOR`

---

## 一、背景與目標

Phase 70 發現在 **0.65–0.70 strong favorite band**：
- model Brier = 0.1865，market Brier = 0.1725，**gap = +0.0140**（市場明顯較優）
- 真實勝率 0.767，而模型均值僅 0.672（低估 ~9.5%）
- 市場均值 0.669（同樣低估，但殘差更小）
- Phase 70 gate：**`MARKET_ONLY_SUPERIOR`**

Phase 71 目標：**五維度深度稽核**市場優勢的穩定性與可信度，確認是否值得進入 Phase 72 paper-only market de-risk guard 提案。

---

## 二、資料摘要

| 項目 | 數值 |
|------|------|
| 總樣本數 | 2,025 |
| 目標段（0.65–0.70）| **103** 筆 |
| feature_version | `phase56_sp_bullpen_context_v1` |
| 分析時間 | 2026-05-07 |

---

## 三、Dimension A — 分段 Market vs Model 指標

| Segment | n | MdlBrier | MktBrier | Delta | WinRate | MktSup |
|---------|---|----------|----------|-------|---------|--------|
| all_games | 2025 | 0.2447 | 0.2438 | +0.0009 | 0.530 | No |
| home_favorite_only | 1429 | 0.2434 | 0.2434 | +0.0000 | 0.554 | No |
| away_favorite_only | 596 | 0.2479 | 0.2447 | +0.0032 | 0.473 | No |
| model_prob_0.60_0.65 | 281 | 0.2406 | 0.2398 | +0.0008 | 0.601 | No |
| **model_prob_0.65_0.70** | **103** | **0.1865** | **0.1725** | **+0.0140** | **0.767** | **Yes** |
| model_prob_0.70_0.75 | 35 | 0.2155 | 0.2105 | +0.0051 | 0.686 | Yes |
| heavy_favorite (≥0.70) | 43 | 0.2078 | 0.2056 | +0.0021 | 0.698 | No |
| phase45_failure | 149 | 0.4078 | 0.3869 | +0.0209 | 0.000 | Yes |
| phase68_failure | 37 | 0.4727 | 0.4275 | +0.0452 | 0.000 | Yes |

**關鍵發現**：市場優勢高度集中在 **0.65–0.70 band**（delta=+0.0140），其他區段幾乎無優勢（gap < 0.005）。

---

## 四、Dimension B — 機率分佈形狀

**目標段（0.65–0.70）分佈比較**：

| 指標 | Model | Market |
|------|-------|--------|
| std | **0.0154** | **0.0579** |
| IQR | 0.0274 | 0.0767 |
| min | 0.650 | 0.550+ |
| max | 0.699 | 0.77+ |

| 比率指標 | 數值 |
|---------|------|
| **compression_ratio** (model_std/market_std) | **0.267** 🔴 |
| rank_correlation (Spearman) | **0.172** 🔴 |
| mean_disagreement \|model-market\| | 0.043 |
| disagreement_rate (\|diff\| ≥ 0.05) | **33.0%** |
| **model_compressed** | **True** |

**全段壓縮分析**：

| Segment | MdlStd | MktStd | Compress | RankCorr | DisgRate |
|---------|--------|--------|----------|----------|---------|
| all_games | 0.0829 | 0.0928 | 0.893 | 0.746 | 42.0% |
| home_favorite_only | 0.0542 | 0.0773 | 0.701 | 0.653 | 38.7% |
| model_prob_0.60_0.65 | 0.0135 | 0.0584 | 0.231 | 0.274 | 36.3% |
| **model_prob_0.65_0.70** | **0.0154** | **0.0579** | **0.267** | **0.172** | **33.0%** |
| model_prob_0.70_0.75 | 0.0132 | 0.0456 | 0.289 | -0.189 | 25.7% |
| heavy_favorite | 0.0343 | 0.0462 | 0.741 | 0.212 | 30.2% |

**解讀**：
- model 在 0.65–0.70 band 幾乎是「水平線」（std=0.015），市場分佈是 3.8 倍更寬（std=0.058）
- Spearman rank correlation 僅 0.17：**模型與市場對個別比賽的排名判斷高度不一致**
- 33% 的比賽兩者差距 ≥ 5%，顯示大量系統性分歧

---

## 五、Dimension C — sp_fip_delta × Market Signal 歸因

| 項目 | 數值 |
|------|------|
| 目標段可用率 | **100.0%** (103/103) |
| 全資料集可用率 | 100.0% |
| mean_sp_fip (目標段) | **+0.322** ⚠️ 高偏移 |
| mean_sp_fip (全體) | +0.008 |
| sp_fip vs model-market diff corr | **-0.338** |
| sp_fip vs market_prob corr | **+0.350** |
| sp_fip vs model residual corr | -0.086 |

**高/低 sp_fip_delta Bucket 分析**（按中位數分割）：

| Bucket | n | MdlBrier | MktBrier | Residual |
|--------|---|----------|----------|---------|
| High sp_fip (> median) | 49 | 0.1843 | **0.1616** | -0.1035 |
| Low sp_fip (≤ median) | 54 | 0.1885 | **0.1825** | -0.0876 |
| Gap (high-low residual) | | | | **-0.0159** |

**關鍵發現**：
- `sp_fip_absorbed_by_market = True`：|sp_fip vs market corr| (0.350) > |sp_fip vs residual corr| (0.086) + 0.05
- `sp_fip_independent_signal = False`：殘差 bucket gap = -0.016 < 0.05 閾值
- **sp_fip_delta 已被市場機率充分吸收，並非獨立訊號**
- 目標段 mean_sp_fip = 0.323 遠高於整體 0.008：此 band 的比賽主場先發投手優勢顯著更大（即主場隊先發投手 FIP 顯著優於客場）

---

## 六、Dimension D — 跨時間窗口市場穩定性

| Window | n | MdlBrier | MktBrier | Delta | WinRate | MktSup |
|--------|---|----------|----------|-------|---------|--------|
| window_1 | 25 | 0.1605 | 0.1537 | +0.0068 | 0.840 | Yes |
| window_2 | 26 | 0.2126 | 0.2055 | +0.0071 | 0.692 | Yes |
| window_3 | 14 | 0.2737 | 0.2560 | +0.0177 | 0.500 | Yes |
| window_4 | 25 | 0.1735 | 0.1611 | +0.0124 | 0.800 | Yes |
| window_5 | 13 | 0.1155 | 0.0748 | +0.0407 | 1.000 | Yes |

**5/5 個窗口市場優勢一致**，`split_instability_detected = False`。

---

## 七、Dimension E — Team 集中度與特徵可用性矩陣

### 7.1 Team 集中度（目標段前 10 隊）

| 主場隊 | n | 佔比 | Brier Delta | Residual |
|--------|---|------|-------------|---------|
| Los Angeles Dodgers | 12 | 11.7% | +0.0205 | -0.080 |
| Milwaukee Brewers | 12 | 11.7% | +0.0129 | -0.169 |
| Houston Astros | 8 | 7.8% | DL | +0.185 |
| New York Mets | 6 | 5.8% | DL | +0.010 |
| Philadelphia Phillies | 6 | 5.8% | DL | -0.005 |
| New York Yankees | 6 | 5.8% | DL | +0.170 |
| Seattle Mariners | 6 | 5.8% | DL | -0.327 |

前兩隊（LAD + MIL）佔 23.4%，市場優勢均正向。前 10 隊無 DL 的隊伍 Brier delta 均為正值。

### 7.2 特徵可用性矩陣

| Feature | 目標段可用% | 全體可用% | 目標段均值 | 全體均值 | ExtDelta |
|---------|------------|----------|----------|---------|---------|
| sp_fip_delta | 100.0% | 100.0% | 0.3228 | 0.0084 | **+0.3144** ⚠️ |
| park_run_factor | 100.0% | 100.0% | 0.9985 | 1.0041 | -0.0055 |
| season_game_index | 100.0% | 100.0% | 0.5929 | 0.6270 | -0.0341 |
| bullpen_fatigue_delta_3d | 0.0% | 0.0% | N/A | N/A | 0.000 |
| home_bullpen_fatigue_3d | 0.0% | 0.0% | N/A | N/A | 0.000 |
| away_bullpen_fatigue_3d | 0.0% | 0.0% | N/A | N/A | 0.000 |

**注意**：sp_fip_delta ExtDelta = +0.314，目標段的比賽主場先發投手大幅優於整體水準，這解釋了為何此 band 市場會更準確地反映先發投手優勢。

---

## 八、Bootstrap 信賴區間

| Segment | 指標 | 觀測值 | 95% CI | excl0 | stable |
|---------|------|--------|--------|-------|--------|
| model_prob_0.65_0.70 | brier_delta_vs_market | **+0.0140** | **[+0.0048, +0.0240]** | ✅ | ✅ |
| model_prob_0.65_0.70 | residual_mean | -0.0951 | [-0.1804, -0.0086] | ✅ | ❌ |
| model_prob_0.65_0.70 | market_residual_mean | -0.0982 | [-0.1698, -0.0222] | ✅ | ❌ |
| heavy_favorite | brier_delta_vs_market | +0.0021 | [-0.0121, +0.0190] | ❌ | ✅ |
| all_games | brier_delta_vs_market | +0.0009 | [-0.0017, +0.0038] | ❌ | ✅ |
| model_prob_0.65_0.70 | sp_fip_residual_bucket_gap | -0.0159 | [-0.1931, +0.1510] | ❌ | ❌ |

**關鍵 CI 結論**：Brier delta [+0.0048, +0.0240] — **穩定且排除零值**，市場優勢在統計上顯著。

---

## 九、負向對照組（6 組）

| 控制組 | 觀測值 | Null均值 | Signal Gap | overfit_risk |
|--------|--------|---------|------------|-------------|
| shuffled_market_assignment | +0.0140 | -0.0562 | **+0.0702** | ❌ False |
| shuffled_model_assignment | +0.0140 | +0.0659 | **-0.0519** | ❌ False |
| random_model_minus_market | +0.0031 | +0.0061 | -0.0030 | ⚠️ True |
| random_sp_fip_bucket | +0.0159 | +0.0628 | **-0.0469** | ❌ False |
| random_split_assignment | +0.0125 | +0.0099 | +0.0026 | ⚠️ True |
| irrelevant_date_bucket_split | +0.0131 | +0.0090 | +0.0041 | ❌ False |

**overfit_risk 數量：2/6**（閾值為 4）→ `overfit_risk_detected = False`

**說明**：
- NC1（市場亂序）：Signal gap = +0.070，顯示真實市場機率分配有意義的結構
- NC2（模型亂序）：Signal gap = -0.052，真實市場對模型分配有依賴性
- NC3（random MMM）：信號微弱（gap=−0.003），顯示 model-market gap 自身信號弱 ⚠️
- NC4（random sp_fip bucket）：Signal gap = -0.047，sp_fip bucket 分析有實際信號
- NC5（random split）：Signal gap 微弱（+0.003）⚠️ — split 分配信號弱
- NC6（無關日期 bucket）：gap=+0.004，低於閾值 → 無 overfit（NC6 邏輯反向：大gap才是risk）

---

## 十、Gate 決策總結

### 摘要旗標

| 旗標 | 結果 |
|------|------|
| `market_dominance_stable` | ✅ True |
| `split_instability_detected` | ✅ False |
| `sp_fip_independent_signal` | ✅ False（sp_fip 已被市場吸收）|
| `overfit_risk_detected` | ✅ False（2/6 < 4）|
| `model_compressed` | ⚠️ True（compression_ratio=0.267）|
| `worth_phase72` | ✅ **True** |

### 🎯 GATE: `MARKET_DE_RISK_GUARD_PROMISING`

**Rationale**:
> Market is clearly superior in 0.65–0.70 band (Brier delta=+0.0140, CI stable and excludes zero, splits consistent). A paper-only market de-risk guard is worth proposing.

**Risk Notes**:
- Market Brier delta in target band = +0.0140, CI=[+0.0048, +0.0240] (stable, excludes zero)
- model_compressed=True：模型機率分佈極度壓縮（std=0.015 vs market=0.058），壓縮比 0.267，說明模型在此 band 缺乏鑑別力
- Rank correlation = 0.172：模型與市場排名判斷高度不一致，難以依靠模型排名進行套利
- NC3 (random_model_minus_market) 與 NC5 (random_split) 均顯示 overfit_risk=True

---

## 十一、Phase 72 建議

**Phase 72 可做 paper-only market de-risk guard proposal**：

調查在 0.65–0.70 band 以 market probability 替代 model probability 的 paper-only simulation，**仍不得 production patch**。

具體方向：
1. **Market De-risk Guard**：設計一個 rule-based 規則：當 model_home_prob ∈ [0.65, 0.70] 時，以 market_home_prob_no_vig 替代 model 預測
2. **Paper-only simulation**：模擬此替換在 2025 資料集上的 Brier score、Kelly 建議影響
3. **Validation**：仍需 Phase 72 bootstrapped backtest，minimum n=1500，split-by-split 穩定性確認

---

## 十二、Governance 確認

```
CANDIDATE_PATCH_CREATED        = False  ✅
PRODUCTION_MODIFIED            = False  ✅
ALPHA_MODIFIED                 = False  ✅
DIAGNOSTIC_ONLY                = True   ✅
PREDICTION_JSONL_OVERWRITTEN   = False  ✅
PIT_SAFE_VALIDATION            = True   ✅
ALPHA                          = 0.40   ✅ (FROZEN)
PHASE70_GATE_ANCHOR            = MARKET_ONLY_SUPERIOR (carried, read-only)
```

---

## 十三、相關檔案

- 完整結果 JSON：`reports/phase71_market_dominance_model_derisk_audit_20260507.json`
- Orchestrator：`orchestrator/phase71_market_dominance_model_derisk_audit.py`
- Runner：`scripts/run_phase71_market_dominance_model_derisk_audit.py`
- 測試套件：`tests/test_phase71_market_dominance_model_derisk_audit.py` (167 tests, all pass)

---

PHASE_71_MARKET_DOMINANCE_MODEL_DERISK_AUDIT_VERIFIED
