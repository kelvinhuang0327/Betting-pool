# P208-A Visible MLB Scorecard Result Viewer

**Scope:** LOCAL_HISTORICAL_REPLAY_ONLY

**Disclaimer:** Historical replay/backtest only; not for live use and not a future betting claim.

## Source Artifacts

- `p207a_local_retrain_scorecard.json`
- `p207a_local_retrain_model_comparison.csv`
- `p207a_local_retrain_predictions.csv`

## Model Leaderboard

| Model | Accuracy | Brier | Log Loss | Calibration Error | Coverage | Reference Only |
|---|---:|---:|---:|---:|---:|---|
| `baseline_fixed_prior` | 53.29% | 0.249187 | 0.691524 | 0.016461 | 100.00% | NO |
| `elo_like_rating` | 54.84% | 0.248577 | 0.690391 | 0.048769 | 100.00% | NO |
| `retrained_team_history_smooth` | 56.38% | 0.246063 | 0.685249 | 0.024793 | 100.00% | NO |
| `calibrated_elo_recent_form` | 54.42% | 0.246033 | 0.685080 | 0.020230 | 100.00% | NO |
| `market_implied_devig(REFERENCE_UNVERIFIED)` | 54.73% | 0.245503 | 0.683898 | 0.031829 | 100.00% | YES |

## Best Models

- Best accuracy model: `retrained_team_history_smooth` (56.38%).
- Best Brier model: `calibrated_elo_recent_form` (0.246033).

## Confidence Band Summary

| Band | Rows | Correct | Accuracy |
|---|---:|---:|---:|
| LOW | 442 | 221 | 50.00% |
| MEDIUM | 498 | 285 | 57.23% |
| HIGH | 32 | 23 | 71.88% |

## Selected-Side Distribution

- HOME: 767
- AWAY: 205

## Top Historical Prediction Examples

| Label | Date | Game | Selected Side | Selected Probability | Band | Correct |
|---|---|---|---|---:|---|---:|
| historical replay / backtest only | 2025-09-25 | Colorado Rockies @ Seattle Mariners | HOME | 72.56% | HIGH | 1 |
| historical replay / backtest only | 2025-09-24 | Colorado Rockies @ Seattle Mariners | HOME | 72.16% | HIGH | 1 |
| historical replay / backtest only | 2025-08-23 | San Francisco Giants @ Milwaukee Brewers | HOME | 71.74% | HIGH | 0 |
| historical replay / backtest only | 2025-09-23 | Colorado Rockies @ Seattle Mariners | HOME | 71.73% | HIGH | 1 |
| historical replay / backtest only | 2025-08-22 | San Francisco Giants @ Milwaukee Brewers | HOME | 71.30% | HIGH | 1 |
| historical replay / backtest only | 2025-08-24 | San Francisco Giants @ Milwaukee Brewers | HOME | 69.70% | HIGH | 0 |
| historical replay / backtest only | 2025-08-13 | Pittsburgh Pirates @ Milwaukee Brewers | HOME | 69.48% | HIGH | 1 |
| historical replay / backtest only | 2025-08-12 | Pittsburgh Pirates @ Milwaukee Brewers | HOME | 68.93% | HIGH | 1 |
| historical replay / backtest only | 2025-08-11 | Pittsburgh Pirates @ Milwaukee Brewers | HOME | 68.35% | HIGH | 1 |
| historical replay / backtest only | 2025-08-10 | New York Mets @ Milwaukee Brewers | HOME | 68.31% | HIGH | 1 |
| historical replay / backtest only | 2025-09-27 | Minnesota Twins @ Philadelphia Phillies | HOME | 67.97% | HIGH | 0 |
| historical replay / backtest only | 2025-08-09 | New York Mets @ Milwaukee Brewers | HOME | 67.70% | HIGH | 1 |
