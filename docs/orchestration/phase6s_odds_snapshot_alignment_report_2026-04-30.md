# Phase 6S — Odds Snapshot Alignment Integration Report
## Date: 2026-04-30 | Author: ML Pipeline Automation

---

## 1. Executive Summary

Phase 6S extends the native timestamp infrastructure introduced in Phase 6R by aligning each prediction row to the best available pre-prediction odds snapshot from the TSL odds timeline. This enables `clv_usable = True` for rows where real-time market odds existed before the model made its prediction, unblocking Closing Line Value computation in Phase 6T.

**Verification Token: `PHASE_6S_ODDS_SNAPSHOT_ALIGNMENT_VERIFIED`**

---

## 2. Phase 6S Scope

| Item | Decision |
|------|----------|
| Output format | JSONL (Phase 6J contract `6j-1.0`) |
| Games | 7 real April 30 MLB scheduled games (loaded from odds timeline) |
| Rows | 14 (7 games × 2 sides: home ML + away ML) |
| Model | `mlb_ml_elo_stub_v1.1.0` — Elo rating 30-team table |
| Adapter version | `6s-1.0.0` |
| Timestamp capture version | `6R-1.0` |
| CLV gate | 5-gate check; `clv_usable = True` for all 14 rows |
| `expected_value` | Computed (edge formula: `predicted_prob − implied_prob`) |
| Phase 6T scope | CLV registry conversion, Kelly sizing, closing odds EV |
| Phase 6T blockers | No live betting execution in this phase |

---

## 3. Odds Timeline Source

**File**: `data/mlb_context/odds_timeline.jsonl`  
**Size**: ~4.3 MB  
**Source**: TSL (Taiwan Sports Lottery) pre-game moneyline snapshots  
**Updated at**: `2026-04-30T13:16:xx Z` (last update on April 30)

### 3.1 Record Schema

Each line in `odds_timeline.jsonl` is a JSON object:

```json
{
  "game_id": "MLB-2026_04_30-12_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES",
  "source": "TSL",
  "book": "TSL",
  "market_type": "moneyline",
  "home_team": "Atlanta Braves",
  "away_team": "Detroit Tigers",
  "opening_home_ml": -125,
  "opening_away_ml": -111,
  "decision_home_ml": -125,
  "decision_away_ml": -111,
  "latest_pregame_home_ml": -125,
  "latest_pregame_away_ml": -111,
  "closing_home_ml": -125,
  "closing_away_ml": -111,
  "opening_ts": "2026-04-29T07:32:46Z",
  "decision_ts": "2026-04-30T05:16:54Z",
  "latest_pregame_ts": "2026-04-30T05:16:54Z",
  "commence_time": "2026-05-01T00:15:00+08:00",
  "updated_at": "2026-04-30T13:16:54Z",
  "odds_history": [
    {
      "ts": "2026-04-29T07:32:46Z",
      "home_ml": -125,
      "away_ml": -111,
      "source": "TSL",
      "book": "TSL",
      "snapshot_type": "opening"
    },
    ...
  ]
}
```

### 3.2 `game_id` Format

```
MLB-{YYYY_MM_DD}-{H_MM_AMPM}-{AWAY_TEAM_NAME}-AT-{HOME_TEAM_NAME}
```

Key: **AWAY team precedes `-AT-`, HOME team follows**. This is the inverse of the `canonical_match_id` convention (`baseball:mlb:{DATE}:{HOME}:{AWAY}`).

The `_extract_from_game_id()` helper (in `align_odds_snapshot.py`) correctly parses the `-AT-` separator. A bug was found and fixed during Phase 6S: the time token (`12_15_PM`) uses underscores and is a single hyphen-delimited segment, so team name extraction starts at `tokens[2]`, not `tokens[3]`.

---

## 4. April 30 Games — Odds Snapshot Inventory

All 7 April 30 MLB games had valid TSL pre-game snapshots available before `08:35:10Z` (the Phase 6S adapter prediction time):

| Game ID | Home | Away | Latest Pre-Snap | Home ML | Away ML | Snap Δ Before Pred |
|---------|------|------|-----------------|---------|---------|--------------------|
| `MLB-2026_04_30-12_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES` | ATL | DET | `05:16:54Z` | -125 | -111 | ~3h 18m |
| `MLB-2026_04_30-12_35_PM-ST_LOUIS_CARDINALS-AT-PITTSBURGH_PIRATES` | PIT | STL | `05:16:54Z` | -200 | +160 | ~3h 18m |
| `MLB-2026_04_30-1_10_PM-WASHINGTON_NATIONALS-AT-NEW_YORK_METS` | NYM | WSH | `05:16:54Z` | -222 | +155 | ~3h 18m |
| `MLB-2026_04_30-1_40_PM-ARIZONA_DIAMONDBACKS-AT-MILWAUKEE_BREWERS` | MIL | ARI | `05:16:54Z` | -133 | +100 | ~3h 18m |
| `MLB-2026_04_30-3_05_PM-KANSAS_CITY_ROYALS-AT-OAKLAND_ATHLETICS` | OAK | KC | `05:16:54Z` | -143 | -111 | ~3h 18m |
| `MLB-2026_04_30-5_35_PM-SAN_FRANCISCO_GIANTS-AT-PHILADELPHIA_PHILLIES` | PHI | SFG | `23:49:26Z` (Apr 29) | -154 | +120 | ~8h 46m |
| `MLB-2026_04_30-7_40_PM-TORONTO_BLUE_JAYS-AT-MINNESOTA_TWINS` | MIN | TOR | `05:16:54Z` | +100 | -133 | ~3h 18m |

All snapshots are within the 24-hour STALE threshold → status = **ALIGNED** for all 14 rows.

---

## 5. New Schema Fields (Phase 6S)

Six new fields are attached to each future model output row:

| Field | Type | Description |
|-------|------|-------------|
| `odds_snapshot_ref` | `str` | Reference key: `{game_id}\|{book}\|snap@{ts}` |
| `odds_snapshot_time_utc` | `str` | ISO8601 UTC timestamp of the selected snapshot |
| `implied_probability_at_prediction` | `float` | Vig-inclusive implied probability from market odds |
| `market_odds_at_prediction` | `int` | American moneyline at the selected snapshot |
| `odds_snapshot_source` | `str` | Book/source identifier (e.g., `"TSL"`) |
| `odds_snapshot_alignment_status` | `str` | `ALIGNED` / `MISSING` / `STALE` / `FUTURE_LEAK_BLOCKED` |

`expected_value` (existing field) is now computed: `EV = predicted_probability − implied_probability_at_prediction`

### 5.1 `odds_snapshot_ref` Example

```
MLB-2026_04_30-12_15_PM-DETROIT_TIGERS-AT-ATLANTA_BRAVES|TSL|snap@2026-04-30T05:16:54Z
```

---

## 6. Alignment Logic

### 6.1 Snapshot Selection Priority

For each row (`selection = home` or `away`), `align_odds_snapshot_for_prediction()`:

1. Resolves `(date, home_code, away_code)` from `canonical_match_id` or `prediction_run_id`
2. Searches `odds_history` for entries with `ts ≤ prediction_time_utc`; selects the **latest** (largest `ts` still ≤ pred_time)
3. Falls back to `latest_pregame_ts` → `decision_ts` → `opening_ts` (in that order) if `odds_history` is empty

### 6.2 Alignment Status Rules

| Status | Condition |
|--------|-----------|
| `ALIGNED` | Valid snapshot found; `snap_ts ≤ pred_time`; `snap_ts ≥ pred_time − 24h` |
| `STALE` | Valid snapshot found but `snap_ts < pred_time − 24h` |
| `FUTURE_LEAK_BLOCKED` | All available snapshots have `ts > pred_time` |
| `MISSING` | No record found for `(date, home, away)` pair |

### 6.3 Implied Probability Formula

```
Negative odds (favourites, e.g. -125):  implied = |odds| / (|odds| + 100)
Positive odds (underdogs,  e.g. +110):  implied = 100 / (100 + odds)
```

This is the vig-inclusive (raw) implied probability.

---

## 7. CLV Usability Gate (TASK 4)

`clv_usable = True` requires **all five gates** to pass simultaneously:

| Gate | Check |
|------|-------|
| G1 | `prediction_time_source` ∈ `{MODEL_INFERENCE_RUNTIME, MODEL_OUTPUT_EMISSION_RUNTIME, SCHEDULER_RUN_RUNTIME}` |
| G2 | `odds_snapshot_ref` is not `None` |
| G3 | `odds_snapshot_time_utc ≤ prediction_time_utc` (no post-prediction odds) |
| G4 | `implied_probability_at_prediction ∈ (0, 1)` (non-null, valid float) |
| G5 | `timestamp_quality_flags` contains no hard-fail flags (e.g., `TIMESTAMP_MISSING`, `PREDICTION_TIME_AFTER_MATCH`) |

**Phase 6S result**: All 14 rows → `clv_usable = True`

---

## 8. Validator Results (M1–M13)

**Command**:
```bash
python3 scripts/validate_model_output_contract.py \
  --candidate data/derived/model_outputs_6s_future_2026-04-30.jsonl \
  --report docs/orchestration/phase6s_validator_run_report_2026-04-30.md \
  --summary data/derived/model_output_contract_validation_summary_6s_2026-04-30.json
```

| Gate | Name | Result |
|------|------|--------|
| M1 | `SCHEMA_VALID` | ✅ PASS 14/14 |
| M2 | `CANONICAL_MATCH_ID_PRESENT` | ✅ PASS 14/14 |
| M3 | `MARKET_KEY_PRESENT` | ✅ PASS 14/14 |
| M4 | `SELECTION_KEY_PRESENT` | ✅ PASS 14/14 |
| M5 | `VERSION_FIELDS_PRESENT` | ✅ PASS 14/14 |
| M6 | `TIMING_VALID` | ✅ PASS 14/14 |
| M7 | `PROBABILITY_VALID` | ✅ PASS 14/14 |
| M8 | `EV_VALID_OR_NULL_WITH_REASON` | ✅ PASS 14/14 |
| M9 | `NO_LEAKAGE_HARD_FAIL` | ✅ PASS 14/14 |
| M10 | `MARKET_SEMANTICS_VALID` | ✅ PASS 14/14 |
| M11 | `CLV_USABLE_FLAG_CORRECT` | ✅ PASS 14/14 |
| M12 | `DRY_RUN_FLAG_CORRECT` | ✅ PASS 14/14 |
| M13 | `NATIVE_TIMESTAMP_CONTRACT` | ✅ PASS 14/14 |

**Readiness decision: `READY_FOR_MODEL_OUTPUT_ADAPTER`**

---

## 9. Sample Output Rows (Home Side)

| canonical_match_id | Sel | Market Odds | Implied Prob | Elo Pred Prob | EV | CLV Usable |
|--------------------|-----|-------------|--------------|---------------|----|------------|
| `baseball:mlb:20260430:ATL:DET` | home | -125 | 0.5556 | 0.6199 | +0.0644 | ✅ |
| `baseball:mlb:20260430:PIT:STL` | home | -200 | 0.6667 | 0.5000 | -0.1667 | ✅ |
| `baseball:mlb:20260430:NYM:WSH` | home | -222 | 0.6894 | 0.6788 | -0.0106 | ✅ |
| `baseball:mlb:20260430:MIL:ARI` | home | -133 | 0.5708 | 0.5715 | +0.0006 | ✅ |
| `baseball:mlb:20260430:OAK:KC` | home | -143 | 0.5885 | 0.5072 | -0.0813 | ✅ |
| `baseball:mlb:20260430:PHI:SFG` | home | -154 | 0.6063 | 0.6467 | +0.0404 | ✅ |
| `baseball:mlb:20260430:MIN:TOR` | home | +100 | 0.5000 | 0.5573 | +0.0573 | ✅ |

> **Note**: EV = Elo predicted probability − vig-inclusive implied probability. Negative EV rows (PIT, NYM, OAK home sides) indicate the Elo model rates the home team below the market. This is expected — Elo is a stub model and closing odds EV is deferred to Phase 6T.

---

## 10. Timestamp Pipeline (5 Stages)

All five stages captured via `NativeTimestampCapture` (`scripts/native_timestamp_helper.py`):

| Stage | Field | Capture Point |
|-------|-------|--------------|
| 1 | `prediction_run_started_at_utc` | Adapter entry point |
| 2 | `feature_cutoff_time_utc` | After odds timeline loaded |
| 3 | `prediction_time_utc` | After Elo inference |
| 4 | `prediction_run_completed_at_utc` | After all rows built |
| 5 | `model_output_written_at_utc` | After JSONL written |

**Timing chain violations: 0**  
**`timestamp_capture_version`**: `6R-1.0`  
**`prediction_time_source`**: `MODEL_INFERENCE_RUNTIME`  
**`feature_cutoff_source`**: `MLB_SCHEDULE_LOAD_TIME`

---

## 11. Test Results (31 Tests)

**File**: `tests/test_phase6s_odds_snapshot_alignment.py`

```
31 passed in 0.10s
```

| Test | Result |
|------|--------|
| `test_chooses_latest_snapshot_before_prediction_time` | ✅ PASS |
| `test_rejects_snapshot_after_prediction_time` | ✅ PASS |
| `test_handles_missing_snapshot_with_status_missing` | ✅ PASS |
| `test_computes_implied_probability_correctly` (×6 params) | ✅ PASS |
| `TestClvUsabilityGate` (×7 subtests) | ✅ PASS |
| `test_clv_usable_true_only_when_gates_pass` | ✅ PASS |
| `test_historical_files_unchanged` | ✅ PASS |
| `test_validator_passes_for_aligned_rows` | ✅ PASS |
| `TestOddsTimelineLoader` (×6 subtests) | ✅ PASS |
| `TestAlignOddsSnapshot` (×3 subtests) | ✅ PASS |
| `test_adapter_row_count` | ✅ PASS |
| `test_adapter_clv_usable_true_for_aligned_rows` | ✅ PASS |
| `test_adapter_no_post_prediction_leakage` | ✅ PASS |

---

## 12. Files Created / Modified

| File | Action | Purpose |
|------|--------|---------|
| `scripts/align_odds_snapshot.py` | Created | Odds snapshot alignment helper; `OddsTimelineLoader`, `align_odds_snapshot_for_prediction()`, `american_to_implied()` |
| `scripts/build_ml_future_model_outputs_6s.py` | Created | Phase 6S adapter: real April 30 games, alignment integrated, CLV gate |
| `data/derived/model_outputs_6s_future_2026-04-30.jsonl` | Created | 14 rows, all `ALIGNED`, all `clv_usable=True` |
| `tests/test_phase6s_odds_snapshot_alignment.py` | Created | 31-test suite |
| `docs/orchestration/phase6s_validator_run_report_2026-04-30.md` | Created | Validator run report |
| `data/derived/model_output_contract_validation_summary_6s_2026-04-30.json` | Created | Validator summary JSON |
| `scripts/native_timestamp_helper.py` | Unchanged (Phase 6R) | |
| `scripts/build_ml_future_model_outputs.py` | Unchanged (Phase 6R) | |
| `data/derived/model_outputs_2026-04-29.jsonl` | Unchanged (2,986 rows) | Historical rows untouched |

---

## 13. Phase 6T Blockers

The following are explicitly out of scope for Phase 6S and are blocked for Phase 6T:

1. **CLV registry conversion** — Store `clv_usable` rows in a persistent CLV registry (database/index) for downstream lookup
2. **Closing odds EV** — `expected_value` in Phase 6S uses the edge formula (`pred_prob − implied_prob`). Phase 6T should recompute using closing line: `EV_closing = pred_prob × (closing_odds / 100) − (1 − pred_prob)`
3. **Kelly sizing** — Fractional Kelly position sizing requires CLV registry + bankroll state
4. **Live betting execution** — No bet submission in Phase 6S; all outputs are advisory only

---

## 14. What Was Verified

- [x] All 7 real April 30 MLB games loaded from canonical odds timeline
- [x] All 14 rows have `odds_snapshot_alignment_status = ALIGNED`
- [x] All 14 rows have `clv_usable = True`
- [x] No post-prediction odds leakage (`snap_ts ≤ pred_time` for all rows)
- [x] `expected_value` computed and non-null for all 14 rows (M8 PASS)
- [x] `match_time_utc` normalized to `Z` format from `+HH:MM` timezone offsets (M6 PASS)
- [x] M1–M13 validator gates: **all PASS 14/14**
- [x] 31/31 tests pass
- [x] Historical file (`model_outputs_2026-04-29.jsonl`, 2,986 rows) untouched
- [x] Phase 6R adapter and Phase 6Q dry-run adapter untouched

---

**PHASE_6S_ODDS_SNAPSHOT_ALIGNMENT_VERIFIED**
