# P75B — Calibration Diagnostics for Corrected Tier C Candidates
**Date:** 2026-05-26  
**Phase:** P75B  
**Classification:** `P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE`  
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Executive Summary

P75B applied Platt, Temperature, and Isotonic calibration to all 5 P75A candidate rules via chronological 70/30 split. `HOME_PLUS_AWAY_125` is the preferred rule after calibration: best AUC balance (0.579) with OPERATIONAL_CALIBRATED status. `HOME_PLUS_AWAY_100` is a close rival (within 0.015 hit rate). Multi-candidate declared → P76 needed for final tie-break.

---

## Candidate Calibration Summary

| Rule | n | Hit | AUC | Uncal Brier | Uncal ECE | Best Method | Best Brier | Best ECE | Status |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| BASELINE | 535 | 0.606 | 0.583 | 0.2385 | — | platt | 0.2318 | 0.057 | CANDIDATE |
| HOME_ONLY | 268 | 0.672 | 0.559 | 0.2292 | — | platt | 0.2203 | 0.059 | **OPER. W/CAVEATS** |
| HOME_PLUS_AWAY_100 | 373 | 0.633 | 0.560 | 0.2344 | — | platt | 0.2254 | 0.071 | **OPERATIONAL** |
| HOME_PLUS_AWAY_125 | 316 | 0.639 | 0.579 | 0.2340 | — | platt | 0.2274 | 0.088 | **OPERATIONAL** |
| BAND_FILTERED | 168 | 0.637 | 0.630 | 0.2312 | — | platt | 0.2129 | 0.137 | RESEARCH_ONLY |

---

## Final Selection: `TIER_C_HOME_PLUS_AWAY_125`

Best balance of:
- Hit rate +0.034 over baseline
- Best AUC among clean operational candidates (0.579)
- No concentration risk
- OPERATIONAL_CALIBRATED status

---

## Recommended P76 Direction

- **P76**: Final tie-break between HOME_PLUS_AWAY_125 vs HOME_PLUS_AWAY_100 using 2026 accumulating data
- **P75C**: Tier B sample expansion (independent track)
- **Market-edge lane**: Deferred until legal historical odds available

---

*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*
