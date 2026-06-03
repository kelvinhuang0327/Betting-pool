# P49 — Offline Historical Monitoring Replay Using P48 Contract

**Date**: 2026-05-26  
**Classification**: `P49_MONITORING_REPLAY_CRITICAL_DIAGNOSTIC`  
**Mode**: `paper_only=true` | `diagnostic_only=true` | `promotion_freeze=true`  
**Platt Coefficients**: a=0.435432, b=0.245464 (locked from P45)

---

## 1. P48 Contract Recap

| Threshold | Warning | Critical |
|-----------|---------|----------|
| ECE (Platt) | > 0.10 | > 0.12 |
| Brier (Platt) | > 0.25 | > 0.27 |
| Edge mean | < 0.07 | CI ≤ 0 |
| Sample | — | SAMPLE_LIMITED if n < 100 |
| Data gap | — | DATA_GAP_BLOCKED (overrides all) |

Priority: DATA_GAP_BLOCKED > SAMPLE_LIMITED > CRITICAL/WARNING > MONITORING_OK

---

## 2. Source Data Inventory

| Source | Status |
|--------|--------|
| Predictions JSONL (phase56) | Present, immutable |
| P45 Platt summary | Present, immutable |
| P47 synthesis summary | Present, immutable |
| P48 contract summary | Present, immutable |
| 2024 closing-line data | **MISSING** (P43_BLOCKED_BY_DATA_GAP) |

---

## 3. Tier C Row Count Verification

| Metric | Value |
|--------|-------|
| Rebuilt Tier C n | 535 |
| Expected n | 535 |
| Match | True |
| Date range | 2025-04-27 to 2025-09-28 |
| Months covered | 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09 |

Filter: `abs(sp_fip_delta) >= 0.5`, `market_home_prob_no_vig in (0,1)`, outcome not null

---

## 4. Monthly Monitoring Replay

| Month | n | Platt ECE | Platt Brier | Mean Edge | Edge CI Low | Status | Alert |
|-------|---|-----------|-------------|-----------|-------------|--------|-------|
| 2025-04 | 16 | 0.0824 | 0.2527 | 0.0359 | 0.0121 | `SAMPLE_LIMITED` | `WARNING` |
| 2025-05 | 120 | 0.0557 | 0.2378 | 0.0093 | -0.0004 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| 2025-06 | 101 | 0.0519 | 0.2401 | -0.0231 | -0.0410 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| 2025-07 | 92 | 0.0403 | 0.2391 | -0.0101 | -0.0240 | `SAMPLE_LIMITED` | `WARNING` |
| 2025-08 | 108 | 0.0435 | 0.2474 | 0.0324 | 0.0214 | `EDGE_DRIFT_WARNING` | `WARNING` |
| 2025-09 | 98 | 0.1229 | 0.2357 | -0.0036 | -0.0144 | `SAMPLE_LIMITED` | `WARNING` |

**Monthly summary**: OK=0, Warning=1, Critical=2, SampleLimited=3, Blocked=0

---

## 5. Rolling Batch Monitoring Replay

Batch size: 100 | Step: 50 | Ordered by game_date | Partial batches omitted

| Batch ID | n | Dates | Platt ECE | Platt Brier | Mean Edge | CI Low | Status | Alert |
|----------|---|-------|-----------|-------------|-----------|--------|--------|-------|
| ROLLING_20250427_20250521_N100 | 100 | 2025-04-27 – 2025-05-21 | 0.1058 | 0.2424 | 0.0190 | 0.0096 | `MIXED_ALERTS` | `WARNING` |
| ROLLING_20250509_20250605_N100 | 100 | 2025-05-09 – 2025-06-05 | 0.0194 | 0.2414 | -0.0051 | -0.0183 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| ROLLING_20250523_20250619_N100 | 100 | 2025-05-23 – 2025-06-19 | 0.1164 | 0.2397 | -0.0190 | -0.0365 | `MIXED_ALERTS` | `CRITICAL` |
| ROLLING_20250605_20250703_N100 | 100 | 2025-06-05 – 2025-07-03 | 0.0778 | 0.2343 | -0.0126 | -0.0297 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| ROLLING_20250619_20250721_N100 | 100 | 2025-06-19 – 2025-07-21 | 0.0669 | 0.2310 | -0.0131 | -0.0266 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| ROLLING_20250705_20250805_N100 | 100 | 2025-07-05 – 2025-08-05 | 0.0656 | 0.2434 | 0.0025 | -0.0114 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| ROLLING_20250721_20250822_N100 | 100 | 2025-07-21 – 2025-08-22 | 0.0637 | 0.2515 | 0.0241 | 0.0113 | `MIXED_ALERTS` | `WARNING` |
| ROLLING_20250806_20250906_N100 | 100 | 2025-08-06 – 2025-09-06 | 0.0564 | 0.2482 | 0.0233 | 0.0116 | `EDGE_DRIFT_WARNING` | `WARNING` |
| ROLLING_20250822_20250918_N100 | 100 | 2025-08-22 – 2025-09-18 | 0.0597 | 0.2388 | 0.0052 | -0.0063 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |

**Rolling summary**: Total=9, OK=0, Warning=3, Critical=6, SampleLimited=0, Blocked=0

---

## 6. Alert Summary

| Scope | Total | OK | Warning | Critical | SampleLimited | Blocked |
|-------|-------|----|---------|----------|---------------|---------|
| Monthly | 6 | 0 | 1 | 2 | 3 | 0 |
| Rolling | 9 | 0 | 3 | 6 | 0 | 0 |

---

## 7. Worst-Case Batch Analysis

| Metric | Value | Threshold |
|--------|-------|-----------|
| Worst Platt ECE | 0.1229 | Warning=0.10, Critical=0.12 |
| Worst Platt Brier | 0.2527 | Warning=0.25, Critical=0.27 |
| Lowest Mean Edge | -0.0231 | Warning=0.07 |
| Lowest Edge CI Low | -0.0410 | Critical: CI ≤ 0 |
| Worst batch | MONTHLY_202509 | — |

---

## 8. Platt Monitoring Baseline Acceptability

**Acceptable**: `False`

CRITICAL alerts detected in rolling replay or worst ECE exceeds critical threshold. Platt calibration may be degrading. Consider re-running P45 recalibration.

---

## 9. Limitations

- **2024 closing-line data gap**: Unresolved. P43_BLOCKED_BY_DATA_GAP persists.
- **Closing line vs CLV**: `mlb_odds_2025_real.csv` has no pre-game timestamps. Edge is vs closing line, not strict Closing Line Value (CLV).
- **Normal approximation CI**: Rolling batch edge CI uses normal approximation (n≥100). Consistent with large-sample theory but differs from P43 bootstrap CI.
- **Platt coefficients are from 80/20 train/test split**: Coefficients (a=0.435432, b=0.245464) were fitted on 428 training rows. Full-dataset coefficients would differ.
- **No live model deployed**: Platt calibration is diagnostic only. No runtime logic was changed.

---

## 10. 2024 Data Gap (Explicit Statement)

The 2024 MLB closing-line data gap remains **unresolved**. `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl` contains no market probability columns. No valid 2024 MLB moneyline odds source exists in the repository. **P43 final classification remains `P43_BLOCKED_BY_DATA_GAP`**. P49 uses 2025 Tier C data only (n=535).

---

## 11. Final P49 Classification

**`P49_MONITORING_REPLAY_CRITICAL_DIAGNOSTIC`**

> This is a paper-only offline diagnostic replay. It does not authorize deployment, live monitoring, production usage, or any change to the champion strategy or runtime recommendation logic.

---

## Governance Flags

| Flag | Value |
|------|-------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `promotion_freeze` | `True` |
| `kelly_deploy_allowed` | `False` |
| `live_api_calls` | `0` |
| `tsl_crawler_modified` | `False` |
| `champion_strategy_changed` | `False` |
| `production_usage_proposed` | `False` |
| `runtime_recommendation_logic_changed` | `False` |

---

## CTO Summary

P49 replays the P48 monitoring contract against actual 2025 Tier C data (n=535). Monthly replay covers Apr–Sep; April/July/September are SAMPLE_LIMITED (n<100). Rolling replay uses batch=100, step=50 across the full season. Platt calibration (a=0.435432, b=0.245464) is applied from P45 locked coefficients. Final classification: `P49_MONITORING_REPLAY_CRITICAL_DIAGNOSTIC`. No live API calls. No runtime logic changes. No production proposals. 2024 data gap remains P43_BLOCKED_BY_DATA_GAP.