# P26G Coverage Recheck Post-P26F 報告

**Phase**: P26G — Coverage Recheck After P26F Dedup Bypass + Daemon Restart
**Date**: 2026-05-21
**Classification**: `P26G_FORCE_CLOSING_ROWS_CONFIRMED`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、Daemon Restart 結果

| 項目 | 值 |
|------|---|
| Old PID | **1715** |
| New PID | **15022** |
| 重啟時間 | **2026-05-21T02:09 UTC** |
| 重啟結果 | ✅ SUCCESS |
| 第一次 tick | 2026-05-21T02:09:34 UTC（TSL fetch OK: 7 snapshots）|

---

## 二、P26F force_closing 機制確認

| 指標 | 值 |
|------|---|
| `force_closing_snapshot=True` rows | **10** ✅ |
| `dedup_bypassed=True` rows | **7** ✅ |
| `closing_gap ≤2h` rows | **1** |
| P26F 機制確認 | ✅ **CONFIRMED WORKING** |

### 第一次 tick 詳細

```
2026-05-21T02:09 UTC — TSL fetch OK: 7 snapshots
  → All 10 new rows: force_closing_snapshot=True ✅
  → 7 rows: dedup_bypassed=True (stable odds forced-written)
  → 1 row within ±2h: 3469566.1 (gap=-0.53h)

Capture schedule:
  closing=True, audit_entries=3
  → 3469785.1 delta=-89.6min (closing)
  → 3469787.1 delta=-31.6min (closing)
```

---

## 三、Coverage Before / After

| Tier | P26F baseline | P26G current | Delta |
|------|--------------|--------------|-------|
| COMPLETE_PAIR | 220 | **220** | **+0** |
| PREGAME_ONLY | 577 | 586 | +9 |
| Total matches | 887 | 897 | +10 |

### Coverage Delta = 0 的原因

P26F 機制完全正確，但第一次 tick 的 coverage 未增加，原因：

1. **3469566.1**（gap=-0.53h）— 唯一 ±2h 內的 closing snapshot，但此 match 是新進 TSL 的場次，**無 pregame snapshot（≥4h 之前）** → 不能形成 COMPLETE_PAIR。

2. **其他 forced rows**（3469930.1, 3469931.1 等）— 有 pregame snapshot，但此 tick 時 gap=6.84h（不在 ±2h 窗口）。這些場次需等到 ~07:00 UTC 才進入 closing window。

---

## 四、P25C Bootstrap

**❌ 未執行** — 220 < 300 threshold，delta = 0

---

## 五、今日預期進展

| 場次 | game_time（UTC）| 進窗時間 | 是否有 pregame |
|------|----------------|---------|--------------|
| 3469930.1 | 09:00 UTC | **07:00 UTC** | ✅ YES |
| 3469931.1 | 09:00 UTC | **07:00 UTC** | ✅ YES |

→ 07:00 UTC daemon tick 預計首次產生 forced closing snapshots for games WITH pregame → **+2 COMPLETE_PAIR**（總計 222）

---

## 六、Final Classification

**`P26G_FORCE_CLOSING_ROWS_CONFIRMED`**

P26F 機制完全確認運作（10 force_closing rows, 7 dedup_bypassed）。
Coverage 需繼續累積。預計 2-7 天達到 300+ pairs 門檻。

---

## 七、Remaining Blockers

| 優先序 | Blocker | 說明 |
|--------|---------|------|
| 🟡 1 | Coverage 累積需時 | 預計每天 +5-15 COMPLETE_PAIR，需 5-15 天達 300 |
| 🟡 2 | 15-min interval blocker | 部分場次 closest gap 仍 >2h |
| ⚪ 3 | P25C bootstrap 門檻 | 達 300 後重跑 |
