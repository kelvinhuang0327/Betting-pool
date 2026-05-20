# A1 — BACKEND 現況 AUDIT
**Report:** audit_a1_backend_2026-04-29.md  
**UTC Date:** 2026-04-29  
**Repo:** /Users/kelvin/Kelvin-WorkSpace/Betting-pool  
**Scope:** 後端排程系統實體狀態盤點（只讀，不修改任何程式或設定）

---

## A1.1 DB Schema 盤點

**DB 路徑（shell 驗證）：**
```
find /Users/kelvin/Kelvin-WorkSpace/Betting-pool -name "*.db" | grep -v .venv
→ /Users/kelvin/Kelvin-WorkSpace/Betting-pool/runtime/agent_orchestrator/orchestrator.db
→ /Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/bankroll_v3.db
→ /Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/baseball_knowledge_graph.db
```

**主要 Orchestrator DB：** `runtime/agent_orchestrator/orchestrator.db`

**全部 table 清單（`.tables` 原始輸出）：**
```
adaptive_policy_state    cto_intent_signals       settings
agent_task_runs          cto_review_runs          task_git_commits
agent_task_runs_archive  cto_settings             task_git_reviews
agent_tasks              planner_dedupe_state     tasks
agent_tasks_archive      runs                     
cto_backlog_items        scheduler_state
```

### LotteryNew 期望表格 vs Betting-pool 實際狀態

| Table | Exists? | Column Evidence (PRAGMA table_info) | Row Count |
|---|---|---|---|
| agent_tasks | YES | id,slot_key,date_folder,title,slug,status,previous_task_id,prompt_file_path,prompt_text,completed_file_path,completed_text,changed_files_json,worker_pid,started_at,completed_at,duration_seconds,error_message,created_at,updated_at,dedupe_key,regime_state,confidence_snapshot,epoch_id,contract_json,focus_keys,signal_state_type,expected_duration_hours,track (27 cols) | 3522 |
| agent_locks | NOT_FOUND | — | NOT_FOUND |
| planner_dedupe_state | YES | dedupe_key,last_regime_state,last_confidence,last_task_id,last_emitted_at,skip_count,updated_at (7 cols) | 1 |
| task_git_commits | YES | id,task_id,task_key,task_title,source_branch,commit_sha,commit_message,integration_group,review_priority,safe_to_autocommit,status,reviewer_role,reviewed_at,merge_branch,merge_commit_sha,reject_reason,superseded_by_task_id,superseded_by_commit_sha,changed_files_json,depends_on_tasks_json,depends_on_commits_json,high_conflict_paths_json,task_status,gate_verdict,gate_reason,created_at,updated_at (27 cols) | 0 |
| exploration_routing_state | NOT_FOUND | — | NOT_FOUND |
| worker_metrics | NOT_FOUND | — | NOT_FOUND |
| scheduling_state | NOT_FOUND | — | NOT_FOUND |
| task_outcomes | NOT_FOUND | — | NOT_FOUND |
| task_type_roi_state | NOT_FOUND | — | NOT_FOUND |

### 其他與排程相關的表格

| Table | Exists? | Column Evidence | Row Count |
|---|---|---|---|
| agent_task_runs | YES | (archive table) | 13449 |
| agent_task_runs_archive | YES | (archive table) | included above |
| agent_tasks_archive | YES | (archive of agent_tasks) | included above |
| tasks | YES | (legacy simple task table) | 134 |
| scheduler_state | YES | id,enabled,interval_minutes,next_planner_run_at,next_worker_run_at,updated_at (6 cols) | 1 |
| runs | YES | (execution run log) | UNKNOWN — not queried |
| cto_review_runs | YES | id,run_id,frequency_mode,started_at,completed_at,duration_seconds,checked_from,checked_until,candidate_count,approved_count,merged_count,rejected_count,deferred_count,superseded_count,duplicate_count,merge_branch,report_md_path,report_json_path,summary,dedupe_key,is_manual,is_force_run,run_intent,parent_run_id,created_at,updated_at,epoch_id (27 cols) | 31 |
| cto_backlog_items | YES | id,finding_id,cto_run_id,source,severity,impact_score,urgency,category,title,description,file_path,line_number,status,priority_score,assigned_to,estimated_hours,task_id,resolution_notes,created_at,updated_at,completed_at,epoch_id (22 cols) | 35 |
| adaptive_policy_state | YES | id,retry_coverage_limit,retry_merge_rate,override_merge_rate,compare_approved_rate,overall_merge_rate,category_priority_boosts,suggestions,policy_confidence,runs_analyzed,computed_at (11 cols) | 1 |

**注意：** `agent_locks`, `worker_metrics`, `scheduling_state`, `task_outcomes`, `task_type_roi_state`, `exploration_routing_state` 六張表格在 LotteryNew DB 中存在，但在 Betting-pool DB 中 **NOT_FOUND**。

---

## A1.2 排程程式檔

| Expected Role | Actual File / Line Evidence | Called By Entry Point? |
|---|---|---|
| planner_tick | `orchestrator/planner_tick.py:959` — `def run_planner_tick() -> dict:` | YES — `app.py:183` `@app.post("/api/system/trigger/planner")` 調用；launchd `com.bettingpool.orchestrator.planner` 調用 `scripts/launchd/run_planner_tick.sh` |
| worker_tick | `orchestrator/worker_tick.py:505` — `def run_worker_tick() -> dict:` | YES — `app.py:194` `@app.post("/api/system/trigger/worker")` 調用；launchd `com.bettingpool.orchestrator.worker` 調用 `scripts/launchd/run_worker_tick.sh` |
| planner_decision | NOT_FOUND — 無 `orchestrator/planner_decision.py`；決策邏輯內嵌於 `planner_tick.py` | NOT_FOUND |
| light_worker | NOT_FOUND — 無 `orchestrator/light_worker_tick.py`；`optional_worker_daemon.py` 存在但非 light worker（呼叫 `run_worker_tick`，不是獨立 light 任務） | NOT_FOUND |
| copilot_daemon | `orchestrator/copilot_daemon.py:356` — `def run_once() -> str:`；`copilot_daemon.py:461` — `def serve_forever(...)` | YES — launchd `com.bettingpool.orchestrator.copilot-daemon` 調用 `scripts/launchd/run_copilot_daemon.sh` |
| fallback_handler | NOT_FOUND — Betting-pool planner_tick.py 無 Fallback P1-P6 邏輯（grep "fallback" 返回空） | NOT_FOUND |
| validation_router | NOT_FOUND — 無獨立 validation_router 模組；無 WORTH_VALIDATION / exploration_routing_state | NOT_FOUND |
| cto_review | `orchestrator/cto_review_tick.py:230` — `def run_cto_review_tick(run_id, force)` | YES — `app.py:209` `@app.post("/api/system/trigger/cto")` 調用；launchd `com.bettingpool.orchestrator.worker-daemon` 執行中 |

---

## A1.3 API Endpoints

**grep 來源：** `app.py` + `orchestrator/api.py`

| Endpoint | Method | File:Line | Related Component |
|---|---|---|---|
| `/` | GET | app.py:91 | health redirect |
| `/health` | GET | app.py:107 | health check |
| `/api/system/info` | GET | app.py:140 | system info |
| `/api/system/trigger/planner` | POST | app.py:172 | planner_tick 手動觸發 |
| `/api/system/trigger/worker` | POST | app.py:183 | worker_tick 手動觸發 |
| `/api/system/trigger/cto` | POST | app.py:194 | cto_review_tick 手動觸發 |
| `/api/summary` | GET | api.py:238 | 任務摘要（讀 agent_tasks） |
| `/api/orchestrator/summary` | GET | api.py:273 | 詳細摘要（alias） |
| `/api/scheduler` | GET | api.py:332 | scheduler_state 讀取 |
| `/api/orchestrator/scheduler` | GET | api.py:333 | alias |
| `/api/scheduler/enable` | POST | api.py:338 | 啟用/停用排程 |
| `/api/orchestrator/scheduler` | POST | api.py:339 | alias |
| `/api/providers` | GET | api.py:347 | provider 設定讀取 |
| `/api/orchestrator/providers` | GET | api.py:348 | alias |
| `/api/providers` | POST | api.py:353 | provider 設定寫入 |
| `/api/orchestrator/providers` | POST | api.py:354 | alias |
| `/api/runtime-mode` | GET | api.py:377 | 執行模式讀取 |
| `/api/orchestrator/runtime-mode` | GET | api.py:378 | alias |
| `/api/runtime-mode` | POST | api.py:383 | 執行模式寫入 |
| `/api/orchestrator/runtime-mode` | POST | api.py:384 | alias |
| `/api/llm-control` | GET | api.py:392 | LLM 控制讀取 |
| `/api/orchestrator/llm-control` | GET | api.py:393 | alias |
| `/api/llm-control` | POST | api.py:398 | LLM 控制寫入 |
| `/api/orchestrator/llm-control` | POST | api.py:399 | alias |
| `/api/orchestrator/run-now` | POST | api.py:409 | 立即執行 planner/worker |
| `/api/orchestrator/run-status` | GET | api.py:446 | 執行狀態查詢 |
| `/api/tasks` | GET | api.py:464 | 任務列表（agent_tasks） |
| `/api/orchestrator/tasks` | GET | api.py:483 | alias |
| `/api/tasks/{task_id}` | GET | api.py:520 | 任務詳情 |
| `/api/orchestrator/tasks/{task_id}` | GET | api.py:540 | alias |
| `/api/runs` | GET | api.py:579 | 執行記錄 |
| `/api/orchestrator/runs` | GET | api.py:593 | alias |
| `/api/orchestrator/backlog` | GET | api.py:609 | CTO backlog |
| `/api/planner/run-now` | POST | api.py:624 | planner 立即執行 |
| `/api/worker/run-now` | POST | api.py:630 | worker 立即執行 |
| `/api/cto/scheduler` | GET | api.py:638 | CTO 排程讀取 |
| `/api/orchestrator/cto/scheduler` | GET | api.py:639 | alias |
| `/api/cto/scheduler` | POST | api.py:651 | CTO 排程設定 |
| `/api/orchestrator/cto/scheduler` | POST | api.py:652 | alias |
| `/api/cto/settings` | GET | api.py:660 | CTO 設定讀取 |
| `/api/orchestrator/cto/providers` | GET | api.py:661 | alias |
| `/api/cto/settings` | POST | api.py:666 | CTO 設定寫入 |
| `/api/orchestrator/cto/providers` | POST | api.py:667 | alias |
| `/api/orchestrator/cto/summary` | GET | api.py:682 | CTO 摘要 |
| `/api/cto/run-now` | POST | api.py:721 | CTO 立即執行 |
| `/api/orchestrator/cto/run-now` | POST | api.py:722 | alias |
| `/api/orchestrator/cto/run-status` | GET | api.py:753 | CTO 執行狀態 |
| `/api/cto/runs` | GET | api.py:766 | CTO 執行記錄 |
| `/api/orchestrator/cto/runs` | GET | api.py:767 | alias |
| `/api/cto/runs/{run_id}` | GET | api.py:789 | CTO 單筆執行詳情 |
| `/api/orchestrator/cto/runs/{run_id}` | GET | api.py:790 | alias |
| `/api/orchestrator/cto/reports/{run_id}` | GET | api.py:813 | CTO 報告 |
| `/api/orchestrator/cto/pending` | GET | api.py:838 | CTO 待審核清單 |
| `/api/cto/backlog` | GET | api.py:862 | CTO backlog 讀取 |
| `/api/orchestrator/cto/backlog` | GET | api.py:863 | alias |
| `/api/orchestrator/cto/backlog/prioritized` | GET | api.py:892 | 優先 backlog |
| `/api/cto/backlog` | POST | api.py:919 | backlog 新增 |
| `/api/orchestrator/cto/backlog` | POST | api.py:920 | alias |
| `/api/orchestrator/cto/backlog/batch` | POST | api.py:943 | batch backlog 新增 |
| `/api/orchestrator/cto/adaptive-policy` | GET | api.py:996 | adaptive policy 讀取 |
| `/api/orchestrator/cto/adaptive-policy/refresh` | POST | api.py:1023 | adaptive policy 重算 |

---

## A1.4 launchd / 背景服務

**repo 內 plist 路徑：** `runtime/agent_orchestrator/launchd/plists/`  
**~/Library/LaunchAgents 相關 plist（shell 驗證）：**
```
com.bettingpool.main.plist
com.bettingpool.orchestrator.copilot-daemon.plist
com.bettingpool.orchestrator.planner.plist
com.bettingpool.orchestrator.worker-daemon.plist
com.bettingpool.orchestrator.worker.plist
```

**launchctl list 原始輸出（已過濾）：**
```
2330    0       com.bettingpool.orchestrator.worker-daemon
-       0       com.bettingpool.orchestrator.worker
-       0       com.bettingpool.orchestrator.planner
2355    0       com.bettingpool.main
2314    0       com.bettingpool.orchestrator.copilot-daemon
```

| Label | Source | Loaded? | Evidence |
|---|---|---|---|
| com.bettingpool.main | ~/Library/LaunchAgents + runtime/plist | YES (PID 2355) | launchctl list output, PID 2355 |
| com.bettingpool.orchestrator.planner | ~/Library/LaunchAgents + runtime/plist | REGISTERED BUT NOT RUNNING ("-" PID) | launchctl list shows "-" PID; StartInterval=600s; invokes scripts/launchd/run_planner_tick.sh |
| com.bettingpool.orchestrator.worker | ~/Library/LaunchAgents + runtime/plist | REGISTERED BUT NOT RUNNING ("-" PID) | launchctl list shows "-" PID; StartInterval=600s; invokes scripts/launchd/run_worker_tick.sh |
| com.bettingpool.orchestrator.worker-daemon | ~/Library/LaunchAgents + runtime/plist | YES (PID 2330) | launchctl list, PID 2330 |
| com.bettingpool.orchestrator.copilot-daemon | ~/Library/LaunchAgents + runtime/plist | YES (PID 2314) | launchctl list, PID 2314 |
| scripts/com.mlb.odds_capture.plist | repo scripts/ | UNKNOWN | plist 存在於 repo 但未在 launchctl list 中出現 |

**注意：** planner 與 worker-tick launchd jobs 已註冊但 PID 為 "-"，代表上次執行已結束（非常駐）；worker-daemon 與 copilot-daemon 為常駐 process。

---

## A1.5 start / stop scripts

| Script | Purpose (based on first 40 lines content) | Evidence |
|---|---|---|
| start_all.sh | 啟動三個服務 (backend=agent_orchestrator.py api, frontend=http.server, proxy=proxy_server.py)；執行 health_check.sh + smoke_check.sh；支援 --foreground 前台督管模式 | start_all.sh:1-61, lines show BACKEND_CMD, FRONTEND_CMD, PROXY_CMD |
| stop_all.sh | 停止三個服務 PID file；強殺 port owner；支援 --quiet | stop_all.sh:1-22 |
| scripts/manage_daemon.sh | (僅此一個腳本) — UNKNOWN（未讀取內容） | file_search:scripts/manage_daemon.sh |
| scripts/launchd/run_planner_tick.sh | launchd 觸發 planner_tick 的包裝腳本 | runtime/agent_orchestrator/launchd/plists/com.bettingpool.orchestrator.planner.plist:11 |
| scripts/launchd/run_worker_tick.sh | launchd 觸發 worker_tick 的包裝腳本 | find /scripts/launchd/ output |
| scripts/launchd/run_worker_daemon.sh | 啟動 worker daemon 常駐服務 | find /scripts/launchd/ output |
| scripts/launchd/run_copilot_daemon.sh | 啟動 copilot_daemon 常駐服務 | find /scripts/launchd/ output |
| scripts/launchd/health_check.sh | 健康檢查（由 start_all.sh 呼叫） | start_all.sh:32 |
| scripts/launchd/smoke_check.sh | 冒煙測試（由 start_all.sh 呼叫） | start_all.sh:38 |
| scripts/launchd/manage_launch_agents.sh | launchd agent 管理（install/uninstall；支援 --scope system） | scripts/launchd/ directory listing |
| scripts/launchd/common.sh | 共用變數與函式（BACKEND_PORT, FRONTEND_PORT, PROXY_PORT, PID 管理） | start_all.sh:6 `source common.sh` |

---

## A1 Conclusion

```
Backend reality: 4 expected tables present (agent_tasks, planner_dedupe_state, task_git_commits, scheduler_state) / 6 expected tables MISSING (agent_locks, exploration_routing_state, worker_metrics, scheduling_state, task_outcomes, task_type_roi_state).
Planner code: PRESENT (evidence: orchestrator/planner_tick.py:959 — def run_planner_tick())
Worker code: PRESENT (evidence: orchestrator/worker_tick.py:505 — def run_worker_tick())
Background runner: RUNNING — worker-daemon PID 2330, copilot-daemon PID 2314; planner/worker-tick NOT_RUNNING (launchd "-" PID, interval-based)
Last successful task completion: 2026-04-25T13:37:17.402345+00:00 (sqlite3 SELECT MAX(completed_at) FROM agent_tasks WHERE status='COMPLETED')
```

---

## RISK FLAGS (A1)

1. **DB schema mismatch** — 6 LotteryNew 表格在 Betting-pool DB 缺失 (`agent_locks`, `worker_metrics`, `scheduling_state`, `task_outcomes`, `task_type_roi_state`, `exploration_routing_state`)。如果 Phase 2 要引入這些表格的邏輯，必須先 migrate schema。
2. **planner/worker tick launchd not running** — PID 為 "-"，代表上次執行已結束。排程可能未正常觸發，或設計為 one-shot（StartInterval 600s 代表每 10 分鐘觸發一次，已執行完畢屬正常）。
3. **task_git_commits row count = 0** — 表格存在但無資料，代表 CTO git commit 追蹤功能從未被使用。
4. **dual DB** — `orchestrator.db` 為主要 orchestration DB；`bankroll_v3.db` 與 `baseball_knowledge_graph.db` 為 domain-specific DB，三者之間無 foreign key 關聯。
5. **domain mismatch in task prompts** — `signal_state_type` 欄位存在但值如 `deep_research_calibration`, `deep_research_feature` 帶有 LotteryNew 語意，與 Betting-pool 賽事/盤口語意不一致。
