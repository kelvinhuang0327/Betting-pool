# P112 Lane A 市場合約對齊差距診斷報告 (2026-05-31)

本報告針對 Lane A（台灣運彩 MLB 市場）進行 outcome-only pipeline 與合約要求的對齊差距診斷，僅限於 diagnostic-only，無任何 production、推薦、賠率、EV、Kelly、CLV、下注等邏輯。

## 合約市場類型與差距總結

| 市場類型             | 合約要求欄位                        | pipeline 欄位                        | 策略覆蓋         | 差距類型             | 備註                                   |
|----------------------|-------------------------------------|--------------------------------------|------------------|----------------------|----------------------------------------|
| moneyline            | game_id, predicted_side, source_trace, odds | game_id, predicted_side, source_prediction_version | HIGH_FIP, MID_FIP, LOW_FIP | 缺少 odds           | outcome-only pipeline 不產生 odds，無法對齊合約要求 |
| run_line             | game_id, predicted_side, source_trace, odds | (無)                                 | (無)             | 市場未覆蓋           | run_line 市場 outcome-only pipeline 未覆蓋           |
| total_runs           | game_id, predicted_side, source_trace, odds | (無)                                 | (無)             | 市場未覆蓋           | total_runs 市場 outcome-only pipeline 未覆蓋         |
| first_five_innings   | game_id, predicted_side, source_trace, odds | (無)                                 | (無)             | 市場未覆蓋           | first_five_innings 市場 outcome-only pipeline 未覆蓋 |

## Governance Flag
- paper_only: true
- diagnostic_only: true
- production_ready: false
- real_bet_allowed: false
- recommendation_allowed: false
- odds_used: false
- ev_computed: false
- clv_computed: false
- kelly_computed: false
- stake_sizing: false

## 結論
本診斷僅供合約 gap review，嚴格禁止任何 production、推薦、賠率、EV、Kelly、CLV、下注等行為。所有差距均已明確標註，後續如需對齊合約，需另行設計 production-ready pipeline。
