# P39J Pitcher Feature Pilot Scope
**Date:** 2026-05-15  
**Status:** DEFERRED — no `CTO_DECISION: run pitcher feature pilot` signal received  
**paper_only:** True | **production_ready:** False

---

## Context

P39I confirmed that Statcast batting rolling features (launch speed, hard-hit rate, barrel rate) do **not** robustly improve P38A baseline Brier. The batting track is frozen.

This document scopes what a pitcher-feature pilot (P39K) would look like **if** the CTO decides to continue feature research rather than waiting for odds unblock.

---

## Why Pitcher Features May Be More Promising

| Dimension | Batting Rolling | Pitcher-Level |
|-----------|----------------|---------------|
| Outcome driver | Partial (offense) | Direct (run prevention, starter quality) |
| Pregame predictability | Moderate | High (probable starter known) |
| Statcast availability | Yes (team-level) | Yes (pitcher-level FIP, ERA, xFIP) |
| Retrosheet proxy | Scoring rate | Won't get individual pitcher ERA without pybaseball |
| Signal hypothesis | Weak (shown by P39H/I) | Stronger — starter quality is the strongest pregame known factor |
| Already tested | Yes — NO_ROBUST_IMPROVEMENT | No |

**Key insight**: MLB game outcome correlates most strongly with starting pitcher quality. The P38A logistic model currently has no pitcher-level features — only team-level rolling winrate and run differential (from the base Retrosheet model). This is the most underexplored dimension.

---

## Candidate Features for P39K

### Group 1 — Probable Starter Rolling Performance
| Feature | Definition | Leakage-safe? |
|---------|-----------|--------------|
| `home_starter_era_rolling_10g` | Home SP ERA over last 10 starts (before game_date) | ✅ |
| `away_starter_era_rolling_10g` | Away SP ERA over last 10 starts | ✅ |
| `home_starter_fip_rolling_10g` | Home SP FIP over last 10 starts | ✅ |
| `away_starter_fip_rolling_10g` | Away SP FIP | ✅ |
| `diff_starter_era` | away_era - home_era | ✅ |
| `diff_starter_fip` | away_fip - home_fip | ✅ |

### Group 2 — Starter Workload / Rest
| Feature | Definition | Leakage-safe? |
|---------|-----------|--------------|
| `home_starter_days_rest` | Days since home SP last pitched | ✅ |
| `away_starter_days_rest` | Days since away SP last pitched | ✅ |
| `home_starter_pitch_count_last` | Pitch count in last start | ✅ |
| `away_starter_pitch_count_last` | Pitch count in last start | ✅ |

### Group 3 — Bullpen Workload Proxy
| Feature | Definition | Leakage-safe? |
|---------|-----------|--------------|
| `home_bullpen_ip_rolling_3d` | Home bullpen innings pitched last 3 days | ✅ |
| `away_bullpen_ip_rolling_3d` | Away bullpen IP last 3 days | ✅ |
| `home_bullpen_era_rolling_7g` | Home relief ERA last 7 games | ✅ |
| `away_bullpen_era_rolling_7g` | Away relief ERA last 7 games | ✅ |

---

## Required Source Feasibility

| Source | Coverage | Cost | Availability |
|--------|---------|------|-------------|
| `pybaseball.pitching_stats()` | Season-level FIP/ERA by pitcher | Free | ✅ Available |
| `pybaseball.statcast_pitcher()` | Pitch-level data by pitcher | Free | ✅ Available (slow) |
| `pybaseball.pitching_stats_bref()` | B-Ref rolling stats | Free | ✅ Available |
| Retrosheet game logs | Starting pitcher per game | Free | ✅ Available (P32 already parsed) |
| MLB Stats API | Game-by-game pitcher usage | Free | ✅ Available |

**Key dependency**: Need a `game_id → probable_starter` mapping for 2024. Sources:
1. Retrosheet GL2024: field 101 (home pitcher), field 102 (away pitcher)
2. MLB Stats API: `schedule` endpoint with `hydrate=probablePitcher`

P32 Retrosheet parser already extracts these fields — they just weren't used in P38A feature set.

---

## Non-Goals for P39K

- No full implementation without CTO approval (`CTO_DECISION: run pitcher feature pilot`)
- No odds / CLV calculation
- No production edge claim
- No model deployment
- No live game data
- No committed raw pybaseball pitcher data

---

## P39K Task Structure If Approved

```
P39K-A: Extract probable starter from Retrosheet GL2024 (P32 already parsed, reuse)
P39K-B: Fetch pitcher ERA/FIP rolling via pybaseball — local-only, gitignored
P39K-C: Join to P38A OOF rows (same bridge pattern as P39F/G)
P39K-D: Walk-forward ablation (reuse P39I script, new feature groups)
P39K-E: If ROBUST_IMPROVEMENT → proceed to calibration
         If NO_ROBUST_IMPROVEMENT → freeze feature track entirely, wait for P3 odds
```

**Estimated sessions**: 2–3 rounds (P39K-A through P39K-C = 1 session; P39K-D/E = 1 session).

---

## CTO Signal Required

To activate P39K:
```
CTO_DECISION: run pitcher feature pilot
```

Without this signal, the pitcher feature pilot remains in DEFERRED state.

---

## Acceptance Marker

`P39J_PITCHER_FEATURE_PILOT_DEFERRED_20260515`
