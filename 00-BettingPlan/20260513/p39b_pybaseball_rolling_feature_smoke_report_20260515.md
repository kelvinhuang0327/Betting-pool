# P39B — Pybaseball Rolling Feature Smoke Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Script**: `scripts/build_pybaseball_pregame_features_2024.py`  
**Script Version**: `p39b_pybaseball_rolling_v1`

---

## Summary-Only Smoke (offline, no network)

**Command:**
```bash
.venv/bin/python scripts/build_pybaseball_pregame_features_2024.py \
  --summary-only --start-date 2024-04-01 --end-date 2024-04-03 --window-days 7
```

**Result:** PASS

**Key output:**
```
  script_version                      : p39b_pybaseball_rolling_v1
  paper_only                          : True
  date_range                          : {'start': '2024-04-01', 'end': '2024-04-03', 'n_days': 3}
  rolling_window_days                 : 7
  sample_window_check                 : {'game_date': '2024-04-01', 'window_start': '2024-03-25', 'window_end': '2024-03-31', 'pregame_safe': True}
  implemented_features                : 12 rolling + batted-ball features
  odds_boundary                       : CONFIRMED (design: no odds columns)
  leakage_violations                  : 0
  Summary hash                        : 56a9d8592657e8a9
  Pregame-safe                        : CONFIRMED
  Odds boundary                       : CONFIRMED
  Marker: P39B_ROLLING_FEATURE_CORE_READY_20260515
  Marker: P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515
```

**Pregame-safe window verification:**
- `game_date = 2024-04-01`
- `window_end = 2024-03-31` (D-1, strictly before game_date ✅)
- `window_start = 2024-03-25` (7-day lookback ✅)

---

## Pytest Run — P39B Tests (20 tests)

**Command:**
```bash
.venv/bin/pytest tests/test_p39b_pybaseball_leakage_policy.py tests/test_p39b_pybaseball_feature_aggregation.py -v
```

**Result:** 20 passed in 2.57s

### Leakage Policy Tests (11 tests — PASS)

| Test | Result |
|------|--------|
| `test_validate_window_accepts_d_minus_1` | PASS |
| `test_validate_window_rejects_same_day` | PASS |
| `test_validate_window_rejects_future` | PASS |
| `test_assert_no_odds_columns_accepts_baseball_stats` | PASS |
| `test_assert_no_odds_columns_rejects_odds_keyword` | PASS |
| `test_assert_no_odds_columns_rejects_moneyline_keyword` | PASS |
| `test_assert_no_odds_columns_rejects_sportsbook_keyword` | PASS |
| `test_rolling_features_exclude_as_of_date_rows` | PASS |
| `test_rolling_features_window_end_before_as_of_date` | PASS |
| `test_rolling_features_empty_input_fail_soft` | PASS |
| `test_acceptance_marker` | PASS |

Acceptance marker: `P39B_LEAKAGE_POLICY_TESTS_PASS_20260515`

### Feature Aggregation Tests (9 tests — PASS)

| Test | Result |
|------|--------|
| `test_team_daily_row_count` | PASS |
| `test_avg_launch_speed` | PASS |
| `test_hard_hit_rate_proxy` | PASS |
| `test_barrel_rate_proxy` | PASS |
| `test_missing_optional_columns_fail_soft` | PASS |
| `test_no_odds_columns_in_output` | PASS |
| `test_rolling_sample_size` | PASS |
| `test_deterministic_output_hash` | PASS |
| `test_acceptance_marker` | PASS |

Acceptance marker: `P39B_FEATURE_AGGREGATION_TESTS_PASS_20260515`

---

## Verified Invariants

| Invariant | Status |
|-----------|--------|
| `window_end < game_date` (D-1 strict) enforced for all rows | ✅ CONFIRMED |
| `assert_no_odds_columns` rejects exact + keyword matches | ✅ CONFIRMED |
| `build_rolling_features` excludes as_of_date row from window | ✅ CONFIRMED |
| Empty input fail-soft returns empty DataFrame | ✅ CONFIRMED |
| Barrel proxy: launch_speed >= 98 AND 26 <= angle <= 30 | ✅ CONFIRMED |
| Hard-hit proxy: launch_speed >= 95 | ✅ CONFIRMED |
| Output is deterministic (same hash on repeat call) | ✅ CONFIRMED |
| No network calls in unit tests (synthetic fixture only) | ✅ CONFIRMED |

---

## Smoke Status

**P39B_PYBASEBALL_ROLLING_FEATURE_SMOKE_PASS_20260515**
