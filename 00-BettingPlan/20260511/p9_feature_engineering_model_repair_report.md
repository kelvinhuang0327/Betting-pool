# P9 Feature Engineering & Model Architecture Repair — Final Report

**日期**: 2026-05-11  
**分支**: main  
**Python**: 3.13.8  
**狀態**: ✅ 完成 — `P9_FEATURE_ENGINEERING_MODEL_REPAIR_READY`

---

## 1. P9 目標摘要

P8 診斷發現模型存在以下根本缺陷 (Root Causes)：

| 代號 | 嚴重度 | 問題描述 | P9 處置 |
|------|--------|----------|---------|
| RC-1 | CRITICAL | `home_bias=1.0` 常數特徵 — 人工膨脹主場勝率 | 以 Logit 修正移除 |
| RC-3 | HIGH | 無獨立棒球信號 — 僅市場賠率反推概率 | 新增 bullpen_delta、rest_delta、win_rate_delta |
| RC-4 | MEDIUM | 無穩定 game_id / 無去重機制 | 實作 `build_mlb_game_id()` + `dedupe_mlb_rows()` |
| RC-5 | LOW | 預測-市場聯結 HIGH 風險 | 改為 canonical key 聯結 |

**硬性限制**（全程遵守）：
- `paper_only = True`（永不啟用實際下注）
- `leakage_safe = True`（滾動勝率僅使用賽前歷史）
- 不修改 `mlb_moneyline.py` 現有訓練/預測路徑

---

## 2. 新增/修改模組

### 2.1 `wbc_backend/prediction/mlb_game_key.py`（新增）
提供穩定 game_id 工具與去重邏輯：

- `normalize_mlb_team(value)` — 包裹 P8 `normalize_mlb_team_name()`，支援底線大寫格式
- `build_mlb_game_id(date, home, away)` → `YYYY-MM-DD_HOME_AWAY`
- `parse_context_game_id(context_id)` — 解析 `MLB-YYYY_MM_DD-time-AWAY-AT-HOME` 格式
- `dedupe_mlb_rows(rows)` — 依 game_id 去重，優先保留含 `model_prob_home` 的行

### 2.2 `wbc_backend/prediction/mlb_feature_repair.py`（新增）
保守型特徵修復模組（RC-1 / RC-3 / RC-4 修復核心）：

**Logit 修正公式：**
```
logit_adj = logit(model_prob)
           − bias_correction
           − 0.03 × (bullpen_delta / 3)
           + 0.02 × (rest_delta / 7)
           + 0.05 × win_rate_delta

repaired_prob = sigmoid(logit_adj)
```

**新增特徵欄位（每行）：**
- `game_id`、`raw_model_prob_home`
- `bullpen_usage_last_3d_home/away`、`bullpen_delta`
- `rest_days_home/away`、`rest_delta`
- `recent_win_rate_home/away`、`win_rate_delta`
- `probability_source = "repaired_model_candidate"`
- `repaired_feature_version = "p9_feature_repair_v1"`
- `repaired_home_bias_removed`、`repaired_feature_trace`

### 2.3 `scripts/run_mlb_repaired_model_probability_export.py`（新增）
CLI 工具：套用 P9 特徵修復，輸出 4 種 artifacts。

### 2.4 `wbc_backend/simulation/strategy_simulator.py`（修改）
新增 `repaired_model_candidate` 概率來源追蹤：`repaired_model_row_count`、`repaired_home_bias_removed_count`、`repaired_feature_version_seen`。

---

## 3. Task 8 — 特徵修復輸出 (P5 CSV 全量)

**輸入**: `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv` (2430 行)

| 指標 | 數值 |
|------|------|
| 輸入行數 | 2430 |
| 輸出行數 | 2402 |
| 去重移除 | 28 行 |
| Bullpen join 命中 | 2346 / 2402 (97.7%) |
| Bullpen join 遺漏 | 56 |
| Rest join 命中 | 2281 / 2402 (95.0%) |
| Rest join 遺漏 | 121 |
| **home_bias_logit_correction** | **+0.1969** |
| avg_model_prob_before (RC-1 修復前) | 0.5360 |
| avg_model_prob_after (RC-1 修復後) | 0.4876 |
| leakage_safe | True |
| paper_only | True |

> **P8 對比**：P8 記錄 avg_model_prob=0.566，avg_market_prob=0.518，excess logit ≈ 0.541。  
> P9 實際估計 home_bias_correction=0.1969（在全量 2430 行上重新計算，分佈更廣，修正較小）。

**輸出 artifacts**：
- `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_repaired_features.csv`
- `outputs/predictions/PAPER/2026-05-11/mlb_repaired_model_probabilities.jsonl`
- `outputs/predictions/PAPER/2026-05-11/repaired_feature_metadata.json`
- `outputs/predictions/PAPER/2026-05-11/repaired_probability_summary.md`

---

## 4. Task 9 — OOF 校準結果

**輸入**: `mlb_odds_with_repaired_features.csv` (2402 行)

| 指標 | 修復前 (P8 raw) | 修復後 (P9 raw) | P9 OOF 校準 |
|------|----------------|----------------|-------------|
| BSS | −0.0333 | −0.0580 | **−0.0283** |
| ECE | — | 0.0816 | **0.0352** |
| 有效行數 | 2430 | 2402 | 1949 |
| 推薦狀態 | — | — | `OOF_IMPROVED_BUT_STILL_BLOCKED` |
| 部署狀態 | — | — | `PAPER_ONLY_CANDIDATE` |

> **解讀**：修復後 raw BSS 更差（-0.0580 vs -0.0333），顯示 RC-1 修正後，模型與市場的對齊性更誠實（原始概率膨脹已被揭露）。OOF 校準使 BSS 改善至 -0.0283，但仍為負值，表示模型還無法超越市場基準。ECE 大幅改善（0.082 → 0.035）代表校準一致性顯著提升。

**輸出 artifacts**：
- `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_oof_calibrated_probabilities.csv`
- `outputs/predictions/PAPER/2026-05-11/oof_calibration_evaluation.json`
- `outputs/predictions/PAPER/2026-05-11/oof_calibration_folds.json`
- `outputs/predictions/PAPER/2026-05-11/p7_oof_calibration_summary.md`

---

## 5. Task 10 — 策略模擬結果

**策略名稱**: `moneyline_edge_threshold_v0_p9_repaired_oof`  
**輸入**: `mlb_odds_with_oof_calibrated_probabilities.csv`  
**日期範圍**: 2025-03-01 → 2025-12-31

| 指標 | 數值 |
|------|------|
| n | 1949 |
| 下注數 | 1076 |
| BSS | −0.0283 |
| ECE | 0.0352 |
| ROI | **+0.20%** |
| Gate 狀態 | `BLOCKED_NEGATIVE_BSS` |

> **解讀**：ROI 微幅正值（+0.20%），顯示特徵修復後策略已接近盈虧平衡，但 BSS 尚未達到 ≥0 的部署門檻。

**輸出 artifacts**：
- `outputs/simulation/PAPER/2026-05-11/..._moneyline_edge_threshold_v0_p9_repaired_oof_*.jsonl`
- `outputs/simulation/PAPER/2026-05-11/..._moneyline_edge_threshold_v0_p9_repaired_oof_*_report.md`

---

## 6. Task 11 — 投注建議閘門

**Gate 狀態**: `BLOCKED_NEGATIVE_BSS`（符合預期）  
**allow_recommendation**: False  
**所有建議**: 均為 `gate=BLOCKED_SIMULATION_GATE`  
**paper_only**: True（所有輸出均為模擬，無實際下注）

---

## 7. 測試覆蓋

| 測試文件 | 測試數 | 狀態 |
|----------|--------|------|
| `tests/test_mlb_game_key.py` | 17 | ✅ 全通過 |
| `tests/test_mlb_feature_repair.py` | 38 | ✅ 全通過 |
| `tests/test_run_mlb_repaired_model_probability_export.py` | 12 | ✅ 全通過 |
| 既有 P8/P7/P6 測試套組 | 205 | ✅ 無回歸 |

**總計**: 272 個測試，0 失敗。

---

## 8. P10 計劃建議

P9 修復後的關鍵發現：
1. **BSS 仍為負值**（-0.0283）— 需要更強的獨立特徵或更長的訓練窗口
2. **Bullpen/Rest join 遺漏率** 3-5% — 可改善 context 文件覆蓋率
3. **ROI +0.20%** — 方向正確，需要統計顯著性驗證

**P10 建議方向**：
- 新增球場 ERA 等獨立投手特徵
- 擴大 training window（使用 2023-2025 三年數據）
- 提升 context file join 命中率
- 進行 walk-forward BSS 趨勢分析

---

## 9. 最終標記

```
P9_FEATURE_ENGINEERING_MODEL_REPAIR_READY
```

**所有 P9 artifacts 均為 paper_only=True，leakage_safe=True，不用於實際下注。**
