# P26 — CLV Line-Aware Matching Repair
**Date**: 2026-05-20  
**Final Classification**: P26_CLEAN_CLV_INCONCLUSIVE_DIAGNOSTIC_COMPLETED  
**paper_only**: true | **diagnostic_only**: true

---

## 本輪工程交接報告

### 1. 本輪目標

修復 P25 診斷的 CRITICAL CLV construction bug：以 outcome name（含盤口線）匹配 pregame/closing，不再用 index position，完全消除人工 CLV artifact。重跑 clean CLV diagnostic，確認修復後的真實 CLV 訊號強度。

---

### 2. 已完成事項

| 項目 | 狀態 |
|------|------|
| Pre-flight branch/git status 確認 | ✅ |
| P23/P24/P25 artifacts 存在確認 | ✅ |
| Source snapshot drift 記錄（+15 records，不覆蓋 P23） | ✅ |
| `wbc_backend/clv/outcome_matching.py` 實作 | ✅ |
| MNL 2-way/3-way shape mismatch 偵測 | ✅ |
| HDC/OU/TTO line-aware name matching | ✅ |
| OE side matching | ✅ |
| UNSUPPORTED_MARKET 路徑 | ✅ |
| PARSE_FAILED 路徑 | ✅ |
| 禁止 index fallback | ✅ |
| `tests/test_p26_clv_line_aware_matching.py` (23 tests) | ✅ |
| `scripts/p26_clv_line_aware_matching.py` | ✅ |
| P26 tests: 23/23 PASS | ✅ |
| P17 standalone: 64/64 PASS | ✅ |
| P12-P17 regression: 296/296 PASS | ✅ |
| JSON schema: 4/4 PASS | ✅ |
| Forbidden scan: 0 affirmative hits | ✅ |
| No index fallback contract 驗證 | ✅ |
| 4 JSON artifacts 產出 | ✅ |
| 4 report .md 產出 | ✅ |

---

### 3. 修改或產出的檔案

**新增**:
- [`wbc_backend/clv/outcome_matching.py`](../../wbc_backend/clv/outcome_matching.py)
- [`wbc_backend/clv/__init__.py`](../../wbc_backend/clv/__init__.py)
- [`tests/test_p26_clv_line_aware_matching.py`](../../tests/test_p26_clv_line_aware_matching.py)
- [`scripts/p26_clv_line_aware_matching.py`](../../scripts/p26_clv_line_aware_matching.py)

**Artifacts**:
- `data/paper_recommendations/p26_clv_line_aware_matching_result_20260520.json`
- `data/paper_recommendations/p26_clean_clv_diagnostic_20260520.json`
- `data/paper_recommendations/p26_skipped_outcome_audit_20260520.json`
- `data/paper_recommendations/p26_old_vs_clean_clv_comparison_20260520.json`

**Reports**:
- `report/p26_clv_line_aware_matching_result_20260520.md`
- `report/p26_clean_clv_diagnostic_20260520.md`
- `report/p26_old_vs_clean_clv_comparison_20260520.md`
- `report/p26_final_validation_20260520.md`

---

### 4. 驗證結果

| 驗證 | PASS/FAIL |
|------|-----------|
| P26 tests 23/23 | **PASS** |
| P17 standalone 64/64 | **PASS** |
| P12-P17 regression 296/296 | **PASS** |
| JSON schema 4/4 | **PASS** |
| Forbidden scan (affirmative) | **0 hits PASS** |
| paper_only=true 所有 artifacts | **PASS** |
| no index fallback | **PASS** |
| P23 baseline 未被覆蓋 | **PASS** |

---

### 5. 目前結論

**CLV 修復確認：P22 正向均值完全由 construction bug 驅動**

| 指標 | Old Pipeline | Clean Pipeline |
|------|-------------|---------------|
| Mean CLV | +0.2332% | +0.034% |
| \|CLV\|>50% 案例 | 20 | **0（全消除）** |
| Top-1% sum | 908.32% | 21.92%（-97.6%）|
| CI (95%) | [-0.10, +0.58] | [-0.09, +0.16] |
| CI crosses zero | Yes | **Yes** |

**Clean CLV 分類：CLEAN_INCONCLUSIVE**  
修復後 mean ≈ +0.034%，CI 穿越 0，無統計顯著正向訊號。

---

### 6. 尚未完成事項

- Clean per-market bootstrap CI 的全量細分報告（A2 JSON 有，report 只有彙總）
- TTO 市場：是否「home/away」team 的 TTO 為不同 market_code 尚未確認
- MNL name mismatch（team name 變更，非 line move）分類尚未深化

---

### 7. 風險與不確定點

1. **MNL MISSING_OUTCOME**：在 clean pipeline 中，若 team name 在 closing 換了（e.g., 替補陣容顯示不同名稱），會被歸類為 MISSING_OUTCOME。此情況在 P25 audit 發現 3 pairs（1.3%），影響小但存在。
2. **OE 結構性無資訊**：OE 的 odds 移動極小（P25 std=0.84%），即使 matched 也幾乎無 CLV，會稀釋整體均值向 0。
3. **樣本積累速度**：tsl_odds_history.jsonl 當前有效 pairs=236，要達到統計顯著的 CLV 訊號，至少需要更多季度資料。

---

### 8. 建議下一輪優先處理方向

1. **P27 — OE 市場排除研究**：確認將 OE 排除後，clean CLV 的 CI 是否收窄（OE 被確認為 PASS_BUT_NON_INFORMATIVE）。
2. **P28 — Per-market clean CLV 深化**：MNL/HDC/OU/TTO 個別 CI 分析，找出哪個市場最有 CLV 訊號潛力。
3. **Model quality gap**：MLB walkforward Brier=0.2487（接近 random），考慮重啟特徵工程改善模型品質。
4. **TSL 資料積累**：繼續 2026 regular season TSL 收集，建立逐漸增長的 pregame 時間點資料集。

---

### 9. 下一輪可直接執行的 task prompt

```
請執行 P27 — Clean CLV Per-Market Deep Dive：
1. 以 P23 pinned snapshot (2788 lines)，使用 P26 line-aware matching
2. 計算 MNL/HDC/OU/TTO 各別的 bootstrap CI（排除 OE）
3. 確認哪個市場有最強的 CLV 訊號或最窄的 CI
4. 確認 OE 排除後整體 CI 是否改善
5. 所有 artifacts paper_only=true / diagnostic_only=true
6. 不作 production proposal / champion replacement / profitability claim
7. 產出 data/paper_recommendations/p27_*.json 和 report/p27_*.md
```

---

### 10. CTO Agent 摘要（10行）

P26 成功修復 P25 診斷的 CRITICAL CLV construction bug。原 P22 pipeline 以 index position 比較 pregame/closing outcome，在盤口線移動時產生人工 CLV（最高 +107.14%）。P26 實作 wbc_backend/clv/outcome_matching.py，改以 outcome name 精確匹配：LINE_MOVED 跳過，MARKET_SHAPE_MISMATCH 跳過，完全禁止 index fallback。23/23 deterministic tests PASS，P17 64/64 PASS，P12-P17 296/296 PASS，JSON schema 4/4 PASS，forbidden scan 0 hits。Clean CLV 執行結果：old mean +0.2332%（artifact）→ clean mean +0.034%（接近 0）；|CLV|>50% cases 從 20 降至 0；top-1% sum 從 908 降至 22（-97.6%）。CI [-0.09, +0.16] 穿越 0，分類 CLEAN_INCONCLUSIVE。結論：P22 正向 CLV 均值完全由 bug 驅動，修復後無統計顯著正向訊號。champion=fixed_edge_5pct 維持，promotion frozen，P26_CLEAN_CLV_INCONCLUSIVE_DIAGNOSTIC_COMPLETED。
