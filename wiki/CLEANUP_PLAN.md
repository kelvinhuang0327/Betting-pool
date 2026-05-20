# Cleanup Plan

## Immediate Removal

Current result: no broad immediate removal is safe.

Reasons:

- `main.py` still depends on root `models/`, `strategy/`, and `report/formatter.py`
- `data/tsl_crawler.py` still has active import paths from WBC data loaders
- the worktree currently contains many uncommitted runtime and research changes

## File Classification

### KEEP

| Scope | Current status | Evidence |
| --- | --- | --- |
| `scripts/run_mode.py` | Active runtime | Primary launcher for mode selection |
| `main.py` | Active runtime | Imports root `models/`, `strategy/`, `report/formatter.py` |
| `wbc_backend/run.py` | Active runtime | Pipeline-level WBC runner |
| `scripts/run_mlb_*.py` | Active runtime | Task-specific MLB jobs |
| `scripts/report_center.py`, `scripts/product_dashboard.py`, `scripts/run_postgame_sync.py` | Active runtime | Operational entry scripts |
| `examples/*.py` | Keep | Example and experimentation surface |
| `scripts/legacy_entrypoints/*` | Keep for now | Historical runners still intentionally retained |
| `models/` | Keep | Still imported by `main.py`, `learning/cold_start.py`, and internal legacy stack |
| `strategy/` | Keep | Still imported by `main.py`, `report/formatter.py`, and tests |
| `wbc_backend/models/` | Keep | Active backend model layer |
| `wbc_backend/strategy/` | Keep | Active backend strategy layer |
| `data/wbc_backend/reports/*.json`, `*.jsonl`, `*.csv` | Keep outside wiki | Runtime and research artifacts |
| `docs/reports/postmortem/*` | Keep | Historical review layer |
| `research/postmortem_reports/*` | Keep outside wiki | Generated research artifacts |
| `CLAUDE.md` | Keep | Agent collaboration rules |
| `README.md` | Keep | User-facing top-level documentation |

### MIGRATE_TO_WIKI

| Scope | Current status | Target |
| --- | --- | --- |
| `docs/MODE_GUIDE.md` | Current operational knowledge | Fold into `wiki/ENTRYPOINTS.md` |
| `docs/wbc_backend_architecture.md` | Current architecture knowledge | Fold into `wiki/ARCHITECTURE.md` |
| `docs/roadmap_mirofish_phases.md` | Current migration and system direction context | Summarize in future wiki growth |
| `docs/system_review_report_2026-03-07.md` | Review knowledge | Summarize, keep source in docs |
| `docs/v3_institutional_research_architecture_2026-03-05.md` | Review knowledge | Summarize, keep source in docs |
| `data/wbc_backend/reports/WBC_Review_Meeting_Latest.md` | Knowledge mixed into reports | Migrate content or re-home later |
| `data/wbc_backend/reports/Day1_Summary_V3_Institutional.md` | Knowledge mixed into reports | Migrate content or re-home later |

### BACKUP_AND_ARCHIVE

| Scope | Current status | Action later |
| --- | --- | --- |
| `docs/archive/cleanup/*` | Historical cleanup record | Preserve as archive source |
| `docs/archive/plans/github_telegram_migration_plan.md` | Historical plan | Preserve as archive source |
| legacy operational notes in `docs/` after wiki migration | Historical once canonicalized | Keep in `docs/archive/` or current archive paths |

### DELETE_CANDIDATE

| Scope | Current status | Blocker |
| --- | --- | --- |
| `data/tsl_crawler.py` | Candidate only | Still imported by `data/wbc_data.py` and `data/wbc_pool_[a-d].py` |
| `report/formatter.py` | Candidate only | Still imported by `main.py` |
| selected `_phase*.py` scripts in `scripts/` | Candidate only | Need execution and dependency review first |
| selected debug scripts in `scripts/` | Candidate only | Need usage review first |

## Duplication Map

| Old | Current | Status |
| --- | --- | --- |
| `main.py` | `scripts/run_mode.py` | Legacy wrapper remains active |
| `main.py` | `wbc_backend/run.py` | Different layer; wrapper vs pipeline |
| `models/ensemble.py` | `wbc_backend/models/ensemble.py` and `wbc_backend/models/dynamic_ensemble.py` | Duplicate family; root version still active via legacy path |
| `models/bayesian.py` | `wbc_backend/models/bayesian.py` | Duplicate family; root version still active via legacy path |
| `models/elo.py` | `wbc_backend/models/elo.py` | Duplicate family; root version still active via legacy path |
| `models/poisson.py` | `wbc_backend/models/poisson.py` | Duplicate family; root version still active via legacy path |
| `strategy/kelly_criterion.py` and root strategy stack | `wbc_backend/strategy/*` | Parallel strategy layers; root still active via legacy path |
| `report/formatter.py` | `wbc_backend/reporting/` | Root formatter still active via `main.py` |
| `data/tsl_crawler.py` | `data/tsl_crawler_v2.py` | V2 exists, but V1 still powers WBC data loaders |
| `scripts/legacy_entrypoints/*` | newer `scripts/run_*` surfaces | Historical command set kept alongside newer task runners |

## Dependency Removal First

These areas require dependency removal before any cleanup action:

- root `models/`
- root `strategy/`
- `report/formatter.py`
- `data/tsl_crawler.py`

## Backup Strategy

### Archive Structure

Recommended structure:

- `archive/pre-cleanup-snapshots/`
- `archive/legacy_docs/`
- `archive/legacy_runtime_notes/`

### Snapshot Targets

Before any later cleanup phase, snapshot at least:

- `docs/`
- `models/`
- `strategy/`
- `scripts/legacy_entrypoints/`
- `data/wbc_backend/reports/` knowledge Markdown files
- `report/formatter.py`
- `data/tsl_crawler.py`

### Rollback Strategy

- create a dedicated git tag before cleanup work
- keep file-level backups for mixed knowledge locations
- perform cleanup only after dependency checks and narrow validation
- revert by tag if any later cleanup breaks runner behavior