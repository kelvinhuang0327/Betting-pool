# P26 Old vs Clean CLV Comparison Report
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 核心發現

P25 診斷發現的 CRITICAL bug（index-based 跨盤口線比較）已在 P26 修復。  
以下量化比較 old pipeline 與 clean pipeline 的差異。

---

## 比較表

| 指標 | Old Pipeline (P22 index-based) | Clean Pipeline (P26 line-aware) | Δ |
|------|-------------------------------|--------------------------------|---|
| 方法 | `for i in range(min(n_pre, n_clo))` | name-based matching | — |
| Observations | 2,499 | 2,331 | **-168** |
| Mean CLV % | **+0.2332%** | **+0.034%** | **-0.1992pp** |
| \|CLV\| > 50% count | **20** | **0** | **-20** |
| Top-1% sum | **908.32%** | **21.92%** | **-886.40%** |
| Bootstrap CI (95%) | [-0.1013, +0.5812] | [-0.0914, +0.1561] | 上界大幅收窄 |
| CI crosses zero | Yes (but bias from outliers) | Yes (true estimate) | — |

---

## 影響分析

### P22 正向均值完全由 bug 驅動

舊 pipeline 正向 CLV 均值 +0.2332% = 人工 artifact。

- 20 個 |CLV|>50% outliers 的 top-1% sum = **908.32%**
- 修復後 top-1% sum = **21.92%**（減少 41.4 倍）
- 修復後均值降至 +0.034%（接近 0，CI 穿越 0）

### LINE_MOVED skips 分布（P25 預測 vs P26 實測）

| Market | P25 預測 mismatch 數 | P26 LINE_MOVED 數 |
|--------|---------------------|------------------|
| HDC | 28 pairs (12.2%) | 確認 LINE_MOVED 存在 |
| OU | 21 pairs (9.1%) | 確認 LINE_MOVED 存在 |
| TTO | 32 pairs (14.7%) | 確認 LINE_MOVED 存在 |
| OE | 0 | 0 |
| MNL | 3 name mismatch + shape | 6 MARKET_SHAPE_MISMATCH |

### 人工 CLV artifact 案例還原（P25 case study）

| 項目 | 數值 |
|------|------|
| Pregame: 底特律老虎 handicap | -1.5 @ 2.90 |
| Closing: 底特律老虎 handicap | -2.5 @ 1.40 |
| Old pipeline CLV (index 0) | **(2.90-1.40)/1.40 × 100 = +107.14%** ← artifact |
| Clean pipeline | **LINE_MOVED → skip, CLV = None** ✅ |

---

## 結論

1. **老 pipeline 正向 CLV = artifact**，不代表真實市場效率優勢
2. **Clean pipeline CLV 均值 ≈ 0**（+0.034%, CI 穿越 0）
3. **CLV 訊號目前統計不顯著**，在 N=2,331 觀測值下無法作為策略信號
4. 修復正確且必要；但修復後的 clean CLV 並未提供可用的正向訊號

**不作 profitability claim。不作 production proposal。champion 保持 fixed_edge_5pct 不變。**
