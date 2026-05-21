# Active Task — P26H Pair Formation Monitor + P26G Delivery Closure

> **[COMPLETED 2026-05-21]** `P26H_PAIR_FORMATION_MONITOR_AND_P26G_CLOSURE_20260521`
> CEO Decision: `CEO_DECISION_PARTIALLY_APPROVED` (2026-05-21)
> 主軸對齊：主軸二前置 (CLV validation readiness)
> 模式：`paper_only=true`、`diagnostic_only=true`、`production_proposal=false`
> **Final Classification**: `P26H_EXPECTED_PAIRS_PREDICTION_BROKEN`
> **Next Task**: P26I — Closing Window Capture Gap Investigation (3469930.1, 3469931.1)

---

## Branch Governance (MANDATORY)

- Canonical Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Canonical Branch: `main`
- 禁止新增 branch / worktree / clone / detached HEAD
- 新分支需明確授權：`YES: create new branch for <reason>`

### Pre-flight (必跑)

```bash
cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool
git rev-parse --show-toplevel
git branch --show-current
git status --short
git fetch origin
git status --branch --short
git log --oneline -8
```

若 repo 非 canonical / branch 非 `main` / detached HEAD → 立即 STOP。

---

## 任務名稱

`P26H_PAIR_FORMATION_MONITOR_AND_P26G_CLOSURE_20260521`

## 背景

1. **P26F runtime 已生效** (HEAD = `8a98f52`)：
   - Daemon PID 1715 → 15022，Cycle #1 已完成。
   - `force_closing_snapshot=True` rows = 10 (repo artifact)。
   - `dedup_bypassed=True` rows = **7** (以 repo artifact 為單一事實源，交接報告寫 2 為觀測 timing 差異，不採用)。
   - 1 row 在 closing window (gap=-0.53h)，但缺對應 pregame。

2. **COMPLETE_PAIR 仍為 220**：
   - Delta = 0，未形成新 CLV pair。
   - P25C bootstrap 正確 NOT RUN (220 < 300)。

3. **P26G artifacts 已產出但 untracked**：
   - `data/paper_recommendations/p26g_coverage_recheck_post_p26f_20260521.json`
   - `report/p26g_coverage_recheck_post_p26f_20260521.md`
   - `00-BettingPlan/20260521/p26g_coverage_recheck_post_p26f_20260521.md`
   - git log 中無 P26G commit hash → **交付未閉環**。

4. **P26G JSON 自宣告今日預計 +2 pair**：
   - `next_closing_candidates` = [3469930.1, 3469931.1]（兩者皆 `has_pregame=true`，`window_entry_utc=07:00Z`）
   - `expected_new_pairs_today: 2`
   - **必須驗證** 此自動預測為 ground truth 或修正預測邏輯。

5. **Phase 8 validation 結果在 P26G 缺失**，必須 rerun 並記錄實測值。

6. **dirty worktree** 包含 30+ 個 daemon/runtime/data 檔 (含 `tsl_odds_history.jsonl` 2892 行)，commit scope **必須白名單**，禁止 stage raw feed。

---

## 目標

1. **P26G 治理閉環**：將既有 P26G artifacts (JSON/MD/BettingPlan) 提交至 main，產出 commit hash。
2. **P26H Pair Formation Monitor**：對 force_closing rows 做 match-level 分類，記錄 COMPLETE_PAIR before/after，**驗證 expected_new_pairs_today=2**。
3. **P1 missing-pregame 初步分類**：對每個 force_closing row 標註 missing_pregame / missing_closing / complete / ambiguous。
4. **Phase 8 targeted tests rerun + forbidden scan**：實測非沿用。
5. 若且僅若 COMPLETE_PAIR >= 300，才執行 P25C bootstrap；否則僅輸出 monitoring artifact。

---

## 允許修改範圍

### 新增 JSON artifacts

- `data/paper_recommendations/p26h_force_closing_pair_formation_20260521.json`
- `data/paper_recommendations/p26h_pregame_gap_classification_20260521.json`
- `data/paper_recommendations/p26h_phase8_validation_20260521.json`
- 若 bootstrap 執行：`data/paper_recommendations/p25c_clv_bootstrap_rerun_20260521.json`

### 新增 Markdown reports

- `report/p26h_force_closing_pair_formation_20260521.md`
- `report/p26h_pregame_gap_classification_20260521.md`
- `report/p26h_final_validation_20260521.md`
- `00-BettingPlan/20260521/p26h_pair_formation_monitor_20260521.md`
- 若 bootstrap 執行：`report/p25c_clv_bootstrap_rerun_20260521.md`、`00-BettingPlan/20260521/p25c_clv_bootstrap_rerun_20260521.md`

### 允許讀取

- `data/tsl_odds_history.jsonl` (**只讀**)
- `data/mlb_context/odds_capture_schedule.json` (**只讀**)
- `data/paper_recommendations/p26g_*` (既有)
- `data/paper_recommendations/p26f_*` (既有)
- `report/p26g_*`、`report/p26f_*` (既有)
- `logs/daemon_heartbeat.jsonl` (**只讀**)
- `tests/` 目錄

### Commit scope 白名單 (嚴格)

僅允許 stage 以下檔案：

```
data/paper_recommendations/p26g_coverage_recheck_post_p26f_20260521.json
report/p26g_coverage_recheck_post_p26f_20260521.md
00-BettingPlan/20260521/p26g_coverage_recheck_post_p26f_20260521.md
data/paper_recommendations/p26h_*_20260521.json
report/p26h_*_20260521.md
00-BettingPlan/20260521/p26h_*_20260521.md
00-Plan/roadmap/CEO-Decision.md
00-Plan/roadmap/CTO-Analysis.md
00-Plan/roadmap/roadmap.md
00-Plan/roadmap/active_task.md
```

若執行 bootstrap，額外允許：
```
data/paper_recommendations/p25c_clv_bootstrap_rerun_20260521.json
report/p25c_clv_bootstrap_rerun_20260521.md
00-BettingPlan/20260521/p25c_clv_bootstrap_rerun_20260521.md
```

---

## 禁止修改範圍 (絕對禁止)

- ❌ 不得 stage 或 commit `data/tsl_odds_history.jsonl` (raw feed)
- ❌ 不得 stage 或 commit `data/tsl_odds_snapshot.json`、`data/tsl_fetch_status.json`、`data/.live_cache/*`、`logs/daemon_heartbeat.jsonl`
- ❌ 不得 stage 或 commit `data/learning_state.json`、`data/mlb_context/external_closing_state.json`、`data/mlb_context/odds_capture_schedule.json`、`data/mlb_context/odds_timeline.jsonl`
- ❌ 不得 stage 或 commit `outputs/predictions/PAPER/**`、`data/wbc_backend/**` 等 runtime output
- ❌ 不得 `git add .` 或 `git add -A`，必須逐檔指定
- ❌ 不得重啟 daemon
- ❌ 不得修改 scheduler / dedup / crawler / ingestion 程式碼
- ❌ 不得呼叫 live odds API
- ❌ 不得手動補造 snapshots
- ❌ 不得替換 champion `fixed_edge_5pct`
- ❌ 不得啟動 optimizer promotion
- ❌ 不得發布 production proposal
- ❌ 不得宣稱可獲利 / profitability claim
- ❌ 不得 merge PR #2
- ❌ 不得新增 repo / worktree / branch
- ❌ 不得執行 P25C bootstrap 除非 COMPLETE_PAIR >= 300
- ❌ 不得修改 `data/tsl_odds_history.jsonl` 或任何 raw source data

---

## 執行階段

### Phase 0 — Pre-flight

如上 Branch Governance 區塊；若 STOP 條件觸發，立即停止。

### Phase 1 — P26G Closure Inventory

1. 確認 P26G 三個 artifact 檔存在 (JSON/MD/BettingPlan)。
2. 從 P26G JSON 讀出：
   - `force_closing_rows = 10`
   - `dedup_bypassed_true_count = 7`
   - `closing_gap_le_2h_count = 1`
   - `coverage_before.complete_pair = 220`
   - `coverage_after.complete_pair = 220`
   - `next_closing_candidates` (3469930.1, 3469931.1)
   - `expected_new_pairs_today = 2`
3. 確認 P26G artifact 已準備提交 (作為 Phase 8 commit 一部分)。

### Phase 2 — Force-Closing Row Inventory

只讀 `data/tsl_odds_history.jsonl`，統計：

1. total rows
2. `force_closing_snapshot=True` rows (應為 10，需驗證)
3. `dedup_bypassed=True` rows (應為 7，需驗證)
4. `capture_reason="closing_window"` rows
5. 依 match_id 分組的 force_closing rows
6. 依 gap to game_time 分組 (≤2h / 2-6h / 6-15h / >15h)
7. 每 row 的 match_id、game_time_utc、snapshot_ts_utc、gap_hours

### Phase 3 — Pair Formation Diagnosis

對每個 force_closing row 的 match_id，跨整個 history 查詢：

- `has_pregame_snapshot` (≥4h 前)
- `has_closing_snapshot` (≤2h 內)
- `complete_pair`
- `missing_side`：
  - `complete`
  - `missing_pregame`
  - `missing_closing`
  - `ambiguous`
- `earliest_pregame_gap_hours`
- `closest_closing_gap_hours`
- markets available (MNL/HDC/OU/F5...)
- `line_comparable_potential` 若資訊足夠

### Phase 4 — Expected_New_Pairs Ground Truth 驗證

針對 P26G 自宣告的 `next_closing_candidates`：

1. 3469930.1：是否在今日內取得 closing snapshot？
2. 3469931.1：是否在今日內取得 closing snapshot？
3. 結果三選一：
   - `MATCHED`：兩場皆形成 COMPLETE_PAIR
   - `PARTIAL`：1 場形成
   - `UNMATCHED`：0 場形成 → P26G 自我預測 broken，需補一個 diagnostic 而非進入 P26I

### Phase 5 — Coverage Recheck

重新統計：

1. COMPLETE_PAIR current
2. delta vs P26G baseline = 220
3. missing_pregame count (在 force_closing rows 中)
4. missing_closing count
5. ambiguous count
6. 是否 COMPLETE_PAIR >= 300

若 < 300：
- 不執行 bootstrap
- 輸出 P26H monitoring artifact
- Final Classification 候選：`P26H_PAIR_FORMATION_BELOW_BOOTSTRAP_THRESHOLD` 或 `P26H_PREGAME_GAP_CONFIRMED`

若 >= 300：
- 執行 Phase 6 P25C bootstrap rerun

### Phase 6 — P25C Bootstrap (僅 COMPLETE_PAIR >= 300 時)

- filter `line_comparable=True`
- exclude `LINE_SHIFT_UNCOMPARABLE`
- iterations = 5000
- seed = 42
- output per-market + overall CI
- 若 CI cross zero → 不可宣稱 edge → `P25C_..._INCONCLUSIVE`

### Phase 7 — Targeted Tests + Forbidden Scan

```bash
source .venv/bin/activate

# Targeted tests
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

# Forbidden scan (新產出檔)
grep -RniE "production proposal|promotion|profitab|guaranteed profit|live odds api|crawler modif|champion replacement" \
  report/p26h_*_20260521.md \
  00-BettingPlan/20260521/p26h_*_20260521.md \
  data/paper_recommendations/p26h_*_20260521.json \
  $( [ -f data/paper_recommendations/p25c_clv_bootstrap_rerun_20260521.json ] && echo "data/paper_recommendations/p25c_clv_bootstrap_rerun_20260521.json report/p25c_clv_bootstrap_rerun_20260521.md 00-BettingPlan/20260521/p25c_clv_bootstrap_rerun_20260521.md" ) \
  || echo "GREP_CLEAN_CANDIDATE"
```

註：若只命中 governance guard 的 `false` 欄位 (e.g. `"promotion_allowed": false`)，標記為 `non-positive hit`，仍視為 CLEAN。

### Phase 8 — Commit (白名單 only)

```bash
# 1. P26G closure files
git add data/paper_recommendations/p26g_coverage_recheck_post_p26f_20260521.json \
        report/p26g_coverage_recheck_post_p26f_20260521.md \
        00-BettingPlan/20260521/p26g_coverage_recheck_post_p26f_20260521.md

# 2. P26H monitoring files
git add data/paper_recommendations/p26h_force_closing_pair_formation_20260521.json \
        data/paper_recommendations/p26h_pregame_gap_classification_20260521.json \
        data/paper_recommendations/p26h_phase8_validation_20260521.json \
        report/p26h_force_closing_pair_formation_20260521.md \
        report/p26h_pregame_gap_classification_20260521.md \
        report/p26h_final_validation_20260521.md \
        00-BettingPlan/20260521/p26h_pair_formation_monitor_20260521.md

# 3. Roadmap governance files
git add 00-Plan/roadmap/CEO-Decision.md \
        00-Plan/roadmap/CTO-Analysis.md \
        00-Plan/roadmap/roadmap.md \
        00-Plan/roadmap/active_task.md

# 4. (Conditional) P25C bootstrap files
# git add data/paper_recommendations/p25c_clv_bootstrap_rerun_20260521.json \
#         report/p25c_clv_bootstrap_rerun_20260521.md \
#         00-BettingPlan/20260521/p25c_clv_bootstrap_rerun_20260521.md

# 5. Verify no raw feed staged
git diff --cached --name-only | grep -E "tsl_odds_history|tsl_odds_snapshot|tsl_fetch_status|live_cache|daemon_heartbeat|learning_state|odds_capture_schedule|odds_timeline" && echo "FORBIDDEN_STAGED" || echo "STAGE_CLEAN"

# 6. Commit (僅在 STAGE_CLEAN 時執行)
git commit -m "P26H+P26G: pair formation monitor + closure

- P26G artifacts committed (force_closing rows=10, dedup_bypassed=7, COMPLETE_PAIR=220)
- P26H pair formation monitor: force_closing match-level classification
- Expected_new_pairs_today=2 ground truth validation
- COMPLETE_PAIR <delta>; P25C bootstrap <ran|blocked>
- paper_only=true; promotion=frozen; production_proposal=false

Final Classification: <see active_task>"
```

---

## 驗收標準

1. **P26G artifacts 已 commit**，git log 顯示包含 P26G/P26H 的 commit hash。
2. **`p26h_force_closing_pair_formation_20260521.json` 必含**：
   - `paper_only=true`
   - `diagnostic_only=true`
   - `production_proposal=false`
   - `promotion_allowed=false`
   - `profitability_claim=false`
   - `champion_replacement_allowed=false`
   - `force_closing_rows_total: <int>`
   - `dedup_bypassed_count: <int>` (應 = 7 或合理修正)
   - `pair_formation_breakdown` (complete/missing_pregame/missing_closing/ambiguous counts)
   - `coverage_before.complete_pair: 220`
   - `coverage_after.complete_pair: <int>`
   - `delta_complete_pairs: <int>`
   - `whether_bootstrap_ran: false|true`
   - `expected_new_pairs_today_ground_truth: MATCHED|PARTIAL|UNMATCHED`
   - `final_classification: <one of below>`
3. **`p26h_pregame_gap_classification_20260521.json` 必含**：
   - 對每個 force_closing match 的 missing_side 標籤
   - 初步原因分類：`natural_late_listing` / `pregame_capture_gap` / `matching_rule_question` / `inconclusive`
4. **`p26h_phase8_validation_20260521.json` 必含**：
   - targeted pytest 實測值 (PASS/FAIL/總數/執行時間)
   - forbidden scan 結果 (CLEAN / non-positive hit / positive)
5. **commit scope 白名單檢核**：`git diff --cached --name-only` 不含 raw feed / daemon state / runtime output。
6. **兩大主軸對齊註記**：每個 JSON 含 `axis_alignment: "axis_2_clv_validation_precondition"` 欄位。

## Final Classification (擇一)

- `P26H_PAIR_FORMATION_CONFIRMED` — COMPLETE_PAIR 增長且 expected_new_pairs ground truth = MATCHED
- `P26H_PAIR_FORMATION_BELOW_BOOTSTRAP_THRESHOLD` — pair 有增長但 < 300
- `P26H_MISSING_PREGAME_BLOCKER_CONFIRMED` — 多數 force_closing rows 缺 pregame，需 P26I 診斷 pregame capture
- `P26H_EXPECTED_PAIRS_PREDICTION_BROKEN` — expected_new_pairs_today=2 為 UNMATCHED，P26G 自我預測 broken
- `P26H_MONITOR_INCONCLUSIVE` — 資料不足以分類
- `P25C_CLV_BOOTSTRAP_RERUN_COMPLETED_INCONCLUSIVE` — bootstrap 跑了但 CI cross zero
- `P25C_CLV_BOOTSTRAP_RERUN_COMPLETED_POSITIVE` — bootstrap CI > 0
- `P25C_CLV_BOOTSTRAP_RERUN_COMPLETED_NEGATIVE` — bootstrap CI < 0
- `P26H_VALIDATION_FAILED` — targeted tests FAIL 或 forbidden scan positive hit
- `P26H_BLOCKED_BY_SCOPE_VIOLATION` — 任務過程逾越禁止範圍

---

## Required Final Output

1. force_closing rows count (實測 vs P26G artifact 7)
2. dedup_bypassed count (實測 vs P26G artifact 7)
3. pair formation breakdown (complete / missing_pregame / missing_closing / ambiguous)
4. COMPLETE_PAIR before / after / delta
5. expected_new_pairs_today ground truth (MATCHED / PARTIAL / UNMATCHED)
6. whether P25C bootstrap was run
7. targeted tests PASS / FAIL counts
8. forbidden scan result (CLEAN / non-positive / positive)
9. commit hash (or 拒絕 commit 原因)
10. final classification
11. CTO agent 10 行內摘要

---

## CEO Invariants (強制不可違反)

- `paper_only=true` 全程維持
- `promotion`、`champion replacement`、`production proposal`、`live odds API`、`TSL crawler modification` 全部禁止
- `fixed_edge_5pct` champion 保留
- PR #2 不得 merge
- 不新增 repo / worktree / branch
- 不重啟 daemon、不改 scheduler、不改 dedup
- raw feed (`tsl_odds_history.jsonl`) 與 runtime state 絕對不可 commit
- **主軸一** (MLB → 台彩 paper recommendation) 與 **主軸二 後置** (策略 optimizer diagnostic) 今日**不啟動**；僅 **主軸二前置** (CLV validation readiness) 在 scope 內
- 若任何 invariant 違反 → 立即 STOP，回報 `P26H_BLOCKED_BY_SCOPE_VIOLATION`
