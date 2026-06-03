# P72B — Prediction-vs-Market Objective Contract + P72A Decision Gate

**Date**: 2026-05-26  
**Classification**: `P72B_OBJECTIVE_CONTRACT_READY`

---

## Pre-flight

| Check | Value |
|---|---|
| Repo | /Users/kelvin/Kelvin-WorkSpace/Betting-pool |
| Branch | main |
| P72A commit | 5c2a26b ✅ |
| paper_only | True |
| uses_historical_odds | False |
| the_odds_api_key_required | False |

---

## Source Artifacts

- `data/mlb_2025/derived/p72a_odds_free_strategy_accuracy_backtest_summary.json` — loaded: True
- P72A classification: `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED`

---

## ⚠️ Interpretation Boundary

P72A confirmed the model has directional predictive skill (AUC > 0.50 across tiers). This means the model predicts game outcomes better than chance. It does NOT mean bets on this model produce positive expected value against market odds. Market edge requires: (1) odds data, (2) calibrated probability comparison to implied odds, (3) pregame timing integrity, (4) cross-year validation. None of these have been established for 2025 (P64–P66 showed negative edge -0.032).

---

## Objective / Metric Taxonomy — 5 Lanes

### Lane: `PREDICTION_ONLY` — Outcome Prediction Accuracy

| Field | Value |
|---|---|
| Odds required | False |
| API key required | False |
| Current status | **ACTIVE** |

**Allowed metrics**: AUC, Brier score, log-loss, hit rate, ECE (calibration), monthly stability, sample size, bootstrap CI, chronological stability

**Allowed conclusions**: predictive signal confirmed/weak/inconclusive/negative; accuracy ranking across strategies; sample-limited vs robust; model has directional skill; monthly consistency of accuracy

**Forbidden conclusions**: model generates profit (accuracy alone does not establish this); model probability beats implied market probability (requires odds comparison); closing-line advantage; betting recommendation; production deployment; Kelly fraction for real bets

> P72A operated entirely in this lane. Results are valid for ranking model accuracy. They do NOT establish market edge.

### Lane: `MARKET_EDGE` — Market Edge Diagnostic

| Field | Value |
|---|---|
| Odds required | True |
| API key required | True |
| Current status | **BLOCKED_AWAITING_ODDS** |
| Blocker | THE_ODDS_API_KEY not configured; 2024 CSV unavailable |

**Allowed metrics**: model probability (calibrated), market implied probability (no-vig), side mapping (home/away consistency), odds source trace, pregame timestamp, edge = model_prob - market_implied_prob

**Allowed conclusions**: paper-only market edge diagnostic; edge positive/negative/near-zero; edge stability across months

**Forbidden conclusions**: unconditional profit assertion; production recommendation (without cross-year validation); betting strategy ready for deployment

> P64–P66 attempted this lane with 2025 CSV odds. Mean edge = -0.032 (negative). Lane blocked for cross-year work. Unblocked only when historical odds API key is available.

### Lane: `CLV` — Closing Line Value Diagnostic

| Field | Value |
|---|---|
| Odds required | True |
| API key required | True |
| Current status | **BLOCKED_AWAITING_PREGAME_ODDS** |
| Blocker | No pregame timestamp-separated odds available; single-snapshot CSV only |

**Allowed metrics**: pregame opening odds (timestamped), closing odds (timestamped), line movement audit trail, side comparability check, minimum 1000 games for robust CLV estimate

**Allowed conclusions**: closing-line movement diagnostic; beat-the-close frequency

**Forbidden conclusions**: bettable edge (unless sample >= 1000 and cross-year validated)

> CLV requires time-series odds (opening → closing). 2025 CSV was a single post-game snapshot. Unblocked only with multi-snapshot historical feed.

### Lane: `EV_KELLY_BANKROLL` — Expected Value / Kelly / Bankroll Sizing

| Field | Value |
|---|---|
| Odds required | True |
| API key required | True |
| Current status | **BLOCKED_ODDS_AND_APPROVAL_REQUIRED** |
| Blocker | Requires odds + calibrated edge confirmation + CEO deployment approval |

**Allowed metrics**: calibrated model probability, market decimal odds, payout assumptions, bankroll policy, position sizing rules, risk control approval

**Allowed conclusions**: theoretical Kelly fraction (paper, diagnostic only); paper bankroll simulation (no real deployment)

**Forbidden conclusions**: deploy Kelly fractions to real bets (ever, without CEO approval); claim profitability from theoretical Kelly alone

> P62–P64 computed theoretical Kelly fractions for paper purposes only. kelly_deploy_allowed=False always. P72A AUC/hit-rate results are NOT inputs to this lane.

### Lane: `PRODUCTION_RECOMMENDATION` — Production Betting Recommendation

| Field | Value |
|---|---|
| Odds required | True |
| API key required | True |
| Current status | **BLOCKED** |

**Allowed metrics**: 

**Allowed conclusions**: 

**Forbidden conclusions**: any production recommendation while BLOCKED

> All 8 gates must pass before any production recommendation. P72A passes GATE_01 partially (accuracy confirmed, single 2025 season). GATE_03–GATE_08 remain blocked. No production recommendation is authorized.

---

## P72A Strategy Classification

| Strategy | n | AUC | Hit Rate | Sample Tier | Pred. Signal | Market Edge | Prod. Status | Role |
|---|---|---|---|---|---|---|---|---|
| `S00_BASELINE_ALL` | 2025 | 0.5716 | 0.5299 | HIGH | **CONFIRMED** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | BASELINE_REFERENCE |
| `S01_TIER_C_DIRECTIONAL` | 535 | 0.5834 | 0.6056 | HIGH | **CONFIRMED** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | PRIMARY_OPERATIONAL_CANDIDATE |
| `S02_TIER_B_DIRECTIONAL` | 98 | 0.6461 | 0.5918 | LOW | **CONFIRMED** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | BEST_AUC_DIAGNOSTIC_CANDIDATE |
| `S03_TIER_A_DIRECTIONAL` | 24 | 0.5546 | 0.7083 | SAMPLE_LIMITED | **SAMPLE_LIMITED** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | WATCHLIST_ONLY |
| `S04_TIER_C_PLATT_CALIBRATED` | 535 | 0.5932 | 0.5664 | HIGH | **CONFIRMED** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | CALIBRATION_REFERENCE |
| `S05_HOME_FAVOR_STRONG` | 268 | 0.5591 | 0.6716 | MEDIUM | **WEAK** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | HOME_ADVANTAGE_SIGNAL |
| `S06_AWAY_FAVOR_STRONG` | 267 | 0.545 | 0.5393 | MEDIUM | **WEAK** | NOT_EVALUATED_ODDS_REQUIRED | BLOCKED | AWAY_UNDERPERFORMER |

### Per-Strategy Notes

**`S00_BASELINE_ALL`** — BASELINE_REFERENCE
> Establishes random baseline for hit rate (53.0%) and AUC (0.572).
> **Recommended next**: Use as accuracy baseline for all future comparisons

**`S01_TIER_C_DIRECTIONAL`** — PRIMARY_OPERATIONAL_CANDIDATE
> n=535 with 6/6 monthly stability. Best balance of sample size and confirmed signal. Recommended for operational evaluation if odds ever available.
> **Recommended next**: P73A: Tier C deep-dive — sub-tier stability, home/away decomposition, bootstrap CI expansion

**`S02_TIER_B_DIRECTIONAL`** — BEST_AUC_DIAGNOSTIC_CANDIDATE
> Highest AUC (0.646) but n=98 and monthly stability=UNSTABLE. NOT production-ready. Research candidate only until n >= 200 and stability improves.
> **Recommended next**: P73B: Tier B sample expansion — expand to multi-year data if available; cross-validation

**`S03_TIER_A_DIRECTIONAL`** — WATCHLIST_ONLY
> n=24, SAMPLE_LIMITED. Hit rate 70.8% is statistically unreliable at this sample size. Wide CI [0.500, 0.875] confirms. Do not draw conclusions.
> **Recommended next**: Hold watchlist — do not evaluate until n >= 50

**`S04_TIER_C_PLATT_CALIBRATED`** — CALIBRATION_REFERENCE
> Platt calibration improves AUC (0.593 vs 0.583 raw) but reduces hit rate (0.566 vs 0.606). Better for probability accuracy; directional picks prefer raw.
> **Recommended next**: P73C: Compare raw vs Platt probability quality; evaluate if calibration helps future odds-lane work

**`S05_HOME_FAVOR_STRONG`** — HOME_ADVANTAGE_SIGNAL
> Hit rate 67.2% — strongest raw hit rate in the set. Home advantage may partially explain; needs home-bias adjustment for fair comparison.
> **Recommended next**: P73A: Include in Tier C deep-dive as home-side sub-analysis

**`S06_AWAY_FAVOR_STRONG`** — AWAY_UNDERPERFORMER
> Hit rate 53.9% barely above baseline. Away FIP delta advantage is not translating into outcomes at the same rate as home-favored games.
> **Recommended next**: Deprioritize; investigate why away picks underperform vs home picks

---

## Decision Thresholds

| Category | Threshold | Status |
|---|---|---|
| tier_c_operational_candidate | n>=500, AUC>=0.56, hit_rate>=0.58 | **MEETS_THRESHOLD** |
| tier_b_research_candidate | n>=75, AUC>=0.62, hit_rate>=? | **MEETS_THRESHOLD_WITH_CAVEATS** |
| tier_a_watchlist | n < 50 | **WATCHLIST_ONLY** |
| production_gate | see below | **BLOCKED** |

---

## Recommended P73 Paths

| Path | Priority | Odds Required | Blocker | Order |
|---|---|---|---|---|
| `P73A` — Tier C Operational Stability Deep-Dive | **PRIMARY** | False | None | 1 |
| `P73B` — Tier B Sample Expansion / Cross-Validation | **PRIMARY** | False | Low n — may need 2024 data for cross-year validation | 2 |
| `P73C` — Calibration Improvement for Odds-Free Probability | **SECONDARY** | False | None | 3 |
| `P73D` — Market-Edge Lane Resume (API Key Required) | **DEFERRED** | True | THE_ODDS_API_KEY not configured | 4 |
| `P73E` — Doubleheader Join Disambiguation | **SECONDARY** | False | None | 5 |

**Primary recommendation**: P73A + P73B (run in parallel if possible)
**Deferred**: P73D (pending API key)

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
| p72a_results_used_as_ev_evidence | False |
| p72a_results_used_as_clv_evidence | False |
| p72a_results_used_as_kelly_evidence | False |

---

## Forbidden Claims Scan

**Result**: CLEAN — 0 violations

Verified: no profitability claim, no EV claim, no CLV claim, no Kelly deployment, no production proposal.

---

## Key Findings

- **prediction_accuracy_confirmed**: True
- **market_edge_evaluated**: False
- **odds_used**: False
- **ev_calculated**: False
- **clv_calculated**: False
- **p72a_results_as_ev_or_clv**: False
- **production_blocked**: True
- **best_prediction_candidate**: S01_TIER_C_DIRECTIONAL (operational) + S02_TIER_B_DIRECTIONAL (research)
- **sample_limited_strategies**: ['S03_TIER_A_DIRECTIONAL']

---

## Final Classification: `P72B_OBJECTIVE_CONTRACT_READY`

---

## CTO Agent 10-Line Summary

1. P72B defines a 5-lane objective contract: PREDICTION_ONLY, MARKET_EDGE, CLV, EV_KELLY, PRODUCTION.
2. P72A operated entirely in PREDICTION_ONLY lane — no odds, no EV, no CLV.
3. S01_TIER_C (n=535, AUC=0.583, hit=0.606, 6/6 months) → PRIMARY OPERATIONAL CANDIDATE.
4. S02_TIER_B (n=98, AUC=0.646) → BEST AUC RESEARCH CANDIDATE, monthly stability UNSTABLE.
5. S03_TIER_A (n=24) → SAMPLE_LIMITED WATCHLIST ONLY — no conclusions safe.
6. Market edge lane BLOCKED — awaiting THE_ODDS_API_KEY and historical data.
7. Production recommendation lane BLOCKED — 7/8 gates pending.
8. Prediction accuracy ≠ positive EV — this boundary is formally enforced in contract.
9. Recommended next: P73A (Tier C deep-dive) + P73B (Tier B sample expansion).
10. P72B classification: P72B_OBJECTIVE_CONTRACT_READY.

---

### Next 24h Prompt

Run P73A — Tier C Operational Stability Deep-Dive:
- Sub-tier bands within Tier C (0.50–0.75 / 0.75–1.00 / 1.00–1.25)
- Home vs away decomposition within Tier C
- Pitcher identity stability (does the same pitcher matchup pattern repeat?)
- Bootstrap CI expansion with n_boot=5000
- Year-over-year note: 2024 data still unavailable; single-year caveat
- Run P73B in parallel: Tier B monthly volatility root cause

*paper_only=True | diagnostic_only=True | uses_historical_odds=False | live_api_calls=0*
*No EV claim | No CLV claim | No production proposal | No champion replacement*
