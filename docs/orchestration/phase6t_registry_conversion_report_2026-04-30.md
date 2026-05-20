# Phase 6T — ML-Only Prediction Registry Conversion Report
**Date:** 2026-04-30  
**Phase:** 6T  
**Status:** ✅ COMPLETE — `PHASE_6T_REGISTRY_CONVERSION_VERIFIED`

---

## 1. Summary

Phase 6T converts validated Phase 6S ML-only model output rows into flat
prediction registry rows. All 14 rows from the April 30 Phase 6S run passed
all eligibility gates and were written to the Phase 6T registry.

| Metric | Value |
|---|---|
| Source rows (Phase 6S) | 14 |
| Converted (Phase 6T) | **14** |
| Rejected | 0 |
| Idempotency (2nd run) | 0 new rows (all 14 deduped) |
| Tests | **41 / 41 PASS** |
| Execution mode | `RESEARCH_ONLY` |
| Governance status | `VALIDATED_ML_ONLY` |
| Live bets activated | **0** |

---

## 2. Input

- **Source:** `data/derived/model_outputs_6s_future_2026-04-30.jsonl`
- **Schema version:** `6j-1.0`
- **Phase:** 6S
- **Games:** 7 April 30 MLB games × 2 sides = 14 rows
- **All rows:** `clv_usable=True`, `odds_snapshot_alignment_status=ALIGNED`

---

## 3. Eligibility Gates

Phase 6T enforces 7 eligibility gates. All 14 source rows passed all gates.

| Gate | Rule | Source rows passing |
|---|---|---|
| G1 | `clv_usable = True` | 14 / 14 |
| G2 | `odds_snapshot_alignment_status = ALIGNED` | 14 / 14 |
| G3 | `odds_snapshot_ref` present | 14 / 14 |
| G4 | `expected_value` present (non-null) | 14 / 14 |
| G5 | No future odds leakage (`snap_ts ≤ pred_ts`) | 14 / 14 |
| G6 | No hard-fail `timestamp_quality_flags` | 14 / 14 |
| G7 | `prediction_time_source` in allowed set + M13 chain fields present | 14 / 14 |

---

## 4. Registry Output

**File:** `data/wbc_backend/reports/prediction_registry_6t_2026-04-30.jsonl`  
**Summary:** `data/wbc_backend/reports/prediction_registry_6t_summary_2026-04-30.json`  
**Registry schema version:** `6t-1.0`

### 4.1 April 30 Registry Rows

| Canonical Match ID | Side | Market Odds | Pred Prob | EV |
|---|---|---|---|---|
| baseball:mlb:20260430:ATL:DET | home | -125 | 0.6199 | **+0.064385** |
| baseball:mlb:20260430:ATL:DET | away | -111 | 0.3801 | -0.146007 |
| baseball:mlb:20260430:PIT:STL | home | -200 | 0.5000 | -0.166667 |
| baseball:mlb:20260430:PIT:STL | away | +160 | 0.5000 | **+0.115385** |
| baseball:mlb:20260430:NYM:WSH | home | -222 | 0.6788 | -0.010624 |
| baseball:mlb:20260430:NYM:WSH | away | +155 | 0.3212 | -0.070974 |
| baseball:mlb:20260430:MIL:ARI | home | -133 | 0.5715 | **+0.000648** |
| baseball:mlb:20260430:MIL:ARI | away | +100 | 0.4285 | -0.071463 |
| baseball:mlb:20260430:OAK:KC | home | -143 | 0.5072 | -0.081282 |
| baseball:mlb:20260430:OAK:KC | away | -111 | 0.4928 | -0.033261 |
| baseball:mlb:20260430:PHI:SFG | home | -154 | 0.6467 | **+0.040370** |
| baseball:mlb:20260430:PHI:SFG | away | +120 | 0.3533 | -0.101214 |
| baseball:mlb:20260430:MIN:TOR | home | +100 | 0.5573 | **+0.057312** |
| baseball:mlb:20260430:MIN:TOR | away | -133 | 0.4427 | -0.128127 |

**Positive EV rows:** 5 of 14 (36%)  
**Max EV:** +0.115385 (PIT:STL away, +160 ML)  
**Min EV:** -0.166667 (PIT:STL home, -200 ML — model disagreed with heavy favourite pricing)

### 4.2 Registry Row Schema

Each registry row contains 50 fields across these groups:

| Group | Fields |
|---|---|
| Identity | `prediction_id`, `source_model_output_id`, `prediction_run_id` |
| Match | `canonical_match_id`, `game_id`, `sport`, `league`, `home_team_code`, `away_team_code`, `event_start_time_utc` |
| Market | `market_type`, `market_key`, `selection`, `selection_key`, `market_line` |
| Probabilities | `predicted_probability`, `implied_probability_at_prediction`, `expected_value`, `market_odds_at_prediction` |
| Odds snapshot | `odds_snapshot_ref`, `odds_snapshot_time_utc`, `odds_snapshot_source`, `odds_snapshot_alignment_status` |
| Timestamp chain (6O) | `prediction_time_utc`, `feature_cutoff_time_utc`, `prediction_run_started_at_utc`, `prediction_run_completed_at_utc`, `model_output_written_at_utc`, `prediction_time_source`, `feature_cutoff_source`, `timestamp_capture_version`, `timestamp_quality_flags` |
| CLV / governance | `clv_usable`, `governance_status`, `execution_mode`, `signal_state_type` |
| Live execution (blocked) | `live_bet_submitted=False`, `live_bet_stake=None`, `live_bet_ref=None` |
| Provenance | `source_model`, `model_family`, `model_version`, `feature_version`, `adapter_version`, `phase` |
| Quality | `model_quality_flags`, `data_quality_flags`, `dry_run` |
| Schema / audit | `validation_schema_version`, `registry_schema_version`, `created_at_utc` |

---

## 5. Governance

All registry rows carry hard governance values that cannot be overridden at
conversion time:

| Field | Value | Enforcement |
|---|---|---|
| `execution_mode` | `RESEARCH_ONLY` | Hard-coded constant in converter |
| `governance_status` | `VALIDATED_ML_ONLY` | Hard-coded constant in converter |
| `live_bet_submitted` | `False` | Always set to `False` |
| `live_bet_stake` | `None` | Always set to `None` |
| `live_bet_ref` | `None` | Always set to `None` |
| `signal_state_type` | `ML_ONLY_FUTURE_PREGAME` | Hard-coded constant |

`validate_registry_row()` rejects any row where `execution_mode` is not
`PAPER_ONLY` or `RESEARCH_ONLY`, or where `live_bet_submitted=True`, or where
`live_bet_ref` is set.

---

## 6. Idempotency

The deduplication key is the 5-tuple:

```
(canonical_match_id, market_type, selection, prediction_time_utc, odds_snapshot_ref)
```

On a second run against the same source file, all 14 rows are detected as
duplicates and skipped. The registry JSONL remains at exactly 14 lines.

---

## 7. Production Registry Protection

The existing production registry at
`data/wbc_backend/reports/prediction_registry.jsonl` (66 rows, WBC game-level
schema) was **not modified**. Phase 6T writes to a separate isolated file:

```
data/wbc_backend/reports/prediction_registry_6t_2026-04-30.jsonl
```

The production registry uses the `append_prediction_record()` function in
`wbc_backend/reporting/prediction_registry.py`, which takes domain objects
(`AnalyzeRequest`, `Matchup`, etc.) and writes a deeply-nested schema.
Phase 6T uses a flat ML-only schema that is incompatible with and fully
separate from the production registry.

---

## 8. Downstream Readiness

| Consumer | Status | Condition |
|---|---|---|
| Research layer | READY | `clv_usable=True` on all rows |
| Settlement ingestion | READY | `event_start_time_utc` populated for all rows |
| ROI tracking | READY | `expected_value` + `execution_mode` present |
| CLV generation (Phase 6U) | READY | `clv_usable=True` + `odds_snapshot_ref` on all rows |

### Phase 6U Blockers (not in scope for 6T)

1. **CLV record generation** — requires closing odds vs. pre-prediction odds
2. **Kelly sizing** — requires bankroll state + CLV registry
3. **Settlement linkage** — requires game results ingestion

---

## 9. Test Coverage

**File:** `tests/test_phase6t_registry_conversion.py`  
**Result:** 41 / 41 PASS in 0.29s

| Test class | Tests | Coverage |
|---|---|---|
| `TestEligibilityGates` | 17 | G1–G7 gate enforcement (parametrized) |
| `TestConversionContent` | 8 | Governance fields, prediction_id stability, timestamp chain, schema version |
| `TestValidateRegistryRow` | 5 | Null critical field, live bet activation, invalid execution_mode |
| `TestIdempotency` | 3 | Dedup key, single-row idempotency, run_converter idempotency |
| `TestFullStackApril30` | 8 | Real 14-row integration: count, critical fields, CLV, alignment, EV, governance, live betting, idempotency |

---

## 10. Files Created / Modified

| File | Action |
|---|---|
| `scripts/convert_ml_output_to_registry_6t.py` | **CREATED** — Phase 6T converter |
| `data/wbc_backend/reports/prediction_registry_6t_2026-04-30.jsonl` | **CREATED** — 14 registry rows |
| `data/wbc_backend/reports/prediction_registry_6t_summary_2026-04-30.json` | **CREATED** — conversion summary |
| `tests/test_phase6t_registry_conversion.py` | **CREATED** — 41 tests |
| `docs/orchestration/phase6t_registry_conversion_report_2026-04-30.md` | **CREATED** — this report |
| `data/wbc_backend/reports/prediction_registry.jsonl` | **NOT MODIFIED** (66 production rows preserved) |
| `data/derived/model_outputs_6s_future_2026-04-30.jsonl` | **NOT MODIFIED** (14 Phase 6S source rows) |
| `data/derived/model_outputs_2026-04-29.jsonl` | **NOT MODIFIED** (2,986 historical rows) |

---

## 11. Verification Token

```
PHASE_6T_REGISTRY_CONVERSION_VERIFIED
```
