# P39C — Feature Join Certification Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Scope**: P38A OOF Predictions × P39B Rolling Pybaseball Features — Join Certification  
**Author**: CTO Agent  
**Status**: RESEARCH ONLY — PAPER_ONLY=True, production_ready=False

---

## ⚠️ Mandatory Constraints

> - PAPER_ONLY=True on all P39C artifacts
> - production_ready=False
> - No wagering, no live odds, no production write
> - No odds columns in any join output
> - No betting decision derived from this join
> - No model edge claim
> - pybaseball is a baseball stats source — NOT an odds source
> - CLV / EV / Kelly sizing still require a licensed odds source (not resolved in P39C)

---

## 1. Implemented Join Utility

**File**: `scripts/join_p38a_oof_with_p39b_features.py`  
**Script Version**: `p39c_feature_join_v1`  
**Prev Version**: `p39b_pybaseball_rolling_v1`

### Pure Functions

| Function | Responsibility |
|----------|---------------|
| `assert_no_odds_columns(columns)` | Reject odds columns (exact + keyword substring); raises `ValueError` |
| `validate_join_leakage(p38a_df, feature_df)` | Check `feature_window_end < as_of_date` AND `leakage_status == pregame_safe` |
| `join_home_away_features(p38a_df, feature_df)` | Left join home + away features; prefix home_/away_; derive diffs |
| `summarize_join_result(joined_df)` | Compute match rates, odds boundary, deterministic hash |

### CLI Modes

| Flag | Behaviour |
|------|-----------|
| `--summary-only` | Default; print summary, no file write |
| `--fixture-mode` | Synthetic inline P38A + synthetic rolling features CSV |
| `--execute --out-file PATH` | Write enriched CSV to PATH |
| `--dry-run` | Show what would be written, no actual write |
| `--p38a-path PATH` | Custom P38A CSV path |
| `--p39b-path PATH` | Custom P39B rolling features CSV path |

---

## 2. Test Results — 12/12 PASS

**File**: `tests/test_p39c_feature_join_contract.py`  
**Runtime**: 1.54s

| Test | Coverage Target | Result |
|------|----------------|--------|
| `test_joins_home_team_features_by_game_date_and_team` | Home join by (game_date, home_team) | ✅ PASS |
| `test_joins_away_team_features_by_game_date_and_team` | Away join by (game_date, away_team) | ✅ PASS |
| `test_home_prefix_applied_correctly` | home_ prefix on all feature columns | ✅ PASS |
| `test_away_prefix_applied_correctly` | away_ prefix on all feature columns | ✅ PASS |
| `test_differential_features_derived_correctly` | diff_* = home - away | ✅ PASS |
| `test_rejects_feature_window_end_equal_to_game_date` | Same-day window rejection | ✅ PASS |
| `test_rejects_feature_window_end_after_game_date` | Future window rejection | ✅ PASS |
| `test_rejects_leakage_status_not_pregame_safe` | Non-pregame_safe rejection | ✅ PASS |
| `test_rejects_odds_columns` | Exact + keyword odds detection | ✅ PASS |
| `test_missing_team_handled_fail_soft_with_nan` | Missing feature → NaN, no crash | ✅ PASS |
| `test_deterministic_output_for_same_inputs` | Same inputs → identical output | ✅ PASS |
| `test_acceptance_marker` | Sentinel | ✅ PASS |

---

## 3. Smoke Result

**Mode**: `--fixture-mode --summary-only`  
**P38A**: 5 synthetic games (2024-04-15 to 2024-04-19)  
**P39B**: 10 rows from `data/pybaseball/fixtures/P39C_SYNTHETIC_ROLLING_FEATURES_20260515.csv`  

| Metric | Value |
|--------|-------|
| Total P38A rows | 5 |
| Home feature match rate | **100%** (5/5) |
| Away feature match rate | **100%** (5/5) |
| Leakage violations | 0 |
| Odds boundary | CONFIRMED |
| Deterministic hash | `a68c22490415d14d` |

---

## 4. Leakage Guarantees

| Guarantee | Mechanism | Status |
|-----------|-----------|--------|
| `feature_window_end < game_date` (strict D-1) | `validate_join_leakage()` checks all rows before join | ✅ ENFORCED |
| Same-day feature window rejected | `wend >= asof` → violation list → `sys.exit(1)` | ✅ ENFORCED |
| Future feature window rejected | `wend >= asof` → same check | ✅ ENFORCED |
| `leakage_status == pregame_safe` required | `validate_join_leakage()` | ✅ ENFORCED |
| No odds columns in inputs or output | `assert_no_odds_columns()` called 3× (P38A, P39B, joined) | ✅ ENFORCED |

---

## 5. Odds Boundary Guarantees

| Guarantee | Status |
|-----------|--------|
| P39B rolling features contain no odds columns | ✅ Confirmed (fixture + code) |
| P38A OOF predictions contain no odds columns | ✅ Confirmed (p_oof is model output, not market odds) |
| Joined output contains no odds columns | ✅ Confirmed (checked post-join by `assert_no_odds_columns`) |
| `p_oof` is a model probability, NOT an odds-implied probability | ✅ Confirmed by P38A gate result |

---

## 6. Unmatched Team Handling

- Join is **left join** (P38A left table)
- Teams absent from the rolling feature file → `NaN` values in enriched output
- No crash on unmatched rows
- Tested by `test_missing_team_handled_fail_soft_with_nan` (PASS)

---

## 7. Known Limitations

| Limitation | Impact | Next Step |
|-----------|--------|-----------|
| Real Statcast rolling features not yet generated | Smoke uses synthetic fixture only | P39D: run `build_pybaseball_pregame_features_2024.py` on real data |
| Retrosheet team codes ≠ Statcast team codes for some teams | CHA≠CHW, SDN≠SDP, etc. | Normalization layer required before full P38A join |
| P38A CSV lacks away_team column | Must use identity bridge or game_id-based parsing | `_enrich_p38a_with_game_meta()` handles home_team; identity bridge needed for away |
| Rolling features only for 2024 MLB | No multi-year depth | Expand Statcast pull in P39D |
| pybaseball does NOT provide odds | CLV/EV/Kelly still require licensed odds source | Separate P3 odds pipeline |

---

## 8. Next Step: P39D

> **P39D — Full 2024 Rolling Feature Generation and P38A OOF Enrichment**
>
> Tasks:
> 1. Run `build_pybaseball_pregame_features_2024.py --execute` for full 2024 season
>    (requires network / Statcast API access and cache warmup)
> 2. Normalize team codes (Retrosheet → Statcast)
> 3. Enrich all 2,187 P38A rows with real rolling features
> 4. Validate match rate on real data (target: ≥ 80% both home + away)
> 5. Report Brier improvement vs. baseline P38A (logistic regression only)
>
> **Pre-condition**: Real Statcast data must NOT be committed to git.
> Cache in `data/pybaseball/local_only/` (gitignored).

---

## 9. Critical Reminders

- **pybaseball does NOT solve the P3 odds pipeline**
- **CLV still requires a separate licensed odds source** (not available as of 2026-05-15)
- **No production edge claim**: P39C join is research enrichment only
- **PAPER_ONLY=True** on all outputs
- **No push to origin** without explicit user YES

---

## 10. Artifacts Summary

| Artifact | Status |
|----------|--------|
| `scripts/join_p38a_oof_with_p39b_features.py` | ✅ Created |
| `tests/test_p39c_feature_join_contract.py` | ✅ Created (12 tests, all PASS) |
| `data/pybaseball/fixtures/P39C_SYNTHETIC_ROLLING_FEATURES_20260515.csv` | ✅ Created (10 rows) |
| `00-BettingPlan/20260513/p39c_p38a_p39b_feature_join_contract_20260515.md` | ✅ Created |
| `00-BettingPlan/20260513/p39c_feature_join_smoke_report_20260515.md` | ✅ Created |
| `00-BettingPlan/20260513/p39c_feature_join_certification_report_20260515.md` | ✅ Created (this file) |

---

## Acceptance Markers

- `P39C_FEATURE_JOIN_CONTRACT_20260515_READY` — join contract doc ✅
- `P39C_JOIN_UTILITY_READY_20260515` — join script prints in smoke ✅
- `P39C_FEATURE_JOIN_TESTS_PASS_20260515` — 12/12 tests PASS ✅
- `P39C_FEATURE_JOIN_SMOKE_PASS_20260515` — smoke PASS ✅
- `P39C_PUSH_NOT_AUTHORIZED_20260515` — no explicit YES received ✅

---

**P39C_FEATURE_JOIN_CERTIFICATION_READY_20260515**
