# P39I Walk-Forward Feature Ablation Report
**Date:** 2026-05-16
**Classification:** `NO_ROBUST_IMPROVEMENT`
**paper_only:** True | **production_ready:** False

---

## Fold Definitions

| Fold | Train N | Test N | Train Start | Train End | Test Start | Test End | Skipped |
|------|---------|--------|-------------|-----------|------------|----------|---------|
| 0 | 437 | 437 | 2024-04-15 | 2024-05-18 | 2024-05-18 | 2024-06-20 | No |
| 1 | 874 | 437 | 2024-04-15 | 2024-06-20 | 2024-06-20 | 2024-07-26 | No |
| 2 | 1311 | 437 | 2024-04-15 | 2024-07-26 | 2024-07-26 | 2024-08-28 | No |
| 3 | 1748 | 439 | 2024-04-15 | 2024-08-28 | 2024-08-28 | 2024-09-30 | No |

---

## Feature Group Results

### Aggregate Metrics (per feature group)

| Group | Mean ΔBrier | Median ΔBrier | % Folds Improved | Worst Degradation | Best Improvement | N Folds | Classification |
|-------|------------|---------------|-----------------|-------------------|-----------------|---------|----------------|
| `baseline_p_oof` | 0.0000 | 0.0000 | 0.0 | 0.0000 | 0.0000 | 4 | `NO_ROBUST_IMPROVEMENT` |
| `diff_features_only` | 0.0019 | 0.0011 | 0.0 | 0.0044 | 0.0009 | 4 | `NO_ROBUST_IMPROVEMENT` |
| `home_away_rolling_only` | 0.0016 | 0.0003 | 0.2 | 0.0069 | -0.0012 | 4 | `NO_ROBUST_IMPROVEMENT` |
| `full_statcast_rolling` | 0.0021 | 0.0011 | 0.0 | 0.0061 | 0.0001 | 4 | `NO_ROBUST_IMPROVEMENT` |
| `p_oof_plus_full_statcast` | 0.0017 | 0.0011 | 0.2 | 0.0053 | -0.0007 | 4 | `NO_ROBUST_IMPROVEMENT` |

---

## Per-Fold Detail

### baseline_p_oof

| Fold | Train N | Test N | Baseline Brier | Candidate Brier | ΔBrier | Improved |
|------|---------|--------|----------------|-----------------|--------|---------|
| 0 | 437 | 437 | 0.2467 | 0.2467 | 0.0000 | ❌ |
| 1 | 874 | 437 | 0.2524 | 0.2524 | 0.0000 | ❌ |
| 2 | 1311 | 437 | 0.2491 | 0.2491 | 0.0000 | ❌ |
| 3 | 1748 | 439 | 0.2475 | 0.2475 | 0.0000 | ❌ |

### diff_features_only

| Fold | Train N | Test N | Baseline Brier | Candidate Brier | ΔBrier | Improved |
|------|---------|--------|----------------|-----------------|--------|---------|
| 0 | 437 | 437 | 0.2467 | 0.2511 | 0.0044 | ❌ |
| 1 | 874 | 437 | 0.2524 | 0.2534 | 0.0010 | ❌ |
| 2 | 1311 | 437 | 0.2491 | 0.2500 | 0.0009 | ❌ |
| 3 | 1748 | 439 | 0.2475 | 0.2487 | 0.0012 | ❌ |

### home_away_rolling_only

| Fold | Train N | Test N | Baseline Brier | Candidate Brier | ΔBrier | Improved |
|------|---------|--------|----------------|-----------------|--------|---------|
| 0 | 437 | 437 | 0.2467 | 0.2536 | 0.0069 | ❌ |
| 1 | 874 | 437 | 0.2524 | 0.2512 | -0.0012 | ✅ |
| 2 | 1311 | 437 | 0.2491 | 0.2492 | 0.0001 | ❌ |
| 3 | 1748 | 439 | 0.2475 | 0.2481 | 0.0005 | ❌ |

### full_statcast_rolling

| Fold | Train N | Test N | Baseline Brier | Candidate Brier | ΔBrier | Improved |
|------|---------|--------|----------------|-----------------|--------|---------|
| 0 | 437 | 437 | 0.2467 | 0.2529 | 0.0061 | ❌ |
| 1 | 874 | 437 | 0.2524 | 0.2537 | 0.0013 | ❌ |
| 2 | 1311 | 437 | 0.2491 | 0.2500 | 0.0010 | ❌ |
| 3 | 1748 | 439 | 0.2475 | 0.2476 | 0.0001 | ❌ |

### p_oof_plus_full_statcast

| Fold | Train N | Test N | Baseline Brier | Candidate Brier | ΔBrier | Improved |
|------|---------|--------|----------------|-----------------|--------|---------|
| 0 | 437 | 437 | 0.2467 | 0.2520 | 0.0053 | ❌ |
| 1 | 874 | 437 | 0.2524 | 0.2540 | 0.0016 | ❌ |
| 2 | 1311 | 437 | 0.2491 | 0.2496 | 0.0006 | ❌ |
| 3 | 1748 | 439 | 0.2475 | 0.2468 | -0.0007 | ✅ |

---

## Robust Improvement Summary

Criteria for ROBUST_IMPROVEMENT (all three must pass):
- mean delta Brier ≤ −0.002
- ≥ 60% folds improved
- worst fold degradation ≤ +0.005

| Feature Group | Classification |
|---------------|----------------|
| `diff_features_only` | `NO_ROBUST_IMPROVEMENT` |
| `home_away_rolling_only` | `NO_ROBUST_IMPROVEMENT` |
| `full_statcast_rolling` | `NO_ROBUST_IMPROVEMENT` |
| `p_oof_plus_full_statcast` | `NO_ROBUST_IMPROVEMENT` |

---

## Interpretation Guard

- This is a paper-only research audit. No production edge is claimed.
- No odds, no CLV, no betting recommendation.
- pybaseball rolling features are a baseball stats source, not an odds source.
- P38A baseline remains the operative model until robust improvement is confirmed.

---

## Acceptance Marker

`P39I_WALKFORWARD_ABLATION_NO_ROBUST_IMPROVEMENT_20260515`