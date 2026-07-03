# P232-A — 2025 Single-Season Run Line Feature Ablation Scorecard

> **單一球季（2025-only）、僅本機歷史 / replay 描述性回測、run line 讓分/賠率來源未經驗證（provenance-unverified）。** 非未來預測、非下注建議、無 EV/Kelly 宣稱、無 live 市場宣稱、無 production/DB/registry 變更、非已證實 edge、非跨球季驗證。

## 範疇聲明
- SINGLE-SEASON: 2025 only; NOT a multi-season validation (multi-season expansion remains HOLD per P230-A/P231-F5A)
- 2025-ONLY: evaluation universe is data/mlb_2025/mlb_odds_2025_real.csv (2025 season) only
- HISTORICAL PAPER-ONLY: local historical / replay descriptive backtest; NO future prediction / hit-rate claim
- PROVENANCE-UNVERIFIED: run line spread/prices are a post-game unverified snapshot (is_verified_real=False); settlement / event-threshold reference only, NEVER a model input feature
- NOT LIVE: NO live-market claim; no real-time provider access
- NOT PRODUCTION: NO production / DB / registry mutation; NO publication
- NOT REAL BETTING: NO betting recommendation; NO EV/Kelly claim
- NOT A PROVEN EDGE: descriptive feature-ablation research artifact only, not a validated betting edge
- this is a feature-ablation study of the EXISTING P226-A/P228-A model architecture; it does not add, retrain, or search over new features

## Gate 0 — P226-A / P228-A Run Line 重現
- 錨點 train_frac=`0.6`；訓練期 `2025-03-18`→`2025-07-18`（1458 場）；測試期 `2025-07-18`→`2025-09-28`（972 場）
- coinflip baseline：accuracy=0.4568、brier=0.2500
- poisson_team_rate_model（full_model）：accuracy=0.6008、brier=0.2395、ECE=0.0483
- train-fold-only Platt calibrated：brier=0.2375
- **Gate 0 校準狀態**：`GATE0_REPRODUCED_P228A_CALIBRATED_BRIER`
- **Gate 0 狀態**：`GATE0_REPRODUCED_P226A_RUN_LINE_METRICS`

## 消融特徵群組
| variant | note |
|---|---|
| full_model | control; identical feature set to P226-A poisson_team_rate_model (offense rate + defense rate + home_adv, all present) |
| ablate_offense_rate | rolling run-scoring (offense) rate replaced by league-average runs for both teams; defense rate and home_adv unchanged |
| ablate_defense_rate | rolling run-allowing (defense) rate replaced by league-average runs for both teams; offense rate and home_adv unchanged |
| ablate_team_strength_both | closest local analog to an 'Elo / team strength' ablation: both offense and defense rates replaced by league-average runs for both teams (only home_adv still differentiates home from away lambda) |
| ablate_home_field | home_adv fixed at 1.0 (no home-field calibration applied); offense/defense rates unchanged |

### 不適用的建議特徵群組（本模型未使用）
| group | status | note |
|---|---|---|
| rest_days | NOT_PRESENT_IN_BASELINE_MODEL | P226-A/P228-A poisson_team_rate_model has no rest-day input; there is no rest-day feature in this model to ablate. |
| rsi_streak_recent_form | NOT_PRESENT_IN_BASELINE_MODEL | P226-A/P228-A poisson_team_rate_model uses a shrinkage-smoothed rolling run rate, not an RSI or win/loss streak feature; there is no separate RSI/streak input in this model to ablate. |

## 消融結果（chronological split grid：0.5 / 0.6 / 0.7）
| variant | train_frac | test(decided) | accuracy | brier | ECE | delta_brier_vs_full | beats_coinflip | not_worse_tol |
|---|--:|--:|--:|--:|--:|--:|:--:|:--:|
| full_model | 0.5 | 1215 | 0.6107 | 0.2382 | 0.0414 | 0.000000 | YES | YES |
| ablate_offense_rate | 0.5 | 1215 | 0.6173 | 0.2388 | 0.0530 | 0.000599 | YES | YES |
| ablate_defense_rate | 0.5 | 1215 | 0.6132 | 0.2415 | 0.0584 | 0.003218 | YES | YES |
| ablate_team_strength_both | 0.5 | 1215 | 0.6099 | 0.2456 | 0.0883 | 0.007411 | YES | YES |
| ablate_home_field | 0.5 | 1215 | 0.6115 | 0.2382 | 0.0400 | -0.000029 | YES | YES |
| full_model | 0.6 | 972 | 0.6008 | 0.2395 | 0.0483 | 0.000000 | YES | YES |
| ablate_offense_rate | 0.6 | 972 | 0.6111 | 0.2403 | 0.0537 | 0.000811 | YES | YES |
| ablate_defense_rate | 0.6 | 972 | 0.6029 | 0.2441 | 0.0668 | 0.004518 | YES | YES |
| ablate_team_strength_both | 0.6 | 972 | 0.6008 | 0.2488 | 0.0935 | 0.009276 | YES | YES |
| ablate_home_field | 0.6 | 972 | 0.6060 | 0.2396 | 0.0479 | 0.000056 | YES | YES |
| full_model | 0.7 | 729 | 0.6022 | 0.2380 | 0.0412 | 0.000000 | YES | YES |
| ablate_offense_rate | 0.7 | 729 | 0.6077 | 0.2408 | 0.0500 | 0.002816 | YES | YES |
| ablate_defense_rate | 0.7 | 729 | 0.5967 | 0.2436 | 0.0652 | 0.005585 | YES | YES |
| ablate_team_strength_both | 0.7 | 729 | 0.5953 | 0.2509 | 0.0977 | 0.012864 | no | YES |
| ablate_home_field | 0.7 | 729 | 0.6036 | 0.2380 | 0.0455 | 0.000001 | YES | YES |

## 解讀
- 判定規則（預先設定、非依結果調整）：某 variant 在全部 split grid 上皆嚴格優於 coinflip（brier < coinflip_brier）視為「訊號存活」；全部 variant 皆存活→`SIGNAL_PERSISTS_ACROSS_ABLATIONS`；全部 variant 皆不存活→`SIGNAL_COLLAPSES_UNDER_ABLATION`；部分存活部分不存活→`SIGNAL_DEPENDS_ON_FRAGILE_FEATURE_GROUP`；其餘情況→`INCONCLUSIVE`。
- robust_variants（全部 split 皆存活）：['ablate_offense_rate', 'ablate_defense_rate', 'ablate_home_field']
- fragile_variants（至少一個 split 劣於 coinflip 超過容忍帶）：（無）
- **最終判定**：`SIGNAL_DEPENDS_ON_FRAGILE_FEATURE_GROUP`

## 限制
- **SINGLE-SEASON ONLY**：本研究僅使用 2025 一個球季；不構成跨球季穩健性宣稱，多球季擴充仍為 HOLD（P230-A/P231-F5A）。
- 本模型（poisson_team_rate_model）本身沒有 Elo、休息天數、RSI/streak 特徵；`ablate_team_strength_both` 是「Elo/team strength」建議消融群組在本模型的最接近本機對應，並非真正的 Elo 特徵消融。
- run line 讓分/賠率的來源未經驗證（is_verified_real=False、賽後單快照），沿用 P226-A/P228-A/P230-A 已記載的已知限制；本檔僅將讓分值作為 settlement 門檻使用，從未作為模型輸入特徵。
- 本檔未計算 bootstrap 信賴區間；訊號存活判定僅以固定容忍帶＋split grid 計數判定，非嚴格統計檢定。

## 免責聲明
- **SINGLE-SEASON / 2025-ONLY**：僅 2025 一季，非多球季驗證。
- **HISTORICAL / PAPER-ONLY**：全部數字皆為歷史回測結果，無真實下注、無資金部署。
- **PROVENANCE-UNVERIFIED**：run line 讓分/賠率為賽後單快照，非賽前 PIT 資料。
- **NOT LIVE / NOT PRODUCTION**：無即時市場串接、無 production/DB/registry 變更。
- **NOT REAL BETTING**：無下注建議、無 EV/Kelly 宣稱。
- **NOT A PROVEN EDGE**：本報告不構成已證實的下注優勢宣稱，僅為描述性、可重現的特徵消融研究，供後續研究參考。
