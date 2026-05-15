# P39F — April Home+Away Enrichment Report
**Date**: 2026-05-15
**Marker**: `P39F_APRIL_HOME_AWAY_ENRICHMENT_PASS_20260515`
**Status**: PASS — Target ≥80% Complete Home+Away: **EXCEEDED (100%)**

---

## Pipeline

```
P38A OOF (2187 rows)
  ↓  enrich_p38a_with_identity_bridge.py
  ↓  (bridge join: 2187/2187 = 100%)
bridge-enriched P38A (with home_team, away_team, game_date)
  ↓  join_p38a_oof_with_p39b_features.py
  ↓  (Statcast rolling features: Apr 8–30, 690 rows)
Final enriched output (with home + away Statcast features)
```

---

## April In-Scope Results

| Metric | Value |
|--------|-------|
| April P38A rows | 210 |
| Bridge match | 210/210 = 100.0% |
| Home feature match | **210 / 210 = 100.0%** |
| Away feature match | **210 / 210 = 100.0%** |
| **Complete home+away match** | **210 / 210 = 100.0%** |
| TARGET (≥80%) | ✅ **PASS** |
| Odds boundary | CONFIRMED |
| Leakage violations | 0 |
| Deterministic hash | `9f0ad16d6b8e87f3` |

---

## Feature Columns in Output

**Home side (5 features)**:
- `home_rolling_pa_proxy`
- `home_rolling_avg_launch_speed`
- `home_rolling_hard_hit_rate_proxy`
- `home_rolling_barrel_rate_proxy`
- `home_sample_size`

**Away side (5 features)** — **NEW in P39F** (was 0% before):
- `away_rolling_pa_proxy`
- `away_rolling_avg_launch_speed`
- `away_rolling_hard_hit_rate_proxy`
- `away_rolling_barrel_rate_proxy`
- `away_sample_size`

**Differential features**:
- `diff_rolling_avg_launch_speed`
- `diff_rolling_hard_hit_rate_proxy`
- `diff_sample_size`

**Metadata**: `game_id`, `fold_id`, `p_oof`, `model_version`, `game_date`, `home_team`, `away_team`, `bridge_match_status`

---

## Before vs. After P39F Bridge Enrichment

| | P39E (Before) | P39F (After) |
|--|--------------|-------------|
| Home match (April) | 210/210 = 100% | 210/210 = 100% |
| **Away match (April)** | **0/210 = 0%** | **210/210 = 100%** |
| **Complete home+away (April)** | **0%** | **100%** |

---

## Output File

`data/pybaseball/local_only/p39f_enriched_p38a_april_home_away.csv`
- gitignored — NOT committed
- 2,187 rows (all P38A), 23 columns

---

## P39G Readiness

Away team recovery is complete and validated at 100% for April in-scope rows. Full-season away enrichment (P39G) can proceed once Statcast rolling features are generated for the full 2024 season (Apr 15 → Sep 30, ~2,187 unique game-date windows).

---

## Status

`P39F_APRIL_HOME_AWAY_ENRICHMENT_PASS_20260515`

PAPER_ONLY=True | pybaseball ≠ odds source
