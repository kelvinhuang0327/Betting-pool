# WBC Prediction Strategy Research Board Report

## 1. Executive Summary
This report reflects the latest **full 40-game replay registry** gate validation (no simulated probabilities).

### Key Findings [DATA]
- Evaluable sample: **40 pregame snapshots**.
- Ensemble Brier: **0.141523** (threshold 0.22 -> pass).
- Bayesian Brier: **0.141632** (ensemble slightly better, but not significant).
- Permutation p-value (ensemble vs bayesian): **0.988551** (no significant advantage).
- Final governance decision: **HOLDOUT_REQUIRED**.

---

## 2. Real Data Gate Evidence [DATA]

| Metric | Value |
| :--- | :--- |
| `n_registry_rows` | 66 |
| `n_latest_unique_games` | 40 |
| `n_pregame_snapshots` | 40 |
| `n_evaluable_games` | 40 |
| `n_pair_fallback_matches` | 29 |
| `ensemble_brier` | 0.141523 |
| `bayesian_brier` | 0.141632 |
| `nn_brier` | 0.153735 |
| `ensemble_accuracy` | 0.800000 |
| `bayesian_accuracy` | 0.800000 |
| `permutation_p_ens_vs_bayes` | 0.988551 |
| `mcnemar_p_ens_vs_bayes` | 1.000000 |
| `cap_check.max_prob` | 0.850000 |
| `cap_check.violations` | 0 |

Evidence source:
- `data/wbc_backend/reports/gate_validation_evidence.json`
- `scripts/verify_gating_stats.py`
- `scripts/diagnose_gate_coverage.py`

---

## 3. Stage Decision

| Stage | Status | Reason |
| :--- | :--- | :--- |
| Stage1 Integrity | PASS | 40 valid pregame snapshots with deterministic replay path. |
| Stage2 Validation | PASS | Ensemble Brier 0.141523 < threshold 0.22. |
| Stage3 Risk | PASS | Hard cap check passed (`min=0.15`, `max=0.85`, no violations). |
| Stage4 Deployment | FAIL | No significant edge over Bayesian (`p=0.988551`). |
| Stage5 Stability | FAIL | Rolling-10 Brier stability std = 0.063873 (above bound 0.03). |

Final decision: **HOLDOUT_REQUIRED**

---

## 4. Action Plan (Revised)

1. Keep hard cap at serving boundary (0.15~0.85) and re-validate weekly.
2. Run holdout A/B for Stage4 significance against Bayesian baseline.
3. Add stability regularization to reduce rolling-10 Brier volatility before guarded deploy.

## 5. Blend Search Evidence

- Exhaustive blend scan (`lambda` from 0.00 to 1.00, step 0.025) completed on 40 replay samples.
- Best Brier found at `lambda=0.525`: **0.140803** vs bayesian **0.141632**.
- Stage4 remains FAIL: permutation `p=0.818436` (no significant edge).
- Stage5 remains FAIL: rolling stability std `0.062011` (> 0.03 policy bound).
- Evidence file: `data/wbc_backend/reports/gate_blend_search.json`.
