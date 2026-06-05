# P145 Daily Paper CLI Enablement — Implementation Report

- **Task**: P145 Daily Paper CLI Enablement Implementation v2
- **Date**: 2026-06-05
- **Repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- **Branch**: `main`
- **Base HEAD**: `24d2c038a6f8dd86a30f2ddb6bca7538df0301e5`（local == origin/main）
- **Policy artifact**: `report/p145_daily_paper_job_enablement_policy.md`（依 v2 prompt 明確納入允許範圍）

## 1. What Was Changed

### `scripts/run_mlb_daily_scheduler.py`
1. 新增 CLI 參數 `--run-paper-recommendation`（default `"false"`）。
2. 新增 CLI 參數 `--run-paper-evaluation`（default `"false"`）。
3. 兩者皆透過既有 `_bool_arg` helper 解析為 boolean。
4. 解析結果以 keyword 參數傳入既有 `run_daily_mlb_scheduler(..., run_paper_recommendation=..., run_paper_evaluation=...)` 呼叫。
5. 啟動 echo 區塊新增兩行旗標狀態輸出，便於 daemon log 稽核。
6. Docstring 補充 daemon opt-in 用法範例。
7. **核心 scheduler defaults 未變動**：`orchestrator/mlb_daily_scheduler.py` 的 `run_paper_recommendation: bool = False` / `run_paper_evaluation: bool = False` 完全未修改。

### `tests/test_mlb_daily_scheduler.py`
新增 P145 CLI 接線測試（tests 42–45），沿用既有 monkeypatch 風格、無新測試框架依賴：

| Test | 驗證內容 |
|---|---|
| `test_42_cli_paper_flags_default_off` | 未帶旗標時，CLI 傳入 orchestrator 的兩個值皆為 `False`（default-off invariant） |
| `test_43_cli_paper_flags_explicit_opt_in` | 明確 `true` 時，兩個值皆以 `True` 傳入 scheduler invocation |
| `test_44_cli_paper_flags_are_independent` | 兩旗標獨立；單獨開啟其一不影響另一個；明確 `false` 解析為 `False` |
| `test_45_cli_default_invocation_never_calls_live_paper_job` | 真實 CLI 預設呼叫（mock 之外的完整 pipeline、`--no-write`）絕不觸及 live-probe `run_paper_recommendation_job` |

## 2. Default-OFF Invariant
- CLI 層：`--run-paper-recommendation` / `--run-paper-evaluation` 預設字串 `"false"` → 解析為 `False`。
- Python 函數層：`run_daily_mlb_scheduler` 預設 `False`（P144 既有，未變動）。
- 雙層 default-off 保證：任何未明確帶旗標的 CLI 呼叫者與所有離線測試，均不會觸發 live 網路抓取（`_pick_game` / `_probe_tsl`）。

## 3. Explicit Opt-In Mechanism
Daemon 啟動腳本需明確傳遞：

```bash
.venv/bin/python scripts/run_mlb_daily_scheduler.py \
    --date <YYYY-MM-DD> --mode today --source fixture --limit 15 \
    --run-paper-recommendation true --run-paper-evaluation true
```

Rollback：自 daemon invoker 移除旗標即立刻回到 pre-P145 offline/dry-run 狀態（無需改 code）。

## 4. Tests Run

| Suite | Result |
|---|---|
| `pytest tests/test_mlb_daily_scheduler.py -q` | **45 passed**（含新增 4 個 P145 測試） |
| `pytest tests/test_mlb_paper_evaluation_runner.py -q` | **21 passed** |
| CLI `--help` smoke test | 兩個新參數正確顯示 |

## 5. Safety Invariants（Explicit Non-Actions）
- ❌ 無 DB write（僅既有 paper-only 檔案輸出路徑，且測試全程 `--no-write` / tmp_path）。
- ❌ 無 live API call（live-probe 路徑在所有測試中均被 mock 或預設關閉）。
- ❌ 無 provider unlock。
- ❌ 無 production betting unlock。
- ❌ 無 EV/CLV/Kelly unlock。
- ❌ 無 registry mutation、無 controlled_apply、無 daemon 啟動。
- ❌ 未觸碰 tolerated daemon/runtime dirty files。
- ❌ 未建立 branch、未 commit、未 push（active_task.md 未明確授權 commit → 保持 uncommitted）。

## 6. Remaining Next Step（本任務未涵蓋）
Daemon 啟動腳本（cron / GitHub Action / 本地排程器）尚未更新為帶上
`--run-paper-recommendation true --run-paper-evaluation true`。
該檔案不在本任務 Allowed File Whitelist 內，需由下一個明確授權的任務
（建議 P146: daemon invoker flag enablement）執行，以開始累積 paper corpus
（目前僅 2 rows，Blocker B5）。

## 7. Final Classification
`P145_DAILY_PAPER_CLI_ENABLEMENT_READY_UNCOMMITTED`
