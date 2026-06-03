# P85 — Prediction Convention Invariant Gate

**Date**: 2026-05-27  
**Classification**: `P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY`  
**Phase**: diagnostic-only, paper-only  

## Summary

This gate verifies the semantic correctness of the prediction convention
established in P84G and validated in P84H. It guards against silent side
inversion or label fossilization in future regression baselines.

## Convention Under Guard

| Rule | Definition |
|------|------------|
| `sp_fip_delta` | `home_sp_fip - away_sp_fip` |
| FIP semantics | lower is better |
| delta > 0 | home pitcher worse → `predicted_side = 'away'` |
| delta < 0 | away pitcher worse → `predicted_side = 'home'` |
| delta == 0 | tie → `model_probability` threshold decides |
| `model_probability` | P(home wins), NOT P(predicted side wins) |
| `actual_winner` | derived from `result_home_score` vs `result_away_score` |
| `is_correct` | `predicted_side == actual_winner` |

## Step Results

### ✅ Artifact Existence + Predecessor Classification Lock
**Status**: `PASSED`  

### ✅ FIP Positive Delta → Away
**Status**: `PASSED`  
Rows with delta > 0: 396 | Violations: 0  

### ✅ FIP Negative Delta → Home
**Status**: `PASSED`  
Rows with delta < 0: 412 | Violations: 0  

### ✅ Zero-Delta Policy Documentation
**Status**: `PASSED`  
Zero-delta rows in dataset: 0 | Min abs delta: 0.0077  
Policy: No zero-delta rows in current dataset (min abs delta = 0.0077). Policy documented for future gate enforcement.  

### ✅ model_probability Semantic Check
**Status**: `PASSED`  
Mean model_probability: 0.503383 | Below 0.5: 396 | Violations: 0  

### ✅ actual_winner Score Derivation
**Status**: `PASSED`  
Outcome rows: 808 | Violations: 0  

### ✅ is_correct Label Consistency
**Status**: `PASSED`  
n_correct: 460 | hit_rate: 0.569307 | Violations: 0  

### ✅ AUC / hit_rate Semantic Guard
**Status**: `PASSED`  
hit_rate: 0.569307 | AUC: 0.594315  
Matches P84H: hit_rate=True auc=True  
Platt/isotonic refit: **FORBIDDEN_BY_GOVERNANCE**  

### ✅ Governance Flags Scan
**Status**: `PASSED`  
Total row-level violations: 0  
Counts: {'paper_only_false': 0, 'diagnostic_only_false': 0, 'production_ready_true': 0, 'odds_used_true': 0, 'market_edge_true': 0}  

## P85 Governance Invariants

| Flag | Value |
|------|-------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `production_ready` | `False` |
| `odds_used` | `False` |
| `ev_computed` | `False` |
| `clv_computed` | `False` |
| `kelly_computed` | `False` |
| `live_api_calls` | `0` |
| `paid_api_called` | `False` |
| `canonical_rows_modified` | `False` |
| `outcome_rows_modified` | `False` |
| `p83e_mapping_modified` | `False` |
| `champion_replaced` | `False` |

## Final Classification

**`P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY`**

Rationale: All 9 invariant checks passed. FIP convention correct, probability semantics correct, label consistency verified, AUC/hit_rate semantically consistent. P84G fix confirmed not regressed.

## Scope Constraints

- No model retraining
- No Platt scaling / isotonic refit
- No odds / EV / CLV / Kelly computation
- No production betting recommendation
- No live API calls
- Coverage-limited signal (34.07%) NOT packaged as full-season claim
- hit_rate 56.9% / primary_125 60.3% NOT claimed as betting edge