# P27 Per-Market Clean CLV Isolation Report
**Date**: 2026-05-20  
**Phase**: P27_PER_MARKET_CLV_ISOLATION  
**paper_only**: true | **diagnostic_only**: true  
**Source**: P23/P26-pinned snapshot (first 2,788 lines)  
**Matching module**: `wbc_backend/clv/outcome_matching.py` (P26 line-aware)

---

## 資料概況

| 項目 | 數值 |
|------|------|
| P23/P26 pinned lines | 2,788 |
| Current snapshot lines | 2,808（drift +20，僅記錄） |
| Valid CLV pairs | 236 |
| Matching method | Line-aware name matching（P26） |
| Index fallback | 無 |

---

## Per-Market 詳細結果

### MNL（Moneyline）

| 指標 | 數值 |
|------|------|
| Clean obs (N) | 681 |
| Unique matches | 233 |
| Skipped | 6（MARKET_SHAPE_MISMATCH：2-way vs 3-way） |
| Mean CLV % | +0.0449% |
| Median CLV % | 0.0000% |
| 5% Trimmed mean | +0.023% |
| 10% Trimmed mean | 依 JSON |
| Bootstrap CI (95%) | **[-0.2196, +0.2980]** |
| CI crosses zero | **Yes** |
| Positive rate | 35.54% |
| \|CLV\| > 10% count | 11 |
| \|CLV\| > 25% count | 依 JSON |
| \|CLV\| > 50% count | 0 |
| **Classification** | **MARKET_CLEAN_INCONCLUSIVE** |

**解讀**：MNL 是最大的市場（N=681）。CI 寬度 ±0.26pp，遠大於 mean +0.04%。median=0 顯示分布對稱於 0。11 個 |CLV|>10% 觀測值需留意是否仍有 name variation（非 line move 的 team alias 差異）。

---

### HDC（Handicap）

| 指標 | 數值 |
|------|------|
| Clean obs (N) | 402 |
| Unique matches | 201 |
| Skipped | 56（LINE_MOVED：盤口線移動） |
| Mean CLV % | **-0.0027%**（負值，但接近 0） |
| Median CLV % | 0.0000% |
| 5% Trimmed mean | +0.009% |
| Bootstrap CI (95%) | **[-0.3239, +0.3220]** |
| CI crosses zero | **Yes** |
| Positive rate | 38.31% |
| \|CLV\| > 10% count | 3 |
| **Classification** | **MARKET_CLEAN_INCONCLUSIVE** |

**解讀**：HDC 有最多 LINE_MOVED skips（56），是 P25 CRITICAL bug 的主要來源。修復後 mean ≈ 0，CI 最寬（±0.32pp），完全不顯著。HDC 盤口調整頻繁，CLV signal 難以在此市場提取。

---

### OU（Over/Under）

| 指標 | 數值 |
|------|------|
| Clean obs (N) | 418 |
| Unique matches | 209 |
| Skipped | 42（LINE_MOVED：total line 移動） |
| Mean CLV % | +0.0377% |
| Median CLV % | 0.0000% |
| 5% Trimmed mean | +0.0505% |
| Bootstrap CI (95%) | **[-0.2542, +0.3325]** |
| CI crosses zero | **Yes** |
| Positive rate | 37.08% |
| \|CLV\| > 10% count | 5 |
| **Classification** | **MARKET_CLEAN_INCONCLUSIVE** |

**解讀**：OU 有 42 LINE_MOVED skips，但 5% trimmed mean (+0.05%) 略高於 raw mean，顯示殘餘 outlier 有輕微雜訊。CI 仍大幅穿越 0。

---

### OE（Odd/Even）

| 指標 | 數值 |
|------|------|
| Clean obs (N) | 460 |
| Unique matches | 230 |
| Skipped | 0（名稱固定，無 LINE_MOVED 風險） |
| Mean CLV % | +0.0083%（接近 0） |
| Median CLV % | 0.0000% |
| 5% Trimmed mean | +0.0033% |
| Bootstrap CI (95%) | **[-0.0692, +0.0862]** |
| CI crosses zero | **Yes** |
| Positive rate | 15.65%（最低，顯示 odds 幾乎不動） |
| \|CLV\| > 10% count | **0** |
| **Classification** | **MARKET_CLEAN_INCONCLUSIVE** |

**解讀**：OE 的 positive rate 只有 15.65%（遠低於其他市場 30-38%），顯示 TSL 的 OE odds 幾乎是固定的，CLV ≈ 0 為結構性必然。OE 是 P25 定義的「PASS_BUT_NON_INFORMATIVE」市場。CI 最窄（±0.08pp），因為幾乎不動，就算排除 0 假說也毫無意義。

---

### TTO（Team Total）

| 指標 | 數值 |
|------|------|
| Clean obs (N) | 370 |
| Unique matches | 185 |
| Skipped | 64（LINE_MOVED：team total 移動，最高） |
| Mean CLV % | +0.0815%（各市場最高） |
| Median CLV % | 0.0000% |
| 5% Trimmed mean | +0.0214% |
| Bootstrap CI (95%) | **[-0.3090, +0.4742]** |
| CI crosses zero | **Yes** |
| Positive rate | 30.00% |
| \|CLV\| > 10% count | 11 |
| **Classification** | **MARKET_CLEAN_INCONCLUSIVE** |

**解讀**：TTO 有最多 LINE_MOVED skips（64/434 = 14.7%），同時 mean 最高（+0.08%）。但 CI 上界 +0.47% vs 下界 -0.31%，寬度達 0.78pp，完全無法排除 mean=0。樣本 N=370 偏少且分布最不穩定。

---

## 市場比較彙總

| Market | N | Mean% | CI(95%) | Median | Trimmed5% | CI∋0 | 分類 |
|--------|---|-------|---------|--------|-----------|------|------|
| MNL | 681 | +0.0449 | [-0.22, +0.30] | 0.00 | +0.023 | **Yes** | INCONCLUSIVE |
| HDC | 402 | -0.0027 | [-0.32, +0.32] | 0.00 | +0.009 | **Yes** | INCONCLUSIVE |
| OU | 418 | +0.0377 | [-0.25, +0.33] | 0.00 | +0.051 | **Yes** | INCONCLUSIVE |
| OE | 460 | +0.0083 | [-0.07, +0.09] | 0.00 | +0.003 | **Yes** | INCONCLUSIVE |
| TTO | 370 | +0.0815 | [-0.31, +0.47] | 0.00 | +0.021 | **Yes** | INCONCLUSIVE |

**所有市場 CI 均穿越 0，median 均為 0.00%，無任何市場可視為有正向 CLV 訊號。**

---

## 結論

**Final Classification**: `P27_ALL_MARKETS_CLEAN_CLV_INCONCLUSIVE`

所有 5 個市場在 P26 line-aware matching 修復後，clean CLV 在統計上均不顯著。  
不作任何 profitability claim。不作任何投注建議。champion=fixed_edge_5pct 維持不變。
