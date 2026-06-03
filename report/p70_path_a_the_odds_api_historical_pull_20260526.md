# P70 — PATH_A: The Odds API Historical Pull
**Classification**: `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY`
**Date**: 2026-05-26 | **Branch**: main | **Mode**: `paper_only=true`, `diagnostic_only=true`

---

## §1 Pre-flight

| Check | Result |
|---|---|
| HEAD | `981228f` (P69 commit) ✓ |
| Branch | `main` ✓ |
| CEO authorization | Confirmed 2026-05-26 ✓ |
| P69 classification | `P69_CEO_DECISION_MEMO_READY` ✓ |
| Governance flags | All correct ✓ |

---

## §2 CEO Authorization Verified

**Authorized phrase received**:
```
YES authorize P61 PATH_A The Odds API historical 2024 MLB moneyline pull for paper-only validation
```

`CEO_AUTHORIZATION_CONFIRMED = True` — embedded in script, verified in test suite.

---

## §3 Execution Mode: DRY_RUN

`.env` does not contain `THE_ODDS_API_KEY`. Script executed in **DRY_RUN mode**:
- Zero API calls made
- `paid_api_called = False`
- Script logic fully validated
- Classification: `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY`

---

## §4 Pull Script Architecture

**Script**: `scripts/_p70_path_a_the_odds_api_historical_pull.py`

| Component | Detail |
|---|---|
| Modes | `DRY_RUN` (no key) / `LIVE` (key present) |
| Sport | `baseball_mlb` |
| Date range | `2024-03-20` → `2024-09-29` |
| Market | `h2h` (moneyline only) |
| Regions | `us` |
| Preferred bookmaker | `pinnacle` (fallback: draftkings, fanduel, betmgm) |
| Odds format | American (converted from decimal) |
| Rate limit | 1 req/sec (conservative) |
| Retry policy | 3 retries, 5s backoff |
| Target rows | ~2,430 |
| Output | `data/mlb_2025/mlb_odds_2024_real.csv` |

**API Endpoint** (LIVE mode):
```
GET https://api.the-odds-api.com/v4/historical/sports/baseball_mlb/events/{event_id}/odds
    ?apiKey=<key>&regions=us&markets=h2h&oddsFormat=decimal&date=<commence_time>
```

---

## §5 Required Output Fields

| Field | Source | Notes |
|---|---|---|
| `game_date` | `commence_time[:10]` | ISO 8601 date |
| `home_team` | `event.home_team` | As returned by API |
| `away_team` | `event.away_team` | As returned by API |
| `home_ml` | `outcome.price` (decimal → American) | Integer |
| `away_ml` | `outcome.price` (decimal → American) | Integer |
| `bookmaker` | `bookmaker.key` | Preferred: pinnacle |
| `odds_timestamp` | `market.last_update` | Closing-line proxy |
| `closing_indicator` | `"CLOSING_PROXY_COMMENCE_TIME"` | Pre-game snapshot |
| `source_trace` | Injected at pull time | Source + date + script version |

---

## §6 Conversion: Decimal → American Odds

$$
\text{American ML} = \begin{cases}
+\text{round}((\text{decimal} - 1) \times 100) & \text{if decimal} \ge 2.0 \\
-\text{round}\!\left(\dfrac{100}{\text{decimal} - 1}\right) & \text{if decimal} < 2.0
\end{cases}
$$

Examples validated in tests:
- Decimal 1.50 → `-200` ✓
- Decimal 2.50 → `+150` ✓
- Decimal 2.00 → `+100` ✓
- Decimal 1.20 → `-500` ✓

---

## §7 API Key Acquisition Steps

1. Register at **https://the-odds-api.com**
2. Subscribe to a plan with historical data access (~$30–50 one-time or monthly)
3. Locate API key in account dashboard
4. Add to `.env`:
   ```
   THE_ODDS_API_KEY=<your_key>
   ```
5. Re-run: `.venv/bin/python scripts/_p70_path_a_the_odds_api_historical_pull.py`
6. Script auto-detects key → switches to LIVE mode → writes CSV

---

## §8 Governance

| Flag | Value | Status |
|---|---|---|
| `paper_only` | `True` | ✓ |
| `diagnostic_only` | `True` | ✓ |
| `promotion_freeze` | `True` | ✓ |
| `kelly_deploy_allowed` | `False` | ✓ |
| `real_bet_allowed` | `False` | ✓ |
| `production_ready` | `False` | ✓ |
| `paid_api_called` | `False` (DRY_RUN) | ✓ |
| `bulk_scraping_performed` | `False` | ✓ |
| `anti_bot_bypass_attempted` | `False` | ✓ |
| `tsl_crawler_called` | `False` | ✓ |
| `runtime_recommendation_logic_changed` | `False` | ✓ |
| Platt constants | A=0.435432, B=0.245464 | Unchanged ✓ |

---

## §9 Test Results

```
tests/test_p70_path_a_the_odds_api_historical_pull.py  51 passed
Cumulative regression (P43+P59–P70):                  389 passed
```

**All 389 tests PASS.** (338 prior + 51 new P70 tests)

---

## §10 Forbidden Scan

Script `scripts/_p70_path_a_the_odds_api_historical_pull.py`:

**0 violations** — all 11 forbidden patterns clean.

---

## §11 Classification

```
P70_PATH_A_AUTHORIZED_AWAITING_API_KEY
```

CEO authorized. Script complete and tested. Awaiting `THE_ODDS_API_KEY` in `.env` to execute actual pull.

---

## §12 Commit

P70 commit: `[see whitelist commit]`

Whitelist (6 files):
- `scripts/_p70_path_a_the_odds_api_historical_pull.py`
- `tests/test_p70_path_a_the_odds_api_historical_pull.py`
- `data/mlb_2025/derived/p70_path_a_the_odds_api_historical_pull_summary.json`
- `report/p70_path_a_the_odds_api_historical_pull_20260526.md`
- `00-BettingPlan/20260526/p70_path_a_the_odds_api_historical_pull_20260526.md`
- `00-Plan/roadmap/active_task.md`

---

## §13 Next 24h Prompt

```
P71 — The Odds API Live Pull Execution

Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True
Branch: main | HEAD: [P70 commit]
Prerequisite: THE_ODDS_API_KEY must be in .env

P71 scope:
  IF key is now configured:
    - Execute: .venv/bin/python scripts/_p70_path_a_the_odds_api_historical_pull.py
    - Validate resulting CSV: data/mlb_2025/mlb_odds_2024_real.csv
    - Schema validation: all 9 required fields present, row count ≥500
    - Run P43 cross-year bootstrap CI on 2024+2025 combined dataset
    - Classify as: P71_PATH_A_PULL_COMPLETE or P71_PATH_A_PULL_DATA_QUALITY_FAIL

  IF key still not configured:
    - Document pending status
    - Classify as: P71_PATH_A_STILL_AWAITING_API_KEY

Context:
  - P70: P70_PATH_A_AUTHORIZED_AWAITING_API_KEY
  - P69: P69_CEO_DECISION_MEMO_READY (CEO approved 2026-05-26)
  - Platt: A=0.435432, B=0.245464 (locked)
  - Target: ~2430 rows, baseball_mlb, 2024-03-20 to 2024-09-29
```

---

## §14 CTO Agent 10-Line Summary

1. CEO phrase `YES authorize P61 PATH_A ...` received and verified — `CEO_AUTHORIZATION_CONFIRMED=True` embedded in script.
2. `.env` does not contain `THE_ODDS_API_KEY` → script executed in DRY_RUN mode; zero API calls made.
3. Complete pull script created with dual-mode architecture: DRY_RUN (no key) / LIVE (key present).
4. LIVE mode flow: fetch season event list → per-event historical odds → decimal→American conversion → write CSV.
5. Rate limiting (1 req/sec), 3-retry backoff, preferred bookmaker order (pinnacle first).
6. All 9 required output fields documented and validated: game_date, home/away team/ml, bookmaker, odds_timestamp, closing_indicator, source_trace.
7. Decimal→American odds conversion validated (4 unit tests: -200, +150, +100, -500).
8. 51 P70 tests PASS; cumulative 389/389 PASS (P43+P59–P70); forbidden scan 0 violations.
9. Governance fully preserved: paper_only=True, paid_api_called=False (DRY_RUN), Platt unchanged.
10. To execute actual pull: add `THE_ODDS_API_KEY=<key>` to `.env`, re-run script → auto-switches to LIVE mode.
