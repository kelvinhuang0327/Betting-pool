# P44 Signal Temporal Stability + Calibration Audit

**Date:** 2026-05-25
**Phase:** P44 (diagnostic-only, paper_only=true)

## Governance Flags
- paper_only: `True`
- diagnostic_only: `True`
- promotion_freeze: `True`
- kelly_deploy_allowed: `False`
- live_api_calls: `0`

## Data Inventory
- Source: `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
- Closing odds: `mlb_odds_2025_real.csv`
- Phase56 rows: 2025
- Quality rows (delta available, not fallback): 1428
- Joined rows (with closing-line market): 1426
- Tier C rows (|delta| >= 0.50): 535

## P44.A — Monthly Temporal Edge Breakdown (Tier C)

| Month | n | Mean Edge | Std | Pos Rate | CI Low | CI High | Classification |
|-------|---|-----------|-----|----------|--------|---------|----------------|
| 2025-04 | 16 | 0.0954 | 0.0816 | 0.875 | 0.0548 | 0.1344 | ✅ STABLE |
| 2025-05 | 120 | 0.1050 | 0.0926 | 0.875 | 0.0882 | 0.1212 | ✅ STABLE |
| 2025-06 | 101 | 0.1101 | 0.0922 | 0.871 | 0.0919 | 0.1275 | ✅ STABLE |
| 2025-07 | 92 | 0.1083 | 0.0838 | 0.924 | 0.0913 | 0.1253 | ✅ STABLE |
| 2025-08 | 108 | 0.1003 | 0.0813 | 0.907 | 0.0851 | 0.1159 | ✅ STABLE |
| 2025-09 | 98 | 0.1084 | 0.0830 | 0.908 | 0.0922 | 0.1246 | ✅ STABLE |

**Overall Temporal Pattern:** ✅ `TEMPORAL_STABLE`

## P44.B — Calibration Audit (Tier C, 10-bin)

| Bin | n | Predicted Mean | Actual Win Rate | Gap |
|-----|---|----------------|-----------------|-----|
| [0.0, 0.1) | 0 | — | — | — |
| [0.1, 0.2) | 1 | 0.1915 | 0.0000 | +0.1915 |
| [0.2, 0.3) | 86 | 0.2644 | 0.4767 | -0.2124 |
| [0.3, 0.4) | 156 | 0.3479 | 0.4551 | -0.1072 |
| [0.4, 0.5) | 24 | 0.4013 | 0.4583 | -0.0570 |
| [0.5, 0.6) | 22 | 0.5987 | 0.6818 | -0.0831 |
| [0.6, 0.7) | 151 | 0.6567 | 0.6821 | -0.0254 |
| [0.7, 0.8) | 95 | 0.7364 | 0.6421 | +0.0943 |
| [0.8, 0.9) | 0 | — | — | — |
| [0.9, 1.0) | 0 | — | — | — |

**Brier Score:** `0.248133`
**ECE:** `0.095289` (bins used: 6)
**Calibration Classification:**  `MODERATE_MISCALIBRATED`

## Final P44 Classification

**P44 Classification:** `P44_MODERATE — further monitoring warranted`

## Known Limitations
- 2024 closing-line data gap **remains unresolved** — temporal analysis covers 2025 only.
- CSV closing-line odds are from a single post-season scrape; no pregame trajectory available.
- This is edge vs closing-line, NOT strict CLV.
- Sigmoid model is the locked P40/P41/P42 mapping; no post-hoc recalibration applied.
- **No production deployment proposal. No champion replacement. Paper-only.**
