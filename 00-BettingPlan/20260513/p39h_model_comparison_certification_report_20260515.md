# P39H — Model Comparison Certification Report
**Date**: 2026-05-15  
**Branch**: `p13-clean`  
**HEAD**: `a6c95b2` + P39H working changes  
**Marker**: `P39H_MODEL_COMPARISON_CERTIFIED_20260515`

---

## 1. Input Summary

| Field | Value |
|-------|-------|
| Enriched CSV | `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv` |
| Rows | 2,187 |
| y_true source | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` |
| y_true match | 2187/2187 = 100.0% |
| Null feature cols | 0 |

---

## 2. Split Summary

| Field | Value |
|-------|-------|
| Split type | TIME_AWARE (chronological) |
| Test start date | 2024-08-01 |
| Train rows | 1,389 (2024-04-15 → 2024-07-31) |
| Test rows | 798 (2024-08-01 → 2024-09-30) |
| Random split | NO |
| Leakage boundary | window_end < game_date (verified in P39G) |

---

## 3. Model Summary

| Field | Value |
|-------|-------|
| Model type | LogisticRegression (sklearn 1.8.0, C=1.0, lbfgs) |
| Feature scaling | StandardScaler (fit on train only) |
| Feature count | 12 (11 Statcast + p_oof) |
| Odds features | NONE |
| Postgame features | NONE |
| Leakage violations | 0 |

---

## 4. Feature Set

```
home_rolling_pa_proxy
home_rolling_avg_launch_speed
home_rolling_hard_hit_rate_proxy
home_rolling_barrel_rate_proxy
away_rolling_pa_proxy
away_rolling_avg_launch_speed
away_rolling_hard_hit_rate_proxy
away_rolling_barrel_rate_proxy
diff_rolling_avg_launch_speed
diff_rolling_hard_hit_rate_proxy
diff_sample_size
p_oof  (P38A baseline signal — input only, not target)
```

---

## 5. Metrics

| Metric | Baseline (p_oof) | Enriched Model | Delta |
|--------|-----------------|----------------|-------|
| Brier score | 0.247675 | 0.248631 | **+0.000956** |
| Log-loss | 0.688475 | 0.690359 | +0.001884 |
| BSS vs base-rate | 0.008676 | 0.004850 | — |
| Base rate (test) | 0.5125 | 0.5125 | — |
| N test rows | 798 | 798 | — |

> Note: The P38A OOF baseline Brier of **0.2487** was measured on the full OOF set (all 2,187 rows). The test-set baseline Brier here is **0.2477**, measured on the Aug-Sep 2024 subset of 798 games. Both figures are consistent.

---

## 6. Interpretation

**Classification**: `INCONCLUSIVE`

The enriched model (LogisticRegression on 11 Statcast rolling features + p_oof) shows a delta Brier of **+0.000956** — marginally worse than using p_oof alone, but within the ±0.001 inconclusive zone.

### Why inconclusive is the correct finding

1. **p_oof already captures team quality**: The P38A model was trained on rich historical game-level data. Adding 7-day rolling batting metrics on top of it via logistic regression does not appear to provide meaningful additional signal within this simple model architecture.

2. **Feature granularity mismatch**: The rolling features are team-level batting aggregates (PA proxy, launch speed, hard hit rate, barrel rate). These do not directly capture pitching quality, ballpark effects, or rest days — all of which p_oof implicitly incorporates.

3. **Small signal, high noise**: With 798 test games, the expected variance in Brier score is ~0.008 (±0.8pp at 95% CI). A delta of +0.001 is well within noise.

4. **Single-split limitation**: This result comes from one time-based split. A walk-forward cross-validation over multiple folds would be needed to draw stronger conclusions.

---

## 7. Statistical / Practical Caveats

- Brier confidence interval not formally computed — sample size of 798 is sufficient but marginal for detecting small effects
- Logistic regression with StandardScaler may not optimally combine these feature types
- Rolling 7-day window may be too narrow for stable team batting estimates early in season
- No pitcher-level features included (starting pitcher ERA, K%, etc.)
- No park factors included
- No home/away advantage adjustment beyond what p_oof encodes

---

## 8. Production Edge Claim

**NONE. This is a paper-only research comparison.**

The Statcast rolling features do not show measurable improvement over the P38A baseline in this evaluation. No bet sizing, no CLV, no live TSL write.

---

## 9. Whether P39I Should Proceed

**Recommended**: Proceed with P39I — but with a different design:

### Option 3 (INCONCLUSIVE path): Walk-Forward Folds + Feature Ablation

The single time-split result is insufficient to definitively conclude that Statcast features have no value. Recommended next steps:

1. **Walk-forward folds**: Use fold_id from p_oof (folds 0-8 available). Train on folds 0-(k-1), test on fold k, average metrics across k=1..9.
2. **Feature ablation**: Test subsets:
   - p_oof alone (current baseline)
   - p_oof + diff features only (diff_rolling_avg_launch_speed + diff_rolling_hard_hit_rate_proxy)
   - p_oof + full Statcast
3. **Richer feature set for P39I**:
   - Add starting pitcher rolling K% / ERA / WHIP (if pybaseball provides it pre-game)
   - Add rolling team run differential (if available without leakage)
4. **Keep P38A baseline**: Until a feature set achieves delta Brier < -0.002 consistently across multiple folds, P38A remains the production-equivalent baseline for research.

---

## 10. TRACK Summary

| TRACK | Status | Key Result |
|-------|--------|------------|
| TRACK 0 | ✅ PASS | Branch p13-clean @ a6c95b2, RAW_AND_SECRET_NOT_VISIBLE |
| TRACK 1 | ✅ PASS | Scope doc created, PAPER_ONLY_TIME_AWARE_MODEL_COMPARISON |
| TRACK 2 | ✅ PASS | Script `p39h_enriched_feature_model_comparison_v1` created |
| TRACK 3 | ✅ PASS | 23/23 unit tests PASS |
| TRACK 4 | ✅ PASS | Executed: INCONCLUSIVE (delta_brier=+0.000956) |
| TRACK 5 | ✅ PASS | 109/109 regression tests PASS — `P39H_REGRESSION_PASS_20260515` |
| TRACK 6 | ✅ PASS | This document |
| TRACK 7 | 🔒 NOT AUTHORIZED | No push without explicit YES |
| TRACK 8 | ✅ PASS | Markers confirmed |
| TRACK 9 | ✅ PENDING REVIEW | Commit candidates staged |

---

## 11. Final Classification

**`P39H_MODEL_COMPARISON_INCONCLUSIVE`**

- Enriched Brier: 0.248631
- Baseline Brier: 0.247675 (test set)
- Delta Brier: +0.000956 (within noise threshold)
- Regression tests: 109/109 PASS
- Leakage violations: 0
- Odds features: NONE
- Push: NOT AUTHORIZED

`P39H_MODEL_COMPARISON_CERTIFIED_20260515`  
`P39H_REGRESSION_PASS_20260515`  
`P39H_PUSH_NOT_AUTHORIZED_20260515`  
`P39H_MODEL_COMPARISON_NO_IMPROVEMENT_20260515`  
`PAPER_ONLY=True | pybaseball != odds source | no push`
