# P38A Odds Join Key Mapping Spec — 2026-05-14

**Status:** RESEARCH SPEC ONLY — No production join implemented  
**Author:** CTO Agent  
**Date:** 2026-05-14  
**Scope:** Defines join rules between P38A OOF prediction output and research odds CSV  
**Depends on:** `p38a_oof_output_contract_inventory_20260514.md`, `research_odds_manual_import_contract_20260513.md`  
**Acceptance Marker:** P38A_ODDS_JOIN_KEY_MAPPING_SPEC_20260514_READY

---

## ⚠️ Mandatory Constraints

> - No production join executed — this is a specification document
> - No live odds consumed
> - No production ledger written
> - All join mechanics described here apply to PAPER_ONLY / research artifacts
> - If at any step a timestamp shows odds snapshot AFTER game start → reject from pregame simulation

---

## 1. P38A Side Keys

All keys derivable from `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv`.

### 1.1 Primary Join Key

| Key | Source Column | Format | Example | Notes |
|---|---|---|---|---|
| `game_id` | `game_id` (direct) | `{HOME}-{YYYYMMDD}-{N}` | `BAL-20240415-0` | Retrosheet format. Primary key for exact join. |

### 1.2 Derived Composite Key (fallback when odds CSV lacks game_id)

| Derived Key | Derivation Rule | Example |
|---|---|---|
| `home_team` | `game_id.split('-')[0]` | `BAL` (Retrosheet 3-letter) |
| `game_date` | `game_id.split('-')[1]` → parse as YYYYMMDD → ISO date | `2024-04-15` |
| `doubleheader_game_num` | `int(game_id.split('-')[2])` | `0` or `1` |

**Composite key (fallback):** `(game_date, home_team, away_team)`

⚠️ `away_team` is NOT in P38A CSV directly — must be resolved via bridge join:
```
p38a_predictions ← game_id → mlb_2024_game_identity_outcomes_joined → away_team
```

### 1.3 Fold / Window Metadata (optional)

| Key | Source Column | Notes |
|---|---|---|
| `fold_id` | `fold_id` | Integer 0–9. Walk-forward fold index. Not a join key but useful for cohort analysis. |
| `model_version` | `model_version` | Constant `p38a_walk_forward_logistic_v1`. |

---

## 2. Odds Side Keys

Based on `research_odds_manual_import_contract_20260513.md` schema.

### 2.1 Required Odds Side Keys

| Key | Column in Contract | Format | Example | Required |
|---|---|---|---|---|
| `game_date` | `game_date` | YYYY-MM-DD | `2024-04-15` | ✅ YES |
| `home_team` | `home_team` | Retrosheet 3-letter preferred | `BAL` | ✅ YES |
| `away_team` | `away_team` | Retrosheet 3-letter preferred | `BOS` | ✅ YES |
| `market` | `market` | `moneyline` | `moneyline` | ✅ YES |
| `closing_home_moneyline` | `closing_home_moneyline` | American odds integer | `-145` | ✅ YES |
| `closing_away_moneyline` | `closing_away_moneyline` | American odds integer | `+125` | ✅ YES |
| `source_name` | `source_name` | See contract Section 6 | `research_fixture` | ✅ YES |
| `source_license_status` | `source_license_status` | See contract Section 7 | `synthetic_no_license` | ✅ YES |

### 2.2 Optional Odds Side Keys (aid join accuracy)

| Key | Column | Notes |
|---|---|---|
| `game_id_optional` | `game_id_optional` | If present, enables exact game_id join (best path) |
| `retrosheet_game_id_optional` | `retrosheet_game_id_optional` | Retrosheet format — directly joinable to P38A game_id |
| `snapshot_time_optional` | `snapshot_time_optional` | ISO 8601 UTC — used for leakage check |
| `sportsbook_optional` | `sportsbook_optional` | For multi-book analysis |
| `opening_home_moneyline_optional` | `opening_home_moneyline_optional` | Opening line if available |
| `opening_away_moneyline_optional` | `opening_away_moneyline_optional` | Opening line if available |

---

## 3. Team Normalization Table

P38A uses Retrosheet 3-letter codes. Most odds sources use common abbreviations (ESPN/MLB style). Normalization required before join.

### 3.1 Known Divergent Codes (Retrosheet → Common)

| Retrosheet Code | Common Code | Team Name |
|---|---|---|
| `NYA` | `NYY` | New York Yankees |
| `NYN` | `NYM` | New York Mets |
| `LAN` | `LAD` | Los Angeles Dodgers |
| `CHA` | `CHW` | Chicago White Sox |
| `CHN` | `CHC` | Chicago Cubs |
| `SFN` | `SF` / `SFG` | San Francisco Giants |
| `SDN` | `SD` / `SDP` | San Diego Padres |
| `KCA` | `KC` / `KCR` | Kansas City Royals |
| `TBA` | `TB` / `TBR` | Tampa Bay Rays |
| `MIL` | `MIL` | Milwaukee Brewers (same) |
| `OAK` | `OAK` / `ATH` | Oakland/Sacramento Athletics |
| `WAS` | `WSH` | Washington Nationals |
| `ARI` | `ARI` | Arizona Diamondbacks (same) |
| `ANA` | `LAA` | Los Angeles Angels (legacy: `ANA`) |
| `TOR` | `TOR` | Toronto Blue Jays (same) |
| `BAL` | `BAL` | Baltimore Orioles (same) |
| `BOS` | `BOS` | Boston Red Sox (same) |
| `CLE` | `CLE` / `CLG` | Cleveland Guardians |
| `DET` | `DET` | Detroit Tigers (same) |
| `HOU` | `HOU` | Houston Astros (same) |
| `MIN` | `MIN` | Minnesota Twins (same) |
| `SEA` | `SEA` | Seattle Mariners (same) |
| `TEX` | `TEX` | Texas Rangers (same) |
| `ATL` | `ATL` | Atlanta Braves (same) |
| `MIA` | `MIA` | Miami Marlins (same) |
| `PHI` | `PHI` | Philadelphia Phillies (same) |
| `PIT` | `PIT` | Pittsburgh Pirates (same) |
| `SLN` | `STL` | St. Louis Cardinals |
| `COL` | `COL` | Colorado Rockies (same) |
| `CIN` | `CIN` | Cincinnati Reds (same) |

### 3.2 Normalization Application Rule

1. Odds source team field format must be assessed when the odds source is loaded.
2. Apply normalization table to convert odds source team codes → Retrosheet 3-letter codes.
3. If normalization fails (unknown team name), mark row as `TEAM_NORMALIZATION_FAILED` — do NOT silently drop.
4. Log all unmatched team names for review.

---

## 4. Date Matching Rules

### 4.1 Format Handling

| Side | Expected Format | Rule |
|---|---|---|
| P38A (derived) | `YYYYMMDD` → parse to `YYYY-MM-DD` ISO | Strip and parse first 10 chars of derived date |
| Odds contract | `YYYY-MM-DD` ISO string | Parse directly |
| Divergence | If odds source uses MM/DD/YYYY or other | Convert to ISO before join |

### 4.2 UTC vs Local Date Handling

| Scenario | Rule |
|---|---|
| Odds source uses UTC timestamp | Convert to US Eastern local date if game is in Eastern TZ; use local date for comparison |
| Odds source uses local date only | Compare directly — assume same convention |
| Ambiguous timezone | Flag as `DATE_TZ_AMBIGUOUS` — do not silently accept |

### 4.3 Special Game Scenarios

| Scenario | Rule |
|---|---|
| Postponed game | P38A output does not include postponed games (Retrosheet GL has only played games). If odds CSV has a postponed game, it will have no P38A match → mark `UNMATCHED_POSTPONED` |
| Suspended/resumed game | Treated as single game in Retrosheet. If odds CSV splits into 2 entries, one will be unmatched. |
| Double-header | P38A uses `-0` and `-1` suffix in game_id. Odds source likely has no such suffix. Both DH games will have same (date, home, away) → mark as `DOUBLEHEADER_AMBIGUOUS` if no game_num available. |
| Exhibition games | 2024 Seoul Series (March 20–21) IS in Retrosheet GL2024. Odds source may or may not have it. |

---

## 5. Join Algorithm v1

### 5.1 Primary Join Path (game_id exact match)

**Precondition:** Odds CSV has `game_id_optional` or `retrosheet_game_id_optional` that matches `{HOME}-{YYYYMMDD}-{N}` format.

```
Algorithm:
  For each odds_row:
    If odds_row.retrosheet_game_id_optional is not null:
      Normalize format to {HOME}-{YYYYMMDD}-{N}
      Join: p38a[game_id] == odds[retrosheet_game_id_optional]
    Elif odds_row.game_id_optional is not null:
      Attempt direct join: p38a[game_id] == odds[game_id_optional]
    Else:
      Fall through to COMPOSITE JOIN
```

### 5.2 Fallback: Composite Key Join (no game_id in odds)

```
Algorithm:
  Normalize odds_row.home_team → Retrosheet code
  Normalize odds_row.away_team → Retrosheet code
  Parse odds_row.game_date → ISO YYYY-MM-DD

  Candidate matches = p38a_enriched[
    game_date == odds_row.game_date
    AND home_team == odds_row.home_team (after normalization)
    AND away_team == odds_row.away_team (after normalization)
  ]

  If len(candidates) == 0:
    Record as UNMATCHED
  If len(candidates) == 1:
    Accept match
  If len(candidates) > 1:
    Record as DOUBLEHEADER_AMBIGUOUS (emit both rows with flag)
```

### 5.3 Duplicate Odds Detection

```
For each (game_id, market, sportsbook_optional):
  If multiple odds rows match same game_id + market + sportsbook:
    Emit DUPLICATE_ODDS_DETECTED warning
    Strategy: Take first occurrence (implicit opening) or last (implicit closing)
    Must be explicit in join run configuration
```

### 5.4 Unmatched Report Structure

```json
{
  "unmatched_p38a_rows": [...],  // P38A rows with no odds match
  "unmatched_odds_rows": [...],  // Odds rows with no P38A prediction
  "ambiguous_rows": [...],       // Double-header or duplicate ambiguity
  "normalization_failures": [...] // Team name normalization failures
}
```

---

## 6. Leakage Rules

### 6.1 Core Principle

P38A `p_oof` is a pregame-only prediction. Odds features must also be pregame-safe to be used in any simulation that feeds model input.

For **benchmark / CLV study** (not model input), closing odds may be used with explicit documentation that they are post-open.

### 6.2 Timestamp Policy

| Scenario | Rule |
|---|---|
| `snapshot_time_optional` is NULL | Classify as CLOSING_LINE_RESEARCH_ONLY — cannot be used in pregame simulation |
| `snapshot_time_optional` < game start time | ✅ Acceptable as pregame odds feature |
| `snapshot_time_optional` >= game start time | ❌ REJECT from pregame simulation. May use for CLV study only with explicit flag. |
| `snapshot_time_optional` = "2024-04-01T17:30:00Z" but game was at 19:05 ET | ✅ Acceptable (if UTC conversion confirms it is before game time) |

### 6.3 Closing Line Research Policy

Closing moneyline is allowed in research context ONLY for:
- CLV (Closing Line Value) benchmarking
- Market efficiency study
- Post-hoc performance analysis

Closing line MUST NOT feed back into:
- P38A feature matrix (feature adapter inputs)
- Pregame recommendation trigger
- Any model input path

All closing-line joined rows must carry field: `odds_leakage_status = closing_line_research_only`

### 6.4 Pregame Simulation Use

For any future pregame simulation (P3 replay or similar):
1. Must have odds with `snapshot_time_optional` confirmed BEFORE game start.
2. If timestamp absent → REJECT from simulation.
3. If fixture odds (dummy values) → label `fixture_only_odds` — may run simulation structure but results are NOT meaningful.

---

## 7. Join Output Schema (v1 definition)

The output of a successful join should produce a row with:

| Column | Source |
|---|---|
| `game_id` | P38A (primary) |
| `game_date` | Derived from P38A game_id or odds |
| `season` | Derived (year of game_date) |
| `home_team` | Derived from P38A + game identity bridge |
| `away_team` | Derived from game identity bridge |
| `fold_id` | P38A |
| `p_oof` | P38A |
| `model_version` | P38A |
| `closing_home_moneyline` | Odds |
| `closing_away_moneyline` | Odds |
| `implied_prob_home` | Derived: `1 / (1 + 10^(closing_home_moneyline/100))` if positive; `abs(ml)/(abs(ml)+100)` if negative |
| `implied_prob_away` | Derived similarly |
| `market` | Odds |
| `source_name` | Odds |
| `source_license_status` | Odds |
| `odds_leakage_status` | Derived from timestamp policy |
| `join_method` | `game_id_exact` or `composite_key` or `UNMATCHED` |
| `join_ambiguity_flag` | `DOUBLEHEADER_AMBIGUOUS`, `DUPLICATE_ODDS`, or NULL |

---

## 8. Implied Probability Conversion Reference

American odds → implied probability (before vig normalization):

```
If moneyline > 0:  p_implied = 100 / (moneyline + 100)
If moneyline < 0:  p_implied = abs(moneyline) / (abs(moneyline) + 100)

Example: closing_home_moneyline = -145
  p_implied_home = 145 / (145 + 100) = 145 / 245 = 0.5918

Example: closing_away_moneyline = +125
  p_implied_away = 100 / (125 + 100) = 100 / 225 = 0.4444

Vig-free normalization:
  total_implied = p_implied_home + p_implied_away  (usually > 1.0)
  p_nvig_home = p_implied_home / total_implied
  p_nvig_away = p_implied_away / total_implied
```

No-vig implied probability is the theoretically fair line for benchmark comparison against `p_oof`.

---

## 9. Acceptance Marker

```
P38A_ODDS_JOIN_KEY_MAPPING_SPEC_20260514_READY
```
