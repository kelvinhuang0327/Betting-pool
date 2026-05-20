# P26 Final Validation Report
**Date**: 2026-05-20  
**Phase**: P26_CLV_LINE_AWARE_MATCHING_REPAIR  
**paper_only**: true | **diagnostic_only**: true

---

## 本輪目標

修復 CLV construction 的 outcome matching bug（P25 CRITICAL 發現）：  
不再用 index position 比較 pregame/closing odds，改以 outcome name（含盤口線）精確匹配。

---

## 驗證矩陣

| 驗證項目 | 結果 |
|----------|------|
| P26 新增 tests (23個) | **23/23 PASS** |
| P17 standalone | **64/64 PASS** |
| P12-P17 regression | **296/296 PASS** |
| JSON schema (paper_only=true, diagnostic_only=true) | **4/4 PASS** |
| Forbidden scan (affirmative claims) | **0 hits** |
| No index fallback contract | **PASS** |
| P23 baseline 未被覆蓋 | **PASS** |
| Drift 僅記錄不修改 | **PASS** |

---

## Source Snapshot 狀態

| 項目 | P23 Pinned | Current |
|------|-----------|---------|
| Lines | 2,788 | 2,803 |
| SHA256 | ac1320de... | 157f4bdb... |
| Action | — | 僅記錄，P26 diagnostic 使用前 2788 行 |

---

## CLV Repair 結果

| 指標 | Old Pipeline | Clean Pipeline | Δ |
|------|-------------|---------------|---|
| Observations | 2,499 | 2,331 | -168 |
| Mean CLV % | **+0.2332%** | **+0.034%** | -0.2pp |
| \|CLV\| > 50% count | **20** | **0** | **全消除** |
| Top-1% sum | **908.32%** | **21.92%** | **-97.6%** |
| CI (95%) | [-0.10, +0.58] | [-0.09, +0.16] | 上界大幅收窄 |
| CI crosses zero | Yes | **Yes** | — |

**Skip breakdown**: LINE_MOVED=162, MARKET_SHAPE_MISMATCH=6, Total=168

---

## Clean CLV 分類

**CLEAN_INCONCLUSIVE** (CI 穿越 0)

- Mean = +0.034%（接近 0）
- CI = [-0.0914, +0.1561]（CI 穿越 0）
- n = 2,331（樣本足夠，但訊號統計不顯著）
- 結論：**P22 正向 CLV 均值完全由 construction bug 驅動，修復後無可用訊號**

---

## 嚴格禁止事項確認

| 禁止事項 | 狀態 |
|---------|------|
| 合併 PR #2 | 未執行 |
| 聲稱可獲利 | 未聲稱 |
| CLV 轉投注建議 | 未作 |
| 替換 fixed_edge_5pct champion | 未替換 |
| Strategy optimizer promotion | 未啟動 |
| 修改 TSL crawler 或 live odds API | 未修改 |
| 用 source drift 覆蓋 P23/P24/P25 baseline | 未覆蓋 |
| Line moved 時 index fallback 補算 CLV | 未使用 |

---

## 最終分類

**P26_CLEAN_CLV_INCONCLUSIVE_DIAGNOSTIC_COMPLETED**

- CLV line-aware matching repair: COMPLETED
- Clean CLV CI crosses zero: CONFIRMED
- P25 CRITICAL bug diagnosis: VERIFIED and FIXED
- 下一步：需更長時間的 TSL 資料累積，或外部歷史 odds 資料，方能取得統計顯著的 CLV 觀測
