# P69 — CEO Decision Memo: PATH_A Authorization
**Date**: 2026-05-26 | **Branch**: main | **Classification**: `P69_CEO_DECISION_MEMO_READY`

---

## Evidence Trail Verified

| Phase | Classification |
|---|---|
| P61 | `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT` |
| P67 | `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW` |
| P68 | `P68_ODDSPORTAL_BLOCKED_BY_TOS` |

2024 gap status: `UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A`

---

## Free Source PATH_B: Exhausted

| Source | Result |
|---|---|
| Kaggle datasets | No moneyline odds — game stats only |
| GitHub repositories | 0 repos with 2024 MLB odds |
| Kaggle synthetic | Fake data — unusable |
| SBRO | Archive frozen at 2021 |
| aussportsbetting | HTTP 403 blocked |
| OddsPortal | ToS 2.11 + robots.txt — legally inaccessible |

All 6 free sources exhausted. No usable 2024 MLB closing-line dataset found via free PATH_B.

---

## PATH_A: The Odds API

| Field | Value |
|---|---|
| Source | `https://the-odds-api.com` |
| Pull type | One-time historical (NOT live) |
| Data | 2024 MLB regular season moneyline |
| Estimated cost | $30–50 one-time |
| Data quality | HIGH |
| Schema match | HIGH (~50-line conversion script) |
| Timeline after auth | 1–2 days |
| Called in P69 | **NO** — memo-only |

Required fields (9): `game_date`, `home_team`, `away_team`, `home_ml`, `away_ml`, `bookmaker`, `odds_timestamp`, `closing_indicator`, `source_trace`

---

## Governance

`paper_only=True` | `diagnostic_only=True` | `promotion_freeze=True` | `paid_api_called=False`
`the_odds_api_called_in_p69=False` | `live_api_calls=0` | `bulk_scraping_performed=False`
`real_bet_allowed=False` | `production_ready=False`
Platt constants: A=0.435432, B=0.245464 (locked)

---

## CEO Decision Options

### ✅ APPROVE
**Copy-paste phrase:**
```
YES authorize P61 PATH_A The Odds API historical 2024 MLB moneyline pull for paper-only validation
```
**Next task**: P70 — The Odds API Historical Pull (authorized, one-time, paper-only)

---

### ❌ REJECT
**Copy-paste phrase:**
```
NO reject P61 PATH_A and freeze 2024 closing-line scope
```
**Next task**: P70 — 2024 Scope Freeze (accept P43_BLOCKED_BY_DATA_GAP as permanent)

---

### ⏸ DEFER
**Copy-paste phrase:**
```
DEFER P61 PATH_A pending more information
```
**Next task**: P70 — CEO Information Request (define open questions, re-present later)

---

## Test Results

| Suite | Count | Result |
|---|---|---|
| P69 tests | 42 | ✅ PASS |
| Cumulative regression (P43+P59–P69) | 338 | ✅ PASS |

Forbidden scan: **0 violations**

---

## Allowed / Prohibited Use

**Allowed (if approved):** paper simulation, diagnostic validation, research-internal only
**Prohibited (always):** live betting, Kelly staking, production output, champion replacement, commercial redistribution
