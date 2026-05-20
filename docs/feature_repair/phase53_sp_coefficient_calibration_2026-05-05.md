# Phase 53 — SP Feature Coefficient Calibration Audit Report

**日期**: 2026-05-05  
**Phase53 Version**: `phase53_sp_coefficient_calibration_v1`  
**Gate**: `FEATURE_COEFFICIENT_PAPER_ONLY` ✅  
**Safe Coefficient**: 0.25x  
**Audit Hash**: `eb1a0785bc8073a4`

---

## Executive Summary

Phase 52A gate = `FEATURE_REPAIR_NOT_EFFECTIVE`，原因是 `heavy_favorite ECE delta = +0.000425`（輕微惡化）。
本次 Phase 53 對 Phase50/52 的 sp_fip_delta adjustment rule（`tanh(delta * 0.5) * 0.003`）做 offline coefficient calibration audit，
測試 scale multiplier ∈ [0.0, 0.25, 0.5, 0.75, 1.0, 1.25]，
共 6 組係數設定。

**結論**：

- Best by overall BSS: **scale=1.25**  
- Best by heavy_favorite ECE: **scale=0.25**  
- Safe coefficient（滿足全部 7 項條件）: **0.25x**  
- Gate: **`FEATURE_COEFFICIENT_PAPER_ONLY`**

> 所有評估結果均為 `diagnostic_only=True`，不可直接 productionize。
> `CANDIDATE_PATCH_CREATED=False`, `PRODUCTION_MODIFIED=False`

---

## Why Phase 52 Was Not Sufficient

| 指標 | Phase52 (scale=1.00) | Baseline | Delta | 問題 |
|------|---------------------|---------|-------|------|
| overall BSS | 0.021329 | 0.021177 | +0.000152 | ✅ 改善 |
| overall ECE | 0.030328 | 0.031097 | -0.000769 | ✅ 改善 |
| heavy_favorite ECE | — | — | +0.000425 | ❌ **Gate 失敗點** |

**根因分析**：`tanh(delta * 0.5) * 0.003` 在 heavy_favorite 賽事（市場賠率差大）中，
FIP delta 較大，tanh 壓縮效果有限，導致 ECE 輕微惡化。
需測試更保守係數（0.50x / 0.25x）是否可改善 heavy_favorite ECE，
同時維持整體 BSS 不退步。

---

## Coefficient Grid Table

| Scale | Effective Coeff | Adjusted (rows/rate) | Mean Adj | Max Adj | Overall BSS | Overall ECE | HF ECE | HC BSS |
|-------|----------------|---------------------|----------|---------|-------------|-------------|--------|--------|
| 0.00 | 0.000000 | 18 (0.9%) | 0.000003 | 0.001174 | 0.021175 | 0.031098 | 0.084557 | 0.203527 |
| 0.25 | 0.000750 | 1356 (67.0%) | 0.000122 | 0.001174 | 0.021214 | 0.029819 | 0.084472 | 0.203601 |
| 0.50 | 0.001500 | 1356 (67.0%) | 0.000241 | 0.001228 | 0.021253 | 0.030218 | 0.087373 | 0.20828 |
| 0.75 | 0.002250 | 1356 (67.0%) | 0.000360 | 0.001612 | 0.021291 | 0.030915 | 0.085054 | 0.208352 |
| 1.00 | 0.003000 | 1356 (67.0%) | 0.000479 | 0.002149 | 0.021329 | 0.030328 | 0.084977 | 0.208424 |
| 1.25 | 0.003750 | 1356 (67.0%) | 0.000598 | 0.002686 | 0.021367 | 0.029347 | 0.084899 | 0.208495 |

---

## Best Overall Coefficient

Best by overall BSS: **scale=1.25**

---

## Best heavy_favorite-Safe Coefficient

Best by heavy_favorite ECE（最低 ECE）: **scale=0.25**

---

## Safe Coefficient Selection Result

**Gate**: `FEATURE_COEFFICIENT_PAPER_ONLY` ✅  
**Safe coefficient**: 0.25x

**Gate rationale**:
> scale=0.25 滿足全部 7 項安全條件： overall BSS delta=+0.000037, overall ECE delta=-0.001278, heavy_favorite ECE delta=-0.000080（改善或持平）。 adjusted_rate=67.0%, max_abs_adj=0.001174。 本係數為 diagnostic_only，不可直接 productionize。

### 安全條件（7 項需全部滿足）

| 條件 | 要求 | 結果 |
|------|------|------|
| overall BSS >= baseline | ≥ 0.021177 | 詳見 grid table |
| overall ECE <= baseline | ≤ 0.031097 | 詳見 grid table |
| heavy_favorite ECE <= baseline | ≤ baseline HF ECE | **Gate 關鍵條件** |
| high_confidence BSS 不惡化 | ≥ baseline HC BSS - 0.001 | 詳見 grid table |
| month:2025-04 BSS 不惡化 | ≥ baseline Apr BSS - 0.001 | 詳見 grid table |
| adjusted_rate >= 30% | ≥ 30% | 詳見 grid table |
| max_abs_adjustment <= 0.025 | ≤ 0.025 | 詳見 grid table |

---

## Segment Comparison Table (Baseline vs Safe Coefficient / Best Candidate)

> Scale used: 0.25x

| Segment | n | baseline BSS | candidate BSS | delta BSS | baseline ECE | candidate ECE | delta ECE | Label |
|---------|---|-------------|--------------|-----------|-------------|--------------|-----------|-------|
| overall | 2025 | 0.021177 | 0.021214 | +0.000037 | 0.031097 | 0.029819 | -0.001278 | — UNCHANGED |
| month:2025-04 | 53 | 0.113139 | 0.113307 | +0.000168 | 0.199221 | 0.199191 | -0.000030 | — UNCHANGED |
| month:2025-05 | 411 | 0.031910 | 0.031938 | +0.000028 | 0.042167 | 0.042152 | -0.000015 | — UNCHANGED |
| month:2025-06 | 397 | -0.005391 | -0.005316 | +0.000075 | 0.081469 | 0.078969 | -0.002500 | — UNCHANGED |
| month:2025-07 | 369 | 0.007656 | 0.007715 | +0.000059 | 0.032205 | 0.032224 | +0.000019 | — UNCHANGED |
| odds_bucket:heavy_favorite | 268 | 0.195232 | 0.195326 | +0.000094 | 0.084552 | 0.084472 | -0.000080 | — UNCHANGED |
| odds_bucket:mid | 721 | -0.008848 | -0.008828 | +0.000020 | 0.039885 | 0.039873 | -0.000012 | — UNCHANGED |
| confidence:high_confidence | 195 | 0.203570 | 0.203601 | +0.000031 | 0.072027 | 0.072003 | -0.000024 | — UNCHANGED |
| confidence:low_confidence | 1257 | 0.003067 | 0.003098 | +0.000031 | 0.018777 | 0.017993 | -0.000784 | — UNCHANGED |
| disagreement:high | 191 | -0.020780 | -0.018738 | +0.002042 | 0.075902 | 0.070935 | -0.004967 | ✅ IMPROVED |
| disagreement:low | 776 | 0.033032 | 0.031914 | -0.001118 | 0.033450 | 0.031027 | -0.002423 | ❌ DEGRADED |

---

## Gate Recommendation

```
gate = FEATURE_COEFFICIENT_PAPER_ONLY
safe_coefficient = 0.25
best_by_overall_bss = 1.25
best_by_heavy_favorite_ece = 0.25
diagnostic_only = True
candidate_patch_created = False
production_modified = False
```

---

## Limitations

1. **FIP proxy 仍為 historical 估算**（Phase 52 繼承限制）
2. **調整幅度上限 ±0.025**（Phase50 cap 不隨 scale 改變）
3. **評估為 offline / paper-only**：無 live 驗證
4. **scale_grid 為等比間隔**：最佳係數可能在網格點之間
5. **segment 分類固定**：heavy_favorite / high_confidence 定義為 Phase52 一致
6. **`tanh` 函數形式假設不變**：若形式本身有問題，scale 調整無法解決

---

## Next Phase Recommendation

**Phase 54 — Re-run Phase43/44/45 Stability Audit with Safe SP Coefficient**

  使用 safe_coefficient=0.25x 重跑 Phase43/44/45 穩定性審計，確認 SP feature 在各種市場條件下的穩定性。

---

## Hard Rules Verification

| 規則 | 狀態 |
|------|------|
| CANDIDATE_PATCH_CREATED = False | ✅ |
| PRODUCTION_MODIFIED = False | ✅ |
| diagnostic_only = True | ✅ |
| 無 look-ahead leakage | ✅ |
| 無 ensemble / re-training | ✅ |
| gate ≠ PATCH | ✅ |
| paper-only / offline only | ✅ |

---

## Completion Marker

```
PHASE_53_SP_COEFFICIENT_CALIBRATION_VERIFIED
gate=FEATURE_COEFFICIENT_PAPER_ONLY
safe_coefficient=0.25
best_by_overall_bss=1.25
best_by_heavy_favorite_ece=0.25
baseline_n=2025
baseline_bss=0.021177
baseline_ece=0.031097
candidate_patch_created=False
production_modified=False
diagnostic_only=True
```
