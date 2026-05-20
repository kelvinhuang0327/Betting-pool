# Architecture

## Current Layers

### Root Layer

The repository root still contains active legacy runtime components:

- `models/`
- `strategy/`
- `report/formatter.py`
- `main.py`

This layer is not archival yet.
It is still imported by the active compatibility path in `main.py` and by a small number of supporting modules and tests.

### `wbc_backend` Layer

`wbc_backend/` is the newer structured backend layer.
It contains the maintained pipeline, model families, reporting surface, UX launchers, evaluation flows, and strategy modules.

This is the target canonical implementation direction, but that direction is not fully enforced yet.

## Current Duplication

The repository currently has parallel implementations in at least these areas:

- root `models/` vs `wbc_backend/models/`
- root `strategy/` vs `wbc_backend/strategy/`
- `main.py` vs `scripts/run_mode.py` vs `wbc_backend/run.py`
- `data/tsl_crawler.py` vs `data/tsl_crawler_v2.py`
- `report/formatter.py` vs `wbc_backend/reporting/`

## Reports Boundary

`data/wbc_backend/reports/` is mixed-use today.
It contains both:

- generated runtime artifacts such as JSON, JSONL, CSV, and per-game deep reports
- a small number of knowledge-oriented Markdown files

This means the directory itself cannot be treated as purely archival or purely canonical knowledge.
Classification must happen file by file.

## Target Direction

The intended direction is:

- keep `wbc_backend/` as the long-term canonical implementation layer
- keep root modules only as long as active imports still require them
- move knowledge into `wiki/` or archived `docs/`
- keep artifacts in `data/`, `report/`, `research/postmortem_reports/`, and `logs/`

## Explicit Non-Goal

This wiki does not declare the migration complete.
It only records the current state and the safe target direction.
No deletion or import refactor is implied by this document.