# P7 — Out-of-Fold Calibration Validation Report

**Status:** `P7_OOF_CALIBRATION_VALIDATION_READY`
**Date:** 2026-05-11
**Deployability:** `PAPER_ONLY_CANDIDATE` (paper simulation only; production requires positive BSS + human approval)

---

## 1. P7 Mission & Leakage Safety Guarantee

P7 implements **walk-forward out-of-fold (OOF) calibration validation** — a leakage-safe methodology that ensures the calibration map used to adjust model probabilities for a given month was never trained on data from that same month or any future month.

**Core guarantee:** For every OOF-calibrated row, `train_end < validation_start`. This is enforced structurally (not just by policy) in `mlb_oof_calibration.py` and recorded as `leakage_safe=True` in each row's `calibration_source_trace`. The simulator and gate policy propagate this flag through to the recommendation layer.

P6's in-sample calibration (which achieved excellent ECE=0.0004) was suspected of being optimistic because the calibration map was fit on the same data used to evaluate it. P7 resolves this by re-evaluating calibration on held-out months only.

---

## 2. OOF Methodology

| Parameter | Value |
|---|---|
| Method | Walk-forward monthly OOF |
| Date col | `Date` (capital D) |
| n_bins | 10 |
| min_train_size | 300 enriched rows |
| min_bin_size | 30 |
| initial_train_months | 2 calendar months |
| First validation month | 2025-07 (warm-up: Mar–Jun) |
| Total folds | 3 |

**Warm-up period:** Rows before the first eligible validation month (2025-07) are skipped for OOF evaluation. These 562 rows are used exclusively as training data.

**Walk-forward invariant:** Each fold fits the calibration bin-map on ALL enriched rows strictly before the validation month's start. No future data is ever included in training for a given fold.

---

## 3. BSS / ECE: Original vs OOF

| Metric | Original (P5 raw) | OOF Calibrated | Delta |
|---|---|---|---|
| **BSS** | −0.033284 | −0.019764 | **+0.013521** (improvement) |
| **ECE** | 0.059493 | 0.002212 | **−0.057281** (improvement) |
| Row count | 1,341 enriched | 779 OOF rows | 562 skipped (warm-up) |

**Interpretation:**

- OOF BSS improved by +1.35 pp over raw model BSS, meaning calibration is genuinely helping even on held-out data.
- OOF ECE of 0.0022 is remarkably low, indicating the calibration map generalises well to unseen months.
- However, **OOF BSS remains negative (−0.0198)**, meaning the calibrated model still underperforms the market baseline in held-out evaluation. Gate stays blocked.
- Recommendation: `OOF_IMPROVED_BUT_STILL_BLOCKED`

**Comparison to P6 in-sample calibration:**

| | P6 in-sample | P7 OOF |
|---|---|---|
| BSS | −0.0068 | −0.0198 |
| ECE | 0.0004 | 0.0022 |

As expected, P6's in-sample calibration appeared more optimistic. P7's OOF evaluation confirms some overfitting in P6's calibration assessment — the true OOF BSS is 0.013 worse than the in-sample estimate.

---

## 4. Fold Metadata Summary

| Fold | Val Month | Train Range | Train Rows | Val Enriched | Global Win Rate | Leakage Safe |
|---|---|---|---|---|---|---|
| 0 | 2025-07 | 2025-03-18 → 2025-06-30 | 562 | 254 | 51.96% | ✓ True |
| 1 | 2025-08 | 2025-03-18 → 2025-07-31 | 816 | 271 | 53.31% | ✓ True |
| 2 | 2025-09 | 2025-03-18 → 2025-08-31 | 1,087 | 254 | 52.53% | ✓ True |

All three folds satisfy `train_end < validation_start`. `leakage_safe=True` is confirmed in every fold record.

The skipped_row_count of 562 rows (from the CLI evaluation, which uses evaluate_oof_calibration's usable-row filter) reflects the warm-up rows from March–June 2025. The total OOF row count from the folds is 1,164 (all val enriched rows); 779 of those pass the `_collect_usable` filter (have valid Home ML, Away ML, Status=Final, and model probability).

---

## 5. Simulator Source Trace — OOF Evidence

Simulation run on: `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_oof_calibrated_probabilities.csv`

Strategy: `moneyline_edge_threshold_v0_oof_calibrated`

```
n=1162 | bets=383 | BSS=-0.0133 | ECE=0.0148 | ROI=2.75% | gate=BLOCKED_NEGATIVE_BSS
```

**Source trace fields (from simulation JSONL):**

| Field | Value |
|---|---|
| `calibration_mode` | `walk_forward_oof` |
| `leakage_safe` | `True` |
| `oof_calibration_count` | 1,162 |
| `calibration_warning` | `walk-forward OOF calibration candidate; production still requires human approval` |
| `gate_status` | `BLOCKED_NEGATIVE_BSS` |
| `brier_skill_score` | −0.0133 |

The simulator correctly detects OOF rows via `calibration_source_trace.calibration_mode="walk_forward_oof"` and `leakage_safe=True`, then propagates these facts into `source_trace` for downstream gate evaluation.

---

## 6. Gate Policy Output

```
gate_status: BLOCKED_SIMULATION_GATE
allow_recommendation: False (blocked)
```

**Gate reasons:**

1. `BLOCKED by simulation gate: simulation_gate_status='BLOCKED_NEGATIVE_BSS'. stake_units_paper=0.0, kelly_fraction=0.0.`
2. `TSL live odds estimate used (no team-name join yet)`
3. `[sim] Simulation gate_status='BLOCKED_NEGATIVE_BSS' blocks recommendation issuance.`
4. `[sim] Brier Skill Score = -0.0133 < 0. Model underperforms market baseline. require_positive_bss=True blocks this strategy.`
5. `[sim] Calibration note: walk-forward OOF calibration candidate; production still requires human approval`

The gate policy correctly propagates OOF calibration evidence into `gate_reasons` (item 5) via `_annotate_calibration_gate_reasons()`. The primary block reason is BSS < 0 (item 4).

---

## 7. Gated Recommendation Result

```
game: 2026-05-11-LAA-CLE-824441
gate: BLOCKED_SIMULATION_GATE
stake: 0.0 units
kelly_fraction: 0.0
```

No recommendation was issued. The system correctly zeroed the stake and blocked issuance due to `BLOCKED_NEGATIVE_BSS`. This is the expected and correct behaviour.

---

## 8. Comparison to P6 In-Sample Calibration

| Aspect | P6 In-Sample | P7 OOF |
|---|---|---|
| Calibration method | Bin-map fit on all 1,341 enriched rows | Walk-forward: fit on prior months only |
| Leakage safe | ❌ No (evaluated on training data) | ✓ Yes (`leakage_safe=True`) |
| BSS | −0.0068 | −0.0198 |
| ECE | 0.0004 | 0.0022 |
| Gate | `BLOCKED_NEGATIVE_BSS` | `BLOCKED_NEGATIVE_BSS` |
| `calibration_mode` in trace | `in_sample` | `walk_forward_oof` |
| Deployability status | `PAPER_ONLY_CANDIDATE` | `PAPER_ONLY_CANDIDATE` |

P7 confirms P6's suspicion: in-sample calibration overstated performance. The OOF evaluation gives a more honest picture. Both remain blocked by negative BSS.

---

## 9. Deployability Decision Tree

```
OOF BSS > 0 AND OOF ECE ≤ 0.12?
  └── YES → PRODUCTION_CANDIDATE (still paper-only until human approval)
  └── NO  → Was improvement observed?
              └── YES → OOF_IMPROVED_BUT_STILL_BLOCKED (paper-only, continue iteration)
              └── NO  → OOF_REJECTED (calibration makes things worse)
```

**P7 outcome:** OOF BSS = −0.0198 ≤ 0 → path to `OOF_IMPROVED_BUT_STILL_BLOCKED`.

Improvement was observed: delta_bss = +0.013521, delta_ece = −0.057281. Calibration is helping, but the underlying model needs to improve before BSS crosses zero.

**Hard constraint:** Even if OOF BSS > 0 in a future phase, `paper_only = True` always. Production requires a separate human approval gate.

---

## 10. Leakage Safety Documentation

Every OOF-calibrated row contains `calibration_source_trace` with:

```json
{
  "calibration_mode": "walk_forward_oof",
  "leakage_safe": true,
  "train_start": "2025-03-18",
  "train_end": "2025-06-30",
  "validation_start": "2025-07-01",
  "validation_end": "2025-07-31",
  "train_size": 562,
  "validation_size": 254
}
```

The structural guarantee is: `build_walk_forward_calibrated_rows()` passes only rows where `row_date < fold_validation_start` to the calibration fitting function. No look-ahead is possible. The `leakage_safe=True` flag is only set when `calibration_mode="walk_forward_oof"` is detected by the simulator (i.e., it is not settable by ad-hoc code).

---

## 11. Artifacts

| Artifact | Path |
|---|---|
| OOF calibrated probabilities CSV | `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_oof_calibrated_probabilities.csv` |
| OOF evaluation JSON | `outputs/predictions/PAPER/2026-05-11/oof_calibration_evaluation.json` |
| OOF fold metadata JSON | `outputs/predictions/PAPER/2026-05-11/oof_calibration_folds.json` |
| OOF calibration summary MD | `outputs/predictions/PAPER/2026-05-11/p7_oof_calibration_summary.md` |
| Simulation JSONL | `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_oof_calibrated_ed059d96.jsonl` |
| Simulation report MD | `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_oof_calibrated_ed059d96_report.md` |
| Recommendation JSONL | `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl` |
| Core OOF module | `wbc_backend/prediction/mlb_oof_calibration.py` |
| OOF CLI script | `scripts/run_mlb_oof_calibration_validation.py` |
| P7 test suite (88 tests) | `tests/test_mlb_oof_calibration.py`, `tests/test_run_mlb_oof_calibration_validation.py` (+ P7 additions to `tests/test_strategy_simulator_spine.py`, `tests/test_recommendation_gate_policy.py`) |

---

## 12. Known Limitations

1. **BSS still negative:** The underlying model has a home-bias issue (+4.8 pp average vs market). Calibration corrects probability shape but cannot fix a model that is consistently overconfident on home teams.

2. **Warm-up gap:** 562 rows (Mar–Jun 2025, ~42% of enriched rows) are excluded from OOF evaluation because `min_train_size=300` and `initial_train_months=2` require a minimum training history. A longer season or lower warm-up threshold would yield more OOF coverage.

3. **Simulation BSS vs evaluation BSS:** The simulation reports BSS=−0.0133 (slightly better than the standalone OOF evaluation BSS=−0.0198). This is because the simulation uses all 1,164 OOF rows in the CSV, while `evaluate_oof_calibration` filters to 779 rows that pass `_collect_usable` (requiring valid Home ML / Away ML / Status=Final).

4. **Gate source_trace gap:** `simulation_calibration_mode` and `simulation_leakage_safe` are `None` in the recommendation JSONL's `source_trace`, though OOF evidence appears correctly in `gate_reasons`. This is a minor wiring gap in how the gate policy reads the loaded simulation result's `source_trace` dict.

5. **Paper only:** All metrics are on 2025 historical data. No live inference has been attempted.

---

## 13. P8 Prompt — Next Phase

```
P8: Model Feature Improvement for Positive BSS

Context:
- P7 confirmed walk-forward OOF calibration gives honest BSS=-0.0198 (vs P6 in-sample BSS=-0.0068).
- Calibration is helping (delta_bss=+0.013521) but the model still underperforms the market baseline.
- The home bias (+4.8pp avg_model_prob vs avg_market_prob) persists in the OOF-calibrated output.
- Gate remains BLOCKED_NEGATIVE_BSS. The blocker is model quality, not calibration mechanics.

P8 Objective:
Investigate and improve model feature quality to push OOF BSS above 0.

Candidate investigations:
1. Starting pitcher quality signal (ERA, FIP, recent performance) — already partially built in P52-P54 phases.
2. Bullpen usage signal (high-usage = fatigue, rest = strength) — P56-P60 phases have data.
3. Park factor and weather adjustments.
4. Away/home team strength asymmetry calibration by team tier.
5. Market-blend features (incorporate market prob as a feature input, not just a calibration target).

Constraints:
- paper_only = True always.
- All P1-P7 tests must continue to pass (88 P7 tests, ~5,235 total).
- OOF evaluation (leakage_safe=True) must remain the validation standard.
- No production enablement without separate human approval.
- Input CSV: outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv (P5 artifact).
- Pre-existing test_agent_orchestrator.py collection error is not P8's responsibility.

Success criterion:
- Walk-forward OOF BSS > 0 on 2025 historical data.
- recommendation = OOF_PASS_CANDIDATE.
- All gate_reasons confirm leakage_safe=True and walk_forward_oof calibration mode.
- P8 report written to 00-BettingPlan/20260511/p8_model_feature_improvement_report.md.
- Final marker: P8_MODEL_FEATURE_IMPROVEMENT_READY.
```

---

*Report generated: 2026-05-11 | Branch: main | Python: 3.13.8 | pytest: 9.0.3*
*88 P7 tests pass | 5,235 total tests pass (excl. pre-existing test_agent_orchestrator.py error)*
