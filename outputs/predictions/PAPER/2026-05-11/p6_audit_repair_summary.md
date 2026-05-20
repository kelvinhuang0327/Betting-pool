# P6 MLB Model Probability Audit & Calibration Repair

**Generated**: 2026-05-11T03:35:07.306753+00:00
**Input**: `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv`
**Bins**: 10 | **Min bin size**: 30

## Audit Summary

| Metric | Value |
|---|---|
| Row count | 2430 |
| Usable count | 1341 |
| Missing model prob | 1089 |
| Missing market prob | 0 |
| Missing outcome | 0 |
| Model Brier | 0.255225 |
| Market Brier | 0.247004 |
| **BSS** | **-0.033283** |
| ECE | 0.059493 |
| Avg model prob | 0.566072 |
| Avg market prob | 0.518116 |
| Avg outcome (home win rate) | 0.522744 |

## Orientation Checks

| Check | Value |
|---|---|
| Home win rate when model > 0.5 | 0.5364 |
| Home win rate when model < 0.5 | 0.4747 |
| Avg model prob when home wins | 0.5708 |
| Avg model prob when home loses | 0.5609 |

## Segment Audits — Monthly BSS

| Month | Count | Model Brier | Market Brier | BSS | ECE |
|---|---|---|---|---|---|
| 2025-03 | 0 | None | None | None | None |
| 2025-04 | 54 | 0.22686 | 0.215191 | -0.054226 | 0.099444 |
| 2025-05 | 244 | 0.273974 | 0.258429 | -0.060152 | 0.147277 |
| 2025-06 | 264 | 0.24963 | 0.245288 | -0.017702 | 0.054179 |
| 2025-07 | 254 | 0.254035 | 0.254468 | 0.001702 | 0.071487 |
| 2025-08 | 271 | 0.257149 | 0.24353 | -0.055923 | 0.05833 |
| 2025-09 | 254 | 0.248198 | 0.240815 | -0.030658 | 0.050651 |

## Segment Audits — Market Prob Bucket

| Bucket | Count | BSS | ECE |
|---|---|---|---|
| __unassigned__ | 0 | None | None |
| heavy_fav_>=0.60 | 192 | -0.044212 | 0.059193 |
| slight_fav_0.50-0.60 | 620 | -0.021046 | 0.07111 |
| slight_underdog_0.40-0.50 | 467 | -0.032308 | 0.0788 |
| underdog_home_<0.40 | 62 | -0.136129 | 0.184191 |

## Segment Audits — Favorite Side

| Side | Count | BSS | ECE |
|---|---|---|---|
| __unassigned__ | 0 | None | None |
| away_fav | 529 | -0.043894 | 0.090023 |
| home_fav | 812 | -0.026316 | 0.067665 |

## Calibration Candidate Evaluation

| Metric | Original | Calibrated | Delta |
|---|---|---|---|
| BSS | -0.033284 | -0.0068 | 0.026484 |
| ECE | 0.059493 | 0.000375 | -0.059118 |

**Recommendation**: `KEEP_BLOCKED`

> ⚠️ in-sample calibration candidate — not production deployable unless OOF validated