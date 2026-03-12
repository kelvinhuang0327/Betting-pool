# Project Cleanup Phase 6

Date: 2026-03-12

## Scope

Final integration of intentionally retained root wrappers.

## Removed Root Wrappers

- `backtester.py`
- `backtest_mlb_2025.py`
- `fetch_wbc_all_players.py`
- `fetch_wbc_2025_stats.py`
- `fetch_wbc_2025_stats_full.py`
- `generate_daily.sh`

Canonical script locations remain:

- `scripts/legacy_entrypoints/backtester.py`
- `scripts/legacy_entrypoints/backtest_mlb_2025.py`
- `scripts/legacy_entrypoints/fetch_wbc_all_players.py`
- `scripts/legacy_entrypoints/fetch_wbc_2025_stats.py`
- `scripts/legacy_entrypoints/fetch_wbc_2025_stats_full.py`
- `scripts/legacy_entrypoints/generate_daily.sh`

## Reference Updates

- `.github/workflows/daily_update.yml`
  - now runs `python scripts/legacy_entrypoints/fetch_wbc_all_players.py`
- `.github/skills/update-wbc-data/SKILL.md`
  - updated all fetch command examples to `scripts/legacy_entrypoints/...`
- `docs/github_telegram_migration_plan.md`
  - updated Daily Data Sync command path
- `wbc_backend/research/system_audit.py`
  - updated backtest script path reference

## Validation

- `python3 main.py --list` passed.
- `python3 -m wbc_backend.run --help` passed.
- `python3 -m pytest -q` passed (`182 passed`).

## Result

Repository root now keeps only core entrypoint/config/module folders and no legacy wrapper script clutter.
