# P26F Closing Snapshot Dedup Bypass 報告

**Phase**: P26F — Fix Closing Snapshot Dedup
**Date**: 2026-05-21
**Classification**: `P26F_CLOSING_DEDUP_BYPASS_COMPLETED`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、本輪目標

P26E 確認 closing=True trigger 已觸發，但 `append_tsl_history()` 的 MNL dedup
filter 阻止了 closing snapshot 寫入 `tsl_odds_history.jsonl`。
本輪實作 `force_closing` bypass，讓 closing window 內的快照強制寫入。

---

## 二、P26E Blocker 回顧

```
append_tsl_history() 邏輯（修改前）:
  if odds_key == dedup_state[match_id]:
      continue   ← 阻止寫入（即使在 closing window 內）

結果：3469710.1 在 15:10 UTC 有 closing=True trigger，
      但 MNL odds 未變 → snapshot 被 dedup 跳過 → 無 closing snapshot
```

---

## 三、實作摘要

### 呼叫鏈修改（4 個檔案）

```
odds_capture_scheduler.run_scheduled_capture()
  → capture_live_odds(force_closing=windows["closing"])  ← 新增
    → _fetch_tsl_odds(force_closing=...)
      → TSLCrawlerV2.fetch_baseball_games(force_closing=...)
        → save_tsl_snapshot(games=..., source=..., force_closing=...)
          → append_tsl_history(..., force_closing=...)  ← 核心修改
```

### `append_tsl_history()` 修改前後

| 行為 | Before | After |
|------|--------|-------|
| `force_closing=False`（預設）| dedup 照常 | **不變** |
| `force_closing=True` + odds 相同 | 跳過（Bug）| **強制寫入** ✅ |
| `force_closing=True` + odds 不同 | 正常寫入 | 正常寫入（不變）|
| 無 MNL 市場的遊戲 | 永遠寫入 | **不變** |

### Force-saving 時加入 audit 欄位

```json
{
  "force_closing_snapshot": true,
  "capture_reason": "closing_window",
  "dedup_bypassed": true
}
```

---

## 四、Before / After 行為

### Before（P26E root cause）

```
14:55 UTC: 3469710.1 snapshot saved (gap=2.15h, odds=費城費城人:1.58)
15:10 UTC: closing=True trigger fires — but odds unchanged
           → dedup skips → NO snapshot written
           → game_time 17:05 UTC passes without closing snapshot
           → PREGAME_ONLY (not COMPLETE_PAIR)
```

### After（P26F fix）

```
14:55 UTC: 3469710.1 snapshot saved (gap=2.15h, odds=費城費城人:1.58)
15:10 UTC: closing=True → force_closing=True
           → dedup BYPASSED → snapshot force-written
           → gap = 17:05 - 15:10 = 1h55min (inside ±2h)
           → force_closing_snapshot=True, dedup_bypassed=True
           → COMPLETE_PAIR ✅
```

---

## 五、Tests

| 套件 | 結果 |
|------|------|
| `test_p26f_closing_dedup_bypass.py` | ✅ **15/15 PASS** |
| `test_p26b_scheduler_extension.py` | ✅ 16/16 |
| `test_p25_clv_construction_fix.py` | ✅ 21/21 |
| `test_p26_clv_line_aware_matching.py` | ✅ 23/23 |
| P12–P17 governance | ✅ 318/318 |
| **合計** | ✅ **393/393 PASS** |

---

## 六、預期 Coverage 影響

| 項目 | 值 |
|------|---|
| Near-miss matches（closest gap 2-3h）| 69 |
| 若 daemon 重啟並執行 2-3 天 | 預計 +50-69 new COMPLETE_PAIR |
| P25C bootstrap 門檻 | 300 |
| 目前 | 220 |
| 達標時間估計 | 重啟後 2-7 天 |

---

## 七、Daemon Restart 建議

P26F code change 已 commit。但 daemon PID 1715 是 long-running process，
已在 P26F commit 前 import module。

**建議重啟**以確保 force_closing 邏輯生效：
```bash
scripts/manage_daemon.sh restart
```

若不重啟：daemon 在現有 Python session 中無法 reload，force_closing 不會傳遞。

---

## 八、Remaining Blockers

| 優先序 | Blocker | 狀態 |
|--------|---------|------|
| 🟡 1 | Daemon 建議重啟（載入 P26F code）| 需授權或手動執行 |
| 🟡 2 | 等待 2-7 天累積 closing snapshots | 自動進行 |
| 🟡 3 | Coverage 達 300 → P25C bootstrap | 達標後執行 |
| 🟡 4 | Blocker 1（15-min interval）仍存在 | 可考慮降至 5min |

---

## 九、Next Step

```
1. 重啟 daemon（建議授權句：YES: 授權重啟 odds_capture_daemon）
2. 等 2-7 天
3. 執行 P26G coverage recheck
4. 若 COMPLETE_PAIR >= 300 → 執行 P25C bootstrap
```

---

## 十、Final Classification

**`P26F_CLOSING_DEDUP_BYPASS_COMPLETED`**
