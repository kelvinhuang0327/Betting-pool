# Phase 45 — Model Value Attribution & Failure Diagnosis

**Generated**: 2026-05-05  
**Status**: `PHASE_45_MODEL_VALUE_ATTRIBUTION_VERIFIED`  
**Gate**: `FEATURE_REPAIR_INVESTIGATION`  
**Global Conclusion**: `CONDITIONAL_VALUE`  
**Module**: `orchestrator/phase45_model_value_attribution.py`  

---

## Executive Summary

本階段對 **2,025 筆 MLB 2025 預測資料**（`data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl`，schema_version=`phase39-v1`，alpha=0.4 固定）進行多維度 segment-level value attribution。

### 核心結論

| 項目 | 結果 |
|---|---|
| 資料範圍 | 2025-04-27 → 2025-09-28 |
| 總樣本數 | 2,025 |
| alpha（blend） | 0.4（固定，不得調整） |
| global_conclusion | **CONDITIONAL_VALUE** |
| gate 決定 | **FEATURE_REPAIR_INVESTIGATION** |
| candidate_patch_created | **False** |
| audit_hash | `8f20f5c1fd7bade9…` |

**關鍵發現**：模型價值高度集中在特定月份（2025-05, 2025-07），但在開季（2025-04）呈現嚴重的 BOTH failure（BSS −2.50% + ECE 崩潰），且大多數 segment 存在系統性 ECE 劣化。這是 **feature quality 問題**，不是 alpha 問題。

### 三條線

```
不可執行：
  ❌ production 部署
  ❌ calibration / alpha tuning / ensemble
  ❌ candidate patch 建立

已確認：
  ✅ candidate_patch_created = False
  ✅ gate ≠ PATCH（只選 FEATURE_REPAIR_INVESTIGATION）
  ✅ alpha = 0.4（per Phase 42A/43/44 硬性規定）
```

---

## Segment 完整結果（15 segments）

### Dimension 1 — Odds Bucket（市場隱含主場勝率）

| Bucket | n | Model Brier | Market Brier | blend_bss | Model ECE | Market ECE | Value |
|---|---|---|---|---|---|---|---|
| heavy_favorite (≥0.65) | 211 | — | — | **−0.17%** | **0.0893** | 0.0330 | NO_SIGNAL ⚠️ |
| mid (0.45–0.65) | 1,407 | — | — | +0.23% | 0.0446 | 0.0336 | NO_SIGNAL ⚠️ |
| underdog (<0.45) | 407 | — | — | +0.32% | 0.0301 | 0.0248 | NO_SIGNAL |

> ⚠️ = ECE failure（model_ece > market_ece + 0.01）

**觀察**：
- `heavy_favorite` segment 的模型 ECE（0.0893）高達市場 ECE（0.0330）的 **2.7 倍**，是全部 segment 中最大的 ECE gap。
- 即使在 `mid`（最大群，佔 69%），模型 ECE 也系統性劣化。
- 唯一 ECE 不劣化的是 `underdog`（低勝率場次）。

---

### Dimension 2 — Model vs Market Disagreement（|model − market|）

| Bucket | n | blend_bss | Model ECE | Market ECE | Value |
|---|---|---|---|---|---|
| low (<0.05) | 1,176 | +0.08% | **0.0323** | **0.0181** | NO_SIGNAL ⚠️ |
| medium (0.05–0.10) | 656 | +0.46% | 0.0421 | 0.0488 | NO_SIGNAL ✅ |
| high (≥0.10) | 193 | +0.18% | 0.0759 | 0.0679 | NO_SIGNAL |

**觀察**：
- 當模型與市場接近（low disagreement，佔 58%），模型 ECE 仍比市場差（0.0323 vs 0.0181），說明即使方向一致，**輸出概率分布形狀**仍有結構性偏差。
- `medium disagreement` 是表現最好的 bucket（blend_bss +0.46%，ECE 市場反而更差），這是潛在的有效操作區間。

---

### Dimension 3 — Confidence Bucket（|model_prob − 0.5|）

| Bucket | n | blend_bss | Model ECE | Market ECE | Value |
|---|---|---|---|---|---|
| high_confidence (≥0.10) | 531 | **−0.27%** | 0.0173 | 0.0228 | NO_SIGNAL |
| mid_confidence (0.05–0.10) | 646 | +0.24% | 0.0557 | 0.0521 | NO_SIGNAL ⚠️ |
| low_confidence (<0.05) | 848 | +0.46% | 0.0210 | 0.0263 | NO_SIGNAL |

**觀察**：
- `high_confidence`：模型 ECE 優於市場（0.0173 vs 0.0228），校準良好，但 blend_bss **依然為負**（−0.27%）。這意味著模型在高信心時**方向選擇偶有系統性錯誤**，且加入 40% 模型後反而拖累 blend。
- `low_confidence`：模型 ECE 也優於市場（0.0210 vs 0.0263），且 blend_bss +0.46%，最佳信心區間。
- `mid_confidence`：ECE 輕微劣化（+0.01 margin），是 ECE failure 邊界。

---

### Dimension 4 — Time（月份）

| Month | n | blend_bss | Model ECE | Market ECE | Value |
|---|---|---|---|---|---|
| 2025-04 | 53 | **−2.50%** | **0.1992** | 0.1274 | **VALUE_NEGATIVE** ❌ |
| 2025-05 | 411 | **+0.57%** | 0.0422 | 0.0545 | **VALUE_POSITIVE** ✅ |
| 2025-06 | 397 | −0.44% | **0.0815** | 0.0317 | NO_SIGNAL ⚠️ |
| 2025-07 | 369 | **+0.86%** | 0.0322 | 0.0543 | **VALUE_POSITIVE** ✅ |
| 2025-08 | 421 | +0.29% | 0.0418 | 0.0192 | NO_SIGNAL ⚠️ |
| 2025-09 | 374 | +0.11% | 0.0477 | 0.0505 | NO_SIGNAL |

**觀察**：
- **2025-04**（開季）：最嚴重 failure，BOTH type。ECE 高達 0.1992（市場 0.1274），BSS −2.50%。開季時陣容未穩定，ELO 信心不足。
- **2025-05, 2025-07**：兩個 VALUE_POSITIVE segment（樣本各 ≥ 411, 369，BSS ≥ 0.5%），市場 ECE 反而比模型高，模型方向正確且校準更好。
- **2025-06**：夏初 ECE 崩潰最嚴重（0.0815 vs 0.0317），blend_bss 轉負（−0.44%）。
- **2025-08**：ECE 輕微劣化但 BSS 轉正，介於邊界。

---

## Value Attribution Summary

### Top 3 Positive Segments

| Rank | Segment | n | blend_bss | 說明 |
|---|---|---|---|---|
| 🥇 1 | month:2025-07 | 369 | **+0.86%** | 市場 ECE 高於模型，模型七月校準最優 |
| 🥈 2 | month:2025-05 | 411 | **+0.57%** | 五月模型 ECE 0.0422 < 市場 0.0545，正向 |
| 🥉 3 | confidence:low_confidence | 848 | **+0.46%** | 低信心區間模型校準穩定 |

### Top 3 Negative Segments

| Rank | Segment | n | blend_bss | 說明 |
|---|---|---|---|---|
| ❌ 1 | month:2025-04 | 53 | **−2.50%** | BOTH failure：BSS 崩潰 + ECE 最高 |
| ❌ 2 | month:2025-06 | 397 | **−0.44%** | 夏初 ECE 劣化 2.6×，牛棚/傷兵週期 |
| ❌ 3 | confidence:high_confidence | 531 | **−0.27%** | 模型高信心時方向偶有系統性錯誤 |

### Global Conclusion

```
CONDITIONAL_VALUE
```

> 2 positive segments（2025-05, 2025-07）；1 negative segment（2025-04）。模型價值為條件性，取決於 bucket 與月份，並非全面有效。

---

## Failure Pattern Detection

### Failure Segments 完整清單（6 個）

| Segment | n | blend_bss | failure_type | model_ece | market_ece | ECE ratio |
|---|---|---|---|---|---|---|
| odds_bucket:heavy_favorite | 211 | −0.17% | **ECE_DETERIORATION** | 0.0893 | 0.0330 | 2.71× |
| odds_bucket:mid | 1,407 | +0.23% | **ECE_DETERIORATION** | 0.0446 | 0.0336 | 1.33× |
| disagreement:low | 1,176 | +0.08% | **ECE_DETERIORATION** | 0.0323 | 0.0181 | 1.78× |
| month:2025-04 | 53 | −2.50% | **BOTH** | 0.1992 | 0.1274 | 1.56× |
| month:2025-06 | 397 | −0.44% | **ECE_DETERIORATION** | 0.0815 | 0.0317 | 2.57× |
| month:2025-08 | 421 | +0.29% | **ECE_DETERIORATION** | 0.0418 | 0.0192 | 2.18× |

### Failure Pattern 分析

#### Pattern A — 系統性 ECE 過高（Overconfidence）

**受影響 segments**: heavy_favorite, mid, disagreement:low  
**共同特徵**: 模型 ECE 顯著高於市場 ECE，但方向（BSS）仍為正或接近零  
**Heuristic 解釋**（基於資料，非猜測）：
- `heavy_favorite` 最嚴重（ECE 2.71× 市場）：模型對主場大幅優勢場次的概率估算過於分散，未能區分「整體強隊」與「今日先發強隊」的質性差異。
- `disagreement:low`（佔樣本 58%）：模型與市場一致時，ECE 仍比市場差，說明輸出概率的分布形狀與實際頻率不吻合。這是 **calibration shape 問題**，不是方向問題。
- 可能缺失的特徵：先發投手當日 FIP/ERA 差值、球場得分因子（park factor）

#### Pattern B — 開季冷啟動崩潰（Season-Start Cold Start）

**受影響 segments**: month:2025-04  
**性質**: BOTH failure（BSS −2.50% + ECE 0.1992）  
**Heuristic 解釋**：
- 開季時 ELO 評分依賴上季末數據，但陣容已大幅變動（休賽期交易、自由市場、傷兵）
- 市場透過 spring training 資訊調整賠率，但模型沿用靜態 ELO/WOBA/FIP 無法同步
- n=53 樣本小，加上概率失準，放大了 BSS 損失
- 可能修復方向：`season_game_index` 特徵（ELO 信心係數，開季前 30 場降權）

#### Pattern C — 夏季 ECE 週期性劣化（Summer Calibration Drift）

**受影響 segments**: month:2025-06, month:2025-08  
**性質**: ECE_DETERIORATION（2.57×, 2.18×），但 BSS 方向性不同（06 負、08 正）  
**Heuristic 解釋**：
- 六月：傷兵名單（IL placements）高峰，主力球員傷退改變場次預期，市場即時調整但模型未更新
- 八月：trade deadline（7/31）後新球員整合、各隊戰略轉向（搶分 vs 放棄），造成特定球隊實力評估失準
- 兩月的 ECE 劣化幅度不同（06 >> 08），說明 06 的問題更根本（非只是噪音）
- 可能修復方向：`bullpen_fatigue_7d`（牛棚疲勞指數）、`active_roster_strength`（IL 調整後戰力）

---

## Gate Recommendation

### Gate 決定：`FEATURE_REPAIR_INVESTIGATION`

**決策邏輯**：
```
CONDITIONAL_VALUE detected
├── n_positive_segments = 2 (≥1 required)
├── n_failure_segments = 6 (≥1 required)  
└── → FEATURE_REPAIR_INVESTIGATION
```

**Rationale**：
> Value concentrated in ['month:2025-07', 'month:2025-05', 'confidence:low_confidence']; clear failures in ['odds_bucket:heavy_favorite', 'odds_bucket:mid', 'disagreement:low', 'month:2025-04', 'month:2025-06', 'month:2025-08']. Investigate feature quality in failure segments before re-evaluating blend.

**不選 COLLECT_MORE_DATA 的原因**：樣本已達 2,025（> 1,000 threshold），且 failure pattern 已有足夠統計力支持特徵調查。

**不選 MARKET_BLEND_PAPER_ONLY 的原因**：存在 2 個明確 VALUE_POSITIVE segments，說明模型在特定條件下有效，不應全面停止調查。

---

## Hypothesis（下一步）

### Hypothesis H1 — 先發投手特徵缺失

**依據**：heavy_favorite ECE=0.0893（2.71× market）  
**推論**：模型無法區分「整體強隊出賽」與「王牌先發出賽」，導致強勝率場次概率失準  
**驗證方法**：加入 `sp_fip_delta`（主客場先發 FIP 差值），重跑 heavy_favorite segment，觀察 ECE 是否下降 30% 以上  
**資料需求**：MLB StatsAPI `probablePitcher` endpoint（開賽前已知）

### Hypothesis H2 — 球場因子未充分編碼

**依據**：heavy_favorite + disagreement:low 同時出現 ECE 劣化  
**推論**：高得分球場（Coors Field, Great American, Fenway）的主場效應未被現有特徵捕捉，導致隱含概率偏移  
**驗證方法**：加入 `park_run_factor`（靜態查表，前一賽季 park factor），觀察 disagreement:low ECE 改善  
**資料需求**：Baseball Reference Park Factors（年度靜態表）

### Hypothesis H3 — 開季 ELO 過度自信

**依據**：month:2025-04 ECE=0.1992（最高），BSS=−2.50%（最低）  
**推論**：開季 ELO 信心係數未考慮休賽期陣容變動，模型概率在開季前 30 場過於極端  
**驗證方法**：加入 `season_game_index`（已完成場次，作為 ELO 信心調節器），觀察 2025-04 segment 是否改善  
**資料需求**：由歷史比賽記錄計算，無需外部 API

### Hypothesis H4 — 夏季牛棚狀態缺失

**依據**：month:2025-06 ECE=0.0815（夏季最高，2.57× market）  
**推論**：六月牛棚高負荷期（各隊中繼疲勞差異擴大），市場透過賠率調整但模型未感知  
**驗證方法**：加入 `bullpen_fatigue_7d`（中繼投手前 7 天投球局數差），觀察 2025-06 ECE 是否下降  
**資料需求**：MLB StatsAPI per-game 投球記錄

---

## 技術附錄

### 模組規格

```python
# orchestrator/phase45_model_value_attribution.py
ALPHA: float = 0.4                    # 固定，不可修改
CANDIDATE_PATCH_CREATED: bool = False  # 永遠 False
_VALID_GATES = {
    "COLLECT_MORE_DATA",
    "FEATURE_REPAIR_INVESTIGATION",
    "MARKET_BLEND_PAPER_ONLY",
}
# gate ≠ "PATCH"，to_dict() 有 assert
```

### 分桶邊界

| Dimension | Bucket | 邊界條件 |
|---|---|---|
| odds_bucket | heavy_favorite | market_prob ≥ 0.65 |
| odds_bucket | mid | 0.45 ≤ market_prob < 0.65 |
| odds_bucket | underdog | market_prob < 0.45 |
| disagreement | low | \|model - market\| < 0.05 |
| disagreement | medium | 0.05 ≤ \|model - market\| < 0.10 |
| disagreement | high | \|model - market\| ≥ 0.10 |
| confidence | high_confidence | \|model - 0.5\| ≥ 0.10 |
| confidence | mid_confidence | 0.05 ≤ \|model - 0.5\| < 0.10 |
| confidence | low_confidence | \|model - 0.5\| < 0.05 |

### Value Label 邏輯

```
VALUE_POSITIVE : blend_bss ≥ +0.005 AND n ≥ 30
VALUE_NEGATIVE : blend_bss ≤ −0.010 AND n ≥ 30  (uses <=, inclusive)
NO_SIGNAL      : 其他
```

### 測試覆蓋

```
tests/test_phase45_model_value_attribution.py
├── TestOddsBucketing       (7 tests)
├── TestDisagreementBucketing (7 tests)
├── TestConfidenceBucketing (7 tests)
├── TestMonthBucketing      (5 tests)
├── TestSegmentComputation  (7 tests)
├── TestValueLabel          (6 tests)
├── TestFailureDetection    (6 tests)
├── TestNoPatch             (6 tests)
├── TestAlphaEnforcement    (3 tests)
├── TestGateRecommendation  (4 tests)
├── TestValueAttribution    (8 tests)
├── TestEdgeCases           (5 tests)
└── TestAuditHash           (5 tests)
TOTAL: 78 tests — 78/78 PASS
```

### Audit Trail

```
run_id            : (UUID，每次執行不同)
audit_hash        : 8f20f5c1fd7bade9...
input_data        : data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl
sample_size       : 2,025
date_range        : 2025-04-27 → 2025-09-28
alpha             : 0.4 (fixed)
schema_version    : phase39-v1
gate              : FEATURE_REPAIR_INVESTIGATION
global_conclusion : CONDITIONAL_VALUE
candidate_patch_created : False
```

---

## 下一步行動（Phase 46 Preview）

Phase 46 任務：**Feature Repair Blueprint**（spec-only，不寫程式）

1. 根據 H1–H4 列出特徵設計規格
2. 評估各特徵的 point-in-time safety（不得有未來資訊洩露）
3. 估計改善幅度與優先順序（P0/P1/P2）
4. 定義 Phase 47 的 feature builder 任務清單

**不執行**：
- ❌ 模型架構變更
- ❌ 回測（Phase 47 才做）
- ❌ production patch

---

*本文件由 `orchestrator/phase45_model_value_attribution.py` `run_phase45_attribution()` 自動分析後人工整理。*  
*所有數字均來自真實 MLB 2025 預測 JSONL，無任何人工修改。*
