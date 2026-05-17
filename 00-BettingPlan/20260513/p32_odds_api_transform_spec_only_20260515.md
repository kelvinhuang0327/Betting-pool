# P3.2 Odds API Transform Spec — 2026-05-15

**Status:** SPEC_ONLY (Transform not executed — no raw data available)  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Trigger:** ODDS_DATA_NOT_READY (no raw JSON in local_only/)  
**Script:** `scripts/transform_odds_api_to_research_contract.py`  
**Acceptance Marker:** `P32_ODDS_API_TRANSFORM_SPEC_ONLY_20260515`

---

## 1. Transform Overview

Converts raw The Odds API historical h2h JSON → 23-column research contract CSV.

| Input | Output |
|---|---|
| `data/research_odds/local_only/the_odds_api_2024/YYYY-MM-DD.json` | `data/research_odds/local_only/research_contract_2024.csv` |
| Raw The Odds API response + `_fetch_meta` | 23-column research contract (gitignored) |

---

## 2. Output Schema (23 Columns)

| # | Column | Type | Source | Notes |
|---|---|---|---|---|
| 1 | `game_id` | str | Derived | `{home_retro}-{YYYYMMDD}-{N}` (N=0 assumed) |
| 2 | `game_date` | str | `commence_time[:10]` | YYYY-MM-DD |
| 3 | `season` | int | `game_date[:4]` | 4-digit year |
| 4 | `away_team` | str | Normalized | Full name → Retrosheet via lookup table |
| 5 | `home_team` | str | Normalized | Full name → Retrosheet via lookup table |
| 6 | `home_ml_american` | int | API outcome price | American odds integer |
| 7 | `away_ml_american` | int | API outcome price | American odds integer |
| 8 | `home_ml_decimal` | float | Computed | From American via formula |
| 9 | `away_ml_decimal` | float | Computed | From American via formula |
| 10 | `home_implied_prob_raw` | float | Computed | Includes vig |
| 11 | `away_implied_prob_raw` | float | Computed | Includes vig |
| 12 | `vig_total` | float | Computed | Sum of raw probs (> 1.0) |
| 13 | `home_no_vig_prob` | float | Computed | Proportional removal |
| 14 | `away_no_vig_prob` | float | Computed | Proportional removal |
| 15 | `bookmaker_key` | str | API `bookmaker.key` | e.g., `draftkings` |
| 16 | `market_key` | str | Constant | `h2h` |
| 17 | `odds_timestamp_utc` | str | `_fetch_meta.snapshot_utc` | ISO 8601 UTC |
| 18 | `snapshot_type` | str | Classified | `historical_pre_game_assumed` |
| 19 | `source_name` | str | Constant | `the_odds_api` |
| 20 | `source_row_number` | int | Sequential | 1-indexed within output CSV |
| 21 | `source_license_status` | str | Constant | `local_only_paid_provider_no_redistribution` |
| 22 | `source_license_type` | str | Constant | `paid_provider_historical_api` |
| 23 | `retrieval_method` | str | Constant | `the_odds_api_historical_h2h` |

---

## 3. Conversion Formulas

### 3.1 American → Decimal

```python
def american_to_decimal(american: int) -> float:
    if american > 0:
        return 1.0 + american / 100.0
    else:
        return 1.0 + 100.0 / abs(american)
```

### 3.2 American → Raw Implied Probability (with vig)

```python
def american_to_implied_prob(american: int) -> float:
    if american > 0:
        return 100.0 / (100.0 + american)
    else:
        return abs(american) / (abs(american) + 100.0)
```

### 3.3 No-Vig Removal (Proportional Method)

```python
def no_vig_probs(raw_home, raw_away):
    total = raw_home + raw_away
    home_no_vig = raw_home / total
    away_no_vig = raw_away / total
    return home_no_vig, away_no_vig
```

### 3.4 CLV Edge (downstream, not in transform)

```python
clv_edge_home = p_oof - home_no_vig_prob
```

---

## 4. Team Name Normalization

The Odds API returns full team names (e.g., `"Baltimore Orioles"`). P38A uses Retrosheet 3-letter codes (e.g., `BAL`).

**Lookup table (30 teams + aliases):**

| Full Name | Retrosheet Code |
|---|---|
| Baltimore Orioles | BAL |
| Boston Red Sox | BOS |
| New York Yankees | NYA |
| Tampa Bay Rays | TBA |
| Toronto Blue Jays | TOR |
| Chicago White Sox | CHA |
| Cleveland Guardians | CLE |
| Detroit Tigers | DET |
| Kansas City Royals | KCA |
| Minnesota Twins | MIN |
| Houston Astros | HOU |
| Los Angeles Angels | ANA |
| Oakland Athletics / Sacramento Athletics | OAK |
| Seattle Mariners | SEA |
| Texas Rangers | TEX |
| Atlanta Braves | ATL |
| Miami Marlins | MIA |
| New York Mets | NYN |
| Philadelphia Phillies | PHI |
| Washington Nationals | WAS |
| Chicago Cubs | CHN |
| Cincinnati Reds | CIN |
| Milwaukee Brewers | MIL |
| Pittsburgh Pirates | PIT |
| St. Louis Cardinals | SLN |
| Arizona Diamondbacks | ARI |
| Colorado Rockies | COL |
| Los Angeles Dodgers | LAN |
| San Diego Padres | SDN |
| San Francisco Giants | SFN |

---

## 5. Leakage Classification

| Dimension | Value |
|---|---|
| `snapshot_type` | `historical_pre_game_assumed` |
| Snapshot time | 21:00 UTC (fetcher constant) |
| Coverage | Before most night games (EST 17:00) |
| Risk | LOW for night games; MEDIUM for daytime games |
| Mitigation | Flag daytime games using bridge table `game_date + commence_time` |
| P38A OOF | Walk-forward trained — no future data used |
| CLV computation | Uses pre-game odds → valid closing-line value computation |

**Assumption:** All fetched snapshots tagged as `historical_pre_game_assumed`. Full leakage audit requires join to game start times in the bridge table — implemented in TRACK 4 join smoke.

---

## 6. Execution Commands (When Data is Available)

```bash
# Step 1: Fetch (requires .env with THE_ODDS_API_KEY)
.venv/bin/python scripts/fetch_odds_api_historical_mlb_2024_local.py \
  --start-date 2024-04-01 \
  --end-date 2024-04-10 \
  --execute

# Step 2: Transform (requires JSON in local_only/)
.venv/bin/python scripts/transform_odds_api_to_research_contract.py \
  --in-dir data/research_odds/local_only/the_odds_api_2024 \
  --out-file data/research_odds/local_only/research_contract_2024.csv \
  --execute

# Step 3: Verify output
wc -l data/research_odds/local_only/research_contract_2024.csv
head -3 data/research_odds/local_only/research_contract_2024.csv
```

---

## 7. Acceptance Marker

```
P32_ODDS_API_TRANSFORM_SPEC_ONLY_20260515
```
