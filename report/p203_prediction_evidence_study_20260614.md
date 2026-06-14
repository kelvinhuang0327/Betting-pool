# P203 Prediction Evidence Study — INCONCLUSIVE

- **Final classification:** `P203_PRED_EVIDENCE_INCONCLUSIVE`
- **Task:** P203-PRED-EVIDENCE (IMPLEMENTATION_RESEARCH)
- **Generated at:** 2026-06-14T00:00:00Z
- **HEAD:** `122ba7895958157fc650b7d108676c13324fa91d` (main)

## 1. Executive Verdict

Primary comparison — **candidate_full vs frozen Elo baseline** (pooled OOS, n=2010):

- Brier improvement (baseline − candidate) point estimate: **-0.002757** (95% CI [-0.007517, 0.001864], 2000 block-bootstrap resamples).
- Frozen baseline Brier = 0.249811; candidate_full Brier = 0.252568.
- Folds where candidate improved: 2/5.
- **Verdict: `INCONCLUSIVE`.** Positive only if the 95% CI lower bound exceeds 0, log loss does not materially worsen, a majority of folds improve, and the gain is not driven by a single small segment.

## 2. Scope and Non-Actions

- research evidence only; NOT production model promotion
- no model/champion/registry/controlled_apply mutation
- no recommendation/evaluator mutation
- no MLB/StatsAPI endpoint or network call
- no live/historical data acquisition
- no provider unlock; live transport remains HOLD

## 3. Data Contract

- Loader: `data.mlb_data_loader.load_mlb_records()`; data_source tag `mlb_2025_retrosheet`.
- Raw rows: 2430; eligible rows: 2430; unique game_ids: 2430; excluded rows: 0.
- Duplicate (date,away,home) rows: 56 — canonical unit = game_id; rows sharing (date,away,home) are doubleheaders kept as distinct games (no dedup).
- Date range: 2025-03-18 → 2025-09-28 (184 unique dates).
- Target: `actual_home_win` — 1 if home team final score > away team final score, else 0; home-win base rate 0.542798.
- Frozen baseline: pre-game Elo win probability 1/(1+10^((away_elo-home_elo)/400)).
- Input fingerprints: scores `614341bf6a6e7f77f2c2ff2f0433b29fb56b51d8eed223c22ea1ff9705ee903c`; odds `56ee44889c3cb9430c60dbbba5bab6f692dc32620eadfa9cc062cda4d2078c6c`.

Excluded predictive fields (leakage risk / post-game):

- `market_home_prob` — closing-line/post-season scrape provenance mixed with Elo fallback; point-in-time pregame semantics NOT clear -> leakage risk, excluded as predictor
- `ou_line` — over/under total line, same closing/post-game provenance concern -> excluded as predictor
- `actual_home_score` — post-game outcome
- `actual_away_score` — post-game outcome
- `actual_home_win` — prediction target (post-game outcome), never an input
- `actual_total_runs` — post-game outcome

## 4. Leakage Controls

- Structural check `leakage_free` = **True** over 5 folds.
- All train dates strictly before test fold: True; no train/test index overlap: True; test folds disjoint: True.
- all features are pre-game rolling state computed by the loader with strict look-ahead isolation (Elo/rolling stats updated only after each game); features for a game use only prior-game outcomes.
- Missing-value handling: rows with any non-finite feature, non-binary target, or unparseable date are excluded and counted.

## 5. Frozen Baseline

- Pre-game Elo win probability, no fitting. Brier 0.249811, log loss 0.692915, ECE 0.053463, calibration intercept/slope 0.121462/0.501987.

## 6. Walk-Forward Design

- expanding-window chronological, date-disjoint segments; 6 segments → 5 OOS folds; primary metric out-of-sample Brier score.

| Fold | Train n | Test n | Train dates | Test dates |
|---|---|---|---|---|
| 0 | 420 | 400 | 2025-03-18→2025-04-27 | 2025-04-28→2025-05-27 |
| 1 | 820 | 408 | 2025-03-18→2025-05-27 | 2025-05-28→2025-06-27 |
| 2 | 1228 | 404 | 2025-03-18→2025-06-27 | 2025-06-28→2025-07-30 |
| 3 | 1632 | 394 | 2025-03-18→2025-07-30 | 2025-07-31→2025-08-29 |
| 4 | 2026 | 404 | 2025-03-18→2025-08-29 | 2025-08-30→2025-09-28 |

## 7. Calibration Result

- Method: Platt/logistic calibration (sigmoid(a+b*logit(p))); calibrator fitted only on past (training-fold) rows; candidate uses an inner past-only date split (last 20% of training dates) for calibration.
- Calibrated baseline Brier 0.248346 vs frozen 0.249811; improvement 0.001465 (95% CI [-0.00197, 0.004735]).
- Calibrated baseline ECE 0.035953 (frozen 0.053463).

## 8. Feature Groups

- **elo**: home_elo, away_elo
- **offense**: home_woba, away_woba
- **pitching**: home_fip, away_fip
- **form**: home_rsi, away_rsi
- **schedule**: home_rest_days, away_rest_days

## 9. Ablation Results

Delta vs candidate_full Brier (positive => removing the group worsens => group adds value):

| Group removed | Ablation Brier | Δ vs candidate | Group adds value |
|---|---|---|---|
| elo | 0.250886 | -0.001682 | False |
| offense | 0.252061 | -0.000507 | False |
| pitching | 0.251298 | -0.00127 | False |
| form | 0.251929 | -0.000639 | False |
| schedule | 0.25777 | 0.005202 | True |

## 10. Reference Model Comparison

- Simple reference (past-only home-win climatology) Brier 0.251192.
- Candidate_full vs reference Brier improvement -0.001376 (95% CI [-0.003558, 0.000882]).

## 11. Segment Stability

By prob band (frozen baseline prob):

| Band | n | Baseline Brier | Candidate Brier | Δ improvement | Insufficient |
|---|---|---|---|---|---|
| p_lt_0.45 | 670 | 0.255596 | 0.257783 | -0.002186 | False |
| p_0.45_0.55 | 669 | 0.251764 | 0.253368 | -0.001604 | False |
| p_gt_0.55 | 671 | 0.242087 | 0.246564 | -0.004477 | False |

By fold:

| Fold | n | Baseline Brier | Candidate Brier | Δ improvement |
|---|---|---|---|---|
| fold_0 | 400 | 0.242311 | 0.263011 | -0.0207 |
| fold_1 | 408 | 0.253432 | 0.255059 | -0.001628 |
| fold_2 | 404 | 0.255609 | 0.249507 | 0.006103 |
| fold_3 | 394 | 0.253025 | 0.24878 | 0.004245 |
| fold_4 | 404 | 0.244647 | 0.246468 | -0.001821 |

## 12. Statistical Uncertainty

- Paired block bootstrap by game-date, 2000 resamples, fixed seed 20260614, 150 date blocks.
- brier_improvement = brier_baseline - brier_candidate (positive => candidate better).
- Primary 95% CI for Brier improvement: [-0.007517, 0.001864]; lower bound above zero: False.
- Significance is **not** claimed from a point estimate alone.

## 13. Success/Failure Gate

- **Classification: INCONCLUSIVE.**

| Criterion | Value |
|---|---|
| brier_point_improves | False |
| ci95_lower_above_zero | False |
| log_loss_not_materially_worse | True |
| log_loss_delta | 0.005727 |
| leakage_free | True |
| majority_folds_improved | False |
| folds_improved | 2/5 |
| not_single_segment_driven | False |
| coverage_equal | True |

- Thresholds: log-loss material abs 0.01, majority folds 3, segment min n 100.

## 14. Limitations

- [Inferred] Features are crude proxies (rolling run-rate-based wOBA/FIP, win-rate RSI), not true game-specific point-in-time pitcher/lineup data.
- [Inferred] market_home_prob (closing line) is excluded as a predictor due to post-season scrape provenance; this study cannot speak to market-informed models.
- [Inferred] A null/inconclusive result reflects the proxy-feature ceiling, not necessarily a model implementation limit; it cannot by itself distinguish model limitation from data limitation.
- [Inferred] Single 2025 season; no cross-season generalisation tested.
- [Inferred] Calibration uses a single primary method (Platt); other calibrators not adopted as primary.

## 15. Recommended Next Step

- package evidence; do not promote candidate; next task must narrow uncertainty without relaxing leakage controls; NO live implementation
- Packaging (branch/commit/PR) is a separately authorized action; this study does not self-authorize it.
- Live transport remains HOLD; model/recommendation promotion and live implementation are NOT authorized.

## 16. Required Completion Check

- Eligible sample: 2430 games (raw 2430), data_source `mlb_2025_retrosheet`.
- OOS folds: 5; pooled OOS n: 2010.
- Leakage-free: True.
- Primary Brier improvement: -0.002757 (95% CI [-0.007517, 0.001864]).
- Final classification: `P203_PRED_EVIDENCE_INCONCLUSIVE`.
- Network/API/DB/runtime/production mutations: NONE.
- Live transport: HOLD. Track B: not sent.

