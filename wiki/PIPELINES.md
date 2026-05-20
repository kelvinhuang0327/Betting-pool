# Pipelines (Canonical)

Purpose

Describe production and research pipelines, responsibilities, and canonical entrypoints.

Key Concepts

- Data flow: ingestion → cleaning/validation → feature engineering → modeling/ensemble → WBC rule adjustments → simulation/market calibration → EV selection → reporting.
- Owners: ingestion (`wbc_backend.ingestion`), pipeline runner (`wbc_backend.pipeline` / `wbc_backend.run.py`), API (`wbc_backend.api`), reporting (`wbc_backend.reporting`).

Rules / Constraints

- No look-ahead: all prediction inputs must be pregame snapshots; enforce timestamp monotonicity checks.
- High-risk folders: `data/`, `models/`, and production `wbc_backend/*`—changes require explicit migration plan and backups.
- Production gating: only surface markets that pass model & market gates (sample, Brier/calibration, stability, EV threshold).

Examples

Quick run commands:

```bash
python examples/run_pipeline.py
python wbc_backend/run.py --mode train
python wbc_backend/run.py --mode backtest
```

Backtest artifacts location:

- `data/wbc_backend/walkforward_summary.json`
- `data/wbc_backend/model_artifacts.json`

Source

docs/wbc_backend_architecture.md, docs/v3_institutional_research_architecture_2026-03-05.md, docs/optimization_report_2026-02-26.md

