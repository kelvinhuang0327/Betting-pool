# P7 OOF Calibration Validation Summary

**Generated**: 2026-05-11T07:35:58.651408+00:00
**Input**: outputs/predictions/PAPER/2026-05-11/p13_ml/ml_odds_with_walk_forward_predictions.csv

## Results

| Metric | Original | OOF Calibrated | Delta |
|--------|----------|----------------|-------|
| BSS | -0.014313 | -0.033835 | -0.019521 |
| ECE | 0.012419 | 0.004323 | -0.008096 |

**OOF Row Count**: 681
**Skipped (warm-up)**: 644
**Total Folds**: 2
**First Validation Month**: 2025-08

## Recommendation

**OOF_REJECTED**
**Deployability**: REJECTED

## Gate Reasons

- OOF BSS=-0.0338 did not improve over original BSS=-0.0143. Calibration does not generalize out-of-fold.
- walk-forward OOF calibration candidate; production still requires human approval

## Leakage Safety

- Calibration maps are fit on **past data only** (train_end < validation_start).
- Validation outcomes are **never used** in calibration fitting.
- `leakage_safe = True` in all OOF row traces.

> ⚠️ walk-forward OOF calibration candidate; production still requires human approval