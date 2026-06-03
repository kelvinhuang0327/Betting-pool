# P45 Platt Scaling Recalibration Pilot

**Date:** 2026-05-26
**Phase:** P45 (diagnostic-only, paper_only=true)

## Governance Flags
- paper_only: `True`
- diagnostic_only: `True`
- promotion_freeze: `True`
- kelly_deploy_allowed: `False`
- live_api_calls: `0`
- tsl_crawler_modified: `False`
- champion_strategy_changed: `False`

## P44 Baseline Reference
- ECE: `0.0953`
- Brier: `0.2481`
- Classification: `MODERATE_MISCALIBRATED`

## Data Inventory
- Phase56 rows: 2025
- Quality rows: 1428
- Joined rows: 1426
- Tier C rows (|delta|>=0.50): 535

## P45.A — Train/Test Platt Pilot (80/20)

- Train n: 428, Test n: 107
- platt_a: `0.435432`, platt_b: `0.245464`
- Raw ECE (test): `0.097154`
- Calibrated ECE (test): `0.070058`
- ECE Improvement: `0.027096`
- Raw Brier (test): `0.230849`
- Calibrated Brier (test): `0.226447`
- Brier Improvement: `0.004402`

## P45.B — 5-Fold Cross Validation

| Fold | Train n | Test n | Raw ECE | Cal ECE | ECE Δ | Raw Brier | Cal Brier |
|------|---------|--------|---------|---------|-------|-----------|-----------|
| 1 | 428 | 107 | 0.1158 | 0.1001 | +0.0156 | 0.2550 | 0.2465 |
| 2 | 428 | 107 | 0.1288 | 0.0423 | +0.0865 | 0.2601 | 0.2399 |
| 3 | 428 | 107 | 0.1518 | 0.1156 | +0.0362 | 0.2737 | 0.2557 |
| 4 | 428 | 107 | 0.0906 | 0.1027 | -0.0121 | 0.2210 | 0.2239 |
| 5 | 428 | 107 | 0.0972 | 0.0701 | +0.0271 | 0.2308 | 0.2264 |

**CV Aggregate:**
- Mean Raw ECE: `0.116838`
- Mean Calibrated ECE: `0.086164`
- Mean ECE Improvement: `0.030673`
- Mean Brier Improvement: `0.009656`
- **CV Classification:** ✅ `RECALIBRATION_HELPFUL`

## P45.C — Walk-Forward Monthly Calibration

| Train Months | Eval Month | Train n | Eval n | Raw ECE | Cal ECE | ECE Δ |
|-------------|------------|---------|--------|---------|---------|-------|
| 2025-04 | 2025-05 | 16 | 120 | 0.1187 | 0.1057 | +0.0131 |
| 2025-04+2025-05 | 2025-06 | 136 | 101 | 0.1121 | 0.0599 | +0.0523 |
| 2025-04+2025-05+2025-06 | 2025-07 | 237 | 92 | 0.1057 | 0.0382 | +0.0676 |
| 2025-04+2025-05+2025-06+2025-07 | 2025-08 | 329 | 108 | 0.1350 | 0.0737 | +0.0613 |
| 2025-04+2025-05+2025-06+2025-07+2025-08 | 2025-09 | 437 | 98 | 0.1348 | 0.0523 | +0.0825 |

**Walk-Forward Classification:** ✅ `WALK_FORWARD_HELPFUL`

## Overfit Risk Discussion

✅ Platt coefficients are within reasonable range (|a| <= 3, |b| <= 2).
- 5-fold CV provides out-of-fold ECE estimate, reducing overfit risk.
- Walk-forward evaluation tests temporal generalization.
- Monthly walk-forward uses only prior data for fitting (no look-ahead).

## Final P45 Classification

**P45 Classification:** `P45_RECALIBRATION_HELPFUL`

## Known Limitations
- 2024 closing-line data gap **remains unresolved** — analysis covers 2025 only.
- Platt scaling is diagnostic only; no recalibrated model is deployed.
- ECE computed on same dataset as edge; not an independent market test.
- **No production deployment proposal. No champion replacement. Paper-only.**
