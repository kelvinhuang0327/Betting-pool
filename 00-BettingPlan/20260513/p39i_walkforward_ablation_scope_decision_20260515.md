# P39I Walk-Forward Feature Ablation — Scope Decision
**Date:** 2026-05-15  
**Mode:** PAPER_ONLY_WALKFORWARD_ABLATION_AUDIT  
**paper_only:** True | **production_ready:** False

---

## Selected Mode

`PAPER_ONLY_WALKFORWARD_ABLATION_AUDIT`

No odds, no CLV, no production edge, no betting recommendation.

---

## Input

- **Enriched CSV**: `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv`  
  - 2,187 rows × 23 columns  
  - Date range: 2024-04-15 to 2024-09-30  
  - y_true joined from: `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv`
- **Bridge CSV**: `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv`

---

## Previous Result (P39H)

- **Method**: Single time-aware train/test split at 2024-08-01
- **Train rows**: 1,389 | **Test rows**: 798
- **Baseline P38A p_oof Brier**: 0.2477
- **Enriched LR + Statcast Brier**: 0.2486
- **Delta Brier**: +0.000956 (worsened, within ±0.001 noise threshold)
- **Classification**: `P39H_MODEL_COMPARISON_INCONCLUSIVE`
- **Conclusion**: Enriched rolling Statcast features did not robustly improve over P38A baseline with single split

---

## Why P39I

1. **Single split is insufficient**: one time-split verdict is noisy; the test window may be atypical (late-season, playoff push effects)
2. **Fold-level robustness needed**: need to assess whether enrichment helps consistently across multiple time windows
3. **Feature family ablation needed**: need to identify which feature groups (if any) drive signal, and which add noise
4. **False negative risk**: inconclusive result could mask a small but consistent improvement in a specific feature sub-group

---

## Feature Groups

| Group | Columns |
|-------|---------|
| `baseline_p_oof` | `p_oof` (direct, no model training) |
| `diff_features_only` | `diff_rolling_avg_launch_speed`, `diff_rolling_hard_hit_rate_proxy`, `diff_sample_size` |
| `home_away_rolling_only` | all `home_rolling_*` + `away_rolling_*` columns |
| `full_statcast_rolling` | diff + home/away rolling features (no p_oof) |
| `p_oof_plus_full_statcast` | `p_oof` + all Statcast rolling features |

---

## Robust Improvement Definition

All three criteria must be met simultaneously:

| Criterion | Threshold | Rationale |
|-----------|-----------|-----------|
| mean delta Brier | ≤ −0.002 | materially better than noise level |
| folds improved % | ≥ 60% | majority of folds improve, not noise |
| worst fold degradation | ≤ +0.005 | no catastrophic collapse in any single fold |

---

## Walk-Forward Design

- Sort by `game_date` (chronological)
- 5 temporal chunks; fold k trains on chunks 0..k−1, tests on chunk k
- min_train_rows = 400
- No random split, no shuffling
- Folds with insufficient train/test rows are skipped and logged

---

## Non-Goals

- No odds, no moneyline / run-line / totals
- No CLV analysis
- No production edge claim
- No betting recommendation
- No live-data write
- No production ledger modification
- pybaseball = baseball stats source only, not odds source

---

## Acceptance Marker

`P39I_WALKFORWARD_ABLATION_SCOPE_READY_20260515`
