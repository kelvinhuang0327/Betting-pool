# P10 Independent Feature Candidate Export Summary

Generated: 2026-05-11T05:09:02.866056+00:00

## Input
- Input CSV: `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_repaired_features.csv`
- Rows loaded: 2402
- Lookback games: 15
- Candidate mode: `feature_only`

## Feature Coverage
- `home_recent_win_rate`: 2402/2402 (100.0%)
- `away_recent_win_rate`: 2402/2402 (100.0%)


## Probability Shift
| Metric | Before (P9 repaired) | After (P10 candidate) |
|--------|---------------------|----------------------|
| avg | 0.4876 | 0.5000 |
| min | 0.1119 | 0.5000 |
| max | 0.8610 | 0.5000 |

## Gate Status
- paper_only: `True`
- leakage_safe: `True`
- production_enabled: `False`
- probability_source: `feature_candidate`

## Output Artifacts
- `outputs/predictions/PAPER/2026-05-11/feature_only/mlb_independent_features.jsonl`
- `outputs/predictions/PAPER/2026-05-11/feature_only/mlb_odds_with_independent_features.csv`
- `outputs/predictions/PAPER/2026-05-11/feature_only/mlb_feature_candidate_probabilities.jsonl`
- `outputs/predictions/PAPER/2026-05-11/feature_only/mlb_odds_with_feature_candidate_probabilities.csv`
- `outputs/predictions/PAPER/2026-05-11/feature_only/independent_feature_coverage.json`
