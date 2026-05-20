# Phase 49 — Feature Repair Evaluation Report

**報告日期**: 2026-05-05  
**Run ID**: `95de9c21-7dc5-4df6-a814-597c8892482b`  
**Generated at**: 2026-05-05T04:30:46.077569+00:00  

---

## Executive Summary

Phase 49 重新執行 evaluation pipeline，比較 baseline JSONL 與 Phase48 P0 feature 增強版 JSONL。

| 項目 | 值 |
|---|---|
| **feature_effect_mode** | `REPORT_ONLY` |
| **gate_recommendation** | `FEATURE_INJECTION_REQUIRED` |
| baseline rows | 2,025 |
| phase48 rows | 2,025 |
| candidate_patch_created | `False` |
| production_modified | `False` |

---

## Feature Effect Mode

> **REPORT_ONLY**: Phase48 P0 features are present in JSONL but not yet injected into model prediction path. Metric deltas are expected to be zero or not attributable. Next required phase is model feature injection.

**結論**: `phase48.model_home_prob` 與 `baseline.model_home_prob` 完全相同（差值 = 0）。
P0 features 已掛載於 JSONL 的 `p0_features` 欄位，但尚未進入 prediction model 的計算路徑。
所有 metric delta 均為 **0（設計如此，非 bug）**。

**Gate rationale**: feature_effect_mode=REPORT_ONLY: Phase48 model_home_prob is identical to baseline, confirming P0 features are NOT yet injected into the prediction model. Metric deltas are zero by construction. Next required action: Phase 50 Feature Injection into Backtest Model.

---

## Baseline vs Phase48 Metrics

| Source | N | Brier | BSS vs Market | ECE | Log Loss |
|---|---|---|---|---|---|
| Baseline | 2,025 | 0.244706 | -0.003894 | 0.031097 | 0.682205 |
| Phase48  | 2,025 | 0.244706 | -0.003894 | 0.031097 | 0.682205 |
| **Delta** | — | +0.000000 | +0.000000 | +0.000000 | +0.000000 |

---

## Critical Segment Comparison

| Segment | N | Baseline BSS | Phase48 BSS | Δ BSS | Baseline ECE | Phase48 ECE | Δ ECE | Label |
|---|---|---|---|---|---|---|---|---|
| `month:2025-04` | 53 | -0.0688 | -0.0688 | +0.0000 | 0.1992 | 0.1992 | +0.0000 | UNCHANGED |
| `month:2025-05` | 411 | +0.0077 | +0.0077 | +0.0000 | 0.0422 | 0.0422 | +0.0000 | UNCHANGED |
| `month:2025-06` | 397 | -0.0277 | -0.0277 | +0.0000 | 0.0815 | 0.0815 | +0.0000 | UNCHANGED |
| `month:2025-07` | 369 | +0.0125 | +0.0125 | +0.0000 | 0.0322 | 0.0322 | +0.0000 | UNCHANGED |
| `odds_bucket:heavy_favorite` | 211 | -0.0159 | -0.0159 | +0.0000 | 0.0893 | 0.0893 | +0.0000 | UNCHANGED |
| `odds_bucket:mid` | 1407 | -0.0017 | -0.0017 | +0.0000 | 0.0446 | 0.0446 | +0.0000 | UNCHANGED |
| `confidence:high_confidence` | 531 | -0.0180 | -0.0180 | +0.0000 | 0.0173 | 0.0173 | +0.0000 | UNCHANGED |
| `confidence:low_confidence` | 848 | +0.0028 | +0.0028 | +0.0000 | 0.0210 | 0.0210 | +0.0000 | UNCHANGED |
| `disagreement:high` | 193 | -0.0389 | -0.0389 | +0.0000 | 0.0759 | 0.0759 | +0.0000 | UNCHANGED |
| `disagreement:low` | 1176 | +0.0002 | +0.0002 | +0.0000 | 0.0323 | 0.0323 | +0.0000 | UNCHANGED |

---

## Feature Availability Summary

| Feature | 可用筆數 | 可用率 | 狀態 |
|---|---|---|---|
| park_run_factor (F-002) | 2,025/2,025 | 100.0% | ✅ 全量可用 |
| season_game_index (F-004) | 2,025/2,025 | 100.0% | ✅ 全量可用 |
| sp_fip_delta (F-001) | 0/2,025 | 0.0% | ⚠️ Neutral fallback（無 FIP context） |
| feature_audit_hash | 2,025/2,025 | 100.0% | ✅ |

**Feature Availability Label**: `FEATURE_READY_FOR_INJECTION`

---

## Leakage Guard Summary

| 指標 | 值 |
|---|---|
| 觸發 leakage guard 的行數 | 2,025/2,025 (100.0%) |
| 最常見被攔截欄位 | `home_win` |
| feature_audit_hash 穩定 | `True` |
| 備注 | 'home_win' intercepted in 2025 rows; zero feature impact confirmed. |

---

## Gate Recommendation

**`FEATURE_INJECTION_REQUIRED`**

> feature_effect_mode=REPORT_ONLY: Phase48 model_home_prob is identical to baseline, confirming P0 features are NOT yet injected into the prediction model. Metric deltas are zero by construction. Next required action: Phase 50 Feature Injection into Backtest Model.

---

## Next Phase Recommendation

**Phase 50 — Feature Injection into Backtest Model**

目標：將 Phase48 P0 features (`park_run_factor`, `season_game_index`) 注入 backtest model 的特徵向量，重新訓練或微調 model，使 `model_home_prob` 受 P0 features 影響。

成功標準：
- `feature_effect_mode = MODEL_AFFECTING`
- 2025-04 BSS > −1%
- heavy_favorite ECE < 0.060
- high_confidence BSS ≥ 0
- overall BSS > baseline

---

## 不變量驗證

| 規則 | 狀態 |
|---|---|
| `candidate_patch_created = False` | ✅ |
| `production_modified = False` | ✅ |
| alpha = 0.4（未調整）| ✅ |
| 無外部 API / LLM 呼叫 | ✅ |
| gate ∈ valid set | ✅ (`FEATURE_INJECTION_REQUIRED`) |
| feature_effect_mode 正確偵測 | ✅ (`REPORT_ONLY`) |

---

## 驗證標記

```
PHASE_49_FEATURE_REPAIR_EVALUATION_VERIFIED
feature_effect_mode=REPORT_ONLY
gate=FEATURE_INJECTION_REQUIRED
baseline_n=2025
phase48_n=2025
delta_bss=+0.000000
park_availability=100.0%
season_idx_availability=100.0%
sp_fip_availability=0.0%
leakage_triggered=2025/2025
candidate_patch_created=False
production_modified=False
```