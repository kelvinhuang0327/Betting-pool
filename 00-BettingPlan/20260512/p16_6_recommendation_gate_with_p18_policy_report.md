# P16.6 Recommendation Gate Re-run with P18 Risk-Repaired Policy

**Status**: `P16_6_RECOMMENDATION_GATE_WITH_P18_POLICY_READY`  
**Date**: 2026-05-12  
**Repo**: `Betting-pool-p13`, branch `p13-clean`  
**HEAD at run**: `fc94e3d`  
**Script**: `scripts/run_p16_6_recommendation_gate_with_p18_policy.py`

---

## 1. Objective

Re-issue recommendation rows using the P18 risk-repaired strategy policy
(`e0p0500_s0p0025_k0p10_o2p50`). The original P16 gate was blocked due to
excessive drawdown under the sweep-derived parameters. P18 found a valid policy
that reduces max drawdown from 44.80% to 1.85%, enabling the gate to pass.

---

## 2. P16 Original Gate Status (Blocked)

| Field | Value |
|---|---|
| Gate decision | `P16_BLOCKED_RISK_PROFILE_VIOLATION` |
| Max drawdown (original) | 44.80% |
| Drawdown limit | 25.00% |
| Root cause | Kelly fraction too high (1.0), stake cap too high (5%) |

---

## 3. P18 Risk Repair — Selected Policy

Policy file: `outputs/predictions/PAPER/2026-05-12/p18_strategy_policy_risk_repair/selected_strategy_policy.json`

| Parameter | Value |
|---|---|
| `selected_policy_id` | `e0p0500_s0p0025_k0p10_o2p50` |
| `edge_threshold` | 0.0500 (5.0%) |
| `max_stake_cap` | 0.0025 (0.25% of bankroll) |
| `kelly_fraction` | 0.10 (10% fractional Kelly) |
| `odds_decimal_max` | 2.50 |
| `n_bets` | 324 |
| `roi_mean` | +10.78% |
| `roi_ci_low_95` | -0.99% |
| `roi_ci_high_95` | +20.78% |
| `max_drawdown_pct` | 1.847% |
| `sharpe_ratio` | 0.1016 |
| `hit_rate` | 52.78% |
| `gate_decision` | `P18_STRATEGY_POLICY_RISK_REPAIRED` |
| `paper_only` | `true` |
| `production_ready` | `false` |

---

## 4. P16.6 Gate Flow

The gate applies per-row checks in this order using the P18 policy parameters:

1. `production_ready` must be `False` → `P16_6_BLOCKED_PRODUCTION`
2. `paper_only` must be `True` → `P16_6_BLOCKED_NOT_PAPER_ONLY`
3. `odds_join_status == JOINED` → `P16_6_BLOCKED_UNKNOWN`
4. Valid probabilities (0 < p_model < 1, p_market > 0) → `P16_6_BLOCKED_UNKNOWN`
5. Valid odds (odds_decimal > 1.0) → `P16_6_BLOCKED_UNKNOWN`
6. `odds_decimal <= odds_decimal_max` (2.50) → `P16_6_BLOCKED_ODDS_ABOVE_POLICY_MAX`
7. `edge >= edge_threshold` (0.05) → `P16_6_BLOCKED_EDGE_BELOW_P18_THRESHOLD`
8. `max_drawdown_pct <= 25.0%` (policy-level check) → `P16_6_BLOCKED_POLICY_RISK_INVALID`
9. `sharpe_ratio >= 0.0` (policy-level check) → `P16_6_BLOCKED_POLICY_RISK_INVALID`
10. All checks pass → `P16_6_ELIGIBLE_PAPER_RECOMMENDATION`

Stake computation: `stake = min(full_kelly * kelly_fraction, max_stake_cap)`  
where `full_kelly = (edge) / (odds_decimal - 1)`, capped at 0.0025.

---

## 5. Input Data

| Source | Path |
|---|---|
| P15 joined OOF | `outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/joined_oof_with_odds.csv` |
| P18 selected policy | `outputs/predictions/PAPER/2026-05-12/p18_strategy_policy_risk_repair/selected_strategy_policy.json` |

| Metric | Count |
|---|---|
| Total input rows | 1577 |
| Rows with JOINED odds | 1575 |
| Rows with non-JOINED odds | 2 |

---

## 6. Gate Decision Results

**Overall gate decision**: `P16_6_PAPER_RECOMMENDATION_GATE_READY`

| Reason code | Count | % of total |
|---|---|---|
| `P16_6_ELIGIBLE_PAPER_RECOMMENDATION` | 324 | 20.5% |
| `P16_6_BLOCKED_EDGE_BELOW_P18_THRESHOLD` | 907 | 57.5% |
| `P16_6_BLOCKED_ODDS_ABOVE_POLICY_MAX` | 344 | 21.8% |
| `P16_6_BLOCKED_UNKNOWN` | 2 | 0.1% |
| **Total** | **1577** | **100%** |

Primary block reasons:
- **907 rows blocked** because model edge < 5% (P18 edge threshold)
- **344 rows blocked** because decimal odds > 2.50 (P18 odds cap — avoids heavy favourites)
- **2 rows blocked** as UNKNOWN (non-JOINED odds — no market data available)

---

## 7. Eligible Recommendation Rows

324 rows passed all gate checks.

| Metric | Value |
|---|---|
| Count | 324 |
| Paper stake fraction (all) | 0.0025 (stake cap binding) |
| Edge range | 0.0500 to 0.2489 |
| Odds (decimal) range | 1.5882 to 2.5000 |
| `paper_only` | `True` (all rows) |
| `production_ready` | `False` (all rows) |
| `strategy_policy` | `capped_kelly_p18` |
| `created_from` | `P16_6_RECOMMENDATION_GATE_RERUN_WITH_P18_POLICY` |

Sample eligible rows:

| game_id | date | side | edge | odds_decimal | paper_stake |
|---|---|---|---|---|---|
| `2025-05-08_MIN_BAL` | 2025-05-08 | HOME | 0.0535 | 1.5882 | 0.0025 |
| `2025-05-09_MIN_SF` | 2025-05-09 | HOME | 0.0744 | 2.0000 | 0.0025 |
| `2025-05-09_SEA_TOR` | 2025-05-09 | HOME | 0.0770 | 1.6667 | 0.0025 |
| `2025-05-09_ATH_NYY` | 2025-05-09 | HOME | 0.1949 | 2.3500 | 0.0025 |
| `2025-05-09_LAA_BAL` | 2025-05-09 | HOME | 0.0735 | 2.2000 | 0.0025 |

---

## 8. Risk Profile (from P18 Policy)

Source file: `p16_6_policy_risk_profile.json`

| Metric | Value |
|---|---|
| `roi_mean` | +10.78% |
| `roi_ci_low_95` | -0.99% |
| `roi_ci_high_95` | +20.78% |
| `max_drawdown_pct` | **1.847%** (well under 25% limit) |
| `sharpe_ratio` | 0.1016 (positive) |
| `n_bets` | 324 |
| `hit_rate` | 52.78% |
| `edge_threshold` | 0.05 |
| `max_stake_cap` | 0.0025 |
| `kelly_fraction` | 0.10 |
| `odds_decimal_max` | 2.50 |

---

## 9. Output Files (6 total)

All written to: `outputs/predictions/PAPER/2026-05-12/p16_6_recommendation_gate_p18_policy/`

| File | Description |
|---|---|
| `recommendation_rows.csv` | All 1577 rows with gate decisions (29 columns) |
| `recommendation_summary.json` | Aggregate summary (19 keys) |
| `recommendation_summary.md` | Human-readable markdown summary |
| `gate_reason_counts.json` | Per-reason code counts (sorted keys) |
| `p18_policy_applied.json` | Copy of P18 policy used for this run |
| `p16_6_policy_risk_profile.json` | Risk profile derived from P18 policy |

---

## 10. Safety Invariants Verified

| Invariant | Status |
|---|---|
| `paper_only = True` for all 1577 rows | ✅ VERIFIED |
| `production_ready = False` for all 1577 rows | ✅ VERIFIED |
| `PAPER_ONLY=true` flag required at CLI level | ✅ ENFORCED |
| No live TSL calls | ✅ CONFIRMED |
| No real bets | ✅ CONFIRMED |
| Output directory is untracked (not committed) | ✅ CONFIRMED |

---

## 11. Determinism Evidence

Two independent runs were executed:
- Run 1: `outputs/.../p16_6_recommendation_gate_p18_policy/`
- Run 2: `outputs/.../p16_6_recommendation_gate_p18_policy_run2/`

Both runs produced identical results:
- 1577 total rows
- 324 eligible
- 907 blocked (edge below threshold)
- 344 blocked (odds above max)
- 2 blocked (UNKNOWN)

The `test_determinism_two_runs` integration test also confirms this formally.

---

## 12. Test Suite Results

Full P14–P18 + P16.6 test suite:

```
239 passed in 40.63s
```

Breakdown:
- `test_p14_strategy_policies.py` — P14 strategy policies
- `test_p14_strategy_simulator.py` — P14 simulator
- `test_p15_market_odds_adapter.py` — P15 adapter
- `test_p16_recommendation_gate.py` — P16 gate (original, unmodified)
- `test_p16_recommendation_input_adapter.py` — P16 input adapter
- `test_p18_drawdown_diagnostics.py` — P18 drawdown
- `test_p18_strategy_policy_grid.py` — P18 grid
- `test_p18_strategy_policy_contract.py` — P18 contracts
- `test_run_p14_strategy_simulation_spine.py` — P14 CLI
- `test_run_p15_market_odds_join_simulation.py` — P15 CLI
- `test_run_p16_recommendation_gate_reevaluation.py` — P16 CLI (original)
- `test_run_p18_strategy_policy_risk_repair.py` — P18 CLI
- `test_p16_p18_policy_loader.py` — **NEW: 18 tests** (P18 policy loader)
- `test_run_p16_6_recommendation_gate_with_p18_policy.py` — **NEW: 17 tests** (P16.6 CLI)

---

## 13. New Code Created / Modified

| File | Type | Purpose |
|---|---|---|
| `wbc_backend/recommendation/p16_p18_policy_loader.py` | NEW | Load + validate P18 selected policy JSON |
| `wbc_backend/recommendation/p16_recommendation_gate.py` | EXTENDED | P16.6 gate functions using P18 policy |
| `wbc_backend/recommendation/p16_recommendation_row_builder.py` | EXTENDED | P16.6 row type with P18 policy fields |
| `scripts/run_p16_6_recommendation_gate_with_p18_policy.py` | NEW | CLI for P16.6 gate re-run |
| `tests/test_p16_p18_policy_loader.py` | NEW | 18 unit tests for policy loader |
| `tests/test_run_p16_6_recommendation_gate_with_p18_policy.py` | NEW | 17 integration tests for P16.6 CLI |

---

## 14. Recommendation Summary (from JSON)

```json
{
  "p16_6_gate": "P16_6_PAPER_RECOMMENDATION_GATE_READY",
  "p18_source_gate": "P18_STRATEGY_POLICY_RISK_REPAIRED",
  "p18_policy_id": "e0p0500_s0p0025_k0p10_o2p50",
  "p18_edge_threshold": 0.05,
  "p18_max_stake_cap": 0.0025,
  "p18_kelly_fraction": 0.1,
  "p18_odds_decimal_max": 2.5,
  "n_input_rows": 1577,
  "n_joined_rows": 1575,
  "n_policy_eligible_rows": 1575,
  "n_recommended_rows": 324,
  "n_blocked_rows": 1253,
  "selected_policy_max_drawdown_pct": 1.84685812906932,
  "selected_policy_sharpe_ratio": 0.10156971381097146,
  "selected_policy_n_bets": 324,
  "paper_only": true,
  "production_ready": false
}
```

---

## 15. Next Steps

| Step | Description | Status |
|---|---|---|
| P17 | Paper execution simulation (track hypothetical P&L against live odds) | NOT STARTED |
| P19 | Walk-forward re-calibration with P18 policy constraints locked in | NOT STARTED |
| Monitoring | Track paper recommendation outcomes vs actual game results | NOT STARTED |
| Live gating | DO NOT promote to production until P17 + additional validation complete | ENFORCED |

---

## Appendix A: Gate Reason Code Definitions

| Code | Meaning |
|---|---|
| `P16_6_ELIGIBLE_PAPER_RECOMMENDATION` | Row passed all P16.6 gate checks |
| `P16_6_BLOCKED_EDGE_BELOW_P18_THRESHOLD` | Model edge < 5% (P18 edge threshold) |
| `P16_6_BLOCKED_ODDS_ABOVE_POLICY_MAX` | Decimal odds > 2.50 (P18 odds cap) |
| `P16_6_BLOCKED_ODDS_ABOVE_POLICY_MAX` | No market odds data (non-JOINED) or invalid data |
| `P16_6_BLOCKED_PRODUCTION` | production_ready = True (safety block) |
| `P16_6_BLOCKED_NOT_PAPER_ONLY` | paper_only = False (safety block) |
| `P16_6_BLOCKED_POLICY_RISK_INVALID` | P18 policy failed drawdown or sharpe check |
| `P16_6_BLOCKED_INVALID_STAKE` | Stake computation produced invalid result |
| `P16_6_BLOCKED_UNKNOWN` | Non-JOINED status or invalid probability/odds data |

---

## Appendix B: CLI Invocation

```bash
cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13

.venv/bin/python scripts/run_p16_6_recommendation_gate_with_p18_policy.py \
  --joined-oof outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/joined_oof_with_odds.csv \
  --p15-ledger outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/simulation_ledger.csv \
  --p18-policy outputs/predictions/PAPER/2026-05-12/p18_strategy_policy_risk_repair/selected_strategy_policy.json \
  --output-dir outputs/predictions/PAPER/2026-05-12/p16_6_recommendation_gate_p18_policy \
  --paper-only true
```

Exit code: `0`  
Overall gate: `P16_6_PAPER_RECOMMENDATION_GATE_READY`

---

**Terminal marker**: `P16_6_RECOMMENDATION_GATE_WITH_P18_POLICY_READY`
