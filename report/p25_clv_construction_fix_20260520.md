# P25 CLV Construction Fix 報告

**Phase**: P25 — CLV Construction Fix (HDC / OU / TTO Line-Shift Bug)
**Date**: 2026-05-20
**Classification**: `P25_CLV_CONSTRUCTION_FIX_COMPLETED`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、Bug Root Cause

### 問題描述

TSL odds history 中，HDC（讓分）、OU（大小分）、TTO（球隊總分）的 outcome name **包含盤口線（line）**：

| Market | 範例 outcome name |
|--------|------------------|
| HDC    | `底特律老虎 -2.5` / `密爾瓦基釀酒人 +2.5` |
| OU     | `大 8.5` / `小 8.5` |
| TTO    | `大 4.5` / `小 4.5` |

P22（舊）CLV pipeline 以 **array index 位置**（`outcomes[0]` = side A，`outcomes[1]` = side B）比較 pregame 和 closing 賠率。當 pregame → closing 之間 **盤口線移動**（line shift），index[0] 在 pregame 對應 `-1.5` 盤，在 closing 對應 `-2.5` 盤，因此 CLV 公式在比較**不同盤口的賠率**，數學上無意義。

### 量化影響

| Market | Mismatch pairs | Outliers \|CLV\| > 50% |
|--------|---------------|----------------------|
| HDC    | 12.2% (28/229) | 17 |
| TTO    | 14.7% (32/217) | — |
| OU     | 9.1% (21/230)  | — |

**最嚴重假陽性範例**：
```
match 3468261.1 | HDC | 底特律老虎 -1.5 @ 2.90 (pregame) → 底特律老虎 -2.5 @ 1.40 (closing)
Old CLV = (2.90 - 1.40) / 1.40 × 100 = +107.14%  ← 完全是 artifact
```

---

## 二、Before / After Comparison

| 項目 | Before (P22 index-based) | After (P25 line-aware) |
|------|--------------------------|------------------------|
| HDC line shift | 繼續比較，產生假 CLV | `LINE_SHIFT_UNCOMPARABLE`，clv_pct=None |
| OU line shift  | 繼續比較，產生假 CLV | `LINE_SHIFT_UNCOMPARABLE`，clv_pct=None |
| TTO line shift | 繼續比較，產生假 CLV | `LINE_SHIFT_UNCOMPARABLE`，clv_pct=None |
| HDC/OU/TTO same line | 同樣比較（正確）| `CLV_COMPARABLE`，CLV 正常計算 |
| MNL 2-way | 同樣計算（正確）| `CLV_COMPARABLE`，行為不變 |
| MNL 3-way | 部份 index 錯誤 | `CLV_COMPARABLE`，name-based match |
| MNL shape mismatch | 可能比較 2-way vs 3-way | `LINE_SHIFT_UNCOMPARABLE`，保護排除 |

---

## 三、HDC / OU / TTO Line-Shift Handling

**實作位置**：[wbc_backend/clv/outcome_matching.py](../wbc_backend/clv/outcome_matching.py)

### 核心邏輯

```python
def _match_line_encoded_market(market_code, pre_outcomes, clo_outcomes):
    pre_map = _outcome_map(pre_outcomes)   # {outcomeName: odds}
    clo_map = _outcome_map(clo_outcomes)

    for name, pre_odds in pre_map.items():
        if name not in clo_map:
            # 盤口線移動：pregame 的 outcome name 在 closing 中找不到
            # → LINE_MOVED status，不計算 CLV，不用 index fallback
            yield OutcomeMatchResult(status=LINE_MOVED, clv_pct=None, ...)
        else:
            # 同一 outcome name（同盤口）→ 正常計算 CLV
            clv_abs, clv_pct = _compute_clv(pre_odds, clo_map[name])
            yield OutcomeMatchResult(status=MATCHED, clv_pct=clv_pct, ...)
```

### P25 CLV Status Mapping

| `MatchStatus` (internal) | `clv_status` (P25 API) | `excluded_from_clean_clv` |
|--------------------------|------------------------|--------------------------|
| `MATCHED`                | `CLV_COMPARABLE`       | `False` |
| `LINE_MOVED`             | `LINE_SHIFT_UNCOMPARABLE` | `True` |
| `MARKET_SHAPE_MISMATCH`  | `LINE_SHIFT_UNCOMPARABLE` | `True` |
| `MISSING_OUTCOME`        | `MISSING_CLOSING_ODDS` | `True` |
| `PARSE_FAILED`           | `MISSING_OPENING_ODDS` | `True` |
| `UNSUPPORTED_MARKET`     | `UNSUPPORTED_MARKET`   | `True` |

---

## 四、MNL Unaffected Proof

MNL outcome name 是球隊名稱（`芝加哥白襪`、`底特律老虎`），不含盤口線數字。`_match_mnl()` 函數以 outcome name 作為 key 進行 name-based matching，不受 line shift 問題影響。

額外保護：MNL 2-way vs 3-way shape mismatch 會被偵測並排除（`MARKET_SHAPE_MISMATCH`），確保 2-way 和 3-way 市場的 outcome index 不會互相比較。

**測試驗證**（`TestMNLUnaffected`）：
- `test_mnl_clv_still_computed` → 2-way MNL CLV 正常計算 ✅
- `test_mnl_3way_clv_computed` → 3-way MNL CLV 正常計算 ✅
- `test_mnl_2way_vs_3way_excluded` → shape mismatch 正確排除 ✅

---

## 五、Line-Shift 排除數量

**可執行範圍（TSL WBC pregame-safe 797 場）**：

依 P25 audit 的已知比例（來自 P24/P26 診斷）：

| Market | 預估 mismatch 比例 | 797 場估算排除 pairs |
|--------|-------------------|---------------------|
| HDC    | ~12.2%            | ~97 pairs excluded |
| TTO    | ~14.7%            | ~117 pairs excluded |
| OU     | ~9.1%             | ~72 pairs excluded |
| MNL    | 0%（name match）  | 0 pairs excluded |

實際數量需執行 `scripts/p26_clv_line_aware_matching.py` 於 TSL WBC 資料集上確認。

---

## 六、WBC Clean CLV Validation 重啟

**可以重啟**：TSL WBC pregame-safe games = 797（≥4h pregame）

重啟條件：
1. ✅ HDC line shift 不再產生假陽性 CLV
2. ✅ OU / TTO line shift 使用 name-based comparison
3. ✅ MNL CLV 行為不受影響
4. ✅ line-shift rows 有明確 `excluded_from_clean_clv=True` audit status
5. 分析時 filter `line_comparable=True` 的 rows 進行 clean CLV bootstrap

---

## 七、Remaining Blockers

1. **MLB pregame-safe = 0**：`mlb_odds_2025_real.csv` 全部為 post-game proxy，MLB CLV validation 仍阻塞，直到 2026 regular season 開始實時 TSL 收集。
2. **P1 w_market sweep blocked**：MLB `market_prob` 為 post-game proxy，Orchestrator 實驗仍無法執行。
3. **模型品質不足**：即使 CLV 修復後，MLB walkforward Brier=0.2487（近乎隨機），hit rate=46.25% < 50%。Model quality 需獨立修復。

---

## 八、測試結果摘要

| 測試套件 | 結果 | 通過數 |
|----------|------|--------|
| `test_p25_clv_construction_fix.py` | ✅ PASS | **21/21** |
| `test_p26_clv_line_aware_matching.py` | ✅ PASS | **23/23** |

---

## 九、Modified / Added Files

| 檔案 | 操作 | 說明 |
|------|------|------|
| `wbc_backend/clv/outcome_matching.py` | MODIFIED | 新增 P25 API 欄位（`clv_status`, `line_comparable`, `line_shift_detected`, `excluded_from_clean_clv`, `audit_reason`）+ `to_dict()` 更新 |
| `tests/test_p25_clv_construction_fix.py` | CREATED | 21 tests，涵蓋 P25 驗收標準 |
| `data/paper_recommendations/p25_clv_construction_fix_20260520.json` | CREATED | Artifact JSON |
| `report/p25_clv_construction_fix_20260520.md` | CREATED | 本文件 |
| `00-BettingPlan/20260520/p25_clv_construction_fix_20260520.md` | CREATED | BettingPlan 副本 |
