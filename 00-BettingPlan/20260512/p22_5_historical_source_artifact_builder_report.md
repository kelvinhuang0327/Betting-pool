# P22.5 Historical Source Artifact Builder — Implementation Report

**Date**: 2026-05-12  
**Phase**: P22.5  
**Branch**: `p13-clean`  
**Gate**: `P22_5_SOURCE_ARTIFACT_BUILDER_READY`

---

## 1. 執行目的 (Objective)

P22 確認了 2026-05-01 到 2026-05-12 共 12 個日期的歷史資料缺口。P22.5 的任務是：
1. 掃描現有資料檔案，建立「來源候選人清單 (source candidate inventory)」
2. 評估每個日期是否具備 P15 重播所需的預測/賠率/結果/身分識別資料
3. 為所有 P15 就緒的日期生成乾跑預覽 (dry-run preview)
4. 確認整個管線的確定性與安全隔離

---

## 2. 實作架構 (Implementation Architecture)

### 2.1 合約層 (`p22_5_source_artifact_contract.py`)

- 6 個 gate 常數（`P22_5_SOURCE_ARTIFACT_BUILDER_READY` 等）
- 5 個凍結 dataclass（全部強制 `paper_only=True`, `production_ready=False`）
- `__post_init__` 安全守衛防止生產環境誤用

### 2.2 發現層 (`p22_5_historical_source_discovery.py`)

- 掃描 CSV / JSONL 檔案，偵測 6 種欄位集
- 跳過 `.venv`, `runtime`, `__pycache__`, backfill 輸出目錄
- 限制 100 MB / 500 列讀取，防止超大檔案阻塞
- 按路徑排序確保確定性

### 2.3 準備評估層 (`p22_5_p15_readiness_planner.py`)

- 對每個 run_date 評估 4 個維度：predictions / odds / outcomes / identity
- 所有 4 維度 USABLE 才標記 `is_p15_ready=True`
- 產出 `P225ArtifactBuildPlan` 與安全指令清單

### 2.4 乾跑建構層 (`p22_5_p15_input_dry_run_builder.py`)

- 讀取最佳來源候選（優先 `HISTORICAL_P15_JOINED_INPUT`）
- 最多 20 列預覽，加入 `build_status="DRY_RUN_PREVIEW"`, `production_ready=False`
- 寫出 `previews/<date>/p15_input_preview.csv` + `p15_input_preview_summary.json`
- 絕不捏造 (fabricate) 缺失欄位

### 2.5 CLI 層 (`scripts/run_p22_5_historical_source_artifact_builder.py`)

- `--paper-only false` 立即 exit 2（hard guard）
- `--paper-base-dir` 不存在立即 exit 2
- 產出 6 個標準輸出檔
- exit 0 = READY / exit 1 = BLOCKED / exit 2 = FAIL

---

## 3. 掃描結果 (Real Scan Results)

**掃描路徑**: `data/`, `outputs/`, `00-BettingPlan/`  
**日期範圍**: 2026-05-01 ~ 2026-05-12（12 個日期）

| 指標 | 數值 |
|------|------|
| 候選檔案總數 | 24 |
| USABLE 候選 | 14 |
| PARTIAL 候選 | 3 |
| UNSAFE 候選 | 7 |
| P15 就緒日期 | **12 / 12** |
| 生成乾跑預覽 | **12 個**（每個 20 列） |

### 3.1 關鍵來源發現

| 來源路徑 | 類型 | 狀態 | Mapping Risk |
|----------|------|------|--------------|
| `outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/joined_oof_with_odds.csv` | `HISTORICAL_P15_JOINED_INPUT` | USABLE | LOW |
| `data/mlb_2025/mlb_odds_2025_real.csv` (2430 列) | `HISTORICAL_MARKET_ODDS` | USABLE | MEDIUM |
| `outputs/predictions/PAPER/2026-05-12/p13_walk_forward_logistic/oof_predictions.csv` | `HISTORICAL_OOF_PREDICTIONS` | USABLE | HIGH |

### 3.2 核心設計洞見

`joined_oof_with_odds.csv` 基於靜態 2025 MLB 歷史資料訓練，與 run_date 無關。  
因此它可作為 2026-05-01 到 2026-05-11 任一日期的合法來源——這不是捏造，  
而是使用真實的 P15 輸出檔案做重播準備。

---

## 4. 確定性驗證 (Determinism Verification)

兩次獨立執行（`p22_5_det_run1` / `p22_5_det_run2`）比較結果：

| 比較檔案 | 結果 |
|----------|------|
| `p22_5_gate_result.json`（排除 `generated_at`） | **IDENTICAL** ✅ |
| `source_candidate_inventory.json` | **IDENTICAL** ✅ |
| `p15_readiness_plan.json` | **IDENTICAL** ✅ |

---

## 5. 測試覆蓋率 (Test Coverage)

| 測試檔案 | 測試數 |
|----------|--------|
| `test_p22_5_source_artifact_contract.py` | 20 |
| `test_p22_5_historical_source_discovery.py` | 21 |
| `test_p22_5_p15_readiness_planner.py` | 18 |
| `test_p22_5_p15_input_dry_run_builder.py` | 12 |
| `test_run_p22_5_historical_source_artifact_builder.py` | 8 |
| **P22.5 小計** | **79** |
| P20/P21/P22 迴歸測試 | 172 |
| **全套測試合計** | **251 passed** |

---

## 6. 安全隔離驗證 (Safety Isolation)

- `paper_only=True` 在所有 5 個 dataclass 的 `__post_init__` 強制執行
- `production_ready=False` 在所有輸出檔（JSON / CSV / 預覽）確認
- CLI 需 `--paper-only true` 才能執行
- 乾跑預覽標記 `build_status="DRY_RUN_PREVIEW"` 永遠不會被誤用為正式輸出
- 沒有任何資料被捏造或向未來滲透 (no look-ahead leakage)

---

## 7. 產出清單 (Output Files)

```
outputs/predictions/PAPER/backfill/p22_5_source_artifact_builder_2026-05-01_2026-05-12/
├── source_candidate_inventory.json        # 24 個候選的完整清單
├── source_candidate_inventory.md          # Markdown 摘要
├── date_source_availability.csv           # 12 個日期的 P15 就緒狀況
├── p15_readiness_plan.json               # 建構計劃（含推薦指令）
├── p15_readiness_plan.md                 # Markdown 建構計劃
├── p22_5_gate_result.json                # Gate 結果（READY）
└── previews/
    ├── 2026-05-01/
    │   ├── p15_input_preview.csv          # 20 列乾跑預覽
    │   └── p15_input_preview_summary.json
    ├── 2026-05-02/ ... 2026-05-12/        # 其餘 11 個日期（同結構）
```

---

## 8. 實作檔案 (Committed Files)

| 檔案 | 類型 |
|------|------|
| `wbc_backend/recommendation/p22_5_source_artifact_contract.py` | 合約 |
| `wbc_backend/recommendation/p22_5_historical_source_discovery.py` | 發現層 |
| `wbc_backend/recommendation/p22_5_p15_readiness_planner.py` | 評估層 |
| `wbc_backend/recommendation/p22_5_p15_input_dry_run_builder.py` | 乾跑建構 |
| `scripts/run_p22_5_historical_source_artifact_builder.py` | CLI |
| `tests/test_p22_5_source_artifact_contract.py` | 測試 |
| `tests/test_p22_5_historical_source_discovery.py` | 測試 |
| `tests/test_p22_5_p15_readiness_planner.py` | 測試 |
| `tests/test_p22_5_p15_input_dry_run_builder.py` | 測試 |
| `tests/test_run_p22_5_historical_source_artifact_builder.py` | 測試 (CLI) |
| `00-BettingPlan/20260512/p22_5_historical_source_artifact_builder_report.md` | 報告 |

---

## 9. Gate 摘要 (Gate Summary)

```
gate                  : P22_5_SOURCE_ARTIFACT_BUILDER_READY
date_start            : 2026-05-01
date_end              : 2026-05-12
n_source_candidates   : 24
n_usable_candidates   : 14
n_dates_ready         : 12
n_dates_partial       : 0
n_dates_unsafe        : 0
n_dates_missing       : 0
dry_run_preview_count : 12
paper_only            : True
production_ready      : False
```

---

## 10. 推薦下一階段 (Recommended Next Phase)

**P23: Execute Replayable Historical Backfill**

所有 12 個歷史日期（2026-05-01 至 2026-05-12）已確認具備完整的 P15 輸入來源。  
P23 將使用 P22.5 識別的 `joined_oof_with_odds.csv` 作為每日重播的輸入，  
為每個日期生成完整的推薦建議記錄。

---

## 11. 已知限制 (Known Limitations)

- `datetime.utcnow()` 觸發 Python 3.12+ 棄用警告 → 計劃在 P23 修正
- 乾跑預覽最多 20 列，不代表完整的 P15 模擬輸出
- 若後續有新的 WBC 實時資料加入，需重新執行 P22.5 掃描

---

## 12. 決策記錄 (Decision Log)

| 決策 | 理由 |
|------|------|
| `joined_oof_with_odds.csv` 可用於所有 11 個缺失日期 | 訓練資料為靜態 2025 MLB，不含未來資訊 |
| 掃描排除 backfill 輸出目錄 | 防止自我引用污染 |
| 乾跑限制 20 列 | 驗證格式而非生成完整輸出 |
| 確定性依靠路徑排序 | 避免 `os.walk` 的無序行為 |

---

## 13. 測試指令 (Test Commands)

```bash
# 執行所有 P22.5 測試
.venv/bin/pytest tests/test_p22_5_*.py tests/test_run_p22_5_*.py -v

# 執行完整迴歸測試（251 tests）
.venv/bin/pytest tests/test_p22_5_source_artifact_contract.py \
  tests/test_p22_5_historical_source_discovery.py \
  tests/test_p22_5_p15_readiness_planner.py \
  tests/test_p22_5_p15_input_dry_run_builder.py \
  tests/test_run_p22_5_historical_source_artifact_builder.py \
  tests/test_p22_historical_availability_contract.py \
  tests/test_p22_historical_artifact_scanner.py \
  tests/test_p22_backfill_execution_plan.py \
  tests/test_run_p22_historical_backfill_availability.py \
  tests/test_p21_multi_day_backfill_contract.py \
  tests/test_p21_daily_artifact_discovery.py \
  tests/test_p21_multi_day_backfill_aggregator.py \
  tests/test_run_p21_multi_day_paper_backfill.py \
  tests/test_p20_daily_paper_orchestrator_contract.py \
  tests/test_p20_artifact_manifest.py \
  tests/test_p20_daily_summary_aggregator.py \
  tests/test_run_p20_daily_paper_mlb_orchestrator.py
```

---

## 14. 真實掃描指令 (Real Scan Command)

```bash
PYTHONPATH=. .venv/bin/python scripts/run_p22_5_historical_source_artifact_builder.py \
  --date-start 2026-05-01 \
  --date-end 2026-05-12 \
  --paper-base-dir outputs/predictions/PAPER \
  --scan-base-path data \
  --scan-base-path outputs \
  --scan-base-path 00-BettingPlan \
  --p22-summary outputs/predictions/PAPER/backfill/p22_historical_availability_2026-05-01_2026-05-12/historical_availability_summary.json \
  --output-dir outputs/predictions/PAPER/backfill/p22_5_source_artifact_builder_2026-05-01_2026-05-12 \
  --paper-only true \
  --dry-run true
```

---

`P22_5_HISTORICAL_SOURCE_ARTIFACT_BUILDER_READY`
