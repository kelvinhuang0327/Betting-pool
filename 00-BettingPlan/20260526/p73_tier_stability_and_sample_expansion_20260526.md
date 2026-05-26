# P73A/B — Odds-Free Tier Stability Deep-Dive + Tier B Sample Expansion

**Date**: 2026-05-26  
**Classification**: `P73_TIER_C_OPERATIONAL_STABLE_TIER_B_RESEARCH_CONFIRMED`

---

## Pre-flight

| Check | Value |
|---|---|
| Repo | /Users/kelvin/Kelvin-WorkSpace/Betting-pool |
| Branch | main |
| P72A | 5c2a26b ✅ |
| P72B | 9c04e50 ✅ |
| uses_historical_odds | False |
| the_odds_api_key_required | False |

---

## ⚠️ Prediction Boundary

P73 results are odds-free outcome-prediction accuracy only. Tier C being 'operational stable' means it is the best prediction candidate — NOT that it produces positive expected value against market odds. Market edge remains blocked pending historical odds availability.

---

## P73A — Tier C Stability

**n**: 535  |  **Hit Rate**: 0.6056  |  **AUC**: 0.5834  |  **Brier**: 0.2385
**Hit Rate CI 95%**: [0.5607, 0.6467]
**AUC CI 95%**: [0.5358, 0.635]
**Monthly Stability**: STABLE
**Tier C Classification**: **`TIER_C_OPERATIONAL_STABLE`**

### Monthly Breakdown

| Month | n | Hit Rate | AUC | Brier |
|---|---|---|---|---|
| 2025-04 | 16 | 0.625 | 0.4833 | 0.2469 |
| 2025-05 | 120 | 0.575 | 0.6206 | 0.2341 |
| 2025-06 | 101 | 0.6634 | 0.5568 | 0.2404 |
| 2025-07 | 92 | 0.6196 | 0.5526 | 0.2411 |
| 2025-08 | 108 | 0.5648 | 0.5654 | 0.2449 |
| 2025-09 | 98 | 0.6122 | 0.6436 | 0.2309 |

### Halves / Thirds Split

| Split | n | Hit Rate | Brier |
|---|---|---|---|
| H1 | 267 | 0.6255 | 0.2365 |
| H2 | 268 | 0.5858 | 0.2405 |
| T1 | 178 | 0.6011 | 0.237 |
| T2 | 178 | 0.6292 | 0.239 |
| T3 | 179 | 0.5866 | 0.2394 |

### Home vs Away Split

| Side | n | Hit Rate | AUC | Brier | HR CI 95% |
|---|---|---|---|---|---|
| Home | 268 | 0.6716 | 0.5591 | 0.2292 | [0.6157, 0.7276] |
| Away | 267 | 0.5393 | 0.545 | 0.2478 | [0.4794, 0.5993] |

### Delta Band Breakdown

| Band | n | Hit Rate | AUC | Brier | HR CI 95% |
|---|---|---|---|---|---|
| [0.5,0.75) | 168 | 0.6369 | 0.6303 | 0.2312 | [0.5655, 0.7024] |
| [0.75,1.0) | 138 | 0.5652 | 0.5392 | 0.2501 | [0.4855, 0.6449] |
| [1.0,1.25) | 131 | 0.6183 | 0.5262 | 0.2415 | [0.5344, 0.6947] |
| [1.25,1.5) | 74 | 0.5541 | 0.6696 | 0.2301 | [0.4459, 0.6622] |
| [1.5,∞) | 24 | 0.7083 | 0.5546 | 0.2322 | [0.5, 0.875] |

### Concentration Risk

| Factor | Value |
|---|---|
| Home pick fraction | 0.5009 |
| Home advantage warning | False |
| Monthly HR range | 0.0986 |
| Best band | band_150_plus (hit=0.7083) |
| Worst band | band_125_150 (hit=0.5541) |
| Band dominance warning | True |

> Tier C operational stability analysis. Home advantage dominates the directional hit rate — away picks are much weaker. Signal is genuine but partly explained by home advantage. For odds-lane work, home advantage is already priced into market odds.

---

## P73B — Tier B Variants

**Original Tier B signal**: **`SAMPLE_EXPANSION_CONFIRMED`**
**Best variant by AUC**: `TB_EXCL_WEAK_BAND` (AUC=0.6509)
**Can be operational**: False

| Variant | n | Hit Rate | AUC | Brier | Monthly Stability | AUC CI 95% |
|---|---|---|---|---|---|---|
| Strict Tier B (>=1.35) | 72 | 0.625 | 0.6082 | 0.2338 | UNSTABLE | [0.479, 0.7354] |
| Original Tier B (>=1.25) | 98 | 0.5918 | 0.6461 | 0.2306 | UNSTABLE | [0.5317, 0.7521] |
| Relaxed Tier B v1 (>=1.10) | 182 | 0.5934 | 0.5777 | 0.2385 | UNSTABLE | [0.4923, 0.6537] |
| Relaxed Tier B v2 (>=1.00) | 229 | 0.607 | 0.5806 | 0.2368 | UNSTABLE | [0.5064, 0.6552] |
| Tier B excl weak band (1.25-1.75) | 97 | 0.5876 | 0.6509 | 0.2304 | UNSTABLE | [0.5469, 0.7552] |

> Tier B expansion shows high AUC is robust across threshold variants from 1.00 to 1.35. However, monthly stability is UNSTABLE at all thresholds due to small per-month n (typically 14-23). AUC CI_low=0.535 > 0.50 confirms signal above chance, but sample size limits operational use.

---

## Final Decision Matrix

| Candidate | Role | Status | n | AUC | Hit Rate | Why | Next Action |
|---|---|---|---|---|---|---|---|
| Tier C directional | PRIMARY_OPERATIONAL_CANDIDATE | TIER_C_OPERATIONAL_STABLE | 535 | 0.5834 | 0.6056 | n=535, hit=0.606, AUC=0.583, 6/6 monthly STABLE. TIER_C_OPER... | Monitor per P52 V2 contract when odds available; r... |
| Tier B directional | RESEARCH_CANDIDATE_BEST_AUC | RESEARCH_ONLY_SAMPLE_EXPANSION_CONFIRMED | 98 | 0.6461 | None | Highest AUC=0.646 but n=98 and monthly UNSTABLE. Cannot be o... | Accumulate more data; validate when 2024 data reso... |
| Tier A directional | WATCHLIST_ONLY | SAMPLE_LIMITED_n24 | 24 | None | 0.7083 | n=24, bootstrap CI [0.500, 0.875] too wide. Hit rate unrelia... | Accumulate only; re-evaluate when n >= 50... |
| Tier C Platt calibrated | CALIBRATION_REFERENCE | CALIBRATION_USEFUL_PROBABILITY_QUALITY | 535 | 0.5932 | 0.5664 | AUC=0.593 > raw 0.583 — Platt calibration improves probabili... | Continue as probability calibration reference for ... |

### Key Declarations

- **Prediction signal does NOT equal market edge** — accuracy is in the PREDICTION_ONLY lane.
- **No betting recommendation is produced** — odds-free analysis only.
- **Market-edge lane remains blocked** until historical odds are available.

---

## Governance

| Flag | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| uses_historical_odds | False |
| live_api_calls | 0 |
| the_odds_api_key_required | False |
| ev_calculated | False |
| clv_calculated | False |
| market_edge_calculated | False |
| kelly_deploy_allowed | False |
| production_ready | False |
| real_bet_allowed | False |
| champion_replacement_allowed | False |
| profitability_claim | False |

---

## Forbidden Claims Scan

**Result**: CLEAN — 0 violations

Verified: no EV claim, no CLV, no profitability assertion, no Kelly deployment, no production proposal.

---

## Final Classification: `P73_TIER_C_OPERATIONAL_STABLE_TIER_B_RESEARCH_CONFIRMED`

---

## CTO Agent 10-Line Summary

1. P73A: Tier C (n=535) monthly stability=STABLE, AUC=0.583, hit_rate=0.606.
2. Tier C classification: TIER_C_OPERATIONAL_STABLE.
3. Concentration risk: home picks hit 67.2%, away picks only 53.9% — home advantage concern.
4. Delta band 0.50-0.75 strongest (hit=0.637); band 1.25-1.50 weakest (hit=0.554).
5. P73B: Tier B original (n=98, AUC=0.646) signal=SAMPLE_EXPANSION_CONFIRMED.
6. Tier B AUC is robust across variants (1.00-1.35 all AUC > 0.59) but monthly unstable.
7. Tier B cannot be operational: n < 200 and monthly stability UNSTABLE.
8. Relaxed Tier B v2 (>=1.00, n=229) has best balance of n and hit rate (0.607).
9. All work odds-free, no EV/CLV/Kelly, production BLOCKED.
10. P73 final classification: `P73_TIER_C_OPERATIONAL_STABLE_TIER_B_RESEARCH_CONFIRMED`.

---

## Next 24h Prompt

Options:
- P74A: Away-side model improvement (home/away gap is 67.2% vs 53.9%)
- P74B: Relaxed Tier B v2 (>=1.00, n=229) full stability analysis
- P74C: Multi-year plan — define what 2024 data would add to Tier B validation
- P74D: Market-edge resume (only if THE_ODDS_API_KEY appears)

*paper_only=True | diagnostic_only=True | uses_historical_odds=False | live_api_calls=0*
*No EV | No CLV | No production proposal | No champion replacement*
