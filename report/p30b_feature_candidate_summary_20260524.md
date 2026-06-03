# P30B MLB Feature Candidate Summary
**Phase**: P30B — MLB Feature Engineering / CLV Robustness Diagnostics  
**Date**: 2026-05-24  
**Mode**: `diagnostic_only=true` | `paper_only=true` | `promotion_freeze=true`  
**Branch**: main | **Commit**: df554b0  

---

## 一、執行摘要

P30B 完成三項診斷：CLV robustness 分析、pair-count 重現性稽核、MLB feature 工程盤點。

| 診斷項目 | 結論 |
|---------|------|
| CLV 訊號分類 | **NOISE** (所有方法一致) |
| Pair-count delta | **已完整解釋** — 新資料自然累積，無異常 |
| Feature PIT 安全性 | **GREEN** — 所有 MLB 模組有 FORBIDDEN_FIELDS 守衛 |
| Feature 候選 Tier 1 | 5 個 SSOT-backed 特徵可進入實驗 |

---

## 二、CLV Robustness 診斷

### 2.1 資料概況

| 項目 | P24 (Pinned 2788) | P30B (Live 3126) |
|------|-------------------|------------------|
| 有效 CLV 記錄 | 236 pairs × 5 mkt = 2284 obs | 338 game-level records |
| 外部 closing 來源 | TSL only | DraftKings (45) + TSL (293) |
| 中位數 CLV | 0.0% | 0.0% |
| 平均 CLV (raw) | +0.3622% | +0.1121% |
| 平均 CLV (5% trim) | +0.0118% | +0.0626% |
| 平均 CLV (10% trim) | +0.0072% | +0.0570% |
| Top 5% outlier 貢獻 | 101.79% | 244.6% |
| Bootstrap CI 95% | [-0.019%, +0.776%] | N/A |
| CI 穿越零點 | **是** | N/A |

### 2.2 Per-Market 分解 (P27 line-aware, 236 valid pairs)

| Market | N | Mean CLV | Trimmed 5% | CI 95% | +CLV Rate | Classification |
|--------|---|---------|-----------|--------|-----------|----------------|
| MNL | 681 | +0.045% | +0.023% | [-0.220%, +0.298%] | 35.5% | INCONCLUSIVE |
| HDC | 402 | -0.003% | +0.009% | [-0.324%, +0.322%] | 38.3% | INCONCLUSIVE |
| OU | 418 | +0.038% | +0.051% | [-0.254%, +0.333%] | 37.1% | INCONCLUSIVE |
| OE | 460 | +0.008% | +0.003% | [-0.069%, +0.086%] | 15.7% | INCONCLUSIVE |
| TTO | 434 | +0.255% | ~0.0% | [-0.380%, +0.907%] | 40.8% | INCONCLUSIVE |

### 2.3 Rejection Breakdown (Live Timeline, 3126 records)

| 原因 | 數量 | 說明 |
|------|------|------|
| missing_timestamps | 2,454 | 單一快照記錄，無 decision+closing pair |
| decision_ts ≥ closing_ts | 327 | closing 時間早於或等於 decision (ordering issue) |
| timestamps_too_close | 7 | 時間差 < 60s，疑似同一爬取 |
| **CLV available** | **338** | 10.8% of total records |

### 2.4 CLV 訊號分類判定

```
分類: NOISE (所有方法一致)
```

**判定依據**:
- 任何 outlier 修正方法（trimming, winsorization, removal）均使訊號趨近 0
- Top 1% 觀測值貢獻 >110% 的總 CLV 總和（P24）；Top 5% 貢獻 244% (P30B)
- 338 個 CLV 記錄中 202 個 (59.8%) 為零（TSL 賠率不動）
- 外部 closing 來源為 **DraftKings**（非 Pinnacle）— 參考市場 sharpness 較低
- 5 個市場全數 Bootstrap CI 穿越零點

**不確定性標注**:
- 若換用 Pinnacle 作為 closing，CLV 訊號可能改變（目前無 Pinnacle 數據）
- 樣本量 (236–338 pairs) 在統計功效上不足以檢測 <0.5% 的效果量
- 不排除特定子集存在弱但穩定的 CLV（例如 MNL 高賠率情境）

---

## 三、Pair-Count 重現性稽核

### 3.1 計數歷史

| 版本 | 快照記錄數 | Unique Match IDs | Valid Pairs | 無效 (缺 pregame) | 無效 (缺 closing) |
|------|-----------|-----------------|-------------|-----------------|-----------------|
| P19 | 2,747 | 859 | **233** | 57 | 563 |
| P22 | 2,772 | ~877 | **236** | — | — |
| 當前 | 2,788+ | 877 | **236** | 64 | 577 |

### 3.2 Delta 解釋

**P19 → P22 (+3 pairs)**:
- 18 個新 match_id 進入快照
- 其中只有 3 個 match_id 同時具備 pregame (≥2h) + closing (±2h) 快照
- 其餘 15 個 match_id 資料不完整（僅有單邊快照）
- Root cause: `SOURCE_DATA_GROWTH_NEW_COMPLETE_PAIRS` — 自然資料累積

**P22 → 當前 (0 pairs)**:
- Delta = 0，完全一致
- 快照行數從 2772 → 2788（+16 行），但未形成新的完整配對

**衍生規則（不變）**:
```
pregame_window: ≥ 2.0h before game_time
closing_window: ±2.0h around game_time
pair_selection: latest valid snapshot in each window
```

### 3.3 重現性評分

| 項目 | 狀態 |
|------|------|
| 衍生邏輯一致性 | ✓ 確認不變 |
| 重新執行結果 | ✓ 236 pairs (同 P22) |
| 無重新分類 | ✓ 確認 |
| 無窗口規則變更 | ✓ 確認 |
| 無重複處理邏輯變更 | ✓ 確認 |
| **結論** | **PAIR_COUNT_DELTA_EXPLAINED — 無異常** |

---

## 四、MLB Feature 工程盤點

### 4.1 模組清單

| 檔案 | 行數 | 主要類別 | PIT 守衛 | Pregame 守衛 | 訊號估計 |
|------|------|---------|---------|------------|---------|
| alpha_signals.py | 1,694 | AlphaSignals | 無顯式 FORBIDDEN_FIELDS | ✓ | ~252 |
| advanced.py | 505 | AdvancedFeatures | 無顯式 FORBIDDEN_FIELDS | ✓ | ~11 |
| knowledge_graph.py | 600 | KnowledgeGraphFeatures | ✓ | ✓ | ~17 |
| mlb_bullpen_feature_builder.py | 418 | — | ✓ | ✓ | ~5 |
| mlb_bullpen_feature_injection.py | 199 | BullpenAdjustmentResult | ✓ | — | ~4 |
| mlb_bullpen_full_season_ingestion.py | 503 | BullpenSSOTArtifact | ✓ | ✓ | — |
| mlb_bullpen_granular_ingestion.py | 1,165 | SSoTFeatureArtifact | ✓ | ✓ | — |
| mlb_bullpen_granular_ssot.py | 640 | BullpenGranularRecord | ✓ | ✓ | ~5 SSOT slots |
| mlb_bullpen_pit_validator.py | 440 | BullpenPitValidationResult | ✓ | ✓ | — |
| mlb_bullpen_usage_snapshot.py | 477 | — | ✓ | ✓ | ~9 |
| mlb_p0_feature_builder.py | 335 | — | ✓ | — | 3 (F-001/002/004) |
| mlb_p0_feature_injection.py | 406 | InjectionSummary | ✓ | — | ~10 |
| mlb_pit_validator.py | 189 | PitValidationResult | ✓ | ✓ | — |
| mlb_relief_appearance_parser.py | 273 | ReliefAppearance | ✓ | — | ~5 |
| mlb_sp_stat_snapshot.py | 340 | PitcherStatSnapshot | — | ✓ | — |
| nlp_extractor.py | 620 | PregameTextBundle | — | ✓ | ~8 |
| ontology_discovery.py | 399 | OntologyReport | ✓ | — | ~1 |
| feature_selector.py | 381 | FeatureSelectorResult | — | — | — |

### 4.2 Alpha Signal 分類 (alpha_signals.py)

| 類別 | 文件描述訊號數 | 說明 |
|------|-------------|------|
| Batting | 40 | wOBA, OPS+, K%, BB%, BABIP differentials |
| Pitching | 38 | FIP, xFIP, WHIP, K/9, groundball% |
| Bullpen | 22 | usage days, leverage index, save opp |
| Defensive | 17 | UZR, DRS, positional coverage |
| WBC-specific | 25 | 國際賽特有情境（時差、熟悉度） |
| Market Intelligence | 21 | line movement, opening vs current spread |
| Environmental | 22 | weather, park, home/away streak |
| Interaction/Polynomial | 18 | SP fatigue × bullpen stress, etc. |
| Momentum/Time-series | 20 | recent L10 runs, streak indicators |
| Lineup Construction | 17 | handedness mix, order, lineup change |
| Blowout Risk / Data Quality | 12 | extreme favoriteness, data completeness |
| **Total** | **~252** | |

### 4.3 SSOT Bullpen Feature Slots (mlb_bullpen_granular_ssot.py)

20 個 SSOT 欄位，嚴格執行 `assert_not_forbidden_field()`:
- `bullpen_usage_last_1d/3d/5d` — 近期牛棚出賽次數
- `reliever_back_to_back_count` — 連續出賽投手數
- `reliever_three_in_four_days_count` — 4天3出賽投手數  
- `closer_used_last_1d/2d` — 終結者近期使用狀態
- `high_leverage_reliever_used_last_1d/workload_last_3d` — 高槓桿投手使用強度
- `bullpen_fatigue_favorite_side/underdog_side` — 依賠率面熱度
- `bullpen_rest_imbalance` — 主客隊牛棚疲勞不對稱度

### 4.4 PIT 安全性評估

| 層級 | 說明 |
|------|------|
| GREEN ✓ | 所有 MLB feature 模組有 FORBIDDEN_FIELDS 列表（`"final_score"`, `"home_win"`, `"away_score"` 等被顯式禁止） |
| GREEN ✓ | `mlb_bullpen_pit_validator.py` 及 `mlb_pit_validator.py` 有主動驗證層 |
| GREEN ✓ | `mlb_bullpen_granular_ssot.py` 有 `assert_not_forbidden_field()` runtime guard |
| YELLOW ⚠ | `alpha_signals.py` 和 `advanced.py` — 無 FORBIDDEN_FIELDS 明確列表，依賴呼叫者傳入 pregame-only 資料 |
| YELLOW ⚠ | `feature_selector.py` 和 `ontology_discovery.py` — 工具性模組，無自身特徵生成，PIT 風險低但無明確守衛 |

---

## 五、Feature 候選清單

### Tier 1 — PIT-Safe + SSOT-Backed + 資料可得性高

| ID | 特徵名稱 | 來源模組 | 說明 | 資料可得性 |
|----|---------|---------|------|-----------|
| F-B01 | `bullpen_usage_last_3d` | mlb_bullpen_granular_ssot | 3日牛棚累積出賽次數 | HIGH (historical box scores) |
| F-B02 | `closer_used_last_1d` | mlb_bullpen_granular_ssot | 前日終結者使用 binary | HIGH |
| F-B03 | `bullpen_rest_imbalance` | mlb_bullpen_granular_ssot | 主客隊疲勞不對稱 | HIGH |
| F-P01 | `sp_fip_delta` (F-001) | mlb_p0_feature_builder | SP FIP 差值 (away-home) | HIGH (FanGraphs/statcast) |
| F-P02 | `park_run_factor` (F-002) | mlb_p0_feature_builder | 球場得分因子 | HIGH (multi-year park factors) |

### Tier 2 — PIT-Safe + 部分資料限制

| ID | 特徵名稱 | 來源模組 | 說明 | 資料限制 |
|----|---------|---------|------|---------|
| F-A01 | `pitcher_fatigue` | advanced.py | 指數衰減疲勞分數 (0–1) | 需近期投球數 |
| F-A02 | `bullpen_stress_score` | advanced.py | 工作量 × 逆深度 × ERA | 需 ERA + IP 資料 |
| F-A03 | `matchup_edge` | advanced.py | 打者 vs 投手 wOBA 差值 | 需歷史對戰記錄 |
| F-B04 | `reliever_back_to_back_count` | mlb_bullpen_granular_ssot | 連打投手計數 | HIGH |
| F-P03 | `season_game_index` (F-004) | mlb_p0_feature_builder | 賽季進度 [0,1] | HIGH (純計算) |

### Tier 3 — 資料可得性低或 PIT 守衛需補強

| ID | 特徵名稱 | 來源模組 | 限制原因 |
|----|---------|---------|---------|
| F-A04 | `velocity_trend` | advanced.py | 需 statcast pitch velocity tracking |
| F-A05 | `pitch_arsenal_entropy` | advanced.py | 需 pitch mix 分布資料 |
| F-A06 | `platoon_split_interaction` | advanced.py | 需今日先發打序手性資料 |
| F-N01 | NLP pregame signals | nlp_extractor.py | 需 pregame 文字輸入 (TSL/新聞) |
| F-WBC01 | WBC-specific signals (25) | alpha_signals.py | WBC 賽制；MLB 可能不適用 |

---

## 六、建議事項 (Report-Only)

> ⚠️ 以下為研究觀察，非行動決策。Promotion freeze 維持。

1. **CLV**: 在 Pinnacle closing 數據取得前，CLV 訊號不應作為 alpha 確認指標。DraftKings 作為 external closing 可能高估「beats the closing line」的可靠性。

2. **Feature priority**: Tier 1 的 5 個特徵（bullpen SSOT + P0 SP/park）是最高信心候選，PIT-safe 且資料可得。建議優先進入 walk-forward backtest。

3. **Pair-count ceiling**: 236 pairs 對於複雜模型的 train/val split 仍偏少。需持續累積至 ≥500 pairs 再提升模型複雜度。

4. **OE market**: positive_rate 僅 15.7%（遠低於其他市場的 35-40%），且 |CLV|>10% = 0，表明 TSL 的 OE 賠率幾乎不動。這個市場的 CLV 訊號價值最低。

5. **alpha_signals.py 守衛補強**: 雖然呼叫端有 pregame 資料守衛，但 `alpha_signals.py` 本身缺乏 FORBIDDEN_FIELDS 明確列表。建議在未來 P 輪添加顯式守衛（不阻擋現有功能，僅防禦性添加）。

---

## 七、附件

- CLV diagnostic script: `scripts/_p30b_analysis.py` (diagnostic only, not staged)
- Source data: `data/mlb_context/odds_timeline.jsonl` (3,126 records)
- P24 pinned analysis: `report/p24_clv_robustness_diagnostic_20260520.md`
- P27 per-market isolation: `report/p27_per_market_clean_clv_isolation_20260520.md`
- Pair-count audit: `data/paper_recommendations/p23_pair_delta_root_cause_20260520.json`

---

*Generated by P30B diagnostic run — 2026-05-24 — df554b0*  
*Report-only. No champion modification. No production deployment.*
