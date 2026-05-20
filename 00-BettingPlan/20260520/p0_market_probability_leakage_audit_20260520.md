# P0 Market Probability Timestamp Leakage Audit — 交接文件

**日期**: 2026-05-20
**任務代號**: P0_MARKET_PROBABILITY_TIMESTAMP_LEAKAGE_AUDIT
**Final Classification**: `P0_MARKET_BASELINE_LEAKAGE_CONFIRMED`
**P1 狀態**: **BLOCKED（暫停）**

---

## 任務摘要

稽核 P29 ablation 所有 market_prob 資料來源的時間戳安全性。

**核心發現**：
- P29 ablation 的 market_prob 100% 來自 `data/mlb_2025/mlb_odds_2025_real.csv`
- 該 CSV 無 `snapshot_timestamp` 欄位，MEMORY 2026-03-20 確認為 post-season 單次快照
- pregame_safe 覆蓋率：**0/2,430 (0.0%)**
- leakage_type=post_game_proxy：**2,430/2,430 (100%)**
- P29 所報 V3 Brier=0.244154、V0 Brier=0.244354 均在污染基準上計算，不可作為 P1 sweep 依據

---

## 決策矩陣

| 條件 | 結果 |
|------|------|
| pregame_safe ≥ 80%？ | ❌ 0.0% |
| leakage 確認？ | ✅ post_game_proxy 100% |
| MEMORY 外部驗證？ | ✅ 2026-03-20 確認 |
| snapshot_timestamp 存在？ | ❌ 欄位不存在 |
| **P1 可啟動？** | **❌ 否** |

---

## 輸出 Artifact

| 檔案 | 描述 |
|------|------|
| `scripts/p0_market_probability_leakage_audit.py` | 稽核腳本（含 3 unit tests PASS） |
| `data/paper_recommendations/p0_market_probability_leakage_audit_20260520.json` | 含 2,430 筆 per-row leakage flag |
| `report/p0_market_probability_leakage_audit_20260520.md` | 完整技術報告 |

---

## P1 重啟條件

需滿足以下任一：
1. 取得帶有 pregame snapshot_timestamp 的 MLB 歷史 odds API 資料
2. TSL 2026 regular season 實時收集累積 ≥ 300 pregame snapshot
3. 以現有 TSL 233 closing pairs 重做 P29（樣本數偏低，需評估統計效力）

---

## CEO Invariants 確認

- paper_only=true ✅
- production_proposal=false ✅
- champion_replacement_allowed=false ✅
- champion=`fixed_edge_5pct`（維持）✅
- PR #2 未 merge ✅
- production default path 未修改 ✅

---

## 下一步（待 CEO 確認）

- P0 結論：P1 w_market sweep 暫停
- 建議發起 P2：pregame odds timeline 盤點（評估 TSL 實時收集進度與外部 odds API 可行性）
- 或維持現狀等待 2026 regular season TSL 資料累積

*paper_only=true | diagnostic_only=true | 不含任何生產提案 | 不含獲利聲明*
