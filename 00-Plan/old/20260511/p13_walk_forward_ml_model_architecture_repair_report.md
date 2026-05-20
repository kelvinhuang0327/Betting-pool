# P13 Walk-Forward ML Model Architecture Repair Report

Marker: `P13_WALK_FORWARD_ML_MODEL_ARCHITECTURE_REPAIR_READY`

## 1. Repo + Branch + Env Evidence

- repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- branch: `main`
- branch state: `ahead 38, behind 1`
- python: `3.13.8`
- pytest: `9.0.3`
- sklearn: `1.8.0`
- note: dirty working tree preserved as requested; no cleanup performed.

## 2. P12 Baseline Summary

- P12 marker: `P12_FEATURE_FAMILY_ABLATION_CONTEXT_SAFETY_READY`
- best variant: `no_rest`
- best OOF BSS: `-0.027537`
- context safety: CLEAN for active pregame pipeline context files
- 16/16 ablation variants: blocked (no positive BSS)
- conclusion: root cause is model architecture, not feature selection.

## 3. Inline Baseline Confirmation (from artifacts)

- current best variant: `no_rest`
- current best OOF BSS: `-0.027537`
- current best OOF ECE: `0.042400`
- useful families: `recent_form`, `starter`
- noisy/zero families: `rest` (slight noise), `bullpen` (0 marginal), `weather` (0 marginal)
- context safety status: active pregame context files are safe
- gate status: `BLOCKED_NEGATIVE_BSS`

## 4. ML Feature Matrix Summary

Created module:
- `wbc_backend/prediction/mlb_ml_feature_matrix.py`

Key behavior:
- leakage-safe matrix rows only
- default policy `p13_v1`
- includes: `indep_recent_win_rate_delta`, `indep_starter_era_delta`
- excludes by default: rest/weather fields and bullpen proxy
- optional market/base feature allowed only by explicit flag
- outputs metadata with missing counts and policy trace

P13 run metrics:
- input_count: `2402`
- output_count (matrix rows): `1893`
- dropped_count: `509`
- missing_by_feature:
  - `indep_recent_win_rate_delta`: 16
  - `indep_starter_era_delta`: 493

## 5. Walk-Forward Split Summary

Created module:
- `wbc_backend/prediction/mlb_walk_forward_model.py`

Walk-forward settings used:
- min_train_size: `300`
- initial_train_months: `2`
- validation_months: `1`

Result:
- fold_count: `4`
- prediction_count: `1327`
- skipped_count: `566`
- leakage rule enforced: `train_end < validation_start` for every fold

## 6. Model Training Summary

Model:
- type: `logistic_regression` (sklearn)
- version label: `p13_walk_forward_logistic_v1`
- feature policy: `p13_v1`
- features:
  - `indep_recent_win_rate_delta`
  - `indep_starter_era_delta`

Training status:
- folds trained: `4`
- training failures: none
- mean_abs_coef (across folds): `0.141479`

## 7. Probability Export Result

Created script:
- `scripts/run_mlb_walk_forward_ml_candidate.py`

Command run:

```bash
.venv/bin/python scripts/run_mlb_walk_forward_ml_candidate.py \
  --input-csv outputs/predictions/PAPER/2026-05-11/mlb_odds_with_feature_candidate_probabilities.csv \
  --output-dir outputs/predictions/PAPER/2026-05-11/p13_ml \
  --model-type logistic_regression \
  --feature-policy p13_v1 \
  --min-train-size 300 \
  --initial-train-months 2
```

CLI summary:
- input_count: `2402`
- matrix_count: `1893`
- prediction_count: `1327`
- fold_count: `4`
- probability range: `[0.3360, 0.7095]`

## 8. OOF Calibration Result

Command run:

```bash
.venv/bin/python scripts/run_mlb_oof_calibration_validation.py \
  --input-csv outputs/predictions/PAPER/2026-05-11/p13_ml/ml_odds_with_walk_forward_predictions.csv \
  --output-dir outputs/predictions/PAPER/2026-05-11/p13_ml \
  --n-bins 10 \
  --min-train-size 300 \
  --min-bin-size 30 \
  --initial-train-months 2
```

Result:
- original_bss: `-0.014313`
- oof_bss: `-0.033835`
- delta_bss: `-0.019521` (worse)
- original_ece: `0.012419`
- oof_ece: `0.004323` (better calibration shape)
- recommendation: `OOF_REJECTED`
- deployability_status: `REJECTED`

## 9. Simulation Result

Command run:

```bash
.venv/bin/python scripts/run_mlb_strategy_simulation_spine.py \
  --date-start 2025-03-01 \
  --date-end 2025-12-31 \
  --strategy-name moneyline_edge_threshold_v0_p13_walk_forward_ml \
  --edge-threshold 0.01 \
  --kelly-cap 0.05 \
  --input-csv outputs/predictions/PAPER/2026-05-11/p13_ml/mlb_odds_with_oof_calibrated_probabilities.csv
```

Result:
- sample_size: `681`
- bet_count: `327`
- BSS: `-0.033834`
- ECE: `0.004323`
- ROI proxy: `-0.9115%`
- gate_status: `BLOCKED_NEGATIVE_BSS`

P13 source_trace evidence after patch:
- `walk_forward_ml_candidate_count = 681`
- `ml_model_type = ['logistic_regression']`
- `ml_feature_policy = ['p13_v1']`
- `ml_features_used = ['indep_recent_win_rate_delta','indep_starter_era_delta']`

## 10. Recommendation Result

Command run:

```bash
.venv/bin/python scripts/run_mlb_tsl_paper_recommendation.py \
  --date 2026-05-11 \
  --simulation-strategy-name moneyline_edge_threshold_v0_p13_walk_forward_ml \
  --allow-replay-paper
```

Result:
- simulation gate loaded: yes
- simulation gate status: `BLOCKED_NEGATIVE_BSS`
- recommendation gate: `BLOCKED_SIMULATION_GATE`
- paper_only: `true`
- stake_units_paper: `0.0`
- TSL probe: still blocked / 403

Recommendation source_trace includes ML evidence:
- `simulation_walk_forward_ml_candidate_count = 681`
- `simulation_ml_model_type = ['logistic_regression']`
- `simulation_ml_feature_policy = ['p13_v1']`
- `simulation_ml_features_used = [...]`

## 11. Test Results (PASS/FAIL counts)

P13 new tests:
- `tests/test_mlb_ml_feature_matrix.py`
- `tests/test_mlb_walk_forward_model.py`
- `tests/test_run_mlb_walk_forward_ml_candidate.py`

Result:
- `8 passed`

P12 tests:
- `48 passed`

P11 + targeted regression group (plus simulator/recommendation/model-probability contract):
- `165 passed`

Post-patch affected suites:
- `62 passed`

Missing files in requested command:
- `tests/test_mlb_feature_context_keys.py` not found
- `tests/test_mlb_feature_context_loader.py` not found
- equivalent existing P11 suite was executed instead.

## 12. Output Artifact Paths

P13 ML candidate outputs:
- `outputs/predictions/PAPER/2026-05-11/p13_ml/ml_feature_matrix.csv`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/ml_walk_forward_predictions.jsonl`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/ml_odds_with_walk_forward_predictions.csv`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/ml_model_metadata.json`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/ml_candidate_summary.md`

OOF calibration outputs:
- `outputs/predictions/PAPER/2026-05-11/p13_ml/mlb_odds_with_oof_calibrated_probabilities.csv`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/oof_calibration_evaluation.json`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/oof_calibration_folds.json`
- `outputs/predictions/PAPER/2026-05-11/p13_ml/p7_oof_calibration_summary.md`

Simulation output:
- `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p13_walk_forward_ml_f0ebf602.jsonl`
- `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p13_walk_forward_ml_f0ebf602_report.md`

Recommendation output:
- `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

## 13. Status Flags

- ML feature matrix module created: `true`
- walk-forward ML model module created: `true`
- ML candidate export CLI created: `true`
- walk-forward predictions produced: `true`
- OOF calibration produced: `true`
- simulation produced: `true`
- recommendation run produced: `true`
- production enablement attempted: `false`
- real bets placed: `false`
- replay-default-validation modified: `false`
- branch protection modified: `false`
- LotteryNew touched: `false`

## 14. Current Conclusion

P13 objective was completed technically, but candidate quality failed:

- We replaced manual logit correction with true walk-forward training.
- The trained logistic candidate does not pass the performance gate.
- OOF BSS worsened (`-0.014313 -> -0.033835`) and simulation remains blocked.
- Recommendation stays correctly blocked with zero stake.

This is an honest negative result and it is still meaningful progress: architecture replacement is now in place and test-covered, so next iterations can focus on model quality rather than pipeline plumbing.

## 15. P14 Recommended Direction

Decision rule applied:
- ML OOF BSS worsened and remains negative.

Recommended P14:

```text
P14 = model architecture rollback + feature/noise diagnostics
```

Practical P14 focus:
1. keep P13 pipeline but test alternate estimators and stronger regularization constraints.
2. add richer leakage-safe independent signals (lineup certainty, pitcher form windows, market microstructure timing) before retraining.
3. run side-by-side benchmark against P12 best (`no_rest`) and keep only candidates that improve BSS out-of-sample.
4. keep production NO_GO while TSL 403 and negative BSS persist.

## 16. Next Executable Task Prompt

```text
ROLE
You are Betting-pool's P14 Model Architecture Rollback + Noise Diagnostics Agent.

MISSION
Use the completed P13 pipeline as baseline, then run controlled architecture and regularization experiments to recover BSS.

TASKS
1. Compare:
   - P12 best no_rest baseline
   - P13 logistic walk-forward
   - P14 alternatives (regularized logistic variants, optional tree model if safe)
2. Keep the same walk-forward protocol and leakage-safe feature policy.
3. Produce a strict comparison table:
   - original_bss
   - oof_bss
   - delta_bss
   - ece
   - simulation gate_status
4. Run simulation and recommendation only for top candidate.
5. Keep paper-only and no production changes.

MARKER
P14_MODEL_ARCH_ROLLBACK_NOISE_DIAGNOSTICS_READY
```

