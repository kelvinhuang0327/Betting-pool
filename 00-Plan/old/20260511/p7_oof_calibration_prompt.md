# P7 Out-of-Fold Calibration Validation 任務提示

**前置條件**: P6 完成標記 `P6_REAL_MODEL_BSS_REPAIR_READY` 已確認。

---

## 背景

P6 實作了等寬分箱校準 (`mlb_probability_calibration_repair.py`)，樣本內 BSS 從 -0.0333 改善至 -0.0068（+0.0265），ECE 從 0.0595 降至 0.0004。**但這是樣本內校準**，`calibration_candidate_evaluation.py` 正確標記 `recommendation=KEEP_BLOCKED` 與 `in_sample_warning`。

**P7 任務**：實作 Out-of-Fold (K-Fold) 交叉驗證，確認校準效果在未見資料上的泛化能力，決定是否升級為生產候選。

---

## P7 任務清單

### Task 1: 環境確認
- 確認 Python 環境、pytest 版本、在 `main` 分支
- 確認 P6 artifacts 都存在：
  - `outputs/predictions/PAPER/2026-05-11/calibration_candidate_evaluation.json` → `recommendation=KEEP_BLOCKED`
  - `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_calibrated_probabilities.csv`
  - `00-BettingPlan/20260511/p6_real_model_bss_repair_report.md`

### Task 2: 設計 OOF 驗證邏輯
- 輸入：1,341 個有效行（有 model_prob_home + outcome + market_prob）
- K=5 折（按時間順序分割，**不可隨機打亂** — 防止未來資訊洩漏）
- 每折流程：
  1. 用其餘 K-1 折的資料訓練 bin calibration 映射（呼叫 `calibrate_probabilities_by_bins`）
  2. 將學到的 bin 邊界 + bin 校準值 **套用到** 目標折（不重新訓練）
  3. 計算目標折的 BSS 和 ECE
- 彙整：計算 OOF BSS（加權平均）、OOF ECE（加權平均）、OOF delta_bss vs 原始 BSS

### Task 3: 實作 OOF 驗證模組
建立 `wbc_backend/prediction/mlb_oof_calibration_validator.py`：
```python
def validate_calibration_oof(
    rows: list[dict],
    *,
    model_prob_col: str = "model_prob_home",
    outcome_col: str = "home_win",
    n_folds: int = 5,
    n_bins: int = 10,
    min_bin_size: int = 30,
) -> dict:
    """
    Return:
      - oof_bss: float | None
      - oof_ece: float | None
      - oof_delta_bss: float | None (vs baseline market_brier)
      - original_bss: float | None  (in-sample full data)
      - per_fold_bss: list[float | None]
      - per_fold_ece: list[float | None]
      - n_folds: int
      - n_bins: int
      - usable_rows: int
      - fold_sizes: list[int]
      - recommendation: "PRODUCTION_CANDIDATE" | "KEEP_BLOCKED"
      - recommendation_reason: str
    """
```
- **時間順序分割**：按 Date 欄位升序排列後等分
- **應用 bin 映射**：從訓練折學到 bin 邊界與校準值，套用到測試折（稀疏 bin 仍使用訓練折全局勝率混合）
- `recommendation = "PRODUCTION_CANDIDATE"` 條件：`oof_bss > 0`
- `recommendation = "KEEP_BLOCKED"` 條件：`oof_bss <= 0` 或 `oof_bss is None`

### Task 4: 建立 CLI 腳本
建立 `scripts/run_mlb_oof_calibration_validation.py`：
- `--input-csv`: 輸入 CSV（必須在 `outputs/predictions/PAPER/`）
- `--output-dir`: 輸出目錄（必須在 `outputs/predictions/PAPER/`）
- `--n-folds`: 預設 5
- `--n-bins`: 預設 10
- `--min-bin-size`: 預設 30
- 輸出檔案：
  - `oof_calibration_validation.json`：完整 OOF 結果
  - `p7_oof_validation_summary.md`：人類可讀摘要
- stdout 一行摘要：`oof_bss=X | oof_ece=X | recommendation=X`

### Task 5: 條件性升級邏輯
若 OOF BSS > 0，在 `calibration_candidate_evaluation.json` 旁邊寫入：
- `oof_validation.json`：含 OOF 結果
- 更新 `evaluate_calibration_candidate()` 的 `recommendation`（或建立新函數 `evaluate_with_oof()`）：
  - `PRODUCTION_CANDIDATE`: OOF BSS > 0
  - `KEEP_BLOCKED`: OOF BSS ≤ 0

**注意**：如果升級為 PRODUCTION_CANDIDATE，**仍然不允許真實下注**。這只是研究驗證狀態。

### Task 6: Strategy Simulator 更新
在 `strategy_simulator.py` 的 source_trace 中：
- 若 `oof_bss_validated = True`（通過 OOF）：移除 `calibration_warning` 或改為 `calibration_status = "oof_validated"`
- 若 `oof_bss_validated = False`：保留 `calibration_warning`

### Task 7: 測試
建立 `tests/test_mlb_oof_calibration_validator.py`（≥10 tests）：
1. 按時間排序分割（最早日期在 Fold 0）
2. 5 折後測試集總行數 = 輸入行數
3. 訓練集永遠比測試集早
4. OOF BSS 是 float 或 None
5. 稀疏 bin 不崩潰
6. n_folds=1 應拒絕（raise ValueError）
7. 空輸入返回 KEEP_BLOCKED
8. 行數少於 n_folds*min_bin_size 時發出警告
9. recommendation 為合法值
10. per_fold_bss 列表長度 = n_folds

### Task 8: 執行 OOF 驗證 CLI

```bash
.venv/bin/python scripts/run_mlb_oof_calibration_validation.py \
  --input-csv outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv \
  --output-dir outputs/predictions/PAPER/2026-05-11/ \
  --n-folds 5 \
  --n-bins 10 \
  --min-bin-size 30
```

### Task 9: 決策點
- 若 `oof_bss > 0`：升級為 PRODUCTION_CANDIDATE，產出 `oof_validation.json`，更新 P7 報告
- 若 `oof_bss ≤ 0`：記錄「OOF 驗證失敗，校準無法泛化」，建議 P8 嘗試 Walk-Forward 或更多訓練資料

### Task 10: 最終報告
建立 `00-BettingPlan/20260511/p7_oof_calibration_report.md`，包含：
- OOF 驗證結果（逐折 BSS/ECE）
- 決策：PRODUCTION_CANDIDATE 或 KEEP_BLOCKED
- 後續建議
- 完成標記：`P7_OOF_CALIBRATION_VALIDATION_READY`

### Task 11: P8 提示
若 OOF 通過，P8 應實作：Walk-Forward 驗證（滾動視窗）
若 OOF 未通過，P8 應實作：擴充訓練集或特徵重要性分析，找出偏差根源

---

## 成功標準

| 標準 | 驗收條件 |
|------|---------|
| OOF 按時間分割（無資訊洩漏）| 每折測試集日期均晚於訓練集 |
| OOF BSS 計算正確 | 數值合理（-1 到 1 之間）|
| 稀疏分箱不崩潰 | min_bin_size 混合邏輯正確套用 |
| 所有 P1-P6 測試通過 | ≥216 tests |
| 決策清晰記錄 | 有完整 p7_oof_calibration_report.md |

---

## 重要限制（不可違反）

1. **禁止真實下注** — paper_only=True 永遠不得移除
2. **禁止偽造改善** — OOF BSS 必須真實計算
3. **禁止忽略負面結果** — OOF BSS ≤ 0 時必須如實記錄
4. **時間分割** — 不可使用隨機分割，必須按日期排序
5. **數據隔離** — 校準映射訓練絕不能看到測試折資料

---

**前置完成標記**: `P6_REAL_MODEL_BSS_REPAIR_READY`  
**本任務完成標記**: `P7_OOF_CALIBRATION_VALIDATION_READY`
