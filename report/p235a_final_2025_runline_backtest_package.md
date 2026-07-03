# P235-A — Final 2025 Run Line Backtest Package

> **最終、獨立、僅本機歷史 / paper-only 的 2025 Run Line backtest 彙整包。** 彙整 P226-A / P228-A / P230-A / P232-A 既有結果，並附本機統計附錄；非未來預測、非下注建議、無 EV/Kelly 宣稱、無 live 市場宣稱、無 production/DB 變更、非已證實 edge、非跨球季驗證、非 true-PIT 驗證。

## Executive Summary
- This is the final, standalone, historical paper-only 2025 Run Line backtest package for MLB, consolidating P226-A (baseline model), P228-A (robustness + calibration), P230-A (local multi-season data audit), and P232-A (feature ablation); P234 has no local artifact and is acknowledged as not found (see p234_status).
- The poisson_team_rate_model beats the 0.5 coinflip Brier baseline on the 2025 run_line test set (972 decided games): accuracy 0.6008 vs 0.4568, Brier 0.2395 vs 0.2500; train-fold-only Platt calibration further improves Brier to 0.2375 and ECE from 0.0483 to 0.0180.
- Robustness holds across pre-registered chronological splits (3/3 beat coinflip) and most monthly windows (4/5, 2 skipped for insufficient train rows); a local-only bootstrap/permutation appendix on the same 972-game ledger shows the Brier improvement is statistically distinguishable from zero at the 95% level (seeded, deterministic, no retraining).
- Feature ablation shows the signal depends on a fragile feature group: each single component (offense rate, defense rate, home field) survives alone across all 3 splits, but removing offense+defense together fails to beat coinflip at the 0.7 train-fraction split.
- Data status: 2024=LABEL_ONLY_NO_ODDS, 2025=FULL_RUNLINE_EVAL_READY, 2026=MISSING_OR_UNUSABLE; multi-season expansion remains structurally blocked, not a modeling gap.
- Provider path status: PARKED_OPTIONAL — no provider has been contacted and no true-PIT provider data has ever been used in this evidence chain.
- This package is 2025-only, historical paper-only, uses odds of unverified provenance, is not true-PIT, is not a betting edge, is not live, is not production, is not a future prediction, and is not a multi-season validation.

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- 2025-ONLY: single-season evaluation universe (data/mlb_2025/mlb_odds_2025_real.csv); NOT a multi-season validation
- descriptive synthesis of already-published P226-A / P228-A / P230-A / P232-A results plus a local-only statistical appendix computed from existing prediction ledgers; NOT a new model, NOT a re-run, NOT a re-derivation, NO retraining
- PROVENANCE-UNVERIFIED: run line spread/prices are a post-game unverified snapshot (is_verified_real=False); settlement / descriptive market reference only, NEVER a model input feature; NOT true point-in-time (PIT) data
- NO betting recommendation; NO EV/Kelly claim; NOT a proven betting edge
- NO live-market claim; NOT production; NOT real betting; NO future prediction
- NO provider was contacted for this package; provider path status is PARKED_OPTIONAL
- P226-A / P228-A / P230-A / P232-A source artifacts are read-only inputs and are not modified by this package

## 1. Gate 0 Reproduction
- 狀態：`GATE0_REPRODUCED_P235A_FINAL_PACKAGE`
- 方法：accuracy/Brier/calibrated-Brier independently recomputed from report/p226a_run_line_total_predictions.csv and report/p228a_run_line_robustness_predictions.csv raw ledger rows (no retraining); ECE verified against report/p228a_run_line_robustness_scorecard.json (pytest-covered tracked artifact)
- coinflip：accuracy=0.4568、brier=0.2500
- poisson_team_rate_model：accuracy=0.6008、brier=0.2395
- train-fold-only Platt calibrated：brier=0.2375
- ECE：0.0483 -> 0.0180
- all_within_tolerance：`True`

## 2. Scorecard Summary
- 來源：`report/p226a_run_line_total_scorecard.json`；測試期 `2025-07-18`→`2025-09-28`（972 場）
- coinflip baseline：accuracy=0.4568、brier=0.2500
- poisson_team_rate_model：accuracy=0.6008、brier=0.2395、ECE=0.0483

## 3. Prediction Ledger References
| task | path | rows | role |
|---|---|--:|---|
| P226-A | `report/p226a_run_line_total_predictions.csv` | 3888 | run line / total probability model + paper backtest predictions (baseline_coinflip_50pct + poisson_team_rate_model, run_line + total markets) |
| P228-A | `report/p228a_run_line_robustness_predictions.csv` | 972 | run line robustness & train-fold-only Platt calibration predictions (raw + calibrated probabilities, anchor split) |
| P232-A | `report/p232a_run_line_feature_ablation_predictions.csv` | 4860 | 2025 single-season run line feature ablation predictions (full_model + 4 ablation variants x 3 chronological splits) |

## 4. Robustness Summary
- 3/3 chronological splits beat coinflip; 4/5 monthly windows beat coinflip (2 skipped, insufficient train)
- P228-A 穩健性判定：`ROBUST_ENOUGH_FOR_FURTHER_HISTORICAL_RESEARCH`

## 5. Calibration Summary
- Brier 0.2395 -> 0.2375; ECE 0.0483 -> 0.0180
- 校準是否改善 Brier：`True`；改善 ECE：`True`

## 6. Ablation Summary
- 判定：`SIGNAL_DEPENDS_ON_FRAGILE_FEATURE_GROUP`
- SIGNAL_DEPENDS_ON_FRAGILE_FEATURE_GROUP: single-component ablations (ablate_offense_rate, ablate_defense_rate, ablate_home_field) survive across all 3 splits; removing offense+defense together (ablate_team_strength_both) fails to beat coinflip at train_frac=0.7
- 失敗切分細節：train_frac=0.7、accuracy=0.5953、brier=0.2509 (> coinflip brier=0.2500)

## 7. Data Status
- 來源：`report/p230a_local_multiseason_runline_data_audit.json`
- 2024 = `LABEL_ONLY_NO_ODDS`
- 2025 = `FULL_RUNLINE_EVAL_READY`
- 2026 = `MISSING_OR_UNUSABLE`

## 8. P234 Status
- found_locally = `False`
- No P234 report, script, or task artifact exists anywhere in this repository as of this build (report/, 00-Plan/, scripts/, tests/ all searched for 'p234'). P234 is acknowledged per task instructions but not consolidated because there is no local evidence to consolidate; this is a factual gap-report, not a fabricated status.

## 9. Provider Path Status
- 狀態：`PARKED_OPTIONAL`
- provider_replies_received = 0
- true_pit_provider_data_used = `False`
- no provider was contacted to build this package; the provider path remains parked pending a separate, explicit Owner decision

## 10. Local-Only Statistical Appendix
- 來源 ledger：`report/p226a_run_line_total_predictions.csv`（972 場 run_line test-set decided games）；no_retraining=`True`
- **Bootstrap 95% CI**（seed=235235、n_resamples=5000）：mean brier margin (coinflip-poisson) = 0.010467，95% CI = [0.000956, 0.019645]
- **Paired permutation test**（seed=235236、n_permutations=5000）：one-sided p-value = 0.015197（H1：poisson Brier 改善 > 0）
- **Chronological split stability**：split-grid 3/3 勝出、monthly windows 4/5 (2 skipped: insufficient train rows)（彙整自 P228-A，非本檔重算）
- **Predictive baseline**（`PREDICTIVE_BASELINE`，coinflip）：accuracy=0.4568、brier=0.2500
- **Majority-class reference**（`REFERENCE_ONLY`）：AWAY base rate=0.5432、HOME base rate=0.4568；若一律預測較多的一側，準確率=0.5432（descriptive test-set base rate of the more frequent actual side; computed post-hoc from test-set outcomes, NOT a valid pre-registered forward predictive baseline (a safe train-fold majority baseline cannot be computed from existing artifacts without re-deriving per-split labels); presented for descriptive reference only, NOT a betting/edge baseline）
- **Model**（`MODEL`，poisson_team_rate_model）：accuracy=0.6008、brier=0.2395
- 完整統計附錄表格見 `report/p235a_final_2025_runline_statistical_appendix.csv`

## 11. Limitation Labels
- `2025-ONLY`
- `HISTORICAL_PAPER_ONLY`
- `ODDS_PROVENANCE_UNVERIFIED`
- `NOT_TRUE_PIT`
- `NOT_BETTING_EDGE`
- `NOT_LIVE`
- `NOT_PRODUCTION`
- `NOT_FUTURE_PREDICTION`
- `NOT_MULTI_SEASON_VALIDATION`

## 12. Decision Options
- **HOLD_ARCHIVE_CURRENT_EVIDENCE**：Archive this package as the final, standalone 2025 Run Line backtest evidence record; no further Run Line work is authorized by this package alone.
- **RESTART_PROVIDER_PATH_LATER**：Later restart the provider outreach path only if the Owner wants a true point-in-time (PIT) evidence upgrade; NOT authorized by this package.
- **CROSS_SEASON_VALIDATION_LATER**：Later attempt cross-season validation only if actual usable multi-season Run Line data becomes locally available (currently blocked per P230-A: 2024=LABEL_ONLY_NO_ODDS, 2026=MISSING_OR_UNUSABLE); NOT authorized by this package.

## 免責聲明
- **2025-ONLY**：僅 2025 一季，非多球季驗證。
- **HISTORICAL / PAPER-ONLY**：全部數字皆為歷史回測結果，無真實下注、無資金部署。
- **ODDS PROVENANCE UNVERIFIED / NOT TRUE-PIT**：run line 讓分/賠率為賽後單快照。
- **NOT LIVE / NOT PRODUCTION**：無即時市場串接、無 production/DB/registry 變更。
- **NOT REAL BETTING / NOT A PROVEN EDGE**：無下注建議、無 EV/Kelly 宣稱。
- **NOT FUTURE PREDICTION**：所有評分場次皆為已完賽歷史場次。
- **NOT MULTI-SEASON VALIDATION**：本包僅涵蓋 2025 單一球季。
