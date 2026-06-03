# P94 High-FIP Subset Diagnostic — FIP-Stratified Tracking Gate

**Date**: 2026-05-28  |  **Branch**: main  |  **HEAD**: 2221f0f (P93)
**Final Classification**: `P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY`

---

## ⚠️ 重要聲明

- `paper_only=true` | `diagnostic_only=true` | `production_ready=false`
- `NO_REAL_BET=true` | `odds_used=false` | `ev_computed=false` | `clv_computed=false` | `kelly_computed=false`
- Partial coverage: **828 / 2430 rows = 34.07%**（March–May 2026 only）

---

## Gate 狀態

| Gate | 狀態 |
|------|------|
| Gate 1 Canonical Entry | ✅ PASS |
| Gate 3 Upstream Consistency | ✅ PASS |
| High-FIP Metrics Tolerance | ✅ PASS |

---

## Step 3 — High-FIP Subset Metrics（|Δ FIP| ≥ 1.5）

| 指標 | 數值 | P93 基準 |
|------|------|--------|
| n | 287 | 287 |
| hit_rate | `0.641115` | `0.641115` |
| Brier | `0.233554` | — |
| ECE | `0.058885` | — |
| predicted_home_ratio | `0.536585` | — |
| actual_home_ratio | `0.526132` | — |

---

## Step 4 — Bootstrap 95% CI（1000 次 resamples）

- **CI**: `(0.581882, 0.69338)`
- **Observed**: `0.641115`
- **Home baseline**: `0.524752` | **Aggregate model**: `0.569307`
- **Stability**: `STRONG` (ci_low > 0.55 = True)

---

## Step 5 — Temporal Split（三等分）

| Third | n | hit_rate | date_start | date_end |
|-------|---|----------|------------|----------|
| 1 | 95 | `0.663158` | 2026-03-26 | 2026-04-14 |
| 2 | 96 | `0.614583` | 2026-04-14 | 2026-05-03 |
| 3 | 96 | `0.645833` | 2026-05-03 | 2026-05-26 |

- **Temporal stable** (all > 0.55): `True`

---

## Step 6 — Side Split

| Side | n | hit_rate |
|------|---|----------|
| Home predicted | 154 | `0.655844` |
| Away predicted | 133 | `0.62406` |

- **|delta|**: `0.031784` | threshold 0.10 | **Side balanced**: `True`

---

## Step 7 — Mid / Low FIP Segment Qualification

| Bucket | n | hit_rate | above_baseline+0.03 | binomial p |
|--------|---|----------|---------------------|------------|
| mid_fip | 343 | `0.530612` | False | `0.43551` |
| low_fip | 178 | `0.52809` | False | `0.494861` |

- **Segment qualification**: `LOW_MID_FIP_NOT_TRACKABLE`

---

## Step 8 — Sample Sufficiency

| Month | n | hit_rate |
|-------|---|----------|
| 2026-03 | 34 | `0.735294` |
| 2026-04 | 143 | `0.601399` |
| 2026-05 | 110 | `0.663636` |

- **any_month_below_30**: `False` | **monthly_sample_limited**: `False`
- **Partial coverage**: `828 / 2430 = 0.340741`
- **Season scope**: March–May 2026 only

---

## Final Classification

**`P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY`**

> Bootstrap ci_low=0.5819 > 0.55; all temporal thirds > 0.55; side_balanced=True; monthly_limited=False

---

## Governance Summary

| Flag | Value |
|------|-------|
| odds_used | false |
| ev_computed | false |
| clv_computed | false |
| kelly_computed | false |
| production_ready | false |
| paper_only | true |
| diagnostic_only | true |
| live_api_calls | 0 |
| paid_api_called | false |
