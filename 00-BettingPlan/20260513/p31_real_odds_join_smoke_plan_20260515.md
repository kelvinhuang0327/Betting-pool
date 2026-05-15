# P3.1 Real Odds ≥100 Rows Join Smoke Plan — 2026-05-15

**Status:** REAL_JOIN_SMOKE_NOT_EXECUTED_DATA_NOT_PRESENT  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Reason:** No real 2024 MLB odds data present in `data/research_odds/local_only/` — all sources blocked pending user decision (see `p31_no_download_blocker_20260515.md`)  
**5-Row Fixture Smoke:** Previously EXECUTED and PASSED (5/5) — see `p38a_fixture_only_join_smoke_report_20260514.md`  
**References:**
- `p38a_odds_join_key_mapping_spec_20260514.md` (join algorithm v1)
- `p38a_oof_output_contract_inventory_20260514.md` (P38A OOF schema)
- `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` (bridge table)
- `data/research_odds/fixtures/P38A_JOIN_SMOKE_TEMPLATE_20260514.csv` (5-row fixture)

---

## 1. Smoke Test Not Executed — Reason

```
STATUS: REAL_JOIN_SMOKE_NOT_EXECUTED_DATA_NOT_PRESENT
REASON: data/research_odds/local_only/ is empty.
DEPENDENCY: One of the 4 unblock paths (see p31_no_download_blocker_20260515.md) must be completed first.
```

The join infrastructure is fully built. The test will execute the moment real data arrives.

---

## 2. What the ≥100 Row Join Smoke Tests

### 2.1 Purpose

Verify that real external odds data (any approved source) can be:
1. Ingested in the 23-column contract CSV format
2. Joined to P38A OOF predictions via `game_id` key
3. Joined to bridge table to derive `y_true_home_win` and game metadata
4. Produce a valid P38A + odds + outcome 3-way joined row with all required fields non-null

### 2.2 Required Columns in Input Odds File (23-Column Contract)

```
game_id, game_date, season, away_team, home_team,
home_ml_american, away_ml_american,
home_ml_decimal, away_ml_decimal,
home_implied_prob_raw, away_implied_prob_raw,
vig_total, home_no_vig_prob, away_no_vig_prob,
bookmaker_key, market_key, odds_timestamp_utc,
snapshot_type, source_name, source_row_number,
source_license_status, source_license_type, retrieval_method
```

### 2.3 Join Algorithm v1 (from join key spec)

```python
# Step 1: Load P38A OOF predictions
oof = pd.read_csv("outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv")

# Step 2: Load bridge table (game_id → metadata + y_true)
bridge = pd.read_csv("data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv")

# Step 3: Load real odds (local_only)
odds = pd.read_csv("data/research_odds/local_only/<source_file>.csv")

# Step 4: Three-way join
# Join 1: OOF predictions → bridge (inner, on game_id)
oof_bridge = oof.merge(bridge, on="game_id", how="inner")

# Join 2: oof_bridge → odds (inner, on game_id)
joined = oof_bridge.merge(odds, on="game_id", how="inner")

# Assert: ≥100 rows
assert len(joined) >= 100, f"Join produced only {len(joined)} rows — minimum 100 required"

# Assert: No null values in critical columns
critical_cols = ["p_oof", "home_ml_american", "home_no_vig_prob", "y_true_home_win"]
for col in critical_cols:
    assert joined[col].isna().sum() == 0, f"Null values found in {col}"
```

### 2.4 Expected Smoke Test Output Columns

| Column | Source | Type | Notes |
|---|---|---|---|
| `game_id` | P38A / bridge / odds (all 3) | str | Join key |
| `game_date` | bridge | str (YYYY-MM-DD) | From bridge table |
| `season` | bridge | int | 2024 |
| `away_team` | bridge | str | Retrosheet 3-letter |
| `home_team` | bridge | str | Retrosheet 3-letter |
| `fold_id` | P38A | int | 0–9 (10-fold WF-OOF) |
| `p_oof` | P38A | float | Predicted home-win prob |
| `model_version` | P38A | str | `p38a_walk_forward_logistic_v1` |
| `home_ml_american` | odds | int | e.g., -150 |
| `away_ml_american` | odds | int | e.g., +130 |
| `home_no_vig_prob` | odds | float | No-vig implied prob |
| `away_no_vig_prob` | odds | float | No-vig implied prob |
| `bookmaker_key` | odds | str | e.g., `draftkings` |
| `odds_timestamp_utc` | odds | str | ISO 8601 |
| `snapshot_type` | odds | str | `closing` or `pregame` |
| `source_license_status` | odds | str | Must NOT be `synthetic_no_license` |
| `y_true_home_win` | bridge | int | 1=home win, 0=away win |
| `vig_total` | odds | float | Vig/overround |
| `home_implied_prob_raw` | odds | float | Raw implied prob before vig removal |

---

## 3. ≥100 Row Minimum Justification

| Requirement | Value | Rationale |
|---|---|---|
| Minimum rows | 100 | Sufficient for basic coverage verification and statistical sanity check |
| Ideal rows | 500–2,187 | Full 2024 season for CLV analysis |
| Maximum possible | 2,187 | Full P38A OOF prediction count |
| Bridge coverage | 2,429 input → 2,187 predictions (90.04% coverage) | Some game_ids may not join |
| Odds join drop rate (expected) | 5–20% | Team normalization and timestamp matching may exclude some games |
| Expected joined rows (full season) | 1,700–2,100 | Acceptable |

---

## 4. Source-Specific Join Notes

### The Odds API (if approved)

```python
# Raw response structure (JSON):
{
  "id": "<event_id>",
  "sport_key": "baseball_mlb",
  "commence_time": "2024-04-03T23:35:00Z",  # UTC ISO 8601 → map to game_date
  "home_team": "Baltimore Orioles",           # → Retrosheet: "BAL"
  "away_team": "Boston Red Sox",              # → Retrosheet: "BOS"
  "bookmakers": [{
    "key": "draftkings",
    "markets": [{
      "key": "h2h",
      "outcomes": [
        {"name": "Baltimore Orioles", "price": -145},  # American moneyline
        {"name": "Boston Red Sox", "price": +122}
      ]
    }]
  }]
}

# game_id derivation:
# game_id = f"{home_retrosheet_code}-{game_date_no_dash}-0"
# e.g., "BAL-20240403-0"
```

### Kaggle oliviersportsdata (if purchased)

```
Separator: semicolon (;)
Encoding: UTF-8
Odds format: American moneyline
Team format: UNKNOWN — schema inspection required post-purchase
Date format: UNKNOWN — schema inspection required post-purchase
game_id derivation: must map to Retrosheet format via home_team + game_date
```

---

## 5. Success Criteria for ≥100 Row Smoke

| Criterion | Pass Condition |
|---|---|
| Row count | `len(joined) >= 100` |
| No null `p_oof` | `joined["p_oof"].isna().sum() == 0` |
| No null `home_ml_american` | `joined["home_ml_american"].isna().sum() == 0` |
| No null `home_no_vig_prob` | `joined["home_no_vig_prob"].isna().sum() == 0` |
| No null `y_true_home_win` | `joined["y_true_home_win"].isna().sum() == 0` |
| License not synthetic | `"synthetic_no_license"` NOT present in `source_license_status` |
| season == 2024 | `joined["season"].nunique() == 1` and `joined["season"].iloc[0] == 2024` |
| p_oof in (0, 1) | `joined["p_oof"].between(0.01, 0.99).all()` |
| home_no_vig_prob in (0, 1) | `joined["home_no_vig_prob"].between(0.01, 0.99).all()` |
| model_version correct | `joined["model_version"].iloc[0] == "p38a_walk_forward_logistic_v1"` |

---

## 6. Output File Location

When executed, results go to:
```
outputs/predictions/PAPER/p38a_2024_oof/p38a_oof_real_odds_joined_100row_smoke.csv
```

Report goes to:
```
00-BettingPlan/20260513/p31_real_odds_join_smoke_EXECUTED_20260515.md
```

---

## 7. Acceptance Marker

```
REAL_JOIN_SMOKE_NOT_EXECUTED_DATA_NOT_PRESENT_20260515
```

**Note:** When user provides data and test passes, this marker is superseded by:
```
P31_REAL_ODDS_JOIN_SMOKE_EXECUTED_20260515_READY
```
