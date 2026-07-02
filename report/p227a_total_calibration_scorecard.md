# P227-A — Total Over-Dispersion Calibration (Paper-Only MVP)

> **僅本機歷史 / replay 描述性回測。** 非未來預測、非下注建議、無 EV/Kelly 宣稱、無 live 市場宣稱、無 production/DB 變更、非已證實 edge。

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- descriptive backtest only; NO future prediction / hit-rate claim
- NO betting recommendation; NO EV/Kelly claim; NOT a proven edge
- NO live-market claim; NOT production; NOT real betting
- phi_hat and Platt (a,b) are fit on the train fold ONLY; never fit on O/U line, odds, or market-implied probability
- O/U line values are used ONLY as event threshold / settlement / evaluation; American odds prices are never read by this module
- push rows are excluded from accuracy/Brier/ECE denominators and from the Platt fit; push_count/push_rate reported separately

## Gate 0 — P226-A 重現
- train_frac=0.6；訓練期 `2025-03-18`→`2025-07-18`（1458 場）；測試期 `2025-07-18`→`2025-09-28`（972 場）
- home_adv（P226-A train-only 校準，逐場交叉核對相符）：`1.0116`
- Total baseline_coinflip_50pct：accuracy=0.4956、brier=0.2500
- Total poisson_team_rate_model：accuracy=0.5022、brier=0.2637、ECE=0.0959、decided=918、push=54
- Run line poisson_team_rate_model（未變動，僅回歸檢查）：accuracy=0.6008、brier=0.2395

## Method A — Variance Inflation / Dispersion Scaling
- `phi_hat`（train fold 1458 場，不含 O/U 線輸入）：`2.366514`
- 預測：常態近似 mu=lambda_total、variance=phi_hat*lambda_total、`Phi` 以 `math.erf` 實作；整數線用連續性校正並保留 p_over+p_under+p_push=1。

## Method B — Platt / Logistic Calibration
- 擬合樣本（train fold 排除 push）：1402 場
- 凍結係數：`a=-0.022772`、`b=-0.109014`
- 輸入：P226-A raw Poisson `p_over` 的 logit；輸出套用於 test fold raw p_over；push 機率沿用 P226-A 原始 Poisson 輸出（Platt 只重新校準條件式 over/under 分配）。

## 校準手臂比較（測試期，Total 市場）
| model | decided | push | accuracy | log_loss | brier_score | calibration_error |
|---|--:|--:|--:|--:|--:|--:|
| baseline_coinflip_50pct | 918 | 54 | 0.4956 | 0.6931 | 0.2500 | 0.0044 |
| poisson_team_rate_model | 918 | 54 | 0.5022 | 0.7231 | 0.2637 | 0.0959 |
| variance_inflation_normal | 918 | 54 | 0.4913 | 0.7060 | 0.2562 | 0.0752 |
| platt_logistic_calibration | 918 | 54 | 0.5044 | 0.6987 | 0.2528 | 0.0510 |

**最佳（Brier）**：`baseline_coinflip_50pct`
**是否優於 P226-A Poisson Brier 0.2637**：`True`
**是否優於 coinflip baseline Brier 0.2500**：`False`

## 結論
- 校準手臂修復了 P226-A Poisson 模型「輸給 coinflip」的問題（Brier 較 poisson_team_rate_model 改善），但測試期 Brier 仍未優於 0.5 coinflip baseline（0.2500）。誠實結論：over-dispersion 校準有幫助但尚不足以構成有效預測能力。
- 本報告為本機歷史 paper-only 回測，非未來預測、非下注建議、非 production/live、非已證實下注優勢。
