# P26K 收盤抓取觸發器根本原因診斷報告

**任務 ID**: `P26K_CLOSING_FETCH_TRIGGER_ROOT_CAUSE_DIAGNOSTIC_20260521`
**日期**: 2026-05-21 (診斷日: 2026-05-23)
**模式**: `paper_only=true` / `diagnostic_only=true` / `read_only=true`
**主軸對齊**: `axis_2_clv_validation_precondition`
**最終分類**: `P26K_SOURCE_STATE_TRULY_EMPTY_CONFIRMED`

---

## 摘要

2026-05-21 收盤視窗 (07:00–09:00 UTC) 期間，兩場 NPB 目標賽事 (`3469930.1` 讀賣巨人 vs 養樂多燕子、`3469931.1` 廣島東洋鯉魚 vs 橫濱海灣之星) 的收盤賠率未被捕獲。

**主要根本原因**: `SOURCE_STATE_TRULY_EMPTY` — TSL 在收盤視窗開放前，已將目標 NPB 賽事從預購賭盤中撤除。

**次要根本原因**: `QUOTA_HARD_CAP` — OddsAPI MLB 外部收盤每日上限 2 次，已在 daemon 重啟後 15 分鐘內（02:09–02:24Z）全數耗盡。

---

## 第一部分：目標賽事

| 欄位 | 值 |
|------|-----|
| match_id_1 | `3469930.1` 讀賣巨人 vs 養樂多燕子 |
| match_id_2 | `3469931.1` 廣島東洋鯉魚 vs 橫濱海灣之星 |
| 聯賽 | NPB |
| 開賽時間 (UTC) | 2026-05-21T09:00:00Z |
| 開賽時間 (台北) | 2026-05-21 17:00 +08:00 |
| 預期收盤視窗 | 07:00–09:00Z (T-120min 至 T-0min) |

---

## 第二部分：TSL 收盤失敗分析（主要根本原因）

### 2.1 最後快照時間點

| match_id | 最後 TSL 快照 | 距開賽時間 | 分類 |
|----------|--------------|------------|------|
| 3469930.1 | 2026-05-21T03:24:52Z | T-335min (~5.6h) | pregame_only |
| 3469931.1 | 2026-05-21T04:55:09Z | T-245min (~4.1h) | pregame_only |

收盤視窗 (07:00–09:00Z) 期間：**兩場賽事皆 0 筆快照**。

### 2.2 TSL Daemon 執行狀態（確認正常運作）

- TSL crawler 每 15 分鐘被呼叫一次（透過 `capture_live_odds` → `_fetch_tsl_odds`）
- `determine_capture_windows()` 確認在 07:00–09:00Z 期間設 `force_closing=True`（`delta_minutes ≤ 120min`）
- P26F dedup bypass 已激活（`force_closing=True` 時跳過 MNL 去重）
- **結論**：Daemon 執行路徑正確無誤，但 TSL API 回傳結果中已不含這兩場賽事

### 2.3 根本原因分類

**`SOURCE_STATE_TRULY_EMPTY`** — TSL 在 03:24Z–04:55Z 之間，將這兩場 NPB 賽事從預購賭盤清單中移除，早於收盤視窗約 4–5.6 小時。

> **P26J 標籤退役聲明**: `TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED` 標籤已退役。
> 精確描述為 `TSL_PREGAME_LIST_CLEARED_BEFORE_CLOSING_WINDOW`。
> TSL 系統仍在運行且被呼叫；問題在於特定賽事的資料已不再提供，而非 TSL 整體不可用。

---

## 第三部分：OddsAPI 配額耗盡分析（次要根本原因）

### 3.1 每日上限機制

```python
# wbc_backend/mlb_data/daily_closing_capture.py:164
if api_calls >= 2:
    return {"status": "skipped_daily_cap_reached", "trigger_reason": f"cap=2 reached, calls={api_calls}"}
```

### 3.2 配額耗盡時間線

| 時間 (UTC) | api_calls_today | 狀態 |
|------------|----------------|------|
| 01:00–01:51Z | 2 | 上限已到 (重啟前) |
| 02:09:35Z | — | P26G daemon 重啟，狀態重置 |
| 02:07Z | 1 | 第 1 次 OddsAPI 呼叫 |
| 02:24Z | 2 | 第 2 次呼叫，**上限命中** |
| 07:10–08:56Z | 2 | **全部 8 個收盤週期：BLOCKED** |

### 3.3 Heartbeat 欄位澄清

| 欄位 | 實際含義 | 常見誤解 |
|------|----------|----------|
| `status="captured"` | Heartbeat 已寫入 | ≠ 賠率已抓取 |
| `fetched=false` | OddsAPI 外部收盤未成功 | ≠ TSL 未執行 |
| `api_calls_today=2` | OddsAPI 上限命中 | ≠ TSL 呼叫次數 |
| `next_trigger_minutes=null` | Reason 字串無分鐘數，regex 無匹配 | ≠ Scheduler bug |

`next_trigger_minutes=null` 的技術原因：heartbeat 解析 `trigger_reason` 使用 regex `(\d+\.?\d*)\s*min`。當 reason 為 `"cap=2 reached, calls=2"` 時，無任何分鐘數字串，故 regex 返回 null。**屬於預期行為，非 bug**。

---

## 第四部分：CEO 假設驗證

**CEO 假設**: `STARTUP_ONLY_FETCH_ARCHITECTURE`（收盤抓取僅在 daemon 啟動時觸發）

| 系統 | 驗證結果 |
|------|----------|
| TSL | **REFUTED** — TSL 每 15 分鐘執行一次（非僅在啟動時）|
| OddsAPI | **PLAUSIBLE_NOT_PROVED** — 2 次呼叫在重啟後立即耗盡，造成啟動時專用的外觀；實際根本原因為 QUOTA_HARD_CAP |

**整體狀態**: `PARTIALLY_REFUTED`

---

## 第五部分：P26 階段終點聲明

| 項目 | 狀態 |
|------|------|
| P26K 根本原因識別 | ✅ 已完成 |
| P26L 是否必要 | ❌ 不需要（根本原因已確認，修正屬於另一任務） |
| 可行動性 | ✅ Actionable |
| 主要建議行動 | `SOURCE_AVAILABILITY_MONITOR_REQUIRED` |
| 次要建議行動 | `QUOTA_POLICY_REVIEW_REQUIRED` |

---

## 第六部分：CLV 樣本完整性聲明

| 量測點 | COMPLETE_PAIR 數 |
|--------|----------------|
| P26H/P26I baseline | 220 |
| P26J rerun (09:12Z) | 219 (暫時性 -1) |
| 當前 (P26K 診斷後) | **223** |

COMPLETE_PAIR 目前為 223（高於基準線 220），CLV 樣本未受損。目標賽事 3469930.1/3469931.1 因無收盤快照，分類為 `pregame_only`，不計入 COMPLETE_PAIR。

---

**報告 ID**: `p26k_closing_fetch_trigger_root_cause_20260521`
**JSON 對照**: `data/paper_recommendations/p26k_closing_fetch_trigger_root_cause_20260521.json`
