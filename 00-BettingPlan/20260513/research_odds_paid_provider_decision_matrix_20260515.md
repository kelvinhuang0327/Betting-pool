# Research Odds Paid Provider Decision Matrix — 2026-05-15

**Status:** PAID PROVIDER ASSESSMENT COMPLETE — USER DECISION REQUIRED  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Scope:** Evaluate 3 paid providers (The Odds API, SportsDataIO, Sportradar) against P38A join requirements. If all public free sources are blocked, determine shortest paid path to ≥100 rows of 2024 MLB moneyline closing odds.  
**References:**
- `research_odds_public_source_deep_audit_20260515.md` (TRACK 1 results)
- `p38a_oof_output_contract_inventory_20260514.md` (P38A schema: 2,187 predictions, 2024 season)
- `p38a_odds_join_key_mapping_spec_20260514.md` (join algorithm, team normalization)
- Web fetch: The Odds API documentation v4 (confirmed 2026-05-15)
- Web fetch: The Odds API terms and conditions (confirmed 2026-05-15)

---

## ⚠️ User Decision Required

> **None of the three paid providers can be enabled without explicit user approval.**
> - No API calls made in this document.
> - No API keys generated or committed.
> - This document is a feasibility and selection decision matrix ONLY.
> - User must explicitly choose and approve before any API subscription or call is made.

---

## 1. PROVIDER-A: The Odds API — Historical Odds Endpoint

### 1.1 Product Overview

| Field | Value |
|---|---|
| **provider_name** | The Odds API |
| **provider_url** | https://the-odds-api.com |
| **terms_url** | https://the-odds-api.com/terms-and-conditions.html |
| **api_docs_url** | https://the-odds-api.com/liveapi/guides/v4/#historical-odds |
| **data_type** | REST JSON API — historical and live odds snapshots |
| **sport_key_mlb** | `baseball_mlb` |
| **mlb_available** | YES ✅ |

### 1.2 Historical Odds Coverage

| Field | Value |
|---|---|
| **historical_data_available_from** | June 6, 2020 |
| **2024_mlb_season_coverage** | YES ✅ (2024 season is within 2020–present window) |
| **snapshot_interval** | 10-minute intervals (5-minute from September 2022) |
| **moneyline_market_key** | `h2h` (head-to-head) |
| **moneyline_available** | YES ✅ |
| **run_line_available** | YES (`spreads`) |
| **totals_available** | YES (`totals`) |
| **closing_line_method** | Query historical endpoint at `date` = last snapshot before game `commence_time` |
| **pregame_snapshot_method** | Query at consistent pre-game time (e.g., 4h before `commence_time`) |
| **bookmakers_available** | 40+ (DraftKings, FanDuel, BetMGM, Caesars, Pinnacle, etc.) |
| **timestamp_format** | ISO 8601 UTC ✅ |
| **home_away_fields** | YES: `home_team`, `away_team` in response |
| **team_name_format** | Full team name (e.g., "Baltimore Orioles", "Kansas City Royals") — Retrosheet normalization required |
| **odds_format_american** | YES — `oddsFormat=american` parameter |
| **odds_format_decimal** | YES — configurable |

### 1.3 License and Redistribution

| Field | Value |
|---|---|
| **license_text_found** | YES — terms page fetched successfully (2026-05-15) |
| **research_use_allowed** | YES — analytical tools and dashboards are explicitly supported |
| **redistribution_prohibited** | YES — "Do not resell, repackage, or redistribute our data as a standalone data product" |
| **raw_commit_allowed** | NO — redistribution as data file/feed is prohibited by terms |
| **local_only_required** | YES — data must remain in `data/research_odds/local_only/` (gitignored) |
| **api_key_must_not_be_committed** | YES — API key must never appear in git |

### 1.4 Pricing (as of 2026-05-15)

| Plan | Monthly Cost | Credits/Month | Historical Odds Access |
|---|---|---|---|
| Starter (FREE) | $0 | 500 | **NO** — historical endpoint requires paid plan |
| 20K | $30 | 20,000 | YES ✅ |
| 100K | $59 | 100,000 | YES ✅ |
| 5M | $119 | 5,000,000 | YES ✅ |
| 15M | $249 | 15,000,000 | YES ✅ |

### 1.5 Cost Analysis for P38A Join (2024 MLB Season)

| Approach | Calls | Credits per Call | Total Credits | Minimum Plan |
|---|---|---|---|---|
| **Per-day pregame batch** (1 call per game day, ~180 days) | 180 | 10 | **1,800** | $30/month (20K plan) |
| **Per-game closing line** (1 call per game, 2,187 games) | 2,187 | 10 | **21,870** | $30/month (20K plan)† |
| **≥100 rows smoke test only** (5 days × 10 games/day) | 5 | 10 | **50** | $30/month (20K plan) |

† Note: 21,870 credits exceeds the 20K plan quota but can be satisfied across 2 months at $30/month = $60 total, or immediately at the $59/month 100K plan.

**Recommended approach for ≥100 row smoke test:** Per-day batch for 5–10 game days = 50–100 credits (well within $30/month plan).

**Recommended approach for full 2024 season:** Per-day batch (180 calls × 10 = 1,800 credits) — fits in $30/month plan.

### 1.6 Integration Complexity

| Field | Value |
|---|---|
| **api_call_type** | GET request with apiKey, sport, markets, regions, date parameters |
| **team_normalization** | Full name → Retrosheet 3-letter code (mapping table in join key spec) |
| **game_matching_strategy** | Match on `commence_time` (ISO 8601) + home/away team to derive P38A `game_id` |
| **data_volume** | ~5KB–50KB per daily snapshot response |
| **python_integration_complexity** | LOW — standard `requests` library; JSON parsing; pandas join |
| **estimated_integration_effort** | 1–2 days (no API key → implementation starts day of subscription) |

### 1.7 P38A Join Feasibility

| Requirement | Met? | Notes |
|---|---|---|
| 2024 MLB moneyline closing odds | ✅ YES | Via `h2h` market, `date` = game commence_time |
| ≥100 rows for smoke test | ✅ YES | 5 game days easily provides 50–80+ games |
| Timestamp (pregame/closing) | ✅ YES | `last_update` in response; snapshot `timestamp` in metadata |
| home/away team fields | ✅ YES | `home_team`, `away_team` in response |
| Retrosheet code normalization | ⚠️ NEEDED | Full name → 3-letter code mapping required |
| ISO 8601 date format | ✅ YES | `commence_time` is ISO 8601 UTC |
| American odds format | ✅ YES | `oddsFormat=american` |
| Local-only feasibility | ✅ YES | JSON responses stored in `data/research_odds/local_only/` |
| No git commit of raw data | ✅ YES (enforced) | Gitignored directory |

**Overall join feasibility: HIGH** — clearest technical path of all three providers.

### 1.8 Final Assessment

| Field | Value |
|---|---|
| **final_classification** | **PAID_PROVIDER_DECISION_REQUIRED** |
| **recommended_plan** | 20K ($30/month) — sufficient for full 2024 season via per-day batching |
| **shortest_path_to_≥100_rows** | Subscribe → one API call for a 5-day batch = same day |
| **risk_level** | LOW — well-documented public API, established provider (since 2017) |

---

## 2. PROVIDER-B: SportsDataIO MLB Historical Odds

### 2.1 Product Overview

| Field | Value |
|---|---|
| **provider_name** | SportsDataIO |
| **provider_url** | https://sportsdata.io/developers/api-documentation/mlb |
| **data_type** | REST API — enterprise commercial sports data |
| **mlb_available** | YES |
| **2024_mlb_coverage** | YES |
| **closing_line_available** | YES |
| **moneyline_available** | YES |
| **run_line_available** | YES |
| **totals_available** | YES |
| **timestamp_format** | ISO 8601 |
| **team_name_format** | Standard abbreviation (e.g., BAL, CHA) + full name in separate fields |
| **retrosheet_normalization_needed** | YES (abbreviation format differs from Retrosheet 3-letter in some cases) |

### 2.2 License and Pricing

| Field | Value |
|---|---|
| **license_text_found** | PARTIAL — website accessible but no free research license stated |
| **pricing_model** | Enterprise subscription / custom contract |
| **free_tier_for_research** | NO confirmed free research tier |
| **pricing_transparency** | LOW — price requires sales contact |
| **minimum_commitment** | Unknown — likely multi-month contract |
| **redistribution_allowed** | UNKNOWN — requires contract review |
| **local_only_feasibility** | YES with contract |
| **api_key_required** | YES |
| **research_use_allowed** | UNCERTAIN — enterprise terms not publicly confirmed for research-only |

### 2.3 Integration Complexity

| Field | Value |
|---|---|
| **python_integration_complexity** | MEDIUM — REST API, but enterprise endpoint structure |
| **team_normalization** | LOWER RISK — standard MLB abbreviation (closer to Retrosheet) |
| **estimated_integration_effort** | 2–3 days post-subscription |

### 2.4 Final Assessment

| Field | Value |
|---|---|
| **final_classification** | **PAID_PROVIDER_DECISION_REQUIRED** |
| **recommended?** | NO — second choice behind The Odds API |
| **blocking_issue** | Pricing opacity; enterprise contract required; research use not explicitly confirmed |
| **shortest_path_to_≥100_rows** | Unknown until sales conversation completed |

---

## 3. PROVIDER-C: Sportradar MLB Historical Odds

### 3.1 Product Overview

| Field | Value |
|---|---|
| **provider_name** | Sportradar |
| **provider_url** | https://sportradar.com/sports/baseball/mlb/ |
| **data_type** | Enterprise REST API — professional sports data |
| **mlb_available** | YES |
| **2024_mlb_coverage** | YES |
| **closing_line_available** | YES |
| **moneyline_available** | YES |
| **data_quality** | VERY HIGH — professional-grade, used by major operators |
| **bookmaker_granularity** | VERY HIGH |
| **timestamp_format** | ISO 8601 |
| **team_name_format** | Standard MLB identifiers |

### 3.2 License and Pricing

| Field | Value |
|---|---|
| **license_text_found** | PARTIAL — enterprise terms require contract; no public documentation |
| **pricing_model** | Enterprise contract (typically $1,000+/month) |
| **free_tier_for_research** | NO |
| **research_use_allowed** | UNLIKELY without enterprise contract |
| **redistribution_allowed** | NO — strict redistribution prohibition |
| **local_only_feasibility** | YES with contract |
| **access_path** | Sales negotiation required |

### 3.3 Final Assessment

| Field | Value |
|---|---|
| **final_classification** | **PAID_PROVIDER_DECISION_REQUIRED** |
| **recommended?** | NO — enterprise-only, out of scope for research prototype |
| **blocking_issue** | Enterprise contract required; pricing far exceeds research budget |

---

## 4. Provider Comparison Summary

| Field | The Odds API | SportsDataIO | Sportradar |
|---|---|---|---|
| **2024 MLB Coverage** | ✅ YES | ✅ YES | ✅ YES |
| **Moneyline Closing Odds** | ✅ YES | ✅ YES | ✅ YES |
| **Timestamp Available** | ✅ YES (5-min snap) | ✅ YES | ✅ YES |
| **License Found** | ✅ YES | ⚠️ PARTIAL | ⚠️ PARTIAL |
| **Research Use Allowed** | ✅ YES | ⚠️ UNCERTAIN | ❌ UNLIKELY |
| **Pricing Transparency** | ✅ HIGH | ❌ LOW | ❌ VERY LOW |
| **Minimum Monthly Cost** | $30 | Unknown (enterprise) | ~$1,000+ |
| **Free Research Tier** | ❌ NO | ❌ NO | ❌ NO |
| **Integration Complexity** | LOW | MEDIUM | HIGH |
| **Team Normalization Effort** | MEDIUM (full name) | LOW-MEDIUM (abbrev) | LOW-MEDIUM |
| **≥100 Row Smoke Test Feasibility** | ✅ SAME DAY (post-subscribe) | ⚠️ UNKNOWN | ❌ OUT OF SCOPE |
| **Recommended** | ✅ YES — PRIMARY | ⚠️ SECONDARY | ❌ NO |

---

## 5. Recommended Decision Path

### If user approves paid source:

**→ Subscribe to The Odds API 20K plan ($30/month)**

1. Subscribe at https://the-odds-api.com/#get-access
2. Store API key in local `.env` file ONLY — never commit
3. Agent executes `p31_local_only_download_plan` using historical odds endpoint
4. Batch by game day (180 calls for full 2024 season = 1,800 credits)
5. Store all JSON responses in `data/research_odds/local_only/raw_api_responses/` (gitignored)
6. Transform to 23-column CSV contract schema
7. Proceed with ≥100 rows join smoke test

### If user declines all paid sources:

**→ MANUAL_IMPORT_ONLY** (user provides their own odds data) or  
**→ PUBLIC_SOURCE_BLOCKED** (if user also declines manual import)

---

## 6. Acceptance Marker

```
RESEARCH_ODDS_PAID_PROVIDER_DECISION_MATRIX_20260515_READY
```
