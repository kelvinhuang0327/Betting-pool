# P68 — OddsPortal ToS and Scraping Feasibility Probe
**Classification**: `P68_ODDSPORTAL_BLOCKED_BY_TOS`
**Date**: 2026-05-26 | **Branch**: main | **Mode**: `paper_only=true`, `diagnostic_only=true`

---

## §1 Pre-flight Result

| Check | Result |
|---|---|
| repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✓ |
| branch | `main` ✓ |
| HEAD | `6ceeaf3` (P67 commit) ✓ |
| uncommitted changes | runtime / logs / daemon output only — all in exclusion list ✓ |
| governance flags | all correct ✓ |

Pre-flight: **PASS**

---

## §2 Dirty File Assessment

Only runtime / daemon / odds cache / log files modified (all in non-whitelist paths). No P68-relevant files were pre-modified. Working tree clean for whitelist purposes.

---

## §3 P67 Context Loaded

| Field | Value |
|---|---|
| P67 classification | `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW` ✓ |
| OddsPortal candidate | Present ✓ |
| 2024 data gap | UNRESOLVED_PENDING_P68_SCRAPE_FEASIBILITY ✓ |
| paid/live/TSL in P67 | 0 (all False) ✓ |
| P67 commit | `6ceeaf3` ✓ |

P67 established OddsPortal as a "partial" source: 2024 data visible in web UI, but no bulk CSV download, and ToS Section references restricted automated extraction. P68 is the formal ToS + robots.txt + page structure review.

---

## §4 ToS / Access Review

### 4a. ToS Source

| Field | Value |
|---|---|
| ToS URL | `https://www.oddsportal.com/terms/` |
| ToS accessible | Yes |
| Operator | Livesport s.r.o. (Prague, Czech Republic) |
| ToS last updated | 09.10.2023 |
| ToS classification | **`TOS_BLOCKS_SCRAPING`** |
| Risk level | **BLOCKING** |

### 4b. Key Clauses (direct quotes)

**Section 2.9 — Content rights:**
> "the use of copyright works in the form of reproduction (copying) for the purpose of direct or indirect economic gain ... is not permitted without our express consent."

**Section 2.10 — Protection of Databases:**
> "no extraction (copying) or exploitation (making available to the public) of the Database Content or of a qualitatively or quantitatively substantial part thereof is permitted without our express consent."

**Section 2.11 — Illegal interventions (key clause):**
> "You must not burden our server on which the Website is hosted with automated requests, nor assist any third party in such activity. Furthermore, you are not permitted to use our content available on the Website by embedding, aggregating, **scraping** or recreating it without our express consent, unless otherwise provided for by applicable laws and regulations."

**Section 2.2 — Personal use restriction:**
> "Your access to and use of the Website, and the use of any information that may be provided to you in connection with the Website are, however, at your sole choice, discretion, risk and for your **personal use only**. You may not use the Website or our content for **commercial purposes**."

### 4c. robots.txt Findings

| Field | Value |
|---|---|
| robots.txt URL | `https://www.oddsportal.com/robots.txt` |
| robots.txt accessible | Yes |
| Disallow for `User-agent: *` | `*-2024*`, `*-2023*`, ..., `*-1998*` (all historical years) |
| Target URL pattern | `/baseball/usa/mlb-2024/results/` matches `*-2024*` |
| Verdict | **ALL historical season pages are explicitly disallowed for all bots** |

The robots.txt `Disallow: *-2024*` pattern covers the exact URL pattern needed for 2024 MLB data extraction. This is an independent blocking signal from the ToS.

### 4d. ToS Summary Assessment

Both ToS (Section 2.11 scraping prohibition) and robots.txt (explicit `Disallow: *-2024*` for all user-agents) independently block automated data extraction. No research exemption is stated. Express written consent from Livesport s.r.o. would be required before any extraction could be considered lawful. No automated scraping is permitted under current ToS.

---

## §5 Page Structure Probe

### Methodology

Single manual `fetch_webpage` call — no automation, no pagination loop, no bulk extraction. This is the minimal probe allowed under P68 diagnostic-only governance.

### Findings

| Field | Result |
|---|---|
| Page reachable | Yes |
| Page title | "MLB 2024 Results, Scores & Historical Odds" |
| Season navigation | 2019–2026 links confirmed visible |
| Pagination | 50 pages ([1][2]...[50][Next]) |
| Estimated total rows | ~2,500 games |
| Odds table visible | Yes |
| Decimal odds visible | Yes |
| Home/Away teams visible | Yes |
| Score visible | Yes |
| Date visible | Yes |
| Stage visible (Regular / Play Offs) | Yes |
| Anti-bot triggered | No |
| Access blocked | No |

### Sample Observed Rows (World Series 2024)

| Date | Away Team | Away Odds | Home Team | Home Odds |
|---|---|---|---|---|
| 25 Oct 2024 | New York Yankees | 2.37 | Los Angeles Dodgers | 1.71 |
| 26 Oct 2024 | New York Yankees | 2.20 | Los Angeles Dodgers | 1.74 |
| 27 Oct 2024 | Los Angeles Dodgers | 1.70 | New York Yankees | 2.31 |
| 29 Oct 2024 | New York Yankees | 2.20 | Los Angeles Dodgers | 1.77 |
| 30 Oct 2024 | New York Yankees | 2.37 | Los Angeles Dodgers | 1.71 |

### Page Classification: `PAGE_VISIBLE_BUT_CLOSING_ODDS_UNCLEAR`

Data is visible and structurally sound. However, odds labels on the results page do not explicitly distinguish "closing" vs "opening" prices. Settled (post-result) odds are shown, which functionally correspond to closing-line prices, but no explicit "closing" timestamp or label appears in the results table.

---

## §6 Schema Alignment Assessment

### Field Coverage

| Required Field | OddsPortal Equivalent | Present | Conversion Needed |
|---|---|---|---|
| `game_date` | Date string (e.g. "25 Oct 2024") | ✓ | datetime parse |
| `home_team` | Home Team (full name) | ✓ | name normalization (→ abbreviation) |
| `away_team` | Away Team (full name) | ✓ | name normalization |
| `home_ml` | Home Odds (decimal) | ✓ | decimal → American ML |
| `away_ml` | Away Odds (decimal) | ✓ | decimal → American ML |
| `odds_type` | Not labeled | ✗ (inferred) | must label as "inferred_closing" |
| `source_url` | Page URL (observer-assigned) | ✓ | assign at extraction time |
| `source_observed_at` | Not on page | ✗ | must inject at extraction time |
| `provenance_note` | Not on page | ✗ | must annotate with ToS risk note |

### Join Feasibility

Date + Away Team + Home Team are sufficient join keys to match against 2024 MLB game records, after name normalization. **Doubleheader disambiguation (game number within date) is NOT visible** on the results page — this would be an unresolved ambiguity for doubleheader games.

### Closing-Line Confidence

**LOW** — odds are post-settlement but not explicitly labeled "closing." The distinction between opening and closing odds is not clear from the results page alone. Additional per-game detail pages would need to be inspected to determine if closing timestamps are available.

### Schema Status: `SCHEMA_BLOCKED_BY_TOS`

Fields are technically observable, but ToS Section 2.11 prohibits scraping and Section 2.10 prohibits database extraction without express consent. robots.txt independently blocks automated access. Schema alignment analysis is moot until express consent is obtained from Livesport s.r.o.

---

## §7 Final Classification

```
P68_ODDSPORTAL_BLOCKED_BY_TOS
```

**Decision path:**
1. OddsPortal ToS classification = `TOS_BLOCKS_SCRAPING` (Sections 2.10 + 2.11) → immediate BLOCK
2. robots.txt `Disallow: *-2024*` for all user-agents → independent BLOCK
3. No research exemption stated in ToS
4. Express written consent from Livesport s.r.o. required before any extraction
5. Schema fields are observable but extraction is legally prohibited

OddsPortal has the data. The data is publicly viewable. The 2024 season is present. But the legal framework categorically prohibits automated extraction. This path requires either (a) formal consent request to Livesport s.r.o. or (b) fallback to P61 PATH_A.

---

## §8 Recommended Next Step

### Option A (Preferred): CEO Decision on P61 PATH_A — The Odds API

- **Source**: The Odds API (`https://the-odds-api.com`)
- **Cost**: ~$30–50 one-time historical pull (estimated in P61)
- **Data**: 2024 MLB historical closing-line moneyline odds (full season)
- **Legal**: Paid subscription with explicit data use terms
- **Requires**: CEO authorization (per P61 resolution plan)
- **Task**: Draft CEO decision memo with cost/benefit analysis

### Option B (Long-shot): Consent Request to Livesport s.r.o.

- Submit formal data access request to `info@livesport.eu` citing research purpose
- Explicitly non-commercial, non-redistributed use
- Response time uncertain; no guarantee of approval
- Only viable if CEO rejects PATH_A on cost grounds

### Recommendation

**Proceed directly to CEO Decision Memo for P61 PATH_A.** OddsPortal is blocked. The Odds API historical pull is the last viable free-source-alternative and the cost (~$30–50) is modest relative to the research value. A CEO authorization memo should be prepared immediately.

---

## §9 Governance Preservation Result

| Flag | Value | Status |
|---|---|---|
| `paper_only` | `True` | ✓ |
| `diagnostic_only` | `True` | ✓ |
| `promotion_freeze` | `True` | ✓ |
| `kelly_deploy_allowed` | `False` | ✓ |
| `live_api_calls` | `0` | ✓ |
| `paid_api_called` | `False` | ✓ |
| `tsl_crawler_called` | `False` | ✓ |
| `bulk_scraping_performed` | `False` | ✓ |
| `anti_bot_bypass_attempted` | `False` | ✓ |
| `runtime_recommendation_logic_changed` | `False` | ✓ |
| `real_bet_allowed` | `False` | ✓ |
| `production_ready` | `False` | ✓ |
| P45 Platt constants | A=0.435432, B=0.245464 | Unchanged ✓ |
| P52 thresholds | Unchanged | ✓ |
| P64/P65/P66/P67 artefacts | Unchanged | ✓ |

All governance invariants preserved. No automated extraction was performed. No anti-bot bypass was attempted. Probe was strictly limited to reading publicly accessible ToS and robots.txt, plus a single page load for structure inspection.

---

## §10 2024 Data Gap Status

| Field | Value |
|---|---|
| Gap status (P67) | UNRESOLVED_PENDING_P68_SCRAPE_FEASIBILITY |
| Gap status (P68) | **UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A** |
| OddsPortal | BLOCKED — ToS Section 2.11 + robots.txt `*-2024*` |
| SBRO | BLOCKED — archive frozen at 2021 |
| Kaggle/GitHub | No usable odds dataset found |
| aussportsbetting | BLOCKED — HTTP 403 |
| Last remaining path | P61 PATH_A — The Odds API paid historical pull (CEO authorization required) |

The 2024 closing-line gap remains unresolved. All free public sources have now been exhausted or blocked. P61 PATH_A (paid API) is the only remaining viable path.

---

## §11 Test Results

```
tests/test_p68_oddsportal_tos_scraping_feasibility.py  36 passed
Cumulative regression (P43+P59–P68):                  296 passed
```

**All 296 tests PASS.** (260 prior + 36 new P68 tests)

---

## §12 Forbidden Scan Result

Script `scripts/_p68_oddsportal_tos_scraping_feasibility.py` scanned for all forbidden affirmative patterns:

| Pattern | Found |
|---|---|
| `production_ready = True` | NOT FOUND |
| `kelly_deploy_allowed = True` | NOT FOUND |
| `real_bet_allowed = True` | NOT FOUND |
| `paid_api_called = True` | NOT FOUND |
| `LIVE_API_CALLS: int = 1` | NOT FOUND |
| `TSL_CRAWLER_CALLED: bool = True` | NOT FOUND |
| `BULK_SCRAPING_PERFORMED: bool = True` | NOT FOUND |
| `ANTI_BOT_BYPASS_ATTEMPTED: bool = True` | NOT FOUND |
| `RUNTIME_RECOMMENDATION_LOGIC_CHANGED: bool = True` | NOT FOUND |
| `PROMOTION_FREEZE: bool = False` | NOT FOUND |

**Forbidden scan: 0 violations (CLEAN)**

---

## §13 Commit Hash

P68 commit: `[see whitelist commit after this report]`

Whitelist files (6):
- `scripts/_p68_oddsportal_tos_scraping_feasibility.py`
- `tests/test_p68_oddsportal_tos_scraping_feasibility.py`
- `data/mlb_2025/derived/p68_oddsportal_tos_scraping_feasibility_summary.json`
- `report/p68_oddsportal_tos_scraping_feasibility_20260526.md`
- `00-BettingPlan/20260526/p68_oddsportal_tos_scraping_feasibility_20260526.md`
- `00-Plan/roadmap/active_task.md`

---

## §14 Next 24h Prompt

```
P69 — CEO Decision Memo: P61 PATH_A Authorization (The Odds API Historical Pull)

Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True
Prerequisites:
  - P68_ODDSPORTAL_BLOCKED_BY_TOS (this report)
  - P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW
  - P61 PATH_A resolution plan

Context:
  - All free public sources for 2024 MLB closing-line ML data are exhausted / blocked
  - OddsPortal: ToS Section 2.11 + robots.txt *-2024* disallow automated extraction
  - SBRO: archive frozen at 2021
  - Kaggle/GitHub: no odds data found
  - aussportsbetting: HTTP 403

P61 PATH_A requires CEO authorization:
  - Source: The Odds API (https://the-odds-api.com)
  - Estimated cost: ~$30-50 one-time historical pull for 2024 MLB season
  - Data delivered: JSON per-game moneyline odds (home ML, away ML, timestamps)
  - Use: 2024 closing-line validation of Platt-calibrated model (paper_only mode only)

P69 Objectives:
  1. Draft a CEO decision memo with the following sections:
     - Background (P61→P67→P68 evidence trail)
     - Cost/benefit analysis (~$30-50 for ≥2430 rows of 2024 closing-line data)
     - Data use constraints (paper_only, non-commercial, non-redistributed)
     - Risk assessment (paid API, data quality, join feasibility)
     - Decision request: APPROVE / REJECT / DEFER
  2. If APPROVED: proceed to P70 — The Odds API 2024 historical pull
  3. If REJECTED: document as final path exhaustion and freeze 2024 validation scope
  4. Classify as:
     P69_CEO_APPROVED_PROCEED_PATH_A |
     P69_CEO_REJECTED_FREEZE_2024_SCOPE |
     P69_CEO_DEFERRED_PENDING_INFO

Governance constraints:
  - Do NOT call The Odds API in P69
  - P69 is memo-drafting only (paper_only=True)
  - No live API, no TSL, no bulk scraping, no Kelly deployment
```

---

## §15 CTO Agent 10-Line Summary

P68 executed ToS and scraping feasibility probe for OddsPortal.com as 2024 MLB closing-line source.
ToS (`/terms/`) retrieved and analysed: Sections 2.10 (database extraction) and 2.11 (scraping/automated requests) explicitly prohibit extraction without express written consent from Livesport s.r.o.
robots.txt reviewed: `Disallow: *-2024*` for `User-agent: *` directly covers the target URL `/baseball/usa/mlb-2024/results/`.
Page structure confirmed: 2024 data visible, 50-page pagination, decimal odds observable — technically accessible but legally blocked.
Schema alignment assessed: 6/9 required fields visible; closing-line label absent; doubleheader disambiguation absent.
Classification: `P68_ODDSPORTAL_BLOCKED_BY_TOS` — both ToS and robots.txt independently block automated extraction.
2024 data gap status: `UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A` — all free/public sources now exhausted.
36 P68 tests PASS; cumulative regression 296/296 PASS (P43+P59–P68); forbidden scan 0 violations.
Governance preserved: no scraping, no paid API, no live API, no TSL, no anti-bot bypass, no runtime logic changes.
Next step: P69 — CEO Decision Memo authorizing P61 PATH_A (The Odds API, ~$30–50 one-time historical pull for 2024 MLB closing-line data).
