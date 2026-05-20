# P26C Closing Coverage Monitor 報告

**Phase**: P26C — Monitor TSL Closing Coverage Lift
**Date**: 2026-05-20
**Classification**: `P26C_MONITORING_CONTINUES_INSUFFICIENT_NEW_PAIRS`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、本輪目標

監控 P26B scheduler extension（commit `107535d`）是否實際觸發 WBC/NPB closing
capture，統計新增的 closing snapshots，確認 CLV pair coverage 是否達到 300+
以啟動 P25C bootstrap rerun。

---

## 二、P26B Dependency

| 項目 | 狀態 |
|------|------|
| P26B commit | `107535d` (2026-05-20T13:34:58 UTC) |
| Scheduler extension | ✅ deployed (`odds_capture_scheduler.py`) |
| Tests | ✅ 16/16 PASS |
| Expected effect | WBC/NPB game_time ±2h → closing=True |

---

## 三、Daemon Monitoring Result

### 關鍵發現：Daemon 載入舊程式碼

| 項目 | 值 |
|------|---|
| Daemon PID | 1381 |
| Daemon 啟動時間（UTC）| **2026-05-20T12:12** |
| P26B commit 時間（UTC）| **2026-05-20T13:34** |
| 最後 heartbeat（UTC）| **2026-05-20T13:29** |
| Daemon 在 P26B commit 後執行 | ❌ **NO** |
| 新程式碼是否生效 | ❌ **NO** |

### 根本原因

```
odds_capture_daemon.py 是長期執行進程（long-running process）。
Python 模組在進程啟動時一次性 import，之後不會自動 reload。

Daemon 啟動於 12:12 UTC → import 了 P26B commit (13:34 UTC) 之前的舊版
odds_capture_scheduler.py → _load_wbc_npb_game_times() 函式不在記憶體中。

即使 daemon 在 13:29 執行了一次 tick（記錄在 heartbeat），
也是用舊程式碼，不會觸發 WBC/NPB closing window。
```

### 必要動作

```bash
# 重啟 daemon 以載入 P26B 新程式碼
scripts/manage_daemon.sh restart
# 或
kill 1381  # 讓 launchd 自動重啟
```

---

## 四、新增 Snapshot 統計

| 項目 | 值 |
|------|---|
| P26B commit 後新增 rows | **0** |
| 新增 closing snapshots（game_time ±2h）| **0** |
| `_wbc_npb_audit` entries（capture schedule 中）| **0** |
| closing=True captures since P26B | **0** |

---

## 五、CLV Pair Coverage Before / After

| Tier | Before（P25B baseline）| After（P26C current）| Delta |
|------|----------------------|---------------------|-------|
| COMPLETE_PAIR | 220 | **220** | **+0** |
| PREGAME_ONLY | 577 | 577 | 0 |
| CLOSING_ONLY | 74 | 74 | 0 |
| NO_VALID_SNAPSHOTS | 16 | 16 | 0 |

**Coverage 完全未變（daemon 尚未使用新程式碼）。**

---

## 六、是否達到 300+ Pairs

| 項目 | 值 |
|------|---|
| 目前 complete CLV pairs | 220 |
| P25C bootstrap 門檻 | 300 |
| 差距 | **-80 pairs** |
| P25C bootstrap 啟動 | ❌ **不啟動** |

---

## 七、是否執行 P25C Bootstrap

**❌ 未執行** — 理由：
- current complete pairs = 220（低於 300 threshold）
- delta = 0（daemon 尚未以新程式碼執行）
- 過早重跑 bootstrap 結果與 P25B 完全相同，無意義

---

## 八、目前 Blocker

| 優先序 | Blocker | 行動 |
|--------|---------|------|
| 1 | **Daemon 需重啟**（載入 P26B 新程式碼）| `scripts/manage_daemon.sh restart` |
| 2 | **等待資料累積**（2-3 週）| 重啟後，daemon 在 WBC/NPB game_time ±2h 自動抓 closing |
| 3 | **Coverage 差距 80 pairs**（220 → 300）| 最快幾天後可重查 |
| 4 | **MLB 仍阻塞**（pregame-safe = 0）| 2026 regular season 後 |

---

## 九、Next Step

```
立即：
  scripts/manage_daemon.sh restart
  → daemon 重新 import 新版 odds_capture_scheduler.py
  → _load_wbc_npb_game_times() 生效

驗證（重啟後 ~30min）：
  tail -f data/mlb_context/odds_capture_schedule.json
  → 確認有 _wbc_npb_audit 條目或 closing=True

等待 2-3 天：
  重跑 p26_build_tsl_closing_snapshot_schedule.py
  → 確認 COMPLETE_PAIR >= 300
  → 啟動 P25C bootstrap rerun
```

---

## 十、Final Classification

**`P26C_MONITORING_CONTINUES_INSUFFICIENT_NEW_PAIRS`**

P26B extension 已部署，但 daemon 因為是 long-running process 而載入舊程式碼。
**需重啟 daemon**。重啟後，2-3 天應能累積足夠 closing snapshots 達到 300+ pairs 門檻。
