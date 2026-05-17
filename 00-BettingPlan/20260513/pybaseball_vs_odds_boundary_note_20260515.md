# pybaseball vs. Odds Data — Boundary Note — 2026-05-15

**Task Round:** P3.7A — TRACK 4  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Generated:** 2026-05-15

---

## 1. What pybaseball CAN Do

| Capability | Status |
|---|---|
| Fetch Statcast pitch-level data (Baseball Savant) | ✅ CONFIRMED (11,662 rows in 3-day smoke) |
| Fetch per-pitcher / per-batter Statcast | ✅ Available |
| Rolling batting / pitching stat features | ✅ Available (with pregame-safe cutoff) |
| Team schedule / record proxy | ✅ Available |
| Player ID cross-reference | ✅ Available |
| Serve as feature input for P38A / P39 | ✅ YES — as research enrichment |
| FanGraphs team batting (anti-scraping) | ⚠️ 403 in smoke — known risk |

---

## 2. What pybaseball CANNOT Do

| Item | Status |
|---|---|
| Provide moneyline odds | ❌ IMPOSSIBLE — not a sportsbook data source |
| Provide closing line / opening line | ❌ IMPOSSIBLE |
| Provide implied probability from vig | ❌ IMPOSSIBLE |
| Provide CLV reference price | ❌ IMPOSSIBLE |
| Replace The Odds API | ❌ IMPOSSIBLE |
| Replace licensed odds provider | ❌ IMPOSSIBLE |
| Serve as P3 odds source | ❌ NOT APPLICABLE |

---

## 3. P3 Odds Source Blocker — Still Active

The P3 odds pipeline blocker is **independent of pybaseball** and remains unresolved:

| Blocker | Status |
|---|---|
| `.env` / `THE_ODDS_API_KEY` | NOT PRESENT |
| `data/research_odds/local_only/` CSV | EMPTY |
| The Odds API paid subscription | Operator decision required |
| 6 local commits push to `origin/p13-clean` | Awaiting explicit YES |

**P3 final classification remains:** `OPERATOR_DECISION_PENDING`

---

## 4. Correct Role of pybaseball in This Research Stack

```
┌─────────────────────────────────────────────────────────┐
│              Research Stack Boundary Map                │
├─────────────────────────────┬───────────────────────────┤
│ pybaseball (this adapter)   │ P3 Odds Pipeline          │
│                             │                           │
│ • Baseball statistics       │ • Moneyline odds          │
│ • Statcast pitch data       │ • Sportsbook prices       │
│ • Team batting / pitching   │ • No-vig probability      │
│ • Schedule / records        │ • CLV reference           │
│ • Feature enrichment (P39)  │                           │
│                             │ Source: The Odds API      │
│ Source: Baseball Savant /   │ or licensed CSV provider  │
│   FanGraphs / BaseballRef   │                           │
├─────────────────────────────┴───────────────────────────┤
│         These two pipelines DO NOT overlap              │
│  pybaseball CANNOT substitute for odds data             │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Unlock Paths (Unchanged)

### For pybaseball feature enrichment (P39 path — NOW UNBLOCKED):
```
P3.7A smoke: PASS → P3.8 build rolling feature pipeline
```

### For P3 odds CLV benchmark (still blocked — requires one of):
```
Option A: YES: push the 6 local commits on p13-clean to origin
Option B: KEY_READY: The Odds API key is in .env as THE_ODDS_API_KEY. Please execute P3.8.
Option C: DATA_READY: I dropped a CSV to data/research_odds/local_only/. Please execute P3.8.
```

---

## 6. Fallback Note for pybaseball

If pybaseball smoke fails in future rounds:

| Failure Mode | Cause | Fallback |
|---|---|---|
| 403 on FanGraphs | Anti-scraping block | Use Statcast only (Baseball Savant) |
| 403 on Baseball Savant | Rate limit | Reduce date range, add cache |
| Schema drift | pybaseball version change | Pin version, update column mapping |
| Total outage | External site down | Use pre-cached parquet from `local_only/` |

---

## 7. Acceptance Marker

```
PYBASEBALL_ODDS_BOUNDARY_NOTE_20260515_READY
```
