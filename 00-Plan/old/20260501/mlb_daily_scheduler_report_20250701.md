# MLB Daily Scheduler — Dry-run Report

**Run Date**: 2025-07-01
**Run ID**: SCHED_20250701_REPLAY_20260507T0846103
**Mode**: replay
**Source**: replay
**Scheduler Mode**: dry_run
**Gate**: `MLB_SCHEDULER_API_MVP_READY`

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
- **Duration**: 0.046s
- **Total Advisories**: 12
- **Ledger Entries Written**: 0

### Postgame Review Job
- **Status**: SUCCESS
- **Duration**: 0.021s
- **Reviewed Count**: 4
- **Pending Count**: 0
- **Failure Notes**: 7
- **Brier Score**: 0.2323
- **Recommendation Accuracy**: 75.00%

---

## Report Paths

- Advisory Report: `reports/mlb_daily_advisory_dry_run_20250701.json`
- Ledger: `reports/mlb_paper_betting_ledger.jsonl`
- Review Report: `reports/mlb_postgame_review_20250701.json`
- Reviewed Snapshot: `reports/mlb_paper_betting_reviewed_snapshot_20250701.jsonl`

---

## Gate

**MLB_SCHEDULER_API_MVP_READY**

> scheduler + API handlers + manifest operational; reviewed_count=4, pending=0, safety flags verified

---

## Governance Disclaimer

> This report is **PAPER-ONLY** / **NO REAL BET** / **NO PROFIT CLAIM**.
> The scheduler is a dry-run research tool. No real bets are placed.
> No guaranteed profit is implied. Human review required before any decision.

---

**Created**: 2026-05-07T08:46:10.382308+00:00
**Module Version**: mlb_daily_scheduler_v1

## Completion Marker

`MLB_DAILY_SCHEDULER_API_MVP_VERIFIED`

<!-- MLB_DAILY_SCHEDULER_API_MVP_VERIFIED -->