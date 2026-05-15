# P39D — Execution Scope Decision
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Author**: CTO Agent  
**Status**: RESEARCH ONLY — PAPER_ONLY=True, production_ready=False

---

## ⚠️ Mandatory Constraints

> - PAPER_ONLY=True on all P39D artifacts
> - No production write, no live betting, no odds ledger modification
> - Raw Statcast cache → `data/pybaseball/local_only/` (gitignored, NOT committed)
> - Generated local-only feature CSV → `data/pybaseball/local_only/` (NOT committed)
> - Only committable artifacts: synthetic fixtures, reports, script changes (no raw data)
> - No odds columns in any output
> - pybaseball does NOT provide odds / CLV

---

## 1. Selected Mode

**APRIL_SAMPLE_EXECUTION**

Rationale:
- Full 2024 season Statcast (~700k+ rows, ~30MB) requires sustained network and significant wall time.
- April 2024 subset (10 days = 2024-04-01 → 2024-04-10) is small enough to complete in < 3 minutes under normal network conditions.
- April sample covers the games in the P38A OOF fixture set used in P39C smoke.
- If April succeeds: full season expansion is well-defined (P39E).
- If April fails (403, timeout, rate-limit): fail-soft, produce deferred resume plan.

**FULL_SEASON_DEFERRED** — reserved for P39E, pending April sample success.  
**NETWORK_BLOCKED** — contingency if pybaseball returns 403 or sustained timeout.

---

## 2. Selected Date Range

| Parameter | Value |
|-----------|-------|
| start_date | `2024-04-01` |
| end_date | `2024-04-10` |
| Calendar days | 10 |
| Approx MLB games | ~40–45 (4-5 games/day × 10 days) |
| Approx Statcast rows | ~40,000–80,000 pitch events |
| Expected wall time | 30–120 seconds |

---

## 3. Window Configuration

| Parameter | Value |
|-----------|-------|
| window_days | 7 |
| window_end | `as_of_date - 1` (strict D-1) |
| window_start | `window_end - 6` |
| leakage_status | `pregame_safe` for all rows |

Rolling window covers prior-week team batting statistics. For games on 2024-04-01, the window will be empty or minimal (Spring Training data not in Statcast scope), so `sample_size` may be 0 for early dates.

---

## 4. Expected Output

### 4a. Team-Day Aggregates (intermediate, local-only)
- One row per `(game_date, game_pk, batting_team)`
- Columns: `game_date, team, game_pk, plate_appearances_proxy, batted_balls, avg_launch_speed, avg_launch_angle, avg_estimated_woba_using_speedangle, hard_hit_rate_proxy, barrel_rate_proxy, avg_release_speed_against, source`
- NOT committed

### 4b. Rolling Features (local-only CSV)
**Path**: `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv`

| Column | Description |
|--------|-------------|
| `as_of_date` | Game date for which feature is computed |
| `team` | Team code |
| `feature_window_start` | Rolling window start (D-7) |
| `feature_window_end` | Rolling window end (D-1) |
| `window_days` | 7 |
| `sample_size` | # game-days in window with data |
| `leakage_status` | Always `pregame_safe` |
| `rolling_pa_proxy` | Plate appearances in window |
| `rolling_avg_launch_speed` | Mean launch speed |
| `rolling_hard_hit_rate_proxy` | Hard-hit rate |
| `rolling_barrel_rate_proxy` | Barrel rate |

- NOT committed (gitignored path)
- Companion `.summary.json` also local-only

### 4c. Enriched P38A OOF Sample (local-only CSV)
**Path**: `data/pybaseball/local_only/p39d_enriched_p38a_sample_2024_04_01_04_10.csv`

P38A rows from 2024-04-01 → 2024-04-10 enriched with rolling features via P39C join utility.
- NOT committed

---

## 5. Raw Data Policy

| Rule | Detail |
|------|--------|
| Raw Statcast cache | `data/pybaseball/local_only/cache/` — gitignored |
| Generated feature CSV | `data/pybaseball/local_only/` — gitignored |
| Enriched P38A CSV | `data/pybaseball/local_only/` — gitignored |
| pybaseball library calls | Only inside `--execute` flag path |
| Summary JSON | `data/pybaseball/local_only/` — gitignored |
| Committable artifacts | Reports in `00-BettingPlan/20260513/`, script changes, tests |

Verified gitignore coverage:
```
data/pybaseball/local_only/   ← line 86 of .gitignore
```

---

## 6. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| pybaseball / Baseball Savant timeout | Medium | Smoke fails | Fail-soft → `P39D_REAL_PYBASEBALL_EXECUTE_SMOKE_FAILED_20260515`; retry with smaller date range |
| 403 / rate-limit from Baseball Savant | Medium | Smoke fails | Same fail-soft; consider --cache-dir replay |
| Schema drift (Statcast column names change) | Low | Aggregation breaks | `REQUIRED_STATCAST_COLS` check logs warning, returns empty; smoke still passes at infra level |
| Team code mismatch (CHA≠CHW, SDN≠SDP) | Medium | Low match rate | Normalization pass required in P39E |
| Early April 2024 window empty (no prior data) | High | `sample_size=0` for 2024-04-01→04-07 rows | Expected behavior; feature will be NaN, not a bug |
| Large memory usage (if April fetch is large) | Low | OOM on small machine | Chunked fetch not yet implemented; acceptable for 10-day scope |

---

## 7. Full Season Expansion Plan (P39E)

If April sample succeeds:
1. Expand date range to full 2024 season: `2024-03-20` → `2024-10-01`
2. Implement chunked monthly fetch to avoid timeouts (30-day chunks)
3. Concatenate monthly CSVs into full-season rolling feature file
4. Normalize team codes (add `data/mlb_2024/processed/mlb_team_code_normalization.csv`)
5. Enrich all 2,187 P38A OOF rows
6. Target: ≥ 80% home match rate, ≥ 80% away match rate
7. Report Brier improvement vs. P38A baseline

---

## Acceptance Marker

**P39D_EXECUTION_SCOPE_DECISION_20260515_READY**
