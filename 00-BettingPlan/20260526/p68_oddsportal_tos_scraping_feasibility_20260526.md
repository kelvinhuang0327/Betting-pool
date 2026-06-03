# P68 — OddsPortal ToS and Scraping Feasibility Probe
**Date**: 2026-05-26 | **Classification**: `P68_ODDSPORTAL_BLOCKED_BY_TOS`

---

## Classification Verdict

| Item | Result |
|---|---|
| ToS Classification | `TOS_BLOCKS_SCRAPING` |
| robots.txt | `Disallow: *-2024*` for all User-agents |
| Page Classification | `PAGE_VISIBLE_BUT_CLOSING_ODDS_UNCLEAR` |
| Schema Status | `SCHEMA_BLOCKED_BY_TOS` |
| **P68 Final** | **`P68_ODDSPORTAL_BLOCKED_BY_TOS`** |

---

## ToS Blocking Evidence

**Section 2.11** (Illegal interventions):
> "you are not permitted to use our content available on the Website by embedding, aggregating, **scraping** or recreating it without our express consent."

**Section 2.10** (Database protection):
> "no extraction (copying) or exploitation of the Database Content … is permitted without our express consent."

**robots.txt**: `User-agent: *` → `Disallow: *-2024*` covers `/baseball/usa/mlb-2024/results/` exactly.

---

## 2024 Data Gap Status

`UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A`

All free public sources exhausted or blocked:
- OddsPortal → **BLOCKED** (this P68 result)
- SBRO → **BLOCKED** (archive frozen at 2021, P67)
- Kaggle/GitHub → **NO DATA** (P67)
- aussportsbetting → **BLOCKED** (HTTP 403, P67)

---

## Recommendation

**CEO Decision Required — P61 PATH_A**

Escalate to The Odds API paid historical pull:
- Cost: ~$30–50 one-time
- Data: 2024 MLB closing-line moneyline (full season)
- Legal: paid subscription with explicit terms
- Next task: P69 CEO Decision Memo

No scraping without express written consent from Livesport s.r.o. (OddsPortal operator).

---

## Governance

`paper_only=true` | `bulk_scraping_performed=false` | `anti_bot_bypass_attempted=false`
`live_api_calls=0` | `paid_api_called=false` | `tsl_crawler_called=false`
`real_bet_allowed=false` | `production_ready=false`
Platt constants: A=0.435432, B=0.245464 (unchanged)

---

## Test Results

- P68 tests: **36/36 PASS**
- Cumulative regression (P43+P59–P68): **296/296 PASS**
- Forbidden scan: **0 violations**
