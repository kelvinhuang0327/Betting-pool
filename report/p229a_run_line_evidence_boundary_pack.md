# P229-A — Run Line Evidence Boundary Pack

> **僅本機歷史 / replay 描述性彙整。** 本檔不是新模型任務，只彙整 P226-A / P227-A / P228-A 既有結果；非未來預測、非下注建議、無 EV/Kelly 宣稱、無 live 市場宣稱、無 production/DB 變更、非已證實 edge。

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- descriptive synthesis of already-published P226-A / P227-A / P228-A results; NOT a new model, NOT a re-run, NOT a re-derivation
- NO betting recommendation; NO EV/Kelly claim; NOT a proven edge
- NO live-market claim; NOT production; NOT real betting
- NO future prediction; NO CLV claim; NO tradable-odds-edge claim
- P226-A / P227-A / P228-A source artifacts are read-only inputs and are not modified by this pack
- recommended next technical step is NOT authorized by this pack; a separate explicit Owner authorization is required before any further work begins

## 1. Evidence Inventory
### 1.1 P226-A Run Line baseline
- 測試期 `2025-07-18`→`2025-09-28`（972 場）
- coinflip baseline：accuracy=0.4568、brier=0.2500
- poisson_team_rate_model：accuracy=0.6008、brier=0.2395、ECE=0.0483

### 1.2 P228-A Split Robustness
- split-grid：3/3 嚴格勝出、3/3 不劣於容忍帶
| train_frac | test_period | poisson_accuracy | poisson_brier | beats_coinflip |
|--:|---|--:|--:|:--:|
| 0.5 | 2025-06-27→2025-09-28 | 0.6107 | 0.2382 | YES |
| 0.6 | 2025-07-18→2025-09-28 | 0.6008 | 0.2395 | YES |
| 0.7 | 2025-08-05→2025-09-28 | 0.6022 | 0.2380 | YES |

### 1.3 P228-A Monthly Robustness
- monthly windows：4/5 嚴格勝出、5/5 不劣於容忍帶（另有 2 個月因樣本不足被排除評分）
- P228-A 穩健性最終判定：`ROBUST_ENOUGH_FOR_FURTHER_HISTORICAL_RESEARCH`

### 1.4 P228-A Calibration
- train-fold-only Platt：raw brier=0.2395 → calibrated brier=0.2375（改善 Brier：`True`）
- raw ECE=0.0483 → calibrated ECE=0.0180（改善 ECE：`True`）

### 1.5 P227-A Total Limitation
- best_by_brier=`baseline_coinflip_50pct`；beats_coinflip_brier=`False`；beats_poisson_brier=`True`
- coinflip brier=0.2500；poisson accuracy=0.5022、brier=0.2637

## 2. What Is Supported
- Run Line signal is robust enough for further historical research (P228-A final label: `ROBUST_ENOUGH_FOR_FURTHER_HISTORICAL_RESEARCH`).
- Run Line is stronger than Total under the current historical, paper-only Poisson team-rate model family (Run Line beats the 0.5 coinflip Brier baseline; Total does not).
- Deterministic, test-covered local artifacts exist for P226-A and P228-A (reports + CSVs + passing pytest suites), so the reported figures are reproducible from tracked repo state.

## 3. What Is Not Supported
- NO real betting edge claim — all figures are descriptive historical backtest statistics, not a forward-looking edge claim.
- NO live readiness — no live market data transport exists or has been authorized for this line of work.
- NO production readiness — no DB / registry / production writes have occurred as part of P226-A / P227-A / P228-A / this pack.
- NO future prediction ability — all evaluated games are historical (already-played 2025 season games); no forward-looking game is scored.
- NO proof of tradable odds edge — no verified pregame odds price feed has been used; run line lines/prices are used for settlement and descriptive reference only, never as a model input feature.
- NO CLV evidence — the odds source (`mlb_odds_2025_real.csv`) is a post-game unverified snapshot (`is_verified_real=False`), not a point-in-time pregame capture, so no closing-line-value claim is possible.

## 4. Missing Evidence / Next Gates
- True point-in-time (PIT) odds with real capture timestamps (current data is a post-game unverified snapshot, not a pregame feed).
- Multi-season data, if locally available, to test cross-season robustness (current evidence is a single season, 2025, plus a 2024 warm-up-only set).
- Stronger data provenance / a verified-real odds source for run line settlement and any future market-reference use.
- Starter / lineup / injury point-in-time features, if made available later, to replace the current team-rate-only inputs.
- Final Owner decision before any future-output, live, or production work is attempted.

## 5. Recommended Next Technical Step
- 候選：**local multi-season data availability audit for Run Line**
- 其他候選（未擇定）：
  - feature-ablation scorecard for Run Line
  - true-PIT odds provenance audit
- 授權狀態：`NOT_AUTHORIZED_YET`
- This pack recommends but does not authorize the next step; a separate explicit Owner authorization is required before any further work begins.

## 免責聲明
- **HISTORICAL**：全部數字皆為歷史回測結果（引用自 P226-A/P227-A/P228-A 既有報告）。
- **PAPER-ONLY**：無真實下注、無資金部署。
- **NOT LIVE**：無即時市場串接。
- **NOT PRODUCTION**：無 production/DB/registry 變更、無發布。
- **NOT REAL BETTING**：無下注建議、無 EV/Kelly 宣稱。
- **NOT A PROVEN EDGE**：本報告不構成已證實的下注優勢宣稱，僅為描述性、可重現的歷史統計彙整，供後續研究與決策參考。
