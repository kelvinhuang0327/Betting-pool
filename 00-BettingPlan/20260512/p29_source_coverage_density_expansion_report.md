# P29 Source Coverage & Active Entry Density Expansion — Final Report

**產出時間**: 2026-05-12  
**分析管線階段**: P29  
**分支**: `p13-clean`  
**前序 Commit**: `a85f5be` (P28 完成)

---

## 1. P29 Gate 結果

```
P29_SOURCE_COVERAGE_DENSITY_EXPANSION_BLOCKED: P29_BLOCKED_SOURCE_COVERAGE_INSUFFICIENT
```

| 欄位 | 數值 |
|------|------|
| `p29_gate` | `P29_BLOCKED_SOURCE_COVERAGE_INSUFFICIENT` |
| `audit_status` | `DENSITY_EXPANSION_BLOCKED_INSUFFICIENT_SOURCE` |
| `paper_only` | `true` |
| `production_ready` | `false` |

---

## 2. 密度診斷 (Density Diagnosis)

### 當前狀態

| 指標 | 數值 |
|------|------|
| 總來源資料列 | 1,577 |
| 當前活躍入場 (active entries) | 324 |
| 目標活躍入場 | 1,500 |
| 密度缺口 (density_gap) | 1,176 |
| 活躍轉換率 | 20.5% (324 / 1,577) |

### Gate Reason 分佈

| Gate Reason | 筆數 | 佔比 |
|-------------|------|------|
| `P16_6_ELIGIBLE_PAPER_RECOMMENDATION` ← 活躍 | 324 | 20.5% |
| `P16_6_BLOCKED_EDGE_BELOW_P18_THRESHOLD` | 907 | 57.5% |
| `P16_6_BLOCKED_ODDS_ABOVE_POLICY_MAX` | 344 | 21.8% |
| `P16_6_BLOCKED_UNKNOWN` | 2 | 0.1% |
| **合計** | **1,577** | **100%** |

### 主要阻塞原因

- **Primary blocker**: `edge_threshold` — 57.5% 的資料因 edge < 5% 遭到阻擋。
- 次要阻塞: `odds_cap` — 21.8% 的資料因 odds > 2.50 遭到阻擋。

---

## 3. 政策敏感性模擬 (Policy Sensitivity Simulation)

### 政策格 (Policy Grid)

測試 64 種組合：

| 參數 | 測試值 |
|------|--------|
| `edge_threshold` | 0.02, 0.03, 0.04, 0.05 |
| `odds_decimal_max` | 2.50, 3.00, 4.00, 999 (無上限) |
| `max_stake_cap` | 0.001, 0.0025 |
| `kelly_fraction` | 0.05, 0.10 |

### 模擬結果

| 指標 | 數值 |
|------|------|
| 測試組合總數 | 64 |
| 最佳政策候選活躍筆數 | **563** |
| 目標 (1,500) 是否可達 | **否** |
| 任一候選達到目標 | **否** |

### 分析說明

最寬鬆政策 (`edge_threshold=0.02`, `odds_decimal_max=999`) 下，仍只有 **563** 筆可活躍。

原因：P25 資料集中有相當比例的 edge 值為負數或低於 2%，即使完全移除 odds 上限，也無法通過 edge ≥ 2% 門檻達到 1,500 筆目標。

**所有政策候選均標記為**:
- `is_deployment_ready = False`
- `exploratory_only = True`
- `paper_only = True`
- `production_ready = False`

---

## 4. 來源覆蓋掃描 (Source Coverage Expansion Scan)

### 掃描範圍

- `data/` 目錄下所有 CSV/XLSX 檔
- `outputs/predictions/PAPER/backfill/` 目錄下其他 P25 範圍

### 掃描結果

| 來源類型 | 候選數 | 安全可用數 |
|----------|--------|------------|
| 其他 P25 日期範圍 (子集) | 2 | 0 |
| Raw 資料檔 (mlb_odds, gl2025 等) | 多個 | 0 |
| **合計** | **多個** | **0** |

### 不可用原因

| 來源 | 原因 |
|------|------|
| Alt P25 `2025-05-08→2025-05-14` | 子集 (subset)，資料重疊風險，無去重管道 |
| Alt P25 `2025-05-08→2025-05-21` | 子集 (subset)，資料重疊風險，無去重管道 |
| `data/mlb_2025/mlb_odds_2025_real.csv` | 17 欄，不含 `edge`, `y_true`, `gate_reason` 等必要 P25 欄位 |
| `data/mlb_2025/gl2025.zip` | 賽事 game log，需完整 P22→P25 管道轉換 |

**結論**: 無安全可用的新資料來源可立即擴充樣本量。

---

## 5. 決定性驗證 (Determinism Check)

兩次獨立執行：

| 執行 | Gate | 活躍筆數 |
|------|------|---------|
| 第 1 次 | `P29_BLOCKED_SOURCE_COVERAGE_INSUFFICIENT` | 563 |
| 第 2 次 | `P29_BLOCKED_SOURCE_COVERAGE_INSUFFICIENT` | 563 |

**✅ 決定性驗證通過 — 兩次結果完全一致。**

---

## 6. 輸出檔案

路徑: `outputs/predictions/PAPER/backfill/p29_source_coverage_density_expansion_2025-05-08_2025-09-28/`

| 檔案 | 說明 |
|------|------|
| `p29_gate_result.json` | Gate 結果 JSON |
| `density_expansion_plan.json` | 完整擴充計劃 JSON |
| `density_diagnosis.json` | 密度診斷 JSON |
| `density_diagnosis.md` | 密度診斷 Markdown |
| `policy_sensitivity_results.csv` | 64 政策候選 CSV |
| `policy_sensitivity_summary.json` | 政策敏感性摘要 JSON |
| `source_coverage_expansion.json` | 來源掃描 JSON |
| `source_coverage_expansion.md` | 來源掃描 Markdown |

---

## 7. 推薦後續行動 (Recommended Next Action)

> **BLOCKED**: 無安全來源擴充方案，且無政策候選可達目標 1,500 筆。  
> 建議取得額外 MLB 歷史賽季資料（2024 或更早賽季，或 2026 賽季完整資料），重新執行 P22→P25 管道後再進行 P29 審核。

### P30 建議路徑

1. **取得 MLB 2024 完整賽季資料** 並透過 P22→P23→P24→P25 管道生成新的 True Date Slices。
2. 確保新資料與現有 2025 資料無重疊（date dedup）。
3. 重新執行 P29，驗證合併後的活躍入場是否達到 1,500 筆目標。

---

## 8. 測試結果

### P29 測試 (100 tests)

| 測試檔 | 通過 |
|--------|------|
| `test_p29_density_expansion_contract.py` | ✅ |
| `test_p29_density_diagnosis_analyzer.py` | ✅ |
| `test_p29_policy_sensitivity_simulator.py` | ✅ |
| `test_p29_source_coverage_expansion_scanner.py` | ✅ |
| `test_p29_density_expansion_planner.py` | ✅ |
| `test_run_p29_source_coverage_density_expansion.py` | ✅ |

### 完整回歸測試 (P28 + P29)

```
204 passed in 12.27s
```

**✅ 全部通過，無任何失敗。**

---

## 9. Terminal Marker

```
P29_SOURCE_COVERAGE_DENSITY_EXPANSION_BLOCKED: P29_BLOCKED_SOURCE_COVERAGE_INSUFFICIENT
```
