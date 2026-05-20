# Research Layer

Purpose

Capture research practices, experimental controls, gating rules and reusable insights from reports.

Key Concepts

- Research phases: functional audit → feature expansion → methodological expansion → portfolio upgrade → infra stabilization (see `v3` phase plan).
- Gating checklist (canonical): sample size threshold, calibration (Brier), statistical significance, rolling stability (rolling std), and EV/ROI checks.

Rules / Constraints

- WBC sample guidance: treat small-sample results conservatively; prefer >50 WBC-equivalent games for credible conclusions (ideal ≥200 for stable ROI claims).
- Model gating numerics (extracted):
	- Brier thresholds: preferred <0.22 (research gate), <0.23 considered minimal for WBC credible backtest.
	- Optimization params (for ML markets): `min_train_games=240`, `lookback=12`, `retrain_every=40`, `ev_threshold=0.03`.
	- Walk-forward evaluation: time-ordered retraining, no synthetic leakage.

Patterns & Insights (from reports)

- Small-sample risk: many postmortems show noise-driven negatives when `n` is very small.
- Calibration drift: recurring cause of negative ROI on positive-edge bets — requires periodic Platt/Isotonic recalibration and monitoring.
- Regime failures: when a regime shows persistent negative ROI, mute or disable until sample grows.
- Crawler/version drift: data ingestion mismatches (v1 vs v2) cause downstream gating failures and false negatives.

Examples / How-to

- Reproducible replay: use `data/wbc_backend/artifacts/v3_research_cycle.json` + `wbc_backend/research/execution.py` with `--research-cycle`.
- Holdout A/B: run the holdout against Bayesian baseline before Stage4 deploy.

Source

docs/wbc_backend_architecture.md, wbc_research_report.md, docs/optimization_report_2026-02-26.md, research/postmortem_reports/*

Extracted research summary (from `wbc_research_report.md`):
- Evaluable sample: 40 pregame snapshots
- Ensemble Brier: 0.141523 (passed 0.22 threshold) but Stage4 deployment significance = FAIL
- Action: keep cap, run A/B holdout, add stability regularization
