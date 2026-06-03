# P26D Daemon Restart & Coverage Recheck（Authorized）報告

**Phase**: P26D — Daemon Restart Authorized Execution
**Date**: 2026-05-20
**Classification**: `P26D_DAEMON_RESTARTED_NO_GAMES_IN_WINDOW`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、授權狀態

| 項目 | 狀態 |
|------|------|
| 授權句 | `YES: 授權重啟 odds_capture_daemon` |
| 授權確認 | ✅ **已授權** |

---

## 二、Daemon Restart 結果

| 項目 | 值 |
|------|---|
| Old PID | **1381** |
| New PID | **67442** |
| 重啟時間 | **2026-05-20T13:51 UTC** |
| 重啟結果 | ✅ **SUCCESS** |
| 第一次 tick | 2026-05-20T13:51:06 UTC（Cycle #1）|
| Daemon status | RUNNING（launchd，PID 67442）|

---

## 三、P26B Scheduler Activation 確認

### 核心證據

新 PID 67442 在 13:51 UTC 完成第一次 tick，capture record 顯示：

```json
{
  "timestamp": "2026-05-20T13:51:06Z",
  "windows": {
    "continuous": true,
    "decision": false,
    "pregame": false,
    "closing": false,
    "_wbc_npb_audit": []   ← 鍵存在！P26B 程式碼已載入
  }
}
```

| 指標 | 狀態 |
|------|------|
| `_wbc_npb_audit` key 存在 | ✅ YES |
| 舊版 dict（4 keys）| ❌ NO（已是新版 5 keys）|
| P26B `_load_wbc_npb_game_times()` 生效 | ✅ YES |
| audit entries 數量 | **0**（原因：無場次在 ±2h window）|

---

## 四、Audit 為空的原因

| 分析 | 值 |
|------|---|
| Tick 時間 | 13:51 UTC |
| ±2h window | 11:51 – 15:51 UTC |
| WBC games in window | **0** |
| 最近即將進窗的場次 | 3469710.1（game 17:05 UTC，15:05 進窗）|

P26B 程式碼正確運作。目前只是因為 13:51 UTC 附近沒有 WBC/NPB 開賽，所以 `_wbc_npb_audit` 為空 list（`[]`）。

---

## 五、首批 WBC 場次預計進窗時間

| Match ID | game_time（UTC）| 進窗時間（UTC）| 預計 audit 出現 |
|----------|----------------|--------------|---------------|
| 3469710.1 | 17:05 | **15:05** | ~15:06 tick |
| 3469714.1 | 17:10 | **15:10** | ~15:21 tick |
| 3469709.1 | 17:40 | **15:40** | ~15:51 tick |

→ **約 1h 後**，daemon 的下次 15-min tick 將首次看到 `_wbc_npb_audit` 非空條目。

---

## 六、Coverage Before / After

| Tier | P26C baseline | P26D current | Delta |
|------|--------------|--------------|-------|
| COMPLETE_PAIR | 220 | **220** | **+0** |
| PREGAME_ONLY | 577 | 577 | 0 |
| New rows since restart | — | **4** | — |
| New closing snapshots | — | **0** | — |

---

## 七、P25C Bootstrap

**❌ 未執行** — 220 < 300 threshold，delta = 0。

Daemon 剛重啟，首批 closing snapshots 預計今天 15:05–17:45 UTC 開始累積。

---

## 八、Final Classification

**`P26D_DAEMON_RESTARTED_NO_GAMES_IN_WINDOW`**

Daemon 重啟成功，P26B 程式碼確認生效（`_wbc_npb_audit` key 存在）。
目前無 WBC 場次在 ±2h window → 空 audit，coverage 未變。
預計首批 WBC audit entries ~15:06 UTC 出現，首批 closing snapshots ~17:05 UTC 開始。

---

## 九、Next Steps

```
今天（UTC）：
  15:06 → 第一個 _wbc_npb_audit 非空 entry 預計出現
  17:05–17:45 → 首批 WBC closing snapshot 寫入 tsl_odds_history.jsonl
  
2-3 天後：
  重跑 coverage analysis → 確認 COMPLETE_PAIR delta
  
當 COMPLETE_PAIR >= 300：
  執行 P25C bootstrap rerun（line_comparable=True，seed=42）
```
