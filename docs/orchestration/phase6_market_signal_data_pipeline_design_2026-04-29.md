# Phase 6 — Market Signal CLV Validation Data Pipeline Design

**Date:** 2026-04-29
**Author:** Betting-pool Orchestrator Research Agent
**Triggered by:** Phase 5.5 validation decision = `NEEDS_DATA_PIPELINE`
**Source task:** #6168 (`validation_market_signal`)
**Source report:** `research/market_signal_validation_20260429.md`

---

## Background

Phase 5.5 executed a validation of the market signal CLV hypothesis from source task #6161
(`lane: market_signal`, decision: `WORTH_VALIDATION`).

The hypothesis:

> *Bets placed where CLV_proxy > 0.03 will outperform the benchmark model's overall ROI
> by at least 3 percentage points over a sample of ≥200 bets per market regime.*

The validation was blocked by two data-pipeline gaps:

1. **No persisted benchmark model predictions** — `prediction_registry.jsonl` exists (66 rows, WBC 2026 only)
   but predictions use `game_id` keys (e.g. `A05`, `D06`) that do not match the
   `match_id` keys in `tsl_odds_history.jsonl` (e.g. `3452364.1`). Overlap = **0 rows**.

2. **Insufficient CLV_high sample** — even with market-movement proxy, CLV_high bucket
   has only 38 matches (all 2026), far below the ≥200 required.

This document provides the Betting-pool-native design for a data pipeline that will
unblock the validation.

---

## 1. Current Data Inventory

| Data Source | Exists? | Key Fields | Row Count | Current Use | Gap |
|---|---|---|---|---|---|
| `data/tsl_odds_history.jsonl` | ✅ | `match_id`, `fetched_at`, `game_time`, `markets[{marketCode, outcomes}]` | 1,205 rows / 411 unique matches | Odds history, market movement | No `snapshot_type`; no `implied_probability`; no `settlement_result`; `match_id` format differs from `game_id` in prediction registry |
| `data/wbc_2026_authoritative_snapshot.json` | ✅ | `games`, `version`, `generated_at` | 40 games (WBC 2026) | WBC game schedule reference | Coverage limited to WBC 2026 only; no CPBL/MLB leagues |
| `data/wbc_backend/reports/prediction_registry.jsonl` | ✅ | `game_id`, `recorded_at_utc`, `prediction.home_win_prob`, `decision_report.decision`, `decision_report.expected_clv` | 66 rows (WBC 2026) | Pre-game model decisions | `game_id` ≠ TSL `match_id`; no feature version; no `prediction_time_utc` vs odds timestamp alignment |
| `data/wbc_backend/reports/postgame_results.jsonl` | ✅ | `game_id`, `actual_result.{home_score, away_score, home_win}`, `prediction_summary.decision` | 49 rows (WBC 2026) | Post-game model evaluation, learning | No odds snapshot linked; `game_id` format overlaps prediction_registry for 2/9 WBC games; no ROI per bet |
| `data/wbc_backend/walkforward_summary.json` | ✅ | `games=2188`, `ml_roi`, `ml_hit_rate`, `brier`, `logloss` | Aggregate only (2188 games) | Deployment gate check | Aggregate only; no per-match probability export; walk-forward used MLB 2024 data but that data is not in repo |
| `data/wbc_backend/market_validation.json` | ✅ | `ML.{ml_bets, ml_roi, ml_hit_rate}`, `RL.{rl_bets, rl_roi}`, `OU.{ou_bets, ou_roi}` | Aggregate only | Model strategy validation summary | Aggregate only; no per-market CLV breakdown; no regime segmentation of ROI |
| `data/wbc_backend/calibration_compare.json` | ✅ | `platt.{...}`, `isotonic.{...}` | Aggregate summary | Calibration selection at deployment | No per-match calibration error; not linked to individual predictions |
| `data/wbc_backend/model_artifacts.json` | ✅ | `calibration`, `params`, `odds_band_stats` | Aggregate | Model artifact registry | No prediction probability per match_id persisted |
| `data/wbc_backend/portfolio_risk.json` | ✅ | `bankroll`, `total_exposure`, `daily_pnl`, `current_drawdown`, `is_circuit_breaker_active` | Live state only | Real-time risk control | No historical bankroll timeseries; no per-bet ROI record |
| `data/wbc_backend/reports/prediction_registry_replay.jsonl` | ✅ | Same schema as prediction_registry | Unknown rows | Replay / simulation | Not inspected for row count; same `game_id` mismatch issue expected |
| `data/wbc_backend/reports/mlb_calibration_baseline_snapshot_2026-04-25.json` | ✅ | Calibration snapshot | Aggregate | Calibration baseline | No per-match probability export |
| Settlement / realized ROI file | ❌ MISSING | `match_id`, `market_type`, `bet_selection`, `stake`, `realized_roi`, `settled_at_utc` | — | — | Not produced by current pipeline |
| Opening odds per match | ❌ MISSING (inferred only) | `match_id`, `market_type`, `opening_decimal_odds`, `snapshot_type=OPENING` | — | — | TSL crawler does not tag `snapshot_type`; earliest snapshot used as proxy but not guaranteed pre-match |
| Match-to-prediction join key | ❌ MISSING | Bidirectional mapping `tsl_match_id ↔ game_id` | — | — | WBC `game_id` (pool-code `A05`) and TSL `match_id` (numeric `3452364.1`) are different identifier systems; no join table exists |
| Historical CPBL/MLB odds (2024–2025) | ❌ MISSING | Same as tsl_odds_history schema | — | — | Walk-forward used 2,188 MLB games internally during training but these odds are not in repo |

---

## 2. CLV Validation Data Contract

This section defines the **minimum data contract** required to validate the market signal
CLV hypothesis. All fields must exist in a joinable form before running the validation script.

### 2.1 Match / Market Identity

```jsonc
{
  "match_id":          "string  — canonical match identifier, consistent across all tables",
  "league":            "string  — e.g. WBC, CPBL, NPB, MLB",
  "sport":             "string  — e.g. baseball",
  "match_time_utc":    "ISO8601 — scheduled first pitch in UTC",
  "market_type":       "string  — MNL | HDC | OU | OE | TTO",
  "selection":         "string  — home | away | over | under | odd | even",
  "bookmaker":         "string  — e.g. TSL_BLOB3RD"
}
```

### 2.2 Odds Snapshots

```jsonc
{
  "snapshot_id":             "string  — UUID per snapshot row",
  "match_id":                "string  — FK to match identity",
  "snapshot_type":           "enum    — OPENING | CLOSING | INTERMEDIATE",
  "snapshot_time_utc":       "ISO8601 — when snapshot was fetched",
  "decimal_odds":            "float   — e.g. 1.72",
  "implied_probability":     "float   — 1 / decimal_odds",
  "market_type":             "string  — MNL | HDC | OU ...",
  "selection":               "string  — home | away | over | under"
}
```

**snapshot_type rules:**
- `OPENING` = first snapshot fetched for this `match_id × market_type × selection` pair
- `CLOSING` = snapshot fetched within 30 minutes before `match_time_utc` (configurable)
- `INTERMEDIATE` = any snapshot between OPENING and CLOSING

Leakage guard: `snapshot_time_utc < match_time_utc` must hold for all OPENING and CLOSING tags.

### 2.3 Model Prediction

```jsonc
{
  "prediction_id":          "string  — UUID per prediction",
  "match_id":               "string  — FK, must use same canonical match_id as odds tables",
  "model_version":          "string  — e.g. gbm_stack_v2.1",
  "prediction_time_utc":    "ISO8601 — when model ran inference",
  "predicted_probability":  "float   — home win probability (for MNL market)",
  "confidence":             "float   — model confidence score (existing: confidence_index)",
  "feature_version":        "string  — feature set version used",
  "market_type":            "string  — which market this prediction applies to",
  "selection":              "string  — home | away | over | under"
}
```

**Critical:** `prediction_time_utc` must be before the CLOSING snapshot time. If not,
the prediction cannot be used for CLV computation (forward leakage).

### 2.4 Betting Decision

```jsonc
{
  "decision_id":       "string  — UUID per decision",
  "match_id":          "string  — FK",
  "prediction_id":     "string  — FK to prediction",
  "bet_decision":      "enum    — BET | NO_BET",
  "stake_fraction":    "float   — fraction of bankroll Kelly-adjusted",
  "expected_value":    "float   — model_prob * decimal_odds - 1",
  "risk_cap_reason":   "string  — why stake was capped (or null)",
  "no_bet_reason":     "string  — why no bet was placed (or null)"
}
```

### 2.5 Settlement

```jsonc
{
  "settlement_id":     "string  — UUID per settled bet",
  "match_id":          "string  — FK",
  "decision_id":       "string  — FK",
  "result":            "string  — home_win | away_win | over | under | odd | even",
  "settled_at_utc":    "ISO8601 — when result was confirmed",
  "stake":             "float   — absolute stake",
  "payout":            "float   — payout received (0 if loss)",
  "realized_roi":      "float   — (payout - stake) / stake",
  "closing_line_value":"float   — CLV_proxy = model_prob - implied_probability_close",
  "hit":               "bool    — did the bet win?"
}
```

---

## 3. Current Gap Against Contract

| Required Field | Current Source | Available? | Quality | Needed Fix |
|---|---|---|---|---|
| `match_id` (canonical) | TSL: `match_id` (numeric e.g. `3452364.1`); Prediction: `game_id` (WBC code e.g. `A05`) | PARTIAL | AMBIGUOUS | Create bidirectional `match_id ↔ game_id` join table; choose one canonical format |
| `league` | TSL: derivable from team names (KBO/NPB teams present); Prediction: `prediction.diagnostics.regime` = `"pool"` | PARTIAL | PARTIAL | Add `league` field to crawler output and prediction records |
| `match_time_utc` | TSL: `game_time` (local TZ `+08:00`); Prediction: `recorded_at_utc` (not game time) | PARTIAL | AMBIGUOUS | Normalize `game_time` to UTC in crawler; add `match_time_utc` to prediction record |
| `market_type` | TSL: `markets[].marketCode` (MNL, HDC, OU, OE, TTO) | ✅ | READY | — |
| `selection` | TSL: `markets[].outcomes[].outcomeName` (team names, not home/away) | PARTIAL | PARTIAL | Normalize to `home | away | over | under | odd | even` |
| `snapshot_type` | Not present in any TSL record | ❌ | MISSING | Add `snapshot_type` logic to `data/tsl_crawler_v2.py` |
| `snapshot_time_utc` | TSL: `fetched_at` (UTC, present) | ✅ | READY | Rename to `snapshot_time_utc` in contract layer |
| `decimal_odds` | TSL: `markets[].outcomes[].odds` (string) | ✅ | PARTIAL | Cast to float at ingest |
| `implied_probability` | Not stored; must be computed | ❌ | MISSING | Compute at ingest: `1 / decimal_odds` |
| `model_version` | Not stored in prediction_registry | ❌ | MISSING | Add `model_version` field to prediction exporter |
| `prediction_time_utc` | `prediction_registry.recorded_at_utc` ≈ prediction time | PARTIAL | PARTIAL | Confirm `recorded_at_utc` is before match start, not after |
| `predicted_probability` | `prediction.home_win_prob` (exists in registry) | ✅ | PARTIAL | Match to TSL `match_id` (currently 0 overlap) |
| `confidence` | `prediction.confidence_score` (exists) | ✅ | PARTIAL | Same join issue |
| `feature_version` | Not stored | ❌ | MISSING | Add to prediction exporter |
| `match_id × prediction join` | **Zero overlap** between TSL `match_id` and prediction `game_id` | ❌ | MISSING | Core blocker — requires ID mapping table |
| `bet_decision` | `decision_report.decision` (NO_BET / BET) | ✅ | PARTIAL | All 66 predictions = NO_BET; no actual BET records exist |
| `stake_fraction` | Not stored for actual bets | ❌ | MISSING | Log Kelly stake at decision time |
| `expected_value` | `decision_report.expected_clv` (all = 0.0 in current records) | PARTIAL | LEAKAGE_RISK | `expected_clv = 0.0` for all records suggests pipeline not writing real EV |
| `result` | `postgame_results.actual_result.home_win` | ✅ | PARTIAL | No odds snapshot linked; game_id overlap = 2/9 for prediction×postgame |
| `settled_at_utc` | `postgame_results.recorded_at_utc` | ✅ | PARTIAL | Only 49 WBC games; no CPBL/MLB |
| `realized_roi` | Not computed; no bets placed | ❌ | MISSING | Requires bet + settlement linkage |
| `closing_line_value` | Not stored; `decision_report.trailing_clv` exists but = 0.0 | PARTIAL | LEAKAGE_RISK | `trailing_clv = 0.0` for all records; formula not yet operational |
| `hit` | Derivable from `actual_result` + `selection` | PARTIAL | PARTIAL | Requires selection normalization |
| Historical CPBL/MLB odds 2024–2025 | Not in repo | ❌ | MISSING | Backfill pipeline required for ≥200 sample |

**Summary of critical gaps:**

1. **`match_id` join key** — TSL numeric IDs and WBC pool-code game_ids are entirely different systems with 0 overlap.
2. **`snapshot_type`** — missing from all 1,205 TSL records. Cannot distinguish opening from closing.
3. **`model_version`, `feature_version`** — not persisted, preventing auditability.
4. **`expected_clv` and `trailing_clv` = 0.0** — pipeline fields exist but are not populated (all decisions = NO_BET, `edge_tier = FORBIDDEN`).
5. **Settlement linkage** — `postgame_results` has no odds snapshot attached; ROI cannot be computed.
6. **Sample coverage** — only WBC 2026 (40–66 games). Walk-forward training used 2,188 games but those odds are not in repo.

---

## 4. Betting-pool Native CLV Formulas

All formulas below use Betting-pool terminology. No lottery-domain terms.

### 4.1 Core Definitions

```
implied_probability(decimal_odds) = 1 / decimal_odds

# Vig-adjusted (no-vig) implied probability for two-outcome market:
impl_home = 1 / odds_home
impl_away = 1 / odds_away
overround = impl_home + impl_away          # typically 1.02–1.06 for TSL
novig_home = impl_home / overround
novig_away = impl_away / overround
```

### 4.2 CLV Formulas

```
# Primary CLV (requires model prediction):
CLV_probability_delta = predicted_probability - implied_probability(closing_decimal_odds)

# Market movement delta (proxy, no model required):
market_movement_delta = implied_probability(closing_odds) - implied_probability(opening_odds)

# Edge at bet time (requires model and opening odds):
realized_edge = predicted_probability - implied_probability(opening_decimal_odds)

# ROI per settled bet:
ROI = (payout - stake) / stake
    = (decimal_odds * stake - stake) / stake   if win
    = -1.0                                      if loss

# Trailing CLV (requires closing odds after bet placement):
trailing_CLV = implied_probability(closing_odds) - implied_probability(odds_at_bet_time)
```

### 4.3 Validity Rules

| Formula | Valid When | Invalid When |
|---|---|---|
| `CLV_probability_delta` | `prediction_time_utc < snapshot_time_utc(CLOSING)` AND `prediction_time_utc < match_time_utc` | Model ran after closing line or after match start |
| `market_movement_delta` | `OPENING` and `CLOSING` snapshots both exist for same `match_id × market_type × selection` | Only one snapshot exists, or snapshots are post-match |
| `realized_edge` | `prediction_time_utc < match_time_utc` AND opening snapshot time confirmed pre-match | Snapshot `fetched_at` is post-match (leakage risk noted in Phase 5.5) |
| `ROI` | `settled_at_utc` exists AND `bet_decision = BET` | No bet was placed (`NO_BET`); formula undefined |
| `trailing_CLV` | Closing snapshot `snapshot_time_utc` is within 30 min before `match_time_utc` | Closing snapshot ambiguity — may be post-match for some TSL records |

### 4.4 Leakage Rules (Hard Guards)

1. `prediction_time_utc MUST BE BEFORE closing odds snapshot_time_utc`
   — if prediction is computed after closing line, the model had access to closing market information.

2. `prediction_time_utc MUST BE BEFORE match_time_utc`
   — no prediction from any model that ran after first pitch.

3. `closing_decimal_odds MUST NOT appear as a model feature` for the same prediction
   — closing odds cannot be an input feature and also the benchmark.

4. `actual_result (settlement) MUST ONLY be joined AFTER match_time_utc + settle_window`
   — settlement result cannot be accessed during feature extraction or prediction.

5. `no future market data in training features`
   — training fold for walk-forward split T must use only games before time T.

6. `OPENING snapshot must be fetched BEFORE first pitch`
   — tag `snapshot_type = OPENING` only when `snapshot_time_utc < match_time_utc`.

---

## 5. Sample Sufficiency Rules

### 5.1 Rationale

These thresholds are Betting-pool-native. They are based on:
- Standard power analysis for two-sample t-test (α=0.05, power=0.80)
- Conservative assumption of moderate effect size (Cohen's d ≈ 0.3–0.4 for ROI delta)
- Current available data (282 matches with ≥2 snapshots, 2026 only)

Do NOT use LotteryNew thresholds. Sports betting markets have different variance
and sample requirements.

### 5.2 Proposed Thresholds

| Validation Type | Minimum N | Notes |
|---|---|---|
| CLV bucket validation (CLV_high vs CLV_low ROI) | **≥ 200 per bucket** | Two-sample t-test; this is the Phase 5.5 target. CLV_high had only 38. |
| Market movement validation (opening→closing delta) | **≥ 150 matches** with 2+ snapshots | Current: 282 matches ✅ if snapshot_type is tagged |
| ROI validation per market (ML / RL / OU) | **≥ 300 settled bets per market type** | Based on walk-forward showing 1,544 ML bets over 2,188 games |
| Walk-forward split minimum (test fold) | **≥ 200 games per fold** | Walk-forward already uses 2,188 games; per-fold min is proportional |
| Per-regime sample (LIQUID_MARKET, etc.) | **≥ 100 per regime** | PROVISIONAL — regime definitions not yet validated for Betting-pool |
| Calibration stability window | **≥ 500 games** | Deployment gate already uses 500; preserve this threshold |

**All thresholds marked:** `PROVISIONAL_THRESHOLD_REQUIRES_RECALIBRATION`

Rationale: Until the first real CLV_high vs CLV_low ROI comparison is computed on actual
settled bets with proper opening/closing tagging, these thresholds should be treated as
provisional. Recalibrate after the first 500 bets with full settlement data.

---

## 6. Implementation Plan

### Phase 6A — Data Contract / Schema Spec

**Goal:** Define JSONL schemas as documentation. No runtime change.

**Files likely created:**
- `docs/orchestration/data_contract_clv_validation.md` (schema spec)
- `docs/orchestration/match_id_mapping_spec.md` (canonical ID design)

**Acceptance criteria:**
- Schema documents for all 5 contract sections (identity, odds snapshot, prediction, decision, settlement)
- Canonical `match_id` format chosen and documented
- `snapshot_type` enum documented with classification rules
- No runtime file modified

**Rollback:** Delete docs files; no code change to revert.

**Risk:** Low. Documentation only.

---

### Phase 6B — Crawler Snapshot Type Tagging

**Goal:** Add `snapshot_type = OPENING | CLOSING | INTERMEDIATE` logic to crawler output.

**Files likely changed:**
- `data/tsl_crawler_v2.py` — add `snapshot_type` classification based on `fetched_at` vs `game_time`
- `data/tsl_odds_history.jsonl` — new snapshots tagged; historical records NOT backfilled (append-only)
- `data/tsl_snapshot.py` — possibly updated if it processes snapshots

**Classification logic:**
```python
CLOSING_WINDOW_MINUTES = 30  # configurable
if snapshot_time < match_time - timedelta(hours=4):
    snapshot_type = "OPENING"
elif match_time - timedelta(minutes=CLOSING_WINDOW_MINUTES) <= snapshot_time < match_time:
    snapshot_type = "CLOSING"
elif snapshot_time >= match_time:
    snapshot_type = "POST_MATCH"  # exclude from CLV computation
else:
    snapshot_type = "INTERMEDIATE"
```

**Acceptance criteria:**
- All new TSL snapshots have `snapshot_type` field
- `snapshot_time_utc < match_time_utc` enforced for OPENING and CLOSING
- Historical JSONL records without `snapshot_type` handled gracefully (fallback = `INTERMEDIATE`)
- Existing crawler unit tests pass

**Rollback:** Revert `tsl_crawler_v2.py` change; new JSONL rows with `snapshot_type` remain (harmless extra field).

**Risk:** Medium. Crawler change may affect downstream consumers. Write tests first.

---

### Phase 6C — Prediction Registry Enhancement

**Goal:** Persist `model_version`, `prediction_time_utc`, `feature_version`, and canonical `match_id` per prediction.

**Files likely changed:**
- Prediction pipeline entry point (inspect `wbc_backend/` or `models/` for the export function)
- `data/wbc_backend/reports/prediction_registry.jsonl` — new records have enhanced schema

**New fields to add:**
```jsonc
{
  "canonical_match_id": "string — TSL numeric match_id, required for join",
  "model_version":      "string — e.g. gbm_stack_v2.1",
  "feature_version":    "string — e.g. features_32_v1",
  "prediction_time_utc":"ISO8601 — when inference ran (not recorded_at_utc of API call)"
}
```

**Acceptance criteria:**
- New prediction records contain `canonical_match_id` that joins to `tsl_odds_history.match_id`
- `prediction_time_utc` confirmed before `match_time_utc`
- `model_version` non-empty
- Old records without these fields handled by downstream code (nullable / optional)

**Rollback:** New fields are additive; old consumers ignore unknown fields.

**Risk:** Medium. Requires identifying where predictions are written and adding the ID mapping.

---

### Phase 6D — Settlement Join

**Goal:** Link settled match result to prediction and odds snapshot; compute `realized_roi` and `hit`.

**Files likely changed:**
- New script: `scripts/build_settlement_join.py` (read-only computation, writes to `data/`)
- New output: `data/clv_settlement_joined.jsonl`
  - columns: `match_id`, `prediction_id`, `market_type`, `selection`, `decimal_odds_at_bet`,
    `closing_decimal_odds`, `CLV_probability_delta`, `realized_roi`, `hit`, `settled_at_utc`

**Acceptance criteria:**
- All 5 leakage rules in §4.4 enforced; records that fail leakage check are tagged `leakage=True` and excluded from analysis
- `realized_roi` only populated for `bet_decision = BET` rows
- Script idempotent (safe to rerun)
- Output row count matches settled bets with valid prediction+odds join

**Rollback:** Delete `data/clv_settlement_joined.jsonl`; no source files modified.

**Risk:** Low (new file only). Correctness risk: leakage rules must be tested with edge cases.

---

### Phase 6E — CLV Validation Script

**Goal:** Compute CLV buckets, check sample sufficiency, run statistical test, output validation report.

**Files likely changed:**
- New script: `scripts/validate_clv_signal.py`
- Output: `research/market_signal_validation_{date}.md` (new dated report)

**Script logic:**
1. Load `data/clv_settlement_joined.jsonl`
2. Compute `CLV_probability_delta` per row
3. Bucket into `CLV_high (>0.03)`, `CLV_mid`, `CLV_low`
4. Check `len(CLV_high) >= 200` and `len(CLV_low) >= 200`
5. Compute ROI per bucket
6. Run two-sample t-test (CLV_high ROI vs CLV_low ROI)
7. Check `p < 0.05` AND `ROI_delta >= +0.03`
8. Output validation decision: `VALIDATED | REJECTED | INCONCLUSIVE_NEED_MORE_DATA | NEEDS_DATA_PIPELINE`

**Acceptance criteria:**
- All 5 leakage rules re-checked before analysis
- Sample counts reported before statistical test
- Decision enum written to report
- Report passes contamination check (0 lottery-domain terms)

**Rollback:** Delete script; no data file modified.

**Risk:** Low (analysis only).

---

### Phase 6F — Orchestrator Integration

**Goal:** When a validation report produces `NEEDS_DATA_PIPELINE`, the planner automatically
creates a `data_pipeline` task instead of re-queuing the same validation.

**Files likely changed:**
- `orchestrator/planner_tick.py` — add routing logic for `NEEDS_DATA_PIPELINE` decision
- New task type: `data_pipeline` in `orchestrator/db.py` task_type enum

**Routing logic:**
```python
# In process_completed_exploration_tasks() or equivalent router:
if validation_decision == "NEEDS_DATA_PIPELINE":
    create_task(
        task_type="data_pipeline",
        lane="market_signal_clv",
        title="Build CLV validation data pipeline",
        priority=HIGH,
        dedupe_key=f"data_pipeline:market_signal:{today}",
    )
elif validation_decision == "VALIDATED":
    create_task(task_type="strategy_review", ...)
elif validation_decision == "REJECTED":
    create_task(task_type="audit", ...)
```

**Acceptance criteria:**
- Planner does NOT create a new `validation_market_signal` task if `NEEDS_DATA_PIPELINE`
- `data_pipeline` task is created with correct dedupe_key
- No automatic strategy promotion
- Existing `process_completed_exploration_tasks` path not broken

**Rollback:** Revert `planner_tick.py` change.

**Risk:** Medium. Planner logic change — requires regression test.

---

## 7. Future Implementation Prompts

### Prompt 1 — Phase 6A: Data Contract Spec (No Runtime Mutation)

```text
# TASK: BETTING-POOL PHASE 6A — CLV VALIDATION DATA CONTRACT SPEC

GOAL:
Write the canonical data contract for Betting-pool CLV validation as documentation files.
No code changes. No runtime mutation.

INPUT:
- docs/orchestration/phase6_market_signal_data_pipeline_design_2026-04-29.md
  (§2 CLV Validation Data Contract, §3 Gap Table)

DELIVERABLES:

1. docs/orchestration/data_contract_clv_validation.md
   - Full JSONL schema for each of the 5 contract sections
   - Field descriptions, types, nullability, example values
   - Leakage guard rules per field

2. docs/orchestration/match_id_mapping_spec.md
   - Design for canonical match_id that works across TSL and prediction registry
   - Mapping table spec: tsl_match_id (numeric), wbc_game_id (pool code), league, match_date
   - Rules for handling leagues without WBC-style game IDs (CPBL, NPB, MLB)

CONSTRAINTS:
- Documentation files only
- No code changes
- No DB changes
- No external API calls
- No git commit (unless explicitly instructed)
- LotteryNew contamination check must = 0

ACCEPTANCE CRITERIA:
- Both docs files created
- All 5 contract sections documented
- Canonical match_id design covers WBC + CPBL + MLB
- Leakage rules explicitly stated per field
- Contamination = 0
```

---

### Prompt 2 — Phase 6B: Crawler Snapshot Type Tagging

```text
# TASK: BETTING-POOL PHASE 6B — ADD SNAPSHOT_TYPE TO TSL CRAWLER

GOAL:
Add snapshot_type (OPENING / CLOSING / INTERMEDIATE / POST_MATCH) classification
to data/tsl_crawler_v2.py.

New snapshots written to data/tsl_odds_history.jsonl will include snapshot_type.
Historical records are NOT backfilled (append-only file).

INPUT:
- docs/orchestration/phase6_market_signal_data_pipeline_design_2026-04-29.md (§6B)
- docs/orchestration/data_contract_clv_validation.md (Phase 6A output — must exist first)
- data/tsl_crawler_v2.py (existing crawler)
- data/tsl_odds_history.jsonl (existing history, append-only)

CLASSIFICATION RULE:
  CLOSING_WINDOW_MINUTES = 30  # configurable via config/settings.py
  
  if fetched_at < game_time - 4 hours:
      snapshot_type = "OPENING"   # use ONLY first snapshot per match×market×selection
  elif game_time - 30min <= fetched_at < game_time:
      snapshot_type = "CLOSING"
  elif fetched_at >= game_time:
      snapshot_type = "POST_MATCH"  # exclude from CLV computation
  else:
      snapshot_type = "INTERMEDIATE"

CONSTRAINTS:
- Modify only data/tsl_crawler_v2.py and config/settings.py (for CLOSING_WINDOW_MINUTES)
- Do NOT modify data/tsl_odds_history.jsonl (append-only)
- Do NOT modify DB schema
- Do NOT modify model or strategy files
- Write a unit test in tests/ covering the classification logic
- Pass py_compile before commit

ACCEPTANCE CRITERIA:
- tsl_crawler_v2.py writes snapshot_type on every new record
- Classification logic is unit-tested (≥3 test cases: OPENING, CLOSING, POST_MATCH)
- snapshot_time_utc < match_time_utc enforced for OPENING and CLOSING
- Existing crawler behaviour for fields other than snapshot_type is unchanged
- LotteryNew contamination check = 0
```

---

## 8. Missing Evidence Records

Per the cross-system design guard rule — if a concept cannot be mapped with evidence, report:

- `DOMAIN_DESIGN_REQUIRED: canonical_match_id mapping table`
  `MISSING_EVIDENCE: No join table or normalization layer exists between TSL numeric match_ids and WBC pool-code game_ids. Zero-row overlap confirmed.`

- `DOMAIN_DESIGN_REQUIRED: settlement_result joined to bet`
  `MISSING_EVIDENCE: postgame_results.jsonl contains 49 WBC settlement records but none include odds snapshot references. No realized_roi record exists for any bet.`

- `DOMAIN_DESIGN_REQUIRED: snapshot_type classification`
  `MISSING_EVIDENCE: tsl_odds_history.jsonl has 1,205 records, none with snapshot_type field. Opening vs closing is inferred only by temporal position, which has confirmed leakage risk.`

---

## 9. Scope Confirmation

- ✅ No code modified
- ✅ No DB schema changed
- ✅ No crawler changed
- ✅ No model changed
- ✅ No external API called
- ✅ No new orchestrator tasks created
- ✅ No validation task executed
- ✅ No CTO review or merge policy implemented
- ✅ No git commit made
- ✅ LotteryNew contamination = 0 (see §10)

---

## 10. Contamination Check

This document was reviewed for lottery-domain terms.
All disallowed lottery-domain patterns were searched. Result: 0 occurrences.
This document contains only Betting-pool-native market, odds, and CLV terminology.
