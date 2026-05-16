# P39J P3 Odds Unblock Assessment
**Date:** 2026-05-15  
**paper_only:** True | **production_ready:** False

---

## Current P3 Status

| Item | Status |
|------|--------|
| Operator decision gate | `OPERATOR_DECISION_PENDING` |
| THE_ODDS_API_KEY in .env | ❌ Not present |
| Local odds CSV in data/research_odds/local_only/ | ❌ Not present |
| True pregame moneyline odds | ❌ Not available |
| CLV benchmark | ❌ Not possible without odds |
| EV calculation | ❌ Not possible without odds |

---

## Why P3 Odds Is Now the Highest-ROI Next Step

### 1. Feature enrichment track exhausted (batting rolling)

P39 conducted 4 rounds of Statcast batting rolling feature work:
- P39B–D: feature engineering + join certification
- P39G: full-season enrichment (2187 rows)
- P39H: single time-aware split → INCONCLUSIVE
- P39I: 4-fold walk-forward ablation → **NO_ROBUST_IMPROVEMENT** (all ΔBrier > 0)

Result: batting quality rolling averages do not improve Brier over the logistic P38A baseline. The model-only feature axis has diminishing returns without external market signal.

### 2. The fundamental evaluation gap

Even if a future feature set improved Brier by −0.005 (a large jump), **we cannot determine**:
- Whether the model has a positive edge vs. the market
- What the closing line value (CLV) is
- Which games to bet, and at what size (Kelly requires p_market)
- Whether observed Brier improvement survives against closing odds

Without odds: Brier improvement = academic research. With odds: Brier improvement = monetizable edge.

### 3. TSL moneyline schema is ready

The TSL market schema (P38, `wbc_backend/markets/tsl_market_schema.py`) defines:
- `MONEYLINE_HOME_AWAY` with `is_paper_implemented=True`
- Odds fields: `odds_home_ml`, `odds_away_ml`
- Settlement semantics defined

The schema is waiting for actual odds data. The pipe is built; the source is missing.

---

## Unblock Paths

### Path A — The Odds API (Recommended for Speed)

| Item | Detail |
|------|--------|
| Provider | [The Odds API](https://the-odds-api.com) |
| Coverage | MLB moneyline, run line, totals |
| Historical data | Available on paid plans (Essential+) |
| Free tier | 500 requests/month (not enough for 2424 games) |
| Key env var | `THE_ODDS_API_KEY` in `.env` |
| Existing script | `scripts/fetch_odds_from_api.py` (P3.2, dry-run mode) |
| Cost estimate | ~$49/month for Essential plan |
| What CTO does | Sign up → copy key → add to `.env` as `THE_ODDS_API_KEY` |
| Agent signal | `KEY_READY: The Odds API key is in .env as THE_ODDS_API_KEY` |

If KEY_READY:
```bash
# Agent resumes P3.7 odds fetch pipeline:
PYTHONPATH=. .venv/bin/python scripts/fetch_odds_from_api.py \
  --sport baseball_mlb --season 2024 --paper-only
```

### Path B — Local CSV Drop (Zero Spend)

| Item | Detail |
|------|--------|
| What | Operator drops a CSV with historical 2024 MLB moneyline odds |
| Target path | `data/research_odds/local_only/` |
| Expected schema | game_date, home_team, away_team, odds_home_ml, odds_away_ml |
| Source examples | Betfair historical data, Pinnacle export, SBR odds archive |
| Cost | $0 (if operator has access) |
| What CTO does | Obtain CSV → drop to `data/research_odds/local_only/` |
| Agent signal | `DATA_READY: I dropped a CSV to data/research_odds/local_only/` |

If DATA_READY:
```bash
# Agent validates schema and runs join smoke:
PYTHONPATH=. .venv/bin/python scripts/validate_odds_csv_import.py \
  --input data/research_odds/local_only/ --paper-only
```

### Path C — Paid Historical Provider (Higher Quality, Slower)

| Provider | Notes |
|----------|-------|
| Pinnacle historical | Best closing line quality; requires bespoke arrangement |
| SportRadar | Enterprise; expensive |
| RundownAPI | ~$20/month, decent MLB coverage |
| Sportradar odds | Reseller model; months to contract |

Timeline: 2–8 weeks. Not recommended as first step.

### Path D — Manual Import Contract

- CTO manually records ~50 upcoming games with closing lines
- Follows P37.5 manual odds approval package format
- Allows smoke-test of the full CLV pipeline on small N
- Limitation: backward-looking CLV impossible without historical data

---

## What Happens After Unblock

```
P3 odds → join to P38A OOF rows → CLV = p_model - p_implied(odds)
       → Kelly fraction → paper ledger paper recommendation
       → EV calculation → ROI simulation
       → P39J+ calibration validation with real market
```

This is the path to production-quality evaluation. Nothing in P38/P39 feature work is a substitute.

---

## If Neither KEY_READY Nor DATA_READY

**No action taken.** This assessment document is the terminal artifact for P3 until an operator signal is received.

**Commitment**: Do not create further gate-only blocking documents for P3. This is the final assessment until a signal changes the state.

---

## Acceptance Marker

`P39J_P3_ODDS_UNBLOCK_ASSESSMENT_READY_20260515`
