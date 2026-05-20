# MLB Daily Scheduler — Dry-run Report

**Run Date**: 2026-05-07
**Run ID**: SCHED_20260507_FIXTURE_20260507T0846027
**Mode**: today
**Source**: fixture
**Scheduler Mode**: dry_run
**Gate**: `MLB_SCHEDULER_DATA_LIMITED`

---

## Safety Flags

| Flag | Value |
|------|-------|
| NO_REAL_BET | True |
| NO_PROFIT_CLAIM | True |
| PAPER_ONLY | True |
| LEDGER_OVERWRITE_BLOCKED | True |
| SCHEDULER_DRY_RUN_ONLY | True |
| NO_AUTO_EXECUTION | True |
| PRODUCTION_MODIFIED | False |

```
NO_REAL_BET = True
NO_PROFIT_CLAIM = True
PAPER_ONLY = True
LEDGER_OVERWRITE_BLOCKED = True
SCHEDULER_DRY_RUN_ONLY = True
NO_AUTO_EXECUTION = True
```

---

## Job Results

### Pregame Advisory Job
- **Status**: SUCCESS
- **Duration**: 0.026s
- **Total Advisories**: 4
- **Ledger Entries Written**: 0
- **Warnings**: fixture source: loaded 4 games from data/fixtures/mlb_current_source_sample_20260507.json

### Postgame Review Job
- **Status**: DATA_LIMITED
- **Duration**: 0.003s
- **Reviewed Count**: 0
- **Pending Count**: 6
- **Failure Notes**: 7
- **Warnings**: pending_results=6: result source did not cover all entries; reviewed_count=0 — all entries still pending

---

## Report Paths

- Advisory Report: `reports/mlb_daily_advisory_dry_run_20260507.json`
- Ledger: `reports/mlb_paper_betting_ledger.jsonl`
- Review Report: `reports/mlb_postgame_review_20260507.json`
- Reviewed Snapshot: `reports/mlb_paper_betting_reviewed_snapshot_20260507.jsonl`

---

## Gate

**MLB_SCHEDULER_DATA_LIMITED**

> pipeline runs but pending_count=6 — source (fixture/replay) lacks live results

---

## Governance Disclaimer

> This report is **PAPER-ONLY** / **NO REAL BET** / **NO PROFIT CLAIM**.
> The scheduler is a dry-run research tool. No real bets are placed.
> No guaranteed profit is implied. Human review required before any decision.

---

**Created**: 2026-05-07T08:46:02.779216+00:00
**Module Version**: mlb_daily_scheduler_v1

## Completion Marker

`MLB_DAILY_SCHEDULER_API_MVP_VERIFIED`

<!-- MLB_DAILY_SCHEDULER_API_MVP_VERIFIED -->