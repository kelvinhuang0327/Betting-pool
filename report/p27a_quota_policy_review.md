# P27A — OddsAPI Quota 政策審查（紙上提案）

**任務 ID**: P27A  
**父任務**: P26K  
**建立日期**: 2026-05-23  
**模式**: `paper_only=true` | `diagnostic_only=true` | `read_only=true` | `production_proposal=false`

---

## 1. 現況

| 項目 | 值 |
|------|-----|
| 每日上限 | `cap=2` |
| 位置 | `daily_closing_capture.py:164` |
| 邏輯 | `if api_calls_today >= 2: skip` |
| 配額範圍 | OddsAPI MLB 外部收盤（不含 TSL） |
| 狀態儲存 | **in-memory**，daemon 重啟後歸零 |
| 分配策略 | 先到先用（無收盤視窗保留） |

---

## 2. P26K 失敗重建

```
02:09:35Z  — P26G daemon 重啟，api_calls_today 重置為 0
02:07Z     — 1st OddsAPI 呼叫 → api_calls_today = 1
02:24Z     — 2nd OddsAPI 呼叫 → api_calls_today = 2  ← 配額耗盡

07:10Z~08:56Z — 收盤視窗 8 個週期，全部觸發 "cap=2 reached, calls=2"
              → fetched=false
              → 收盤賠率: 0 筆
```

**結論**: 重啟後 15 分鐘內耗盡全日配額，導致收盤視窗完全封鎖。

---

## 3. 失敗模式分析

### 失敗模式 1：重啟狀態遺失（HIGH）
每次 daemon 重啟都會將 `api_calls_today` 歸零，立即重新消耗全日配額。任何重啟日都會重現 P26K 情境。

### 失敗模式 2：先到先用分配（MEDIUM）
沒有收盤視窗保留機制，非收盤時段呼叫可耗盡全部配額。

### 失敗模式 3：cap=2 極低容錯（HIGH）
cap=2 無任何容錯空間。一次重啟或兩次早段呼叫 = 收盤視窗完全黑盒。

---

## 4. 提案政策

### 政策 A：收盤視窗保留（POLICY_A_CLOSING_WINDOW_RESERVE）
在非收盤時段，只允許使用 `cap - 1` 次呼叫。保留最後 1 次給收盤視窗。

```
可用呼叫數（非收盤時段）= cap - calls_reserved_for_closing
calls_reserved_for_closing = 1（若今日仍有未完成的收盤視窗目標）
```

**P26K 情境結果**: 07:10Z 至少有 1 次呼叫可用。

### 政策 B：持久化 Quota 狀態（POLICY_B_PERSIST_QUOTA_STATE）
將 `api_calls_today` 寫入磁碟（`data/mlb_context/external_closing_state.json` 已存在）。  
Daemon 重啟時從磁碟讀取，而非歸零。

```
on_startup:
  today_utc = date.today(utc)
  state = load(external_closing_state.json)
  if state.date == today_utc:
    api_calls_today = state.api_calls_today
  else:
    api_calls_today = 0  # 新的一天，正常歸零
```

**P26K 情境結果**: 02:09Z 重啟後讀到 `api_calls_today = N`（前輪值），不會重新消耗。

### 政策 C：組合方案（推薦）
同時應用政策 B（持久化）+ 政策 A（保留收盤配額）。覆蓋兩種失敗模式。

---

## 5. 建議

**優先**: 政策 C（組合方案）  
**前提確認**: 若 `cap=2` 反映實際 OddsAPI 訂閱等級上限，需先評估升級訂閱的可行性。  
**實作複雜度**: 低至中等。

---

## 6. 限制聲明

- 本文件為紙上政策提案，`implementation_status = NOT_IMPLEMENTED`
- 不修改 `daily_closing_capture.py` 或任何 daemon 代碼
- 不呼叫任何 live odds API
- `paper_only=true` | `production_proposal=false`

---

*Artifact: `data/paper_recommendations/p27a_quota_policy_review.json`*
