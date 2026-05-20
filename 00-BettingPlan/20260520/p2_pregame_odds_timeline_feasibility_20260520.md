# P2 Pregame Odds Timeline Feasibility — BettingPlan

**Phase**: P2  
**Date**: 2026-05-20  
**Status**: COMPLETE  
**Classification**: `P2_LIMITED_TIMELINE_SMOKE_ONLY`

---

## 核心結論

> **MLB pregame-safe games = 0。P1 w_market sweep 持續暫停。**

系統內所有 MLB odds 來源（`mlb_odds_2025_real.csv`, `odds_timeline_canonical.jsonl`, `odds_timeline.jsonl`）均為單次賽後 ingest，無 pregame snapshot_timestamp，無法用於 CLV computation 或 market baseline。

---

## Source Inventory 摘要

| 來源 | Tier | Pregame Safe | 用途 |
|---|---|---|---|
| `mlb_odds_2025_real.csv` (2,430 rows) | post_game_proxy | 0 | ❌ 不可用 |
| `odds_timeline_canonical.jsonl` (2,430 rows) | post_game_proxy | 0 | ❌ 不可用 |
| `odds_timeline.jsonl` (2,398 rows) | no_timestamp | 0 | ❌ 不可用 |
| `tsl_odds_history.jsonl` (2,815 rows) | strict_4h pregame | **797** | ⚠️ WBC only |
| `mlb-2025-asplayed.csv` | no_odds | 0 | 僅結果標籤 |

---

## 三問決策

| 問題 | 答案 |
|---|---|
| 可以重啟 P1 w_market sweep？ | **否** — MLB pregame-safe=0 |
| 可以重做 clean CLV validation？ | **有限** — WBC MNL only，需先修 P25 CLV bug |
| 可以支撐 Moneyline paper v3？ | **否** — 需 MLB pregame-safe ≥300 |

---

## 下一步（Research Only）

| 行動 | 性質 |
|---|---|
| 修復 P25 CLV construction bug（name matching） | Research |
| 以 WBC MNL 797 場跑 CLV smoke test | Research |
| 規劃 MLB live odds API 接入以積累 pregame-safe 資料 | Research pipeline |

---

## Champion 狀態

- `fixed_edge_5pct`：**PRESERVED / HOLD**
- w_market sweep：**BLOCKED**
- 推廣：**FROZEN**

---

**P2 COMPLETE** ✅  
*paper_only=true / diagnostic_only=true / no production proposals*
