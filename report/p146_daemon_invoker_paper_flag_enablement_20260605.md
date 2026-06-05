# P146 Daemon Invoker Paper Flag Enablement — Implementation Report

- **Task**: P146 Daemon Invoker Paper Flag Enablement
- **Date**: 2026-06-05
- **Repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- **Branch**: `main`
- **Base HEAD (before commit)**: `23e974a275542ecf9086cf7a1d359b89c39d8b31`（P145）
- **origin/main**: `24d2c038a6f8dd86a30f2ddb6bca7538df0301e5`（local ahead 2 after commit）

## 1. What Was Changed

### `.github/workflows/daily_update.yml`
新增一個 GitHub Actions step，插入於 `Install dependencies` 與 `Run Data Update` 之間：

```yaml
- name: Run MLB Daily Scheduler (Paper Mode)
  run: |
    if [ -f .venv/bin/python ]; then
      PYTHON=.venv/bin/python
    else
      PYTHON=python3
    fi
    $PYTHON scripts/run_mlb_daily_scheduler.py \
      --date "$(date -u +'%Y-%m-%d')" \
      --mode today \
      --source fixture \
      --limit 15 \
      --run-paper-recommendation true \
      --run-paper-evaluation true \
      || echo "MLB daily scheduler step failed (non-blocking)"
```

**既有 WBC step (`Run Data Update`) 完全未修改。**
**既有 `Commit and Push changes` step 完全未修改。**

## 2. 為什麼選擇 `.github/workflows/daily_update.yml`

P146 scope gate（P145 commit 後 read-only 勘察）結果：

| 候選位置 | 實際呼叫 MLB scheduler | 選擇理由 |
|---|---|---|
| `.github/workflows/daily_update.yml` | 否（僅 WBC 舊腳本） | **唯一**存在的自動化 cron 入口（UTC 00:00 每日） |
| `start_all.sh` | 否（backend/frontend/proxy） | 非排程，為服務啟動腳本 |
| `scripts/launchd/plists/*.plist.tmpl` | 否（指向 start_all.sh） | 無 MLB scheduler 呼叫 |
| `crontab` | 空 | 無任何 cron 項目 |
| `scripts/agent_orchestrator.py` | 否 | 無 MLB scheduler 呼叫 |

GitHub Actions 提供透明執行日誌、版控追蹤，且此 workflow 已有 cron 觸發機制，是最低侵入性的 paper corpus 累積入口。

## 3. Non-Fatal 設計理由

```bash
|| echo "MLB daily scheduler step failed (non-blocking)"
```

- `--source fixture`：使用離線 fixture 資料，不依賴 live MLB API。
- TSL probe（`_probe_tsl`）在 CI 環境預計回傳 403，`run_paper_recommendation_job` 會以 `DATA_LIMITED` 結束而非拋出例外（P141 設計保證）。
- 即使 paper step 完全失敗，`|| echo` 確保 exit code 為 0，不阻斷 `Run Data Update`（WBC 腳本）及後續 `Commit and Push`。
- 這意味著現有 WBC 自動化的 SLA 零影響。

## 4. 步驟執行順序

```
1. Checkout Repository
2. Set up Python 3.10
3. Install dependencies
4. [NEW] Run MLB Daily Scheduler (Paper Mode)  ← P146 新增，non-fatal
5. Run Data Update                              ← 未修改
6. Commit and Push changes                      ← 未修改
```

## 5. Safety Invariants（Explicit Non-Actions）
- ❌ 無 DB write（paper-only artifacts 寫入 `outputs/` 或 `data/` 子目錄，stake=0）。
- ❌ 無 production betting unlock（paper_only 語義由 P141 設計保證）。
- ❌ 無 EV/CLV/Kelly unlock（run_paper_recommendation_job 內部 stake=0）。
- ❌ 無 provider unlock（TSL probe 預期 403 失敗，graceful DATA_LIMITED）。
- ❌ 無 live API call 在本地測試中手動觸發（步驟僅在 CI 執行）。
- ❌ 未修改 service.py、.gitignore、或任何 source code 邏輯。
- ❌ 未觸碰 tolerated daemon/runtime dirty files。
- ❌ 未 push（local 保留，等待 PR 授權）。

## 6. Validation Run
- PyYAML 不可用（未安裝，不安裝套件）。
- 手動結構驗證：**15/15 PASS**（含 step 順序、旗標存在性、WBC step 完整性、無 tab 字元）。
- `grep -n` 確認兩個 paper 旗標及 `non-blocking` 均存在。

## 7. Pytest
本任務僅修改 workflow YAML，無 Python 邏輯變動，pytest 不需運行。P145 測試（45 + 21）於前輪確認通過且本次未修改任何 Python 檔案，保持有效。

## 8. 下一步建議
1. PR：將 `main [ahead 2]`（P145 + P146）推送並開 PR 合併至 origin/main。
2. 等待首次 CI 執行（UTC 00:00 或手動 `workflow_dispatch`），確認 paper step 產生 `outputs/recommendations/PAPER/<date>/` 目錄下的 artifact。
3. 若 TSL probe 如預期 403，`paper_recommendation` 會以 `DATA_LIMITED` 結束——這是正常狀態，需等待 TSL 授權後才會升級為 `SUCCESS`。
4. `paper_evaluation` 在初期因 PAPER corpus 僅 2 rows，預計以 `DATA_LIMITED` 或 `small_sample` 警告結束——正常，隨每日累積改善。

## 9. Final Classification
`P146_DAEMON_INVOKER_PAPER_FLAG_ENABLEMENT_COMMITTED`
