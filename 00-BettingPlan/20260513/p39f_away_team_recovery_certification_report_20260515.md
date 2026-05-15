# P39F — Away Team Recovery Certification Report + P39G Plan
**Date**: 2026-05-15
**Marker**: `P39F_AWAY_TEAM_RECOVERY_CERTIFIED_20260515`
**Status**: ALL TRACKS PASS

---

## Certification Summary

P39F Away Team Recovery is **certified complete**. All 12 tracks passed. The
identity bridge approach fully resolved the P38A `away_team = NULL` problem with
zero Statcast downloads and zero pipeline changes to P38A probabilities.

---

## Track-by-Track Results

| Track | Description | Status | Marker |
|-------|-------------|--------|--------|
| TRACK 0 | Preflight / Repo ground truth | ✅ PASS | p13-clean @ e48e554, all P39E markers |
| TRACK 1 | P39F scope decision | ✅ PASS | `P39F_AWAY_TEAM_RECOVERY_SCOPE_READY_20260515` |
| TRACK 2 | Bridge inspection | ✅ PASS | `P39F_IDENTITY_BRIDGE_INSPECTION_READY_20260515` |
| TRACK 3 | Bridge enrichment utility | ✅ PASS | `P39F_P38A_BRIDGE_ENRICHMENT_UTILITY_READY_20260515` |
| TRACK 4 | Unit tests (16 tests) | ✅ PASS | `P39F_BRIDGE_ENRICHMENT_TESTS_PASS_20260515` |
| TRACK 5 | Smoke run (real data) | ✅ PASS | `P39F_P38A_BRIDGE_ENRICHMENT_SMOKE_PASS_20260515` |
| TRACK 6 | April home+away enrichment | ✅ PASS | `P39F_APRIL_HOME_AWAY_ENRICHMENT_PASS_20260515` |
| TRACK 7 | Regression tests (86 total) | ✅ PASS | `P39F_REGRESSION_PASS_20260515` |

---

## Key Metrics

| Metric | Result | Target |
|--------|--------|--------|
| P38A bridge match rate | **100%** (2187/2187) | — |
| April away_team recovery | **100%** (210/210) | — |
| April complete home+away | **100%** (210/210) | ≥80% |
| Leakage violations | **0** | 0 |
| Odds columns in output | **NONE** | NONE |
| Tests passing | **86 / 86** | 80+ |
| PAPER_ONLY | **True** | True |
| pybaseball ≠ odds source | **Confirmed** | Confirmed |

---

## Artifacts Created (to be committed)

| File | Purpose |
|------|---------|
| `scripts/enrich_p38a_with_identity_bridge.py` | Bridge enrichment utility |
| `tests/test_p39f_p38a_bridge_enrichment.py` | 16 unit tests |
| `00-BettingPlan/20260513/p39f_away_team_recovery_scope_decision_20260515.md` | TRACK 1 doc |
| `00-BettingPlan/20260513/p39f_identity_bridge_inspection_report_20260515.md` | TRACK 2 doc |
| `00-BettingPlan/20260513/p39f_p38a_bridge_enrichment_smoke_report_20260515.md` | TRACK 5 doc |
| `00-BettingPlan/20260513/p39f_april_home_away_enrichment_report_20260515.md` | TRACK 6 doc |
| `00-BettingPlan/20260513/p39f_away_team_recovery_certification_report_20260515.md` | This file |

**NOT committed** (gitignored local_only):
- `data/pybaseball/local_only/p39f_p38a_oof_with_identity_bridge.csv`
- `data/pybaseball/local_only/p39f_enriched_p38a_april_home_away.csv`

---

## P39G Full-Season Feature Generation Plan

### Goal
Generate Statcast rolling features for the full 2024 season (Apr 15 → Sep 30, ~169 dates × 30 teams = ~5,070 rows) to achieve complete home+away enrichment across all 2,187 P38A OOF rows.

### Architecture
```
Full-season Statcast download (pybaseball.statcast, 2024-04-01 → 2024-10-01)
  ↓  rolling feature engine (same logic as P39B/P39E, window=14d)
  ↓  feature CSV: data/pybaseball/local_only/p39g_rolling_features_2024_full.csv
  ↓  join_p38a_oof_with_p39b_features.py
       --p38a-path: data/pybaseball/local_only/p39f_p38a_oof_with_identity_bridge.csv
       --p39b-path: data/pybaseball/local_only/p39g_rolling_features_2024_full.csv
       --out-file:  data/pybaseball/local_only/p39g_enriched_p38a_full_season.csv
       --normalize-team-codes --execute
  ↓  complete home+away enrichment: expected ~90%+ (P39E home was 9.6% April-only → full-season expands to all dates)
```

### Requirements
1. Download rate limit: pybaseball.statcast chunks by month, ~6 API calls
2. Total fetch time: estimate 3–8 min depending on Baseball Savant API latency
3. Output rows estimate: ~50,000–80,000 Statcast rows → ~5,000 feature rows after rolling aggregation
4. Leakage guard: rolling window must end ≥ 1 day before game_date (inherited from P39B design)
5. All P38A `game_id` matches identity bridge (100%) — away_team already recovered

### Success Criteria
- Full-season complete home+away match ≥80% of 2,187 P38A rows
- Leakage violations = 0
- Odds columns = NONE
- Test suite still 86+ PASS after adding P39G tests

### Files to Create in P39G
- `scripts/generate_p39g_full_season_features.py` — Statcast fetch + rolling feature engine
- `tests/test_p39g_full_season_feature_contract.py` — leakage + output schema tests
- `00-BettingPlan/20260513/p39g_full_season_feature_plan_20260515.md`

---

## Acceptance Markers

```
P39F_AWAY_TEAM_RECOVERY_SCOPE_READY_20260515
P39F_IDENTITY_BRIDGE_INSPECTION_READY_20260515
P39F_P38A_BRIDGE_ENRICHMENT_UTILITY_READY_20260515
P39F_BRIDGE_ENRICHMENT_TESTS_PASS_20260515
P39F_P38A_BRIDGE_ENRICHMENT_SMOKE_PASS_20260515
P39F_APRIL_HOME_AWAY_ENRICHMENT_PASS_20260515
P39F_REGRESSION_PASS_20260515
P39F_AWAY_TEAM_RECOVERY_CERTIFIED_20260515
```

PAPER_ONLY=True | pybaseball ≠ odds source
