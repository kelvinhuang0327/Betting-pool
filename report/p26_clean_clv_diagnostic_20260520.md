# P26 Clean CLV Diagnostic Report
**Date**: 2026-05-20  
**Phase**: P26_CLV_LINE_AWARE_MATCHING_REPAIR  
**paper_only**: true | **diagnostic_only**: true  
**Source**: P23-pinned snapshot (first 2,788 lines of tsl_odds_history.jsonl)

---

## 資料概況

| 項目 | 數值 |
|------|------|
| P23 pinned records | 2,788 |
| Valid CLV pairs | 236 |
| Invalid pairs | 641 |

---

## Skip 統計

| Skip Reason | Count | 說明 |
|-------------|-------|------|
| LINE_MOVED | 162 | HDC/OU/TTO 盤口線移動，pregame outcome name 不在 closing |
| MARKET_SHAPE_MISMATCH | 6 | MNL 2-way vs 3-way 不同型態 |
| **Total Skipped** | **168** | 總跳過 outcome 配對數 |
| MATCHED (clean valid) | 2,331 | 進入 CLV 計算 |
| Total results | 2,499 | — |

---

## CLV 結果對比

| 指標 | Old (index-based) | Clean (line-aware) | 變化 |
|------|------------------|-------------------|------|
| Observations | 2,499 | 2,331 | -168 |
| Mean CLV % | **+0.2332%** | **+0.034%** | -0.1992pp |
| Std CLV % | — | — | — |
| \|CLV\| > 50% count | **20** | **0** | **-20 (全消除)** |
| Top-1% sum | **908.32** | **21.92** | **-886.40 (97.6%↓)** |
| Bootstrap CI (95%) | [-0.1013, +0.5812] | **[-0.0914, +0.1561]** | — |
| CI crosses zero | Yes | **Yes** | — |

---

## Per-Market Clean CLV

| Market | Old N | Old Mean | Clean N | Clean Mean | Clean CI | CI Crosses 0 |
|--------|-------|---------|---------|-----------|---------|--------------|
| MNL | 472 | — | ~466 | — | — | — |
| HDC | 458 | — | ~402 | — | — | — |
| OU | 460 | — | ~418 | — | — | — |
| OE | 460 | — | 460 | — | — | — |
| TTO | 434 | — | ~385 | — | — | — |

*(詳細數值見 JSON artifact)*

---

## Clean CLV 信號解讀

- **Clean mean = +0.034%**：接近 0，遠小於 old mean (+0.2332%)
- **CI = [-0.0914, +0.1561]**：CI 穿越 0，無法排除 mean=0 的假說
- **所有 |CLV|>50% 案例已消除**：P25 確認的 20 個人工 outlier 全部是 LINE_MOVED artifacts
- **Top-1% sum 從 908.32 → 21.92**：減少 97.6%，確認舊 pipeline 正向均值完全由 bug 驅動

---

## 結論

**clean CLV 分類：CLEAN_INCONCLUSIVE**

雖然 mean 為正（+0.034%），但 95% bootstrap CI 穿越 0（[-0.0914, +0.1561]），樣本量 n=2,331 但訊號強度極弱，無法統計顯著地排除 mean=0。

P22 pipeline 報告的正向 CLV mean (+0.2332%) 已確認為 construction bug artifact。修復後，CLV 訊號在目前樣本下無統計顯著性。

**不應以此作為投注信號。不作任何 profitability claim。**
