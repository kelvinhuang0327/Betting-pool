# P10 Independent Feature Candidate Export Summary

Generated: 2026-05-11T06:43:15.028770+00:00

## Input
- Input CSV: `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_repaired_features.csv`
- Rows loaded: 2402
- Lookback games: 15
- Candidate mode: `feature_augmented`

## Feature Coverage
- `home_recent_win_rate`: 2387/2402 (99.4%)
- `away_recent_win_rate`: 2387/2402 (99.4%)
- `home_rest_days`: 2284/2402 (95.1%)
- `away_rest_days`: 2287/2402 (95.2%)
- `wind_kmh`: 2080/2402 (86.6%)
- `temp_c`: 2080/2402 (86.6%)
- `starter_era_proxy_away`: 2058/2402 (85.7%)
- `starter_era_proxy_home`: 2080/2402 (86.6%)


## Probability Shift
| Metric | Before (P9 repaired) | After (P10 candidate) |
|--------|---------------------|----------------------|
| avg | 0.4876 | 0.4881 |
| min | 0.1119 | 0.1051 |
| max | 0.8610 | 0.8589 |

## Gate Status
- paper_only: `True`
- leakage_safe: `True`
- production_enabled: `False`
- probability_source: `feature_candidate`

## Output Artifacts
- `outputs/predictions/PAPER/2026-05-11/mlb_independent_features.jsonl`
- `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_independent_features.csv`
- `outputs/predictions/PAPER/2026-05-11/mlb_feature_candidate_probabilities.jsonl`
- `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_feature_candidate_probabilities.csv`
- `outputs/predictions/PAPER/2026-05-11/independent_feature_coverage.json`
