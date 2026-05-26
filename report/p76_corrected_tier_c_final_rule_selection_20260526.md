# P76 — Corrected Tier C Final Rule Selection + 2026 Accumulation Plan
**Date:** 2026-05-26  
**Phase:** P76  
**Classification:** `P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA`  
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Executive Summary

Scorecard delta = 0.0003 < threshold 0.02 — margin is too narrow to declare a clear winner. **Dual finalists retained** until 2026 live accumulation provides discriminating evidence. HOME_PLUS_AWAY_125 score=0.5543; HOME_PLUS_AWAY_100 score=0.5540.

---

## Finalist Metrics (from P75B)

| Rule | n | Hit | AUC | Cal Brier | Cal ECE | Cal Method | Coverage | Status |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.633 | 0.560 | 0.2254 | 0.0712 | isotonic | 0.70 | **OPERATIONAL_CALIBRATED** |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.639 | 0.579 | 0.2274 | 0.0877 | temperature | 0.59 | **OPERATIONAL_CALIBRATED** |

---

## Weighted Scorecard

Axis weights: Directional=30% | Calibration=25% | Coverage=20% | Stability/Risk=15% | Future Readiness=10%

| Axis | Weight | HOME_PLUS_AWAY_125 | HOME_PLUS_AWAY_100 | Winner |
|---|---:|---:|---:|---|
| directional | 30% | 0.430 | 0.337 | 125 ✓ |
| calibration | 25% | 0.434 | 0.509 | 100 ✓ |
| coverage | 20% | 0.690 | 0.816 | 100 ✓ |
| stability_risk | 15% | 0.750 | 0.750 | TIE |
| future_readiness | 10% | 0.662 | 0.501 | 125 ✓ |
| **TOTAL** | **100%** | **0.5543** | **0.5540** | **DUAL** |

---

## Decision

> Score delta 0.0003 < threshold 0.02. HOME_PLUS_AWAY_125 wins axes: ['directional', 'future_readiness'] (score=0.5543); HOME_PLUS_AWAY_100 wins axes: ['calibration', 'coverage'] (score=0.5540). Dual finalists retained pending 2026 live accumulation data.

**Classification:** `P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA`

---

## 2026 Accumulation Plan

- **Primary rule:** `TIER_C_HOME_PLUS_AWAY_125`
- **Shadow rule(s):** `TIER_C_HOME_PLUS_AWAY_100`
- **Accumulation window:** 2026-04-01 → 2026-10-31
- **Stop criteria:** Rolling 100-game hit_rate < 0.55 → halt + P_REVIEW
- **Tier B trigger:** n >= 200 (expected ~2026-09)
- **Market-edge:** DEFERRED — THE_ODDS_API_KEY acquired AND historical odds for 2025-2026 available

### Monthly Cadence

| Month | Action |
|---|---|
| 2026-06 | First mid-season check-in (P77). Collect Tier C 2026 games. |
| 2026-07 | Tier B count check. Rolling accuracy monitor. |
| 2026-08 | Mid-season stability review. Adjust shadow rule if needed. |
| 2026-09 | P78 trigger: if Tier B n>=200, run sample expansion analysis. |
| 2026-10 | End-season consolidation. Final 2026 accuracy report. |
| 2026-11 | P80 trigger: if odds API key acquired, run market-edge analysis. |

---

## Research Roadmap P76 → P81

| Phase | Name | Target | Gate | Status |
|---|---|---|---|---|
| **P76** | Corrected Tier C Final Rule Selection + 2026 Accumulation Plan | 2026-05-26 | Scorecard delta >= 0.02 for selection; else dual retention.... | CURRENT |
| **P77** | 2026 Mid-Season Check-in (Tier C Live Accumulation) | 2026-06-30 | n>=30 games in 2026 season. Rolling hit_rate > 0.55.... | PLANNED |
| **P78** | Tier B Sample Expansion Analysis | 2026-09-30 | Tier B n>=200 confirmed by P77 accumulation.... | PLANNED |
| **P79** | Combined Tier Analysis (Tier B + Tier C) | 2026-10-31 | Both Tier B and Tier C have n>=200 in 2026 data.... | PLANNED |
| **P80** | Market-Edge Integration (Odds-Lane) | 2026-11-30 | Requires THE_ODDS_API_KEY and >=100 games with pregame odds.... | DEFERRED |
| **P81** | Strategy Finalization + Research Archive | 2026-12-31 | All prior phases complete; paper_only=True maintained throug... | PLANNED |

---

*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*