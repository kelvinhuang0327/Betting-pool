# P26 TSL Closing Snapshot Coverage Fix 報告

**Phase**: P26 — TSL Closing Snapshot Coverage Diagnosis & Schedule Fix
**Date**: 2026-05-20
**Classification**: `P26_CLOSING_COVERAGE_DIAGNOSTIC_ONLY`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、本輪目標

P25B 發現有效 CLV pairs 只有 220/886 場（24.8%），577 場缺 closing snapshot。
本輪診斷根因並建立 diagnostic closing capture schedule，提出修復路徑，
讓後續 WBC/NPB 場次能在 `game_time ±2h` 內取得 closing snapshot。

---

## 二、P25B Dependency

| 項目 | 值 |
|------|---|
| P25B 結論 | `P25B_WBC_CLV_BOOTSTRAP_RERUN_COMPLETED_INCONCLUSIVE` |
| 有效 CLV pairs | 220 場（pregame ≥4h + closing ±2h） |
| 缺 closing 場次 | 577 場（65.1%） |
| P25B CLV result | mean=+0.076%, 95% CI crosses zero → INCONCLUSIVE |
| 主要阻塞 | closing snapshot 缺口，非 CLV construction |

---

## 三、Closing Gap Root Cause

### 根因分類

| 根因 | 分類 | 嚴重度 |
|------|------|--------|
| `determine_capture_windows()` 不讀 WBC/NPB game_times | **CLOSING_SCHEDULE_NOT_DEFINED** | **PRIMARY** |
| Daemon 對 WBC/NPB 永遠跑 continuous mode，無 closing trigger | **CRAWLER_RUNTIME_NOT_TRIGGERED** | **SECONDARY** |

### 技術細節

`wbc_backend/mlb_data/odds_capture_scheduler.determine_capture_windows()` 讀取的資料來源：

```python
# 現有程式碼（odds_capture_scheduler.py line 97）
timelines = _load_timelines(TIMELINE_PATH)
# TIMELINE_PATH = data/mlb_context/odds_timeline.jsonl
# → 僅含 MLB 場次，不含 WBC/NPB
```

WBC/NPB 場次記錄在 `data/tsl_odds_history.jsonl`，但**從未被 scheduler 讀取**。

結果：
- Closing window（`0 <= delta_minutes <= PREGAME_LEAD_MINUTES=5`）對 WBC/NPB 永遠不觸發
- Daemon 以 15 分鐘固定間隔在 continuous mode 抓取
- 15 分鐘間隔無法保證每場賽事有 ±2h 內的快照

### 數量佐證

| 指標 | 值 |
|------|---|
| 缺 closing 場次數 | 577 |
| 最近一個快照距 2h 窗口的平均 gap | **2.93h** |
| 若只加密 15 分鐘間隔能修復的數量 | **19/577（3.3%）** |
| → 結論 | 加密固定間隔無效，必須加入 game-relative schedule |

---

## 四、Current Coverage

```
Coverage Tier        | Count | Pct
---------------------|-------|------
COMPLETE_PAIR        |   220 | 24.8%  ← 有效 CLV pairs
PREGAME_ONLY         |   577 | 65.1%  ← 缺 closing（可修）
CLOSING_ONLY         |    74 |  8.3%  ← 缺 pregame
NO_VALID_SNAPSHOTS   |    16 |  1.8%
Total                |   887 | 100%
```

### 缺 Closing 的 Game Start Hour 分布（UTC）

```
09:00 UTC  163  ████████████████████████████████  (最多：日本/台灣主場下午場)
23:00 UTC   84  ████████████████
22:00 UTC   65  █████████████
17:00 UTC   52  ██████████
01:00 UTC   40  ████████
20:00 UTC   35  ███████
10:00 UTC   29  █████
00:00 UTC   26  █████
18:00 UTC   22  ████
...
```

09:00 UTC（= 台灣時間 17:00）佔 28.3%，是主要缺口時段。

---

## 五、Proposed Schedule Fix

### 實作方案

```python
# wbc_backend/mlb_data/odds_capture_scheduler.py
# determine_capture_windows() 修改建議

def determine_capture_windows(now=None):
    # 現有：只讀 MLB timeline
    timelines = _load_timelines(TIMELINE_PATH)
    
    # 新增：也讀取 WBC/NPB game manifest
    wbc_game_times = _load_wbc_game_times("data/tsl_odds_history.jsonl")
    
    for game_dt in wbc_game_times:
        delta_minutes = (game_dt - now).total_seconds() / 60.0
        if 0 <= delta_minutes <= PREGAME_LEAD_MINUTES:
            windows["closing"] = True
        if 0 <= delta_minutes <= 30:
            windows["pregame"] = True
```

### Closing Capture Target Offsets

| Offset | Label | 說明 |
|--------|-------|------|
| game_time - 90min | `closing_pre_90min` | 主要 closing snapshot |
| game_time - 30min | `closing_pre_30min` | 備用 closing snapshot |
| game_time + 30min | `closing_post_30min` | Post-game 確認（如 TSL 仍顯示） |

---

## 六、Expected Coverage Lift

| 指標 | Before Fix | After Fix |
|------|-----------|-----------|
| COMPLETE_PAIR matches | 220 (24.8%) | **~797 (89.9%)** |
| 有效 CLV pairs | 220 | **~797** |
| Bootstrap sample size | 2,115 outcomes | **~9,000+ outcomes** |
| Lift | — | **+577 pairs / +65.1pp** |

--- 

## 七、為何仍為 Diagnostic-Only

1. **Live crawler 變更**：修改 `determine_capture_windows()` 會立即影響 production daemon 行為，需要明確授權
2. **Raw data 變更**：新的 closing snapshots 會追加至 `data/tsl_odds_history.jsonl`（live feed file）
3. **需要 2-3 週觀察期**：修復後需累積足夠 closing snapshots 才能重跑 bootstrap
4. **驗證 gate**：新增的 closing snapshot 品質需獨立驗證（確認 fetched_at 確實在 game_time ±2h 內）

---

## 八、Remaining Blockers

1. **授權待確認**：`determine_capture_windows()` 擴充需要明確授權才能部署到 daemon
2. **Bootstrap 重跑需等待**：修復後需 2-3 週 WBC/NPB season 資料才能達到 600+ comparable pairs
3. **MLB 仍阻塞**：MLB pregame-safe = 0（`mlb_odds_2025_real.csv` 全為 post-game proxy）
4. **CLV 可能仍 INCONCLUSIVE**：即使有 797 pairs，market 可能仍然有效（CI crosses zero）

---

## 九、Next Step After Schedule Fix

```
優先序：
1. [NOW]    授權 determine_capture_windows() 擴充（WBC/NPB game manifest 加入）
2. [+2wk]   累積 closing snapshots（目標 600+ complete pairs）
3. [+2wk]   重跑 P25B bootstrap（P25C），確認 INCONCLUSIVE → NEUTRAL/POSITIVE/NEGATIVE
4. [+2wk]   若仍 INCONCLUSIVE：啟動模型品質修復（Brier improvement）
5. [+2mo]   MLB 2026 regular season TSL 收集（4 月起），建立真實 MLB CLV dataset
```

---

## 十、Final Classification

**`P26_CLOSING_COVERAGE_DIAGNOSTIC_ONLY`**

根因已確認，修復路徑清楚，diagnostic schedule 已產出（577 場 proposed captures）。
等待授權後可立即實作 `determine_capture_windows()` 擴充。

---

## 十一、Modified / New Files

| 檔案 | 操作 |
|------|------|
| `scripts/p26_build_tsl_closing_snapshot_schedule.py` | CREATED — diagnostic schedule builder |
| `data/paper_recommendations/p26_tsl_closing_snapshot_schedule_20260520.json` | CREATED — 577 proposed closing captures |
| `data/paper_recommendations/p26_closing_coverage_fix_20260520.json` | CREATED |
| `report/p26_closing_coverage_fix_20260520.md` | CREATED |
| `00-BettingPlan/20260520/p26_closing_coverage_fix_20260520.md` | CREATED |
