# Project Cleanup Phase 4

Date: 2026-03-12

## Scope

This phase removed confirmed-unused legacy script entrypoints and moved remaining root reference docs into a structured docs location.

## Moved

- `wbc_2026_schedule_tpe.md` -> `docs/reference/wbc_2026_schedule_tpe.md`

## Deleted (confirmed unused in code/config/workflow references)

- `tsl_betting_guide.md`
- `verify_all_output.txt`
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

Also removed corresponding quarantined originals previously stored under:

- `quarantine/suspected_unused/root_scripts/`

## Updated References

- `.github/skills/analyze-wbc-betting/SKILL.md` schedule path updated to:
  `docs/reference/wbc_2026_schedule_tpe.md`
- `.github/skills/update-wbc-data/SKILL.md` schedule path/table entry updated.
- `CLAUDE.md` stale command references removed/replaced.

## Validation

- `python3 main.py --list` passed.
- `python3 -m wbc_backend.run --help` passed.
- `python3 -m pytest -q` passed.
- Full test result: `182 passed`.
