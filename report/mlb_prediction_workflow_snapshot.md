# MLB Prediction Workflow Snapshot

**Scope:** `LOCAL_PAPER_WORKFLOW_SNAPSHOT`

**Disclaimer:** Local historical replay and local prediction snapshot only. Paper-market metrics are for workflow validation, not live betting advice.

## Retrain Result

- Warmup rows: `2429`
- Evaluation rows: `2430`
- Train: `2025-03-18` to `2025-07-18` (1458 games)
- Test: `2025-07-18` to `2025-09-28` (972 games)
- Best by Brier: `calibrated_elo_recent_form`

| Model | Accuracy | Brier | Log Loss | ECE |
|---|---:|---:|---:|---:|
| `baseline_fixed_prior` | 0.5329 | 0.2492 | 0.6915 | 0.0165 |
| `elo_like_rating` | 0.5484 | 0.2486 | 0.6904 | 0.0488 |
| `retrained_team_history_smooth` | 0.5638 | 0.2461 | 0.6852 | 0.0248 |
| `calibrated_elo_recent_form` | 0.5442 | 0.2460 | 0.6851 | 0.0202 |

## Moneyline Paper Workflow

- Prediction rows scored: `972`
- Paper candidates: `398` (40.95%)
- Candidate hit rate: `51.26%`
- Net result units: `0.254282`
- ROI on staked units: `4.70%`
- Avg EV per unit: `0.130176`
- Avg Kelly used: `1.36%`
- Backtest CSV: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/report/mlb_prediction_workflow_moneyline_backtest.csv`

### Top Paper Moneyline Candidates

| Date | Game | Side | Sel Prob | Odds | EV | Kelly | Result |
|---|---|---|---:|---:|---:|---:|---:|
| 2025-09-18 | Cleveland Guardians @ Detroit Tigers | AWAY | 50.95% | +200 | 0.528 | 1.50% | 0.0300 |
| 2025-07-28 | Atlanta Braves @ Kansas City Royals | HOME | 62.23% | +145 | 0.525 | 1.50% | -0.0150 |
| 2025-09-23 | Detroit Tigers @ Cleveland Guardians | HOME | 63.98% | +135 | 0.504 | 1.50% | 0.0203 |
| 2025-09-18 | New York Yankees @ Baltimore Orioles | HOME | 53.70% | +175 | 0.477 | 1.50% | -0.0150 |
| 2025-08-25 | Detroit Tigers @ Athletics | HOME | 52.39% | +180 | 0.467 | 1.50% | 0.0270 |
| 2025-09-20 | New York Yankees @ Baltimore Orioles | HOME | 53.73% | +165 | 0.424 | 1.50% | -0.0150 |
| 2025-08-14 | Detroit Tigers @ Minnesota Twins | HOME | 52.91% | +165 | 0.402 | 1.50% | -0.0150 |
| 2025-08-19 | New York Mets @ Washington Nationals | HOME | 52.88% | +165 | 0.401 | 1.50% | -0.0150 |
| 2025-07-20 | Detroit Tigers @ Texas Rangers | HOME | 55.87% | +150 | 0.397 | 1.50% | -0.0150 |
| 2025-09-12 | Detroit Tigers @ Miami Marlins | HOME | 51.13% | +170 | 0.381 | 1.50% | 0.0255 |
| 2025-08-31 | Detroit Tigers @ Kansas City Royals | HOME | 56.35% | +145 | 0.380 | 1.50% | -0.0150 |
| 2025-07-26 | Toronto Blue Jays @ Detroit Tigers | AWAY | 54.82% | +150 | 0.371 | 1.50% | 0.0225 |

## Taiwan Sports Lottery Market Coverage

| Market | Status | Rows With Lines | Coverage |
|---|---|---:|---:|
| `moneyline` | `EVALUATED_IN_WORKFLOW` | 2430 | 100.00% |
| `run_line` | `LINES_AND_RESULTS_AVAILABLE_MODEL_PROBABILITY_PENDING` | 2430 | 100.00% |
| `total_runs` | `LINES_AND_RESULTS_AVAILABLE_MODEL_PROBABILITY_PENDING` | 2430 | 100.00% |
| `first_five` | `NO_LOCAL_F5_LINES_OR_F5_RESULTS_IN_SOURCE` | 0 | 0.00% |

## Local 2026 Prediction Snapshot

- Rows: `828`
- Date range: `['2026-03-25', '2026-05-31']`
- Latest local prediction date: `2026-05-31`
- Latest prediction CSV: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/report/mlb_prediction_workflow_latest_2026_predictions.csv`
- Outcome-attached accuracy: `56.93%` (460/808)

| Date | Game | Side | Sel Prob | Version |
|---|---|---|---:|---|
| 2026-05-31 | Miami Marlins @ New York Mets | HOME | 57.13% | `p84b_diagnostic_baseline_v1` |

## Output Files

- `markdown`: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/report/mlb_prediction_workflow_snapshot.md`
- `json`: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/report/mlb_prediction_workflow_snapshot.json`
- `moneyline_csv`: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/report/mlb_prediction_workflow_moneyline_backtest.csv`
- `latest_predictions_csv`: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/report/mlb_prediction_workflow_latest_2026_predictions.csv`
