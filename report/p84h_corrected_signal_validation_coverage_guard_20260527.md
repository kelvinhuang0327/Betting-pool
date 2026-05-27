# P84H — Corrected 2026 Prediction-Only Signal Validation + Coverage Guard

**Generated**: 2026-05-27T07:06:12.162666+00:00
**Phase**: P84H | **Date**: 2026-05-27
**Predecessor**: P84G@021a8a8 — P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED

> ⚠️ **diagnostic_only=true** | **paper_only=true** | **production_ready=false**
> **odds_used=false** | **ev_computed=false** | **clv_computed=false** | **kelly_computed=false**
> Partial 2026 coverage (828/2430, March–May only). No full-season claim. No production claim.

---

## Final Classification: `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED`

**Rationale:**
- hit_rate = 0.569307 > 0.55 ✓
- AUC(prob, home_win) = 0.594315 > 0.56 ✓
- Coverage 34.07% (828/2430) — COVERAGE_LIMITED (March–May 2026 only)
- ECE = 0.069682 — calibration weak but acceptable for diagnostic tracking
- primary_125 hit_rate = 0.602851, significantly above random (p<0.05)
- No full-season claim | No production claim | Diagnostic-only use

### Key Metrics Summary

| Metric | Value |
|--------|-------|
| hit_rate (all, n=808) | 0.569307 |
| AUC(prob, home_win) | 0.594315 |
| ECE (10-bin) | 0.069682 |
| Coverage (canonical/schedule) | 34.07% |
| Coverage class | COVERAGE_LIMITED |
| primary_125 hit_rate (n=491) | 0.602851 |
| primary_125 significant (α=0.05) | True |

---

## Step 2 — Recomputed Metrics vs P84E Artifact

| Metric | Recomputed | P84E Reference | Delta | OK? |
|--------|-----------|---------------|-------|-----|
| hit_rate | 0.569307 | 0.569307 | 0.000000 | ✓ |
| auc | 0.594315 | 0.594315 | 0.000000 | ✓ |
| brier | 0.249408 | 0.249408 | 0.000000 | ✓ |
| ece | 0.069682 | 0.069682 | 0.000000 | ✓ |

---

## Step 3a — Monthly Split

| Month | n | hit_rate | AUC | Brier | ECE |
|-------|---|---------|-----|-------|-----|
| 2026-03 | 73 | 0.616438 | 0.682946 | 0.231470 | 0.087881 |
| 2026-04 | 389 | 0.542416 | 0.562500 | 0.257490 | 0.100108 |
| 2026-05 | 346 | 0.589595 | 0.612450 | 0.244105 | 0.042460 |

## Step 3b — Chronological Thirds

| Third | n | date_range | hit_rate | AUC | Brier |
|-------|---|-----------|---------|-----|-------|
| first_third | 269 | 2026-03-25 – 2026-04-16 | 0.531599 | 0.578769 | 0.254956 |
| second_third | 269 | 2026-04-16 – 2026-05-06 | 0.617100 | 0.626880 | 0.239578 |
| third_third | 270 | 2026-05-06 – 2026-05-26 | 0.559259 | 0.574353 | 0.253673 |

## Step 3c — Side Split

| predicted_side | n | hit_rate | AUC | Brier | ECE |
|---------------|---|---------|-----|-------|-----|
| home | 412 | 0.592233 | 0.551913 | 0.242853 | 0.047374 |
| away | 396 | 0.545455 | 0.551337 | 0.256228 | 0.092891 |

## Step 3d — Rule Subset Split

| Subset | n | hit_rate | AUC | Brier | ECE |
|--------|---|---------|-----|-------|-----|
| primary_125 | 491 | 0.602851 | 0.611055 | 0.245795 | 0.075904 |
| shadow_100 | 536 | 0.595149 | 0.609431 | 0.248071 | 0.082219 |
| tier_b | 94 | 0.563830 | 0.566576 | 0.246039 | 0.011976 |
| tier_a | 84 | 0.488095 | 0.492630 | 0.250590 | 0.028535 |

---

## Step 4 — Calibration Analysis

**ECE** = 0.069682 — **WEAK**

*(Platt/isotonic refit: FORBIDDEN by governance)*

**Reliability Curve (10 bins):**

| Bin | n | Mean Prob | Empirical HR | Gap |
|-----|---|----------|-------------|-----|
| [0.2, 0.3) | 144 | 0.300000 | 0.375000 | -0.075000 |
| [0.3, 0.4) | 132 | 0.350841 | 0.507576 | -0.156735 |
| [0.4, 0.5) | 120 | 0.447535 | 0.491667 | -0.044132 |
| [0.5, 0.6) | 121 | 0.550483 | 0.528926 | 0.021558 |
| [0.6, 0.7) | 291 | 0.676665 | 0.618557 | 0.058108 |

**Notes on calibration weakness sources:**
- Partial season coverage (2026-03 through 2026-05 only) — small n inflates ECE
- model_probability is FIP-delta derived proxy; not calibrated for 2026 outcomes
- No score transformation applied — systematic over/under confidence possible

---

## Step 5 — Coverage Classification

| Field | Value |
|-------|-------|
| Schedule rows (full 2026 season) | 2430 |
| Canonical rows | 828 |
| Outcome-available rows | 808 |
| Canonical coverage ratio | 34.07% |
| Outcome coverage ratio | 97.58% |
| Coverage classification | **COVERAGE_LIMITED** |
| Date range covered | 2026-03 through 2026-05 |
| Full-season claim valid | False |
| Production claim valid | False |

---

## Step 6 — Subset Binomial Test (H₀: hit_rate = 0.50, one-sided greater)

| Subset | n | hit_rate | p-value | Significant α=0.05 | Wilson CI 95% |
|--------|---|---------|---------|-------------------|--------------|
| all | 808 | 0.569307 | 0.000046 | True | [0.534915, 0.603043] |
| primary_125 | 491 | 0.602851 | 0.000003 | True | [0.558933, 0.645173] |
| shadow_100 | 536 | 0.595149 | 0.000006 | True | [0.553059, 0.635886] |
| tier_b | 94 | 0.563830 | 0.128221 | False | [0.463027, 0.659620] |

---

## Governance Scan

| Flag | Value |
|------|-------|
| paper_only | True |
| diagnostic_only | True |
| production_ready | False |
| odds_used | False |
| ev_computed | False |
| clv_computed | False |
| kelly_computed | False |
| live_api_calls | 0 |
| paid_api_called | False |
| canonical_rows_modified | False |
| outcome_rows_modified | False |
| p83e_mapping_modified | False |
| champion_replaced | False |

---

_P84H — Corrected 2026 Prediction-Only Signal Validation + Coverage Guard_
_diagnostic_only=true | paper_only=true | production_ready=false_
_No odds, no EV, no CLV, no Kelly, no live API, no production deployment_