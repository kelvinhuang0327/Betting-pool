# P8 Model Deep Diagnostics Summary
**Generated:** 2026-05-20T09:54:07.209950+00:00

## Core Metrics: Raw vs OOF

| Metric | Raw Model | OOF Calibrated | Delta |
|---|---|---|---|
| BSS | -0.033283 | -0.027668 | +0.005615 |
| ECE | 0.059493 | 0.042928 | -0.016565 |
| Model Brier | 0.255225 | 0.251124 | -0.004101 |
| Market Brier | 0.247004 | 0.244363 | -0.002641 |
| Avg Model Prob | 0.566072 | 0.564784 | -0.001288 |
| Avg Market Prob | 0.518116 | 0.532452 | +0.014336 |
| Avg Home Win Rate | 0.522744 | 0.530528 | +0.007784 |
| Avg Model−Market | 0.047956 | 0.032332 | -0.015624 |
| Usable Rows | 1341 | 1949 | — |

## Orientation Diagnostics

| Orientation | Raw BSS | OOF BSS |
|---|---|---|
| normal | -0.033284 | -0.027668 |
| inverted_model | -0.097697 | -0.073847 |
| swapped_home_away | -0.033284 | -0.027668 |
| **best_orientation** | **normal** | **normal** |


## Join Integrity Audit

- **risk_level:** LOW
- missing_game_id: 0
- duplicate_game_id: 0
- duplicate_date_team_key: 0
- missing_home_team: 0
- missing_away_team: 0
- same_home_away: 0

## Worst Segments (by composite score)

| # | Segment | By | Rows | BSS | ECE | Avg Edge | Reason |
|---|---|---|---|---|---|---|---|
| 1 | extreme_home_bias_>=0.15 | home_bias_bucket | 193 | -0.103586 | 0.159173 | 0.200812 | negative_bss=-0.1036; high_ece=0.1592; high_home_bias_edge=0.2008 |
| 2 | hi_conf_>=0.65 | confidence_bucket | 68 | -0.088249 | 0.160532 | 0.124041 | negative_bss=-0.0882; high_ece=0.1605; high_home_bias_edge=0.1240 |
| 3 | strong_away_bias_<-0.08 | home_bias_bucket | 225 | -0.090722 | 0.126161 | -0.125809 | negative_bss=-0.0907; high_ece=0.1262 |
| 4 | strong_home_bias_0.08-0.15 | home_bias_bucket | 414 | -0.045126 | 0.102897 | 0.112960 | negative_bss=-0.0451; high_ece=0.1029; high_home_bias_edge=0.1130 |
| 5 | 2025-05 | month | 404 | -0.055518 | 0.099233 | 0.088504 | negative_bss=-0.0555; high_ece=0.0992; high_home_bias_edge=0.0885 |
| 6 | away_fav | favorite_side | 669 | -0.043026 | 0.088222 | 0.118496 | negative_bss=-0.0430; high_ece=0.0882; high_home_bias_edge=0.1185 |
| 7 | med_hi_conf_0.60-0.65 | confidence_bucket | 313 | -0.034495 | 0.074625 | 0.080038 | negative_bss=-0.0345; high_ece=0.0746; high_home_bias_edge=0.0800 |
| 8 | 2025-06 | month | 394 | -0.036033 | 0.056512 | 0.032832 | negative_bss=-0.0360; high_ece=0.0565 |
| 9 | low_conf_<0.55 | confidence_bucket | 553 | -0.017820 | 0.050156 | 0.005573 | negative_bss=-0.0178; high_ece=0.0502 |
| 10 | neutral_-0.02-0.02 | home_bias_bucket | 316 | 0.000588 | 0.069800 | -0.000013 | high_ece=0.0698 |

## Probability Diagnostics (OOF)

- model_prob_min: 0.417722
- model_prob_max: 0.660532
- model_prob_std: 0.050702
- market_prob_min: 0.267176
- market_prob_max: 0.774799
- market_prob_std: 0.092671
- overconfident_count: 815
- underconfident_count: 355

## Outcome Diagnostics (OOF rows)

- outcome_one_count: 1034
- outcome_zero_count: 917
- outcome_null_count: 0
- outcome_balance: 0.530000
