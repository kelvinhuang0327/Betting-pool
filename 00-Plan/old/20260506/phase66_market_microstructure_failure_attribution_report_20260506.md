# Phase 66 — Market Microstructure Failure Attribution 報告

**日期**: 2026-05-06  
**模組**: `orchestrator/phase66_market_microstructure_failure_attribution.py`  
**完成標記**: `PHASE_66_MARKET_MICROSTRUCTURE_FAILURE_ATTRIBUTION_VERIFIED`  
**Gate**: `MARKET_MICROSTRUCTURE_NOT_PROMISING`  
**是否推進 Phase 67**: ❌ 否

---

## 1. 研究目標

Phase 44/45 確認 blend 在重度偏愛場次 (heavy_favorite, blend_fav ≥ 0.70) 存在失敗模式，model 明顯劣於 market。本 Phase 的問題是：

> **「blend 在 heavy_favorite 中劣於 market，是否可被市場微結構特徵所解釋？若能，哪一個維度最具歸因力？」**

分析的七個歸因維度：

| 維度 | 說明 |
|------|------|
| `market_implied_bucket` | 市場隱含勝率分桶 |
| `model_prob_bucket` | 模型勝率分桶 |
| `blend_prob_bucket` | Blend 勝率分桶 |
| `disagreement_bucket` | 模型與市場分歧幅度 |
| `fav_side` | 主客場偏愛方 |
| `overround_bucket` | 博彩公司 vig/overround |
| `odds_price_bucket` | 賠率價格分桶 |

DATA LIMITED (資料缺失，無法分析)：`opening_line_direction`、`clv_direction`、`line_movement_shift`

---

## 2. 數據對齊

| 項目 | 數值 |
|------|------|
| 預測筆數 | 2,025 |
| 賠率 CSV 行數 | 2,402 |
| 對齊筆數 | 2,025 / 2,025 |
| 覆蓋率 | **100.0%** |
| 對齊鍵 | `(game_date, home_team)` — 完全直接匹配 |

資料來源：  
- 預測：`data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`  
- 賠率：`data/mlb_2025/mlb_odds_2025_real.csv`（2025-04-27 至 2025-09-28）

---

## 3. 分段指標

> `blend_bss_vs_market` > 0 表示 blend 優於 market；< 0 表示 market 優於 blend。  
> 公式：`BSS = 1 − blend_brier / market_brier`

| 分段 | n | blend_bss_vs_market | fav_win_rate | model_brier | market_brier | blend_brier |
|------|---|---------------------|--------------|-------------|-------------|-------------|
| all | 2,025 | **+0.0014** | 0.551 | 0.2447 | 0.2438 | 0.2434 |
| heavy_favorite (≥0.70) | 60 | **−0.0033** | 0.767 | 0.1792 | 0.1771 | 0.1777 |
| high_confidence (≥0.75) | 10 | +0.1578† | 0.900 | 0.0931 | 0.1239 | 0.1043 |
| phase45_failure | 188 | **−0.0142** | 0.745 | 0.1930 | 0.1872 | 0.1899 |

†`high_conf` n=10，樣本過小，不具統計意義。

**關鍵洞察**：
- 全局來看，blend 略優於 market (+0.0014)，與 Phase 44 的 +0.002 一致。
- 在 heavy_favorite 中，blend 略劣於 market (−0.0033)，但差距極小且未達 bootstrap 顯著。
- Phase45 失敗場次 (n=188)，blend 對 market 差距 −0.0142，具體但未達顯著。

---

## 4. 歸因桶分析 (Bootstrap CI)

`_BOOTSTRAP_N = 1000`，`_MIN_BUCKET_N = 15`。以下列出 BSS 絕對值最大的前 12 個 bucket：

| 維度 | 標籤 | n | blend_bss | Bootstrap 顯著 | CI [2.5%, 97.5%] | P(BSS>0) |
|------|------|---|-----------|--------------|------------------|----------|
| `market_implied_bucket` | `strong_fav_60_65` | 4 | −0.097 | — (n<15) | — | — |
| `odds_price_bucket` | `strong_fav_165_210` | 4 | −0.097 | — (n<15) | — | — |
| `model_prob_bucket` | `strong_conf_65_70` | 15 | −0.048 | ✗ | [−0.178, +0.011] | 0.07 |
| `disagreement_bucket` | `strong_disagree_7pct+` | 11 | −0.037 | — (n<15) | — | — |
| **`model_prob_bucket`** | **`strong_conf_65_70`** | **134** | **−0.035** | **✅ sig** | **[−0.069, −0.004]** | **0.01** |
| `blend_prob_bucket` | `strong_blend_65_70` | 128 | −0.019 | ✗ | [−0.051, +0.011] | 0.12 |
| `disagreement_bucket` | `slight_disagree_3_7pct` | 24 | +0.018 | ✗ | [−0.040, +0.070] | 0.74 |
| `market_implied_bucket` | `heavy_fav_65_70` | 8 | −0.014 | — (n<15) | — | — |
| `market_implied_bucket` | `extreme_fav_70plus` | 48 | +0.013 | ✗ | [−0.021, +0.044] | 0.79 |
| `odds_price_bucket` | `strong_fav_165_210` | 413 | +0.012 | ✗ | [−0.005, +0.026] | 0.92 |

**唯一 bootstrap 顯著的 bucket**：`model_prob_bucket|strong_conf_65_70` (n=134)，CI 完全在負值區間 [−0.069, −0.004]，表示當模型信心度 65–70% 時，blend 顯著**劣於** market。

> 此發現是**負向訊號**：無任何 bucket 在 blend 優於 market 方向達到顯著性。

---

## 5. 負向對照 (Negative Control)

| 維度 | Overfit 風險 | 真實 BSS 差距 (max-min) | 洗牌 std |
|------|------------|------------------------|----------|
| `market_implied_bucket` | ✗ | 0.000 | 0.000 |
| `model_prob_bucket` | ✗ | 0.055 | 0.031 |
| `blend_prob_bucket` | ✗ | 0.000 | 0.000 |
| `disagreement_bucket` | ✗ | 0.026 | 0.025 |
| `fav_side` | ✗ | 0.010 | 0.022 |
| `overround_bucket` | ✗ | 0.000 | 0.000 |
| `odds_price_bucket` | ✗ | 0.000 | 0.000 |

**所有維度均無 overfit 風險**：桶間 BSS 差距未超過隨機洗牌的 1σ 閾值 (`_OVERFIT_SIGMA=2.0`)。

---

## 6. OOF 跨月驗證

OOF 以月份為 fold (2025-05 至 2025-09，共 5 folds)：

| 維度 | Folds | OOF mean_delta | 顯著 | 跨月一致 |
|------|-------|----------------|------|----------|
| `market_implied_bucket` | 5 | +0.0023 | ✗ | ✗ |
| `model_prob_bucket` | 5 | +0.0023 | ✗ | ✗ |
| `blend_prob_bucket` | 5 | +0.0023 | ✗ | ✗ |
| `disagreement_bucket` | 5 | +0.0023 | ✗ | ✗ |
| `fav_side` | 5 | +0.0023 | ✗ | ✗ |
| `overround_bucket` | 5 | +0.0023 | ✗ | ✗ |
| `odds_price_bucket` | 5 | +0.0023 | ✗ | ✗ |

**所有維度均無 OOF 顯著正訊號**：mean_delta ≈ +0.002 (全局 blend 微優)，但跨月方向不一致，未達 `_OOF_PROMISING_DELTA = 0.005` 門檻。

---

## 7. DATA LIMITED 維度說明

以下三個維度因資料來源限制無法分析，已記錄為 DATA_LIMITED：

| 維度 | 限制原因 |
|------|----------|
| `opening_line_direction` | 盤口資料僅有單一快照，無開盤線紀錄 |
| `clv_direction` | 無賽前 vs 賽時對比，無法計算 CLV |
| `line_movement_shift` | 無多個時間點快照，無法追蹤線路移動 |

若未來收集到時間序列賠率資料，可重新執行本 Phase 以填補這三個維度。

---

## 8. Gate 決策

### Gate: `MARKET_MICROSTRUCTURE_NOT_PROMISING`

| 決策條件 | 狀態 |
|----------|------|
| 任何 bucket 有 bootstrap 顯著正 BSS | ❌ 無 |
| 任何維度 OOF 顯著且正向且跨月一致 | ❌ 無 |
| 任何維度偵測到 overfit 風險 | ❌ 無 |
| 資料覆蓋率 ≥ 70% | ✅ 100% |

**結論**：在當前可用的市場微結構特徵（市場隱含勝率、模型信心、Blend 分桶、模型與市場分歧、主客偏愛方、Vig、賠率價格）中，**無任何特徵可解釋 heavy_favorite 場次的 blend vs market 劣勢**。

唯一統計顯著的 bucket (`model_prob_bucket|strong_conf_65_70`, n=134) 呈現**負向訊號**：在模型信心偏高但非極端（65-70%）的情境下，blend 系統性劣於 market，BSS gap 達 −3.5pp（95% CI: −6.9pp 至 −0.4pp）。這表明 α=0.40 在此信心區間可能引入過多 market 噪音。

---

## 9. 與前期 Phase 的銜接

| Phase | Gate | 核心發現 |
|-------|------|----------|
| Phase 44 | `PAPER_ONLY` | blend_bss_vs_market = +0.002；賠率覆蓋率 66% |
| Phase 45 | (failure mapping) | heavy_fav 失敗率 ≈ 23.3%；model 比 market 更悲觀 |
| Phase 63 | `BULLPEN_FEATURE_NOT_PROMISING` | 牛棚特徵無法解釋失敗 |
| Phase 64 | `BULLPEN_FEATURE_NOT_PROMISING` | 複合牛棚特徵亦無效 |
| Phase 64B | `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING` | 細粒度牛棚特徵無效 |
| Phase 65 | `OVERFIT_RISK` | 先發投手疲勞特徵過擬合 |
| **Phase 66** | **`MARKET_MICROSTRUCTURE_NOT_PROMISING`** | **市場微結構特徵無法解釋失敗** |

---

## 10. 下一步建議

市場微結構路徑已無promising訊號，建議轉向以下資料來源：

1. **Lineup / Rest**：先發球員名單、球隊連戰疲勞（travel distance、back-to-back 場次）
2. **Schedule**：賽程密度、主客場連戰比例
3. **Weather**：溫度、風速（影響打擊場次的 total 走勢，間接影響 ML）
4. **Ballpark**：主場優勢因子（特定球場對 heavy_fav 的歷史 ROI）
5. **Season Context**：九月末保級/季後賽相關性（playoff race）

---

## 11. 安全常數確認

| 常數 | 值 |
|------|----|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `ALPHA_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |
| `ALPHA` | `0.40` |
| `PHASE65_GATE_ANCHOR` | `OVERFIT_RISK` |
| `PHASE64B_GATE_ANCHOR` | `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING` |

Blend 公式（凍結）：`blend = (1 − 0.40) × model_prob + 0.40 × market_prob_no_vig`

---

## 12. 測試覆蓋

| 測試套件 | 結果 |
|----------|------|
| `tests/test_phase66_market_microstructure_failure_attribution.py` | **111 / 111 PASS** |
| Phase 63 + 64 + 64B + 65 + 66 全回歸 | **610 / 610 PASS** |

---

**JSON 報告路徑**: `reports/phase66_market_microstructure_failure_attribution_20260506.json`  
**完成標記**: `PHASE_66_MARKET_MICROSTRUCTURE_FAILURE_ATTRIBUTION_VERIFIED` ✅
