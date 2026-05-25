# P47 Calibration Strategy Consolidation — P43-P46 Synthesis Report

**Date:** 2026-05-26
**Phase:** P47 (synthesis diagnostic, paper_only=true)

## Executive Summary

Phases P43-P46 completed a full diagnostic arc on the 2025 Tier C sp_fip_delta edge signal. The key findings are: (1) the edge is real and temporally stable across all 6 months of the 2025 MLB season; (2) the raw sigmoid model is moderately miscalibrated (ECE=0.0953); (3) Platt scaling reliably reduces ECE to ~0.07-0.09 across CV and walk-forward evaluation; (4) Isotonic regression shows no consistent advantage over Platt in temporal out-of-sample tests. **Selected monitoring stream: Platt calibrated probability.** No champion replacement. No deployment. 2024 data gap remains unresolved.

## Governance Flags
- paper_only: `True`
- diagnostic_only: `True`
- promotion_freeze: `True`
- kelly_deploy_allowed: `False`
- live_api_calls: `0`
- tsl_crawler_modified: `False`
- champion_strategy_changed: `False`
- production_usage_proposed: `False`
- runtime_recommendation_logic_changed: `False`

## P43-P46 Evidence Table

| Phase | Key Result | Classification |
|-------|-----------|----------------|
| P43 | Tier C n=535, mean_edge=0.1059, CI fully positive | `EDGE_CONFIRMED` |
| P44 temporal | 6/6 months STABLE, n=535 | `TEMPORAL_STABLE` |
| P44 calibration | ECE=0.095289, Brier=0.248133 | `MODERATE_MISCALIBRATED` |
| P45 Platt | CV ECE 0.1168→0.0862, WF=WALK_FORWARD_HELPFUL | `P45_RECALIBRATION_HELPFUL` |
| P46 Isotonic | CV ECE iso=0.0842 vs platt=0.0862, beats Platt 2/5 folds | `P46_MIXED_RECALIBRATION_DIAGNOSTIC` |

## Selected Monitoring Probability Stream

**Selected: `PLATT_CALIBRATED`**

### Rationale
- P45 Platt: CV mean ECE 0.1168 → 0.0862 (Δ +0.0307)
- P45 Walk-forward: WALK_FORWARD_HELPFUL
- P46 Isotonic: CV mean ECE 0.0842 vs Platt 0.0862 (Δ +0.0020)
- P46 Isotonic beats Platt in 2/5 CV folds
- P46 Walk-forward: PLATT_WALK_FORWARD_PREFERRED
- Platt selected: CV ECE improvement confirmed (+0.0307), walk-forward helpful. Isotonic not preferred due to weak CV (beats Platt only 2/5 folds) and walk-forward preference for Platt (P46.C PLATT_WALK_FORWARD_PREFERRED).

### Why Platt is preferred over Isotonic
- Isotonic achieves marginally lower ECE on a single train/test split (0.058 vs 0.070)
- In 5-fold CV, Isotonic only beats Platt in 2/5 folds; mean ECE gap is only 0.002
- Walk-forward temporal evaluation shows Platt preferred in 3/5 months (PLATT_WALK_FORWARD_PREFERRED)
- Platt is a 2-parameter parametric model; Isotonic has 13+ knots and more capacity to overfit
- For monitoring purposes, Platt's temporal stability is more important than single-split ECE

### Why Raw Sigmoid is not retained after P45
- Raw ECE=0.0953 is MODERATE_MISCALIBRATED — systematic bias confirmed
- Platt CV mean ECE=0.0862 shows consistent improvement (Δ +0.0307)
- P45 walk-forward: all 5 evaluation months show ECE improvement after Platt
- No reason to accept higher miscalibration when a stable recalibration is available

## Monitoring Thresholds (Diagnostic Guardrails Only)

These are advisory thresholds for future monitoring. They are NOT betting instructions.

| Metric | Baseline | Warning | Critical |
|--------|----------|---------|----------|
| ECE | 0.086164 | > 0.1 | > 0.12 |
| Brier | 0.238477 | > 0.25 | > 0.27 |
| Mean Edge | 0.1059 | < 0.07 | CI crosses zero |
| Monthly stability | All CI positive | Any CI crosses zero | Two consecutive months |
| Sample batch | — | — | n < 100 → SAMPLE_LIMITED |

## Data Gap Register

| Gap | Status | Priority |
|-----|--------|----------|
| 2024 MLB closing-line odds (Home ML / Away ML) | UNAVAILABLE — no CSV or API source exists in repository... | HIGH |
| Cross-year market-edge validation | BLOCKED by 2024 closing-line odds gap... | HIGH |
| 2026 live odds (real-time TSL integration) | BLOCKED by no-live-call governance (live_api_calls=0)... | MEDIUM |
| External odds source provenance documentation | mlb_odds_2025_real.csv marked is_verified_real=False for mos... | MEDIUM |
| Approved paper-trading monitoring loop | Not approved — promotion_freeze=true... | LOW |

### Gap Details

**2024 MLB closing-line odds (Home ML / Away ML)** (`HIGH`)
- Status: UNAVAILABLE — no CSV or API source exists in repository
- Impact: Cross-year (2024+2025) closing-line edge validation is blocked. P43 final classification remains P43_BLOCKED_BY_DATA_GAP. Only 2025 single-year EDGE_CONFIRMED available.
- Resolution: Source a 2024 MLB moneyline odds CSV with schema matching mlb_odds_2025_real.csv (Date, Away, Home, Away ML, Home ML, Away Score, Home Score). Verified external source required — e.g., historical odds API or vendor export.

**Cross-year market-edge validation** (`HIGH`)
- Status: BLOCKED by 2024 closing-line odds gap
- Impact: Cannot confirm that Tier C edge generalizes across seasons. Single-year 2025 finding could be spurious or season-specific.
- Resolution: Depends on resolution of 2024 closing-line odds gap.

**2026 live odds (real-time TSL integration)** (`MEDIUM`)
- Status: BLOCKED by no-live-call governance (live_api_calls=0)
- Impact: Cannot evaluate model on 2026 regular season games in real time. Paper-trading monitoring requires pre-game odds snapshot collection.
- Resolution: Explicit governance authorization required to begin TSL live odds collection. Suggested: explicit CEO/CTO authorization for a limited capture window.

**External odds source provenance documentation** (`MEDIUM`)
- Status: mlb_odds_2025_real.csv marked is_verified_real=False for most rows
- Impact: Cannot confirm that closing-line probabilities are authentic pre-game market odds. CSV was sourced from a single post-season scrape (all timestamps post-game). This makes edge vs closing-line a proxy measure, not true CLV.
- Resolution: Source data with pre-game timestamps and multi-snapshot trajectory. Alternatively, document the data vendor and confirm pre-game capture time.

**Approved paper-trading monitoring loop** (`LOW`)
- Status: Not approved — promotion_freeze=true
- Impact: No automated monitoring pipeline for ongoing ECE/edge tracking. Monitoring thresholds defined in P47 are advisory only.
- Resolution: Requires explicit CEO/CTO approval to implement an automated paper-only monitoring loop (no live bets, no Kelly deployment).

## Risk and Uncertainty

- **Single-year finding**: All edge and calibration results are based on 2025 data only.
- **Post-season odds proxy**: CSV closing-line odds are from a single post-season scrape.
  Edge measured against these odds is approximate, not true pregame CLV.
- **535 sample limitation**: Tier C n=535 is sufficient for bootstrap CI but not for
  fine-grained subgroup analysis or cross-year generalization claims.
- **Market adaptation risk**: If the sp_fip_delta signal becomes known, market may adapt.
  Temporal stability (P44) is reassuring for 2025 but not a forward guarantee.

## Final P47 Classification

**P47 Classification:** `P47_PLATT_SELECTED_FOR_MONITORING_DIAGNOSTIC`

## Known Limitations
- 2024 closing-line data gap **remains unresolved** — all findings are 2025-only.
- No production deployment proposed.
- No champion strategy replacement.
- No runtime recommendation logic changed.
- **Paper-only diagnostic throughout P43-P47.**
