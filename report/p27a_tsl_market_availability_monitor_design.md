# P27A — TSL 市場可用性監控器設計（紙上方案）

**任務 ID**: P27A  
**父任務**: P26K  
**建立日期**: 2026-05-23  
**模式**: `paper_only=true` | `diagnostic_only=true` | `read_only=true` | `production_proposal=false`

---

## 1. 動機

P26K 確認的根本原因 `SOURCE_STATE_TRULY_EMPTY`：TSL 在收盤視窗（07:00–09:00Z）開放前約 4–5.6 小時，已將 NPB 目標賽事從預購賭盤清單撤除。

| 賽事 | 最後看見時間 | 撤除時間（估）| 距開賽 | 收盤視窗快照數 |
|------|------------|-------------|--------|-------------|
| 3469930.1 (讀賣 vs 燕子) | 03:24:52Z | 03:39Z | 5.6h | **0** |
| 3469931.1 (廣島 vs 橫濱) | 04:55:09Z | 05:10Z | 4.1h | **0** |

Daemon 每 15 分鐘正常呼叫 TSL（`force_closing=True` 已激活），但 TSL 回應中不含目標賽事。**系統對此無任何警告或紀錄。** 這是本設計要填補的缺口。

---

## 2. 偵測 Schema

每次 TSL 輪詢後，為每個目標 `match_id` 寫入一筆可用性紀錄：

| 欄位 | 類型 | 說明 |
|------|------|------|
| `match_id` | string | TSL 賽事 ID（如 `3469930.1`） |
| `league` | string | 聯賽代碼（如 `NPB`） |
| `game_time_utc` | ISO 8601 | 賽事預定開賽時間（UTC） |
| `first_seen_timestamp` | ISO 8601 | 首次在 TSL 回應中出現的時間 |
| `last_seen_timestamp` | ISO 8601 | 最近一次在 TSL 回應中出現的時間 |
| `latest_seen_in_source` | boolean | 最新一輪輪詢是否有此賽事 |
| `disappeared_at` | ISO 8601 / null | 首次確認消失的時間；仍存在時為 null |
| `hours_before_game` | float / null | 消失時距開賽剩餘小時數 |
| `consecutive_absent_cycles` | integer | 連續缺席輪詢次數 |
| `source_name` | string | 資料來源名稱（`TSL_PREGAME_LIST`） |
| `source_response_context` | string | 消失當下 TSL 回應摘要（如 `total_games=12, NPB=0`） |
| `classification` | enum / null | 分類標籤（見下節） |
| `classification_rationale` | string / null | 分類理由說明 |

---

## 3. 警報分類條件

### `TSL_MARKET_WITHDRAWAL_EARLY` — 嚴重度: HIGH
**觸發條件**:
```
match 曾出現 (first_seen_timestamp != null)
AND latest_seen_in_source == false
AND disappeared_at != null
AND hours_before_game > 2.0
```
**語意**: TSL 在距開賽超過 2 小時前即撤除賭盤，收盤賠率**無法**透過 TSL 抓取。

**P26K 實例**: 3469930.1（5.6h 早撤）、3469931.1（4.1h 早撤）

---

### `TSL_MARKET_NORMAL_REMOVAL` — 嚴重度: INFO
**觸發條件**:
```
match 曾出現
AND latest_seen_in_source == false
AND disappeared_at != null
AND hours_before_game <= 2.0
```
**語意**: TSL 在賽前 2 小時內撤除，符合一般市場關閉時機，無需特別警示。

---

### `TSL_MARKET_NEVER_SEEN` — 嚴重度: MEDIUM
**觸發條件**:
```
match_id 列在預期清單中
AND first_seen_timestamp == null
AND game_time_utc < now
```
**語意**: 預期賽事從未在 TSL 回應中出現過。

---

## 4. P26K 反向套用驗證

以本設計 retroactively 套用至 P26K 資料：

```
match_id=3469930.1:
  first_seen_timestamp: UNKNOWN (schema 未存在)
  last_seen_timestamp:  2026-05-21T03:24:52Z
  disappeared_at:       2026-05-21T03:39:00Z (估)
  hours_before_game:    5.35
  classification:       TSL_MARKET_WITHDRAWAL_EARLY  ✓
  收盤視窗快照:         0

match_id=3469931.1:
  first_seen_timestamp: UNKNOWN
  last_seen_timestamp:  2026-05-21T04:55:09Z
  disappeared_at:       2026-05-21T05:10:00Z (估)
  hours_before_game:    3.83
  classification:       TSL_MARKET_WITHDRAWAL_EARLY  ✓
  收盤視窗快照:         0
```

**結論**: 本 schema 能正確分類 P26K 失敗情境。

---

## 5. 整合點分析（僅作設計參考，不修改代碼）

若未來實作，整合點為 `tsl_snapshot.py` 的 TSL 回應解析後段：
- 將 TSL 返回的 `match_id` 集合與已知目標清單比對
- 更新 `data/derived/tsl_market_availability_state.json`（設計路徑）

**本設計不修改任何現有代碼。**

---

## 6. 限制聲明

- `paper_only=true` — 本文件為設計草案，無任何代碼實作
- `production_proposal=false` — 不構成生產部署提案
- 不修改 daemon、crawler、scheduler、ingestion 任何代碼
- 不呼叫任何 live odds API

---

*Artifact: `data/paper_recommendations/p27a_tsl_market_availability_monitor_design.json`*
