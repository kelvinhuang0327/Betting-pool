# A3 — LOTTERYNEW → BETTING-POOL REFERENCE MAPPING
**Report:** audit_a3_mapping_2026-04-29.md  
**UTC Date:** 2026-04-29  
**Repo:** /Users/kelvin/Kelvin-WorkSpace/Betting-pool  
**LotteryNew Repo:** /Users/kelvin/Kelvin-WorkSpace/LotteryNew  
**Scope:** LotteryNew 概念逐一對應到 Betting-pool 現況（只讀，不修改任何程式或設定）

---

## 前置說明

LotteryNew 白名單確認：
```
ls /Users/kelvin/Kelvin-WorkSpace/LotteryNew/wiki/system/
→ decision_engine.md  feedback_loop.md  governance.md  orchestrator.md  stability_audit.md  validation_gates.md

ls /Users/kelvin/Kelvin-WorkSpace/LotteryNew/orchestrator/
→ common.py  db.py  planner_tick.py  worker_tick.py  planner_decision.py  api.py  light_worker_tick.py  cto_review_tick.py  ...
```

白名單路徑可存取，繼續 A3 分析。

---

## 語意替換對照表

| LotteryNew | Betting-pool |
|---|---|
| 彩種 | 賽事 / 盤口 / 市場 |
| active strategy | active model / active betting strategy |
| shadow strategy | shadow model / benchmark model |
| watchdog edge | ROI / CLV / hit-rate / drawdown monitor |
| draw window | match window / settle window |
| validation | backtest / walk-forward / leakage audit |
| forced exploration | new hypothesis research |
| reject rule | bankroll / risk-cap / no-bet rule |
| CTO review | merge / deployment review |

---

## A3 Reference Mapping Table

| LotteryNew Concept | LotteryNew Source File:Line | Betting-pool Equivalent | Domain Rewrite | Priority |
|---|---|---|---|---|
| **agent_tasks table** | LotteryNew/orchestrator/db.py:152 `CREATE TABLE IF NOT EXISTS agent_tasks` — 含 worker_type 欄位（research/light 分離）、epoch_id、value_score | Betting-pool/orchestrator/db.py:308 `create_task()` 寫入 orchestrator.db 內 agent_tasks — 同名同結構但缺少 `worker_type` 欄位（grep 確認 NOT_FOUND in schema）；有 signal_state_type、track 欄位為 Betting-pool 延伸 | 保留 `agent_tasks` 命名；補充 Betting-pool 特有欄位如 `match_id`, `market_type` 供盤口追蹤 | MUST_PORT (worker_type 欄位缺失導致多 worker 分類失效) |
| **agent_locks table** | LotteryNew/orchestrator/db.py:240 `CREATE TABLE IF NOT EXISTS agent_locks` — runner,pid,task_id,started_at,heartbeat_at,lock_type; 用於 worker 唯一性保證 | NOT_FOUND — `SELECT name FROM sqlite_master WHERE name='agent_locks'` 返回空，DB 無此表；copilot_daemon.py 有自己的 `_write_lock/_read_lock` 實作基於 JSON 檔案 | 若引入多 worker 並發，需建立 `match_worker_locks` 表（賽事 worker 鎖），依 match_id + worker_type 確保唯一性 | MUST_PORT (缺少 DB-level 鎖導致多 worker 並發不安全) |
| **planner_tick + AUTO-MONITOR contract** | LotteryNew/orchestrator/planner_tick.py:1562 `AUTO-MONITOR replacement`；planner_decision.py 存在作為獨立決策模組 | Betting-pool/orchestrator/planner_tick.py:959 `def run_planner_tick()` — AUTO-MONITOR 邏輯內嵌（planner_tick.py:470 monitoring dedupe 邏輯存在）；**無獨立 planner_decision.py**（`ls orchestrator/` 確認 NOT_FOUND） | Planner tick 整合賽事日程監控：每場賽事自動發出「開賽前監控任務」（pre-match monitoring task），用 `match_id:YYYY-MM-DD` 作 dedupe_key，防止重複監控同場賽事 | MUST_PORT (planner_decision.py 缺失導致決策邏輯與排程邏輯耦合過高) |
| **worker_tick claim flow** | LotteryNew/orchestrator/worker_tick.py:1391 `Claim a QUEUED task`；LotteryNew/orchestrator/db.py:1268-1303 `get_worker_lock / acquire_worker_lock / release_worker_lock`（DB-level lock） | Betting-pool/orchestrator/worker_tick.py:538 `queued_tasks = db.list_tasks(status="QUEUED", limit=1)` → 565 `db.update_task(status="RUNNING")` — 無 DB-level atomic lock；直接 list+update，存在 race condition 風險 | 賽事 worker claim flow：claim 前需確認同場賽事 (match_id) 無進行中任務；使用 `BEGIN IMMEDIATE` transaction 保證原子性 | MUST_PORT (無 atomic claim 保護，多 worker 情境下可能重複認領同一任務) |
| **light_worker** | LotteryNew/orchestrator/light_worker_tick.py:324 `def run()` — 獨立 light worker 負責 monitoring/fallback 輕量任務；`db.count_active_light_workers()` 適應性限流 | NOT_FOUND — `ls orchestrator/` 無 light_worker_tick.py；optional_worker_daemon.py 呼叫 run_worker_tick（非輕量化分流）；copilot_daemon.py 有輕量執行但非 light_worker 角色 | 賽事資料同步 worker：獨立輕量 worker 專責賽況更新（odds fetch, score update）與系統健康巡查；不佔用主 worker 的 LLM quota | OPTIONAL (目前單一 worker 架構可運作，僅在高頻賽事需求時才有必要) |
| **Fallback P1-P6** | LotteryNew/orchestrator/planner_tick.py:1567-1834 `_FALLBACK_PRIORITY_ORDER = ["watchdog", ...]`；P1=系統看門狗, P2=CTO預檢, P3=佇列衛生, P4=知識庫同步, P5=UX可觀測性, P6=Light Worker健康 | NOT_FOUND — grep "FALLBACK\|fallback\|P1\|P2\|P3\|P4\|P5\|P6" 在 Betting-pool/orchestrator/planner_tick.py 返回空；Betting-pool planner 無任何 fallback 階梯邏輯 | 賽事盤點 Fallback 階梯：P1=賠率資料健康巡查, P2=賽程同步確認, P3=任務佇列衛生, P4=知識庫同步（wiki/DATA_SOURCES.md）, P5=部署審核健康, P6=Copilot Daemon 健康 | MUST_PORT (缺少 fallback 導致 planner 在所有主任務被 daily_cap 擋住時產出 SKIPPED，系統空轉) |
| **Forced Exploration A-F** | LotteryNew/orchestrator/planner_tick.py:1855-2053 `_EXPLORATION_LANES`；A=外部信號假說, B=約束後處理, C=長窗口殘差, D=跨彩種遷移, E=拒絕規則, F=UX決策品質 | NOT_FOUND — grep "forced_exploration\|FORCED_EXPLORATION\|exploration.*lane" 在 Betting-pool/orchestrator/planner_tick.py 返回空 | 新假說研究 (New Hypothesis Research)：A=外部賠率信號假說, B=特徵後處理假說, C=長週期殘差研究, D=跨賽種遷移（MLB→WBC）, E=No-bet Rule假說, F=部署品質研究；dedupe_key=`new_hypothesis:{lane}:{YYYY-MM-DD}` | OPTIONAL (對成熟研究管線有價值，但 Betting-pool 目前研究任務直接由 planner 候選池生成，短期可以維持現狀) |
| **Exploration Result Router** | LotteryNew/orchestrator/planner_tick.py:2437-2558 `_is_exploration_already_routed / _derive_exploration_result`；讀取 forced_exploration 任務輸出，決定 WORTH_VALIDATION / WATCH_ONLY / REJECT；寫入 exploration_routing_state 表 | NOT_FOUND — `exploration_routing_state` 表不存在（sqlite3 查詢確認）；planner_tick.py 無 exploration routing 邏輯 | 假說路由器 (Hypothesis Router)：讀取 new_hypothesis 任務輸出，決定是否升級為 backtest/walk-forward 驗證任務 | OPTIONAL (需先實作 Forced Exploration 才有意義) |
| **WORTH_VALIDATION → validation task** | LotteryNew/orchestrator/planner_tick.py:1929-2039 `WORTH_VALIDATION` decision；planner 在下一個 tick 排入 validation task；wiki/system/validation_gates.md 定義 T0-T4 tier | Betting-pool/orchestrator/planner_tick.py:207 `signal_state_type="deep_research_backtest_validity"` 等任務類型存在，但無明確 WORTH_VALIDATION 決策閘道；`validation_checks` 欄位存在於 task blueprint 但非 gating 機制 | 預測驗證任務 (Prediction Validation Task)：research 任務輸出 CLV/ROI 信號強度分級；WORTH_VALIDATION → 排入 walk-forward backtest 任務；leakage audit 為 T0 必選門 | MUST_PORT (目前缺乏結構化的 research → validation 升級路徑，驗證任務依賴人工判斷) |
| **CTO Review / merge policy** | LotteryNew/orchestrator/cto_review_tick.py:3 — `CTO review tick — batches pending git commits, classifies them, reviews them`；LotteryNew/orchestrator/db.py:654 `active_strategy_state` 表；LotteryNew/orchestrator/cto_review_tick.py:1503 `db.set_active_strategy_state(active_strategy=...)` | Betting-pool/orchestrator/cto_review_tick.py:230 `def run_cto_review_tick()` — 有 CTO review，讀取 `cto_review_runs`（31 rows）和 `cto_backlog_items`（35 rows）；**但無 `active_strategy_state` 表**（grep 在 db.py 返回空）；`task_git_commits` 0 rows 代表 git commit 追蹤未啟用 | 部署審核 / 合併政策 (Merge / Deployment Review)：CTO review 改為審核盤口模型部署；`active_betting_model_state` 表追蹤 active model / benchmark model；無 active_strategy → 對應 無 active_betting_model | MUST_PORT (active_strategy_state 表缺失導致 CTO review 無法寫入策略狀態；task_git_commits 0 rows 表示 git 追蹤功能未啟用) |
| **UTC dedupe day / Asia/Taipei display day convention** | LotteryNew/orchestrator/common.py:690 `def dedupe_day_utc()` — UTC for dedupe_key；LotteryNew/orchestrator/common.py:698 `def display_day_taipei()` — Asia/Taipei for display only；README: "Do NOT use for dedupe_key — use dedupe_day_utc() instead" | Betting-pool/orchestrator/common.py:38 `datetime.now(timezone.utc).strftime("%Y%m%d")` for date_folder — **UTC 使用正確**；但無明確的 `dedupe_day_utc()` / `display_day_taipei()` 分離函式；planner_tick.py:609 `now = datetime.now(timezone.utc)` 正確使用 UTC | UTC dedupe / display 分離慣例：強制要求所有 dedupe_key 使用 `dedupe_day_utc()`；UI 顯示賽事時間使用 Asia/Taipei（台灣運彩標準）；兩個函式需明確分離 | MUST_PORT (無明確的 dedupe_day_utc() 函式隔離，未來若有開發者混用 local timezone，將導致 dedupe key 跨日重複建立) |
| **daily cap / dedupe_key** | LotteryNew/orchestrator/planner_tick.py:460 `Daily cap for date-keyed monitoring — any QUEUED/RUNNING/COMPLETED today → skip`；dedupe_key 格式 `monitoring:{source}:{YYYY-MM-DD}` | Betting-pool/orchestrator/planner_tick.py:612 `recent_dedupe_keys = {str(task.get("dedupe_key") or "") for task in recent_tasks}` — dedupe_key 存在但無明確 daily cap 邏輯；`build_task_dedupe_key(blueprint)` 基於 content hash；**不是日期型 daily cap** | 盤口監控每日上限：同一賽事（match_id）每日只建立一次監控任務；dedupe_key 格式改為 `match_monitoring:{match_id}:{YYYY-MM-DD}`（UTC）；FAILED 任務不擋當日重試 | MUST_PORT (現有 dedupe 基於 content hash，不具備「每盤口每日上限」語意，高頻賽事日可能重複建立監控任務) |

---

## 特殊說明

### NOT_APPLICABLE 項目

無。所有 12 個 LotteryNew 概念均可找到 Betting-pool 合理對應或明確缺口。

### WHITELIST_INSUFFICIENT 項目

無。所有分析均在白名單檔案範圍內完成。

---

## 缺口摘要

| Priority | Count | Items |
|---|---|---|
| MUST_PORT | 7 | agent_tasks(worker_type), agent_locks, worker_tick atomic claim, Fallback P1-P6, WORTH_VALIDATION gate, CTO active_strategy_state, UTC dedupe 函式分離, daily cap 機制 |
| OPTIONAL | 3 | light_worker, Forced Exploration A-F, Exploration Result Router |
| SKIP | 0 | — |

---

## RISK FLAGS (A3)

1. **domain mismatch** — Betting-pool planner_tick.py 內 `signal_state_type` 值如 `deep_research_calibration`, `deep_research_feature` 保留 LotteryNew 彩票語意，未轉換為 `match_calibration`, `odds_feature` 等賽事語意。(evidence: planner_tick.py:123-267)

2. **DB schema mismatch** — 6 張 LotteryNew 核心表格缺失：`agent_locks`, `worker_metrics`, `scheduling_state`, `task_outcomes`, `task_type_roi_state`, `exploration_routing_state`；`active_strategy_state` 亦缺失。任何依賴這些表格的 LotteryNew 邏輯 port 過來都需要先 migrate。

3. **task_type 空值風險** — Betting-pool agent_tasks 表無 `task_type` 欄位（LotteryNew 有 `worker_type`）；`signal_state_type` 欄位雖存在，但 db.py 的 list_tasks 不依此過濾，worker_tick 不依此 claim 分流，存在任務類型混亂風險。

4. **dedupe key 日期混亂風險** — Betting-pool 缺少 `dedupe_day_utc()` / `display_day_taipei()` 明確分離；若未來開發者使用 local time 建立 dedupe_key，同一賽事可能在午夜前後建立兩筆監控任務。

5. **validation 任務重複建立** — 無 WORTH_VALIDATION 閘道，planner 可能為同一研究方向重複建立 backtest 任務；現有 dedupe 基於 content hash，不保證同語意任務只建立一次。

6. **background runner 沒 claim（atomic 缺失）** — worker_tick 使用 list→update 非原子方式認領任務（worker_tick.py:538-567），無 DB-level lock；若同時有兩個 worker instance（e.g., launchd timer 提前觸發），可能雙重認領同一 QUEUED 任務。

7. **merge policy 風險** — `task_git_commits` 0 rows，CTO review 無實際 git commit 審核資料；`active_strategy_state` 缺失，CTO 無法寫入當前 active betting model 狀態；merge/deployment policy 形同虛設。

8. **production DB / external API 風險** — `bankroll_v3.db` 獨立於 `orchestrator.db`，兩者無 foreign key；若 worker 修改 bankroll 資料，orchestrator 無法感知；外部 odds API 呼叫無 circuit breaker 在 orchestrator 層。

9. **launchd label 命名可能衝突** — `~/Library/LaunchAgents` 同時存在 `com.bettingpool.*` 與 `com.novel.*` 系列，若 novel 系統也在同機器運行，LaunchAgent logs 路徑可能混淆（未驗證 WorkingDirectory 是否都正確指向各自 repo）。

---

## FINAL RECOMMENDATION

**NEEDS_BASELINE_CLEANUP**

理由：
1. 核心 orchestration 鏈路（planner → worker → CTO review → UI）已完整存在並有活躍資料（agent_tasks 3522 rows，last completed 2026-04-25T13:37:17 UTC）。
2. 7 個 MUST_PORT 缺口中有 4 個屬於「安全性補強」（agent_locks, atomic claim, fallback, daily cap），在低並發單機場景下不會立即崩潰，但會在高負載或多 worker 情境下產生問題。
3. `active_strategy_state` 缺失與 `task_git_commits` 0 rows 代表 CTO review 功能雖「存在」但未完全接通，Phase 2 前需確認是否要啟用 git commit 追蹤功能。
4. domain mismatch（彩票語意殘留）必須在 Phase 2 實作前清理，否則新增 Betting-pool 特有邏輯會與舊語意衝突。
