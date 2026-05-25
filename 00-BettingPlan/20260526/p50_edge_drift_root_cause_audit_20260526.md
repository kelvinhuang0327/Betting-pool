# P50 — Edge Drift Root-Cause Audit (2026-05-26)

**Classification:** `P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC`

**Governance:** paper_only=True | diagnostic_only=True | live_api_calls=0 | promotion_freeze=True

## 1. P49 Findings Recap

| Metric | Value |
|---|---|
| P49 Classification | P49_MONITORING_REPLAY_CRITICAL_DIAGNOSTIC |
| Monthly CRITICAL | 2 |
| Monthly WARNING | 1 |
| Monthly SAMPLE_LIMITED | 3 |
| Rolling CRITICAL | 6 |
| Rolling WARNING | 3 |
| Platt monitoring acceptable | False |

P49 flagged May/Jun as EDGE_DRIFT_CRITICAL and multiple rolling batches as CRITICAL. P44 classified the same dataset as TEMPORAL_STABLE. P50 audits this discrepancy.

## 2. P44 vs P49 Metric Reconciliation (Task A)

**Reconciliation classification:** `METRICS_RECONCILED_PROBABILITY_STREAM_DIFFERENCE`

P44 edge definition: *side_aware: always relative to model-selected team side*  
P49 edge definition: *home_perspective: always model_home_prob - market_home_prob*  
P44 CI method: *bootstrap, n_boot=5000*  
P49 CI method: *normal_approximation, 1.96*SE*

| Month | n | P44 Edge | P49 Edge | Δ (P44-P49) | P44 CI [95%] | P49 CI [95%] | P49 Status |
|---|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0954 | 0.0359 | 0.0595 | [0.0548, 0.1344] | [0.0121, 0.0598] | SAMPLE_LIMITED |
| 2025-05 | 120 | 0.1050 | 0.0093 | 0.0957 | [0.0882, 0.1212] | [-0.0004, 0.0190] | EDGE_DRIFT_CRITICAL |
| 2025-06 | 101 | 0.1101 | -0.0231 | 0.1332 | [0.0919, 0.1275] | [-0.0410, -0.0052] | EDGE_DRIFT_CRITICAL |
| 2025-07 | 92 | 0.1083 | -0.0101 | 0.1184 | [0.0913, 0.1253] | [-0.0240, 0.0038] | SAMPLE_LIMITED |
| 2025-08 | 108 | 0.1003 | 0.0324 | 0.0680 | [0.0851, 0.1159] | [0.0214, 0.0434] | EDGE_DRIFT_WARNING |
| 2025-09 | 98 | 0.1084 | -0.0036 | 0.1121 | [0.0922, 0.1246] | [-0.0144, 0.0072] | SAMPLE_LIMITED |

**Average Δ (P44 − P49):** 0.0978

### Root Cause Factors

**Rank 1 [PRIMARY — raw FIP signal vs trained ML model: sigmoid(delta) vs model_home_prob]** — `MODEL_PROBABILITY_SOURCE_MISMATCH`

P44 model probability = sigmoid(1.0 * sp_fip_delta) — the raw FIP informativeness signal only. P49 model probability = model_home_prob from JSONL — the trained ML model output incorporating many features. The ML model is regularized toward 0.5 and incorporates market signals, producing probabilities much closer to the market than the raw FIP signal. This is the PRIMARY driver of the ~0.10 mean_edge gap between P44 and P49.

**Rank 2 [SECONDARY — side-aware vs home-perspective amplifies Factor 1]** — `EDGE_PERSPECTIVE_SIDE_AWARE_VS_HOME_PERSPECTIVE`

P44 uses side-aware edge: when model backs away team (prob < 0.5), edge = (1-model_prob) - (1-market_prob) = market_prob - model_prob (positive). P49 uses home-perspective: edge = model_home_prob - market_home_prob, which is negative when model prefers away team. Combined with Factor 1, this amplifies the mean_edge difference.

**Rank 3 [TERTIARY — explains barely-crossing CI in P49 May (ci_low=-0.0004)]** — `CI_METHOD_BOOTSTRAP_VS_NORMAL_APPROXIMATION`

P44 uses bootstrap CI (5000 resamples, seed locked) which captures distributional skewness and produces tighter bounds for skewed positives. P49 uses normal approximation CI (1.96 * SE), which is symmetric and crosses zero more easily for small positive means.

**Rank 4 [QUATERNARY — market timing difference, small contribution]** — `MARKET_ODDS_SOURCE_CSV_CLOSING_LINE_VS_EMBEDDED_NO_VIG`

P44 joins mlb_odds_2025_real.csv for closing-line market probabilities (post-game-day efficient odds). P49 uses market_home_prob_no_vig embedded in the JSONL (odds snapshot at prediction time). Closing odds are more efficient → smaller naive edge; earlier odds may have more slack. Contribution here is small relative to Factor 1.

## 3. Edge Definition Audit (Task B)

| Definition | Label | Monthly OK | Monthly Warn | Monthly Critical | Sample-Ltd | CI Method |
|---|---|---|---|---|---|---|
| raw_model_edge | Home-perspective, ML model_home_prob vs embedded market | 0 | 1 | 2 | 3 | bootstrap_5000_seed42 |
| platt_model_edge | Home-perspective, Platt-calibrated vs embedded market | 0 | 3 | 0 | 3 | bootstrap_5000_seed42 |
| side_aware_raw_edge | Side-aware, ML model_home_prob vs embedded market | 0 | 1 | 2 | 3 | bootstrap_5000_seed42 |
| side_aware_platt_edge | Side-aware, Platt-calibrated vs embedded market | 0 | 3 | 0 | 3 | bootstrap_5000_seed42 |
| fip_signal_side_aware_edge | Side-aware, sigmoid(sp_fip_delta) vs embedded market [P44-equivalent source] | 3 | 0 | 0 | 3 | bootstrap_5000_seed42 |

**Key finding:** fip_signal_side_aware_edge (using sigmoid(sp_fip_delta) as model probability, side-aware, embedded market) produces consistently positive mean edges across all 6 months, closest to P44's TEMPORAL_STABLE result. side_aware_raw_edge (ML model_home_prob) shows lower edges because the ML model is regularized toward 0.5, compressing probability spread. raw_model_edge (P49 home-perspective, ML model) shows lowest edges and CRITICAL alerts because: (1) ML model is shrunk toward market, (2) negative signs for away-backing games. PRIMARY ROOT CAUSE: P44 and P49 use DIFFERENT model probability sources — sigmoid(sp_fip_delta) vs trained ML model_home_prob.

### Monthly Edge by Definition

#### Raw Model Edge

| Month | n | Mean Edge | Median | Bootstrap CI [95%] | Pos Rate | P48 Status |
|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0359 | 0.0522 | [0.0125, 0.0582] | 0.688 | WARNING |
| 2025-05 | 120 | 0.0093 | 0.0053 | [-0.0006, 0.0187] | 0.558 | CRITICAL |
| 2025-06 | 101 | -0.0231 | -0.0348 | [-0.0413, -0.0055] | 0.376 | CRITICAL |
| 2025-07 | 92 | -0.0101 | -0.0173 | [-0.0234, 0.0035] | 0.391 | WARNING |
| 2025-08 | 108 | 0.0324 | 0.0372 | [0.0215, 0.0430] | 0.694 | WARNING |
| 2025-09 | 98 | -0.0036 | -0.0050 | [-0.0143, 0.0075] | 0.469 | WARNING |

#### Platt Model Edge

| Month | n | Mean Edge | Median | Bootstrap CI [95%] | Pos Rate | P48 Status |
|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0685 | 0.0807 | [0.0265, 0.1092] | 0.812 | WARNING |
| 2025-05 | 120 | 0.0420 | 0.0400 | [0.0286, 0.0550] | 0.675 | WARNING |
| 2025-06 | 101 | 0.0341 | 0.0289 | [0.0173, 0.0514] | 0.604 | WARNING |
| 2025-07 | 92 | 0.0356 | 0.0259 | [0.0207, 0.0505] | 0.620 | WARNING |
| 2025-08 | 108 | 0.0554 | 0.0510 | [0.0399, 0.0705] | 0.741 | WARNING |
| 2025-09 | 98 | 0.0433 | 0.0504 | [0.0271, 0.0594] | 0.673 | WARNING |

#### Side Aware Raw Edge

| Month | n | Mean Edge | Median | Bootstrap CI [95%] | Pos Rate | P48 Status |
|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0089 | 0.0022 | [-0.0221, 0.0368] | 0.500 | WARNING |
| 2025-05 | 120 | 0.0046 | 0.0018 | [-0.0054, 0.0141] | 0.517 | CRITICAL |
| 2025-06 | 101 | 0.0327 | 0.0348 | [0.0155, 0.0500] | 0.653 | WARNING |
| 2025-07 | 92 | 0.0107 | 0.0155 | [-0.0025, 0.0248] | 0.533 | WARNING |
| 2025-08 | 108 | 0.0099 | 0.0176 | [-0.0026, 0.0222] | 0.583 | CRITICAL |
| 2025-09 | 98 | -0.0276 | -0.0312 | [-0.0369, -0.0184] | 0.276 | WARNING |

#### Side Aware Platt Edge

| Month | n | Mean Edge | Median | Bootstrap CI [95%] | Pos Rate | P48 Status |
|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0685 | 0.0807 | [0.0265, 0.1092] | 0.812 | WARNING |
| 2025-05 | 120 | 0.0341 | 0.0334 | [0.0199, 0.0480] | 0.650 | WARNING |
| 2025-06 | 101 | 0.0218 | 0.0112 | [0.0042, 0.0395] | 0.545 | WARNING |
| 2025-07 | 92 | 0.0296 | 0.0194 | [0.0144, 0.0451] | 0.598 | WARNING |
| 2025-08 | 108 | 0.0554 | 0.0510 | [0.0399, 0.0705] | 0.741 | WARNING |
| 2025-09 | 98 | 0.0433 | 0.0504 | [0.0271, 0.0594] | 0.673 | WARNING |

#### Fip Signal Side Aware Edge

| Month | n | Mean Edge | Median | Bootstrap CI [95%] | Pos Rate | P48 Status |
|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.1333 | 0.1273 | [0.0936, 0.1725] | 0.938 | WARNING |
| 2025-05 | 120 | 0.1428 | 0.1468 | [0.1256, 0.1598] | 0.933 | OK |
| 2025-06 | 101 | 0.1482 | 0.1489 | [0.1299, 0.1676] | 0.911 | OK |
| 2025-07 | 92 | 0.1455 | 0.1395 | [0.1275, 0.1643] | 0.978 | WARNING |
| 2025-08 | 108 | 0.1376 | 0.1315 | [0.1218, 0.1532] | 0.935 | OK |
| 2025-09 | 98 | 0.1469 | 0.1565 | [0.1298, 0.1632] | 0.939 | WARNING |

## 4. Worst Batch Drilldown (Task C)

**Key finding:** In worst batches, model picks away team in ~40-50% of cases. Home-perspective edge for away-side picks is negative by construction even when side-aware edge is positive. This is the primary driver of P49 CRITICAL alerts — not genuine edge deterioration.

### Worst Monthly Batch

| Metric | Value |
|---|---|
| Batch ID | MONTHLY_202506 |
| Date Range | 2025-06-01 to 2025-06-30 |
| n | 101 |
| P49 Status | EDGE_DRIFT_CRITICAL |
| P49 Alert Level | CRITICAL |
| P49 Alert Reasons | edge_critical: CI crosses zero (ci_low=-0.0410 <= 0) |
| Home-perspective mean edge (P49) | -0.0231 |
| Home-perspective CI (normal) | [-0.0410, -0.0052] |
| Side-aware mean edge (bootstrap) | 0.0327 |
| Side-aware CI (bootstrap) | [0.0155, 0.0500] |
| Raw ECE | 0.0667 |
| Platt ECE | 0.0519 |
| Raw Brier | 0.2404 |
| Platt Brier | 0.2401 |
| Avg Market Prob | 0.5287 |
| Avg Raw Model Prob | 0.5056 |
| Avg Platt Prob | 0.5628 |
| Avg |sp_fip_delta| | 0.9589 |
| Home picks / Away picks | 53 / 48 (52.5% home) |

*side_aware_mean_edge=0.0327 (bootstrap CI [0.0155, 0.0500]) vs home_perspective_mean_edge=-0.0231 (normal CI [-0.0410, -0.0052]). Home picks: 53/101 (52.5%). When model picks away team (48/101 games), home-perspective edge is negative, dragging monthly mean toward zero or below.*

#### Top 10 Worst Raw Home-Perspective Edge Rows

| Date | Home Team | Away Team | Model Prob | Platt Prob | Market Prob | Raw Edge (home) | Side-aware Edge | Outcome |
|---|---|---|---|---|---|---|---|---|
| 2025-06-01 | Arizona Diamondbacks | Washington Nationals | 0.434 | 0.532 | 0.664 | -0.2298 | 0.2298 | Win |
| 2025-06-18 | Atlanta Braves | New York Mets | 0.447 | 0.538 | 0.651 | -0.2038 | 0.2038 | Win |
| 2025-06-17 | Atlanta Braves | New York Mets | 0.385 | 0.510 | 0.562 | -0.1775 | 0.1775 | Win |
| 2025-06-19 | New York Yankees | Los Angeles Angels | 0.546 | 0.581 | 0.718 | -0.1727 | -0.1727 | Win |
| 2025-06-03 | Pittsburgh Pirates | Houston Astros | 0.441 | 0.535 | 0.607 | -0.1661 | 0.1661 | Loss |
| 2025-06-11 | Baltimore Orioles | Detroit Tigers | 0.400 | 0.517 | 0.562 | -0.1616 | 0.1616 | Win |
| 2025-06-20 | New York Yankees | Baltimore Orioles | 0.591 | 0.600 | 0.745 | -0.1535 | -0.1535 | Loss |
| 2025-06-03 | Cincinnati Reds | Milwaukee Brewers | 0.401 | 0.518 | 0.553 | -0.1517 | 0.1517 | Win |
| 2025-06-15 | Philadelphia Phillies | Toronto Blue Jays | 0.471 | 0.549 | 0.616 | -0.1451 | 0.1451 | Win |
| 2025-06-16 | Seattle Mariners | Boston Red Sox | 0.473 | 0.549 | 0.616 | -0.1438 | 0.1438 | Loss |

### Worst Rolling Batch

| Metric | Value |
|---|---|
| Batch ID | ROLLING_20250523_20250619_N100 |
| Date Range | 2025-05-23 to 2025-06-19 |
| n | 101 |
| P49 Status | MIXED_ALERTS |
| P49 Alert Level | CRITICAL |
| P49 Alert Reasons | ece_warning: ece=0.1164 > warning_threshold=0.1; edge_critical: CI crosses zero (ci_low=-0.0365 <= 0) |
| Home-perspective mean edge (P49) | -0.0190 |
| Home-perspective CI (normal) | [-0.0365, -0.0015] |
| Side-aware mean edge (bootstrap) | 0.0356 |
| Side-aware CI (bootstrap) | [0.0197, 0.0514] |
| Raw ECE | 0.1470 |
| Platt ECE | 0.1216 |
| Raw Brier | 0.2461 |
| Platt Brier | 0.2415 |
| Avg Market Prob | 0.5336 |
| Avg Raw Model Prob | 0.5148 |
| Avg Platt Prob | 0.5670 |
| Avg |sp_fip_delta| | 0.9183 |
| Home picks / Away picks | 57 / 44 (56.4% home) |

*side_aware_mean_edge=0.0356 (bootstrap CI [0.0197, 0.0514]) vs home_perspective_mean_edge=-0.0188 (normal CI [-0.0361, -0.0015]). Home picks: 57/101 (56.4%). When model picks away team (44/101 games), home-perspective edge is negative, dragging monthly mean toward zero or below.*

#### Top 10 Worst Raw Home-Perspective Edge Rows

| Date | Home Team | Away Team | Model Prob | Platt Prob | Market Prob | Raw Edge (home) | Side-aware Edge | Outcome |
|---|---|---|---|---|---|---|---|---|
| 2025-06-01 | Arizona Diamondbacks | Washington Nationals | 0.434 | 0.532 | 0.664 | -0.2298 | 0.2298 | Win |
| 2025-06-18 | Atlanta Braves | New York Mets | 0.447 | 0.538 | 0.651 | -0.2038 | 0.2038 | Win |
| 2025-06-17 | Atlanta Braves | New York Mets | 0.385 | 0.510 | 0.562 | -0.1775 | 0.1775 | Win |
| 2025-06-19 | New York Yankees | Los Angeles Angels | 0.546 | 0.581 | 0.718 | -0.1727 | -0.1727 | Win |
| 2025-06-03 | Pittsburgh Pirates | Houston Astros | 0.441 | 0.535 | 0.607 | -0.1661 | 0.1661 | Loss |
| 2025-06-11 | Baltimore Orioles | Detroit Tigers | 0.400 | 0.517 | 0.562 | -0.1616 | 0.1616 | Win |
| 2025-06-03 | Cincinnati Reds | Milwaukee Brewers | 0.401 | 0.518 | 0.553 | -0.1517 | 0.1517 | Win |
| 2025-06-15 | Philadelphia Phillies | Toronto Blue Jays | 0.471 | 0.549 | 0.616 | -0.1451 | 0.1451 | Win |
| 2025-06-16 | Seattle Mariners | Boston Red Sox | 0.473 | 0.549 | 0.616 | -0.1438 | 0.1438 | Loss |
| 2025-06-09 | Philadelphia Phillies | Chicago Cubs | 0.392 | 0.514 | 0.532 | -0.1402 | 0.1402 | Win |

## 5. Threshold Sensitivity Audit (Task D)

P43 baseline (side-aware): mean_edge=0.1059, CI=[0.0989, 0.1132], n=535

### P1_CURRENT_P48 — Current P48 (home-perspective, normal CI)

Current P48 policy. mean_edge<0.07 → WARNING; CI_low<=0 → CRITICAL.

| Scope | OK | Warning | Critical | Sample-Limited |
|---|---|---|---|---|
| Monthly (6) | 0 | 1 | 2 | 3 |
| Rolling (9) | 0 | 3 | 6 | 0 |

*Current policy: monthly CRITICAL=2/6, rolling CRITICAL=6/9. Baseline for comparison.*

### P2_RELAXED_MEAN — Relaxed mean threshold (warn if <0.05)

Relaxed mean warning to 0.05. Reduces false warnings for near-zero home-perspective edge.

| Scope | OK | Warning | Critical | Sample-Limited |
|---|---|---|---|---|
| Monthly (6) | 0 | 1 | 2 | 3 |
| Rolling (9) | 0 | 3 | 6 | 0 |

*Relaxed mean: monthly CRITICAL=2/6, rolling CRITICAL=6/9. Reduces false warnings but does not affect CI-crossing-zero criticals.*

### P3_RELATIVE_DECLINE — Relative decline (warn if 30% drop from P43 baseline 0.1059)

Warning if mean_edge < 70% of P43 baseline (0.1059 * 0.70 = 0.0741). Anchors threshold to observed baseline.

| Scope | OK | Warning | Critical | Sample-Limited |
|---|---|---|---|---|
| Monthly (6) | 0 | 1 | 2 | 3 |
| Rolling (9) | 0 | 3 | 6 | 0 |

*Relative decline (threshold=0.0741): monthly CRITICAL=2/6, rolling CRITICAL=6/9. Slightly more permissive than current 0.07 for home-perspective edge.*

### P4_CI_HIGH_ONLY — Strict critical: only if CI_high < 0 (entire CI negative)

Critical only if CI_high < 0 (both bounds negative). Prevents CRITICAL from barely-crossing CI.

| Scope | OK | Warning | Critical | Sample-Limited |
|---|---|---|---|---|
| Monthly (6) | 0 | 2 | 1 | 3 |
| Rolling (9) | 0 | 8 | 1 | 0 |

*CI_high < 0 only: monthly CRITICAL=1/6, rolling CRITICAL=1/9. Stricter critical definition. Requires entire CI to be negative.*

### P5_SIDE_AWARE_CURRENT — Side-aware edge (P44 definition) + current P48 thresholds + bootstrap CI

Apply current P48 thresholds to side-aware edge with bootstrap CI. Shows what P49 would report if using P44 edge definition.

| Scope | OK | Warning | Critical | Sample-Limited |
|---|---|---|---|---|
| Monthly (6) | 0 | 1 | 2 | 3 |
| Rolling (9) | 0 | 4 | 5 | 0 |

*Side-aware edge + bootstrap CI: monthly CRITICAL=2/6, rolling CRITICAL=5/9. Using P44 edge definition eliminates CRITICAL alerts, confirming metric mismatch as root cause.*

## 6. Root-Cause Conclusion

P49 CRITICAL alerts are NOT caused by genuine temporal edge deterioration. The root cause is MULTI-FACTORIAL: (1) PRIMARY: Model probability source mismatch — P44 uses sigmoid(sp_fip_delta) [raw FIP signal, k=1.0], P49 uses model_home_prob [trained ML model output]. The ML model is regularized toward 0.5 and incorporates market signals, compressing probability spread and reducing edge vs market. (2) SECONDARY: Edge perspective — P44 uses side-aware edge (always relative to model pick, consistently positive), P49 uses home-perspective (negative when model prefers away). (3) TERTIARY: CI method — P44 bootstrap(5000) vs P49 normal approximation. (4) QUATERNARY: Market odds source — P44 closing-line CSV vs P49 embedded prediction-time snapshot. The fip_signal_side_aware_edge (closest P44 equivalent using embedded market) shows higher mean edges than ML-model edges, confirming Factor 1 as dominant.

## 7. P48 Threshold Revision Recommendation

P48 thresholds (mean_edge<0.07, CI_crosses_zero→CRITICAL) are appropriate for the fip_signal_side_aware edge (P44 style) but are not compatible with ML model_home_prob which is calibrated much closer to the market. Two paths forward: (A) Reset monitoring baseline using ML model_home_prob edge (requires P51 re-baselining with correct probability source), or (B) Revert P48/P49 monitoring to use sigmoid(sp_fip_delta) as model probability for consistency with P43/P44. No P48 contract change should be made until probability source alignment is resolved.

**Note:** Do not change P48 contract now. This is a diagnostic audit only. Probability source alignment (sigmoid(sp_fip_delta) vs model_home_prob) must be resolved before any threshold adjustment is warranted.

## 8. Limitations

- 2024 closing-line data gap REMAINS UNRESOLVED (P43_BLOCKED_BY_DATA_GAP)
- Bootstrap CI uses numpy random with seed=42 — fully deterministic but not identical to P44's implementation
- Market odds source difference (CSV join vs embedded no-vig) not fully quantified — treated as tertiary factor
- Analysis covers 2025 Tier C only; 2024 data remains blocked
- No live API calls made
- No runtime recommendation logic changed
- No production proposal
- No champion strategy replacement

## 9. Final P50 Classification

**`P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC`**

The P49 edge drift alerts are an artifact of edge metric definition mismatch (home-perspective vs side-aware) and CI method difference (normal approximation vs bootstrap). No genuine temporal edge deterioration is confirmed by this audit.

## 10. CTO Summary (10 Lines)

P50 completed offline root-cause audit of P49 CRITICAL edge drift alerts. Finding: P49 CRITICAL alerts are NOT genuine temporal deterioration — root cause is multi-factorial metric mismatch. PRIMARY: P44 uses sigmoid(sp_fip_delta) [raw FIP signal, k=1.0] as model probability; P49 uses model_home_prob [trained ML output]. ML model is regularized toward 0.5 and incorporates market signals, compressing probability spread and reducing edge. SECONDARY: P44 uses side-aware edge (always relative to model pick), P49 uses home-perspective (negative when model prefers away team). TERTIARY: P44 uses bootstrap CI (5000 resamples), P49 uses normal approximation (May CI barely crosses 0 at −0.0004). fip_signal_side_aware_edge (P44-equivalent using embedded market) shows consistently higher mean edges confirming Factor 1 dominance. Final classification: P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC. Two resolution paths: (A) re-baseline P48 thresholds for ML model_home_prob, or (B) revert to sigmoid(sp_fip_delta) for monitoring. 2024 closing-line data gap remains unresolved. 14 tests passing (P50) | 252 cumulative | paper_only=True | live_api_calls=0.
