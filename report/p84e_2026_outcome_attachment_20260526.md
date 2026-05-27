# P84E — 2026 Outcome Attachment Pipeline for Canonical Prediction Rows

**Classification**: `P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS`  
**Date**: 2026-05-27  
**Generated**: 2026-05-27T05:17:54.476832+00:00  

---

## 1. Pre-flight & Prerequisites

| Check | Result |
|---|---|
| P84D classification | `P84D_PITCHER_COVERAGE_AUDIT_READY_NO_BACKFILL` |
| P84C classification | `P84C_PARTIAL_SNAPSHOT_READY_OUTCOMES_PENDING` |
| Canonical prediction rows | 828 |
| Prerequisites OK | True |

---

## 2. Outcome Collector

| Field | Value |
|---|---|
| Source | `MLB_STATS_API_PUBLIC_RESULT` |
| Endpoint | `statsapi.mlb.com/api/v1/schedule` (public, no key) |
| Date chunks queried | 3 |
| Games in outcome map | 891 |
| MLB Stats API calls | 3 |
| Odds API calls | 0 |
| API key accessed | false |
| Fabricated outcomes | false |

---

## 3. Outcome Attachment Results

| Metric | Count |
|---|---|
| Total canonical rows | 828 |
| Outcome available (Final) | 808 |
| Outcome pending | 20 |
| Outcome coverage | 97.58% |
| n_correct | 348 |
| n_incorrect | 460 |

---

## 4. Prediction-Only Outcome Metrics

> **Sample note**: n_outcome_available=808.
> 2026 season is still in progress — partial-season results only.
> Do not infer full-season conclusions from partial outcomes.

### Overall (All Canonical Rows)

| Metric | Value |
|---|---|
| n_outcome_available | 808 |
| hit_rate | 0.4307 |
| hit_rate CI 95% | [0.3970, 0.4651] |
| AUC | 0.5943 |
| Brier Score | 0.2494 |
| ECE | 0.0697 |

### Monthly Outcome Distribution

| Month | n_outcome | n_correct | hit_rate |
|---|---|---|---|
| 2026-03 | 73 | 28 | 0.3836 |
| 2026-04 | 389 | 178 | 0.4576 |
| 2026-05 | 346 | 142 | 0.4104 |

### Primary 125 Flagged

| Metric | Value |
|---|---|
| n_rows | 509 |
| n_outcome_available | 496 |
| sample_limited (< 30) | False |
| hit_rate | 0.4234 |
| AUC | 0.6152 |
| Brier | 0.2518 |

### Shadow 100 Flagged

| Metric | Value |
|---|---|
| n_rows | 552 |
| n_outcome_available | 537 |
| sample_limited (< 30) | False |
| hit_rate | 0.4264 |
| AUC | 0.6113 |
| Brier | 0.2526 |

### Tier B Candidate

| Metric | Value |
|---|---|
| n_rows | 97 |
| n_outcome_available | 94 |
| sample_limited (< 30) | False |
| hit_rate | 0.4362 |
| AUC | 0.5666 |
| Brier | 0.2460 |

---

## 5. Remaining Blockers

| Item | Status |
|---|---|
| n_outcome_pending | 20 (games scheduled / not yet Final) |
| Odds / EV / CLV / Kelly | BLOCKED — P82 BLOCKED_NO_REAL_DATASET |
| production_ready | false |

---

## 6. Governance Invariants

| Invariant | Value |
|---|---|
| paper_only | true |
| diagnostic_only | true |
| production_ready | false |
| odds_api_called | false |
| ev_calculated | false |
| clv_calculated | false |
| kelly_calculated | false |
| fabricated_outcomes | false |
| market_edge_calculated | false |
| api_key_accessed | false |
