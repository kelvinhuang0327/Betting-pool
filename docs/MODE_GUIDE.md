# Mode Guide

This repository has three user-facing operating modes:

## WBC Production

- Purpose: official WBC 2026 analysis and reporting.
- Entry: `python scripts/run_mode.py --mode wbc`
- Safe for betting: yes, when verification passes.

## MLB Paper-Only Research

- Purpose: benchmark model quality against a single canonical market snapshot.
- Entry:
  - `python scripts/run_mode.py --mode mlb-paper`
  - `python scripts/run_mode.py --mode mlb-benchmark`
  - `python scripts/run_mode.py --mode mlb-alpha`
- Safe for betting: no.
- CLV: unavailable in the current single-snapshot dataset.

## Spring Training Sandbox

- Purpose: observe spring games with the shared analysis pipeline.
- Entry: `python scripts/run_mode.py --mode spring`
- Safe for betting: no.
- Marked as: `SANDBOX_ONLY` and `NOT_RECOMMENDED_FOR_BETTING`.

## Best Practice

If you are unsure which command to use, run:

```bash
python scripts/run_mode.py
```

That command prints the current mode dashboard. You can also run:

- `python scripts/run_mode.py --mode reports`
- `python scripts/run_mode.py --mode wbc`
- `python scripts/run_mode.py --mode mlb-paper`
- `python scripts/run_mode.py --mode mlb-benchmark`
- `python scripts/run_mode.py --mode mlb-alpha`
- `python scripts/run_mode.py --mode spring`

If you want a report-only view, use:

```bash
python scripts/report_center.py
```
