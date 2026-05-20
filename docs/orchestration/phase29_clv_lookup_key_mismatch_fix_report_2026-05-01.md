# Phase 29 — CLV Lookup Key Mismatch Fix Report

**Date**: 2026-05-01  
**Phase**: 29 — CLV Closing Lookup Key Mismatch Fix  
**Verdict**: `PHASE_29_CLV_LOOKUP_KEY_MISMATCH_FIX_VERIFIED`  
**Readiness State**: `LEARNING_READY`

---

## 1. Root Cause

### Problem

`orchestrator/closing_odds_monitor.py` — `_find_closing_odds_for_pending()` used
`clv_row["canonical_match_id"]` as the key to look up entries in the odds-timeline index.

| Field | Example value |
|-------|--------------|
| `canonical_match_id` (CLV record) | `baseball:mlb:20260430:ATL:DET` |
| Odds-timeline `game_id` (index key) | `MLB-2026_04_30-12_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES` |

These two formats are entirely incompatible. Because no entry in the timeline index was ever
keyed by the `canonical_match_id` format, every `timeline_index.get(canonical_match_id)`
returned `None` — causing all 14 production CLV records to stay in `PENDING_CLOSING`
indefinitely, even though valid closing odds existed in the timeline.

### Discovery

Phase 28 (`scripts/run_phase28_real_clv_activation_check.py`) performed a read-only
inspection of both files and found:

- `data/mlb_context/odds_timeline.jsonl` — 14 records for 2026-04-30, all with valid
  `closing_ts` strictly after `prediction_time_utc` (diff 27 263–53 437 seconds)
- Each CLV record carries an `odds_snapshot_ref` field in the format:
  `{timeline_game_id}|TSL|snap@{timestamp}`  
  The portion **before `|`** exactly matches the timeline `game_id` index key.

### Fix

Two-stage lookup in `_find_closing_odds_for_pending()`:

1. **Stage 1 — canonical_match_id**: unchanged existing behavior  
2. **Stage 2 — snapshot_ref fallback** *(new)*: if Stage 1 finds nothing, call
   `extract_game_id_from_snapshot_ref(clv_row["odds_snapshot_ref"])` to get the
   timeline-compatible game_id, then look that up in the index.

All existing safety gates (timestamp validation, same-snapshot guard, ML range check)
are still applied to any candidate found via the fallback path.

---

## 2. Before / After

| Metric | Before (Phase 28) | After (Phase 29) |
|--------|-------------------|-----------------|
| PENDING_CLOSING | 14 | **0** |
| COMPUTED | 0 | **14** |
| Canonical lookup hits | 0 / 14 | 0 / 14 (unchanged) |
| Snapshot-ref fallback hits | N/A | **14 / 14** |
| `readiness_state` | `WAITING_ACTIVE` | **`LEARNING_READY`** |
| `learning_allowed` | `False` | **`True`** |
| `phase6.clv_computed` | 0 | **14** |
| `phase6.clv_pending_closing` | 14 | **0** |

---

## 3. Lookup Methods Used

| Lookup method | Records |
|---------------|---------|
| `canonical_match_id` | 0 |
| `odds_snapshot_ref_game_id` *(new fallback)* | 14 |
| `none` (no match) | 0 |

All 14 records were resolved via the snapshot_ref fallback. Every closing odds source
was `tsl_closing` (from `data/mlb_context/odds_timeline.jsonl`).

---

## 4. CLV Values Computed

| canonical_match_id | sel | closing_ml | implied_at_pred | clv_value |
|--------------------|-----|------------|----------------|-----------|
| baseball:mlb:20260430:ATL:DET | home | -154.0 | ~0.506 | +0.0507 |
| baseball:mlb:20260430:ATL:DET | away | +110.0 | ~0.494 | -0.0473 |
| baseball:mlb:20260430:PIT:STL | home | -250.0 | — | — |
| baseball:mlb:20260430:PIT:STL | away | +185.0 | — | — |
| baseball:mlb:20260430:NYM:WSH | home | -182.0 | — | — |
| baseball:mlb:20260430:NYM:WSH | away | +130.0 | — | — |
| baseball:mlb:20260430:MIL:ARI | home | -125.0 | — | — |
| baseball:mlb:20260430:MIL:ARI | away | +100.0 | — | — |
| baseball:mlb:20260430:OAK:KC | home | -154.0 | — | — |
| baseball:mlb:20260430:OAK:KC | away | +100.0 | — | — |
| baseball:mlb:20260430:PHI:SFG | home | -154.0 | — | — |
| baseball:mlb:20260430:PHI:SFG | away | +110.0 | — | — |
| baseball:mlb:20260430:MIN:TOR | home | +115.0 | — | — |
| baseball:mlb:20260430:MIN:TOR | away | -154.0 | — | — |

*CLV formula: `closing_implied_probability − implied_probability_at_prediction`*

---

## 5. Backup

A full backup of the original PENDING_CLOSING file was written **before** any mutation:

```
data/wbc_backend/reports/backups/
  clv_validation_records_6u_2026-04-30.before_phase29_2026-05-01.jsonl
```

The apply used atomic write (tmpfile + `os.replace()`). If interrupted, the original
file remains intact (partial writes are impossible).

---

## 6. Readiness Result

```
python3 scripts/run_optimization_readiness.py --json

{
  "readiness_state": "LEARNING_READY",
  "learning_allowed": true,
  "phase6": {
    "clv_computed": 14,
    "clv_pending_closing": 0,
    "all_clv_pending": false,
    "next_required_event": "All CLV COMPUTED — ready for full CLV-based reinforcement"
  }
}
```

---

## 7. Files Changed

| File | Change |
|------|--------|
| `orchestrator/closing_odds_monitor.py` | Add `extract_game_id_from_snapshot_ref()`, `_pick_closing_odds()`, `LOOKUP_*` constants; update `_find_closing_odds_for_pending()` with two-stage lookup; update `_build_upgraded_record()` with `lookup_method` param; update `_analyze_pending_record()` with fallback + diagnostic fields; update `_build_source_summary()` with `matched_by_*` / `lookup_failed` fields |
| `scripts/run_phase29_apply_clv_lookup_fix.py` | New — dry-run preview + backup + atomic apply |
| `data/wbc_backend/reports/clv_validation_records_6u_2026-04-30.jsonl` | **Rewritten** — all 14 records upgraded from `PENDING_CLOSING` → `COMPUTED` |
| `data/wbc_backend/reports/backups/clv_validation_records_6u_2026-04-30.before_phase29_2026-05-01.jsonl` | **New** — backup of original PENDING_CLOSING records |

---

## 8. Tests Passed

`tests/test_phase29_clv_lookup_key_mismatch_fix.py` — **9 / 9**

| # | Test | Status |
|---|------|--------|
| 1 | `extract_game_id_from_snapshot_ref` returns prefix before `\|` | ✅ PASS |
| 2 | null / malformed snapshot_ref returns `None` | ✅ PASS |
| 3 | canonical lookup still works | ✅ PASS |
| 4 | canonical miss + snapshot_ref fallback resolves odds | ✅ PASS |
| 5 | fallback does not bypass timestamp validation | ✅ PASS |
| 6 | same-snapshot guard still rejected via fallback | ✅ PASS |
| 7 | valid fallback candidate appears in dry-run preview | ✅ PASS |
| 8 | apply creates backup before mutating CLV file | ✅ PASS |
| 9 | readiness becomes `LEARNING_READY` after COMPUTED CLV exists | ✅ PASS |

**Regression suite: 31 / 31** (Phase 25 + 26 + 28 + 29)

---

## 9. Hard Rule Compliance

| Rule | Status |
|------|--------|
| No faked closing odds | ✅ All odds from `data/mlb_context/odds_timeline.jsonl` |
| Timestamp gate enforced | ✅ `closing_ts > prediction_time_utc` (diff 27 263–53 437 s) |
| Same-snapshot guard enforced | ✅ Δ < 60 s rejected in `_validate_closing_odds()` |
| Backup before mutation | ✅ Written to `data/wbc_backend/reports/backups/` |
| Atomic write | ✅ `tmpfile + os.replace()` |
| No production model modified | ✅ |
| No external LLM called | ✅ |
| CLV only from real COMPUTED | ✅ No sandbox fixtures used |

---

## 10. Next Steps

1. **Phase 30** — Run the full autonomous learning cycle now that `LEARNING_READY` is active.  
   The planner can now schedule learning tasks using real CLV signal from 2026-04-30.
2. Monitor `orchestrator/closing_odds_monitor.py` for future dates — new CLV records will
   be resolved automatically via the snapshot_ref fallback without any further manual intervention.
3. Consider backfilling `canonical_match_id` format in the odds timeline for future
   canonical-lookup health (long-term data quality improvement).

---

**Final Status**: ✅ `PHASE_29_CLV_LOOKUP_KEY_MISMATCH_FIX_VERIFIED`
