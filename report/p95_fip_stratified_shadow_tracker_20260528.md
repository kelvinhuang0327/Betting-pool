# P95 FIP-Stratified Shadow Tracker — Segment-Aware Diagnostic Report

**Date**: 2026-05-28  |  **Branch**: main  |  **HEAD**: fc8e51f (P94)
**Final Classification**: `P95_FIP_STRATIFIED_SHADOW_TRACKER_READY_WITH_LIMITED_COVERAGE`

---

## ⚠️ 重要聲明

- `paper_only=true` | `diagnostic_only=true` | `production_ready=false`
- `NO_REAL_BET=true` | `odds_used=false` | `ev_computed=false` | `clv_computed=false` | `kelly_computed=false`
- **Partial coverage**: 828 / 2430 rows = 34.07%（March–May 2026 only）
- P94 前置條件：`P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY`（ci_low=0.582, temporal_stable=True）

---

## Segment Tracker Policy

| Segment | 追蹤狀態 |
|---------|---------|
| HIGH_FIP (\|Δ FIP\| ≥ 1.5) | `allowed_diagnostic_only` |
| MID_FIP (0.5 ≤ \|Δ FIP\| < 1.5) | `watch_only_not_trackable` |
| LOW_FIP (\|Δ FIP\| < 0.5) | `watch_only_not_trackable` |
| Aggregate display | `allowed_with_warning` |
| Recommendation | ❌ forbidden |
| Product surface | ❌ forbidden |

---

## HIGH_FIP Segment（`HIGH_FIP_DIAGNOSTIC_TRACKING_ALLOWED`）

| 指標 | 數值 | P94 基準 | 容差通過 |
|------|------|---------|--------|
| n | 287 | 287 | ✅ |
| hit_rate | `0.641115` | `0.641115` | ✅ |
| Brier | `0.233554` | — | — |
| ECE | `0.058885` | — | — |
| predicted_home_ratio | `0.536585` | — | — |
| actual_home_ratio | `0.526132` | — | — |
| AUC | `0.639584` | — | — |

### HIGH_FIP Monthly Split

| Month | n | hit_rate |
|-------|---|----------|
| 2026-03 | 34 | `0.735294` |
| 2026-04 | 143 | `0.601399` |
| 2026-05 | 110 | `0.663636` |

### HIGH_FIP Side Split

| Side | n | hit_rate |
|------|---|----------|
| Home predicted | 154 | `0.655844` |
| Away predicted | 133 | `0.62406` |

---

## MID_FIP Segment（`MID_FIP_WATCH_ONLY`）

| 指標 | 數值 | P93 基準 | 容差通過 |
|------|------|---------|--------|
| n | 343 | 343 | ✅ |
| hit_rate | `0.530612` | `0.530612` | ✅ |
| Brier | `0.263307` | — | — |
| ECE | `0.109629` | — | — |
| binomial p vs home baseline | `0.43551` | — | — |

> ⚠️ MID_FIP hit_rate 未超過 home_baseline + 0.03 閾值，標記為 **watch-only**，不作為 diagnostic tracking signal。

### MID_FIP Monthly Split

| Month | n | hit_rate |
|-------|---|----------|
| 2026-03 | 26 | `0.5` |
| 2026-04 | 170 | `0.517647` |
| 2026-05 | 147 | `0.55102` |

---

## LOW_FIP Segment（`LOW_FIP_WATCH_ONLY`）

| 指標 | 數值 | P93 基準 | 容差通過 |
|------|------|---------|--------|
| n | 178 | 178 | ✅ |
| hit_rate | `0.52809` | `0.52809` | ✅ |
| Brier | `0.248187` | — | — |
| ECE | `0.010113` | — | — |
| binomial p vs home baseline | `0.494861` | — | — |

> ⚠️ LOW_FIP hit_rate 未超過 home_baseline + 0.03 閾值，標記為 **watch-only**，不作為 diagnostic tracking signal。

### LOW_FIP Monthly Split

| Month | n | hit_rate |
|-------|---|----------|
| 2026-03 | 13 | `0.538462` |
| 2026-04 | 76 | `0.486842` |
| 2026-05 | 89 | `0.561798` |

---

## Final Classification

**`P95_FIP_STRATIFIED_SHADOW_TRACKER_READY_WITH_LIMITED_COVERAGE`**

> All tolerance checks passed. Partial coverage 828/2430 = 0.3407 < 0.50 (March-May 2026 only). High-FIP diagnostic tracking allowed; mid/low FIP watch-only. Full-season readiness requires continued data accumulation.

---

## Governance & Drift Guard Summary

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
| live_api_calls | 0 |
| paid_api_calls | 0 |
| production_ready | false |
| paper_only | true |
| diagnostic_only | true |
