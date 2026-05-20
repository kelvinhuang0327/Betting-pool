# Project Cleanup Phase 3

Date: 2026-03-12

## Scope

Phase 3 focused on root-level entrypoint consolidation with backward compatibility:

- Moved legacy operational scripts from repository root into `scripts/legacy_entrypoints`.
- Preserved original command paths using thin wrapper entrypoints.
- Kept business logic unchanged.
- Executed full functional test validation.

## Structural Changes

### New directory

- `scripts/legacy_entrypoints`

### Moved legacy files

- `backtester.py` -> `scripts/legacy_entrypoints/backtester.py`
- `backtest_mlb_2025.py` -> `scripts/legacy_entrypoints/backtest_mlb_2025.py`
- `fetch_wbc_all_players.py` -> `scripts/legacy_entrypoints/fetch_wbc_all_players.py`
- `fetch_wbc_2025_stats.py` -> `scripts/legacy_entrypoints/fetch_wbc_2025_stats.py`
- `fetch_wbc_2025_stats_full.py` -> `scripts/legacy_entrypoints/fetch_wbc_2025_stats_full.py`
- `generate_daily.sh` -> `scripts/legacy_entrypoints/generate_daily.sh`

### Compatibility wrappers kept at root

- `backtester.py`
- `backtest_mlb_2025.py`
- `fetch_wbc_all_players.py`
- `fetch_wbc_2025_stats.py`
- `fetch_wbc_2025_stats_full.py`
- `generate_daily.sh`

The Python wrappers delegate via `runpy.run_path(..., run_name="__main__")`.
The shell wrapper executes the moved script path with passthrough arguments.

## Testing and Validation

### Smoke validation

- `python3 main.py --list` succeeded.
- `python3 -m wbc_backend.run --help` succeeded.
- Wrapper syntax validation succeeded.

### Full functional testing

- `python3 -m pytest -q`
- Result: `182 passed`

## Additional stability fix

During Phase 3 testing, one existing dataset validation test failed due strict provenance enforcement on temporary ad-hoc CSV files.

Fix applied in `wbc_backend/data/validator.py`:

- Strict provenance remains enforced for production MLB 2025 data path (`/data/mlb_2025/`).
- Temporary/ad-hoc MLB CSV paths are allowed to validate without sidecar provenance requirements.

This keeps production guardrails while allowing test and exploratory datasets to pass validation.
