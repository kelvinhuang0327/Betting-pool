# Strategy Simulation Report — moneyline_edge_threshold_v0_oof_calibrated

**Simulation ID:** `sim-moneyline_edge_threshold-ed059d96`  
**Date Range:** 2025-03-01 → 2025-12-31  
**Generated:** 2026-05-11T04:27:37.154857+00:00  
**Paper-Only:** True  

## Gate Status

**`BLOCKED_NEGATIVE_BSS`**

- Brier Skill Score = -0.0133 < 0. Model underperforms market baseline. require_positive_bss=True blocks this strategy.

## Metrics Summary

| Metric | Value |
|--------|-------|
| Sample size | 1162 |
| Bet count | 383 |
| Skipped count | 2 |
| Avg model prob | 0.5349 |
| Avg market prob | 0.5311 |
| Brier (model) | 0.2482 |
| Brier (market) | 0.2449 |
| Brier Skill Score | -0.0133 |
| ECE | 0.0148 |
| ROI (%) | 2.75 |
| Max Drawdown (%) | 79.07 |
| Sharpe proxy | 0.0246 |
| Avg edge (%) | 0.0038 |
| Avg Kelly fraction | 0.0139 |

## Source Trace

```json
{
  "strategy_name": "moneyline_edge_threshold_v0_oof_calibrated",
  "date_start": "2025-03-01",
  "date_end": "2025-12-31",
  "edge_threshold": 0.01,
  "kelly_cap": 0.05,
  "input_rows_total": 1164,
  "model_prob_source": "column:model_prob_home",
  "market_prob_source": "american_moneyline_pair_to_no_vig(Home ML, Away ML)",
  "rows_parsed": 1162,
  "rows_skipped": 2,
  "missing_market_data": 2,
  "missing_model_data": 0,
  "probability_source_mode": "calibrated_model",
  "real_model_count": 0,
  "calibrated_model_count": 1162,
  "market_proxy_count": 0,
  "missing_model_prob_count": 0,
  "calibration_mode": "walk_forward_oof",
  "oof_calibration_count": 1162,
  "leakage_safe": true,
  "calibration_warning": "walk-forward OOF calibration candidate; production still requires human approval",
  "deployability_note": "OOF calibration with leakage_safe=True; eligible for paper-only candidate evaluation",
  "gate_status": "BLOCKED_NEGATIVE_BSS",
  "sample_size": 1162,
  "bet_count": 383
}
```

---
*PAPER-ONLY simulation. No real bets placed. No production enablement.*
