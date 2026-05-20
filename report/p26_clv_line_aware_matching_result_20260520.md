# P26 CLV Line-Aware Matching — Implementation Report
**Date**: 2026-05-20  
**Phase**: P26_CLV_LINE_AWARE_MATCHING_REPAIR  
**paper_only**: true | **diagnostic_only**: true  
**production_proposal**: false | **champion_replacement**: false | **profitability_claim**: false

---

## 摘要

P25 確認 CLV construction 存在 CRITICAL bug：P22 pipeline 以 index position 比較 pregame/closing outcomes，在盤口線移動時產生人工 CLV artifact（最高 +107.14%）。

P26 實作 line-aware outcome matching，以 outcome name（含盤口線）為 key 進行匹配，完全消除 index fallback 路徑。

---

## 修復內容

### 新模組：`wbc_backend/clv/outcome_matching.py`

| 市場 | 比較方法 | 跳過條件 |
|------|----------|----------|
| MNL | 以 team name 精確匹配 | 2-way vs 3-way → MARKET_SHAPE_MISMATCH |
| HDC | 以 outcome name（含盤口線）精確匹配 | pregame name 不在 closing → LINE_MOVED |
| OU | 以 outcome name（含 total line）精確匹配 | total line 不同 → LINE_MOVED |
| OE | 以 outcome name（單/雙）精確匹配 | 名稱固定，不會有 LINE_MOVED 風險 |
| TTO | 以 outcome name（含 team total）精確匹配 | total 不同 → LINE_MOVED |
| 其他 | — | UNSUPPORTED_MARKET |

### 禁止事項確認

- ✅ 無 index fallback：line moved 時直接 skip，不補算 CLV
- ✅ 不破壞 P22/P23/P24/P25 artifacts
- ✅ 不修改 TSL crawler 或 live odds API
- ✅ 不作 production proposal

---

## 測試結果

**P26 新增 tests**: `tests/test_p26_clv_line_aware_matching.py`

| Test Class | Tests | 結果 |
|------------|-------|------|
| TestHDCMatching | 4 | PASS |
| TestOUMatching | 3 | PASS |
| TestOEMatching | 2 | PASS |
| TestTTOMatching | 2 | PASS |
| TestMNLMatching | 5 | PASS |
| TestParseFailures | 4 | PASS |
| TestNoIndexFallback | 3 | PASS |
| **Total** | **23** | **23/23 PASS** |

### 關鍵 case 驗證

| Case | 預期 | 實際 |
|------|------|------|
| HDC -1.5 pre vs -2.5 clo | LINE_MOVED, clv=None | ✅ PASS |
| HDC -1.5 pre vs -1.5 clo | MATCHED, clv計算 | ✅ PASS |
| OU 8.5 pre vs 9.5 clo | LINE_MOVED, clv=None | ✅ PASS |
| OU 8.5 pre vs 8.5 clo | MATCHED, clv計算 | ✅ PASS |
| OE 單/雙 match | MATCHED | ✅ PASS |
| TTO 大4.5 vs 大5.5 | LINE_MOVED | ✅ PASS |
| MNL 2-way vs 3-way | MARKET_SHAPE_MISMATCH | ✅ PASS |
| P25 critical case (+107.14% artifact) | LINE_MOVED, clv=None | ✅ PASS |

---

## Source Snapshot Drift

| 項目 | P23 Pinned | Current |
|------|-----------|---------|
| Line count | 2,788 | 2,803 |
| SHA256 | ac1320de... | 157f4bdb... |
| Drift | — | **+15 records** |

**動作**：僅記錄，不覆蓋 P23 baseline。P26 diagnostic 使用 P23 pinned snapshot（前 2788 行）。

---

## 結論

- CLV matching 修復完成，line-aware name matching 正確替換 index-based matching
- 23/23 deterministic tests PASS
- 禁止 index fallback 合約通過
