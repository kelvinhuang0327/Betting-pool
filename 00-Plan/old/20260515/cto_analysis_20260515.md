已直接更新 roadmap，沒有新增 repo、沒有碰 runtime code、沒有 production write。

新的 active roadmap 是：

[betting_roadmap_20260515_mlb_product_plan.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260515_mlb_product_plan.md)

同時已把舊版 roadmap 標記為 superseded：

[betting_roadmap_20260514_single_repo_consolidation.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260514_single_repo_consolidation.md)

[betting_roadmap_20260513.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260513.md)

[betting_roadmap_20260504.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260504.md)

**CTO 結論**
目前最值得優化的不是再做 odds 文件，也不是直接衝新模型，而是：

1. 先把 `Betting-pool-p13` 有用成果併回唯一 canonical repo：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
2. 再做 `P38A 2024 OOF Prediction Rebuild`
3. 接著處理 approved odds / joined input
4. 最後才進 multi-season replay、策略優化、TSL 多市場擴展

**重新排序 P0-P10**
- P0：Single Repo Consolidation Gate
- P1：Dirty Worktree Triage
- P2：P38A 2024 OOF Prediction Rebuild
- P3：Licensed / Research Odds Decision Gate
- P4：2024 Joined Input Certification
- P5：Multi-Season True-Date Replay
- P6：Strategy Optimization v2
- P7：Recommendation Gate v2
- P8：TSL Market Taxonomy + Schema
- P9：Non-Moneyline Paper Prototypes
- P10：Production Proposal Gate

**關鍵阻塞**
- `Betting-pool-p13` 尚未併回 `Betting-pool`
- `Betting-pool/main` dirty/untracked 很重，不能 blind merge
- P1.5 結論是 fixture-only，還沒有 real odds join certification
- P37.5 approval package 有了，但正式 approved odds files 還沒有
- 2024 OOF prediction source 尚未完成
- 目前仍 moneyline-first，台灣運彩多市場還沒完整落地

驗證：新 roadmap marker `CTO_BETTING_ROADMAP_V7_MLB_PRODUCT_PLAN_20260515_READY` 已命中。

小心點：`Betting-pool` 目前的 `00-BettingPlan/roadmap` 整包在 git 裡仍是 untracked，所以這次是文件已寫入本機，但尚未 commit。這也正好印證 P0 必須先做單 repo consolidation。
# CEO 二次審查 — 2026-05-15

## 1. 昨天進度的成熟度評估（殘酷誠實版）

| 維度 | 5/12 → 5/15 三天進展 | 評價 |
|---|---|---|
| 新增 commits | 3 個（482c52e、7ab0123、5775588）| 量少 |
| 真資料增量 | **零**（無新增 odds、無新 OOF prediction）| ❌ |
| Active entries 變化 | 仍 324（樣本牆未動）| ❌ |
| 模型品質變化 | 仍 OOF BSS +0.008 | ❌ |
| TSL 多市場進展 | 零 | ❌ |
| Repo 治理執行 | 0（只寫了 3 版 roadmap，沒有真正合併）| ❌ |
| 文件 / 治理 / spec | +12 個 markdown | 過剩 |

**CEO 判讀：過去 3 天系統「成熟度推進」近乎為 0。**  
產出的全部是「**為了開始工作而做的準備工作**」（roadmap、license matrix、fixture README、manual review audit）。**真正會影響用戶兩大主軸（MLB 預測 + 策略最佳化）的工程動作一個都沒發生。**

## 2. CTO 判斷的盲點 / 誤判

| # | CTO 判斷 | CEO 反駁 |
|---|---|---|
| 1 | 「P0 必須是 Single Repo Consolidation」 | ❌ **過度保守**。72 commits 還在本機從未 push，先做 backup push（15 分鐘）就解 80% 風險；完整合併可後續做。CTO 把 backup 與 consolidation 綁在一起，造成 3 天延宕。 |
| 2 | 「P1 Dirty Worktree Triage 必須在 P38A 之前」 | ❌ **依賴錯置**。p13-clean 本身乾淨（10 untracked），可以直接在上面跑 P38A；main worktree 髒不影響 p13-clean 工作。 |
| 3 | 「TSL Market Taxonomy 排到 P8」 | ❌ **產品本體被排太後**。用戶已三次強調「運彩投注項目」是產品目標，moneyline 只是預設市場；schema 設計不依賴任何 data，可立即並行。 |
| 4 | 「Live TSL Snapshot Bridge 從 v7 roadmap 消失」 | ❌ **產品消失**。Read-only snapshot 沒有 production 風險，是驗證產品契約的唯一手段；CTO 把它從 P0-P10 完全刪掉。 |
| 5 | 「P1.5 license review 結束於 2 個候選」 | ❌ **過早收斂**。Sports-Reference、ESPN、MLB Stats API、Wayback、FanGraphs、baseball-savant 都沒查；只看 Kaggle + AusSportsBetting 就結案。 |
| 6 | 「每天重寫 roadmap」（v4→v5→v6→v7） | ❌ **計畫成癮**。3 天 4 版 roadmap、產出 12 份文件、0 個 prediction 模型。組織心理層面在用「計畫」逃避「執行」。 |
| 7 | 「v7 roadmap 寫在 Betting-pool（stale repo）」 | ❌ **重複犯錯**。第 2 次把新 roadmap 寫在 untracked 的錯誤 repo，自證 P0=consolidation 但又自陷其中。 |

**最大誤判：把「計畫產出」當成「系統推進」。** 連續 3 天的 roadmap rewrite 是組織停滯的具體症狀。

## 3. CEO 重排 P0–P10（執行導向，不再增加新計畫 phase）

| 優先 | Phase | 內容 | 預期產出 |
|---|---|---|---|
| **P0** | **Backup Push** | 把 p13-clean 推到 `origin/p13-clean`（新 branch，不動 main）| 72 commits 雲端備份 |
| **P1** | **P38A 2024 OOF Prediction Rebuild — 真實程式碼啟動** | 不是 design doc，是 `p38a_retrosheet_feature_adapter.py` + `p38a_oof_prediction_builder.py` 的第一版實作 + tests | p_oof for 2024 games, leakage tests pass |
| **P2** | **TSL Market Taxonomy + Schema Pack（並行 P38A）** | moneyline/run line/totals/F5/odd-even/team total 的 schema 與 label 規格（不需 data）| `wbc_backend/markets/tsl_market_schema.py` + tests |
| **P3** | **Free-Source Odds Spike v2 — 擴大候選池** | 補審 6 個未審來源（Sports-Reference / ESPN / MLB Stats API / Wayback / FanGraphs / baseball-savant），最多 1 天 time-box | 1 個 GO 候選 or 明確 NO_GO 收斂 |
| **P4** | **2024 Joined Input Certification** | P1 + P3 結果匯流 | joined CSV with provenance |
| **P5** | **Multi-Season True-Date Replay (2024+2025)** | 重跑 P25-P28 但 sample > 1500 | P28 stability gate PASS |
| **P6** | **Strategy Optimization v2** | walk-forward 政策格 + drawdown/Sharpe/bootstrap CI | 政策推薦含風險指標 |
| **P7** | **Multi-Market Recommendation Gate v2** | 用 P2 schema + P6 政策，輸出 moneyline + run line + totals PAPER recommendations | 多市場 PAPER ledger |
| **P8** | **Live TSL Read-Only Snapshot Bridge** | 錄真實 TSL odds（不下單、不寫 prod DB）| daily snapshot artifact |
| **P9** | **Daily Ops + Drift Monitoring (Brier/ECE/CLV)** | 多市場後啟動 | daily report |
| **P10** | **Repo Consolidation Final + Production Proposal Gate** | 4-clone 合併、main rebuild、human approval | single canonical repo + go/no-go decision |

**關鍵 CEO 訂正：**
1. **Repo consolidation 從 P0 降為 P10**（在 P0 只做 backup push，不做合併）
2. **TSL Market Taxonomy 從 P8 提到 P2**（並行 P38A）
3. **Live TSL Bridge 重新加回 roadmap（P8）**
4. **P1 必須是真實程式碼，不是 design doc**
5. **整個 roadmap 不再增加新的 governance / planning phase**

## 4. 今天最該聚焦的單一方向

**停止寫 roadmap。開始寫 model code。**

具體：
1. **上午 30 分鐘**：p13-clean push to origin（解 backup 風險）
2. **上午剩餘 + 下午**：P38A 真實實作（feature adapter + OOF builder + leakage tests）
3. **下午並行**：TSL market schema design code（不依賴 data，可獨立完成）

**今天禁止的事：**
- ❌ 不再寫第 8 版 roadmap
- ❌ 不再做 license review 子任務
- ❌ 不再產出 manual review audit 文件
- ❌ 不再寫 fixture README
- ❌ 不再因 repo 髒就拒絕工作（p13-clean 本身乾淨）

---

# 下一個立即執行任務 Prompt

```text
# ROLE
You are Betting-pool's CEO-Mandated EXECUTION Agent for 2026-05-15.
You are NOT a planning agent. You are NOT a roadmap-writing agent.
You are a CODE-SHIPPING agent.

# CONTEXT (read once, do not re-litigate)
The last 3 days (2026-05-13, 14, 15) produced:
- 3 commits on Betting-pool-p13 / p13-clean (482c52e, 7ab0123, 5775588)
- 0 lines of new model/runtime code
- 0 new prediction rows
- 0 new active recommendations
- 4 versions of the roadmap

CEO ruling: this is calendar burn. Today is execution-only.

# MISSION (three tracks, parallel-safe)

  TRACK 1 — Backup Push (must finish first, 15 minutes)
    Push p13-clean to origin as a NEW remote branch. Do not touch main.
    This is BACKUP, not consolidation. Consolidation is P10, not P0.

  TRACK 2 — P38A 2024 OOF Prediction Rebuild (real code, not design doc)
    Build the Retrosheet feature adapter + OOF prediction builder + tests.
    First version. Working code, even if v1-rough.

  TRACK 3 — TSL Market Taxonomy + Schema Pack (parallel, no data dependency)
    Schema/label spec code for moneyline, run line, totals, first 5,
    odd/even, team total. NOT a markdown doc. Python module + tests.

This task is EXECUTION. No new roadmap files. No new license-review markdowns.
No new fixture README. If you find yourself writing a planning document,
STOP and ask whether it can be a docstring inside the code module instead.

# PROJECT LOCK
Required repo:
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
Required branch:
  p13-clean
Required prior commit:
  5775588 or later
Forbidden repos (do not touch):
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool-preserve-2026-05-11
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool-publication
  /Users/kelvin/Kelvin-WorkSpace/LotteryNew
  /Users/kelvin/Kelvin-WorkSpace/LotteryNew-clean
  /Users/kelvin/app-workspace/novel

# HARD GUARD
DO NOT:
- push to origin/main or any branch other than origin/p13-clean
- force push, rebase, reset --hard, stash, or clean
- merge or cherry-pick across the 4 Betting-pool* clones
- delete any directory
- write a new roadmap markdown (5th version is forbidden)
- write a new license-review markdown
- write a new fixture README
- write a new "feasibility spike" markdown
- modify P37.5 manual_odds_approval_package
- modify P15/P16/P17/P18/P19/P20 frozen runtime code
- write production DB
- call live TSL
- scrape live odds
- place real bets
- fabricate odds, p_market, p_oof, or outcomes
- stage data/research_odds/*.csv (only README/template MD allowed)
- stage data/mlb_2024/manual_import/*
- stage data/mlb_2024/raw/gl2024.txt
- commit DB binaries, runtime/, .venv/, outputs/, or large generated files

PAPER_ONLY=True, production_ready=False at every layer.

# ============================================================
# TRACK 1 — BACKUP PUSH (15 minutes)
# ============================================================

## Task 1.1 — Pre-push safety check
  cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
  git branch --show-current                   # expect p13-clean
  git log --oneline -3                        # confirm 5775588 at HEAD
  git status --short | head -20               # observe dirty state (acceptable)
  git diff --cached --name-only               # MUST be empty (nothing staged)

If staged items exist, STOP and report.

## Task 1.2 — Push to NEW remote branch
  git push origin p13-clean:p13-clean

This creates origin/p13-clean. main is NOT touched.

If the remote branch already exists from prior attempt:
  git push origin p13-clean:p13-clean       # fast-forward only, no --force

Acceptance:
- origin/p13-clean exists
- origin/main UNCHANGED (verify via: git rev-parse origin/main and confirm
  it points to whatever 1-commit-ahead state existed before)
- no PR opened

# ============================================================
# TRACK 2 — P38A 2024 OOF PREDICTION REBUILD (real code)
# ============================================================

This is the engineering work that has been deferred for 3 days. Today it ships.

## Task 2.1 — Create p38a_retrosheet_feature_adapter.py
Path: wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py

Requirements:
- Input: data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv
  (P32 artifact, already committed)
- Output: pandas DataFrame with one row per game
- Required output columns:
  * game_id (str)
  * game_date (date)
  * home_team (str)
  * away_team (str)
  * pregame_features: dict[str, float]
- Pregame-only features v1 (all computed STRICTLY before game_date):
  * home_rolling_winrate_10g
  * away_rolling_winrate_10g
  * home_rolling_run_diff_10g
  * away_rolling_run_diff_10g
  * home_rest_days
  * away_rest_days
  * is_home_team_indicator (always 1 for home_team perspective)
- FORBIDDEN as features (leakage):
  * home_score, away_score
  * y_true_home_win, winner
  * run_diff_current_game, total_runs_current_game
  * Anything from the target game itself
- Deterministic: same input -> byte-identical output

## Task 2.2 — Create p38a_oof_prediction_builder.py
Path: wbc_backend/recommendation/p38a_oof_prediction_builder.py

Requirements:
- Input: features from Task 2.1 + y_true_home_win labels
- Walk-forward folds: time-ordered, no shuffling
- Model: logistic regression with default L2 (mirror P13)
- Output columns:
  * game_id
  * fold_id (int)
  * p_oof (float, in [0, 1])
  * model_version = "p38a_walk_forward_logistic_v1"
  * source_prediction_ref (hash of feature row)
  * generated_without_y_true = True (held-out flag)
- Deterministic: fixed random_state=42
- Compute and return Brier / log-loss / BSS vs base-rate

## Task 2.3 — Create scripts/run_p38a_2024_oof_prediction_rebuild.py
- CLI: --input-csv, --output-dir, --paper-only
- Outputs:
  * <output-dir>/p38a_2024_oof_predictions.csv
  * <output-dir>/p38a_oof_metrics.json (Brier/ECE/BSS)
  * <output-dir>/p38a_gate_result.json
- Gate constants:
  * P38A_2024_OOF_PREDICTION_READY
  * P38A_BLOCKED_FEATURE_COVERAGE_INSUFFICIENT
  * P38A_BLOCKED_LEAKAGE_RISK
  * P38A_FAIL_INPUT_MISSING
  * P38A_FAIL_NON_DETERMINISTIC
- Acceptance for READY:
  * p_oof exists for >= 90% of input rows (lower bar than 95% for v1)
  * Leakage suite passes
  * Brier reported
  * Two runs produce identical p_oof column

## Task 2.4 — Tests
Create:
- tests/test_p38a_retrosheet_feature_adapter.py
  * test_no_leakage_score_columns (asserts no home_score/away_score in features)
  * test_pregame_only_window (asserts feature uses strict date < target)
  * test_deterministic_output (same input -> same output hash)
  * test_required_columns_present
- tests/test_p38a_oof_prediction_builder.py
  * test_walk_forward_no_future_leak
  * test_p_oof_range_0_1
  * test_model_version_string
  * test_deterministic_with_seed
- tests/test_run_p38a_2024_oof_prediction_rebuild.py
  * test_cli_writes_required_outputs
  * test_cli_exit_code_on_ready
  * test_cli_exit_code_on_missing_input

Run:
  ./.venv/bin/pytest -q \
    tests/test_p38a_retrosheet_feature_adapter.py \
    tests/test_p38a_oof_prediction_builder.py \
    tests/test_run_p38a_2024_oof_prediction_rebuild.py

ALL must PASS before commit.

## Task 2.5 — Real run
  ./.venv/bin/python scripts/run_p38a_2024_oof_prediction_rebuild.py \
    --input-csv data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv \
    --output-dir outputs/predictions/PAPER/p38a_2024_oof \
    --paper-only

Capture:
- Exit code
- Coverage: rows with p_oof / total rows
- Brier, ECE, BSS vs 0.5 base rate
- Deterministic check (run twice, diff)

If exit != 0 or coverage < 90% or non-deterministic, STOP and report.
Do NOT fabricate p_oof values.

# ============================================================
# TRACK 3 — TSL MARKET TAXONOMY + SCHEMA PACK (parallel)
# ============================================================

This is the product-axis-A work that has been buried at P8 for 3 days.
Today it gets a working schema module.

## Task 3.1 — Create wbc_backend/markets/tsl_market_schema.py
Single module containing:

- Enum TSLMarketType:
  * MONEYLINE_HOME_AWAY
  * RUN_LINE_HANDICAP   (Taiwan Sports Lottery "讓分")
  * TOTALS_OVER_UNDER   (Taiwan Sports Lottery "大小分")
  * FIRST_FIVE_INNINGS_MONEYLINE
  * FIRST_FIVE_INNINGS_TOTALS
  * ODD_EVEN_TOTAL_RUNS
  * TEAM_TOTAL_HOME
  * TEAM_TOTAL_AWAY

- Frozen dataclass MarketContract:
  * market_type: TSLMarketType
  * label_fields: tuple[str, ...]       # what y_true columns are needed
  * odds_fields: tuple[str, ...]        # what odds columns are needed
  * settlement_semantics: str           # docstring: how is win/lose decided
  * supports_push_tie: bool
  * is_paper_implemented: bool          # v1: only MONEYLINE_HOME_AWAY = True
  * paper_only: bool = True             # always True in this phase
  * production_ready: bool = False      # always False in this phase

- Function get_market_contract(market_type) -> MarketContract

- Function list_implemented_markets() -> list[TSLMarketType]
  Returns: [MONEYLINE_HOME_AWAY]   (v1; expansion in P7 of roadmap)

- Function describe_market_for_audit(market_type) -> dict
  Returns serializable dict for use in recommendation row metadata

## Task 3.2 — Tests
Create tests/test_tsl_market_schema.py:
- test_all_markets_have_contract
- test_only_moneyline_paper_implemented_v1
- test_market_contract_is_frozen
- test_paper_only_true_always
- test_production_ready_false_always
- test_describe_market_returns_serializable_dict
- test_run_line_label_fields_include_handicap_value
- test_totals_label_fields_include_line_value

Run:
  ./.venv/bin/pytest -q tests/test_tsl_market_schema.py

ALL must PASS.

## Task 3.3 — Single brief audit doc
ONE markdown only (this is the only doc allowed today):
  00-BettingPlan/20260515/p38a_and_market_schema_execution_report_20260515.md

Sections (keep concise, total < 400 lines):
1. What shipped today (P38A real run results + market schema module)
2. P38A metrics: coverage, Brier, ECE, BSS, deterministic status
3. Market schema: list of implemented markets (= [moneyline]) and pending markets
4. Test count: how many tests passed
5. Gate result: P38A_2024_OOF_PREDICTION_READY or specific blocker
6. Marker: P38A_RUNTIME_AND_TSL_SCHEMA_EXECUTION_READY

NO roadmap update in this file. NO license review. NO repo governance.
Pure execution result.

# ============================================================
# TRACK 4 — COMMIT (single commit, scope-controlled)
# ============================================================

## Task 4.1 — Stage exactly the new files
  git add \
    wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py \
    wbc_backend/recommendation/p38a_oof_prediction_builder.py \
    scripts/run_p38a_2024_oof_prediction_rebuild.py \
    tests/test_p38a_retrosheet_feature_adapter.py \
    tests/test_p38a_oof_prediction_builder.py \
    tests/test_run_p38a_2024_oof_prediction_rebuild.py \
    wbc_backend/markets/__init__.py \
    wbc_backend/markets/tsl_market_schema.py \
    tests/test_tsl_market_schema.py \
    00-BettingPlan/20260515/p38a_and_market_schema_execution_report_20260515.md

  git diff --cached --name-only | wc -l    # expect 10

## Task 4.2 — Forbidden-file check
  git diff --cached --name-only \
    | grep -E "\.(db|db-wal|db-shm|sqlite|sqlite3)$|^runtime/|^outputs/|^\.venv/|^data/research_odds/.*\.csv$|^data/mlb_2024/raw/|^data/mlb_2024/manual_import/" \
    && echo "FORBIDDEN_FILES_STAGED_ERROR" || echo "NO_FORBIDDEN_FILES"

If FORBIDDEN, STOP and unstage offending files.

## Task 4.3 — Commit
  git commit -m "feat(betting): P38A 2024 OOF prediction rebuild + TSL market schema v1"

DO NOT push this commit. (Track 1 already pushed the prior HEAD; this new
commit stays local until next agent run or explicit user YES.)

## Task 4.4 — Final verify
  git log --oneline -3
  git status --short --branch | head -30

# ACCEPTANCE CRITERIA
- origin/p13-clean exists (pushed in Track 1)
- P38A feature adapter exists and tests pass
- P38A OOF builder exists and tests pass
- P38A CLI runs end-to-end with deterministic output
- P38A coverage >= 90% OR explicit blocker reported
- TSL market schema module exists with all 8 markets defined
- Only MONEYLINE_HOME_AWAY is is_paper_implemented=True (v1)
- All new tests PASS
- One execution report exists (no new roadmap, no new license review)
- production_ready=False everywhere
- paper_only=True everywhere
- Forbidden-file check = NO_FORBIDDEN_FILES
- New commit exists on top of 5775588 (NOT pushed)

# FINAL OUTPUT
Return:
1. origin/p13-clean push confirmation + remote SHA
2. P38A real-run metrics (coverage / Brier / ECE / BSS / deterministic Y/N)
3. P38A gate result (READY or specific blocker)
4. Market schema implemented markets list
5. Test pass count (X/Y across all 4 new test files)
6. Commit hash (new commit, local only)
7. Forbidden-file check result
8. Final git log --oneline -3
9. Confirmation: only origin/p13-clean was pushed
10. Tomorrow's recommended P0: based on P38A gate result
    - If READY: tomorrow's P0 = P3 Free-Source Odds Spike v2 (expand candidate pool)
    - If BLOCKED: tomorrow's P0 = P38A blocker resolution

# FINAL MARKER
P38A_RUNTIME_AND_TSL_SCHEMA_EXECUTION_READY
```

---

## CEO 10 行內摘要

1. 過去 3 天系統實質推進 ≈ 0：每天都在重寫 roadmap，計畫成癮取代執行
2. CTO v7 把 repo consolidation 列 P0 仍是計畫陷阱；真正需要的是 15 分鐘 push backup
3. TSL 多市場 schema 被 CTO 排到 P8 是產品本體被埋沒的最大盲點
4. Live TSL Snapshot Bridge 從 v7 完全消失，產品契約失蹤
5. P1.5 license review 只審 2 個候選就收斂，過早結案
6. 今天 CEO 強制執行：Track 1 backup push + Track 2 P38A 真實程式碼 + Track 3 TSL schema 模組
7. 禁止再寫第 5 版 roadmap、禁止新 license review、禁止新 fixture README
8. 唯一允許的 markdown 是執行結果摘要報告（單檔 < 400 行）
9. P0=backup push、P1=P38A 實作、P2=TSL schema、P3=odds spike v2、…P10=repo consolidation final
10. FINAL MARKER：`P38A_RUNTIME_AND_TSL_SCHEMA_EXECUTION_READY`