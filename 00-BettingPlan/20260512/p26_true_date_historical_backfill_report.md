# P26 True-Date Historical Backfill Replay — 最終驗收報告

**標記 (Marker)**: `P26_TRUE_DATE_HISTORICAL_BACKFILL_READY`  
**執行日期**: 2026-05-12  
**分支**: `p13-clean`  
**前置 commit**: `6452911` (P25 真實賽事日期來源分離)  
**作者**: AI Quant Research Pipeline

---

## 1. 任務目標 (Objective)

P26 任務目標：在 P25 完成真實賽事日期 (true game_date) 來源分離後，對 P25 輸出的真實日期切片 (true-date slices) 執行歷史回測重播 (Historical Backfill Replay)。

**核心原則**:
- 只使用 P25 真實日期切片作為輸入來源
- 絕不重用 P23 重複物化資料 (`p23_historical_replay/p15_materialized/`)
- 絕不將 2025 賽季資料重新標記為 2026 年證據
- `paper_only=True`, `production_ready=False` 貫穿全流程

---

## 2. 系統架構 (System Architecture)

P26 模組分層設計：

```
scripts/run_p26_true_date_historical_backfill.py   ← CLI 入口
    └── wbc_backend/recommendation/
        ├── p26_true_date_replay_contract.py        ← 型別定義 & 常數
        ├── p26_true_date_replay_input_adapter.py   ← 切片載入 & 驗證
        ├── p26_per_date_true_replay_runner.py      ← 單日回測執行
        └── p26_true_date_replay_aggregator.py      ← 跨日聚合 & 輸出
```

**資料流**:
```
P25 true_date_slices/<date>/p15_true_date_input.csv
    → 驗證 (日期吻合、必要欄位)
    → 識別 active entries (gate_decision == P16_6_ELIGIBLE_PAPER_RECOMMENDATION)
    → 讀取已結算資料 (settlement_status / pnl_units / is_win / is_loss)
    → 聚合跨日統計
    → 6 個輸出檔案
```

---

## 3. 合約設計 (Contract Design)

### 3.1 Per-Date 閘門常數
| 常數 | 說明 |
|------|------|
| `P26_DATE_REPLAY_READY` | 該日期回測成功 |
| `P26_DATE_BLOCKED_NO_TRUE_DATE_SLICE` | 切片檔案不存在或為空 |
| `P26_DATE_BLOCKED_INVALID_TRUE_DATE_SLICE` | 欄位缺失或日期不符 |
| `P26_DATE_BLOCKED_P15_INPUT_BUILD_FAILED` | 輸入轉換失敗 |
| `P26_DATE_BLOCKED_REPLAY_FAILED` | 回測執行失敗 |
| `P26_DATE_FAIL_CONTRACT_VIOLATION` | 合約違規 |

### 3.2 聚合閘門常數
| 常數 | 說明 |
|------|------|
| `P26_TRUE_DATE_HISTORICAL_BACKFILL_READY` | ≥1 個日期成功 |
| `P26_BLOCKED_NO_READY_DATES` | 所有日期皆 blocked |
| `P26_BLOCKED_ALL_DATES_FAILED` | 所有日期皆失敗 |
| `P26_FAIL_INPUT_MISSING` | P25 目錄不存在 |
| `P26_FAIL_NON_DETERMINISTIC` | 兩次執行結果不同 |

### 3.3 不變量 (Invariants)
所有 frozen dataclass 在 `__post_init__` 強制驗證：
- `paper_only=True` (否則 `ValueError`)
- `production_ready=False` (否則 `ValueError`)

---

## 4. 輸入資料規格 (Input Data Specification)

P25 真實日期切片為 P17 推薦帳本資料，欄位包含：

| 欄位 | 說明 |
|------|------|
| `game_id` | 比賽識別碼 |
| `date` | 真實賽事日期 (YYYY-MM-DD) |
| `gate_decision` | P16.6 閘門決策 |
| `paper_stake_units` | 已計算下注單位 (0 for blocked) |
| `pnl_units` | 已計算損益 |
| `settlement_status` | 結算狀態 (SETTLED_WIN / SETTLED_LOSS / UNSETTLED_NOT_RECOMMENDED) |
| `is_win`, `is_loss` | 結算布林值 |
| `y_true` | 真實賽果 |

**關鍵設計**: 結算資料已由 P17 處理完畢，P26 直接讀取，不重複執行 P16/P17 管線。

---

## 5. 策略參數 (Policy Constants)

```python
EDGE_THRESHOLD    = 0.05   # 最低邊緣值
MAX_STAKE_CAP     = 0.0025 # 最大下注比例 (bankroll fraction)
KELLY_FRACTION    = 0.10   # Kelly 係數
ODDS_DECIMAL_MAX  = 2.50   # 最大賠率
```

Active 條件: `gate_decision == 'P16_6_ELIGIBLE_PAPER_RECOMMENDATION'`

---

## 6. 輸出規格 (Output Specification)

每次 CLI 執行產生 6 個檔案到 `output_dir/`：

| 檔案 | 說明 |
|------|------|
| `p26_gate_result.json` | 整體閘門結果 |
| `true_date_replay_summary.json` | 聚合統計 |
| `true_date_replay_summary.md` | 人類可讀摘要 |
| `date_replay_results.csv` | 每日回測結果表 |
| `blocked_dates.json` | 封鎖日期清單 |
| `artifact_manifest.json` | 產物清單 |

---

## 7. 測試結果 (Test Results)

### 7.1 P26 單元測試
```
tests/test_p26_true_date_replay_contract.py
tests/test_p26_true_date_replay_input_adapter.py
tests/test_p26_per_date_true_replay_runner.py
tests/test_p26_true_date_replay_aggregator.py
tests/test_run_p26_true_date_historical_backfill.py

結果: 108 passed
```

### 7.2 全套測試 (P23 + P24 + P25 + P26)
```
結果: 357 passed in 32.20s
```

所有 P23、P24、P25 既有測試維持通過，零回歸。

---

## 8. 真實煙霧測試 (Real Narrow Smoke Run)

### 8.1 執行指令
```bash
PYTHONPATH=. .venv/bin/python scripts/run_p26_true_date_historical_backfill.py \
  --date-start 2025-05-08 \
  --date-end 2025-05-14 \
  --p25-dir outputs/predictions/PAPER/backfill/p25_true_date_source_separation_2025-05-08_2025-05-14 \
  --output-dir outputs/predictions/PAPER/backfill/p26_true_date_historical_backfill_2025-05-08_2025-05-14 \
  --paper-only true
```

### 8.2 輸出結果
```
[P26] gate=P26_TRUE_DATE_HISTORICAL_BACKFILL_READY
[P26] dates_requested=7  dates_ready=7  dates_blocked=0
[P26] total_active=25  wins=11  losses=14
[P26] total_stake=6.2500  total_pnl=-0.5507  ROI=-0.0881  hit_rate=0.4400
Exit code: 0
```

### 8.3 逐日統計
| 日期 | 總列數 | Active | 勝 | 敗 | Stake | PnL |
|------|--------|--------|----|----|-------|-----|
| 2025-05-08 | 4 | 1 | 1 | 0 | 0.25 | +0.1471 |
| 2025-05-09 | 15 | 6 | 3 | 3 | 1.50 | +0.0398 |
| 2025-05-10 | 11 | 6 | 3 | 3 | 1.50 | +0.1500 |
| 2025-05-11 | 12 | 5 | 1 | 4 | 1.25 | −0.7125 |
| 2025-05-12 | 11 | 4 | 2 | 2 | 1.00 | 0.0000 |
| 2025-05-13 | 11 | 1 | 1 | 0 | 0.25 | +0.3250 |
| 2025-05-14 | 12 | 2 | 0 | 2 | 0.50 | −0.5000 |
| **合計** | **76** | **25** | **11** | **14** | **6.25** | **−0.5507** |

---

## 9. 聚合績效分析 (Aggregate Performance Analysis)

| 指標 | 數值 |
|------|------|
| 總下注單位 | 6.25 units |
| 總損益 | −0.5507 units |
| 聚合 ROI | **−8.81%** |
| 命中率 (Hit Rate) | **44.0%** (11/25) |
| 未結算 | 0 筆 |

**分析**:
- 7 日內 25 筆 active 推薦，全數已結算
- ROI −8.81% 在小樣本 (n=25) 下屬正常統計波動範圍
- Hit rate 44% 低於隨機猜測 50%，顯示此窄範圍樣本有負偏
- 需 P27 擴展至 2025-05-08 → 2025-09-28 (140 日, 樣本數 ≥ 1500) 以獲得統計顯著性

---

## 10. 決定論驗證 (Determinism Verification)

執行兩次 (`p26_det_run1`, `p26_det_run2`)，排除 `generated_at` 與 `output_dir` 後比較：

| 檔案 | 結果 |
|------|------|
| `p26_gate_result.json` | ✅ IDENTICAL |
| `true_date_replay_summary.json` | ✅ IDENTICAL |
| `blocked_dates.json` | ✅ IDENTICAL |
| `artifact_manifest.json` | ✅ IDENTICAL |
| `date_replay_results.csv` | ✅ IDENTICAL |

**結論**: P26 完全決定論 ✅

---

## 11. 資料隔離驗證 (Data Isolation Verification)

P26 確保以下資料隔離規則：

| 規則 | 狀態 |
|------|------|
| 不使用 `p23_historical_replay/p15_materialized/` | ✅ 來源為 P25 true-date slices |
| 不將 2025 資料重標記為 2026 | ✅ `date` 欄位保持原始值 |
| 不重跑 P16/P17 管線 | ✅ 直接讀取已計算之 settlement 欄位 |
| `paper_only=True` 貫穿全層 | ✅ dataclass `__post_init__` 強制驗證 |
| `production_ready=False` 貫穿全層 | ✅ dataclass `__post_init__` 強制驗證 |

---

## 12. 新增檔案清單 (Files Added)

| 檔案 | 說明 |
|------|------|
| `wbc_backend/recommendation/p26_true_date_replay_contract.py` | 型別 & 常數定義 |
| `wbc_backend/recommendation/p26_true_date_replay_input_adapter.py` | 切片載入 & 驗證 |
| `wbc_backend/recommendation/p26_per_date_true_replay_runner.py` | 單日回測執行器 |
| `wbc_backend/recommendation/p26_true_date_replay_aggregator.py` | 跨日聚合器 |
| `scripts/run_p26_true_date_historical_backfill.py` | CLI 入口 |
| `tests/test_p26_true_date_replay_contract.py` | 合約單元測試 |
| `tests/test_p26_true_date_replay_input_adapter.py` | 輸入轉接器測試 |
| `tests/test_p26_per_date_true_replay_runner.py` | 單日執行器測試 |
| `tests/test_p26_true_date_replay_aggregator.py` | 聚合器測試 |
| `tests/test_run_p26_true_date_historical_backfill.py` | CLI 整合測試 |
| `00-BettingPlan/20260512/p26_true_date_historical_backfill_report.md` | 本報告 |

---

## 13. 閘門決策 (Gate Decision)

```
P26_TRUE_DATE_HISTORICAL_BACKFILL_READY
```

**條件滿足**:
- ✅ 357 tests passed (P23 + P24 + P25 + P26)
- ✅ 7/7 真實日期切片成功回測
- ✅ 所有輸出結果決定論 (5/5 檔案 IDENTICAL)
- ✅ `paper_only=True`, `production_ready=False` 貫穿全層
- ✅ 無資料洩漏 (data leakage) 風險

---

## 14. 已知限制 (Known Limitations)

1. **樣本數不足**: n=25 (7天) 遠低於統計顯著門檻 (≥1500 建議)
2. **狹窄時間窗**: 僅覆蓋 2025-05-08 至 2025-05-14 (7天)
3. **ROI -8.81% 不具代表性**: 小樣本波動正常

---

## 15. 下一階段 (Next Phase)

### P27: 全 2025 賽季真實日期回填擴展

**目標範圍**: 2025-05-08 → 2025-09-28 (約 140 個賽事日, 預估 ≥ 1500 筆 active 推薦)

**步驟**:
1. 執行 P25 全範圍掃描 (`--date-start 2025-05-08 --date-end 2025-09-28`)
2. 驗證所有日期切片可用性
3. 執行 P26 全範圍回測
4. 生成統計顯著性報告 (n ≥ 1500)
5. 若 Sharpe ratio > 0.5，進行 P28 策略最佳化

**指令範例**:
```bash
# P25 全範圍
PYTHONPATH=. .venv/bin/python scripts/run_p25_true_date_source_separation.py \
  --date-start 2025-05-08 --date-end 2025-09-28 \
  --scan-base-path data --scan-base-path outputs \
  --output-dir outputs/predictions/PAPER/backfill/p25_true_date_source_separation_2025-05-08_2025-09-28 \
  --paper-only true

# P26 全範圍
PYTHONPATH=. .venv/bin/python scripts/run_p26_true_date_historical_backfill.py \
  --date-start 2025-05-08 --date-end 2025-09-28 \
  --p25-dir outputs/predictions/PAPER/backfill/p25_true_date_source_separation_2025-05-08_2025-09-28 \
  --output-dir outputs/predictions/PAPER/backfill/p26_true_date_historical_backfill_2025-05-08_2025-09-28 \
  --paper-only true
```

---

*生成時間: 2026-05-12 | 標記: `P26_TRUE_DATE_HISTORICAL_BACKFILL_READY` | PAPER_ONLY*
