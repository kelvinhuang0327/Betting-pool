# MLB Daily Advisory — Dry-run MVP Report

> **⚠️ PAPER-ONLY — DRY-RUN — NO REAL BET — NO PROFIT CLAIM**
>
> 本報告所有投注建議均為 paper-only 模擬，不代表任何真實下注、
> 真實獲利、或真實 edge 聲明。所有結果僅供研究與回測使用。

**Date:** 2025-07-01
**Requested Mode:** replay
**Effective Mode:** replay
**Total Advisories:** 12
**Report Generated:** 2026-05-07T06:56:13.429663+00:00

---

## Safety Flags

- **production_modified**: `False`
- **candidate_patch_created**: `False`
- **alpha_modified**: `False`
- **prediction_jsonl_overwritten**: `False`
- **no_edge_claim**: `True`
- **no_profit_claim**: `True`
- **diagnostic_only**: `True`
- **paper_only**: `True`
- **no_real_bet**: `True`

---

## Market Coverage Matrix

| Market | Available | Notes |
|--------|-----------|-------|
| moneyline | ✅ YES | moneyline: available via model_home_prob + market_home_prob_no_vig |
| runline | ❌ NO | runline: UNAVAILABLE — run line spread/odds not in prediction JSONL |
| total | ❌ NO | total: UNAVAILABLE — totals line/odds not in prediction JSONL |
| result | ✅ YES |  |
| odds | ❌ NO | runline: UNAVAILABLE — run line spread/odds not in prediction JSONL |
| market_home_prob | ✅ YES | moneyline: available via model_home_prob + market_home_prob_no_vig |
| closing_market | ❌ NO |  |

---

## Advisory Summary

| Metric | Value |
|--------|-------|
| Total Advisories | 12 |
| PASS | 5 |
| WATCH_ONLY | 2 |
| LEAN (HOME+AWAY) | 4 |
| MARKET_ONLY_SHADOW | 1 |
| Ledger Entries Written | 7 |
| Pending Review | 0 |
| Reviewed | 7 |

**Paper bet W/L:** 3W / 1L / 0P

---

## Brier Score (Metrics SSOT)

- **n**: 12
- **brier**: 0.2272
- **baseline_brier**: 0.2222
- **bss_vs_baseline**: -0.0225
- **ssot_function**: `calculate_brier_score`

---

## Game Advisories

| # | Date | Away | Home | Model | Market | Gap | ML Rec | Risk Flags |
|---|------|------|------|-------|--------|-----|--------|------------|
| 1 | 2025-07-01 | New York Yankees | Toronto Blue Jays | 0.517 | 0.401 | +0.116 | **LEAN_HOME** | — |
| 2 | 2025-07-01 | St. Louis Cardinals | Pittsburgh Pirates | 0.510 | 0.583 | -0.073 | **WATCH_ONLY** | — |
| 3 | 2025-07-01 | Minnesota Twins | Miami Marlins | 0.555 | 0.438 | +0.117 | **LEAN_HOME** | — |
| 4 | 2025-07-01 | Athletics | Tampa Bay Rays | 0.636 | 0.607 | +0.029 | **PASS** | — |
| 5 | 2025-07-01 | Cincinnati Reds | Boston Red Sox | 0.502 | 0.522 | -0.020 | **PASS** | MODEL_MARKET_NEAR_IDENTICAL |
| 6 | 2025-07-01 | Los Angeles Angels | Atlanta Braves | 0.522 | 0.651 | -0.129 | **LEAN_AWAY** | — |
| 7 | 2025-07-01 | Cleveland Guardians | Chicago Cubs | 0.618 | 0.639 | -0.021 | **PASS** | — |
| 8 | 2025-07-01 | Baltimore Orioles | Texas Rangers | 0.525 | 0.630 | -0.105 | **LEAN_AWAY** | — |
| 9 | 2025-07-01 | Houston Astros | Colorado Rockies | 0.340 | 0.438 | -0.098 | **WATCH_ONLY** | — |
| 10 | 2025-07-01 | Kansas City Royals | Seattle Mariners | 0.592 | 0.553 | +0.039 | **PASS** | — |
| 11 | 2025-07-01 | San Francisco Giants | Arizona Diamondbacks | 0.552 | 0.543 | +0.009 | **PASS** | MODEL_MARKET_NEAR_IDENTICAL |
| 12 | 2025-07-01 | Chicago White Sox | Los Angeles Dodgers | 0.696 | 0.745 | -0.048 | **MARKET_ONLY_SHADOW** | IN_PHASE71_DERISK_BAND |

---

## Feedback Loop — Failure Notes

### Observations
- 4 LEAN recommendation(s) generated; lean_accuracy=0.75
- 1 paper bet(s) resulted in LOST outcome this session
- 1 game(s) in Phase71/72 de-risk band [0.65,0.70); MARKET_ONLY_SHADOW applied; no lean generated per Phase72 governance

### Suspected Failure Modes
- model-market divergence at open may not persist to game time; line movement risk not modeled

### Proposed Next Audit
- Accumulate 30+ replay sessions to evaluate lean accuracy stability
- Cross-reference LEAN outcomes with Phase71 market superiority segments
- Monitor MARKET_ONLY_SHADOW outcomes vs LEAN outcomes across sessions
- Evaluate whether model-market gap > 0.10 is predictive in out-of-band games

**Blocked Auto Change:** human_review_required: governance rules prohibit auto-modification of model, alpha, or stake sizing based on dry-run advisory results
**human_review_required:** `True`
**alpha_change_blocked:** `True`
**model_change_blocked:** `True`

---

## Phase Chain

- **phase69_gate**: `CALIBRATION_OBJECTIVE_NOT_PROMISING`
- **phase70_gate**: `MARKET_ONLY_SUPERIOR`
- **phase71_gate**: `MARKET_DE_RISK_GUARD_PROMISING`
- **phase72_gate**: `MARKET_DERISK_GUARD_SPEC_READY`
- **metrics_ssot_gate**: `METRICS_SSOT_FOUNDATION_READY`

---

## Gate Conclusion

**Gate: `MLB_DAILY_ADVISORY_LEDGER_READY`**

> Replay mode produced: advisory + append-only ledger + reviewed results + Brier metrics (metrics_ssot) + failure notes + paper-only safety flags

---

## No Profit Claim

本系統不聲稱已找到可盈利的投注 edge。所有 paper advisory 均為研究目的，不代表任何真實獲利預期。Brier score 與其他 metrics 僅為統計診斷工具。

**NO_PROFIT_CLAIM = True**
**NO_EDGE_CLAIM = True**
**PAPER_ONLY = True**
**NO_REAL_BET = True**

---

## Completion Marker

`MLB_DAILY_ADVISORY_REPLAY_LEDGER_VERIFIED`

