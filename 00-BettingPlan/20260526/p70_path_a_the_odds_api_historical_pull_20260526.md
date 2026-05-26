# P70 BettingPlan — PATH_A: The Odds API Historical Pull
**Date**: 2026-05-26 | **Classification**: `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY`

---

## Status

| Item | Value |
|---|---|
| Mode | DRY_RUN (no API key in .env) |
| CEO Authorization | ✅ Confirmed 2026-05-26 |
| Script | `scripts/_p70_path_a_the_odds_api_historical_pull.py` ✅ |
| Tests | 51 PASS (P70) / 389 PASS (cumulative) ✅ |
| paid_api_called | `False` (dry-run) |
| Output CSV | Not yet written (awaiting key) |

---

## Pull Configuration

- Sport: `baseball_mlb`
- Season: `2024-03-20` → `2024-09-29`
- Market: `h2h` (moneyline only)
- Bookmakers: pinnacle → draftkings → fanduel → betmgm
- Estimated rows: ~2,430
- Output: `data/mlb_2025/mlb_odds_2024_real.csv`

---

## Action Required to Execute Pull

```
1. Register at https://the-odds-api.com (~$30–50)
2. Add to .env: THE_ODDS_API_KEY=<your_key>
3. Run: .venv/bin/python scripts/_p70_path_a_the_odds_api_historical_pull.py
   → Script auto-detects key → LIVE mode → writes CSV
```

---

## Governance

`paper_only=True` | `real_bet_allowed=False` | `kelly_deploy_allowed=False` | `production_ready=False`  
Platt: A=0.435432, B=0.245464 (unchanged)

---

## Next Step

**P71** — Once `THE_ODDS_API_KEY` is configured, execute live pull → validate CSV → run P43 cross-year bootstrap CI.
