# Phase 59-Pre+ — Heavy-Favorite Local Calibration Counterfactual

**Report Date**: 2026-05-06  
**Phase Version**: `phase59_pre_heavy_favorite_local_calibration_v1`  
**Audit Hash**: `fe71fbf6d62bafe3`  
**Run Timestamp**: 2026-05-06T02:35:34.101636+00:00  

---

## 0. Safety Flags

| Flag | Value |
|------|-------|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED`     | `False` |
| `ALPHA_MODIFIED`          | `False` |
| `DIAGNOSTIC_ONLY`         | `True` |
| `ALPHA` (blend weight)    | `0.4` (frozen) |

## 1. Input Artifacts

| Field | Value |
|-------|-------|
| Input JSONL | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl` |
| Input Audit Hash | `sha256:4ea8134872cda018a71544a765f94e5edf0e2dc9b3ae1f8c410c3445dc5c7696` |
| Total Sample Size | 2025 rows |
| Date Range | 2025-04-27 → 2025-09-28 |

**Selection rationale**: Using `mlb_2025_per_game_predictions.jsonl` (Phase42A baseline)
because it is the canonical, audit-hashed artifact with complete market probabilities
and verified home_win labels for the full 2025 MLB season. Blend is computed fresh
from `model_home_prob` and `market_home_prob_no_vig` at alpha=0.4 to avoid any
dependency on pre-computed blend values.

## 2. Calibration Validation Strategy

**Method**: `rolling_monthly_oof`

For each evaluation month M, the calibrator is trained on **all data with
`game_date` strictly before the first day of M**. This guarantees:
- No game from month M appears in training data (temporal isolation)
- No in-sample fit-and-evaluate (strictly out-of-fold)
- PIT safety: calibration cannot use future results to adjust past predictions

| Split | Months | Rows |
|-------|--------|------|
| Training only (not evaluated) | 2025-04, 2025-05 | 464 |
| Evaluation (OOF calibrated)   | 2025-06, 2025-07, 2025-08, 2025-09 | 1561 |

**PIT guard**: `assert_no_lookahead()` called before every calibrator fit.

## 3. Sample Composition (Evaluation Split)

| Bucket | n | Fraction |
|--------|---|----------|
| 0.50-0.60 | 1206 | 77.3% |
| 0.60-0.70 | 320 | 20.5% |
| 0.70-0.80 | 35 | 2.2% |
| **Total eval** | **1561** | 100% |
| Heavy favorite (≥0.70) | 35 | 2.2% |

## 4. Results: Baseline vs Isotonic vs Platt (OOF Evaluation Split)

| Metric | Baseline | Isotonic | Platt |
|--------|----------|----------|-------|
| Overall BSS | +0.021172 | +0.015020 | +0.019405 |
| Overall ECE | +0.025883 | +0.022583 | +0.014872 |
| **Heavy Fav ECE** (≥0.70) | **+0.077877** | **+0.106086** | **+0.174188** |
| Heavy Fav n | 35 | 35 | 35 |
| High Conf BSS (≥0.65) | +0.214730 | +0.177206 | +0.167171 |
| High Conf n | 121 | 121 | 121 |
| Phase45 Failure Segments | 1 | 1 | 1 |
| Bootstrap CI lower | +0.000000 | -0.015022 | -0.008397 |
| Bootstrap CI upper | +0.000000 | +0.003059 | +0.004877 |
| Bootstrap P(improve) | 0.00% | 7.70% | 28.00% |
| Bootstrap Significant | False | False | False |

## 5. Bucket-Level ECE Comparison

| Bucket | n | Baseline ECE | Isotonic ECE | Platt ECE | Baseline BSS | Isotonic BSS | Platt BSS |
|--------|---|-------------|--------------|-----------|-------------|-------------|---------|
| 0.50-0.60 | 1206 | +0.0299 | +0.0211 | +0.0121 | -0.0026 | -0.0051 | +0.0004 |
| 0.60-0.70 | 320 | +0.0051 | +0.0467 | +0.0477 | +0.0761 | +0.0556 | +0.0665 |
| 0.70-0.80 | 35 | +0.0779 | +0.1061 | +0.1742 | +0.3397 | +0.3374 | +0.2423 |

## 6. Negative Control (Shuffled-Label Sanity Check)

A calibrator trained on **randomly shuffled labels** should not improve heavy_fav ECE.
If it does, the result in §4 is likely an artifact of overfit or data leakage.

| Metric | Value |
|--------|-------|
| Real Baseline Heavy Fav ECE | +0.0779 |
| Shuffled Isotonic Heavy Fav ECE | +0.1067 |
| Shuffled Platt Heavy Fav ECE | +0.2090 |
| Sanity Check Passed | `True` |

**Interpretation**: Shuffled-label ECE does not beat real baseline — negative control passes. Calibration gains (if any) are not due to overfit.

## 7. Gate Conclusion

### 🔬 `BULLPEN_HYPOTHESIS_RETAINED`

**Rationale**: Neither isotonic (ECE 0.1061) nor Platt (ECE 0.1742) substantially improves heavy_fav ECE vs baseline (0.0779). Calibration layer is not the bottleneck.

---

## 8. Next Step Recommendation

Proceed to Phase59: acquire real bullpen boxscore / relief appearance data. Bullpen feature hypothesis remains the primary candidate explanation for heavy_favorite / high_confidence ECE failures.

## 9. Bootstrap CI Interpretation

Bootstrap samples (n=1000) were drawn with replacement from the evaluation set.
CI is the 2.5th–97.5th percentile of (variant_BSS − baseline_BSS) deltas.

- **CI straddles 0** → NOT SIGNIFICANT. Improvement could be sampling noise.
- **CI strictly > 0** → SIGNIFICANT at 95% level. Improvement is likely real.

| Variant | CI [+0.025, +0.975] | Significant |
|---------|----------|-------------|
| Isotonic | [-0.0150, +0.0031] | False |
| Platt    | [-0.0084, +0.0049] | False |

## 10. Data Sufficiency Notes

- Total sample: **2025** rows (full 2025 season backtest)
- Evaluation split: **1561** rows
- Heavy favorite in eval: **35** rows


---

`PHASE_59_PRE_HEAVY_FAVORITE_LOCAL_CALIBRATION_COUNTERFACTUAL_VERIFIED`
