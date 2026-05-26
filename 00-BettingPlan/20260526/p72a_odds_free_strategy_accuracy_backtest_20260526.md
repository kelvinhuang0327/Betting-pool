# P72A — Odds-Free Strategy Accuracy Backtest

**Date**: 2026-05-26  
**Classification**: `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED`

---

## Pre-flight

| Check | Value |
|---|---|
| Repo | /Users/kelvin/Kelvin-WorkSpace/Betting-pool |
| Branch | main |
| HEAD | 1d8adb8 |
| paper_only | True |
| uses_historical_odds | **False** |
| the_odds_api_key_required | **False** |

---

## Source Artifacts

- `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` — 2025 games (2025-04-27 to 2025-09-28)
- Months covered: 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09
- Empirical home win rate: 0.5299

---

## ⚠️ Interpretation Note

These metrics measure outcome-prediction accuracy only. A hit rate above random baseline or AUC > 0.50 means the model has directional predictive skill. This does NOT imply positive EV against market odds. Market edge requires comparing model probabilities to odds-implied probabilities, which is a separate analysis requiring historical odds data.

**This analysis does NOT use odds, does NOT calculate EV or CLV, 
and does NOT constitute a betting recommendation.**

---

## Strategies Evaluated

| Strategy | Description | Threshold |
|---|---|---|
| `S00_BASELINE_ALL` | Baseline: all games, model_home_prob predicts home win | 0.0 |
| `S01_TIER_C_DIRECTIONAL` | Tier C directional: |sp_fip_delta|>=0.50, pick team model favors | 0.5 |
| `S02_TIER_B_DIRECTIONAL` | Tier B directional: |sp_fip_delta|>=1.25, pick team model favors | 1.25 |
| `S03_TIER_A_DIRECTIONAL` | Tier A directional: |sp_fip_delta|>=1.50, pick team model favors | 1.5 |
| `S04_TIER_C_PLATT_CALIBRATED` | Tier C with Platt-calibrated prob (P45 locked constants) | 0.5 |
| `S05_HOME_FAVOR_STRONG` | sp_fip_delta >= 0.50 (home team strongly favored by FIP delta) | 0.5 |
| `S06_AWAY_FAVOR_STRONG` | sp_fip_delta <= -0.50 (away team strongly favored by FIP delta) | 0.5 |

---

## Metrics Table

| Strategy | n | Coverage | Hit Rate | AUC | Brier | Log-Loss | ECE | Signal |
|---|---|---|---|---|---|---|---|---|
| `S00_BASELINE_ALL` | 2025 | 1.0 | 0.5299 | 0.5716 | 0.2447 | 0.6822 | 0.031 | **PREDICTIVE_SIGNAL_CONFIRMED** |
| `S01_TIER_C_DIRECTIONAL` | 535 | 0.2642 | 0.6056 | 0.5834 | 0.2385 | 0.6693 | 0.0685 | **PREDICTIVE_SIGNAL_CONFIRMED** |
| `S02_TIER_B_DIRECTIONAL` | 98 | 0.0484 | 0.5918 | 0.6461 | 0.2306 | 0.6532 | 0.0662 | **PREDICTIVE_SIGNAL_CONFIRMED** |
| `S03_TIER_A_DIRECTIONAL` | 24 | 0.0119 | 0.7083 | 0.5546 | 0.2322 | 0.6563 | 0.1852 | **PREDICTIVE_SIGNAL_WEAK** |
| `S04_TIER_C_PLATT_CALIBRATED` | 535 | 0.2642 | 0.5664 | 0.5932 | 0.2405 | 0.6738 | 0.0292 | **PREDICTIVE_SIGNAL_CONFIRMED** |
| `S05_HOME_FAVOR_STRONG` | 268 | 0.1323 | 0.6716 | 0.5591 | 0.2292 | 0.6504 | 0.0983 | **PREDICTIVE_SIGNAL_WEAK** |
| `S06_AWAY_FAVOR_STRONG` | 267 | 0.1319 | 0.5393 | 0.545 | 0.2478 | 0.6884 | 0.0396 | **PREDICTIVE_SIGNAL_WEAK** |

Hit Rate CI (95%) and AUC CI (95%) from bootstrap (n_boot=2000/1000, seed=42):

| Strategy | Hit Rate | HR CI [lo, hi] | AUC | AUC CI [lo, hi] |
|---|---|---|---|---|
| `S00_BASELINE_ALL` | 0.5299 | [0.5086, 0.5521] | 0.5716 | [0.5467, 0.5966] |
| `S01_TIER_C_DIRECTIONAL` | 0.6056 | [0.5645, 0.6449] | 0.5834 | [0.538, 0.6335] |
| `S02_TIER_B_DIRECTIONAL` | 0.5918 | [0.4898, 0.6837] | 0.6461 | [0.5346, 0.7555] |
| `S03_TIER_A_DIRECTIONAL` | 0.7083 | [0.5, 0.875] | 0.5546 | [0.3182, 0.7899] |
| `S04_TIER_C_PLATT_CALIBRATED` | 0.5664 | [0.5234, 0.6093] | 0.5932 | [0.5459, 0.6379] |
| `S05_HOME_FAVOR_STRONG` | 0.6716 | [0.6157, 0.7276] | 0.5591 | [0.4845, 0.6281] |
| `S06_AWAY_FAVOR_STRONG` | 0.5393 | [0.4831, 0.5993] | 0.545 | [0.475, 0.6107] |

---

## Monthly Stability Table

| Strategy | Month | n | Hit Rate | Brier |
|---|---|---|---|---|
| `S00_BASELINE_ALL` | 2025-04 | 53 | 0.566 | 0.2217 |
| `S00_BASELINE_ALL` | 2025-05 | 411 | 0.5158 | 0.242 |
| `S00_BASELINE_ALL` | 2025-06 | 397 | 0.5139 | 0.2513 |
| `S00_BASELINE_ALL` | 2025-07 | 369 | 0.5583 | 0.2481 |
| `S00_BASELINE_ALL` | 2025-08 | 421 | 0.5249 | 0.2448 |
| `S00_BASELINE_ALL` | 2025-09 | 374 | 0.5348 | 0.2405 |
| `S01_TIER_C_DIRECTIONAL` | 2025-04 | 16 | 0.625 | 0.2469 |
| `S01_TIER_C_DIRECTIONAL` | 2025-05 | 120 | 0.575 | 0.2341 |
| `S01_TIER_C_DIRECTIONAL` | 2025-06 | 101 | 0.6634 | 0.2404 |
| `S01_TIER_C_DIRECTIONAL` | 2025-07 | 92 | 0.6196 | 0.2411 |
| `S01_TIER_C_DIRECTIONAL` | 2025-08 | 108 | 0.5648 | 0.2449 |
| `S01_TIER_C_DIRECTIONAL` | 2025-09 | 98 | 0.6122 | 0.2309 |
| `S02_TIER_B_DIRECTIONAL` | 2025-04 | 2 | 0.5 | N/A |
| `S02_TIER_B_DIRECTIONAL` | 2025-05 | 23 | 0.5652 | 0.2267 |
| `S02_TIER_B_DIRECTIONAL` | 2025-06 | 21 | 0.6667 | 0.2338 |
| `S02_TIER_B_DIRECTIONAL` | 2025-07 | 14 | 0.7143 | 0.2403 |
| `S02_TIER_B_DIRECTIONAL` | 2025-08 | 20 | 0.55 | 0.2078 |
| `S02_TIER_B_DIRECTIONAL` | 2025-09 | 18 | 0.5 | 0.2422 |
| `S03_TIER_A_DIRECTIONAL` | 2025-04 | 1 | 0.0 | N/A |
| `S03_TIER_A_DIRECTIONAL` | 2025-05 | 9 | 0.7778 | 0.2331 |
| `S03_TIER_A_DIRECTIONAL` | 2025-06 | 8 | 0.875 | 0.2192 |
| `S03_TIER_A_DIRECTIONAL` | 2025-07 | 2 | 1.0 | N/A |
| `S03_TIER_A_DIRECTIONAL` | 2025-08 | 1 | 0.0 | N/A |
| `S03_TIER_A_DIRECTIONAL` | 2025-09 | 3 | 0.3333 | N/A |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-04 | 16 | 0.5 | 0.2527 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-05 | 120 | 0.575 | 0.2378 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-06 | 101 | 0.5545 | 0.2401 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-07 | 92 | 0.587 | 0.2391 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-08 | 108 | 0.5463 | 0.2474 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-09 | 98 | 0.5816 | 0.2357 |
| `S05_HOME_FAVOR_STRONG` | 2025-04 | 8 | 0.625 | 0.2229 |
| `S05_HOME_FAVOR_STRONG` | 2025-05 | 62 | 0.6452 | 0.225 |
| `S05_HOME_FAVOR_STRONG` | 2025-06 | 50 | 0.72 | 0.2436 |
| `S05_HOME_FAVOR_STRONG` | 2025-07 | 45 | 0.7111 | 0.2294 |
| `S05_HOME_FAVOR_STRONG` | 2025-08 | 54 | 0.6111 | 0.2328 |
| `S05_HOME_FAVOR_STRONG` | 2025-09 | 49 | 0.6939 | 0.2165 |
| `S06_AWAY_FAVOR_STRONG` | 2025-04 | 8 | 0.625 | 0.2709 |
| `S06_AWAY_FAVOR_STRONG` | 2025-05 | 58 | 0.5 | 0.2438 |
| `S06_AWAY_FAVOR_STRONG` | 2025-06 | 51 | 0.6078 | 0.2373 |
| `S06_AWAY_FAVOR_STRONG` | 2025-07 | 47 | 0.5319 | 0.2524 |
| `S06_AWAY_FAVOR_STRONG` | 2025-08 | 54 | 0.5185 | 0.2569 |
| `S06_AWAY_FAVOR_STRONG` | 2025-09 | 49 | 0.5306 | 0.2453 |

---

## Thirds Stability

| Strategy | Third | n | Hit Rate |
|---|---|---|---|
| `S00_BASELINE_ALL` | 1 | 675 | 0.5274 |
| `S00_BASELINE_ALL` | 2 | 675 | 0.5259 |
| `S00_BASELINE_ALL` | 3 | 675 | 0.5363 |
| `S01_TIER_C_DIRECTIONAL` | 1 | 178 | 0.6011 |
| `S01_TIER_C_DIRECTIONAL` | 2 | 178 | 0.6292 |
| `S01_TIER_C_DIRECTIONAL` | 3 | 179 | 0.5866 |
| `S02_TIER_B_DIRECTIONAL` | 1 | 32 | 0.5625 |
| `S02_TIER_B_DIRECTIONAL` | 2 | 33 | 0.6667 |
| `S02_TIER_B_DIRECTIONAL` | 3 | 33 | 0.5455 |
| `S03_TIER_A_DIRECTIONAL` | 1 | 8 | 0.75 |
| `S03_TIER_A_DIRECTIONAL` | 2 | 8 | 0.75 |
| `S03_TIER_A_DIRECTIONAL` | 3 | 8 | 0.625 |
| `S04_TIER_C_PLATT_CALIBRATED` | 1 | 178 | 0.5618 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2 | 178 | 0.5787 |
| `S04_TIER_C_PLATT_CALIBRATED` | 3 | 179 | 0.5587 |
| `S05_HOME_FAVOR_STRONG` | 1 | 89 | 0.6517 |
| `S05_HOME_FAVOR_STRONG` | 2 | 89 | 0.7303 |
| `S05_HOME_FAVOR_STRONG` | 3 | 90 | 0.6333 |
| `S06_AWAY_FAVOR_STRONG` | 1 | 89 | 0.5281 |
| `S06_AWAY_FAVOR_STRONG` | 2 | 89 | 0.5506 |
| `S06_AWAY_FAVOR_STRONG` | 3 | 89 | 0.5393 |

---

## Best and Worst Strategy

- **Best predictive strategy**: `S02_TIER_B_DIRECTIONAL`
- **Worst predictive strategy**: `S06_AWAY_FAVOR_STRONG`

---

## Failure Segment Analysis

| Strategy | Worst Month | Best Month | Home Hit | Away Hit | Tier C | Tier B | Tier A |
|---|---|---|---|---|---|---|---|
| `S00_BASELINE_ALL` | 2025-06 | 2025-04 | 0.5299 | None | 0.5664 | 0.6327 | 0.5417 |
| `S01_TIER_C_DIRECTIONAL` | 2025-08 | 2025-06 | 0.6716 | 0.5393 | 0.6056 | 0.5918 | 0.7083 |
| `S02_TIER_B_DIRECTIONAL` | 2025-04 | 2025-07 | 0.72 | 0.4583 | 0.5918 | 0.5918 | 0.7083 |
| `S03_TIER_A_DIRECTIONAL` | 2025-04 | 2025-07 | 0.75 | 0.6667 | 0.7083 | 0.7083 | 0.7083 |
| `S04_TIER_C_PLATT_CALIBRATED` | 2025-04 | 2025-07 | 0.5664 | None | 0.5664 | 0.6327 | 0.5417 |
| `S05_HOME_FAVOR_STRONG` | 2025-08 | 2025-06 | 0.6716 | None | 0.6716 | 0.72 | 0.75 |
| `S06_AWAY_FAVOR_STRONG` | 2025-05 | 2025-04 | None | 0.5393 | 0.5393 | 0.4583 | 0.6667 |

---

## Governance

| Field | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| uses_historical_odds | False |
| live_api_calls | 0 |
| paid_api_called | False |
| the_odds_api_key_required | False |
| market_edge_calculated | False |
| ev_calculated | False |
| clv_calculated | False |
| kelly_deploy_allowed | False |
| production_ready | False |
| real_bet_allowed | False |
| champion_replacement_allowed | False |
| profitability_claim | False |

---

## Key Disclaimers

- **Odds used**: NO — this backtest uses no betting odds.
- **API key required**: NO — `the_odds_api_key_required=False`.
- **EV / CLV**: NOT calculated. Accuracy != profitability.
- **Betting recommendation**: This is a diagnostic accuracy study, NOT a betting strategy.
- Positive AUC or hit rate above baseline means the model has directional skill.
  It does NOT mean bets on this model would be profitable against market lines.

---

## Final Classification: `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED`

---

## CTO Agent 10-Line Summary

1. Source: 2025 MLB 2025 games (Apr–Sep), zero odds data used.
2. 7 strategies evaluated: ALL, Tier C/B/A directional, Tier C Platt, Home/Away strong.
3. Best strategy by AUC: `S02_TIER_B_DIRECTIONAL`.
4. Worst strategy by AUC: `S06_AWAY_FAVOR_STRONG`.
5. Empirical home win baseline: 0.530 — used as random baseline reference.
6. All metrics are accuracy-only: hit rate, AUC, Brier, log-loss, ECE.
7. No EV, CLV, Kelly, or profit/ROI calculated — those require odds data.
8. Monthly stability and thirds stability reported per strategy.
9. Interpretation: AUC > 0.50 = directional skill; does NOT imply +EV vs market.
10. P72A classification: `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED`.

*paper_only=True | diagnostic_only=True | uses_historical_odds=False | live_api_calls=0*
