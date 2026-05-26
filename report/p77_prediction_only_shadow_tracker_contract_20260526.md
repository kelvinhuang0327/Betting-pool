# P77 — 2026 Prediction-Only Shadow Tracker Contract

> **Date**: 2026-05-26  
> **Classification**: `P77_SHADOW_TRACKER_CONTRACT_READY`  
> **Mode**: paper_only=true | diagnostic_only=true | NO_REAL_BET=true

---

## 1. Pre-flight / Source Artifacts

All 9 required source artifacts verified:  
- `p72a_json`: `p72a_odds_free_strategy_accuracy_backtest_summary.json`
- `p72b_json`: `p72b_objective_metric_contract_summary.json`
- `p73_json`: `p73_tier_stability_and_sample_expansion_summary.json`
- `p74_json`: `p74_tier_c_home_away_bias_correction_summary.json`
- `p75a_json`: `p75a_tier_c_corrected_rule_validator_summary.json`
- `p75b_json`: `p75b_calibration_diagnostics_corrected_tier_c_summary.json`
- `p76_json`: `p76_corrected_tier_c_final_rule_selection_summary.json`
- `p76_md`: `p76_corrected_tier_c_final_rule_selection_20260526.md`
- `predictions_jsonl`: `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`

---

## 2. P76 Dual-Finalist Verification

| Field | Value | Expected |
|-------|-------|----------|
| Classification | `P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA` | `P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA` |
| HOME_PLUS_AWAY_125 score | 0.5543 | 0.5543 |
| HOME_PLUS_AWAY_100 score | 0.554 | 0.5540 |
| Score delta | 0.0003 | 0.0003 |
| Tie-break threshold | 0.02 | 0.02 |
| Dual finalists | True | True |
| Primary tracking rule | `TIER_C_HOME_PLUS_AWAY_125` | `TIER_C_HOME_PLUS_AWAY_125` |
| Shadow tracking rule | `TIER_C_HOME_PLUS_AWAY_100` | `TIER_C_HOME_PLUS_AWAY_100` |
| Accumulation plan | True | True |

**Verification**: PASS ✅

---

## 3. 2026 Shadow Tracker Row Schema

Schema version: `p77-v1`  
Total fields: 28  
Required fields: 25  
Governance fields: 8

### Governance Fields (all frozen)

| Field | Frozen Value |
|-------|-------------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `market_edge_evaluated` | `False` |
| `odds_used` | `False` |
| `ev_calculated` | `False` |
| `clv_calculated` | `False` |
| `kelly_calculated` | `False` |
| `production_ready` | `False` |

---

## 4. Rule Computation Contract

### TIER_C_HOME_PLUS_AWAY_125 (`primary_tracking_rule`)

Tier C home picks (abs_sp_fip_delta >= 0.50, home advantage) + Tier C away picks (abs_sp_fip_delta >= 1.25, away advantage).

- **Predicted side**: sign(sp_fip_delta) — positive → home, negative → away, zero → home
- **Home threshold**: `abs_sp_fip_delta >= 0.5`
- **Away threshold**: `abs_sp_fip_delta >= 1.25`
- **Market-edge fields used**: False
- **Function**: `compute_selected_rule_home_plus_away_125_flag`

### TIER_C_HOME_PLUS_AWAY_100 (`shadow_tracking_rule`)

Tier C home picks (abs_sp_fip_delta >= 0.50, home advantage) + Tier C away picks (abs_sp_fip_delta >= 1.00, away advantage).

- **Predicted side**: sign(sp_fip_delta) — positive → home, negative → away, zero → home
- **Home threshold**: `abs_sp_fip_delta >= 0.5`
- **Away threshold**: `abs_sp_fip_delta >= 1.0`
- **Market-edge fields used**: False
- **Function**: `compute_shadow_rule_home_plus_away_100_flag`

### TIER_B_CANDIDATE (`accumulation_tracking`)

Mid-band games: abs_sp_fip_delta in [0.25, 0.50). Tracks below-Tier-C pitcher matchups. Requires n>=200 before P78 full analysis.


- **Home threshold**: `abs_sp_fip_delta >= 0.25`
- **Away threshold**: `abs_sp_fip_delta >= 0.5`
- **Market-edge fields used**: False
- **Function**: `compute_tier_b_candidate_flag`

### TIER_A_WATCHLIST (`watchlist_only`)

Highest conviction: abs_sp_fip_delta >= 1.50. Track but do not operationalize while n < 50.


- **Home threshold**: `abs_sp_fip_delta >= 1.5`
- **Lower bound**: `1.5`
- **Market-edge fields used**: False
- **Function**: `compute_tier_a_watchlist_flag`

### Semantic Validation (2025 Data)

| Rule | Computed n | Expected n | Match |
|------|-----------|-----------|-------|
| `TIER_C_HOME_ONLY` | 268 | 268 | ✅ |
| `TIER_C_HOME_PLUS_AWAY_100` | 373 | 373 | ✅ |
| `TIER_C_HOME_PLUS_AWAY_125` | 316 | 316 | ✅ |

**All counts match P75B**: ✅ PASS

---

## 5. Monthly Metrics Contract

Computed per rule, per month (no odds metrics):  

| Metric | Description |
|--------|-------------|
| `n` | Number of games in this rule for this month |
| `hit_rate` | Fraction of games where predicted_side == actual_winner |
| `hit_rate_ci_95` | Wilson 95% confidence interval for hit_rate |
| `auc` | ROC-AUC if probability distribution supports it (requires n >= 20) |
| `brier` | Brier score (lower = better calibration) |
| `log_loss` | Log-loss (lower = better) |
| `ece` | Expected Calibration Error |
| `home_n` | Count of home-side picks in this rule-month |
| `away_n` | Count of away-side picks in this rule-month |
| `home_hit_rate` | Hit rate for home-side picks only |
| `away_hit_rate` | Hit rate for away-side picks only |
| `tier_b_n` | Running total of Tier B candidate rows (abs_sp_fip_delta 0.25–0.50) |
| `tier_a_n` | Running total of Tier A watchlist rows (abs_sp_fip_delta >= 1.50) |
| `rolling_100_hit_rate` | Rolling 100-game hit rate (reported if cumulative n >= 100) |

**2026 Monthly Cadence:**

| Month | Action |
|-------|--------|
| 2026-06 | First P77 check-in. Collect Tier C 2026 games. Compute June hit_rate. Report rule counts. |
| 2026-07 | Tier B count check. Rolling accuracy monitor. Compute 3-month cumulative stats. |
| 2026-08 | Mid-season stability review. Adjust shadow rule if downgrade criteria met. |
| 2026-09 | P78 trigger: if Tier B n >= 200, launch sample expansion analysis. |
| 2026-10 | End-season consolidation. Final 2026 accuracy report. Compute full-season AUC/Brier/ECE. |
| 2026-11 | P80 trigger: if odds API key acquired, run market-edge analysis (deferred lane). |

---

## 6. Re-evaluation Triggers

### Tier C Selected/Shadow Re-evaluation

| Checkpoint | n Threshold | Action |
|------------|------------|--------|
| checkpoint_1 | 50 | First interim accuracy check — no downgrade unless hit_rate < 0.50 for all games so far |
| checkpoint_2 | 100 | Rolling 100-game hit rate becomes available. Downgrade if hit_rate < 0.55. |
| operational_checkpoint | 200 | Full re-evaluation: compare primary vs shadow, update preferred rule. |
| seasonal_checkpoint | end_of_2026_regular_season | Final 2026 accuracy report. Decision on 2027 tracking configuration. |

**Downgrade Criteria:**

- **rolling_100_floor**: Rolling 100-game hit_rate < 0.55 → Halt primary rule tracking. Escalate to P_REVIEW phase.
- **consecutive_monthly_floor**: Monthly hit_rate < 0.5 for 2 consecutive eligible months (n >= 10) → Flag rule as degraded. Promote shadow rule to primary if shadow is stable.
- **ece_worsening**: ECE materially worsens vs P75B baseline (delta ECE > 0.03 sustained over 2+ months) → Trigger calibration review. Do not downgrade on a single month.

### Tier B Re-evaluation

- Rule: `TIER_B_ABS_DELTA_025_050`
- Trigger when: **n >= 200** (expected 2026-09)
- Phase: **P78**
- Pre-trigger status: `research_only`

### Tier A Watchlist

- Rule: `TIER_A_WATCHLIST_ABS_DELTA_150_PLUS`
- Operational minimum: **n >= 50**
- Status: `watchlist_only`

### Market-Edge Lane

- Status: **DEFERRED** (blocked in P77)
- Required condition: THE_ODDS_API_KEY acquired AND historical odds for 2025-2026 available
- Trigger phase: P80
- Separation guarantee: Market-edge analysis (CLV/EV/Kelly) is kept in a separate, blocked lane. It CANNOT activate without explicit authorization and live odds data.

---

## 7. Governance Invariants

| Invariant | Value |
|-----------|-------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `uses_historical_odds` | `False` |
| `live_api_calls` | `0` |
| `the_odds_api_key_required` | `False` |
| `odds_used` | `False` |
| `ev_calculated` | `False` |
| `clv_calculated` | `False` |
| `market_edge_evaluated` | `False` |
| `kelly_calculated` | `False` |
| `kelly_deploy_allowed` | `False` |
| `production_ready` | `False` |
| `real_bet_allowed` | `False` |
| `champion_replacement_allowed` | `False` |
| `profitability_claim` | `False` |
| `promotion_freeze` | `True` |

---

## 8. Forbidden Phrase Scan

- Patterns checked: 15
- Violations: []
- Scan result: PASS ✅

---

## 9. P78 Recommendation

- **Trigger condition**: Tier B n >= 200 in 2026 accumulation (expected 2026-09)
- **Expected phase**: P78
- **Content**: Full Tier B (abs_sp_fip_delta 0.25–0.50) sample expansion analysis. Compare Tier B vs Tier C finalists on 2026 live data.
- **Market-edge note**: Market-edge (CLV/EV) analysis remains DEFERRED in P80 until odds API key acquired.

---

## 10. Final Classification

```
P77_SHADOW_TRACKER_CONTRACT_READY
```

---

## CTO Agent 10-Line Summary

1. P77 contract formalizes 2026 prediction-only shadow tracking for both Tier C finalists from P76.
2. P76 dual-finalist decision verified: HOME_PLUS_AWAY_125 (0.5543) vs HOME_PLUS_AWAY_100 (0.5540), delta=0.0003 < 0.02.
3. Row schema (28 fields) defined; 8 governance booleans frozen (paper_only=true, production_ready=false, etc.).
4. Rule computation is deterministic: predicted_side = sign(sp_fip_delta), home threshold=0.50, away thresholds=1.00/1.25.
5. Semantic validation PASSED: computed counts match P75B (HOME_ONLY=268, AWAY_100=373, AWAY_125=316) on 2025 data.
6. Monthly metrics (n, hit_rate, AUC, Brier, ECE, home/away split, rolling 100) defined for each rule-month; no odds metrics.
7. Re-evaluation triggers: n≥50, n≥100, n≥200, end-of-season; downgrade on rolling-100 < 0.55 or 2 consecutive monthly < 0.50.
8. Tier B (abs_delta 0.25–0.50) tracked separately; P78 fires when Tier B n≥200 (~2026-09).
9. Market-edge lane (CLV/EV/Kelly) blocked; Tier A watchlist (abs_delta≥1.50) tracked without operationalization.
10. live_api_calls=0, forbidden scan PASS — contract ready for 2026 shadow accumulation.

---

*P77 contract: paper_only=true | diagnostic_only=true | production_ready=false*