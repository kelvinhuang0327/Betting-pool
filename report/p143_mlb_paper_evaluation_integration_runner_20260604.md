# P143 MLB Paper Evaluation Integration Runner

**日期**: 2026-06-04
**任務**: P143_MLB_PAPER_EVALUATION_INTEGRATION_RUNNER
**最終分類**: `P143_MLB_PAPER_EVALUATION_INTEGRATION_RUNNER_READY_FOR_COMMIT`

---

## 摘要

P143 實作完成。本任務建立了一個離線、paper-only 的評估整合 runner，將 P141 PAPER 推薦輸出（`outputs/recommendations/PAPER/<date>/`）接入 P142 評估器（`orchestrator/mlb_paper_evaluator.py`），支援單日與批次兩種模式，並在 scheduler 中新增 `run_paper_evaluation_job()`。

**129 個測試全部通過**（新增 22 個 P143 測試，含 18 個 runner 測試 + 4 個 scheduler 測試）。所有 paper-only 安全閘均保持啟用。

---

## Phase 0 驗證

| 項目 | 狀態 |
|---|---|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| Branch | `main` ✅ |
| local HEAD = origin/main | `2678ec1f57e478a4a1dd443c2ad866da1e7d0639` ✅ |
| Staged files | 0 ✅ |
| PR #6 P141 | MERGED ✅ |
| PR #7 P142 | MERGED ✅ |
| P144 files | 無 ✅ |

---

## 實作內容

### 1. `scripts/run_mlb_paper_evaluation.py`（新建 — CLI runner）

鏡像 `scripts/run_mlb_tsl_paper_recommendation.py` 的 argparse 風格。

**支援模式**：

| Flag | 說明 |
|---|---|
| `--date YYYY-MM-DD` | 單日評估（與 `--all-dates` 互斥）|
| `--all-dates` | 批次評估 PAPER 根目錄下所有日期資料夾 |
| `--paper-dir PATH` | 明確指定 paper 目錄（單日：日期資料夾；批次：根目錄）|
| `--outcome-path PATH` | 明確指定 outcome JSONL 路徑（預設：`p84e`）|
| `--output PATH` | 明確指定輸出 artifact 路徑 |

安全硬閘（全部啟用）：
```python
_NO_DB_WRITES = True
_NO_LIVE_API_CALLS = True
_NO_PROVIDER_UNLOCK = True
_NO_PRODUCTION_BETTING = True
_NO_EV_CLV_KELLY_UNLOCK = True
_PAPER_ONLY = True
```

### 2. `orchestrator/mlb_daily_scheduler.py`（修改 — 新增 `run_paper_evaluation_job`）

新增 `run_paper_evaluation_job()` 函數，回傳 `DailyJobResult`：

```python
run_paper_evaluation_job(
    run_date: str,
    *,
    paper_dir: str | None = None,
    outcome_path: str | None = None,
    output_path: str | None = None,
) -> DailyJobResult
```

狀態邏輯：
- `evaluated_count == 0` → `DATA_LIMITED` + warning
- `evaluated_count > 0` → `SUCCESS`
- 任何例外 → `FAILED`

Safety flags（10 個欄位）：
```json
{
  "paper_only": true,
  "no_real_bet": true,
  "no_profit_claim": true,
  "production_modified": false,
  "no_auto_execution": true,
  "scheduler_dry_run_only": true,
  "no_ev_clv_kelly_unlock": true,
  "no_db_writes": true,
  "no_live_api_calls": true,
  "no_provider_unlock": true
}
```

**未修改**：`run_pregame_advisory_job`、`run_paper_recommendation_job`、`run_postgame_review_job` 行為不受影響。

### 3. `orchestrator/mlb_paper_evaluator.py`（最小修改）

修正了 `timestamp_utc` no-op bug：
```python
# 修改前（no-op）：
"timestamp_utc": getattr(metrics, "generated_at_utc", None) or ""

# 修改後（正確）：
"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()
```

新增兩個批次 helper：
- `discover_paper_dates(paper_root) -> list[str]` — 掃描根目錄，回傳 YYYY-MM-DD 格式的日期清單（已排序）。
- `execute_batch_evaluation(paper_root, outcome_path, summary_output_path) -> dict` — 逐日評估，聚合 per-date + aggregate 摘要。

既有指標數學（hit_rate / Brier / ROI / binomial p-value）**完全未修改**。

---

## CLI 合約

```bash
# 單日
.venv/bin/python scripts/run_mlb_paper_evaluation.py --date 2026-05-11

# 批次
.venv/bin/python scripts/run_mlb_paper_evaluation.py --all-dates

# 明確路徑
.venv/bin/python scripts/run_mlb_paper_evaluation.py \
    --paper-dir outputs/recommendations/PAPER/2026-05-11 \
    --outcome-path data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl \
    --output data/mlb_2026/derived/p143_eval_20260511.json
```

**實際運行結果（2026-06-04）**：

| 模式 | 指令 | 結果 |
|---|---|---|
| 單日 `--date 2026-05-11` | 對 2 個 paper rows 評估 | ✅ exit 0，artifact 寫出 |
| 批次 `--all-dates` | dates_found=['2026-05-11']，total_rows=2 | ✅ exit 0，artifact 寫出 |

---

## 評估器整合合約

- **Paper 目錄**：`outputs/recommendations/PAPER/<date>/`（遞歸掃描 `*.jsonl`）
- **Outcome 檔**：`data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl`（828 筆）
- **比對鍵**：game_id PK suffix（最後一段數字）
- **輸出 artifact**：`data/mlb_2026/derived/p143_paper_eval_<date_nodash>.json`

---

## 觀測到的樣本數據（2026-06-04）

| 指標 | 值 |
|---|---|
| evaluated_count | 2 |
| matched_outcome_count | 2 |
| hit_rate | 1.0 |
| brier_score | 0.211325 |
| shadow_unit_roi | 0.8886 |
| binomial_p_value | 0.25 |
| **注意** | 樣本數 2，無統計意義。隨每日鏈自動累積。|

---

## Paper-Only 安全閘確認

| 閘名 | 狀態 |
|---|---|
| `_NO_DB_WRITES = True` | ✅ 永久啟用 |
| `_NO_LIVE_API_CALLS = True` | ✅ 永久啟用 |
| `_NO_PROVIDER_UNLOCK = True` | ✅ 永久啟用 |
| `_NO_PRODUCTION_BETTING = True` | ✅ 永久啟用 |
| `_NO_EV_CLV_KELLY_UNLOCK = True` | ✅ 永久啟用 |
| `service.py` 未修改 | ✅ |
| `.gitignore` 未修改 | ✅ |
| 既有 evaluator 指標數學 | ✅ 未修改 |

---

## 測試結果

| 套件 | 結果 | 測試數 | 新增 |
|---|---|---|---|
| `test_mlb_paper_evaluation_runner.py` | **PASS** | 18 | +18 (P143) |
| `test_mlb_paper_evaluator.py` | **PASS** | 5 | 0 |
| `test_mlb_daily_scheduler.py` | **PASS** | 31 | +4 (P143 tests 28-31) |
| `test_run_mlb_tsl_paper_recommendation_smoke.py` | **PASS** | 13 | 0 |
| `test_run_mlb_tsl_paper_recommendation_simulation_gate.py` | **PASS** | 21 | 0 |
| `test_mlb_advisory_api.py` | **PASS** | 41 | 0 |
| **合計** | **PASS** | **129** | **+22** |

---

## 剩餘阻擋

| ID | 阻擋項目 | 分類 | 影響 |
|---|---|---|---|
| B1 | TSL live feed 403 Forbidden | `BLOCKS_ONLY_LIVE_ODDS` | Paper row 仍寫出（stake=0）；evaluator 正確處理 shadow_unit_roi |
| B2 | Simulation gate BSS = -14.1% | `BLOCKS_PAPER_MLB_OUTPUT_WITH_STAKE` | Stake 阻擋；paper 審計軌跡仍寫出 |
| B3 | 無合法授權賠率（True P0） | `BLOCKS_ONLY_PRODUCTION_RECOMMENDATION` | Paper tracking 不受影響 |
| B4 | `runtime/agent_orchestrator/training_memory.json` daemon 重生 | `COSMETIC_DIRTY_TREE_NOISE` | 不影響評估邏輯；建議在獨立 hygiene 任務中加 `.gitignore` |

---

## 明確聲明

- ✅ 無 DB writes
- ✅ 無 live API 呼叫
- ✅ 無 provider unlock
- ✅ 無 production betting unlock
- ✅ 無 EV/CLV/Kelly unlock
- ✅ 無 commit（未 stage）
- ✅ 無 push
- ✅ P144 未啟動

## 修改/建立檔案清單（P143 白名單內）

```
scripts/run_mlb_paper_evaluation.py                                          (新建 — CLI runner)
orchestrator/mlb_daily_scheduler.py                                          (修改 — 新增 run_paper_evaluation_job)
orchestrator/mlb_paper_evaluator.py                                          (最小修改 — timestamp_utc + batch helpers)
tests/test_mlb_paper_evaluation_runner.py                                    (新建 — 18 個 runner 測試)
tests/test_mlb_daily_scheduler.py                                            (修改 — 新增 tests 28-31)
data/mlb_2026/derived/p143_paper_eval_20260511.json                          (新建 — 單日 artifact)
data/mlb_2026/derived/p143_paper_eval_batch_20260604.json                    (新建 — 批次 artifact)
data/mlb_2026/derived/p143_mlb_paper_evaluation_integration_runner_summary.json (新建 — 任務摘要)
report/p143_mlb_paper_evaluation_integration_runner_20260604.md              (新建 — 本報告)
```
