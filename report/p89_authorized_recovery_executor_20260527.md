# P89 Authorized Recovery Executor — 2026-05-27

## Classification
`P89_RECOVERY_COMPLETE_CONTRACT_RESTORED`

## Authorization
- Status: **GRANTED** — phrase verified
- Phrase received: `YES regenerate stale downstream artifacts for P87 recovery`
- Phrase ok: `True`

## Pre-Recovery State
- P86 pre: `P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY`
- Canonical rows mtime: `2026-05-27T08:10:02.982283+00:00`
- P84E rows mtime pre: `2026-05-27T08:25:17.495891+00:00`
- Delta (canonical − p84e): `-914.5s`

## Recovery Sequence Execution

| Phase | Script | Exit | Classification | Status |
|-------|--------|------|---------------|--------|
| P84E | `scripts/_p84e_2026_outcome_attachment_pipeline.py` | 0 | `P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS` | ✅ PASS |
| P84F | `scripts/_p84f_predicted_side_calibration_diagnostic.py` | 0 | `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK` | ✅ PASS |
| P84G | `scripts/_p84g_predicted_side_mapping_fix.py` | 0 | `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED` | ✅ PASS |
| P84H | `scripts/_p84h_corrected_signal_validation_coverage_guard.py` | 0 | `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED` | ✅ PASS |
| P85 | `scripts/_p85_prediction_convention_invariant_gate.py` | 0 | `P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY` | ✅ PASS |
| P86 | `scripts/_p86_artifact_regeneration_dependency_contract.py` | 0 | `P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY` | ✅ PASS |

## Post-Recovery State
- P84E rows mtime post: `2026-05-27T08:28:18.528204+00:00`
- P84E newer than canonical: `True`
- Stale resolved: `True`

## Metrics Validation (n=808, tolerance=1e-4)

| Metric | Baseline | Post-Recovery | Delta | Within Tolerance |
|--------|----------|--------------|-------|-----------------|
| hit_rate | 0.569307 | 0.569307 | 0.00e+00 | ✅ |
| auc | 0.594315 | 0.594315 | 0.00e+00 | ✅ |
| brier | 0.249408 | 0.249408 | 0.00e+00 | ✅ |
| ece | 0.069682 | 0.069682 | 0.00e+00 | ✅ |

## P86 Contract Restored
- Post P86 classification: `P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY`
- Expected: `P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY`
- Contract restored: `True`

## Governance (20 flags)

| Flag | Value |
|------|-------|
| `paper_only` | ✅ `True` |
| `diagnostic_only` | ✅ `True` |
| `production_ready` | ⚠️ `False` |
| `no_real_bet` | ✅ `True` |
| `odds_used` | ⚠️ `False` |
| `ev_computed` | ⚠️ `False` |
| `clv_computed` | ⚠️ `False` |
| `kelly_computed` | ⚠️ `False` |
| `paid_api_called` | ⚠️ `False` |
| `no_frozen_artifact_modification` | ✅ `True` |
| `no_fabricated_outcomes` | ✅ `True` |
| `no_model_refit` | ✅ `True` |
| `explicit_yes_phrase_verified` | ✅ `True` |
| `recovery_scope_minimal` | ✅ `True` |
| `metrics_tolerance_checked` | ✅ `True` |
| `no_taiwan_lottery_recommendation` | ✅ `True` |
| `no_betting_advice` | ✅ `True` |
| `no_stake_computation` | ✅ `True` |
| `no_historical_artifact_overwrite` | ✅ `True` |
| `authorization_phrase_immutable` | ✅ `True` |

---

**NO production betting. NO EV/CLV/Kelly. NO Taiwan lottery recommendation.**
**NO real bet. NO stake computation. Diagnostic only.**

Classification: `P89_RECOVERY_COMPLETE_CONTRACT_RESTORED`