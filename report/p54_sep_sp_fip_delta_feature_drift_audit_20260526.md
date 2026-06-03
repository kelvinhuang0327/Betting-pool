# P54 — Sep 2025 SP FIP Delta Feature Drift Audit

**Run date**: 2026-05-25  
**Final classification**: `P54_NO_FEATURE_DRIFT_FOUND_DIAGNOSTIC`

> **Framing**: This is a paper-only, diagnostic-only analysis. No deployment, no production usage, no runtime logic changes, no Platt constant refitting.

---

## 1. P53 Recap

- Classification: `SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC`
- Sep n: 98, platt_ece: 0.122929 (critical threshold: 0.12)
- Bootstrap 95% CI: [0.062, 0.215] → CI_low=0.062 < 0.12
- Conclusion: Sep exceedance is sample-sensitive, not high-confidence confirmed drift
- P45 Platt: A=0.435432, B=0.245464 (locked, not modified)

---

## 2. Tier C Dataset Verification

- Source: `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
- Filter: |sp_fip_delta|>=0.5, market_home_prob_no_vig in (0,1), home_win defined
- **Tier C n = 535** (expected 535 ✓)

---

## 3. Monthly SP FIP Delta Distribution

| Period | n | mean_fd | std_fd | mean_abs | p75_abs | p90_abs | extreme≥1.0 | extreme≥1.5 |
|--------|---|---------|--------|----------|---------|---------|-------------|-------------|
| Apr | 16 | -0.04875 | 1.022982 | 0.945 | 1.1125 | 1.3 | 0.5 | 0.0625 |
| May | 120 | 0.0465 | 1.013579 | 0.953833 | 1.2 | 1.45 | 0.433333 | 0.075 |
| Jun | 101 | 0.039109 | 1.014337 | 0.958911 | 1.15 | 1.45 | 0.425743 | 0.079208 |
| Jul | 92 | -0.019565 | 0.969931 | 0.917391 | 1.1 | 1.35 | 0.380435 | 0.021739 |
| Aug | 108 | 0.018981 | 0.966899 | 0.918056 | 1.1 | 1.35 | 0.425926 | 0.009259 |
| Sep | 98 | 0.002551 | 1.003175 | 0.956633 | 1.1375 | 1.35 | 0.459184 | 0.030612 |

---

## 4. Statistical Comparison (Sep vs Baseline)

| Comparison | KS statistic | MW U | MW z | MW p-approx | n_sep | n_other |
|------------|-------------|------|------|-------------|-------|---------|
| sep_vs_may | 0.103231 | 5760.5 | -0.2579 | 0.796447 | 98 | 120 |
| sep_vs_jun | 0.0882 | 4910.0 | -0.096 | 0.923504 | 98 | 101 |
| sep_vs_jul | 0.129991 | 4103.5 | -1.0678 | 0.285616 | 98 | 92 |
| sep_vs_aug | 0.108655 | 4888.5 | -0.9443 | 0.345001 | 98 | 108 |
| sep_vs_full_tier_c | 0.073469 | 25224.0 | -0.5954 | 0.551557 | 98 | 535 |

> Note: KS and Mann-Whitney are descriptive. Small p-values alone do not imply deployment action. Sample sizes are modest; interpret with caution.

---

## 5. Calibration Error by FIP Delta Band

### Sep

| Band | n | raw_ece | platt_ece | platt_brier | actual_wr | mean_platt_prob | cal_gap |
|------|---|---------|-----------|-------------|-----------|----------------|---------|
| 0.50_0.75 | 25 | 0.093612 | 0.169051 | 0.242244 | 0.52 | 0.566816 | 0.046816 |
| 0.75_1.00 | 28 | 0.155643 | 0.107692 | 0.228483 | 0.678571 | 0.57088 | 0.107692 |
| 1.00_1.25 | 27 | 0.165456 | 0.245988 | 0.231454 | 0.555556 | 0.575448 | 0.019893 |
| 1.25_1.50 | 15 | 0.06442 | 0.091057 | 0.248943 | 0.533333 | 0.572113 | 0.03878 |
| 1.50_plus | 3 | 0.1391 | 0.175133 | 0.221535 | 0.666667 | 0.58368 | 0.082986 |

### full_tier_c

| Band | n | raw_ece | platt_ece | platt_brier | actual_wr | mean_platt_prob | cal_gap |
|------|---|---------|-----------|-------------|-----------|----------------|---------|
| 0.50_0.75 | 168 | 0.063031 | 0.055475 | 0.237771 | 0.559524 | 0.574733 | 0.015209 |
| 0.75_1.00 | 138 | 0.066599 | 0.060184 | 0.246777 | 0.557971 | 0.575375 | 0.017404 |
| 1.00_1.25 | 131 | 0.107499 | 0.081938 | 0.245799 | 0.534351 | 0.579832 | 0.045481 |
| 1.25_1.50 | 74 | 0.122578 | 0.084187 | 0.225417 | 0.662162 | 0.577975 | 0.084187 |
| 1.50_plus | 24 | 0.158854 | 0.152434 | 0.240108 | 0.541667 | 0.573727 | 0.03206 |

### May

| Band | n | raw_ece | platt_ece | platt_brier | actual_wr | mean_platt_prob | cal_gap |
|------|---|---------|-----------|-------------|-----------|----------------|---------|
| 0.50_0.75 | 43 | 0.178942 | 0.068261 | 0.242655 | 0.534884 | 0.579634 | 0.04475 |
| 0.75_1.00 | 25 | 0.252232 | 0.054221 | 0.22924 | 0.64 | 0.585779 | 0.054221 |
| 1.00_1.25 | 29 | 0.114903 | 0.037258 | 0.235484 | 0.62069 | 0.583432 | 0.037258 |
| 1.25_1.50 | 14 | 0.12345 | 0.207168 | 0.232854 | 0.571429 | 0.585787 | 0.014359 |
| 1.50_plus | 9 | 0.247589 | 0.255503 | 0.253309 | 0.444444 | 0.579549 | 0.135104 |

### Jun

| Band | n | raw_ece | platt_ece | platt_brier | actual_wr | mean_platt_prob | cal_gap |
|------|---|---------|-----------|-------------|-----------|----------------|---------|
| 0.50_0.75 | 33 | 0.142336 | 0.065045 | 0.227598 | 0.575758 | 0.563792 | 0.011966 |
| 0.75_1.00 | 25 | 0.153724 | 0.078634 | 0.260743 | 0.48 | 0.55501 | 0.07501 |
| 1.00_1.25 | 22 | 0.173223 | 0.178868 | 0.233324 | 0.636364 | 0.563147 | 0.073217 |
| 1.25_1.50 | 13 | 0.170569 | 0.129879 | 0.253358 | 0.461538 | 0.562886 | 0.101347 |
| 1.50_plus | 8 | 0.174212 | 0.086264 | 0.224419 | 0.625 | 0.582385 | 0.042615 |

### Aug

| Band | n | raw_ece | platt_ece | platt_brier | actual_wr | mean_platt_prob | cal_gap |
|------|---|---------|-----------|-------------|-----------|----------------|---------|
| 0.50_0.75 | 34 | 0.046097 | 0.043203 | 0.242587 | 0.558824 | 0.585924 | 0.027101 |
| 0.75_1.00 | 28 | 0.146775 | 0.164955 | 0.27229 | 0.428571 | 0.593527 | 0.164955 |
| 1.00_1.25 | 26 | 0.163069 | 0.126131 | 0.262988 | 0.461538 | 0.587669 | 0.126131 |
| 1.25_1.50 | 19 | 0.209937 | 0.194068 | 0.200768 | 0.789474 | 0.595405 | 0.194068 |
| 1.50_plus | 1 | 0.496 | 0.437225 | 0.191166 | 1.0 | 0.562775 | 0.437225 |

---

## 6. Side / Outcome Composition Audit

> selected_side derived from model_home_prob > 0.5; favorite_side derived from market_home_prob_no_vig > 0.5

| Period | n | home_sel% | away_sel% | home_wr% | away_wr% | sel_side_wr% | fav_sel% | dog_sel% |
|--------|---|-----------|-----------|----------|----------|--------------|----------|----------|
| full_tier_c | 535 | 70.8% | 29.2% | 56.6% | 43.4% | 57.4% | 75.5% | 24.5% |
| Sep | 98 | 60.2% | 39.8% | 58.2% | 41.8% | 61.2% | 84.7% | 15.3% |
| May | 120 | 79.2% | 20.8% | 57.5% | 42.5% | 56.7% | 80.0% | 20.0% |
| Jun | 101 | 52.5% | 47.5% | 55.4% | 44.6% | 53.5% | 63.4% | 36.6% |
| Jul | 92 | 70.7% | 29.3% | 58.7% | 41.3% | 59.8% | 71.7% | 28.3% |
| Aug | 108 | 87.0% | 13.0% | 54.6% | 45.4% | 56.5% | 76.9% | 23.1% |

---

## 7. Root-Cause Conclusion

**Final P54 Classification: `P54_NO_FEATURE_DRIFT_FOUND_DIAGNOSTIC`**

No substantial sp_fip_delta distribution drift, extreme concentration, or side composition shift found in Sep 2025 vs baseline. Sep calibration sensitivity is likely sample-size dominated.

---

## 8. Limitations

- Sep n=98 is modest; all statistics have wide confidence intervals.
- selected_side is derived from model_home_prob > 0.5 threshold, not confirmed actual bet side.
- Mann-Whitney p-values use normal approximation; not exact for small samples.
- KS thresholds for 'substantial' are judgment-based; no formal multiple-testing correction.
- sp_fip_delta reflects pre-game SP matchup quality; bullpen FIP composition not separately decomposed.

---

## 9. 2024 Data Gap Status

- **P43_BLOCKED_BY_DATA_GAP**: 2024 closing-line data gap remains unresolved.
- Cross-year validation (2024 vs 2025) is blocked pending 2024 data acquisition.
- This gap does **not** affect the 2025-only P54 analysis.

---

## 10. Governance

| Flag | Value |
|------|-------|
| paper_only | True |
| diagnostic_only | True |
| promotion_freeze | True |
| kelly_deploy_allowed | False |
| live_api_calls | 0 |
| tsl_crawler_modified | False |
| champion_strategy_changed | False |
| production_usage_proposed | False |
| runtime_recommendation_logic_changed | False |
| platt_constants_modified | False |
| p52_contract_overwritten | False |
| p53_artifact_overwritten | False |

---

## 11. Next Recommended Diagnostic

If P54 finds no feature drift, the Sep sample-sensitivity remains the primary explanation.
Recommended next step:
- **P55**: Expand Sep 2025 sample using adjacent game windows (±7 days boundary extension)
  to test stability of ECE as sample grows, OR
- **P55**: Investigate bullpen FIP composition shifts in Sep (separate from SP FIP delta).

No Platt recalibration, no deployment, no production changes are recommended at this stage.

---

*Report generated by scripts/_p54_sep_sp_fip_delta_feature_drift_audit.py*
*Run date: 2026-05-25*