# P26H Pregame Gap Classification — 2026-05-21

**Phase**: P26H | **Date**: 2026-05-21  
**paper_only**: true | **diagnostic_only**: true  
**axis_alignment**: axis_2_clv_validation_precondition

---

## Classification Schema

| Label | Definition |
|-------|-----------|
| `missing_pregame` | Has closing snapshot (≤2h gap) but NO pregame (≥4h gap) — CLV pair impossible |
| `missing_closing` | Has pregame (≥4h gap) but NO closing (≤2h gap) yet |
| `complete` | Both pregame + closing present — COMPLETE_PAIR, CLV-eligible |
| `ambiguous` | Insufficient data |

---

## Per-Match Classification (10 Force-Closing Matches)

| match_id | Label | Gap(h) | pregame | closing | P26I Priority | Root Cause |
|----------|-------|--------|---------|---------|--------------|-----------|
| 3469566.1 | missing_pregame | -0.53 | ❌ | ✅ | LOW | Natural late listing / pregame never captured |
| 3469930.1 | missing_closing | 6.84 | ✅ | ❌ | **HIGH** | P26G prediction broken — closing not captured |
| 3469931.1 | missing_closing | 6.84 | ✅ | ❌ | **HIGH** | P26G prediction broken — closing not captured |
| 3469903.1 | missing_closing | 15.01 | ✅ | ❌ | MEDIUM | Closing window pending (far advance) |
| 3469904.1 | missing_closing | 15.09 | ✅ | ❌ | MEDIUM | Closing window pending (far advance) |
| 3469923.1 | missing_closing | 17.92 | ✅ | ❌ | MEDIUM | Closing window pending (far advance) |
| 3469941.1 | missing_closing | 20.51 | ✅ | ❌ | LOW | Far advance, natural progression |
| 3469943.1 | missing_closing | 20.92 | ✅ | ❌ | LOW | Far advance, natural progression |
| 3469963.1 | missing_closing | 23.47 | ✅ | ❌ | LOW | Far advance, natural progression |
| 3469964.1 | missing_closing | 23.51 | ✅ | ❌ | LOW | Far advance, natural progression |

---

## Summary by Root Cause

| Root Cause | Count |
|-----------|-------|
| `pregame_never_captured_closing_only` | 1 |
| `P26G_prediction_broken_near_pregame_no_closing` | **2** |
| `pregame_captured_far_advance_closing_pending` | 7 |

## P26I Priority Summary

| Priority | Count | Action |
|----------|-------|--------|
| HIGH | 2 | Investigate closing window capture miss for 3469930.1, 3469931.1 |
| MEDIUM | 3 | Monitor — will enter closing window in coming days |
| LOW | 5 | Natural progression — no action needed |

---

## P26I Recommendation

**Scope**: Diagnose why 3469930.1 and 3469931.1 (game_time=2026-05-21T09:00+08:00) did not receive a ≤2h closing snapshot despite:
1. Having pregame snapshots at 6.84h gap
2. P26G predicting closing window entry at 07:00Z
3. Being classified as `has_pregame=True` in P26G artifact

**Hypothesis**: Daemon cycle interval (likely ~30min) may have cycled through the 07:00Z–09:00Z window but failed to capture these specific match IDs, possibly due to scheduler match_id filter, API pagination, or match cancellation.
