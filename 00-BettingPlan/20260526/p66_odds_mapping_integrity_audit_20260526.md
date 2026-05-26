# P66 — Odds Mapping Integrity Audit
**Date**: 2026-05-26  
**Phase**: P66  
**Classification**: `P66_ODDS_MAPPING_INTEGRITY_CONFIRMED`

---

## 最終分類

```
P66_ODDS_MAPPING_INTEGRITY_CONFIRMED
```

P64/P65 所記錄的穩定負向邊緣（mean edge = −0.0325，535 筆資料列）**已確認為真實現象**，並非賠率映射錯誤、邊選投反、轉換公式錯誤或 Edge 計算錯誤所導致。

---

## 審計摘要

| 審計步驟 | 狀態 |
|---|---|
| Step 2 — Join 完整性 | `JOIN_INTEGRITY_PASS` |
| Step 3 — 邊選映射 | `SIDE_MAPPING_PASS` |
| Step 4 — 賠率轉換 | `ODDS_CONVERSION_PASS` |
| Step 5 — Edge 重新計算 | `EDGE_RECALCULATION_PASS` |
| 禁用詞掃描 | `CLEAN`（0 violations） |

---

## 關鍵數字

| 指標 | 數值 |
|---|---|
| P64 資料列數 | 535 |
| Join 未命中 | 0 |
| 雙重標頭重複 Key | 28（`last-row-wins`，非錯誤） |
| Side 反轉數 | 0 |
| 賠率轉換錯誤 | 0 |
| Edge 重算最大 delta | 0.000000 |
| 平均 edge（原始） | −0.032473 |
| 平均 edge（重算） | −0.032473 |
| 正向 edge 筆數（原始/重算） | 200 / 200 |

---

## 治理標誌（Immutable）

| 標誌 | 值 |
|---|---|
| `paper_only` | `true` |
| `kelly_deploy_allowed` | `false` |
| `production_ready` | `false` |
| `real_bet_allowed` | `false` |
| `live_api_calls` | `0` |
| `runtime_recommendation_logic_changed` | `false` |
| `data_year_2024_gap_remains_unresolved` | `true` |

---

## 測試結果

- P66 專項測試：**36/36 PASS**
- 累積回歸（P43 + P59–P66）：**227/227 PASS**

---

## 重要發現

1. **雙重標頭隱式去重**: 賠率 CSV 中有 28 個重複 `(date, home_team)` Key，對應雙重標頭賽事。P64 使用 `dict[key]=row` 隱式保留最後一筆（last-row-wins）。這是確定性行為，非映射錯誤。建議 P67+ 改用 `game_id`-based join 明確消歧。

2. **Platt 公式符號**: P66 腳本草稿初次採用錯誤符號（`+A*logit+B`），在實作審查階段自行發現並修正（應為 `−A*logit−B`）。P64 原始碼全程正確，此為 P66 實作過程中的自我校正。

3. **負向 edge 確認為真**: mean edge = −0.0325 在 2025 球季全域範圍確認，無任何映射或計算人為因素。

---

## 下一步建議

**P67 — 2024 資料缺口填補**

2024 球季資料缺口自 P61 起標記為 `UNRESOLVED`。P66 確認了 2025 的負向 edge，擴充至 2024 能驗證跨賽季一致性，並正式關閉 `data_year_2024_gap_remains_unresolved` 旗標。

**備選 P67 — 雙重標頭 Join 消歧**

將 P64 join key 從 `(date, home_team)` 改為 `game_id`-based，明確處理 28 筆雙重標頭重複 Key。
