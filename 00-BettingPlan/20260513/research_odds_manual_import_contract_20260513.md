# Research Odds Manual Import Contract — 2026-05-13

**Status:** RESEARCH-ONLY CONTRACT  
**Author:** CTO Agent  
**Date:** 2026-05-13  
**Scope:** Research-grade odds import path — non-production, non-wagering  
**Acceptance Marker:** RESEARCH_ODDS_MANUAL_IMPORT_CONTRACT_20260513_READY

---

## ⚠️ Mandatory Non-Goals

Before reading this contract, confirm the following prohibitions:

- ❌ 不得直接升級為 production odds
- ❌ 不得寫入正式 betting ledger
- ❌ 不得把 local-only raw odds commit（除非 license 明確允許且使用者核准）
- ❌ 不得跳過 license risk matrix（見 `research_odds_license_risk_matrix_20260513.md`）
- ❌ 不得使用 research odds 做 edge claim 或 wagering decisions

---

## 1. Purpose

This contract defines the canonical CSV schema for importing research-grade odds
data into the P38A replay pipeline. It applies to:
- User-provided manual odds exports
- License-approved community datasets
- Hand-curated fixture data for testing

It does NOT apply to any production or live-wagering path.

---

## 2. File Storage Policy

| Scope                  | Path                                            | Git Status             |
|------------------------|-------------------------------------------------|------------------------|
| Local research data    | `data/research_odds/local_only/`                | `.gitignore` — NOT committed |
| Fixture samples (CI)   | `data/research_odds/fixtures/`                  | ✅ Can be committed if license allows |
| Import contract docs   | `00-BettingPlan/20260513/`                      | ✅ Committed            |
| Example/template CSV   | `data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv` | ✅ Committed (no real data) |

---

## 3. CSV Column Schema (Canonical)

All columns are required unless marked `_optional`.

| Column Name                           | Type    | Required | Example Value                       | Notes                                                                 |
|---------------------------------------|---------|----------|-------------------------------------|-----------------------------------------------------------------------|
| `season`                              | integer | ✅        | `2024`                              | 4-digit year of the MLB season                                        |
| `game_date`                           | string  | ✅        | `2024-04-01`                        | ISO 8601 (YYYY-MM-DD). MUST be parseable.                             |
| `game_id_optional`                    | string  | ❌        | `2024-04-01_NYA_BOS_0`             | Internal identifier if available                                      |
| `retrosheet_game_id_optional`         | string  | ❌        | `BOS202404010`                      | Retrosheet game_id format if available; aids join                     |
| `home_team`                           | string  | ✅        | `BOS`                               | Retrosheet 3-letter code preferred; see normalization table            |
| `away_team`                           | string  | ✅        | `NYA`                               | Retrosheet 3-letter code preferred                                     |
| `sportsbook_optional`                 | string  | ❌        | `Pinnacle`                          | Name of sportsbook if known                                           |
| `market`                              | string  | ✅        | `moneyline`                         | Must be in approved market taxonomy (see Section 5)                   |
| `home_moneyline`                      | integer | ✅ *      | `-130`                              | American odds. If only closing is available, put in closing columns.  |
| `away_moneyline`                      | integer | ✅ *      | `+112`                              | American odds.                                                        |
| `draw_moneyline_optional`             | integer | ❌        | `NULL`                              | For 3-way markets only (not applicable for MLB)                       |
| `opening_home_moneyline_optional`     | integer | ❌        | `-120`                              | Opening line if available                                             |
| `opening_away_moneyline_optional`     | integer | ❌        | `+102`                              | Opening line if available                                             |
| `closing_home_moneyline`              | integer | ✅ **     | `-130`                              | Closing line — at least one closing pair required                     |
| `closing_away_moneyline`              | integer | ✅ **     | `+112`                              | Closing line — at least one closing pair required                     |
| `snapshot_time_optional`              | string  | ❌        | `2024-04-01T17:30:00Z`             | ISO 8601 UTC snapshot time if available                               |
| `source_name`                         | string  | ✅        | `user_manual_export`               | Identifies the data origin (see approved values in Section 6)         |
| `source_license_status`               | string  | ✅        | `user_owned`                        | Must be one of the approved license status values (Section 7)         |
| `import_scope`                        | string  | ✅        | `research_only`                     | Must be in approved scope taxonomy (Section 8)                        |
| `imported_by`                         | string  | ✅        | `cto_agent_20260513`               | Who imported the data                                                 |
| `imported_at`                         | string  | ✅        | `2026-05-13T00:00:00Z`             | ISO 8601 UTC import timestamp                                         |
| `notes`                               | string  | ❌        | `Manually exported from DraftKings` | Free text; capture source quirks, adjustments, caveats                |

`*` = home_moneyline + away_moneyline: at minimum, closing pair required. Generic pair only needed if no opening/closing distinction is available.

`**` = closing_home_moneyline + closing_away_moneyline: at least ONE complete closing pair required per row. Rows without any closing line are rejected.

---

## 4. Validation Rules

### 4.1 Field-Level Rules

| Rule ID | Field                         | Rule                                                                      |
|---------|-------------------------------|---------------------------------------------------------------------------|
| R01     | `game_date`                   | MUST be parseable as ISO 8601 date. Reject if not parseable.             |
| R02     | `home_team`                   | MUST be non-empty. MUST match Retrosheet 3-letter code OR approved alias. |
| R03     | `away_team`                   | MUST be non-empty. Same as R02.                                           |
| R04     | `home_team != away_team`      | REJECT rows where home_team equals away_team.                            |
| R05     | `market`                      | MUST be in approved market taxonomy (Section 5).                          |
| R06     | `closing_home_moneyline`      | MUST have at least one of (closing_home_moneyline, closing_away_moneyline) present. |
| R07     | `closing_home_moneyline` type | American odds: integer, never zero. Range: -9999 to +9999. Not NULL if present. |
| R08     | `closing_away_moneyline` type | Same as R07.                                                              |
| R09     | American odds conversion      | MUST be convertible to implied probability: P = 100/(odds+100) for positive; P = -odds/(-odds+100) for negative. Reject if conversion produces P ≤ 0 or P ≥ 1. |
| R10     | `source_license_status`       | MUST NOT be `UNKNOWN_FOR_COMMITTED_DATA` for any committed fixture.       |
| R11     | `import_scope`                | MUST be one of: `research_only`, `local_only`, `approved_fixture`.        |

### 4.2 Row-Level Rules

| Rule ID | Rule                                                                              |
|---------|-----------------------------------------------------------------------------------|
| R20     | No exact duplicate rows on (game_date, home_team, away_team, market, source_name). |
| R21     | `season` MUST be consistent with year in `game_date`. (e.g., season=2024 → game_date starts with 2024) |
| R22     | `game_date` MUST be a valid MLB season date for the given `season`. No Jan–Feb dates for MLB regular season. |
| R23     | If `retrosheet_game_id_optional` is provided, it MUST match the expected format: `{TEAM}{YYYYMMDD}{N}` (e.g., `BOS202404010`). |

### 4.3 File-Level Rules

| Rule ID | Rule                                                                              |
|---------|-----------------------------------------------------------------------------------|
| R30     | File encoding: UTF-8.                                                             |
| R31     | Field separator: comma (,). Quote character: double quote ("). CSV per RFC 4180. |
| R32     | First row MUST be header matching exact column names above.                       |
| R33     | File name format: `odds_research_{source_name}_{season}_{YYYYMMDD}.csv`         |
| R34     | File path: `data/research_odds/local_only/` (for real data) or `data/research_odds/fixtures/` (for CI fixtures). |

---

## 5. Market Taxonomy

| Market Value        | Description                          | Allowed   |
|---------------------|--------------------------------------|-----------|
| `moneyline`         | Standard win/loss moneyline          | ✅ YES     |
| `run_line`          | Run line (spread equivalent)         | ✅ YES (future P8) |
| `total_over_under`  | Total runs over/under                | ✅ YES (future P8) |
| `first_5_moneyline` | First 5 innings moneyline            | ✅ YES (future P7) |
| `series`            | Series betting                       | ❌ REJECT (not supported) |
| `prop`              | Player/game props                    | ❌ REJECT (not supported) |

---

## 6. Approved `source_name` Values

| Value                    | Description                                      |
|--------------------------|--------------------------------------------------|
| `user_manual_export`     | Manually captured by user from sportsbook UI    |
| `kaggle_us_sports_master` | Kaggle oliviersportsdata dataset (CC BY-NC 4.0) |
| `aussportsbetting`       | AusSportsBetting.com (if terms confirmed OK)    |
| `pinnacle_historical`    | Pinnacle historical API (if access obtained)    |
| `research_fixture`       | Synthetic fixture generated for testing         |
| `other_approved`         | Other source — must describe in `notes` field  |

---

## 7. Approved `source_license_status` Values

| Value                          | Meaning                                                         |
|--------------------------------|-----------------------------------------------------------------|
| `user_owned`                   | Data is user-owned; no third-party license                     |
| `cc_by_nc_4`                   | Creative Commons CC BY-NC 4.0                                  |
| `personal_noncommercial`       | Personal/non-commercial use permitted per source terms         |
| `synthetic_no_license`         | Synthetic data; no license applies                             |
| `license_confirmed_research`   | Source confirmed research-use permitted; see notes for details |
| `UNKNOWN_FOR_COMMITTED_DATA`   | ❌ BLOCKED — DO NOT USE for any committed file                 |
| `manual_review_pending`        | License under review — DO NOT commit this file                 |

---

## 8. Approved `import_scope` Values

| Value               | Meaning                                                           |
|---------------------|-------------------------------------------------------------------|
| `research_only`     | Research feasibility only. No production use. No wagering.       |
| `local_only`        | Local machine only. Do NOT commit. Do NOT share.                 |
| `approved_fixture`  | Approved for CI fixture use. May be committed (small sample).    |

---

## 9. Example Template Row (Not Real Data)

```
season,game_date,game_id_optional,retrosheet_game_id_optional,home_team,away_team,sportsbook_optional,market,home_moneyline,away_moneyline,draw_moneyline_optional,opening_home_moneyline_optional,opening_away_moneyline_optional,closing_home_moneyline,closing_away_moneyline,snapshot_time_optional,source_name,source_license_status,import_scope,imported_by,imported_at,notes
2024,2024-04-01,,,BOS,NYA,Pinnacle,moneyline,-130,+112,,,-120,+102,-130,+112,2024-04-01T17:30:00Z,user_manual_export,user_owned,research_only,cto_agent_20260513,2026-05-13T00:00:00Z,Example row — NOT real odds
```

---

## 10. Schema Versioning

| Version  | Date       | Changes                                     |
|----------|------------|---------------------------------------------|
| v1.0     | 2026-05-13 | Initial definition — P1 investigation       |

---

## 11. Validation Script Reference

Future validation script should be placed at:
`scripts/validate_research_odds_import.py`

Expected behavior:
- Read CSV from file path argument
- Apply all R01-R34 rules
- Output JSON report: `{valid: bool, errors: [...], row_count: int}`
- Exit 0 on pass, exit 1 on any hard failure
- Do NOT connect to any external service
- Do NOT write to any production path

---

**Acceptance Marker:** RESEARCH_ODDS_MANUAL_IMPORT_CONTRACT_20260513_READY
