# P8 Model Deep Diagnostics Summary
**Generated:** 2026-05-20T09:54:06.814770+00:00

## Core Metrics: Raw vs OOF

| Metric | Raw Model | OOF Calibrated | Delta |
|---|---|---|---|
| BSS | 0.302420 | 0.135162 | -0.167258 |
| ECE | 0.385000 | 0.432500 | +0.047500 |
| Model Brier | 0.151550 | 0.187887 | +0.036337 |
| Market Brier | 0.217251 | 0.217251 | +0.000000 |
| Avg Model Prob | 0.615000 | 0.567500 | -0.047500 |
| Avg Market Prob | 0.533898 | 0.533898 | +0.000000 |
| Avg Home Win Rate | 1.000000 | 1.000000 | +0.000000 |
| Avg Model−Market | 0.081102 | 0.033602 | -0.047500 |
| Usable Rows | 20 | 20 | — |

## Orientation Diagnostics

| Orientation | Raw BSS | OOF BSS |
|---|---|---|
| normal | 0.302419 | 0.135158 |
| inverted_model | -0.756265 | -0.486243 |
| swapped_home_away | -0.756265 | -0.486243 |
| **best_orientation** | **normal** | **normal** |


## Join Integrity Audit

- **risk_level:** LOW
- missing_game_id: 20
- duplicate_game_id: 0
- duplicate_date_team_key: 0
- missing_home_team: 0
- missing_away_team: 0
- same_home_away: 0

## Worst Segments (by composite score)

| # | Segment | By | Rows | BSS | ECE | Avg Edge | Reason |
|---|---|---|---|---|---|---|---|
| 1 | low_conf_<0.55 | confidence_bucket | 6 | -0.006345 | 0.467500 | -0.001398 | negative_bss=-0.0063; high_ece=0.4675 |
| 2 | neutral_-0.02-0.02 | home_bias_bucket | 7 | 0.004261 | 0.465000 | 0.001102 | high_ece=0.4650 |
| 3 | 2025-05 | month | 20 | 0.135158 | 0.432500 | 0.033602 | high_ece=0.4325 |
| 4 | home_fav | favorite_side | 20 | 0.135158 | 0.432500 | 0.033602 | high_ece=0.4325 |
| 5 | med_conf_0.55-0.60 | confidence_bucket | 10 | 0.157828 | 0.427500 | 0.038602 | high_ece=0.4275 |
| 6 | mild_home_bias_0.02-0.08 | home_bias_bucket | 12 | 0.196301 | 0.417500 | 0.048602 | high_ece=0.4175 |
| 7 | med_hi_conf_0.60-0.65 | confidence_bucket | 4 | 0.290739 | 0.392500 | 0.073602 | high_ece=0.3925; high_home_bias_edge=0.0736 |
| 8 | strong_home_bias_0.08-0.15 | home_bias_bucket | 1 | 0.317724 | 0.385000 | 0.081102 | high_ece=0.3850; high_home_bias_edge=0.0811 |

## Probability Diagnostics (OOF)

- model_prob_min: 0.520000
- model_prob_max: 0.615000
- model_prob_std: 0.029580
- market_prob_min: 0.533898
- market_prob_max: 0.533898
- market_prob_std: 0.000000
- overconfident_count: 7
- underconfident_count: 0

## Outcome Diagnostics (OOF rows)

- outcome_one_count: 20
- outcome_zero_count: 0
- outcome_null_count: 0
- outcome_balance: 1.000000
