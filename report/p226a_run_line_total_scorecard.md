# P226-A — Run Line / Total Probability Model + Paper Backtest

> **僅本機歷史 / replay 描述性回測。** 非未來預測、非下注建議、無 EV/Kelly 宣稱（paper ROI 為描述性回測統計，非前瞻 edge 宣稱）、無 live 市場宣稱、無 production/DB/registry 變更、無發布、無 strategy activation。

## 範疇聲明
- LOCAL HISTORICAL / REPLAY BACKTEST ONLY
- descriptive backtest only; NO future prediction / hit-rate claim
- NO betting recommendation; NO EV/Kelly claim; paper ROI is a descriptive backtest statistic only, NOT a forward-looking edge claim
- NO live-market claim
- NO production / DB / registry mutation; NO real publication
- NO future-ticket mutation; NO strategy activation; NO leaderboard/evaluator change
- run line / total lines and prices are post-game unverified snapshot (is_verified_real=False) — settlement / paper-ROI reference only, NOT a pregame feed, NOT a CLV claim, NEVER used as a model input feature
- push rows are excluded from accuracy/Brier denominators and from the paper ROI staked base (stake returned, zero net); push_count/push_rate reported separately

## 資料盤點
| file | usable | rows | outcome_labeled | role |
|---|---|--:|--:|---|
| mlb_odds_2025_real.csv | YES | 2430 | 2430 | evaluation universe (walk-forward train+test); scores + RL/O-U lines same row |
| mlb-2024-asplayed.csv | YES | 2429 | 2429 | team runs-for/runs-against rolling rate warm-up only (not scored) |
| mlb_odds_2025_real.csv [Home RL Spread / RL Home / RL Away] | SETTLEMENT_AND_REFERENCE_ONLY | 972 | 0 | run line settlement + descriptive market reference (de-vig implied prob) |
| mlb_odds_2025_real.csv [O/U / Over / Under] | SETTLEMENT_AND_REFERENCE_ONLY | 972 | 0 | total settlement + descriptive market reference (de-vig implied prob) |

## 訓練 / 測試切分（嚴格時間序，train 期 < test 期）
- 訓練期：`2025-03-18` → `2025-07-18`（1458 場）
- 測試期：`2025-07-18` → `2025-09-28`（972 場）
- 球隊得失分率暖身（前一季，僅 seed 狀態）：2429 場
- home_adv（train-only 收盤形式比例校準）：`1.0116`

## Run Line 市場比較（測試期）
| model | decided | push | push_rate | accuracy | log_loss | brier_score | calibration_error | paper_roi | paper_net_units |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| baseline_coinflip_50pct | 972 | 0 | 0.000 | 0.4568 | 0.6931 | 0.2500 | 0.0432 | -0.0654 | -63.61 |
| poisson_team_rate_model | 972 | 0 | 0.000 | 0.6008 | 0.6731 | 0.2395 | 0.0483 | -0.0101 | -9.82 |
| _market_implied_devig(REFERENCE_UNVERIFIED)_ | 972 | 0 | — | 0.6152 | 0.6646 | 0.2359 | 0.0301 | — | — |

**最佳（Brier）**：`poisson_team_rate_model`

## Total 市場比較（測試期）
| model | decided | push | push_rate | accuracy | log_loss | brier_score | calibration_error | paper_roi | paper_net_units |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| baseline_coinflip_50pct | 918 | 54 | 0.056 | 0.4956 | 0.6931 | 0.2500 | 0.0044 | -0.0520 | -47.75 |
| poisson_team_rate_model | 918 | 54 | 0.056 | 0.5022 | 0.7231 | 0.2637 | 0.0959 | -0.0388 | -35.59 |
| _market_implied_devig(REFERENCE_UNVERIFIED)_ | 918 | 54 | — | 0.4869 | 0.6941 | 0.2505 | 0.0264 | — | — |

**最佳（Brier）**：`baseline_coinflip_50pct`

## 解讀
- run line / total 的盤口線值與美式賠率僅用於 settlement 與 paper ROI，從未進入模型輸入特徵（PIT-safe）。
- push 列（total 整數線常見，佔比可觀）已排除於 accuracy/Brier/ROI 分母，另計 push_rate。
- 市場隱含機率（`market_implied_devig(REFERENCE_UNVERIFIED)`）為賽後快照，屬 look-ahead，僅作參考、不可視為賽前預測能力、不列入最佳模型排名。
- paper ROI 為本機歷史回測統計量，NOT 前瞻 edge / EV / Kelly 宣稱。
- **Run line 上 Poisson 模型明顯優於 50% coinflip baseline**（實測約 60% vs 46%、Brier 明顯較低），顯示 D=home-away 的 Skellam 分布形狀＋home_adv 校準抓到了讓分盤結構性的資訊。
- **Total 上 Poisson 模型反而不如 baseline**（Brier 高於 0.25 的常數下限）：實測預測總分均值與實際均值相近，但實際 total runs 變異數遠大於獨立 Poisson 假設隱含的變異數（over-dispersion，如大比分/延長賽等肥尾事件），導致模型機率過度自信、Brier 反而變差。這是純球隊得失分率模型在 total 市場上誠實的已知限制，不是程式錯誤；若要改善需要能捕捉變異數的模型（如 Negative Binomial）或投手/牛棚層級資料，非本任務範疇。
