# MLB Prediction Workflow Snapshot

**Scope:** `LOCAL_PAPER_WORKFLOW_SNAPSHOT`

**Disclaimer:** Corrected 2025 date-batched local retraining/evaluation and a separate existing P84-B 2026 prediction snapshot, plus an explicitly separate retrospective P278-A paper-only corrected-model shadow when supplied. Historical odds lack verified pregame timestamps, so Moneyline hit rate, EV, and ROI are diagnostic/descriptive only and do not establish a verified betting edge. The corrected retrained model did not generate or replace the P84-B snapshot, and the P278-A shadow is not a live or pregame publication.

## Corrected 2025 Local Retrain and Evaluation

- Result context: `CORRECTED_2025_LOCAL_DATE_BATCHED_RETRAIN_EVALUATION`
- State transition: `PREDICT_FULL_DATE_THEN_UPDATE`
- Warmup rows: `2429`
- Evaluation rows: `2430`
- Train: `2025-03-18` to `2025-07-18` (1461 games)
- Test: `2025-07-19` to `2025-09-28` (969 games)
- Complete-date counts: train `112`, test `72`
- Train fraction: requested `0.600000`, effective `0.601235`
- Split strategy: `complete_date_boundary_nearest_requested_row_fraction`
- Tie rule: `earlier boundary (smaller train partition) wins equal-distance ties`
- Selected boundary: after `2025-07-18`; test starts `2025-07-19`
- Best by Brier: `retrained_team_history_smooth`

| Model | Accuracy | Brier | Log Loss | ECE |
|---|---:|---:|---:|---:|
| `baseline_fixed_prior` | 0.5325 | 0.2492 | 0.6916 | 0.0171 |
| `elo_like_rating` | 0.5470 | 0.2489 | 0.6911 | 0.0503 |
| `retrained_team_history_smooth` | 0.5635 | 0.2461 | 0.6854 | 0.0251 |
| `calibrated_elo_recent_form` | 0.5418 | 0.2463 | 0.6855 | 0.0233 |

## Corrected 2025 Historical Moneyline Diagnostic

- Historical odds do not have verified pregame timestamps.
- Candidate hit rate, EV, Kelly, and ROI below are descriptive workflow diagnostics, not a verified betting edge or live wagering evidence.
- Odds timing status: `HISTORICAL_ODDS_PREGAME_TIMESTAMP_UNVERIFIED`
- Claim status: `DESCRIPTIVE_DIAGNOSTIC_NOT_VERIFIED_BETTING_EDGE`
- Prediction rows scored: `969`
- Paper candidates: `414` (42.72%)
- Candidate hit rate: `54.59%`
- Net result units: `0.210458`
- ROI on staked units: `3.86%`
- Avg EV per unit: `0.102107`
- Avg Kelly used: `1.32%`
- Backtest CSV: `report/mlb_prediction_workflow_moneyline_backtest.csv`

### Top Historical Paper Rows (Diagnostic Only)

| Date | Game | Side | Sel Prob | Odds | EV | Kelly | Result |
|---|---|---|---:|---:|---:|---:|---:|
| 2025-08-28 | Boston Red Sox @ Baltimore Orioles | HOME | 52.36% | +175 | 0.440 | 1.50% | -0.0150 |
| 2025-09-10 | Pittsburgh Pirates @ Baltimore Orioles | HOME | 59.24% | +130 | 0.363 | 1.50% | 0.0195 |
| 2025-07-28 | Atlanta Braves @ Kansas City Royals | HOME | 54.92% | +145 | 0.346 | 1.50% | -0.0150 |
| 2025-07-21 | San Diego Padres @ Miami Marlins | AWAY | 60.67% | +120 | 0.335 | 1.50% | 0.0180 |
| 2025-08-11 | Boston Red Sox @ Houston Astros | HOME | 56.60% | +135 | 0.330 | 1.50% | 0.0203 |
| 2025-07-26 | Los Angeles Dodgers @ Boston Red Sox | AWAY | 55.11% | +140 | 0.323 | 1.50% | -0.0150 |
| 2025-08-07 | Miami Marlins @ Atlanta Braves | HOME | 59.73% | +120 | 0.314 | 1.50% | 0.0180 |
| 2025-08-27 | Tampa Bay Rays @ Cleveland Guardians | HOME | 58.06% | +125 | 0.306 | 1.50% | 0.0187 |
| 2025-09-17 | Texas Rangers @ Houston Astros | HOME | 57.93% | +125 | 0.304 | 1.50% | 0.0187 |
| 2025-09-23 | Detroit Tigers @ Cleveland Guardians | HOME | 55.19% | +135 | 0.297 | 1.50% | 0.0203 |
| 2025-07-22 | San Diego Padres @ Miami Marlins | AWAY | 60.98% | +110 | 0.281 | 1.50% | -0.0150 |
| 2025-08-29 | Seattle Mariners @ Cleveland Guardians | HOME | 54.35% | +135 | 0.277 | 1.50% | 0.0203 |

## Taiwan Sports Lottery Market Coverage

| Market | Status | Rows With Lines | Coverage |
|---|---|---:|---:|
| `moneyline` | `EVALUATED_IN_WORKFLOW` | 2430 | 100.00% |
| `run_line` | `LINES_AND_RESULTS_AVAILABLE_MODEL_PROBABILITY_PENDING` | 2430 | 100.00% |
| `total_runs` | `LINES_AND_RESULTS_AVAILABLE_MODEL_PROBABILITY_PENDING` | 2430 | 100.00% |
| `first_five` | `NO_LOCAL_F5_LINES_OR_F5_RESULTS_IN_SOURCE` | 0 | 0.00% |

## Existing 2026 Prediction Snapshot (Separate and Stale)

- Result context: `EXISTING_2026_PREDICTION_SNAPSHOT`
- Rows: `828`
- Date range: `['2026-03-25', '2026-05-31']`
- Latest local prediction date: `2026-05-31`
- Snapshot source model/version: `p84b_diagnostic_baseline_v1`
- Freshness status: `STALE_EXISTING_LOCAL_SNAPSHOT`
- Corrected 2025 retrained model generated these 2026 predictions: `False`
- Corrected-model to 2026 prediction handoff: `NOT_PERFORMED`
- Latest prediction CSV: `report/mlb_prediction_workflow_latest_2026_predictions.csv`
- Outcome rows: `828`
- Raw `outcome_available=true` rows: `808`
- P275 gate-available rows: `0`
- Unavailable-before-observation rows: `0`
- Missing/invalid evidence rows: `808`
- Availability coverage limitation: P274 currently has only one prospective record and does not establish season-wide point-in-time coverage or replay readiness.
- Outcome-attached accuracy: `N/A` (0/0)

| Date | Game | Side | Sel Prob | Version |
|---|---|---|---:|---|
| 2026-05-31 | Miami Marlins @ New York Mets | HOME | 57.13% | `p84b_diagnostic_baseline_v1` |

## Corrected 2026 Moneyline Shadow (Separate and Retrospective)

- Status: `AVAILABLE_RETROSPECTIVE_PAPER_ONLY`
- Artifact version: `p278a_corrected_moneyline_shadow_v1`
- Selected algorithm: `retrained_team_history_smooth`
- Rows: `828`
- State mode: `frozen_final_2025_state`
- Retrospective paper-only diagnostic; not a live or verified pregame publication.
- Existing P84-B baseline replaced: `False`
- Champion activated: `False`
- P275 update attempted / allowed / denied / applied: `0` / `0` / `0` / `0`
- Outcome-evaluation denominator: `0`
- Accuracy: `N/A`
- Brier: `N/A`
- ROI / EV / Kelly: `N/A` / `N/A` / `N/A`
- No outcome-based comparative winner or betting edge is declared.

## Output Files

- `markdown`: `report/mlb_prediction_workflow_snapshot.md`
- `json`: `report/mlb_prediction_workflow_snapshot.json`
- `moneyline_csv`: `report/mlb_prediction_workflow_moneyline_backtest.csv`
- `latest_predictions_csv`: `report/mlb_prediction_workflow_latest_2026_predictions.csv`
