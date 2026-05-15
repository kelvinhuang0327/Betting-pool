# P3.1 No-Download Blocker Report — 2026-05-15

**Status:** NO_DOWNLOAD_BLOCKER — AWAITING USER APPROVAL  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Blocker Type:** ALL_SOURCES_BLOCKED_PENDING_USER_DECISION  
**References:**
- `p31_research_odds_source_decision_20260515.md` (TRACK 3 decision: PAID_PROVIDER_DECISION_REQUIRED)
- `research_odds_public_source_deep_audit_20260515.md` (TRACK 1)
- `research_odds_paid_provider_decision_matrix_20260515.md` (TRACK 2)

---

## 1. Current State

No real 2024 MLB moneyline closing odds data is available for local-only use.

| Location | Content |
|---|---|
| `data/research_odds/local_only/` | Empty (gitignored) |
| `data/research_odds/fixtures/` | Synthetic fixture only (5 rows, `source_license_status=synthetic_no_license`) |

---

## 2. Blocker Root Cause Analysis

| Source | Blocker | Resolution Required |
|---|---|---|
| CANDIDATE-03-B (Gumroad) | No Gumroad purchase made | User approval → purchase → agent download |
| CANDIDATE-04 (AusSportsBetting) | HTTP 403 on terms page | User manual browser visit → terms review |
| CANDIDATE-08-A (tobijegede) | Dataset inaccessible | None — REJECTED (no path forward) |
| CANDIDATE-09 (GitHub) | Zero qualifying repos | None — REJECTED (no path forward) |
| The Odds API (PROVIDER-A) | No subscription active | User approves $30/month → agent implements |
| SportsDataIO (PROVIDER-B) | No subscription; pricing unclear | User initiates sales contact |
| Sportradar (PROVIDER-C) | Enterprise contract required | Out of scope for research prototype |
| Manual import | No user-provided file present | User drops file into `data/research_odds/local_only/` |

**All 8 paths to real data are blocked by the same root cause: user decision required.**

---

## 3. What Exists Today (No Blocker)

The following smoke infrastructure is ready and working, with NO external data required:

| Asset | Status | Rows | Blocker |
|---|---|---|---|
| `P38A_JOIN_SMOKE_TEMPLATE_20260514.csv` | ✅ COMMITTED | 5 (synthetic) | None |
| Join smoke script (5-row) | ✅ VERIFIED (5/5 PASS) | 5 | None |
| P38A OOF predictions CSV | ✅ COMMITTED | 2,187 real | None |
| Bridge table (game identity) | ✅ COMMITTED | ~2,429 | None |
| 23-column contract schema | ✅ COMMITTED | N/A | None |
| Team normalization table | ✅ COMMITTED | 30 teams | None |
| `data/research_odds/local_only/` directory | ✅ EXISTS (empty, gitignored) | 0 | None |

**The plumbing is complete. Only the source data (real odds) is missing.**

---

## 4. Unblock Paths (Ranked by Speed)

### Path 1 — The Odds API ($30/month) [Fastest]
- Subscribe to The Odds API 20K plan
- Agent creates `scripts/fetch_odds_api_historical.py` same session
- One script execution → ≥100 rows in `data/research_odds/local_only/`
- Time to ≥100 rows: **same day (< 2 hours)**
- Cost: **$30/month**

### Path 2 — Manual File Import [Zero cost if user has data]
- User provides any CSV with moneyline odds for 2024 MLB games
- Drop into `data/research_odds/local_only/my_odds_data.csv`
- Agent validates schema, transforms to 23-column contract, runs join smoke
- Time to ≥100 rows: **same session (< 30 minutes)**
- Cost: **$0**

### Path 3 — Gumroad Purchase [Low cost, license confirmed]
- User purchases CANDIDATE-03-B (oliviersportsdata full dataset)
- Agent validates schema post-purchase + runs join smoke
- Time to ≥100 rows: **1–2 days** (purchase + download + validation)
- Cost: **~$5–$20 one-time** (Gumroad price not confirmed)

### Path 4 — AusSportsBetting [Free if terms acceptable]
- User visits terms page manually in browser
- User reports terms content to agent
- If acceptable: agent creates download script; user downloads
- Time to ≥100 rows: **1–2 days**
- Cost: **$0 (if terms acceptable)**

---

## 5. Next-Session Resume Instructions

When user provides ANY of the following, agent can immediately proceed:

```
CASE A — Odds API:
  User says: "I subscribed to The Odds API, key is in .env"
  → Create scripts/fetch_odds_api_historical.py
  → Execute batch pull for 5 game days (≥50 games)
  → Transform + join → run ≥100 rows smoke
  → Write p31_real_odds_join_smoke_EXECUTED_20260515.md

CASE B — Manual import:
  User says: "I dropped a CSV in data/research_odds/local_only/"
  → Validate schema (23-column contract check)
  → Transform if needed
  → Run ≥100 rows join smoke
  → Write p31_real_odds_join_smoke_EXECUTED_20260515.md

CASE C — Gumroad:
  User says: "I downloaded the oliviersportsdata full dataset to data/research_odds/local_only/"
  → Validate schema (check semicolon separator, timestamp column, team format)
  → Transform + normalize team codes
  → Run ≥100 rows join smoke
  → Write p31_real_odds_join_smoke_EXECUTED_20260515.md

CASE D — AusSportsBetting:
  User says: "Terms are [content], download is available at [URL], format is [X]"
  → Reclassify CANDIDATE-04 based on user-reported terms
  → Create download script if acceptable
  → Run ≥100 rows join smoke
  → Write p31_real_odds_join_smoke_EXECUTED_20260515.md
```

---

## 6. Acceptance Marker

```
P31_NO_DOWNLOAD_BLOCKER_20260515_READY
```

**Blocking Classification:** `ALL_SOURCES_BLOCKED_PENDING_USER_DECISION`  
**Next Unlocked Track:** TRACK 5 (join smoke) — unblocked automatically when data arrives
