# P26D Daemon Restart & Coverage Recheck 報告

**Phase**: P26D — Daemon Restart Authorization Gate
**Date**: 2026-05-20
**Classification**: `P26D_DAEMON_RESTART_AWAITING_AUTHORIZATION`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、授權狀態

| 項目 | 狀態 |
|------|------|
| 授權句 | `YES: 授權重啟 odds_capture_daemon` |
| 本輪收到授權 | ❌ **未授權** |
| 執行模式 | **Readiness-only**，Daemon 未重啟 |

---

## 二、P26B / P26C Dependency

| 項目 | 值 |
|------|---|
| P26B commit | `107535d` — scheduler extension deployed |
| P26C finding | Daemon PID 1381 loaded old code (started before P26B commit) |
| P26C coverage | 220 COMPLETE_PAIR (baseline) |

---

## 三、Daemon 當前狀態

| 項目 | 值 |
|------|---|
| PID | 1381 |
| 啟動時間 | ~12:12 UTC (P26B commit 前 82 分鐘) |
| 最後 heartbeat | **2026-05-20T13:44:13 UTC** |
| P26B commit 後執行 | ✅ YES (13:44 > 13:34) |
| 新程式碼生效 | ❌ NO (old import in memory) |
| `_wbc_npb_audit` 出現 | ❌ NO |

### 13:44 Capture 的關鍵證據

```json
{
  "timestamp": "2026-05-20T13:44:10Z",
  "windows": {
    "continuous": true,
    "decision": false,
    "pregame": false,
    "closing": false
    // ↑ No "_wbc_npb_audit" key → OLD determine_capture_windows() in memory
  }
}
```

P26B 版本的 `determine_capture_windows()` 回傳 dict 包含 `_wbc_npb_audit` 鍵。
**缺少此鍵** = daemon 確實運行舊程式碼。

---

## 四、Daemon 重啟 Readiness

| 項目 | 值 |
|------|---|
| `scripts/manage_daemon.sh` 存在 | ✅ |
| restart 命令 | `scripts/manage_daemon.sh restart` |
| 機制 | `launchctl stop` → `launchctl start` (launchd PList) |
| 效果 | 新 Python process → import P26B 版 `odds_capture_scheduler.py` → `_load_wbc_npb_game_times()` 生效 |
| 第一次 tick 預計 | ~15min 後 |

---

## 五、新增 Snapshot 統計（P26B commit 後）

| 項目 | 值 |
|------|---|
| 新增 rows | 3 |
| 新增 closing snapshots（±2h）| **0** |
| 最新 snapshot | 2026-05-20T13:44:11 UTC |

3 個新 rows 均為 pregame（4-11h before game_time），即使 P26B 已生效也不是 closing。

---

## 六、Coverage Before / After

| Tier | Before (P26C) | After (P26D) | Delta |
|------|--------------|--------------|-------|
| COMPLETE_PAIR | 220 | **220** | **+0** |
| PREGAME_ONLY | 577 | 577 | 0 |
| P25C 門檻 | — | 300 | **-80 pairs** |

→ **P25C bootstrap NOT triggered**（220 < 300，且 delta = 0）

---

## 七、重啟後預期結果

重啟後，daemon 會以 P26B 版程式碼運行。以下場次是最近的候選 closing 場次：

| Match ID | Game Time（UTC）| Hours Away | 預期觸發 |
|----------|----------------|------------|---------|
| 3469709.1 | 2026-05-20T17:40 | ~4h | closing trigger ~15:40-17:45 UTC |
| 3469809.1 | 2026-05-20T22:40 | ~9h | closing trigger ~20:40-22:45 UTC |
| 3469785.1 | 2026-05-21T00:40 | ~11h | closing trigger ~22:40-00:45 UTC |

`_wbc_npb_audit` 將在這些場次進入 ±2h window 時出現。

---

## 八、Final Classification

**`P26D_DAEMON_RESTART_AWAITING_AUTHORIZATION`**

所有重啟 readiness 條件滿足。等待授權句：
`YES: 授權重啟 odds_capture_daemon`
