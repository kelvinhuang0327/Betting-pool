# Phase 42 — MLB Calibration Repair Report

**Generated**: 2026-05-04T09:21:24Z
**Input Path**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl`
**Row Count**: 2025
**N Splits**: 5
**Methods Evaluated**: identity, binwise, platt, isotonic, market_blend

---

## Classification

**Result**: `CALIBRATION_REPAIR_NOT_HELPFUL`

---

## Split Summary

| Fold | Train Start | Train End | Test Start | Test End | Train N | Test N |
|------|-------------|-----------|------------|----------|---------|--------|
| 1 | 2025-04-27 | 2025-05-22 | 2025-05-22 | 2025-06-17 | 337 | 337 |
| 2 | 2025-04-27 | 2025-06-17 | 2025-06-17 | 2025-07-11 | 674 | 337 |
| 3 | 2025-04-27 | 2025-07-11 | 2025-07-12 | 2025-08-09 | 1011 | 337 |
| 4 | 2025-04-27 | 2025-08-09 | 2025-08-09 | 2025-09-03 | 1348 | 337 |
| 5 | 2025-04-27 | 2025-09-03 | 2025-09-03 | 2025-09-28 | 1685 | 337 |

---

## Per-Method Overall Metrics

| Method | Cal Brier | Raw Brier | Market Brier | Cal BSS | Raw BSS | Cal ECE | Raw ECE | N |
|--------|-----------|-----------|--------------|---------|---------|---------|---------|---|
| identity | 0.2459 | 0.2459 | 0.2451 | -0.0031 (-0.3%) | -0.0031 (-0.3%) | 0.0314 | 0.0314 | 1685 |
| binwise | 0.2502 | 0.2459 | 0.2451 | -0.0207 (-2.1%) | -0.0031 (-0.3%) | 0.0341 | 0.0314 | 1685 |
| platt | 0.2460 | 0.2459 | 0.2451 | -0.0036 (-0.4%) | -0.0031 (-0.3%) | 0.0136 | 0.0314 | 1685 |
| isotonic | 0.2508 | 0.2459 | 0.2451 | -0.0234 (-2.3%) | -0.0031 (-0.3%) | 0.0328 | 0.0314 | 1685 |
| market_blend_a0.4 | 0.2444 | 0.2459 | 0.2451 | +0.0028 (+0.3%) | -0.0031 (-0.3%) | 0.0323 | 0.0314 | 1685 |

---

## Market Blend Alpha Grid

| Alpha | Cal Brier | Cal BSS | Cal ECE |
|-------|-----------|---------|---------|
| 0.0 | 0.2451 | +0.0000 (+0.0%) | 0.0317 |
| 0.1 | 0.2448 | +0.0012 (+0.1%) | 0.0336 |
| 0.2 | 0.2446 | +0.0021 (+0.2%) | 0.0331 |
| 0.3 | 0.2445 | +0.0026 (+0.3%) | 0.0362 |
| 0.4 | 0.2444 | +0.0028 (+0.3%) | 0.0323 |
| 0.5 | 0.2444 | +0.0027 (+0.3%) | 0.0280 |
| 0.6 | 0.2446 | +0.0022 (+0.2%) | 0.0283 |
| 0.7 | 0.2448 | +0.0014 (+0.1%) | 0.0241 |
| 0.8 | 0.2450 | +0.0003 (+0.0%) | 0.0259 |
| 0.9 | 0.2454 | -0.0012 (-0.1%) | 0.0265 |
| 1.0 | 0.2459 | -0.0031 (-0.3%) | 0.0314 |

---

## Summary

| Metric | Raw Model | Calibrated (market_blend) | Market Baseline |
|--------|-----------|-----------------------------------|-----------------|
| Brier  | 0.2459 | 0.2444 | 0.2451 |
| BSS    | -0.0031 (-0.3%) | +0.0028 (+0.3%) | 0.0 (baseline) |
| ECE    | 0.0314 | 0.0323 | — |

**Best Method**: `market_blend` (alpha=0.4)

---

## BSS Safety Gate

- **Gate Status**: ✅ ALLOWED
- **BSS (calibrated)**: 0.0028
- **Model Brier**: 0.244407
- **Market Brier**: 0.245103
- **Task Kind**: `metric_repair`
- **Block Reason**: —
- **Recommendation**: BSS >= 0, no restriction.

**Patch Gate**: ✅ PATCH_GATE_RECHECK_ELIGIBLE

---

## Next Recommended Action

❌ Calibration did not improve Brier/ECE on out-of-sample folds.
   → Focus on DATA_REPAIR or FEATURE_REPAIR_INVESTIGATION first.

---

## Notes

- PATCH_GATE_RECHECK_ELIGIBLE: calibrated BSS >= 0. However, this script does NOT create a CANDIDATE_PATCH.

---

_Phase 42 MLB Calibration Repair — read-only analysis, no production changes._