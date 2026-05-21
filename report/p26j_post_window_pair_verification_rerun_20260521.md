# P26J Post-Window Pair Verification (Rerun) — 2026-05-21

**Generated:** 2026-05-21T09:12:47Z  
**Phase:** P26J  
**Run Type:** post_window_rerun (after 09:10Z threshold)  
**Timing Guard:** ✅ PASS (UTC 09:12:47 ≥ 09:10:00)

---

## Phase 1 — Commit Verification

| Commit | Description | Status |
|--------|-------------|--------|
| `d644f3f` | P26H+P26G: pair formation monitor + closure | ✅ Confirmed |
| `60a73a7` | P26I: closing capture gap investigation | ✅ Confirmed |
| `34fc118` | P26J: post-window pair verification (readiness checkpoint) | ✅ HEAD |

**Baseline confirmed:**
- target_match_ids: `["3469930.1", "3469931.1"]`
- COMPLETE_PAIR baseline: 220
- target_pair_delta baseline: 0
- bootstrap_ran: false

---

## Phase 2 — Post-Window Target Pair Analysis

### Game Reference
Both targets: game_time = `2026-05-21T17:00:00+08:00` = `2026-05-21T09:00:00Z`  
True closing window (gap 0–2h): `2026-05-21T07:00:00Z – 09:00:00Z`

### Match 3469930.1

| fetched_at | gap_h | capture_reason | force_closing | dedup_bypassed | markets |
|-----------|-------|---------------|---------------|----------------|---------|
| 2026-05-21T02:07:00Z | 6.88 | _(none)_ | False | False | 0 |
| 2026-05-21T02:09:35Z | 6.84 | closing_window | True | True | 0 |
| 2026-05-21T02:24:39Z | 6.59 | closing_window | True | True | 0 |
| 2026-05-21T02:39:43Z | 6.34 | closing_window | True | True | 0 |
| 2026-05-21T02:54:45Z | 6.09 | closing_window | True | True | 0 |
| 2026-05-21T03:09:49Z | 5.84 | closing_window | True | True | 0 |
| 2026-05-21T03:24:52Z | 5.59 | closing_window | True | True | 0 |

**Summary:**
- Total rows: 7 | Pregame (gap ≥ 4h): 7 | Closing (gap 0–2h): **0**
- `force_closing` labeled: 6 — but all at gap 5.59–6.84h, NOT within 0–2h window
- `markets = []` on ALL rows — source provided no market data
- **Pair Status: `PREGAME_ONLY_NO_CLOSING`**

---

### Match 3469931.1

| fetched_at | gap_h | capture_reason | force_closing | dedup_bypassed | markets |
|-----------|-------|---------------|---------------|----------------|---------|
| 2026-05-21T02:07:00Z | 6.88 | _(none)_ | False | False | 0 |
| 2026-05-21T02:09:35Z | 6.84 | closing_window | True | True | 0 |
| 2026-05-21T02:24:39Z | 6.59 | closing_window | True | True | 0 |
| 2026-05-21T02:39:43Z | 6.34 | closing_window | True | True | 0 |
| 2026-05-21T02:54:45Z | 6.09 | closing_window | True | **False** | 0 |
| 2026-05-21T03:09:49Z | 5.84 | closing_window | True | True | 0 |
| 2026-05-21T03:24:52Z | 5.59 | closing_window | True | True | 0 |
| 2026-05-21T04:55:09Z | 4.08 | _(none)_ | False | False | 0 |

**Summary:**
- Total rows: 8 | Pregame (gap ≥ 4h): 8 | Closing (gap 0–2h): **0**
- `force_closing` labeled: 6 — all at gap 5.59–6.84h, NOT within 0–2h window
- Last row fetched at 04:55Z (gap 4.08h) — still 4h pre-game, no closing row
- `markets = []` on ALL rows — source provided no market data
- **Pair Status: `PREGAME_ONLY_NO_CLOSING`**

---

### Target Summary

| Target | Total Rows | Pregame | Closing (gap 0–2h) | Pair Status |
|--------|-----------|---------|---------------------|-------------|
| 3469930.1 | 7 | 7 | 0 | `PREGAME_ONLY_NO_CLOSING` |
| 3469931.1 | 8 | 8 | 0 | `PREGAME_ONLY_NO_CLOSING` |

**target_pair_delta = 0** (neither target formed a complete pair)

---

## Phase 4 — Coverage Recheck

| Metric | Value |
|--------|-------|
| Total match_ids in history | 903 |
| COMPLETE_PAIR (current) | **219** |
| COMPLETE_PAIR (baseline) | 220 |
| Delta vs baseline | **–1** |
| pregame_only | 593 |
| closing_only | 50 |
| missing_closing | 593 |
| missing_pregame | 50 |
| total force_closing rows | 60 |
| total dedup_bypassed rows | 50 |

> ⚠️ COMPLETE_PAIR dropped by 1 vs baseline. Neither target added. Net: –1.

**P25C Bootstrap Eligibility:** NOT ELIGIBLE (219 < 300 threshold)  
**bootstrap_ran = false** — no change

---

## Phase 5 — Final Classification

```
P26J_TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED
```

**Rationale:**
1. TSL source returned `markets=[]` on ALL rows for both targets — no market data available at any point
2. `force_closing=True` labeled rows were captured ~5.6–6.8h before game (not in 0–2h closing window)
3. During the actual closing window (07:00–09:00Z), `fetched=false` in ALL 8 daemon cycles
4. `api_calls_today=2` remained stable — no additional API calls made during closing window
5. No closing row (gap 0–2h) formed for either target

---

*This is a read-only verification report. No code changes, no crawler modifications, no bootstrap execution.*
