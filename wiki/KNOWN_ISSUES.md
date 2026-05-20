# Known Issues (Canonical)

Purpose

List canonical issues discovered during consolidation and their short remediation notes.

Key Issues

- Duplicate code paths: `models/` vs `wbc_backend/models/`. Remediation: plan a single migration path and update imports after tests.
- Multiple entrypoints: `scripts/run_mode.py` (primary), `main.py` (legacy), `wbc_backend/run.py` (pipeline). Remediation: standardize on `scripts/run_mode.py` → `wbc_backend/run.py` and deprecate `main.py` after dependency inventory.
- Crawler duplication: `data/tsl_crawler.py` vs `data/tsl_crawler_v2.py` — some loaders still import the old crawler. Remediation: confirm active crawler, add compatibility shim, migrate callers.
- Mixed reports folder: `data/wbc_backend/reports` contains both runtime artifacts and human knowledge docs. Remediation: enforce reports-only policy and move knowledge sections to wiki summaries.

Source

repo-wide scan, docs/wbc_backend_architecture.md
