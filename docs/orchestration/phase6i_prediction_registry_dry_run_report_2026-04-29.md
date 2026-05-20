# Phase 6I: Prediction Registry Dry-Run Report
**Date**: 2026-04-29
**Phase**: 6I (Dry-Run Only — No Model Changes, No CLV Validation, No Commit)
**Status**: DRY_RUN_COMPLETE
**Depends On**: Phase 6H (222d0bc)

---

## 1. Executive Summary

**No usable MLB/KBO/NPB prediction source was found.** All candidate files lack at least one of the three mandatory fields required to produce a valid prediction registry row: `canonical_match_id`, `predicted_probability`, and `prediction_time_utc`.

The readiness decision from Phase 6G (`NOT_READY_DOMAIN_MISMATCH`) remains unchanged and is now more precisely characterized as `NOT_READY_MODEL_CAPABILITY_GAP`: the odds side has 4,356 opening+closing pairs ready for CLV measurement, but the model side has no pre-game MLB/KBO/NPB probability output that satisfies the Phase 6A contract.

Dry-run stub rows have been emitted for all bridge matches × allowed markets to document the schema shape and identify exactly which fields are missing.

---

## 2. Input Evidence

| Input File | Size | Rows / Records | Role |
|---|---:|---:|---|
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ~26 MB | 28,941 | Odds opening+closing snapshots |
| `data/derived/match_identity_bridge_2026-04-29.jsonl` | ~303 KB | 383 | Canonical match ID bridge |
| `data/derived/team_alias_map_2026-04-29.csv` | 5.6 KB | — | Team alias normalisation |
| `data/derived/manifest_dry_run_summary_2026-04-29.json` | 1.8 KB | — | Phase 6G gate summary |
| `data/wbc_backend/reports/prediction_registry.jsonl` | 430 KB | 66 | WBC-only registry (reference) |
| `docs/orchestration/phase6h_prediction_registry_extension_design_2026-04-29.md` | 33 KB | — | Phase 6H schema spec |

### Phase 6G Key Stats (from manifest_dry_run_summary)

- `odds_records`: 28,941
- `selection_keys`: 5,963
- `opening_closing_pairs`: 4,356
- `allowed_market_records` (ML/RL/OU): {'ML': 1057, 'RL': 1310, 'OU': 3596}
- `bridge_ready_records`: 0
- `readiness_decision`: NOT_READY_DOMAIN_MISMATCH

---

## 3. Candidate Prediction Source Inventory

| File | Exists? | Rows | has canonical_match_id? | has market_key? | has predicted_probability? | has model_version? | Usable? | Reason |
|---|:---:|---:|:---:|:---:|:---:|:---:|:---:|---|
| `mlb_decision_quality_report.json` | ✅ | 1,493 | ❌ | ❌ | ✅ | ❌ | ❌ | MODEL_CAPABILITY_GAP: missing canonical_match_id |
| `mlb_paper_tracking_report.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `mlb_alpha_discovery_report.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `mlb_model_family_report.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `mlb_calibration_baseline_snapshot_2026-04-25.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `mlb_pregame_coverage_report.json` | ✅ | 38 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `model_artifacts.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `market_validation.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |
| `walkforward_summary.json` | ✅ | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | MODEL_CAPABILITY_GAP: no predicted_probability field |

### Inventory Findings

- **`mlb_decision_quality_report.json`**: Contains 1,493 per-game rows with `predicted_home_win_prob` — the closest thing to a prediction source. However it **lacks** `canonical_match_id`, `market_key`, `prediction_time_utc`, and `model_version`. Its `game_id` format (`MLB-2025_04_24-...`) does not match the bridge's `canonical_match_id` format (`baseball:unknown_league:YYYYMMDD:...`). It is a paper-tracking report, not a real-time prediction registry.
- **All other candidate files**: No `predicted_probability` field at any level. These are aggregate metric or calibration reports.
- **WBC `prediction_registry.jsonl`**: WBC-only (A05–D06); all 7 CLV contract fields absent as established in Phase 6H.

**Conclusion**: No usable MLB/KBO/NPB prediction source exists. The model pipeline does not currently emit pre-game per-market probability outputs in a registry-compatible format.

---

## 4. Dry-Run Adapter Method

The adapter (`scripts/build_prediction_registry_dry_run.py`) implements the following logic:

1. **Load inputs**: odds snapshots, match identity bridge, team alias map, manifest summary, WBC registry.
2. **Probe candidate files**: For each of 9 candidate MLB/KBO/NPB report files, check for the three mandatory prediction fields.
3. **Evaluate Phase 6H gates P1–P10**: Since no usable source is found, all gates are marked `BLOCKED: MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE`.
4. **Build dry-run stubs**: For each unique `(canonical_match_id, market_key)` combination in the odds data, emit 2 stub rows (home+away or over+under) with `dry_run=true`, `predicted_probability=null`, `clv_usable=false`.
5. **Write output JSONL**: All stubs written to `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl`.
6. **Write report**: This document.

### MCG Gaps Confirmed by Adapter

| MCG ID | Field | Status |
|---|---|---|
| MCG-01 | `canonical_match_id` | ❌ No MLB/KBO/NPB match-level ID in any prediction source |
| MCG-02 | `model_version` | ❌ Not stored in any output file |
| MCG-03 | `feature_version` | ❌ Not stored in any output file |
| MCG-04 | `leakage_guard_version` | ❌ Not stored in any output file |
| MCG-05 | `market_key` per row | ❌ Game-level only; no per-market prediction rows |
| MCG-06 | `selection_key` per row | ❌ No selection-level tracking |
| MCG-07 | `odds_snapshot_ref` | ❌ No odds reference in any prediction output |
| MCG-08 | `prediction_time_utc` | ❌ Absent from all candidate files |
| MCG-09 | `ou_line_ref` | ❌ OU line not stored in prediction outputs |
| MCG-10 | RL probability derivation | ❌ Only `home_win_prob`; no run-differential distribution |

---

## 5. Phase 6H Gate Results

All Phase 6H quality gates (P1–P10) are blocked because no usable MLB/KBO/NPB prediction source exists.

| Gate | Status | Note |
|---|---|---|
| `P1_CANONICAL_MATCH_ID_PRESENT` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P2_SELECTION_KEY_PRESENT` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P3_MARKET_ALLOWED` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P4_PREDICTION_TIME_VALID` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P5_MODEL_VERSION_PRESENT` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P6_FEATURE_VERSION_PRESENT` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P7_PROBABILITY_VALID` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P8_ODDS_SNAPSHOT_REF_VALID` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P9_NO_LEAKAGE_HARD_FAIL` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |
| `P10_DECISION_CANDIDATE_PRESENT` | BLOCKED | MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE |

**Gate summary**: 0/10 pass · 10/10 BLOCKED

---

## 6. Output Summary

| Output | Path | Rows | Status |
|---|---|---:|---|
| Dry-run adapter script | `scripts/build_prediction_registry_dry_run.py` | — | ✅ Created |
| Dry-run report | `docs/orchestration/phase6i_prediction_registry_dry_run_report_2026-04-29.md` | — | ✅ Created |
| Dry-run stub JSONL | `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl` | 2,080 | ✅ Created (all `dry_run=true`, `clv_usable=false`) |

### Dry-Run Stub JSONL — Schema Sample

```json
{
  "schema_version": "6i-dry-run-1.0",
  "dry_run": true,
  "prediction_status": "MODEL_CAPABILITY_GAP",
  "clv_usable": false,
  "reason": "MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE",
  "canonical_match_id": "baseball:unknown_league:20260313:...",
  "market_type": "ML",
  "market_key": "ML",
  "selection": "home",
  "selection_key": "baseball:unknown_league:...:ML:NULL:home",
  "prediction_time_utc": null,
  "model_version": "NOT_IMPLEMENTED",
  "feature_version": "NOT_IMPLEMENTED",
  "leakage_guard_version": "NOT_IMPLEMENTED",
  "predicted_probability": null,
  "confidence": null,
  "expected_value": null,
  "odds_snapshot_ref": null,
  "data_quality_flags": ["MODEL_CAPABILITY_GAP", "DRY_RUN_PLACEHOLDER", "CLV_NOT_USABLE"]
}
```

---

## 7. Readiness Decision

```
NOT_READY_MODEL_CAPABILITY_GAP
```

**Rationale**:

| Dimension | Status | Evidence |
|---|---|---|
| Odds side | ✅ Ready | 4,356 OPENING+CLOSING pairs; ML/RL/OU markets present |
| Bridge side | ⚠️ Partial | 383 bridge rows but all `league=unknown_league`; format mismatch with MLB game IDs |
| Prediction side | ❌ Not Ready | 0 MLB/KBO/NPB pre-game probability records satisfying Phase 6A contract |
| Version fields | ❌ Not Ready | `model_version`, `feature_version`, `leakage_guard_version` all absent |
| CLV computable | ❌ Blocked | Requires prediction side ready first |

Previous decision `NOT_READY_DOMAIN_MISMATCH` (Phase 6G) is now refined to `NOT_READY_MODEL_CAPABILITY_GAP` (Phase 6I): the domain commitment is confirmed (`DOMAIN_COMMITMENT_MLB_KBO_NPB`), but the model pipeline does not yet emit per-game, per-market probability outputs in registry-compatible format.

---

## 8. Findings

1. **WBC registry is not reusable as MLB/KBO/NPB prediction registry.** The 66 WBC rows cover games A05–D06 played 2026-03-08/09. They use WBC pool-slot game IDs (`A05`), lack all 7 CLV contract fields, and have no temporal or competition overlap with the MLB/KBO/NPB odds window (2026-03-13+).

2. **Existing odds side has usable OPENING/CLOSING data.** Phase 6G confirmed 4,356 opening+closing pairs across ML/RL/OU markets, all with valid implied probabilities. The odds infrastructure is ready to support CLV calculation once predictions are available.

3. **Model/prediction side lacks canonical MLB/KBO/NPB probability outputs.** The closest candidate (`mlb_decision_quality_report.json`, 1,493 per-game rows) has `predicted_home_win_prob` but is a retrospective paper-tracking report — not a pre-game prediction registry. It lacks `canonical_match_id` in bridge-compatible format, `prediction_time_utc`, `market_key`, and `model_version`.

4. **Bridge `canonical_match_id` format does not match MLB report `game_id` format.** Bridge uses `baseball:unknown_league:YYYYMMDD:team_name:team_name`; MLB decision quality report uses `MLB-YYYY_MM_DD-HH_MM_[AP]M-TEAM_NAME-AT-TEAM_NAME`. An alias normalisation layer is required.

5. **Do not run formal CLV validation yet.** Prerequisite: at least one MLB/KBO/NPB pre-game probability record must exist with all Phase 6A contract fields present and `pre_game_verified=true`. This condition is not met.

6. **All 10 Phase 6H quality gates are blocked** at the source-discovery level, not at the schema validation level. The adapter cannot even reach schema validation because no input rows satisfy the minimum candidacy threshold.

---

## 9. Recommended Next Step

**Phase 6J: Model Output Contract Implementation**

Phase 6J must implement the model adapter layer that produces `data/derived/future_model_predictions_YYYY-MM-DD.jsonl` with real pre-game probabilities. Required actions in Phase 6J:

| # | Action | Resolves MCG |
|---|---|---|
| 1 | Add `MODEL_VERSION`, `FEATURE_VERSION`, `LEAKAGE_GUARD_VERSION` constants to model modules | MCG-02, MCG-03, MCG-04 |
| 2 | Implement `canonical_match_id` generation that matches bridge format | MCG-01 |
| 3 | Implement per-market row explosion (ML×2, RL×2, OU×2 per game) | MCG-05, MCG-06 |
| 4 | Record `prediction_time_utc` at inference time with `pre_game_verified` flag | MCG-08 |
| 5 | Attach `odds_snapshot_ref` linking prediction to opening odds row | MCG-07 |
| 6 | Add `ou_line_ref` from opening OU odds for OU row derivation | MCG-09 |
| 7 | Implement run-differential distribution for RL probability | MCG-10 |
| 8 | Implement Phase 6H quality gates P1–P10 as pre-write validators | P1–P10 |

Alternative fast path: if only settlement join (CLV via closing odds alone) is the goal, Phase 6J can use the mlb_decision_quality_report's `predicted_home_win_prob` values as a **sandbox-only** source — but this requires explicitly labeling them as `clv_usable=false` / `clv_source=sandbox` and not counting them toward the ≥200 live CLV hypothesis threshold.

---

## 10. Scope Confirmation

| Constraint | Status |
|---|---|
| `prediction_registry.jsonl` modified | ❌ NOT done |
| Model code modified | ❌ NOT done |
| Real predictions generated | ❌ NOT done |
| Fake/placeholder probabilities inserted as valid | ❌ NOT done (all `predicted_probability=null`) |
| Crawler modified | ❌ NOT done |
| DB or migrations modified | ❌ NOT done |
| Existing data files modified | ❌ NOT done |
| External API called | ❌ NOT done |
| Orchestrator task created | ❌ NOT done |
| Formal CLV validation run | ❌ NOT done |
| Git commit made | ❌ NOT done |

---

*Phase 6I DRY_RUN_COMPLETE — token: NOT_READY_MODEL_CAPABILITY_GAP*
