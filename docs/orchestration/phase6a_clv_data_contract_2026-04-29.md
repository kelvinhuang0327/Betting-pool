# Phase 6A — CLV Validation Data Contract Specification

**Date:** 2026-04-29
**Type:** Schema contract and readiness specification — NOT an implementation
**Predecessor:** Phase 6 design (`3a34c3b`) — `docs/orchestration/phase6_market_signal_data_pipeline_design_2026-04-29.md`
**Author:** Betting-pool Orchestrator Research Agent

---

## Executive Summary

This document defines the **canonical data contract** for the Betting-pool CLV validation
pipeline. It is a schema and readiness specification only. No code, DB, crawler, model,
or runtime files are modified by this document.

The CLV hypothesis under validation (Phase 5.5 source task #6161):

> *Bets placed where CLV_proxy > 0.03 will outperform the benchmark model's overall ROI
> by at least 3 percentage points over a sample of ≥200 bets per market regime.*

This contract defines the data structures, field-level validation rules, join keys,
leakage guards, and backward-compatibility adapters required to test that hypothesis.

### Current Blockers

| Blocker | Status | Required in Phase |
|---|---|---|
| `snapshot_type` missing from all 1,205 TSL odds records | BLOCKING | 6B |
| TSL `match_id` (numeric `3452364.1`) ↔ model `game_id` (WBC pool code `A05`) bridge absent — overlap = 0 | BLOCKING | 6C |
| `expected_clv` and `trailing_clv` fields exist in prediction_registry but are placeholder 0.0 | BLOCKING | 6C |
| `postgame_results` ↔ `prediction_registry` game_id overlap = 2/9 (WBC codes) | PARTIAL | 6D |
| Benchmark model per-match probability outputs not persisted to any file | BLOCKING | 6C |
| CLV_high sample = 38 (need ≥200 per bucket) | INSUFFICIENT | 6D + 6E |

---

## 1. Evidence Read

| File | Status | Key Findings |
|---|---|---|
| `docs/orchestration/phase6_market_signal_data_pipeline_design_2026-04-29.md` | ✅ Read | Full Phase 6 design: data inventory, gap table, formulas, 6A–6F plan |
| `research/market_signal_validation_20260429.md` | ✅ Read | Phase 5.5 decision: NEEDS_DATA_PIPELINE; CLV_high sample = 38; benchmark predictions absent |
| `research/market_signal_hypothesis_2026-04-29.md` | ✅ Read | Hypothesis source, CLV_proxy definition, required data sources |
| `data/tsl_odds_history.jsonl` | ✅ Read | 1,205 rows, 411 unique match_ids, fields: match_id/fetched_at/game_time/home_team_name/away_team_name/markets[{marketCode, outcomes}]; no snapshot_type; odds as string |
| `data/wbc_backend/reports/prediction_registry.jsonl` | ✅ Read | 66 rows, game_id format "A05"/"D06", decision=NO_BET for all, expected_clv=0.0, trailing_clv=0.0, edge_tier=FORBIDDEN, confidence_score=0.82, diagnostics keys: model_count/stack_confidence/snr/divergence/regime/wbc_eb_delta/wbc_pitch_delta/wbc_star_delta |
| `data/wbc_backend/reports/postgame_results.jsonl` | ✅ Read | 49 rows, game_id format mixed (WBC codes AND numeric 788xxx), actual_result with home_score/away_score/home_win, evaluation with brier/logloss/winner_correct, no odds linked |
| `data/wbc_backend/model_artifacts.json` | ✅ Read | keys: calibration/params/odds_band_stats; params: min_train_games/retrain_every/ev_threshold/lookback/min_confidence |
| `data/wbc_backend/market_validation.json` | ✅ Read | ML: ml_roi=-0.0085, RL: rl_roi=-0.0353, OU: ou_roi=-0.121; aggregate only |
| `data/wbc_backend/portfolio_risk.json` | ✅ Read | bankroll=81500, drawdown=0.185, is_circuit_breaker_active, consecutive_losses |
| `config/settings.py` | ✅ Read | EV_STRONG=0.07, EV_MEDIUM=0.03, EV_PASS=0.01, KELLY_FRACTION=0.15, DAILY_LOSS_STOP_PCT=0.15, DRAWDOWN_MAX=0.20 |
| `strategy/risk_control.py` | ✅ Read | RiskStatus(GREEN/YELLOW/RED), evaluates daily_loss, model_error_consecutive, market_anomaly_count |

---

## 2. Canonical Entity Model

### 2.1 Entity: MatchIdentity

**Purpose:** Single source of truth for a sporting match. All other entities reference
a match via `canonical_match_id`.

**Natural key:** `canonical_match_id` (see §3 for derivation rules)

| Field | Type | Required | Description |
|---|---|---|---|
| `canonical_match_id` | string | YES | Derived composite ID (see §3) |
| `sport` | string | YES | Always `"baseball"` for current scope |
| `league` | string | YES | `WBC` / `CPBL` / `NPB` / `MLB` / `KBO` |
| `match_time_utc` | ISO8601 | YES | Scheduled first pitch in UTC |
| `home_team` | string | YES | Normalized team code e.g. `JPN`, `TPE` |
| `away_team` | string | YES | Normalized team code |
| `season` | string | YES | e.g. `2026`, `2025` |
| `raw_tsl_match_id` | string | OPTIONAL | TSL numeric ID e.g. `3452364.1` (FK bridge) |
| `raw_game_id` | string | OPTIONAL | WBC pool code e.g. `A05` (FK bridge) |
| `venue` | string | OPTIONAL | Stadium / city |
| `match_status` | string | OPTIONAL | `SCHEDULED` / `IN_PROGRESS` / `FINAL` / `POSTPONED` |

**Validation rules:**
- `canonical_match_id` must not be null
- `match_time_utc` must be valid ISO8601 with UTC offset
- `home_team` ≠ `away_team`
- `league` must be in known set: `{WBC, CPBL, NPB, MLB, KBO, OTHERS}`
- `match_status` defaults to `SCHEDULED` if omitted

---

### 2.2 Entity: MarketIdentity

**Purpose:** Identifies a specific betting market for a match (moneyline, handicap, over/under, etc.).

**Natural key:** `market_key` (see §3)

| Field | Type | Required | Description |
|---|---|---|---|
| `market_key` | string | YES | Derived composite key |
| `canonical_match_id` | string | YES | FK → MatchIdentity |
| `market_type` | string | YES | `ML` / `RL` / `OU` / `OE` / `OTHER` |
| `market_line` | string | OPTIONAL | Handicap line e.g. `-1.5` or OU total e.g. `8.5`; null for moneyline |
| `bookmaker` | string | YES | e.g. `TSL_BLOB3RD` |
| `raw_market_code` | string | OPTIONAL | Original TSL code: `MNL` / `HDC` / `OU` / `OE` / `TTO` |

**Market type normalization (TSL → contract):**

| TSL `marketCode` | Contract `market_type` | Notes |
|---|---|---|
| `MNL` | `ML` | Moneyline / win-loss |
| `HDC` | `RL` | Run-line / handicap |
| `OU` | `OU` | Over-under total runs |
| `OE` | `OE` | Odd-even total |
| `TTO` | `OTHER` | Total-team-over (alternative total) |

---

### 2.3 Entity: OddsSnapshot

**Purpose:** A single timestamped odds observation for a market selection.
Multiple snapshots per market exist at different points in time.

**Natural key:** `snapshot_id` (UUID)

| Field | Type | Required | Description |
|---|---|---|---|
| `snapshot_id` | UUID string | YES | Unique per snapshot row |
| `canonical_match_id` | string | YES | FK → MatchIdentity |
| `market_key` | string | YES | FK → MarketIdentity |
| `selection_key` | string | YES | FK → selection-level key (see §3) |
| `snapshot_type` | enum | YES | `OPENING` / `CLOSING` / `INTERMEDIATE` / `POST_MATCH` |
| `snapshot_time_utc` | ISO8601 | YES | When the odds were fetched (UTC) |
| `market_type` | string | YES | Same as MarketIdentity |
| `market_line` | string | OPTIONAL | Null for ML |
| `selection` | string | YES | `home` / `away` / `over` / `under` / `odd` / `even` |
| `decimal_odds` | float | YES | e.g. `1.72` |
| `implied_probability` | float | YES | `1 / decimal_odds` |
| `bookmaker` | string | YES | e.g. `TSL_BLOB3RD` |
| `raw_match_id` | string | OPTIONAL | TSL match_id before normalization |
| `raw_outcome_name` | string | OPTIONAL | TSL outcomeName before normalization |
| `ingestion_run_id` | string | YES | Batch ID that produced this record |
| `schema_version` | string | YES | e.g. `"1.0"` |
| `data_quality_flags` | list[string] | YES | e.g. `[]` or `["MISSING_CANONICAL_ID", "ODDS_STRING_CAST"]` |

**snapshot_type classification rules:**

```
CLOSING_WINDOW_MINUTES = 30  # from config

if snapshot_time_utc >= match_time_utc:
    snapshot_type = "POST_MATCH"   # excluded from CLV computation
elif match_time_utc - 30min <= snapshot_time_utc < match_time_utc:
    snapshot_type = "CLOSING"
elif snapshot_time_utc < match_time_utc AND is_first_for(match × market × selection):
    snapshot_type = "OPENING"
else:
    snapshot_type = "INTERMEDIATE"
```

**Leakage guard:** `snapshot_time_utc < match_time_utc` must hold for OPENING and CLOSING.
POST_MATCH records must never be used in CLV computation.

---

### 2.4 Entity: ModelPrediction

**Purpose:** A model's probability estimate for a market selection, recorded before the match.

**Natural key:** `prediction_id` (UUID)

| Field | Type | Required | Description |
|---|---|---|---|
| `prediction_id` | UUID string | YES | Unique per prediction |
| `canonical_match_id` | string | YES | FK → MatchIdentity (must use same canonical form) |
| `schema_version` | string | YES | e.g. `"1.0"` |
| `model_version` | string | YES | e.g. `"gbm_stack_v2.1"` — currently NOT stored |
| `feature_version` | string | YES | e.g. `"features_32_v1"` — currently NOT stored |
| `prediction_time_utc` | ISO8601 | YES | When inference ran — currently approximated by `recorded_at_utc` |
| `market_type` | string | YES | `ML` / `RL` / `OU` |
| `market_line` | string | OPTIONAL | Null for ML |
| `selection` | string | YES | `home` / `away` / `over` / `under` |
| `predicted_probability` | float | YES | e.g. `0.55` (home win prob for ML) |
| `confidence` | float | YES | Model confidence score (currently `confidence_score` in registry) |
| `expected_value` | float | YES | `predicted_prob × decimal_odds - 1` at decision time |
| `risk_features` | object | OPTIONAL | `{snr, divergence, regime, wbc_pitch_delta, wbc_eb_delta}` |
| `training_window_id` | string | YES | Identifies training data window — currently NOT stored |
| `walk_forward_split_id` | string | YES | Walk-forward fold identifier — currently NOT stored |
| `leakage_guard_version` | string | YES | Version of leakage rules applied — currently NOT stored |

**Validation rules:**
- `0.0 ≤ predicted_probability ≤ 1.0`
- `prediction_time_utc < match_time_utc`
- `prediction_time_utc` must be before closing odds snapshot
- `model_version` must not be empty
- `canonical_match_id` must resolve to a known MatchIdentity

---

### 2.5 Entity: BettingDecision

**Purpose:** Records whether a bet was placed for a given prediction, including stake and risk reasoning.

**Natural key:** `decision_id` (UUID)

| Field | Type | Required | Description |
|---|---|---|---|
| `decision_id` | UUID string | YES | Unique per decision |
| `schema_version` | string | YES | `"1.0"` |
| `canonical_match_id` | string | YES | FK → MatchIdentity |
| `prediction_ref` | UUID string | YES | FK → ModelPrediction.prediction_id |
| `odds_snapshot_ref` | UUID string | YES | FK → OddsSnapshot.snapshot_id at decision time |
| `market_type` | string | YES | `ML` / `RL` / `OU` |
| `market_line` | string | OPTIONAL | |
| `selection` | string | YES | `home` / `away` / `over` / `under` |
| `decision_time_utc` | ISO8601 | YES | When decision was made |
| `bet_decision` | enum | YES | `BET` / `NO_BET` |
| `stake_fraction` | float | OPTIONAL | Fraction of bankroll (Kelly-adjusted); null if NO_BET |
| `expected_value` | float | YES | EV at decision time (currently `expected_clv` = 0.0 placeholder) |
| `risk_cap_reason` | string | OPTIONAL | Why stake was capped below Kelly recommendation |
| `no_bet_reason` | string | OPTIONAL | Why no bet was placed (e.g. `"FORBIDDEN_TIER"`, `"BELOW_EV_THRESHOLD"`) |
| `model_version` | string | YES | Same as prediction model_version |

**Current state:** All 66 existing prediction_registry rows have `bet_decision = NO_BET`
and `expected_value = 0.0`. No actual BET records exist. Settlement cannot be computed.

---

### 2.6 Entity: SettlementResult

**Purpose:** Records the verified final result for a match and computes realized ROI per bet.

**Natural key:** `settlement_id` (UUID)

| Field | Type | Required | Description |
|---|---|---|---|
| `settlement_id` | UUID string | YES | Unique per settlement |
| `schema_version` | string | YES | `"1.0"` |
| `canonical_match_id` | string | YES | FK → MatchIdentity |
| `decision_ref` | UUID string | YES | FK → BettingDecision.decision_id |
| `settled_at_utc` | ISO8601 | YES | When result was confirmed |
| `result_source` | string | YES | e.g. `"AP_NEWS"`, `"WBC_OFFICIAL"`, `"MANUAL_VERIFIED"` |
| `final_score` | object | YES | `{home_score: int, away_score: int}` |
| `market_type` | string | YES | |
| `market_line` | string | OPTIONAL | |
| `selection` | string | YES | |
| `outcome` | string | YES | `home_win` / `away_win` / `over` / `under` / `odd` / `even` / `push` |
| `hit` | bool | YES | Did the bet selection win? |
| `stake` | float | OPTIONAL | Absolute stake; null if NO_BET |
| `payout` | float | OPTIONAL | Payout received; null if NO_BET |
| `realized_roi` | float | OPTIONAL | `(payout - stake) / stake`; null if NO_BET |
| `closing_line_value` | float | OPTIONAL | `predicted_prob - implied_prob(closing_odds)` |
| `settlement_quality_flags` | list[string] | YES | e.g. `[]` or `["UNVERIFIED_SOURCE"]` |

**Validation rules:**
- `settled_at_utc > match_time_utc`
- `realized_roi` is null (not zero) when `bet_decision = NO_BET`
- `hit` must be consistent with `outcome` and `selection`
- `result_source` must be in approved source list

---

### 2.7 Entity: CLVValidationRecord

**Purpose:** One row per bet-eligible prediction joining odds, prediction, decision, and settlement
for CLV analysis. This is the primary input to the Phase 6E validation script.

**Natural key:** `validation_id` (UUID)

| Field | Type | Required | Description |
|---|---|---|---|
| `validation_id` | UUID string | YES | Unique per record |
| `schema_version` | string | YES | `"1.0"` |
| `canonical_match_id` | string | YES | |
| `market_type` | string | YES | |
| `market_line` | string | OPTIONAL | |
| `selection` | string | YES | |
| `prediction_ref` | UUID | YES | FK → ModelPrediction |
| `opening_odds_ref` | UUID | YES | FK → OddsSnapshot (OPENING type) |
| `closing_odds_ref` | UUID | YES | FK → OddsSnapshot (CLOSING type) |
| `decision_ref` | UUID | YES | FK → BettingDecision |
| `settlement_ref` | UUID | OPTIONAL | FK → SettlementResult; null if match not yet settled |
| `predicted_probability` | float | YES | From ModelPrediction |
| `implied_probability_open` | float | YES | `1 / opening_decimal_odds` |
| `implied_probability_close` | float | YES | `1 / closing_decimal_odds` |
| `clv_probability_delta` | float | YES | `predicted_probability - implied_probability_close` |
| `market_movement_delta` | float | YES | `implied_probability_close - implied_probability_open` |
| `realized_roi` | float | OPTIONAL | From SettlementResult; null if unsettled or NO_BET |
| `hit` | bool | OPTIONAL | From SettlementResult |
| `leakage_status` | enum | YES | `PASS` / `FAIL` / `WARNING` / `UNKNOWN` |
| `sample_bucket` | string | YES | `CLV_HIGH` / `CLV_MID` / `CLV_LOW` / `UNCLASSIFIED` |
| `validation_window_id` | string | YES | e.g. `"2026-Q1"` — groups records for one validation run |

**sample_bucket classification:**

```
if clv_probability_delta > 0.03:   sample_bucket = "CLV_HIGH"
elif clv_probability_delta >= 0.0: sample_bucket = "CLV_MID"
else:                               sample_bucket = "CLV_LOW"
```

---

### 2.8 Entity: LeakageAuditRecord

**Purpose:** Per-prediction audit trail confirming leakage rules were checked.

**Natural key:** `audit_id` (UUID)

| Field | Type | Required | Description |
|---|---|---|---|
| `audit_id` | UUID string | YES | |
| `schema_version` | string | YES | `"1.0"` |
| `prediction_ref` | UUID | YES | FK → ModelPrediction |
| `canonical_match_id` | string | YES | |
| `audit_time_utc` | ISO8601 | YES | When audit was run |
| `leakage_guard_version` | string | YES | e.g. `"v1.0"` |
| `checks` | list[object] | YES | Per-rule results: `{rule_id, status, detail}` |
| `overall_status` | enum | YES | `PASS` / `FAIL` / `WARNING` / `UNKNOWN` |
| `disqualified_reason` | string | OPTIONAL | Set if `overall_status = FAIL` |

---

## 3. Canonical ID Strategy

### 3.1 Current Problem

The two primary data sources use incompatible identifier systems:

| Source | ID Format | Example | Namespace |
|---|---|---|---|
| `tsl_odds_history.jsonl` | TSL numeric match ID | `3452364.1` | TSL internal |
| `prediction_registry.jsonl` | WBC pool-code game ID | `A05` | WBC tournament grid |
| `postgame_results.jsonl` | Mixed: WBC codes AND numeric | `B06`, `788130` | Mixed — both systems appear |

**Overlap as of 2026-04-29:** 0 rows (TSL numeric IDs never appear in prediction registry;
WBC pool codes never appear in TSL odds history).

### 3.2 Proposed Canonical Match ID

```
canonical_match_id = "{sport}:{league}:{date_utc}:{home_team_code}:{away_team_code}"
```

**Construction rules:**

| Component | Rule | Example |
|---|---|---|
| `sport` | Always `"baseball"` for current scope | `baseball` |
| `league` | Uppercase normalized league code | `WBC`, `CPBL`, `NPB` |
| `date_utc` | Date only in UTC (YYYYMMDD) | `20260313` |
| `home_team_code` | Uppercase 3-letter normalized code | `JPN`, `TPE`, `USA` |
| `away_team_code` | Same | `KOR`, `MEX` |

**Full example:**
```
baseball:WBC:20260313:JPN:KOR
```

### 3.3 ID Construction from Existing Sources

**From TSL `tsl_odds_history.jsonl`:**
```python
# game_time = "2026-03-13T12:00:00+08:00"  → UTC: 20260313
# home_team_name = "羅德海洋"               → normalize to team code (requires lookup table)
# away_team_name = "西武獅"                 → normalize to team code
canonical_match_id = f"baseball:CPBL:{date_utc}:{home_code}:{away_code}"
```

**From Prediction Registry `game_id = "A05"`:**
```python
# Requires wbc_2026_authoritative_snapshot.json lookup:
# game_id A05 → home=CUB, away=COL, match_time=2026-03-08
canonical_match_id = f"baseball:WBC:20260308:CUB:COL"
```

**DOMAIN_DESIGN_REQUIRED: Team name normalization table**
**MISSING_EVIDENCE:** TSL uses Chinese team names (e.g. `"羅德海洋"` for Rakuten Monkeys,
`"西武獅"` for Seibu Lions). No normalization table currently maps Chinese names to
3-letter codes. Required for canonical_match_id construction from TSL data.

### 3.4 Proposed market_key and selection_key

```
market_key   = "{canonical_match_id}:{market_type}:{market_line_or_NULL}"
selection_key = "{market_key}:{selection}"
```

**Examples:**
```
market_key    = "baseball:CPBL:20260313:RAK:SEI:ML:NULL"
selection_key = "baseball:CPBL:20260313:RAK:SEI:ML:NULL:home"

market_key    = "baseball:WBC:20260308:CUB:COL:OU:8.5"
selection_key = "baseball:WBC:20260308:CUB:COL:OU:8.5:over"
```

### 3.5 Collision / Ambiguity Handling

| Scenario | Handling |
|---|---|
| Same teams play twice on same UTC day | Append disambiguator: `{canonical_match_id}:g2` |
| Team name maps to multiple codes | Flag `data_quality_flags: ["AMBIGUOUS_TEAM_NAME"]`; exclude from analysis |
| Doubleheader with different local day but same UTC date | Use `match_time_utc` minute precision in edge-case variant |
| TSL match_id with `.1` suffix (e.g. `3452364.1`) | Strip `.1` suffix when joining to base match, retain full ID in `raw_tsl_match_id` |
| WBC pool code with no TSL equivalent | `raw_tsl_match_id = null`; `data_quality_flags: ["NO_TSL_MATCH"]` |

---

## 4. JSONL Schema Contracts

### 4.1 odds_snapshots.jsonl

```jsonc
{
  "schema_version": "1.0",
  "snapshot_id": "550e8400-e29b-41d4-a716-446655440001",
  "source": "TSL_BLOB3RD",
  "canonical_match_id": "baseball:CPBL:20260313:RAK:SEI",
  "raw_match_id": "3452364.1",
  "sport": "baseball",
  "league": "CPBL",
  "match_time_utc": "2026-03-13T04:00:00Z",
  "snapshot_time_utc": "2026-03-13T03:30:16Z",
  "snapshot_type": "OPENING",
  "market_type": "ML",
  "market_line": null,
  "selection": "away",
  "decimal_odds": 1.53,
  "implied_probability": 0.6536,
  "bookmaker": "TSL_BLOB3RD",
  "ingestion_run_id": "run_20260313_001",
  "data_quality_flags": []
}
```

**Field notes:**
- `decimal_odds`: cast from TSL string `"1.53"` to float
- `implied_probability`: computed at ingest as `round(1 / decimal_odds, 6)`
- `snapshot_type`: derived from `snapshot_time_utc` vs `match_time_utc` (Phase 6B)
- `canonical_match_id`: derived via normalization (Phase 6C team lookup)

---

### 4.2 model_predictions.jsonl

```jsonc
{
  "schema_version": "1.0",
  "prediction_id": "550e8400-e29b-41d4-a716-446655440002",
  "model_version": "gbm_stack_v2.1",
  "feature_version": "features_32_v1",
  "canonical_match_id": "baseball:WBC:20260308:CUB:COL",
  "prediction_time_utc": "2026-03-08T11:32:00Z",
  "market_type": "ML",
  "market_line": null,
  "selection": "home",
  "predicted_probability": 0.48,
  "confidence": 0.8208,
  "expected_value": 0.0,
  "risk_features": {
    "snr": 0.72,
    "divergence": 0.04,
    "regime": "pool",
    "wbc_pitch_delta": -12,
    "wbc_eb_delta": 0.01
  },
  "training_window_id": "tw_2024_mlb_2188",
  "walk_forward_split_id": "wf_fold_01",
  "leakage_guard_version": "v1.0"
}
```

**Gap note:** `model_version`, `feature_version`, `training_window_id`, `walk_forward_split_id`,
and `leakage_guard_version` are all currently absent from `prediction_registry.jsonl`.
These must be added in Phase 6C.

---

### 4.3 betting_decisions.jsonl

```jsonc
{
  "schema_version": "1.0",
  "decision_id": "550e8400-e29b-41d4-a716-446655440003",
  "canonical_match_id": "baseball:WBC:20260308:CUB:COL",
  "market_type": "ML",
  "market_line": null,
  "selection": "home",
  "decision_time_utc": "2026-03-08T11:32:11Z",
  "bet_decision": "NO_BET",
  "stake_fraction": null,
  "expected_value": 0.0,
  "risk_cap_reason": null,
  "no_bet_reason": "FORBIDDEN_TIER",
  "model_version": "gbm_stack_v2.1",
  "prediction_ref": "550e8400-e29b-41d4-a716-446655440002",
  "odds_snapshot_ref": null
}
```

**Gap note:** `odds_snapshot_ref` is null for all current records because prediction registry
and TSL odds history cannot be joined (match_id overlap = 0).

---

### 4.4 settlement_results.jsonl

```jsonc
{
  "schema_version": "1.0",
  "settlement_id": "550e8400-e29b-41d4-a716-446655440004",
  "canonical_match_id": "baseball:WBC:20260313:MEX:BRA",
  "decision_ref": "550e8400-e29b-41d4-a716-446655440003",
  "settled_at_utc": "2026-03-09T14:59:14Z",
  "result_source": "AP_NEWS",
  "final_score": {"home_score": 16, "away_score": 0},
  "market_type": "ML",
  "market_line": null,
  "selection": "home",
  "outcome": "home_win",
  "hit": true,
  "stake": null,
  "payout": null,
  "realized_roi": null,
  "closing_line_value": null,
  "settlement_quality_flags": ["NO_BET_PLACED"]
}
```

**Gap note:** `realized_roi` and `closing_line_value` are null because no actual BET
was placed (all current decisions = NO_BET). These fields remain null until real bets are placed.

---

### 4.5 clv_validation_records.jsonl

```jsonc
{
  "schema_version": "1.0",
  "validation_id": "550e8400-e29b-41d4-a716-446655440005",
  "canonical_match_id": "baseball:CPBL:20260313:RAK:SEI",
  "market_type": "ML",
  "market_line": null,
  "selection": "away",
  "prediction_ref": "550e8400-e29b-41d4-a716-446655440002",
  "opening_odds_ref": "550e8400-e29b-41d4-a716-446655440001",
  "closing_odds_ref": "550e8400-e29b-41d4-a716-446655441001",
  "decision_ref": "550e8400-e29b-41d4-a716-446655440003",
  "settlement_ref": "550e8400-e29b-41d4-a716-446655440004",
  "predicted_probability": 0.68,
  "implied_probability_open": 0.6536,
  "implied_probability_close": 0.6289,
  "clv_probability_delta": 0.0511,
  "market_movement_delta": -0.0247,
  "realized_roi": -1.0,
  "hit": false,
  "leakage_status": "PASS",
  "sample_bucket": "CLV_HIGH",
  "validation_window_id": "2026-Q1"
}
```

---

## 5. Field-Level Validation Rules

### 5.1 Numeric Range Rules

| Field | Rule | Fail Action |
|---|---|---|
| `decimal_odds` | `> 1.0` | Reject row; add `"INVALID_ODDS"` to `data_quality_flags` |
| `implied_probability` | `0.0 < implied_probability ≤ 1.0` | Reject row |
| `predicted_probability` | `0.0 ≤ predicted_probability ≤ 1.0` | Reject row |
| `stake_fraction` | `0.0 < stake_fraction ≤ 1.0` when present | Warn; cap at `MAX_SINGLE_BET_PCT = 0.015` per config |
| `realized_roi` | `>= -1.0` (cannot lose more than stake) | Flag `"INVALID_ROI"` |
| `clv_probability_delta` | Unbounded but expected in `(-0.3, +0.3)` | Warn if outside range |
| `confidence` | `0.0 ≤ confidence ≤ 1.0` | Reject row |

### 5.2 Enum Rules

| Field | Allowed Values |
|---|---|
| `snapshot_type` | `OPENING` / `CLOSING` / `INTERMEDIATE` / `POST_MATCH` |
| `market_type` | `ML` / `RL` / `OU` / `OE` / `OTHER` |
| `bet_decision` | `BET` / `NO_BET` |
| `leakage_status` | `PASS` / `FAIL` / `WARNING` / `UNKNOWN` |
| `sample_bucket` | `CLV_HIGH` / `CLV_MID` / `CLV_LOW` / `UNCLASSIFIED` |
| `overall_status` (audit) | `PASS` / `FAIL` / `WARNING` / `UNKNOWN` |
| `match_status` | `SCHEDULED` / `IN_PROGRESS` / `FINAL` / `POSTPONED` |
| `selection` | `home` / `away` / `over` / `under` / `odd` / `even` / `push` |

### 5.3 Timestamp Rules

| Rule | Description |
|---|---|
| `prediction_time_utc < match_time_utc` | Model must predict before game starts |
| `closing snapshot_time_utc < match_time_utc` | Closing odds must be pre-game |
| `opening snapshot_time_utc < match_time_utc` | Opening odds must be pre-game |
| `settled_at_utc > match_time_utc` | Settlement only after game ends |
| `snapshot_time_utc < match_time_utc` for OPENING / CLOSING | Leakage hard rule |
| `prediction_time_utc < closing_snapshot_time_utc` | Cannot predict after closing line |

### 5.4 Required-Field Rules

| Rule | Applies To |
|---|---|
| `canonical_match_id` must not be null | All entities |
| `snapshot_type` must not be null | OddsSnapshot |
| `model_version` must not be empty string | ModelPrediction |
| `prediction_time_utc` must be set | ModelPrediction |
| `bet_decision` must be set | BettingDecision |
| `hit` and `outcome` must both be set if `bet_decision = BET` and `settled_at_utc` exists | SettlementResult |

---

## 6. Leakage Rules

### 6.1 Hard-Fail Rules (leakage_status = FAIL — record excluded from analysis)

| Rule ID | Condition | Description |
|---|---|---|
| L1 | `prediction_time_utc >= match_time_utc` | Prediction made after game started |
| L2 | `prediction_time_utc >= closing_snapshot_time_utc` | Model saw closing odds (forward leakage) |
| L3 | Closing odds appear in model feature vector for same prediction | Model was trained on the line it is now predicting against |
| L4 | Settlement result joined before `prediction_time_utc` | Outcome accessed at inference time |
| L5 | Training fold includes any game with `match_time_utc > fold_cutoff_utc` | Walk-forward split boundary violation |
| L6 | `odds_snapshot.snapshot_time_utc` is null or unparseable | Cannot verify temporal ordering |
| L7 | `canonical_match_id` ambiguous — maps to >1 known match | Join may be incorrect |

### 6.2 Warning-Only Rules (leakage_status = WARNING — record flagged but included with caveat)

| Rule ID | Condition | Description |
|---|---|---|
| W1 | Only one odds snapshot exists for this match × market × selection | Cannot distinguish opening from closing; temporal analysis unreliable |
| W2 | Closing odds estimated from latest pre-match snapshot, not a tagged CLOSING record | May be `INTERMEDIATE` used as proxy |
| W3 | `INTERMEDIATE` snapshot used as closing proxy due to no CLOSING tag | Snapshot type approximation |
| W4 | Bookmaker or source changes between opening and closing snapshot | Line may not be from the same market liquidity pool |
| W5 | `prediction_time_utc` approximated from `recorded_at_utc` rather than inference timestamp | Temporal ordering less certain |

---

## 7. Sample Sufficiency Rules

All thresholds are:
**PROVISIONAL_THRESHOLD_REQUIRES_RECALIBRATION**

These thresholds are Betting-pool-native estimates based on standard power analysis for
two-sample t-tests (α=0.05, power=0.80, assumed effect size Cohen's d ≈ 0.3–0.4 for ROI
comparison). They are NOT copied from any external system and must be recalibrated once
Betting-pool has larger samples of actual settled bets.

| Validation Type | Minimum N | Rationale |
|---|---|---|
| CLV_HIGH bucket (CLV_prob_delta > 0.03) | **≥ 200 settled decisions** | Two-sample t-test power requirement vs CLV_LOW |
| CLV_LOW bucket (CLV_prob_delta ≤ 0) | **≥ 200 settled decisions** | Comparison baseline |
| Market movement validation (opening→closing odds pairs) | **≥ 300 matched pairs** | Line movement correlation analysis |
| ROI validation (any strategy vs benchmark) | **≥ 300 settled decisions** | Standard sports betting power threshold |
| Per-market validation (ML only, RL only, OU only) | **≥ 150 settled decisions per market** | Market-segmented ROI comparison |
| Per-regime validation (LIQUID_MARKET etc.) | **≥ 100 settled decisions per regime** | Regime-segmented CLV analysis |
| Walk-forward split (test fold) | **≥ 500 historical matches where available** | Deployment gate already uses 500; preserve |
| Calibration stability window | **≥ 500 games** | Existing deployment gate threshold; maintain |

**Current state vs thresholds:**

| Bucket | Current N | Required N | Status |
|---|---|---|---|
| CLV_HIGH (proxy-based, WBC 2026 only) | 38 | 200 | INSUFFICIENT — 5.3× gap |
| CLV_LOW | ~244 (proxy 2026) | 200 | BORDERLINE — needs settlement data |
| ML settled decisions | 0 actual BET records | 150 | MISSING |
| RL settled decisions | 0 actual BET records | 150 | MISSING |
| OU settled decisions | 0 actual BET records | 150 | MISSING |

---

## 8. Backward Compatibility Plan

Existing files must NOT be modified. Adapters bridge the gap between existing format
and the new contract schema. These adapters are designed in this document; implemented in later phases.

### 8.1 Compatibility Table

| Existing File | Current Fields | Missing Contract Fields | Migration / Adapter Strategy |
|---|---|---|---|
| `data/tsl_odds_history.jsonl` | `match_id`, `fetched_at`, `game_time`, `home_team_name`, `away_team_name`, `source`, `markets[{marketCode, outcomes[{outcomeName, odds}]}]` | `canonical_match_id`, `snapshot_id`, `snapshot_type`, `implied_probability`, `market_type` (normalized), `selection` (normalized), `decimal_odds` (float-cast), `ingestion_run_id`, `schema_version`, `data_quality_flags` | **Adapter 6B:** Read TSL records, derive `snapshot_type` from `fetched_at` vs `game_time`, cast `odds` string → float, compute `implied_probability`, normalize `marketCode` → `market_type`, normalize `outcomeName` → `selection`, derive `canonical_match_id` via team normalization lookup. Write to `odds_snapshots.jsonl` (new file). Original file unchanged. |
| `data/wbc_backend/reports/prediction_registry.jsonl` | `game_id`, `recorded_at_utc`, `teams.{home, away}`, `prediction.{home_win_prob, confidence_score, diagnostics}`, `decision_report.{decision, expected_clv, trailing_clv, edge_tier}` | `canonical_match_id`, `prediction_id`, `model_version`, `feature_version`, `prediction_time_utc`, `market_type`, `selection`, `expected_value` (non-zero), `training_window_id`, `walk_forward_split_id`, `leakage_guard_version`, `schema_version` | **Adapter 6C:** Map `game_id` → `canonical_match_id` via WBC schedule lookup (`wbc_2026_authoritative_snapshot.json`). Map `recorded_at_utc` → `prediction_time_utc` (approximation; flag W5). Map `confidence_score` → `confidence`. Generate `prediction_id` as UUID. `model_version` requires code change to persist at inference time. Write to `model_predictions.jsonl` (new file). Original file unchanged. |
| `data/wbc_backend/reports/postgame_results.jsonl` | `game_id`, `recorded_at_utc`, `teams`, `actual_result.{home_score, away_score, home_win}`, `prediction_summary.{decision, predicted_home_win_prob}`, `evaluation.{winner_correct, home_win_brier}` | `canonical_match_id`, `settlement_id`, `decision_ref`, `settled_at_utc`, `result_source`, `outcome`, `hit`, `stake`, `payout`, `realized_roi`, `closing_line_value`, `settlement_quality_flags`, `schema_version` | **Adapter 6D:** Map `game_id` → `canonical_match_id` (WBC schedule lookup; same as 6C). Map `actual_result.home_win` → `outcome` (`home_win` / `away_win`). Map `recorded_at_utc` → `settled_at_utc`. Generate `settlement_id` as UUID. `decision_ref` requires joining prediction_registry adapter output. `realized_roi` = null for all current records (NO_BET). Write to `settlement_results.jsonl` (new file). Original file unchanged. |

### 8.2 Bridge Priority

The most critical compatibility gap is the **match_id bridge** between TSL and prediction registry.
Without this bridge, `clv_validation_records.jsonl` cannot be populated.

Priority order:
1. Team name normalization table (TSL Chinese → 3-letter code)
2. WBC game_id → match_time_utc + teams mapping (already in `wbc_2026_authoritative_snapshot.json`)
3. Canonical ID construction functions
4. snapshot_type classification logic

---

## 9. Implementation Acceptance Criteria

The following criteria define done-ness for each later phase:

### Phase 6B (Crawler / Ingestor Changes)

- [ ] All new TSL odds snapshots written to `odds_snapshots.jsonl` include `snapshot_type` field
- [ ] `snapshot_type` correctly classified as `OPENING` for first pre-match snapshot per match × market × selection
- [ ] `snapshot_type = CLOSING` only when `snapshot_time_utc ≥ match_time_utc - CLOSING_WINDOW_MINUTES`
- [ ] `POST_MATCH` records are tagged and excluded from CLV computation
- [ ] `decimal_odds` cast from string to float at ingest
- [ ] `implied_probability = 1 / decimal_odds` computed at ingest
- [ ] Historical JSONL records without `snapshot_type` are processed with `snapshot_type = INTERMEDIATE` fallback
- [ ] Existing crawler tests pass unchanged

### Phase 6C (Prediction Registry Enhancement)

- [ ] New prediction records include `canonical_match_id`, `model_version`, `feature_version`, `prediction_time_utc`
- [ ] `canonical_match_id` constructed from WBC schedule lookup resolves ≥95% of WBC game_ids
- [ ] `prediction_time_utc` confirmed before `match_time_utc` for all records (leakage rule L1)
- [ ] `model_version` non-empty for all new records
- [ ] Old records without these fields handled gracefully (nullable fields)

### Phase 6D (Settlement Join)

- [ ] `settlement_results.jsonl` covers ≥95% of known completed WBC 2026 matches
- [ ] `decision_ref` successfully joins settlement to betting_decisions for all BET records
- [ ] `realized_roi` is null (not 0.0) for all NO_BET records
- [ ] `settled_at_utc > match_time_utc` holds for all records (validation rule)
- [ ] Script is idempotent

### Phase 6E (CLV Validation Script)

- [ ] Script produces `clv_validation_records.jsonl`
- [ ] All 7 leakage hard-fail rules checked per record
- [ ] `leakage_status` set per record
- [ ] Sample bucket counts reported before statistical test
- [ ] If `CLV_HIGH N < 200`: output `NEEDS_MORE_DATA`, not a validation decision
- [ ] No external API calls
- [ ] No production betting action triggered

### Phase 6F (Orchestrator Integration)

- [ ] Planner routes `NEEDS_DATA_PIPELINE` → creates `data_pipeline` task, not re-validation
- [ ] `data_pipeline` task has correct dedupe_key preventing duplicate creation
- [ ] No auto-promotion of strategy
- [ ] Existing exploration/validation task routing unaffected

---

## 10. Future Task Boundaries

| Phase | Scope | What Changes |
|---|---|---|
| **6A (this document)** | Documentation only | Defines schemas, rules, IDs, compatibility plan — no code, DB, or data changes |
| **6B** | Odds ingestion — snapshot_type | Modifies `data/tsl_crawler_v2.py`; adds `snapshot_type` to new TSL records; writes to `odds_snapshots.jsonl` |
| **6C** | Prediction registry enhancement | Modifies prediction export code; adds `canonical_match_id`, `model_version`, `prediction_time_utc` to new records; writes to `model_predictions.jsonl` |
| **6D** | Settlement join | New script `scripts/build_settlement_join.py`; reads postgame_results + predictions; writes `settlement_results.jsonl` |
| **6E** | CLV validation script | New script `scripts/validate_clv_signal.py`; reads `clv_validation_records`; outputs validation decision report |
| **6F** | Orchestrator routing | Modifies `orchestrator/planner_tick.py`; routes `NEEDS_DATA_PIPELINE` → `data_pipeline` task type |

---

## 11. Scope Confirmation

- ✅ No code modified
- ✅ No DB schema changed
- ✅ No crawler changed
- ✅ No model changed
- ✅ No data files modified (existing JSONL / JSON files untouched)
- ✅ No external API called
- ✅ No orchestrator task created
- ✅ No git commit made

---

## 12. Contamination Check

This document was reviewed for disallowed lottery-domain patterns.
All disallowed patterns were searched. Result: 0 occurrences.
This document contains only Betting-pool-native market, odds, and CLV terminology.
