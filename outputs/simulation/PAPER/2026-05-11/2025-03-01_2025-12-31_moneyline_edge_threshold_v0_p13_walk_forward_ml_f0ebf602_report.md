# Strategy Simulation Report — moneyline_edge_threshold_v0_p13_walk_forward_ml

**Simulation ID:** `sim-moneyline_edge_threshold-f0ebf602`  
**Date Range:** 2025-03-01 → 2025-12-31  
**Generated:** 2026-05-11T07:37:16.402421+00:00  
**Paper-Only:** True  

## Gate Status

**`BLOCKED_NEGATIVE_BSS`**

- Brier Skill Score = -0.0338 < 0. Model underperforms market baseline. require_positive_bss=True blocks this strategy.

## Metrics Summary

| Metric | Value |
|--------|-------|
| Sample size | 681 |
| Bet count | 327 |
| Skipped count | 0 |
| Avg model prob | 0.5447 |
| Avg market prob | 0.5329 |
| Brier (model) | 0.2477 |
| Brier (market) | 0.2396 |
| Brier Skill Score | -0.0338 |
| ECE | 0.0043 |
| ROI (%) | -0.91 |
| Max Drawdown (%) | 86.84 |
| Sharpe proxy | -0.0082 |
| Avg edge (%) | 0.0118 |
| Avg Kelly fraction | 0.0221 |

## Source Trace

```json
{
  "strategy_name": "moneyline_edge_threshold_v0_p13_walk_forward_ml",
  "date_start": "2025-03-01",
  "date_end": "2025-12-31",
  "edge_threshold": 0.01,
  "kelly_cap": 0.05,
  "input_rows_total": 681,
  "model_prob_source": "column:model_prob_home",
  "market_prob_source": "american_moneyline_pair_to_no_vig(Home ML, Away ML)",
  "rows_parsed": 681,
  "rows_skipped": 0,
  "missing_market_data": 0,
  "missing_model_data": 0,
  "probability_source_mode": "calibrated_model",
  "real_model_count": 0,
  "calibrated_model_count": 681,
  "market_proxy_count": 0,
  "missing_model_prob_count": 0,
  "walk_forward_ml_candidate_count": 681,
  "ml_model_type": [
    "logistic_regression"
  ],
  "ml_feature_policy": [
    "p13_v1"
  ],
  "ml_features_used": [
    "indep_recent_win_rate_delta",
    "indep_starter_era_delta"
  ],
  "leakage_safe": true,
  "ml_candidate_note": "P13 walk-forward ML candidate probabilities; paper-only and still requires positive BSS gate to pass",
  "calibration_mode": "walk_forward_oof",
  "oof_calibration_count": 681,
  "calibration_warning": "walk-forward OOF calibration candidate; production still requires human approval",
  "deployability_note": "OOF calibration with leakage_safe=True; eligible for paper-only candidate evaluation",
  "gate_status": "BLOCKED_NEGATIVE_BSS",
  "sample_size": 681,
  "bet_count": 327
}
```

---
*PAPER-ONLY simulation. No real bets placed. No production enablement.*
