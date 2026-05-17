# P33: 2024 Prediction / Odds Gap Analysis — Report

**Marker**: `P33_2024_PREDICTION_ODDS_GAP_BUILDER_BLOCKED`
**Phase**: P33 — 2024 Prediction/Odds Gap Analysis
**Gate Result**: `P33_BLOCKED_NO_VERIFIED_PREDICTION_SOURCE`
**Date**: 2026-05-13
**PAPER_ONLY**: True | **PRODUCTION_READY**: False

---

## 1. Executive Summary

P33 executed a complete scan of all data directories in the repo for valid 2024
MLB prediction and market-odds source files.  **Zero ready sources were found for
either category.**  Every candidate file was blocked by one or more hard guards
(non-2024 year token, dry-run marker, missing `game_id` column, or missing
prediction/odds columns).

Gate is **BLOCKED**.  No fabricated predictions or odds were produced.  The next
phase (`P34_DUAL_SOURCE_ACQUISITION_PLAN`) must acquire at least one verified 2024
prediction file and one verified 2024 closing-odds file before the joined input
spec can be filled.

---

## 2. Scan Results

| Category | Candidates Found | Ready | Blocked |
|---|---|---|---|
| Prediction files | 467 | 0 | 467 |
| Odds files | 469 | 0 | 469 |

### Primary blocker reasons

- **Cross-year path token** — the vast majority of files live under `2025/`, `2026/`,
  or have `dry_run_2026-*` path fragments; the scanner rejects any file whose path
  contains a non-2024 year token.
- **No `game_id` column** — JSON and JSONL files that do contain numeric fields
  are not keyed by a game identifier compatible with the 2024 game log.
- **No prediction / odds columns** — result/outcome CSVs (e.g., P32 processed
  files) contain only identity and score columns, not model probabilities or
  decimal odds.

### Notable files inspected and rejected

| File | Reason |
|---|---|
| `data/mlb_2025/mlb_odds_2025_real.csv` | Path contains `2025`; season ≠ 2024 |
| `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl` | Path contains `2026`; dry-run flag |
| `outputs/predictions/PAPER/20260507/` … | Path contains `2026`; future-dated |

---

## 3. Required Schema for P34

The full 13-field joined input spec (`REQUIRED_JOINED_INPUT_FIELDS`) has been
written to:

```
data/mlb_2024/processed/p33_joined_input_gap/joined_input_required_spec.json
```

| # | Field | Source |
|---|---|---|
| 1 | `game_id` | P32 game log identity |
| 2 | `game_date` | P32 game log identity |
| 3 | `home_team` | P32 game log identity |
| 4 | `away_team` | P32 game log identity |
| 5 | `y_true_home_win` | P32 game outcomes |
| 6 | `p_model` | **MISSING — prediction source** |
| 7 | `p_oof` | **MISSING — prediction source** |
| 8 | `p_market` | **MISSING — odds source** |
| 9 | `odds_decimal` | **MISSING — odds source** |
| 10 | `source_prediction_ref` | provenance metadata |
| 11 | `source_odds_ref` | provenance metadata |
| 12 | `paper_only` | safety flag |
| 13 | `production_ready` | safety flag |

All 13 fields are recorded as `MISSING` in `joined_input_schema_gap.json`.  A
skeleton header-only CSV (`mlb_2024_joined_input_schema.csv`) and a gap-rows CSV
(`mlb_2024_joined_input_gap_rows.csv`) with game identity populated from P32 and
all prediction/odds cells null have been written for reference.

---

## 4. Prediction Source Recommendations (Research-Only)

All recommendations are `paper_only=True, production_ready=False`.  **Priority 1**
must be resolved before P34 can proceed.

### pred_r01 — Retrain local XGBoost/LightGBM on P32 gl2024 features ⭐ Priority 1

- **Acquisition**: Use P32 `mlb_2024_game_identity_outcomes_joined.csv` (2,429 rows)
  as the target, engineer features from gl2024.txt, and train an out-of-fold (OOF)
  model within the repo.
- **Required schema fields**: `game_id`, `p_model`, `p_oof`
- **License**: Self-generated; no external license required.
- **Effort**: Medium (≈2-3 days feature engineering + model training).
- **Blocker if skipped**: No 2024 calibrated prediction probability; EV analysis
  impossible.

### pred_r02 — FiveThirtyEight MLB ELO Archive ⭐ Priority 2

- **Reference**: https://github.com/fivethirtyeight/data/tree/master/mlb-elo
- **Format**: CSV, public GitHub.
- **License**: CC BY 4.0 — academic/research use permitted.
- **Effort**: Low (download and parse `mlb_elo.csv`, filter `season == 2024`).
- **Note**: ELO ratings are pre-game win-probability estimates; `elo_prob1` maps
  to `p_model`.

### pred_r03 — Baseball Prospectus PECOTA ⭐ Priority 3

- **Reference**: https://www.baseballprospectus.com/
- **Format**: CSV download (subscription required).
- **License**: Commercial subscription; verify terms before any redistribution.
- **Effort**: High.

---

## 5. Odds Source Recommendations (Research-Only)

### odds_r01 — sportsbookreviewsonline.com 2024 Closing Moneylines ⭐ Priority 1

- **Reference**: https://www.sportsbookreviewsonline.com/scoresoddsarchives/mlb/mlboddsarchives.htm
- **Format**: Excel/CSV download, freely available.
- **License**: Personal research use; check ToS before redistribution.
- **Effort**: Low (download per-month Excel files, parse home/away ML to decimal).
- **Required schema fields**: `game_id`, `p_market`, `odds_decimal`
- **Blocker if skipped**: No market prior; Kelly criterion and EV calculations
  cannot be validated.

### odds_r02 — The Odds API Historical Endpoint ⭐ Priority 2

- **Reference**: https://the-odds-api.com/historical-odds-api/
- **Format**: JSON REST API.
- **License**: Paid API key; historical snapshots available under paid plan.
- **Effort**: Medium (API key, pagination, date-range back-fill for 2024-03 to
  2024-09).

### odds_r03 — Pinnacle Historical Odds Archive ⭐ Priority 3

- **Reference**: https://www.pinnacle.com/en/betting-resources/betting-tools/historical-odds
- **Format**: CSV export.
- **License**: Verify terms; no-redistribution clause common.
- **Effort**: Medium.

---

## 6. Artifacts Written

```
data/mlb_2024/processed/p33_joined_input_gap/
  p33_gate_result.json                       ← gate=P33_BLOCKED_NO_VERIFIED_PREDICTION_SOURCE
  p33_source_gap_summary.json                ← full gap summary (prediction_missing=True, odds_missing=True)
  p33_source_gap_summary.md                  ← human-readable gap report
  prediction_source_candidates.csv           ← 467 candidates (all blocked)
  odds_source_candidates.csv                 ← 469 candidates (all blocked)
  source_recommendations.json                ← 3 prediction + 3 odds recommendations
  joined_input_required_spec.json            ← 13-field required spec
  joined_input_schema_gap.json               ← all 13 fields: MISSING
  mlb_2024_joined_input_schema.csv           ← header-only template
  mlb_2024_joined_input_gap_rows.csv         ← 2,429 game-identity rows, pred/odds null
  mlb_2024_joined_input_schema_manifest.json ← artifact manifest
```

---

## 7. Test Coverage

| Test File | Tests |
|---|---|
| `test_p33_prediction_odds_gap_contract.py` | contract, gates, fields, dataclasses |
| `test_p33_2024_source_gap_auditor.py` | CSV/JSON readers, path helpers, classifiers, scanner |
| `test_p33_joined_input_spec_validator.py` | spec builder, leakage detection, schema gap |
| `test_p33_safe_source_recommendation_builder.py` | catalogues, builders, safety validator |
| `test_p33_joined_input_skeleton_writer.py` | all 5 skeleton writers, validate outputs |
| `test_run_p33_2024_prediction_odds_gap_builder.py` | CLI guards, gate logic, main() integration |
| **Total** | **203 tests — all pass** |

---

## 8. Determinism

Running the CLI twice produces the same gate:
`P33_BLOCKED_NO_VERIFIED_PREDICTION_SOURCE` (verified via `_determinism_check`).

---

## 9. Next Phase

**P34 — Dual Source Acquisition Plan**

P34 must acquire:
1. A verified 2024 MLB game-level prediction file (recommended: retrain OOF model
   from P32 gl2024 features — `pred_r01`).
2. A verified 2024 MLB closing moneyline odds file (recommended:
   sportsbookreviewsonline.com archive — `odds_r01`).

Only after both sources are validated and joined to the P32 game identity spine
can the joined input spec be certified `P33_PREDICTION_ODDS_GAP_PLAN_READY` and
EV analysis proceed.

---

`P33_2024_PREDICTION_ODDS_GAP_BUILDER_BLOCKED`
