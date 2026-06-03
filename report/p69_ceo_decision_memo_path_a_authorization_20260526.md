# P69 — CEO Decision Memo: P61 PATH_A Authorization for The Odds API Historical Pull
**Classification**: `P69_CEO_DECISION_MEMO_READY`
**Date**: 2026-05-26 | **Branch**: main | **Mode**: `paper_only=true`, `diagnostic_only=true`

---

## §1 Pre-flight Result

| Check | Result |
|---|---|
| repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✓ |
| branch | `main` ✓ |
| HEAD | `cda1a90` (P68 commit) ✓ |
| uncommitted changes | runtime / logs / daemon output only — non-whitelist ✓ |
| governance flags | all correct ✓ |

Pre-flight: **PASS**

---

## §2 Dirty File Assessment

Only runtime / daemon / odds cache / log files modified (all in non-whitelist paths). No P69-relevant files were pre-modified. Working tree clean for whitelist purposes.

---

## §3 Evidence Trail Loaded

| Phase | Classification | Verification |
|---|---|---|
| P61 | `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT` | ✓ |
| P67 | `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW` | ✓ |
| P68 | `P68_ODDSPORTAL_BLOCKED_BY_TOS` | ✓ |

All prior-phase governance blocks verified: `paid_api_called=False`, `live_api_calls=0`, `bulk_scraping_performed=False` across all three phases. Evidence trail is clean and internally consistent.

2024 gap status at P68 exit: **`UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A`**

---

## §4 CEO Decision Memo

---

### TO: CEO
### FROM: CTO / Research Lead
### DATE: 2026-05-26
### RE: Authorization Request — P61 PATH_A: The Odds API One-Time Historical Pull for 2024 MLB Closing-Line Validation

---

### 4a. Executive Summary

We are requesting **one-time authorization** to make a paid API call to The Odds API (`the-odds-api.com`) to retrieve 2024 MLB regular season historical moneyline odds for **paper-only research validation only**.

**Cost**: approximately $30–50 (one-time)
**Purpose**: close the 2024 closing-line data gap that currently blocks our P43 cross-year validation
**Use**: diagnostic only — paper simulation, research validation, never for live betting or production

This is a data-sourcing decision, not a betting recommendation or production proposal.

---

### 4b. Evidence Trail (P61 → P67 → P68)

**P61** `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT`:
- Confirmed 2024 MLB closing-line data is absent from our dataset
- Identified P43 as blocked by this gap: `P43_BLOCKED_BY_DATA_GAP`
- Proposed two resolution paths: PATH_A (paid API) and PATH_B (free sources)
- Recommended executing PATH_B first; escalate to PATH_A if PATH_B fails

**P67** `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`:
- Exhaustive free-source search executed (13 queries, 7 sources evaluated)
- Kaggle: 27 datasets found — all game stats, no moneyline odds
- GitHub: 0 public repos with 2024 MLB odds
- SBRO: archive frozen at 2021 — no 2024 data
- aussportsbetting: HTTP 403 — blocked
- OddsPortal: data visible in web UI, but classified as "needs ToS review"
- Free-source PATH_B yielded no legally usable bulk dataset

**P68** `P68_ODDSPORTAL_BLOCKED_BY_TOS`:
- OddsPortal ToS Section 2.11: explicitly prohibits scraping and automated requests
- OddsPortal ToS Section 2.10: explicitly prohibits database extraction without express consent
- OddsPortal robots.txt: `Disallow: *-2024*` for all user-agents — independently blocks crawling
- OddsPortal data is visible but **legally inaccessible** under current ToS
- No bulk extraction performed (governance preserved throughout)

**Conclusion**: Free-source PATH_B is exhausted. PATH_A is the only remaining viable path.

---

### 4c. Why 2024 Closing-Line Data Matters

Our current model validation is limited to 2025 data (1,426 quality rows after join). The P43 cross-year edge stability study requires 2024 closing-line data to:

1. Run a cross-year bootstrap confidence interval on the combined 2024+2025 dataset (~3,856 quality rows)
2. Verify whether the positive-edge signal in 2025 is consistent across years
3. Determine if P43 can be upgraded from `P43_BLOCKED_BY_DATA_GAP` to `P43_CROSS_YEAR_EDGE_CONFIRMED` or similar

If 2024 confirms positive edge → strengthens research conclusion.
If 2024 shows negative edge → weakens conclusion but is scientifically valid and should be accepted. Either outcome is useful.

---

### 4d. Why Free Sources Are Insufficient

| Source | Status | Reason |
|---|---|---|
| Kaggle (27 datasets) | BLOCKED | No moneyline odds — game stats only |
| GitHub (3 queries) | BLOCKED | 0 repos with 2024 MLB odds |
| Kaggle synthetic | REJECTED | Faker-generated fake data |
| SBRO | BLOCKED | Archive frozen at 2021 |
| aussportsbetting | BLOCKED | HTTP 403 |
| OddsPortal | BLOCKED | ToS Section 2.11 + robots.txt prohibit extraction |

**All 6 free sources exhausted.** No legally usable, bulk-loadable 2024 MLB closing-line dataset was found.

---

### 4e. Why OddsPortal Cannot Be Used

OddsPortal.com (Livesport s.r.o.) has:
- ToS Section 2.11: *"you are not permitted to use our content … by embedding, aggregating, **scraping** or recreating it without our express consent"*
- ToS Section 2.10: *"no extraction (copying) or exploitation of the Database Content … is permitted without our express consent"*
- robots.txt: `Disallow: *-2024*` for `User-agent: *` — independent technical signal
- No research or non-commercial exemption stated
- Express written consent from Livesport s.r.o. would be required — impractical timeline

---

### 4f. Proposed PATH_A Scope

| Field | Value |
|---|---|
| Source | The Odds API (`https://the-odds-api.com`) |
| Pull type | One-time historical data pull (NOT live odds) |
| Data | 2024 MLB regular season moneyline odds |
| Date range | 2024-03-20 to 2024-09-29 (~162 games × 30 teams = ~2,430 game-rows) |
| Estimated cost | $30–50 one-time |
| Data quality | HIGH (structured JSON, per-game timestamps) |
| Schema match | HIGH — conversion script ~50 lines |
| Timeline | 1–2 days after authorization |

---

### 4g. Required Data Fields

| Required Field | The Odds API Source | Notes |
|---|---|---|
| `game_date` | Event timestamp | ISO 8601 parse |
| `home_team` | `home_team` field | Name normalization required |
| `away_team` | `away_team` field | Name normalization required |
| `home_ml` | Decimal odds (home) | Convert to American ML |
| `away_ml` | Decimal odds (away) | Convert to American ML |
| `bookmaker` | `bookmaker.key` | Label market source |
| `odds_timestamp` | `last_update` / `commence_time` | Closing-line proxy |
| `closing_indicator` | Inferred from final snapshot | Pre-game final snapshot = closing |
| `source_trace` | Injected at pull time | Source URL + pull date + script version |

---

### 4h. Governance Restrictions (Non-Negotiable)

All of the following apply regardless of CEO decision:

| Restriction | Status |
|---|---|
| `paper_only=true` | Permanent — no production use |
| `diagnostic_only=true` | Permanent — no live recommendation |
| `kelly_deploy_allowed=false` | Permanent — no staking |
| `real_bet_allowed=false` | Permanent — no actual betting |
| `production_ready=false` | Permanent — no system deployment |
| `champion_strategy_changed=false` | Permanent — no replacement |
| `promotion_freeze=true` | Permanent — no optimizer promotion |
| Platt constants | Locked: A=0.435432, B=0.245464 |
| P52 thresholds | Unchanged |

The paid API call itself (if approved) would be a one-time, offline historical data pull — categorically different from live odds API calls, which remain permanently prohibited.

---

### 4i. Allowed Use (if Approved)

- Paper-only simulation using 2024 closing-line data as model input
- Diagnostic-only validation of P43 cross-year edge stability
- Research-internal use — no commercial distribution
- Joining 2024 closing-line odds to 2024 model predictions for edge calculation
- P43 cross-year bootstrap CI on ~3,856 combined quality rows (2024+2025)

### 4j. Prohibited Use (regardless of approval)

- Live betting or real money wagering
- Production recommendation output
- Kelly criterion staking deployment
- Champion strategy replacement
- Commercial redistribution of The Odds API data
- Aggregation or re-publication of odds data to third parties
- Any claim of profitability or production readiness

---

### 4k. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| 2024 data shows negative edge → weakens cross-year conclusion | LOW — scientifically valid outcome | Accept as valid finding; no suppression |
| The Odds API data quality is lower than expected | MEDIUM | Validate completeness (all 30 teams, full regular season) before join |
| Cost exceeds estimate | LOW | $30–50 is bounded; cancel if pricing is outside range |
| Schema mismatch | LOW | P61 assessed schema match as HIGH; conversion script ~50 lines |
| Data redistribution risk | LOW | Strict paper-only governance, no external sharing |

---

### 4l. Cost / Benefit

| Item | Value |
|---|---|
| Cost | $30–50 one-time |
| Rows unlocked | ~2,430 (2024 MLB regular season) |
| Cost per row | ~$0.012–0.021 per game-row |
| P43 research unlock | Cross-year edge CI on ~3,856 rows |
| Research value | HIGH — resolves the largest single gap in our validation pipeline |
| Opportunity cost of rejection | P43 remains permanently blocked at `P43_BLOCKED_BY_DATA_GAP` |

---

## §5 PATH_A Scope Summary

**The Odds API** → one-time historical pull → 2024 MLB regular season moneyline → ~$30–50 → paper-only.

---

## §6 CEO Decision Options

### Option 1 — APPROVE

Authorize The Odds API one-time historical pull for 2024 MLB closing-line validation.

**Next task**: P70 — The Odds API Historical Pull (authorized, one-time paid call, paper-only)

**Copy-paste phrase for CEO:**
```
YES authorize P61 PATH_A The Odds API historical 2024 MLB moneyline pull for paper-only validation
```

---

### Option 2 — REJECT

Decline PATH_A. Freeze 2024 closing-line scope. Accept `P43_BLOCKED_BY_DATA_GAP` as permanent.

**Next task**: P70 — 2024 Scope Freeze (document final gap, archive P43 blocked status, close research loop)

**Copy-paste phrase for CEO:**
```
NO reject P61 PATH_A and freeze 2024 closing-line scope
```

---

### Option 3 — DEFER

Request more information before committing.

**Next task**: P70 — CEO Information Request (define open questions, re-present PATH_A after answers)

**Copy-paste phrase for CEO:**
```
DEFER P61 PATH_A pending more information
```

---

## §7 Recommended Next Task per Decision

| CEO Decision | Next Task | Classification |
|---|---|---|
| APPROVE | P70 — The Odds API historical pull | `P70_PATH_A_PULL_AUTHORIZED` |
| REJECT | P70 — 2024 scope freeze | `P70_2024_SCOPE_FROZEN_BY_CEO` |
| DEFER | P70 — CEO information request | `P70_DECISION_DEFERRED_PENDING_INFO` |

---

## §8 Governance Restrictions (P69)

| Flag | Value | Status |
|---|---|---|
| `paper_only` | `True` | ✓ |
| `diagnostic_only` | `True` | ✓ |
| `promotion_freeze` | `True` | ✓ |
| `kelly_deploy_allowed` | `False` | ✓ |
| `live_api_calls` | `0` | ✓ |
| `paid_api_called` | `False` | ✓ |
| `the_odds_api_called_in_p69` | `False` | ✓ |
| `tsl_crawler_called` | `False` | ✓ |
| `bulk_scraping_performed` | `False` | ✓ |
| `anti_bot_bypass_attempted` | `False` | ✓ |
| `runtime_recommendation_logic_changed` | `False` | ✓ |
| `real_bet_allowed` | `False` | ✓ |
| `production_ready` | `False` | ✓ |
| P45 Platt constants | A=0.435432, B=0.245464 | Unchanged ✓ |

All governance invariants preserved throughout P69.

---

## §9 Test Results

```
tests/test_p69_ceo_decision_memo_path_a_authorization.py  42 passed
Cumulative regression (P43+P59–P69):                     338 passed
```

**All 338 tests PASS.** (296 prior + 42 new P69 tests)

---

## §10 Forbidden Scan Result

Script `scripts/_p69_ceo_decision_memo_path_a_authorization.py` scanned for forbidden affirmative patterns:

| Pattern | Found |
|---|---|
| `production_ready = True` | NOT FOUND |
| `kelly_deploy_allowed = True` | NOT FOUND |
| `real_bet_allowed = True` | NOT FOUND |
| `paid_api_called = True` | NOT FOUND |
| `PAID_API_CALLED: bool = True` | NOT FOUND |
| `LIVE_API_CALLS: int = 1` | NOT FOUND |
| `TSL_CRAWLER_CALLED: bool = True` | NOT FOUND |
| `BULK_SCRAPING_PERFORMED: bool = True` | NOT FOUND |
| `ANTI_BOT_BYPASS_ATTEMPTED: bool = True` | NOT FOUND |
| `RUNTIME_RECOMMENDATION_LOGIC_CHANGED: bool = True` | NOT FOUND |
| `PROMOTION_FREEZE: bool = False` | NOT FOUND |
| `the_odds_api_called_in_p69: True` | NOT FOUND |

**Forbidden scan: 0 violations (CLEAN)**

---

## §11 Final Classification

```
P69_CEO_DECISION_MEMO_READY
```

The memo is complete, the evidence trail is verified, all CEO decision options are documented with exact copy-paste phrases, and governance is preserved. Awaiting CEO decision before P70 can begin.

---

## §12 Commit Hash

P69 commit: `981228f`

Whitelist files (6):
- `scripts/_p69_ceo_decision_memo_path_a_authorization.py`
- `tests/test_p69_ceo_decision_memo_path_a_authorization.py`
- `data/mlb_2025/derived/p69_ceo_decision_memo_path_a_authorization_summary.json`
- `report/p69_ceo_decision_memo_path_a_authorization_20260526.md`
- `00-BettingPlan/20260526/p69_ceo_decision_memo_path_a_authorization_20260526.md`
- `00-Plan/roadmap/active_task.md`

---

## §13 Next 24h Prompt

```
P70 — CEO Decision on P61 PATH_A: Execute Based on CEO Response

Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True
Branch: main | HEAD: [P69 commit hash]

CEO Decision Required (one of three phrases from P69 memo):

  APPROVE: "YES authorize P61 PATH_A The Odds API historical 2024 MLB moneyline pull for paper-only validation"
  REJECT:  "NO reject P61 PATH_A and freeze 2024 closing-line scope"
  DEFER:   "DEFER P61 PATH_A pending more information"

P70 scope branches on CEO response:

  IF APPROVE:
    - Execute one-time The Odds API historical pull for 2024 MLB moneyline
    - Target: ~2,430 rows, date range 2024-03-20 to 2024-09-29
    - Required fields: game_date, home_team, away_team, home_ml, away_ml, bookmaker, odds_timestamp, closing_indicator, source_trace
    - Write to: data/mlb_2025/mlb_odds_2024_real.csv
    - paper_only=True: NEVER used for live betting or production
    - Classify as: P70_PATH_A_PULL_AUTHORIZED

  IF REJECT:
    - Document 2024 scope freeze
    - Archive P43_BLOCKED_BY_DATA_GAP as permanent status
    - Close research loop on 2024 validation
    - Classify as: P70_2024_SCOPE_FROZEN_BY_CEO

  IF DEFER:
    - Document open CEO questions
    - Re-present PATH_A after answers received
    - Classify as: P70_DECISION_DEFERRED_PENDING_INFO

Context:
  - P69 classification: P69_CEO_DECISION_MEMO_READY
  - P68 classification: P68_ODDSPORTAL_BLOCKED_BY_TOS
  - P67 classification: P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW
  - P61 classification: P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT
  - 2024 gap status: UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A
  - P43 status: P43_BLOCKED_BY_DATA_GAP (blocked since P61)

Governance constraints for P70 (APPROVE branch):
  - Only call The Odds API if CEO phrase is EXACTLY as specified above
  - paper_only=True, real_bet_allowed=False, production_ready=False
  - Platt constants locked: A=0.435432, B=0.245464
  - No Kelly deployment, no champion replacement, no runtime logic changes
  - ≥20 tests, cumulative regression, 6 whitelist files, commit
```

---

## §14 CTO Agent 10-Line Summary

P69 drafted the CEO decision memo for P61 PATH_A authorization — The Odds API one-time historical pull for 2024 MLB closing-line data (~$30–50).
Evidence trail P61→P67→P68 verified: all three prior classifications confirmed; all prior-phase governance blocks clean (no paid/live/TSL calls).
Free-source PATH_B is fully exhausted: 6 sources evaluated, 0 produced a legally usable 2024 MLB moneyline dataset.
OddsPortal block reconfirmed: ToS Section 2.11 + robots.txt `*-2024*` independently prohibit automated extraction.
PATH_A spec documented: 9 required fields, ~2,430 rows, ~$30–50, HIGH data quality, HIGH schema match.
Allowed use: paper-only, diagnostic-only, research validation, never for live betting or production.
CEO decision options: APPROVE / REJECT / DEFER — exact copy-paste phrases embedded in memo.
42 P69 tests PASS; cumulative regression 338/338 PASS (P43+P59–P69); forbidden scan 0 violations.
Governance fully preserved: no API calls, no scraping, no live data, no anti-bot bypass, Platt constants unchanged.
Next step: P70 — execute based on CEO decision (APPROVE → The Odds API pull; REJECT → freeze 2024 scope; DEFER → info request).
