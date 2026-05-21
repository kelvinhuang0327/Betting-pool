# P26I Closing Capture Gap Investigation — 2026-05-21

**Task**: `P26I_CLOSING_WINDOW_CAPTURE_GAP_INVESTIGATION_20260521`  
**paper_only**: true | **diagnostic_only**: true | **production_proposal**: false  
**axis_alignment**: axis_2_clv_validation_precondition

---

## Executive Summary (CTO 10-Line)

P26H evaluated `expected_new_pairs_today=2` as BROKEN (UNMATCHED) — but did so at 02:54Z, **4.1h before the 07:00Z closing window opened**. That classification was premature. P26I investigation at ~03:09Z confirms: daemon IS running (latest heartbeat 03:09:50Z), TSL IS listing 3469930.1 and 3469931.1 every 15min cycle (6 captures each, all PREGAME gap 5.8–6.9h), source IS available, no matching rule bug. The closing window for these games (game_time=17:00+08:00 = 09:00Z UTC) opens at 07:00Z — still 3.85h away. COMPLETE_PAIR remains 220 (delta=0), bootstrap blocked (220 < 300). Root cause: P26G prediction logic is conditionally optimistic (assumes daemon uptime through window); P26H evaluation was too early. **Final Classification: `P26I_CLOSING_CAPTURE_GAP_INCONCLUSIVE`**. Recommend P26J: post-game (09:00Z+) validation — if daemon ran through window, expect COMPLETE_PAIR=222 (+2).

---

## Key Metrics

| Metric | Value |
|--------|-------|
| 3469930.1 diagnosis | Pregame only; closing window not yet open at analysis |
| 3469931.1 diagnosis | Identical to 3469930.1 |
| Root cause | P26H premature evaluation + P26G conditional-only prediction |
| Daemon status | RUNNING (03:09:50Z) |
| COMPLETE_PAIR | 220 (delta=0) |
| Bootstrap | BLOCKED (220 < 300) |
| Tests | 75 PASS + 318 PASS = 393 PASS / 0 FAIL |
| Forbidden scan | GREP_CLEAN_CANDIDATE |
| Final classification | `P26I_CLOSING_CAPTURE_GAP_INCONCLUSIVE` |

---

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 02:07Z | First snapshots for 3469930.1/3469931.1 (gap=6.88h, pregame) |
| 02:09Z–02:54Z | P26F force_closing active, 4 more cycles (gap 6.08–6.84h, all pregame) |
| 02:54Z | P26H analysis — labeled UNMATCHED (premature, window not open) |
| 03:09Z | P26I analysis — daemon confirmed running, 6th cycle captured |
| **07:00Z** | **Closing window OPENS for 3469930.1/3469931.1** |
| 09:00Z | Games start — P26J validation point |

---

## P26J Action

Post-game validation after 09:00Z:
- Confirm ≤2h closing snapshots for 3469930.1/3469931.1 in history
- If yes: P26G prediction FULFILLED, COMPLETE_PAIR expected=222
- If no: Confirm daemon stopped before 07:00Z, P26G prediction confirmed BROKEN
