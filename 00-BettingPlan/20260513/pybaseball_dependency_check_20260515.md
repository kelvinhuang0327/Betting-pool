# pybaseball Dependency Check — 2026-05-15

**Task Round:** P3.7A — TRACK 1  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Generated:** 2026-05-15

---

## 1. Installation Status

| Item | Value |
|---|---|
| pybaseball installed | **YES** |
| Version | **2.2.7** |
| Install target | `.venv` (project virtual environment) |
| Install command | `.venv/bin/pip install pybaseball` |
| Source repo | https://github.com/jldbc/pybaseball |
| requirements.txt updated | YES — `pybaseball>=2.2.7` added |

### Dependencies installed alongside pybaseball 2.2.7

| Package | Version |
|---|---|
| pybaseball | 2.2.7 |
| pyarrow | 24.0.0 |
| beautifulsoup4 | 4.14.3 |
| lxml | 6.1.0 |
| tqdm | 4.67.3 |
| pygithub | 2.9.1 |
| cryptography | 48.0.0 |

---

## 2. Known Risks

| Risk | Description |
|---|---|
| Scraping dependency | pybaseball scrapes Baseball Reference, FanGraphs, Baseball Savant — external website layout changes may break fetches |
| 403 / rate limit | Baseball Reference blocks aggressive requests; pybaseball's cache mitigates this |
| Schema drift | Column names may change between pybaseball versions or if source sites restructure |
| Network dependency | Requires live internet connection; no offline mode |
| Data freshness | Statcast data typically has 1-2 day lag; game day data may be incomplete |

---

## 3. Explicit Data Boundary Declaration

> **pybaseball does NOT provide betting odds.**
>
> pybaseball sources: Baseball Reference, FanGraphs, Baseball Savant (Statcast).
> None of these sources provide moneyline odds, closing odds, sportsbook prices,
> or CLV reference prices.
>
> This adapter is classified as: **research-only baseball statistics**
> It CANNOT serve as an odds source for P3 CLV benchmark.
> It CANNOT replace The Odds API or any licensed sportsbook odds provider.
> It CAN serve as feature enrichment input for P38A / P39 model validation.

---

## 4. Acceptance Marker

```
PYBASEBALL_DEPENDENCY_CHECK_20260515_READY
```
