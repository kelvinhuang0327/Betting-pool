# Phase 6U — CLV Validation Record Generation Report
**Date:** 2026-04-30  
**Verification Token:** `PHASE_6U_CLV_RECORD_GENERATION_VERIFIED`

---

## Summary

Phase 6U is the **final stage of Phase 6**. It generates CLV (Closing Line Value)
validation records exclusively from Phase 6T prediction registry rows, after all
registry and data-quality gates pass.

| Metric | Value |
|---|---|
| Source registry rows | 14 |
| Eligible (G1–G8 pass) | 14 |
| Blocked (gate fail) | 0 |
| Skipped (duplicate) | 0 |
| CLV records written | 14 |
| → COMPUTED | 0 |
| → PENDING_CLOSING | 14 |
| Validation errors | 0 |
| Test suite | 69/69 PASS (0.10s) |

---

## Architecture

### Source Constraint
Phase 6U consumes **only** from `data/wbc_backend/reports/prediction_registry_6t_2026-04-30.jsonl`
(Phase 6T output, 14 rows). Raw model outputs are never used directly.

### Gate Chain (G1–G9)

| Gate | Field | Condition |
|---|---|---|
| G1 | `clv_usable` | Must be `True` |
| G2 | `odds_snapshot_ref` | Must be non-empty |
| G3 | `odds_snapshot_time_utc` | Must be ≤ `prediction_time_utc` (no future leak) |
| G4 | `expected_value` | Must be present |
| G5 | `execution_mode` | Must be `RESEARCH_ONLY` or `PAPER_ONLY` |
| G6 | `live_bet_submitted` | Must be `False` |
| G7 | `governance_status` | Must be `VALIDATED_ML_ONLY` |
| G8 | `timestamp_quality_flags` | No hard-fail flags |
| G9 | Closing odds | Available → COMPUTED; not available → PENDING_CLOSING |

### CLV Status Logic

```
COMPUTED        — closing_ts strictly after prediction_time_utc, closing_ml present
PENDING_CLOSING — no valid closing odds yet (game in future, or pre-prediction snapshot)
BLOCKED         — a G1–G8 gate failed (record excluded from output)
```

### CLV Formula (when COMPUTED)
```
closing_implied_prob = american_to_implied(closing_ml)
clv_value = closing_implied_prob - implied_probability_at_prediction
```
Positive CLV = beat the closing line (favorable market movement).

### Closing Odds Priority
1. `external_closing_home/away_ml` (OddsAPI / Pinnacle) — when `external_closing_ts > prediction_time_utc`
2. `closing_home/away_ml` (TSL fallback) — when `closing_ts > prediction_time_utc`

The critical constraint: closing timestamp **must be strictly after** `prediction_time_utc`.
This prevents the pre-game snapshot (used for Phase 6S odds alignment) from being
double-counted as a "closing line."

### Selection-Aware Lookup
- `selection = "home"` → home ML fields (`closing_home_ml`, `external_closing_home_ml`)
- `selection = "away"` → away ML fields (`closing_away_ml`, `external_closing_away_ml`)

### Idempotency
Dedup key: `(prediction_id, odds_snapshot_ref, selection)` — 3-tuple.  
Second run with identical input produces 0 new records.

---

## April 30 Output — PENDING_CLOSING (Expected)

All 14 records are correctly `PENDING_CLOSING` because:

- `prediction_time_utc = 2026-04-30T08:35:10Z` (predictions made at 08:35 AM)
- `closing_ts = 2026-04-30T05:16:54Z` (TSL snapshot at 05:16 AM — **before** prediction)
- `external_closing_home_ml = None` for all April 30 games

The odds timeline's `closing_home_ml` for April 30 is the **same pre-game snapshot**
captured for Phase 6S odds alignment — it is not a true post-game closing line.
April 30 games start at 12:15 PM–7:40 PM EDT; true closing odds are only
available after each game starts.

| Game | Selection | EV | CLV Status |
|---|---|---|---|
| ATL vs DET | home | +0.0644 | PENDING_CLOSING |
| ATL vs DET | away | −0.1460 | PENDING_CLOSING |
| STL vs PIT | home | −0.1667 | PENDING_CLOSING |
| STL vs PIT | away | +0.1154 | PENDING_CLOSING |
| WSH vs NYM | home | −0.0106 | PENDING_CLOSING |
| WSH vs NYM | away | −0.0710 | PENDING_CLOSING |
| ARI vs MIL | home | +0.0006 | PENDING_CLOSING |
| ARI vs MIL | away | −0.0715 | PENDING_CLOSING |
| KC vs OAK | home | −0.0813 | PENDING_CLOSING |
| KC vs OAK | away | −0.0333 | PENDING_CLOSING |
| SFG vs PHI | home | +0.0404 | PENDING_CLOSING |
| SFG vs PHI | away | −0.1012 | PENDING_CLOSING |
| TOR vs MIN | home | +0.0573 | PENDING_CLOSING |
| TOR vs MIN | away | −0.1281 | PENDING_CLOSING |

---

## Output Files

| File | Description |
|---|---|
| `data/wbc_backend/reports/clv_validation_records_6u_2026-04-30.jsonl` | 14 CLV records |
| `data/wbc_backend/reports/clv_validation_records_6u_summary_2026-04-30.json` | Run summary |

### CLV Record Schema (33 fields)

```
clv_record_id            — deterministic uuid5: "6u-{prediction_id}:{snap_ref}:{selection}"
prediction_id            — from 6T registry (provenance link)
canonical_match_id       — e.g. "baseball:mlb:20260430:ATL:DET"
game_id                  — e.g. "MLB-2026_04_30-12_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES"
league                   — "MLB"
market_type              — "moneyline"
selection                — "home" | "away"
predicted_probability    — model output
implied_probability_at_prediction  — from Phase 6S odds snapshot
market_odds_at_prediction          — American ML at snapshot time
expected_value           — EV = predicted_prob - implied_prob
odds_snapshot_ref        — audit reference to odds snapshot
odds_snapshot_time_utc   — when the pre-prediction snapshot was captured
prediction_time_utc      — when prediction was generated
event_start_time_utc     — scheduled game start
closing_odds             — American ML at closing time (None if PENDING)
closing_implied_probability        — implied prob at closing (None if PENDING)
closing_odds_time_utc    — closing odds timestamp (None if PENDING)
closing_odds_source      — "external" | "tsl" | None
clv_value                — closing_implied - implied_at_prediction (None if PENDING)
clv_status               — COMPUTED | PENDING_CLOSING | BLOCKED
block_reason             — rejection reason (None unless BLOCKED)
execution_mode           — "RESEARCH_ONLY"
governance_status        — "VALIDATED_ML_ONLY"
source_model             — e.g. "mlb_moneyline_v1"
signal_state_type        — "ML_ONLY_FUTURE_PREGAME"
source_registry_file     — path to 6T registry (provenance)
clv_schema_version       — "6u-1.0"
source_phase             — "6U"
created_at_utc           — record creation timestamp
prediction_time_source   — from 6O chain
timestamp_capture_version — from 6O chain
timestamp_quality_flags  — from 6O chain
```

---

## Test Suite

**File:** `tests/test_phase6u_clv_record_generation.py`  
**Result:** 69/69 PASS in 0.10s

### Test Classes

| Class | Tests | Description |
|---|---|---|
| `TestT1Computed` | 5 | COMPUTED status, fields, formula, no validation errors |
| `TestT2PendingStaleTs` | 4 | closing_ts before prediction_time → PENDING |
| `TestT3PendingNoTimeline` | 1 | Game not in timeline → PENDING |
| `TestT4BlockedCLVUnusable` | 3 | G1 gate — clv_usable=False blocked |
| `TestT5BlockedLiveBet` | 3 | G6 gate — live_bet_submitted=True blocked |
| `TestT6Idempotency` | 3 | Second run = 0 new records; key stability |
| `TestT7ClosingPriority` | 3 | External > TSL; stale external fallback |
| `TestT8FutureLeakG3` | 2 | G3 gate — odds_snapshot after prediction blocked |
| `TestT9SummaryCounts` | 2 | Stats totals correct |
| `TestT10FullStackApril30` | 13 | 14 records, all PENDING, 0 errors, 7 games, pairs |
| `TestT11CLVFormula` | 3 | Positive, negative CLV; 6dp rounding |
| `TestT12SelectionAware` | 4 | Home/away get correct ML from home/away fields |
| `TestT13DedupKey` | 4 | Key is 3-tuple; components correct |
| `TestT14ValidateComputed` | 3 | COMPUTED — valid passes; missing fields fail |
| `TestT15ValidatePending` | 1 | PENDING with clv_value → error |
| `TestT16ValidateBlocked` | 1 | BLOCKED without block_reason → error |
| `TestT17NoLiveBetField` | 2 | live_bet_submitted absent from records |
| `TestT18ExecutionModeGate` | 3 | G5 — LIVE_ONLY blocked; RESEARCH/PAPER allowed |
| `TestT19GovernanceGate` | 2 | G7 — wrong governance blocked |
| `TestT20TimestampFlagGate` | 3 | G8 — hard-fail flag blocked |
| `TestAmericanToImplied` | 4 | Conversion formula correctness |

---

## Implementation Files

| File | Role |
|---|---|
| `scripts/generate_clv_records_6u.py` | CLV record generator (Phase 6U) |
| `tests/test_phase6u_clv_record_generation.py` | 69-test suite |
| `data/wbc_backend/reports/clv_validation_records_6u_2026-04-30.jsonl` | 14 CLV records |
| `data/wbc_backend/reports/clv_validation_records_6u_summary_2026-04-30.json` | Run summary |

---

## Phase 6 Completion

All Phase 6 sub-phases are now complete:

| Phase | Token | Description |
|---|---|---|
| 6R | `PHASE_6R_ML_ONLY_TIMESTAMP_INTEGRATION_VERIFIED` | Native timestamp fields |
| 6S | `PHASE_6S_ODDS_SNAPSHOT_ALIGNMENT_VERIFIED` | Odds alignment + CLV gate |
| 6T | `PHASE_6T_REGISTRY_CONVERSION_VERIFIED` | Registry conversion |
| 6U | `PHASE_6U_CLV_RECORD_GENERATION_VERIFIED` | CLV validation records |

---

## Hard Rules Enforced

- CLV generated only from Phase 6T registry (never raw model output)
- Phase 6T registry gates are not bypassed
- Future odds are never used as closing lines (strict `closing_ts > prediction_time_utc`)
- `PENDING_CLOSING` records never carry `clv_value`
- `live_bet_submitted` field is absent from all CLV records
- Production `data/wbc_backend/reports/prediction_registry.jsonl` (66 WBC rows) not touched
- Historical rows not modified
