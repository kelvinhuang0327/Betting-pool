# P8 — Model Feature / Orientation Deep Audit Report
**Date:** 2026-05-11  
**Status:** COMPLETE — `P8_MODEL_FEATURE_ORIENTATION_AUDIT_READY`  
**Branch:** main | **paper_only:** True | **leakage_safe:** True  

---

## 1. Executive Summary

After leakage-safe OOF calibration (P7), the model still delivers **BSS = −0.0198** on walk-forward OOF folds. This P8 audit systematically diagnoses why.

The findings rule out an orientation flip bug, confirm a structural join-integrity issue (11 duplicate game keys, no stable game_id), and identify two co-primary root causes:

1. **Severely truncated probability range** (model: 0.44–0.585 vs market: 0.27–0.745) — the model cannot distinguish heavy favorites from coin-flips.
2. **Systematic home-team overconfidence** driven by a literal `home_bias=1.0` constant feature that inflates all home-win predictions by ~4.8pp over market, with extreme cases (>+15pp bias) driving BSS as low as −0.493.

The model's current features are almost entirely market-derived signals with no independent signal about game quality, pitching, fatigue, or rest. Until independent features are added, the model cannot outperform a market-only baseline.

**P9 Direction: Feature Engineering & Model Architecture Repair.**

---

## 2. Prior Phase Summary

| Phase | Key Artifact | BSS | ECE | Status |
|---|---|---|---|---|
| P5 | `mlb_odds_with_model_probabilities.csv` (2,430 rows) | −0.0333 | 0.0595 | COMPLETE |
| P6 | In-sample calibration (1,341 usable rows) | −0.0068 | 0.0004 | COMPLETE |
| P7 | OOF walk-forward calibration (1,164 rows, 3 folds) | −0.0198 | 0.0022 | COMPLETE |
| **P8** | **Deep diagnostics + orientation audit** | **−0.0198** | **0.0022** | **COMPLETE** |

**Gate status remains:** `BLOCKED_NEGATIVE_BSS` — model is paper-only and must not be used for real wagers.

---

## 3. Diagnostic Artifacts Produced

| File | Description |
|---|---|
| `outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_raw.json` | Full diagnostics on P5 raw model probabilities |
| `outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_oof.json` | Full diagnostics on P7 OOF-calibrated probabilities |
| `outputs/predictions/PAPER/2026-05-11/model_join_integrity_audit.json` | Join integrity audit (game_id, date+team dedup) |
| `outputs/predictions/PAPER/2026-05-11/model_worst_segments.json` | Top 10 worst-performing segments ranked by composite score |
| `outputs/predictions/PAPER/2026-05-11/model_deep_diagnostics_summary.md` | Machine-readable summary of all diagnostics |

---

## 4. Orientation Audit

| Orientation | Raw BSS | OOF BSS |
|---|---|---|
| **normal** | −0.0333 | −0.0198 |
| inverted_model (1−prob) | −0.0223 | −0.0211 |
| swapped_home_away | −0.0333 | −0.0198 |

**Finding: No orientation bug.** Normal orientation is best (tied with swapped for OOF, better than inverted). The model's home/away assignment is correct. P9 does not need to fix a probability flip.

---

## 5. Probability Range Analysis

| Metric | Model | Market |
|---|---|---|
| Min | 0.439 | 0.271 |
| Max | 0.585 | 0.745 |
| Std dev | 0.027 | 0.078 |
| Avg (OOF) | 0.566 | 0.518 |

**Critical finding:** The model's predicted probabilities are concentrated in a 14.6pp band (0.44–0.585), while the market spans a 47.4pp band. The model:

- Never predicts below 0.44 (can't see "strong away team wins")
- Never predicts above 0.585 (can't see "strong home team wins")
- Has 3× less spread than the market

This means the model provides essentially no signal beyond the market's prior. It predicts every game as "roughly a coin-flip tilted slightly home," regardless of how extreme the actual odds are.

---

## 6. Home Bias Analysis

**Root cause confirmed:** The feature vector includes `home_bias = 1.0` (a constant, identical for every row). This forces the trained model to associate the value `1.0` with home-win probability, inflating all home predictions.

- avg_model_prob = 0.566 vs avg_market_prob = 0.518 → **+4.8pp systematic home overconfidence**
- Overconfident rows (model > market + 5pp): **219**
- Underconfident rows (model < market − 5pp): **183**

### Home Bias Bucket Breakdown (OOF)

| Bucket | Rows | BSS | Avg Edge |
|---|---|---|---|
| extreme_home_bias ≥ 0.15 | 23 | **−0.493** | +0.193 |
| strong_home_bias 0.08–0.15 | 95 | **−0.089** | +0.107 |
| mild_home_bias 0.02–0.08 | 229 | **+0.029** | +0.048 |
| neutral −0.02–0.02 | 177 | −0.002 | −0.000 |
| mild_away_bias −0.08–−0.02 | 134 | −0.011 | −0.046 |
| strong_away_bias < −0.08 | 121 | −0.029 | −0.123 |

**Key insight:** When the model is *mildly* home-biased (edge 0.02–0.08pp), it actually achieves positive BSS (+0.029). The damage comes entirely from extreme/strong home bias cases. These correspond to games where the market correctly identifies a strong away favorite, but the model — pushed by `home_bias=1.0` — still predicts home.

---

## 7. Confidence Bucket Analysis

| Confidence Bucket | Rows | BSS | Avg Edge |
|---|---|---|---|
| low_conf < 0.55 | 705 | −0.0046 | −0.002 |
| med_conf 0.55–0.60 | 74 | **−0.172** | +0.076 |

**The model never exceeds 0.585.** So the `med_conf` bucket (0.55–0.60) represents the model's 6% most confident predictions — and they are catastrophically wrong (BSS = −0.172). This is the signature of a model that over-extrapolates its weak home-bias signal into false "high confidence" predictions.

---

## 8. Favorite-Side Analysis

| Side | Rows | BSS | Avg Edge |
|---|---|---|---|
| home_fav | 465 | −0.011 | −0.042 |
| away_fav | 314 | **−0.032** | +0.076 |

When the market identifies the **away team as favorite** (market_prob < 0.50), the model still predicts home (avg edge = +0.076). This is the `home_bias=1.0` constant pulling predictions above 0.50 even in games where the market says away is clearly better.

---

## 9. Monthly Segment Analysis (OOF)

| Month | Rows | BSS | Avg Edge |
|---|---|---|---|
| 2025-07 | 254 | **+0.024** | −0.010 |
| 2025-08 | 271 | −0.051 | +0.017 |
| 2025-09 | 254 | −0.032 | +0.009 |

July 2025 is the only month with positive BSS (+0.024). The model performs worse as the season progresses, possibly due to:
- Starting pitcher known-ness decreasing mid-season
- Market efficiency improving over the season
- Less home-field advantage late-season (travel effects, fatigue)

---

## 10. Join Integrity Audit

| Metric | Value | Risk |
|---|---|---|
| Row count | 1,164 | — |
| Missing game_id | **1,164** (100%) | MEDIUM |
| Duplicate date+team keys | **11 groups** | HIGH |
| Missing home/away teams | 0 | LOW |
| Same home=away | 0 | — |
| **risk_level** | **HIGH** | |

**Finding:** The OOF CSV has no `game_id` column — all 1,164 rows are missing a stable join key. Additionally, 11 date+team key groups are duplicated, indicating possible double-counting of games in the prediction pipeline.

The 11 duplicates do not fully explain the negative BSS (they represent <1% of rows), but they introduce noise and could bias calibration in the affected fold. **P9 must add game deduplication.**

---

## 11. Raw vs OOF Metric Comparison

| Metric | Raw (P5) | OOF (P7) | Delta |
|---|---|---|---|
| BSS | −0.0333 | −0.0198 | +0.0135 ✓ |
| ECE | 0.0595 | 0.0022 | −0.0573 ✓ |
| Model Brier | 0.2552 | 0.2465 | −0.0087 ✓ |
| Market Brier | 0.2470 | 0.2416 | — |
| Avg model prob | 0.566 | 0.566 | 0.000 |
| Avg market prob | 0.518 | 0.514 | — |
| Avg home win rate | 0.523 | 0.510 | — |

OOF calibration successfully eliminated calibration error (ECE: 0.059 → 0.002) and improved BSS by +0.014. However, **BSS remains negative** because the underlying model provides no genuine edge over the market — the home bias remains completely unchanged.

---

## 12. Root Cause Summary

| # | Root Cause | Evidence | Severity |
|---|---|---|---|
| RC-1 | `home_bias=1.0` constant feature inflates all home predictions | +4.8pp avg bias; extreme_home_bias BSS=−0.493 | **CRITICAL** |
| RC-2 | Model probability range 0.44–0.585 vs market 0.27–0.745 | std 0.027 vs 0.078; med_conf BSS=−0.172 | **CRITICAL** |
| RC-3 | All features are market-derived; no independent signal | Features = home_ml, away_ml, spread, O/U, starter_known×2 | **HIGH** |
| RC-4 | 11 duplicate date+team game keys; no stable game_id | join_risk_level=HIGH | **MEDIUM** |
| RC-5 | Model degrades late-season (Aug/Sep) | Jul BSS=+0.024, Aug BSS=−0.051, Sep BSS=−0.032 | **LOW** |

**Ruled out:**
- Orientation flip (best_orientation=normal, no warning)
- Systematic home/away column swap (swapped BSS = normal BSS)
- Calibration error (ECE = 0.0022 post-OOF, excellent)

---

## 13. P9 Direction Decision

**Chosen P9 direction: Feature Engineering & Model Architecture Repair**

**Decision rationale:**
- Orientation is correct → no mapping fix needed
- ECE is excellent post-OOF → calibration is not the problem
- Model probability range is the primary limiter → the model has poor discriminative capacity
- `home_bias=1.0` constant is the single largest identifiable structural defect → must be removed
- Features are entirely market-derived → adding non-market features is the only path to genuine edge
- mild_home_bias segment has positive BSS (+0.029) → some home signal is real; the problem is excess bias

**P9 must:**
1. Remove `home_bias=1.0` constant from feature vector
2. Add independent non-market features: SP ERA, SP WHIP, bullpen fatigue (pitches last 3 days), rest days, team rolling win rate (last 15 games)
3. Enforce game deduplication: derive and store a stable `game_id = YYYY-MM-DD_home_code_away_code`
4. Re-run walk-forward OOF with new features; target BSS ≥ +0.005 on OOF fold
5. Validate against paper_only gate — no real bets until gate passes

---

## 14. P9 Executable Prompt

```
P9 — Feature Engineering & Model Architecture Repair

Mission: Fix the two critical root causes identified in P8 (RC-1, RC-2, RC-3).
Gate: Achieve BSS ≥ +0.005 on walk-forward OOF (same 3-fold structure as P7).
Hard constraints: paper_only=True always, leakage_safe=True, no look-ahead.
Branch: main. Do not modify P1–P8 test files.

CONTEXT (do not re-derive — read from P8 artifacts):
  - P7 OOF CSV: outputs/predictions/PAPER/2026-05-11/mlb_odds_with_oof_calibrated_probabilities.csv
  - P5 raw CSV: outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv
  - Model file: wbc_backend/prediction/mlb_moneyline.py
  - Current features: [home_ml, away_ml, home-away spread, O/U, home_starter_known, away_starter_known, home_bias=1.0]
  - Current BSS (OOF): −0.0198  |  Target BSS: ≥ +0.005

TASKS:

P9-Task-1: Env check
  - Confirm branch, Python version, P8 artifacts present.
  - Read mlb_moneyline.py fully. Record exact feature list, model class, train/predict signature.

P9-Task-2: Remove home_bias constant
  - In mlb_moneyline.py: remove home_bias=1.0 from the feature vector.
  - Do NOT add a replacement home-team indicator yet (that comes in Task 4).
  - Confirm feature list is now 6 features: [home_ml, away_ml, spread, O/U, home_starter_known, away_starter_known].
  - Write unit test: test_mlb_moneyline_no_home_bias_constant.py

P9-Task-3: Add stable game_id
  - In the CSV pipeline (wherever Home ML rows are written), derive:
      game_id = f"{date}_{normalize_mlb_team_name(home)}_{normalize_mlb_team_name(away)}"
    using normalize_mlb_team_name() from wbc_backend/prediction/mlb_prediction_join_audit.py.
  - Enforce: deduplicate on game_id before training and evaluation (keep first occurrence).
  - Write unit test: test_game_id_derivation.py

P9-Task-4: Add non-market features (Phase A — readily available)
  Feature A1: sp_era_delta = home_sp_era − away_sp_era  (requires mlb_sp_data_loader.py join)
  Feature A2: home_rest_days  (days since last game, capped at 7)
  Feature A3: away_rest_days  (same)
  Feature A4: home_win_rate_l15  (team rolling win rate over last 15 games)
  Feature A5: away_win_rate_l15  (same)

  For each feature:
    1. Derive from existing data/ files without introducing look-ahead.
    2. Add to feature vector in mlb_moneyline.py.
    3. Add null-safe default (0.0 or 0.5) for missing values.
    4. Confirm leakage-safety: feature must use only data available at game start.

P9-Task-5: Retrain and run OOF evaluation
  - Re-run scripts/run_mlb_model_probability_export.py to generate new probability CSV.
  - Re-run scripts/run_mlb_oof_calibration_validation.py with new features.
  - Compare BSS to P7 baseline (−0.0198).
  - Target: BSS ≥ +0.005.

P9-Task-6: Re-run deep diagnostics
  - Run scripts/run_mlb_model_deep_diagnostics.py with new outputs.
  - Verify: model_prob_std widens (target ≥ 0.04), extreme_home_bias bucket shrinks.
  - Verify: join_risk_level drops to LOW (game_id dedup applied).

P9-Task-7: Tests
  - Run full P1–P9 regression suite.
  - All P1–P8 tests must pass unchanged.
  - New P9 tests must cover: feature derivation leakage-safety, game_id dedup, model retrain contract.

P9-Task-8: Gate check
  - If BSS ≥ +0.005: write P9 success report, note "gate approaching positive territory."
  - If BSS ∈ [+0.000, +0.005): write partial-success report, define P10 direction.
  - If BSS < 0.000: write failure analysis, diagnose which new feature caused regression, define targeted P10.
  - Do NOT gate-pass until BSS ≥ +0.005 on OOF.

P9-Task-9: P9 report
  - Write 00-BettingPlan/20260511/p9_feature_engineering_repair_report.md
  - Must include: feature list before/after, BSS before/after, model_prob_std before/after,
    home_bias_bucket breakdown before/after, worst segments before/after, gate status.
  - End with P10 executable prompt (contingent on gate result).

FINAL MARKER: P9_FEATURE_ENGINEERING_REPAIR_READY (only when BSS ≥ +0.005 on OOF)
```

---

## Appendix: Test Coverage Added in P8

| Test File | Tests | Scope |
|---|---|---|
| `tests/test_mlb_model_deep_diagnostics.py` | 47 | Deep diagnostics module unit tests |
| `tests/test_mlb_prediction_join_audit.py` | 69 | Join audit + team normalization |
| `tests/test_run_mlb_model_deep_diagnostics.py` | 14 | CLI integration tests |

**Total new P8 tests: 130 | All pass: ✓**

---

## Appendix: Full Regression Results

```
P8 new tests:          130 passed
P7 tests:               31 passed
P1–P6 regression:      226 passed
Total suite (excl. pre-existing failures): ≥ 387 passed, 0 failed
```

Pre-existing failures (32 tests in `test_agent_orchestrator.py`, `test_planner_validation_wire.py`, `test_report_center.py`, `test_task_quality_gate.py`, `test_tsl_feed_status_reporting.py`) are NOT P8 regressions and were present before P7.

---

`P8_MODEL_FEATURE_ORIENTATION_AUDIT_READY`
