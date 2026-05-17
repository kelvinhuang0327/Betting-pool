# P39H — Modeling Scope Decision
**Date**: 2026-05-15  
**Mode**: PAPER_ONLY_TIME_AWARE_MODEL_COMPARISON  
**Marker**: `P39H_MODELING_SCOPE_DECISION_20260515_READY`

---

## 1. Selected Mode

**PAPER_ONLY_TIME_AWARE_MODEL_COMPARISON**

This is a research-only comparison. No production bets, no live TSL, no CLV, no betting recommendation, no edge claim.

---

## 2. Input

| Field | Value |
|-------|-------|
| Enriched CSV | `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv` |
| Rows | 2,187 |
| Date range | 2024-04-15 → 2024-09-30 |
| Null feature cols | 0 (all 8 rolling cols 100% non-null) |
| y_true source | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` |
| y_true join key | `game_id` |
| y_true match rate | 100.0% (2187/2187) |

---

## 3. Baseline

| Metric | Value |
|--------|-------|
| Baseline model | P38A p_oof (calibrated OOF probability) |
| Baseline Brier | 0.2487 |
| Baseline BSS | +0.0020 vs base-rate |
| Training context | P38A OOF (cross-validated, no leakage) |

---

## 4. Candidate Model

| Attribute | Value |
|-----------|-------|
| Model type | LogisticRegression (sklearn, C=1.0, max_iter=1000) |
| Features | 8 rolling Statcast features + p_oof |
| Feature scaling | StandardScaler (fit on train only) |
| Complexity | Low — no tree ensemble, no tuning |
| Odds features | NONE |
| Postgame features | NONE |
| Target leakage | NONE |

### Feature columns
```
home_rolling_pa_proxy
home_rolling_avg_launch_speed
home_rolling_hard_hit_rate_proxy
home_rolling_barrel_rate_proxy
away_rolling_pa_proxy
away_rolling_avg_launch_speed
away_rolling_hard_hit_rate_proxy
away_rolling_barrel_rate_proxy
diff_rolling_avg_launch_speed
diff_rolling_hard_hit_rate_proxy
diff_sample_size
p_oof
```

---

## 5. Split Policy

| Attribute | Value |
|-----------|-------|
| Split type | Time-aware (chronological) |
| Split key | `game_date` |
| Default test_start_date | 2024-08-01 |
| Train rows | 1,389 (2024-04-15 → 2024-07-31) |
| Test rows | 798 (2024-08-01 → 2024-09-30) |
| Random split | **FORBIDDEN** |
| Same-game leakage | **FORBIDDEN** |
| Feature window | 7-day rolling, window_end < game_date (verified in P39G) |

---

## 6. Expected Outputs

| Output | Path |
|--------|------|
| Metrics JSON | `outputs/predictions/PAPER/p39h_enriched_feature_model_comparison_20260515.json` |
| Report | `00-BettingPlan/20260513/p39h_enriched_feature_model_comparison_report_20260515.md` |

### Metrics included
- Train rows, test rows
- Feature columns used
- Baseline Brier (p_oof on test)
- Enriched Brier (model on test)
- Delta Brier
- Baseline log-loss
- Enriched log-loss
- BSS vs base-rate (enriched)
- Interpretation: improved / not improved / inconclusive

---

## 7. Non-Goals

- No production bet
- No live TSL write
- No CLV computation
- No betting recommendation
- No edge claim
- No push without explicit YES
- No odds features
- No random split
- No postgame data

---

`P39H_MODELING_SCOPE_DECISION_20260515_READY`  
`PAPER_ONLY=True | pybaseball != odds source | no push`
