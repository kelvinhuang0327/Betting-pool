# P26E Coverage Recheck 報告

**Phase**: P26E — Coverage Recheck After P26D Daemon Restart
**Date**: 2026-05-21
**Classification**: `P26E_COVERAGE_STILL_BELOW_BOOTSTRAP_THRESHOLD`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、Daemon 狀態

| 項目 | 值 |
|------|---|
| 當前 PID | **1715** |
| 最後 heartbeat | 2026-05-21T01:06:52 UTC |
| Daemon 狀態 | ✅ RUNNING |
| P26B code active | ✅ 確認（_wbc_npb_audit key 存在）|

---

## 二、`_wbc_npb_audit` 確認

| 項目 | 值 |
|------|---|
| P26D restart 後 captures | 8 |
| 非空 `_wbc_npb_audit` captures | **3** ✅ |
| closing=True 出現 | ✅ YES |
| pregame=True 出現 | ✅ YES |
| P26B scheduler 實際運作 | ✅ **CONFIRMED** |

### Audit 範例

```
2026-05-20T15:10 UTC:
  3469710.1 費城費城人 @ 辛辛那堤紅人 (game 17:05 UTC, delta=114.2min)
  3469714.1 坦帕灣光芒 @ 巴爾的摩金鶯 (game 17:10 UTC, delta=119.2min)
  → closing=True, trigger_type=["decision","closing"]

2026-05-21T01:06 UTC:
  3469775.1~3469777.1 等 5 場（delta=-82 to -87min，game 已開賽）
  → closing=True
```

---

## 三、Coverage Before / After

| Tier | Before | After | Delta |
|------|--------|-------|-------|
| COMPLETE_PAIR | 220 | **220** | **+0** |
| PREGAME_ONLY | 577 | 577 | 0 |
| New rows since restart | — | 23 | — |
| New closing snapshots | — | **0** | — |

---

## 四、根因：兩個新 Blockers

### Blocker 1：Daemon 間隔過粗（15-min）

P26B 的 closing trigger 運作正確，但 15-min 間隔無法保證每場賽事都有 ±2h 內的快照。

```
3469710.1 game_time 17:05 UTC:
  14:55 UTC 最後快照 → gap = 2.15h（恰在 2h 之外）
  15:10 UTC trigger 時 gap = 1.92h（在 2h 之內）→ 但未被 dedup 通過
```

69 場 `near miss`（最近快照在 2.0-3.0h 之間）。

### Blocker 2：TSL Dedup Filter 阻止 Closing Snapshot 寫入

`data/tsl_snapshot.py::append_tsl_history()` 以 MNL 賠率為 key 進行 dedup：

```python
if odds_key is not None and dedup_state.get(match_id) == odds_key:
    continue  # 跳過：賠率未變
```

當 ±2h closing window 內賠率沒有變動，即使 `closing=True` trigger 已觸發，snapshot 仍不會寫入 `tsl_odds_history.jsonl`。

**Dedup entries**: 829 matches 有記錄，被防重複保護阻止。

---

## 五、P25C Bootstrap

**❌ 未執行** — 220 < 300 threshold，delta = 0

---

## 六、修復方案

### 優先方案 A（最快）：Force-Save Closing Snapshot

**修改 `data/tsl_snapshot.py` 或 `live_odds_collector.py`**：

當 `determine_capture_windows()` 回傳 `closing=True`，強制寫入 closing snapshot，繞過 MNL dedup filter（或加入 `closing_forced=True` flag 標記）。

```python
# 建議修改 append_tsl_history()
def append_tsl_history(..., force_closing: bool = False):
    if odds_key is not None and not force_closing:
        if dedup_state.get(match_id) == odds_key:
            continue  # 只在非強制模式時 skip
```

**預期效果**：69 場 near-miss 可在未來捕捉到 closing snapshot。

### 方案 B：縮短 Daemon 間隔

```bash
# 需授權句：YES: 授權將 daemon interval 從 15min 改為 5min
```

5-min 間隔可確保每場賽事至少一個快照在 ±2h 內。

---

## 七、Final Classification

**`P26E_COVERAGE_STILL_BELOW_BOOTSTRAP_THRESHOLD`**

P26B scheduler 已確認運作（3 capture records with audit），但因 Blocker 1 + Blocker 2，Coverage delta = 0。需修復 dedup filter 才能累積 closing snapshots。

---

## 八、Next Step

```
立即可執行（不需授權）：
P26F_FIX_CLOSING_SNAPSHOT_DEDUP
  修改 data/tsl_snapshot.py
  在 closing window 內 force-save snapshot（繞過 MNL dedup）
  預期：未來 WBC/NPB games 在 ±2h 內有 closing snapshot
  
授權後可執行：
YES: 授權將 daemon interval 從 15min 改為 5min
  降低間隔提高覆蓋率
```
