# P7 OOF Calibration Validation Summary

**Generated**: 2026-05-11T06:44:07.177265+00:00
**Input**: outputs/predictions/PAPER/2026-05-11/mlb_odds_with_feature_candidate_probabilities.csv

## Results

| Metric | Original | OOF Calibrated | Delta |
|--------|----------|----------------|-------|
| BSS | -0.050579 | -0.027668 | 0.022911 |
| ECE | 0.081139 | 0.042928 | -0.038211 |

**OOF Row Count**: 1949
**Skipped (warm-up)**: 451
**Total Folds**: 5
**First Validation Month**: 2025-05

## Recommendation

**OOF_IMPROVED_BUT_STILL_BLOCKED**
**Deployability**: PAPER_ONLY_CANDIDATE

## Gate Reasons

- OOF BSS=-0.0277 improved over original BSS=-0.0506 but remains <= 0. Gate stays blocked.
- walk-forward OOF calibration candidate; production still requires human approval

## Leakage Safety

- Calibration maps are fit on **past data only** (train_end < validation_start).
- Validation outcomes are **never used** in calibration fitting.
- `leakage_safe = True` in all OOF row traces.

> ⚠️ walk-forward OOF calibration candidate; production still requires human approval