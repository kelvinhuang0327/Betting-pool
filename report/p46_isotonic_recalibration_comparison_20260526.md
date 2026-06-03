# P46 Isotonic Regression Recalibration Comparison

**Date:** 2026-05-26
**Phase:** P46 (diagnostic-only, paper_only=true)

## Governance Flags
- paper_only: `True`
- diagnostic_only: `True`
- promotion_freeze: `True`
- kelly_deploy_allowed: `False`
- live_api_calls: `0`
- tsl_crawler_modified: `False`
- champion_strategy_changed: `False`
- production_usage_proposed: `False`

## Baselines (P44/P45 Reference)
- P44 raw ECE: `0.0953`, raw Brier: `0.2481`
- P45 Platt test ECE: `0.0701`
- P45 Platt 5-fold mean ECE: `0.0862`

## Data Inventory
- Phase56 rows: 2025
- Quality rows: 1428
- Joined rows: 1426
- Tier C rows (|delta|>=0.50): 535

## P46.A — Train/Test Comparison (80/20, seed=42)

- Train n: 428, Test n: 107
- Isotonic knot count: 13
- Cal prob range: [0.333333, 1.0]

| Method | ECE | Brier |
|--------|-----|-------|
| Raw sigmoid | 0.0972 | 0.2308 |
| Platt (P45) | 0.0701 | 0.2264 |
| Isotonic (P46) | 0.0578 | 0.2227 |

- Isotonic vs Platt ECE Δ: `+0.0123`
- Isotonic vs Raw ECE Δ: `+0.0394`

## P46.B — 5-Fold CV Comparison

| Fold | Train n | Test n | Raw ECE | Platt ECE | Iso ECE | Iso−Platt ECE Δ | Knots |
|------|---------|--------|---------|-----------|---------|-----------------|-------|
| 1 | 428 | 107 | 0.1158 | 0.1001 | 0.0330 | +0.0671 | 17 |
| 2 | 428 | 107 | 0.1288 | 0.0423 | 0.0950 | -0.0527 | 20 |
| 3 | 428 | 107 | 0.1518 | 0.1156 | 0.1254 | -0.0098 | 18 |
| 4 | 428 | 107 | 0.0906 | 0.1027 | 0.1097 | -0.0070 | 19 |
| 5 | 428 | 107 | 0.0972 | 0.0701 | 0.0578 | +0.0123 | 13 |

**CV Aggregate:**
| Mean Raw ECE | Mean Platt ECE | Mean Iso ECE | Iso beats Platt (folds) |
|---|---|---|---|
| 0.1168 | 0.0862 | 0.0842 | 2/5 |

**CV Classification:** ⚠️ `ISOTONIC_COMPARABLE`

## P46.C — Walk-Forward Monthly Comparison

| Train Months | Eval Month | Eval n | Raw ECE | Platt ECE | Iso ECE | Best ECE |
|-------------|------------|--------|---------|-----------|---------|----------|
| 2025-04 | 2025-05 | 120 | 0.1187 | 0.1057 | 0.2493 | platt |
| 2025-04+2025-05 | 2025-06 | 101 | 0.1121 | 0.0599 | 0.1130 | platt |
| 2025-04+2025-05+2025-06 | 2025-07 | 92 | 0.1057 | 0.0382 | 0.0640 | platt |
| 2025-04+2025-05+2025-06+2025-07 | 2025-08 | 108 | 0.1350 | 0.0737 | 0.1007 | platt |
| 2025-04+2025-05+2025-06+2025-07+2025-08 | 2025-09 | 98 | 0.1348 | 0.0523 | 0.0698 | platt |

**Walk-Forward Classification:** ⚠️ `PLATT_WALK_FORWARD_PREFERRED`

## Overfit Risk Discussion
✅ Isotonic knot count (13) is reasonable relative to dataset size.
- Isotonic regression is monotone by construction but can memorize training data finely.
- Walk-forward evaluation tests temporal generalization on unseen future months.
- 5-fold CV provides out-of-fold ECE estimate; instability across folds indicates overfit.

## Final P46 Classification

**P46 Classification:** ⚠️ `P46_MIXED_RECALIBRATION_DIAGNOSTIC`

## Known Limitations
- 2024 closing-line data gap **remains unresolved** — analysis covers 2025 only.
- Isotonic calibration is diagnostic only; no recalibrated model is deployed.
- Both methods applied to closing-line edge dataset, not independent test set.
- **No production deployment. No champion replacement. Paper-only.**
