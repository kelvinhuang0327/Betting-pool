# P207-A — Local MLB Retrain + Prediction Scorecard

> **僅本機歷史 / replay 描述性回測。** 非未來預測、非下注建議、無 EV/ROI/payout/Kelly/CLV、無 live 市場宣稱、無 production/DB/registry 變更、無發布、無 strategy activation。

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- descriptive backtest only; NO future prediction / hit-rate claim
- NO betting recommendation; NO EV/ROI/payout/Kelly/CLV claim
- NO live-market claim
- NO production / DB / registry mutation; NO real publication
- NO future-ticket mutation; NO strategy activation; NO leaderboard/evaluator change
- odds fields are post-game unverified snapshot (is_verified_real=False) — reference only

## 資料盤點
| file | usable | rows | outcome_labeled | role |
|---|---|--:|--:|---|
| mlb_odds_2025_real.csv | YES | 2430 | 2430 | evaluation universe (walk-forward train+test); outcome derived from scores |
| mlb-2024-asplayed.csv | YES | 2429 | 2429 | Elo / rolling warm-up only (not scored) |
| mlb_odds_2025_real.csv [Home ML/Away ML] | REFERENCE_ONLY | 2428 | 0 | descriptive market reference (de-vig implied prob) |

## 訓練 / 測試切分（嚴格時間序，train 期 < test 期）
- 訓練期：`2025-03-18` → `2025-07-18`（1458 場）
- 測試期：`2025-07-18` → `2025-09-28`（972 場）
- Elo 暖身（前一季，僅 seed 狀態）：2429 場
- train 主場勝率先驗：`0.5494`；Platt(A,B)=(0.5203, 0.1266)
- odds 狀態：`PRESENT_BUT_TIMING_UNVERIFIED`；outcome 狀態：`AVAILABLE`

## 模型比較（測試期）
| model | train | test | accuracy | log_loss | brier_score | calibration_error | coverage |
|---|--:|--:|--:|--:|--:|--:|--:|
| baseline_fixed_prior | 1458 | 972 | 0.5329 | 0.6915 | 0.2492 | 0.0165 | 1.000 |
| elo_like_rating | 1458 | 972 | 0.5484 | 0.6904 | 0.2486 | 0.0488 | 1.000 |
| retrained_team_history_smooth | 1458 | 972 | 0.5638 | 0.6852 | 0.2461 | 0.0248 | 1.000 |
| calibrated_elo_recent_form | 1458 | 972 | 0.5442 | 0.6851 | 0.2460 | 0.0202 | 1.000 |
| _market_implied_devig(REFERENCE_UNVERIFIED)_ | — | 972 | 0.5473 | 0.6839 | 0.2455 | 0.0318 | 1.000 |

**最佳（Brier）**：`calibrated_elo_recent_form`（市場行為 look-ahead，不列入排名）

## 最佳模型信心區間分佈（測試期）
| band | n | correct | hit_rate |
|---|--:|--:|--:|
| HIGH | 32 | 23 | 0.7188 |
| MEDIUM | 498 | 285 | 0.5723 |
| LOW | 442 | 221 | 0.5000 |

selected_side 分佈：`{'HOME': 767, 'AWAY': 205}`

## 解讀
- 準確率 53–57% / Brier ~0.246 為 MLB 純球隊強度模型的誠實可信區間；再往上需 game-specific（逐場投手/休息/陣容）資料。
- 校準（Platt）主要改善 calibration_error（ECE），對 Brier 提升有限。
- 市場隱含機率為賽後快照，屬 look-ahead，僅作參考、不可視為賽前預測能力。
