# P26K OddsAPI api_calls_today 配額耗盡鑑識報告

**任務 ID**: `P26K_CLOSING_FETCH_TRIGGER_ROOT_CAUSE_DIAGNOSTIC_20260521`
**日期**: 2026-05-21 (診斷日: 2026-05-23)
**分類**: `QUOTA_HARD_CAP`
**模式**: `paper_only=true` / `diagnostic_only=true` / `read_only=true`

---

## 摘要

2026-05-21，OddsAPI MLB 外部收盤每日上限（2 次/日）在 daemon 重啟後 15 分鐘內全數耗盡（02:09Z→02:24Z），導致整個收盤視窗（07:10–08:56Z）共 8 個週期全部被 hard cap 攔截。

---

## 一、Hard Cap 程式碼定位

```python
# wbc_backend/mlb_data/daily_closing_capture.py — 第 164 行
if api_calls >= 2:
    logger.warning(
        "Daily closing BLOCKED: daily cap reached (api_calls_today=%d/2)", api_calls
    )
    return {
        "status": "skipped_daily_cap_reached",
        "api_calls_today": api_calls,
        "games_updated": 0,
        "trigger_reason": f"cap=2 reached, calls={api_calls}",
    }
```

- **上限值**: 2 次/日
- **觸發條件**: `api_calls_today >= 2`
- **狀態檔案**: `data/mlb_context/external_closing_state.json`
- **計數器位置**: 第 227 行（`api_calls += 1`，僅在真正發出 HTTP 請求後遞增）

---

## 二、配額耗盡時間線（2026-05-21 UTC）

| 時間 (UTC) | api_calls_today | fetched | 事件 |
|------------|----------------|---------|------|
| 00:00Z (假設) | 0 | false | 新的一天，狀態重置 |
| 01:06Z | 2 | false | 上限已命中（重啟前狀態） |
| 01:21Z–01:51Z | 2 | false | 全部 BLOCKED (3 heartbeats) |
| **02:09:35Z** | — | — | **P26G daemon 重啟，狀態重置** |
| 02:07Z | 1 | false | 第 1 次 OddsAPI 呼叫（重啟後第一個週期） |
| **02:24Z** | **2** | false | **第 2 次呼叫，cap=2 命中** |
| 02:39Z–06:55Z | 2 | false | 全部 BLOCKED（每 15 分鐘） |
| 07:10Z–08:56Z | 2 | false | **收盤視窗 8 個週期：全部 BLOCKED** |

---

## 三、next_trigger_minutes=null 解析

heartbeat 中 `next_trigger_minutes=null` 的技術路徑：

1. `run_scheduled_capture` 呼叫 `run_daily_closing_capture`
2. 返回 `trigger_reason = "cap=2 reached, calls=2"`
3. heartbeat 解析函數嘗試 regex: `r"(\d+\.?\d*)\s*min"` 提取分鐘數
4. `"cap=2 reached, calls=2"` 不含 `min` 子字串 → **regex 返回 None**
5. heartbeat 寫入 `next_trigger_minutes: null`

**結論**: `null` 是 cap 命中時的預期行為，**非 Scheduler bug**。

---

## 四、daemon Heartbeat 欄位解析說明

> ⚠️ **重要澄清**: `fetched` 和 `api_calls_today` 欄位**僅反映 OddsAPI 外部收盤系統**，與 TSL 無關。

| 欄位 | 正確解讀 |
|------|----------|
| `status="captured"` | Heartbeat 已寫入磁碟；**不代表任何賠率被抓取** |
| `fetched=false` | OddsAPI 外部收盤本日未成功取得資料；**TSL 仍在正常執行** |
| `api_calls_today=2` | OddsAPI 呼叫上限命中；**不反映 TSL 呼叫次數** |
| `next_trigger_minutes=null` | Reason 字串無分鐘數，regex 無匹配；**非 bug** |

---

## 五、建議行動

**分類**: `QUOTA_POLICY_REVIEW_REQUIRED`

建議改進方向（此為 read_only 診斷，不實作）：

1. **保留 1 次收盤配額**: 新增邏輯，在 `api_calls >= 1` 時若現在是收盤視窗（T-15min 前），優先保留此次呼叫
2. **防止重啟後立即消耗配額**: daemon 重啟後，延遲第一次 OddsAPI 呼叫至非緊急時段
3. **提高每日配額上限**: 若服務方案允許，從 2 次/日提升至更高值
4. **監控配額消耗**: 加入配額即將耗盡的警報機制（如 api_calls >= 1 時發 Telegram 通知）

---

**報告 ID**: `p26k_api_calls_forensics_20260521`
**JSON 對照**: `data/paper_recommendations/p26k_api_calls_forensics_20260521.json`
