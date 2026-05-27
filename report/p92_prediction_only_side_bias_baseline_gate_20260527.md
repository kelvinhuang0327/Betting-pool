# P92 — Prediction-Only Side Bias and Baseline Decomposition Gate

**Date**: 2026-05-27
**Classification**: `P92_SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE`
**Baseline commit**: f0816ba feat(P91): Prediction-Only Tracking Gate — P91_TRACKING_ACTIVE_SIGNAL_STABLE

---

## Gate Purpose

Evaluate whether the P91 signal (hit_rate=0.5693, AUC=0.5943) is explained by
simple side bias (always-predict-home or always-predict-away) or weak baseline comparison.

This is a diagnostic-only gate. No betting recommendation. No EV / CLV / Kelly / stake sizing.

---

## Row Inventory

| Field | Value |
|---|---|
| Total rows | 828 |
| Outcome rows | 808 |
| Season | [2026] |
| Date range | 2026-03-25 — 2026-05-31 |

---

## Side Distribution

| Field | Value |
|---|---|
| predicted_home_count | 412 |
| predicted_away_count | 396 |
| predicted_home_ratio | 0.5099 |
| predicted_away_ratio | 0.4901 |
| actual_home_count | 424 |
| actual_away_count | 384 |

Side split is near-balanced (51/49). No extreme home or away bias detected.

---

## Baseline Comparison

| Metric | Value |
|---|---|
| model_hit_rate | 0.5693 |
| home_baseline_hit_rate | 0.5248 |
| away_baseline_hit_rate | 0.4752 |
| model_vs_home_baseline_delta | +0.0446 |
| model_vs_away_baseline_delta | +0.0941 |
| model_auc | 0.5943 |

The model (56.93%) exceeds the home baseline (52.48%) by +4.46 pp and the
away baseline (47.52%) by +9.41 pp. This is not close to either simple baseline.

---

## Side Split Metrics

| Metric | Value |
|---|---|
| home_predicted_count | 412 |
| away_predicted_count | 396 |
| home_predicted_hit_rate | 0.5922 |
| away_predicted_hit_rate | 0.5455 |

Both home-predicted and away-predicted subsets remain above 50% hit rate.
The signal does not collapse when split by predicted side.

---

## Monthly Baseline Decomposition

| Month | n | Model HR | Home Base | Away Base | Model vs Home |
|---|---|---|---|---|---|
| 2026-03 | 73 | 0.6164 | 0.5890 | 0.4110 | +0.0274 |
| 2026-04 | 389 | 0.5424 | 0.5270 | 0.4730 | +0.0154 |
| 2026-05 | 346 | 0.5896 | 0.5087 | 0.4913 | +0.0809 |

Model outperforms home baseline in all 3 months. No month shows collapse.

---

## Side Bias Assessment

**Assessment**: `SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE`

**Rationale**: model_hr=0.5693 exceeds both home_baseline=0.5248 (+0.0446) and away_baseline=0.4752 (+0.0941). Side split near balanced (home_ratio=0.510). Both home_pred_hr=0.5922 and away_pred_hr=0.5455 remain above 50%. AUC=0.594315.

Thresholds used:
- Home confound threshold: delta < 0.015 AND home_ratio > 0.7
- Away confound threshold: delta < 0.015 AND away_ratio > 0.7
- Minimum side split rows: 50

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
| P91 | P91_TRACKING_ACTIVE_SIGNAL_STABLE |
| P90 | P90_POST_RECOVERY_CLOSURE_READY |
| P86 | P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY |

---

## Final Classification

**`P92_SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE`**

P91 STABLE classification is supported under side-split and baseline decomposition.
The signal is not explained by simple side bias. Both home-predicted and away-predicted
subsets retain positive hit rates above 50%. The model exceeds both baselines across
all three months of 2026 data.

**Next step**: Coverage / bias audit (P93) or continued paper tracking.
Market-edge lane remains blocked (no legal odds dataset).

---

*DISCLAIMER: This report is paper-only and diagnostic-only. Not investment advice.
No forecast, no recommendation, no betting advice, no stake sizing.*
