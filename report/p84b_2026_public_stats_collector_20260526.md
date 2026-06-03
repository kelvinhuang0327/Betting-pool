# P84B — 2026 Public Stats Collector Implementation
**Date:** 2026-05-26
**Classification:** `P84B_SCHEDULE_READY_PITCHER_MODEL_BLOCKED`
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Summary

P84B collects public MLB 2026 schedule and pitcher season stats, applies a deterministic
diagnostic baseline model, then retries P83E.

---

## Public API Scope

| Endpoint | Purpose | Odds? |
|---|---|---|
| `statsapi.mlb.com/api/v1/schedule` | 2026 regular season games | No |
| `statsapi.mlb.com/api/v1/people/{id}/stats` | Pitcher season HR/BB/HBP/SO/IP | No |

**MLB Stats API calls:** 256
**Odds API calls:** 0

---

## Schedule Collector Result

| Item | Value |
|---|---|
| Schedule API ok | True |
| Total API games | 2443 |
| Rows collected | 2443 |
| Written to disk | True |
| Path | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2026/schedule/mlb_2026_schedule.jsonl` |
| Source trace | `MLB_STATS_API_PUBLIC_SCHEDULE` |

---

## Pitcher FIP Feature Result

| Item | Value |
|---|---|
| Rows total | 2443 |
| FEATURE_READY | 837 |
| FEATURE_PENDING | 1606 |
| Gate pass | False |
| Written | True |

**FIP formula:** `((13*HR + 3*(BB+HBP) - 2*K) / IP) + 3.1`
**Min IP threshold:** 5.0

---

## Model Output Result

| Item | Value |
|---|---|
| Rows total | 2443 |
| DERIVABLE | 837 |
| MODEL_PENDING | 1606 |
| Gate pass | False |
| Model source | `DIAGNOSTIC_BASELINE_MODEL` |
| Version | `p84b_diagnostic_baseline_v1` |

**Model note:** Diagnostic baseline using sp_fip_delta → sigmoid(delta * 0.6).
Clamped to [0.30, 0.70]. Not production quality. paper_only=True.

---

## P83E Retry Classification

| Item | Value |
|---|---|
| P83E classification | `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA` |
| Canonical rows written | False |
| Canonical row count | 0 |

---

## Governance Invariants

| Invariant | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| live_api_calls (odds) | 0 |
| odds_used | False |
| ev_calculated | False |
| clv_calculated | False |
| kelly_calculated | False |
| production_ready | False |
| forbidden_scan_pass | True |

---

## Final Classification

**`P84B_SCHEDULE_READY_PITCHER_MODEL_BLOCKED`**

P84B collects public MLB schedule/pitcher stats (no odds) and applies a deterministic baseline model to produce P83E upstream files. No edge/EV/CLV/Kelly computed. paper_only=True, diagnostic_only=True.
