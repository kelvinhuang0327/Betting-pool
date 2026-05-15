# P39H — Time-Aware Enriched Feature Model Comparison Report
**Date**: 2026-05-15  
**Script**: `p39h_enriched_feature_model_comparison_v1`  
**PAPER_ONLY**: True  

---

## 1. Split Summary

| Field | Value |
|-------|-------|
| Split type | TIME_AWARE (chronological) |
| Test start date | 2024-08-01 |
| Train rows | 1389 |
| Test rows | 798 |
| Random split | NO |

---

## 2. Feature Set

- `home_rolling_pa_proxy`
- `home_rolling_avg_launch_speed`
- `home_rolling_hard_hit_rate_proxy`
- `home_rolling_barrel_rate_proxy`
- `away_rolling_pa_proxy`
- `away_rolling_avg_launch_speed`
- `away_rolling_hard_hit_rate_proxy`
- `away_rolling_barrel_rate_proxy`
- `diff_rolling_avg_launch_speed`
- `diff_rolling_hard_hit_rate_proxy`
- `diff_sample_size`
- `p_oof`

---

## 3. Metrics

| Metric | Baseline (p_oof) | Enriched Model | Delta |
|--------|-----------------|---------------|-------|
| Brier score | 0.247675 | 0.248631 | 0.000956 |
| Log-loss | 0.688475 | 0.690359 | 0.001884 |
| BSS vs base-rate | 0.008676 | 0.00485 | — |
| Base rate | 0.5125 | 0.5125 | — |

---

## 4. Interpretation

**Result**: INCONCLUSIVE  
**Delta Brier**: 0.000956 (negative = enriched model is better)  

> delta_brier < 0 means enriched model is better (lower Brier is better). No production edge claim. Paper-only research comparison.

---

## 5. Feature Coefficients (Logistic Regression)

| Feature | Coefficient |
|---------|------------|
| `p_oof` | 0.090909 |
| `home_rolling_hard_hit_rate_proxy` | 0.074493 |
| `diff_rolling_hard_hit_rate_proxy` | 0.057289 |
| `away_rolling_pa_proxy` | 0.052710 |
| `diff_sample_size` | 0.038806 |
| `away_rolling_barrel_rate_proxy` | -0.027762 |
| `home_rolling_barrel_rate_proxy` | 0.025182 |
| `home_rolling_pa_proxy` | 0.021096 |
| `away_rolling_hard_hit_rate_proxy` | -0.006591 |
| `home_rolling_avg_launch_speed` | 0.003134 |
| `diff_rolling_avg_launch_speed` | 0.002176 |
| `away_rolling_avg_launch_speed` | -0.000076 |

---

## 6. Guards

| Guard | Status |
|-------|--------|
| Odds features | NONE |
| Leakage violations | 0 |
| Random split | NO |
| Production edge claim | NO |
| Push | NOT AUTHORIZED |

---

`P39H_ENRICHED_MODEL_COMPARISON_NO_IMPROVEMENT_20260515`  
`PAPER_ONLY=True | pybaseball != odds source | no push`