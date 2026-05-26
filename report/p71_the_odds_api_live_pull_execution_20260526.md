# P71 — The Odds API Live Pull Execution
## Awaiting-Key Closure Report
**Date:** 2026-05-26  
**Classification:** `P71_PATH_A_STILL_AWAITING_API_KEY`  
**Mode:** AWAITING_KEY  
**Branch:** `main` | **Head at P70:** `549cf29`

---

## 1. Pre-Flight

| Check | Result |
|---|---|
| Repo canonical | ✅ PASS |
| Branch | `main` |
| HEAD (P70 commit) | `549cf29` |
| Python | 3.13.8 |
| pytest | 9.0.3 |
| P70 script DRY_RUN | ✅ `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY` |
| THE_ODDS_API_KEY | `KEY_LINE_MISSING` |

---

## 2. Dirty File Assessment

Runtime/daemon files modified since P70 commit (non-blocking — all excluded from commit):

- `data/learning_state.json` — daemon learning state
- `data/tsl_odds_snapshot.json`, `data/tsl_odds_history.jsonl` — crawler output
- `runtime/` — PID files, daemon status
- `logs/` — daemon logs
- `outputs/` — paper portfolio tracker

None of these are whitelist files. P71 commit stages exactly 6 whitelist files.

---

## 3. P70 Context Verification

```
P70 classification: P70_PATH_A_AUTHORIZED_AWAITING_API_KEY
P70 mode: DRY_RUN
P70 api_key_configured: false
P70 paid_api_called: false
P70 rows_written: 0
P70 ceo_authorization_confirmed: true
P70 CEO phrase: "YES authorize P61 PATH_A The Odds API historical 2024 MLB moneyline pull for paper-only validation"
P70 pull_config: baseball_mlb | h2h | us | pinnacle | 2024-03-20→2024-09-29 | ~2430 rows est.
```

P70 dry-run re-confirmed stable on 2026-05-26 immediately before P71.

---

## 4. API Key Status

```
detection method: check env var THE_ODDS_API_KEY, then .env file
result: API_KEY_MISSING
live_api_calls: 0
paid_api_called: False
```

No API call was made. No external network request was performed.

---

## 5. Awaiting-Key Closure (Step 3A)

P71 executed the awaiting-key closure path:

- Loaded P70 context and verified `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY`
- Confirmed key is absent: `API_KEY_MISSING`
- Set `live_api_calls=0`, `paid_api_called=False`
- Documented 7-step process to configure key and execute live pull
- Classified: **`P71_PATH_A_STILL_AWAITING_API_KEY`**
- Summary written: `data/mlb_2025/derived/p71_the_odds_api_live_pull_execution_summary.json`

---

## 6. CSV Schema Documentation

Once the API key is configured and P70 executes a live pull, the output CSV must validate:

| Field | Type | Constraint |
|---|---|---|
| `game_date` | string | Within 2024-03-20 → 2024-09-29 |
| `home_team` | string | Non-empty |
| `away_team` | string | Non-empty |
| `home_ml` | numeric | Valid float/int |
| `away_ml` | numeric | Valid float/int |
| `bookmaker` | string | Non-empty (prefer `pinnacle`) |
| `odds_timestamp` | string | ISO 8601 |
| `closing_indicator` | string | Non-empty |
| `source_trace` | string | Non-empty |

**Minimum row count:** 500 (target ~2430)  
**Validator:** `scripts/_p71_the_odds_api_live_pull_execution.py::validate_csv()`

---

## 7. Setup Required for Live Pull

To transition from `P71_PATH_A_STILL_AWAITING_API_KEY` to `P71_PATH_A_PULL_COMPLETE`:

1. Register at https://the-odds-api.com
2. Purchase a plan with historical data access (~$30–50)
3. Locate API key in account dashboard
4. Add to `.env`: `THE_ODDS_API_KEY=<your_key>`
5. Run P70 script: `.venv/bin/python scripts/_p70_path_a_the_odds_api_historical_pull.py`
6. Script auto-detects key → LIVE mode → writes `data/mlb_2025/mlb_odds_2024_real.csv`
7. Re-run P71 script to validate CSV and advance classification

---

## 8. Governance

| Flag | Value |
|---|---|
| `PAPER_ONLY` | `True` |
| `DIAGNOSTIC_ONLY` | `True` |
| `PROMOTION_FREEZE` | `True` |
| `KELLY_DEPLOY_ALLOWED` | `False` |
| `REAL_BET_ALLOWED` | `False` |
| `PRODUCTION_READY` | `False` |
| `PAID_API_CALLED` | `False` |
| `LIVE_API_CALLS` | `0` |
| `TSL_CRAWLER_CALLED` | `False` |
| `BULK_SCRAPING_PERFORMED` | `False` |
| `ANTI_BOT_BYPASS_ATTEMPTED` | `False` |
| `RUNTIME_RECOMMENDATION_LOGIC_CHANGED` | `False` |
| `CEO_AUTHORIZATION_CONFIRMED` | `True` |
| Platt A (P45 locked) | `0.435432` |
| Platt B (P45 locked) | `0.245464` |
| P52 ECE warn threshold | `0.10` |
| P52 ECE crit threshold | `0.12` |
| P52 Brier warn threshold | `0.25` |
| P52 Brier crit threshold | `0.27` |
| P52 Edge warn threshold | `0.07` |

---

## 9. Test Results

### P71 Tests
```
tests/test_p71_the_odds_api_live_pull_execution.py — 48 passed in 0.11s
```

Coverage groups:
- §1 P70 context loaded (4 tests)
- §2 API key detection — no exposure (5 tests)
- §3 Classification validity (3 tests)
- §4 Required schema fields (2 tests)
- §5 Output CSV path (2 tests)
- §6 Governance flags (9 tests)
- §7 Platt constants (3 tests)
- §8 P52 thresholds (2 tests)
- §9 paid_api_called / live_api_calls (2 tests)
- §10 CSV validator unit tests (4 tests)
- §11 Setup instructions (1 test)
- §12 Summary structure (3 tests)
- §13 Forbidden affirmative scan (2 tests)
- §14 Active task updated (2 tests)
- §15 Governance assertion guard (2 tests)

### Cumulative Regression: P43 + P59–P71
```
437 passed in 2.68s
```
Prior (P43+P59–P70): 389 PASS  
P71 new tests: 48  
Total: **437 PASS, 0 FAIL**

---

## 10. Forbidden Scan

Scanned `scripts/_p71_the_odds_api_live_pull_execution.py` for forbidden affirmative patterns:

```
REAL_BET_ALLOWED: bool = True       → 0 matches
KELLY_DEPLOY_ALLOWED: bool = True   → 0 matches
PRODUCTION_READY: bool = True       → 0 matches
BULK_SCRAPING_PERFORMED: bool = True → 0 matches
ANTI_BOT_BYPASS_ATTEMPTED: bool = True → 0 matches
CEO_AUTHORIZATION_CONFIRMED: bool = False → 0 matches
```

**Result: 0 violations**

---

## 11. Git Commit

```
git add scripts/_p71_the_odds_api_live_pull_execution.py
git add tests/test_p71_the_odds_api_live_pull_execution.py
git add data/mlb_2025/derived/p71_the_odds_api_live_pull_execution_summary.json
git add report/p71_the_odds_api_live_pull_execution_20260526.md
git add "00-BettingPlan/20260526/p71_the_odds_api_live_pull_execution_20260526.md"
git add "00-Plan/roadmap/active_task.md"
git commit (6 whitelist files only)
```

---

## 12. Classification

**`P71_PATH_A_STILL_AWAITING_API_KEY`**

Awaiting-key closure completed. Zero API calls. Zero data written. Full infrastructure ready to auto-advance to `P71_PATH_A_PULL_COMPLETE` upon key configuration.

---

## 13. Next 24h Prompt (Copyable)

```
P72 — Once THE_ODDS_API_KEY is configured in .env:
  1. Re-run scripts/_p70_path_a_the_odds_api_historical_pull.py (LIVE mode)
  2. Run scripts/_p71_the_odds_api_live_pull_execution.py to validate CSV
  3. Expected: P71 auto-advances to P71_PATH_A_PULL_COMPLETE
  4. CSV requirements: 9 schema fields, ≥500 rows, date range 2024-03-20→2024-09-29

Alternatively — P72 (Deferred API Key):
  Document the 2024 real-odds gap as permanent research limitation.
  Close PATH_A track. Proceed with alternative feature engineering.
```

---

## 14. CTO 10-Line Summary

1. P71 executed the awaiting-key closure (Step 3A) on 2026-05-26.  
2. API key detection result: `API_KEY_MISSING` — no `THE_ODDS_API_KEY` found in `.env` or environment.  
3. Zero API calls made, zero CSV rows written, paid_api_called=False.  
4. P70 context loaded and verified: `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY` (dry-run stable).  
5. Classification: `P71_PATH_A_STILL_AWAITING_API_KEY`.  
6. Complete CSV validation infrastructure implemented: schema check, row count ≥500, moneyline numeric, date range.  
7. 7-step setup guide documented: register → subscribe → add key → re-run P70 → P70 auto-switches to LIVE.  
8. P71 tests: 48 PASS; cumulative P43+P59–P71: 437 PASS, 0 FAIL.  
9. Governance fully preserved: Platt constants locked, P52 thresholds locked, no runtime logic changed.  
10. Next: P72 — add `THE_ODDS_API_KEY` to `.env` and re-run P70 to execute actual 2024 MLB moneyline pull.
