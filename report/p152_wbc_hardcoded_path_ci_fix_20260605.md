# P152 WBC Hardcoded Path CI Fix — Implementation Report

- **Task**: P152 Fix WBC Hardcoded Path in Daily Workflow
- **Date**: 2026-06-05
- **Repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- **Branch**: `main`
- **Base HEAD**: `06c62171c5f0ad7bf7f2fd2558623f6803d9a55d`（P145+P146 merge）

## 1. Root Cause

`scripts/legacy_entrypoints/fetch_wbc_all_players.py` line 93（修正前）：

```python
output_file = f"/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_all_players_realtime.json"
```

此為開發者本機 macOS 絕對路徑。GitHub Actions Ubuntu runner 上不存在 `/Users/kelvin/` 路徑，導致：

```
FileNotFoundError: [Errno 2] No such file or directory:
    '/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_all_players_realtime.json'
```

此 bug 自 2026-05-26 起每天觸發，使 `Run Data Update` step 失敗，
進而 skip `Commit and Push changes` step，paper artifacts 無法自動推回 repo。

## 2. What Was Changed

### `scripts/legacy_entrypoints/fetch_wbc_all_players.py`

1. 新增 `from pathlib import Path` import。
2. 在模組頂層計算 `_REPO_ROOT = Path(__file__).resolve().parents[2]`
   （`__file__` 在 `scripts/legacy_entrypoints/` 下，兩層 parent 到 repo root）。
3. 將 hardcoded 路徑替換為：
   ```python
   output_file = _REPO_ROOT / "data" / "wbc_all_players_realtime.json"
   output_file.parent.mkdir(parents=True, exist_ok=True)
   ```
4. `print(f"Finished! ... {output_file.resolve()}")` 使用 `Path.resolve()`。

**輸出行為不變**：檔案仍寫至 `<repo_root>/data/wbc_all_players_realtime.json`。

### `tests/test_fetch_wbc_all_players.py`（新建）

5 個測試覆蓋：
| Test | 驗證內容 |
|---|---|
| `test_p152_repo_root_is_not_hardcoded` | source 不含 `/Users/kelvin` 字串 |
| `test_p152_repo_root_resolves_correctly` | `_REPO_ROOT` == 實際 repo root |
| `test_p152_output_path_is_relative_to_repo_root` | 輸出路徑相對 `_REPO_ROOT` 為 `data/wbc_all_players_realtime.json` |
| `test_p152_run_writes_to_tmp_path` | `WBCCrawler.run()` 在 monkeypatched `_REPO_ROOT` 下寫入 JSON（無網路呼叫）|
| `test_p152_run_creates_parent_dir` | `data/` 目錄不存在時自動建立 |

## 3. Safety Invariants
- ❌ 無 DB write。
- ❌ 無手動 live API call（測試 stub `get_active_wbc_teams` 返回空列表；腳本本身 `stats = []` 佔位符，不執行球員 stats 抓取）。
- ❌ 無 production betting unlock、無 EV/CLV/Kelly unlock、無 provider unlock。
- ❌ 未修改 `.github/workflows/daily_update.yml`（P146 workflow 未動）。
- ❌ 未修改任何 paper job 邏輯（P145/P146 完全不受影響）。
- ✅ `py_compile` PASS。
- ✅ 5 tests PASS（0.07s）。

## 4. Why CI Was Failing Before This Fix

CI 失敗鏈（pre-P152）：
1. `Run Data Update` → `fetch_wbc_all_players.py` → `FileNotFoundError` → step 失敗
2. Workflow conclusion = `failure`
3. `Commit and Push changes` → skipped
4. Paper artifacts（P146 產生的）無法自動推回 repo

修復後（post-P152）：
1. `Run MLB Daily Scheduler (Paper Mode)`（P146）→ 執行（non-fatal）
2. `Run Data Update` → `fetch_wbc_all_players.py` → 成功寫入 `data/wbc_all_players_realtime.json`
3. `Commit and Push changes` → 正常執行（`git add data/*.json`）

## 5. Next Recommended Step

1. 開 PR：`release/p152-wbc-hardcoded-path-ci-fix` → `main`，讓 P152 修復進入主線。
2. 合併後等下一次 UTC 00:00 排程 run（或手動 workflow_dispatch），驗證：
   - `Run Data Update` step 首次 SUCCESS
   - `Run MLB Daily Scheduler (Paper Mode)` step 執行結果
   - `Commit and Push changes` step 正常提交 paper artifacts

## 6. Final Classification
`P152_WBC_HARDCODED_PATH_CI_FIX_COMMITTED`
