# P39A Pybaseball Pregame-Safe Leakage Policy — 2026-05-15

**Task Round:** P3.8 / P39A — TRACK 2  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`  
**Generated:** 2026-05-15

---

## 0. Policy Overview

**Zero tolerance for look-ahead leakage.** Every feature row must be provably derivable
from information available **before first pitch** of the game being predicted.

Violation: reject row, write audit finding, do not silently fill or impute.

---

## 1. Core Temporal Cutoff Rule

Given a game with `game_date = D` and first pitch time `T`:

| Rule | Expression |
|---|---|
| **Feature window end** | `feature_window_end <= D - 1` (day boundary) |
| **Feature window start** | `feature_window_start = D - N_days` |
| **Data used** | Only Statcast / game records with `game_date < D` |
| **Same-day data** | FORBIDDEN — see Section 3 |

```python
def validate_feature_window(game_date: date, feature_window_end: date) -> bool:
    """Returns True iff window end is strictly before game_date."""
    return feature_window_end < game_date
```

**Violation**: If `feature_window_end >= game_date` → `leakage_status = leakage_detected`. Reject row.

---

## 2. Rolling Window Conventions

### Day-Based Windows (batting / team form)

```
game_date = D
window_7d  → [D-7, D-1] (inclusive both ends)
window_14d → [D-14, D-1]
window_30d → [D-30, D-1]
```

### Start-Based Windows (pitcher stats)

```
L3 starts → the 3 most recent game dates where pitcher appeared as SP, all < D
L5 starts → the 5 most recent game dates where pitcher appeared as SP, all < D
```

Both day-based and start-based windows use **strictly < game_date** as the upper bound.

### Minimum Sample Size

| Feature Type | Minimum Sample | If Below Minimum |
|---|---|---|
| Team rolling batting | 3 games | `feature_value = NaN`, `leakage_status = review_required` |
| SP rolling | 1 start | `feature_value = NaN`, `leakage_status = review_required` |
| Bullpen rolling | 1 game | `feature_value = NaN`, `leakage_status = review_required` |

NaN rows are retained in output for auditing. Do NOT fill with global mean unless explicitly specified.

---

## 3. Same-Day Game Isolation Rule

The 2024 MLB schedule includes **doubleheaders** (two games on same day, same teams).

### Rule

> A feature computed for Game 2 of a doubleheader **MUST NOT** use any Statcast data
> from Game 1 of the same doubleheader.

### Implementation

```
game_identifier = (game_date, home_team, away_team, game_pk)

For Game 2 of doubleheader (identified by game_pk):
    feature_window_end = game_date - 1  (previous calendar day)
    Do NOT include game_date records, even from Game 1
```

**Rationale**: When predicting Game 2, Game 1 has already started / completed.
Including Game 1 outcomes constitutes look-ahead leakage in a pregame model.

Exception: If the model is explicitly time-stamped (first pitch time of Game 2 > completion time of Game 1) and the use case is clearly post-Game-1 / pre-Game-2, this can be revisited in a separate leakage policy revision. Default = forbidden.

---

## 4. Postponed / Suspended Game Handling

| Scenario | Rule |
|---|---|
| Game postponed (no result) | Drop from result set. Do not treat as win or loss. |
| Game suspended mid-game | Drop partial game from rolling stats if result not yet official. |
| Game resumed on later date | Treat resumed date as the official `game_date` for outcome. |
| Rain delay (same-day completion) | Game still counts for that day's record — no special handling needed. |

Implementation: use `game_pk` as the unique game identifier. Check `post_home_score` / `post_away_score` for null → drop from outcome-dependent features.

---

## 5. Timezone / Game Start Time Ambiguity

| Issue | Rule |
|---|---|
| Statcast `game_date` is UTC date | Treat as local date of the game; do not convert to UTC midnight |
| Day games vs night games on same date | Both belong to same `game_date`; safe cutoff is end of D-1 |
| West coast games ending after midnight UTC | Still assigned to local game_date (MLB convention) — no override needed |
| First pitch time unknown | Default to conservative cutoff: `feature_window_end = game_date - 1` |

> **Conservative default**: When in doubt, use `D-1` as cutoff. Never use `D`.

---

## 6. Odds / Market Data Isolation

| Rule | Enforcement |
|---|---|
| No moneyline column in feature output | `assert_no_odds_columns(df.columns)` |
| No closing line | Same assertion |
| No implied probability from vig | Same assertion |
| No CLV | Same assertion |
| No line movement feature | Same assertion |

```python
FORBIDDEN_ODDS_COLUMNS = {
    "moneyline", "closing_line", "opening_line", "odds", "vig",
    "implied_prob", "home_ml", "away_ml", "home_odds", "away_odds",
    "clv", "closing_implied_prob", "no_vig_prob",
}

def assert_no_odds_columns(columns: list[str]) -> None:
    found = set(columns) & FORBIDDEN_ODDS_COLUMNS
    if found:
        raise ValueError(f"LEAKAGE_DETECTED: Odds columns in feature output: {found}")
```

This assertion must run on every feature DataFrame before save or downstream join.

---

## 7. Actual Result / Label Leakage

| Rule | Enforcement |
|---|---|
| Do NOT include `y_true` (win/loss) in features | Drop `y_true`, `home_win`, `away_win`, `final_score` from feature table |
| Do NOT use postgame run totals as features | Postgame run total = result leakage |
| Rolling win rate: use only games with `game_date < D` | Validated by core cutoff rule |
| Do NOT use in-game stats from the game being predicted | Must filter by `game_pk != target_game_pk` |

---

## 8. Violation Handling Protocol

When any violation is detected:

### Step 1 — Mark Row

```
leakage_status = "leakage_detected"
```

### Step 2 — Reject Row

Do NOT include row in downstream pipeline. Write to audit log.

### Step 3 — Write Audit Finding

```
audit_finding = {
    "game_date": str,
    "team": str,
    "feature_name": str,
    "violation_type": "window_overlap" | "odds_column" | "result_leakage" | "same_day_data",
    "detail": str,
    "rejected_at": ISO8601_UTC,
}
```

Audit log path: `data/pybaseball/local_only/p39a_leakage_audit_{date}.jsonl` (gitignored)

### Step 4 — Do NOT Silently Fill

Do not replace rejected rows with:
- Global mean imputation
- Prior game value
- Constant fill
- NaN-fill that masks the violation

Raise or log explicitly. Downstream consumers must handle missing features explicitly.

---

## 9. leakage_status Field Values

| Value | Meaning |
|---|---|
| `pregame_safe` | All window checks passed; no forbidden columns; safe to use |
| `review_required` | Below minimum sample size; use with caution |
| `leakage_detected` | Window overlap or forbidden data detected; REJECT |

---

## 10. Pre-Run Checklist (Mandatory)

Before running any feature build:

- [ ] Confirm `game_date` column is `datetime.date` not `str` (comparison safety)
- [ ] Confirm `feature_window_end < game_date` for all rows
- [ ] Run `assert_no_odds_columns(df.columns)`
- [ ] Confirm `y_true` / `home_win` / `away_win` not in feature output
- [ ] Confirm doubleheader pairs are handled (see Section 3)
- [ ] Confirm postponed games dropped (see Section 4)
- [ ] Write `generated_at` (UTC) to every row

---

## 11. Acceptance Marker

```
P39A_PYBASEBALL_PREGAME_SAFE_POLICY_20260515_READY
```
