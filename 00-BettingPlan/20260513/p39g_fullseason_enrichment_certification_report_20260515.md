# P39G — Full-Season Enrichment Certification Report
**Date**: 2026-05-15  
**Branch**: `p13-clean`  
**HEAD**: `d14b17c` + P39G working changes (uncommitted)  
**Marker**: `P39G_FULLSEASON_ENRICHMENT_CERTIFIED_20260515`

---

## 1. P39G Objective

Produce full-season 2024 Statcast rolling features (2024-03-20 → 2024-10-01) and use them to enrich all 2,187 P38A OOF rows with home+away pregame-safe batting metrics. Target: ≥80% complete home+away match rate for all P38A rows (not just April).

---

## 2. TRACK Summary

| TRACK | Title | Status | Key Result |
|-------|-------|--------|------------|
| TRACK 0 | Preflight | ✅ PASS | p13-clean @ d14b17c, 13 commits ahead, no local_only staged |
| TRACK 1 | Scope doc | ✅ PASS | `p39g_fullseason_execution_scope_20260515.md` created |
| TRACK 2 | Script enhanced | ✅ PASS | `p39g_pybaseball_chunked_v1`, 14-chunk logic verified |
| TRACK 3 | Full-season fetch | ✅ PASS | 14/14 chunks SUCCESS, 5,880 rolling feature rows, 0 FAILED |
| TRACK 4 | Bridge enrichment | ✅ PASS | 2187/2187 bridge match (100%) |
| TRACK 5 | Full P38A OOF join | ✅ PASS | 2187/2187 home+away match (100%) |
| TRACK 6 | Regression tests | ✅ PASS | 86/86 PASS |
| TRACK 7 | Quality report | ✅ PASS | All 8 feature cols 100% non-null, sane ranges |
| TRACK 8 | Certification | ✅ PASS | This document |
| TRACK 9 | Push gate | 🔒 NOT AUTHORIZED | No push without explicit YES |

---

## 3. Final Classification

**`P39G_FULLSEASON_ENRICHMENT_READY`**

- Home feature match rate: **100.0%** (target ≥80%)
- Away feature match rate: **100.0%** (target ≥80%)
- Complete home+away: **2187/2187 (100.0%)**
- Leakage violations: **0**
- Odds columns: **NONE**
- Regression tests: **86/86 PASS**

---

## 4. Statcast Fetch Summary

| Chunk | Date Range | Status | Rows |
|-------|-----------|--------|------|
| 0 | 2024-03-20 → 2024-04-02 | SUCCESS | 45,053 |
| 1 | 2024-04-03 → 2024-04-16 | SUCCESS | 54,526 |
| 2 | 2024-04-17 → 2024-04-30 | SUCCESS | 54,406 |
| 3 | 2024-05-01 → 2024-05-14 | SUCCESS | 54,182 |
| 4 | 2024-05-15 → 2024-05-28 | SUCCESS | 53,128 |
| 5 | 2024-05-29 → 2024-06-11 | SUCCESS | 53,088 |
| 6 | 2024-06-12 → 2024-06-25 | SUCCESS | 54,235 |
| 7 | 2024-06-26 → 2024-07-09 | SUCCESS | 54,041 |
| 8 | 2024-07-10 → 2024-07-23 | SUCCESS | 42,339 |
| 9 | 2024-07-24 → 2024-08-06 | SUCCESS | 53,874 |
| 10 | 2024-08-07 → 2024-08-20 | SUCCESS | 55,478 |
| 11 | 2024-08-21 → 2024-09-03 | SUCCESS | 56,735 |
| 12 | 2024-09-04 → 2024-09-17 | SUCCESS | 54,257 |
| 13 | 2024-09-18 → 2024-10-01 | SUCCESS | 48,205 |
| **Total** | | **14/14 SUCCESS** | **733,547** |

Post-dedup (game_date, game_pk, batter): 51,645 rows  
Team-daily aggregates: 5,042 rows  
Rolling features: 5,880 rows (all 30 teams, full season)

---

## 5. Bug Fix Applied (P39G)

**Root cause**: `build_team_daily_statcast_aggregates()` called `float()` on pandas nullable float columns. With pybaseball's `Float64` dtype, `.mean()` returns `pd.NA` (not `np.nan`) for groups with all-null values, causing `TypeError: float() argument must be a string or a real number, not 'NAType'`.

**Fix**: Added module-level `_to_float_or_none(val)` helper that safely handles `pd.NA`, `np.nan`, and `None`. Replaced all `float(...)` calls in `build_team_daily_statcast_aggregates()` and `_mean()` in `build_rolling_features()`.

**Impact**: No data loss — only affects null-handling branch for groups with missing Statcast data. Feature values for groups with valid data are unchanged.

---

## 6. Acceptance Markers Emitted

```
P39G_FULLSEASON_EXECUTION_SCOPE_READY_20260515
P39G_CHUNKED_FETCH_RUNTIME_READY_20260515
P39G_FULLSEASON_FEATURE_GENERATION_PASS_20260515
P39G_P38A_BRIDGE_ENRICHMENT_PASS_20260515
P39G_FULL_P38A_OOF_ENRICHMENT_PASS_20260515
P39G_REGRESSION_PASS_20260515
P39G_ENRICHED_FEATURE_QUALITY_REPORT_READY_20260515
P39G_FULLSEASON_ENRICHMENT_CERTIFIED_20260515
P39G_PUSH_NOT_AUTHORIZED_20260515
```

---

## 7. P39H Plan

**Objective**: Use the P39G enriched features to retrain a P38A-class model and compare Brier scores.

### Design constraints
- Time-aware train/test split (no cross-contamination by date)
- Train on folds 0-4, test on fold 5 (or last fold by date)
- Features: 8 rolling Statcast features + `p_oof` (P38A baseline calibrated probability)
- Target: `y_true_home_win` from bridge
- Baseline Brier: **0.2487** (P38A OOF, reported in P38A certification)

### Steps
1. Load `p39g_enriched_p38a_oof_fullseason.csv` + join `y_true_home_win` from bridge
2. Train logistic regression / gradient boost on time-ordered folds
3. Report Brier score vs. P38A baseline
4. **No production edge claim** — research only

### PAPER_ONLY constraint
- No live predictions
- No odds data
- No push without explicit YES

### Success criterion
- Model trains without leakage (window_end < game_date confirmed)
- Brier score reported with confidence interval
- Any improvement over baseline is exploratory, not production-ready

---

## 8. Files to Commit (TRACK 11 candidate)

| File | Status |
|------|--------|
| `scripts/build_pybaseball_pregame_features_2024.py` | Modified (P39G chunked fetch + NAType fix) |
| `00-BettingPlan/20260513/p39g_fullseason_execution_scope_20260515.md` | New |
| `00-BettingPlan/20260513/p39g_fullseason_feature_generation_report_20260515.md` | New |
| `00-BettingPlan/20260513/p39g_enriched_feature_quality_report_20260515.md` | New |
| `00-BettingPlan/20260513/p39g_fullseason_enrichment_certification_report_20260515.md` | This file |

**DO NOT commit**: any CSV/JSON in `data/pybaseball/local_only/`, manifest, raw Statcast CSVs.

---

`P39G_FULLSEASON_ENRICHMENT_CERTIFIED_20260515`  
`PAPER_ONLY=True | pybaseball != odds source | no push`
