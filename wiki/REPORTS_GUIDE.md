# Reports Guide

Purpose

Explain how reports and generated analysis are preserved, summarized, and used as evidence without being moved into the wiki.

Key Concepts

- Reports remain authoritative artifacts and live in `data/` or `archive/`.
- Wiki holds concise summaries, repeated failure patterns, and decision-level insights extracted from reports.

Summary Template (for each report)

- Title, date
- Primary verdict (PASS/FAIL)
- Key numeric evidence (sample n, brier, p-values)
- Action items (who, what, when)

Extracted Patterns (examples)

- Small-sample risk: low `n` (e.g., 40 pregame snapshots) produces high variance; prefer aggregating similar regimes before deciding.
- Calibration drift: recurring cause of negative ROI on positive-edge bets — requires Platt/Isotonic recalibration and monitoring.
- Regime failure: disable regimes with persistent negative ROI once sample threshold is met.
- Crawler/version drift: ensure active crawler version and align ingestion modules; misaligned crawler versions cause gating failures.
- Market gating: enable markets only after ROI + backtest + market-quality gate; RL/OU often fail under current models.

Where to find reports

- Active reports: `data/wbc_backend/reports/`
- Deep generated reports: `archive/legacy_reports/wbc_backend_reports/generated_outputs/`
- Postmortems: `research/postmortem_reports/`, `docs/reports/postmortem/`

How to use a report as evidence

1. Create a short summary using the template and add to this page or `wiki/RESEARCH_LAYER.md`.
2. Link to the original artifact path. Do not copy content into wiki.
3. Extract numeric gates and update `wiki/GOVERNANCE.md` if thresholds change.

Source

wbc_research_report.md, research/postmortem_reports/*, docs/optimization_report_2026-02-26.md
