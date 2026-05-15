# P39A Pybaseball Minimal Runtime Plan — 2026-05-15

**Task Round:** P3.8 / P39A — TRACK 3  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Generated:** 2026-05-15

---

## 1. Proposed Script Path

```
scripts/build_pybaseball_pregame_features_2024.py
```

---

## 2. Proposed Behavior

| Property | Value |
|---|---|
| Default mode | `--summary-only` (no external fetch, no write) |
| External fetch | Only if `--execute` flag is present |
| Raw data write | Only if `--execute` + `--write-local` |
| Raw data target | `data/pybaseball/local_only/` (gitignored line 86) |
| Feature CSV output | Only if `--out-file` specified |
| Fail-soft | On FanGraphs 403 / schema drift → log warning, continue with available data |
| Odds boundary | Hard assertion before any save; raises `ValueError` on violation |
| Leakage check | Hard assertion on every feature window; raises `LeakageError` on violation |

### What Script NEVER Does

- Does NOT commit to git
- Does NOT write to production ledger
- Does NOT write odds data
- Does NOT produce moneyline / CLV output
- Does NOT push to origin

---

## 3. CLI Interface

```
scripts/build_pybaseball_pregame_features_2024.py

Required:
  --start-date YYYY-MM-DD    First game_date to build features for
  --end-date   YYYY-MM-DD    Last game_date to build features for (inclusive)

Optional:
  --window-days  INT          Rolling window size in days (default: 14)
  --summary-only              Dry-run: report what would be built, no fetch (default)
  --execute                   Actually fetch Statcast data and compute features
  --out-file PATH             Write feature CSV to this path (local_only only)
  --cache-dir PATH            Directory to cache raw Statcast chunks (default: data/pybaseball/local_only/cache)

Output modes:
  --summary-only (default)    Print row count estimate, date range, feature list
  --execute                   Fetch + compute + optionally write
```

### Example Invocations

```bash
# Dry-run (safe, no fetch)
.venv/bin/python scripts/build_pybaseball_pregame_features_2024.py \
    --start-date 2024-04-01 --end-date 2024-04-03 --window-days 7 --summary-only

# Execute with local cache write
.venv/bin/python scripts/build_pybaseball_pregame_features_2024.py \
    --start-date 2024-04-01 --end-date 2024-04-30 --window-days 14 --execute \
    --out-file data/pybaseball/local_only/p39a_features_2024_apr.csv

# Full season (long-running, not for CI)
.venv/bin/python scripts/build_pybaseball_pregame_features_2024.py \
    --start-date 2024-03-20 --end-date 2024-09-30 --window-days 14 --execute \
    --out-file data/pybaseball/local_only/p39a_features_2024_full.csv
```

---

## 4. Minimum Smoke Specification

### Smoke Parameters

| Parameter | Value |
|---|---|
| Date range | 2024-04-01 → 2024-04-10 |
| Rolling window | 7 days |
| Mode | `--summary-only` (no external fetch needed for smoke) |

### Smoke Pass Criteria

| Check | Pass Condition |
|---|---|
| Script exits 0 | ✅ |
| Estimated output row count > 0 | ✅ |
| No leakage violations reported | ✅ |
| No odds columns in feature schema | ✅ |
| `leakage_status` field present in schema | ✅ |
| Deterministic summary hash stable across two runs | ✅ (same inputs → same hash) |
| No `THE_ODDS_API_KEY` or `.env` read | ✅ |

### Smoke Fail Criteria (classify as FAIL)

| Condition | Classification |
|---|---|
| Script exits non-zero | SMOKE_FAIL |
| `leakage_detected` rows > 0 | SMOKE_FAIL_LEAKAGE |
| Odds columns detected | SMOKE_FAIL_ODDS_BOUNDARY |
| Exception on import | SMOKE_FAIL_IMPORT_ERROR |

---

## 5. Pure Functions (Must Be Independently Testable)

These functions are exposed at module level (no side effects, no external fetch):

```python
def validate_feature_window(game_date: date, feature_window_end: date) -> bool:
    """True iff window_end < game_date. Core leakage guard."""
    ...

def assert_no_odds_columns(columns: list[str]) -> None:
    """Raises ValueError if any forbidden odds column is present."""
    ...

def summarize_statcast_frame(df: pd.DataFrame) -> dict:
    """
    Returns summary dict:
      rows, columns, date_range_start, date_range_end,
      sample_columns, odds_boundary_status, leakage_rows
    """
    ...

def build_rolling_window_dates(game_date: date, window_days: int) -> tuple[date, date]:
    """Returns (window_start, window_end) where window_end = game_date - 1 day."""
    ...
```

---

## 6. Test Plan

### Unit Tests

| Test | File | Description |
|---|---|---|
| `test_validate_feature_window` | `tests/test_p39a_leakage.py` | window_end < game_date → True; window_end == game_date → False |
| `test_assert_no_odds_columns_clean` | `tests/test_p39a_leakage.py` | Clean columns → no raise |
| `test_assert_no_odds_columns_dirty` | `tests/test_p39a_leakage.py` | `moneyline` in columns → raises ValueError |
| `test_build_rolling_window_dates` | `tests/test_p39a_leakage.py` | 7-day window → correct start/end |
| `test_summarize_statcast_frame_empty` | `tests/test_p39a_leakage.py` | Empty DF → summary with rows=0, no crash |
| `test_403_fallback` | `tests/test_p39a_leakage.py` | Simulated HTTPError 403 → returns None, no raise |

### Fixture Tests

| Test | File | Description |
|---|---|---|
| `test_rolling_aggregation_correctness` | `tests/test_p39a_features.py` | 10-row fixture DF → correct hard_hit_rate |
| `test_doubleheader_isolation` | `tests/test_p39a_features.py` | Game 2 features do not include Game 1 data |
| `test_postponed_game_drop` | `tests/test_p39a_features.py` | Null score row dropped from rolling window |

### Smoke Test

| Test | Command | Pass Condition |
|---|---|---|
| Script smoke | `.venv/bin/python scripts/build_pybaseball_pregame_features_2024.py --start-date 2024-04-01 --end-date 2024-04-10 --window-days 7 --summary-only` | exit 0, no leakage, no odds |

### CI Note

Unit + fixture tests should run in `< 10 seconds` with no external network calls.  
Smoke test requires network (Baseball Savant). Tag with `@pytest.mark.network` for optional skip in CI.

---

## 7. Dependency Notes

| Dependency | Required | Notes |
|---|---|---|
| `pybaseball >= 2.2.7` | Yes | Pinned in requirements.txt |
| `pandas >= 2.0` | Yes | Required for `.pipe()` chains |
| `numpy` | Yes | For `np.nan` handling |
| `requests` | Indirect | via pybaseball |
| `.env` / `THE_ODDS_API_KEY` | **NO** | This script must NOT read odds API credentials |

---

## 8. Gitignore Compliance

All output paths must fall within gitignored directories:

```
data/pybaseball/local_only/     ← gitignored (line 86)
data/pybaseball/local_only/cache/  ← also gitignored
```

Script must validate output path before write:

```python
def assert_output_path_gitignored(path: str) -> None:
    if "local_only" not in path:
        raise ValueError(f"Output path must be under local_only/: {path}")
```

---

## 9. Acceptance Marker

```
P39A_PYBASEBALL_MINIMAL_RUNTIME_PLAN_20260515_READY
```
