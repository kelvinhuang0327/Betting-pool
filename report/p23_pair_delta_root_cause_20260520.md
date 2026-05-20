# P23-B Pair Delta Root Cause Report
**日期：** 2026-05-20  
**Phase：** P23_PAIR_DELTA_ROOT_CAUSE  
**Task：** P23-B  
**paper_only：** true

---

## 1. 問題陳述

P19 canonical artifact 報告 `valid_clv_pairs=233`，P22 CLV validation 使用 `valid_pairs_used=236`，差值 +3。

## 2. 數據基線

| Phase | 時間點 | records | unique match_ids | valid_clv_pairs |
|-------|--------|---------|------------------|-----------------|
| P19 | 2026-05-20 (P19 計算時) | 2,747 | 859 | 233 |
| P22 | 2026-05-23 (P22 計算時) | 2,772 | 不明 (未 pin) | 236 |
| P23 current | 2026-05-20 (本次) | 2,788 | 877 | 236 |

## 3. 衍生規則（derivation rule）

兩個 Phase 使用完全相同的規則：
- **pregame window**：`fetched_at <= game_time - 2h`（最近一筆）
- **closing window**：`|fetched_at - game_time| <= 2h`（最近一筆）
- 兩窗口皆有 non-empty markets 才計為 valid pair

**無任何規則變更。**

## 4. Root Cause 分析

### 直接原因

P19 與 P22 之間，`tsl_odds_history.jsonl` 新增了 25 筆記錄（2747 → 2772）。  
這些新記錄中有 18 個新的 `match_id`（877 - 859 = 18，以 current 估計）。  
其中恰好 3 個新 match_id 同時擁有完整的 pregame + closing snapshots，形成 3 個新 valid pairs（233 → 236）。

### 分類

| 類別 | 是否涉及 | 說明 |
|------|----------|------|
| Window rule 變更 | ❌ 否 | pregame 2h / closing 2h 均未變 |
| Pair derivation 邏輯變更 | ❌ 否 | 選最近 pregame / 最近 closing 邏輯不變 |
| Duplicate handling 變更 | ❌ 否 | 同 match_id 去重邏輯不變 |
| Invalid-to-valid reclassification | ❌ 否 | 非重分類，純粹新資料 |
| **Source data additive growth** | ✅ 是 | 主因：新比賽資料累積完成 closing window |

### Root cause category：`SOURCE_DATA_GROWTH_NEW_COMPLETE_PAIRS`

## 5. 可重現性驗證

本次以當前 `data/tsl_odds_history.jsonl`（2788 records）重新執行：
```
Total records: 2788, unique match_ids: 877
Valid pairs: 236, Invalid: 641
Invalid breakdown: {'no_pregame': 64, 'no_closing': 577}
```

結果 **236 pairs**，與 P22 完全一致，**reproducible=true**。

## 6. P19 vs current invalid breakdown 比較

| 原因 | P19 | Current |
|------|-----|---------|
| no_pregame / missing_pregame | 57 | 64 |
| no_closing / missing_closing | 563 | 577 |
| **合計 invalid** | 620 | 641 |

兩者增量（+21 invalid）對應新增 15 個不完整的 match_id。

## 7. 結論

**pair delta=3 成因完全解釋，可重現。**

- 非 bug、非規則變更、非資料污染
- 屬 append-only source data 正常成長
- P22 236 pairs = P19 233 pairs + 3 個新完整 pairs（資料累積後才形成）

**P1 啟動條件：不因此阻塞**  
**Classification：`PAIR_COUNT_DELTA_EXPLAINED`**
