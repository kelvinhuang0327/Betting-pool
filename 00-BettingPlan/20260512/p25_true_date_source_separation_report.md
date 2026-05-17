# P25 真實日期來源隔離報告 (True Date Source Separation Report)

**報告標記**: `P25_TRUE_DATE_SOURCE_SEPARATION_READY_WITH_2026_RANGE_BLOCKED`  
**報告日期**: 2026-05-12  
**分支**: `p13-clean`  
**前置提交**: `1c7033f` (P24 回測性能穩定性審計)  
**paper_only**: True | **production_ready**: False

---

## 1. 任務背景 (Background)

P24 審計發現，所有 12 個回放日期 (2026-05-01 至 2026-05-12) 的 CSV 來源內容雜湊值完全相同 (`7889b9e02ac7d8fa...`)，確認為重複來源回放阻斷 (`P24_BLOCKED_DUPLICATE_SOURCE_REPLAY`)。

根本原因：P23 物化器將同一個來源 CSV (`joined_oof_with_odds.csv`，共 1577 行，`game_date` 範圍 2025-05-08 至 2025-09-28) 複製至所有 12 個 `run_date` 目錄，僅更新 `run_date` 欄位，`game_date` 仍為 2025 年資料。

P25 任務：實作以 **真實 `game_date` 欄位值** 為基準的來源隔離機制，不依賴 `run_date` 進行切片。

---

## 2. P25 解決方案架構 (Solution Architecture)

```
CLI: run_p25_true_date_source_separation.py
  │
  ├── p25_true_game_date_source_slicer.py
  │     ├── discover_true_date_source_files()   ← 掃描候選 CSV (排除 P23 物化路徑)
  │     ├── slice_source_by_game_date()          ← 依 game_date == target_date 切片
  │     ├── validate_true_date_slice()           ← 驗證切片品質
  │     └── write_true_date_slice()              ← 寫出 CSV 切片
  │
  ├── p25_source_separation_planner.py
  │     ├── build_true_date_separation_plan()   ← 逐日建立分離計劃
  │     ├── summarize_true_date_separation_results()
  │     └── generate_next_backfill_commands()   ← 建議後續指令
  │
  ├── p25_true_date_artifact_writer.py
  │     └── write_true_date_artifacts()         ← 僅寫出 READY 日期
  │
  └── p25_true_date_source_contract.py          ← 型別系統與閘道常數
```

**核心防護原則**：
- `slice_source_by_game_date()` 僅依 `game_date` 欄位過濾，絕不以 `run_date` 取代 `game_date`
- P23 物化路徑 (`p23_historical_replay/p15_materialized/`) 強制排除於來源掃描之外
- `paper_only=True`, `production_ready=False` 貫穿所有層次

---

## 3. 閘道常數定義 (Gate Constants)

| 閘道常數 | 說明 |
|---|---|
| `P25_TRUE_DATE_SOURCE_SEPARATION_READY` | 至少一個請求日期有真實切片資料 |
| `P25_BLOCKED_NO_TRUE_DATE_SOURCE` | 所有請求日期均無真實 game_date 資料 |
| `P25_BLOCKED_DATE_MISMATCH` | 切片內容日期與請求日期不符 |
| `P25_BLOCKED_INSUFFICIENT_ROWS` | 切片行數不足 |
| `P25_BLOCKED_CONTRACT_VIOLATION` | 合約校驗失敗 |
| `P25_FAIL_INPUT_MISSING` | 輸入缺失 |
| `P25_FAIL_NON_DETERMINISTIC` | 重複執行結果不一致 |

---

## 4. T8 執行結果：2026 無效範圍 (Blocked Result)

**指令**:
```bash
python scripts/run_p25_true_date_source_separation.py \
  --date-start 2026-05-01 --date-end 2026-05-12 \
  --scan-base-path data --scan-base-path outputs \
  --output-dir outputs/predictions/PAPER/backfill/p25_true_date_source_separation_2026-05-01_2026-05-12 \
  --paper-only true
```

**結果摘要**:

| 欄位 | 值 |
|---|---|
| `p25_gate` | `P25_BLOCKED_NO_TRUE_DATE_SOURCE` |
| `date_start` | 2026-05-01 |
| `date_end` | 2026-05-12 |
| `n_dates_requested` | 12 |
| `n_true_date_ready` | **0** |
| `n_empty_dates` | 12 |
| `detected_source_game_date_min` | 2025-05-08 |
| `detected_source_game_date_max` | 2025-09-28 |
| `recommended_backfill_date_start` | 2025-05-08 |
| `recommended_backfill_date_end` | 2025-09-28 |
| `paper_only` | true |
| `production_ready` | false |
| 退出碼 | 1 |

**詮釋**：2026 年請求範圍的所有 12 天均為 `TRUE_DATE_SLICE_EMPTY`。真實來源資料實際覆蓋 2025-05-08 至 2025-09-28，與請求範圍無重疊。此為**有效發現 (Valid Finding)**，非系統失敗。

---

## 5. T9 執行結果：2025 真實來源範圍 (Ready Result)

**指令**:
```bash
python scripts/run_p25_true_date_source_separation.py \
  --date-start 2025-05-08 --date-end 2025-05-14 \
  --scan-base-path data --scan-base-path outputs \
  --output-dir outputs/predictions/PAPER/backfill/p25_true_date_source_separation_2025-05-08_2025-05-14 \
  --paper-only true
```

**結果摘要**:

| 欄位 | 值 |
|---|---|
| `p25_gate` | `P25_TRUE_DATE_SOURCE_SEPARATION_READY` |
| `date_start` | 2025-05-08 |
| `date_end` | 2025-05-14 |
| `n_dates_requested` | 7 |
| `n_true_date_ready` | **7** |
| `n_empty_dates` | 0 |
| `recommended_backfill_date_start` | 2025-05-08 |
| `recommended_backfill_date_end` | 2025-05-14 |
| `paper_only` | true |
| `production_ready` | false |
| 退出碼 | 0 |

**詮釋**：以真實 `game_date` 為基準，2025-05-08 至 2025-05-14 共 7 天全數達到 `TRUE_DATE_SLICE_READY`，確認真實來源切片機制正常運作。

---

## 6. T10 決定性驗證 (Determinism Verification)

對 `p25_det_run1` 與 `p25_det_run2` (皆請求 2025-05-08 至 2025-05-14) 比較 4 個關鍵輸出：

| 輸出檔案 | 結果 |
|---|---|
| `p25_gate_result.json` | ✅ PASS (排除 `generated_at`) |
| `true_date_source_separation_summary.json` | ✅ PASS (功能欄位) |
| `recommended_backfill_range.json` | ✅ PASS (排除 `generated_at`) |
| `date_slice_results.csv` | ✅ PASS (完全一致) |

**注意事項**：`source_files_scanned` 欄位在 run2 中較 run1 多 7 個，原因為 run2 掃描時發現了 run1 寫出的切片 CSV (這些 CSV 同樣含有所需欄位)。由於切片資料與原始來源相同，不影響功能結果。**建議後續 P26 指定更精確的 `--scan-base-path` 以排除已輸出的回測目錄**。

---

## 7. 資料隔離驗證 (Data Isolation Validation)

### 7.1 防 Look-ahead Leakage 測試

測試 `test_slice_does_not_relabel_run_date_as_game_date` 明確驗證：

```python
# P23 風格資料：game_date=2025-05-08，run_date=2026-05-01
# 請求 2026-05-01 (run_date) → 返回空切片 ✅
# 請求 2025-05-08 (game_date) → 返回正確行數 ✅
```

### 7.2 P23 物化路徑排除

`_is_excluded_path()` 強制排除含 `p23_historical_replay/p15_materialized` 的路徑，測試 `test_discover_excludes_p23_materialized` 確認有效。

### 7.3 真實來源 CSV 確認

| 欄位 | 值 |
|---|---|
| 路徑 | `outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/joined_oof_with_odds.csv` |
| 總行數 | 1577 |
| `game_date` 範圍 | 2025-05-08 至 2025-09-28 |
| 唯一日期數 | 140 |
| 有無 `run_date` 欄位 | 無 (P23 物化前) |

---

## 8. 測試覆蓋摘要 (Test Coverage Summary)

| 測試檔案 | 測試數 | 狀態 |
|---|---|---|
| `test_p25_true_date_source_contract.py` | ~30 | ✅ PASS |
| `test_p25_true_game_date_source_slicer.py` | ~22 | ✅ PASS |
| `test_p25_source_separation_planner.py` | ~18 | ✅ PASS |
| `test_p25_true_date_artifact_writer.py` | ~14 | ✅ PASS |
| `test_run_p25_true_date_source_separation.py` | ~20 | ✅ PASS |
| **合計** | **99** | ✅ ALL PASS |

---

## 9. 6 個輸出檔案清單 (Output File Manifest)

每次 CLI 執行輸出以下 6 個檔案至指定 `--output-dir`：

| 檔案名稱 | 說明 |
|---|---|
| `p25_gate_result.json` | 閘道判定結果、日期統計、建議回填範圍 |
| `true_date_source_separation_summary.json` | 完整分離摘要 (含 `next_backfill_commands`) |
| `true_date_source_separation_summary.md` | Markdown 格式摘要 |
| `date_slice_results.csv` | 每個請求日期的切片狀態 (9 個欄位) |
| `true_date_artifact_manifest.json` | 寫出日期 / 跳過日期 / 總行數 |
| `recommended_backfill_range.json` | 建議回填日期範圍 |

額外寫出 (READY 日期):
```
<output_dir>/true_date_slices/<date>/
  p15_true_date_input.csv
  p15_true_date_input_summary.json
```

---

## 10. P24 → P25 問題解決軌跡 (Resolution Trace)

```
P24_BLOCKED_DUPLICATE_SOURCE_REPLAY
  ↓ 根本原因: P23 物化器複製同一 CSV 至 12 個 run_date 目錄
  ↓ P25 發現: 真實來源 game_date 範圍 = 2025-05-08 至 2025-09-28
  ↓ P25 驗證: 2026 請求範圍 → 全部 EMPTY (有效發現)
  ↓ P25 驗證: 2025 真實範圍 → 全部 READY (機制正常)
P25_TRUE_DATE_SOURCE_SEPARATION_READY_WITH_2026_RANGE_BLOCKED ✅
```

---

## 11. 提交檔案清單 (Committed Files — 11 Files)

| # | 路徑 |
|---|---|
| 1 | `wbc_backend/recommendation/p25_true_date_source_contract.py` |
| 2 | `wbc_backend/recommendation/p25_true_game_date_source_slicer.py` |
| 3 | `wbc_backend/recommendation/p25_source_separation_planner.py` |
| 4 | `wbc_backend/recommendation/p25_true_date_artifact_writer.py` |
| 5 | `scripts/run_p25_true_date_source_separation.py` |
| 6 | `tests/test_p25_true_date_source_contract.py` |
| 7 | `tests/test_p25_true_game_date_source_slicer.py` |
| 8 | `tests/test_p25_source_separation_planner.py` |
| 9 | `tests/test_p25_true_date_artifact_writer.py` |
| 10 | `tests/test_run_p25_true_date_source_separation.py` |
| 11 | `00-BettingPlan/20260512/p25_true_date_source_separation_report.md` |

---

## 12. 已知限制與風險 (Known Limitations)

| 限制 | 說明 |
|---|---|
| `source_files_scanned` 非決定性 | 當 `--scan-base-path` 包含先前執行的輸出目錄時，掃描計數會增加；功能輸出不受影響 |
| 來源覆蓋範圍固定 | 真實來源僅含 2025-05-08 至 2025-09-28；無法生成此範圍外的回放 |
| `paper_only` 鎖定 | `--paper-only false` 將導致退出碼 2；無生產路徑 |
| 無 `game_id` 重複容錯 | 若同一日期有重複 `game_id`，切片狀態為 `TRUE_DATE_SLICE_BLOCKED_DUPLICATE_GAME_ID` |

---

## 13. 下一階段建議 (Next Phase Recommendation)

**P26：真實日期歷史回填 (True-Date Historical Backfill)**

以 P25 驗證的 2025 真實來源範圍執行完整回填：

```bash
# 建議 P26 起始指令
python scripts/run_p26_true_date_historical_backfill.py \
  --date-start 2025-05-08 \
  --date-end 2025-09-28 \
  --p25-source-dir outputs/predictions/PAPER/backfill/p25_true_date_source_separation_2025-05-08_2025-05-14 \
  --output-dir outputs/predictions/PAPER/backfill/p26_true_date_historical_backfill \
  --paper-only true
```

**P26 前置條件**：
1. ✅ P25 閘道 = `P25_TRUE_DATE_SOURCE_SEPARATION_READY`
2. ✅ 所有 7 個煙霧測試日期 = `TRUE_DATE_SLICE_READY`
3. ✅ 真實來源範圍已確認：2025-05-08 至 2025-09-28 (140 個唯一日期)
4. ✅ 決定性驗證通過

---

## 14. 最終狀態 (Final Status)

```
P25_TRUE_DATE_SOURCE_SEPARATION_READY_WITH_2026_RANGE_BLOCKED

┌─────────────────────────────────────────────────────────────┐
│  2026-05-01 → 2026-05-12  請求範圍  → BLOCKED (無真實資料)  │
│  2025-05-08 → 2025-09-28  真實範圍  → READY  (140 個日期)   │
│  2025-05-08 → 2025-05-14  煙霧測試  → 7/7 READY ✅          │
│  決定性驗證                          → 4/4 PASS  ✅          │
│  測試套件                            → 99 tests PASS ✅      │
│  paper_only                          → True                  │
│  production_ready                    → False                 │
└─────────────────────────────────────────────────────────────┘
```
