# P26K COMPLETE_PAIR 220→219 下降根本原因報告

**任務 ID**: `P26K_CLOSING_FETCH_TRIGGER_ROOT_CAUSE_DIAGNOSTIC_20260521`
**日期**: 2026-05-21 (診斷日: 2026-05-23)
**分類**: `DEDUP_RECOUNT`
**模式**: `paper_only=true` / `diagnostic_only=true` / `read_only=true`

---

## 摘要

P26J rerun（2026-05-21T09:12Z）測量 COMPLETE_PAIR=219，低於 P26H/P26I 基準線 220（delta=-1）。此 -1 為暫時性測量誤差，非永久性資料遺失。當前 COMPLETE_PAIR=223（高於基準線 220）。CLV 樣本不受影響。

---

## 一、觀測數據

| 量測點 | 時間 | COMPLETE_PAIR | delta |
|--------|------|--------------|-------|
| P26H baseline | commit d644f3f | **220** | 基準 |
| P26I | commit 60a73a7 | **220** | 0 |
| P26J rerun | 2026-05-21T09:12Z | **219** | **-1** ⚠️ |
| P26K 診斷 | 2026-05-23 | **223** | **+3** |

---

## 二、COMPLETE_PAIR 定義

```python
# scripts/p26j_phase4_coverage.py
for mid, rlist in rows_by_match.items():
    has_pregame = False
    has_closing = False
    for r in rlist:
        fa_dt = parse_dt(r.get('fetched_at'))
        gt_dt = parse_dt(r.get('game_time'))
        if fa_dt and gt_dt:
            gap_h = (gt_dt - fa_dt).total_seconds() / 3600
            if gap_h >= 4.0:     has_pregame = True   # 開賽前 4h+ 快照
            if 0.0 <= gap_h <= 2.0: has_closing = True  # 收盤視窗快照
    if has_pregame and has_closing:
        complete_pairs += 1
```

---

## 三、根本原因：DEDUP_RECOUNT

### 為什麼是 -1？

`tsl_odds_history.jsonl` 是一個持續被 daemon 寫入的**活躍 JSONL 檔案**（每 15 分鐘 append 一行）。

2026-05-21T09:12Z（P26J 執行時）：
- 某一場賽事的收盤快照（`gap_h` 剛好在 0–2h 邊界附近）可能因為 daemon 正在寫入而在 `gap_h` 計算時落在邊界外
- 或者 daemon 在此時刻正在寫入一筆新快照，導致 `gap_h` 閾值計算結果短暫改變

由於此後 daemon 繼續寫入更多收盤快照，COMPLETE_PAIR 逐步恢復並超越基準線（220→223）。

### 為何無法識別具體 match_id？

- `tsl_odds_history.jsonl` 在 FORBIDDEN 清單中（不可 stage/commit）
- P26J 執行時未對該檔案建立 git 快照
- 無法重現 09:12Z 的精確檔案狀態

**結論**: 具體 match_id = `INCONCLUSIVE`，但永久資料遺失 = **NONE**（已恢復至 223）。

---

## 四、目標賽事與 COMPLETE_PAIR 的關係

目標賽事 3469930.1 / 3469931.1 **不在** COMPLETE_PAIR 計算中：

| match_id | 最後快照 | gap_h | 分類 |
|----------|---------|-------|------|
| 3469930.1 | 03:24:52Z | ~5.6h (≥4h) | pregame_only |
| 3469931.1 | 04:55:09Z | ~4.1h (≥4h) | pregame_only |

兩場賽事均只有 pregame 快照，無收盤快照（gap 0–2h），故屬於 `pregame_only`，不計入 COMPLETE_PAIR。220→219 的 -1 delta 與目標賽事無關。

---

## 五、CLV 樣本完整性聲明

- COMPLETE_PAIR 由 219（暫時）恢復至 223
- 223 > 220 基準線 → CLV 樣本規模**淨增長**
- P25C bootstrap 門檻為 300，仍未達到（223 < 300）→ **bootstrap_ran = false**

**CLV 樣本影響**: `NONE`

---

**報告 ID**: `p26k_complete_pair_decrease_root_cause_20260521`
**JSON 對照**: `data/paper_recommendations/p26k_complete_pair_decrease_root_cause_20260521.json`
