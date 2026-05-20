# Phase 67 — Lineup / Rest / Schedule / Ballpark Context Failure Attribution

**Date**: 2026-05-06  
**Status**: COMPLETE  
**Gate**: `OVERFIT_RISK`  
**Completion Marker**: `PHASE_67_CONTEXT_FAILURE_ATTRIBUTION_VERIFIED`  
**Phase Version**: `phase67_context_failure_attribution_v1`

---

## 1. Objective

Investigate whether lineup availability, rest/travel schedule, day/night, ballpark run environment, or divisional structure can explain the blend model's failure pattern (particularly the heavy-favorite underperformance identified in Phase 45).

**Safety constants (ALL FROZEN — unchanged from Phase 66):**

| Constant | Value |
|---|---|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `ALPHA_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |
| `ALPHA` | `0.40` |

---

## 2. Phase Chain Anchors

| Phase | Gate | Meaning |
|---|---|---|
| 64b | `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING` | Bullpen granularity adds no edge |
| 65 | `OVERFIT_RISK` | Bullpen load signal is noise-level |
| 66 | `MARKET_MICROSTRUCTURE_NOT_PROMISING` | Line movement / CLV / opening direction: data limited + no signal |
| **67** | **`OVERFIT_RISK`** | **Context dimensions show noise-level BSS variance** |

---

## 3. Data Sources

| Source | Path | Records |
|---|---|---|
| Predictions (Phase 56 SP+Bullpen context) | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` | 2025 games |
| Retrosheet GL2025 (game log) | `data/mlb_2025/gl2025.txt` | 2430 rows → 2025 unique `(date, home_team)` keys |

**Context alignment**: 2025 / 2025 = **100.0%** ✓ (exceeds `_MIN_COVERAGE_RATE = 0.70`)

Context dimensions derived from GL2025: rest days per team, back-to-back flags, consecutive road games, day/night, day of week, double-header status, divisional matchup, park run factor, season phase.

---

## 4. Blend Formula (frozen)

```
blend = (1 - 0.40) × model_home_prob + 0.40 × market_home_prob_no_vig
fav_prob = max(blend, 1 - blend)
BSS = 1 - blend_brier / market_brier      (direct ratio vs market reference)
```

---

## 5. Segment Sizes

| Segment | N | Definition |
|---|---|---|
| All | 2025 | Full 2025 MLB regular season |
| Heavy Favorite | 60 | `fav_prob >= 0.70` |
| High Confidence | 10 | `fav_prob >= 0.75` |
| Extreme Favorite | 1 | `fav_prob >= 0.80` |
| Phase 45 Failure | 170 | `fav_prob >= 0.60 AND fav_win == 0` |

---

## 6. Segment Metrics

| Segment | N | blend_brier | market_brier | **blend_bss_vs_market** | fav_win_rate | ECE |
|---|---|---|---|---|---|---|
| All | 2025 | 0.2434 | 0.2438 | **+0.0014** | 0.551 | 0.0261 |
| Heavy Favorite | 60 | 0.1777 | 0.1771 | **−0.0033** | 0.767 | 0.0526 |
| High Confidence | 10 | 0.1043 | 0.1239 | **+0.1578** | 0.900 | 0.1284 |
| Phase 45 Failure | 170 | 0.4100 | 0.4135 | **+0.0085** | 0.000 | 0.6395 |

**Notes:**
- Overall blend is marginally better than market (+0.0014 BSS), consistent with Phases 63–66.
- Heavy-favorite segment (n=60): blend is marginally worse (−0.0033 BSS). Still too small for bootstrap significance.
- High-confidence segment (n=10): massive positive BSS (+0.1578) but n=10 is unreliable.
- Phase 45 failure segment (n=170, by definition these are losing favorites): blend slightly better than market (+0.0085), moderate calibration error.

---

## 7. Available Context Dimensions (12)

| # | Dimension | Buckets |
|---|---|---|
| 1 | `home_rest_days_bucket` | b2b_0d, rest_1d, rest_2d, rest_3d, rest_4plus |
| 2 | `away_rest_days_bucket` | b2b_0d, rest_1d, rest_2d, rest_3d, rest_4plus |
| 3 | `rest_imbalance_bucket` | home_2plus_more, home_1_more, equal_rest, away_1_more, away_2plus_more |
| 4 | `back_to_back_bucket` | both_b2b, home_b2b, away_b2b, neither_b2b |
| 5 | `day_night_bucket` | day_game, night_game |
| 6 | `day_of_week_bucket` | weekend, monday, friday, midweek |
| 7 | `double_header_bucket` | single_game, dh_game1, dh_game2 |
| 8 | `divisional_matchup_bucket` | same_division, same_league_diff_div, interleague |
| 9 | `fav_side_bucket` | home_fav, away_fav |
| 10 | `park_run_env_bucket` | pitcher_park (<0.97), neutral_park (0.97–1.03), hitter_park (>1.03) |
| 11 | `season_phase_bucket` | early_season, mid_season, late_season |
| 12 | `away_consec_road_bucket` | road_trip_1_3, road_trip_4_6, road_trip_7plus |

---

## 8. Attribution Results — Top 10 Buckets

| Rank | Dimension | Bucket | N | blend_bss | Boot Sig | CI |
|---|---|---|---|---|---|---|
| 1 | away_rest_days_bucket | rest_2d | 7 | **+0.0426** | ✗ | [0.000, 0.000]* |
| 2 | home_rest_days_bucket | rest_4plus | 15 | **+0.0350** | ✗ | [−0.026, 0.090] |
| 3 | away_rest_days_bucket | rest_4plus | 15 | **+0.0350** | ✗ | [−0.026, 0.090] |
| 4 | home_rest_days_bucket | rest_2d | 9 | **+0.0295** | ✗ | [0.000, 0.000]* |
| 5 | season_phase_bucket | early_season | 187 | **−0.0159** | ✗ | [−0.032, 0.000] |
| 6 | away_consec_road_bucket | road_trip_7plus | 224 | **−0.0151** | ✗ | [−0.033, 0.003] |
| 7 | double_header_bucket | dh_game1 | 46 | **+0.0138** | ✗ | [−0.033, 0.059] |
| 8 | rest_imbalance_bucket | away_1_more | 51 | **+0.0122** | ✗ | [−0.022, 0.044] |
| 9 | back_to_back_bucket | home_b2b | 51 | **+0.0122** | ✗ | [−0.022, 0.044] |
| 10 | back_to_back_bucket | neither_b2b | 228 | **+0.0106** | ✗ | [−0.009, 0.028] |

*CI = [0.000, 0.000] indicates n < `_MIN_BUCKET_N = 15` → bootstrap skipped (result: not significant).

**No bucket achieved bootstrap significance (ci_lower > 0).**

---

## 9. Negative Control Analysis (OVERFIT_RISK Detection)

The negative control permutes (shuffles) outcome labels within each dimension and measures the standard deviation of BSS deltas across buckets. If `shuffled_std >= real_delta`, the signal is noise-level.

| Dimension | real_delta | shuffled_std | Overfit Risk? |
|---|---|---|---|
| rest_imbalance_bucket | 0.0114 | 0.0159 | **YES** |
| back_to_back_bucket | 0.0128 | 0.0153 | **YES** |
| day_night_bucket | 0.0040 | 0.0046 | **YES** |
| double_header_bucket | 0.0127 | 0.0128 | **YES** |
| park_run_env_bucket | 0.0055 | 0.0060 | **YES** |
| home_rest_days_bucket | — | — | No |
| away_rest_days_bucket | — | — | No |
| day_of_week_bucket | — | — | No |
| divisional_matchup_bucket | — | — | No |
| fav_side_bucket | — | — | No |
| season_phase_bucket | — | — | No |
| away_consec_road_bucket | — | — | No |

**5 of 12 dimensions triggered overfit risk.** The BSS variation across their buckets is indistinguishable from random labeling noise.

---

## 10. OOF Temporal Consistency

Monthly leave-one-fold-out validation across the 2025 season: no dimension produced `oof_significant = True`.

- `any_oof_promising = False`
- All 12 dimensions show inconsistent signs across monthly folds, mean OOF delta ≈ −0.0045 (market slightly better on average).

---

## 11. DATA_LIMITED Dimensions

These dimensions could not be computed from available data sources:

| Dimension | Missing Field | Reason |
|---|---|---|
| `travel_distance` | `travel_miles_proxy` | No geocoded travel routes available |
| `getaway_day` | `getaway_day_flag` | Schedule structure not extracted from GL2025 |
| `lineup_available` | `injury_report_available` | No real-time injury data pipeline |
| `lineup_missing` | `lineup_missing_count` | No actual lineup submission data |
| `key_batter_missing` | `key_batter_il_flag` | No IL/injury tracking per game |

These dimensions are theoretically motivated (e.g., lineup availability is a known informational edge) but cannot be evaluated with the current data pipeline.

---

## 12. Gate Decision

**Gate: `OVERFIT_RISK`**

### Decision Logic Applied

1. Coverage check: 2025/2025 aligned → ≥ `_MIN_SEGMENT_N`. ✓  
2. **Overfit risk check: 5 dimensions have shuffled_std ≥ real_delta.** → **OVERFIT_RISK triggered.**

The gate fires at step 2. Even though some dimensions (rest_imbalance, back-to-back, day/night, double-header, park environment) show positive BSS variation across their buckets, the negative control demonstrates that this variation is consistent with random noise. The signal does not exceed the floor set by label permutation.

### Rationale

> Negative control overfit risk detected for dimensions: ['rest_imbalance_bucket', 'back_to_back_bucket', 'day_night_bucket', 'double_header_bucket', 'park_run_env_bucket']. Shuffled label std ≥ real BSS spread — signal is noise-level.

### What This Means

- The blend model's small positive and negative BSS variations across context buckets (rest days, back-to-back, day/night, ballpark, double-header) are not distinguishable from what random label assignment produces.
- This does **not** mean context features are irrelevant forever — it means the 2025 sample (n=2025 games, with fragmented bucket sizes of 7–228 per context cell) lacks the statistical power to detect any real context effect.
- The DATA_LIMITED dimensions (lineup, travel, injury) remain untested and could still harbor exploitable signal if data became available.

---

## 13. Failure Attribution Summary

| Attribution Hypothesis | Result |
|---|---|
| Rest advantage (home/away, imbalance, B2B) | Noise-level BSS variation. Overfit risk confirmed. |
| Day/Night game structure | Overfit risk. BSS delta < shuffled noise. |
| Ballpark run environment | Overfit risk. Real delta ≈ shuffled std. |
| Double-header context | Overfit risk. Signal indistinguishable from noise. |
| Divisional / interleague matchup | No overfit risk detected, but no positive bootstrap significance. |
| Season phase (early/mid/late) | No overfit risk, slight early-season underperformance (−0.016 BSS), but not bootstrap-significant. |
| Long road trips (7+ consecutive) | No overfit risk, slight underperformance (−0.015 BSS), not significant. |
| Lineup availability | DATA_LIMITED — cannot evaluate without IL/injury feed. |
| Travel distance | DATA_LIMITED — no geocoded route data. |
| Getaway day | DATA_LIMITED — not tracked in GL2025 format. |

---

## 14. Next Steps and Recommendations

**`worth_phase68 = False`** — Current context dimensions do not warrant a production patch.

### For Phase 68 (if pursued)

1. **Increase sample size** before re-evaluating context effects. With n=60 heavy favorites and bucket sizes of 7–50, most context cells are below `_MIN_BUCKET_N`. Pooling across multiple seasons (2023–2025) would increase statistical power substantially.
2. **DATA_LIMITED resolution**: If lineup/injury data becomes available (e.g., via Baseball Reference IL transactions, MLBAM injury API), the `lineup_missing_count` and `key_batter_il_flag` dimensions should be the first to evaluate.
3. **Season phase signal**: Early-season (n=187, BSS=−0.0159) is the strongest non-overfit-flagged negative signal. Consider whether model features are systematically misspecified for games before Memorial Day.
4. **Long road trips**: `road_trip_7plus` (n=224, BSS=−0.0151) is the second strongest non-overfit negative signal. Away teams on long road trips (7+ games) show slightly worse-than-market blend predictions. Data collection priority.

### Gate Summary for Phase 68 Planning

```
Phase 67 Gate: OVERFIT_RISK
Interpretation: No exploitable context signal confirmed in 2025 data.
                Context-based patching would risk introducing noise.
Action: Do NOT modify blend formula or market weighting.
        Log OVERFIT_RISK. Continue diagnostic-only monitoring.
```

---

## 15. File Inventory

| File | Status |
|---|---|
| `orchestrator/phase67_context_failure_attribution.py` | ✅ FINAL |
| `scripts/run_phase67_context_failure_attribution.py` | ✅ FINAL |
| `tests/test_phase67_context_failure_attribution.py` | ✅ 174 passed, 1 skipped |
| `reports/phase67_context_failure_attribution_20260506.json` | ✅ Generated |
| `00-BettingPlan/phase67_context_failure_attribution_report_20260506.md` | ✅ This file |

**Full regression (Phase 63–67): 785/785 PASS**

---

*Generated: 2026-05-06 | marker: `PHASE_67_CONTEXT_FAILURE_ATTRIBUTION_VERIFIED`*
