# Entrypoints & Modes

Purpose

Canonical list of user-facing entrypoints, modes, and quick commands.

Key Concepts

- Primary launcher: `scripts/run_mode.py` — prints mode dashboard and routes to pipeline modes.
- Pipeline runner: `wbc_backend/run.py` — supports `--mode train|backtest|research-cycle`.
- Legacy entrypoint: `main.py` — legacy inference wrapper; treat as legacy until migration.

Modes (canonical)

- `wbc` — Production WBC analysis (only enabled when verification/gates pass).
- `mlb-paper`, `mlb-benchmark`, `mlb-alpha` — research/paper-only modes; not for betting.
- `spring` — sandbox; NOT_RECOMMENDED_FOR_BETTING.

Quick commands

```bash
python scripts/run_mode.py --mode wbc
python scripts/run_mode.py --mode mlb-paper
python scripts/report_center.py
python wbc_backend/run.py --mode backtest
```

Rules / Notes

- If uncertain, run `python scripts/run_mode.py` to get the dashboard and recommended command.
- Do not use `main.py` for production runs; prefer `wbc_backend` runner.

Source

docs/MODE_GUIDE.md, README.md

# Entrypoints

## Primary Entry

### `scripts/run_mode.py`

Status: primary user-facing entrypoint.

Use this when:

- starting a new session in the repository
- choosing between WBC, MLB paper, report center, or spring modes
- needing the supported mode surface without remembering lower-level commands

Why this is primary:

- `README.md` points new users here
- `main.py` explicitly labels this as the preferred canonical launcher
- it routes into the maintained `wbc_backend.ux` launcher layer

Typical usage:

- `python scripts/run_mode.py`
- `python scripts/run_mode.py --mode wbc`
- `python scripts/run_mode.py --mode mlb-paper`

## Secondary Entrypoints

### `main.py`

Status: legacy wrapper that is still active.

Use this only when:

- running legacy WBC single-game flows that still depend on root `models/`, `strategy/`, and `report/formatter.py`
- validating compatibility for the old runtime path

Notes:

- this is not the primary entrypoint
- it still imports the legacy root stack, so it cannot be treated as dead code yet

### `wbc_backend/run.py`

Status: pipeline-level WBC backend entrypoint.

Use this when:

- running backend-oriented WBC analysis directly
- invoking train, backtest, scheduler, improve, or research-cycle flows
- working below the top-level mode launcher

Typical usage:

- `python -m wbc_backend.run`
- `python -m wbc_backend.run --train`
- `python -m wbc_backend.run --backtest`

## Usage Boundary

- User-facing mode selection: `scripts/run_mode.py`
- Legacy single-game compatibility: `main.py`
- Backend WBC pipeline operations: `wbc_backend/run.py`

## Non-Canonical Runners

The following are valid but not canonical top-level entries:

- `scripts/run_mlb_*.py` for task-specific MLB jobs
- `scripts/report_center.py` for report-only access
- `examples/*.py` for examples and experimentation
- `scripts/legacy_entrypoints/*` for retained legacy operational scripts