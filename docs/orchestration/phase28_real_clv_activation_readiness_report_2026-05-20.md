# Phase 28 — Real CLV Activation Readiness Report

**Date**: 2026-05-20  
**Generated at**: 2026-05-20T09:51:22.811634+00:00  
**Phase**: 28 — Real CLV Activation Readiness Check  
**Verdict**: `PHASE_28_REAL_CLV_ACTIVATION_READINESS_VERIFIED`  
**Activation Decision**: `READY_TO_COMPUTE`

---

## 1. CLV File Inventory

| File | Records | PENDING | COMPUTED |
|------|---------|---------|---------|
| `data/wbc_backend/reports/clv_validation_records_6u_2026-04-30.jsonl` | 1 | 1 | 0 |
| `data/mlb_context/odds_timeline.jsonl` | (timeline) | — | — |

**Status**: All 1 production CLV records are `PENDING_CLOSING`.  No real `COMPUTED` CLV exists yet.

---

## 2. Root Cause — Closing Monitor Game-ID Mismatch

The current `closing_odds_monitor.py` uses `clv_row["canonical_match_id"]` as the key
to look up entries in the odds-timeline index. However, the timeline index is keyed by its
own `game_id` field.  These two formats are incompatible:

| Field | Example value |
|-------|--------------|
| `canonical_match_id` | `baseball:mlb:20260430:ATL:DET` |
| Odds-timeline `game_id` | `MLB-2026_04_30-12_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES` |

Because they never match, the monitor silently reports all records as
`no closing odds found` and leaves them in `PENDING_CLOSING` indefinitely.

**Resolution (Phase 29)**: Update the monitor to fall back to the game-id portion of
`odds_snapshot_ref` when the canonical-match-id lookup fails. The `odds_snapshot_ref` field
already contains the correct timeline `game_id` prefix:

```
odds_snapshot_ref = "MLB-2026_04_30-12_15_PM-...-AT-ATLANTA_BRAVES|TSL|snap@..."
                      ↑ this portion matches the odds-timeline game_id key
```

---

## 3. Closing Odds Candidate Evaluation

### 3.1 Current Monitor Behavior (broken)

| Metric | Value |
|--------|-------|
| Pending records inspected | 1 |
| Timeline entries found (canonical lookup) | 0 |
| Valid candidates found | 0 |
| Would upgrade to COMPUTED | 0 |
| Block reason | `game_id_mismatch_canonical_vs_timeline_key` |

### 3.2 Improved Matching (snapshot-ref, implemented in Phase 29)

| Metric | Value |
|--------|-------|
| Pending records inspected | 1 |
| Timeline entries found (snapshot_ref lookup) | 1 |
| Valid candidates found | 1 |
| Would upgrade to COMPUTED | 1 |
| Would remain PENDING | 0 |

---

## 4. Per-Record Decision Table

| prediction_id | match | sel | snapshot_game_id | closing_ml | closing_ts | would_compute | block_reason |
|---------------|-------|-----|-----------------|------------|------------|--------------|------------|
| `pred_001` | `baseball:mlb:20260430:ATL:DET` | home | `2_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES` | -154.0 | 2026-04-30T16:09:33 | ✓ | — |

---

## 5. Closing Sources Evaluated

| Source | Records with data | Used in preview |
|--------|-----------------|----------------|
| `data/mlb_context/odds_timeline.jsonl` — `closing_{side}_ml` | 1 | Primary |
| `data/mlb_context/odds_timeline.jsonl` — `external_closing_{side}_ml` | 0 | Secondary |
| `data/tsl_odds_history.jsonl` — pre-game snapshots | 0 | Not valid (all pre-game, fetched before prediction) |
| External API | 0 | Not available (no external_closing_ts in timeline for 2026-04-30) |

---

## 6. Activation Decision

**Decision**: `READY_TO_COMPUTE`

Valid closing odds exist in `data/mlb_context/odds_timeline.jsonl` for at least
1 of 1 pending CLV records.

**Required action** (Phase 29):

1. Update `orchestrator/closing_odds_monitor.py` — in `_find_closing_odds_for_pending()`
   and `_analyze_pending_record()`, add a fallback lookup using the game_id extracted
   from `clv_row["odds_snapshot_ref"]` when the canonical-match-id lookup returns None.
2. Run `python3 orchestrator/closing_odds_monitor.py --date 2026-04-30`.
3. Verify upgraded file is written to `data/wbc_backend/reports/`.
4. Confirm `optimization_state.classify()` returns `DATA_READY`.
5. System enters `LEARNING_READY` — planner may schedule learning tasks.

---

## 7. Production Readiness Impact

| State | Value |
|-------|-------|
| Current state | `WAITING_ACTIVE` |
| After Phase 29 fix + monitor run | `LEARNING_READY` (if decision = READY_TO_COMPUTE) |
| learning_allowed after fix | `True` |
| sandbox CLV used for this determination | No — production CLV records only |

---

## 8. Recommended Next Actions

1. **Phase 29** — Fix closing monitor game-id matching (snapshot-ref fallback).
2. Run monitor with `--date 2026-04-30` and verify upgraded JSONL is created.
3. Confirm `get_phase6_status()` returns at least one `COMPUTED` record.
4. Run `python3 scripts/run_optimization_readiness.py --print` → `LEARNING_READY`.
5. Monitor LLM audit card once planner begins scheduling learning tasks.

---

**Final Status**: ✅ `PHASE_28_REAL_CLV_ACTIVATION_READINESS_VERIFIED`
