# P93 — Prediction-Only Coverage and Feature Bias Audit Gate

**Date**: 2026-05-27
**Classification**: `P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP`
**Baseline commit**: fdd341e feat(P92): Prediction-Only Side Bias Baseline Gate

---

## Gate Purpose

Evaluate whether the P92-confirmed prediction-only signal is concentrated in specific
abs_sp_fip_delta ranges (FIP delta magnitude), or broadly distributed across all game types.

This is a diagnostic-only gate. No betting recommendation. No EV / CLV / Kelly / stake sizing.

---

## Row Inventory

| Field | Value |
|---|---|
| Total rows | 828 |
| Outcome rows | 808 |
| rows_with_sp_fip_delta | 808 |
| rows_missing_sp_fip_delta | 0 |
| coverage_rate_sp_fip_delta | 1.0000 |
| coverage_gap_ratio | 0.0000 |
| rows_missing_predicted_side | 0 |

FIP delta is available for all 808 outcome rows (100% coverage). No coverage gap.

---

## Feature Distribution

| Field | Value |
|---|---|
| sp_fip_delta min | -5.9298 |
| sp_fip_delta max | 7.1667 |
| sp_fip_delta mean | -0.0560 |
| sp_fip_delta median | -0.0260 |
| sp_fip_delta p10 | -2.2003 |
| sp_fip_delta p25 | -1.1396 |
| sp_fip_delta p50 | -0.0278 |
| sp_fip_delta p75 | 1.064 |
| sp_fip_delta p90 | 1.8841 |
| abs_sp_fip_delta mean | 1.3390 |
| abs_sp_fip_delta median | 1.0919 |

---

## Quartile Decomposition (by abs_sp_fip_delta)

| Quartile | n | abs_fip range | Model HR | Home Base | Away Base |
|---|---|---|---|---|---|
| Q1 | 202 | [0.0077, 0.5874] | 0.5248 | 0.5050 | 0.4950 |
| Q2 | 202 | [0.5883, 1.0919] | 0.5594 | 0.5347 | 0.4653 |
| Q3 | 202 | [1.0919, 1.8398] | 0.5347 | 0.5099 | 0.4901 |
| Q4 | 202 | [1.8492, 7.1667] | 0.6584 | 0.5495 | 0.4505 |

Q4 (high FIP delta) shows substantially higher hit_rate (0.6584) versus Q1 (0.5248).
All quartiles are above 50%, but the Q4 advantage is significant (+13.4 pp over Q1).

---

## Bucket Analysis

| Bucket | n | Model HR | Home Base | Model vs Home |
|---|---|---|---|---|
| low (<0.5) | 178 | 0.5281 | 0.4944 | +0.0337 |
| mid (0.5–1.5) | 343 | 0.5306 | 0.5394 | +-0.0087 |
| high (>=1.5) | 287 | 0.6411 | 0.5261 | +0.1150 |

High-FIP bucket hit_rate (0.6411) exceeds low-FIP (0.5281) by 0.1130.

---

## Monthly Bucket Decomposition

| Month | n | Model HR | Low HR | High HR | Low n | High n |
|---|---|---|---|---|---|---|
| 2026-03 | 73 | 0.6164 | 0.5385 | 0.7353 | 13 | 34 |
| 2026-04 | 389 | 0.5424 | 0.4868 | 0.6014 | 76 | 143 |
| 2026-05 | 346 | 0.5896 | 0.5618 | 0.6636 | 89 | 110 |

Low-FIP performance is inconsistent across months (Mar 0.538, Apr 0.487, May 0.562).
High-FIP performance is consistently strong (Mar 0.735, Apr 0.601, May 0.664).

---

## Feature Concentration Assessment

**Assessment**: `SIGNAL_CONCENTRATED_IN_HIGH_FIP`

**Rationale**: High-FIP bucket hit_rate=0.6411 exceeds low-FIP=0.5281 by 0.1130 (threshold 0.08). Low-FIP monthly collapse detected in: ['2026-04']. Q4 dominates signal (hit_rate=0.6584).

Thresholds used:
- High concentration delta threshold: 0.08
- Low bucket collapse threshold: 0.5
- Coverage gap threshold: 0.1
- Min quartile rows: 30

---

## Governance Scan

| Flag | Status |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| production_ready | False |
| odds_used | False |
| ev_computed | False |
| clv_computed | False |
| kelly_computed | False |
| live_api_calls | 0 |
| paid_api_called | False |
| no_real_bet | True |
| no_champion_replacement | True |
| no_runtime_recommendation_mutation | True |
| no_production_betting_recommendation | True |
| no_taiwan_lottery_betting_recommendation | True |
| no_calibration_refit | True |
| no_model_retraining | True |
| no_canonical_rows_modification | True |
| no_raw_data_modification | True |
| no_historical_artifact_overwrite | True |
| scope_within_whitelist | True |

**governance_all_pass**: True

This report is diagnostic-only. No betting recommendation. No investment advice.
No EV, CLV, Kelly, or stake sizing. No real bet. No production change.

---

## Classification Locks

| Phase | Classification |
|---|---|
| P92 | P92_SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE |
| P91 | P91_TRACKING_ACTIVE_SIGNAL_STABLE |
| P90 | P90_POST_RECOVERY_CLOSURE_READY |
| P86 | P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY |

---

## Final Classification

**`P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP`**

The P91/P92 signal is materially concentrated in high abs_sp_fip_delta rows (>=1.5).
High-FIP games show consistent performance across all 3 months (60-74%).
Low-FIP games are inconsistent and show near-baseline performance in April (48.7%).
The aggregate P91 signal (56.9%) is pulled upward primarily by high-FIP games.

**Implication**: P91 STABLE remains valid, but the signal is not uniformly strong.
High-FIP games are the primary driver. Low-FIP games contribute weakly.
Market-edge lane remains BLOCKED (no legal odds dataset).

**Next step**: P94 — High-FIP subset deeper diagnostic, or continued paper tracking
with FIP-stratified tracking to confirm signal persistence.

---

*DISCLAIMER: This report is paper-only and diagnostic-only. Not investment advice.
No forecast, no recommendation, no betting advice, no stake sizing.*
