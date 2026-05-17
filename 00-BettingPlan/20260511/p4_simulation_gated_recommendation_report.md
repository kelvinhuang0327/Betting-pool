# P4 Simulation-Gated Recommendation — 交付報告

**任務代號**: P4_SIMULATION_GATED_RECOMMENDATION  
**日期**: 2026-05-11  
**Branch**: main  
**報告版本**: v1.0  
**最終標記**: `P4_SIMULATION_GATED_RECOMMENDATION_READY`

---

## 1. 執行摘要

P4 目標：將 P3 模擬骨幹 (simulation spine) 接回 P2 的 MLB→TSL 紙本建議流程，加入「模擬品質閘門」，確保建議只在模擬統計驗證通過後才被允許。

**交付成果**:
| 交付項 | 狀態 |
|--------|------|
| `wbc_backend/simulation/simulation_result_loader.py` | ✅ 完成 |
| `scripts/run_mlb_tsl_paper_recommendation.py` 更新（閘門整合）| ✅ 完成 |
| `wbc_backend/recommendation/recommendation_row.py` 新增兩個 gate status | ✅ 完成 |
| `tests/test_simulation_result_loader.py` (16 tests) | ✅ 36 passed |
| `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py` (20 tests) | ✅ 36 passed |
| 真實模擬閘門建議產出物 | ✅ 完成 |

**P1/P2/P3 回歸**: 102/102 passed ✅

---

## 2. 核心設計決策

### 2.1 閘門優先順序

模擬閘門在 TSL 來源閘門 **之前** 檢查，但 TSL 403 封鎖仍然能覆蓋模擬 PASS：

```
模擬閘門 (BLOCKED?) → yes → BLOCKED_SIMULATION_GATE / BLOCKED_NO_SIMULATION
       ↓ no
TSL 來源閘門 (BLOCKED?) → yes → BLOCKED_TSL_SOURCE
       ↓ no
邊緣/Kelly 閘門 → BLOCKED_EDGE_NEGATIVE / BLOCKED_KELLY_ZERO
       ↓ pass all
PASS (stake > 0)
```

**重要不變量**: `paper_only=True` 在所有輸出中永遠為 `True`。

### 2.2 BSS=0 (市場代理) 模式

本次運行的模擬使用市場隱含概率作為模型概率代理（因 CSV 中無 `model_prob_home` 欄位）。BSS 由構造決定為 ~0，但閘門仍顯示 PASS，並在 `source_trace` 中加入明確警告：

```json
"simulation_model_prob_note": "WARNING: model_prob_home column not found — 
  using market implied prob as proxy. BSS will be ~0 by construction. 
  Do not interpret as model skill."
```

### 2.3 封鎖但仍寫入審計行

即使模擬閘門封鎖，系統仍會寫入一個 `stake=0.0`、`kelly=0.0` 的審計行，而非不產生輸出。這確保：
- 完整的稽核軌跡
- 下游管線可偵測「封鎖但嘗試過」的狀態

### 2.4 `--allow-missing-simulation-gate` 旗標

當開發環境中尚無模擬結果時，可用此旗標繞過「找不到模擬」的封鎖。僅允許在 `simulation is None` 時使用。

---

## 3. 新增檔案

### 3.1 `wbc_backend/simulation/simulation_result_loader.py`

**功能**:
- `load_simulation_result_from_jsonl(path)` — 從 PAPER JSONL 載入 `StrategySimulationResult`，拒絕非 PAPER 路徑和 `paper_only=False`
- `load_latest_simulation_result(simulation_dir, strategy_name)` — 在 PAPER 區遞迴搜尋最新結果，可依 `strategy_name` 篩選
- `_assert_paper_path(path)` — 安全檢查：`"outputs/simulation/PAPER" in resolved.as_posix()`

**安全設計**: 使用字串包含檢查而非 `Path.relative_to()`，允許 pytest `tmp_path` 測試正常運作，同時在生產路徑上阻擋非 PAPER 路徑。

### 3.2 `recommendation_row.py` 新增兩個閘門狀態

```python
VALID_GATE_STATUSES = frozenset({
    "PASS",
    "BLOCKED_BRIER", "BLOCKED_ECE", "BLOCKED_PAPER_ONLY",
    "BLOCKED_TSL_SOURCE", "BLOCKED_MLB_SOURCE", "BLOCKED_MODEL_VERSION",
    "BLOCKED_KELLY_ZERO", "BLOCKED_EDGE_NEGATIVE",
    "BLOCKED_SIMULATION_GATE",   # ← P4 新增
    "BLOCKED_NO_SIMULATION",     # ← P4 新增
})
```

---

## 4. 修改檔案

### 4.1 `scripts/run_mlb_tsl_paper_recommendation.py`

**新增 CLI 參數**:
```
--simulation-result-path PATH       明確指定模擬 JSONL 路徑
--simulation-strategy-name NAME     自動搜尋時的策略名稱篩選（預設: moneyline_edge_threshold_v0）
--require-simulation-gate / --no-require-simulation-gate
--allow-missing-simulation-gate     找不到模擬時允許繼續
```

**新增 imports**:
```python
from wbc_backend.recommendation.recommendation_gate_policy import (
    build_recommendation_gate_from_simulation,
)
from wbc_backend.simulation.simulation_result_loader import (
    load_latest_simulation_result,
    load_simulation_result_from_jsonl,
)
```

**`build_recommendation()` 簽名更新**:
```python
def build_recommendation(
    game: dict,
    date_str: str,
    tsl_live: bool,
    tsl_note: str,
    simulation_gate: dict | None = None,
) -> MlbTslRecommendationRow:
```

---

## 5. 真實模擬閘門建議產出物

**執行指令**:
```bash
.venv/bin/python scripts/run_mlb_tsl_paper_recommendation.py \
  --date 2026-05-11 \
  --simulation-strategy-name moneyline_edge_threshold_v0 \
  --allow-replay-paper
```

**執行輸出**:
```
[SIM-GATE] simulation_gate=LOADED_LATEST(strategy=moneyline_edge_threshold_v0) | gate_status=PASS | allow_recommendation=True
[PAPER-ONLY] LIVE | 2026-05-11-LAA-CLE-824441 | home_prob=0.5403 | market=moneyline | side=home | odds=1.8886 | edge=0.0108 | kelly=0.0000 | stake=0.0u | gate=BLOCKED_TSL_SOURCE | output=...
```

**產出物路徑**: `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

**產出物摘要**:
| 欄位 | 值 |
|------|----|
| `game_id` | `2026-05-11-LAA-CLE-824441` |
| `gate_status` | `BLOCKED_TSL_SOURCE` |
| `paper_only` | `true` |
| `stake_units_paper` | `0.0` |
| `kelly_fraction` | `0.0` |
| `simulation_gate_status` (source_trace) | `PASS` |
| `simulation_id` (source_trace) | `sim-moneyline_edge_threshold-f8695fec` |
| `simulation_allow_recommendation` | `true` |

**驗證**: 模擬閘門載入並通過 (`PASS`)。TSL 403 封鎖仍正確覆蓋為 `BLOCKED_TSL_SOURCE`。`paper_only=true` 不變量保持。

---

## 6. 測試結果

### P4 新增測試

```
tests/test_simulation_result_loader.py          16 tests
tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py  20 tests
─────────────────────────────────────────────────────
合計: 36 passed in 7.96s
```

**測試涵蓋**:
- 從 JSONL 載入有效模擬結果
- 拒絕非 PAPER 路徑 (`ValueError`)
- 拒絕 `paper_only=False`（`ValueError`）
- 拒絕格式錯誤的 JSON
- 按 `generated_at_utc` 選擇最新結果
- 按 `strategy_name` 篩選
- 空目錄返回 `None`
- 模擬 PASS 允許建議路徑（但 TSL 仍封鎖）
- 模擬封鎖 (`BLOCKED_NEGATIVE_BSS`, `BLOCKED_HIGH_ECE`, `BLOCKED_LOW_SAMPLE`) 強制 `stake=0`, `kelly=0`
- `BLOCKED_NO_SIMULATION` 封鎖缺少模擬的建議
- TSL 封鎖優先於模擬 PASS
- `source_trace` 包含 `simulation_id` 和 `simulation_gate_status`
- `paper_only=True` 不變量 (all gates)
- `--allow-missing-simulation-gate` 繞過缺失模擬

### P1/P2/P3 回歸測試

```
tests/test_recommendation_row_contract.py
tests/test_run_mlb_tsl_paper_recommendation_smoke.py
tests/test_strategy_simulation_result_contract.py
tests/test_strategy_simulator_spine.py
tests/test_run_mlb_strategy_simulation_spine.py
tests/test_recommendation_gate_policy.py
─────────────────────────────────────────────────────
合計: 102 passed in 1.17s
```

**全回歸**: 0 failures, 0 errors ✅

---

## 7. 閘門決策邏輯

### `build_recommendation_gate_from_simulation()` 返回結構

```python
{
    "allow_recommendation": bool,
    "gate_status": str,  # "PASS" | "BLOCKED_*"
    "gate_reasons": list[str],
    "simulation_id": str | None,
    "paper_only": bool,
}
```

### 狀態映射

| 模擬 `gate_status` | `allow_recommendation` | 建議 `gate_status` |
|---------------------|------------------------|--------------------|
| `PASS` | `True` | 繼續（由 TSL/Kelly 閘門決定）|
| `BLOCKED_NEGATIVE_BSS` | `False` | `BLOCKED_SIMULATION_GATE` |
| `BLOCKED_HIGH_ECE` | `False` | `BLOCKED_SIMULATION_GATE` |
| `BLOCKED_LOW_SAMPLE` | `False` | `BLOCKED_SIMULATION_GATE` |
| `BLOCKED_NO_MARKET_DATA` | `False` | `BLOCKED_SIMULATION_GATE` |
| `BLOCKED_NO_RESULTS` | `False` | `BLOCKED_SIMULATION_GATE` |
| `None` (無模擬) | `False` | `BLOCKED_NO_SIMULATION` |

---

## 8. 已知限制

| 限制 | 描述 |
|------|------|
| BSS=0 (市場代理) | CSV 無 `model_prob_home` 欄位，模擬使用市場隱含概率代理。BSS 由構造為 ~0，不代表模型技能。 |
| TSL 403 封鎖 | 台灣運彩仍返回 403，導致 TSL 來源閘門封鎖。建議仍寫入審計行，`stake=0`。 |
| 模擬緩存 | 每次執行重新搜尋最新模擬結果，無快取機制。大量模擬文件時可能變慢。 |

---

## 9. 安全注意事項

- `paper_only=True` 在所有代碼路徑中硬式編碼
- 非 PAPER 路徑在 loader 和 CLI 中雙重拒絕
- 不涉及任何真實下注、生產 API 或資金操作

---

## 10. 流水線狀態

```
P1 (MLB 數據管線)           ✅ COMPLETE
P2 (MLB→TSL 建議)          ✅ COMPLETE
P3 (模擬骨幹)              ✅ COMPLETE
P4 (模擬閘門建議)          ✅ COMPLETE ← 本報告
P5 (模型概率預測) → 待開始
```

---

## 11. P5 預覽

P5 目標：移除市場代理模擬限制，生產真實的每場比賽 `model_prob_home` 預測。

**關鍵任務**:
1. 在 `models/` 中建立真實 MLB 勝率預測模型（輸出 `model_prob_home`）
2. 更新 simulation spine CSV 以包含 `model_prob_home` 欄位
3. 驗證模型輸出合約（`0 < prob < 1`，樣本數 >= 1500）
4. 重新運行模擬，驗證 BSS > 0（真實模型技能驗證）
5. 將預測登記行連接至模擬骨幹

---

## 12. 完成標記

```
P4_SIMULATION_GATED_RECOMMENDATION_READY
```

**所有代碼路徑均為 PAPER-ONLY。未進行任何真實下注、生產 API 呼叫或資金操作。**

---

*報告生成: 2026-05-11 | 作者: MLB AI Quant Research Platform*
