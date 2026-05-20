# 2026 WBC 深度對決分析：United States (USA) vs Canada (CAN)

## 📊 核心實力指標 (Left vs Right)

| 指標 | United States (USA) | Canada (CAN) | 差異 |
|---|---:|---:|---:|
| 台灣比賽日期 | 2026-03-14 | 2026-03-14 | 同日 |
| 預賽戰績 | 3-1 | 3-1 | USA 優勢 |
| 場均得分 (RS/G) | 8.75 | 5.25 | CAN -3.50 |
| 場均失分 (RA/G) | 4.25 | 2.50 | CAN -1.75 |
| 得失分差/場 (RD/G) | +4.50 | +2.75 | CAN -1.75 |
| OPS+ | 無資料 | 無資料 | 無資料 |
| FIP- | 無資料 | 無資料 | 無資料 |
| K-BB% | 無資料 | 無資料 | 無資料 |
| DER | 無資料 | 無資料 | 無資料 |
| Elo | 無資料 | 無資料 | 無資料 |

## 🧢 關鍵投打對決模擬 (Matchup Depth)

| 項目 | United States (USA) | Canada (CAN) |
|---|---|---|
| 台灣比賽日期 | 2026-03-14 | 2026-03-14 |
| 先發投手預估 | 無資料 | 無資料 |
| 先發投手球種/球速可驗證資料 | 無資料 | 無資料 |
| 牛棚深度可驗證資料 | 無資料 | 無資料 |
| 專項對戰加權資料 | 無資料 | 無資料 |

## 🎯 比分機率分佈 (Poisson 回歸)

資料來源：
- 官方完賽資料：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_2026_live_scores.json`
- 模型設定：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/model_artifacts.json`

回歸參數：
- `lambda_USA = 5.62`
- `lambda_CAN = 4.75`
- 特定對戰加權：`無資料`（無可驗證拆分資料）

機率結果：
- USA 9 局勝率：`0.5436`
- CAN 9 局勝率：`0.3345`
- 9 局平手率：`0.1219`
- 全場 USA 勝率（平手 50/50）：`0.6045`
- 全場 CAN 勝率（平手 50/50）：`0.3955`

## 🗺️ 得分機率矩陣圖

- 矩陣 CSV：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-14_USA_CAN_poisson_matrix.csv`
- 矩陣摘要：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-14_USA_CAN_poisson_summary.json`

ASCII 熱度圖（USA 為列，CAN 為欄）：

```text
       + 01234567890
USA 10 |    ....    
USA  9 |   .::::.   
USA  8 |  .:===-:.  
USA  7 |  .-+**+-:. 
USA  6 |  .=#%%*=:. 
USA  5 |  :=#@%*=:. 
USA  4 |  .=*##*=:. 
USA  3 |  .-=++=:.  
USA  2 |   .:-::.   
USA  1 |     ..     
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
