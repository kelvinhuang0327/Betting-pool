# P26K 收盤抓取觸發器根本原因診斷 — BettingPlan 摘要

**日期**: 2026-05-21 (診斷日: 2026-05-23)
**分類**: `P26K_SOURCE_STATE_TRULY_EMPTY_CONFIRMED`
**模式**: `paper_only=true` / `read_only=true` / `No real bet`

---

## 執行摘要

2026-05-21 收盤視窗（07:00–09:00 UTC）期間，兩場 NPB 目標賽事收盤賠率未被捕獲。

**診斷結論：系統正常執行，TSL 資料源在收盤視窗前已撤除賭盤。**

---

## 目標賽事

| match_id | 對戰 | 開賽 (UTC) | 收盤快照數 |
|----------|------|-----------|-----------|
| 3469930.1 | 讀賣巨人 vs 養樂多燕子 (NPB) | 09:00Z | **0** |
| 3469931.1 | 廣島東洋鯉魚 vs 橫濱海灣之星 (NPB) | 09:00Z | **0** |

---

## 根本原因

### 主要：SOURCE_STATE_TRULY_EMPTY

TSL 在 03:24Z–04:55Z（距開賽 4–5.6 小時）已將目標賽事從預購賭盤清單移除。

- Daemon 正常運行（每 15 分鐘呼叫 TSL）
- `force_closing=True` 於 07:00–09:00Z 正確激活
- TSL API 回應中已無這兩場賽事

### 次要：QUOTA_HARD_CAP

OddsAPI MLB 外部收盤每日上限 2 次，於 02:24Z 耗盡（P26G daemon 重啟後 15 分鐘內）。

---

## CEO 假設驗證

- `STARTUP_ONLY_FETCH_ARCHITECTURE` 假設：**PARTIALLY_REFUTED**
  - TSL：每 15 分鐘執行（非僅啟動時）
  - OddsAPI：配額耗盡使其「看似」僅啟動時有效，實際根因為 QUOTA_HARD_CAP

---

## 建議行動

| 優先度 | 行動 |
|--------|------|
| 主要 | `SOURCE_AVAILABILITY_MONITOR_REQUIRED` — 偵測 TSL 何時移除賽事並提前捕獲收盤賠率 |
| 次要 | `QUOTA_POLICY_REVIEW_REQUIRED` — OddsAPI 配額管理改善，避免重啟後立即耗盡 |

---

## P26 結案聲明

- **P26K**: CLOSED（根本原因已確認）
- **P26L**: 不需要（根本原因明確，修正屬另一任務）
- **CLV 樣本**: COMPLETE_PAIR=223（高於基準線 220），未受影響

---

**關聯報告**: [report/p26k_closing_fetch_trigger_root_cause_20260521.md](../../report/p26k_closing_fetch_trigger_root_cause_20260521.md)
**關聯 JSON**: [data/paper_recommendations/p26k_closing_fetch_trigger_root_cause_20260521.json](../../data/paper_recommendations/p26k_closing_fetch_trigger_root_cause_20260521.json)
