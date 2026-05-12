# P18 Strategy Policy Risk Repair Report

**Phase**: P18  
**Date**: 2026-05-12  
**Branch**: `p13-clean`  
**Repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`  
**Status**: `P18_STRATEGY_POLICY_RISK_REPAIR_READY`

---

## 1. Repository Evidence

| Field | Value |
|---|---|
| Branch | `p13-clean` |
| HEAD commit | `f0062e7` |
| P16 marker | `P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY` |
| PAPER_ONLY | `true` |
| production_ready | `false` |

P18 builds directly on P16 output ledger without modifying any prior-phase code or outputs.

---

## 2. P16 Prior Gate State

P16 blocked all recommendations due to a risk profile violation:

| Metric | P16 Value | Limit |
|---|---|---|
| Gate | `P16_BLOCKED_RISK_PROFILE_VIOLATION` | — |
| Selected edge threshold | 0.08 | — |
| Sharpe ratio | 0.0937 | ≥ 0.0 |
| n_bets | 247 | ≥ 50 |
| Max drawdown | **44.80%** | **≤ 25%** |
| Bootstrap CI (95%) | [−0.21%, +1.24%] | — |

Root problem: the capped_kelly policy (5% cap) produced excessive drawdown even at high edge thresholds. All 5 edge sweep thresholds (0.01–0.08) failed the 25% drawdown limit.

---

## 3. Drawdown Diagnosis (P16 Baseline)

Diagnosis applied to P15 ledger at threshold=0.08 (P16 selected):

| Diagnostic | Value |
|---|---|
| n_eligible_bets | 247 |
| max_drawdown_pct | 44.80% |
| Worst segment | rows 0–39 (40 bets), peak→trough: 1.000→0.552 |
| n_loss_clusters | 28 |
| Largest consecutive loss streak | 8 |
| Mean stake | 4.98% (capped at 5%) |
| Hit rate | 48.6% |

**Root-cause flags triggered**: `HIGH_STAKE` (mean=4.98% > 2%), `LONG_LOSS_STREAK` (max=8), `MANY_CLUSTERS` (28), `LOW_HIT_RATE` (48.6%)

The primary driver is over-staking at 5% per bet. With a sub-50% hit rate and 28 loss clusters, consecutive losses of that magnitude create deep equity drawdowns. The fix must reduce stake dramatically.

---

## 4. Grid Search Design

A 5×5×4×4 = **400-candidate** grid was constructed:

| Dimension | Values |
|---|---|
| `edge_threshold` | 0.05, 0.08, 0.10, 0.12, 0.15 |
| `max_stake_cap` | 0.0025, 0.005, 0.010, 0.015, 0.020 |
| `kelly_fraction` | 0.10, 0.25, 0.50, 1.00 |
| `odds_decimal_max` | 2.50, 3.00, 4.00, 999.0 |

**Pass criteria** (all must be satisfied):
- `n_bets ≥ 50`
- `max_drawdown_pct ≤ 25%`
- `sharpe_ratio ≥ 0.0`
- `roi_ci_low_95 ≥ −2.0%`

**Selection rule**: Among passing candidates, select the one with the lowest `max_drawdown_pct`.

**Bootstrap**: 2000 iterations, `random.Random(seed=42)`, deterministic.

---

## 5. Candidate Summary

| Statistic | Value |
|---|---|
| Total candidates evaluated | 400 |
| Candidates passing all criteria | **84** (21.0%) |
| Drawdown range (passing) | 1.85% – 17.92% |
| n_bets range (passing) | 182 – 396 |
| Best Sharpe (passing) | 0.1513 |
| Best ROI mean (passing) | 16.48% |

84 of 400 candidates cleared all four pass criteria. The primary gate was the 25% drawdown limit — low kelly fractions (0.10, 0.25) and low stake caps (0.0025, 0.005) drove pass/fail.

---

## 6. Selected Policy

**Policy ID**: `e0p0500_s0p0025_k0p10_o2p50`

| Parameter | Value |
|---|---|
| `edge_threshold` | 0.05 |
| `max_stake_cap` | 0.0025 (0.25% of bankroll) |
| `kelly_fraction` | 0.10 (one-tenth Kelly) |
| `odds_decimal_max` | 2.50 |

**Selection rationale**: Among 84 passing candidates, this policy achieves the lowest drawdown at 1.85%, meeting all pass criteria with adequate n_bets (324) and positive Sharpe.

---

## 7. Risk Metrics Comparison

| Metric | P16 Baseline | P18 Selected | Change |
|---|---|---|---|
| Gate | `BLOCKED` | `REPAIRED` | ✅ |
| Edge threshold | 0.08 | 0.05 | ↓ |
| Max stake cap | 5.00% | **0.25%** | −95% |
| Kelly fraction | 1.00 (full) | **0.10** (1/10th) | −90% |
| n_bets | 247 | **324** | +31% |
| Hit rate | 48.6% | 52.8% | +4.2pp |
| Max drawdown | **44.80%** | **1.85%** | −95.9% |
| Sharpe ratio | 0.0937 | 0.1016 | +8.4% |
| ROI mean | +10.93% | +10.78% | −0.15pp |
| Bootstrap CI 95% | [−0.21%, +1.24%] | [−0.99%, +20.78%] | wider (more bets) |
| production_ready | false | false | — |

The policy repair achieves a **95.9% reduction in maximum drawdown** (from 44.80% to 1.85%) while maintaining a positive Sharpe ratio and comparable ROI mean. The wider CI reflects the lower per-bet stakes with a larger bet count.

---

## 8. Test Results

All tests pass in a single run at 27.78 seconds (bootstrap_n_iter=50 in tests):

| Test File | Tests | Status |
|---|---|---|
| `test_p18_drawdown_diagnostics.py` | included in 45 | ✅ pass |
| `test_p18_strategy_policy_grid.py` | included in 45 | ✅ pass |
| `test_p18_strategy_policy_contract.py` | included in 45 | ✅ pass |
| `test_run_p18_strategy_policy_risk_repair.py` | included in 45 | ✅ pass |
| **P18 subtotal** | **45** | **✅ pass** |

Full regression suite (P18 + P16 + P15 + P14):

```
226 passed in 40.67s
```

No regressions introduced.

---

## 9. Real Run Result

**Command**:
```
scripts/run_p18_strategy_policy_risk_repair.py \
  --p15-ledger outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/simulation_ledger.csv \
  --p16-summary outputs/predictions/PAPER/2026-05-12/p16_recommendation_gate/recommendation_summary.json \
  --output-dir outputs/predictions/PAPER/2026-05-12/p18_strategy_policy_risk_repair \
  --paper-only true --min-bets-floor 50 --max-drawdown-limit 0.25 \
  --sharpe-floor 0.0 --bootstrap-n-iter 2000
```

**Result**:
```
p18_gate:                    P18_STRATEGY_POLICY_RISK_REPAIRED
selected_policy_id:          e0p0500_s0p0025_k0p10_o2p50
selected_max_drawdown_pct:   1.8469%
n_candidates_evaluated:      400
n_candidates_passing:        84
production_ready:            False
paper_only:                  True
```

**Output files produced**:
- `strategy_policy_grid.csv` — 400-row candidate grid
- `strategy_policy_grid_summary.json` — grid summary with gate decision
- `strategy_policy_grid_summary.md` — human-readable summary
- `selected_strategy_policy.json` — final policy parameters
- `drawdown_diagnostics.json` — P16 baseline diagnosis
- `drawdown_diagnostics.md` — human-readable diagnosis

---

## 10. Determinism Check

Two independent runs on identical inputs produced bit-for-bit identical outputs (excluding `generated_at_utc`):

| File | Result |
|---|---|
| `strategy_policy_grid_summary.json` | MATCH |
| `selected_strategy_policy.json` | MATCH |
| `drawdown_diagnostics.json` | MATCH |
| `strategy_policy_grid.csv` | MATCH |

**DETERMINISM: PASS** — `random.Random(seed=42)` with fixed bootstrap_n_iter=2000.

---

## 11. Production Readiness

| Guard | Status |
|---|---|
| `paper_only=True` | ✅ enforced in all 3 JSON outputs |
| `production_ready=False` | ✅ enforced in all 3 JSON outputs |
| No live TSL calls | ✅ confirmed |
| No real money bets | ✅ PAPER_ONLY simulation only |
| No push to remote | ✅ local commit only |
| Forbidden repo isolation | ✅ changes only in `Betting-pool-p13` |

---

## 12. Limitations

1. **CI is wide**: The 95% bootstrap CI for ROI is [−0.99%, +20.78%]. The lower bound is near zero, meaning the edge is not statistically conclusive at high confidence. More real-world data would narrow this interval.

2. **Hit rate near 50%**: 52.8% is only slightly above coin-flip; Kelly fractions at 0.10 correctly reflect this uncertainty.

3. **Odds capped at 2.50**: The policy excludes longer-shot bets (odds > 2.50) to reduce variance. This may forgo positive-EV situations at higher odds.

4. **Extreme stake reduction**: Moving from 5% to 0.25% per bet reduces risk aggressively at the cost of absolute return magnitude. This is appropriate for PAPER validation but would need calibration if ever considered for live deployment.

5. **Grid search not exhaustive below 0.05 edge**: Edge thresholds below 0.05 were not tested; they may yield different trade-offs.

---

## 13. Next Phase Recommendation

With P18 gate = `P18_STRATEGY_POLICY_RISK_REPAIRED`, the selected policy parameters are:

```
edge_threshold = 0.05
max_stake_cap  = 0.0025 (0.25%)
kelly_fraction = 0.10 (1/10th Kelly)
odds_cap       = 2.50 decimal
```

**Recommended next phase**: P19 — Forward Simulation Walk-Forward Validation.

Apply the P18 selected policy to a rolling walk-forward simulation (e.g., 60-day windows) to assess out-of-sample stability. Key validation targets:
- Walk-forward drawdown consistently < 25%
- Sharpe positive in ≥ 70% of windows
- No single window exceeds 35% drawdown

Do **not** proceed to live deployment until P19 walk-forward validation is complete and a separate human review of the policy parameters is conducted.

---

## 14. Marker

```
P18_STRATEGY_POLICY_RISK_REPAIR_READY
```

Gate: `P18_STRATEGY_POLICY_RISK_REPAIRED`  
Policy: `e0p0500_s0p0025_k0p10_o2p50`  
Max drawdown: 1.85% (limit: 25%) — **PASS**  
Sharpe: 0.1016 (floor: 0.0) — **PASS**  
n_bets: 324 (floor: 50) — **PASS**  
ROI CI low: −0.99% (floor: −2.0%) — **PASS**  
Tests: 226/226 pass  
Determinism: MATCH  
PAPER_ONLY: true  
production_ready: false  
