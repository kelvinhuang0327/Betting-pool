# P96 High-FIP Segment Drift Monitor
**Generated:** 2026-05-28T03:08:38.402407Z
**Classification:** `P96_HIGH_FIP_DRIFT_MONITOR_STABLE_COVERAGE_LIMITED`

---

## Governance

> ⚠️ **DIAGNOSTIC ONLY** — No betting recommendation, no product claim, no production use.
>
> `paper_only=true` | `diagnostic_only=true` | `production_ready=false`
> `odds_used=false` | `ev_computed=false` | `clv_computed=false` | `kelly_computed=false`

---

## Upstream Chain

| Phase | Classification |
|-------|----------------|
| P94   | `P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY` |
| P95   | `P95_FIP_STRATIFIED_SHADOW_TRACKER_READY_WITH_LIMITED_COVERAGE` |
| P96   | `P96_HIGH_FIP_DRIFT_MONITOR_STABLE_COVERAGE_LIMITED` |

---

## HIGH_FIP Overall

| Metric | Value |
|--------|-------|
| n | 287 |
| hit_rate | 0.641115 |
| aggregate_monthly_status | `MONTHLY_ALL_STABLE` |
| rolling_status | `STABLE` |

---

## Monthly Drift — HIGH_FIP (|ΔFIP| ≥ 1.5)

| Month | n | hit_rate | AUC | Brier | Status |
|-------|---|----------|-----|-------|--------|
| 2026-03 | 34 | 0.735294 | 0.688889 | 0.231176 | STABLE |
| 2026-04 | 143 | 0.601399 | 0.480824 | 0.291399 | STABLE |
| 2026-05 | 110 | 0.663636 | 0.530544 | 0.279091 | STABLE |

Drift rule: STABLE if n≥30 and hit_rate≥0.55; DRIFT_WARNING if n≥30 and hit_rate<0.55; SAMPLE_LIMITED if n<30.

---

## Rolling Windows — HIGH_FIP (window=100, step=25)

| Window | Start | End | n | hit_rate | Status |
|--------|-------|-----|---|----------|--------|
| 0 | 2026-03-26 | 2026-04-15 | 100 | 0.650000 | ROLLING_STABLE |
| 1 | 2026-03-31 | 2026-04-19 | 100 | 0.630000 | ROLLING_STABLE |
| 2 | 2026-04-05 | 2026-04-25 | 100 | 0.620000 | ROLLING_STABLE |
| 3 | 2026-04-11 | 2026-04-30 | 100 | 0.630000 | ROLLING_STABLE |
| 4 | 2026-04-15 | 2026-05-04 | 100 | 0.640000 | ROLLING_STABLE |
| 5 | 2026-04-19 | 2026-05-10 | 100 | 0.660000 | ROLLING_STABLE |
| 6 | 2026-04-25 | 2026-05-17 | 100 | 0.650000 | ROLLING_STABLE |
| 7 | 2026-04-30 | 2026-05-22 | 100 | 0.670000 | ROLLING_STABLE |

`rolling_status = STABLE`

---

## Control Segment Comparison (Watch-Only)

| Segment | n | hit_rate | Tracking Status | Promoted? |
|---------|---|----------|-----------------|-----------|
| MID_FIP | 343 | 0.530612 | `MID_FIP_WATCH_ONLY` | No |
| LOW_FIP | 178 | 0.528090 | `LOW_FIP_WATCH_ONLY` | No |

---

## Coverage

| Metric | Value |
|--------|-------|
| canonical_rows | 828 |
| schedule_total | 2430 |
| schedule_coverage_pct | 34.0741% |
| coverage_status | `COVERAGE_LIMITED` |
| observed_range | 2026-03 to 2026-05 |
| full_season_claim | False |

---

## Final Classification

```
P96_HIGH_FIP_DRIFT_MONITOR_STABLE_COVERAGE_LIMITED
```

All HIGH_FIP monthly windows stable (hit_rate >= 0.55). Rolling windows all STABLE. Coverage limited to 34.07% (March–May 2026 only). No product or production claim permitted.

---

## Governance Guards

All guards locked. No odds, EV, CLV, Kelly, stake sizing, Taiwan lottery recommendation,
champion replacement, production mutation, calibration refit, or live/paid API calls.

| Guard | Value |
|-------|-------|
| odds_used | false |
| ev_computed | false |
| clv_computed | false |
| kelly_computed | false |
| stake_sizing | false |
| taiwan_lottery_recommendation | false |
| champion_replacement | false |
| production_mutation | false |
| calibration_refit | false |
| paper_only | **true** |
| diagnostic_only | **true** |
| production_ready | **false** |
| real_bet_allowed | **false** |
| recommendation_allowed | **false** |
