# Project Cleanup Phase 1

Date: 2026-03-12

## Scope

This phase performed low-risk repository cleanup only:

- Archived obvious root-level output files.
- Archived legacy report artifacts.
- Quarantined OS junk files.
- Preserved runtime compatibility for existing report archive paths.

No application logic, imports, API behavior, or model code was changed.

## Created Directories

- `archive/root_reports`
- `archive/legacy_reports/wbc_backend_reports`
- `quarantine/os_junk`
- `build/runtime_artifacts`

## Moved Files

### Root reports archived

- `a01_report.txt` -> `archive/root_reports/a01_report.txt`
- `b01_report.txt` -> `archive/root_reports/b01_report.txt`
- `c03_report.txt` -> `archive/root_reports/c03_report.txt`
- `backtest_results_real_2025.txt` -> `archive/root_reports/backtest_results_real_2025.txt`
- `backtest_results_sure_bets.txt` -> `archive/root_reports/backtest_results_sure_bets.txt`
- `output.txt` -> `archive/root_reports/output.txt`
- `output_mlb_v3.txt` -> `archive/root_reports/output_mlb_v3.txt`
- `report_output.txt` -> `archive/root_reports/report_output.txt`
- `simulation_output.txt` -> `archive/root_reports/simulation_output.txt`

### Legacy WBC backend reports archived

- `data/wbc_backend/reports/Daily_2026-03-03.md` -> `archive/legacy_reports/wbc_backend_reports/Daily_2026-03-03.md`
- `data/wbc_backend/reports/Day1_Summary_V2.md` -> `archive/legacy_reports/wbc_backend_reports/Day1_Summary_V2.md`
- `data/wbc_backend/reports/Pool_Day1_Reports.tar.gz` -> `archive/legacy_reports/wbc_backend_reports/Pool_Day1_Reports.tar.gz`
- `data/wbc_backend/reports/review_archive/` -> `archive/legacy_reports/wbc_backend_reports/review_archive/`

### OS junk quarantined

- `.DS_Store` -> `quarantine/os_junk/root.DS_Store`
- `data/.DS_Store` -> `quarantine/os_junk/data.DS_Store`
- `data/wbc_backend/.DS_Store` -> `quarantine/os_junk/data_wbc_backend.DS_Store`
- `wbc_backend/.DS_Store` -> `quarantine/os_junk/wbc_backend.DS_Store`

## Compatibility Notes

- `last_report.txt` was not moved because `telegram_bot/bot.py` reads it directly.
- `verify_all_output.txt` was not moved because project documentation still references it.
- `data/wbc_backend/reports/review_archive/` was recreated as an empty directory after archival because runtime settings still point to that path.

## Deferred to Later Phases

- Consolidating duplicate model and strategy implementations.
- Moving suspected unused scripts into a quarantine area.
- Fixing documentation drift such as stale command references.
- Reorganizing core source directories.

## Validation Checklist

- Files moved only from low-risk output/archive categories.
- No core Python package paths changed.
- Existing runtime archive path preserved with a compatibility directory.
