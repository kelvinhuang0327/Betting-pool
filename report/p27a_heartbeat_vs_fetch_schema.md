# P27A — Heartbeat-vs-Fetch 欄位語義消歧 Schema 設計

**任務 ID**: P27A  
**父任務**: P26K  
**建立日期**: 2026-05-23  
**模式**: `paper_only=true` | `diagnostic_only=true` | `read_only=true` | `production_proposal=false`

---

## 1. 問題描述

P26K 診斷需多個 Phase 才能分清「TSL 來源為空」與「OddsAPI 被 quota 封鎖」的差異，根本原因是 Heartbeat 欄位語義模糊：

| 現有欄位 | 實際語義 | 混淆語義 |
|---------|---------|---------|
| `status="captured"` | heartbeat 記錄已寫入磁碟 | 收盤賠率已被抓取 |
| `fetched=false` | OddsAPI 外部收盤失敗 | TSL 未執行 |
| `api_calls_today=2` | OddsAPI 呼叫計數（不含 TSL） | 跨來源總呼叫數 |
| `trigger_reason="cap=2 reached, calls=2"` | OddsAPI 被 quota 封鎖 | TSL 也被封鎖 |

---

## 2. 現有 Schema（重建自 P26K）

```json
{
  "timestamp": "2026-05-21T07:10:00Z",
  "status": "captured",
  "fetched": false,
  "api_calls_today": 2,
  "trigger_reason": "cap=2 reached, calls=2",
  "next_trigger_minutes": null
}
```

**閱讀困難**: 看到 `status="captured"` 會誤以為收盤賠率已取得。實際上 `fetched=false` 且 0 筆賠率。

---

## 3. 提案 Schema（新增欄位，不刪除舊欄位）

向後相容：所有新欄位為附加，不重命名或刪除現有欄位。

| 新欄位 | 類型 | 語義 |
|--------|------|------|
| `heartbeat_written` | boolean | 心跳記錄是否成功寫入磁碟（對應舊 `status="captured"` 的真實語義） |
| `tsl_fetch_attempted` | boolean | 本週期是否呼叫 TSL |
| `tsl_response_received` | boolean | TSL 是否回傳非空回應 |
| `tsl_target_games_found` | integer | TSL 回應中目標 `match_id` 的數量（0 = 來源為空）|
| `tsl_source_empty_for_targets` | boolean | TSL 回應正常但目標賽事缺席 |
| `external_fetch_attempted` | boolean | 是否嘗試呼叫 OddsAPI |
| `external_fetch_blocked_by_quota` | boolean | OddsAPI 是否因 quota 被封鎖 |
| `external_fetch_success` | boolean | OddsAPI 是否成功回傳收盤資料 |
| `external_api_calls_today` | integer | 今日 OddsAPI 呼叫數（明確範圍：OddsAPI only） |
| `closing_odds_captured` | boolean | 是否有至少 1 筆目標賽事的收盤賠率被儲存（舊 `status="captured"` 的應有語義） |
| `source_availability_flags` | dict | 各來源本週期可用性摘要 |

---

## 4. P26K 反向套用示例

**收盤視窗 07:10Z 週期** — 新舊對照：

```json
// 舊 schema（P26K 原始值）
{
  "status": "captured",
  "fetched": false,
  "api_calls_today": 2,
  "trigger_reason": "cap=2 reached, calls=2"
}

// 提案 schema（附加欄位）
{
  "heartbeat_written": true,
  "tsl_fetch_attempted": true,
  "tsl_response_received": true,
  "tsl_target_games_found": 0,
  "tsl_source_empty_for_targets": true,
  "external_fetch_attempted": false,
  "external_fetch_blocked_by_quota": true,
  "external_fetch_success": false,
  "external_api_calls_today": 2,
  "closing_odds_captured": false,
  "source_availability_flags": {
    "TSL": "AVAILABLE_BUT_EMPTY",
    "ODDSAPI_MLB": "BLOCKED_BY_QUOTA"
  }
}
```

**診斷效益**: 新 schema 讓根本原因在單筆記錄中一目了然，無需多 Phase 交叉比對。

---

## 5. 遷移策略

- **向後相容**: 舊欄位保留，新欄位附加
- **歷史記錄**: 新欄位對舊記錄預設為 `null`/`false`
- **無破壞性變更**: 現有消費者繼續讀取 `status`、`fetched`、`api_calls_today` 不受影響

---

## 6. 限制聲明

- 本文件為紙上 Schema 設計，`implementation_status = NOT_IMPLEMENTED`
- 不修改 daemon heartbeat writer、`tsl_snapshot.py`、`daily_closing_capture.py` 任何代碼
- `paper_only=true` | `production_proposal=false`
- 實作需要修改的代碼位置僅作設計參考，不構成實作授權

---

*Artifact: `data/paper_recommendations/p27a_heartbeat_vs_fetch_schema.json`*
