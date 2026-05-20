# P26B Scheduler Extension — Readiness Report

**Phase**: P26B — Scheduler Extension Authorization Gate
**Date**: 2026-05-20
**Classification**: `P26B_SCHEDULER_EXTENSION_READY_AWAITING_AUTHORIZATION`
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 一、本輪目標

在明確授權後，擴充 `determine_capture_windows()` 讓 scheduler 能讀取 WBC/NPB
`game_times`，並在 `game_time` 附近觸發 closing capture，把有效 CLV pairs
從 220 → 797（+65.1pp）。

---

## 二、授權狀態

| 項目 | 狀態 |
|------|------|
| 授權句 | `YES: 授權擴充 determine_capture_windows() 讀取 WBC/NPB game_times` |
| 本輪收到授權 | ❌ **未授權** |
| 執行模式 | **Readiness-only**，不修改 scheduler code |

---

## 三、P26 Root Cause 摘要

| 層級 | 根因 | 說明 |
|------|------|------|
| PRIMARY | `CLOSING_SCHEDULE_NOT_DEFINED` | `determine_capture_windows()` 只讀 `data/mlb_context/odds_timeline.jsonl`（MLB）；WBC/NPB game_times 完全不在 scheduler 視野內 |
| SECONDARY | `CRAWLER_RUNTIME_NOT_TRIGGERED` | 15-min 固定間隔只能偶然覆蓋 19/577 場（3.3%）；avg missing gap = 2.93h |

---

## 四、Implementation Summary（設計完成，等待授權）

### 新增函式：`_load_wbc_npb_game_times()`

```python
# wbc_backend/mlb_data/odds_capture_scheduler.py (proposed)
def _load_wbc_npb_game_times(
    source_path: Path = Path("data/tsl_odds_history.jsonl"),
    lookahead_hours: float = 48.0,
    now: datetime | None = None,
) -> list[datetime]:
    """Load upcoming WBC/NPB game times. Gracefully returns [] on any failure."""
    if not source_path.exists():
        return []
    if now is None:
        now = datetime.now(timezone.utc)
    cutoff = now + timedelta(hours=lookahead_hours)
    seen: set[str] = set()
    game_times: list[datetime] = []
    try:
        for line in source_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            mid = str(row.get("match_id", ""))
            if mid in seen:
                continue  # Deduplicate per match
            seen.add(mid)
            gt = _parse_ts_utc(row.get("game_time", ""))
            if gt and now <= gt <= cutoff:
                game_times.append(gt)
    except OSError:
        return []
    return game_times
```

### `determine_capture_windows()` 擴充

```python
# 現有 MLB logic (unchanged)
for tl in timelines.values():
    ct = parse_ts(tl.commence_time)
    ...  # 原邏輯不動

# NEW: WBC / NPB extension (additive only)
wbc_game_times = _load_wbc_npb_game_times(now=now)
audit_details: list[dict] = []

for gt in wbc_game_times:
    delta_minutes = (gt - now).total_seconds() / 60.0
    if delta_minutes < -120:          # >2h after game start → skip
        continue
    triggered: list[str] = []
    if DECISION_LEAD_MINUTES <= delta_minutes <= DECISION_LEAD_MINUTES + 60:
        windows["decision"] = True
        triggered.append("decision")
    if 0 <= delta_minutes <= 30:
        windows["pregame"] = True
        triggered.append("pregame")
    if -120 <= delta_minutes <= PREGAME_LEAD_MINUTES:
        windows["closing"] = True
        triggered.append("closing")
    if triggered:
        audit_details.append({
            "source": "tsl_odds_history",
            "game_time": gt.isoformat(),
            "minutes_to_game": round(delta_minutes, 1),
            "trigger_type": triggered,
            "trigger_reason": f"WBC/NPB game_time triggered: {triggered}",
        })

windows["_audit_details"] = audit_details
return windows
```

---

## 五、WBC / NPB Schedule Source

| 優先序 | Source | 說明 |
|--------|--------|------|
| 1 | `data/tsl_odds_history.jsonl` | Live feed，即時更新，有 `game_time` + `match_id` |
| 2 | `data/paper_recommendations/p26_tsl_closing_snapshot_schedule_20260520.json` | Diagnostic schedule（577 場），可作 backfill |

`tsl_odds_history.jsonl` 欄位確認：
- `match_id` ✅
- `game_time` ✅（含 timezone，如 `2026-03-13T12:00:00+08:00`）
- `home_team_name` / `away_team_name` ✅

---

## 六、Trigger Window Rules

| Window | Rule（delta_minutes = game_time - now）| 說明 |
|--------|----------------------------------------|------|
| `decision` | `60 ≤ delta ≤ 120` | 2-3h 前觸發 decision capture |
| `pregame` | `0 ≤ delta ≤ 30` | 開賽前 30min 觸發 pregame capture |
| `closing` | `-120 ≤ delta ≤ 5` | 開賽前 5min 至開賽後 2h（確保 closing snapshot 被捕捉）|

---

## 七、Backward Compatibility

| 項目 | 保證 |
|------|------|
| MLB timeline 邏輯 | ✅ 完全不變（additive extension） |
| `tsl_odds_history.jsonl` 不存在 | ✅ `wbc_game_times = []`，graceful degradation |
| OSError / parse failure | ✅ return `[]`，scheduler 不 crash |
| Return dict schema | ✅ 保留 `continuous/decision/pregame/closing` 鍵；新增 `_audit_details` |
| Downstream `should_capture_now()` | ✅ 不需改動（`any(windows.values())` 仍有效） |

---

## 八、Tests Designed（10 cases，等待授權後建立）

| # | Test | Expected |
|---|------|----------|
| 1 | MLB existing behavior preserved (no WBC file) | decision/pregame/closing unchanged |
| 2 | WBC game at T-90min | `decision=True` |
| 3 | WBC game at T-30min | `pregame=True` |
| 4 | WBC game at T-5min | `closing=True` |
| 5 | WBC game at T+30min | `closing=True`（within -120min window）|
| 6 | WBC game at T+3h | no trigger（`delta < -120`）|
| 7 | Missing `tsl_odds_history.jsonl` | no crash, `wbc_game_times=[]` |
| 8 | NPB game uses identical logic | same as WBC |
| 9 | MLB window unaffected when WBC game present | both trigger independently |
| 10 | `_audit_details` populated on WBC trigger | non-empty list with trigger_reason |

---

## 九、Risks

| 風險 | 嚴重度 | 緩解方案 |
|------|--------|----------|
| `tsl_odds_history.jsonl` 過大（I/O 每 15min）| LOW | 只讀最後 N 行（e.g., 最後 2000 行），或改用獨立 game manifest |
| Game timezone 解析錯誤 | LOW | `dateutil.parser.parse` 已處理 `+08:00`，並轉換 UTC |
| Match 重複（同 match_id 多行）| NONE | `seen` set dedup |
| Closing window 延伸至 -120min | LOW | TSL 通常在賽後 30min 停止顯示，不會浪費 API 資源 |

---

## 十、Next Step After Authorization

```
授權後立即可執行：
1. 在 wbc_backend/mlb_data/odds_capture_scheduler.py 實作擴充
2. 建立 tests/test_p26b_scheduler_extension.py（10 test cases）
3. 執行 pytest 全套驗證
4. Commit → daemon 下次執行（≤15min）立即生效
5. 觀察 data/tsl_odds_history.jsonl：
   - 確認 game_time ±2h 內開始出現新快照
   - 目標 2 週內達到 600+ complete CLV pairs
6. 重跑 P25B bootstrap（P25C）
```

---

## 十一、Final Classification

**`P26B_SCHEDULER_EXTENSION_READY_AWAITING_AUTHORIZATION`**

Implementation design 完成，data source 確認可用，backward compatibility 低風險。
等待授權句：`YES: 授權擴充 determine_capture_windows() 讀取 WBC/NPB game_times`
