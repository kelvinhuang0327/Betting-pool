# Project Cleanup Phase 2

Date: 2026-03-12

## Scope

This phase isolated suspected-unused root scripts while preserving command compatibility.
It also fixed stale documentation command references.

No prediction logic, API contracts, model behavior, or package imports were changed.

## Quarantine Target

- `quarantine/suspected_unused/root_scripts`

## Moved Files

- `analyze_wbc_arbitrage.py`
- `fetch_tsl.py`
- `fetch_wbc_players_test.py`
- `fetch_wbc_stats_test.py`
- `simulate_compound_betting.py`
- `simulate_tpe_aus_2025.py`
- `simulate_wbc_spread.py`
- `verify_phase1.py`
- `verify_phase2.py`
- `verify_phase3.py`

All files above were moved into:

- `quarantine/suspected_unused/root_scripts/`

## Compatibility Strategy

For each moved root script, a thin compatibility launcher was recreated at the original path.
Each launcher forwards execution to the quarantined file using `runpy.run_path(..., run_name="__main__")`.

This preserves existing command usage such as:

- `python simulate_wbc_spread.py`
- `python verify_phase1.py`

## Documentation Fixes

- `CLAUDE.md`
  - Updated Telegram startup command from `python telegram_bot/main.py` to `python telegram_bot/bot.py`.
  - Updated report command from `python verify_all_output.txt` to `cat verify_all_output.txt`.
  - Added note that `simulate_wbc_spread.py` is served via compatibility launcher.

- `docs/github_telegram_migration_plan.md`
  - Updated Daily Data Sync reference from `fetch_wbc_players_test.py` to `fetch_wbc_all_players.py`.
  - Updated live updater path to `data/live_updater.py`.

## Validation

- Compatibility launcher files compile under Python.
- Test discovery still succeeds (`pytest --collect-only`).
- Core runtime report archive path from Phase 1 remains present.
- Added `pytest.ini` to keep test collection scoped to `tests/` and to exclude `archive/quarantine/build`.

## Risk Notes

- These scripts were marked suspected-unused based on current repo references, not runtime telemetry.
- Launchers reduce break risk, but downstream behavior still depends on each script's original assumptions.
