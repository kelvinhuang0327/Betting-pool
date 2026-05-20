# Phase 6J — Model Output Contract Design for MLB/KBO/NPB

**Date**: 2026-04-29
**Phase**: 6J (Documentation / Contract Design Only — No Model Changes, No Predictions, No Commit)
**Status**: DESIGN_COMPLETE
**Predecessor**: Phase 6I (f00ccb6) — `NOT_READY_MODEL_CAPABILITY_GAP`
**Depends On**: Phase 6A CLV data contract, Phase 6H prediction registry extension design

---

## 1. Executive Summary

Phase 6I confirmed that no usable MLB/KBO/NPB prediction source exists.
All 10 Phase 6H quality gates were BLOCKED with `MODEL_CAPABILITY_GAP_NO_MLB_KBO_NPB_PREDICTION_SOURCE`.
The odds side is structurally ready (4,356 OPENING+CLOSING pairs).
The prediction side has zero registry-compatible outputs.

This document defines the **model output contract** — the canonical schema and rules
that any MLB/KBO/NPB prediction pipeline component must satisfy before its outputs
can be consumed by the prediction registry, CLV measurement, or settlement join.

The contract covers:

- Canonical output file schema (`data/derived/model_outputs_YYYY-MM-DD.jsonl`)
- Market-specific probability semantics (ML, RL, OU)
- Versioning identifiers
- Timing and leakage rules
- Expected value computation contract
- Model capability gap (MCG) closure plan (MCG-01 through MCG-10)
- Quality gates M1–M12
- Backward compatibility
- Implementation roadmap (Phase 6K → 6O)
- Ready-to-copy Phase 6K prompt

**No model code is modified. No predictions are generated. No DB or runtime changes.
No commit. Scope: documentation only.**

---

## 2. Evidence Read

| File | Status | Size | Key Findings |
|---|---|---|---|
| `docs/orchestration/phase6i_prediction_registry_dry_run_report_2026-04-29.md` | ✅ Read | 13 KB / 225 lines | Readiness = NOT_READY_MODEL_CAPABILITY_GAP; 0/10 gates pass; 2,080 dry-run stubs emitted with `predicted_probability=null` |
| `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl` | ✅ Read | 2.0 MB / 2,080 rows | All `dry_run=true`, `clv_usable=false`, `predicted_probability=null`; market breakdown ML=766 / RL=656 / OU=658 |
| `docs/orchestration/phase6h_prediction_registry_extension_design_2026-04-29.md` | ✅ Read | 33 KB | 28-field per-market schema; MCG-01–MCG-10 gap list; quality gates P1–P10 |
| `docs/orchestration/phase6f_future_event_capture_manifest_2026-04-29.md` | ✅ Read | 33 KB | Future event capture manifest schema; canonical_match_id derivation |
| `docs/orchestration/phase6a_clv_data_contract_2026-04-29.md` | ✅ Read | 36 KB | 7 CLV contract fields: `canonical_match_id`, `market_key`, `selection_key`, `model_version`, `feature_version`, `leakage_guard_version`, `prediction_time_utc` |
| `data/wbc_backend/model_artifacts.json` | ✅ Read | 805 B | Keys: `calibration` (Platt: a=1.1077, b=-0.0184), `params` (min_train=240, retrain_every=40, markets=[ML/RL/OU]), `odds_band_stats`; **no `model_version` field** |
| `data/wbc_backend/market_validation.json` | ✅ Read | 788 B | Aggregate ML/RL/OU metrics (ML roi=-0.008, RL roi=-0.035, OU roi=-0.121); brier/logloss aggregate only; **no per-game rows, no predicted_probability** |
| `data/wbc_backend/walkforward_summary.json` | ✅ Read | 301 B | Aggregate: games=2188, ml_roi=-0.011, rl_roi=-0.062, ou_roi=-0.122, ece=0.035; **no per-game rows, no model_version** |
| `data/wbc_backend/reports/mlb_decision_quality_report.json` | ✅ Read | 976 KB / 1,493 per_game rows | Has `predicted_home_win_prob`; game_id format `MLB-2025_04_24-...`; **no `canonical_match_id`, `market_key`, `prediction_time_utc`, `model_version`**; all `clv_available=false` |
| `data/wbc_backend/reports/mlb_paper_tracking_report.json` | ✅ Read | 6.6 KB | `execution_mode=PAPER_ONLY`, `clv_mode=SANDBOX_ONLY`; 1,493 sample aggregate; **no per-game prediction rows** |
| `config/settings.py` | ✅ Read | 5.0 KB | `EV_STRONG=0.07`, `EV_MEDIUM=0.03`, `KELLY_FRACTION=0.15`, `DRAWDOWN_MAX=0.20`, `DAILY_LOSS_STOP_PCT=0.15` |
| `strategy/risk_control.py` | ✅ Read | 3.0 KB | `RiskStatus(GREEN/YELLOW/RED)`; evaluates daily_loss, model_error_consecutive, market_anomaly_count, drawdown_pct |
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ✅ Read (via Phase 6I) | ~26 MB / 28,941 rows | ML/RL/OU markets; canonical_match_id `baseball:unknown_league:YYYYMMDD:...`; 4,356 OPENING+CLOSING pairs |
| `data/derived/match_identity_bridge_2026-04-29.jsonl` | ✅ Read (via Phase 6I) | ~303 KB / 383 rows | All `league=unknown_league`; bridge_status/confidence/quality_flags fields present |

### Missing Evidence

| File | Status | Impact |
|---|---|---|
| `data/wbc_backend/reports/prediction_registry.jsonl` (MLB columns) | Present but WBC-only | MLB prediction output design cannot reference existing rows |
| Any MLB per-game prediction output with `prediction_time_utc` | **ABSENT** — key gap MCG-05 | All timing rules must be built from scratch |
| `model_version` constant in any model module | **ABSENT** — key gap MCG-02 | Versioning contract must be defined here and implemented in Phase 6K+ |

---

## 3. Current Model Output Inventory

| Source | Exists? | Output Type | Match-level rows? | Market-level rows? | `predicted_probability`? | `prediction_time_utc`? | Version fields? | Usable for CLV? | Gap |
|---|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `model_artifacts.json` | ✅ | Calibration params + training hyperparams | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No prediction rows; parameter store only |
| `market_validation.json` | ✅ | Aggregate ML/RL/OU ROI | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Aggregate metrics; no per-game data |
| `walkforward_summary.json` | ✅ | Walkforward aggregate ROI + ECE | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | Aggregate; no per-game, no version |
| `mlb_decision_quality_report.json` | ✅ | Per-game paper tracking | ✅ (1,493 rows) | ❌ | ✅ (`predicted_home_win_prob`) | ❌ | ❌ | ❌ | MCG-01,05,06,07,08,10 — missing `canonical_match_id`, `market_key`, `selection_key`, `prediction_time_utc`, `model_version` |
| `mlb_paper_tracking_report.json` | ✅ | Aggregate PAPER_ONLY tracking | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | PAPER_ONLY / SANDBOX_ONLY; aggregate only |
| `prediction_registry.jsonl` | ✅ | WBC-only game-level predictions | ✅ (66 WBC rows) | ❌ | ✅ (game-level `home_win_prob`) | ❌ | ❌ | ❌ | WBC domain; wrong league; MCG-01–10 all absent |
| `future_model_predictions_dry_run_2026-04-29.jsonl` | ✅ | Dry-run stubs (Phase 6I output) | ✅ (2,080 rows) | ✅ (ML/RL/OU × 2) | ❌ (`null`) | ❌ (`null`) | ❌ (`NOT_IMPLEMENTED`) | ❌ | Intentionally non-CLV-usable; schema template only |

**Inventory Conclusion**: No file in the current codebase contains a row that satisfies
the minimum threshold to be ingested into the prediction registry for CLV measurement:
`canonical_match_id` + `predicted_probability` (not null) + `prediction_time_utc`.

---

## 4. Model Output Contract

### 4.1 Canonical Output File

```
data/derived/model_outputs_YYYY-MM-DD.jsonl
```

Where `YYYY-MM-DD` is the date of the prediction run (not the match date).

One JSONL file per prediction run. Each line is one independent prediction record
for one market-selection on one match. Six rows per match (ML×2, RL×2, OU×2) when
all markets are covered, or fewer when RL/OU is a capability gap.

### 4.2 Required Fields

| Field | Type | Nullable | Description |
|---|---|:---:|---|
| `schema_version` | string | NO | Contract version e.g. `"6j-1.0"` |
| `model_output_id` | string | NO | Unique identifier for this row: UUID v4 or deterministic hash of `(prediction_run_id, selection_key)` |
| `prediction_run_id` | string | NO | Identifier for the batch inference run e.g. `"run_2026-04-29T10:00:00Z"` |
| `model_family` | string | NO | e.g. `"mlb_moneyline"`, `"mlb_runline"`, `"mlb_totals"` |
| `model_version` | string | NO | Semver model identifier (see §6) |
| `feature_version` | string | NO | Semver feature set identifier (see §6) |
| `leakage_guard_version` | string | NO | Semver leakage guard identifier (see §6) |
| `training_window_id` | string | NO | Training window descriptor (see §6) |
| `walk_forward_split_id` | string | NO | Walk-forward split reference (see §6) |
| `sport` | string | NO | Always `"baseball"` for current scope |
| `league` | string | NO | `"MLB"`, `"KBO"`, or `"NPB"` |
| `canonical_match_id` | string | NO | Bridge-compatible ID: `baseball:{league}:{YYYYMMDD}:{home_code}:{away_code}` |
| `raw_match_id` | string | YES | Source system match ID (e.g. TSL match ID) |
| `match_time_utc` | ISO8601 | NO | Scheduled first pitch in UTC |
| `home_team_code` | string | NO | Normalized team code |
| `away_team_code` | string | NO | Normalized team code |
| `market_type` | string | NO | `"ML"`, `"RL"`, `"OU"` |
| `market_line` | float | YES | Spread or total line; required for RL and OU; null for ML |
| `market_key` | string | NO | e.g. `"ML"`, `"RL-1.5"`, `"OU-8.5"` |
| `selection` | string | NO | `"home"`, `"away"`, `"over"`, `"under"` |
| `selection_key` | string | NO | Composite: `"{canonical_match_id}:{market_key}:{model_version}:{selection}"` |
| `prediction_time_utc` | ISO8601 | NO | UTC timestamp when inference was executed (must be pre-game) |
| `predicted_probability` | float | NO | Model probability for the selection winning; **must not be null in a real output row** |
| `confidence` | string | YES | `"HIGH"`, `"MEDIUM"`, `"LOW"`, `"INSUFFICIENT_SAMPLE"` |
| `probability_source` | string | NO | `"model_direct"`, `"calibrated_platt"`, `"ensemble"` — documents the probability derivation |
| `feature_cutoff_time_utc` | ISO8601 | NO | Latest feature input timestamp; must be ≤ `prediction_time_utc` |
| `odds_snapshot_ref` | string | YES | `snapshot_id` from `odds_snapshots_YYYY-MM-DD.jsonl` used at prediction time |
| `implied_probability_at_prediction` | float | YES | `1 / decimal_odds` from odds snapshot; null if `odds_snapshot_ref` missing |
| `expected_value` | float | YES | `predicted_probability * decimal_odds - 1`; null if `odds_snapshot_ref` missing |
| `model_quality_flags` | list[string] | NO | e.g. `["CALIBRATION_APPLIED", "WALKFORWARD_VALIDATED"]` |
| `data_quality_flags` | list[string] | NO | e.g. `["ODDS_SNAPSHOT_MISSING"]`, or empty list `[]` |

### 4.3 Example Record

```json
{
  "schema_version": "6j-1.0",
  "model_output_id": "7f3a2c9e-1b4d-4e8a-9c0f-2d5e6a7b8c90",
  "prediction_run_id": "run_2026-05-15T08:30:00Z",
  "model_family": "mlb_moneyline",
  "model_version": "mlb_moneyline_v1.0.0",
  "feature_version": "features_mlb_pregame_v1.0.0",
  "leakage_guard_version": "leakage_guard_pregame_v1.0.0",
  "training_window_id": "train_2022-2025_regular_season",
  "walk_forward_split_id": "wf_2026w01",
  "sport": "baseball",
  "league": "MLB",
  "canonical_match_id": "baseball:MLB:20260515:NYY:BOS",
  "raw_match_id": "tsl_3847291.1",
  "match_time_utc": "2026-05-15T23:05:00Z",
  "home_team_code": "NYY",
  "away_team_code": "BOS",
  "market_type": "ML",
  "market_line": null,
  "market_key": "ML",
  "selection": "home",
  "selection_key": "baseball:MLB:20260515:NYY:BOS:ML:mlb_moneyline_v1.0.0:home",
  "prediction_time_utc": "2026-05-15T22:30:00Z",
  "predicted_probability": 0.5812,
  "confidence": "MEDIUM",
  "probability_source": "calibrated_platt",
  "feature_cutoff_time_utc": "2026-05-15T20:00:00Z",
  "odds_snapshot_ref": "snap_2026-05-15T22:25:00Z_tsl_3847291.1",
  "implied_probability_at_prediction": 0.5405,
  "expected_value": 0.0749,
  "model_quality_flags": ["CALIBRATION_APPLIED", "WALKFORWARD_VALIDATED"],
  "data_quality_flags": []
}
```

---

## 5. Market-Specific Probability Semantics

### 5.1 ML (Moneyline)

| Property | Value |
|---|---|
| `market_type` | `"ML"` |
| `market_line` | `null` |
| `market_key` | `"ML"` |
| Selections | `"home"`, `"away"` |
| `predicted_probability` semantics | Probability that the selected team wins the match (full game result) |
| Constraint | Exactly two records per match: `selection="home"` and `selection="away"` |
| Probability sum check | `P(home) + P(away)` should sum to approximately 1.0 (within calibration tolerance ±0.02) |
| Current capability | `predicted_home_win_prob` exists in `mlb_decision_quality_report.json` — **not registry-compatible** due to missing `canonical_match_id`, `prediction_time_utc`, `model_version` |

**Implementation note**: ML is the minimum viable market. Phase 6L should implement ML-only adapter first.
Do not block ML on RL/OU capability gap.

### 5.2 RL (Run Line)

| Property | Value |
|---|---|
| `market_type` | `"RL"` |
| `market_line` | Spread line e.g. `-1.5` or `+1.5` |
| `market_key` | `"RL-1.5"` or `"RL+1.5"` |
| Selections | `"home"`, `"away"` (with reference to `market_line`) |
| `predicted_probability` semantics | Probability that the selected side covers the spread (total runs differential vs. line) |
| Requirement | **Line-specific probability**. Must be derived from a run-differential distribution model, not from ML win probability alone. |
| If unavailable | Set `prediction_status = "MODEL_CAPABILITY_GAP_RL_LINE_SPECIFIC_PROBABILITY"`, `predicted_probability = null`, `data_quality_flags = ["MODEL_CAPABILITY_GAP_RL_LINE_SPECIFIC_PROBABILITY"]` |

> ⚠️ **HARD RULE**: Do not derive RL probability from ML `predicted_home_win_prob` by applying
> a fixed heuristic or margin transform unless a validated run-differential transformation model
> exists with documented out-of-sample calibration evidence. Any such derivation must explicitly
> set `probability_source = "heuristic_rl_from_ml"` and `model_quality_flags` must include
> `"RL_HEURISTIC_UNVALIDATED"`.

**Current capability**: ABSENT. `mlb_decision_quality_report.json` has only `predicted_home_win_prob`
(game-level win probability). No run-differential distribution model output exists.

### 5.3 OU (Over/Under Totals)

| Property | Value |
|---|---|
| `market_type` | `"OU"` |
| `market_line` | Total line e.g. `8.5`, `9.0` |
| `market_key` | `"OU-8.5"` or `"OU-9.0"` |
| Selections | `"over"`, `"under"` |
| `predicted_probability` semantics | Probability that total runs scored in the match exceed (`over`) or fall below (`under`) `market_line` |
| Requirement | **Total distribution model**. Must be derived from a calibrated total runs model, team offense/defense rating, or Poisson-based total runs distribution. |
| If unavailable | Set `prediction_status = "MODEL_CAPABILITY_GAP_OU_TOTAL_DISTRIBUTION"`, `predicted_probability = null`, `data_quality_flags = ["MODEL_CAPABILITY_GAP_OU_TOTAL_DISTRIBUTION"]` |

> ⚠️ **HARD RULE**: Do not derive OU probability from ML `predicted_home_win_prob` or win-margin
> distribution unless a validated total runs model exists with documented calibration evidence.
> `market_validation.json` currently shows OU ROI = -0.122, which is evidence of poor OU model
> quality. Any OU probability output must include `probability_source` documentation and must not
> inherit the ML Platt calibration parameters.

**Current capability**: ABSENT. Current model produces only win probability (home vs. away),
not a total runs distribution.

### 5.4 Market Capability Summary

| Market | Current Probability Output? | Registry-Compatible? | Unblocking Requirement |
|---|:---:|:---:|---|
| ML | ✅ `predicted_home_win_prob` exists (per game) | ❌ Missing contract fields | Add `canonical_match_id`, `prediction_time_utc`, `model_version`, `market_key`, `selection_key` |
| RL | ❌ No RL-specific probability | ❌ | Build run-differential distribution model |
| OU | ❌ No total runs distribution | ❌ | Build calibrated total runs model |

---

## 6. Versioning Contract

### 6.1 Field Formats

| Field | Format | Example |
|---|---|---|
| `model_version` | `{domain}_{market}_v{MAJOR}.{MINOR}.{PATCH}` | `mlb_moneyline_v1.0.0` |
| `feature_version` | `features_{domain}_{type}_v{MAJOR}.{MINOR}.{PATCH}` | `features_mlb_pregame_v1.0.0` |
| `leakage_guard_version` | `leakage_guard_{type}_v{MAJOR}.{MINOR}.{PATCH}` | `leakage_guard_pregame_v1.0.0` |
| `training_window_id` | `train_{start_year}-{end_year}_{scope}` | `train_2022-2025_regular_season` |
| `walk_forward_split_id` | `wf_{year}w{week:02d}` | `wf_2026w01` |
| `prediction_run_id` | `run_{ISO8601_UTC_timestamp}` | `run_2026-05-15T08:30:00Z` |
| `model_output_id` | UUID v4 or `sha256({prediction_run_id}:{selection_key})[:16]` | `7f3a2c9e-1b4d-4e8a` |

### 6.2 Version Bump Rules

| Version Type | Bump MAJOR when | Bump MINOR when | Bump PATCH when |
|---|---|---|---|
| `model_version` | Architecture change (new algorithm family, feature space change) | Hyperparameter retuning, retrain on extended data | Bug fix in inference code |
| `feature_version` | Feature set change (add/remove features) | Feature computation update (same features, improved code) | Bug fix |
| `leakage_guard_version` | Leakage rule change (new hard rule, new timing gate) | Leakage rule refinement | Bug fix |

### 6.3 Current State

All three version fields are `"NOT_IMPLEMENTED"` in all existing files.
`model_artifacts.json` does not contain a `model_version` field.
Phase 6K must implement constants at minimum:

```python
# In model modules — Phase 6K action item
MODEL_VERSION = "mlb_moneyline_v1.0.0"
FEATURE_VERSION = "features_mlb_pregame_v1.0.0"
LEAKAGE_GUARD_VERSION = "leakage_guard_pregame_v1.0.0"
TRAINING_WINDOW_ID = "train_2022-2025_regular_season"
```

---

## 7. Timing / Leakage Contract

### 7.1 Hard Rules (Gate M9_NO_LEAKAGE_HARD_FAIL)

Any violation of a hard rule must cause `data_quality_flags` to include `"LEAKAGE_HARD_FAIL"`
and the row must be rejected from the prediction registry.

| Rule ID | Rule | Check |
|---|---|---|
| T1 | `prediction_time_utc < match_time_utc` | `datetime(prediction_time_utc) < datetime(match_time_utc)` |
| T2 | `feature_cutoff_time_utc <= prediction_time_utc` | Features used in inference must not have timestamps after inference time |
| T3 | Training window end date < `prediction_time_utc` | No data from the test period used in training |
| T4 | Odds features: referenced `odds_snapshot_time_utc <= prediction_time_utc` | If any feature was derived from odds, the odds snapshot must pre-date inference |
| T5 | Closing odds must not be used as model features | Closing odds arrive after the pre-game gate closes; using them as features is look-ahead |
| T6 | Settlement / result fields must not be present at prediction time | `actual_result`, `home_score`, `away_score`, `winner` must not be in the feature vector |

### 7.2 Warning Rules (Gate M6_TIMING_VALID — warning level)

| Warning ID | Condition | Warning Flag |
|---|---|---|
| W1 | `prediction_time_utc` within 30 minutes before `match_time_utc` | `"LATE_PREDICTION_WITHIN_30MIN"` |
| W2 | `feature_cutoff_time_utc` is missing or null | `"FEATURE_CUTOFF_MISSING"` |
| W3 | `odds_snapshot_ref` is missing when `probability_source` contains `"odds"` | `"ODDS_SNAPSHOT_REF_MISSING_CLAIMED_ODDS_FEATURE"` |
| W4 | `model_version` contains `"NOT_IMPLEMENTED"` | `"MODEL_VERSION_NOT_IMPLEMENTED"` |
| W5 | `walk_forward_split_id` contains `"NOT_IMPLEMENTED"` | `"WALK_FORWARD_SPLIT_NOT_IMPLEMENTED"` |

### 7.3 Pre-Game Gate

The pre-game gate is defined in Phase 6H §6 as T3 (30-minute pre-game cutoff).

```
pre_game_verified = (prediction_time_utc < match_time_utc - 30min)
```

Only rows with `pre_game_verified = true` are eligible for `clv_usable = true`.
Rows with `pre_game_verified = false` must have `clv_usable = false`.

### 7.4 Existing Evidence Against Timing Rules

`mlb_decision_quality_report.json` per_game rows have:
- `predicted_home_win_prob`: ✅ present
- `prediction_time_utc`: ❌ absent — T1 cannot be verified
- `feature_cutoff_time_utc`: ❌ absent — T2 cannot be verified
- `clv_available`: all `false` — consistent with timing not being verified

All 1,493 rows are therefore **not eligible** for CLV measurement under this contract.

---

## 8. Expected Value Contract

### 8.1 EV Computation Rule

```
implied_probability_at_prediction = 1 / decimal_odds_at_prediction

expected_value = (predicted_probability * decimal_odds_at_prediction) - 1
```

Where `decimal_odds_at_prediction` is the decimal odds from the odds snapshot
referenced by `odds_snapshot_ref` at time `prediction_time_utc`.

### 8.2 Nullability Rules

| Condition | `expected_value` | `implied_probability_at_prediction` |
|---|---|---|
| `odds_snapshot_ref` is present | Compute | Compute |
| `odds_snapshot_ref` is null | Must be `null` | Must be `null` |
| `predicted_probability` is null | Must be `null` | Can still be computed if odds ref present |
| Row is `dry_run=true` | Must be `null` | Should be `null` (non-CLV-usable) |

### 8.3 EV Threshold Reference (from `config/settings.py`)

| Setting | Value | Usage |
|---|---|---|
| `EV_STRONG` | 0.07 (7%) | Strong bet signal |
| `EV_MEDIUM` | 0.03 (3%) | Medium bet signal |
| `EV_SMALL` | 0.01 (1%) | Small bet signal |
| `EV_PASS` | 0.01 (1%) | Minimum threshold; below = no bet |

### 8.4 CLV Exclusion Rule

If `expected_value` was computed using **closing odds** (i.e., `odds_snapshot_ref` points to
a `snapshot_type=CLOSING` record), the row must be flagged:

```
data_quality_flags += ["EV_FROM_CLOSING_ODDS_CLV_EXCLUDED"]
clv_usable = false
```

This prevents inflated CLV signals from predictions that did not actually precede the closing line.

### 8.5 Settlement Join

CLV is computed post-game:

```
clv = predicted_probability - implied_probability_at_closing
```

Where `implied_probability_at_closing = 1 / decimal_closing_odds`.

This join is not implemented in Phase 6J. It is assigned to Phase 6O.
The model output contract does not include settlement fields — those belong in the registry join.

---

## 9. Model Capability Gap Closure Plan

| Gap ID | Gap Description | Current Evidence | Required Output | Owner Phase | Acceptance Criteria |
|---|---|---|---|---|---|
| MCG-01 | `canonical_match_id` absent from all MLB prediction outputs | `game_id` format `MLB-2025_04_24-...` incompatible with bridge format `baseball:unknown_league:YYYYMMDD:...` | Model inference must emit `canonical_match_id` in bridge-compatible format | Phase 6L | `canonical_match_id` present in every `model_outputs_*.jsonl` row; format matches `baseball:{LEAGUE}:{YYYYMMDD}:{home}:{away}` |
| MCG-02 | `model_version` absent from all files | `model_artifacts.json` has no version field | Add `MODEL_VERSION` constant to inference module | Phase 6K | `model_version != "NOT_IMPLEMENTED"` in all output rows |
| MCG-03 | `feature_version` absent from all files | No feature registry exists | Add `FEATURE_VERSION` constant to feature pipeline | Phase 6K | `feature_version != "NOT_IMPLEMENTED"` in all output rows |
| MCG-04 | `leakage_guard_version` absent from all files | No leakage guard versioning | Add `LEAKAGE_GUARD_VERSION` constant and implement timing checks | Phase 6K | `leakage_guard_version != "NOT_IMPLEMENTED"`; T1–T6 verified per row |
| MCG-05 | `prediction_time_utc` absent from all per-game outputs | Not stored at inference time | Record UTC timestamp at inference execution | Phase 6L | `prediction_time_utc` present and `< match_time_utc` for all rows |
| MCG-06 | `market_key` / `selection_key` per-row absent | Game-level outputs only; no market explosion | Per-market row explosion: 2 rows per ML, 2 per RL, 2 per OU | Phase 6L | Output contains exactly 2 rows per market per game; `selection_key` is unique |
| MCG-07 | ML `predicted_probability` not in registry-compatible format | `predicted_home_win_prob` in `mlb_decision_quality_report.json` but paper-only | Emit ML `predicted_probability` with all contract fields | Phase 6L | ML rows have non-null `predicted_probability`; gate M7_PROBABILITY_VALID passes |
| MCG-08 | RL line-specific probability absent | No run-differential distribution model | Build RL probability derivation from run-differential distribution | Phase 6M | RL rows have non-null `predicted_probability`; `probability_source != "heuristic_rl_from_ml"` or validated |
| MCG-09 | OU total distribution probability absent | No total runs model; OU ROI = -0.122 in `market_validation.json` | Build calibrated total runs model | Phase 6M | OU rows have non-null `predicted_probability`; Brier score < 0.25 on held-out data |
| MCG-10 | `odds_snapshot_ref` linkage absent | Odds snapshots exist but no prediction-to-snapshot linking | Attach `odds_snapshot_ref` to every prediction at inference time | Phase 6L | `odds_snapshot_ref` present; `implied_probability_at_prediction` computable |

---

## 10. Quality Gates

The following gates must be applied by any consumer reading `model_outputs_YYYY-MM-DD.jsonl`.
All gates are HARD FAIL unless marked as WARNING.

| Gate ID | Gate Name | Check | Fail Action |
|---|---|---|---|
| M1 | `M1_SCHEMA_VALID` | All required fields present; no unknown fields at schema_version; types correct | Reject row |
| M2 | `M2_CANONICAL_MATCH_ID_PRESENT` | `canonical_match_id` is non-null and matches `baseball:{LEAGUE}:{YYYYMMDD}:{home}:{away}` pattern | Reject row |
| M3 | `M3_MARKET_KEY_PRESENT` | `market_key` is non-null; for RL and OU, `market_line` must be non-null | Reject row |
| M4 | `M4_SELECTION_KEY_PRESENT` | `selection_key` is non-null and matches `{canonical_match_id}:{market_key}:{model_version}:{selection}` | Reject row |
| M5 | `M5_VERSION_FIELDS_PRESENT` | `model_version`, `feature_version`, `leakage_guard_version` all non-null and not `"NOT_IMPLEMENTED"` | Reject row |
| M6 | `M6_TIMING_VALID` | `prediction_time_utc < match_time_utc`; `feature_cutoff_time_utc <= prediction_time_utc` | Hard fail if T1/T2 violated; WARNING for W1–W5 |
| M7 | `M7_PROBABILITY_VALID` | `predicted_probability` in `[0.0, 1.0]`; not null for non-dry-run rows | Reject row |
| M8 | `M8_EV_VALID_OR_NULL_WITH_REASON` | If `odds_snapshot_ref` present: `expected_value` must be computed; if absent: `expected_value` must be null; no fake EVs | Reject row if EV non-null without odds ref |
| M9 | `M9_NO_LEAKAGE_HARD_FAIL` | None of T1–T6 violations; `actual_result` / settlement fields absent from feature vector | Reject row; emit `LEAKAGE_HARD_FAIL` flag |
| M10 | `M10_MARKET_SEMANTICS_VALID` | RL rows have `market_line != null`; OU rows have `market_line != null`; ML rows have `market_line = null`; RL/OU with no line-specific model set to capability gap status | Reject row |
| M11 | `M11_CLV_USABLE_FLAG_CORRECT` | If `dry_run=true` → `clv_usable=false`; if any T1–T6 violation → `clv_usable=false`; if `predicted_probability=null` → `clv_usable=false`; if `pre_game_verified=false` → `clv_usable=false` | Reject row if flag inconsistent |
| M12 | `M12_DRY_RUN_FLAG_CORRECT` | If `dry_run=true`: `predicted_probability=null`, `expected_value=null`, `clv_usable=false` must all hold | Reject row if dry_run=true but any of the three is non-null or true |

### Gate Interaction Rules

- M9 takes precedence over all other gates. A leakage hard fail rejects the row regardless of other gate results.
- M11 and M12 are consistency checkers — they do not accept rows that pass M7 but fail the flag logic.
- For RL/OU with `MODEL_CAPABILITY_GAP_RL_LINE_SPECIFIC_PROBABILITY` or `MODEL_CAPABILITY_GAP_OU_TOTAL_DISTRIBUTION` status, M7 is waived (null `predicted_probability` is expected) but M10 must still pass.

---

## 11. Backward Compatibility

| Concern | Resolution |
|---|---|
| Existing `data/wbc_backend/reports/prediction_registry.jsonl` | **Unchanged**. WBC registry remains WBC-only. The new `model_outputs_YYYY-MM-DD.jsonl` is a separate additive file. No backfill of WBC rows with new contract fields. |
| `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl` (Phase 6I) | **Unchanged**. This file remains non-CLV-usable (`dry_run=true`, `predicted_probability=null`). It serves as schema documentation only. Its `schema_version = "6i-dry-run-1.0"` is distinct from the production `"6j-1.0"` schema. |
| `data/wbc_backend/reports/mlb_decision_quality_report.json` | **Unchanged**. This file remains a paper-tracking report. It is not a prediction registry input. The Phase 6J contract does not backfill historical predictions. |
| `data/wbc_backend/model_artifacts.json` | **Unchanged**. Calibration parameters are not modified by this contract design. |
| `model_artifacts.json` calibration (Platt: a=1.1077, b=-0.0184) | The existing Platt calibration parameters are compatible with the new contract. New rows must document `probability_source = "calibrated_platt"` when these parameters are applied. |
| Phase 6A CLV contract | The Phase 6J model output contract is fully additive to Phase 6A. All 7 CLV contract fields required by Phase 6A are present in the Phase 6J schema (§4.2). |
| `config/settings.py` thresholds | Not modified. EV thresholds (EV_STRONG=0.07, EV_MEDIUM=0.03) apply at the strategy layer, not at the model output layer. |

---

## 12. Implementation Roadmap

| Phase | Name | Scope | Inputs | Outputs | Blocks |
|---|---|---|---|---|---|
| **6K** | Model Output Contract Validator | Implement schema validator for `model_outputs_*.jsonl`; check gates M1–M12; produce validation report | Phase 6J contract spec; any candidate model output file | Validator script `scripts/validate_model_output.py`; validation report `docs/orchestration/phase6k_validation_report_*.md` | Phase 6L |
| **6L** | ML-Only Model Output Adapter | Adapter reads `mlb_decision_quality_report.json`, resolves `canonical_match_id`, attaches `prediction_time_utc`, emits ML rows to `model_outputs_*.jsonl` | Phase 6K validator; bridge; `mlb_decision_quality_report.json` | `data/derived/model_outputs_YYYY-MM-DD.jsonl` (ML rows only) | Phase 6M, 6N |
| **6M** | RL/OU Probability Model | Design and implement run-differential (RL) and total runs (OU) probability outputs | Phase 6L ML outputs (for team quality signals); team run environment data | RL and OU rows in `model_outputs_*.jsonl` | Phase 6N |
| **6N** | Registry Conversion | Convert validated `model_outputs_*.jsonl` rows into prediction registry format; CLV-usable flag assignment | Phase 6K validator passing; Phase 6L/6M outputs | `data/derived/future_model_predictions_YYYY-MM-DD.jsonl` (real; not dry-run) | Phase 6O |
| **6O** | Settlement Join + CLV Validation | Join validated predictions with closing odds; compute CLV; test Phase 5.5 hypothesis | Phase 6N registry; closing odds from `odds_snapshots_*.jsonl` | CLV validation report; Phase 5.5 hypothesis test result | — |

### Phase 6K Priority

Phase 6K is the immediate next step. It must:
1. Read any candidate MLB model output file.
2. Apply gates M1–M12.
3. Report pass/fail with field-level evidence.
4. Not modify any source file.
5. Not generate new predictions.

Phase 6K unblocks Phase 6L by providing the acceptance test harness before any production adapter is written.

---

## 13. Next Prompt

The following prompt is ready to copy for Phase 6K:

---

```
# TASK: BETTING-POOL PHASE 6K — MODEL OUTPUT CONTRACT VALIDATOR

GOAL:
Implement a schema validator for the Phase 6J model output contract.
The validator reads candidate model output files and applies quality gates M1–M12.
This phase is documentation + script creation only. No model changes. No predictions. No commit.

CONTEXT:
- Phase 6J (this document): docs/orchestration/phase6j_model_output_contract_design_2026-04-29.md
- Phase 6J contract schema version: "6j-1.0"
- Quality gates to implement: M1_SCHEMA_VALID through M12_DRY_RUN_FLAG_CORRECT
- Candidate input file: data/derived/future_model_predictions_dry_run_2026-04-29.jsonl (dry-run; all rows expected to fail M7 and M5)
- Production input (to be created by Phase 6L): data/derived/model_outputs_YYYY-MM-DD.jsonl

REQUIRED OUTPUTS:
1. scripts/validate_model_output.py
   - Args: --input (default: data/derived/model_outputs_*.jsonl), --report, --output-summary
   - stdlib only, no network
   - Applies gates M1–M12 per row
   - Prints compact gate-level summary
   - Writes Markdown report
   - Writes JSON summary with gate pass/fail counts

2. docs/orchestration/phase6k_model_output_validator_report_YYYY-MM-DD.md
   - Sections: Evidence Read, Validator Implementation, Gate Results, Sample Rows, Readiness Decision, Scope Confirmation

SCOPE CONSTRAINTS:
- Do NOT modify model code
- Do NOT generate new predictions
- Do NOT modify any existing data files
- Do NOT call external APIs
- Do NOT create orchestrator tasks
- Do NOT run formal CLV validation
- Do NOT commit

ACCEPTANCE CRITERIA:
- Validator runs on dry-run JSONL (2,080 rows) and correctly identifies all M5, M7 failures
- Gate results are evidence-based (not assumed)
- Report includes pass/fail counts per gate
- Contamination = 0
```

---

## 14. Scope Confirmation

| Constraint | Status |
|---|---|
| Source data files modified | ❌ NOT done |
| Model code modified | ❌ NOT done |
| New predictions generated | ❌ NOT done |
| Fake/placeholder probabilities inserted as valid | ❌ NOT done |
| `prediction_registry.jsonl` modified | ❌ NOT done |
| `future_model_predictions_dry_run_2026-04-29.jsonl` modified | ❌ NOT done |
| `mlb_decision_quality_report.json` modified | ❌ NOT done |
| `model_artifacts.json` modified | ❌ NOT done |
| Crawler modified | ❌ NOT done |
| DB or migrations modified | ❌ NOT done |
| External API called | ❌ NOT done |
| Orchestrator task created | ❌ NOT done |
| Formal CLV validation run | ❌ NOT done |
| Git commit made | ❌ NOT done |
| Lottery-domain terms used | ❌ NOT done |

---

*Phase 6J DESIGN_COMPLETE — token: PHASE_6J_MODEL_OUTPUT_CONTRACT_VERIFIED*
