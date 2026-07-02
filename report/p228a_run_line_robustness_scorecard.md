# P228-A — Run Line Robustness & Calibration Paper-Only Scorecard

> **僅本機歷史 / replay 描述性回測。** 非未來預測、非下注建議、無 EV/Kelly 宣稱、無 live 市場宣稱、無 production/DB 變更、非已證實 edge。

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- descriptive backtest only; NO future prediction / hit-rate claim
- NO betting recommendation; NO EV/Kelly claim; NOT a proven edge
- NO live-market claim; NOT production; NOT real betting
- chronological split grid and monthly windows are deterministic and no-shuffle; no random search was performed
- Platt calibration (a, b) is fit on the train fold ONLY; never fit on run line price, odds, or market-implied probability
- run line spread is used ONLY as event threshold / settlement; American odds prices are never read by this module
- push rows are excluded from accuracy/Brier/ECE denominators
- this MVP does not compute bootstrap confidence intervals; robustness is assessed via a pre-registered fixed Brier near-tie tolerance only

## Gate 0 — P226-A Run Line 重現
- 錨點 train_frac=`0.6`；訓練期 `2025-03-18`→`2025-07-18`（1458 場）；測試期 `2025-07-18`→`2025-09-28`（972 場）
- coinflip baseline：accuracy=0.4568、brier=0.2500
- poisson_team_rate_model：accuracy=0.6008、brier=0.2395、ECE=0.0483
- **Gate 0 狀態**：`GATE0_REPRODUCED_P226A_RUN_LINE_METRICS`

## 1. Chronological Split Grid（無 shuffle、預先設定）
| train_frac | train_rows | test_rows | test_period | coinflip_brier | poisson_accuracy | poisson_brier | poisson_ece | beats_coinflip | brier_margin |
|--:|--:|--:|---|--:|--:|--:|--:|:--:|--:|
| 0.5 | 1215 | 1215 | 2025-06-27→2025-09-28 | 0.2500 | 0.6107 | 0.2382 | 0.0414 | YES | 0.011765 |
| 0.6 | 1458 | 972 | 2025-07-18→2025-09-28 | 0.2500 | 0.6008 | 0.2395 | 0.0483 | YES | 0.010467 |
| 0.7 | 1701 | 729 | 2025-08-05→2025-09-28 | 0.2500 | 0.6022 | 0.2380 | 0.0412 | YES | 0.011973 |

## 2. Monthly Rolling Windows（擴展視窗 walk-forward，train>=300 場 / test>=20 場 才評分）
| window | status | train_rows | test_rows | home_adv | coinflip_brier | poisson_accuracy | poisson_brier | poisson_ece | beats_coinflip | brier_margin |
|---|---|--:|--:|--:|--:|--:|--:|--:|:--:|--:|
| 2025-03 | SKIPPED_INSUFFICIENT_TRAIN | 0 | 67 | — | — | — | — | — | — | — |
| 2025-04 | SKIPPED_INSUFFICIENT_TRAIN | 67 | 391 | — | — | — | — | — | — | — |
| 2025-05 | EVALUATED | 458 | 411 | 1.0442 | 0.2500 | 0.6472 | 0.2317 | 0.0601 | YES | 0.018301 |
| 2025-06 | EVALUATED | 869 | 397 | 1.0006 | 0.2500 | 0.5894 | 0.2503 | 0.1001 | no | -0.000308 |
| 2025-07 | EVALUATED | 1266 | 369 | 1.0078 | 0.2500 | 0.6314 | 0.2322 | 0.0454 | YES | 0.017767 |
| 2025-08 | EVALUATED | 1635 | 421 | 1.0171 | 0.2500 | 0.5748 | 0.2464 | 0.0596 | YES | 0.003633 |
| 2025-09 | EVALUATED | 2056 | 374 | 1.0271 | 0.2500 | 0.6310 | 0.2308 | 0.0455 | YES | 0.019197 |

## 3. Train-Fold-Only Platt Calibration（於 P226-A 預設 split 上）
- 擬合樣本（train fold 排除 push）：1458 場（train fold 共 1458 場）
- 凍結係數：`a=0.665413`、`b=-0.025904`
| | accuracy | brier_score | calibration_error(ECE) | decided_count |
|---|--:|--:|--:|--:|
| raw (P226-A Poisson) | 0.6008 | 0.2395 | 0.0483 | 972 |
| calibrated (Platt) | 0.6060 | 0.2375 | 0.0180 | 972 |

**校準是否改善 Brier**：`True`　**校準是否改善 ECE**：`True`

### Reliability Diagnostics（10 bins，凍結預測後計算）
| bin | n(raw) | mean_pred(raw) | empirical(raw) | gap(raw) | n(cal) | mean_pred(cal) | empirical(cal) | gap(cal) |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| [0.0,0.1) | 0 | — | — | — | 0 | — | — | — |
| [0.1,0.2) | 14 | 0.1816 | 0.3571 | 0.1755 | 0 | — | — | — |
| [0.2,0.3) | 146 | 0.2621 | 0.3151 | 0.0530 | 28 | 0.2758 | 0.3571 | 0.0814 |
| [0.3,0.4) | 264 | 0.3454 | 0.4015 | 0.0561 | 320 | 0.3602 | 0.3625 | 0.0023 |
| [0.4,0.5) | 180 | 0.4492 | 0.4167 | 0.0325 | 271 | 0.4482 | 0.4096 | 0.0386 |
| [0.5,0.6) | 161 | 0.5515 | 0.5217 | 0.0298 | 234 | 0.5498 | 0.5470 | 0.0027 |
| [0.6,0.7) | 144 | 0.6470 | 0.6111 | 0.0359 | 114 | 0.6320 | 0.6579 | 0.0259 |
| [0.7,0.8) | 59 | 0.7255 | 0.6271 | 0.0984 | 5 | 0.7214 | 0.8000 | 0.0786 |
| [0.8,0.9) | 4 | 0.8174 | 0.7500 | 0.0674 | 0 | — | — | — |
| [0.9,1.0) | 0 | — | — | — | 0 | — | — | — |

## 4. 穩健性結論
- 判定規則（預先設定、非依結果調整）：Brier near-tie 容忍帶＝`0.005`；ROBUST 需「所有 split-grid 與所有已評分月度窗皆不劣於 coinflip 超過容忍帶」且「多數（split+window 合計）為嚴格勝出」；否則若嚴格勝出仍佔多數則為 MIXED/SPLIT-SPECIFIC；否則 NOT ROBUST。
- split-grid：3/3 嚴格勝出、3/3 不劣於容忍帶
- monthly windows：4/5 嚴格勝出、5/5 不劣於容忍帶（另有 2 個月因樣本不足被排除評分）
- **最終判定**：`ROBUST_ENOUGH_FOR_FURTHER_HISTORICAL_RESEARCH`

## 限制
- 本 MVP 未計算 bootstrap 信賴區間；穩健性僅以固定容忍帶＋split/window 計數判定，非嚴格統計檢定。
- 月度視窗樣本數隨賽季推進而增長（train fold 為擴展視窗），越早的月份 train fold 越薄、估計越不穩定，已用 `MIN_TRAIN_ROWS_FOR_WINDOW=300` 排除過薄的月份（2025-03/04 因此被排除）。
- Platt 校準只在 P226-A 預設 60/40 split 上驗證，未對 split-grid 每個切分重跑校準。
- 單一球季（2025）＋暖身季（2024）資料，跨球季穩健性未經檢驗。

## 免責聲明
- **HISTORICAL**：全部數字皆為歷史回測結果。
- **PAPER-ONLY**：無真實下注、無資金部署。
- **NOT LIVE**：無即時市場串接。
- **NOT PRODUCTION**：無 production/DB/registry 變更、無發布。
- **NOT REAL BETTING**：無下注建議、無 EV/Kelly 宣稱。
- **NOT A PROVEN EDGE**：本報告不構成已證實的下注優勢宣稱，僅為描述性、可重現的歷史統計分析，供後續研究參考。
