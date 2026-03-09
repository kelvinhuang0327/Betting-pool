# WBC/MLB Model Optimization Report

Date: 2026-02-26
Dataset: `data/mlb_2025/mlb_odds_2025_real.csv` (final games with closing odds)
Method: walk-forward (time-ordered), periodic retraining, Platt calibration, EV gating

## Best Robust Configuration (ML market)
- `min_train_games=240`
- `lookback=12`
- `retrain_every=40`
- `ev_threshold=0.03`
- `markets=("ML",)`

## Out-of-Sample Results
- Games evaluated: `2188`
- ML bets: `1462`
- ML ROI: `+0.51%`
- ML hit rate: `45.62%`
- Brier score: `0.2472`
- Log loss: `0.6876`

## Market Validation
- ML ROI: `+0.51%`
- RL ROI: `-3.58%` (best tested threshold still negative)
- OU ROI: `-12.19%` (structurally negative under current model)

## Production Gating Applied
- Positive-ROI market enabled: `ML`
- Negative-ROI markets disabled by quality gate: `RL`, `OU`
- Top-N recommendation engine now only surfaces markets that passed historical validation.

## Generated Artifacts
- `data/wbc_backend/walkforward_summary.json`
- `data/wbc_backend/model_artifacts.json`
- `data/wbc_backend/market_validation.json`
- `data/wbc_backend/tune_results_top10.json`

## Notes
- Current pipeline is now calibrated + backtested with strict time-ordering.
- Achieving very high long-term win rate with positive ROI remains constrained by market efficiency; current approach prioritizes robustness and avoidable loss reduction.

## Feature Engineering Upgrade (Implemented)
- Added starter-vs-lineup split proxies (`platoon_woba_diff`) with optional pitcher/batter split profile files.
- Added starter `K/BB` level + trend features (`starter_kbb_level_diff`, `starter_kbb_trend_diff`).
- Added park factor adjustments (`park_hr_factor`, `park_run_factor`) and integrated into expected runs.
- Added recency bias features (5/10 game rolling means and variances for wins/runs).
- Added `Bullpen Stress Index` proxy from recent close games, heavy runs allowed, and back-to-back usage.

## Hyperparameter / Calibration Upgrade (Implemented)
- Added Time-Series-aware objective path in `wbc_backend/optimization/tuning.py`.
- Added Optuna multi-objective interface: minimize LogLoss, maximize ROI.
- Added calibration comparison framework: Platt vs Isotonic.
- Current environment note: `optuna` is not installed, so full Bayesian search was not executed in this run.

## WBC Rule Engine Upgrade (Implemented)
- Added `WBC_Rule_Engine` in pipeline:
  - pitch-count logic: lowers starter impact and raises bullpen impact under low pitch limits.
  - roster impact: MLB Top-50 star count boosts team strength.
  - small sample correction: Empirical Bayes shrinkage toward league prior strength.

## Betting Strategy Upgrade (Implemented)
- Added Kelly Criterion + Fractional Kelly (default 0.25) with max stake cap.
- Added strict `edge >= 5%` filter.
- Added high-confidence odds band filtering from backtest artifacts.
- Added market quality gating: negative-ROI markets are disabled.
