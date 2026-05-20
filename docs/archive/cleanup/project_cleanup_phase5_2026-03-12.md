# Project Cleanup Phase 5

Date: 2026-03-12

## Scope

Consolidate duplicate Pool report versions by keeping `_v3` files in active report folders and archiving pre-v3 variants.

## Consolidation Rule

- Active canonical version: `*_v3.txt`
- Legacy version (`*.txt` without `_v3`): moved to archive

## Moved to Archive

Destination root:

- `archive/legacy_reports/wbc_backend_reports/pool_pre_v3/`

Moved files:

- `data/wbc_backend/reports/Pool_A/A01.txt`
- `data/wbc_backend/reports/Pool_A/A02.txt`
- `data/wbc_backend/reports/Pool_B/B01.txt`
- `data/wbc_backend/reports/Pool_B/B02.txt`
- `data/wbc_backend/reports/Pool_C/C01.txt`
- `data/wbc_backend/reports/Pool_C/C02.txt`
- `data/wbc_backend/reports/Pool_D/D01.txt`
- `data/wbc_backend/reports/Pool_D/D02.txt`

## Notes

- `last_report.txt` was kept in root because `telegram_bot/bot.py` reads it directly.
- `report/3_9_prediction_c09.md` was kept because other documentation references it.

## Validation

- `python3 main.py --list` passed.
- `python3 -m wbc_backend.run --help` passed.
- `python3 -m pytest -q` passed.
