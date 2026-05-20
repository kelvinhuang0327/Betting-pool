# P10 Independent Feature Candidate Export Summary

Generated: 2026-05-20T09:54:05.159136+00:00

## Input
- Input CSV: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/predictions/PAPER/2026-05-11/mlb_odds_with_repaired_features.csv`
- Rows loaded: 2402
- Lookback games: 15
- Candidate mode: `feature_augmented`

## Feature Coverage
- `bullpen_proxy`: 2346/2402 (97.7%)
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
| avg | 0.4876 | 0.4855 |
| min | 0.1119 | 0.0730 |
| max | 0.8610 | 0.9023 |

## Gate Status
- paper_only: `True`
- leakage_safe: `True`
- production_enabled: `False`
- probability_source: `feature_candidate`

## Output Artifacts
- `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/predictions/PAPER/_test_p10_feature_candidate/mlb_independent_features.jsonl`
- `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/predictions/PAPER/_test_p10_feature_candidate/mlb_odds_with_independent_features.csv`
- `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/predictions/PAPER/_test_p10_feature_candidate/mlb_feature_candidate_probabilities.jsonl`
- `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/predictions/PAPER/_test_p10_feature_candidate/mlb_odds_with_feature_candidate_probabilities.csv`
- `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/predictions/PAPER/_test_p10_feature_candidate/independent_feature_coverage.json`
