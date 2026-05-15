# P39G — Full-Season Feature Generation Report
**Date**: 2026-05-15  
**Mode**: FULL_SEASON_CHUNKED_EXECUTION  
**Marker**: `P39G_FULLSEASON_FEATURE_GENERATION_PASS_20260515`

---

## 1. Chunked Statcast Fetch

| Field | Value |
|-------|-------|
| Date range | 2024-03-20 → 2024-10-01 (196 days) |
| Chunk size | 14 days |
| Total chunks | 14 |
| Succeeded | 14 |
| Failed | 0 |
| Total pitch rows | 733,547 |
| After dedup (game_date, game_pk, batter) | 51,645 |
| Team-daily rows | 5,042 |
| Rolling feature rows | 5,880 |
| Output | `data/pybaseball/local_only/p39g_rolling_features_2024_fullseason.csv` |
| Manifest | `data/pybaseball/local_only/p39g_statcast_manifest_2024.json` |
| Script version | `p39g_pybaseball_chunked_v1` |
| Odds boundary | CONFIRMED |
| Leakage violations | 0 |

`P39G_FULLSEASON_FEATURE_GENERATION_PASS_20260515`

---

## 2. P38A Bridge Enrichment

| Field | Value |
|-------|-------|
| Input P38A | `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv` |
| Bridge | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` |
| Output | `data/pybaseball/local_only/p39g_p38a_oof_with_identity_bridge.csv` |
| P38A rows | 2,187 |
| Bridge rows | 2,429 |
| Matched | 2187/2187 (100.0%) |
| Unmatched | 0 |
| Missing away_team | 0 |
| Odds columns | NONE |
| Deterministic hash | 82540eba8d8933ec |

`P39G_P38A_BRIDGE_ENRICHMENT_PASS_20260515`

---

## 3. Full P38A OOF Feature Join

| Field | Value |
|-------|-------|
| Input | `data/pybaseball/local_only/p39g_p38a_oof_with_identity_bridge.csv` |
| Features | `data/pybaseball/local_only/p39g_rolling_features_2024_fullseason.csv` |
| Output | `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv` |
| P38A rows | 2,187 |
| Feature rows | 5,880 |
| Home match | 2187/2187 = **100.0%** |
| Away match | 2187/2187 = **100.0%** |
| Complete home+away | 2187/2187 = **100.0%** |
| Leakage violations | 0 |
| Odds boundary | CONFIRMED |

`P39G_FULL_P38A_OOF_ENRICHMENT_PASS_20260515`

---

## 4. Regression Tests

| Suite | Tests | Status |
|-------|-------|--------|
| test_p39b_pybaseball_leakage_policy | 11 | ✅ PASS |
| test_p39b_pybaseball_feature_aggregation | 10 | ✅ PASS |
| test_p39c_feature_join_contract | 19 | ✅ PASS |
| test_team_code_normalization | 30 | ✅ PASS |
| test_p39f_p38a_bridge_enrichment | 16 | ✅ PASS |
| **Total** | **86** | **✅ 86/86 PASS** |

`P39G_REGRESSION_PASS_20260515`

---

## 5. Push Gate

No push has been executed. Repository remains 13+ commits ahead of `origin/p13-clean`.  
Push requires explicit YES from operator.

`P39G_PUSH_NOT_AUTHORIZED_20260515`

---

## 6. Bug Fixed in TRACK 3 Runtime

**Error**: `TypeError: float() argument must be a string or a real number, not 'NAType'`  
**Location**: `build_team_daily_statcast_aggregates()` line 348  
**Cause**: pybaseball returns `Float64` (nullable) dtype; `pd.NA.mean()` → `pd.NA`; `float(pd.NA)` raises  
**Fix**: Added `_to_float_or_none(val)` helper; replaced all `float()` calls on potentially-NA values  
**Scope**: `build_team_daily_statcast_aggregates()` (5 sites) + `_mean()` in `build_rolling_features()` (1 site)  
**Tests impacted**: 0 (fix is null-path only; non-NA paths unchanged)

---

`P39G_FULLSEASON_FEATURE_GENERATION_PASS_20260515`  
`P39G_P38A_BRIDGE_ENRICHMENT_PASS_20260515`  
`P39G_FULL_P38A_OOF_ENRICHMENT_PASS_20260515`  
`P39G_REGRESSION_PASS_20260515`  
`P39G_PUSH_NOT_AUTHORIZED_20260515`  
`PAPER_ONLY=True | pybaseball != odds source | no push`
