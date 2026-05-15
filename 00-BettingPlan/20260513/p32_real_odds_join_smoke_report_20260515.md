# P3.2 Real Odds Join Smoke Report — 2026-05-15

**Status:** NOT_EXECUTED  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Acceptance Marker:** `P32_REAL_ODDS_JOIN_SMOKE_NOT_EXECUTED_20260515`

---

## 1. Execution Status

```
GATE DECISION: ODDS_DATA_NOT_READY (from TRACK 1)

Join smoke NOT EXECUTED.
Reason: No real odds data available in data/research_odds/local_only/
```

---

## 2. Pass Criteria (For Next Session)

| Criterion | Threshold | Notes |
|---|---|---|
| Odds rows after transform | ≥ 100 | Minimum for statistically meaningful join test |
| Join match rate | ≥ 80% | `(game_id, game_date, home_team, away_team)` composite key |
| Parse fatal errors | 0 | No rows with null home/away team |
| Raw data committed to git | 0 | Contract violation if any raw file committed |
| Leakage classification | Explicit | `snapshot_type` must be populated for ALL rows |

---

## 3. Join Key Spec (For Reference)

**Primary join key:** `game_id` (Retrosheet format `{HOME}-{YYYYMMDD}-{N}`)

**Fallback composite key:** `(game_date, home_team, away_team)`

```
P38A OOF predictions:
  outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv
  columns: game_id, fold_id, p_oof, model_version, source_prediction_ref

Bridge table:
  data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv
  columns: game_id, game_date, season, away_team, home_team, ...

Odds contract (to be produced):
  data/research_odds/local_only/research_contract_2024.csv
  columns: [23-column contract]

Join sequence:
  1. p38a_predictions --[game_id]--> bridge_table → adds game_date, home_team, away_team
  2. bridge_enriched --[game_date+home_team+away_team]--> odds_contract → adds home_no_vig_prob
  3. merged --[computed]--> clv_edge_home = p_oof - home_no_vig_prob
```

---

## 4. Expected Join Output Schema

| Column | Source |
|---|---|
| `game_id` | P38A / bridge |
| `game_date` | bridge |
| `season` | bridge |
| `home_team` | bridge |
| `away_team` | bridge |
| `fold_id` | P38A |
| `p_oof` | P38A |
| `model_version` | P38A |
| `home_ml_american` | odds contract |
| `home_no_vig_prob` | odds contract (computed) |
| `bookmaker_key` | odds contract |
| `odds_timestamp_utc` | odds contract |
| `snapshot_type` | odds contract |
| `clv_edge_home` | derived: `p_oof - home_no_vig_prob` |
| `y_true_home_win` | bridge |

---

## 5. Resume Instructions

When data is available:

```
1. Drop real odds contract CSV to:
   data/research_odds/local_only/research_contract_2024.csv

2. Tell agent: "Join smoke ready — data/research_odds/local_only/research_contract_2024.csv exists."

3. Agent will execute join smoke automatically.
```

---

## 6. Acceptance Marker

```
P32_REAL_ODDS_JOIN_SMOKE_NOT_EXECUTED_20260515
```
