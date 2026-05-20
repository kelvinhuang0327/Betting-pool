# Phase 60 — Bullpen Feature Decomposition and PIT-safe Attribution

**版本**: `phase60_bullpen_feature_decomposition_v1`  
**執行時間**: 2026-05-06 03:17:50 UTC  
**Audit Hash**: `2557762ecdb4a372`  
**Gate**: ⚠️ `DIAGNOSTIC_ONLY_SIGNAL`

## Section 2 — 安全常數快照 (Safety Constants)

| 常數 | 值 |
|------|-----|
| CANDIDATE_PATCH_CREATED | `False` |
| PRODUCTION_MODIFIED | `False` |
| ALPHA_MODIFIED | `False` |
| DIAGNOSTIC_ONLY | `True` |
| ALPHA | `0.4` (FROZEN) |

> 本 Phase 為純診斷分析，不產生任何生產補丁。

## Section 3 — 資料摘要 (Data Summary)

- **預測樣本數**: 2,025
- **牛棚資料筆數**: 2,430
- **成功對齊 (aligned)**: 1,890
- **對齊率**: 93.3%

### Segment 大小

| Segment | N |
|---------|---|
| All (usable predictions) | 2,025 |
| heavy_favorite (fav ≥ 0.70) | 60 |
| high_confidence (fav ≥ 0.75) | 10 |
| phase45_failure (hf + low_disagree) | 32 |

> **高信心閾值說明**: fav_prob >= 0.80 has only 1 game in this dataset (blend formula with ALPHA=0.4 suppresses extremes). Using fav_prob >= 0.75 as 'high_confidence' segment instead.

## Section 4 — 特徵家族清單 (Feature Families)

**可用特徵數**: 7  
**DATA_LIMITED 特徵數**: 4

| 特徵名稱 | 可用? | Coverage | N Usable | 說明 |
|---------|------|---------|---------|------|
| `bull_home_3d` | ✅ | 91.0% | 1843 | Raw home bullpen 3-day IP usage |
| `bull_away_3d` | ✅ | 91.0% | 1843 | Raw away bullpen 3-day IP usage |
| `bull_delta_3d` | ✅ | 91.0% | 1843 | Home minus away 3-day usage (positive=home more tired) |
| `bull_norm_delta_3d` | ✅ | 91.0% | 1843 | Normalized: (home-away)/(home+away+1e-6) |
| `fav_fatigue_3d` | ✅ | 91.0% | 1843 | Favored team 3-day bullpen usage |
| `dog_fatigue_3d` | ✅ | 91.0% | 1843 | Underdog team 3-day bullpen usage |
| `fav_vs_dog_delta_3d` | ✅ | 91.0% | 1843 | Fav minus dog 3-day usage (positive=fav more tired) |
| `bull_usage_last_1d` | 🔶 DATA_LIMITED | — | — | Yesterday bullpen usage (IP) *(原因: Not available in mlb_stats_api_boxscore source (only 3d window fetched))* |
| `bull_usage_last_5d` | 🔶 DATA_LIMITED | — | — | 5-day rolling bullpen usage (IP) *(原因: Not available in mlb_stats_api_boxscore source (only 3d window fetched))* |
| `back_to_back_proxy` | 🔶 DATA_LIMITED | — | — | Back-to-back appearance proxy (bullpen-level) *(原因: No inning-by-inning or day-specific bullpen data available)* |
| `closer_high_leverage` | 🔶 DATA_LIMITED | — | — | Closer / high-leverage appearance count *(原因: boxscore source does not expose closer/high-leverage specific usage)* |

## Section 5 — Segment Attribution 分析

### 5A — heavy_favorite Segment (fav ≥ 0.70)

| 特徵 | N | Coverage | ECE | BSS | Calib Residual | win_rate Δ | Bootstrap Sig |
|------|---|---------|-----|-----|---------------|-----------|--------------|
| `bull_home_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | +0.1247 | no |
| `bull_away_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | +0.1241 | no |
| `bull_delta_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | -0.1471 | no |
| `bull_norm_delta_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | -0.1471 | no |
| `fav_fatigue_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | -0.0115 | no |
| `dog_fatigue_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | +0.1694 | no |
| `fav_vs_dog_delta_3d` | 59 | 98.3% | 0.0655 | +0.2315 | -0.0655 | -0.1471 | no |

### 5B — all Segment

| 特徵 | N | ECE | BSS | win_rate Δ |
|------|---|-----|-----|-----------|
| `bull_delta_3d` | 1843 | 0.0287 | +0.0271 | -0.0245 |
| `fav_fatigue_3d` | 1843 | 0.0287 | +0.0271 | +0.0283 |
| `fav_vs_dog_delta_3d` | 1843 | 0.0287 | +0.0271 | -0.0151 |

### 5C — phase45_failure Segment (hf + low_disagreement)

| 特徵 | N | ECE | win_rate Δ | Bootstrap Sig |
|------|---|-----|-----------|--------------|
| `bull_home_3d` | 31 | 0.0545 | +0.1026 | no |
| `bull_away_3d` | 31 | 0.0545 | +0.1750 | no |
| `bull_delta_3d` | 31 | 0.0545 | -0.2125 | no |
| `bull_norm_delta_3d` | 31 | 0.0545 | -0.2125 | no |
| `fav_fatigue_3d` | 31 | 0.0545 | +0.0084 | no |
| `dog_fatigue_3d` | 31 | 0.0545 | +0.1750 | no |
| `fav_vs_dog_delta_3d` | 31 | 0.0545 | -0.0833 | no |

## Section 6 — Rolling Monthly OOF Validation

**特徵**: `fav_vs_dog_delta_3d` (最佳候選)  
**Segment**: heavy_favorite  
**Folds**: 3  
**OOF 平均 win_rate_delta**: `-0.2075`  
**Consistent Sign**: `False`  
**OOF Significant (≥0.02)**: `True`

| 測試月份 | win_rate_delta | N |
|---------|---------------|---|
| 2025-06 | `+0.3776` | 24 |
| 2025-07 | `+0.0000` | 8 |
| 2025-08 | `-1.0000` | 2 |

## Section 7 — Negative Control (Shuffle Test)

**特徵**: `fav_vs_dog_delta_3d` on heavy_fav  
**真實 win_rate_delta**: `+0.0264`  
**Shuffled mean delta**: `-0.0122`  
**Shuffled std**: `0.1067`  
**Null Rejected (real > mean+1.5σ)**: `False`

> 真實訊號無法與隨機排列顯著區分，signal 可能源自噪音。

## Section 8 — DATA_LIMITED 特徵說明

- **`bull_usage_last_1d`**: Not available in mlb_stats_api_boxscore source (only 3d window fetched)
- **`bull_usage_last_5d`**: Not available in mlb_stats_api_boxscore source (only 3d window fetched)
- **`back_to_back_proxy`**: No inning-by-inning or day-specific bullpen data available
- **`closer_high_leverage`**: boxscore source does not expose closer/high-leverage specific usage

這些特徵需要更細粒度的資料源（逐日 boxscore 或 play-by-play 等）才能實現。
建議在未來數據擴充計劃中列入需求。

## Section 9 — PIT 安全性驗證

- **PIT 安全原則**: `entry_date < game_date`（嚴格隔離）
- **bullpen_usage_last_3d_***: 累計 D-1 + D-2 + D-3 局數（開賽前）✅
- **rest_days_***: 賽前狀態資料 ✅
- **home_win 欄位**: 僅作為預測標籤 `_label_home_win`，絕不作為特徵 ✅
- **禁用特徵模式**: `home_win`, `result`, `final`, `winning` — 自動拒絕 ✅

## Section 10 — Phase 45 Failure Segment 根因歸因

Phase 45 的 failure segments 包含：
- `odds_bucket:heavy_favorite` (fav_prob ≥ 0.70)
- `disagreement:low` (|model - market| ≤ 中位數 0.0414)

**phase45_failure 段 `fav_vs_dog_delta_3d` attribution**:
- N = 31
- win_rate_high (fav tired) = 0.6667
- win_rate_low (fav rested) = 0.7500
- win_rate_delta = -0.0833
- Bootstrap 95% CI: [-0.4083, +0.2458]
- Bootstrap Significant: False

> bullpen 疲勞特徵顯示一定方向性，但樣本過小，需謹慎解讀。

## Section 11 — Gate 決策

### ⚠️ Gate: `DIAGNOSTIC_ONLY_SIGNAL`

**理由**: Training-set directional signal present in ≥1 feature family (heavy_fav). OOF mean_delta=-0.2075 is large but inconsistent sign across 3 folds (fold sizes: [24, 8, 2]) — likely noise from small n. n_heavy_fav=60. DIAGNOSTIC ONLY — no production patch.

### 後續行動建議

1. 訊號方向一致，但 OOF 驗證樣本不足（heavy_fav n 偏小）
2. **不建議立即注入生產模型**
3. 建議繼續累積 2025 賽季資料至 ≥ 100 heavy_fav 場次後重新驗證
4. 或探索更細粒度的牛棚資料（1d / closer 特定資料）

---

*Report generated by `phase60_bullpen_feature_decomposition_v1` at 2026-05-06 03:17:50 UTC*  
*Audit hash: `2557762ecdb4a372`*  
*CANDIDATE_PATCH_CREATED=False | PRODUCTION_MODIFIED=False | DIAGNOSTIC_ONLY=True*

`PHASE_60_BULLPEN_FEATURE_DECOMPOSITION_VERIFIED`