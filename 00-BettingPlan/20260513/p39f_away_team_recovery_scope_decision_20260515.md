# P39F — Away Team Recovery Scope Decision
**Date**: 2026-05-15
**Marker**: `P39F_AWAY_TEAM_RECOVERY_SCOPE_READY_20260515`
**Mode**: BRIDGE_ENRICHMENT_FIRST

---

## Problem Statement

### Root Cause
P38A OOF CSV (`outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv`) contains only:
```
game_id, fold_id, p_oof, model_version, source_prediction_ref, generated_without_y_true
```
No `away_team`, no `home_team` column (only extractable from `game_id` prefix), no `game_date`.

P39E partially resolved this by extracting `home_team` from the `game_id` prefix (`CHA-20240415-0` → home_team = CHA → normalized CWS). Away team was permanently 0% match because the CSV had no away_team field.

### Impact
- Overall home match rate: 9.6% (April features only)
- Away match rate: 0% (always, schema limitation)
- Complete home+away enrichment: impossible without recovery

---

## Selected Input Source

**Identity Bridge**: `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv`

| Field | Value |
|-------|-------|
| Rows | 2,429 |
| Date range | 2024-03-20 → 2024-09-30 |
| Duplicate game_id | 0 |
| Missing away_team | 0 |
| Missing home_team | 0 |
| Team code format | Retrosheet (CHA, KCA, LAN, SDN, TBA, etc.) |

### Why This Bridge Works
- Bridge `game_id` format: `CHA-20240415-0` — identical to P38A `game_id` format
- **Direct join on game_id: 2187/2187 = 100% match rate** (confirmed in inspection)
- Bridge contains both `home_team` (Retrosheet) AND `away_team` (Retrosheet)
- No nulls, no duplicates — join is clean

---

## Required Mapping

```
P38A.game_id → bridge.game_id (1:1 exact string match)
  → bridge.home_team (Retrosheet code)
  → bridge.away_team (Retrosheet code)
  → bridge.game_date (YYYY-MM-DD)
```

After bridge enrichment: apply `team_code_normalization` to both `home_team` and `away_team` before joining with P39B Statcast rolling features.

---

## Expected Results

| Metric | Expected |
|--------|---------|
| P38A bridge match rate | **100%** (2187/2187) |
| April in-scope home+away bridge match | **100%** (210/210) |
| April in-scope home feature match (post-normalize) | ~100% (from P39E) |
| April in-scope away feature match (post-normalize) | ~100% (30 teams in April features) |
| April complete home+away feature match | **≥80%** (target) |

---

## Non-Goals

- Not running full-season Statcast fetch (deferred to P39G)
- Not processing odds or CLV data
- Not modifying P38A prediction probabilities (`p_oof` is read-only)
- Not modifying licensed odds approval JSON (P37.5)
- Not pushing without explicit YES

---

## Scope Decision: BRIDGE_ENRICHMENT_FIRST

Rationale:
1. Bridge gives instant 100% away_team recovery at zero network cost
2. Existing April P39E rolling features cover Apr 8–30 → April away feature join is feasible immediately
3. Full-season Statcast fetch (P39G) deferred until bridge recovery is validated

---

## Marker

`P39F_AWAY_TEAM_RECOVERY_SCOPE_READY_20260515`
