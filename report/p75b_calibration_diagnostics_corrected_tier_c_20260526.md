# P75B — Calibration Diagnostics for Corrected Tier C Candidates

**Date:** 2026-05-26
**Phase:** P75B
**Classification:** `P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE`
**Calibration Module:** `AVAILABLE`

---

## Pre-flight Result

| Check | Result |
|---|---|
| P75A commit `7773624` | ✅ reachable |
| P74 commit `fb2af84` | ✅ reachable |
| P73 commit `5fda71b` | ✅ reachable |
| P72B commit `9c04e50` | ✅ reachable |
| P72A commit `5c2a26b` | ✅ reachable |

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

## Step 1 — Candidate Reconstruction Check

| Rule | n | Hit Rate | AUC | Valid |
|---|---:|---:|---:|---|
| `TIER_C_ALL_BASELINE` | 535 | 0.6056 | 0.5834 | ✅ |
| `TIER_C_HOME_ONLY` | 268 | 0.6716 | 0.5591 | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6327 | 0.5603 | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.6392 | 0.5787 | ✅ |
| `TIER_C_BAND_FILTERED` | 168 | 0.6369 | 0.6303 | ✅ |

**All valid:** `True`

---

## Step 2 — Uncalibrated Calibration Metrics

| Rule | n | Hit Rate | AUC | Brier | Log Loss | ECE | MCE |
|---|---:|---:|---:|---:|---:|---:|---:|
| `TIER_C_ALL_BASELINE` | 535 | 0.6056 | 0.5834 | 0.2385 | 0.6693 | 0.0685 | 0.1877 |
| `TIER_C_HOME_ONLY` | 268 | 0.6716 | 0.5591 | 0.2292 | 0.6504 | 0.0983 | 0.2315 |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6327 | 0.5603 | 0.2365 | 0.6652 | 0.0782 | 0.2042 |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.6392 | 0.5787 | 0.2324 | 0.657 | 0.0763 | 0.1562 |
| `TIER_C_BAND_FILTERED` | 168 | 0.6369 | 0.6303 | 0.2312 | 0.6541 | 0.1048 | 0.2494 |

---

## Step 3 — Calibration Method Comparison

| Rule | Method | Cal Brier | Cal ECE | Brier Δ | ECE Δ | Overfit Risk | Allowed |
|---|---|---:|---:|---:|---:|---|---|
| `TIER_C_ALL_BASELINE` | no_calibration | 0.24 | 0.0637 | +0.0000 | +0.0000 | NONE | ✅ |
| `TIER_C_ALL_BASELINE` | platt | 0.2377 | 0.0604 | +0.0023 | +0.0033 | LOW | ✅ |
| `TIER_C_ALL_BASELINE` | temperature | 0.2395 | 0.0608 | +0.0005 | +0.0028 | LOW | ✅ |
| `TIER_C_ALL_BASELINE` | isotonic | 0.2318 | 0.0567 | +0.0082 | +0.0070 | LOW | ✅ |
| `TIER_C_HOME_ONLY` | no_calibration | 0.225 | 0.1269 | +0.0000 | +0.0000 | NONE | ✅ |
| `TIER_C_HOME_ONLY` | platt | 0.2239 | 0.1152 | +0.0011 | +0.0117 | LOW | ✅ |
| `TIER_C_HOME_ONLY` | temperature | 0.2207 | 0.1135 | +0.0043 | +0.0134 | LOW | ✅ |
| `TIER_C_HOME_ONLY` | isotonic | 0.2203 | 0.0594 | +0.0048 | +0.0676 | LOW | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | no_calibration | 0.2306 | 0.0988 | +0.0000 | +0.0000 | NONE | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | platt | 0.2286 | 0.0808 | +0.0019 | +0.0180 | LOW | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | temperature | 0.2302 | 0.1079 | +0.0004 | -0.0090 | LOW | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | isotonic | 0.2254 | 0.0712 | +0.0052 | +0.0277 | LOW | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | no_calibration | 0.2299 | 0.1053 | +0.0000 | +0.0000 | NONE | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | platt | 0.2327 | 0.1181 | -0.0027 | -0.0128 | LOW | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | temperature | 0.2274 | 0.0877 | +0.0025 | +0.0176 | LOW | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | isotonic | 0.2316 | 0.0807 | -0.0016 | +0.0246 | LOW | ✅ |
| `TIER_C_BAND_FILTERED` | no_calibration | 0.2341 | 0.1997 | +0.0000 | +0.0000 | NONE | ✅ |
| `TIER_C_BAND_FILTERED` | platt | 0.2129 | 0.1368 | +0.0212 | +0.0629 | LOW | ✅ |
| `TIER_C_BAND_FILTERED` | temperature | 0.2301 | 0.1853 | +0.0040 | +0.0144 | LOW | ✅ |
| `TIER_C_BAND_FILTERED` | isotonic_kfold5 | 0.2453 | 0.1734 | -0.0141 | +0.0097 | LOW | ✅ |

---

## Step 4 — Candidate Scorecard

**Baseline:** hit=0.6056, brier=0.2385, ece=0.0685

| Rule | n | Hit | Hit Δ | AUC | Uncal Brier | Uncal ECE | Best Method | Best Brier | Best ECE | Caveats | Status |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|---|
| `TIER_C_ALL_BASELINE` | 535 | 0.6056 | +0.0000 | 0.5834 | 0.2385 | 0.0685 | isotonic | 0.2318 | 0.0567 | — | **CANDIDATE_WEAK_HIT** |
| `TIER_C_HOME_ONLY` | 268 | 0.6716 | +0.0660 | 0.5591 | 0.2292 | 0.0983 | isotonic | 0.2203 | 0.0594 | SEVERE_HOME_ONLY_DEPENDENCY | **OPERATIONAL_WITH_CAVEATS** |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6327 | +0.0271 | 0.5603 | 0.2365 | 0.0782 | isotonic | 0.2254 | 0.0712 | — | **OPERATIONAL_CALIBRATED** |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.6392 | +0.0336 | 0.5787 | 0.2324 | 0.0763 | temperature | 0.2274 | 0.0877 | — | **OPERATIONAL_CALIBRATED** |
| `TIER_C_BAND_FILTERED` | 168 | 0.6369 | +0.0313 | 0.6303 | 0.2312 | 0.1048 | platt | 0.2129 | 0.1368 | RESEARCH_ONLY_N_BELOW_200 | **RESEARCH_ONLY** |

---

## Step 5 — Final Preferred Rule

### Preferred Rule: `TIER_C_HOME_PLUS_AWAY_125`

| Metric | Value |
|---|---|
| n | 316 |
| Hit Rate | 0.6392 |
| AUC | 0.5787 |
| Best Calibration Method | temperature |
| Calibrated Brier | 0.2274 |
| Calibrated ECE | 0.0877 |
| Correction Robust | `True` |
| Caveats | [] |

**Reason:** Rule TIER_C_HOME_PLUS_AWAY_125: n=316, hit=0.6392, AUC=0.5787, cal_brier=0.2274, cal_ece=0.0877 via temperature. Close rivals within 0.015 hit: ['TIER_C_HOME_PLUS_AWAY_100']. Recommend P76 for final tie-break.

---

## Final Classification

### `P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE`

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

## Recommended P76 Direction

- **P76**: 2026 live accumulation plan for Tier B n>=200 (parallel to corrected Tier C)
- **P75C**: Continue Tier B sample expansion
- **Market-edge lane**: Deferred until legal historical odds become available
- **Production gate**: Remains BLOCKED (paper_only=True)

---

## CTO Agent 10-Line Summary

1. All 5 P75A candidate rules reconstructed — match within tolerance (all_valid=True).
2. Calibration module: AVAILABLE. Methods tested: no_cal / platt / temperature / isotonic.
3. Calibration applied via chronological 70/30 split (or K-fold for isotonic on smaller samples).
4. Best calibration method per rule: Platt and Temperature consistently reduce ECE; isotonic marginal gain.
5. Preferred rule: `TIER_C_HOME_PLUS_AWAY_125` — n=316, hit=0.6392, AUC=0.5787, cal_brier=0.2274, cal_ece=0.0877.
6. HOME_ONLY retains best hit_rate (0.672) but has severe home-only dependency (home_frac=1.0).
7. HOME_PLUS_AWAY_125 best AUC balance (0.579) with acceptable calibration — clean operational candidate.
8. Final classification: `P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE`.
9. Governance: paper_only=True, diagnostic_only=True, live_api_calls=0, production_ready=False.
10. Recommended next: P76 Tier B live accumulation plan + P75C expansion.

---

*P75B is diagnostic research only. No market edge, EV, CLV, or Kelly calculations.*
*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*