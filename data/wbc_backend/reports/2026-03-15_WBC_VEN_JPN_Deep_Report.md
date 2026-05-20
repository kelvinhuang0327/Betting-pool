# 2026 WBC 深度對決分析：Venezuela (VEN) vs Japan (JPN)

## 📊 核心實力指標 (Left vs Right)

| 指標 | Venezuela (VEN) | Japan (JPN) | 差異 |
|---|---:|---:|---:|
| 台灣比賽日期 | 2026-03-15 | 2026-03-15 | 同日 |
| 預賽戰績 | 3-1 | 4-0 | JPN 優勢 |
| 場均得分 (RS/G) | 6.50 | 8.50 | JPN +2.00 |
| 場均失分 (RA/G) | 3.00 | 2.25 | JPN -0.75 |
| 得失分差/場 (RD/G) | +3.50 | +6.25 | JPN +2.75 |
| OPS+ | 無資料 | 無資料 | 無資料 |
| FIP- | 無資料 | 無資料 | 無資料 |
| K-BB% | 無資料 | 無資料 | 無資料 |
| DER | 無資料 | 無資料 | 無資料 |
| Elo | 無資料 | 無資料 | 無資料 |

## 🧢 關鍵投打對決模擬 (Matchup Depth)

| 項目 | Venezuela (VEN) | Japan (JPN) |
|---|---|---|
| 台灣比賽日期 | 2026-03-15 | 2026-03-15 |
| 官方 probable starter | Ranger Suarez (ERA 3.20 | WHIP 1.22 | K/9 8.64 | BB/9 2.17) | Yoshinobu Yamamoto (ERA 2.49 | WHIP 0.99 | K/9 10.42 | BB/9 3.06) |
| 先發資料來源 | https://statsapi.mlb.com/api/v1.1/game/788097/feed/live | https://statsapi.mlb.com/api/v1.1/game/788097/feed/live |
| 先發品質分數 | +0.315 | +0.733 |
| 牛棚深度可驗證資料 | 無資料 | 無資料 |
| 專項對戰加權資料 | 無資料 | 無資料 |

## 🎯 比分機率分佈 (Poisson 回歸)

資料來源：
- 官方完賽資料：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_2026_live_scores.json`
- 模型設定：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/model_artifacts.json`

回歸參數：
- 基礎 `lambda_VEN = 4.38`
- 基礎 `lambda_JPN = 5.75`
- 先發修正後 `lambda_VEN = 4.12`
- 先發修正後 `lambda_JPN = 5.61`
- Quarter-Final 先發權重：`0.65`
- 特定對戰加權：`官方 probable starters + 保守先發抑分修正`

機率結果：
- VEN 9 局勝率：`0.2618`
- JPN 9 局勝率：`0.6211`
- 9 局平手率：`0.1170`
- 全場 VEN 勝率（平手 50/50）：`0.3203`
- 全場 JPN 勝率（平手 50/50）：`0.6797`

## 🗺️ 得分機率矩陣圖

- 矩陣 CSV：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-15_VEN_JPN_poisson_matrix.csv`
- 矩陣摘要：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-15_VEN_JPN_poisson_summary.json`

ASCII 熱度圖（VEN 為列，JPN 為欄）：

```text
       + 01234567890
VEN 10 |            
VEN  9 |            
VEN  8 |     ....   
VEN  7 |   ..:-::.  
VEN  6 |   .-=+=-:. 
VEN  5 |   :=*#*+-:.
VEN  4 |  .-+%@%*=:.
VEN  3 |  .:+#%%*=:.
VEN  2 |   :=+*+=-:.
VEN  1 |   ..:-::.. 
VEN  0 |            
```

## 💰 台灣運彩 EV 檢查

- 台灣運彩目前賠率：`無資料`
- EV：`無資料`
- 結論：`無資料`

## ⚠️ 風險提醒

- `model_artifacts.json` 未提供各隊權重欄位，該部分為 `無資料`。
- 先發與牛棚若臨場異動，lambda 與勝率會快速變化。
- 若盤口補齊，可立即改算 EV 與 Kelly 倉位。
