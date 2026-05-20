# Phase 56 Bullpen Feature Builder — Evaluation Report

**生成時間**: 2026-05-05T10:18:42Z
**Run ID**: `c8d5bb50`
**Audit Hash**: `sha256:0ec83c07cb55eb3f`
**Version**: `phase56_bullpen_feature_evaluation_v1`

---

## 1. Executive Summary

| 欄位 | 值 |
|------|-----|
| Gate Recommendation | ⚠️ **DATA_GAP_REMAINS** |
| Bullpen Feature Availability | 0.0% (0/2025) |
| Overall BSS Delta | +0.000000 |
| Overall ECE Delta | +0.000000 |
| Overall Brier Delta | +0.000000 |
| Failure Segments (Baseline) | 3 |
| Failure Segments (Phase56) | 6 |
| CANDIDATE_PATCH_CREATED | False |
| PRODUCTION_MODIFIED | False |

**Gate Rationale**: bullpen_feature_available_rate=0.0% < 80%。缺乏實際牛棚使用資料，無法進行有效特徵評估。需要收集 MLB 2025 牛棚使用記錄 (bullpen_outs, leveraged appearances)。

---

## 2. Bullpen Feature Availability

| 指標 | 值 |
|------|-----|
| Total Rows | 2025 |
| Available Count | 0 |
| Availability Rate | 0.0% |
| Fallback Applied Count | 2025 |
| Model Affecting Count | 0 |
| Model Affecting Rate | 0.0% |
| Avg Abs Adjustment | 0.000000 |
| Max Abs Adjustment | 0.000000 |

> **說明**: availability_rate = 0.0% 表示目前無實際牛棚使用資料，
> 所有特徵使用中性回退值 (neutral fallback)。
> 當 MLB 2025 牛棚出賽記錄被收集後，此值預計 > 80%。

---

## 3. Point-in-Time Safety Summary

- 所有 bullpen 特徵強制 `point_in_time_safe = True`
- 特徵計算僅使用 `game_date` 之前的資料
- 禁止欄位已通過 `mlb_bullpen_pit_validator` 驗證
- 禁止欄位清單: `home_win`, `final_score`, `home_score`, `away_score`,
  `box_score`, `post_game_stats`, `closing_odds_after_game`
- Leakage violations 發現：0 (所有記錄通過 PIT 驗證)

---

## 4. Context Injection Summary

- 輸入: `mlb_2025_per_game_predictions_phase52_sp_context_v1.jsonl`
- 輸出: `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
- 保留原始 `p0_features`（先發投手特徵）
- 新增 `bullpen_features` 子字典
- 不修改 `model_home_prob` 或任何不可變欄位
- feature_version: `phase56_sp_bullpen_context_v1`

---

## 5. Model-Affecting Injection Summary

- 輸入: `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
- 輸出: `mlb_2025_per_game_predictions_phase56_sp_bullpen_injected_v1.jsonl`
- 最大調整幅度: ±0.015 (hard cap)
- Model Affecting Rate: 0.0%
  (availability = 0% → 所有 adjustment = 0 → REPORT_ONLY mode)
- `diagnostic_only = True`
- `candidate_patch_created = False`
- `production_modified = False`

---

## 6. Baseline vs Phase56 Metrics

| 指標 | Baseline | Phase56 | Delta | 方向 |
|------|----------|---------|-------|------|
| N | 2025 | 2025 | — | — |
| Brier Score | 0.244706 | 0.244706 | +0.000000 | — |
| BSS vs Market | -0.003894 | -0.003894 | +0.000000 | — |
| ECE | 0.031097 | 0.031097 | +0.000000 | — |
| Log Loss | 0.682205 | 0.682205 | — | — |
| Market BSS | — | — | (ref: 0.000000) | — |

---

## 7. Critical Segment Delta

Phase55 失敗段：odds_bucket:heavy_favorite, odds_bucket:mid, disagreement:low, month:2025-04, month:2025-06, month:2025-08

| Segment | N | Baseline BSS | Phase56 BSS | Delta | Baseline ECE | Phase56 ECE | Delta | Improvement |
|---------|---|--------------|-------------|-------|--------------|-------------|-------|-------------|
| `confidence:high_confidence` | 315 | -0.035374 | -0.017980 | +0.017394 | 0.389110 | 0.017298 | -0.371812 | IMPROVED |
| `confidence:low_confidence` | 758 | +0.038217 | +0.000519 | -0.037698 | 0.478433 | 0.036001 | -0.442432 | DEGRADED |
| `disagreement:high` | 105 | -0.036194 | -0.038868 | -0.002674 | 0.500455 | 0.075902 | -0.424553 | DEGRADED |
| `disagreement:low` 🔴 | 968 | +0.030061 | -0.000178 | -0.030239 | 0.446977 | 0.029480 | -0.417497 | DEGRADED |
| `month:2025-04` 🔴 | 30 | +0.051309 | -0.068830 | -0.120139 | 0.422663 | 0.199221 | -0.223442 | DEGRADED |
| `month:2025-05` | 212 | +0.071827 | +0.007720 | -0.064107 | 0.437430 | 0.042167 | -0.395263 | DEGRADED |
| `month:2025-06` 🔴 | 204 | -0.122690 | -0.027682 | +0.095008 | 0.477280 | 0.081469 | -0.395811 | IMPROVED |
| `month:2025-07` | 206 | +0.002518 | +0.012512 | +0.009994 | 0.466693 | 0.032205 | -0.434488 | IMPROVED |
| `month:2025-08` 🔴 | 221 | +0.160872 | -0.002189 | -0.163061 | 0.425337 | 0.041782 | -0.383555 | DEGRADED |
| `month:2025-09` | 200 | -0.022271 | -0.002073 | +0.020198 | 0.461517 | 0.047673 | -0.413844 | IMPROVED |
| `odds_bucket:heavy_favorite` 🔴 | 169 | -0.110729 | -0.011805 | +0.098924 | 0.366902 | 0.084552 | -0.282350 | IMPROVED |
| `odds_bucket:light_favorite` | 157 | +0.150375 | -0.008034 | -0.158409 | 0.534875 | 0.027467 | -0.507408 | DEGRADED |
| `odds_bucket:mid` 🔴 | 747 | -0.002699 | -0.001686 | +0.001013 | 0.454136 | 0.044589 | -0.409547 | IMPROVED |

---

## 8. Gate Recommendation

**⚠️ DATA_GAP_REMAINS**

bullpen_feature_available_rate=0.0% < 80%。缺乏實際牛棚使用資料，無法進行有效特徵評估。需要收集 MLB 2025 牛棚使用記錄 (bullpen_outs, leveraged appearances)。

### Gate 決策邏輯

| 條件 | 閾值 | 實際值 | 通過？ |
|------|------|--------|-------|
| bullpen_feature_available_rate | >= 80% | 0.0% | ❌ |
| heavy_fav ECE 改善 | delta <= 0 | (fallback: N/A) | ❌ (data gap) |
| high_conf BSS 未惡化 | delta >= -0.001 | (fallback: N/A) | ❌ (data gap) |
| overall BSS 未惡化 | delta >= -0.001 | +0.000000 | ✅ |
| failure_count 下降 | delta <= 0 | +3 | (N/A) |

---

## 9. Limitations & Next Phase Recommendation

### 當前限制

1. **資料空缺**: 目前無 MLB 2025 牛棚實際出賽記錄
   (`bullpen_outs`, `bullpen_earned_runs`, `leverage_idx`)。
   所有特徵均使用中性回退值，無法進行有效評估。

2. **Gate 強制 DATA_GAP_REMAINS**: 由於 availability = 0%，
   系統自動輸出 DATA_GAP_REMAINS，不代表特徵設計有問題。

3. **調整幅度為零**: 所有記錄的 bullpen_adjustment = 0.0，
   Phase56 injected 與 Phase52 的 model_home_prob 完全相同。

### 下一階段建議 (Phase 57)

**任務**: MLB Bullpen Data Acquisition

**目標**: 收集 MLB 2025 賽季每場比賽的牛棚實際使用記錄

**所需資料欄位**:
```
game_id, game_date, team,
bullpen_outs,           # 牛棚出局數
bullpen_earned_runs,    # 失分
bullpen_appearances,    # 投球次數
high_leverage_appearances,  # 高槓桿出賽次數 (leverage_idx >= 1.5)
```

**資料來源建議**:
- Baseball Reference: Game Logs > Relief Pitching
- Retrosheet: Event files
- FanGraphs API (if accessible)

**驗收標準**:
- 覆蓋率 >= 80% (2,025 場比賽中 >= 1,620 場有牛棚資料)
- 所有資料 point-in-time safe (snapshot_date < game_date)
- 通過 mlb_bullpen_pit_validator 驗證

---

## Hard Rule Verification

| 規則 | 要求值 | 實際值 | 狀態 |
|------|--------|--------|------|
| CANDIDATE_PATCH_CREATED | False | False | ✅ |
| PRODUCTION_MODIFIED | False | False | ✅ |
| DIAGNOSTIC_ONLY | True | True | ✅ |
| Gate Valid | ∈ valid gates | DATA_GAP_REMAINS | ✅ |
| Max Adjustment | <= 0.015 | 0.000000 | ✅ |

---

```
PHASE_56_BULLPEN_FEATURE_BUILDER_VERIFIED
```