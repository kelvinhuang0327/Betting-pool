# P22 Historical Backfill Data Availability — Phase Report

**日期**: 2026-05-12  
**分支**: `p13-clean`  
**先行 commit**: `93e46de` — feat(p21): Multi-Day PAPER Backfill Orchestrator  
**安全模式**: `PAPER_ONLY=true`, `PRODUCTION_READY=false`

---

## 1. Repo 狀態證據

```
$ git log --oneline -3
93e46de (HEAD -> p13-clean) feat(p21): Multi-Day PAPER Backfill Orchestrator — aggregates P20 daily runs across date range
c397d14 feat(p20): Daily PAPER MLB Orchestrator — chains P16.6→P19→P17 replay into daily summary
003de53 feat(p19): 完成 odds identity join repair 管線，修復 P17 結算缺口
```

Branch `p13-clean`，無 dirty 狀態。所有 P22 模組均在此 branch 新建，不修改任何既有檔案。

---

## 2. 先行階段證據 — P21

P21 Multi-Day PAPER Backfill Orchestrator (`93e46de`) 已完成：
- Contract: `wbc_backend/recommendation/p21_multi_day_backfill_contract.py`
- Artifact Discovery: `wbc_backend/recommendation/p21_daily_artifact_discovery.py`
- Aggregator: `wbc_backend/recommendation/p21_multi_day_backfill_aggregator.py`
- CLI: `scripts/run_p21_multi_day_paper_backfill.py`
- Tests: 4 files, 109 tests

P21 掃描輸出存在於 `outputs/predictions/PAPER/backfill/p21_*/`，包含 2026-05-12 單日回測結果。

---

## 3. 為什麼 P22 現在可以執行

P21 已可對已知日期執行多日彙整。但在執行之前，需要先知道：
- 哪些歷史日期在 PAPER 目錄有完整 P20 產出
- 哪些日期有可重播的 P15/P16.6/P19 來源
- 哪些日期缺少任何來源 artifact
- 哪些日期存在損壞的 P20 gate

P22 是 **純探索** (discovery-only) 階段：掃描、分類、生成執行計畫，但不執行任何 P21 或 P20 指令。

---

## 4. Historical Availability Contract

**檔案**: `wbc_backend/recommendation/p22_historical_availability_contract.py`

### Gate 常數 (5)

| 常數 | 意義 |
|------|------|
| `P22_HISTORICAL_BACKFILL_AVAILABILITY_READY` | 至少 1 個候選日期 |
| `P22_BLOCKED_NO_AVAILABLE_DATES` | 無任何候選日期 |
| `P22_BLOCKED_CONTRACT_VIOLATION` | 合約違反 |
| `P22_FAIL_INPUT_MISSING` | 輸入參數缺失 |
| `P22_FAIL_NON_DETERMINISTIC` | 非確定性輸出 |

### Date Status 常數 (7)

| 常數 | 意義 |
|------|------|
| `DATE_READY_P20_EXISTS` | P20 完整且 gate 正確 |
| `DATE_READY_REPLAYABLE_FROM_P15_P16_P19` | P15+P16.6+P19 齊全，可重播 |
| `DATE_PARTIAL_SOURCE_AVAILABLE` | 部分 artifact 存在 |
| `DATE_MISSING_REQUIRED_SOURCE` | 無任何 artifact |
| `DATE_BLOCKED_INVALID_ARTIFACTS` | P20 gate 不符 |
| `DATE_BLOCKED_UNSAFE_IDENTITY` | P19 gate 含 FAIL/BLOCKED |
| `DATE_UNKNOWN` | 未知狀態 |

### Frozen Dataclasses (5)

所有 dataclass 均使用 `@dataclass(frozen=True)` + `__post_init__` 安全守衛：
- `P22PhaseArtifactStatus`: 單一 artifact 的掃描狀態
- `P22DateAvailabilityResult`: 單一日期的可用性結果
- `P22HistoricalAvailabilitySummary`: 整個日期範圍的彙整摘要
- `P22BackfillExecutionPlan`: 可執行的回補計畫
- `P22GateResult`: 最終 P22 gate 結果

全部強制 `paper_only=True`, `production_ready=False`，建構時違反則拋出 `ValueError`。

---

## 5. Artifact Scanner 設計

**檔案**: `wbc_backend/recommendation/p22_historical_artifact_scanner.py`

### 掃描的 10 個 Artifact (ARTIFACT_SPEC)

| Key | 子目錄 | 檔名 |
|-----|--------|------|
| P15_JOINED_OOF_WITH_ODDS | p15_market_odds_simulation | joined_oof_with_odds.csv |
| P15_SIMULATION_LEDGER | p15_market_odds_simulation | simulation_ledger.csv |
| P16_6_RECOMMENDATION_ROWS | p16_6_recommendation_gate_p18_policy | recommendation_rows.csv |
| P16_6_RECOMMENDATION_SUMMARY | p16_6_recommendation_gate_p18_policy | recommendation_summary.json |
| P19_ENRICHED_LEDGER | p19_odds_identity_join_repair | enriched_simulation_ledger.csv |
| P19_GATE_RESULT | p19_odds_identity_join_repair | p19_gate_result.json |
| P17_REPLAY_LEDGER | p17_replay_with_p19_identity | paper_recommendation_ledger.csv |
| P17_REPLAY_SUMMARY | p17_replay_with_p19_identity | paper_recommendation_ledger_summary.json |
| P20_DAILY_SUMMARY | p20_daily_paper_orchestrator | daily_paper_summary.json |
| P20_GATE_RESULT | p20_daily_paper_orchestrator | p20_gate_result.json |

### 分類優先順序 (classify_date_availability)

1. P20 files + gate == `P20_DAILY_PAPER_ORCHESTRATOR_READY` → `DATE_READY_P20_EXISTS`
2. P20 files + gate 不符 → `DATE_BLOCKED_INVALID_ARTIFACTS`
3. P19 gate 含 FAIL/BLOCKED → `DATE_BLOCKED_UNSAFE_IDENTITY`
4. 全部 replay required keys 存在且可讀 → `DATE_READY_REPLAYABLE_FROM_P15_P16_P19`
5. 部分 artifact 存在 → `DATE_PARTIAL_SOURCE_AVAILABLE`
6. 無任何 artifact → `DATE_MISSING_REQUIRED_SOURCE`

### 核心函數

- `inspect_phase_artifacts(date_dir)` — 永遠回傳 10 個 `P22PhaseArtifactStatus`
- `scan_single_paper_date(base_dir, run_date)` — 不捏造；缺少目錄時 `phase_statuses=()`
- `scan_paper_date_range(base_dir, date_start, date_end)` — 回傳精確的 N 個結果
- `summarize_scan_results(date_results, date_start, date_end)` — 有候選→READY，無→BLOCKED

---

## 6. Backfill Execution Plan 設計

**檔案**: `wbc_backend/recommendation/p22_backfill_execution_plan.py`

### build_daily_command_for_date 輸出

| 狀態 | 輸出 |
|------|------|
| `DATE_READY_P20_EXISTS` | `# SKIP — 2026-05-12 already P20-ready` |
| `DATE_READY_REPLAYABLE` | 3 個指令 (run_p19, run_p17, run_p20) |
| `DATE_PARTIAL` | `# PARTIAL — build missing artifacts first` |
| `DATE_MISSING` | `# BLOCKED/MISSING — no source artifacts` |
| `DATE_BLOCKED` | `# BLOCKED — invalid or unsafe artifacts` |

### build_p21_command_for_range

當存在可重播日期時，附加 P21 聚合指令，格式：
```
python scripts/run_p21_multi_day_paper_backfill.py --date-start ... --date-end ...
```

### validate_execution_plan

- 拒絕 `production_ready=True`
- 拒絕 `paper_only=False`
- 偵測同一日期同時在 `dates_to_skip_already_ready` 和 `dates_to_replay_from_existing_sources`

### risk_notes (固定 4 條)

所有計畫均內嵌安全備注，包含 `PAPER_ONLY` 聲明。

---

## 7. May 1–May 12 掃描結果

```
$ PYTHONPATH=. .venv/bin/python scripts/run_p22_historical_backfill_availability.py \
    --date-start 2026-05-01 --date-end 2026-05-12 \
    --paper-base-dir outputs/predictions/PAPER \
    --output-dir outputs/predictions/PAPER/backfill/p22_historical_availability_2026-05-01_2026-05-12 \
    --paper-only true
```

### 結果

```
[P22] SUCCESS: P22_HISTORICAL_BACKFILL_AVAILABILITY_READY
  date_start:                2026-05-01
  date_end:                  2026-05-12
  n_dates_scanned:           12
  n_dates_p20_ready:         1
  n_dates_replayable:        0
  n_dates_partial:           0
  n_dates_missing:           11
  n_dates_blocked:           0
  n_backfill_candidate_dates:1
  recommended_next_action:   1 date(s) already P20-ready. 11 date(s) lack source
                             artifacts — consider historical source artifact
                             expansion (P22.5 or TSL).
  production_ready:          False
  paper_only:                True
```

### Gate Result (`p22_gate_result.json`)

```json
{
  "p22_gate": "P22_HISTORICAL_BACKFILL_AVAILABILITY_READY",
  "date_start": "2026-05-01",
  "date_end": "2026-05-12",
  "n_dates_scanned": 12,
  "n_dates_p20_ready": 1,
  "n_dates_replayable": 0,
  "n_dates_partial": 0,
  "n_dates_missing": 11,
  "n_dates_blocked": 0,
  "n_backfill_candidate_dates": 1,
  "paper_only": true,
  "production_ready": false
}
```

**產出目錄**: `outputs/predictions/PAPER/backfill/p22_historical_availability_2026-05-01_2026-05-12/`

---

## 8. 精確 P20 日期掃描結果 (2026-05-12 單日)

```
$ PYTHONPATH=. .venv/bin/python scripts/run_p22_historical_backfill_availability.py \
    --date-start 2026-05-12 --date-end 2026-05-12 \
    --paper-base-dir outputs/predictions/PAPER \
    --output-dir outputs/predictions/PAPER/backfill/p22_historical_availability_2026-05-12_2026-05-12 \
    --paper-only true
```

```
[P22] SUCCESS: P22_HISTORICAL_BACKFILL_AVAILABILITY_READY
  n_dates_scanned:           1
  n_dates_p20_ready:         1
  n_dates_missing:           0
  recommended_next_action:   All 1 date(s) are P20-ready. Run P21 aggregate backfill.
```

確認：2026-05-12 是唯一一個 P20-ready 日期，且 P20 gate `P20_DAILY_PAPER_ORCHESTRATOR_READY` 正確。

---

## 9. 缺失 / 部分 Artifact 分析

| 日期 | 狀態 | 說明 |
|------|------|------|
| 2026-05-01 ~ 2026-05-11 | `DATE_MISSING_REQUIRED_SOURCE` | 無任何 P15/P16.6/P19/P20 artifact |
| 2026-05-12 | `DATE_READY_P20_EXISTS` | 完整 P20 + 正確 gate |

**根本原因**: 本系統自 2026-05-12 才開始生產 PAPER 模式產出。歷史日期 (05-01 ~ 05-11) 從未執行過 P15→P20 管線，因此無任何 artifact。

**結論**: 這 11 個缺失日期**無法**透過 P22 回補，因為 P22 回補的前提是「來源 artifact 存在」。若要補足這 11 天的歷史資料，需要 P22.5 (歷史 TSL 賠率重播) 或手動補齊 P15 simulation artifact。

---

## 10. 測試結果

### P22 測試 (4 個檔案)

```
tests/test_p22_historical_availability_contract.py   — 22 tests
tests/test_p22_historical_artifact_scanner.py        — 22 tests
tests/test_p22_backfill_execution_plan.py            — 19 tests
tests/test_run_p22_historical_backfill_availability.py — 8 tests
Total: 63 passed in 0.67s
```

### P17–P21 回歸測試

```
P20/P21: 109 passed in 4.75s
P17/P19: 112 passed in 9.39s
```

**全部 284 tests passed，0 failures，0 errors。**

---

## 11. 確定性 (Determinism) 結果

兩次獨立執行相同輸入 (2026-05-01 ~ 2026-05-12)，排除 `generated_at` 後比較：

```
p22_gate_result.json:                IDENTICAL
historical_availability_summary.json:IDENTICAL
backfill_execution_plan.json:        IDENTICAL
date_availability_results.csv:       IDENTICAL
```

P22 scanner 和 plan generator 均為純函數輸出，完全確定性。

---

## 12. 生產就緒聲明

- `paper_only = True` — 強制於 contract、scanner、plan、CLI 四個層次
- `production_ready = False` — 同上，任何嘗試設定為 True 的建構均拋出 `ValueError`
- 所有 dataclass 為 `frozen=True` — 不可在建構後修改
- CLI 硬守衛: `--paper-only false` → 立即 exit 2，無任何輸出
- 無任何 DB 寫入、無 TSL 即時呼叫、無生產下注

**P22 是純粹的 artifact 掃描 + 計畫生成階段，不執行任何下注或生產操作。**

---

## 13. 已知限制

1. **歷史空白**: 2026-05-01 ~ 2026-05-11 共 11 天無任何 PAPER artifact，P22 無法回補這些日期。
2. **P22 不執行**: 計畫只列出指令，需手動或 P23 執行。
3. **單一既有日期**: 整個 WBC 2026 PAPER 歷史中只有 2026-05-12 有完整 P20 紀錄。
4. **Replayable 路徑未被觸發**: 因為沒有任何日期有 P15/P16.6/P19 但沒有 P20，replayable 計數 = 0。
5. **TSL 歷史覆蓋度**: 目前 `data/tsl_odds_history.jsonl` 是否涵蓋 05-01 ~ 05-11 未經驗證。

---

## 14. 下一階段建議

### 優先推薦: P22.5 — Historical TSL Artifact Expansion

由於 11 個缺失日期的根本原因是「從未執行過 P15 simulation」，建議的解決路徑：

1. **驗證 TSL 歷史賠率覆蓋度**: 確認 `data/tsl_odds_history.jsonl` 是否有 05-01 ~ 05-11 的賠率快照。
2. **若有**: 建立 P22.5，從歷史 TSL 快照生成 P15 simulation artifact，再啟動 P16.6→P19→P17→P20 管線。
3. **若無**: 需要先執行 TSL 歷史資料回補 (P22.5 前置)，或接受只有 2026-05-12 的歷史資料。

### 備選: 擴展 PAPER 覆蓋日期

從今日起，每日執行 P20 Daily Paper Orchestrator，逐步積累歷史日期。

---

## 15. 終端標記

```
P22_HISTORICAL_BACKFILL_AVAILABILITY_READY
```
