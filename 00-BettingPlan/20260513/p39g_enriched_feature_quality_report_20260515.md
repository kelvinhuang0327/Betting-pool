# P39G — Enriched Feature Quality Report
**Date**: 2026-05-15  
**Mode**: FULL_SEASON_ENRICHMENT  
**Marker**: `P39G_ENRICHED_FEATURE_QUALITY_REPORT_READY_20260515`

---

## 1. Output File

| Field | Value |
|-------|-------|
| File | `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv` |
| Rows | 2,187 |
| Source P38A | `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv` |
| Feature source | `data/pybaseball/local_only/p39g_rolling_features_2024_fullseason.csv` |
| Bridge | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` |

---

## 2. Match Rates

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Bridge match (game_id) | 2187/2187 = **100.0%** | 100% | ✅ PASS |
| Home feature match | 2187/2187 = **100.0%** | ≥80% | ✅ PASS |
| Away feature match | 2187/2187 = **100.0%** | ≥80% | ✅ PASS |
| Complete home+away match | 2187/2187 = **100.0%** | ≥80% | ✅ PASS |

---

## 3. Feature Non-Null Coverage

All 8 rolling feature columns: **2187/2187 (100.0%) non-null** across all rows.

| Column | Non-null | % |
|--------|----------|---|
| `home_rolling_pa_proxy` | 2187 | 100.0% |
| `home_rolling_avg_launch_speed` | 2187 | 100.0% |
| `home_rolling_hard_hit_rate_proxy` | 2187 | 100.0% |
| `home_rolling_barrel_rate_proxy` | 2187 | 100.0% |
| `away_rolling_pa_proxy` | 2187 | 100.0% |
| `away_rolling_avg_launch_speed` | 2187 | 100.0% |
| `away_rolling_hard_hit_rate_proxy` | 2187 | 100.0% |
| `away_rolling_barrel_rate_proxy` | 2187 | 100.0% |

---

## 4. Feature Descriptive Statistics

| Feature | Mean | Std | Min | Max |
|---------|------|-----|-----|-----|
| home_rolling_pa_proxy | 61.09 | 8.79 | 18 | 89 |
| home_rolling_avg_launch_speed | 87.60 | 2.54 | 78.72 | 94.36 |
| home_rolling_hard_hit_rate_proxy | 0.370 | 0.084 | 0.108 | 0.633 |
| home_rolling_barrel_rate_proxy | 0.021 | 0.022 | 0.000 | 0.114 |
| away_rolling_pa_proxy | 60.80 | 9.02 | 20 | 86 |
| away_rolling_avg_launch_speed | 87.69 | 2.72 | 78.28 | 94.92 |
| away_rolling_hard_hit_rate_proxy | 0.376 | 0.087 | 0.076 | 0.646 |
| away_rolling_barrel_rate_proxy | 0.022 | 0.024 | 0.000 | 0.156 |

**Sanity check**: avg_launch_speed range 78–95 mph ✅ (MLB realistic), hard_hit_rate ~37% ✅, barrel_rate ~2% ✅

---

## 5. Coverage Meta

| Field | Value |
|-------|-------|
| Game date range | 2024-04-15 → 2024-09-30 |
| Unique home teams | 30 (all 30 MLB teams) |
| Window days | 7 (D-1 strict, pregame_safe) |
| Leakage violations | 0 |
| Odds columns | NONE |

---

## 6. Upstream TRACK 3 Summary

| Field | Value |
|-------|-------|
| Statcast chunks fetched | 14/14 SUCCESS, 0 FAILED |
| Total raw Statcast rows | 733,547 (pitch-level) |
| After dedup (game_date, game_pk, batter) | 51,645 |
| Team-daily aggregate rows | 5,042 |
| Rolling feature rows | 5,880 |
| Date range | 2024-03-20 → 2024-10-01 |

---

## 7. Constraints Verified

- `PAPER_ONLY = True` — no production write
- `pybaseball ≠ odds source` — confirmed: zero odds/moneyline/sportsbook columns
- `local_only` path guard — all raw and generated data in `data/pybaseball/local_only/` (gitignored)
- `deterministic_hash` — 9f0ad16d6b8e87f3

---

## 8. Classification

**`P39G_FULLSEASON_ENRICHMENT_READY`**

All 2,187 P38A OOF rows enriched with full-season 2024 Statcast rolling features.  
Match rate: 100% home + 100% away. Target ≥80% exceeded.

---

`P39G_ENRICHED_FEATURE_QUALITY_REPORT_READY_20260515`
