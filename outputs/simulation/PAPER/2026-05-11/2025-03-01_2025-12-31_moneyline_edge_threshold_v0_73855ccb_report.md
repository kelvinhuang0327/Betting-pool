# Strategy Simulation Report — moneyline_edge_threshold_v0

**Simulation ID:** `sim-moneyline_edge_threshold-73855ccb`  
**Date Range:** 2025-03-01 → 2025-12-31  
**Generated:** 2026-05-11T03:23:00.094957+00:00  
**Paper-Only:** True  

## Gate Status

**`BLOCKED_NEGATIVE_BSS`**

- Brier Skill Score = -0.0188 < 0. Model underperforms market baseline. require_positive_bss=True blocks this strategy.

## Metrics Summary

| Metric | Value |
|--------|-------|
| Sample size | 2428 |
| Bet count | 848 |
| Skipped count | 2 |
| Avg model prob | 0.5590 |
| Avg market prob | 0.5325 |
| Brier (model) | 0.2464 |
| Brier (market) | 0.2419 |
| Brier Skill Score | -0.0188 |
| ECE | 0.0363 |
| ROI (%) | -0.03 |
| Max Drawdown (%) | 113.87 |
| Sharpe proxy | -0.0003 |
| Avg edge (%) | 0.0265 |
| Avg Kelly fraction | 0.0163 |

## Source Trace

```json
{
  "strategy_name": "moneyline_edge_threshold_v0",
  "date_start": "2025-03-01",
  "date_end": "2025-12-31",
  "edge_threshold": 0.01,
  "kelly_cap": 0.05,
  "input_rows_total": 2430,
  "model_prob_source": "column:model_prob_home",
  "market_prob_source": "american_moneyline_pair_to_no_vig(Home ML, Away ML)",
  "rows_parsed": 2428,
  "rows_skipped": 2,
  "missing_market_data": 2,
  "missing_model_data": 0,
  "probability_source_mode": "real_model",
  "real_model_count": 2428,
  "market_proxy_count": 0,
  "missing_model_prob_count": 0,
  "gate_status": "BLOCKED_NEGATIVE_BSS",
  "sample_size": 2428,
  "bet_count": 848
}
```

---
*PAPER-ONLY simulation. No real bets placed. No production enablement.*
