# P39I Walk-Forward Ablation Certification Report
**Date:** 2026-05-15  
**Certifies:** `P39I_WALKFORWARD_ABLATION_CERTIFIED_20260515`  
**Classification:** `NO_ROBUST_IMPROVEMENT`  
**paper_only:** True | **production_ready:** False

---

## 1. Input Summary

| Item | Value |
|------|-------|
| Enriched CSV | `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv` |
| Rows | 2,187 |
| Date range | 2024-04-15 → 2024-09-30 |
| y_true source | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` |
| Prior result | P39H: single split inconclusive (delta Brier +0.000956) |

---

## 2. Fold Design

- **n_folds_requested:** 5 temporal chunks (last chunk → never-predicted training bootstrap)
- **n_folds_evaluated:** 4 (chunks 1-4 predicted; chunk 0 = initial training only, 437 rows)
- **min_train_rows:** 400 (all 4 folds met threshold)
- **No random split** — time-ordered only

| Fold | Train N | Test N | Train End | Test Window |
|------|---------|--------|-----------|-------------|
| 0 | 437 | 437 | 2024-05-17 | 2024-05-18 → 2024-06-20 |
| 1 | 874 | 437 | 2024-06-19 | 2024-06-20 → 2024-07-26 |
| 2 | 1311 | 437 | 2024-07-25 | 2024-07-26 → 2024-08-28 |
| 3 | 1748 | 439 | 2024-08-27 | 2024-08-28 → 2024-09-30 |

---

## 3. Feature Groups Tested

| Group | Columns | N Features |
|-------|---------|-----------|
| `baseline_p_oof` | `p_oof` (direct) | 0 (no model) |
| `diff_features_only` | `diff_rolling_avg_launch_speed`, `diff_rolling_hard_hit_rate_proxy`, `diff_sample_size` | 3 |
| `home_away_rolling_only` | `home_rolling_*` + `away_rolling_*` | 8 |
| `full_statcast_rolling` | diff + home/away rolling | 11 |
| `p_oof_plus_full_statcast` | `p_oof` + all Statcast rolling | 12 |

---

## 4. Per-Fold Results (Baseline Brier)

Baseline (`p_oof` direct):

| Fold | Test Start | Test N | Baseline Brier |
|------|-----------|--------|----------------|
| 0 | 2024-05-18 | 437 | 0.2467 |
| 1 | 2024-06-20 | 437 | 0.2524 |
| 2 | 2024-07-26 | 437 | 0.2491 |
| 3 | 2024-08-28 | 439 | 0.2475 |

---

## 5. Aggregate Results

| Feature Group | Mean ΔBrier | % Folds Improved | Worst Degradation | Classification |
|---------------|------------|-----------------|-------------------|----------------|
| `diff_features_only` | **+0.0019** | 0% | +0.0044 | NO_ROBUST_IMPROVEMENT |
| `home_away_rolling_only` | **+0.0016** | 25% | +0.0069 | NO_ROBUST_IMPROVEMENT |
| `full_statcast_rolling` | **+0.0021** | 0% | +0.0061 | NO_ROBUST_IMPROVEMENT |
| `p_oof_plus_full_statcast` | **+0.0017** | 25% | +0.0053 | NO_ROBUST_IMPROVEMENT |

**Robust improvement threshold:** mean ΔBrier ≤ −0.002 AND ≥60% folds improved AND worst degradation ≤ +0.005

All four groups **fail all three criteria**:
- mean delta is positive (worsening) for every group
- 0–25% folds improved (threshold: ≥60%)
- worst degradation exceeds +0.005 in 3 of 4 groups

---

## 6. Comparison with P39H

| Metric | P39H (single split) | P39I (walk-forward avg) |
|--------|--------------------|-----------------------|
| Method | Single cut 2024-08-01 | 4-fold walk-forward |
| Baseline Brier | 0.2477 | 0.2464–0.2524 |
| Best candidate ΔBrier | +0.000956 | +0.0016 (best group) |
| Conclusion | INCONCLUSIVE | NO_ROBUST_IMPROVEMENT |

Walk-forward audit **corroborates** and **strengthens** P39H: no feature group consistently improves.

---

## 7. Whether Enriched Features Should Proceed

**Decision: FREEZE P39 Statcast rolling feature track.**

Evidence:
- 4 independent temporal folds all show positive (worsening) delta or no improvement
- No feature group (diff-only, home/away rolling, full Statcast, p_oof+Statcast) passes threshold
- worst-case fold degradation > +0.005 in 3 groups — material risk of harm
- Results consistent with P39H single-split finding

---

## 8. Whether P38A Should Remain Baseline

**Yes. P38A (`p38a_walk_forward_logistic_v1`, Brier ≈ 0.2487) remains the operative model.**

No evidence to replace it with any Statcast-enriched variant.

---

## 9. No Production Edge Claim

This is a paper-only research audit. No production edge is claimed. No odds, no CLV, no betting recommendation. pybaseball is a baseball stats source only.

---

## 10. P39J Decision

### If NO_ROBUST_IMPROVEMENT (current result ✅):

**Recommended P39J actions:**
1. **Freeze P39 pybaseball rolling feature track** — do not pursue further Statcast rolling average enrichment for model uplift with current feature set
2. **Consider alternative feature families** for next research cycle:
   - Pitcher-level features (starter ERA, recent starts, pitch mix) — not in current P39G set
   - Bullpen availability / workload (relief pitcher fatigue)
   - Starting lineup RSI / day-off patterns
   - Vegas consensus odds (once P3 odds source is unblocked — requires explicit operator decision)
3. **P3 odds track remains the highest-leverage unblocked path**: genuine CLV requires pregame odds, not Statcast features
4. **Maintain P38A OOF as production reference** for any future comparison

### Reminder

- pybaseball does not solve odds / CLV
- P3 odds source still blocked pending external API key / operator decision (P3.4 gate: OPERATOR_DECISION_PENDING)
- Next high-ROI action = resolve P3 operator decision → unblock real moneyline odds data

---

## Acceptance Marker

`P39I_WALKFORWARD_ABLATION_CERTIFIED_20260515`

## Regression Test Result

124/124 tests PASS across full regression suite:
- tests/test_p39b_pybaseball_leakage_policy.py
- tests/test_p39b_pybaseball_feature_aggregation.py
- tests/test_p39c_feature_join_contract.py
- tests/test_team_code_normalization.py
- tests/test_p39f_p38a_bridge_enrichment.py
- tests/test_p39h_enriched_model_comparison.py
- tests/test_p39i_walkforward_feature_ablation.py (15 new tests)

`P39I_REGRESSION_PASS_20260515`

## Push Gate

No explicit user YES received. Local commits not pushed.

`P39I_PUSH_NOT_AUTHORIZED_20260515`

`LOCAL_COMMITS_NOT_PUSHED_REQUIRES_EXPLICIT_YES`
