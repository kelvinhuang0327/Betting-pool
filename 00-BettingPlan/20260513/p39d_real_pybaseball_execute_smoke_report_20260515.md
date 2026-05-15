# P39D — Real Pybaseball Execute Smoke Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Script**: `scripts/build_pybaseball_pregame_features_2024.py` (SCRIPT_VERSION=p39b_pybaseball_rolling_v1)  
**PAPER_ONLY**: True

---

## Execution Parameters

| Parameter | Value |
|-----------|-------|
| Mode | EXECUTE (real network fetch) |
| start_date | `2024-04-01` |
| end_date | `2024-04-10` |
| window_days | `7` |
| out_file | `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv` |
| cache_dir | `data/pybaseball/local_only/cache/` |

---

## Command

```bash
.venv/bin/python scripts/build_pybaseball_pregame_features_2024.py \
  --execute \
  --start-date 2024-04-01 \
  --end-date 2024-04-10 \
  --window-days 7 \
  --out-file data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv \
  --cache-dir data/pybaseball/local_only/cache
```

---

## Result: PASS

### Raw Statcast Fetch

| Metric | Value |
|--------|-------|
| Source | Baseball Savant (via pybaseball 2.2.7) |
| Rows returned | **38,331** |
| Columns returned | 118 |
| Date range | 2024-04-01 → 2024-04-10 |
| Fetch time | ~1 second (cache-assisted on second run) |
| Odds boundary (raw) | **CONFIRMED** — no odds columns in Statcast data |

### Team-Daily Aggregates

| Metric | Value |
|--------|-------|
| Team-daily rows | **258** |
| Teams found | 30 (ATH, ATL, AZ, BAL, BOS, CHC, CIN, CLE, COL, CWS, DET, HOU, KC, LAA, LAD, MIA, MIL, MIN, NYM, NYY, PHI, PIT, SD, SEA, SF, STL, TB, TEX, TOR, WSH) |

### Rolling Features

| Metric | Value |
|--------|-------|
| As-of-dates | 10 (2024-04-01 to 2024-04-10) |
| Teams per date | 30 |
| Total rolling feature rows | **300** |
| Rows with launch_speed data | **268** (rows where prior-week data existed) |
| Pregame-safe rows | **300/300 (100%)** |
| Leakage violations | **0** |
| Odds boundary | **CONFIRMED** |

### Output Files

| File | Status |
|------|--------|
| `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv` | Written ✅ |
| `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.summary.json` | Written ✅ |

Both files are in the gitignored `data/pybaseball/local_only/` directory. **NOT committed.**

---

## Observations

### Early-April Window Gap (Expected)
Games on 2024-04-01 through approximately 2024-04-07 have `sample_size=0` in their rolling window because there is no prior-week MLB Statcast data (this is the start of the season). This is correct behavior — the feature values will be NaN. This edge case is documented and acceptable.

### Summary-Only Mode Bug Fix (Applied in TRACK 2)
A minor bug was found and fixed in the script during TRACK 2 review: the `sys.exit(0)` in the summary-only path was incorrectly placed due to a previous edit, causing both summary-only and execute modes to run concurrently. The fix restored proper indentation and the `sys.exit(0)` guard. All regression tests still pass post-fix.

---

## Markers

**P39D_REAL_PYBASEBALL_EXECUTE_SMOKE_PASS_20260515**
