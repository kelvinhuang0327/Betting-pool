# P26I Expected Pair Prediction Failure Analysis — 2026-05-21

**Phase**: P26I | **Date**: 2026-05-21  
**paper_only**: true | **diagnostic_only**: true | **production_proposal**: false  
**axis_alignment**: axis_2_clv_validation_precondition

---

## Summary

P26G predicted `expected_new_pairs_today=2` (3469930.1 and 3469931.1). P26H classified this as `P26H_EXPECTED_PAIRS_PREDICTION_BROKEN` (UNMATCHED). P26I investigation reveals that **P26H's evaluation was premature** — performed 4.1h before the closing window opened. The daemon is still running at P26I analysis time; correctness of P26G's prediction cannot be confirmed until after game time (09:00Z).

---

## Prediction Chain

```
P26G (02:09Z) → predicted expected_new_pairs_today=2
                 → assumed daemon continues through 07:00Z-09:00Z
P26H (02:54Z) → evaluated UNMATCHED (no closing snapshots found)
                 → PROBLEM: evaluated 4.1h BEFORE closing window opened
P26I (03:09Z) → daemon confirmed running
                 → closing window NOT yet open (3.85h remaining)
                 → P26H label was PREMATURE
```

---

## Root Cause Findings

### F1: P26H Analysis Was Premature (HIGH)

P26H ran at 02:54Z. Closing window opens at 07:00Z. Gap = **4.1h**. No closing snapshot can physically exist at 02:54Z for a 07:00Z window. The UNMATCHED label should be `TOO_EARLY_TO_VERIFY`.

### F2: Daemon Running at P26I Time (INFO)

Latest heartbeat: `03:09:50Z`. Daemon running every ~15min since 01:06Z. 6 consecutive captures for both 3469930.1 and 3469931.1 (02:07Z through 03:09Z). All in PREGAME zone (gap 5.8–6.9h).

### F3: TSL Source IS Available (INFO)

Both matches are listed in TSL every cycle with `force_closing=True`, `capture_reason=closing_window`. Source availability is not the issue.

### F4: Historical Daemon Gap Risk (MEDIUM)

On 2026-05-20: daemon stopped at 15:10Z and restarted at 01:06Z+1 (9.9h gap). If daemon stops before 07:00Z today, closing window will be missed. P26G's prediction does not model this risk.

### F5: P26G Prediction Logic Is Conditionally Optimistic (MEDIUM)

P26G presents an unconditional prediction (`expected_new_pairs_today=2`) but the correctness is conditional on daemon uptime in a specific 2h window. Recommendation: future prediction artifacts should include `daemon_uptime_required_until` field.

---

## Prediction Failure Classification

| Candidate | Status |
|-----------|--------|
| `P26I_SCHEDULER_WINDOW_ALIGNMENT_GAP_CONFIRMED` | ❌ Ruled out — daemon IS running |
| `P26I_TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED` | ❌ Ruled out — source capturing every cycle |
| `P26I_MATCHING_RULE_TIMESTAMP_BUG_SUSPECTED` | ❌ Ruled out — timestamps and gap computation verified |
| `P26I_P26G_PREDICTION_LOGIC_TOO_OPTIMISTIC` | ⚠️ Partially applies |
| **`P26I_CLOSING_CAPTURE_GAP_INCONCLUSIVE`** | ✅ **Selected** |

**Final**: `P26I_CLOSING_CAPTURE_GAP_INCONCLUSIVE`

Cannot confirm P26G prediction failure until after 09:00Z (post-game validation). P26H's BROKEN label was premature. P26G prediction may still be fulfilled.

---

## Governance Flags

| Flag | Value |
|------|-------|
| paper_only | true |
| diagnostic_only | true |
| production_proposal | false |
| promotion_allowed | false |
| champion_replacement_allowed | false |
| P25C bootstrap | BLOCKED (220 < 300) |
