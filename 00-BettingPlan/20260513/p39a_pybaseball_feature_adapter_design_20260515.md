# P39A Pybaseball Feature Adapter — Design Document — 2026-05-15

**Task Round:** P3.8 / P39A — TRACK 1  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Precondition:** P3.7A smoke PASS (Statcast 11,662 rows, 2024-04-01→03, no odds columns)  
**Generated:** 2026-05-15

---

## 1. Purpose

Build a **research-only pregame-safe feature adapter** using pybaseball / Statcast data for:

- **P39 feature enrichment** — supplement P38A OOF logistic regression predictions with baseball statistics context
- Specifically: rolling batting, pitching, workload, and team form proxies derived exclusively from pre-game data

### Explicit Non-Goals (Critical Boundary)

| Item | Status |
|---|---|
| Provide moneyline odds | ❌ NOT THIS ADAPTER |
| Provide closing / opening odds | ❌ NOT THIS ADAPTER |
| Provide sportsbook prices | ❌ NOT THIS ADAPTER |
| Provide CLV reference | ❌ NOT THIS ADAPTER |
| Replace The Odds API | ❌ NOT THIS ADAPTER |
| Production betting signals | ❌ NOT THIS ADAPTER |
| Live betting data | ❌ NOT THIS ADAPTER |
| Claim model production edge | ❌ NOT THIS ADAPTER |

> **pybaseball is a baseball statistics library. It cannot serve as an odds source.**  
> P3 odds pipeline remains independently blocked (THE_ODDS_API_KEY absent).

---

## 2. Input Source

### Primary: Baseball Savant (Statcast)

| Property | Value |
|---|---|
| pybaseball function | `statcast(start_dt, end_dt)` |
| Source URL | `https://baseballsavant.mlb.com/` |
| Date range (initial build) | 2024-03-20 → 2024-09-30 (full MLB regular season) |
| Expected rows | ~3M+ pitch-level records for full season |
| Expected columns | 118 (smoke-verified) |
| Granularity | Pitch-level (one row per pitch) |
| Aggregation needed | Yes — must aggregate to game-date / team level |

### Key Input Columns (smoke-verified in P3.7A)

```
pitch_type       game_date        release_speed     release_pos_x
release_pos_z    player_name      batter            pitcher
events           description      launch_speed      launch_angle
estimated_woba_using_speedangle   hit_distance_sc   release_spin_rate
effective_speed  home_team        away_team         inning
```

### External Dependency Risk

| Risk | Level | Mitigation |
|---|---|---|
| Baseball Savant scraping block | Low (Baseball Savant generally open) | Cache locally, retry with backoff |
| FanGraphs 403 | HIGH (confirmed in P3.7A smoke) | Use Statcast only; skip FanGraphs path |
| pybaseball schema drift | Medium (version pinned to 2.2.7) | Validate column presence before aggregation |
| Rate limiting | Medium | Chunk requests by 3-day windows, add sleep |
| pybaseball version mismatch | Low (pinned in requirements.txt) | `assert pybaseball.__version__ >= "2.2.7"` |

---

## 3. Output Contract

Each row in the output feature table represents **one (game_date, team) pair with one feature value**.

### Schema

```
game_date            : YYYY-MM-DD  — the game being predicted
team                 : str         — retrosheet/MLB team code (e.g., "NYY", "LAD")
opponent             : str         — opponent team code
is_home              : bool        — True if team is home team
feature_window_start : YYYY-MM-DD  — start of rolling window (inclusive)
feature_window_end   : YYYY-MM-DD  — end of rolling window (must be < game_date)
source               : str         — "statcast" | "schedule"
feature_name         : str         — e.g. "team_hard_hit_rate_14d"
feature_value        : float       — numeric feature value
sample_size          : int         — number of games/pitches/PAs in window
generated_at         : ISO8601 UTC — generation timestamp
leakage_status       : str         — "pregame_safe" | "review_required" | "leakage_detected"
```

### Output File (research-only, local)

- Path: `data/pybaseball/local_only/p39a_features_2024_{date}.csv`
- Gitignored: `data/pybaseball/local_only/` (line 86 of `.gitignore`)
- Not committed to repo
- Must not contain: odds columns, moneyline, closing_line, vig, clv, implied_prob

---

## 4. Feature Families

### 4.1 Rolling Batting Proxies

| Feature Name | Derivation | Window |
|---|---|---|
| `team_batting_avg_Nd` | Hits / AB (from Statcast `events`) | 7d, 14d |
| `team_obp_proxy_Nd` | (H + BB) / (AB + BB + SF) proxy | 7d, 14d |
| `team_hard_hit_rate_Nd` | Pitches with `launch_speed >= 95 mph` / total batted balls | 7d, 14d |
| `team_k_rate_Nd` | `events == 'strikeout'` / total PA proxy | 7d, 14d |
| `team_bb_rate_Nd` | `events == 'walk'` / total PA proxy | 7d, 14d |
| `team_xwoba_mean_Nd` | Mean `estimated_woba_using_speedangle` | 7d, 14d |
| `team_barrel_rate_Nd` | Statcast barrel events / batted balls | 7d, 14d |

### 4.2 Rolling Pitching Proxies

| Feature Name | Derivation | Window |
|---|---|---|
| `sp_xwoba_allowed_L3` | SP `estimated_woba_using_speedangle` allowed — last 3 starts | L3 starts |
| `sp_k_rate_L3` | SP `events == 'strikeout'` / batters faced — last 3 starts | L3 starts |
| `sp_hard_hit_rate_allowed_L3` | `launch_speed >= 95` allowed by SP — last 3 starts | L3 starts |
| `sp_pitch_count_last_start` | Total pitches in SP's most recent start | Last start |
| `sp_rest_days` | Days since last start appearance | Exact |
| `team_bullpen_era_proxy_7d` | ERA proxy for relievers over last 7 days | 7d |
| `team_bullpen_ip_3d` | Inning count for bullpen last 3 days | 3d |

### 4.3 Starter / Bullpen Workload Proxies

| Feature Name | Derivation | Window |
|---|---|---|
| `bullpen_pitchers_used_2d` | Distinct relievers who threw ≥1 pitch | 2d |
| `bullpen_heavy_usage_flag` | Any reliever with ≥30 pitches in last 2 days | 2d |
| `sp_on_short_rest_flag` | `sp_rest_days <= 3` | Exact |
| `sp_on_extra_rest_flag` | `sp_rest_days >= 6` | Exact |

### 4.4 Recent Team Form Proxies

Derived from `statcast()` game-level aggregates:

| Feature Name | Derivation | Window |
|---|---|---|
| `team_run_differential_7d` | Sum of (runs scored - runs allowed) last 7 games | 7d |
| `team_win_rate_7d` | Win count / 7 (from aggregated outcomes) | 7d |
| `team_run_scored_avg_7d` | Mean runs scored last 7 games | 7d |
| `team_run_allowed_avg_7d` | Mean runs allowed last 7 games | 7d |

### 4.5 Statcast Aggregate Proxies

| Feature Name | Derivation |
|---|---|
| `team_exit_velocity_mean_14d` | Mean `launch_speed` on batted balls |
| `team_launch_angle_mean_14d` | Mean `launch_angle` on batted balls |
| `sp_release_speed_mean_L3` | SP's mean fastball velocity last 3 starts |
| `sp_spin_rate_mean_L3` | SP's mean `release_spin_rate` last 3 starts |

### 4.6 Schedule Density Proxies

| Feature Name | Derivation |
|---|---|
| `back_to_back_flag` | Game yesterday AND today (no rest) |
| `days_since_last_game` | Days since team's last game date |
| `games_in_last_7d` | Count of games in last 7 days |

---

## 5. Integration Path

```
pybaseball Statcast raw (pitch-level)
    ↓ aggregate to game-date / team level
    ↓ apply rolling windows (7d, 14d, L3)
    ↓ pregame-safe cutoff: window_end < game_date
    ↓ validate leakage_status = pregame_safe
    ↓
p39a_features_2024.csv (local_only, gitignored)
    ↓
P38A OOF predictions (p38a_2024_oof_predictions.csv)
    ↓ LEFT JOIN on game_date + team
    ↓
enriched_p38a_2024.csv → P39 calibration / backtest
```

**This pipeline does NOT touch:**
- Moneyline odds
- Sportsbook records
- CLV
- Any betting ledger

---

## 6. Acceptance Marker

```
P39A_PYBASEBALL_FEATURE_ADAPTER_DESIGN_20260515_READY
```
