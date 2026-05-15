# P39C — P38A OOF × P39B Rolling Feature Join Contract
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Status**: RESEARCH ONLY — PAPER_ONLY=True, production_ready=False  
**Author**: CTO Agent  
**Depends on**:
- P38A: `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv`
- P38A identity bridge: `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv`
- P39B rolling feature script: `scripts/build_pybaseball_pregame_features_2024.py`
- P39B output format: `p39b_pybaseball_rolling_v1`

---

## ⚠️ Mandatory Constraints

> - PAPER_ONLY=True on all P39C artifacts
> - production_ready=False
> - No wagering, no live odds, no production write
> - No odds columns in any output
> - No betting decision derived from this join
> - No model edge claim
> - pybaseball is a baseball stats source — NOT an odds source
> - CLV still requires a separate licensed odds source (not resolved here)

---

## 1. Purpose

Join P38A OOF (out-of-fold) predictions with P39B rolling pybaseball features to
produce a **research-only enriched prediction input** suitable for future
feature-augmented modelling experiments.

This join:
- **Does NOT** involve odds, CLV, or betting decisions
- **Does NOT** claim production edge
- **Provides** pregame-safe batting feature enrichment (Statcast-derived)
- **Enables** future experiments: does adding rolling batting features improve
  the model's Brier score in CV?

---

## 2. P38A Side Expected Fields

Source: `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv`
+ identity bridge enrichment

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `game_id` | str | NO | Primary key. Format: `{HOME_TEAM}-{YYYYMMDD}-{N}` |
| `game_date` | str ISO | NO | Derived from `game_id` (split[1] → parse YYYYMMDD) |
| `home_team` | str | NO | Derived from `game_id` (split[0]) |
| `away_team` | str | NO | From identity bridge `mlb_2024_game_identity_outcomes_joined.csv` |
| `p_oof` | float [0, 1] | NO | Walk-forward OOF probability of home team win |
| `fold_id` | int | NO | Cross-validation fold identifier |
| `model_version` | str | NO | `p38a_walk_forward_logistic_v1` |
| `actual_result` / `y_true_home_win` | int {0, 1} | YES | From identity bridge (if joined) |

**Note:** `generated_without_y_true=True` in current P38A CSV — p_oof was generated
without target leakage.

---

## 3. P39B Side Expected Fields

Source: Rolling feature output from `build_rolling_features()` in
`scripts/build_pybaseball_pregame_features_2024.py`

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| `as_of_date` | str ISO | NO | Game date for which features are computed |
| `team` | str | NO | 3-letter MLB team code |
| `feature_window_start` | str ISO | NO | First day of rolling window |
| `feature_window_end` | str ISO | NO | Last day of rolling window (strictly < as_of_date) |
| `window_days` | int | NO | Rolling lookback length |
| `sample_size` | int | NO | Number of game-days in window with data |
| `leakage_status` | str | NO | Must equal `"pregame_safe"` |
| `rolling_pa_proxy` | float | YES | Rolling plate appearances proxy |
| `rolling_avg_launch_speed` | float | YES | Rolling mean launch speed (mph) |
| `rolling_hard_hit_rate_proxy` | float | YES | Rolling hard-hit rate (≥95 mph) |
| `rolling_barrel_rate_proxy` | float | YES | Rolling barrel rate (≥98 mph, 26–30°) |

**Banned columns**: No `odds`, `moneyline`, `spread`, `sportsbook`, `vig`, `implied`
(exact match or keyword substring) — enforced by `assert_no_odds_columns()`.

---

## 4. Join Logic

### 4.1 Primary Join Keys

```
HOME TEAM FEATURE JOIN:
  P38A.game_date == P39B.as_of_date
  AND P38A.home_team == P39B.team

AWAY TEAM FEATURE JOIN:
  P38A.game_date == P39B.as_of_date
  AND P38A.away_team == P39B.team
```

Both are **left joins** (P38A is left table). Missing feature rows produce `NaN`
in the output (fail-soft, no crash).

### 4.2 Column Prefixing

| Source | Prefix Applied To |
|--------|------------------|
| Home team features | `home_rolling_pa_proxy`, `home_rolling_avg_launch_speed`, ... |
| Away team features | `away_rolling_pa_proxy`, `away_rolling_avg_launch_speed`, ... |

**Columns NOT prefixed** (join keys, metadata):
`as_of_date`, `team`, `feature_window_start`, `feature_window_end`, `window_days`,
`leakage_status`, `source`

### 4.3 Derived Differential Features

| Feature | Formula |
|---------|---------|
| `diff_rolling_avg_launch_speed` | `home_rolling_avg_launch_speed - away_rolling_avg_launch_speed` |
| `diff_rolling_hard_hit_rate_proxy` | `home_rolling_hard_hit_rate_proxy - away_rolling_hard_hit_rate_proxy` |
| `diff_sample_size` | `home_sample_size - away_sample_size` |

All differential features may be `NaN` if either side is unmatched.

---

## 5. Leakage Rules

| Rule | Enforcement | On Violation |
|------|-------------|-------------|
| `feature_window_end < game_date` (strict D-1) | `validate_join_leakage()` | Raise / exit |
| Same-day feature window rejected | `feature_window_end == as_of_date` → violation | Raise / exit |
| Future feature window rejected | `feature_window_end > as_of_date` → violation | Raise / exit |
| `leakage_status == "pregame_safe"` required | `validate_join_leakage()` checks all rows | Raise / exit |
| No odds columns in inputs or output | `assert_no_odds_columns()` | Raise / exit |

---

## 6. Output Schema (Enriched)

Base P38A columns + prefixed feature columns + differential columns:

```
game_id, game_date, home_team, away_team, p_oof, fold_id, model_version,
[optional: y_true_home_win],
home_rolling_pa_proxy, home_rolling_avg_launch_speed,
home_rolling_hard_hit_rate_proxy, home_rolling_barrel_rate_proxy, home_sample_size,
away_rolling_pa_proxy, away_rolling_avg_launch_speed,
away_rolling_hard_hit_rate_proxy, away_rolling_barrel_rate_proxy, away_sample_size,
diff_rolling_avg_launch_speed, diff_rolling_hard_hit_rate_proxy, diff_sample_size
```

---

## 7. Known Limitations

1. **No away_team in P38A CSV**: must derive from identity bridge or game_id parsing
2. **pybaseball coverage**: only 2024 MLB season Statcast available (no historical depth)
3. **Sample size risk**: early season games (e.g. April 1–7) have < 7 game-day windows
4. **Team code mismatch**: Retrosheet codes (3-letter) vs Statcast codes may differ
   (e.g. CHA vs CHW, SDN vs SDP) — requires normalization layer (future work)
5. **No odds enrichment**: CLV, EV, and Kelly sizing still require a separate licensed
   odds source not yet available

---

## 8. Next Step: P39D

> P39D: Generate full 2024 rolling feature set (real Statcast pull) and enrich
> complete P38A OOF dataset. Requires: Statcast API access, team code normalization,
> and fixture validation with real data.

---

## Acceptance Marker

**P39C_FEATURE_JOIN_CONTRACT_20260515_READY**
