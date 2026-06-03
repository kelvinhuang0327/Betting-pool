# P75A — Tier C Corrected Rule Validator
**Date:** 2026-05-26  
**Phase:** P75A  
**Classification:** `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`  
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Executive Summary

P75A formally validated P74's corrected Tier C rules. Three rules pass operational gate.
Two pass fully (HOME_PLUS_AWAY_100, HOME_PLUS_AWAY_125); HOME_ONLY passes with caveat (severe home-only dependency).

**Multiple operational candidates → calibration diagnostics needed (P75B).**

---

## Final Candidate Rule Table

| Rule | n | Coverage | Hit | Hit CI | AUC | Stability | Risk | Gate |
|---|---:|---:|---:|---|---:|---|---|---|
| `TIER_C_ALL_BASELINE` | 535 | 1.00 | 0.6056 | [0.561, 0.647] | 0.5834 | ✅ STABLE | LOW | BASELINE |
| `TIER_C_HOME_ONLY` | 268 | 0.50 | 0.6716 | [0.616, 0.728] | 0.5591 | ⚠️ MODERATE | HOME_ONLY_DEP | **OPER. W/CAVEATS** |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.70 | 0.6327 | [0.585, 0.679] | 0.5603 | ⚠️ MODERATE | LOW | **OPERATIONAL** |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.59 | 0.6392 | [0.585, 0.692] | 0.5787 | ⚠️ MODERATE | LOW | **OPERATIONAL** |
| `TIER_C_BAND_FILTERED` | 168 | 0.31 | 0.6369 | [0.565, 0.708] | 0.6303 | ⚠️ MODERATE | LOW | RESEARCH_ONLY |

---

## Key Finding: HOME_PLUS_AWAY_125 Best Overall Balance

- Highest AUC among fully-operational candidates (0.579)
- +0.034 hit rate over baseline with only −0.005 AUC drop
- n=316, CI_low=0.585 ✅

---

## Recommended P75B / P76 Direction

- **P75B**: Calibration diagnostics comparing HOME_PLUS_AWAY_125 vs HOME_ONLY vs HOME_PLUS_AWAY_100
- **P75C**: Tier B sample expansion (parallel, independent)
- **P76**: 2026 live accumulation plan for Tier B n>=200
- **Market-edge lane**: Deferred until odds/API key exists

---

*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*
