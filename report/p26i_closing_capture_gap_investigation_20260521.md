# P26I Closing Capture Gap Investigation — 2026-05-21

**Phase**: P26I | **Date**: 2026-05-21  
**paper_only**: true | **diagnostic_only**: true | **production_proposal**: false  
**axis_alignment**: axis_2_clv_validation_precondition

---

## Pre-flight

| Check | Result |
|-------|--------|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| Branch | `main` ✅ |
| HEAD | `d644f3f` (P26H+P26G commit) ✅ |
| P26H commit verified | `d644f3f` in git log ✅ |
| Stop conditions | None triggered ✅ |

---

## Phase 1 — P26H Verification

| Field | Value |
|-------|-------|
| P26H commit | `d644f3f` ✅ |
| P26H classification | `P26H_EXPECTED_PAIRS_PREDICTION_BROKEN` |
| expected_new_pairs ground truth | `UNMATCHED` |
| COMPLETE_PAIR at P26H | 220 |

---

## Phase 2 — Focus Match Analysis

### game_time Disambiguation

| Field | Value |
|-------|-------|
| 3469930.1 / 3469931.1 game_time | `2026-05-21T17:00:00+08:00` |
| **game_time UTC** | **`2026-05-21T09:00:00Z`** |
| Closing window opens | **07:00Z** |
| Closing window closes | **09:00Z** |
| P26I analysis time | ~03:09Z |
| Time until window at analysis | **~3.85h** |

### 3469930.1 — Snapshot Timeline

| fetched_at (UTC) | gap_hours | Zone | fc | ded | reason |
|-----------------|-----------|------|----|-----|--------|
| 02:07:00 | 6.883h | PREGAME | — | — | — |
| 02:09:35 | 6.840h | PREGAME | ✅ | ✅ | closing_window |
| 02:24:39 | 6.589h | PREGAME | ✅ | ✅ | closing_window |
| 02:39:43 | 6.338h | PREGAME | ✅ | ✅ | closing_window |
| 02:54:45 | 6.087h | PREGAME | ✅ | ✅ | closing_window |
| 03:09:49 | 5.836h | PREGAME | ✅ | ✅ | closing_window |

**Finding**: All 6 rows in PREGAME zone. No closing snapshot because **the closing window (07:00Z) has not yet opened** at analysis time (03:09Z). Daemon IS running.

### 3469931.1 — Snapshot Timeline

Identical game_time and gap profile to 3469930.1 (same batch captures). Same finding.

### 3469566.1 — Comparison (missing_pregame case)

| Field | Value |
|-------|-------|
| game_time UTC | 01:38Z (game already happened) |
| Gap range | -0.48h to -1.53h (POST-GAME) |
| Label | missing_pregame (never had ≥4h pregame) |
| Relationship | Structural, unrelated to 3469930.1/3469931.1 |

---

## Phase 3 — Daemon / Schedule Alignment

| Metric | Value |
|--------|-------|
| Latest daemon heartbeat | `2026-05-21T03:09:50Z` |
| Daemon status | **RUNNING** |
| Cycle interval | ~15 minutes |
| Capture schedule last_run | `2026-05-21T02:54:47Z` (lags 1 cycle) |
| Time to closing window | **~3.85h** |
| Expected cycles before window | ~15 |
| Historical gap risk | 9.9h gap on 2026-05-20 (15:10Z → 01:06Z+1) |

**Daemon is active.** P26H's 02:54Z analysis was 4.1h before the 07:00Z window. The UNMATCHED classification was premature.

---

## Phase 4 — Prediction Logic Audit

**P26G predicted** `expected_new_pairs_today=2` because:
- 3469930.1 and 3469931.1 have confirmed pregame snapshots (gap=6.84h)
- game_time=09:00Z → closing window=07:00Z–09:00Z
- Daemon was running at prediction time

**P26G assumption**: Daemon will continue through 07:00Z–09:00Z window.

**P26H evaluated** at 02:54Z (4.1h BEFORE window) → found 0 closing snapshots → labeled BROKEN. **This was premature.**

**P26G failure classification**: `P26I_P26G_PREDICTION_LOGIC_TOO_OPTIMISTIC`
- Does not model daemon outage risk
- Does not specify `daemon_uptime_required_until` in prediction artifact
- Prediction is conditionally valid but presents as unconditional

---

## Phase 5 — Coverage Recheck

| Metric | P26H | P26I |
|--------|------|------|
| history rows | 2902 | 2912 (+10, new daemon cycle) |
| force_closing rows | 40 | 50 (+10) |
| dedup_bypassed rows | 32 | 41 (+9) |
| COMPLETE_PAIR | 220 | **220** |
| delta | — | **0** |
| missing_pregame | — | 75 |
| missing_closing | — | 586 |
| P25C bootstrap | BLOCKED | **BLOCKED** |

COMPLETE_PAIR=220, bootstrap remains blocked (threshold=300).

---

## Final Classification

`P26I_CLOSING_CAPTURE_GAP_INCONCLUSIVE`

**Rationale**: Analysis was performed at ~03:09Z, 3.85h before the 07:00Z closing window. Daemon IS running and capturing matches every 15min. Cannot confirm or deny the P26G prediction until post-game (09:00Z+). P26H's "BROKEN" label was premature. Risk factor: 9.9h daemon outage history on 2026-05-20.

---

## P26J Recommendation

| Condition | Expected Outcome |
|-----------|-----------------|
| Daemon runs through 09:00Z | COMPLETE_PAIR=222 (+2), P26G prediction **FULFILLED** |
| Daemon stops before 07:00Z | COMPLETE_PAIR=220 (0), P26G prediction **CONFIRMED BROKEN** |

**P26J action**: Post-game validation after 09:00Z UTC (17:00 Taiwan time). Read `data/tsl_odds_history.jsonl`, check 3469930.1 / 3469931.1 for ≤2h closing snapshots. Diagnostic only — no code changes.
