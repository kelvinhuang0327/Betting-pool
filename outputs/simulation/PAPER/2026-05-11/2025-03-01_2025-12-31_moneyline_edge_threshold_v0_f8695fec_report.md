# Strategy Simulation Report — moneyline_edge_threshold_v0

**Simulation ID:** `sim-moneyline_edge_threshold-f8695fec`  
**Date Range:** 2025-03-01 → 2025-12-31  
**Generated:** 2026-05-11T02:59:08.714746+00:00  
**Paper-Only:** True  

## Gate Status

**`PASS`**

- WARNING: model_prob_home column not found — using market implied prob as proxy. BSS will be ~0 by construction. Do not interpret as model skill.
- No bets placed with edge_threshold=0.010. ROI, Sharpe, and max drawdown cannot be computed.
- Gate: PASS — paper-only simulation. Production enablement requires separate governance clearance.

## Metrics Summary

| Metric | Value |
|--------|-------|
| Sample size | 2428 |
| Bet count | 0 |
| Skipped count | 2 |
| Avg model prob | 0.5325 |
| Avg market prob | 0.5325 |
| Brier (model) | 0.2419 |
| Brier (market) | 0.2419 |
| Brier Skill Score | 0.0000 |
| ECE | 0.0194 |
| ROI (%) | null |
| Max Drawdown (%) | null |
| Sharpe proxy | null |
| Avg edge (%) | 0.0000 |
| Avg Kelly fraction | 0.0000 |

## Source Trace

```json
{
  "strategy_name": "moneyline_edge_threshold_v0",
  "date_start": "2025-03-01",
  "date_end": "2025-12-31",
  "edge_threshold": 0.01,
  "kelly_cap": 0.05,
  "input_rows_total": 2430,
  "model_prob_source": "market_implied_prob_proxy (no model_prob_home column)",
  "market_prob_source": "american_moneyline_pair_to_no_vig(Home ML, Away ML)",
  "rows_parsed": 2428,
  "rows_skipped": 2,
  "missing_market_data": 2,
  "missing_model_data": 0,
  "roi_note": "No bets qualified (edge_threshold=0.010). ROI not available.",
  "gate_status": "PASS",
  "sample_size": 2428,
  "bet_count": 0
}
```

---
*PAPER-ONLY simulation. No real bets placed. No production enablement.*
