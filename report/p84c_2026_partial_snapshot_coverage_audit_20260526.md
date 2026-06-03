# P84C — 2026 Canonical Prediction Partial Snapshot + Coverage Gap Audit

**Date**: 2026-05-26  
**Classification**: `P84C_PARTIAL_SNAPSHOT_READY_OUTCOMES_PENDING`  
**Generated**: 2026-05-27T04:45:49.693529+00:00

---

## Summary

| Metric | Value |
|--------|-------|
| Canonical prediction rows | 828 |
| Schedule coverage rate | 34.07% (828 / 2430) |
| Outcomes available | ❌ PENDING |
| Performance metrics (hit_rate / AUC / Brier / ECE) | ❌ BLOCKED |
| Governance | `paper_only=True`, `diagnostic_only=True`, `production_ready=False` |

---

## Step 1 — P84B Artifact Verification

| Field | Value |
|-------|-------|
| P84B Classification | `P84B_SCHEDULE_READY_PITCHER_MODEL_BLOCKED` |
| Schedule rows (P84B summary) | 2443 |
| Pitcher FEATURE_READY (P84B summary) | 837 |
| Model DERIVABLE (P84B summary) | 837 |
| Classification OK | ✅ |

---

## Step 2 — Canonical Row Validation

| Check | Result |
|-------|--------|
| Total rows | 828 |
| Duplicate game_ids | 0 |
| Schema OK | ✅ |
| Governance consistency | ✅ |
| `abs_sp_fip_delta` consistent | ✅ |
| `model_probability` in [0, 1] | ✅ |
| Season = 2026 | ✅ |

---

## Step 3 — Snapshot Metrics

### Monthly Distribution

| Month | Rows |
|-------|------|
| 2026-03 | 73 |
| 2026-04 | 389 |
| 2026-05 | 366 |

### Rule Flags

| Flag | Count |
|------|-------|
| `rule_primary_125_flag` | 509 |
| `rule_shadow_100_flag` | 552 |
| `tier_b_candidate_flag` | 97 |
| `tier_a_watchlist_flag` | 85 |

### Predicted Side Split

- Home: 405  
- Away: 423

### Model Probability Distribution

| Stat | Value |
|------|-------|
| Min | 0.3 |
| Max | 0.7 |
| Mean | 0.504004 |
| Median | 0.504298 |
| Stdev | 0.153685 |

### Outcome Status

- `actual_winner` populated: **0** / 828
- `outcomes_available`: **❌ PENDING** — accuracy metrics (hit_rate, AUC, Brier, ECE) are BLOCKED

---

## Step 4 — Coverage Gap Audit

### Pipeline Funnel

| Stage | Count |
|-------|-------|
| Schedule (total) | 2430 |
| FIP FEATURE_READY | 828 |
| FIP FEATURE_PENDING | 1602 |
| Model DERIVABLE | 828 |
| Model MODEL_PENDING | 1602 |
| Canonical predictions | 828 |

**Schedule coverage**: **34.07%** — below 50% threshold → P84D required

### Gap Analysis

| Transition | Gap Count |
|------------|-----------|
| Schedule → FIP FEATURE_READY | 1602 |
| FIP FEATURE_READY → Model DERIVABLE | 0 |
| Model DERIVABLE → Canonical | 0 |

**Top pending reasons**: `NO_PROBABLE_PITCHER` (3167), `INSUFFICIENT_IP` (12)

---

## Step 5 — Remediation Path

- **P84D** (priority 1): Pitcher coverage improvement + probable pitcher backfill  
  _Schedule coverage is 34.07% (<50%). 1602 games lack FIP features. Top reason: NO_PROBABLE_PITCHER._
- **P84E** (priority 2): Outcome attachment pipeline  
  _828 canonical rows have outcome fields (result_home_score, actual_winner) but all values are None. Outcomes required for hit_rate, AUC, Brier, ECE._

**Sufficient for diagnostic snapshot**: ✅ (828 rows ≥ 200)  
**Performance conclusion possible**: ❌ BLOCKED by OUTCOMES_PENDING

---

## Governance Invariants

| Field | Value |
|-------|-------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `production_ready` | `False` |
| `live_api_calls` | `0` |
| `api_key_accessed` | `False` |
| `ev_calculated` | `False` |
| `clv_calculated` | `False` |
| `kelly_calculated` | `False` |
| `odds_used` | `False` |
| `uses_historical_odds` | `False` |
| `real_bet_allowed` | `False` |
| `outcomes_available` | `False` |
