# Phase 6H: Prediction Registry Extension Design — MLB / KBO / NPB
**Date**: 2026-04-29  
**Phase**: 6H (Documentation Only — No Model Changes, No Commits, No Data Modifications)  
**Status**: DESIGN_COMPLETE  
**Depends On**: Phase 6A (CLV Data Contract), Phase 6E (Domain Commitment), Phase 6F (Future Event Capture Manifest), Phase 6G (Dry-Run Verification)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Evidence Read](#2-evidence-read)
3. [Current Prediction Registry Inventory](#3-current-prediction-registry-inventory)
4. [Gap Against Phase 6A Contract](#4-gap-against-phase-6a-contract)
5. [Extended MLB/KBO/NPB Registry Schema](#5-extended-mlbkbonpb-registry-schema)
6. [Prediction Timing / Leakage Rules](#6-prediction-timing--leakage-rules)
7. [Market Coverage Rules](#7-market-coverage-rules)
8. [Model Compatibility Requirements](#8-model-compatibility-requirements)
9. [Backward Compatibility Plan](#9-backward-compatibility-plan)
10. [Registry Quality Gates](#10-registry-quality-gates)
11. [Implementation Roadmap](#11-implementation-roadmap)
12. [Next Prompt — Phase 6I Ready-to-Copy](#12-next-prompt--phase-6i-ready-to-copy)
13. [Scope Confirmation](#13-scope-confirmation)

---

## 1. Executive Summary

### Problem Statement

The current `data/wbc_backend/reports/prediction_registry.jsonl` was designed for WBC tournament games only. It contains 66 rows covering 9 WBC pool games (A05–D06) played on 2026-03-08 to 2026-03-09. **All 7 CLV contract fields required by Phase 6A are absent** (`canonical_match_id`, `market_key`, `selection_key`, `model_version`, `feature_version`, `leakage_guard_version`, `prediction_time_utc`).

Phase 6G dry-run confirmed that 4,356 opening+closing odds pairs exist in `data/derived/` for MLB/KBO/NPB games from 2026-03-13 onward — but **bridge-ready count = 0** because no MLB/KBO/NPB model predictions have been registered. The prediction pipeline and the CLV measurement infrastructure exist on parallel tracks with no overlap.

### Phase 6H Goal

Design the schema, rules, quality gates, and implementation roadmap for a new prediction registry at:

```
data/derived/future_model_predictions_YYYY-MM-DD.jsonl
```

This file format must:
1. Satisfy all 7 CLV contract fields from Phase 6A
2. Express per-market, per-selection predicted probability (not just game-level)
3. Include explicit version identifiers (`model_version`, `feature_version`, `leakage_guard_version`)
4. Link to the match identity bridge via `canonical_match_id`
5. Maintain full backward compatibility with the existing WBC registry
6. Prevent any look-ahead leakage by enforcing strict pre-game prediction timestamps

### Key Finding

Phase 6G established `READINESS_DECISION = NOT_READY_DOMAIN_MISMATCH`. Phase 6H establishes **exactly what must be built** to resolve that mismatch. Phase 6I will implement the adapter layer.

---

## 2. Evidence Read

The following files were inspected during Phase 6H:

| File | Size | Key Finding |
|---|---|---|
| `data/wbc_backend/reports/prediction_registry.jsonl` | 66 rows | WBC-only; all 7 CLV fields absent |
| `data/wbc_backend/model_artifacts.json` | 3 keys | `params.markets=['ML','RL','OU']`; no version fields |
| `data/wbc_backend/walkforward_summary.json` | 11 keys | 2,188 games; ML/RL/OU ROI available |
| `data/wbc_backend/market_validation.json` | 3 keys | ML, RL, OU per-market stats |
| `data/wbc_backend/reports/mlb_decision_quality_report.json` | 1,493 per-game rows | `clv_available=False`; sandbox mode |
| `data/wbc_backend/reports/mlb_paper_tracking_report.json` | 11 keys | PAPER_ONLY; FROZEN_UNTIL_GENUINE_PREGAME |
| `docs/orchestration/phase6a_clv_data_contract_2026-04-29.md` | 36 KB | 7-field CLV contract specification |
| `docs/orchestration/phase6e_domain_commitment_decision_2026-04-29.md` | 18 KB | `DOMAIN_COMMITMENT_MLB_KBO_NPB` |
| `docs/orchestration/phase6f_future_event_capture_manifest_2026-04-29.md` | 33 KB | Capture manifest with timing rules |
| `docs/orchestration/phase6g_manifest_dry_run_report_2026-04-29.md` | 11 KB | 4,356 pairs; bridge_ready=0; NOT_READY |
| `config/settings.py` | 5 KB | `EV_STRONG=0.07`, `EV_MEDIUM=0.03`, `KELLY_FRACTION=0.15`, `DRAWDOWN_MAX=0.20` |

### Registry Inspection Summary

Top-level fields present in all 66 rows:

```
calibration_metrics, decision_report, deployment_gate, game_id,
game_output, portfolio_metrics, prediction, recorded_at_utc,
request, simulation, teams, top_bets, verification
```

Nested `prediction` sub-fields (game-level):

```
game_id, home_win_prob, away_win_prob, expected_home_runs,
expected_away_runs, x_factors, diagnostics, sub_model_results,
confidence_score, market_bias_score
```

Nested `decision_report` sub-fields:

```
match_id, match_label, timestamp, edge_score, edge_tier, edge_valid,
edge_details, real_edge_score, real_edge_label, realism_tradeable,
decay_half_life, decay_urgency, expected_clv, trailing_clv,
timing_action, optimal_delay_minutes, bets, total_exposure_pct,
sharpness_level, market_regime, market_regime_confidence
```

Nested `deployment_gate` sub-fields:

```
status, selected_calibration, checks
```

Note: `bets` is `[]` in all 66 rows; `top_bets` is `[]` in all 66 rows; `model_version`/`feature_version` absent at all nesting levels.

### MLB Decision Quality Report — per_game Fields

```
game_id, regime, decision, edge, clv, brier, logloss,
calibration_flag, predicted_home_win_prob, market_home_prob,
decision_home_prob, closing_home_prob, actual_result,
passed_strict_gate, was_selected_for_bet,
clv_available, clv_source, benchmark_source, paper_pnl
```

Note: `clv_available = False` in all 1,493 rows (sandbox mode, single snapshot, no genuine closing odds).

---

## 3. Current Prediction Registry Inventory

### Schema Coverage Table

| Field | Present in Registry? | Example Value | Problem for MLB/KBO/NPB CLV |
|---|---|---|---|
| `game_id` | ✅ Yes (top-level) | `"A05"` | WBC format only; MLB uses long-form IDs |
| `recorded_at_utc` | ✅ Yes | `"2026-03-08T11:32:11.088607+00:00"` | Can serve as `prediction_time_utc` proxy; must be confirmed pre-game |
| `teams` | ✅ Yes | `{"home":…,"away":…}` | Schema exists but WBC team names differ |
| `prediction.home_win_prob` | ✅ Yes | `0.48` | Game-level only; no per-market breakdown |
| `prediction.away_win_prob` | ✅ Yes | `0.52` | Game-level only |
| `prediction.expected_home_runs` | ✅ Yes | `4.62` | Used for OU derivation; needs line reference |
| `prediction.expected_away_runs` | ✅ Yes | `4.62` | Used for OU derivation; needs line reference |
| `prediction.sub_model_results` | ✅ Yes | list of 6 model outputs | Version-untagged; no `model_version` field |
| `decision_report.expected_clv` | ✅ Yes | `0.0` (sandbox) | CLV computed but always 0.0 (no closing odds) |
| `decision_report.bets` | ✅ Yes | `[]` | Always empty; no active bet tracking |
| `top_bets` | ✅ Yes | `[]` | Always empty |
| `deployment_gate.status` | ✅ Yes | `"READY"` | Gate checks pass; but no version metadata |
| `deployment_gate.selected_calibration` | ✅ Yes | `"isotonic"` | Calibration type recorded |
| **`canonical_match_id`** | ❌ **ABSENT** | — | Cannot join to bridge; bridge_ready=0 |
| **`market_key`** | ❌ **ABSENT** | — | No per-market prediction record |
| **`selection_key`** | ❌ **ABSENT** | — | No per-selection prediction record |
| **`model_version`** | ❌ **ABSENT** | — | Cannot identify which model produced prediction |
| **`feature_version`** | ❌ **ABSENT** | — | Cannot verify feature set stability |
| **`leakage_guard_version`** | ❌ **ABSENT** | — | Cannot audit leakage protection version |
| **`prediction_time_utc`** | ❌ **ABSENT** | — | Must be explicit; `recorded_at_utc` insufficient |
| `odds_snapshot_ref` | ❌ Absent | — | No reference to which odds snapshot was used |

### Coverage Counts

```
Total rows                      :  66
WBC game_ids                    :  9 unique (A05–D06)
Rows with non-empty top_bets    :   0 / 66
CLV contract fields present     :   0 / 7 (0%)
MLB/KBO/NPB rows                :   0 / 66
```

### Root Cause

The registry was built for WBC tournament research (single snapshot, paper-only). It was never designed to support CLV measurement. The `game_id` field is a WBC pool slot identifier, not a universal match ID. Market-level predictions are implicit (derived from `home_win_prob`) rather than explicit named records.

---

## 4. Gap Against Phase 6A Contract

### Phase 6A Required Fields vs Current Availability

| Required Contract Field | Phase 6A Requirement | Current Source | Available? | Needed Design |
|---|---|---|---|---|
| `canonical_match_id` | Unique ID matching bridge table | WBC `game_id` (A05) | ❌ No | New ID generation layer for MLB: e.g. `MLB-2025_04_24-10_05_PM-TEXAS_RANGERS-AT-ATHLETICS` format from `mlb_decision_quality_report` |
| `market_key` | `"ML"` / `"RL"` / `"OU"` | Implicit in `home_win_prob` | ❌ No | Per-market record explosion: one JSONL row per (game × market) |
| `selection_key` | `"home"` / `"away"` / `"over"` / `"under"` | No tracking | ❌ No | Explicit selection field required for each row |
| `model_version` | Semver string e.g. `"v3.2.1"` | Not stored anywhere | ❌ No | Version constant in model module; must be emitted at prediction time |
| `feature_version` | Semver string e.g. `"v2.0.0"` | Not stored anywhere | ❌ No | Feature hash or version constant in feature pipeline |
| `leakage_guard_version` | Semver string e.g. `"v1.0.0"` | Not stored anywhere | ❌ No | Version of the leakage guard module; must be embedded |
| `prediction_time_utc` | ISO-8601 UTC, strictly pre-game | `recorded_at_utc` (proxy) | ⚠️ Partial | `recorded_at_utc` exists but is not explicitly pre-game verified; must add `pre_game_verified: bool` |

### Derivation Feasibility

Some fields can be derived from existing predictions:

| Target Field | Derivation Path | Feasibility |
|---|---|---|
| `market_key=ML` | → `predicted_probability = home_win_prob` | ✅ Feasible |
| `market_key=ML` | → `predicted_probability = away_win_prob` (away selection) | ✅ Feasible |
| `market_key=OU` | → `predicted_probability = P(total > line)` derived from `expected_home_runs + expected_away_runs` | ⚠️ Needs `ou_line` reference |
| `market_key=RL` | → `predicted_probability = P(home wins by >1.5)` | ⚠️ Needs run-differential distribution |
| `odds_snapshot_ref` | → `data/derived/odds_snapshots_YYYY-MM-DD.jsonl` filename + row index | ✅ Feasible at generation time |

### Fields That Cannot Be Derived (Must Be Added at Source)

| Field | Reason Cannot Be Derived | Action Required |
|---|---|---|
| `model_version` | Not stored in any file; no version constant in codebase | Add `MODEL_VERSION = "v1.0.0"` constant to model module |
| `feature_version` | Feature pipeline has no version tag | Add `FEATURE_VERSION = "v1.0.0"` constant to feature module |
| `leakage_guard_version` | Leakage guard has no version tag | Add `LEAKAGE_GUARD_VERSION = "v1.0.0"` constant |
| `canonical_match_id` for MLB | MLB ID format must match bridge format exactly | Adapter must generate matching `game_id` strings |

---

## 5. Extended MLB/KBO/NPB Registry Schema

### Design Principle

The new registry is a **per-market, per-selection** record. Each game with 3 markets (ML home, ML away, OU over, OU under, RL home, RL away) produces **6 rows** per game. This is additive — the WBC registry is unchanged.

### Target File Path

```
data/derived/future_model_predictions_YYYY-MM-DD.jsonl
```

Where `YYYY-MM-DD` is the date the predictions were generated (never the game date — the generation date must be ≤ game start).

### Schema Definition (28 Required Fields)

```jsonl
{
  // ── Identity ─────────────────────────────────────────────────────────────
  "canonical_match_id":     "MLB-2026_04_30-07_10_PM-NEW_YORK_YANKEES-AT-BOSTON_RED_SOX",
  "market_key":             "ML",
  "selection_key":          "home",
  "league":                 "MLB",
  "game_date_local":        "2026-04-30",
  "game_time_utc":          "2026-04-30T23:10:00+00:00",

  // ── Prediction Content ────────────────────────────────────────────────────
  "predicted_probability":  0.523,
  "predicted_probability_calibrated": 0.511,
  "calibration_method":     "isotonic",
  "home_win_prob_raw":      0.523,
  "away_win_prob_raw":      0.477,
  "expected_runs_home":     4.62,
  "expected_runs_away":     4.15,
  "ou_line_ref":            8.5,
  "confidence_score":       0.821,

  // ── CLV Contract Fields (Phase 6A Required) ───────────────────────────────
  "prediction_time_utc":    "2026-04-30T18:45:00+00:00",
  "pre_game_verified":      true,
  "model_version":          "v1.0.0",
  "feature_version":        "v1.0.0",
  "leakage_guard_version":  "v1.0.0",
  "odds_snapshot_ref":      "data/derived/odds_snapshots_2026-04-30.jsonl:42",

  // ── Regime / Model Diagnostics ────────────────────────────────────────────
  "regime":                 "regular_season",
  "ev_threshold_applied":   0.07,
  "edge_score":             0.0,
  "edge_valid":             false,
  "edge_tier":              "NO_BET",

  // ── Decision ─────────────────────────────────────────────────────────────
  "decision":               "NO_BET",
  "kelly_fraction":         0.0,
  "kelly_stake_pct":        0.0,

  // ── Provenance ────────────────────────────────────────────────────────────
  "recorded_at_utc":        "2026-04-30T18:45:03.221443+00:00",
  "generator":              "phase6i_prediction_registry_adapter_v1"
}
```

### Example Record — ML Home Selection

```json
{
  "canonical_match_id":               "MLB-2026_04_30-07_10_PM-NEW_YORK_YANKEES-AT-BOSTON_RED_SOX",
  "market_key":                        "ML",
  "selection_key":                     "home",
  "league":                            "MLB",
  "game_date_local":                   "2026-04-30",
  "game_time_utc":                     "2026-04-30T23:10:00+00:00",
  "predicted_probability":             0.523,
  "predicted_probability_calibrated":  0.511,
  "calibration_method":                "isotonic",
  "home_win_prob_raw":                 0.523,
  "away_win_prob_raw":                 0.477,
  "expected_runs_home":                4.62,
  "expected_runs_away":                4.15,
  "ou_line_ref":                       8.5,
  "confidence_score":                  0.821,
  "prediction_time_utc":               "2026-04-30T18:45:00+00:00",
  "pre_game_verified":                 true,
  "model_version":                     "v1.0.0",
  "feature_version":                   "v1.0.0",
  "leakage_guard_version":             "v1.0.0",
  "odds_snapshot_ref":                 "data/derived/odds_snapshots_2026-04-30.jsonl:42",
  "regime":                            "regular_season",
  "ev_threshold_applied":              0.07,
  "edge_score":                        0.0,
  "edge_valid":                        false,
  "edge_tier":                         "NO_BET",
  "decision":                          "NO_BET",
  "kelly_fraction":                    0.0,
  "kelly_stake_pct":                   0.0,
  "recorded_at_utc":                   "2026-04-30T18:45:03.221443+00:00",
  "generator":                         "phase6i_prediction_registry_adapter_v1"
}
```

### Per-Game Row Explosion

For each game with full coverage, **6 rows** are emitted:

| Row | `market_key` | `selection_key` | `predicted_probability` Source |
|---|---|---|---|
| 1 | `ML` | `home` | `home_win_prob` |
| 2 | `ML` | `away` | `away_win_prob` |
| 3 | `RL` | `home` | `P(home wins by >1.5)` — run-diff distribution |
| 4 | `RL` | `away` | `P(away wins by >1.5)` — run-diff distribution |
| 5 | `OU` | `over` | `P(total > ou_line_ref)` — Poisson CDF |
| 6 | `OU` | `under` | `1 - P(total > ou_line_ref)` — Poisson CDF |

> **Note**: RL and OU derivation requires `ou_line_ref` from the opening odds snapshot. If the line is unavailable, RL and OU rows must be emitted with `predicted_probability = null` and `edge_valid = false`.

---

## 6. Prediction Timing / Leakage Rules

### Rule Summary

| Rule | ID | Requirement |
|---|---|---|
| **Pre-game gate** | T1 | `prediction_time_utc` < `game_time_utc` — strictly enforced |
| **Minimum advance** | T2 | `prediction_time_utc` ≤ `game_time_utc` − 30 minutes |
| **No intra-game data** | T3 | Feature extraction uses only data available at `prediction_time_utc`; live score, live lineup changes, injury reports published after prediction time are excluded |
| **Snapshot alignment** | T4 | `odds_snapshot_ref` must point to an odds record with `timestamp_utc` < `prediction_time_utc`; opening odds may be used |
| **Verified flag** | T5 | `pre_game_verified = true` only when T1 + T2 + T3 + T4 all pass |
| **Registry rejection** | T6 | Any row with `pre_game_verified = false` is written to `data/derived/rejected_predictions_YYYY-MM-DD.jsonl` and excluded from CLV calculations |

### Timing Architecture

```
  [Odds Snapshot arrives]           t=0  (opening odds, e.g. 24h before game)
       ↓
  [Feature extraction]              t=0 to t=T-60min
       ↓
  [Model inference]                 t ≤ T-30min
  prediction_time_utc recorded      ← this is the CLV anchor
       ↓
  [Registry write]                  t ≤ T-30min
  recorded_at_utc ≥ prediction_time_utc (write latency OK)
       ↓
  [Closing odds snapshot]           t=T (game start)
       ↓
  [CLV calculation]                 t > T
  CLV = closing_implied_prob - predicted_probability
```

### Leakage Guard Responsibilities

The `leakage_guard_version` field tags which version of the leakage guard validated the prediction. The guard must verify:

1. No closing odds used as input features
2. No actual game result in feature set
3. No same-day lineup data unless published before `prediction_time_utc`
4. No pitcher injury reports from within 30 minutes of game start (if received after prediction)

---

## 7. Market Coverage Rules

### Allowed Markets (from Phase 6E Domain Commitment)

| Market | `market_key` | Allowed | Requirement |
|---|---|---|---|
| Moneyline (Win/Loss) | `ML` | ✅ Required | Every game must have ML home + away rows |
| Run Line (Spread) | `RL` | ✅ Allowed | Emit only if opening RL odds available in snapshot |
| Over/Under (Totals) | `OU` | ✅ Allowed | Emit only if `ou_line_ref` available from opening snapshot |
| First 5 Innings (F5) | `F5` | ⛔ Excluded (Phase 6H) | Model not trained on F5 separation |
| Team Totals | `TT` | ⛔ Excluded | Team total model not validated |
| Props (strikeout, HR) | various | ⛔ Excluded | Out of scope for Phase 6 |

### Minimum Coverage Requirement

Each daily predictions file must contain at least:
- ML rows for **all captured games** in the manifest
- Coverage must be ≥ the games count in `data/derived/future_event_capture_manifest_YYYY-MM-DD.json`

### Market Regime Context

The `regime` field records the statistical regime at prediction time:

| `regime` Value | Description | Source |
|---|---|---|
| `regular_season` | Standard MLB/KBO/NPB regular season game | `mlb_decision_quality_report.regime` |
| `small_edge` | Low-confidence edge zone (edge < EV_MEDIUM) | Derived from edge calculation |
| `strong_edge` | High-confidence edge zone (edge ≥ EV_STRONG) | Derived from edge calculation |
| `no_edge` | Below EV_PASS threshold | Derived from edge calculation |

---

## 8. Model Compatibility Requirements

### MODEL_CAPABILITY_GAP Analysis

The following gaps exist between the current model output and the requirements of the new registry schema. Each gap must be resolved in Phase 6I before predictions can be written to `future_model_predictions_YYYY-MM-DD.jsonl`.

| Gap ID | Field | Current State | Required State | Priority |
|---|---|---|---|---|
| MCG-01 | `canonical_match_id` | WBC `game_id` (e.g. `"A05"`) only | MLB format: `"MLB-YYYY_MM_DD-HH_MM_[AP]M-HOME-AT-AWAY"` | **P0 — Blocks all CLV** |
| MCG-02 | `model_version` | Not stored anywhere in pipeline | Explicit semver string emitted per prediction | **P0 — Blocks audit** |
| MCG-03 | `feature_version` | Not stored anywhere | Explicit semver string from feature module | **P0 — Blocks audit** |
| MCG-04 | `leakage_guard_version` | Not stored anywhere | Explicit semver string from guard module | **P0 — Blocks audit** |
| MCG-05 | `market_key` per row | Game-level only (implicit in `home_win_prob`) | One row per (game × market × selection) | **P1 — Blocks market CLV** |
| MCG-06 | `selection_key` per row | No selection tracking | `home`/`away`/`over`/`under` explicit | **P1 — Blocks selection CLV** |
| MCG-07 | `odds_snapshot_ref` | No odds reference in current registry | Reference to specific snapshot row | **P1 — Needed for CLV join** |
| MCG-08 | `prediction_time_utc` | `recorded_at_utc` is proxy only | Explicit timestamp with `pre_game_verified` flag | **P1 — Required by Phase 6A** |
| MCG-09 | `ou_line_ref` | No OU line stored | Opening OU line from odds snapshot | **P2 — Needed for OU rows** |
| MCG-10 | RL probability derivation | `home_win_prob` only | `P(home wins by >1.5)` from run-diff distribution | **P2 — Needed for RL rows** |

### Version Constant Design

Phase 6I must add the following constants to the model/feature/guard modules:

```python
# In wbc_backend/models/stack_model.py (or equivalent MLB model)
MODEL_VERSION = "v1.0.0"

# In wbc_backend/features/feature_pipeline.py (or equivalent)
FEATURE_VERSION = "v1.0.0"

# In wbc_backend/validation/leakage_guard.py (or equivalent)
LEAKAGE_GUARD_VERSION = "v1.0.0"
```

Version increment policy:
- Bump **patch** (`v1.0.x`) for threshold or hyperparameter changes
- Bump **minor** (`v1.x.0`) for new feature additions or feature removals
- Bump **major** (`vx.0.0`) for model architecture changes (e.g. new stacking layer)

### WBC vs MLB Sub-model Architecture

The existing registry shows 6 sub-models:

| Sub-model | `home_win_prob` (WBC A05) | Notes |
|---|---|---|
| `elo` | 0.50 | Baseline parity |
| `poisson` | 0.50 | Run-scoring model |
| `bayesian` | 0.50 | Prior-based |
| `baseline` | 0.50 | Naive base |
| `real_gbm_stack` | **0.99** | CatBoost + LightGBM + XGBoost stack |
| `neural_net` | 0.48 | NN model |

> **Note**: The `real_gbm_stack` producing 0.99 for a WBC pool game is a calibration red flag — this extreme output suggests the WBC model is not calibrated for regular-season MLB play. Phase 6I must apply Platt/isotonic recalibration to GBM outputs before writing MLB predictions.

The `walkforward_summary.json` confirms calibration: `brier = 0.248`, `ml_roi = -0.011` on 2,188 games. The model is near-calibrated on historical data but the stack's extreme outputs on novel (WBC) inputs confirm the need for calibration enforcement at the per-market row level.

---

## 9. Backward Compatibility Plan

### Isolation Strategy

The new registry is written to a **separate path** and does not touch the existing WBC registry:

| Scope | Path | Action |
|---|---|---|
| WBC Registry | `data/wbc_backend/reports/prediction_registry.jsonl` | **READ-ONLY — Not modified** |
| WBC Replay | `data/wbc_backend/reports/prediction_registry_replay.jsonl` | **READ-ONLY — Not modified** |
| New MLB/KBO/NPB Registry | `data/derived/future_model_predictions_YYYY-MM-DD.jsonl` | **New file — additive only** |
| Rejected predictions | `data/derived/rejected_predictions_YYYY-MM-DD.jsonl` | **New file — failure tracking** |

### No Schema Backfill

The 66 WBC rows are **not** to be backfilled with new CLV fields. The WBC games (A05–D06) played on 2026-03-08/09 occurred before the odds capture window (first MLB odds: 2026-03-13). There is no CLV to calculate for those WBC rows, and retroactive schema modification would corrupt the research audit trail.

### Consumer Compatibility

Any downstream consumer reading `prediction_registry.jsonl` will continue to find the WBC schema unchanged. New consumers reading `future_model_predictions_YYYY-MM-DD.jsonl` will use the extended schema. No existing tests are broken.

---

## 10. Registry Quality Gates

The following gates (P1–P10) must pass before any `future_model_predictions_YYYY-MM-DD.jsonl` file is accepted as valid for CLV matching.

| Gate ID | Gate Name | Check | Fail Action |
|---|---|---|---|
| **P1** | `P1_CANONICAL_MATCH_ID_PRESENT` | All rows have non-null `canonical_match_id` matching `r"^[A-Z]{2,5}-\d{4}_\d{2}_\d{2}-"` | Reject file |
| **P2** | `P2_MARKET_KEY_VALID` | All rows have `market_key` in `{"ML","RL","OU"}` | Reject row |
| **P3** | `P3_SELECTION_KEY_VALID` | All rows have `selection_key` in `{"home","away","over","under"}` | Reject row |
| **P4** | `P4_PREDICTION_TIME_PRE_GAME` | All rows: `prediction_time_utc` < `game_time_utc` | Reject row; write to `rejected_predictions` |
| **P5** | `P5_MIN_ADVANCE_30MIN` | All rows: `game_time_utc` − `prediction_time_utc` ≥ 30 minutes | Reject row; write to `rejected_predictions` |
| **P6** | `P6_MODEL_VERSION_PRESENT` | All rows have non-null `model_version` matching `r"^v\d+\.\d+\.\d+$"` | Reject file |
| **P7** | `P7_FEATURE_VERSION_PRESENT` | All rows have non-null `feature_version` matching `r"^v\d+\.\d+\.\d+$"` | Reject file |
| **P8** | `P8_LEAKAGE_GUARD_VERSION_PRESENT` | All rows have non-null `leakage_guard_version` matching `r"^v\d+\.\d+\.\d+$"` | Reject file |
| **P9** | `P9_PROBABILITY_IN_RANGE` | All rows: `0.0 < predicted_probability < 1.0` | Reject row |
| **P10** | `P10_DECISION_CANDIDATE_PRESENT` | At least one row per game has `decision != "NO_BET"` OR all rows legitimately below threshold (acceptable) | Warning only |

### Gate Execution Order

P1 → P6 → P7 → P8 (file-level) → P2 → P3 → P4 → P5 → P9 (row-level) → P10 (file-level summary)

File-level gates that fail cause the entire file to be rejected. Row-level gates cause individual rows to be moved to `rejected_predictions`. The CLV bridge join may proceed with the remaining rows.

---

## 11. Implementation Roadmap

### Phase 6I: Model Adapter Layer (Next Phase)

**Goal**: Create a thin adapter that reads existing model outputs and writes `future_model_predictions_YYYY-MM-DD.jsonl` with all 28 schema fields.

**Deliverables**:
1. Version constants in model/feature/leakage-guard modules (`MODEL_VERSION`, `FEATURE_VERSION`, `LEAKAGE_GUARD_VERSION = "v1.0.0"`)
2. `canonical_match_id` generation utility: converts model's game representation to bridge-compatible format
3. Per-market row expansion: given a game-level prediction, emit 2 ML rows + 2 OU rows (RL optional)
4. Prediction registry writer: `data/derived/future_model_predictions_YYYY-MM-DD.jsonl`
5. Quality gate checker (`P1_CANONICAL_MATCH_ID_PRESENT` through `P10_DECISION_CANDIDATE_PRESENT`)
6. `phase6i_prediction_registry_adapter_report_YYYY-MM-DD.md`: validation report

**Input Dependency**: Requires `data/derived/future_event_capture_manifest_YYYY-MM-DD.json` (Phase 6F output) and `data/derived/odds_snapshots_YYYY-MM-DD.jsonl` (Phase 6B output).

### Phase 6J: CLV Bridge Connection

**Goal**: Connect `future_model_predictions_YYYY-MM-DD.jsonl` to `match_identity_bridge_YYYY-MM-DD.jsonl` and execute the first non-zero CLV computation.

**Deliverables**:
1. Bridge join: `canonical_match_id` → opening odds → closing odds
2. First CLV record: `clv_proxy = closing_implied_prob - predicted_probability`
3. Confirm `bridge_ready_records > 0` (resolving Phase 6G's `NOT_READY_DOMAIN_MISMATCH`)
4. `phase6j_clv_bridge_connection_report_YYYY-MM-DD.md`

### Phase 6K: Statistical CLV Validation

**Goal**: Accumulate ≥ 200 CLV observations and test `CLV_proxy > 0.03` hypothesis.

**Deliverables**:
1. Rolling CLV tracker with regime breakdowns
2. Per-market CLV distribution (ML vs RL vs OU)
3. Bootstrap confidence intervals
4. Go/No-Go decision for Phase 6L (live sizing)

### Phase 6L: Live Registry Activation

**Goal**: Activate live registry writes (not paper-only).

**Gate**: Phase 6K must confirm CLV hypothesis with `p < 0.05` confidence.

**Deliverables**:
1. Live prediction registry pipeline (automated daily writes)
2. Monitoring and alerting
3. Drawdown circuit breaker integration (`DRAWDOWN_MAX = 0.20`)

### Milestone Summary

| Phase | Output | Unblocks |
|---|---|---|
| **6H** (this) | Design document | Phase 6I spec |
| **6I** | Model adapter + version constants + quality gates | `bridge_ready > 0` |
| **6J** | First CLV computation | Statistical validation |
| **6K** | ≥200 CLV observations + hypothesis test | Live activation |
| **6L** | Live registry activation | CLV measurement in production |

---

## 12. Next Prompt — Phase 6I Ready-to-Copy

```
Phase 6I: Prediction Registry Adapter Layer

## Context
Phase 6H (docs/orchestration/phase6h_prediction_registry_extension_design_2026-04-29.md) has defined the schema for `data/derived/future_model_predictions_YYYY-MM-DD.jsonl`.

Domain: DOMAIN_COMMITMENT_MLB_KBO_NPB
Settings: EV_STRONG=0.07, EV_MEDIUM=0.03, KELLY_FRACTION=0.15, DRAWDOWN_MAX=0.20

## Required Input Files
1. `data/derived/future_event_capture_manifest_YYYY-MM-DD.json` (Phase 6F)
2. `data/derived/odds_snapshots_YYYY-MM-DD.jsonl` (Phase 6B)
3. `data/wbc_backend/model_artifacts.json` (calibration params)
4. `data/wbc_backend/walkforward_summary.json` (model ROI baseline)
5. `config/settings.py` (EV thresholds, Kelly fraction)
6. `docs/orchestration/phase6h_prediction_registry_extension_design_2026-04-29.md` (schema)

## Task
Create: `scripts/run_prediction_registry_adapter.py`

The script must:
1. Add version constants:
   - MODEL_VERSION = "v1.0.0"
   - FEATURE_VERSION = "v1.0.0"
   - LEAKAGE_GUARD_VERSION = "v1.0.0"

2. Load game list from `future_event_capture_manifest_YYYY-MM-DD.json`

3. For each game, derive predictions using the existing model pipeline (read-only):
   - `home_win_prob`, `away_win_prob` from GBM stack + isotonic calibration
   - `expected_runs_home`, `expected_runs_away` from Poisson model
   - `ou_line_ref` from opening odds snapshot

4. Emit 6 rows per game (ML home, ML away, RL home, RL away, OU over, OU under) with all 28 schema fields from Phase 6H §5

5. Apply prediction timing rule: `prediction_time_utc` = now() only if now() < game_time_utc − 30min; otherwise skip game

6. Run quality gates P1–P10 from Phase 6H §10

7. Write:
   - Valid rows → `data/derived/future_model_predictions_YYYY-MM-DD.jsonl`
   - Rejected rows → `data/derived/rejected_predictions_YYYY-MM-DD.jsonl`

8. Produce: `docs/orchestration/phase6i_prediction_registry_adapter_report_YYYY-MM-DD.md`

## Quality Gate Requirements
- P1 `canonical_match_id` present and format-valid: 100% pass rate required
- P6/P7/P8 version fields: 100% pass rate required
- P4/P5 pre-game timing: any failure → row rejected, not file rejected

## Scope Constraints
- Do NOT modify `data/wbc_backend/reports/prediction_registry.jsonl`
- Do NOT call external APIs
- Do NOT run CLV calculation (Phase 6J scope)
- Do NOT commit (documentation review required first)

## Success Criteria
1. `data/derived/future_model_predictions_YYYY-MM-DD.jsonl` exists with ≥1 row
2. All P1–P9 gates pass on emitted rows
3. `canonical_match_id` format matches `match_identity_bridge_YYYY-MM-DD.jsonl`
4. `model_version`, `feature_version`, `leakage_guard_version` present on all rows
5. `pre_game_verified = true` on all non-rejected rows

Emit token `PHASE_6I_ADAPTER_VERIFIED` in report when all criteria met.
```

---

## 13. Scope Confirmation

This document is **documentation only**. The following actions were **not** taken during Phase 6H:

| Action | Status |
|---|---|
| Modify `prediction_registry.jsonl` | ❌ NOT done |
| Modify model code | ❌ NOT done |
| Generate new predictions | ❌ NOT done |
| Modify crawler, DB, or existing data files | ❌ NOT done |
| Call external APIs | ❌ NOT done |
| Create orchestrator tasks | ❌ NOT done |
| Run CLV validation | ❌ NOT done |
| Commit to git | ❌ NOT done |

### Evidence-to-Design Chain

| Evidence | Design Conclusion |
|---|---|
| 66 WBC rows, 0/7 CLV fields | New file required; WBC registry untouched |
| `prediction.home_win_prob` game-level only | Per-market row explosion required (6 rows/game) |
| No `model_version` anywhere in pipeline | Version constants must be added at source |
| `top_bets = []` in all 66 rows | Active bet tracking not implemented; new schema designs it explicitly |
| WBC `game_id = "A05"` format | MLB IDs must use bridge-compatible format; adapter layer required |
| 4,356 opening+closing pairs available (Phase 6G) | Prediction coverage is the missing link; this design unblocks it |
| `bridge_ready = 0` (Phase 6G) | Resolved by Phase 6I writing `canonical_match_id`-compatible rows |
| `mlb_decision_quality_report` `clv_available = False` | Confirms no CLV possible without closing odds; Phase 6J will add them |
| `walkforward_summary`: `brier=0.248`, `ml_roi=-0.011` (2,188 games) | Model near-calibrated on historical data; isotonic calibration must be applied to new predictions |
| `real_gbm_stack` outputs 0.99 on WBC inputs | Recalibration mandatory before MLB predictions |

**Phase 6H DESIGN_COMPLETE.**
