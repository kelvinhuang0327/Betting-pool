# 2026 WBC 深度對決分析：Puerto Rico (PUR) vs Italy (ITA)

## 📊 核心實力指標 (Left vs Right)

| 指標 | Puerto Rico (PUR) | Italy (ITA) | 差異 |
|---|---:|---:|---:|
| 台灣比賽日期 | 2026-03-15 | 2026-03-15 | 同日 |
| 預賽戰績 | 3-1 | 4-0 | ITA 優勢 |
| 場均得分 (RS/G) | 3.75 | 8.00 | ITA +4.25 |
| 場均失分 (RA/G) | 1.75 | 2.75 | ITA +1.00 |
| 得失分差/場 (RD/G) | +2.00 | +5.25 | ITA +3.25 |
| OPS+ | 無資料 | 無資料 | 無資料 |
| FIP- | 無資料 | 無資料 | 無資料 |
| K-BB% | 無資料 | 無資料 | 無資料 |
| DER | 無資料 | 無資料 | 無資料 |
| Elo | 無資料 | 無資料 | 無資料 |

## 🧢 關鍵投打對決模擬 (Matchup Depth)

| 項目 | Puerto Rico (PUR) | Italy (ITA) |
|---|---|---|
| 台灣比賽日期 | 2026-03-15 | 2026-03-15 |
| 官方 probable starter | Seth Lugo (ERA 4.15 | WHIP 1.29 | K/9 7.74 | BB/9 3.41) | 官方 feed 尚未列出 |
| 先發資料來源 | https://statsapi.mlb.com/api/v1.1/game/788098/feed/live | https://statsapi.mlb.com/api/v1.1/game/788098/feed/live |
| 先發品質分數 | -0.117 | +0.000 |
| 牛棚深度可驗證資料 | 無資料 | 無資料 |
| 專項對戰加權資料 | 無資料 | 無資料 |

## 🎯 比分機率分佈 (Poisson 回歸)

資料來源：
- 官方完賽資料：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_2026_live_scores.json`
- 模型設定：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/model_artifacts.json`

回歸參數：
- 基礎 `lambda_PUR = 3.25`
- 基礎 `lambda_ITA = 4.88`
- 先發修正後 `lambda_PUR = 3.25`
- 先發修正後 `lambda_ITA = 4.92`
- Quarter-Final 先發權重：`0.65`
- 特定對戰加權：`官方 probable starters + 保守先發抑分修正`

機率結果：
- PUR 9 局勝率：`0.2217`
- ITA 9 局勝率：`0.6574`
- 9 局平手率：`0.1210`
- 全場 PUR 勝率（平手 50/50）：`0.2821`
- 全場 ITA 勝率（平手 50/50）：`0.7179`

## 🗺️ 得分機率矩陣圖

- 矩陣 CSV：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-15_PUR_ITA_poisson_matrix.csv`
- 矩陣摘要：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-15_PUR_ITA_poisson_summary.json`

ASCII 熱度圖（PUR 為列，ITA 為欄）：

```text
       + 01234567890
PUR 10 |            
PUR  9 |            
PUR  8 |            
PUR  7 |     ..     
PUR  6 |   .::::.   
PUR  5 |   :-==-:.  
PUR  4 |  .-+##+=:. 
PUR  3 |  .=#@%#+-. 
PUR  2 |  .=*%%*=:. 
PUR  1 |  .:=++=:.  
PUR  0 |    ....    
```

## 💰 台灣運彩 EV 檢查

- 台灣運彩目前賠率：`無資料`
- EV：`無資料`
- 結論：`無資料`

## ⚠️ 風險提醒

- `model_artifacts.json` 未提供各隊權重欄位，該部分為 `無資料`。
- 先發與牛棚若臨場異動，lambda 與勝率會快速變化。
- 若盤口補齊，可立即改算 EV 與 Kelly 倉位。
