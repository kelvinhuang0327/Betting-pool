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
| 先發投手預估 | 無資料 | 無資料 |
| 先發投手球種/球速可驗證資料 | 無資料 | 無資料 |
| 牛棚深度可驗證資料 | 無資料 | 無資料 |
| 專項對戰加權資料 | 無資料 | 無資料 |

## 🎯 比分機率分佈 (Poisson 回歸)

資料來源：
- 官方完賽資料：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_2026_live_scores.json`
- 模型設定：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/model_artifacts.json`

回歸參數：
- `lambda_VEN = 4.38`
- `lambda_JPN = 5.75`
- 特定對戰加權：`無資料`（無可驗證拆分資料）

機率結果：
- VEN 9 局勝率：`0.2777`
- JPN 9 局勝率：`0.6053`
- 9 局平手率：`0.1170`
- 全場 VEN 勝率（平手 50/50）：`0.3362`
- 全場 JPN 勝率（平手 50/50）：`0.6638`

## 🗺️ 得分機率矩陣圖

- 矩陣 CSV：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-15_VEN_JPN_poisson_matrix.csv`
- 矩陣摘要：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-15_VEN_JPN_poisson_summary.json`

ASCII 熱度圖（VEN 為列，JPN 為欄）：

```text
       + 01234567890
VEN 10 |            
VEN  9 |            
VEN  8 |    ......  
VEN  7 |   .:---::. 
VEN  6 |   .-=++=-:.
VEN  5 |   :=*##*=:.
VEN  4 |   :+#@%#+-.
VEN  3 |   :=#%#*=:.
VEN  2 |   .-=++=-:.
VEN  1 |    .::::.  
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
