# 2026 WBC 深度對決分析：United States (USA) vs Canada (CAN)

## 📊 核心實力指標 (Left vs Right)

| 指標 | United States (USA) | Canada (CAN) | 差異 |
|---|---:|---:|---:|
| 台灣比賽日期 | 2026-03-14 | 2026-03-14 | 同日 |
| 預賽戰績 | 4-1 | 3-2 | USA 優勢 |
| 場均得分 (RS/G) | 8.00 | 4.80 | CAN -3.20 |
| 場均失分 (RA/G) | 4.00 | 3.00 | CAN -1.00 |
| 得失分差/場 (RD/G) | +4.00 | +1.80 | CAN -2.20 |
| OPS+ | 無資料 | 無資料 | 無資料 |
| FIP- | 無資料 | 無資料 | 無資料 |
| K-BB% | 無資料 | 無資料 | 無資料 |
| DER | 無資料 | 無資料 | 無資料 |
| Elo | 無資料 | 無資料 | 無資料 |

## 🧢 關鍵投打對決模擬 (Matchup Depth)

| 項目 | United States (USA) | Canada (CAN) |
|---|---|---|
| 台灣比賽日期 | 2026-03-14 | 2026-03-14 |
| 官方 probable starter | Logan Webb (ERA 3.22 | WHIP 1.24 | K/9 9.74 | BB/9 2.00) | Michael Soroka (ERA 4.52 | WHIP 1.13 | K/9 9.54 | BB/9 2.91) |
| 先發資料來源 | https://statsapi.mlb.com/api/v1.1/game/788100/feed/live | https://statsapi.mlb.com/api/v1.1/game/788100/feed/live |
| 先發品質分數 | +0.389 | +0.105 |
| 牛棚深度可驗證資料 | 無資料 | 無資料 |
| 專項對戰加權資料 | 無資料 | 無資料 |

## 🎯 比分機率分佈 (Poisson 回歸)

資料來源：
- 官方完賽資料：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_2026_live_scores.json`
- 模型設定：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/model_artifacts.json`

回歸參數：
- 基礎 `lambda_USA = 5.50`
- 基礎 `lambda_CAN = 4.40`
- 先發修正後 `lambda_USA = 5.45`
- 先發修正後 `lambda_CAN = 4.27`
- Quarter-Final 先發權重：`0.65`
- 特定對戰加權：`官方 probable starters + 保守先發抑分修正`

機率結果：
- USA 9 局勝率：`0.5849`
- CAN 9 局勝率：`0.2935`
- 9 局平手率：`0.1216`
- 全場 USA 勝率（平手 50/50）：`0.6457`
- 全場 CAN 勝率（平手 50/50）：`0.3543`

## 🗺️ 得分機率矩陣圖

- 矩陣 CSV：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-14_USA_CAN_poisson_matrix.csv`
- 矩陣摘要：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-14_USA_CAN_poisson_summary.json`

ASCII 熱度圖（USA 為列，CAN 為欄）：

```text
       + 01234567890
USA 10 |    ...     
USA  9 |   .:::.    
USA  8 |  .:==-:.   
USA  7 |  .=+*+-:.  
USA  6 |  :+#%*=-.  
USA  5 |  :+%@#+-.  
USA  4 |  :+#%#+-.  
USA  3 |  .-+*+-:.  
USA  2 |  .:--::.   
USA  1 |    ...     
USA  0 |            
```

## 💰 台灣運彩 EV 檢查

- 台灣運彩目前賠率：`無資料`
- EV：`無資料`
- 結論：`無資料`

## ⚠️ 風險提醒

- `model_artifacts.json` 未提供各隊權重欄位，該部分為 `無資料`。
- 先發與牛棚若臨場異動，lambda 與勝率會快速變化。
- 若盤口補齊，可立即改算 EV 與 Kelly 倉位。
