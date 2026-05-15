# P39E — Expanded April Feature Generation Report
**Date**: 2026-05-15
**Marker**: `P39E_EXPANDED_APRIL_FEATURE_GENERATION_PASS_20260515`
**Status**: PASS

---

## Execution Summary

| Parameter | Value |
|-----------|-------|
| Script | `scripts/build_pybaseball_pregame_features_2024.py` |
| Script version | `p39b_pybaseball_rolling_v1` |
| Mode | `--execute` (real Statcast fetch) |
| Start date | 2024-04-08 |
| End date | 2024-04-30 |
| Window days | 7 |
| Output path | `data/pybaseball/local_only/p39e_rolling_features_2024_04_08_04_30.csv` |
| Cache dir | `data/pybaseball/local_only/cache` |

---

## Results

| Metric | Value | Status |
|--------|-------|--------|
| Raw Statcast rows | 90,696 | ✅ |
| Raw Statcast columns | 118 | ✅ |
| Date range | 2024-04-08 → 2024-04-30 | ✅ |
| Team-daily aggregates | 618 rows (some teams had off-days) | ✅ |
| Teams found | 30 (all Statcast canonical) | ✅ |
| Rolling feature rows | 690 (30 teams × 23 as_of_dates) | ✅ |
| Pregame-safe rows | 690 / 690 | ✅ |
| Rows with launch_speed data | 656 / 690 (some dates have sparse data) | ✅ |
| Leakage violations | 0 | ✅ |
| Odds boundary | CONFIRMED | ✅ |

---

## Teams in Output (30 Statcast canonical)

```
ATH, ATL, AZ, BAL, BOS, CHC, CIN, CLE, COL, CWS,
DET, HOU, KC, LAA, LAD, MIA, MIL, MIN, NYM, NYY,
PHI, PIT, SD, SEA, SF, STL, TB, TEX, TOR, WSH
```

---

## Why Apr 8 Start Date

P38A OOF games begin on 2024-04-15. With a 7-day rolling window, features for Apr 15 require data from Apr 8–14. Starting the Statcast fetch on Apr 8 ensures D-1 pregame-safe features are available for every April P38A game.

---

## Why This Resolves the P39D Date Gap

Previous P39D attempt fetched Apr 1–10 (rolling features up to Apr 10 as_of_date). P38A games start Apr 15. Date gap = 5 days → 0% match rate.

This P39E fetch extends to Apr 30, providing rolling feature rows for every as_of_date from Apr 8 to Apr 30, covering all April P38A games.

---

## Data Isolation Status

- Output written to `data/pybaseball/local_only/` — gitignored at line 86 of .gitignore
- **NOT committed** to repo (raw Statcast output)
- PAPER_ONLY = True
- pybaseball ≠ odds source (no betting lines, no CLV)

---

## Marker

`P39E_EXPANDED_APRIL_FEATURE_GENERATION_PASS_20260515`
