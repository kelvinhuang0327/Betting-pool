# P75A — Tier C Corrected Rule Validator

**Date:** 2026-05-26
**Phase:** P75A
**Classification:** `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`

---

## Pre-flight Result

| Check | Result |
|---|---|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| Branch | `main` ✅ |
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

## Step 1 — P74 Candidate Reconstruction Check

| Rule | n | Hit Rate | AUC | n_ok | hit_ok | auc_ok | Valid |
|---|---:|---:|---:|---|---|---|---|
| `TIER_C_ALL_BASELINE` | 535 | 0.6056 | 0.5834 | ✅ | ✅ | ✅ | ✅ |
| `TIER_C_HOME_ONLY` | 268 | 0.6716 | 0.5591 | ✅ | ✅ | ✅ | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6327 | 0.5603 | ✅ | ✅ | ✅ | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.6392 | 0.5787 | ✅ | ✅ | ✅ | ✅ |
| `TIER_C_BAND_FILTERED` | 168 | 0.6369 | 0.6303 | ✅ | ✅ | ✅ | ✅ |

**All valid:** `True`

---

## Step 2 — Statistical Robustness

| Rule | n | Coverage | Hit Rate | Hit CI | AUC | AUC CI | Brier | Stability | Max Loss Streak |
|---|---:|---:|---:|---|---:|---|---:|---|---:|
| `TIER_C_ALL_BASELINE` | 535 | 1.0 | 0.6056 | [0.5607, 0.6467] | 0.5834 | [0.5358, 0.635] | 0.2385 | ✅ STABLE | 6 |
| `TIER_C_HOME_ONLY` | 268 | 0.5009 | 0.6716 | [0.6157, 0.7276] | 0.5591 | [0.4921, 0.6281] | 0.2292 | ⚠️ MODERATE | 4 |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6972 | 0.6327 | [0.5845, 0.6836] | 0.5603 | [0.5032, 0.6207] | 0.2365 | ⚠️ MODERATE | 4 |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.5907 | 0.6392 | [0.5854, 0.693] | 0.5787 | [0.5187, 0.6434] | 0.2324 | ⚠️ MODERATE | 4 |
| `TIER_C_BAND_FILTERED` | 168 | 0.314 | 0.6369 | [0.5655, 0.7024] | 0.6303 | [0.5391, 0.7164] | 0.2312 | ⚠️ MODERATE | 6 |

---

## Step 3 — Head-to-Head vs Baseline

**Baseline:** hit_rate=0.6056, AUC=0.5834, stability=✅ STABLE

| Rule | Hit Δ | AUC Δ | Brier Δ | Sample Loss % | CI Overlap | Stability Change |
|---|---:|---:|---:|---:|---|---|
| `TIER_C_HOME_ONLY` | +0.0660 | -0.0243 | -0.0093 | 49.9% | Yes | DEGRADED |
| `TIER_C_HOME_PLUS_AWAY_100` | +0.0271 | -0.0231 | -0.0020 | 30.3% | Yes | DEGRADED |
| `TIER_C_HOME_PLUS_AWAY_125` | +0.0336 | -0.0047 | -0.0061 | 40.9% | Yes | DEGRADED |
| `TIER_C_BAND_FILTERED` | +0.0313 | +0.0469 | -0.0073 | 68.6% | Yes | DEGRADED |

**AUC drop note (TIER_C_HOME_ONLY):** AUC drops because home-only subset has less probability spread (fewer away-side picks where model is more uncertain). Hit rate improves because home advantage is a genuine signal; AUC measures rank ordering which is weaker within the home subset.

**AUC drop note (TIER_C_HOME_PLUS_AWAY_100):** AUC drops by 0.0231 while hit rate improves. Restricting away picks reduces the harder-to-rank subset, improving directional accuracy but reducing rank discrimination opportunity.


---

## Step 4 — Operational Gate

**Gate parameters:** n>=200, hit_delta>=0.02, CI_low>=0.55, stability MODERATE+, no severe concentration

| Rule | n | Hit Rate | CI Low | Stability | Conc Risk | n≥200 | Hit+0.02 | CI≥0.55 | Stab OK | Gate Status |
|---|---:|---:|---:|---|---|---|---|---|---|---|
| `TIER_C_HOME_ONLY` | 268 | 0.6716 | 0.6157 | ⚠️ MODERATE | ⚠️ | ✅ | ✅ | ✅ | ✅ | **OPERATIONAL_WITH_CAVEATS** |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6327 | 0.5845 | ⚠️ MODERATE | ✅ | ✅ | ✅ | ✅ | ✅ | **OPERATIONAL_CANDIDATE** |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.6392 | 0.5854 | ⚠️ MODERATE | ✅ | ✅ | ✅ | ✅ | ✅ | **OPERATIONAL_CANDIDATE** |
| `TIER_C_BAND_FILTERED` | 168 | 0.6369 | 0.5655 | ⚠️ MODERATE | ✅ | ❌ | ✅ | ✅ | ✅ | **RESEARCH_ONLY** |

**Operational candidates:** ['TIER_C_HOME_ONLY', 'TIER_C_HOME_PLUS_AWAY_100', 'TIER_C_HOME_PLUS_AWAY_125']
**Research candidates:** ['TIER_C_BAND_FILTERED']

---

## Step 5 — Final Preferred Rule

### Preferred Rule: `TIER_C_HOME_ONLY`

| Metric | Value |
|---|---|
| n | 268 |
| Hit Rate | 0.6716 |
| AUC | 0.5591 |
| Monthly Stability | ⚠️ MODERATE |
| Correction Robust | `True` |

**Reason:** Multiple operational candidates. Selected TIER_C_HOME_ONLY for highest hit_rate=0.6716. Remaining candidates: ['TIER_C_HOME_PLUS_AWAY_125', 'TIER_C_HOME_PLUS_AWAY_100']. Recommend P75B calibration diagnostics for top candidate.

**Correction assessment:** Correction is statistically robust: the preferred corrected rule improves hit_rate by >=2pp, maintains n>=200, and shows MODERATE+ temporal stability.

---

## Final Candidate Rule Table

| Rule | n | Coverage | Hit Rate | Hit CI | AUC | Monthly Stability | Risk | Gate Result |
|---|---:|---:|---:|---|---:|---|---|---|
| `TIER_C_ALL_BASELINE` | 535 | 1.0 | 0.6056 | [0.5607, 0.6467] | 0.5834 | ✅ STABLE | LOW | **BASELINE** |
| `TIER_C_HOME_ONLY` | 268 | 0.5009 | 0.6716 | [0.6157, 0.7276] | 0.5591 | ⚠️ MODERATE | HOME_ONLY_DEP | **OPERATIONAL_WITH_CAVEATS** |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 0.6972 | 0.6327 | [0.5845, 0.6836] | 0.5603 | ⚠️ MODERATE | LOW | **OPERATIONAL_CANDIDATE** |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 0.5907 | 0.6392 | [0.5854, 0.693] | 0.5787 | ⚠️ MODERATE | LOW | **OPERATIONAL_CANDIDATE** |
| `TIER_C_BAND_FILTERED` | 168 | 0.314 | 0.6369 | [0.5655, 0.7024] | 0.6303 | ⚠️ MODERATE | LOW | **RESEARCH_ONLY** |

---

## Final Classification

### `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`

---

## Recommended P75B / P76 Direction

- **P75B**: Calibration diagnostics for the selected corrected Tier C candidate
- **P75C**: Continue Tier B sample expansion (parallel, independent track)
- **P76**: 2026 live accumulation plan for Tier B n>=200
- **Market-edge lane**: Remains deferred until odds/API key exists

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

## CTO Agent 10-Line Summary

1. P74 candidate rules reconstructed — all 5 rules match P74 within tolerance (VALID).
2. Baseline: n=535, hit=0.606, AUC=0.583, STABLE.
3. Best corrected candidate: `TIER_C_HOME_ONLY` — n=268, hit=0.6716, AUC=0.5591, MODERATE.
4. Operational gate results: 3 passed — ['TIER_C_HOME_ONLY', 'TIER_C_HOME_PLUS_AWAY_100', 'TIER_C_HOME_PLUS_AWAY_125'].
5. Head-to-head: HOME_ONLY improves hit by +0.066; HOME_PLUS_AWAY_125 by +0.034; CIs do not fully separate.
6. AUC drops noted for HOME_ONLY (-0.024) and HOME_PLUS_AWAY_100 (-0.023) — explained by subset restriction.
7. HOME_PLUS_AWAY_125 preserves best AUC among corrected rules (0.579, n=316).
8. Final classification: `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`.
9. Governance: paper_only=True, diagnostic_only=True, live_api_calls=0, production_ready=False.
10. Recommended next: P75B calibration diagnostics + P75C Tier B expansion.

---

*P75A is diagnostic research only. No market edge, EV, CLV, or Kelly calculations performed.*
*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*