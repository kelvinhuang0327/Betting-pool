# P74 — Tier C Home/Away Bias Correction Research

**Date:** 2026-05-26
**Phase:** P74
**Classification:** `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`

---

## Pre-flight Result

| Check | Result |
|---|---|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| Branch | `main` ✅ |
| P73 commit reachable | `5fda71b` ✅ |
| P72B commit reachable | `9c04e50` ✅ |
| P72A commit reachable | `5c2a26b` ✅ |

---

## Governance Invariants

| Invariant | Value |
|---|---|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `uses_historical_odds` | `False` |
| `live_api_calls` | `0` |
| `the_odds_api_key_required` | `False` |
| `ev_calculated` | `False` |
| `clv_calculated` | `False` |
| `market_edge_calculated` | `False` |
| `kelly_deploy_allowed` | `False` |
| `production_ready` | `False` |
| `real_bet_allowed` | `False` |
| `champion_replacement_allowed` | `False` |
| `profitability_claim` | `False` |

---

## Step 1 — Tier C Reconstruction Check

- n = **535** (expected 535) — ✅
- hit_rate = **0.6056** (expected 0.6056) — ✅
- AUC = **0.5834** (expected 0.5834) — ✅
- Monthly stability: ✅ STABLE
- Reconstruction valid: **True**

---

## Step 2 — Home/Away Decomposition

| Metric | Home | Away | Gap |
|---|---:|---:|---:|
| n | 268 | 267 | — |
| hit_rate | 0.6716 | 0.5393 | 0.1323 |
| AUC | 0.5591 | 0.545 | 0.0141 |
| Brier | 0.2292 | 0.2478 | — |
| Monthly stability | ⚠️ MODERATE | ⚠️ MODERATE | — |

### Away Weakness Diagnosis
- Is general (not month/band specific): **False**
- Is band-specific: **True**
- Away months above 50% hit: **5/6**

### Home Monthly Breakdown

| Month | n | Hit Rate | AUC | Brier |
|---|---:|---:|---:|---:|
| 2025-04 | 8 | 0.625 | None | 0.2229 |
| 2025-05 | 62 | 0.6452 | 0.6136 | 0.225 |
| 2025-06 | 50 | 0.72 | 0.496 | 0.2436 |
| 2025-07 | 45 | 0.7111 | 0.506 | 0.2294 |
| 2025-08 | 54 | 0.6111 | 0.5859 | 0.2328 |
| 2025-09 | 49 | 0.6939 | 0.6971 | 0.2165 |

### Away Monthly Breakdown

| Month | n | Hit Rate | AUC | Brier |
|---|---:|---:|---:|---:|
| 2025-04 | 8 | 0.625 | None | 0.2709 |
| 2025-05 | 58 | 0.5 | 0.5743 | 0.2438 |
| 2025-06 | 51 | 0.6078 | 0.5895 | 0.2373 |
| 2025-07 | 47 | 0.5319 | 0.4818 | 0.2524 |
| 2025-08 | 54 | 0.5185 | 0.4918 | 0.2569 |
| 2025-09 | 49 | 0.5306 | 0.5753 | 0.2453 |

---

## Step 3 — Away Rescue Filters

**Away rescue filter found:** `False`
**Away baseline:** n=267, hit_rate=0.5393

| Filter | n | Hit Rate | AUC | Brier | Monthly Stability | Operational Status |
|---|---:|---:|---:|---:|---|---|
| AWAY_BASELINE | 267 | 0.5393 | 0.545 | 0.2478 | ⚠️ MODERATE | WEAK_SIGNAL |
| AWAY_DELTA_GE_075 | 176 | 0.5227 | 0.5052 | 0.2535 | ❌ UNSTABLE | RESTRICTED_UNSTABLE |
| AWAY_DELTA_GE_100 | 105 | 0.5333 | 0.473 | 0.2551 | ❌ UNSTABLE | RESTRICTED_UNSTABLE |
| AWAY_DELTA_GE_125 | 48 | 0.4583 | 0.5262 | 0.2506 | ❌ UNSTABLE | WATCHLIST_ONLY_N_BELOW_75 |
| AWAY_EXCL_WEAK_BAND_075_100 | 196 | 0.551 | 0.5432 | 0.2466 | ⚠️ MODERATE | CANDIDATE |
| AWAY_STRONG_MONTHS_ONLY | 59 | 0.6102 | 0.5682 | 0.2419 | INSUFFICIENT_MONTHS | WATCHLIST_ONLY_N_BELOW_75 |
| AWAY_HIGH_PROB_CONF_055 | 54 | 0.6111 | 0.6587 | 0.2265 | ⚠️ MODERATE | WATCHLIST_ONLY_N_BELOW_75 |
| AWAY_HIGH_CONF_DELTA_075 | 37 | 0.5135 | 0.6126 | 0.251 | ❌ UNSTABLE | WATCHLIST_ONLY_N_BELOW_75 |
| AWAY_TOP_HALF_DELTA | 133 | 0.5414 | 0.5383 | 0.2489 | ❌ UNSTABLE | RESTRICTED_UNSTABLE |

**Best rescue filter:** `AWAY_EXCL_WEAK_BAND_075_100` — n=196, hit_rate=0.551, AUC=0.5432

---

## Step 4 — Home Robustness Thresholds

**Home stable at full threshold (0.50):** `True`
**Narrowing threshold improves meaningfully:** `True`
**Recommendation:** `NARROW_TO_STRONGER_DELTA`

| Threshold | n | Hit Rate | AUC | Brier | Monthly Stability |
|---|---:|---:|---:|---:|---|
| >=0.5 | 268 | 0.6716 | 0.5591 | 0.2292 | ⚠️ MODERATE |
| >=0.75 | 191 | 0.6545 | 0.5675 | 0.231 | ❌ UNSTABLE |
| >=1.0 | 124 | 0.6694 | 0.6292 | 0.2213 | ❌ UNSTABLE |
| >=1.25 | 50 | 0.72 | 0.6786 | 0.2114 | ❌ UNSTABLE |

---

## Step 5 — Candidate Corrected Rules

**Baseline n:** 535

| Candidate Rule | n | Coverage | Hit Rate | AUC | Brier | Monthly Stability | Home Frac | Status |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `TIER_C_ALL_BASELINE` | 535 | 1.0 | 0.6056 | 0.5834 | 0.2385 | ✅ STABLE | 0.5009 | CANDIDATE |
| `TIER_C_HOME_ONLY` | 268 | 0.5009 | 0.6716 | 0.5591 | 0.2292 | ⚠️ MODERATE | 1.0 | STRONG_CANDIDATE |
| `TIER_C_HOME_PLUS_AWAY_075` | 444 | 0.8299 | 0.6126 | 0.5708 | 0.2388 | ⚠️ MODERATE | 0.6036 | CANDIDATE |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6972 | 0.6327 | 0.5603 | 0.2365 | ⚠️ MODERATE | 0.7185 | STRONG_CANDIDATE |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.5907 | 0.6392 | 0.5787 | 0.2324 | ⚠️ MODERATE | 0.8481 | STRONG_CANDIDATE |
| `TIER_C_HOME_WEIGHTED_AWAY_WATCHLIST` | 268 | 0.5009 | 0.6716 | 0.5591 | 0.2292 | ⚠️ MODERATE | 1.0 | STRONG_CANDIDATE |
| `TIER_C_BAND_FILTERED` | 168 | 0.314 | 0.6369 | 0.6303 | 0.2312 | ⚠️ MODERATE | 0.4583 | WATCHLIST_SAMPLE_LIMITED |

---

## Final Classification

### `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`

A corrected rule exists that improves hit rate and/or AUC without severe sample loss. Home/away correction is confirmed and recommended for P75 validation.

---

## Forbidden Scan Result

- ev_calculated: `False`
- clv_calculated: `False`
- kelly_deployed: `False`
- production_proposed: `False`
- profitability_asserted: `False`
- live_api_calls: `0`
- **Result: `CLEAN`**

---

## Recommended P75 Direction

- **P75A**: Implement prediction-only Tier C corrected rule validator
- **P75B**: Add calibration diagnostics for corrected Tier C candidate
- **P75C**: Continue Tier B sample expansion (parallel track)
- **P75D**: Defer market-edge lane until odds/API key exists

---

## CTO Agent 10-Line Summary

1. P74 reconstructed Tier C (n=535) matching P73A within tolerance — reconstruction VALID.
2. Home hit_rate=0.6716, away hit_rate=0.5393, gap=0.1323 — home/away bias confirmed.
3. Home monthly stability: MODERATE; away monthly stability: MODERATE.
4. Away rescue filters tested: rescue_found=False — best rescue: AWAY_EXCL_WEAK_BAND_075_100 n=196 hit_rate=0.551.
5. Home robustness: NARROW_TO_STRONGER_DELTA; narrowing improves=True.
6. Best candidate rule: `TIER_C_HOME_ONLY` — n=268, hit_rate=0.6716, AUC=0.5591.
7. Final classification: `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`.
8. Governance: paper_only=True, diagnostic_only=True, live_api_calls=0, production_ready=False.
9. Forbidden scan: CLEAN — no EV/CLV/Kelly/profitability claims.
10. Recommended next phase: P75A (corrected rule validator) + P75C (Tier B expansion).

---

*P74 is diagnostic research only. No market edge, EV, CLV, or Kelly calculations performed.*
*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*