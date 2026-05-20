# Governance

Purpose

Rules and decision gates that separate production from research, and define safety controls.

Key Concepts

- Mode governance: `WBC` = production (allowed only when verification gates pass); `MLB` and `Spring` = research/sandbox (no betting).
- Risk controls: Drawdown Adaptive Kelly, Daily Loss Stop, Single Bet Cap, fractional Kelly default 0.25.

Rules / Deployment Gates

- Sample-size gate (WBC): prefer ≥50 WBC-equivalent games for minimal credibility; ideal ≥200 for robust ROI claims.
- Calibration gate: Brier score target (research gate <0.22; conservative gate <0.23).
- Significance gate: Stage4 deploy requires permutation/mcnemar significance vs baseline.
- Stability gate: rolling-window std (policy bound example 0.03); stability regularization required if exceeded.
- Market gate: enable only markets with positive historical ROI and passing market validation (optimization recommends `ev_threshold=0.03`, disable RL/OU if negative ROI observed).

Operational controls

- Bankroll controls: single bet cap 1.5% bankroll, daily loss stop 15%, drawdown-adaptive sizing with max drawdown 20% triggers.
- CI checks: tests, backtest harness, and evidence artifacts required for any migration touching `wbc_backend/*`.

Source

docs/README.md, docs/optimization_report_2026-02-26.md, docs/system_review_report_2026-03-07.md
