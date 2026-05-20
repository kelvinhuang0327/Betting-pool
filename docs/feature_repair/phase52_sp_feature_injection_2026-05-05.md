# Phase 52 SP Feature Injection Report

**日期**: 2026-05-05  
**Feature Version**: phase52_sp_injected_v1  
**Gate**: `FEATURE_REPAIR_NOT_EFFECTIVE`  

## Executive Summary

- sp_fip_delta_availability: **100.0%**
- adjusted_rate: **67.0%** (Phase50: 0.9%)
- delta_bss: **+0.000152**
- gate: **FEATURE_REPAIR_NOT_EFFECTIVE**

## Metric Delta

| Metric | Baseline | Phase52 | Delta |
|--------|----------|---------|-------|
| Brier  | 0.244706 | 0.244668 | -0.000038 |
| BSS    | 0.021177 | 0.021329 | +0.000152 |
| ECE    | 0.031097 | 0.030328 | -0.000769 |
| LogLoss| 0.682205 | 0.682126 | -0.000079 |

## Feature Trigger Statistics

- rows_total: 2025
- rows_adjusted: 1356
- sp_fip_triggered: 1347
- park_factor_triggered: 18
- early_season_triggered: 0
- cap_applied_count: 0

## Critical Segment Deltas

- **month:2025-04**: delta_bss=+0.000671, delta_ece=-0.000120
- **month:2025-05**: delta_bss=+0.000094, delta_ece=-0.001143
- **month:2025-06**: delta_bss=+0.000298, delta_ece=-0.002441
- **month:2025-07**: delta_bss=+0.000295, delta_ece=+0.001702
- **odds_bucket:heavy_favorite**: delta_bss=+0.000463, delta_ece=+0.000425
- **odds_bucket:mid**: delta_bss=+0.000074, delta_ece=+0.001340
- **confidence:high_confidence**: delta_bss=+0.004854, delta_ece=+0.004658
- **confidence:low_confidence**: delta_bss=+0.000401, delta_ece=+0.000397
- **disagreement:high**: delta_bss=-0.004919, delta_ece=+0.004406
- **disagreement:low**: delta_bss=-0.000384, delta_ece=-0.003527

## Gate Rationale

availability 100.0%≥80%, delta_bss=+0.000152 — 未達顯著改善

## Hard Rules

- candidate_patch_created: `False`
- production_modified: `False`

```
PHASE_52_STARTING_PITCHER_BACKFILL_VERIFIED
gate=FEATURE_REPAIR_NOT_EFFECTIVE
sp_fip_delta_availability_rate=1.0000
adjusted_rate=0.6696
delta_bss=+0.000152
candidate_patch_created=False
production_modified=False
```