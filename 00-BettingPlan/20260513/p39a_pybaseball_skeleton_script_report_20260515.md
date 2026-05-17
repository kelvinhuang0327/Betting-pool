# P39A Pybaseball Skeleton Script Report — 2026-05-15

**Task Round:** P3.8 / P39A — TRACK 4  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Script:** `scripts/build_pybaseball_pregame_features_2024.py`  
**Script version:** `p39a_pybaseball_skeleton_v1`  
**Run timestamp:** 2026-05-15T05:28:34Z

---

## 1. Smoke Run Result

**PASS**

```
Mode           : SUMMARY-ONLY (no external fetch)
Start date     : 2024-04-01
End date       : 2024-04-03
Window days    : 7
```

---

## 2. Smoke Checks

| Check | Result |
|---|---|
| Script exit code | **0** ✅ |
| No external network call (summary-only) | ✅ |
| Pregame-safe window check | **CONFIRMED** — window_end=2024-03-31 < game_date=2024-04-01 ✅ |
| Odds boundary | **CONFIRMED** — no odds columns in design ✅ |
| Leakage violations | **0** ✅ |
| Estimated feature count | 28 ✅ |
| Summary hash (deterministic) | `b10a701d511e24cb` ✅ |
| PAPER_ONLY flag | `True` ✅ |
| Marker printed | `P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515` ✅ |

---

## 3. Pure Functions Confirmed Present

| Function | Testable | Description |
|---|---|---|
| `validate_feature_window(game_date, window_end)` | ✅ | Core leakage guard |
| `build_rolling_window_dates(game_date, window_days)` | ✅ | Returns (window_start, window_end) |
| `assert_no_odds_columns(columns)` | ✅ | Hard assertion, raises ValueError |
| `summarize_statcast_frame(df)` | ✅ | Summary dict, no side effects |
| `assert_output_path_gitignored(path)` | ✅ | Prevents raw data commit |
| `compute_summary_hash(summary)` | ✅ | Deterministic SHA-256[:16] |

---

## 4. CLI Flags Confirmed

```
--start-date    ✅
--end-date      ✅
--window-days   ✅ (default 14)
--summary-only  ✅ (default True)
--execute       ✅ (actual Statcast fetch)
--out-file      ✅ (local_only only)
--cache-dir     ✅ (default data/pybaseball/local_only/cache)
```

---

## 5. Invariants Confirmed (Design)

- Does NOT read `.env` or `THE_ODDS_API_KEY`
- Does NOT produce moneyline / CLV / sportsbook output
- All output must be under `data/pybaseball/local_only/` (gitignored)
- In `--summary-only` mode: zero external network calls

---

## 6. Acceptance Marker

```
P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515
```
