# P276-A — Corrected 2025 Local MLB Retrain + Prediction Scorecard

> **僅本機歷史 / replay 描述性回測。** 非未來預測、非下注建議、無 EV/ROI/payout/Kelly/CLV、無 live 市場宣稱、無 production/DB/registry 變更、無發布、無 strategy activation。

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- descriptive backtest only; NO future prediction / hit-rate claim
- NO betting recommendation; NO EV/ROI/payout/Kelly/CLV claim
- NO live-market claim
- NO production / DB / registry mutation; NO real publication
- NO future-ticket mutation; NO strategy activation; NO leaderboard/evaluator change
- historical odds lack verified pregame timestamps (is_verified_real=False) — diagnostic/descriptive reference only; no verified betting edge

## 資料盤點
| file | usable | rows | outcome_labeled | role |
|---|---|--:|--:|---|
| mlb_odds_2025_real.csv | YES | 2430 | 2430 | evaluation universe (date-batched train+test); outcome derived from scores |
| mlb-2024-asplayed.csv | YES | 2429 | 2429 | date-batched Elo / rolling warm-up only (not scored) |
| mlb_odds_2025_real.csv [Home ML/Away ML] | REFERENCE_ONLY | 2428 | 0 | descriptive market reference (de-vig implied prob) |

## 完整日期訓練 / 測試切分（train 最後日 < test 最早日）
- 訓練期：`2025-03-18` → `2025-07-18`（1461 場 / 112 日）
- 測試期：`2025-07-19` → `2025-09-28`（969 場 / 72 日）
- requested train fraction: `0.600000`；effective: `0.601235`
- split strategy: `complete_date_boundary_nearest_requested_row_fraction`
- tie rule: `earlier boundary (smaller train partition) wins equal-distance ties`
- selected boundary: after `2025-07-18`; test starts `2025-07-19`
- 狀態合約：同一 game_date 全部預測使用同一 pre-date state；該日所有預測固定後才一次更新。
- Elo 暖身（前一季，僅 seed 狀態）：2429 場
- train 主場勝率先驗：`0.5496`；Platt(A,B)=(0.5264, 0.1270)
- odds 狀態：`PRESENT_BUT_TIMING_UNVERIFIED`；outcome 狀態：`AVAILABLE`

## 模型比較（測試期）
| model | train | test | accuracy | log_loss | brier_score | calibration_error | coverage |
|---|--:|--:|--:|--:|--:|--:|--:|
| baseline_fixed_prior | 1461 | 969 | 0.5325 | 0.6916 | 0.2492 | 0.0171 | 1.000 |
| elo_like_rating | 1461 | 969 | 0.5470 | 0.6911 | 0.2489 | 0.0503 | 1.000 |
| retrained_team_history_smooth | 1461 | 969 | 0.5635 | 0.6854 | 0.2461 | 0.0251 | 1.000 |
| calibrated_elo_recent_form | 1461 | 969 | 0.5418 | 0.6855 | 0.2463 | 0.0233 | 1.000 |
| _market_implied_devig(REFERENCE_UNVERIFIED)_ | — | 969 | 0.5459 | 0.6842 | 0.2456 | 0.0333 | 1.000 |

**最佳（Brier）**：`retrained_team_history_smooth`（市場行為 look-ahead，不列入排名）

## 最佳模型信心區間分佈（測試期）
| band | n | correct | hit_rate |
|---|--:|--:|--:|
| HIGH | 138 | 86 | 0.6232 |
| MEDIUM | 446 | 252 | 0.5650 |
| LOW | 385 | 208 | 0.5403 |

selected_side 分佈：`{'HOME': 637, 'AWAY': 332}`

## 解讀
- 準確率 53–57% / Brier ~0.246 為 MLB 純球隊強度模型的誠實可信區間；再往上需 game-specific（逐場投手/休息/陣容）資料。
- 校準（Platt）主要改善 calibration_error（ECE），對 Brier 提升有限。
- 歷史賠率沒有經驗證的賽前時間戳，僅作診斷/描述參考；命中率、EV 與 ROI 都不是經驗證的投注邊際。
