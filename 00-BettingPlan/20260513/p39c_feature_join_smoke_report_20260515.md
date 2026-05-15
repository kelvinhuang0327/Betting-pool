# P39C — Feature Join Smoke Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Mode**: FIXTURE (synthetic inline P38A + file-based P39B synthetic fixture)  
**Script**: `scripts/join_p38a_oof_with_p39b_features.py`  
**Script Version**: `p39c_feature_join_v1`

---

## Smoke Command

```bash
.venv/bin/python scripts/join_p38a_oof_with_p39b_features.py \
  --fixture-mode \
  --summary-only
```

---

## P38A Fixture (Synthetic Inline — 5 games)

| game_id | p_oof | game_date | home_team | away_team |
|---------|-------|-----------|-----------|-----------|
| BAL-20240415-0 | 0.52 | 2024-04-15 | BAL | BOS |
| NYY-20240416-0 | 0.61 | 2024-04-16 | NYY | TBR |
| HOU-20240417-0 | 0.45 | 2024-04-17 | HOU | LAA |
| ATL-20240418-0 | 0.58 | 2024-04-18 | ATL | NYM |
| CHC-20240419-0 | 0.50 | 2024-04-19 | CHC | MIL |

---

## P39B Fixture (`data/pybaseball/fixtures/P39C_SYNTHETIC_ROLLING_FEATURES_20260515.csv` — 10 rows)

| as_of_date | team | feature_window_end | leakage_status | rolling_avg_launch_speed |
|------------|------|--------------------|----------------|--------------------------|
| 2024-04-15 | BAL  | 2024-04-14         | pregame_safe   | 91.2 |
| 2024-04-15 | BOS  | 2024-04-14         | pregame_safe   | 93.4 |
| 2024-04-16 | NYY  | 2024-04-15         | pregame_safe   | 92.1 |
| 2024-04-16 | TBR  | 2024-04-15         | pregame_safe   | 89.5 |
| 2024-04-17 | HOU  | 2024-04-16         | pregame_safe   | 94.0 |
| 2024-04-17 | LAA  | 2024-04-16         | pregame_safe   | 88.3 |
| 2024-04-18 | ATL  | 2024-04-17         | pregame_safe   | 95.2 |
| 2024-04-18 | NYM  | 2024-04-17         | pregame_safe   | 90.7 |
| 2024-04-19 | CHC  | 2024-04-18         | pregame_safe   | 91.8 |
| 2024-04-19 | MIL  | 2024-04-18         | pregame_safe   | 90.1 |

---

## Smoke Output

```
P39C Join Utility — p39c_feature_join_v1
  prev_version  : p39b_pybaseball_rolling_v1
  PAPER_ONLY    : True
  mode          : FIXTURE (synthetic inline P38A + file-based P39B)
  p38a_rows     : 5
  p39b_path     : data/pybaseball/fixtures/P39C_SYNTHETIC_ROLLING_FEATURES_20260515.csv
  p39b_rows     : 10
  leakage_violations : 0
  joined_rows   : 5

  Join Summary:
    script_version                          : p39c_feature_join_v1
    paper_only                              : True
    total_p38a_rows                         : 5
    home_feature_match_count                : 5
    home_feature_match_rate                 : 1.0
    away_feature_match_count                : 5
    away_feature_match_rate                 : 1.0
    unmatched_home_count                    : 0
    unmatched_away_count                    : 0
    odds_boundary                           : CONFIRMED
    leakage_violations                      : 0
    deterministic_hash                      : a68c22490415d14d

  Marker: P39C_JOIN_UTILITY_READY_20260515
  PAPER_ONLY=True — no production write
```

---

## Verified Invariants

| Invariant | Status |
|-----------|--------|
| Home feature match rate = 100% | ✅ 5/5 |
| Away feature match rate = 100% | ✅ 5/5 |
| Leakage violations = 0 | ✅ 0 |
| `feature_window_end < as_of_date` for all 10 rows | ✅ confirmed (D-1 strict) |
| `leakage_status == "pregame_safe"` for all 10 rows | ✅ confirmed |
| Odds boundary CONFIRMED | ✅ no odds columns in input or output |
| Deterministic hash | `a68c22490415d14d` |
| No network calls (fixture mode) | ✅ confirmed |
| PAPER_ONLY=True | ✅ confirmed |
| No file write in summary-only mode | ✅ confirmed |

---

## Pytest Run (TRACK 3 — 12 tests)

```
.venv/bin/python -m pytest tests/test_p39c_feature_join_contract.py -v
```

| Test | Result |
|------|--------|
| `test_joins_home_team_features_by_game_date_and_team` | PASS |
| `test_joins_away_team_features_by_game_date_and_team` | PASS |
| `test_home_prefix_applied_correctly` | PASS |
| `test_away_prefix_applied_correctly` | PASS |
| `test_differential_features_derived_correctly` | PASS |
| `test_rejects_feature_window_end_equal_to_game_date` | PASS |
| `test_rejects_feature_window_end_after_game_date` | PASS |
| `test_rejects_leakage_status_not_pregame_safe` | PASS |
| `test_rejects_odds_columns` | PASS |
| `test_missing_team_handled_fail_soft_with_nan` | PASS |
| `test_deterministic_output_for_same_inputs` | PASS |
| `test_acceptance_marker` | PASS |

**12/12 PASS in 1.54s**

Acceptance marker: `P39C_FEATURE_JOIN_TESTS_PASS_20260515`

---

## Smoke Status

**P39C_FEATURE_JOIN_SMOKE_PASS_20260515**
