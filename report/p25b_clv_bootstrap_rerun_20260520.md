# P25B WBC CLV Bootstrap Rerun 報告

**Phase**: P25B — WBC CLV Bootstrap Rerun (Line-Aware, After Construction Fix)
**Date**: 2026-05-20
**Classification**: `P25B_WBC_CLV_BOOTSTRAP_RERUN_COMPLETED_INCONCLUSIVE`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、本輪目標

P25 已修復 HDC/OU/TTO index-based CLV construction bug。本輪在 TSL WBC 資料上執行 line-aware CLV bootstrap rerun，只納入 `line_comparable=True` 的 rows，確認 clean CLV 是否仍 inconclusive，或轉為 neutral/positive/negative。

---

## 二、P25 Fix Dependency

| 項目 | 狀態 |
|------|------|
| `wbc_backend/clv/outcome_matching.py` | ✅ P25 fix merged |
| `tests/test_p25_clv_construction_fix.py` | ✅ 21/21 PASS |
| `tests/test_p26_clv_line_aware_matching.py` | ✅ 23/23 PASS |
| Fix commit | `480b340` |

---

## 三、資料來源

| 項目 | 值 |
|------|---|
| 資料檔 | `data/tsl_odds_history.jsonl` |
| 總 rows | 2,815 |
| Unique match IDs | 886 |
| 日期範圍 | 2026-03-13 → 2026-05-21 |
| 資料來源 | TSL 台彩 crawl（WBC/NPB 等聯賽） |

---

## 四、P2 797 場 vs P25B 220 場差異說明

P2 報告的「797 場」定義為：**有至少一個 ≥4h pregame snapshot 的場次**（即系統曾在賽前 4 小時以上抓取過賠率）。

P25B CLV bootstrap 需要 **pregame AND closing 快照同時存在**：
- pregame: 最後一個 `fetched_at` ≥ `game_time - 4h` 的快照
- closing: 最後一個 `fetched_at` ≈ `game_time ± 2h` 的快照

| 定義 | 場次數 |
|------|--------|
| 有 pregame 快照（P2 定義） | **797** |
| 有 pregame + closing 快照（CLV 需要） | **220** |
| 缺 closing 快照（開賽前後無抓取） | **577** |
| 缺 pregame 快照 | **89** |

**577 場缺 closing** 是資料收集架構問題：TSL crawler 未被排程在開賽時間附近執行，導致大量場次無收盤賠率可比較。這是下一步要解決的基礎設施問題。

---

## 五、Line-Aware Filter 規則

```
filter_rule: line_comparable=True
method:      wbc_backend/clv/outcome_matching.py name-based matching
no_index_fallback: True (confirmed by 21 P25 tests)
```

HDC/OU/TTO：outcome name 包含盤口線。pregame 名稱 ≠ closing 名稱 → `LINE_SHIFT_UNCOMPARABLE`，clv_pct=None，排除。

---

## 六、Excluded Rows 統計

| 排除原因 | 數量 | 比例 |
|----------|------|------|
| `LINE_SHIFT_UNCOMPARABLE` | 236 | 10.0% |
| `MISSING_OPENING_ODDS` | 0 | 0% |
| `MISSING_CLOSING_ODDS` | 0 | 0% |
| `UNSUPPORTED_MARKET` | 0 | 0% |
| **可用 (line_comparable=True)** | **2,115** | **90.0%** |
| **總 outcome results** | **2,351** | — |

---

## 七、Per-Market CLV 統計（Clean, line_comparable=True only）

| Market | n | Mean CLV% | Median | Std | 95% CI lo | 95% CI hi | CI Crosses 0 | Classification |
|--------|---|-----------|--------|-----|-----------|-----------|--------------|----------------|
| **MNL** | 623 | +0.206% | 0.000% | 6.17% | -0.264% | +0.694% | ✅ YES | **INCONCLUSIVE** |
| **HDC** | 366 | -0.054% | 0.000% | 3.49% | -0.411% | +0.289% | ✅ YES | **INCONCLUSIVE** |
| **OU** | 380 | +0.041% | 0.000% | 3.62% | -0.348% | +0.398% | ✅ YES | **INCONCLUSIVE** |
| **TTO** | 312 | +0.107% | 0.000% | 4.53% | -0.384% | +0.622% | ✅ YES | **INCONCLUSIVE** |
| **OE** | 434 | +0.005% | 0.000% | 0.84% | -0.076% | +0.082% | ✅ YES | **INCONCLUSIVE** |
| **ALL** | **2,115** | **+0.076%** | **0.000%** | **4.34%** | **-0.110%** | **+0.257%** | ✅ YES | **INCONCLUSIVE** |

---

## 八、Bootstrap 95% CI 結果

```
Overall clean CLV:
  n = 2,115
  mean = +0.0755%
  95% CI = [-0.1101%, +0.2569%]
  CI crosses zero: TRUE
  → CLEAN_CLV_INCONCLUSIVE
```

---

## 九、Before / After 比較（Construction Fix 效果確認）

| 指標 | Before (P24, index-based) | After (P25B, line-aware) | 變化 |
|------|--------------------------|--------------------------|------|
| Mean CLV | ~+0.362% | **+0.076%** | -0.287pp ↓ |
| Max CLV | +107.14% | +80.65% | -26.5pp ↓ |
| 95% CI lo | ~-0.019% | **-0.110%** | — |
| 95% CI hi | ~+0.776% | **+0.257%** | -0.519pp ↓ |
| CI crosses zero | YES | YES | 維持 |
| Classification | INCONCLUSIVE | **INCONCLUSIVE** | 不變 |

**結論**：移除 236 個 LINE_SHIFT_UNCOMPARABLE rows 後：
- Mean CLV 從 +0.36% 降至 +0.08%，印證舊正值主要來自 construction artifact
- Max CLV 從 +107% 降至 +81%（仍有部分大值，但來源不同）
- CI 仍跨零，clean CLV 為 INCONCLUSIVE
- 修復有效消除 artifact，但未揭示隱藏的正向訊號

---

## 十、結論：仍 Inconclusive，是否可進入下一階段

**結論**：`CLEAN_CLV_INCONCLUSIVE`

修復 CLV construction bug 後，WBC 市場賠率移動與模型預測方向的相關性仍無法統計確認。

**可進入下一階段的條件**：
1. ✅ Line-aware CLV 已建立（可繼續使用）
2. ❌ CLV 仍 INCONCLUSIVE — 需更多資料（更多 closing snapshots）或更好的預測模型
3. 🔄 **下一步建議**：修復 closing snapshot 覆蓋率問題（577 場缺 closing → 安排 TSL crawler 在開賽前後執行），或評估 WBC model-edge 是否能在 220 場 comparable pairs 上展示一致 positive performance

---

## 十一、尚未完成事項

1. **Closing snapshot 覆蓋率**：577/886 場缺 closing → TSL crawler 需增加開賽前後排程
2. **WBC model-edge 驗證**：在 220 comparable pairs 上評估模型預測 vs 市場閉盤賠率
3. **MLB CLV**：pregame-safe=0，阻塞中，需 2026 regular season 實時收集
4. **模型品質改善**：MLB Brier=0.2487（近隨機），WBC 樣本量太小，需整合更多歷史資料
5. **P1 w_market sweep**：MLB `market_prob` 仍為 post-game proxy，阻塞

---

## 十二、Modified / New Files

| 檔案 | 操作 |
|------|------|
| `data/paper_recommendations/p25b_clv_bootstrap_rerun_20260520.json` | CREATED |
| `report/p25b_clv_bootstrap_rerun_20260520.md` | CREATED |
| `00-BettingPlan/20260520/p25b_clv_bootstrap_rerun_20260520.md` | CREATED |
