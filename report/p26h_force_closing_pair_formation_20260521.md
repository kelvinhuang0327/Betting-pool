# P26H Force-Closing Pair Formation Monitor — 2026-05-21

**Phase**: P26H | **Date**: 2026-05-21 | **Status**: DIAGNOSTIC COMPLETE  
**paper_only**: true | **diagnostic_only**: true | **production_proposal**: false  
**axis_alignment**: axis_2_clv_validation_precondition

---

## Summary

P26H monitors the pair formation status of force-closing rows captured by the P26F mechanism. This report covers Phases 2-5: force-closing inventory, pair formation diagnosis, expected-new-pairs ground truth validation, and coverage recheck.

**Final Classification**: `P26H_EXPECTED_PAIRS_PREDICTION_BROKEN`

---

## Phase 2 — Force-Closing Row Inventory

| Metric | Value | vs P26G Baseline |
|--------|-------|-----------------|
| Total history rows | 2,902 | — |
| `force_closing_snapshot=True` rows | **40** | P26G initial: 10 (1 cycle → 4 cycles accumulated) |
| `dedup_bypassed=True` rows | **32** | P26G initial: 7 (multi-cycle accumulation) |
| `capture_reason=closing_window` rows | 40 | — |
| Force-closing unique match_ids | **10** | Same 10 matches as P26G |

### Gap Distribution (by unique match, first occurrence)

| Gap Band | Count | Match IDs |
|----------|-------|-----------|
| ≤ 2h | 1 | 3469566.1 (gap=-0.53h) |
| 2–6h | 0 | — |
| 6–15h | 2 | 3469930.1 (6.84h), 3469931.1 (6.84h) |
| > 15h | 7 | 3469903.1, 3469904.1, 3469923.1, 3469941.1, 3469943.1, 3469963.1, 3469964.1 |

**Note**: 40 rows = 4 daemon cycles × 10 unique matches. P26F mechanism confirmed accumulating correctly.

---

## Phase 3 — Pair Formation Breakdown

| Category | Count | Matches |
|----------|-------|---------|
| `complete` | 0 | — |
| `missing_pregame` | **1** | 3469566.1 |
| `missing_closing` | **9** | All others |
| `ambiguous` | 0 | — |

### Match-Level Detail

| match_id | missing_side | pregame | closing | Gap(h) | Root Cause |
|----------|-------------|---------|---------|--------|-----------|
| 3469566.1 | missing_pregame | ❌ | ✅ | -0.53 | Natural late listing / pregame capture missed |
| 3469930.1 | missing_closing | ✅ | ❌ | 6.84 | **P26G prediction broken** — expected closing today |
| 3469931.1 | missing_closing | ✅ | ❌ | 6.84 | **P26G prediction broken** — expected closing today |
| 3469903.1 | missing_closing | ✅ | ❌ | 15.01 | Closing window not yet reached |
| 3469904.1 | missing_closing | ✅ | ❌ | 15.09 | Closing window not yet reached |
| 3469923.1 | missing_closing | ✅ | ❌ | 17.92 | Closing window not yet reached |
| 3469941.1 | missing_closing | ✅ | ❌ | 20.51 | Closing window not yet reached |
| 3469943.1 | missing_closing | ✅ | ❌ | 20.92 | Closing window not yet reached |
| 3469963.1 | missing_closing | ✅ | ❌ | 23.47 | Closing window not yet reached |
| 3469964.1 | missing_closing | ✅ | ❌ | 23.51 | Closing window not yet reached |

---

## Phase 4 — Expected New Pairs Ground Truth

P26G predicted `expected_new_pairs_today = 2` for:
- 3469930.1 (game_time: 2026-05-21T09:00+08:00, window_entry: 07:00Z)
- 3469931.1 (game_time: 2026-05-21T09:00+08:00, window_entry: 07:00Z)

Both had `has_pregame=True` per P26G artifact. Ground truth scan of full `tsl_odds_history.jsonl`:

| match_id | has_pregame | has_closing_today | result |
|----------|-------------|-------------------|--------|
| 3469930.1 | ✅ | ❌ | NOT MATCHED |
| 3469931.1 | ✅ | ❌ | NOT MATCHED |

**Ground Truth**: `UNMATCHED` (0/2 formed COMPLETE_PAIR)

**Diagnosis**: P26G self-prediction BROKEN. Closing captures for these matches were not found within ≤2h of game_time. Possible causes:
1. Daemon cycle timing missed the 07:00Z–09:00Z closing window
2. Scheduler window boundary alignment issue
3. Matches cancelled/postponed after P26G prediction

→ **Requires P26I investigation**

---

## Phase 5 — Coverage Recheck

| Metric | P26G Baseline | P26H Recheck | Delta |
|--------|--------------|-------------|-------|
| COMPLETE_PAIR | 220 | **220** | **0** |
| pregame_only | 586 | 586 | 0 |
| closing_only | 75 | 75 | 0 |
| no_valid | 16 | 16 | 0 |
| total_matches | 897 | 897 | 0 |

**P25C Bootstrap**: BLOCKED (220 < 300 threshold)

---

## Final Classification

`P26H_EXPECTED_PAIRS_PREDICTION_BROKEN`

P26G predicted 2 new COMPLETE_PAIRs for 2026-05-21; ground truth is UNMATCHED (0 formed). COMPLETE_PAIR remains at 220. P25C bootstrap cannot run. Next step: P26I closing window capture gap investigation for 3469930.1 and 3469931.1.

---

## CEO Invariants Status

| Invariant | Status |
|-----------|--------|
| paper_only=true | ✅ MAINTAINED |
| promotion frozen | ✅ |
| champion_replacement blocked | ✅ |
| production_proposal=false | ✅ |
| P25C bootstrap blocked (220 < 300) | ✅ |
| raw feed not staged | ✅ |
| no new branch/worktree | ✅ |
