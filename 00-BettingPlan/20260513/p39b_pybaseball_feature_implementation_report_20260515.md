# P39B — Pybaseball Rolling Feature Implementation Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Prev Version**: `p39a_pybaseball_skeleton_v1`  
**This Version**: `p39b_pybaseball_rolling_v1`

---

## Objective

Upgrade the P39A skeleton script to a working rolling feature core:
implement `build_team_daily_statcast_aggregates` and `build_rolling_features`,
harden leakage guardrails with keyword-based odds detection, and deliver
validated unit tests for all invariants.

---

## Changes vs. P39A

### Script: `scripts/build_pybaseball_pregame_features_2024.py`

| Change | Details |
|--------|---------|
| `SCRIPT_VERSION` | `p39a_pybaseball_skeleton_v1` → `p39b_pybaseball_rolling_v1` |
| Added `PREV_VERSION` | `p39a_pybaseball_skeleton_v1` |
| Added `FORBIDDEN_ODDS_KEYWORDS` | 6 keyword substrings for case-insensitive column detection |
| Added `REQUIRED_STATCAST_COLS` | `{game_date, game_pk, inning_topbot, home_team, away_team}` |
| Expanded `FORBIDDEN_ODDS_COLUMNS` | Added: spread, over_under, sportsbook, line_move, sharp_money |
| Hardened `assert_no_odds_columns` | Exact + keyword substring check (catches `home_odds`, `sportsbook_id`, etc.) |
| **New**: `build_team_daily_statcast_aggregates` | Statcast pitch-level → team-day batting stats |
| **New**: `build_rolling_features` | Team-day → rolling window features with leakage assertion |
| Updated `summarize_statcast_frame` | Now uses both exact + keyword odds detection |
| Updated `fetch_statcast_range` | Added `pybaseball.cache.enable()` call |
| Updated `build_feature_summary_only` | Added `implemented_features` list to output |
| Updated `main()` summary-only | Prints both P39B and P39A markers |
| Updated `main()` execute mode | Full pipeline: Statcast → aggregates → rolling features |

### New Functions

#### `build_team_daily_statcast_aggregates(df) -> pd.DataFrame`

Groups Statcast pitch-level data by `(game_date, game_pk, batting_team)`.

**Batting team derivation:**
- `inning_topbot == "Top"` → `away_team` bats
- `inning_topbot == "Bot"` → `home_team` bats

**Output columns per group:**

| Column | Source | Fail-soft? |
|--------|--------|-----------|
| `game_date` | str YYYY-MM-DD | required |
| `team` | str | required |
| `game_pk` | int | required |
| `plate_appearances_proxy` | `events.notna().sum()` | yes (None if no events col) |
| `batted_balls` | `launch_speed.notna().sum()` | yes |
| `avg_launch_speed` | mean of non-null ls | yes |
| `avg_launch_angle` | mean of non-null la (requires both ls + la) | yes |
| `avg_estimated_woba_using_speedangle` | mean of non-null xwOBA | yes |
| `hard_hit_rate_proxy` | fraction with ls >= 95 mph | yes |
| `barrel_rate_proxy` | fraction with ls >= 98 AND 26 <= angle <= 30 | yes |
| `avg_release_speed_against` | mean release_speed faced | yes |
| `source` | "pybaseball_statcast" | always |

#### `build_rolling_features(team_daily_df, as_of_dates, window_days) -> pd.DataFrame`

For each `(as_of_date, team)` pair:

```
window_end   = as_of_date - 1           (strict D-1 cutoff)
window_start = window_end - window_days + 1
```

**Hard assertion** (raises `RuntimeError` if violated):
```python
validate_feature_window(as_of, window_end)  # must return True
```

**Output columns:**

| Column | Description |
|--------|-------------|
| `as_of_date` | Python date |
| `team` | str |
| `feature_window_start` | date |
| `feature_window_end` | date (always < as_of_date) |
| `window_days` | int |
| `sample_size` | int (game-days in window) |
| `leakage_status` | "pregame_safe" |
| `rolling_pa_proxy` | sum of plate_appearances_proxy |
| `rolling_avg_launch_speed` | mean avg_launch_speed |
| `rolling_hard_hit_rate_proxy` | mean hard_hit_rate_proxy |
| `rolling_barrel_rate_proxy` | mean barrel_rate_proxy |

---

## Hardened Odds Boundary

`assert_no_odds_columns` now performs **two layers** of checks:

1. **Exact match** against `FORBIDDEN_ODDS_COLUMNS` (18 columns)
2. **Keyword substring** match against `FORBIDDEN_ODDS_KEYWORDS`:
   - `odds`, `moneyline`, `spread`, `sportsbook`, `vig`, `implied`
   - Case-insensitive — catches `home_odds`, `sportsbook_id`, `implied_woba`, etc.

Both `build_team_daily_statcast_aggregates` and `build_rolling_features` call this guard before returning.

---

## Test Coverage

### `tests/test_p39b_pybaseball_leakage_policy.py` (11 tests)

- `validate_feature_window`: D-1 accept, same-day reject, future reject
- `assert_no_odds_columns`: baseball stats accept, odds/moneyline/sportsbook reject
- `build_rolling_features`: as_of_date row excluded, window_end < as_of_date for all rows, empty fail-soft

### `tests/test_p39b_pybaseball_feature_aggregation.py` (9 tests)

- Row count (2 teams → 2 rows)
- `avg_launch_speed` = (98+85+107)/3 ≈ 96.667
- `hard_hit_rate_proxy` = 2/3 ≈ 0.667
- `barrel_rate_proxy` = 1/3 ≈ 0.333
- Missing optional columns fail-soft (no crash, None values)
- No odds columns in output
- `rolling_sample_size` correct (1 game-day in window)
- Deterministic hash (same input → same output hash)

**Total: 20/20 PASS**

---

## Invariants Validated

| Invariant | Status |
|-----------|--------|
| `window_end = as_of_date - 1` (strict D-1) | ✅ CONFIRMED |
| as_of_date row never in window | ✅ CONFIRMED |
| Odds cols rejected (exact + keyword) | ✅ CONFIRMED |
| Barrel proxy formula correct | ✅ CONFIRMED |
| Hard-hit proxy formula correct | ✅ CONFIRMED |
| Empty input fail-soft | ✅ CONFIRMED |
| No network calls in unit tests | ✅ CONFIRMED |
| Deterministic output | ✅ CONFIRMED |
| PAPER_ONLY = True | ✅ CONFIRMED |
| pybaseball does NOT provide odds | ✅ CONFIRMED |

---

## Files Changed / Created

| File | Action |
|------|--------|
| `scripts/build_pybaseball_pregame_features_2024.py` | Upgraded (P39A → P39B) |
| `tests/test_p39b_pybaseball_leakage_policy.py` | Created (11 tests) |
| `tests/test_p39b_pybaseball_feature_aggregation.py` | Created (9 tests) |
| `00-BettingPlan/20260513/p39b_pybaseball_rolling_feature_smoke_report_20260515.md` | Created |
| `00-BettingPlan/20260513/p39b_pybaseball_feature_implementation_report_20260515.md` | Created (this file) |

---

## Acceptance Markers

- `P39B_ROLLING_FEATURE_CORE_READY_20260515` — script prints in summary-only mode ✅
- `P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515` — backward compat marker still prints ✅
- `P39B_LEAKAGE_POLICY_TESTS_PASS_20260515` — 11/11 tests pass ✅
- `P39B_FEATURE_AGGREGATION_TESTS_PASS_20260515` — 9/9 tests pass ✅
- `P39B_PYBASEBALL_ROLLING_FEATURE_SMOKE_PASS_20260515` — smoke PASS ✅

---

**P39B_PYBASEBALL_FEATURE_IMPLEMENTATION_REPORT_20260515_READY**
