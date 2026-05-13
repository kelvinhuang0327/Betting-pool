# Research Odds Join Certification Plan — 2026-05-13

**Status:** PLANNING SKELETON  
**Author:** CTO Agent  
**Date:** 2026-05-13  
**Scope:** Join certification path for research odds ↔ Retrosheet 2024 game log  
**Acceptance Marker:** RESEARCH_ODDS_JOIN_CERTIFICATION_PLAN_20260513_READY

---

## ⚠️ Scope Declaration

> This is a PLANNING DOCUMENT only.
> No odds data is joined or written in this document.
> Runtime implementation requires an odds dataset to be in place first.
> Join certification cannot pass until an ACCEPTABLE_FOR_RESEARCH odds source is provisioned.

---

## 1. Existing Infrastructure Audit

### 1.1 Retrosheet Side (ALREADY EXISTS)

| Component                         | File Path                                                       | Status      |
|-----------------------------------|-----------------------------------------------------------------|-------------|
| Retrosheet parser                 | `wbc_backend/recommendation/p32_retrosheet_game_log_parser.py` | ✅ EXISTS    |
| Retrosheet parser test            | `tests/test_p32_retrosheet_game_log_parser.py`                 | ✅ EXISTS    |
| Game identity CSV (2024)          | `data/mlb_2024/processed/mlb_2024_game_identity.csv`           | ✅ EXISTS    |
| Game outcomes CSV (2024)          | `data/mlb_2024/processed/mlb_2024_game_outcomes.csv`           | ✅ EXISTS    |
| Joined CSV (2024)                 | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` | ✅ EXISTS |
| Raw game log                      | `data/mlb_2024/raw/gl2024.txt` (2,429 rows, untracked)         | ✅ EXISTS (local) |
| Game log manifest                 | `data/mlb_2024/processed/mlb_2024_game_log_manifest.json`      | ✅ EXISTS    |

**Retrosheet game_id format** (confirmed from `mlb_2024_game_identity.csv`):
```
{HOME_TEAM}-{YYYYMMDD}-{GAME_NUMBER}
Example: SDN-20240320-0  (San Diego home, 2024-03-20, single game)
         BOS202404010     (Retrosheet canonical format, alternative)
```

### 1.2 Odds Import Side (P36 — ALREADY HAS SCHEMA)

| Component                         | File Path                                                       | Status      |
|-----------------------------------|-----------------------------------------------------------------|-------------|
| Manual odds import validator      | `wbc_backend/recommendation/p36_manual_odds_import_validator.py` | ✅ EXISTS  |
| Odds approval import gate contract | `wbc_backend/recommendation/p36_odds_approval_contract.py` (assumed) | ✅ EXISTS |
| Manual odds import schema         | `data/mlb_2024/processed/p36_odds_approval_import_gate/manual_odds_import_schema.json` | ✅ EXISTS |
| P36 required columns              | `game_id, game_date, home_team, away_team, p_market, odds_decimal, sportsbook, market_type, closing_timestamp, source_odds_ref, license_ref` | ✅ DEFINED |

**Key finding**: P36 already has a validation framework. The research odds join
certification should EXTEND (not replace) the P36 contract for research-grade data.

---

## 2. Retrosheet Side Expected Fields

The join LEFT side is `mlb_2024_game_identity.csv`:

| Field             | Type    | Example              | Notes                                   |
|-------------------|---------|----------------------|-----------------------------------------|
| `game_id`         | string  | `SDN-20240320-0`     | Home team + date + game number           |
| `game_date`       | string  | `2024-03-20`         | ISO 8601                                |
| `season`          | integer | `2024`               | Always 2024 for this file               |
| `away_team`       | string  | `LAN`                | Retrosheet 3-letter code                |
| `home_team`       | string  | `SDN`                | Retrosheet 3-letter code                |
| `source_name`     | string  | `Retrosheet`         | Fixed value                             |
| `source_row_number` | integer | `1`                | Row number in GL2024                   |

---

## 3. Odds Side Expected Fields

The join RIGHT side is the research odds CSV (per TRACK 3 contract):

| Field                       | Join-Relevant | Notes                                              |
|-----------------------------|---------------|----------------------------------------------------|
| `game_date`                 | ✅ PRIMARY    | Must match Retrosheet game_date (ISO 8601)         |
| `home_team`                 | ✅ PRIMARY    | Must match Retrosheet home_team after normalization |
| `away_team`                 | ✅ PRIMARY    | Must match Retrosheet away_team after normalization |
| `market`                    | Secondary     | Filter to `moneyline` for primary join             |
| `closing_home_moneyline`    | Payload       | Target field for replay                            |
| `closing_away_moneyline`    | Payload       | Target field for replay                            |
| `retrosheet_game_id_optional` | OPTIONAL join key | If present, can use as primary join key      |
| `import_scope`              | Guard         | Must be `research_only` or `local_only`           |
| `is_research`               | Guard         | Must be `true` in all output artifacts             |

---

## 4. Canonical Team Mapping Strategy

### 4.1 Problem
Odds sources use various team name formats:
- Retrosheet: `LAN`, `SDN`, `NYA`, `KCA`, `CHA`
- Common aliases: `LAD`, `SD`, `NYY`, `KC`, `CWS`
- Full names: `Los Angeles Dodgers`, `San Diego Padres`

### 4.2 Normalization Table (Retrosheet ↔ Common Aliases)

| Retrosheet Code | Common Alias(es)                          | Full Name                  |
|-----------------|-------------------------------------------|----------------------------|
| `LAN`           | `LAD`, `LA`, `Dodgers`                    | Los Angeles Dodgers        |
| `SDN`           | `SD`, `SDP`, `Padres`                     | San Diego Padres           |
| `NYA`           | `NYY`, `NY`, `Yankees`                    | New York Yankees           |
| `NYN`           | `NYM`, `Mets`                             | New York Mets              |
| `KCA`           | `KC`, `KCR`, `Royals`                     | Kansas City Royals         |
| `CHA`           | `CWS`, `CHW`, `White Sox`                 | Chicago White Sox          |
| `CHN`           | `CHC`, `Cubs`                             | Chicago Cubs               |
| `SFN`           | `SF`, `SFG`, `Giants`                     | San Francisco Giants       |
| `SLN`           | `STL`, `Cardinals`                        | St. Louis Cardinals        |
| `WAS`           | `WSH`, `WSN`, `Nationals`                 | Washington Nationals       |
| `MIA`           | `FLO`, `FLA`, `Marlins`                   | Miami Marlins              |
| `TBA`           | `TB`, `TBR`, `Rays`                       | Tampa Bay Rays             |
| `ANA`           | `LAA`, `Angels`                           | Los Angeles Angels         |
| `MIN`           | `MIN`, `Twins`                            | Minnesota Twins            |
| `CLE`           | `CLE`, `CLV`, `Guardians`                 | Cleveland Guardians        |
| `PHI`           | `PHI`, `Phillies`                         | Philadelphia Phillies      |
| `ATL`           | `ATL`, `Braves`                           | Atlanta Braves             |
| `HOU`           | `HOU`, `Astros`                           | Houston Astros             |
| `SEA`           | `SEA`, `Mariners`                         | Seattle Mariners           |
| `OAK`           | `OAK`, `Athletics`                        | Oakland/Sacramento Athletics |
| `TEX`           | `TEX`, `Rangers`                          | Texas Rangers              |
| `BOS`           | `BOS`, `Red Sox`                          | Boston Red Sox             |
| `BAL`           | `BAL`, `Orioles`                          | Baltimore Orioles          |
| `TOR`           | `TOR`, `Blue Jays`                        | Toronto Blue Jays          |
| `DET`           | `DET`, `Tigers`                           | Detroit Tigers             |
| `MIL`           | `MIL`, `Brewers`                          | Milwaukee Brewers          |
| `COL`           | `COL`, `Rockies`                          | Colorado Rockies           |
| `ARI`           | `ARI`, `ARZ`, `Diamondbacks`              | Arizona Diamondbacks       |
| `PIT`           | `PIT`, `Pirates`                          | Pittsburgh Pirates         |
| `CIN`           | `CIN`, `Reds`                             | Cincinnati Reds            |

### 4.3 Normalization Implementation

Normalization must produce Retrosheet 3-letter code as canonical output.
Script reference: `scripts/normalize_team_codes.py` (to be created at P38A runtime)

---

## 5. Date Matching Strategy

| Rule                                    | Detail                                                                   |
|-----------------------------------------|--------------------------------------------------------------------------|
| Primary join key                        | `game_date + home_team (normalized) + away_team (normalized)`           |
| Date format                             | Both sides must be ISO 8601 (YYYY-MM-DD) before join                    |
| Retrosheet source                       | `game_date` in `mlb_2024_game_identity.csv`                             |
| Odds source                             | `game_date` in research odds CSV                                         |
| Tolerance                               | ZERO — no fuzzy date matching; exact date match only                    |
| Timezone                                | All dates treated as local game date (no timezone conversion)            |

---

## 6. Doubleheader Handling

| Case                                    | Retrosheet                        | Odds Side                          |
|-----------------------------------------|-----------------------------------|------------------------------------|
| Single game                             | `game_id` ends in `-0`            | `game_id_optional` = `...-0`       |
| First game of doubleheader              | `game_id` ends in `-1`            | Expect separate odds row           |
| Second game of doubleheader             | `game_id` ends in `-2`            | Expect separate odds row           |
| Odds source has no game number          | Use `retrosheet_game_id_optional` if available; else flag as AMBIGUOUS |

**Required doubleheader rule:**
- If `(game_date, home_team, away_team)` resolves to 2 Retrosheet games (DH), and odds source has only 1 row, flag as `JOIN_AMBIGUOUS_DOUBLEHEADER`.
- Do NOT silently assign; require explicit resolution.

---

## 7. Postponed / Suspended Game Handling

| Case                                    | Action                                                               |
|-----------------------------------------|----------------------------------------------------------------------|
| Game in Retrosheet but no odds row      | Flag as `RETROSHEET_ONLY_NO_ODDS` (normal for postponed games)      |
| Game in odds but not in Retrosheet      | Flag as `ODDS_ONLY_NO_RETROSHEET` (investigate — possible postpone/cancel) |
| Resumed game on different date          | Use RESUMED game date for join; add note in `notes` field            |

---

## 8. Home/Away Mismatch Detection

Mismatch can occur if odds source reverses home/away convention.

| Check                                   | Method                                                               |
|-----------------------------------------|----------------------------------------------------------------------|
| Primary check                           | Join on `game_date + home_team + away_team` — if no match, try swap |
| If swap matches                         | Flag as `HOME_AWAY_MISMATCH_DETECTED` and log; user must confirm    |
| If neither matches                      | Flag as `NO_MATCH`                                                   |
| Never silently swap                     | Log all swaps; do not correct silently                              |

---

## 9. Unmatched Game Report Schema

For every unmatched game, produce a record:

```json
{
  "game_date": "2024-04-01",
  "home_team": "BOS",
  "away_team": "NYA",
  "reason_code": "RETROSHEET_ONLY_NO_ODDS",
  "retrosheet_game_id": "BOS-20240401-0",
  "odds_game_id": null,
  "notes": "Game not found in odds source"
}
```

**Reason Codes:**
| Code                            | Meaning                                              |
|---------------------------------|------------------------------------------------------|
| `RETROSHEET_ONLY_NO_ODDS`       | Game in Retrosheet, absent from odds CSV             |
| `ODDS_ONLY_NO_RETROSHEET`       | Row in odds CSV, no matching Retrosheet game         |
| `NO_MATCH`                      | No match found (neither H/A orientation)             |
| `JOIN_AMBIGUOUS_DOUBLEHEADER`   | Doubleheader ambiguity — game number unclear         |
| `HOME_AWAY_MISMATCH_DETECTED`   | Match found only after swapping H/A — review required |
| `TEAM_CODE_UNRESOLVABLE`        | Odds team code cannot be mapped to Retrosheet code   |

---

## 10. Duplicate Odds Report Schema

For every duplicate odds row detected, produce a record:

```json
{
  "game_date": "2024-04-01",
  "home_team": "BOS",
  "away_team": "NYA",
  "market": "moneyline",
  "source_name": "kaggle_us_sports_master",
  "duplicate_count": 2,
  "reason_code": "DUPLICATE_ROW",
  "action": "keep_first_reject_rest"
}
```

---

## 11. No-Leakage Checks

| Check                            | Rule                                                                       |
|----------------------------------|----------------------------------------------------------------------------|
| Odds columns must be pregame     | closing_home_moneyline, closing_away_moneyline must not contain game outcomes |
| Forbidden fields                 | Per P36 schema: y_true, final_score, home_score, away_score, winner, outcome, result, run_diff, total_runs, game_result |
| Date check                       | Odds rows must have `game_date` matching the game, not a postgame date     |
| Snapshot time check (optional)   | If `snapshot_time_optional` present, must be < first pitch time            |
| Closing line validity            | A "closing" line should not contain outcome information                    |

---

## 12. Fixture-Only Smoke Test

```
smoke_id: FIXTURE_JOIN_SMOKE_P1
purpose: Validate join logic with zero real data dependency
input:
  - retrosheet_side: data/research_odds/fixtures/join_test_retrosheet_10games.csv
    (10 games, hand-crafted, matching GL2024 format exactly)
  - odds_side: data/research_odds/fixtures/join_test_odds_10games.csv
    (10 games, synthetic odds, matching manual import contract schema)
expected_results:
  - 10 games joined successfully
  - join_rate = 100%
  - 0 unmatched games
  - 0 duplicates
  - no leakage check failures
  - all output flags: is_research=True, is_synthetic=True
pass_criteria: All 5 assertions pass
file_to_create: scripts/test_research_odds_join_fixture.py
```

---

## 13. Small Date-Range Sample Join Test (When Odds Data Available)

```
smoke_id: SAMPLE_JOIN_P1
purpose: Validate join on real (non-synthetic) research odds sample
precondition: At least 1 ACCEPTABLE_FOR_RESEARCH odds source provisioned
input:
  - retrosheet_side: data/mlb_2024/processed/mlb_2024_game_identity.csv
    (filter to April 1-30, 2024: ~180 games)
  - odds_side: data/research_odds/local_only/{source_name}_2024_april.csv
    (April 2024 sample from provisioned source)
expected_results:
  - join_rate >= 80% (target >= 90%)
  - unmatched game report produced
  - no HOME_AWAY_MISMATCH_DETECTED (or all mismatches documented)
  - team normalization applied and logged
  - output flags: is_research=True, is_synthetic=False
pass_criteria: join_rate >= 80% AND unmatched report produced
```

---

## 14. Criteria for JOIN_CERT_RESEARCH_ODDS_READY

All of the following must be true:

- [ ] Fixture-only smoke test passes (`FIXTURE_JOIN_SMOKE_P1`)
- [ ] Real odds sample exists (ACCEPTABLE_FOR_RESEARCH source provisioned)
- [ ] Sample date-range join completed for April 2024 (≥ 180 games)
- [ ] Join rate ≥ 90% for the sample range
- [ ] Unmatched game report produced for the sample
- [ ] Duplicate odds report produced
- [ ] Team normalization table validated (all 30 MLB teams covered)
- [ ] No leakage check failures
- [ ] Deterministic output confirmed (run twice, diff is empty)
- [ ] All output artifacts have `is_research: true`
- [ ] `join_certification_report_research_odds_YYYYMMDD.md` produced

**Current status:** NOT READY — pending odds source provisioning

---

## 15. Candidate Integration Points (Existing Scripts)

| Script                                       | Relevance                                | Integration Action         |
|----------------------------------------------|------------------------------------------|-----------------------------|
| `wbc_backend/recommendation/p32_retrosheet_game_log_parser.py` | Provides game identity CSV | Use as-is for Retrosheet side |
| `wbc_backend/recommendation/p36_manual_odds_import_validator.py` | Validates odds schema | Extend for research_only scope |
| `data/mlb_2024/processed/mlb_2024_game_identity.csv` | Retrosheet game identity (2024) | Use as join anchor |

**Recommended new script:** `scripts/research_odds_join_certifier.py`
- Input: Retrosheet CSV path, odds CSV path, output report path
- Output: JSON join report + markdown certification report
- No external deps; no network calls
- Must be fully deterministic
- Must pass fixture-only smoke before any real data run

---

## 16. .gitignore Additions Needed

```gitignore
# Research odds — local only, never commit raw data
data/research_odds/local_only/
# Retrosheet raw files — too large for git, not needed in CI
data/mlb_2024/raw/
```

---

**Acceptance Marker:** RESEARCH_ODDS_JOIN_CERTIFICATION_PLAN_20260513_READY
