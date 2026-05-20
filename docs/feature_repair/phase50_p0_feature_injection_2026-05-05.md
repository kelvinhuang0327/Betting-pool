# Phase 50 — P0 Feature Injection Report

**報告日期**: 2026-05-05  
**Feature Version**: `phase50_p0_injected_v1`  
**Generated at**: 2026-05-05T04:38:28.835192+00:00  

---

## Executive Summary

Phase 50 將 Phase48 P0 features 注入 backtest prediction path。
採用保守 deterministic post-hoc adjustment，不重新訓練模型。

| 項目 | 值 |
|---|---|
| **feature_effect_mode** | `MODEL_AFFECTING` |
| **gate_recommendation** | `FEATURE_REPAIR_NOT_EFFECTIVE` |
| rows_total | 2,025 |
| rows_adjusted | 18 |
| adjusted_rate | 0.9% |
| mean_abs_adjustment | 0.000003 |
| max_abs_adjustment | 0.001174 |
| candidate_patch_created | `False` |
| production_modified | `False` |

---

## Injection Statistics

| 指標 | 值 |
|---|---|
| rows_total | 2,025 |
| rows_adjusted | 18 |
| rows_unchanged | 2,007 |
| adjusted_rate | 0.9% |
| mean_abs_adjustment | 0.000003 |
| max_abs_adjustment | 0.001174 |
| orig_adj_correlation | 1.000000 |
| early_season_triggered | 0 |
| park_factor_triggered | 18 |
| sp_fip_triggered | 0 |
| cap_applied_count | 0 |

---

## Baseline vs Phase50 Metrics

| Source | N | Brier | BSS vs Market | ECE | Log Loss |
|---|---|---|---|---|---|
| Baseline | 2,025 | 0.244706 | -0.003894 | 0.031097 | 0.682205 |
| Phase50  | 2,025 | 0.244706 | -0.003897 | 0.031098 | 0.682207 |
| **Delta** | — | +0.000000 | -0.000003 | +0.000001 | +0.000002 |

---

## Critical Segment Delta BSS

| Segment | Δ BSS | Direction |
|---|---|---|
| `month:2025-04` | +0.0000 | — 持平 |
| `month:2025-05` | +0.0000 | ✅ 改善 |
| `month:2025-06` | +0.0000 | — 持平 |
| `month:2025-07` | -0.0000 | — 持平 |
| `odds_bucket:heavy_favorite` | -0.0000 | — 持平 |
| `odds_bucket:mid` | +0.0000 | ✅ 改善 |
| `confidence:high_confidence` | -0.0000 | — 持平 |
| `confidence:low_confidence` | +0.0000 | — 持平 |
| `disagreement:high` | +0.0000 | — 持平 |
| `disagreement:low` | -0.0000 | — 持平 |

---

## Gate Recommendation

**`FEATURE_REPAIR_NOT_EFFECTIVE`**

> MODEL_AFFECTING: P0 features altered predictions but did not meet all success criteria. Feature repair incomplete. apr_ok=False, hf_ok=False, hc_ok=False, overall_ok=False.

---

## Adjustment Logic

Phase 50 採用三組保守 deterministic 調整規則（不重新訓練模型）：

| Rule | 條件 | 效果 |
|---|---|---|
| F-004 season_game_index | `sgi < 0.20` | 往 0.5 收縮（早季不確定性高）|
| F-002 park_run_factor | `prf > 1.05` 且 `p > 0.60` | 降低 home 過度信心 |
| F-001 sp_fip_delta | `available=True` | 依 FIP 差距微調 |
| **Cap** | 總調整量 > 0.025 | Clamp to ±0.025 |
| **Prob clamp** | always | adjusted ∈ [0.01, 0.99] |

---

## 不變量驗證

| 規則 | 狀態 |
|---|---|
| `candidate_patch_created = False` | ✅ |
| `production_modified = False` | ✅ |
| 無外部 API / LLM 呼叫 | ✅ |
| 無 production 修改 | ✅ |
| 不讀取 leakage 欄位 | ✅ |
| 調整量 ≤ ±0.025 cap | ✅ |
| adjusted_prob ∈ [0.01, 0.99] | ✅ |
| gate ∈ valid set | ✅ (`FEATURE_REPAIR_NOT_EFFECTIVE`) |

---

## 驗證標記

```
PHASE_50_P0_FEATURE_INJECTION_VERIFIED
feature_version=phase50_p0_injected_v1
feature_effect_mode=MODEL_AFFECTING
gate=FEATURE_REPAIR_NOT_EFFECTIVE
rows_total=2025
rows_adjusted=18
adjusted_rate=0.0089
mean_abs_adjustment=0.000003
max_abs_adjustment=0.001174
delta_bss=-0.000003
candidate_patch_created=False
production_modified=False
```