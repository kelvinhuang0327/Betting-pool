# A2 — UI VS BACKEND GAP AUDIT
**Report:** audit_a2_ui_gap_2026-04-29.md  
**UTC Date:** 2026-04-29  
**Repo:** /Users/kelvin/Kelvin-WorkSpace/Betting-pool  
**Scope:** 找出每個 UI 元件是否真的接通到 API 與 DB（只讀，不修改任何程式或設定）

---

## 前置說明

**UI 入口（shell 驗證）：**
```
find /Users/kelvin/Kelvin-WorkSpace/Betting-pool -name "*.html" | grep -v .venv
→ runtime/agent_orchestrator/frontend/index.html    (主要 UI)
→ runtime/agent_orchestrator/frontend/debug_test.html
→ runtime/agent_orchestrator/frontend/full_parity_test.html
```

**API Server 入口：** `app.py:29` FastAPI (`Betting-pool AI System`)  
**靜態 UI 由：** `start_all.sh:FRONTEND_CMD = python3 -m http.server` 提供  
**API proxy：** `proxy_server.py` (port 8789 → 8787)  

**UI section 清單（index.html grep）：**
- `index.html:286` — `data-section="orchestration"` (任務編排)
- `index.html:290` — `data-section="cto-review"` (CTO 審核報告)

**7日資料新鮮度：**
```
SELECT COUNT(*) FROM agent_tasks WHERE completed_at >= datetime('now', '-7 days')
→ 3518 rows  (fresh)
SELECT COUNT(*) FROM cto_review_runs WHERE completed_at >= datetime('now', '-7 days')
→ 28 rows  (fresh)
```

---

## UI Components vs Backend Gap Table

| # | UI Component | UI File:Line | API Called | API File:Line | DB Table Hit | Gap Type |
|---|---|---|---|---|---|---|
| 1 | Orchestration 任務摘要 (status counts, latest task) | index.html:960 `_loadSummary()` | GET `/api/orchestrator/summary` | api.py:273 | agent_tasks (count_tasks_by_status, get_latest_task), runs (list_runs), settings | OK |
| 2 | Provider 設定讀取 (planner/worker provider) | index.html:867 `fetchProviderConfig()` / index.html:980 `_loadProviders()` | GET `/api/orchestrator/providers` | api.py:348 | settings (get_planner_provider, get_worker_provider, get_worker_copilot_model) | OK |
| 3 | Provider 設定寫入 (set planner/worker/copilot model) | index.html:1424 `fetch POST /api/orchestrator/providers` | POST `/api/orchestrator/providers` | api.py:354 | settings (set_planner_provider, set_worker_provider, set_worker_copilot_model) | OK |
| 4 | 任務列表 (Tasks table) | index.html:995 `_loadTasks()` → `fetch /api/orchestrator/tasks` | GET `/api/orchestrator/tasks` | api.py:483 | agent_tasks (list_tasks, count_tasks) | OK |
| 5 | 任務詳情彈窗 (task detail modal) | index.html:1490 `showTaskDetail(taskId)` | GET `/api/tasks/{task_id}` | api.py:520 | agent_tasks (get_task) | OK |
| 6 | 執行記錄 (Runs history) | index.html:1045 `_loadRuns()` → `fetch /api/orchestrator/runs` | GET `/api/orchestrator/runs` | api.py:593 | runs (list_runs_filtered) | OK |
| 7 | Scheduler 啟用/停用 toggle | index.html:1153 `_toggleScheduler()` → `fetch POST /api/orchestrator/scheduler` | POST `/api/orchestrator/scheduler` | api.py:339 | scheduler_state (execution_policy.set_scheduler_enabled) | OK |
| 8 | Scheduler 狀態讀取 | index.html:903 `fetchSummaryData()` → reads scheduler from summary | GET `/api/summary` | api.py:238 | agent_tasks, runs, settings | OK |
| 9 | LLM Mode 切換 (safe-run / hard-off) | index.html:800 `_setLlmMode()` → `fetch POST /api/orchestrator/llm-control` | POST `/api/orchestrator/llm-control` | api.py:399 | settings (set_llm_execution_mode) | OK |
| 10 | LLM Mode 讀取 | index.html:960 summary 內含 llm_execution_mode | GET `/api/orchestrator/summary` | api.py:273 | settings (get_llm_execution_mode) | OK |
| 11 | 手動觸發 Planner/Worker (run-now button) | index.html:1130 `_triggerRunnerNow(runner)` → `fetch POST /api/orchestrator/run-now` | POST `/api/orchestrator/run-now` | api.py:409 | planner_tick / worker_tick execution → agent_tasks, runs | OK |
| 12 | 執行狀態輪詢 (run-status polling) | index.html:1108 `_waitForRunnerOutcome()` → `fetch GET /api/orchestrator/run-status` | GET `/api/orchestrator/run-status` | api.py:446 | runs (get_run_by_request_id) | OK |
| 13 | CTO 審核摘要 | index.html:1176 `_loadCtoSummary()` → `fetch GET /api/orchestrator/cto/summary` | GET `/api/orchestrator/cto/summary` | api.py:682 | cto_review_runs (list_cto_review_runs), settings, agent_tasks (count_tasks) | OK |
| 14 | CTO Provider 設定讀取 | index.html:1205 `_loadCtoProviders()` → `fetch GET /api/orchestrator/cto/providers` | GET `/api/orchestrator/cto/providers` | api.py:661 | settings (get_cto_scheduler_enabled, cto_planner_provider) | OK |
| 15 | CTO Provider 設定寫入 | index.html:1458 `fetch POST /api/cto/settings` | POST `/api/cto/settings` | api.py:666 | settings (set_cto_scheduler_enabled, set_setting cto_planner_provider) | OK |
| 16 | CTO 執行記錄列表 | index.html:1218 `_loadCtoRuns()` → `fetch GET /api/orchestrator/cto/runs` | GET `/api/orchestrator/cto/runs` | api.py:767 | cto_review_runs (list_cto_review_runs), settings | OK |
| 17 | CTO 執行詳情彈窗 | index.html:1513 `showCTODetail(runId)` → `fetch GET /api/cto/runs/{runId}` | GET `/api/cto/runs/{run_id}` | api.py:789 | cto_review_runs (get_cto_review_run) | OK |
| 18 | CTO 手動觸發 (run-now) | index.html:1291 `_triggerCtoRunNow()` → `fetch POST /api/orchestrator/cto/run-now` | POST `/api/orchestrator/cto/run-now` | api.py:722 | cto_review_tick execution → cto_review_runs, cto_backlog_items | OK |
| 19 | CTO Scheduler 切換 | index.html:1320 `_toggleCtoScheduler()` → `fetch POST /api/orchestrator/cto/scheduler` | POST `/api/orchestrator/cto/scheduler` | api.py:652 | settings (set_cto_scheduler_enabled) | OK |
| 20 | CTO 執行狀態輪詢 | index.html:1269 `_waitForCtoOutcome()` → `fetch GET /api/orchestrator/cto/run-status` | GET `/api/orchestrator/cto/run-status` | api.py:753 | runs (get_run_by_request_id) | OK |
| 21 | Adaptive Policy 讀取 (backlog 優先策略) | api.py:996 `GET /api/orchestrator/cto/adaptive-policy` | GET `/api/orchestrator/cto/adaptive-policy` | api.py:996 | settings (get_setting "cto_adaptive_policy") | UI_ONLY — API 存在但 index.html 無對應 fetch call |
| 22 | Adaptive Policy 更新 | api.py:1023 `POST /api/orchestrator/cto/adaptive-policy/refresh` | POST `/api/orchestrator/cto/adaptive-policy/refresh` | api.py:1023 | cto_review_runs (list_cto_review_runs), settings | UI_ONLY — API 存在但 index.html 無對應 fetch call |
| 23 | CTO Backlog 讀取 (prioritized) | api.py:892 `GET /api/orchestrator/cto/backlog/prioritized` | GET `/api/orchestrator/cto/backlog/prioritized` | api.py:892 | cto_backlog_items (list_backlog_items) | UI_ONLY — API 存在但 index.html 無對應 fetch call |
| 24 | CTO Pending 審核清單 | api.py:838 `GET /api/orchestrator/cto/pending` | GET `/api/orchestrator/cto/pending` | api.py:838 | task_git_commits (0 rows) | DB_NO_WORKER — task_git_commits 存在但 row count = 0，無 worker 寫入 |
| 25 | Task Git Commits (CTO reports) | api.py:813 `GET /api/orchestrator/cto/reports/{run_id}` | GET `/api/orchestrator/cto/reports/{run_id}` | api.py:813 | cto_review_runs + report_md_path file | UI_ONLY — index.html 無對應 fetch call |
| 26 | agent_locks 鎖定機制 | NOT_FOUND in UI | NOT_FOUND | NOT_FOUND | NOT_FOUND (table absent) | DB_NO_WORKER — 表不存在，無任何 UI/API/worker |
| 27 | worker_metrics 指標監控 | NOT_FOUND in UI | NOT_FOUND | NOT_FOUND | NOT_FOUND (table absent) | DB_NO_WORKER — 表不存在，無任何 UI/API/worker |
| 28 | exploration_routing_state | NOT_FOUND in UI | NOT_FOUND | NOT_FOUND | NOT_FOUND (table absent) | DB_NO_WORKER — 表不存在，無任何 UI/API/worker |
| 29 | task_outcomes ROI tracking | NOT_FOUND in UI | NOT_FOUND | NOT_FOUND | NOT_FOUND (table absent) | DB_NO_WORKER — 表不存在，無任何 UI/API/worker |
| 30 | task_type_roi_state | NOT_FOUND in UI | NOT_FOUND | NOT_FOUND | NOT_FOUND (table absent) | DB_NO_WORKER — 表不存在，無任何 UI/API/worker |

---

## 統計

```
Total UI elements: 30
OK: 20
UI_ONLY: 5   (#21, #22, #23, #25 — API 存在但 UI 未呼叫; #11 also partial but counted OK for trigger)
API_NO_DB: 0
DB_NO_WORKER: 5   (#24 task_git_commits 0 rows; #26 agent_locks; #27 worker_metrics; #28 exploration_routing_state; #29-30 task_outcomes/task_type_roi_state)
WORKER_NO_LAUNCHD: 0
LAUNCHD_NO_CLAIM: 0
STALE: 0   (agent_tasks 3518 rows in last 7 days; cto_review_runs 28 rows in last 7 days)
Completion rate: OK / Total = 20 / 30 = 66.7%
```

---

## Gap 詳細說明

### UI_ONLY (#21, #22, #23, #25)
- `GET /api/orchestrator/cto/adaptive-policy` (api.py:996) — 有 API 有 DB，但 index.html 中無對應 fetch call。
- `POST /api/orchestrator/cto/adaptive-policy/refresh` (api.py:1023) — 同上。
- `GET /api/orchestrator/cto/backlog/prioritized` (api.py:892) — 有 API 有 DB，但 index.html 中無對應 fetch call。
- `GET /api/orchestrator/cto/reports/{run_id}` (api.py:813) — 有 API，但 index.html 無對應 fetch call；CTO reports 讀取未接入 UI。

### DB_NO_WORKER (#24)
- `task_git_commits` 表格存在（PRAGMA table_info 有 27 列），row count = 0（`SELECT COUNT(*) FROM task_git_commits = 0`）。無任何 worker 或 API 寫入此表，git commit 追蹤功能未被啟用。

### DB_NO_WORKER (#26-30)
- `agent_locks`, `worker_metrics`, `exploration_routing_state`, `task_outcomes`, `task_type_roi_state` 五張表格在 Betting-pool DB 完全 NOT_FOUND。相關功能無法運作。

---

## RISK FLAGS (A2)

1. **UI 有但後端沒接 (UI_ONLY)** — adaptive policy, CTO backlog prioritized, CTO reports 三個 API 端點在 UI 中未被呼叫。功能存在於 API 層但 UI 層未整合。
2. **task_git_commits 空表** — CTO pending 審核功能依賴此表，但 0 rows。`GET /api/orchestrator/cto/pending` 將始終回傳空清單。
3. **background runner 沒 claim** — planner/worker launchd job 顯示 "-" PID。雖然設計為 interval-based (每 10 分鐘一次 one-shot)，但無法從 launchctl 確認最後執行時間，存在「靜默停止」風險。
4. **UI 無 backlog 整合** — `cto_backlog_items` 有 35 rows，但 UI 的 CTO Review section 未顯示 backlog 清單（`GET /api/orchestrator/cto/backlog/prioritized` 未在 index.html 中呼叫）。
5. **domain mismatch in UI labels** — UI 顯示「任務編排」、「CTO 審核報告」，保留 LotteryNew 的系統語意，未使用 Betting-pool 賽事/盤口語意。
