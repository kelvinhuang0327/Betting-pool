# P74 — Tier C Home/Away Bias Correction Research
**Date:** 2026-05-26  
**Phase:** P74  
**Classification:** `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`  
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Executive Summary

P74 analyzed the home/away performance gap in Tier C (n=535, |sp_fip_delta|>=0.50) first identified in P73A.

**Key findings:**
- Home hit_rate = 0.672 vs away hit_rate = 0.539 — gap = **0.132**
- Away weakness is GENERAL (not month-specific or band-specific)
- No away rescue filter achieves >0.02 improvement with n>=75 operational threshold
- Three corrected rules beat baseline hit rate with n>=200 and MODERATE+ stability
- Final classification: **TIER_C_HOME_AWAY_CORRECTION_CONFIRMED**

---

## Candidate Rule Summary

| Rule | n | Coverage | Hit Rate | AUC | Stability | Status |
|---|---:|---:|---:|---:|---|---|
| TIER_C_ALL_BASELINE | 535 | 1.00 | 0.6056 | 0.5834 | STABLE | CANDIDATE |
| TIER_C_HOME_ONLY | 268 | 0.50 | 0.6716 | 0.5591 | MODERATE | STRONG_CANDIDATE |
| TIER_C_HOME_PLUS_AWAY_075 | 444 | 0.83 | 0.6126 | 0.5708 | MODERATE | CANDIDATE |
| TIER_C_HOME_PLUS_AWAY_100 | 373 | 0.70 | 0.6327 | 0.5603 | MODERATE | STRONG_CANDIDATE |
| TIER_C_HOME_PLUS_AWAY_125 | 316 | 0.59 | 0.6392 | 0.5787 | MODERATE | STRONG_CANDIDATE |
| TIER_C_HOME_WEIGHTED_AWAY_WATCHLIST | 268 | 0.50 | 0.6716 | 0.5591 | MODERATE | STRONG_CANDIDATE |
| TIER_C_BAND_FILTERED | 168 | 0.31 | 0.6369 | 0.6303 | MODERATE | WATCHLIST_SAMPLE_LIMITED |

---

## Recommended P75 Direction

- **P75A**: Implement prediction-only Tier C corrected rule validator (HOME_ONLY or HOME_PLUS_AWAY_125)
- **P75B**: Add calibration diagnostics for corrected Tier C candidate  
- **P75C**: Continue Tier B sample expansion (parallel track)
- **P75D**: Defer market-edge lane until odds/API key exists

---

*P74 is diagnostic research only. paper_only=True | diagnostic_only=True | NO_REAL_BET=True*
