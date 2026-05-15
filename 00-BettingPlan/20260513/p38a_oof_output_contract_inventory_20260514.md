# P38A OOF Output Contract Inventory — 2026-05-14

**Status:** RESEARCH ONLY — PAPER_ONLY=True, production_ready=False  
**Author:** CTO Agent  
**Date:** 2026-05-14  
**Scope:** P38A 2024 MLB walk-forward OOF prediction output — schema & join readiness  
**Acceptance Marker:** P38A_OOF_OUTPUT_CONTRACT_INVENTORY_20260514_READY

---

## ⚠️ Scope Constraints

> This document describes the P38A OOF prediction output for research and join-readiness planning.
> - PAPER_ONLY=True on all P38A artifacts
> - production_ready=False on all P38A artifacts
> - No wagering, no live odds, no production write
> - gate: P38A_2024_OOF_PREDICTION_READY (already cleared)

---

## 1. P38A Artifact Paths

| Artifact | Path | Status |
|---|---|---|
| **Prediction output CSV** | `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv` | ✅ EXISTS |
| **OOF metrics JSON** | `outputs/predictions/PAPER/p38a_2024_oof/p38a_oof_metrics.json` | ✅ EXISTS |
| **Gate result JSON** | `outputs/predictions/PAPER/p38a_2024_oof/p38a_gate_result.json` | ✅ EXISTS |
| **CLI runner script** | `scripts/run_p38a_2024_oof_prediction_rebuild.py` | ✅ EXISTS |
| **OOF builder module** | `wbc_backend/recommendation/p38a_oof_prediction_builder.py` | ✅ EXISTS |
| **Feature adapter module** | `wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py` | ✅ EXISTS |
| **Source game log (raw)** | `data/mlb_2024/raw/gl2024.txt` | ✅ EXISTS (untracked) |
| **Game identity + outcomes join** | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` | ✅ EXISTS |
| **Rebuild plan doc** | `00-BettingPlan/20260513/p38a_retrosheet_oof_rebuild_plan_20260513.md` | ✅ EXISTS |
| **Execution report** | `00-BettingPlan/20260515/p38a_and_market_schema_execution_report_20260515.md` | ✅ EXISTS |

---

## 2. Deterministic Hash Record

| Field | Value |
|---|---|
| **output_hash (SHA-256)** | `7134eda90c848826e1acc97e76c984c89a811b2e5467f4e92b0e79647e26e099` |
| **hash_source** | SHA-256 of `p_oof` column values sorted by `game_id` |
| **deterministic** | YES — fixed RANDOM_STATE=42, no shuffle, reproducible across runs |
| **commit ref** | `3a9bec9` (local only as of 2026-05-14) |

---

## 3. P38A Prediction Output Schema

**File:** `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv`  
**Row count:** 2,187 rows (+ 1 header)  
**Total input rows:** 2,429  
**Coverage:** 90.04% (rows missing p_oof: 242, due to insufficient training window in early folds)

| # | Column Name | Dtype | Nullable | Example Value | Join Key? | Pregame-Safe? |
|---|---|---|---|---|---|---|
| 1 | `game_id` | string | NO | `BAL-20240415-0` | ✅ PRIMARY JOIN KEY | ✅ YES |
| 2 | `fold_id` | integer (0–9) | NO | `0` | ❌ no | ✅ YES |
| 3 | `p_oof` | float64 [0.0, 1.0] | NO | `0.4879` | ❌ no | ✅ YES — generated without y_true |
| 4 | `model_version` | string (constant) | NO | `p38a_walk_forward_logistic_v1` | ❌ no | ✅ YES |
| 5 | `source_prediction_ref` | string (16-char hex) | NO | `1dbddd8e47e39624` | ❌ audit only | ✅ YES |
| 6 | `generated_without_y_true` | bool | NO | `True` | ❌ no | ✅ YES — confirmed all True |

### 3.1 game_id Format Specification

```
{HOME_TEAM}-{YYYYMMDD}-{GAME_NUMBER}

Examples:
  BAL-20240415-0   → Baltimore Orioles home, 2024-04-15, single/first game
  BAL-20240415-1   → Baltimore Orioles home, 2024-04-15, second game (DH)
  LAN-20240320-0   → Los Angeles Dodgers home, 2024-03-20, single game
```

**Team code standard:** Retrosheet 3-letter code (e.g., `NYA`, `LAN`, `CHA`, `SDN`)
**Date format in game_id:** `YYYYMMDD` (compact, no separators)
**Game number:** `0` = single game or first game of DH; `1` = second game of DH

### 3.2 Derived Fields (parseable from game_id)

| Derived Field | Derivation Rule | Example |
|---|---|---|
| `home_team` | Split on `-`, take index 0 | `BAL` |
| `game_date` | Split on `-`, take index 1, parse as YYYYMMDD → YYYY-MM-DD | `2024-04-15` |
| `doubleheader_game_num` | Split on `-`, take index 2, cast int | `0` or `1` |

---

## 4. Fields NOT Present in P38A Output (Gaps)

| Field | Status | Resolution |
|---|---|---|
| `away_team` | ❌ NOT in output | Derivable via join to `mlb_2024_game_identity_outcomes_joined.csv` on `game_id` |
| `home_team` (explicit col) | ❌ NOT in output | Parseable from `game_id` (index 0) |
| `game_date` (explicit col) | ❌ NOT in output | Parseable from `game_id` (index 1) |
| `actual_result / home_win` | ❌ NOT in output — intentionally excluded | Join to `y_true_home_win` from `mlb_2024_game_identity_outcomes_joined.csv` |
| `home_score / away_score` | ❌ NOT in output | Join to game identity CSV |
| `train_start / test_window` | ❌ NOT explicit | `fold_id` encodes fold index; fold window metadata in `p38a_oof_metrics.json` |
| `generated_at` timestamp | ❌ NOT per-row | Gate JSON has implicit timestamp via commit |
| `run_id` | ❌ NOT in output | `output_hash` + `model_version` serves as run identity |
| `season` | ❌ NOT explicit | Inferred as 2024 from `game_date` |

---

## 5. Join Readiness Assessment

### 5.1 Direct Join Keys Available

| Key | P38A Column | Odds Side Equivalent |
|---|---|---|
| `game_id` | `game_id` | `game_id_optional` / `retrosheet_game_id_optional` in manual import contract |
| `home_team` (derived) | parsed from `game_id[0]` | `home_team` in contract |
| `game_date` (derived) | parsed from `game_id[1]` | `game_date` in contract |
| `doubleheader_game_num` (derived) | parsed from `game_id[2]` | no direct equivalent — must be derived |

### 5.2 Derived Join Keys Needed

| Gap | Resolution |
|---|---|
| `away_team` | Join P38A → game identity CSV, then use `away_team` for secondary key |
| `game_date` as ISO string | Parse from `game_id` middle segment (`YYYYMMDD` → `YYYY-MM-DD`) |
| Season | Extract year from `game_date` |

### 5.3 Team Normalization Needed

| Issue | Detail |
|---|---|
| Retrosheet vs common abbreviation | `CHA` (White Sox) vs `CHW`; `NYA` (Yankees) vs `NYY`; `LAN` (Dodgers) vs `LAD` |
| Retrosheet codes used by P38A | YES — inherited from `mlb_2024_game_identity_outcomes_joined.csv` |
| Odds dataset team naming | Varies by source (see candidate inventory v2) — normalization required |
| Normalization table | Must be defined in join key mapping spec before any join |

### 5.4 Date Normalization Needed

| Issue | Detail |
|---|---|
| Compact vs ISO format | P38A: `YYYYMMDD` in game_id; contract: `YYYY-MM-DD` string |
| Local date vs UTC | P38A uses local game date (from Retrosheet). Odds datasets may use UTC. |
| Postponed games | Not in P38A output (only completed games in GL2024.TXT) |
| Double-headers | Handled via game_id suffix (`-0`, `-1`). Odds source may lack this disambiguation. |

### 5.5 Unresolved Gaps

| Gap | Risk | Mitigation |
|---|---|---|
| `away_team` not in P38A CSV | Medium — requires secondary join to game identity | Use `mlb_2024_game_identity_outcomes_joined.csv` as bridge |
| Odds source lacks `game_id` / Retrosheet ID | High — most odds CSVs don't carry Retrosheet IDs | Fall back to `(game_date, home_team, away_team)` composite key |
| Retrosheet team codes not universal | Medium — must normalize for each odds source | Normalization table in join key mapping spec |
| Double-header disambiguation | Low for now (few DH in 2024) | Track `game_id` suffix vs odds source's handling |
| Odds source timestamp policy | High — closing odds may be postgame | Classify closing-line use as research-benchmark only, not pregame simulation |

---

## 6. P38A Metrics Summary (for reference)

| Metric | Value |
|---|---|
| n_predictions | 2,187 |
| coverage_pct | 90.04% |
| brier | 0.2487 |
| log_loss | 0.6905 |
| brier_skill_score (vs base-rate) | +0.0020 |
| base_rate | 52.81% |
| fold_count | 10 |
| paper_only | True |
| production_ready | False |

---

## 7. Supporting Game Identity CSV Schema

**File:** `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv`

| Column | Role |
|---|---|
| `game_id` | Primary join key (matches P38A game_id format exactly) |
| `game_date` | ISO string YYYY-MM-DD |
| `season` | Integer year |
| `away_team` | Retrosheet 3-letter code |
| `home_team` | Retrosheet 3-letter code |
| `source_name` | "Retrosheet" |
| `source_row_number` | Retrosheet GL row number |
| `away_score` | Final score (NOT for pregame features) |
| `home_score` | Final score (NOT for pregame features) |
| `y_true_home_win` | 1=home win, 0=away win (NOT for pregame features) |

**Join path:** `p38a_2024_oof_predictions.csv` ← `game_id` → `mlb_2024_game_identity_outcomes_joined.csv`

---

## 8. Acceptance Marker

```
P38A_OOF_OUTPUT_CONTRACT_INVENTORY_20260514_READY
```
