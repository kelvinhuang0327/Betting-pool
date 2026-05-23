# Active Task — P30A GREEN BASELINE LOCKED ✅

> **[CLOSED 2026-05-24]** `P30A_GREEN_BASELINE_LOCK`
> HEAD: `e40e02a` | Branch: `main`
> Full suite: **6202 passed / 17 skipped / 0 failed**
> P28 chain: 186/186 | strategy_replay: 282/282
> Next: **P30E** (warning reduction: 6 `utcnow()` call sites → `datetime.now(timezone.utc)`)

> **P26K CLOSED [2026-05-23]** `P26K_CLOSING_FETCH_TRIGGER_ROOT_CAUSE_DIAGNOSTIC_20260521`
> 最終分類: `P26K_SOURCE_STATE_TRULY_EMPTY_CONFIRMED` + `P26K_QUOTA_HARD_CAP_SECONDARY`
>
> **P26K 結案**:
> - 主要根因: `SOURCE_STATE_TRULY_EMPTY` — TSL 在收盤視窗前已撤除 NPB 賭盤（03:24Z/04:55Z）
> - 次要根因: `QUOTA_HARD_CAP` — OddsAPI 每日 cap=2，02:24Z 耗盡，收盤 8 週期全封鎖
> - CEO 假設 `STARTUP_ONLY_FETCH_ARCHITECTURE`：`PARTIALLY_REFUTED`（TSL 每 15min 執行）
> - P26L: **不需要**（根本原因已確認）
> - CLV 樣本: COMPLETE_PAIR=223（>基準線 220），未受損
>
> **P26K commit**: 待產生（P26K artifacts 已建立）
>
> **Preceding Tasks Completed**:
> - `P26H+P26G` → commit `d644f3f`
> - `P26I_CLOSING_CAPTURE_GAP_INVESTIGATION` → commit `60a73a7`
> - `P26J_READINESS_CHECKPOINT` → commit `34fc118`
> - `P26J_POST_WINDOW_PAIR_VERIFICATION_RERUN` → commit `0ccd06d`
> - `P26K_ROOT_CAUSE_DIAGNOSTIC` → 待 commit
>
> **下一步**: `SOURCE_AVAILABILITY_MONITOR_REQUIRED` 或 `QUOTA_POLICY_REVIEW_REQUIRED`（新任務決定）

---

## PROJECT_CONTEXT_LOCK (MANDATORY)

```text
Project          = Betting-pool
Canonical Repo   = /Users/kelvin/Kelvin-WorkSpace/Betting-pool
Canonical Branch = main
Cross-Project Rule:
  若任何任務、檔案、commit 或 roadmap 屬於其他專案 (Stock-Prediction-System / P48 / P49 /
  golden fixture / paper simulation dry-run / Lottery)：
    STOP immediately
    Do NOT summarize as current project work
    Do NOT create artifacts for it
    Report Final Classification = P26K_BLOCKED_BY_CONTEXT_CONTAMINATION
```

---

## Branch Governance (MANDATORY)

- Canonical Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Canonical Branch: `main`
- HEAD: `0ccd06d`
- 禁止新增 branch / worktree / clone / detached HEAD
- 新分支需明確授權：`YES: create new branch for <reason>`

### Pre-flight (必跑 — 含 Context Hygiene + Dirty Worktree 警戒線)

```bash
cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool

# 1. Identity check
git rev-parse --show-toplevel
git branch --show-current
git status --short
git fetch origin
git status --branch --short
git log --oneline -15

# 2. Dirty worktree 警戒線 (CEO 加：>100 須另行授權)
DIRTY_COUNT=$(git status --short | wc -l | tr -d ' ')
echo "DIRTY_WORKTREE_COUNT=${DIRTY_COUNT}"
if [ "${DIRTY_COUNT}" -gt 100 ]; then
  echo "WARNING_DIRTY_WORKTREE_OVER_100 — 須 CEO 顯式授權才能繼續 commit"
fi

# 3. Context contamination scan (CEO 強加)
grep -RniE "P48|P49|Stock-Prediction|golden fixture|paper simulation dry-run" \
  00-Plan 00-BettingPlan report data/paper_recommendations 2>/dev/null \
  | grep -v "Cross-project guard\|context contamination scan\|cross-project\|PROJECT_CONTEXT_LOCK\|BETTING_CONTEXT_CLEAN\|NO_STOCK_CONTEXT_FOUND" \
  && echo "STOCK_CONTAMINATION_DETECTED_ABORT" \
  || echo "NO_STOCK_CONTEXT_FOUND"

# 4. Untracked scripts inventory (僅列出，不刪不 stage)
git status --short | grep "^?? scripts/p26j_" || echo "NO_UNTRACKED_P26J_SCRIPTS"
```

STOP 條件：
- repo 非 canonical / branch 非 `main` / detached HEAD
- `STOCK_CONTAMINATION_DETECTED_ABORT` → `P26K_BLOCKED_BY_CONTEXT_CONTAMINATION`
- `DIRTY_WORKTREE_COUNT > 100` 且無 CEO 授權 → STOP，回報 dirty worktree 規模
- unrelated dirty files block artifact-only work

---

## 任務名稱

`P26K_CLOSING_FETCH_TRIGGER_ROOT_CAUSE_DIAGNOSTIC_20260521`

## 背景

1. **P26J rerun 已完成** (HEAD = `0ccd06d`, Timing Guard PASS @ 09:12:47Z)：
   - `3469930.1`: 7 rows, 0 closing rows, markets=[], last_fetched_at=02:07Z 系列
   - `3469931.1`: 8 rows, 0 closing rows, markets=[], last_fetched_at=04:55Z 系列
   - `target_pair_delta=0`, `expected_new_pairs_today` 預測 broken。
   - 兩 target 都 `PREGAME_ONLY_NO_CLOSING`。

2. **Daemon continuity rerun 顯示嚴重 signal**：
   - closing window `07:00-09:00Z` 共 8 個 heartbeat cycle (每 ~15 min)
   - **ALL 8 cycles `fetched=false`**
   - `api_calls_today=2` **整個 window 保持不變**
   - `next_trigger_minutes=null`
   - `last_heartbeat_before_window=06:55Z`、`first_heartbeat_after_window=09:11Z` (daemon 一直活著)
   - 報告自宣告 "last two api calls were likely the 02:07Z + 02:09Z captures from early morning"

3. **CEO 第一假設 (CTO 未指出但 CEO 補強)**：
   - **last 2 api calls 在 02:07Z+02:09Z，與 P26G daemon restart_time `2026-05-21T02:09:35Z` 高度吻合**
   - 強烈暗示 **「fetch 只在 daemon startup 觸發一次」**，而非按 closing window event 觸發
   - 此 hypothesis 必須在 P26K Phase 3 列為第一優先驗證

4. **COMPLETE_PAIR 220 → 219 (delta = -1)**：
   - CTO 將此排到 P4，**CEO 上拉至 P1**
   - 可能原因 (待 P26K 分類)：eligibility rule drift / new markets=[] row 反向 invalidate / dedup recount / data state shift
   - 若 -1 是 evidence pollution，整個 CLV 樣本可信度需重評估

5. **P26J `TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED` 命名過早**：
   - daemon_continuity JSON 自己給出更精確的 sub_classification `FETCH_NOT_EXECUTED_IN_CLOSING_WINDOW`
   - P26K 必須正式 retire `source unavailable` 命名，改用 evidence-backed 分類

6. **status="captured" 是誤導性的**：
   - 不代表 fetch 成功，只代表 heartbeat 寫入
   - 必須記錄為 retired interpretation

7. **dirty worktree** 包含 30+ 個 daemon/runtime/data 檔 (含 `tsl_odds_history.jsonl`)，**commit scope 必須白名單**，禁止 stage raw feed/runtime/output。

8. **75 PASS / 0 FAIL** 為 P26J 報告值，本輪必須 rerun targeted tests 取得實測值。

---

## 目標

1. **Daemon timeline 重建**：從 `logs/daemon_heartbeat.jsonl` (只讀) 取出 02:00Z–09:30Z 區間所有 heartbeat 與 fetch 狀態，產出 timeline table。
2. **api_calls_today=2 forensics**：追溯 02:07Z + 02:09Z 兩次 api call 的觸發 reason；證實/否定「fetch 只在 startup 觸發」假設。
3. **next_trigger_minutes=null 行為解釋**：搜尋 source code (只讀) 中該欄位的設值邏輯。
4. **Source vs trigger 分離**：證實 `markets=[]` 是 (a) TSL 來源真沒給 vs (b) fetch 沒執行所以 client 自填空，兩者不同 incident response。
5. **COMPLETE_PAIR 220→219 root cause**：分類為 eligibility / pollution / recount / drift / inconclusive。
6. **Primary + Secondary root cause classification**：從 7 個候選類別擇一 primary + 列出 secondary。
7. **Phase 9 targeted tests + forbidden scan**：實測非沿用。
8. **P26 階段終結建議**：明確說明是否需要 P26L 或可以收斂。
9. 全程 `read_only=true`，**禁止任何 code/scheduler/daemon 變更**。

---

## 允許修改範圍

### 新增 JSON artifacts

- `data/paper_recommendations/p26k_closing_fetch_trigger_root_cause_20260521.json`
- `data/paper_recommendations/p26k_api_calls_forensics_20260521.json`
- `data/paper_recommendations/p26k_complete_pair_decrease_root_cause_20260521.json`
- `data/paper_recommendations/p26k_phase9_validation_20260521.json`

### 新增 Markdown reports

- `report/p26k_closing_fetch_trigger_root_cause_20260521.md`
- `report/p26k_api_calls_forensics_20260521.md`
- `report/p26k_complete_pair_decrease_root_cause_20260521.md`
- `report/p26k_final_validation_20260521.md`
- `00-BettingPlan/20260521/p26k_closing_fetch_trigger_root_cause_20260521.md`

### 允許讀取 (**只讀**)

- `data/tsl_odds_history.jsonl`
- `logs/daemon_heartbeat.jsonl`
- `data/mlb_context/odds_capture_schedule.json`
- `data/.live_cache/tsl_dedup_state.json`
- `data/tsl_fetch_status.json`
- `data/tsl_odds_snapshot.json`
- `data/mlb_context/external_closing_state.json`
- `data/paper_recommendations/p26[e-j]_*` (既有)
- `report/p26[e-j]_*`、`00-BettingPlan/20260521/p26[e-j]_*` (既有)
- source code (只讀 grep)：`scripts/odds_capture_daemon*`、`scripts/tsl_*`、`wbc_backend/ingestion/**`、`wbc_backend/odds/**`、相關 scheduler / quota / trigger 程式碼
- `tests/` 目錄

### Commit scope 白名單 (嚴格)

僅允許 stage 以下檔案：

```
data/paper_recommendations/p26k_*_20260521.json
report/p26k_*_20260521.md
00-BettingPlan/20260521/p26k_*_20260521.md
00-Plan/roadmap/CEO-Decision.md
00-Plan/roadmap/CTO-Analysis.md
00-Plan/roadmap/roadmap.md
00-Plan/roadmap/active_task.md
```

**Commit 前必跑驗證**：
```bash
git diff --cached --name-only | grep -E "tsl_odds_history|tsl_odds_snapshot|tsl_fetch_status|live_cache|daemon_heartbeat|learning_state|odds_capture_schedule|odds_timeline|outputs/predictions|wbc_backend/(artifacts|reports)|external_closing_state" && echo "FORBIDDEN_STAGED_ABORT" || echo "STAGE_CLEAN"
```

僅在 `STAGE_CLEAN` 時執行 commit。

---

## 禁止修改範圍 (絕對禁止)

- ❌ 不得 stage 或 commit `data/tsl_odds_history.jsonl` (raw feed)
- ❌ 不得 stage 或 commit `data/tsl_odds_snapshot.json`、`data/tsl_fetch_status.json`、`data/.live_cache/*`、`logs/daemon_heartbeat.jsonl`
- ❌ 不得 stage 或 commit `data/learning_state.json`、`data/mlb_context/external_closing_state.json`、`data/mlb_context/odds_capture_schedule.json`、`data/mlb_context/odds_timeline.jsonl`
- ❌ 不得 stage 或 commit `outputs/predictions/PAPER/**`、`data/wbc_backend/**` runtime output
- ❌ 不得 `git add .` 或 `git add -A`，必須逐檔指定
- ❌ 不得重啟 daemon
- ❌ 不得修改 scheduler / dedup / crawler / ingestion / fetch trigger 程式碼
- ❌ 不得呼叫 live odds API
- ❌ 不得手動補造 snapshots
- ❌ 不得替換 champion `fixed_edge_5pct`
- ❌ 不得啟動 optimizer promotion
- ❌ 不得發布 production proposal
- ❌ 不得宣稱可獲利 / profitability claim
- ❌ 不得 merge PR
- ❌ 不得新增 repo / worktree / branch
- ❌ 不得執行 P25C bootstrap (219 < 300)
- ❌ 不得修改 raw source data
- ❌ **不得開啟 P26L/M/N** 除非 P26K root cause 報告明確要求補刀 (需 CEO 顯式授權)
- ❌ 不得 patch source code 即使發現明顯 bug — 只能記錄為 root cause，**修復屬於 P26K 之後的另一輪**

---

## 執行階段

### Phase 0 — Pre-flight

如上 Branch Governance 區塊；若 STOP 條件觸發，立即停止。

### Phase 0.5 — Untracked P26J Scripts Inventory (CEO 補強)

列出但**不處置**以下 untracked scripts (CEO 已知 4 個)：
- `scripts/p26j_phase2_analysis.py`
- `scripts/p26j_phase3_daemon.py`
- `scripts/p26j_phase3b_heartbeat.py`
- `scripts/p26j_phase4_coverage.py`

對每個 script：
1. 讀檔頭 docstring / 前 20 行判斷用途
2. 分類為：`temporary_analysis_script` / `reusable_diagnostic_candidate` / `unknown`
3. 將分類結果寫入 `p26k_closing_fetch_trigger_root_cause_20260521.json` 的 `untracked_scripts_inventory` 欄位
4. **禁止 stage**、**禁止刪除**、**禁止 commit**，除非後續 CEO 顯式授權
5. commit forbidden pattern 確保 `scripts/p26j_` 永遠不會被 stage

### Phase 1 — Commit Chain Verification

驗證以下 commit 存在：
- `d644f3f` P26H+P26G
- `60a73a7` P26I
- `34fc118` P26J readiness
- `0ccd06d` P26J post-window rerun (HEAD)

從 P26J rerun JSON 讀出 ground truth：
- `target_pair_delta=0`
- `COMPLETE_PAIR_current=219`、`COMPLETE_PAIR_baseline=220`、delta = -1
- 8 cycles 全 `fetched=false`
- `api_calls_today=2`
- `next_trigger_minutes=null`

### Phase 2 — Daemon Timeline Reconstruction (只讀)

從 `logs/daemon_heartbeat.jsonl` 取出 `2026-05-21T01:00:00Z` 到 `2026-05-21T10:00:00Z` 區間所有 heartbeat：

對每筆 row 記錄：
- `timestamp` (UTC)
- `fetched` (true/false)
- `api_calls_today`
- `status` (含 "captured" 等 retired interpretation 註記)
- `next_trigger_minutes`
- `closing_window_active` (依 game schedule 推算 07:00–09:00Z 為 active)
- `daemon_uptime_minutes` (since first heartbeat after restart 02:09Z)

產出 timeline table 並標註：
- restart event @ 02:09:35Z
- 02:07Z 與 02:09Z 兩次 api call 的 cycle
- closing window entry @ 07:00Z
- closing window exit @ 09:00Z
- 8 個 fetched=false cycles

### Phase 3 — Startup-Only Trigger Hypothesis Verification (P0 第一假設)

**CEO 第一假設**：fetch 只在 daemon startup 觸發一次，之後 trigger 永遠 false。

驗證步驟：
1. 確認 02:07Z + 02:09Z 兩次 api call 是否在 daemon restart (02:09:35Z) ±2 分鐘內。
2. 自 P26F commit `8a98f52` 後 daemon 是否有過多次 restart；每次 restart 後 api_calls_today 是否 +N（N>0）並隨即停留不變。
3. Grep 源碼 (只讀)：`grep -rn "api_calls_today\|next_trigger_minutes\|fetch_trigger\|closing_window" scripts/ wbc_backend/ | grep -v test`
4. 結論三選一：
   - `STARTUP_ONLY_TRIGGER_CONFIRMED`：強證據
   - `STARTUP_ONLY_TRIGGER_PLAUSIBLE_NOT_PROVED`：弱證據
   - `STARTUP_ONLY_TRIGGER_REFUTED`：證據不支持，需轉到其他 hypothesis

### Phase 4 — api_calls_today=2 Quota Forensics

可能解釋 (擇一或多選)：
1. **Hard daily quota cap**：source code 中是否有 `MAX_API_CALLS_PER_DAY=2` 等常數？
2. **Dedup state**：`data/.live_cache/tsl_dedup_state.json` 是否阻止重複 fetch 同 match？
3. **Source-side rate limit**：是否有 retry / backoff 鎖住？
4. **Startup-only side effect** (Phase 3 hypothesis)
5. **Inconclusive**：證據不足以分類

### Phase 5 — next_trigger_minutes=null Behavior Explanation

Grep source code (只讀) 找出 `next_trigger_minutes` 設值邏輯：
- 何時設為非 null？
- null 是 expected idle / scheduler bug / 缺少配置？
- 與 closing window event 是否有耦合？

### Phase 6 — Source vs Trigger Separation

對 `3469930.1` / `3469931.1` 的 markets=[] 結論：
1. 若 fetch 從未執行 → `markets=[]` 是 **client 自填空** (vacuous)，不是 source 真沒給。
2. 若 fetch 執行但 source 回 empty → 是 **source 真沒給**。
3. 從 daemon log + tsl_odds_history rows 判斷：**P26J 「source unavailable」命名是否 vacuous claim？**
4. 結論：retire `TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED`，改為更精確 sub_classification。

### Phase 7 — COMPLETE_PAIR 220→219 Decrease Root Cause (CEO 上拉至 P1)

候選分類：
1. `ELIGIBILITY_RULE_DRIFT`：pair eligibility 規則隨新 evidence 收緊
2. `NEW_EVIDENCE_INVALIDATION`：新 markets=[] row 反向 invalidate 既有 valid pair
3. `DEDUP_RECOUNT`：dedup 重算後計入差異
4. `DATA_STATE_SHIFT`：source 檔案歷史改寫 (低概率，應警示)
5. `INCONCLUSIVE`

對應 acceptance：將兩個 baseline (220) 與 current (219) 的 valid pair 清單 diff 出來，找出**被剔除的那 1 個 match_id**，並推斷剔除原因。

### Phase 8 — Root Cause Classification (Primary + Secondary)

7 個候選 primary 分類 (擇一)：
1. `TRIGGER_RULE_GAP` — trigger condition 沒考慮 closing window event
2. `QUOTA_HARD_CAP` — daily quota=2 為硬上限
3. `NEXT_TRIGGER_SCHEDULER_BUG` — next_trigger_minutes 永不被設值
4. `TIMEZONE_MISMATCH` — game_time UTC vs local 比較錯誤
5. `SCHEDULE_TARGET_MISMATCH` — schedule 沒涵蓋這些 target
6. `SOURCE_STATE_TRULY_EMPTY` — source 真的沒給（需 Phase 6 證實）
7. `GOVERNANCE_FLAG_BLOCKED` — paper_only 或其他 flag 攔住了
8. `STARTUP_ONLY_FETCH_ARCHITECTURE` — fetch 只綁 startup event (Phase 3 hypothesis 確認)
9. `INCONCLUSIVE`

Secondary list：列出其他 plausible 但證據不足以為 primary 的分類。

### Phase 9 — Targeted Tests + Forbidden Scan

```bash
source .venv/bin/activate

# Targeted tests (rerun，不沿用 75 PASS)
pytest tests/test_p26f_closing_dedup_bypass.py -q
pytest tests/test_p26b_scheduler_extension.py -q
pytest tests/test_p25_clv_construction_fix.py -q
pytest tests/test_p26_clv_line_aware_matching.py -q
pytest tests/test_blocked_state_daily_monitor_p12.py \
       tests/test_p13_minimal_monitor.py \
       tests/test_p14_no_expansion_guard.py \
       tests/test_p15_no_expansion_watch.py \
       tests/test_p16_no_expansion_hold.py \
       tests/test_p17_hold_state_continuity.py \
       -q

# Forbidden scan (新產出檔 + CEO 補強 Stock 字樣)
grep -RniE "production proposal|promotion|profitab|guaranteed profit|live odds api|crawler modif|champion replacement|patch (scheduler|daemon|dedup|crawler)|P48|P49|Stock-Prediction|golden fixture|paper simulation dry-run" \
  report/p26k_*_20260521.md \
  00-BettingPlan/20260521/p26k_*_20260521.md \
  data/paper_recommendations/p26k_*_20260521.json \
  || echo "GREP_CLEAN_CANDIDATE"
```

註：若只命中 governance guard 的 `false` 欄位 (e.g. `"promotion_allowed": false`)，標記為 `non-positive hit`，仍視為 CLEAN。

### Phase 10 — P26 階段終結建議 + Recommended Next Action

在 final report 明確回答：
- **P26K root cause 是否 actionable？**
- **是否需要 P26L？** 若需要，必須說明 P26L scope 為何 P26K 不能覆蓋。
- **`recommended_next_action`**：從以下 enum 擇一（worker 必須在 `p26k_closing_fetch_trigger_root_cause_20260521.json` 寫入此欄位）：
  - `SCHEDULER_TRIGGER_PATCH_REQUIRED` — root cause 為 scheduler/trigger 程式邏輯，下一輪 (需 CEO 授權) 為 code patch
  - `DAEMON_OPS_FIX_REQUIRED` — root cause 為 daemon runtime 操作（如 startup-only fetch），下一輪 (需 CEO 授權) 為 ops 修復
  - `SOURCE_AVAILABILITY_MONITOR_REQUIRED` — root cause 為 source 真沒給，下一輪為 source-side 監控設計
  - `QUOTA_POLICY_REVIEW_REQUIRED` — root cause 為 api quota 硬上限，下一輪為 policy review
  - `GOVERNANCE_FLAG_REVIEW_REQUIRED` — root cause 為 paper_only/governance flag 攔截，下一輪為 flag 規則重審
  - `TRIGGER_ROOT_CAUSE_IDENTIFIED_NO_CHANGE` — root cause 找到但決定不變動，繼續觀察
  - `MORE_GRANULAR_LOGGING_DIAGNOSTIC_REQUIRED` — root cause inconclusive，需更細 logging
- **不准** unilateral 開 P26L；任何下一輪都需 CEO 顯式授權。

### Phase 11 — Commit (白名單 only)

```bash
# 1. P26K artifacts
git add data/paper_recommendations/p26k_closing_fetch_trigger_root_cause_20260521.json \
        data/paper_recommendations/p26k_api_calls_forensics_20260521.json \
        data/paper_recommendations/p26k_complete_pair_decrease_root_cause_20260521.json \
        data/paper_recommendations/p26k_phase9_validation_20260521.json \
        report/p26k_closing_fetch_trigger_root_cause_20260521.md \
        report/p26k_api_calls_forensics_20260521.md \
        report/p26k_complete_pair_decrease_root_cause_20260521.md \
        report/p26k_final_validation_20260521.md \
        00-BettingPlan/20260521/p26k_closing_fetch_trigger_root_cause_20260521.md

# 2. Roadmap governance files
git add 00-Plan/roadmap/CEO-Decision.md \
        00-Plan/roadmap/CTO-Analysis.md \
        00-Plan/roadmap/roadmap.md \
        00-Plan/roadmap/active_task.md

# 3. Verify no forbidden staged (CEO 補強：含 scripts/p26j_)
git diff --cached --name-only | grep -E "tsl_odds_history|tsl_odds_snapshot|tsl_fetch_status|live_cache|daemon_heartbeat|learning_state|odds_capture_schedule|odds_timeline|outputs/predictions|wbc_backend/(artifacts|reports)|external_closing_state|scripts/p26j_" && echo "FORBIDDEN_STAGED_ABORT" || echo "STAGE_CLEAN"

# 4. Commit (僅在 STAGE_CLEAN 時)
git commit -m "P26K: closing fetch trigger root cause diagnostic (read-only)

- Daemon timeline reconstructed 02:00Z-10:00Z
- 8 closing-window cycles all fetched=false
- api_calls_today=2 stable; last calls at 02:07Z+02:09Z (post-restart)
- Primary root cause: <classification>
- COMPLETE_PAIR 220->219 reason: <category>
- P26J source-unavailable label formally retired
- paper_only=true; read_only=true; promotion=frozen

Final Classification: <see active_task>"
```

---

## 驗收標準

1. **`p26k_closing_fetch_trigger_root_cause_20260521.json` 必含**：
   - `paper_only=true`、`diagnostic_only=true`、`read_only=true`
   - `production_proposal=false`、`promotion_allowed=false`、`profitability_claim=false`、`champion_replacement_allowed=false`
   - `axis_alignment="axis_2_clv_validation_precondition"`
   - `commit_chain`: ["d644f3f", "60a73a7", "34fc118", "0ccd06d"]
   - `daemon_timeline_window`: "2026-05-21T01:00:00Z" – "2026-05-21T10:00:00Z"
   - `startup_only_trigger_hypothesis_status`: CONFIRMED / PLAUSIBLE / REFUTED
   - `api_calls_today_forensics_summary`
   - `next_trigger_minutes_null_explanation`
   - `source_vs_trigger_separation`: { markets_empty_due_to: "fetch_not_executed" | "source_returned_empty" | "inconclusive" }
   - `p26j_source_unavailable_label_retired`: true
   - `primary_classification`: 1/9 候選
   - `secondary_classification`: list
   - `actionable`: true | false
   - `p26l_required`: true | false (若 true 需附 scope justification)
2. **`p26k_api_calls_forensics_20260521.json` 必含**：
   - 02:07Z + 02:09Z 兩次 api call 的 cycle context
   - 自 daemon restart 後 api_calls_today 演進序列
   - 與 P26F commit + P26G restart timing 的關聯分析
3. **`p26k_complete_pair_decrease_root_cause_20260521.json` 必含**：
   - 被剔除的 match_id (220→219 -1 的具體 match)
   - 剔除分類：ELIGIBILITY_RULE_DRIFT / NEW_EVIDENCE_INVALIDATION / DEDUP_RECOUNT / DATA_STATE_SHIFT / INCONCLUSIVE
   - 推論依據 + 是否威脅 CLV 樣本可信度
4. **`p26k_phase9_validation_20260521.json` 必含**：
   - 親自實測的 pytest 結果 (總數 / PASS / FAIL / 執行時間)
   - 與 P26J 報告 75 PASS / 0 FAIL 的比對
   - forbidden scan 結果 (CLEAN / non-positive / positive)
5. **`p26k_final_validation_20260521.md` 必含**：
   - P26 階段終結建議 (P26K 是否為終點)
   - 下一輪建議方向 + 是否需要 CEO 顯式授權
6. **commit scope 白名單檢核** PASS：`git diff --cached --name-only` 不含 raw feed / daemon state / runtime output。
7. 全部 4 個 JSON 含 `read_only=true`、`network_call=false`、`code_modified=false`。

## Final Classification (擇一)

- `P26K_STARTUP_ONLY_FETCH_ARCHITECTURE_CONFIRMED` — CEO 第一假設成真
- `P26K_TRIGGER_RULE_GAP_CONFIRMED`
- `P26K_QUOTA_HARD_CAP_CONFIRMED`
- `P26K_NEXT_TRIGGER_SCHEDULER_BUG_CONFIRMED`
- `P26K_TIMEZONE_MISMATCH_CONFIRMED`
- `P26K_SCHEDULE_TARGET_MISMATCH_CONFIRMED`
- `P26K_SOURCE_STATE_TRULY_EMPTY_CONFIRMED`
- `P26K_GOVERNANCE_FLAG_BLOCKED_CONFIRMED`
- `P26K_ROOT_CAUSE_INCONCLUSIVE` — 需 CEO 授權更精細 logging diagnostic
- `P26K_VALIDATION_FAILED` — targeted tests FAIL 或 forbidden scan positive
- `P26K_BLOCKED_BY_SCOPE_VIOLATION` — 任務過程逾越禁止範圍
- `P26K_BLOCKED_BY_CONTEXT_CONTAMINATION` — 偵測到 Stock-Prediction/P48/P49 內容污染

---

## Required Final Output

1. daemon timeline (heartbeat count + fetched=true/false count + api_calls 增量)
2. startup-only trigger hypothesis status (CONFIRMED / PLAUSIBLE / REFUTED) + 證據
3. api_calls_today=2 forensics 結論
4. next_trigger_minutes=null 解釋
5. source vs trigger 分離結論 (markets=[] 真因)
6. COMPLETE_PAIR -1 root cause 分類 + 被剔除的 match_id
7. P26J source-unavailable label 是否正式 retire
8. primary + secondary root cause classification
9. P26K actionable? 是否需要 P26L?
10. targeted tests PASS / FAIL 實測值
11. forbidden scan 結果
12. commit hash (or 拒絕 commit 原因)
13. final classification
14. CTO agent 10 行內摘要

---

## CEO Invariants (強制不可違反)

- `paper_only=true`、`diagnostic_only=true`、**`read_only=true`** 全程維持
- `promotion`、`champion replacement`、`production proposal`、`live odds API`、`TSL crawler modification`、`daemon restart`、`scheduler/dedup/crawler/ingestion 程式碼修改` 全部禁止
- `fixed_edge_5pct` champion 保留
- PR 不得 merge
- 不新增 repo / worktree / branch
- raw feed (`tsl_odds_history.jsonl`)、daemon state、runtime output 絕對不可 commit
- **不准開 P26L/M/N** 除非 P26K 報告明確要求且 CEO 顯式授權
- **主軸一** (MLB → 台彩 paper recommendation 釋出) 與 **主軸二後置** (策略 optimizer / bootstrap) 今日**不啟動**；僅 **主軸二前置** (CLV validation readiness) 在 scope 內
- 即使發現明顯 code bug，也只能記錄為 root cause；**修復屬於 P26K 之後的另一輪任務**
- 若任何 invariant 違反 → 立即 STOP，回報 `P26K_BLOCKED_BY_SCOPE_VIOLATION`
