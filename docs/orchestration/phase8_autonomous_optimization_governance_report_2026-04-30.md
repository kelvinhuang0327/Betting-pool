# Phase 8 — Autonomous Optimization Governance
**報告日期**: 2026-04-30  
**成功標記**: `PHASE_8_AUTONOMOUS_OPTIMIZATION_GOVERNANCE_VERIFIED`  
**測試結果**: 38/38 passed（+ Phase 7 回歸 30/30 passed）

---

## 目標

防止 scheduler 在錯誤時間點生成錯誤類型任務——特別是在 CLV 數據尚未成熟（PENDING_CLOSING）時，阻止學習型任務（strategy-reinforcement、model-validation、model-patch、feedback）被排程執行，避免向模型注入雜訊或錯誤信號。

---

## 核心實作（7 Tasks）

### Task 1 — `orchestrator/optimization_state.py`（新建）

六狀態分類器，讀取實際系統狀態後分類並回傳允許 / 封鎖的任務 family 清單。

**六個狀態（優先順序高→低）**：

| 優先 | 狀態 | 觸發條件 |
|------|------|----------|
| 1 | `SYSTEM_RELIABILITY_ISSUE` | daemon 心跳超過 90 分鐘、連續 SKIPPED、缺少 strategy_state.json |
| 2 | `DATA_WAITING` | COMPUTED CLV < 10% 或 < 1 筆 |
| 3 | `OPERATOR_UX_GAP` | Decision card 缺少 phase6/phase7 區塊 |
| 4 | `MODEL_WEAKNESS_DETECTED` | avg_clv < -0.010 或 Brier > 0.28 |
| 5 | `ARCHITECTURE_DEBT` | wiki 重複模組 ≥ 2 或 cleanup 未解項目 ≥ 3 |
| 6 | `DATA_READY` | 正常狀態，所有 family 允許 |

**核心封鎖規則**：

| 狀態 | 封鎖的 families |
|------|----------------|
| `DATA_WAITING` | strategy-reinforcement, model-validation-atomic, model-patch-atomic, feedback-atomic |
| `SYSTEM_RELIABILITY_ISSUE` | model-patch-atomic, model-validation-atomic, strategy-reinforcement, feedback-atomic, calibration-atomic, feature-atomic |
| `MODEL_WEAKNESS_DETECTED` | strategy-reinforcement |
| `DATA_READY` | （無封鎖） |

**Convenience helpers**：
- `is_task_family_blocked(family, state_result)` → `bool`
- `is_task_family_allowed(family, state_result)` → `bool`

### Task 2 + 3 — `orchestrator/planner_tick.py`（修改）

在 `run_planner_tick()` 中插入 **STEP 1.5**，位於 STEP 1（blocker resolution）之後、STEP 2（候選列表建立）之前：

```python
# ── STEP 1.5: Phase 8 Optimization Governance ─────────────────────
opt_state_result = optimization_state.classify()
_opt_blocked = opt_state_result.get("blocked_task_families", [])
```

在候選迴圈（`for candidate in all_candidates`）最前端加入 governance gate，排在去重檢查之前：

```python
if opt_state_result:
    if optimization_state.is_task_family_blocked(candidate_family, opt_state_result):
        governance_rejection_count += 1
        logger.info("Governance BLOCKED ...")
        continue
```

成功 return dict 新增 `optimization_state` 與 `governance_rejection_count` 欄位。

### Task 4 — `scripts/ops_decision_card.py`（修改）

新增 `compute_phase8_status(partial_payload=None)` 函數，在 `build_payload()` 中傳入已計算的 phase6/phase7 資料（避免遞迴）。Decision card render 新增 Phase 8 治理區塊，顯示：
- Optimization state
- Recommended action
- Allowed / Blocked families
- Governance reasons

### Task 5 — `orchestrator/training_memory.py`（修改）

新增兩個函數：

- `record_optimization_state_transition(new_state, reasons, previous_state)` — 記錄狀態轉換（自動去重連續相同狀態），最多保留 200 筆
- `get_optimization_state_transitions(n=20)` — 讀取最近 n 筆轉換歷史

**硬性保證**：絕不碰 `consecutive_successes` / `consecutive_failures`，不影響難度調整。

### Task 6 — `tests/test_phase8_optimization_governance.py`（新建）

8 個 scenario 類別，38 個測試 + 1 個成功標記：

| Scenario | 測試重點 |
|----------|---------|
| 1 | DATA_WAITING：全 PENDING → 正確狀態 + 封鎖正確 |
| 2 | DATA_READY：足夠 COMPUTED → 所有 family 允許 |
| 3 | MODEL_WEAKNESS：avg_clv < -0.010 → 封鎖 strategy-reinforcement |
| 4 | SYSTEM_RELIABILITY：stale heartbeat / 缺檔案 → 封鎖 model 任務 |
| 5 | ARCHITECTURE_DEBT：cleanup 項目 ≥ 3 / 重複模組 → 偵測 |
| 6 | OPERATOR_UX_GAP：payload 缺少 phase6/phase7 → 偵測 |
| 7 | Planner gate：DATA_WAITING 封鎖 strategy-reinforcement |
| 8 | Planner gate：DATA_READY 允許 model-validation |

---

## 關鍵 Bug 修復：無窮遞迴

**問題**：`_check_operator_ux_gap(None)` 原設計是在沒有 payload 時自動呼叫 `build_payload()`，但 `build_payload()` → `compute_phase8_status()` → `classify()` → `_check_operator_ux_gap(None)` → 形成無窮迴圈，耗盡 C-stack 後觸發 SIGABRT。

**修復**：
1. `_check_operator_ux_gap(None)` → 直接回傳 `{"gap_detected": False, "reasons": []}` (no-op)
2. `compute_phase8_status(partial_payload=None)` → 傳入 partial_payload 給 `classify()`
3. `build_payload()` → 先計算 phase6/phase7，再以 `partial_payload={"phase6": ..., "phase7": ...}` 傳入 `compute_phase8_status()`

---

## 硬性保護規則（永不鬆動）

1. **DATA_WAITING 必定封鎖** strategy-reinforcement、model-validation-atomic、model-patch-atomic、feedback-atomic
2. **不允許從 PENDING_CLOSING 學習**（Phase 6 / 7 gate 不受影響）
3. **不停用 quality gate**（governance gate 排在 quality gate 之前）
4. **不偽造 COMPUTED CLV**
5. **不修改即時投注執行邏輯**
6. **state transition 記錄絕不影響 consecutive_successes / consecutive_failures**

---

## 測試通過總覽

```
tests/test_phase8_optimization_governance.py  38/38 passed
tests/test_phase7_closing_to_learning.py       30/30 passed  (regression)
```

**`PHASE_8_AUTONOMOUS_OPTIMIZATION_GOVERNANCE_VERIFIED`**
