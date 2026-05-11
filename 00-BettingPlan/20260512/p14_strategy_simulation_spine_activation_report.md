# P14 策略模擬脊柱啟動報告
# P14_STRATEGY_SIMULATION_SPINE_READY

**日期**: 2026-05-12  
**分支**: `p13-clean`  
**狀態**: PAPER_ONLY — production_ready=False  
**前置里程碑**: P13 (BSS=+0.008253, gate_decision=PASS, commit `8e74863`)

---

## 1. 目標摘要

P14 的任務是：以 P13 walk-forward logistic OOF 機率輸出為輸入，
啟動策略模擬脊柱，並透過多個下注策略（Staking Policies）產生
可確定性（Deterministic）、可稽核（Auditable）的 PAPER_ONLY 模擬結果。

> **P14 proves simulation spine activation, not betting profitability.**

---

## 2. P13 輸入證據

| 項目 | 值 |
|------|-----|
| 模型 | `p13_walk_forward_logistic` |
| BSS (OOF) | `+0.008253` |
| Gate Decision | `PASS` |
| OOF CSV 路徑 | `outputs/predictions/PAPER/2026-05-12/p13_walk_forward_logistic/oof_predictions.csv` |
| OOF 樣本數 | 1577 |
| Commit | `8e74863` |

**OOF CSV Schema**: `y_true, p_oof, fold_id, train_window_start, train_window_end, predict_window_start, predict_window_end, source_model, source_bss_oof, paper_only`

---

## 3. 模擬脊柱 Gate 決策

| 欄位 | 值 |
|------|-----|
| `spine_gate` | `MARKET_ODDS_ABSENT_SIMULATION_ONLY` |
| `market_odds_available` | `False` |
| `n_samples` | 1577 |
| `paper_only` | `True` |
| `production_ready` | `False` |

### 為何 Market Odds 缺席？

Walk-forward OOF 只保留 `y_true + p_oof + fold metadata`，不含賽前市場賠率。
這是設計上的正確行為：

- 市場賠率在 OOF 訓練期間並未被模型使用
- P14 的目的是驗證脊柱可消費 P13 的機率輸出並產生確定性結果
- 市場賠率驅動的 Kelly 策略（`capped_kelly`）被正確地阻擋於 `BLOCKED_NO_MARKET_DATA`
- ROI 計算需要市場賠率，`roi_pct=None` 是預期值

---

## 4. 各策略模擬結果

| 策略 | 下注數 | 跳過數 | Gate Status | BSS | ECE | ROI |
|------|--------|--------|-------------|-----|-----|-----|
| `flat` | 739 | 838 | `PAPER_ONLY` | +0.02519 | 0.01709 | None |
| `capped_kelly` | 0 | 1577 | `BLOCKED_NO_MARKET_DATA` | N/A | N/A | None |
| `confidence_rank` | 474 | 1103 | `PAPER_ONLY` | +0.03716 | 0.02875 | None |
| `no_bet` | 0 | 1577 | `PAPER_ONLY` | N/A | N/A | None |

### 策略說明

- **`flat`** (threshold=0.55, stake_fraction=0.02): 純機率閾值篩選，不需市場賠率。739/1577 = 46.9% 下注率。
- **`capped_kelly`** (kelly_cap=0.05): 需要 `decimal_odds`，因缺席而被正確阻擋。
- **`confidence_rank`** (top_n_pct=0.30): 按 `p_oof` 降序排名，取前 30%。474/1577 = 30.1%。BSS 最高 (+0.037)。
- **`no_bet`**: 控制組，零下注，確認跳過計數正確。

---

## 5. Brier Skill Score 說明

```
flat:             BSS = +0.02519 (基準 BSS 0.008253，模擬 subset 的 BSS 為 +0.025)
confidence_rank:  BSS = +0.03716 (取信心最高前 30%，BSS 進一步提升)
```

BSS > 0 代表模型機率優於基準率（climatological mean），符合預期。

---

## 6. 確定性驗證 (Determinism)

執行兩次 CLI，比對 JSON 核心指標與 CSV 帳本：

```
JSON core metrics: IDENTICAL
Ledger rows: 4731, bet decisions differ: 0
```

**結論**: 所有輸出完全確定性，兩次執行的結果逐行相同。

---

## 7. 輸出文件清單

| 文件 | 路徑 |
|------|------|
| 模擬摘要 JSON | `outputs/predictions/PAPER/2026-05-12/p14_strategy_simulation/simulation_summary.json` |
| 模擬摘要 MD | `outputs/predictions/PAPER/2026-05-12/p14_strategy_simulation/simulation_summary.md` |
| 帳本 CSV | `outputs/predictions/PAPER/2026-05-12/p14_strategy_simulation/simulation_ledger.csv` (6308 rows) |

所有輸出均位於 `outputs/predictions/PAPER/` 下，符合 PAPER_ONLY 隔離要求。

---

## 8. 測試覆蓋

| 測試文件 | 測試數 | 結果 |
|----------|--------|------|
| `tests/test_p14_strategy_policies.py` | 30 | ✅ PASS |
| `tests/test_p14_strategy_simulator.py` | 26 | ✅ PASS |
| `tests/test_run_p14_strategy_simulation_spine.py` | 14 | ✅ PASS |
| P13 + 既有模擬測試 (regression) | 169 | ✅ PASS |
| **合計** | **239** | **✅ 全數通過** |

---

## 9. PAPER_ONLY 合規確認

- [x] `paper_only=True` 寫入所有輸出 JSON
- [x] `production_ready=False` 寫入所有輸出 JSON
- [x] 輸出路徑包含 `/PAPER/`
- [x] CLI 以 `--paper-only` 旗標執行
- [x] `PolicyDecision` 強制執行 `paper_only=True`
- [x] 無 push / 無 PR / 無 production 觸發

---

## 10. 新建原始碼文件

| 文件 | 用途 |
|------|------|
| `wbc_backend/simulation/strategy_policies.py` | P14 確定性下注策略函數 |
| `wbc_backend/simulation/p13_strategy_simulator.py` | P14 模擬執行器 |
| `scripts/run_p14_strategy_simulation_spine.py` | P14 CLI 入口 |

| 文件 | 修改原因 |
|------|----------|
| `scripts/run_p13_walk_forward_logistic_oof.py` | 新增 CSV 輸出（P14 輸入所需） |

---

## 11. `strategy_policies.py` 核心設計

```python
REASON_CODES = frozenset({
    "POLICY_SELECTED",
    "BELOW_EDGE_THRESHOLD",
    "MARKET_ODDS_ABSENT",
    "PAPER_ONLY_REQUIRED",
    "INVALID_PROBABILITY",
    "CONTROL_NO_BET",
})

@dataclass(frozen=True)
class PolicyDecision:
    should_bet: bool
    stake_fraction: float
    reason: str        # 必須來自 REASON_CODES
    policy_name: str
```

不變式：
- `reason` 必須在 `REASON_CODES` 中
- `stake_fraction >= 0`
- `should_bet=True` 要求 `stake_fraction > 0`

---

## 12. `p13_strategy_simulator.py` 核心設計

```python
SPINE_GATE_PASS               = "PASS_SIMULATION_SPINE_READY"
SPINE_GATE_MARKET_ABSENT      = "MARKET_ODDS_ABSENT_SIMULATION_ONLY"
SPINE_GATE_INVALID_INPUT      = "FAIL_INVALID_INPUT"
SPINE_GATE_NON_DETERMINISTIC  = "FAIL_NON_DETERMINISTIC"
```

Gate 邏輯：
- 所有列的 `decimal_odds=None` → `MARKET_ODDS_ABSENT_SIMULATION_ONLY`
- 所有列均有 market odds → `PASS_SIMULATION_SPINE_READY`
- 輸入無效 → `FAIL_INVALID_INPUT`

---

## 13. CLI 拒絕條件

CLI (`run_p14_strategy_simulation_spine.py`) 在以下情況拒絕執行：

1. OOF 目錄不存在或缺少必要文件
2. `oof_report.json` 的 `gate_decision != "PASS"`
3. `bss_oof <= 0`
4. 輸出路徑不在 `outputs/predictions/PAPER/` 下
5. 提供無效的策略名稱

---

## 14. 既有失敗測試（P14 前已存在，與 P14 無關）

以下測試在 P14 開始前即已失敗，非 P14 引入：

| 測試文件 | 原因 |
|----------|------|
| `tests/test_institutional_system.py` | `ModuleNotFoundError: wbc_backend.features.knowledge_graph` |
| `tests/test_wbc_data_verification_gate.py` | `ModuleNotFoundError: data.fetch_status` |
| `tests/test_live_wbc_profile_integration.py` | 同上（管線依賴缺失） |
| `tests/test_model_stability_fixes.py` | 同上（管線依賴缺失） |
| `tests/test_orchestrator_mlb_integration.py` | 同上（管線依賴缺失） |
| `tests/test_production_integration.py` | 同上（管線依賴缺失） |

---

## 15. 結論與後續

### 達成目標

✅ P13 OOF 機率成功輸入模擬脊柱  
✅ 4 個策略產生確定性帳本（flat: 739 bets, confidence_rank: 474 bets）  
✅ `capped_kelly` 在市場賠率缺席時被正確阻擋  
✅ 脊柱 gate = `MARKET_ODDS_ABSENT_SIMULATION_ONLY`（設計正確，非錯誤）  
✅ 70 個 P14 單元測試全數通過  
✅ 確定性驗證：兩次執行 4731 行帳本完全相同  
✅ `paper_only=True`, `production_ready=False` 全程強制執行  

### P14 → P15 交接

若要進入 P15（真實賠率下注評估），需要：
1. 取得帶有市場賠率的真實盤口數據（`decimal_odds`, `p_market`）
2. 驗證 `capped_kelly` 策略在有賠率環境下的 BSS 與 ROI
3. 確認 `PASS_SIMULATION_SPINE_READY` gate 可達成
4. 累積足夠樣本（≥1500）通過統計顯著性門檻

> **P14 里程碑**: 模擬脊柱已啟動，可確定性地消費 P13 正 BSS 機率，  
> 並在 PAPER_ONLY 環境下產生多策略下注帳本。下一步需引入市場賠率數據。

---

*報告生成於 P14 Task 10 | 分支: `p13-clean` | PAPER_ONLY | production_ready=False*
