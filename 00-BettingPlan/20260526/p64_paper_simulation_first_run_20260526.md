# P64 — Paper Simulation First Run

**Date:** 2026-05-26
**Phase:** P64
**Classification:** `P64_PAPER_SIMULATION_FIRST_RUN_READY`
**Prior Phase:** P63 `P63_READY_FOR_CEO_REVIEW` (commit `2a0052a`)
**Branch:** `main`

---

## 1. CEO Approval

CEO approval phrase granted:

> `YES approve P62 contract and proceed with P64 paper simulation first run`

P62 contract version: `P62_v1_20260526`
P63 classification at approval: `P63_READY_FOR_CEO_REVIEW`

---

## 2. Governance Flags (Immutable)

| Flag | Value |
|---|---|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `promotion_freeze` | `True` |
| `kelly_deploy_allowed` | `False` |
| `live_api_calls` | `0` |
| `paid_api_called` | `False` |
| `runtime_recommendation_logic_changed` | `False` |
| `real_bet_allowed` | `False` |
| `production_ready` | `False` |
| `2024_data_gap_remains_unresolved` | `True` |

All flags enforced in every emitted row. No exceptions.

---

## 3. Data Sources (Local Only)

| Artifact | Path |
|---|---|
| P62 Contract | `data/mlb_2025/derived/p62_paper_recommendation_contract_draft_summary.json` |
| P63 Readiness | `data/mlb_2025/derived/p63_paper_recommendation_contract_review_readiness_summary.json` |
| Predictions | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` |
| Odds CSV | `data/mlb_2025/mlb_odds_2025_real.csv` |
| P45 Platt | `data/mlb_2025/derived/p45_platt_recalibration_summary.json` |
| P52 Thresholds | `data/mlb_2025/derived/p52_monitoring_contract_v2_summary.json` |

No live API calls. No TSL crawler calls. No paid odds API calls.

---

## 4. Platt Calibration Constants

| Constant | Value | Source | Status |
|---|---|---|---|
| `platt_A` | `0.435432` | P45 artifact | Locked — never refit |
| `platt_B` | `0.245464` | P45 artifact | Locked — never refit |
| Method | `platt_scaled` | — | Unchanged |

Formula: `calibrated = 1 / (1 + exp(-A * logit(model_prob) - B))`

Verified against P62 sample illustration: `model_prob=0.640146 → calibrated≈0.6216`.

---

## 5. Signal and Tier

| Parameter | Value | Status |
|---|---|---|
| Signal | `sp_fip_delta` | Unchanged |
| Tier | `Tier_C` | Locked |
| Threshold | `0.50` | `T_LOCKED` — never re-optimized |
| Market | `moneyline` | — |

---

## 6. Simulation Results

### 6.1 Row Counts

| Metric | Count |
|---|---|
| Total predictions loaded | 2,025 |
| Tier C games (|sp_fip_delta| ≥ 0.50) | **535** |
| Odds matched (date + home_team join) | **535** |
| Unmatched | **0** |
| Total rows emitted | **535** |

All 535 rows matched to `mlb_odds_2025_real.csv` via (game_date, home_team) join. 100% match rate.

### 6.2 Gate Statistics

| Status | Count |
|---|---|
| `GATE_PASS` | 535 |
| `GATE_BLOCK` | 0 |

| Recommendation Status | Count |
|---|---|
| `PAPER_ELIGIBLE_CONTRACT_ONLY` | 535 |

### 6.3 Edge Statistics (Theoretical — Paper Only)

| Metric | Value |
|---|---|
| Edge mean | `-0.032473` |
| Positive edge rows | `200 / 535` |
| Negative edge rows | `335 / 535` |

**Interpretation (diagnostic only):**
The mean edge is negative, meaning the market's implied probability is on average 3.2 pp higher than the model's calibrated probability for the favored side. 200/535 (37.4%) of Tier C games show positive model edge. These figures are **not production-ready conclusions** and require walk-forward validation (P65) before any further inference.

---

## 7. Forbidden Affirmative Scan

| Result | Violations |
|---|---|
| `CLEAN` | `0` |

9 forbidden terms scanned across all 535 rows. Zero violations detected.
No affirmative profit claims. No production readiness claims. No live deployment claims.

---

## 8. P62 Contract Compliance

| Contract Requirement | Status |
|---|---|
| All 33 schema fields present in every row | ✅ |
| `contract_version = P62_v1_20260526` | ✅ |
| `signal_tier = Tier_C` | ✅ |
| `tier_threshold = 0.50` | ✅ |
| `calibration_method = platt_scaled` | ✅ |
| `platt_A = 0.435432` | ✅ |
| `platt_B = 0.245464` | ✅ |
| `market = moneyline` | ✅ |
| `paper_only = True` (every row) | ✅ |
| `diagnostic_only = True` (every row) | ✅ |
| `production_ready = False` (every row) | ✅ |
| `real_bet_allowed = False` (every row) | ✅ |
| `kelly_deploy_allowed = False` (every row) | ✅ |
| `odds_source_trace` non-empty (GATE_PASS rows) | ✅ |
| Gate reasons non-empty for GATE_BLOCK rows | ✅ (no GATE_BLOCK rows) |
| 2024 data gap documented | ✅ |
| No live API calls | ✅ |
| No paid API calls | ✅ |

---

## 9. 2024 Data Gap Status

The 2024 MLB closing-line data gap remains **UNRESOLVED** as of P64.

- P64 covers 2025 games only.
- P61 PATH_A (The Odds API, ~$30–50) and PATH_B (Kaggle/GitHub, $0) have not been executed.
- 2024 extension is blocked until P61 resolution with CEO authorization.
- This constraint is documented in every P64 output artifact.

---

## 10. Output Artifacts

| File | Description |
|---|---|
| `data/mlb_2025/derived/p64_paper_simulation_rows.jsonl` | 535 emitted paper simulation rows |
| `data/mlb_2025/derived/p64_paper_simulation_first_run_summary.json` | Machine-readable summary |
| `scripts/_p64_paper_simulation_first_run.py` | P64 pipeline script |
| `tests/test_p64_paper_simulation_first_run.py` | 36 tests |
| `report/p64_paper_simulation_first_run_20260526.md` | This report |
| `00-BettingPlan/20260526/p64_paper_simulation_first_run_20260526.md` | BettingPlan copy |

---

## 11. Tests

| Scope | Result |
|---|---|
| P64 targeted (36 tests) | **36/36 PASS** |
| Regression P43+P59+P60+P61+P62+P63+P64 | **155/155 PASS** |

Test coverage includes: CEO approval gate, P62 contract load, P63 readiness check, P45 Platt constants, P52 thresholds, Tier C filter, all 33 fields, all governance invariants, no API calls, no postgame leakage, edge/Kelly calculations, status distribution, forbidden scan, 2024 gap.

---

## 12. Limitations

1. **Timestamps are paper-constructed pregame proxies.** The source backtest data (`phase56_sp_bullpen_context_v1`) does not carry real prediction or odds timestamps. All timestamps are constructed as `{game_date}T12:00:00Z` / `T15:00:00Z` / `T17:00:00Z` UTC.
2. **model_home_prob is from backtest, not live inference.** Phase 56 backtest probabilities may differ from a live model deployment.
3. **2024 data gap unresolved.** P43 potential upgrade from `BLOCKED` to `CONFIRMED` requires P61 resolution.
4. **Kelly fractions are theoretical.** `kelly_deploy_allowed=False` is enforced in every row.
5. **No odds API was called.** All odds from `mlb_odds_2025_real.csv` — a local, user-supplied artifact.

---

## 13. Recommended Next Steps

| Option | Description |
|---|---|
| **P65** | Walk-forward validation: split 2025 Tier C rows by time window, assess out-of-sample edge stability |
| **P61 PATH_B** | Free-source 2024 data gap search (Kaggle/GitHub, $0, no CEO auth required) |
| **P61 PATH_A** | The Odds API historical data (~$30–50, requires CEO authorization) |

CEO must authorize the next step explicitly.

---

## 14. Framing Note

> P64 is a **paper-only, diagnostic-only** simulation.
> No rows may be used for live betting decisions.
> Edge calculations are theoretical and have not been validated in live deployment.
> This report does not claim profitability, production readiness, or betting advice.
> 2025 data only — 2024 data gap is documented and unresolved.

---

*Report generated: 2026-05-26 | Classification: P64_PAPER_SIMULATION_FIRST_RUN_READY*
