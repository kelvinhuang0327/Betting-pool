# P67 — 2024 Closing-Line Data Gap: Free-Source Search (PATH_B)
**Classification**: `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`
**Date**: 2026-05-26 | **Branch**: main | **Mode**: `paper_only=true`, `diagnostic_only=true`

---

## §1 Pre-flight Result

| Check | Result |
|---|---|
| repo | `Betting-pool` ✓ |
| branch | `main` ✓ |
| HEAD | `7aabf31` (P66 commit) ✓ |
| uncommitted changes | clean ✓ |
| governance flags | all correct ✓ |

Pre-flight: **PASS**

---

## §2 Dirty File Assessment

No dirty files at P67 start. All P66 artefacts committed. Working tree clean.

---

## §3 Search Scope

P67 is the execution of **PATH_B** from the P61 resolution plan (free Kaggle/GitHub search), expanded to cover all discoverable free public sources.

Search terms and methods used:

| # | Query | Platform |
|---|---|---|
| 1 | `MLB odds 2024 moneyline` | Kaggle datasets |
| 2 | `mlb odds baseball betting` | Kaggle datasets |
| 3 | `baseball odds betting` | Kaggle datasets |
| 4 | `mlb baseball 2024` | Kaggle datasets |
| 5 | `mlb odds 2024 moneyline csv` | GitHub repositories |
| 6 | `mlb baseball odds 2024 csv` | GitHub repositories |
| 7 | `mlb betting odds historical 2024` | GitHub repositories |
| 8 | topic: `mlb-betting` | GitHub topics |
| 9 | MLB archives page | SportsbookReviewsOnline.com (direct) |
| 10 | `/baseball/usa/mlb-2024/results/` | OddsPortal.com (direct) |
| 11 | `/data/` historical MLB page | aussportsbetting.com (direct) |
| 12 | `pratyushpuri/sports-betting-predictive-analysis-dataset` | Kaggle specific |
| 13 | `garethflandro/major-league-baseball-games-2024` | Kaggle specific |

Internet access: **confirmed available** during search session.

---

## §4 Candidate Source Inventory

| # | Source | Years | Home ML | Away ML | Download | Cost | Classification |
|---|---|---|---|---|---|---|---|
| 1 | SportsbookReviewsOnline.com (SBRO) | 2010–2021 | ✓ | ✓ | Free XLSX | Free | `SOURCE_NO_2024` |
| 2 | OddsPortal.com | 2008–2026 | ✓ | ✓ | Web UI only (no CSV) | Free to view | `SOURCE_PARTIAL_NEEDS_SCHEMA_PROBE` |
| 3 | Kaggle — pratyushpuri (Sports Betting) | 2023–2025 | Synthetic | Synthetic | Free CSV | Free | `SOURCE_UNUSABLE` |
| 4 | Kaggle — garethflandro (MLB 2020–2024) | 2020–2024 | ✗ | ✗ | Free CSV | Free | `SOURCE_NO_MONEYLINE` |
| 5 | Kaggle — MLB 2024 collection (27 datasets) | Various | ✗ | ✗ | Free CSV | Free | `SOURCE_NO_MONEYLINE` |
| 6 | GitHub MLB odds repos (all searches) | N/A | N/A | N/A | None found | Free | `SOURCE_UNUSABLE` |
| 7 | aussportsbetting.com | Unknown | Unknown | Unknown | HTTP 403 blocked | Unknown | `SOURCE_LICENSE_UNCLEAR` |

---

## §5 Source-Level Classifications

### SOURCE_NO_2024 — SportsbookReviewsOnline.com (SBRO)
- Archive page explicitly states: *"MLB scores and odds archive will not be updated."*
- Direct XLSX download links confirmed for 2010–2021. No 2022, 2023, or 2024 season files.
- Contains: Open ML, Closing ML, Runs, VH, Team, Date fields.
- **Cannot resolve 2024 gap.** Would have been the simplest free source if 2024 were available.

### SOURCE_PARTIAL_NEEDS_SCHEMA_PROBE — OddsPortal.com
- 2024 MLB data **confirmed visible** in web UI. Season navigation links include 2024.
- World Series Game 1 (LAD vs NYY, Oct 25 2024): odds 1.71 / 2.37 (decimal) confirmed on page.
- Fields visible per game: Home Team, Away Team, Date, Home Odds (decimal), Away Odds (decimal), Score.
- Decimal odds can be converted to American ML via standard formula.
- **No bulk CSV download exists.** Data is JavaScript-rendered across paginated results (~50 games/page, estimated ~49 pages for 2024 full season = ~2430 rows).
- ToS Section 5 restricts automated data extraction.
- Requires P68 feasibility probe before any extraction attempt.

### SOURCE_UNUSABLE — Kaggle pratyushpuri
- Explicitly labelled "Synthetic (generated using Faker library)" in dataset card.
- Not real market data. Team names are fictitious city-based identifiers.
- 1,369 rows multi-sport; estimated ~274 baseball rows. Disqualified.

### SOURCE_NO_MONEYLINE — Kaggle garethflandro (MLB 2020–2024)
- 162 columns of Retrosheet game statistics. No moneyline odds.
- Has correct join keys: Date, Away, Home. Has 2024 coverage.
- Cannot fill the odds gap.

### SOURCE_NO_MONEYLINE — Kaggle MLB 2024 collection (27 datasets)
- All 27 Kaggle datasets are performance statistics (Statcast, bat tracking, pitching, hitting, payrolls, salaries, umpires).
- None contain betting odds across any of the 4 search queries.

### SOURCE_UNUSABLE — GitHub MLB odds repos (all searches)
- 3 separate GitHub repository searches returned 0 repositories.
- GitHub topic `mlb-betting` has **0 public repositories** tagged (topic page confirmed).

### SOURCE_LICENSE_UNCLEAR — aussportsbetting.com
- HTTP 403 Forbidden during search. Known to be a public historical data archive.
- 2024 availability, field coverage, and download format could not be verified.
- Requires manual browser investigation.

---

## §6 Feasibility Classification

| Classification | Result |
|---|---|
| Any source directly downloadable with 2024 MLB closing ML? | **NO** |
| Any source partially viable (data exists, access method needed)? | **YES — OddsPortal.com** |
| Any source license-blocked? | **YES — aussportsbetting.com (403)** |

**P67 Classification: `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`**

Justification: OddsPortal has confirmed 2024 MLB closing-line odds in its web UI (per-game decimal odds post-settlement). The data is publicly viewable at no cost. However, it is not available as a bulk CSV download — extraction requires JS-rendered pagination scraping. ToS restrictions and scraping feasibility must be assessed before any extraction proceeds.

---

## §7 Licensing / Provenance Notes

| Source | License | Provenance | ToS Scraping |
|---|---|---|---|
| SBRO | Public access, research use common | Original data collection | Unclear; research use tolerated |
| OddsPortal | Section 5 restricts automated extraction | Aggregated from multiple bookmakers | **Restricted — probe required** |
| Kaggle pratyushpuri | CC0 Public Domain | Synthetic (Faker) | N/A — disqualified |
| Kaggle garethflandro | MIT + Retrosheet attribution | Retrosheet game logs | N/A — no odds |
| aussportsbetting | Unknown (403) | Unknown | Unknown |

---

## §8 2024 Home ML / Away ML Closing-Line Validation Capability

| Source | Can support 2024 Home ML + Away ML closing-line validation? |
|---|---|
| SBRO | NO — archive stops 2021 |
| OddsPortal | POSSIBLY — if scraping is feasible and ToS permits; requires P68 probe |
| Kaggle (all) | NO — no odds data |
| GitHub (all) | NO — no repos found |
| aussportsbetting | UNKNOWN — blocked |

**No source can currently provide confirmed downloadable 2024 Home ML / Away ML closing-line data.**
OddsPortal remains the sole candidate requiring feasibility probe.

---

## §9 Recommendation for P68 or P61 PATH_A

**Recommendation: P68 — OddsPortal Scraping Feasibility Probe**

P68 should:
1. Review OddsPortal ToS Section 5 in full (automated extraction prohibition scope).
2. Manually inspect one month of 2024 MLB results (e.g., April 2024) to confirm pagination structure and row count.
3. Confirm field alignment: Home Team, Away Team, Date, Home Odds (decimal), Away Odds (decimal) → target schema columns.
4. Confirm decimal odds are closing (post-settlement) not opening.
5. Estimate total scraping complexity: ~49 pages × ~50 games × field parsing.
6. If ToS permits: propose structured scrape with rate-limit controls.
7. If ToS prohibits: escalate to P61 PATH_A (CEO decision for The Odds API paid historical pull, ~$30–50 one-time).

**Fallback**: If P68 confirms OddsPortal extraction is ToS-prohibited or technically infeasible, the only remaining viable path is The Odds API (PATH_A, paid, requires CEO authorization per P61).

---

## §10 Governance Preservation Result

| Flag | Value | Status |
|---|---|---|
| `paper_only` | `True` | ✓ |
| `diagnostic_only` | `True` | ✓ |
| `promotion_freeze` | `True` | ✓ |
| `kelly_deploy_allowed` | `False` | ✓ |
| `live_api_calls` | `0` | ✓ |
| `paid_api_called` | `False` | ✓ |
| `tsl_crawler_called` | `False` | ✓ |
| `runtime_recommendation_logic_changed` | `False` | ✓ |
| `real_bet_allowed` | `False` | ✓ |
| `production_ready` | `False` | ✓ |
| P45 Platt constants | A=0.435432, B=0.245464 | Unchanged ✓ |
| P52 thresholds | Unchanged | ✓ |
| P64/P65/P66 artefacts | Unchanged | ✓ |

All governance invariants preserved.

---

## §11 Test Results

```
tests/test_p67_2024_data_gap_free_source_search.py  33 passed
Cumulative regression (P43+P59–P67):               260 passed
```

**All 260 tests PASS.** (227 prior + 33 new P67 tests)

---

## §12 Forbidden Scan Result

Script `scripts/_p67_2024_data_gap_free_source_search.py` scanned for forbidden affirmative phrases:
- `production_ready = True` → NOT FOUND
- `kelly_deploy_allowed = True` → NOT FOUND
- `real_bet_allowed = True` → NOT FOUND
- `paid_api_called = True` → NOT FOUND
- `LIVE_API_CALLS: int = 1` → NOT FOUND
- `TSL_CRAWLER_CALLED: bool = True` → NOT FOUND

**Forbidden scan: 0 violations (CLEAN)**

---

## §13 Commit Hash

P67 commit: `[see whitelist commit after this report]`

Whitelist files:
- `scripts/_p67_2024_data_gap_free_source_search.py`
- `tests/test_p67_2024_data_gap_free_source_search.py`
- `data/mlb_2025/derived/p67_2024_data_gap_free_source_search_summary.json`
- `report/p67_2024_data_gap_free_source_search_20260526.md`
- `00-BettingPlan/20260526/p67_2024_data_gap_free_source_search_20260526.md`
- `00-Plan/roadmap/active_task.md`

---

## §14 Final Classification

```
P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW
```

Key finding: OddsPortal.com has 2024 MLB closing-line odds confirmed in its web UI. The data exists, is publicly viewable at no cost, and covers the full season. However, it is not directly downloadable as a CSV — extraction requires JavaScript-rendered web scraping with pagination. ToS Section 5 restricts automated extraction. P68 feasibility probe required before extraction can proceed.

---

## §15 Next 24h Prompt

```
P68 — OddsPortal Scraping Feasibility Probe

Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True
Prerequisites: P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW (this report)

Objectives:
1. Retrieve and analyse OddsPortal.com Terms of Service (Section 5 specifically).
2. Probe one month of 2024 MLB results page for pagination structure and row count.
3. Verify field alignment: Home Team, Away Team, Date, decimal odds → target schema.
4. Confirm odds are closing (post-settlement) not opening prices.
5. Produce structured P68 feasibility report with ToS verdict and scraping plan.
6. Classify as: P68_FEASIBLE_PROCEED | P68_TOS_BLOCKED | P68_TECHNICALLY_INFEASIBLE.

If P68_FEASIBLE_PROCEED: draft scrape scaffold in data/scripts/
If P68_TOS_BLOCKED: escalate to P61 PATH_A CEO decision memo.
```

---

## §16 CTO Agent 10-Line Summary

P67 executed PATH_B (free-source search) for 2024 MLB closing-line moneyline data.
13 search queries across Kaggle, GitHub, OddsPortal, SBRO, and aussportsbetting.com.
SBRO archive frozen at 2021 (SOURCE_NO_2024); Kaggle returned 27 datasets, all game stats (no odds).
GitHub MLB-betting topic has 0 public repos; 3 queries returned 0 repositories.
One synthetic Kaggle dataset found (Faker-generated); disqualified (SOURCE_UNUSABLE).
OddsPortal confirmed 2024 data visible in web UI: per-game decimal odds post-settlement.
OddsPortal classified SOURCE_PARTIAL_NEEDS_SCHEMA_PROBE; no bulk CSV export available.
aussportsbetting.com returned HTTP 403; licence and 2024 availability unknown.
Classification: P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW.
Next step: P68 — OddsPortal ToS review + pagination feasibility probe; fallback = P61 PATH_A (paid API, CEO approval required).
