# P26J Daemon Continuity Verification (Rerun) — 2026-05-21

**Generated:** 2026-05-21T09:12:47Z  
**Phase:** P26J  
**Run Type:** daemon_continuity_rerun (after 09:10Z threshold)  
**Timing Guard:** ✅ PASS

---

## Verification Window

| Field | Value |
|-------|-------|
| Start | 2026-05-21T07:00:00Z |
| End | 2026-05-21T09:00:00Z |
| Purpose | Closing window for 17:00 Taiwan time games (game_time = 09:00Z) |

---

## Phase 3 — Daemon Heartbeat Analysis

**Total heartbeat rows (all time):** 2,096  
**Heartbeat rows in 07:00–09:00Z window:** 8

| Timestamp (UTC) | fetched | api_calls_today | status | next_trigger_min |
|----------------|---------|----------------|--------|-----------------|
| 07:10:39 | **false** | 2 | captured | null |
| 07:25:49 | **false** | 2 | captured | null |
| 07:40:51 | **false** | 2 | captured | null |
| 07:55:53 | **false** | 2 | captured | null |
| 08:10:55 | **false** | 2 | captured | null |
| 08:25:57 | **false** | 2 | captured | null |
| 08:40:58 | **false** | 2 | captured | null |
| 08:56:01 | **false** | 2 | captured | null |

**Last heartbeat before window:** 2026-05-21T06:55:35Z  
**First heartbeat after window:** 2026-05-21T09:11:03Z  
**Cycle interval:** ~15 minutes (consistent, no gap)

---

## Key Observations

1. **Daemon was alive and cycling** — 8 heartbeats in window, no stop detected
2. **`fetched=false` in ALL 8 cycles** — the external closing API was NOT called during the entire closing window
3. **`api_calls_today=2` stable throughout** — only 2 API calls occurred all day (likely the 02:07Z + 02:09Z early captures)
4. **`next_trigger_minutes=null`** — no future closing fetch was scheduled
5. **`status='captured'` is misleading** — this field reflects daemon cycle completion, NOT actual data fetch success
6. **No target rows appear in tsl_odds_history.jsonl with fetched_at in 07:00–09:00Z** — confirmed no data received

---

## Root Cause Hypothesis

The external closing API trigger was **not activated** during the 07:00–09:00Z window. Most likely causes:

| Hypothesis | Likelihood | Evidence |
|-----------|-----------|---------|
| api_calls_today quota reached (hard cap at 2) | High | Stable at 2 from 07:10 through 09:00Z |
| Closing trigger condition not evaluating game proximity correctly | Medium | next_trigger_minutes=null even when <2h to game |
| TSL source not listing targets in feed (source-side unavailability) | High | markets=[] on all earlier captures |
| Force-closing logic fired too early (~6h pre-game) and exhausted budget | Medium | All fc_labeled rows are at 5.6–6.9h gap |

---

## Classification

```
DAEMON_RAN_BUT_SOURCE_DID_NOT_RETURN_TARGETS
```

**Sub-classification:** `FETCH_NOT_EXECUTED_IN_CLOSING_WINDOW`

The daemon ran successfully throughout the closing window but the external API fetch was **not triggered** for any cycle. Combined with `markets=[]` on all prior captures, the TSL source appears to have been unavailable for these targets from the start.

---

## Actions

- **Actions taken:** None (read-only verification)
- **Actions blocked:** daemon restart, scheduler modification, crawler modification, manual API call

---

*This is a read-only daemon continuity report. No code changes authorized.*
