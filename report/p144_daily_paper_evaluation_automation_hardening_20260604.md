# P144 Daily Paper Evaluation Automation Hardening

**日期**: 2026-06-04
**任務**: P144_DAILY_PAPER_EVALUATION_AUTOMATION_HARDENING
**最終分類**: `P144_DAILY_PAPER_EVAL_AUTOMATION_HARDENING_COMMITTED_ON_RELEASE_BRANCH`
**Release branch**: `release/p144-daily-paper-evaluation-automation-hardening`

---

## 摘要

P144 將 P141 `run_paper_recommendation_job` 與 P143 `run_paper_evaluation_job` 接入頂層每日排程器 `run_daily_mlb_scheduler`，並硬化「賽前 outcome 尚不可得」這個常態路徑，使 paper 語料與逐日評估 artifact 能以**決定性 / 冪等**方式每日累積。

**142 個測試全部通過**（新增 13 個 P144 測試）。所有 paper-only / dry-run 安全閘維持啟用；`run_daily_mlb_scheduler()` 以預設參數呼叫時**不會觸發任何 live fetch**。

---

## Phase 0 驗證

| 項目 | 狀態 |
|---|---|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| 進入時 branch | `main` ✅ |
| local HEAD = origin/main | `51321c8a9440896a10ad451d59e09b2ec963391f` ✅ |
| Staged files | 0 ✅ |
| Untracked files | 0 ✅ |
| Dirty tree | 僅含 expanded tolerated daemon/runtime 噪音檔 ✅ |
| PR #6 / #7 / #8 | 全部 MERGED ✅ |
| 既有 P144 檔案 | 無 ✅ |
| P144 branch（本地/遠端） | 不存在 ✅ |

---

## 實作內容

### 1. `orchestrator/mlb_daily_scheduler.py`

**(a) 新增 data-status tokens 與門檻常數**
```python
PAPER_EVAL_STATUS_NO_PAPER_ROWS = "NO_PAPER_ROWS"
PAPER_EVAL_STATUS_OUTCOMES_UNAVAILABLE = "OUTCOMES_UNAVAILABLE"
PAPER_EVAL_STATUS_OUTCOMES_MATCHED = "OUTCOMES_MATCHED"
PAPER_EVAL_SMALL_SAMPLE_THRESHOLD = 30
```

**(b) `DailyJobResult` 新增 `details: dict` 欄位**（向後相容，預設空 dict），承載結構化評估摘要。

**(c) `run_paper_evaluation_job` 硬化**
- 新增 `write_output: bool = True` 參數；`False` 時純記憶體評估、不寫任何 artifact（供 orchestrator dry-run / no-write 路徑使用）。
- Outcome-unavailable 語意（核心硬化）：
  - `evaluated_count == 0` → `DATA_LIMITED`（`NO_PAPER_ROWS`）
  - `evaluated_count > 0 且 matched == 0` → **`DATA_LIMITED`（`OUTCOMES_UNAVAILABLE`）** ← 由原本的 `SUCCESS` 改為此（常態賽前情境）
  - `evaluated_count > 0 且 matched > 0` → `SUCCESS`（`OUTCOMES_MATCHED`）
- 小樣本警告：`0 < matched < 30` 時加 warning，metrics 不具統計意義。
- 所有分支都回傳 `DailyJobResult`，例外被捕捉為 `FAILED`（`details.data_status = EXCEPTION`），不會 crash。

**(d) `run_daily_mlb_scheduler` 接線**
- 新增參數：`run_paper_recommendation: bool = False`、`run_paper_evaluation: bool = False`，以及 `paper_allow_replay`、`paper_allow_missing_simulation_gate`、`paper_output_base_dir`、`paper_eval_paper_dir`、`paper_eval_outcome_path`、`paper_eval_output_path`。
- 在 pregame 與 postgame 之間插入 paper recommendation（step 1b）與 paper evaluation（step 1c）。
- `payload["jobs"]` 永遠包含 4 個 job；新增 `payload["scheduler_sequence"]` 清單。
- 兩個 paper step **不影響 gate / manifest**（仍由 pregame + postgame 推導），故既有行為完整保留。

#### 為何兩個 paper step 預設 OFF
- `run_paper_recommendation_job` **必然觸發 live fetch**（`_pick_game` → MLB Stats API、`_probe_tsl` → TSL API）。預設 OFF 可確保 `run_daily_mlb_scheduler()` 以預設參數呼叫（既有測試、`scripts/run_mlb_daily_scheduler.py` CLI、任何 naive caller）**永不觸發 live fetch**；每日 daemon 以 `run_paper_recommendation=True` 顯式啟用。
- `run_paper_evaluation_job` 完全離線，亦預設 OFF 以避免改變既有預設 caller 的行為足跡（含非白名單的 CLI script）；與 recommendation step 一同啟用。

### 2. `orchestrator/mlb_paper_evaluator.py`
**未修改。** Outcome-unavailable / 冪等硬化全部落在 `run_paper_evaluation_job`（scheduler）。evaluator 的 metric 數學本就是 (paper rows, outcome corpus) 的純函數，無需修改，故維持原狀以最小化 diff。

---

## Scheduler Sequence — Before / After

**Before**:
```
pregame_advisory -> postgame_review
```

**After**:
```
pregame_advisory -> paper_recommendation -> paper_evaluation -> postgame_review
```
（`payload["scheduler_sequence"]` 即為上列；paper steps 預設 `NOT_RUN`，啟用後依序執行。）

---

## Outcome-Unavailable 與 Idempotency 合約

| 情境 | data_status | job status | 行為 |
|---|---|---|---|
| 該日無 paper rows | `NO_PAPER_ROWS` | `DATA_LIMITED` | 不 crash；warning「no paper rows」 |
| 有 paper rows、outcome 尚未到 | `OUTCOMES_UNAVAILABLE` | `DATA_LIMITED` | 常態賽前情境；warning「outcomes not yet available」；可寫決定性 artifact |
| 有 paper rows、outcome 已對應 | `OUTCOMES_MATCHED` | `SUCCESS` | 有意義評估；matched<30 時加小樣本警告 |

**Idempotency**：評估 metrics 為 (paper rows, outcome corpus) 純函數。
- Outcome 到達前重跑 → metrics 與 `DailyJobResult.details` 完全相同（artifact 內 `timestamp_utc` 可能不同，metrics 不變）。
- Outcome 到達後重跑 → `SUCCESS`、`matched > 0`、同一 output path 決定性覆寫。

涵蓋測試：`test_33` / `test_34` / `test_runner_idempotent_artifact_metrics` / `test_evaluator_metrics_are_deterministic`。

---

## 實際運行觀測（2026-05-11，`write_output=False` 純記憶體）

| 指標 | 值 |
|---|---|
| status | `SUCCESS` |
| data_status | `OUTCOMES_MATCHED` |
| evaluated_count | 2 |
| matched_outcome_count | 2 |
| coverage_rate | 1.0 |
| hit_rate | 1.0 |
| brier_score | 0.211325 |
| small-sample warning | 是（matched=2 < 30）|
| artifact_written | False（避免寫出非白名單的 p143_paper_eval artifact）|

> 樣本數 2，無統計意義。隨每日鏈啟用後自動累積。

---

## 變更檔案清單（P144 白名單內）

```
orchestrator/mlb_daily_scheduler.py                                              (修改 — 接線 + 硬化 + DailyJobResult.details)
tests/test_mlb_daily_scheduler.py                                                (修改 — 新增 tests 32–41)
tests/test_mlb_paper_evaluation_runner.py                                        (修改 — 新增 3 個 runner 合約測試)
data/mlb_2026/derived/p144_daily_paper_evaluation_automation_hardening_summary.json (新建 — 任務摘要)
report/p144_daily_paper_evaluation_automation_hardening_20260604.md              (新建 — 本報告)
```
（`orchestrator/mlb_paper_evaluator.py` 在白名單內但未修改。）

---

## 測試結果

| 套件 | 指令 | 結果 | 測試數 | 新增 |
|---|---|---|---|---|
| `test_mlb_daily_scheduler.py` | `.venv/bin/python -m pytest tests/test_mlb_daily_scheduler.py -v` | **PASS** | 41 | +10 (tests 32–41) |
| `test_mlb_paper_evaluation_runner.py` | `.venv/bin/python -m pytest tests/test_mlb_paper_evaluation_runner.py -v` | **PASS** | 21 | +3 |
| `test_mlb_paper_evaluator.py` | `.venv/bin/python -m pytest tests/test_mlb_paper_evaluator.py -v` | **PASS** | 5 | 0 |
| `test_run_mlb_tsl_paper_recommendation_smoke.py` | `.venv/bin/python -m pytest tests/test_run_mlb_tsl_paper_recommendation_smoke.py -v` | **PASS** | 13 | 0 |
| `test_run_mlb_tsl_paper_recommendation_simulation_gate.py` | `.venv/bin/python -m pytest tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py -v` | **PASS** | 21 | 0 |
| `test_mlb_advisory_api.py` | `.venv/bin/python -m pytest tests/test_mlb_advisory_api.py -v` | **PASS** | 41 | 0 |
| **合計** | | **PASS** | **142** | **+13** |

---

## Paper-Only 安全閘確認

| 閘 | 狀態 |
|---|---|
| `paper_only` | ✅ |
| `dry_run` / `scheduler_dry_run_only` | ✅ |
| `no_db_writes` | ✅ |
| `no_live_api_calls` | ✅ |
| `no_provider_unlock` | ✅ |
| `no_production_betting_unlock` | ✅ |
| `no_ev_clv_kelly_unlock` | ✅ |
| 預設不觸發 live fetch | ✅（`test_38` 證明）|
| `service.py` 未修改 | ✅ |
| `.gitignore` 未修改 | ✅ |

---

## 剩餘阻擋

| ID | 阻擋 | 分類 | 影響 |
|---|---|---|---|
| B1 | TSL live feed 403 | `BLOCKS_ONLY_LIVE_ODDS` | Paper row stake=0；evaluator 以 shadow_unit_roi 處理 |
| B2 | Simulation gate BSS = −14.1% | `BLOCKS_PAPER_MLB_OUTPUT_WITH_STAKE` | Stake 阻擋；paper 審計軌跡仍寫出 |
| B3 | 無合法授權賠率（真 P0） | `BLOCKS_ONLY_PRODUCTION_RECOMMENDATION` | Paper tracking 不受影響；無 EV/CLV/Kelly unlock |
| B4 | daemon 持續重生 runtime/data/log 噪音檔 | `COSMETIC_DIRTY_TREE_NOISE` | 本任務容忍、未 stage/commit；建議獨立 `.gitignore` hygiene 任務 |
| B5 | Paper 語料極小（2 rows / 1 date）；逐日累積需 daemon 啟用 `run_paper_recommendation=True` + `run_paper_evaluation=True` | `REQUIRES_DAEMON_ENABLEMENT` | 接線已完成；語料增長取決於 daemon 啟用（live-probe）recommendation step |

---

## 明確聲明

- ✅ 無 DB writes
- ✅ 無 live API 呼叫（預設路徑不觸發 live fetch）
- ✅ 無 provider unlock
- ✅ 無 production betting unlock
- ✅ 無 EV/CLV/Kelly unlock
- ✅ `service.py` 未修改
- ✅ `.gitignore` 未修改
- ✅ 無 push、無 PR
- ✅ P145 未啟動

---

## Worker是否需要強模型

**YES** — 本任務修改每日排程器合約與 outcome-unavailable 語意，需較強模型推理編排與風控邊界。
