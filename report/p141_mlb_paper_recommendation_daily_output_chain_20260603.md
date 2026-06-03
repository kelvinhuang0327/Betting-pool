# P141 MLB Paper Recommendation Daily Output Chain

**日期**: 2026-06-03
**任務**: P141_MLB_PAPER_RECOMMENDATION_DAILY_OUTPUT_CHAIN
**最終分類**: `P141_MLB_PAPER_RECOMMENDATION_DAILY_OUTPUT_CHAIN_READY_FOR_COMMIT`

---

## 摘要

P141 實作完成。MLB→TSL paper-only 推薦輸出鏈現在可透過排程器（`run_paper_recommendation_job`）或直接 CLI 腳本（`scripts/run_mlb_tsl_paper_recommendation.py`）為任意日期產生 paper-only 推薦 row，並寫入 `outputs/recommendations/PAPER/<date>/`。

**102 個測試全部通過**（新增 11 個 P141 測試）。`service.py` 未修改，所有 paper-only 安全閘均保持啟用。

---

## Phase 0 驗證

| 項目 | 狀態 |
|---|---|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| Branch | `main` ✅ |
| HEAD | `590a4d16e43f55f48c98b8aa40403f41da8794cd` ✅ |
| local HEAD = origin/main | ✅ |
| 工作樹（source code） | 乾淨（runtime 噪音 9 個 data 檔案，非 source code） |
| Staged files | 0 ✅ |
| PR #4 | MERGED ✅ |
| PR #5 | MERGED ✅ |

**工作樹注意**：發現 9 個 modified runtime/data 檔案（TSL 快取、odds 快照、logs、training memory），由後台 daemon 修改。無一在 P141 白名單內，無 staged。已知問題（.gitignore 缺 runtime/ 路徑）。

---

## 實作內容

### 1. `orchestrator/mlb_daily_scheduler.py` — 新增函數

新增 `run_paper_recommendation_job()` 函數：

```python
run_paper_recommendation_job(
    run_date="2026-06-03",
    allow_replay=True,              # 休賽期/無賽事時用 replay fixture
    allow_missing_simulation_gate=True,  # 無 simulation 結果時跳過 gate
    output_base_dir=None,           # 預設使用 repo root
) -> DailyJobResult
```

功能：
- 呼叫 `scripts.run_mlb_tsl_paper_recommendation.build_recommendation()`
- 寫出 paper row 到 `outputs/recommendations/PAPER/<date>/`
- 回傳 `DailyJobResult` 含 paper 安全 flags
- 支援 replay fallback（無 live 賽事時）
- 支援 simulation gate bypass

安全 flags（永久強制）：
```json
{
  "paper_only": true,
  "no_real_bet": true,
  "production_modified": false,
  "no_auto_execution": true,
  "scheduler_dry_run_only": true,
  "no_ev_clv_kelly_unlock": true
}
```

### 2. `tests/test_run_mlb_tsl_paper_recommendation_smoke.py` — 新增測試類別

新增 `TestP141DailyOutputChain`（7 個測試）：

| 測試 | 驗證內容 |
|---|---|
| `test_today_date_produces_row_paper_only` | 2026-06-03 產生 paper_only=True row |
| `test_row_gate_status_is_valid` | gate_status 在 VALID_GATE_STATUSES 內 |
| `test_kelly_and_stake_zero_when_tsl_blocked` | TSL 403 時 kelly=0, stake=0 |
| `test_service_py_not_required_by_paper_chain` | **service.py 不被 paper 鏈匯入** |
| `test_output_path_under_paper_dir` | 輸出路徑在 PAPER/<date>/ 下 |
| `test_allow_missing_simulation_gate_produces_row` | bypass gate 仍產生 paper_only=True |
| `test_main_cli_allow_missing_simulation_produces_exit_0` | CLI 以 bypass flags 回傳 exit 0 |

### 3. `tests/test_mlb_daily_scheduler.py` — 新增測試 + import

新增 `run_paper_recommendation_job` 到 import 並新增 tests 24-27：

| 測試 | 驗證內容 |
|---|---|
| `test_24` | 回傳 `DailyJobResult` 正確 schema |
| `test_25` | 安全 flags 所有值正確 |
| `test_26` | 成功時輸出路徑在 PAPER/<date>/ |
| `test_27` | allow_replay=True 時用 synthetic fixture，成功回傳 |

---

## Paper-Only 安全閘確認

| 閘名 | 狀態 |
|---|---|
| `_MLB_PAPER_ONLY = True` | ✅ 永久啟用 |
| `MLBLeagueAdapter.deployment_mode = "paper"` | ✅ 未修改 |
| `stake_units_paper = 0` (TSL 403) | ✅ 測試驗證 |
| `kelly_fraction = 0` (TSL 403) | ✅ 測試驗證 |
| `paper_only = True` 在所有 row | ✅ 測試驗證 |
| `wbc_backend.pipeline.service` 不被 paper 鏈匯入 | ✅ 測試驗證 |

---

## 測試結果

| 套件 | 結果 | 測試數 | 新增 |
|---|---|---|---|
| `test_run_mlb_tsl_paper_recommendation_smoke.py` | **PASS** | 13 | +7 (P141) |
| `test_run_mlb_tsl_paper_recommendation_simulation_gate.py` | **PASS** | 21 | 0 |
| `test_mlb_advisory_api.py` | **PASS** | 41 | 0 |
| `test_mlb_daily_scheduler.py` | **PASS** | 27 | +4 (P141) |
| **合計** | **PASS** | **102** | **+11** |

---

## 現有 Paper Row 示例

```
outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl
```

```json
{
  "game_id": "2026-05-11-LAA-CLE-824441",
  "paper_only": true,
  "gate_status": "BLOCKED_SIMULATION_GATE",
  "kelly_fraction": 0.0,
  "stake_units_paper": 0.0,
  "model_ensemble_version": "v1-mlb-moneyline-trained"
}
```

---

## 剩餘阻擋

| ID | 阻擋項目 | 分類 | 影響 |
|---|---|---|---|
| B1 | TSL live feed 403 Forbidden | `BLOCKS_ONLY_LIVE_ODDS` | Paper row 仍寫出（stake=0） |
| B2 | Simulation gate BSS = -14.1% | `BLOCKS_PAPER_MLB_OUTPUT_WITH_STAKE` | Stake 分配阻擋；審計軌跡仍寫出 |
| B3 | 無合法授權賠率（True P0） | `BLOCKS_ONLY_PRODUCTION_RECOMMENDATION` | Paper tracking 不受影響 |

---

## 明確聲明

- ✅ `service.py` **未修改**
- ✅ 無 DB writes
- ✅ 無 live API 呼叫（pytest monkeypatches 全在 test 層）
- ✅ 無 provider unlock
- ✅ 無 production betting unlock
- ✅ 無 EV/CLV/Kelly unlock
- ✅ 無 commit（unstaged）
- ✅ 無 push

---

## 修改檔案清單（P141 白名單內）

```
orchestrator/mlb_daily_scheduler.py           (新增 run_paper_recommendation_job)
tests/test_run_mlb_tsl_paper_recommendation_smoke.py  (新增 TestP141DailyOutputChain)
tests/test_mlb_daily_scheduler.py             (新增 import + tests 24-27)
data/mlb_2026/derived/p141_mlb_paper_recommendation_daily_output_chain_summary.json  (新建)
report/p141_mlb_paper_recommendation_daily_output_chain_20260603.md  (新建)
```

**未修改白名單檔案**（不需要修改）：
```
scripts/run_mlb_tsl_paper_recommendation.py  (已完整，未修改)
```
