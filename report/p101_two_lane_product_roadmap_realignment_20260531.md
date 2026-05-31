
# P101 Two-Lane Product Roadmap Re-alignment — 2026-05-31

## Final Classification
P101_TWO_LANE_ROADMAP_READY_DIAGNOSTIC_ONLY

## Lane A — Taiwan Sports Lottery Pregame Market Contract
- Supported markets: moneyline (winner)
- Run line, total runs, first five innings: blocked (future odds required)
- Required fields: game_id, predicted_side, source_trace, odds
- Recommendation: BLOCKED if legal odds missing
- No odds/EV/CLV/Kelly/recommendation/production

## Lane B — Outcome-Only Strategy Backtest and Learning Plan
- Strategies: HIGH_FIP (diagnostic), MID/LOW (watch-only)
- Scorecard: hit_rate, AUC, Brier, ECE, monthly_stability, side_split, rolling_drift
- Strategy comparison matrix: included
- Learning loop: based on prediction success rate (paper-only)
- Win/loss/score simulation: if data supports
- No calibration refit or production mutation

## Governance
- paper_only=true
- diagnostic_only=true
- production_ready=false
- recommendation_allowed=false
- odds_used=false
- ev_computed=false
- clv_computed=false
- kelly_computed=false
- stake_sizing=false

