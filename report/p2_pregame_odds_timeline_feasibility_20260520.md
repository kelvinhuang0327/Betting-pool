# P2 Pregame Odds Timeline Feasibility Audit

**Phase**: P2 — PREGAME_ODDS_TIMELINE_FEASIBILITY_AUDIT  
**Date**: 2026-05-20  
**Final Classification**: `P2_LIMITED_TIMELINE_SMOKE_ONLY`  
**Constraints**: `paper_only=true` / `diagnostic_only=true`

---

## 一、背景

P0 已確認 `data/mlb_2025/mlb_odds_2025_real.csv` 無 `snapshot_timestamp`，`pregame_safe=0%`，P1 Real Orchestrator w_market ablation sweep **暫停**。

P2 任務：盤點系統內所有 odds timeline 來源，確認是否存在可支撐正式 CLV validation 與 market baseline 的 pregame-safe odds。

---

## 二、Odds Source Inventory

| source_file | rows | has_snapshot_ts | has_game_start_ts | has_market_type | has_odds | has_status_final | timeline_tier | pregame_safe_count |
|---|---|---|---|---|---|---|---|---|
| `data/mlb_2025/mlb_odds_2025_real.csv` | 2,430 | ❌ | ✅ | ✅ | ✅ | ✅ | **post_game_proxy_only** | **0** |
| `data/mlb_context_sources/odds_timeline_canonical.jsonl` | 2,430 | ✅ (ingest date) | ❌ | ✅ | ✅ | ❌ | **post_game_proxy_only** | **0** |
| `data/mlb_context_sources/odds_timeline.jsonl` | 2,398 | ✅ | ❌ | ✅ | ✅ | ❌ | **no_timestamp** | **0** |
| `data/tsl_odds_history.jsonl` | 2,815 | ✅ (fetched_at) | ✅ (game_time) | ✅ | ✅ | ❌ | **strict_4point_pregame** | **797** |
| `data/mlb_2025/mlb-2025-asplayed.csv` | 2,430 | ❌ | ✅ | ❌ | ❌ | ✅ | **no_timestamp** | **0** |
| `wbc_backend/mlb_data/schemas/` | — | ✅ (設計) | ✅ (設計) | ✅ (設計) | ✅ (設計) | ❌ | **no_data** | **0** |

---

## 三、Timeline Tier Breakdown

| Tier | 說明 | 來源數量 |
|---|---|---|
| `strict_4point_pregame` | 有 ≥4h pregame snapshot，fetched_at + game_time 完整 | **1** (TSL WBC) |
| `post_game_proxy_only` | 只有單次 ingest snapshot（賽後） | **2** (MLB CSV + canonical) |
| `no_timestamp` | 無可靠 timestamp 或 game_start | **2** |
| `no_data` | 僅 schema 設計文件，無實際資料 | **1** |

---

## 四、核心三問答

### ❓ Q1：是否可以重啟 P1 w_market sweep？

**答：否。**

MLB moneyline pregame-safe games = **0**。

`mlb_odds_2025_real.csv` 的 2,430 筆及其衍生的 `odds_timeline_canonical.jsonl` 均為單次賽後 ingest，`latest_pregame_home_ml`, `latest_pregame_ts`, `opening_home_ml`, `decision_home_ml` 欄位全為 `null`。`pregame_snapshot_count = 0` 在所有記錄中。

P1 w_market sweep 需要 pregame-safe MLB moneyline odds 作為 `market_prob` 輸入，目前條件不具備，**持續暫停**。

---

### ❓ Q2：是否可以重做 clean CLV validation？

**答：有限度可行（WBC only，存在 P25 construction bug）。**

TSL WBC source 有 797 場賽事具備 ≥4h pregame snapshot（`fetched_at` vs `game_time` gap ≥4h）。

但須注意：
1. **P25 CLV Construction Bug 尚未修復**：HDC/OU/TTO 使用 index-based 比較，而非 name-matching，12-15% pairs 受 handicap line shift 影響，產生人工極端值。
2. **WBC only**：TSL 資料僅覆蓋 WBC 2026，不含 MLB moneyline。
3. **MNL 市場可嘗試小樣本 smoke**：MNL 無 name mismatch 問題，797 場中有效 MNL pairs 可做有限 CLV smoke test。

**結論**：clean CLV validation 需先完成 P25 CLV construction fix（P1 修復），僅限 WBC MNL 市場的小樣本 smoke。

---

### ❓ Q3：是否可以支撐 Moneyline paper recommendation v3？

**答：否。**

MLB pregame-safe moneyline odds = **0**。MLB Moneyline paper recommendation v3 需要：
1. MLB pregame-safe odds（≥300 games）
2. 有效 CLV computation（MLB moneyline，無 construction bug）
3. 統計顯著的 market baseline（MLB）

目前三項條件均不滿足。TSL WBC 資料不能替代 MLB moneyline 需求。

---

## 五、各來源詳細分析

### 5.1 mlb_odds_2025_real.csv — **POST_GAME_PROXY_ONLY**

- **欄位**：`Date, Start Time (EDT), Away, Home, Status, Away ML, Home ML, O/U, Over, Under, Home RL Spread, RL Away, RL Home`
- **缺失**：完全無 `snapshot_timestamp`
- **P0 確認**：`leakage_type=post_game_proxy`，`pregame_safe=0%`
- **不可用於**：CLV、pregame market baseline、w_market sweep

### 5.2 odds_timeline_canonical.jsonl — **POST_GAME_PROXY_ONLY**

- **架構**：符合 schema（含 `latest_pregame_ts`, `opening_ts` 等欄位）
- **實際資料**：所有 pregame 欄位為 `null`，`pregame_snapshot_count=0`
- **原因**：派生自 `mlb_odds_2025_real.csv`，無真正 pregame capture
- **注意**：`odds_history[0].ts` = `2026-03-18T17:56:56Z`（ingest 日期），非 pregame snapshot

### 5.3 odds_timeline.jsonl — **NO_TIMESTAMP**

- 2,398 筆，同為 MLB 2025 single-snapshot 資料
- 無 game_start_ts 可驗證 pregame/postgame 界線
- **不可用**

### 5.4 tsl_odds_history.jsonl — **STRICT_4POINT_PREGAME（WBC only）**

- **2,815 筆 snapshots / 797 場賽事有 ≥4h pregame 抓取**
- 有 `fetched_at`（UTC ISO）+ `game_time`（TZ-aware）
- 含 5 市場：MNL / HDC / OU / OE / TTO
- **限制**：
  - WBC 2026 only，非 MLB
  - P25 CLV construction bug 未修復（HDC/OU/TTO）
  - MNL 仍存在 2-way vs 3-way 混合問題（P25 confirmed）

### 5.5 wbc_backend schemas — **ASPIRATIONAL DESIGN ONLY**

- Schema 設計完整（含 `latest_pregame_ts`, `decision_ts`, `opening_ts`）
- 無對應的已填充 data files
- 代表系統設計意圖，但資料供給缺口尚未填補

---

## 六、可行路徑

| 路徑 | 前置條件 | 預估規模 | 性質 |
|---|---|---|---|
| **WBC MNL CLV smoke test** | 修復 P25 CLV construction bug | ~797 場 | Research only |
| **MLB pregame odds 收集** | 接入 live odds API（TheOddsAPI / DraftKings / 運彩 API）| 需持續收集 ≥300 場 | Research pipeline 建立 |
| **MLB historical pregame odds** | 購買/取得 2025 season odds feed（帶 timestamp）| ~2,430 場 | 外部資料采購 |

> ⚠️ 所有路徑均為 Research Only。不得修改 production default path。不得啟動 w_market sweep。

---

## 七、Final Classification 決策說明

```
MLB_PREGAME_SAFE_GAMES = 0        → P2_PREGAME_ODDS_TIMELINE_READY_FOR_CLV ✗
                                  → P2_PREGAME_ODDS_TIMELINE_COLLECTION_REQUIRED ≈
TSL_WBC_PREGAME_SAFE_GAMES = 797  → Limited WBC smoke test possible
                                  → P2_LIMITED_TIMELINE_SMOKE_ONLY ✓
```

**Final Classification: `P2_LIMITED_TIMELINE_SMOKE_ONLY`**

---

## 八、Champion 狀態確認

- `fixed_edge_5pct`：**PRESERVED / HOLD 維持**
- 推廣：**FROZEN**
- 生產提案：**NONE**
- w_market sweep：**BLOCKED — collection_required before restart**

---

**P2 COMPLETE** ✅  
*paper_only=true / diagnostic_only=true / no production proposals*
