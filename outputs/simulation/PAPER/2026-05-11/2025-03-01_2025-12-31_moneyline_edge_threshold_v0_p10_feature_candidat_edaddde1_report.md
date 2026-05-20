# Strategy Simulation Report — moneyline_edge_threshold_v0_p10_feature_candidate_oof

**Simulation ID:** `sim-moneyline_edge_threshold-edaddde1`  
**Date Range:** 2025-03-01 → 2025-12-31  
**Generated:** 2026-05-11T05:09:35.669260+00:00  
**Paper-Only:** True  

## Gate Status

**`BLOCKED_NEGATIVE_BSS`**

- Brier Skill Score = -0.0283 < 0. Model underperforms market baseline. require_positive_bss=True blocks this strategy.

## Metrics Summary

| Metric | Value |
|--------|-------|
| Sample size | 1949 |
| Bet count | 1076 |
| Skipped count | 2 |
| Avg model prob | 0.5621 |
| Avg market prob | 0.5325 |
| Brier (model) | 0.2513 |
| Brier (market) | 0.2444 |
| Brier Skill Score | -0.0283 |
| ECE | 0.0352 |
| ROI (%) | 0.20 |
| Max Drawdown (%) | 129.67 |
| Sharpe proxy | 0.0018 |
| Avg edge (%) | 0.0296 |
| Avg Kelly fraction | 0.0255 |

## Source Trace

```json
{
  "strategy_name": "moneyline_edge_threshold_v0_p10_feature_candidate_oof",
  "date_start": "2025-03-01",
  "date_end": "2025-12-31",
  "edge_threshold": 0.01,
  "kelly_cap": 0.05,
  "input_rows_total": 1951,
  "model_prob_source": "column:model_prob_home",
  "market_prob_source": "american_moneyline_pair_to_no_vig(Home ML, Away ML)",
  "rows_parsed": 1949,
  "rows_skipped": 2,
  "missing_market_data": 2,
  "missing_model_data": 0,
  "probability_source_mode": "calibrated_model",
  "real_model_count": 0,
  "calibrated_model_count": 1949,
  "market_proxy_count": 0,
  "missing_model_prob_count": 0,
  "calibration_mode": "walk_forward_oof",
  "oof_calibration_count": 1949,
  "leakage_safe": true,
  "calibration_warning": "walk-forward OOF calibration candidate; production still requires human approval",
  "deployability_note": "OOF calibration with leakage_safe=True; eligible for paper-only candidate evaluation",
  "gate_status": "BLOCKED_NEGATIVE_BSS",
  "sample_size": 1949,
  "bet_count": 1076
}
```

---
*PAPER-ONLY simulation. No real bets placed. No production enablement.*
