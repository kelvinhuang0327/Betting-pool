# Research Odds Candidate Inventory v2 — 2026-05-14

**Status:** RESEARCH FEASIBILITY — EXPANDED CANDIDATE INVESTIGATION  
**Author:** CTO Agent  
**Date:** 2026-05-14  
**Scope:** MLB 2024 moneyline pregame/closing odds — public/free-source expansion  
**Version:** v2 (extends v1 from 2026-05-13)  
**Acceptance Marker:** RESEARCH_ODDS_CANDIDATE_INVENTORY_V2_20260514_READY

---

## ⚠️ Mandatory Constraints

> - **No raw odds data downloaded.** This is a source landscape review only.
> - **No scrapers written.** Automation risk is assessed but not implemented.
> - **No raw data committed.** Fixture-only CSVs may be committed if license explicitly permits.
> - **Conditions unclear → MANUAL_APPROVAL_REQUIRED** (not assumed acceptable).
> - **Paid-only sources → PAID_PROVIDER_DECISION_REQUIRED** (not free-source ready).
> - This document does NOT constitute approval to import any odds data.

---

## 1. v1 Summary (Sources from 2026-05-13 Inventory)

| Candidate | v1 Classification | 2024 Coverage |
|---|---|---|
| CANDIDATE-01: Retrosheet game logs | ACCEPTABLE_FOR_RESEARCH (join anchor only) | ✅ YES (no odds) |
| CANDIDATE-02: SportsbookReviewsOnline (SBRO) | REJECTED_FOR_NO_2024_COVERAGE | ❌ Archive frozen at 2021 |
| CANDIDATE-03: Kaggle oliviersportsdata | ACCEPTABLE_FOR_LOCAL_RESEARCH (CC BY-NC 4.0) | Partial — verify 2024 |
| CANDIDATE-04: AusSportsBetting.com | MANUAL_APPROVAL_REQUIRED | Partial — verify 2024 |
| CANDIDATE-05: GitHub community repos | MANUAL_APPROVAL_REQUIRED (per-repo) | Unknown |
| CANDIDATE-06: Manual-Import CSV (user) | ACCEPTABLE_FOR_LOCAL_RESEARCH | User-controlled |
| CANDIDATE-07: Synthetic Fixture Data | ACCEPTABLE_FOR_FIXTURE_ONLY | N/A (synthetic) |

---

## 2. v2 Expanded Candidate Inventory

---

### CANDIDATE-08: Kaggle — US Sports Betting Historical (Multiple Datasets)

| Field | Value |
|---|---|
| **candidate_name** | Kaggle US Sports Historical Odds — aggregated search |
| **source_url** | `https://www.kaggle.com/search?q=mlb+odds+moneyline` |
| **source_type** | Community dataset aggregator (Kaggle) |
| **available seasons** | Varies by dataset — typically 2010–2023; 2024 coverage inconsistent |
| **2024 MLB coverage** | ⚠️ UNCERTAIN — most datasets last updated 2022–2023 |
| **market coverage — moneyline** | ✅ Typical for MLB betting datasets |
| **market coverage — run line** | Partial — varies by dataset |
| **market coverage — totals** | Partial — varies by dataset |
| **closing line availability** | ✅ Common in larger datasets |
| **opening line availability** | Partial — not universal |
| **timestamp availability** | ❌ RARE — most lack snapshot timestamps |
| **sportsbook granularity** | ⚠️ VARIES — some have multi-book, some aggregate only |
| **home/away fields** | ✅ Usually present |
| **team naming format** | Full name or common abbreviation — NOT Retrosheet format |
| **date format** | ISO or US format — varies |
| **odds format** | American or decimal — varies by dataset |
| **historical access method** | Direct CSV download after login |
| **license / terms summary** | Each dataset has its own license. Common: CC BY 4.0, CC BY-NC 4.0, unknown/unspecified |
| **research-only suitability** | ✅ YES if CC BY or CC BY-NC confirmed; ❌ if unspecified |
| **redistribution risk** | Medium — must check per dataset |
| **automation / scraping risk** | ✅ LOW — CSV download only |
| **local-only feasibility** | ✅ YES — small files, no server requirement |
| **join feasibility vs P38A output** | Medium — team normalization required (no Retrosheet codes) |
| **notes** | Must evaluate each specific Kaggle dataset individually. Do not treat "Kaggle" as a single source. Top candidates: `oliviersportsdata/us-sports-master-dataset`, `tobijegede/mlb-historic-odds`. Each requires separate license review. |
| **final classification** | **MANUAL_APPROVAL_REQUIRED** (per-dataset) |

---

### CANDIDATE-09: GitHub — Public MLB Odds CSV Repositories

| Field | Value |
|---|---|
| **candidate_name** | GitHub topic: mlb-odds, sports-betting-odds (CSV repos) |
| **source_url** | `https://github.com/topics/mlb-odds`, `https://github.com/topics/sports-betting` |
| **source_type** | Open-source / community CSV repositories |
| **available seasons** | Varies — often 2010–2022; 2024 coverage rare |
| **2024 MLB coverage** | ⚠️ LOW PROBABILITY — most repos inactive or 2023-capped |
| **market coverage — moneyline** | Varies — some have only totals or spreads |
| **market coverage — run line** | Partial |
| **market coverage — totals** | Partial |
| **closing line availability** | ⚠️ INCONSISTENT — many only have opening |
| **opening line availability** | More common |
| **timestamp availability** | ❌ RARE |
| **sportsbook granularity** | ❌ Often single-source aggregated |
| **home/away fields** | ✅ Usually present |
| **team naming format** | Full name, city name, or common abbreviation — not standardized |
| **date format** | Varies (MM/DD/YYYY, YYYY-MM-DD, YYYYMMDD) |
| **odds format** | Decimal or American — mixed |
| **historical access method** | Clone or download ZIP |
| **license / terms summary** | MIT, Apache 2.0, CC0 common; many have NO license (default copyright reserved) |
| **research-only suitability** | ⚠️ RISKY if no explicit license |
| **redistribution risk** | High if no license specified |
| **automation / scraping risk** | ✅ LOW — static file download |
| **local-only feasibility** | ✅ YES |
| **join feasibility vs P38A output** | Low-Medium — team normalization always needed |
| **notes** | Notable repos: `jimkueh/baseball-reference-scraper` (no odds), `Ulam-1/mlb-betting-model`. Must check each repo's license. Repos with no LICENSE file = DEFAULT COPYRIGHT = do NOT use for research commits. |
| **final classification** | **MANUAL_APPROVAL_REQUIRED** (per-repo license check required) |

---

### CANDIDATE-10: SportsbookReview (SBRO) Historical — API / Premium Access

| Field | Value |
|---|---|
| **candidate_name** | SBR / SportsbookReview Premium Historical Data |
| **source_url** | `https://www.sportsbookreview.com/betting-odds/` |
| **source_type** | Commercial sportsbook review / odds aggregator |
| **available seasons** | 2010–2024 on website; downloadable archive unclear |
| **2024 MLB coverage** | ✅ YES — current season covered on-site |
| **market coverage — moneyline** | ✅ YES |
| **market coverage — run line** | ✅ YES |
| **market coverage — totals** | ✅ YES |
| **closing line availability** | ✅ YES (line moves visible) |
| **opening line availability** | ✅ YES |
| **timestamp availability** | ✅ YES (line movement timestamps) |
| **sportsbook granularity** | ✅ HIGH — 10+ sportsbooks |
| **home/away fields** | ✅ YES |
| **team naming format** | Common abbreviations (NYY, BOS, LAD) |
| **date format** | US format on site (MM/DD/YYYY) |
| **odds format** | American |
| **historical access method** | Web interface only; no public bulk download API; scraping required for bulk access |
| **license / terms summary** | Commercial website; Terms of Service prohibit scraping. No bulk download API. |
| **research-only suitability** | ❌ SCRAPING PROHIBITED by ToS |
| **redistribution risk** | HIGH — commercial data |
| **automation / scraping risk** | ❌ HIGH — ToS violation |
| **local-only feasibility** | ❌ — web-only, no offline download path |
| **join feasibility vs P38A output** | N/A — blocked by scraping prohibition |
| **notes** | The frozen 2010–2021 CSV archive (SBRO) was CANDIDATE-02 in v1. Premium web access does have 2024 but bulk access is prohibited. This candidate covers the premium/web path — distinct from the old frozen archive. |
| **final classification** | **REJECTED_FOR_LICENSE_RISK** (scraping prohibited by ToS) |

---

### CANDIDATE-11: The Odds API — Historical Odds Endpoint (Paid Tier)

| Field | Value |
|---|---|
| **candidate_name** | The Odds API — Historical Odds (paid) |
| **source_url** | `https://the-odds-api.com/liveapi/guides/v4/#historical-odds` |
| **source_type** | Paid API — REST JSON |
| **available seasons** | 2019–present (varies by league) |
| **2024 MLB coverage** | ✅ YES — explicitly listed |
| **market coverage — moneyline** | ✅ YES (h2h market) |
| **market coverage — run line** | ✅ YES (spreads) |
| **market coverage — totals** | ✅ YES |
| **closing line availability** | ✅ YES (snapshot by timestamp) |
| **opening line availability** | ✅ YES (earliest snapshot) |
| **timestamp availability** | ✅ YES — timestamp per snapshot request |
| **sportsbook granularity** | ✅ HIGH — 40+ bookmakers selectable |
| **home/away fields** | ✅ YES |
| **team naming format** | Full team name (e.g., "Baltimore Orioles") — requires normalization |
| **date format** | ISO 8601 UTC |
| **odds format** | American, decimal, or fractional — configurable |
| **historical access method** | REST API call with API key; paid tier required for historical |
| **license / terms summary** | Commercial subscription; terms allow personal/research use on paid tier. Redistribution prohibited. |
| **research-only suitability** | ✅ YES — if paid subscription obtained by user; local research use permitted per terms |
| **redistribution risk** | HIGH — no redistribution allowed; local-only required |
| **automation / scraping risk** | ✅ LOW — official API (not scraping) |
| **local-only feasibility** | ✅ YES — API response stored locally, not committed |
| **join feasibility vs P38A output** | HIGH — team normalization needed (full name → Retrosheet code) |
| **notes** | This is the highest-quality paid option. Free tier does NOT include historical odds. Paid plan costs $79/month (Developer) as of 2026. The user must approve subscription. API key must NOT be committed. |
| **final classification** | **PAID_PROVIDER_DECISION_REQUIRED** — requires user subscription approval |

---

### CANDIDATE-12: SportsDataIO (formerly STATS/Sportradar partner)

| Field | Value |
|---|---|
| **candidate_name** | SportsDataIO MLB Historical Odds |
| **source_url** | `https://sportsdata.io/developers/api-documentation/mlb` |
| **source_type** | Paid commercial sports data API |
| **available seasons** | 2012–present |
| **2024 MLB coverage** | ✅ YES |
| **market coverage — moneyline** | ✅ YES |
| **market coverage — run line** | ✅ YES |
| **market coverage — totals** | ✅ YES |
| **closing line availability** | ✅ YES |
| **opening line availability** | ✅ YES |
| **timestamp availability** | ✅ YES |
| **sportsbook granularity** | ✅ HIGH |
| **home/away fields** | ✅ YES |
| **team naming format** | Standard abbreviation + full name; separate fields |
| **date format** | ISO 8601 |
| **odds format** | American and decimal available |
| **historical access method** | REST API (paid) |
| **license / terms summary** | Enterprise licensing; no free tier for historical odds |
| **research-only suitability** | ⚠️ Unknown for research — terms require commercial contract |
| **redistribution risk** | HIGH — enterprise data |
| **automation / scraping risk** | ✅ LOW — official API |
| **local-only feasibility** | ✅ with contract |
| **join feasibility vs P38A output** | HIGH — standard abbreviation maps cleanly |
| **notes** | Enterprise pricing. No free research tier confirmed. Would require vendor approval. |
| **final classification** | **PAID_PROVIDER_DECISION_REQUIRED** |

---

### CANDIDATE-13: Sportradar Historical Odds

| Field | Value |
|---|---|
| **candidate_name** | Sportradar MLB Historical Odds API |
| **source_url** | `https://sportradar.com/sports/baseball/mlb/` |
| **source_type** | Commercial enterprise sports data provider |
| **available seasons** | Extensive historical archive |
| **2024 MLB coverage** | ✅ YES |
| **market coverage — moneyline** | ✅ YES |
| **market coverage — run line** | ✅ YES |
| **market coverage — totals** | ✅ YES |
| **closing line availability** | ✅ YES |
| **opening line availability** | ✅ YES |
| **timestamp availability** | ✅ YES |
| **sportsbook granularity** | ✅ VERY HIGH |
| **home/away fields** | ✅ YES |
| **team naming format** | Standard MLB team identifiers |
| **date format** | ISO 8601 |
| **odds format** | Multiple formats |
| **historical access method** | REST API (paid enterprise contract) |
| **license / terms summary** | Enterprise contract required; strict redistribution prohibition |
| **research-only suitability** | ❌ Requires enterprise contract; no free research path |
| **redistribution risk** | VERY HIGH |
| **automation / scraping risk** | ✅ LOW — official API |
| **local-only feasibility** | ✅ with contract |
| **join feasibility vs P38A output** | HIGH — professional data quality |
| **notes** | Premium tier product. Not accessible without enterprise contract. |
| **final classification** | **PAID_PROVIDER_DECISION_REQUIRED** |

---

### CANDIDATE-14: OddsPortal — Historical MLB Odds Archive

| Field | Value |
|---|---|
| **candidate_name** | OddsPortal Historical MLB Odds |
| **source_url** | `https://www.oddsportal.com/baseball/usa/mlb/results/` |
| **source_type** | Commercial odds aggregator (web archive) |
| **available seasons** | 2007–present |
| **2024 MLB coverage** | ✅ YES — web-accessible |
| **market coverage — moneyline** | ✅ YES (listed as "1X2" for baseball, plus moneyline) |
| **market coverage — run line** | Partial |
| **market coverage — totals** | Partial |
| **closing line availability** | ✅ YES |
| **opening line availability** | ✅ YES |
| **timestamp availability** | ❌ NO standard bulk timestamp export |
| **sportsbook granularity** | ✅ HIGH — multiple bookmakers |
| **home/away fields** | ✅ YES |
| **team naming format** | Full team name |
| **date format** | DD/MM/YYYY on site |
| **odds format** | Decimal on site |
| **historical access method** | Web interface only; scraping required for bulk; no public download API |
| **license / terms summary** | Terms of Service prohibit automated access / scraping |
| **research-only suitability** | ❌ Scraping prohibited by ToS |
| **redistribution risk** | HIGH — commercial content |
| **automation / scraping risk** | ❌ HIGH — ToS violation |
| **local-only feasibility** | ❌ Not feasible without scraping |
| **join feasibility vs P38A output** | N/A — blocked |
| **notes** | OddsPortal is useful for manual spot-checks but not bulk research extraction. |
| **final classification** | **REJECTED_FOR_LICENSE_RISK** (scraping prohibited) |

---

### CANDIDATE-15: Manual-Import CSV (User-Provided) — Re-affirmed v2 Primary Path

| Field | Value |
|---|---|
| **candidate_name** | Manual Import CSV — User-Owned Data |
| **source_url** | N/A — user provides file |
| **source_type** | User-manual export or hand-curation |
| **available seasons** | Whatever user provides |
| **2024 MLB coverage** | ✅ User-controlled |
| **market coverage — moneyline** | ✅ User-controlled |
| **market coverage — run line** | Optional (future P8) |
| **market coverage — totals** | Optional (future P8) |
| **closing line availability** | ✅ User-provided |
| **opening line availability** | Optional |
| **timestamp availability** | Optional (snapshot_time_optional column) |
| **sportsbook granularity** | Single or multi — user choice |
| **home/away fields** | ✅ Required by contract |
| **team naming format** | Must map to Retrosheet 3-letter code (contract rule) |
| **date format** | ISO 8601 YYYY-MM-DD (contract rule) |
| **odds format** | American (contract rule) |
| **historical access method** | User places file in `data/research_odds/local_only/` |
| **license / terms summary** | User-owned or user-verified; `source_license_status` = `user_owned` or `personal_noncommercial` |
| **research-only suitability** | ✅ ALWAYS — user controls terms |
| **redistribution risk** | User-managed; not committed unless fixture-only |
| **automation / scraping risk** | ✅ ZERO — manual import |
| **local-only feasibility** | ✅ YES — canonical path for non-redistributable data |
| **join feasibility vs P38A output** | ✅ HIGH — contract schema designed for P38A join |
| **notes** | This is the safest and most flexible path. Contract schema at `00-BettingPlan/20260513/research_odds_manual_import_contract_20260513.md`. File goes to `data/research_odds/local_only/` (gitignored). |
| **final classification** | **ACCEPTABLE_FOR_LOCAL_RESEARCH** |

---

### CANDIDATE-16: Fixture-Only Fallback (Synthetic / In-Repo)

| Field | Value |
|---|---|
| **candidate_name** | Fixture-Only Fallback — Synthetic Dummy Data |
| **source_url** | N/A — generated in-repo |
| **source_type** | Synthetic / template fixture |
| **available seasons** | 2024 (game IDs abstracted from Retrosheet, but odds = dummy) |
| **2024 MLB coverage** | ✅ Structural coverage only — odds values are dummy |
| **market coverage — moneyline** | ✅ Structural (dummy values) |
| **closing line availability** | ✅ Structural only |
| **opening line availability** | Optional |
| **timestamp availability** | Optional |
| **sportsbook granularity** | research_fixture (no real sportsbook) |
| **home/away fields** | ✅ YES |
| **team naming format** | Retrosheet 3-letter code (required) |
| **date format** | ISO 8601 YYYY-MM-DD |
| **odds format** | American (dummy values) |
| **historical access method** | In-repo fixture CSV in `data/research_odds/fixtures/` |
| **license / terms summary** | `synthetic_no_license` — no third-party license applies |
| **research-only suitability** | ✅ YES — fully safe |
| **redistribution risk** | ✅ ZERO — synthetic |
| **automation / scraping risk** | ✅ ZERO |
| **local-only feasibility** | ✅ YES — can be committed |
| **join feasibility vs P38A output** | ✅ HIGH — purpose-built for join smoke test |
| **notes** | Source of TRACK 4 join smoke test fixture. Game IDs and teams may use real values abstracted from P38A output as long as odds values are clearly dummy. |
| **final classification** | **ACCEPTABLE_FOR_FIXTURE_ONLY** |

---

## 3. Classification Summary Table

| # | Candidate | 2024 Coverage | Final Classification |
|---|---|---|---|
| 01 | Retrosheet game logs | ✅ (no odds) | ACCEPTABLE_FOR_RESEARCH (join anchor) |
| 02 | SBRO frozen archive | ❌ (frozen 2021) | REJECTED_FOR_NO_2024_COVERAGE |
| 03 | Kaggle oliviersportsdata | ⚠️ Partial | MANUAL_APPROVAL_REQUIRED |
| 04 | AusSportsBetting.com | ⚠️ Partial | MANUAL_APPROVAL_REQUIRED |
| 05 | GitHub community repos | ❓ Unknown | MANUAL_APPROVAL_REQUIRED (per-repo) |
| 06 | Manual-Import CSV | ✅ User-controlled | ACCEPTABLE_FOR_LOCAL_RESEARCH |
| 07 | Synthetic Fixture | ✅ Structural only | ACCEPTABLE_FOR_FIXTURE_ONLY |
| 08 | Kaggle (expanded search) | ⚠️ Uncertain | MANUAL_APPROVAL_REQUIRED (per-dataset) |
| 09 | GitHub CSV repos (expanded) | ⚠️ Low probability | MANUAL_APPROVAL_REQUIRED (per-repo) |
| 10 | SBRO premium web | ✅ web-only | REJECTED_FOR_LICENSE_RISK (scraping) |
| 11 | The Odds API (historical) | ✅ | PAID_PROVIDER_DECISION_REQUIRED |
| 12 | SportsDataIO | ✅ | PAID_PROVIDER_DECISION_REQUIRED |
| 13 | Sportradar | ✅ | PAID_PROVIDER_DECISION_REQUIRED |
| 14 | OddsPortal | ✅ web-only | REJECTED_FOR_LICENSE_RISK (scraping) |
| 15 | Manual-Import (v2 affirmed) | ✅ User-controlled | ACCEPTABLE_FOR_LOCAL_RESEARCH |
| 16 | Fixture-Only Fallback (v2 affirmed) | Structural | ACCEPTABLE_FOR_FIXTURE_ONLY |

---

## 4. Decision Guidance

### 4.1 Immediate next action (zero external dependency)

→ **CANDIDATE-16 (Fixture-Only)** + **CANDIDATE-15 (Manual-Import)** are the two paths that can proceed NOW without any external approval.

### 4.2 Pending user decisions

| Action | Prerequisite |
|---|---|
| Enable The Odds API historical | User approves paid subscription |
| Enable SportsDataIO | User approves enterprise contract |
| Unblock Kaggle datasets | Per-dataset license review (CC BY-NC 4.0 check) |
| Unblock GitHub repos | Per-repo LICENSE file audit |
| Unblock AusSportsBetting | Manual review of current ToS |

### 4.3 Permanently blocked (no path forward without ToS breach)

- SBRO premium web interface (scraping prohibition)
- OddsPortal (scraping prohibition)

---

## 5. Acceptance Marker

```
RESEARCH_ODDS_CANDIDATE_INVENTORY_V2_20260514_READY
```
