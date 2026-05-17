# pybaseball Research Feature Contract — 2026-05-15

**Task Round:** P3.7A — TRACK 3  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Generated:** 2026-05-15

---

## 1. Data Sources Available via pybaseball

| Source | pybaseball Function | Notes |
|---|---|---|
| Statcast pitch-level | `statcast(start_dt, end_dt)` | Baseball Savant; 118+ columns; pitch-level granularity |
| Statcast batter | `statcast_batter(start_dt, end_dt, player_id)` | Per-batter Statcast |
| Statcast pitcher | `statcast_pitcher(start_dt, end_dt, player_id)` | Per-pitcher Statcast |
| FanGraphs batting | `batting_stats(start_season, end_season)` | FanGraphs; 403 risk |
| FanGraphs pitching | `pitching_stats(start_season, end_season)` | FanGraphs; 403 risk |
| Baseball Ref standings | `standings(season)` | Season standings |
| Player ID map | `playerid_lookup(last, first)` | Cross-source player ID |
| Schedule / results | `schedule_and_record(season, team)` | Win/loss record |

---

## 2. NOT Available via pybaseball

| Data Type | Status |
|---|---|
| Moneyline odds | ❌ NOT AVAILABLE |
| Closing line / opening line | ❌ NOT AVAILABLE |
| Sportsbook prices | ❌ NOT AVAILABLE |
| Vig / no-vig probability | ❌ NOT AVAILABLE |
| CLV reference price | ❌ NOT AVAILABLE |
| Live in-game betting data | ❌ NOT AVAILABLE |

> pybaseball is a **baseball statistics** library, not a sports betting data provider.

---

## 3. Candidate Features for P38A / P39 Enrichment

All features must pass pregame-safe rules (see Section 4).

### 3.1 Rolling Team Batting Features
| Feature | Source | Window |
|---|---|---|
| Team wRC+ (rolling N games) | Statcast / FanGraphs batting | 7/14/30 day |
| Team OBP (rolling) | Statcast `on_base_pct` | 7/14 day |
| Team ISO (rolling) | Statcast `isolated_power` | 7/14 day |
| Team K% (rolling) | Statcast | 7/14 day |
| Team BB% (rolling) | Statcast | 7/14 day |
| Hard hit rate (rolling) | Statcast `launch_speed >= 95` | 7/14 day |

### 3.2 Rolling Team Pitching Features
| Feature | Source | Window |
|---|---|---|
| SP ERA (rolling) | Statcast per pitcher | L3 starts |
| SP xFIP / SIERA proxy | Statcast `estimated_woba_using_speedangle` | L3 starts |
| Bullpen IP last N days | Statcast (pitcher) | 3/7 day |
| Bullpen ERA rolling | Statcast | 7 day |
| SP rest days | Schedule/game log | exact |

### 3.3 Workload / Bullpen Proxy
| Feature | Source |
|---|---|
| SP pitch count last game | Statcast |
| Bullpen pitchers used L2 days | Statcast |
| Consecutive heavy usage (>20 pitches) | Statcast |

### 3.4 Recent Form Proxy
| Feature | Source |
|---|---|
| Team W/L last 7 games | `schedule_and_record()` |
| Run differential last 7 games | Schedule record |
| Home/away splits | Statcast aggregate |

### 3.5 Schedule / Context
| Feature | Source |
|---|---|
| Rest days | Derived from game log |
| Back-to-back flag | Derived from schedule |
| Time zone travel proxy | Derived from team / venue |

---

## 4. Pregame-Safe Rules (Mandatory)

> **Data isolation is non-negotiable. No look-ahead leakage permitted.**

| Rule | Description |
|---|---|
| **Cutoff**: game_date | Any feature must use data with `data_date < game_date` only |
| **Rolling window**: closed on left | Window = `[game_date - N_days, game_date - 1_day]` |
| **No result leakage** | Do NOT use `events = home_run / strikeout` from the game being predicted |
| **No postgame Statcast** | Statcast data for game X must not appear in features for game X |
| **Starter identity** | Confirmed starting pitcher must be pregame-known; do not use actual starter if announced after cutoff |
| **leakage_status field** | Every feature row must carry `leakage_status = pregame_safe` |

---

## 5. Suggested Feature Output Schema

```
game_date         : YYYY-MM-DD (the game being predicted)
team              : retrosheet team code
opponent          : retrosheet team code
is_home           : bool
feature_window_start : YYYY-MM-DD
feature_window_end   : YYYY-MM-DD (must be < game_date)
stat_source       : statcast | fangraphs | schedule
feature_name      : str (e.g. "team_hard_hit_rate_14d")
feature_value     : float
generated_at      : ISO8601 UTC
leakage_status    : pregame_safe | review_required | leakage_detected
```

---

## 6. Integration Path (P39 Preview)

```
P38A OOF predictions
    + P3.7A pybaseball feature adapter
    → P39 feature enrichment pipeline
    → enriched_p38a_features_2024.csv
    → backtesting / calibration with baseball context
```

This is **NOT** a betting odds source. It does not replace The Odds API or any CLV benchmark source.

---

## 7. Acceptance Marker

```
PYBASEBALL_RESEARCH_FEATURE_CONTRACT_20260515_READY
```
