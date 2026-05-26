# P61 — 2024 Closing-Line Data Gap Resolution Plan

**Date:** 2026-05-26
**Phase:** P61 (CEO P1 priority — data-sourcing evaluation, paper_only=true)
**Trigger:** P60 completed → CEO P1 elevated from deferred → active

## Governance Flags
- paper_only: `True`
- diagnostic_only: `True`
- promotion_freeze: `True`
- kelly_deploy_allowed: `False`
- live_api_calls: `0`
- tsl_crawler_modified: `False`
- champion_strategy_changed: `False`
- production_usage_proposed: `False`
- runtime_recommendation_logic_changed: `False`
- data_download_attempted: `False`
- paid_api_called: `False`

## Background

- **P43** final classification: `P43_BLOCKED_BY_DATA_GAP`
  - 2024 quality rows: 2158 — zero closing-line odds available
  - 2025 joined rows: 1426 — EDGE_CONFIRMED on 2025 only
- **P60** classification: `P60_EDGE_STABLE_ACROSS_MONTHS`
  - Cross-month stability: `EDGE_STABLE_ACROSS_MONTHS`
  - Average edge across months: `None`

**Gap**: `data/mlb_2025/mlb_odds_2024_real.csv` with columns:
  - `Date`
  - `Away`
  - `Home`
  - `Away Score`
  - `Home Score`
  - `Away ML`
  - `Home ML`
  - Required rows: ~~2430 (full 2024 MLB regular season)
  - Date range: 2024-03-20 to 2024-09-29

## Data Source Evaluation

| Source | Provides ML Odds | Effort | Resolution | Priority |
|--------|-----------------|--------|------------|----------|
| Retrosheet Game Logs | ❌ | LOW — download and parse, but cannot provide odds columns | SCORES_ONLY | LOW |
| Baseball Reference Play-by-Play / Game Log | ❌ | MEDIUM — scraping required, ToS restriction risk | SCORES_ONLY | LOW |
| The Odds API (Historical Odds) | ✅ | MEDIUM — requires API key, paid plan, conversion script | FULL — closest match to required schema | HIGH |
| Sportsbook Review (SBR) Historical Odds | ✅ | HIGH — JavaScript-rendered pages require headless browser; fragile scraping | FULL if successfully scraped | MEDIUM |
| Kaggle / GitHub Archived MLB Odds Datasets | ❌ | LOW-MEDIUM — search, download, validate, convert | PARTIAL_TO_FULL depending on dataset quality | MEDIUM |
| Internal TSL Odds History (2025 Season Only) | ✅ | N/A | NONE | NONE |

### Source Details

#### Retrosheet Game Logs
- **URL/Reference**: https://www.retrosheet.org/gamelogs/
- **Provides moneyline**: False
- **2024 availability**: Available (typically released by Nov following season)
- **Schema compatibility**: PARTIAL — provides Date, Away, Home, Away Score, Home Score but NO Away ML / Home ML
- **Effort**: LOW — download and parse, but cannot provide odds columns
- **Access**: Free, public download
- ⚠️ **Blocker**: Does not contain moneyline odds. Cannot resolve the data gap alone.

#### Baseball Reference Play-by-Play / Game Log
- **URL/Reference**: https://www.baseball-reference.com/
- **Provides moneyline**: False
- **2024 availability**: Available
- **Schema compatibility**: PARTIAL — scores and starters but NO moneyline odds
- **Effort**: MEDIUM — scraping required, ToS restriction risk
- **Access**: Free web access; structured download requires scraping
- ⚠️ **Blocker**: No moneyline odds data. ToS restricts bulk scraping.

#### The Odds API (Historical Odds)
- **URL/Reference**: https://the-odds-api.com/historical-odds-sites-api/
- **Provides moneyline**: True
- **2024 availability**: Available (historical snapshots available from 2020+)
- **Schema compatibility**: HIGH — provides home/away ML in numeric form, convertible to target schema
- **Effort**: MEDIUM — requires API key, paid plan, conversion script
- **Access**: Paid subscription; historical odds endpoint
- ⚠️ **Blocker**: Paid subscription required. Governance allows no live API calls, but
- **Cost**: ~$30-100/month (Starter plan); one-time 2024 season pull feasible
- **Governance action needed**: Explicit CEO authorization for one-time paid API call

#### Sportsbook Review (SBR) Historical Odds
- **URL/Reference**: https://www.sportsbookreview.com/betting-odds/mlb-baseball/
- **Provides moneyline**: True
- **2024 availability**: Available (historical pages accessible by date)
- **Schema compatibility**: MEDIUM — moneyline available but requires HTML scraping + parsing
- **Effort**: HIGH — JavaScript-rendered pages require headless browser; fragile scraping
- **Access**: Free web access; historical data accessible via URL patterns
- ⚠️ **Blocker**: No official API. JavaScript rendering adds complexity. Brittle to site changes.
- **Governance action needed**: None (free access) but live browser/scraping counts as automated data pull

#### Kaggle / GitHub Archived MLB Odds Datasets
- **URL/Reference**: https://www.kaggle.com/search?q=mlb+odds+2024
- **Provides moneyline**: POSSIBLE — varies by dataset
- **2024 availability**: UNCERTAIN — community datasets lag by 6-18 months; 2024 season may be available
- **Schema compatibility**: VARIABLE — must validate column names against target schema
- **Effort**: LOW-MEDIUM — search, download, validate, convert
- **Access**: Free; download via Kaggle API or direct link
- ⚠️ **Blocker**: Quality and completeness not guaranteed. Provenance may be unclear.
- **Governance action needed**: None — download without live API call; offline validation required

#### Internal TSL Odds History (2025 Season Only)
- **URL/Reference**: data/tsl_odds_history.jsonl
- **Provides moneyline**: True
- **2024 availability**: NOT AVAILABLE — TSL file covers 2026 spring training only
- **Schema compatibility**: NOT APPLICABLE — 2025 season not covered
- **Effort**: N/A
- **Access**: Internal file (no live call needed for reading)
- ⚠️ **Blocker**: Zero 2024 coverage. Zero 2025 season overlap.

## Resolution Paths

### ✅ PATH_A: The Odds API (one-time historical pull)
- **Effort**: MEDIUM | **Cost**: ~$30-50 one-time
- **Data quality**: HIGH
- **Timeline**: 1-2 days after authorization
- **Governance**: Explicit CEO authorization for one-time paid API call (not live betting)
- **Rationale**: Only source confirmed to provide 2024 MLB moneyline in structured format. One-time historical pull is distinct from live odds API calls. Would unblock P43 cross-year validation and all downstream cross-year analysis.

### ✅ PATH_B: Kaggle/GitHub community dataset search
- **Effort**: LOW-MEDIUM | **Cost**: $0
- **Data quality**: VARIABLE — must validate
- **Timeline**: 0.5-1 day
- **Governance**: None — offline download, no live API
- **Rationale**: Free path worth exhausting first. If a validated 2024 MLB moneyline CSV exists on Kaggle, it would resolve the gap at zero cost. Must validate completeness (all 30 teams, full regular season) and provenance.

### ⚠️ PATH_C: Sportsbook Review scraping (headless browser)
- **Effort**: HIGH | **Cost**: $0
- **Data quality**: MEDIUM — site-dependent reliability
- **Timeline**: 3-5 days engineering
- **Governance**: Engineering authorization for automated browser session
- **Rationale**: Viable as fallback if PATH_A and PATH_B fail. High engineering cost and fragility outweigh benefit unless other paths are exhausted. JavaScript rendering adds complexity.

## Impact Analysis

**Current state**: P43=`P43_BLOCKED_BY_DATA_GAP`, P60=`P60_EDGE_STABLE_ACROSS_MONTHS`
**Blocked by**: P43 cross-year validation; 2025-only EDGE_CONFIRMED stands

**If gap resolved:**
- P43 could run cross-year bootstrap CI on 2024+2025 combined (~3856 quality rows). If 2024 Tier C shows consistent positive edge, P43 final classification upgrades from P43_BLOCKED_BY_DATA_GAP to P43_CROSS_YEAR_EDGE_CONFIRMED or similar.
- ⚠️ Risk: If 2024 Tier C shows negative or near-zero edge, the combined 2024+2025 CI may narrow or cross zero, weakening the P43 conclusion. This is scientifically correct and should be accepted as a legitimate finding.
- Downstream unlocks:
  - P43 cross-year validation
  - Stronger cross-year ECE/Brier comparison
  - More robust walk-forward calibration (P45/P46 with 2024 data)
  - 2024 Tier C temporal stability analysis (P44 equivalent)

**Recommendation**: Execute PATH_B (free Kaggle/GitHub search) immediately. If PATH_B fails within 1 day, request CEO authorization for PATH_A (The Odds API one-time historical pull). PATH_C is fallback only.

## Final P61 Classification

**P61 Classification:** `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT`

### Recommended Next Actions
1. **TODAY (0 cost)**: Search Kaggle/GitHub for `mlb 2024 odds moneyline` datasets.
   Validate any match against required schema. If found → run P43 with 2024 data.
2. **If PATH_B fails (~1 day)**: Request CEO authorization for The Odds API one-time
   historical pull (~$30-50). This is NOT a live betting API call.
3. **Do NOT** scrape SBR or Baseball Reference without engineering authorization.
4. **Do NOT** make any live API call without explicit governance authorization.

## Known Limitations
- This report evaluates sources; no data was downloaded.
- Cost estimates are approximate and subject to vendor pricing changes.
- Kaggle dataset quality is not guaranteed without inspection.
- 2024 data may show different edge characteristics than 2025 (scientifically valid risk).
- **Paper-only. No production proposal. No champion replacement.**
