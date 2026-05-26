# P79B — Tier B vs Tier C Comparison Harness Fixture Dry-Run

> **Classification**: `P79B_TIER_B_FIXTURE_RESEARCH_ONLY`
> **Schema Version**: `p79b-v1`
> **Generated**: 2026-05-26T17:12:31.576226
> **Mode**: `paper_only=True | diagnostic_only=True | production_ready=False`
> **Fixture Disclaimer**: 2025 data dry-run only. NOT a 2026 live performance claim.

---

## Source Artifacts Verified

- ✅ p79a_tier_b_trigger_readiness_contract_summary.json
- ✅ p79a_tier_b_trigger_readiness_contract_20260526.md
- ✅ _p79a_tier_b_trigger_readiness_contract.py
- ✅ p78_monthly_shadow_tracker_report_template_summary.json
- ✅ p77_prediction_only_shadow_tracker_contract_summary.json
- ✅ p76_corrected_tier_c_final_rule_selection_summary.json
- ✅ p75b_calibration_diagnostics_corrected_tier_c_summary.json
- ✅ p75a_tier_c_corrected_rule_validator_summary.json
- ✅ p74_tier_c_home_away_bias_correction_summary.json
- ✅ p73_tier_stability_and_sample_expansion_summary.json
- ✅ p72b_objective_metric_contract_summary.json
- ✅ p72a_odds_free_strategy_accuracy_backtest_summary.json
- ✅ mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl

## P79A Trigger Readiness Verification

- Classification: `P79A_TIER_B_TRIGGER_READINESS_CONTRACT_READY`
- Snapshot ID: `tier_b_snapshot_2025_202507`
- Trigger n: 219
- Trigger month: `2025-07`
- Market-edge lane: `blocked`
- **Verified**: True

## Fixture Snapshot Reconstruction

- Snapshot ID: `tier_b_snapshot_2025_202507`
- Cutoff month: `2025-07`
- Snapshot months: 2025-04, 2025-05, 2025-06, 2025-07
- Total snapshot rows: 1230

| Candidate | n |
|-----------|---|
| `tier_b` | 219 |
| `primary_125` | 247 |
| `shadow_100` | 269 |
| `baseline_50` | 329 |

## Candidate Metrics Table

| Candidate | n | Hit Rate | CI Lower | CI Upper | AUC | Brier | ECE | Stability | Concentration |
|-----------|---|----------|----------|----------|-----|-------|-----|-----------|---------------|
| `tier_b` | 219 | 0.534 | 0.468 | 0.599 | 0.552 | 0.247 | 0.043 | MODERATE | LOW |
| `primary_125` | 247 | 0.583 | 0.521 | 0.643 | 0.570 | 0.239 | 0.016 | MODERATE | SEVERE |
| `shadow_100` | 269 | 0.569 | 0.509 | 0.627 | 0.579 | 0.240 | 0.020 | MODERATE | MODERATE |
| `baseline_50` | 329 | 0.565 | 0.511 | 0.618 | 0.596 | 0.239 | 0.033 | MODERATE | LOW |

### Home/Away Split

| Candidate | n_home | home_hit_rate | n_away | away_hit_rate | Rolling 100 |
|-----------|--------|---------------|--------|---------------|-------------|
| `tier_b` | 141 | 0.532 | 78 | 0.538 | 0.540 |
| `primary_125` | 226 | 0.597 | 21 | 0.429 | 0.600 |
| `shadow_100` | 226 | 0.597 | 43 | 0.419 | 0.620 |
| `baseline_50` | 226 | 0.597 | 103 | 0.495 | 0.590 |

## Head-to-Head Comparison

| vs | hit_rate_delta | auc_delta | brier_delta | ece_delta |
|----|---------------|-----------|-------------|-----------|
| `vs_primary_125` | -0.0488 | -0.0180 | 0.0082 | 0.0271 |
| `vs_shadow_100` | -0.0346 | -0.0270 | 0.0070 | 0.0232 |
| `vs_baseline_50` | -0.0311 | -0.0443 | 0.0082 | 0.0101 |

## Operational Research Gate

- ✅ `n_gte_200`: True
- ❌ `performance_ok`: False
- ✅ `stability_ok`: True
- ✅ `ece_ok`: True
- ✅ `concentration_ok`: True
- ✅ `prediction_only`: True

**Gate passes**: False
**Fail reasons**: ['performance_ok']

## Fixture Dry-Run Decision

**Classification**: `TIER_B_RESEARCH_ONLY_FIXTURE`

> Gate fails on: ['performance_ok']. Enough conditions pass for research-only status.

**⚠️ Disclaimer**: This classification is based on 2025 fixture data only. It does NOT constitute a 2026 live performance claim. Champion strategy unchanged. No bets recommended.

## Monthly Stability Diagnostics

### tier_b

| Month | n | hit_rate | ci_lower | ci_upper |
|-------|---|----------|----------|----------|
| 2025-04 | 9 | 0.556 | 0.267 | 0.811 |
| 2025-05 | 76 | 0.566 | 0.454 | 0.671 |
| 2025-06 | 69 | 0.493 | 0.378 | 0.608 |
| 2025-07 | 65 | 0.538 | 0.418 | 0.654 |

### primary_125

| Month | n | hit_rate | ci_lower | ci_upper |
|-------|---|----------|----------|----------|
| 2025-04 | 14 | 0.500 | 0.268 | 0.732 |
| 2025-05 | 100 | 0.590 | 0.492 | 0.681 |
| 2025-06 | 61 | 0.574 | 0.449 | 0.690 |
| 2025-07 | 72 | 0.597 | 0.482 | 0.703 |

### shadow_100

| Month | n | hit_rate | ci_lower | ci_upper |
|-------|---|----------|----------|----------|
| 2025-04 | 15 | 0.533 | 0.301 | 0.752 |
| 2025-05 | 107 | 0.570 | 0.475 | 0.660 |
| 2025-06 | 70 | 0.543 | 0.427 | 0.654 |
| 2025-07 | 77 | 0.597 | 0.486 | 0.700 |

### baseline_50

| Month | n | hit_rate | ci_lower | ci_upper |
|-------|---|----------|----------|----------|
| 2025-04 | 16 | 0.562 | 0.332 | 0.769 |
| 2025-05 | 120 | 0.567 | 0.477 | 0.652 |
| 2025-06 | 101 | 0.535 | 0.438 | 0.629 |
| 2025-07 | 92 | 0.598 | 0.496 | 0.692 |


## Future P79 Execution Prompt

```
[P79 — Tier B Sample Expansion Analysis vs Tier C Finalists on 2026 Live Data]
================================================================================

TRIGGER CONDITION: Tier B cumulative n >= 200 in 2026 live accumulation

REQUIRED SNAPSHOT PACKAGE:
  - snapshot_id: tier_b_snapshot_2026_<YYYYMM>       ← set at trigger month
  - trigger_date: <YYYY-MM>                           ← first month n >= 200
  - season: 2026
  - data_cutoff: <YYYY-MM-DD>                        ← last game date in trigger month
  - tier_b_n: <int>                                   ← cumulative Tier B count
  - tier_b_months_covered: list[str]
  - governance_snapshot: all 9 flags from P79A schema

REQUIRED SOURCE FILES:
  - data/mlb_2025/derived/p79a_tier_b_trigger_readiness_contract_summary.json
  - data/mlb_2025/derived/p78_monthly_shadow_tracker_report_template_summary.json
  - data/mlb_2026/derived/mlb_2026_per_game_predictions_<version>.jsonl
  - scripts/_p79b_tier_b_vs_tier_c_comparison_harness.py  ← run on 2026 data

EXPECTED TRIGGER STATE: TIER_B_TRIGGER_FROZEN

COMPARISON HARNESS COMMAND:
  .venv/bin/python scripts/_p79b_tier_b_vs_tier_c_comparison_harness.py \
      --snapshot-id tier_b_snapshot_2026_<YYYYMM> \
      --predictions data/mlb_2026/derived/mlb_2026_per_game_predictions_<ver>.jsonl \
      --output-dir data/mlb_2026/derived/

OUTPUT LOCATIONS:
  - data/mlb_2026/derived/p79_tier_b_comparison_harness_summary.json
  - report/p79_tier_b_comparison_harness_<YYYYMMDD>.md

STOP CONDITIONS:
  - predictions JSONL not found or empty
  - trigger_n < 200
  - governance_snapshot.production_ready == True
  - governance_snapshot.ev_calculated == True
  - governance_snapshot.odds_used == True
  - governance_snapshot.live_api_calls > 0

GOVERNANCE INVARIANTS (must all hold):
  paper_only=True | diagnostic_only=True | production_ready=False
  ev_calculated=False | clv_calculated=False | kelly_calculated=False
  odds_used=False | market_edge_evaluated=False | live_api_calls=0

EXPECTED CLASSIFICATION LIST:
  - P79_TIER_B_FIXTURE_OUTPERFORMS_TIER_C
  - P79_TIER_B_FIXTURE_COMPETITIVE_WITH_TIER_C
  - P79_TIER_B_FIXTURE_RESEARCH_ONLY
  - P79_TIER_B_FIXTURE_UNDERPERFORMS_TIER_C
  - P79_TIER_B_FIXTURE_INCONCLUSIVE
  - P79_BLOCKED_BY_MISSING_SOURCE_ARTIFACT
  - P79_FAILED_VALIDATION

MARKET-EDGE: DEFERRED to P80 (pending odds API key)
PRODUCTION READINESS: NOT achievable in P79

2025 FIXTURE DRY-RUN REFERENCE:
  - P79B fixture classification: TIER_B_RESEARCH_ONLY_FIXTURE
  - 2025 Tier B fixture n at trigger: 219
  - Fixture snapshot: tier_b_snapshot_2025_202507
================================================================================
```

## Governance Invariants

| Flag | Value |
|------|-------|
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

## Forbidden Scan

- **Result**: ✅ PASS
- **Violations**: 0

---

*P79B — Fixture dry-run only. No live data fetched. No production modification.*