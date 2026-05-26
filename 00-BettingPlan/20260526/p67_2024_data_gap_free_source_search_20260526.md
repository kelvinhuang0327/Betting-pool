# P67 — 2024 Data Gap Free-Source Search (PATH_B)
**Date**: 2026-05-26 | **Classification**: `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`

## Summary

P67 executed PATH_B from the P61 resolution plan: exhaustive free public-source search for 2024 MLB closing-line moneyline odds data (13 search queries across Kaggle, GitHub, OddsPortal, SBRO, aussportsbetting.com).

**Result: No directly downloadable free CSV source found for 2024 MLB closing-line moneyline. One partial source identified.**

## Source Findings

| Source | Result |
|---|---|
| SportsbookReviewsOnline.com (SBRO) | Archive frozen at 2021. No 2024 data. `SOURCE_NO_2024` |
| **OddsPortal.com** | **2024 data confirmed visible** (WS Game 1 LAD 1.71/NYY 2.37). No bulk CSV. Requires scraping. `SOURCE_PARTIAL_NEEDS_SCHEMA_PROBE` |
| Kaggle — all MLB 2024 searches (27 datasets) | All game stats / Statcast. No betting odds. `SOURCE_NO_MONEYLINE` |
| Kaggle — synthetic dataset (pratyushpuri) | Faker-generated synthetic data. `SOURCE_UNUSABLE` |
| GitHub — all MLB odds searches | 0 repos found; 0 repos with mlb-betting topic. `SOURCE_UNUSABLE` |
| aussportsbetting.com | HTTP 403 blocked. ToS unknown. `SOURCE_LICENSE_UNCLEAR` |

## Governance

All invariants preserved:
- `paper_only=True`, `diagnostic_only=True`, `promotion_freeze=True`
- `paid_api_called=False`, `live_api_calls=0`, `tsl_crawler_called=False`
- `runtime_recommendation_logic_changed=False`, `real_bet_allowed=False`
- P45 Platt constants unchanged (A=0.435432, B=0.245464)
- 2024 data gap: **UNRESOLVED** (UNRESOLVED_PENDING_P68_SCRAPE_FEASIBILITY)

## Test Results

- P67 tests: **33/33 PASS**
- Cumulative regression (P43+P59–P67): **260/260 PASS**
- Forbidden scan: **0 violations**

## Next Step

**P68 — OddsPortal Scraping Feasibility Probe**
- Review OddsPortal ToS Section 5 (automated extraction restrictions)
- Probe pagination structure for one month of 2024 MLB results
- Confirm field alignment with target schema (Date, Away, Home, Away ML, Home ML)
- Classify as: `P68_FEASIBLE_PROCEED` | `P68_TOS_BLOCKED` | `P68_TECHNICALLY_INFEASIBLE`
- Fallback if blocked: P61 PATH_A (CEO decision for The Odds API paid pull, ~$30–50 one-time)
