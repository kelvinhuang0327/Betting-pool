# Phase 52A — Starting Pitcher Backfill Real Run Verification Report

**日期**: 2026-05-05  
**Feature Version**: `phase52_sp_injected_v1`  
**Gate**: `FEATURE_REPAIR_NOT_EFFECTIVE`  
**執行者**: Automated pipeline (paper-only, offline)

---

## Executive Summary

Phase 52A 為 Phase 52 的真實資料執行驗證補件。使用 MLB 2025 賽季全部 2,025 場比賽，完整執行先發投手 FIP 特徵 backfill pipeline，從 sp_fip_delta 可用率 0%（Phase 50 neutral_fallback）提升至 **100%**。

模型調整率從 Phase 50 的 **0.89%** 大幅提升至 **66.96%**，sp_fip_delta 成功觸發 **1,347 場**注入。整體指標方向一致改善（BSS ↑、Brier ↓、ECE ↓），但幅度細小，且 `heavy_favorite` 桶 ECE 輕微惡化（+0.000425），未達 `FEATURE_REPAIR_EFFECTIVE_PAPER_ONLY` 的全部標準。

**Gate = `FEATURE_REPAIR_NOT_EFFECTIVE`**  
建議：Phase 53 = SP 特徵係數 / 調整幅度校準審計（adjustment coefficient calibration audit）

---

## Phase 52 Pipeline Files

| 檔案 | 狀態 | 行數 |
|------|------|------|
| `data/mlb_sp_data_loader.py` | ✅ 存在 | — |
| `wbc_backend/features/mlb_sp_stat_snapshot.py` | ✅ 存在 | — |
| `wbc_backend/features/mlb_pit_validator.py` | ✅ 存在 | — |
| `scripts/run_phase52_sp_backfill.py` | ✅ 存在 | — |
| `scripts/run_phase52_inject_sp_to_phase48.py` | ✅ 存在 | — |
| `scripts/run_phase52_sp_feature_injection.py` | ✅ 存在 | — |
| `data/mlb_2025/derived/mlb_2025_starting_pitcher_features_phase52.jsonl` | ✅ 產出 | 2,025 |
| `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase52_sp_context_v1.jsonl` | ✅ 產出 | 2,025 |
| `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase52_sp_injected_v1.jsonl` | ✅ 產出 | 2,025 |

---

## SP Backfill Statistics

| 指標 | 數值 | 成功門檻 | 狀態 |
|------|------|----------|------|
| total_rows | 2,025 | = 2,025 | ✅ |
| matched_rows | 2,025 | — | ✅ |
| match_rate | **100.0%** | 100% | ✅ |
| home_starter_present | 2,025 (100.0%) | — | ✅ |
| away_starter_present | 2,025 (100.0%) | — | ✅ |
| unique_starters | **354** | — | ✅ |
| sp_fip_delta_available | 2,025 (100.0%) | ≥ 80% | ✅ |
| historical_proxy | 414 (20.4%) | — | ✅ |
| league_avg_fallback | 597 (29.5%) | — | ✅ |
| mixed_source | 1,014 (50.1%) | — | ✅ |
| point_in_time_safe | 2,025 (100.0%) | 100% | ✅ |
| audit_hash_present | 2,025 (100.0%) | 100% | ✅ |
| fip_delta_nonzero | 1,347 (66.5%) | — | ✅ |
| fip_delta_mean | 0.0084 | — | — |
| fip_delta_min / max | −1.80 / +1.70 | — | — |

> **stat_source 分解**：
> - `historical_proxy` (兩投手皆已知): 414 場 (20.4%)
> - `league_average_fallback` (兩投手均未知): 597 場 (29.5%)  
> - `mixed` (一已知一未知): 1,014 場 (50.1%)

---

## Point-in-Time Validation Summary

| 規則 | 結果 |
|------|------|
| snapshot_date < game_date (嚴格小於) | ✅ 全部 2,025/2,025 |
| 無 forbidden fields（home_win 等 10 項）| ✅ 全部通過 |
| point_in_time_safe 旗標 = True | ✅ 全部 2,025/2,025 |
| audit_hash 存在且非空 | ✅ 全部 2,025/2,025 |
| **safe_rate** | **100.0%** |

---

## Context Injection Summary (Phase48 → Phase52 SP Context)

| 指標 | 數值 | 狀態 |
|------|------|------|
| context_total | 2,025 | ✅ |
| sp_fip_delta_available | 2,025 (100.0%) | ✅ |
| feature_version = `phase52_sp_context_v1` | 2,025 (100.0%) | ✅ |
| sp_context_source 存在 | 2,025 (100.0%) | ✅ |
| sp_context_audit_hash 存在 | 2,025 (100.0%) | ✅ |
| park_run_factor 保留 | 2,025 (100.0%) | ✅ |
| season_game_index 保留 | 2,025 (100.0%) | ✅ |
| home_win 未修改 | ✅ (immutable field guard) | ✅ |
| market_home_prob_no_vig 未修改 | ✅ (immutable field guard) | ✅ |
| inject_rate | 100.0% | ✅ |
| fip_delta_nonzero_rate | 66.5% | ✅ |

---

## Model-Affecting Injection Summary (Phase52 SP Feature Injection)

| 指標 | 數值 | 成功條件 | 狀態 |
|------|------|----------|------|
| feature_effect_mode | `MODEL_AFFECTING` | = MODEL_AFFECTING | ✅ |
| rows_total | 2,025 | — | ✅ |
| rows_adjusted | **1,356** | — | ✅ |
| rows_unchanged | 669 | — | — |
| adjusted_rate | **66.96%** | >> Phase50 0.89% | ✅ |
| mean_abs_adjustment | 0.000479 | — | — |
| max_abs_adjustment | 0.002149 | — | — |
| original_adjusted_correlation | 0.999963 | — | — |
| sp_fip_triggered | **1,347** | — | ✅ |
| park_factor_triggered | 18 | — | — |
| early_season_triggered | 0 | — | — |
| cap_applied_count | 0 | — | ✅ |
| candidate_patch_created | `False` | = False | ✅ |
| production_modified | `False` | = False | ✅ |

> **重大改善**：adjusted_rate 從 Phase50 的 0.89% 提升至 **66.96%**（+66.07pp），sp_fip 觸發 1,347 場，符合 Phase 52 設計目標。

---

## Baseline vs Phase52 Overall Metric Table

| Metric | Baseline | Phase52 | Delta | 方向 |
|--------|----------|---------|-------|------|
| n | 2,025 | 2,025 | 0 | — |
| Brier Score | 0.244706 | 0.244668 | **−0.000038** | ✅ ↓ |
| BSS | 0.021177 | 0.021329 | **+0.000152** | ✅ ↑ |
| ECE | 0.031097 | 0.030328 | **−0.000769** | ✅ ↓ |
| Log Loss | 0.682205 | 0.682126 | **−0.000079** | ✅ ↓ |

> 所有整體指標方向一致改善，但改善幅度細小（BSS +0.015%）。

---

## Critical Segment Delta Table

| Segment | n | baseline_bss | phase52_bss | delta_bss | baseline_ece | phase52_ece | delta_ece | 判斷 |
|---------|---|-------------|-------------|-----------|-------------|-------------|-----------|------|
| month:2025-04 | 53 | 0.113139 | 0.113810 | **+0.000671** | 0.199221 | 0.199101 | −0.000120 | ✅ 改善 |
| month:2025-05 | 411 | 0.031910 | 0.032004 | +0.000094 | 0.042167 | 0.041024 | −0.001143 | ✅ 改善 |
| month:2025-06 | 397 | −0.005391 | −0.005093 | +0.000298 | 0.081469 | 0.079028 | −0.002441 | ✅ 改善 |
| month:2025-07 | 369 | 0.007656 | 0.007951 | +0.000295 | 0.032205 | 0.033907 | **+0.001702** | ⚠️ ECE 輕微惡化 |
| odds_bucket:heavy_favorite | 268 | 0.195232 | 0.195695 | **+0.000463** | 0.084552 | 0.084977 | **+0.000425** | ⚠️ BSS ↑ ECE ↑ |
| odds_bucket:mid | 721 | −0.008848 | −0.008774 | +0.000074 | 0.039885 | 0.041225 | +0.001340 | ⚠️ ECE 略惡化 |
| confidence:high_confidence | 195/194 | 0.203570 | 0.208424 | **+0.004854** | 0.072027 | 0.076685 | +0.004658 | ⚠️ BSS ↑↑ ECE ↑ |
| confidence:low_confidence | 1,257/1,256 | 0.003067 | 0.003468 | +0.000401 | 0.018777 | 0.019174 | +0.000397 | ⚠️ ECE 略惡化 |
| disagreement:high | 193/186 | −0.020780 | −0.025699 | **−0.004919** | 0.075902 | 0.080308 | +0.004406 | ❌ 惡化 |
| disagreement:low | 775/781 | 0.033032 | 0.032648 | −0.000384 | 0.033450 | 0.029923 | −0.003527 | ⚠️ BSS 略降 ECE ↓ |

### 關鍵段觀察

- **heavy_favorite ECE 輕微惡化**（+0.000425）：gate 評定關鍵失敗點
- **disagreement:high BSS 惡化**（−0.004919）：高異議賽場（模型與市場差距 > 10pp）反向走勢
- **high_confidence BSS 顯著改善**（+0.004854）：高信心預測準確率上升
- **2025-04 BSS 改善**（+0.000671）：初季樣本改善
- 整體 4 個月分段中 3 個月 BSS + ECE 均改善（04、05、06月）

---

## Gate Recommendation

```
gate = FEATURE_REPAIR_NOT_EFFECTIVE
```

### Gate 評定邏輯

| 條件 | 要求 | 實際 | 結果 |
|------|------|------|------|
| sp_fip_delta availability | ≥ 80% | **100.0%** | ✅ 通過 |
| overall BSS 改善 | > 0 | **+0.000152** | ✅ 通過 |
| 2025-04 BSS 改善 | > 0 | **+0.000671** | ✅ 通過 |
| heavy_favorite ECE 改善 | delta_ece < 0 | **+0.000425** | ❌ 失敗 |
| high_confidence BSS 不惡化 | ≥ 0 | **+0.004854** | ✅ 通過 |

**失敗原因**：`heavy_favorite ECE` 輕微惡化（+0.000425），未能滿足 `FEATURE_REPAIR_EFFECTIVE_PAPER_ONLY` 所需的「全部 4 個條件同時通過」要求。

### 備注

改善訊號明顯存在（3/4 條件通過，整體指標全面朝正向），但 heavy_favorite 桶校準（ECE）輕微退步，提示目前 FIP proxy 在大賠率差賽事的調整係數可能需要重新校準。

---

## Limitations

1. **FIP proxy 為 historical 估算**：所有 FIP 數值為 2024–2025 代理值（`estimated=True`），非實時資料
2. **聯盟平均 fallback 佔比高**：29.5% 純 fallback + 50.1% mixed，代表約 80% 的比賽至少有一位投手使用聯盟平均
3. **調整幅度細小**：`tanh(delta * 0.5) * 0.003` 最大為 ±0.003，調整機率影響上限 ±0.25pp
4. **heavy_favorite 桶惡化**：ECE +0.000425，可能因 FIP delta 方向與市場已隱含信息不一致
5. **disagreement:high 明顯惡化**：模型與市場高異議場次 BSS −0.004919，需進一步審計
6. **無 production 驗證**：本 phase 全為 paper-only offline evaluation

---

## Next Phase Recommendation

**Gate = `FEATURE_REPAIR_NOT_EFFECTIVE` → 建議 Phase 53**

### Phase 53 = SP Feature Coefficient / Adjustment Calibration Audit

目標：
1. 分析 `tanh(delta * 0.5) * 0.003` 係數是否適合 2025 MLB 分布
2. 審查 heavy_favorite 桶 FIP delta 分布 vs 市場賠率信息重疊度
3. 評估 disagreement:high 段惡化成因（FIP delta 方向與模型信號衝突？）
4. 測試不同 coefficient（0.001 / 0.002 / 0.005）對 heavy_favorite ECE 的影響
5. 若 coefficient 調整可使 heavy_favorite ECE 改善而不損 overall BSS → 重新評定 gate

---

## Hard Rules Verification

| 規則 | 狀態 |
|------|------|
| CANDIDATE_PATCH_CREATED = False | ✅ |
| PRODUCTION_MODIFIED = False | ✅ |
| ALPHA = 0.4 (未調整) | ✅ |
| 無 look-ahead leakage | ✅ (snapshot_date < game_date 全部通過) |
| 無 ensemble / re-training | ✅ |
| 無 post-game data | ✅ |
| gate ≠ PATCH | ✅ |
| paper-only / offline only | ✅ |

---

## Completion Marker

```
PHASE_52A_SP_BACKFILL_REAL_RUN_VERIFIED
gate=FEATURE_REPAIR_NOT_EFFECTIVE
total_rows=2025
match_rate=1.0000
sp_fip_delta_availability_rate=1.0000
point_in_time_safe_rate=1.0000
audit_hash_present_rate=1.0000
adjusted_rate=0.6696
sp_fip_triggered=1347
delta_bss=+0.000152
delta_brier=-0.000038
delta_ece=-0.000769
heavy_favorite_delta_ece=+0.000425 (gate失敗點)
candidate_patch_created=False
production_modified=False
regression=703/703
```
