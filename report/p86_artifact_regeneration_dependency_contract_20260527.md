# P86 — Artifact Regeneration / Dependency Contract

**Date**: 2026-05-27  
**Classification**: `P86_ARTIFACT_CONTRACT_FAILED_STALE_DOWNSTREAM_RISK`  
**Phase**: diagnostic-only

## Purpose

Verifies that the P83E → P84E → P84F/G/H/P85 dependency chain is internally
consistent and that no stale downstream risk exists. Read-only — does NOT
re-run any upstream phase or modify any artifact.

## Dependency Graph

| Phase | Depends On | Required By |
|-------|-----------|-------------|
| p83e_canonical_rows | — | p84e_outcome_attachment, p84f_calibration_diagnostic, p84g_mapping_fix |
| p84e_outcome_attachment | p83e_canonical_rows | p84f_calibration_diagnostic, p84g_mapping_fix, p84h_corrected_validation, p85_invariant_gate |
| p84f_calibration_diag | p83e_canonical_rows, p84e_outcome_attachment | p84g_mapping_fix |
| p84g_mapping_fix | p83e_canonical_rows, p84e_outcome_attachment, p84f_calibration_diag | p84h_corrected_validation, p85_invariant_gate |
| p84h_corrected_validation | p84g_mapping_fix, p84e_outcome_attachment | p85_invariant_gate |
| p85_invariant_gate | p84g_mapping_fix, p84h_corrected_validation | — |

## Step 1 — Artifact Existence

**Status**: PASSED
Missing: none

## Step 3 — Classification Lock

| Phase | Expected | Actual | Locked |
|-------|----------|--------|--------|
| p83e | `P83E_CANONICAL_ROWS_READY` | `P83E_CANONICAL_ROWS_READY` | True |
| p84e | `P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS` | `P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS` | True |
| p84f | `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK` | `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK` | True |
| p84g | `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED` | `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED` | True |
| p84h | `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED` | `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED` | True |
| p85 | `P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY` | `P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY` | True |

## Step 4 — Row Count Check

| Check | Expected | Actual | OK |
|-------|----------|--------|----|
| p83e_row_count | 828 | 828 | True |
| p84e_outcome_available | 808 | 808 | True |
| p84e_total_canonical_rows | 828 | 828 | True |
| p84e_jsonl_total | 828 | 828 | True |
| p84e_jsonl_outcome_avail | 808 | 808 | True |

## Step 5 — Metric Consistency

P84H metrics must match P84E reference within tolerance=0.0001

| Metric | Expected | Actual | Delta | OK |
|--------|----------|--------|-------|----|
| hit_rate | 0.569307 | 0.569307 | 0.0 | True |
| auc | 0.594315 | 0.594315 | 0.0 | True |
| brier | 0.249408 | 0.249408 | 0.0 | True |
| ece | 0.069682 | 0.069682 | 0.0 | True |
| p84h_vs_p84e_ref_hit_rate | None | None | 0.0 | True |
| p84h_vs_p84e_ref_auc | None | None | 0.0 | True |
| p84h_vs_p84e_ref_brier | None | None | 0.0 | True |
| p84h_vs_p84e_ref_ece | None | None | 0.0 | True |
| p85_positive_violations | 0 | 0 | None | True |
| p85_negative_violations | 0 | 0 | None | True |

## Step 6 — Report-vs-JSON Classification Consistency

| Phase | JSON Classification | Report Contains | Consistent |
|-------|-------------------|----------------|------------|
| p83e_summary | `P83E_CANONICAL_ROWS_READY` | True | True |
| p84e_summary | `P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS` | True | True |
| p84f_summary | `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK` | True | True |
| p84g_summary | `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED` | True | True |
| p84h_summary | `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED` | True | True |
| p85_summary | `P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY` | True | True |

## Step 7 — Mtime Ordering

**Status**: FAILED  
Stale risks: 1

| Upstream | Downstream | Delta (s) |
|----------|-----------|-----------|
| canonical_rows | p84e_rows | 6134 |

## Governance

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
| `p83e_through_p85_artifacts_modified` | `False` |
| `calibration_refit` | `False` |
| `no_champion_replacement` | `True` |
| `no_runtime_recommendation_mutation` | `True` |
| `no_production_betting_recommendation` | `True` |

## Scope Constraints

- No model refit, no calibration, no Platt/isotonic
- No EV / CLV / Kelly / stake sizing
- No live API calls, no paid odds
- No champion replacement, no runtime mutation
- No production betting recommendation
- No Taiwan lottery betting recommendation
- P84H signal 56.9% hit_rate is COVERAGE_LIMITED, not packaged as betting edge
- Primary-125 60.3% hit_rate is diagnostic signal only

## Final Classification

`P86_ARTIFACT_CONTRACT_FAILED_STALE_DOWNSTREAM_RISK`

Contract failed: ['step7']