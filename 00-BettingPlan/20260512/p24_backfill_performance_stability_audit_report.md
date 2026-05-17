# P24 Backfill Performance Stability Audit Report

**階段**: P24 Backfill Performance Stability Audit  
**審計範圍**: 2026-05-01 → 2026-05-12（12 個回測日期）  
**執行日期**: 2026-05-12  
**專案分支**: `p13-clean`  
**前序提交**: `937fa0c` (P23 Historical Replay Backfill)  
**最終閘道標記**: `P24_BACKFILL_PERFORMANCE_STABILITY_AUDIT_DUPLICATE_SOURCE_BLOCKED`

---

## 1. 執行摘要 (Executive Summary)

P24 審計對 P23 12 天歷史回播（2026-05-01 至 2026-05-12）進行了完整的來源完整性與效能穩定性分析。

**核心發現**：所有 12 個回播日期共享**完全相同的來源 CSV**（`joined_oof_with_odds.csv`），內容雜湊（排除 `run_date` 欄位）均為：

```
7889b9e02ac7d8faa379f9641ce00f0adef620c0f8abe7f04e3792b32cb218cf
```

這確認了 P23 的物化器（materializer）僅複製同一份 2026-05-12 P15 快照，逐日更改 `run_date` 欄，而非為每個日期獨立抓取對應賽事數據。這是一次**重複來源回播（Duplicate Source Replay）**，而非真正的多日獨立回測。

**P24 閘道判定**：`P24_BLOCKED_DUPLICATE_SOURCE_REPLAY`（Exit Code: 1）  
**下一步建議**：P25 Full Historical Source Separation / True Multi-Date Artifact Builder

---

## 2. 倉庫狀態 (Repository State)

| 項目 | 值 |
|------|-----|
| 倉庫路徑 | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13` |
| 分支 | `p13-clean` |
| P23 提交 | `937fa0c` |
| Python 環境 | `.venv/bin/python` (Python 3.13.8) |
| `PYTHONPATH` | `.` |
| `paper_only` | `True`（所有層級強制執行） |
| `production_ready` | `False`（所有層級強制執行） |

---

## 3. P23 來源回顧 (P23 Source Review)

P23 歷史回播執行流程為：
1. `p23_p15_source_materializer.py` 從 `outputs/predictions/PAPER/<date>/` 讀取 P15 預測數據
2. 為每個回播日期（2026-05-01 → 2026-05-12）寫出 `joined_oof_with_odds.csv`

**發現的問題**：物化器使用的 P15 快照來自同一來源（2026-05-12 的完整 P15 輸出），並對所有 12 個日期複製相同 CSV，僅將 `run_date` 欄位改為對應日期。

**P23 閘道結果**（先前已通過）：
```
P23_HISTORICAL_REPLAY_BACKFILL_READY
12/12 日期全部就緒
```

P23 的閘道邏輯僅驗證文件存在性與欄位完整性，未檢查跨日期來源唯一性——此即 P24 的核心審計目標。

---

## 4. 來源完整性審計 (Source Integrity Audit)

### 4.1 審計設計

模組：`wbc_backend/recommendation/p24_source_integrity_auditor.py`

每個日期的物化 CSV 路徑：
```
outputs/predictions/PAPER/<run_date>/p23_historical_replay/p15_materialized/joined_oof_with_odds.csv
```

計算三種獨立雜湊值：
- **`content_hash`**：對 CSV 全部內容（排除 `run_date` 欄）計算 SHA-256 — 偵測完全相同的底層數據
- **`game_id_set_hash`**：對所有 `game_id` 排序後計算 SHA-256 — 對欄位順序不敏感的賽事集合比較
- **`file_hash`**：對原始文件位元組計算 SHA-256 — 包含 `run_date` 欄，預期每日不同

### 4.2 審計結果

| 指標 | 值 |
|------|-----|
| 審計日期數 | 12 |
| 獨立來源日期數 | **0** |
| 重複來源群組數 | **1**（全部 12 個日期） |
| `source_hash_unique_count` | **1** |
| `source_hash_duplicate_count` | **11** |
| `game_id_set_unique_count` | **1** |
| `all_dates_date_mismatch` | **True** |
| `any_date_date_mismatch` | **True** |

### 4.3 每日詳細雜湊

所有 12 個日期的 `content_hash` 均相同：

```
7889b9e02ac7d8faa379f9641ce00f0adef620c0f8abe7f04e3792b32cb218cf
```

每個文件：
- `row_count`：**1,577 筆**
- `game_id_count`：**1,577 個唯一 game_id**
- `game_date_range_str`：`2025-05-08:2025-09-28`（非 2026）
- `run_date_matches_game_date`：**False**（所有 12 個日期）

### 4.4 時間錯位確認

所有 1,577 個 `game_id` 均屬於 **2025 年 MLB 賽季**（格式：`2025-05-08_BOS_TEX` 等），而回播 `run_date` 為 2026-05-01 至 2026-05-12。這確認了：

> 這些數據是 2025 MLB 球季的 OOF 預測，被錯誤地作為 2026 WBC 回播來源使用。

---

## 5. 效能穩定性分析 (Performance Stability Audit)

### 5.1 每日效能指標

由於所有日期使用相同底層數據，每日效能指標完全相同：

| 指標 | 值 |
|------|-----|
| `n_active_paper_entries` | 324 |
| `n_settled_win` | 171 |
| `n_settled_loss` | 153 |
| `n_unsettled` | 0 |
| `total_stake_units` | 81.0 |
| `total_pnl_units` | 8.7304 |
| `roi_units` | 0.10778278086419754 |
| `hit_rate` | 0.5277777777777778 |
| `game_id_coverage` | 1.0 |

### 5.2 變異性指標

| 指標 | 值 | 解釋 |
|------|-----|------|
| `roi_std_by_date` | **0.00000000** | 零變異——確認重複來源 |
| `roi_min_by_date` | 0.10778278 | |
| `roi_max_by_date` | 0.10778278 | |
| `hit_rate_std_by_date` | **0.00000000** | 零變異——確認重複來源 |
| `active_entry_std_by_date` | **0.00000000** | 零變異——確認重複來源 |

### 5.3 加權總計

| 指標 | 值 |
|------|-----|
| `aggregate_roi_units` | 0.10778278086419754 |
| `aggregate_hit_rate` | 0.5277777777777778 |
| `total_stake_units` | 972.0（= 81.0 × 12） |
| `total_pnl_units` | 104.7648（= 8.7304 × 12） |

**重要警告**：這些加權總計並非來自 12 個獨立日期的真實多日累積，而是同一份數據重複 12 次的人工堆疊結果。任何基於此數據的策略盈利宣稱均無效。

### 5.4 效能可疑性判定

`detect_too_uniform_performance()` 觸發以下警告：
- ✗ 所有日期 ROI 完全相同
- ✗ 所有日期 hit_rate 完全相同
- ✗ 所有日期 active entry 數量完全相同
- ✗ 所有日期共享相同 source content hash
- ✗ 所有 12 個日期：`game_date ≠ run_date`

`performance_stability_flag`：`STABILITY_INSUFFICIENT_VARIANCE`

---

## 6. 閘道決策 (Gate Decision)

### 6.1 閘道優先級

```
優先級 1：STABILITY_SOURCE_INTEGRITY_BLOCKED
  → 超過 50% 的日期來自重複來源群組（12/12 = 100%）
  → 觸發 P24_BLOCKED_DUPLICATE_SOURCE_REPLAY
```

### 6.2 最終閘道結果

```
p24_gate:                    P24_BLOCKED_DUPLICATE_SOURCE_REPLAY
audit_status:                STABILITY_SOURCE_INTEGRITY_BLOCKED
n_dates_audited:             12
n_independent_source_dates:  0
n_duplicate_source_groups:   1
source_hash_unique_count:    1
source_hash_duplicate_count: 11
roi_std_by_date:             0.00000000
hit_rate_std_by_date:        0.00000000
production_ready:            False
paper_only:                  True
blocker_reason:              12/12 dates share identical source content (1 duplicate group(s)).
                             This is duplicate source replay, not independent evidence.
recommended_next_action:     Proceed to P25 Full Historical Source Separation /
                             True Multi-Date Artifact Builder.
```

**CLI Exit Code**：`1`（BLOCKED）

### 6.3 閘道判定說明

`P24_BLOCKED_DUPLICATE_SOURCE_REPLAY` 是一個**有效且正確的審計發現**，而非系統故障。P24 的核心任務正是偵測此類重複來源回播問題。此 BLOCK 狀態表示審計成功完成並如實報告了 P23 的數據隔離問題。

---

## 7. 輸出文件 (Output Files)

```
outputs/predictions/PAPER/backfill/p24_backfill_stability_audit_2026-05-01_2026-05-12/
├── stability_audit_summary.json       # 完整審計摘要
├── stability_audit_summary.md         # 可讀性報告
├── source_integrity_audit.json        # 來源完整性詳細結果
├── performance_stability_audit.json   # 效能穩定性分析
├── duplicate_source_findings.json     # 重複來源群組詳情
└── p24_gate_result.json              # 最終閘道判定
```

---

## 8. 測試覆蓋 (Test Coverage)

### 8.1 P24 測試文件

| 文件 | 測試數 | 狀態 |
|------|--------|------|
| `tests/test_p24_backfill_stability_contract.py` | ~30 | ✅ |
| `tests/test_p24_source_integrity_auditor.py` | ~18 | ✅ |
| `tests/test_p24_performance_stability_analyzer.py` | ~20 | ✅ |
| `tests/test_p24_backfill_stability_auditor.py` | ~15 | ✅ |
| `tests/test_run_p24_backfill_performance_stability_audit.py` | ~15 | ✅ |
| **總計** | **82** | **全部通過** |

### 8.2 回歸測試

P20–P24 全部測試套件：

```
PYTHONPATH=. .venv/bin/pytest -q tests/test_p2{0,1,2,3,4}*.py
347 passed in 0.85s
```

所有 P20、P21、P22、P22.5、P23、P24 測試均通過，無回歸。

---

## 9. 確定性驗證 (Determinism Verification)

執行兩次獨立 P24 運行：

```
run1: outputs/predictions/PAPER/backfill/p24_det_run1/
run2: outputs/predictions/PAPER/backfill/p24_det_run2/
```

比較結果（排除 `generated_at` 欄位）：

```
p24_gate_result.json:           MATCH
source_integrity_audit.json:    MATCH
performance_stability_audit.json: MATCH
duplicate_source_findings.json: MATCH
DETERMINISM: OK
```

---

## 10. 安全性聲明 (Security & Contract Guarantees)

- **`paper_only=True`**：在所有 Frozen Dataclass（`P24DatePerformanceProfile`、`P24DuplicateSourceFinding`、`P24SourceIntegrityProfile`、`P24StabilityAuditSummary`、`P24StabilityGateResult`）的 `__post_init__` 中強制執行
- **`production_ready=False`**：同上，在所有合約層級強制執行
- **不可修改性**：所有合約類別使用 `@dataclass(frozen=True)`
- **前向洩漏防護**：審計僅使用賽前狀態（`run_date` 時刻的數據），不引用任何賽後結算資訊

---

## 11. 新增模組清單 (New Modules)

| 模組 | 路徑 | 說明 |
|------|------|------|
| P24 合約 | `wbc_backend/recommendation/p24_backfill_stability_contract.py` | 凍結 Dataclass + 閘道常數 |
| 來源完整性審計器 | `wbc_backend/recommendation/p24_source_integrity_auditor.py` | SHA-256 雜湊 + 重複偵測 |
| 效能穩定性分析器 | `wbc_backend/recommendation/p24_performance_stability_analyzer.py` | 變異性 + 均一性偵測 |
| 回測穩定性審計主模組 | `wbc_backend/recommendation/p24_backfill_stability_auditor.py` | 整合審計管線 + 輸出寫入 |
| CLI 執行器 | `scripts/run_p24_backfill_performance_stability_audit.py` | 命令列介面（含安全守衛） |

---

## 12. 根本原因分析 (Root Cause Analysis)

### P23 物化器行為

`p23_p15_source_materializer.py` 在執行 P23 回播時：

1. 在 2026-05-12 產生了完整的 P15 `joined_oof_with_odds.csv`（包含 1,577 筆 2025 MLB 賽事）
2. 對所有 12 個回播日期，複製此快照至對應路徑
3. 僅將 `run_date` 欄位替換為各日期值

**後果**：所有 12 個「回播日期」實際上在使用相同的預測輸入，效能指標必然完全一致。

### 數據時間錯位

- 物化 CSV 的 `game_date` 範圍：`2025-05-08:2025-09-28`（2025 MLB 球季）
- 回播的 `run_date` 範圍：`2026-05-01:2026-05-12`（2026 WBC 賽季）
- 所有 1,577 個 game_id 均為 `2025-MMDD_TEAM1_TEAM2` 格式

這表示 P15 的輸出來自一個以 2025 MLB 數據訓練的 OOF 模型，被錯誤地作為 2026 WBC 預測的回播來源。

---

## 13. 生產可用性聲明 (Production Readiness Statement)

```
production_ready: False
paper_only: True
```

P24 BLOCKED 結果確認此回測系統**尚未達到生產就緒標準**，原因：

1. 12 個回播日期全部使用相同底層數據，缺乏獨立多日證據
2. 數據年份錯位（2025 MLB vs 2026 WBC）
3. 零效能變異（std=0.0）是重複數據的統計學確認，而非真實策略穩定性的證明

任何基於此 P23 回播結果的盈利宣稱（ROI=10.78%，hit_rate=52.78%）均來自數據重複，無法作為策略有效性的有效依據。

---

## 14. 下一步行動 (Next Steps)

### P25: Full Historical Source Separation / True Multi-Date Artifact Builder

目標：
1. **獨立日期數據抓取**：為每個回播日期（2026-05-01 → 2026-05-12），獨立從真實賽事數據源抓取該日期的賽事信息
2. **真實多日物化**：每個日期的 `joined_oof_with_odds.csv` 必須包含對應日期的真實賽事
3. **來源分離驗證**：P25 本身應包含 P24 類型的來源完整性驗證，確保每個日期的 `content_hash` 均不同
4. **時間對齊確認**：`game_date` 應與 `run_date` 匹配（或有明確的跨日期賽事設計）

---

## 15. 審計結論標記 (Audit Conclusion Marker)

```
P24_BACKFILL_PERFORMANCE_STABILITY_AUDIT_DUPLICATE_SOURCE_BLOCKED
```

此標記表示：
- ✅ P24 審計已**成功完成**（非失敗）
- ✅ 重複來源問題已被**正確偵測並報告**
- ✅ 所有 82 個單元測試通過
- ✅ 確定性驗證通過（兩次運行結果完全一致）
- ✅ `paper_only=True`，`production_ready=False` 在所有輸出中強制執行
- ⚠️ P23 回播數據不構成獨立多日回測證據
- ⛔ 閘道狀態：`P24_BLOCKED_DUPLICATE_SOURCE_REPLAY`

**後續階段**：P25 Full Historical Source Separation / True Multi-Date Artifact Builder
