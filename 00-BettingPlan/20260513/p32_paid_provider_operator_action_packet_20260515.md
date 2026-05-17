# P3.2 Paid Provider Operator Action Packet — 2026-05-15

**Status:** AWAITING OPERATOR ACTION  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Trigger:** ODDS_DATA_NOT_READY (TRACK 1 gate result)  
**Next Session:** Once any action below is completed, rerun P3.2 and ≥100 rows join smoke will execute automatically.

---

## 1. Why ≥100 Rows Join Smoke Cannot Run Today

| Blocker | Detail |
|---|---|
| `.env` file | MISSING — file does not exist in repo root |
| `THE_ODDS_API_KEY` | NOT FOUND — no API key present |
| `data/research_odds/local_only/` content | EMPTY — only `.gitkeep` |
| Pre-existing real odds CSV | NONE |

No real 2024 MLB odds data is available. The join infrastructure (P38A OOF, bridge table, 23-column contract schema, team normalization table) is complete and waiting — only the source data is missing.

---

## 2. Unlock Options (Pick ONE)

### Option A: The Odds API Subscription [Recommended — Fastest]

**Time to ≥100 rows:** Same session (< 2 hours after subscribing)  
**Cost:** $30/month (20K plan)

**Steps:**

1. Go to: https://the-odds-api.com/#get-access  
2. Subscribe to the **20K plan** ($30/month)  
3. After payment, retrieve your API key from: https://dash.the-odds-api.com/  
4. Create `.env` file in the repo root:  

```
THE_ODDS_API_KEY=replace_me
```

Replace `replace_me` with your actual key.

5. Verify: `cat .env | grep THE_ODDS_API_KEY | sed 's/=.*/=***REDACTED***/'`  
6. Tell the CTO agent: **"Key is ready in `.env`"**

**Agent will immediately:**
- Run `scripts/fetch_odds_api_historical_mlb_2024_local.py --start-date 2024-04-01 --end-date 2024-04-10 --execute`
- Transform JSON → contract CSV
- Run ≥100 rows join smoke
- Compute CLV benchmark table

---

### Option B: Drop Your Own CSV [Zero cost if you already have odds data]

**Time to ≥100 rows:** 30 minutes  
**Cost:** $0 (if you already have data)

**Steps:**

1. Prepare a CSV file with 2024 MLB moneyline odds
2. Required columns (per `research_odds_manual_import_contract_20260513.md`):
   - `season` (integer, 2024)
   - `game_date` (YYYY-MM-DD)
   - `home_team` (Retrosheet 3-letter code or common MLB abbrev)
   - `away_team` (Retrosheet 3-letter code or common MLB abbrev)
   - `market` (must be `moneyline`)
   - `closing_home_moneyline` (American integer, e.g., -145)
   - `closing_away_moneyline` (American integer, e.g., +122)
   - `source_name` (free text, e.g., `user_export_draftkings`)
   - `source_license_status` (e.g., `user_owned` or `local_only_paid_provider_no_redistribution`)
   - `import_scope` (must be `research_only` or `local_only`)
   - `imported_at` (ISO 8601 UTC)
3. Drop the file to: `data/research_odds/local_only/my_odds_data_2024.csv`
4. Tell the CTO agent: **"CSV is in local_only/"**

**Agent will immediately:**
- Validate CSV schema (23-column contract)
- Normalize team codes → Retrosheet
- Run ≥100 rows join smoke
- Compute CLV benchmark table

---

### Option C: Gumroad Dataset (oliviersportsdata) [Low cost, license confirmed]

**Time to ≥100 rows:** 1–2 days  
**Cost:** ~$5–$20 one-time (Gumroad price not confirmed)

**Steps:**

1. Go to Kaggle: https://www.kaggle.com/datasets/oliviersportsdata/us-sports-master-historical-closing-odds
2. Click the Gumroad link to purchase full dataset
3. Download the full MLB CSV (2006–2025, ~46,235 rows, semicolon-separated)
4. Move to: `data/research_odds/local_only/oliviersportsdata_mlb_full.csv`
5. Note: separator is semicolon (`;`) — transform script handles this
6. Tell the CTO agent: **"Gumroad CSV downloaded to local_only/"**

**Agent will:**
- Validate schema (post-purchase schema inspection needed)
- Normalize team codes → Retrosheet
- Filter to 2024 season
- Run ≥100 rows join smoke

---

### Option D: AusSportsBetting [Free if terms acceptable]

**Time to ≥100 rows:** 1–2 days  
**Cost:** $0

**Steps:**

1. Visit in browser: https://www.aussportsbetting.com/terms-and-conditions/
2. Read terms carefully — determine if research use and download are permitted
3. If yes: visit https://www.aussportsbetting.com/data/historical-mlb-results-and-odds-data/
4. Download the data file
5. Move to: `data/research_odds/local_only/aussportsbetting_mlb.csv`
6. Tell the CTO agent: **"AusSportsBetting data downloaded. Terms allow research use."**

---

## 3. `.env` File Format

**Filename:** `.env` (must be in repo root)  
**This file MUST NOT be committed to git — it is gitignored.**

```
# The Odds API credentials — LOCAL ONLY, NEVER COMMIT
THE_ODDS_API_KEY=replace_me
```

**Do NOT:**
- ❌ Commit `.env` to git
- ❌ Share the key in chat, issues, or PRs
- ❌ Put the key anywhere in tracked files

**Gitignore status:** `.env` is already in `.gitignore` ✅

---

## 4. Forbidden Actions (Agent Will Refuse)

```
❌ Committing .env
❌ Committing raw odds JSON from The Odds API
❌ Committing raw CSV from any external provider (unless license explicitly permits)
❌ Committing transformed local-only contract CSV
❌ Pushing without explicit user YES
❌ Using fixture-only data (synthetic_no_license) as if it were real odds
❌ Making edge claims or production wagering decisions from this data
```

---

## 5. What Fetcher Script Does (If Key Ready)

Script: `scripts/fetch_odds_api_historical_mlb_2024_local.py`

```bash
# Dry run (no key needed, no API call):
python3 scripts/fetch_odds_api_historical_mlb_2024_local.py --dry-run --limit-days 2

# Execute 10 days of historical data (key required):
python3 scripts/fetch_odds_api_historical_mlb_2024_local.py \
  --start-date 2024-04-01 \
  --end-date 2024-04-10 \
  --execute

# Full 2024 season (key required, ~1,800 credits):
python3 scripts/fetch_odds_api_historical_mlb_2024_local.py \
  --start-date 2024-04-01 \
  --end-date 2024-09-30 \
  --execute
```

**Outputs (local-only, gitignored):**
- `data/research_odds/local_only/the_odds_api_2024/YYYY-MM-DD.json` (raw)
- `data/research_odds/local_only/the_odds_api_2024/MANIFEST.json`

---

## 6. Credit Usage Estimate (The Odds API)

| Scope | Calls | Credits | Cost (20K plan) |
|---|---|---|---|
| 10-day smoke test | 10 | 100 | Well within quota |
| Full 2024 season (per-day batch) | ~180 | 1,800 | Well within quota |
| True closing per game | ~2,187 | 21,870 | 2 months × $30 |

**Recommended for first run:** 10-day window (~100 credits)

---

## 7. Next Session Resume Instructions

When ready, start next session with:

> "KEY_READY: The Odds API key is in `.env` as `THE_ODDS_API_KEY`. Please execute P3.2 TRACK 2B → fetch 10 days → transform → ≥100 row join smoke → CLV benchmark."

OR:

> "DATA_READY: I dropped a CSV to `data/research_odds/local_only/`. Please validate schema, run join smoke, and compute CLV benchmark."

---

## 8. Acceptance Marker

```
P32_OPERATOR_ACTION_PACKET_READY_20260515
```
