# 2026 WBC 深度對決分析：Korea (KOR) vs Dominican Republic (DOM)

## 📊 核心實力指標 (Left vs Right)

| 指標 | Korea (KOR) | Dominican Republic (DOM) | 差異 |
|---|---:|---:|---:|
| 台灣比賽日期 | 2026-03-14 | 2026-03-14 | 同日 |
| 預賽戰績 | 2-3 | 5-0 | DOM 優勢 |
| 場均得分 (RS/G) | 5.60 | 10.20 | DOM +4.60 |
| 場均失分 (RA/G) | 5.80 | 2.00 | DOM -3.80 |
| 得失分差/場 (RD/G) | -0.20 | +8.20 | DOM +8.40 |
| OPS+ | 無資料 | 無資料 | 無資料 |
| FIP- | 無資料 | 無資料 | 無資料 |
| K-BB% | 無資料 | 無資料 | 無資料 |
| DER | 無資料 | 無資料 | 無資料 |
| Elo | 無資料 | 無資料 | 無資料 |

## 🧢 關鍵投打對決模擬 (Matchup Depth)

| 項目 | Korea (KOR) | Dominican Republic (DOM) |
|---|---|---|
| 台灣比賽日期 | 2026-03-14 | 2026-03-14 |
| 官方 probable starter | Hyun Jin Ryu (ERA 4.20 | WHIP 1.28 | K/9 7.20 | BB/9 2.00) | Cristopher Sánchez (ERA 2.50 | WHIP 1.06 | K/9 9.45 | BB/9 1.96) |
| 先發資料來源 | https://statsapi.mlb.com/api/v1.1/game/788095/feed/live | https://statsapi.mlb.com/api/v1.1/game/788095/feed/live |
| 先發品質分數 | -0.055 | +0.683 |
| 牛棚深度可驗證資料 | 無資料 | 無資料 |
| 專項對戰加權資料 | 無資料 | 無資料 |

## 🎯 比分機率分佈 (Poisson 回歸)

資料來源：
- 官方完賽資料：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_2026_live_scores.json`
- 模型設定：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/model_artifacts.json`

回歸參數：
- 基礎 `lambda_KOR = 3.80`
- 基礎 `lambda_DOM = 8.00`
- 先發修正後 `lambda_KOR = 3.60`
- 先發修正後 `lambda_DOM = 8.03`
- Quarter-Final 先發權重：`0.65`
- 特定對戰加權：`官方 probable starters + 保守先發抑分修正`

機率結果：
- KOR 9 局勝率：`0.0742`
- DOM 9 局勝率：`0.8711`
- 9 局平手率：`0.0547`
- 全場 KOR 勝率（平手 50/50）：`0.1015`
- 全場 DOM 勝率（平手 50/50）：`0.8985`

## 🗺️ 得分機率矩陣圖

- 矩陣 CSV：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-14_KOR_DOM_poisson_matrix.csv`
- 矩陣摘要：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/2026-03-14_KOR_DOM_poisson_summary.json`

ASCII 熱度圖（KOR 為列，DOM 為欄）：

```text
       + 01234567890
KOR 10 |            
KOR  9 |            
KOR  8 |            
KOR  7 |      ......
KOR  6 |     .:----:
KOR  5 |    .:-++++=
KOR  4 |    .-+#%%#+
KOR  3 |    .-+#%@%*
KOR  2 |    .-=*##*+
KOR  1 |     .:-==-:
KOR  0 |       .... 
```

## 💰 台灣運彩 EV 檢查

- 台灣運彩目前賠率：`無資料`
- EV：`無資料`
- 結論：`無資料`

## ⚠️ 風險提醒

- `model_artifacts.json` 未提供各隊權重欄位，該部分為 `無資料`。
- 先發與牛棚若臨場異動，lambda 與勝率會快速變化。
- 若盤口補齊，可立即改算 EV 與 Kelly 倉位。
