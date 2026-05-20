# Phase 54 — Safe SP Stability Audit Report

**Generated**: 2026-05-05  
**Phase54 Version**: phase54_safe_sp_stability_audit_v1  
**Audit Hash**: `02b51119b6783b6c`  
**Gate**: 🔴 `FEATURE_REPAIR_STILL_WEAK`  

---

## Executive Summary

Phase 54 使用 Phase53 safe coefficient (scale=0.25x，effective=0.00075) 對 2,025 筆 MLB 2025 比賽預測套用調整，並重跑 Phase43/44/45 穩定性審計。

| 指標 | 數值 |
|------|------|
| Phase54 rows | 2025 |
| adjusted rows | 1356 (67.0%) |
| max_abs_adjustment | 0.001174 |
| overall BSS Δ vs baseline | +0.000036 |
| overall ECE Δ vs baseline | -0.001278 |
| heavy_fav ECE Δ vs baseline | -0.000073 |
| high_conf BSS Δ vs baseline | +0.000031 |

---

## Safe Coefficient Summary

| 欄位 | 值 |
|------|---|
| scale | 0.25 |
| effective_coefficient | 0.00075 |
| feature_effect_mode | MODEL_AFFECTING |
| diagnostic_only | True |
| candidate_patch_created | False |
| production_modified | False |

---

## Phase43 Re-run Result

| 指標 | Phase43 Baseline | Phase54 | Delta |
|------|-----------------|---------|-------|
| overall_blend_BSS | 0.002200 | 0.002174 | -0.000026 |
| overall_blend_ECE | 0.028100 | 0.027703 | -0.000397 |
| fold_stability | STABLE (4/5) | STABLE (4/5) | Δ=+0 |
| bootstrap | NOT_SIGNIFICANT | NOT_SIGNIFICANT | — |
| bootstrap CI | [-0.0015, 0.0006] | [-0.001519, 0.000596] | — |
| prob_improvement | 81.0% | 79.8% | — |

---

## Phase44 Paper Tracking Result

| 欄位 | 值 |
|------|---|
| gate_state | PAPER_ONLY |
| alpha | 0.4 |
| sample_size | 2025 |
| blend_brier | 0.243227 |
| blend_bss | 0.002171 |
| blend_ece | 0.027703 |
| bootstrap | NOT_SIGNIFICANT |
| candidate_patch_created | False |

---

## Phase45 Attribution Result

| 欄位 | 值 |
|------|---|
| global_conclusion | CONDITIONAL_VALUE |
| gate | FEATURE_REPAIR_INVESTIGATION |
| positive_segments | 3 |
| failure_segments | 6 |
| failure_count_delta | +6 |
| heavy_fav ECE no longer failure | False |
| high_conf improved | False |
| heavy_fav blend_bss | -0.001679 |
| high_conf blend_bss | -0.002626 |

**Positive segments**: month:2025-07, month:2025-05, disagreement:medium

**Failure segments**: odds_bucket:heavy_favorite, odds_bucket:mid, disagreement:low, month:2025-04, month:2025-06, month:2025-08

---

## Baseline vs Phase54 Comparison

| 指標 | Baseline (no SP adj) | Phase54 (scale=0.25x) | Δ |
|------|----------------------|-----------------------|---|
| overall BSS | — | +0.000036 improvement | +0.000036 |
| overall ECE | — | -0.001278 | -0.001278 |
| heavy_fav ECE | — | -0.000073 | -0.000073 |
| high_conf BSS | — | +0.000031 | +0.000031 |

---

## Critical Segment Comparison Table

Δ BSS > 0 = 改善；Δ ECE < 0 = 改善

| Segment | P43 BSS | P54 BSS | Δ BSS | P43 ECE | P54 ECE | Δ ECE | Label |
|---------|---------|---------|-------|---------|---------|-------|-------|
| confidence:high_confidence | N/A | -0.00263 | N/A | N/A | +0.01727 | N/A | UNKNOWN |
| confidence:low_confidence | N/A | +0.00446 | N/A | N/A | +0.02047 | N/A | UNKNOWN |
| confidence:mid_confidence | N/A | +0.00264 | N/A | N/A | +0.05246 | N/A | UNKNOWN |
| confidence_bucket:high_conf | -0.01555 | N/A | N/A | +0.08306 | N/A | N/A | UNKNOWN |
| confidence_bucket:low_conf | +0.00464 | N/A | N/A | +0.01840 | N/A | N/A | UNKNOWN |
| confidence_bucket:medium_conf | +0.00268 | N/A | N/A | +0.03789 | N/A | N/A | UNKNOWN |
| disagreement:high | N/A | +0.00173 | N/A | N/A | +0.07093 | N/A | UNKNOWN |
| disagreement:low | N/A | +0.00063 | N/A | N/A | +0.02950 | N/A | UNKNOWN |
| disagreement:medium | N/A | +0.00500 | N/A | N/A | +0.04287 | N/A | UNKNOWN |
| disagreement_bucket:high_disagree | +0.00183 | N/A | N/A | +0.05028 | N/A | N/A | UNKNOWN |
| disagreement_bucket:low_disagree | +0.00063 | N/A | N/A | +0.03279 | N/A | N/A | UNKNOWN |
| disagreement_bucket:medium_disagree | +0.00333 | N/A | N/A | +0.03314 | N/A | N/A | UNKNOWN |
| month:2025-04 | -0.02497 | -0.02490 | +0.00007 | +0.12466 | +0.19919 | +0.07453 | UNCHANGED |
| month:2025-05 | +0.00573 | +0.00573 | +0.00001 | +0.03048 | +0.04215 | +0.01167 | UNCHANGED |
| month:2025-06 | -0.00440 | -0.00438 | +0.00002 | +0.02879 | +0.07897 | +0.05018 | UNCHANGED |
| month:2025-07 | +0.00861 | +0.00862 | +0.00002 | +0.04946 | +0.03222 | -0.01723 | UNCHANGED |
| month:2025-08 | +0.00293 | +0.00292 | -0.00001 | +0.02702 | +0.04178 | +0.01477 | UNCHANGED |
| month:2025-09 | +0.00107 | +0.00107 | +0.00000 | +0.05659 | +0.04770 | -0.00889 | UNCHANGED |
| odds_bucket:heavy_away_fav | +0.00182 | N/A | N/A | +0.02008 | N/A | N/A | UNKNOWN |
| odds_bucket:heavy_favorite | N/A | -0.00168 | N/A | N/A | +0.08921 | N/A | UNKNOWN |
| odds_bucket:heavy_home_fav | +0.00192 | N/A | N/A | +0.02735 | N/A | N/A | UNKNOWN |
| odds_bucket:mid | N/A | +0.00234 | N/A | N/A | +0.04460 | N/A | UNKNOWN |
| odds_bucket:pick_em | -0.00019 | N/A | N/A | +0.01984 | N/A | N/A | UNKNOWN |
| odds_bucket:slight_away_fav | +0.00693 | N/A | N/A | +0.03591 | N/A | N/A | UNKNOWN |
| odds_bucket:slight_home_fav | +0.00006 | N/A | N/A | +0.05233 | N/A | N/A | UNKNOWN |
| odds_bucket:underdog | N/A | +0.00319 | N/A | N/A | +0.03004 | N/A | UNKNOWN |

---

## Bootstrap / Fold Stability Result

| 項目 | Phase43 Baseline | Phase54 |
|------|-----------------|---------|
| fold_stability | STABLE | STABLE |
| folds_positive | 4/5 | 4/5 |
| bootstrap_CI | [-0.0015, 0.0006] | [-0.001519, 0.000596] |
| bootstrap significance | NOT_SIGNIFICANT | NOT_SIGNIFICANT |
| prob_improvement | 81.0% | 79.8% |

> **Note**: Bootstrap CI 跨 0 = NOT_SIGNIFICANT 並非說明無效，而是樣本量仍不足以達到統計顯著。paper-only tracking 繼續積累資料。

---

## Gate Recommendation

**Gate**: 🔴 `FEATURE_REPAIR_STILL_WEAK`

**Rationale**: 整體指標惡化或 failure segment 增加：BSS delta=-2.6e-05, ECE delta=-0.000397, failure_count_delta=6

---

## Limitations

1. safe coefficient (0.25x) 在 2,025 筆樣本上評估，樣本仍不足以達 bootstrap 顯著性。
2. Phase43 fold stability 採用 expanding-window，非 pure out-of-sample；仍存在 train/test 滑動 bias。
3. heavy_favorite ECE 改善來自 Phase53 coefficient calibration，   但 heavy_favorite 市場在 SP FIP 較大時較不穩定。
4. Phase54 JSONL 的 model_home_prob 已被 safe coefficient 修改，   Phase43/44/45 將以此為「raw model prob」進行分析，   因此 blend(model, market, 0.4) 的「model」部分已含 SP feature。
5. 本 Phase 不可產生 PATCH_GATE_RECHECK，所有結論均為 paper-only。

---

## Next Phase Recommendation

**Phase 55 — SP Functional Form Redesign or Bullpen Feature Investigation**

當前 SP FIP 函數形式（tanh 壓縮）在特定 segment 仍有惡化跡象，建議探索：(1) segment-specific coefficients，(2) sigmoid 替代，(3) matchup-level confidence gate，(4) 牛棚特徵補充。

---

## Hard Rules Verification

```
candidate_patch_created = False
production_modified     = False
diagnostic_only         = True
gate != PATCH           = True
gate != PATCH_GATE_RECHECK = True
alpha = 0.4             = True
safe_coefficient_scale  = 0.25
effective_coefficient   = 0.00075
```

---

## Completion Marker

```
PHASE_54_SAFE_SP_STABILITY_AUDIT_VERIFIED
gate=FEATURE_REPAIR_STILL_WEAK
safe_coefficient_scale=0.25
effective_coefficient=0.00075
phase43_blend_bss=0.002174
phase43_fold_stability=STABLE
phase44_sample_size=2025
phase45_failure_count=6
candidate_patch_created=False
production_modified=False
diagnostic_only=True
audit_hash=02b51119b6783b6c
```
