# pybaseball Research Data Smoke Report — 2026-05-15

**Task Round:** P3.7A — TRACK 2  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Script:** `scripts/pybaseball_research_data_smoke_2024.py`  
**Script version:** `p37a_pybaseball_smoke_v1`  
**Run timestamp:** 2026-05-15T05:20:03Z  
**Date range tested:** 2024-04-01 → 2024-04-03

---

## 1. Overall Result

**PASS**

Statcast primary smoke succeeded. Team batting secondary smoke failed due to FanGraphs 403 (expected scraping risk).

---

## 2. Statcast Smoke

| Item | Value |
|---|---|
| Source | Baseball Savant (via pybaseball `statcast()`) |
| Date range requested | 2024-04-01 → 2024-04-03 |
| Date range actual | 2024-04-01 → 2024-04-03 |
| Rows | **11,662** |
| Columns | **118** |
| Sample columns | `pitch_type`, `game_date`, `release_speed`, `release_pos_x`, `release_pos_z`, `player_name`, `batter`, `pitcher`, `events`, `description` |
| Odds boundary | **CONFIRMED** — no odds columns present |
| Status | **PASS** |

### Odds Boundary Confirmation

The following forbidden columns were checked and **none were found**:

- `moneyline`, `closing_line`, `odds`, `vig`, `implied_prob`
- `home_ml`, `away_ml`, `home_odds`, `away_odds`, `clv`

> ✅ pybaseball Statcast data contains **zero betting odds columns**.
> This is pure baseball statistics (pitch velocity, spin rate, launch angle, etc.)

---

## 3. Team Batting Smoke

| Item | Value |
|---|---|
| Source | FanGraphs (via pybaseball `team_batting()`) |
| Season | 2024 |
| Status | **FAIL** |
| Error | `HTTPError: 403 from https://www.fangraphs.com/leaders-legacy.aspx` |
| Root cause | FanGraphs blocks scraping bots; this is a known pybaseball risk |
| Impact | Low — Statcast (Baseball Savant) is the primary stat source |

---

## 4. Data Source Classification

| Source | Available | Status |
|---|---|---|
| Baseball Savant (Statcast pitch-level) | ✅ | PASS |
| FanGraphs team batting | ❌ | 403 blocked |
| Baseball Reference | Not tested | N/A |

---

## 5. Betting Odds Boundary (Critical)

> **pybaseball does NOT provide betting odds.**
>
> - No moneyline data
> - No closing line data
> - No sportsbook prices
> - No CLV reference prices
>
> This output is **baseball statistics only**.
> It CANNOT be used as an odds source for P3 CLV benchmark.

---

## 6. Raw Data

Raw data was NOT written this round (`--summary-only` mode).  
If raw data write is needed, use `--write-local` flag.  
Raw data target: `data/pybaseball/local_only/` (gitignored, line 85 of `.gitignore`)

---

## 7. Acceptance Marker

```
PYBASEBALL_RESEARCH_DATA_SMOKE_PASS_20260515
```
