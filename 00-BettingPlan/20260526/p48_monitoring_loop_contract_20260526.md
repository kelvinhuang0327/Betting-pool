# P48 — Paper-Only Monitoring Loop Contract for P47 Platt Baseline

**Date**: 2026-05-26  
**Classification**: `P48_MONITORING_CONTRACT_READY_DIAGNOSTIC`  
**Mode**: `paper_only=true` | `diagnostic_only=true` | `promotion_freeze=true`  
**Governance**: No live API calls. No production deployment. No champion replacement.

---

## 1. P47 Baseline Recap

| Metric | Value |
|--------|-------|
| Selected Stream | `PLATT_CALIBRATED` |
| P47 Classification | `P47_PLATT_SELECTED_FOR_MONITORING_DIAGNOSTIC` |
| P47 Commit | `17dad86` |
| ECE (Platt, CV mean) | 0.086164 |
| Brier (Platt, CV mean) | 0.238477 |
| Tier C mean_edge | 0.1059 |
| Tier C edge CI 95% | [0.0989, 0.1132] |
| 2024 Data Gap | Unresolved |

---

## 2. Monitoring Row Schema

Each monitoring row must include the following fields:

- `monitoring_date`
- `season`
- `batch_id`
- `batch_n`
- `probability_stream`
- `raw_ece`
- `platt_ece`
- `raw_brier`
- `platt_brier`
- `mean_edge`
- `edge_ci_low`
- `edge_ci_high`
- `positive_edge_rate`
- `monthly_bucket`
- `status`
- `alert_level`
- `alert_reasons`
- `governance_flags`
- `source_trace`

**Allowed `probability_stream` values:**
- `RAW_SIGMOID`
- `PLATT_CALIBRATED` ← selected by P47
- `ISOTONIC_CALIBRATED`

**Allowed `status` values:**
- `BRIER_DRIFT_CRITICAL`
- `BRIER_DRIFT_WARNING`
- `DATA_GAP_BLOCKED`
- `ECE_DRIFT_CRITICAL`
- `ECE_DRIFT_WARNING`
- `EDGE_DRIFT_CRITICAL`
- `EDGE_DRIFT_WARNING`
- `MIXED_ALERTS`
- `MONITORING_OK`
- `SAMPLE_LIMITED`

**Allowed `alert_level` values:** `NONE`, `WARNING`, `CRITICAL`, `BLOCKED`

---

## 3. Alert Rules (P47 Thresholds)

| Metric | Warning | Critical | Condition |
|--------|---------|----------|-----------|
| ECE | > 0.1 | > 0.12 | rolling ECE on new games |
| Brier | > 0.25 | > 0.27 | rolling Brier score |
| Edge mean | < 0.07 | CI crosses zero | Tier C mean edge |
| Sample | — | — | SAMPLE_LIMITED if batch_n < 100 |
| Data gap | — | — | BLOCKED if closing-line source missing |

**Priority order:**
1. DATA_GAP_BLOCKED overrides all
1. SAMPLE_LIMITED if batch_n < 100
1. CRITICAL dominates WARNING in multi-category alerts
1. MIXED_ALERTS when alerts span multiple categories
1. MONITORING_OK when no alert fires

---

## 4. Offline Fixture Cases and Expected Statuses

| Fixture ID | batch_n | Scenario | Expected Status | Expected Alert |
|------------|---------|----------|-----------------|----------------|
| fixture_01_healthy_baseline | 200 | All metrics within threshold | `MONITORING_OK` | `NONE` |
| fixture_02_sample_limited | 50 | n < 100 | `SAMPLE_LIMITED` | `WARNING` |
| fixture_03_ece_warning | 200 | platt_ece=0.1080 > 0.10 | `ECE_DRIFT_WARNING` | `WARNING` |
| fixture_04_ece_critical | 200 | platt_ece=0.1350 > 0.12 | `ECE_DRIFT_CRITICAL` | `CRITICAL` |
| fixture_05_brier_warning | 200 | platt_brier=0.2580 > 0.25 | `BRIER_DRIFT_WARNING` | `WARNING` |
| fixture_06_brier_critical | 200 | platt_brier=0.2780 > 0.27 | `BRIER_DRIFT_CRITICAL` | `CRITICAL` |
| fixture_07_edge_warning | 200 | mean_edge=0.055 < 0.07 | `EDGE_DRIFT_WARNING` | `WARNING` |
| fixture_08_edge_critical | 200 | ci_low=-0.008 ≤ 0 | `EDGE_DRIFT_CRITICAL` | `CRITICAL` |
| fixture_09_mixed_alerts | 200 | ECE critical + edge warning | `MIXED_ALERTS` | `CRITICAL` |
| fixture_10_data_gap_blocked | 200 | closing-line source missing | `DATA_GAP_BLOCKED` | `BLOCKED` |

---

## 5. Governance Flags

| Flag | Value |
|------|-------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `promotion_freeze` | `True` |
| `kelly_deploy_allowed` | `False` |
| `live_api_calls` | `0` |
| `tsl_crawler_modified` | `False` |
| `champion_strategy_changed` | `False` |
| `production_usage_proposed` | `False` |
| `runtime_recommendation_logic_changed` | `False` |

---

## 6. Limitations

- **2024 closing-line data gap**: `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl` contains no Home ML / Away ML columns. No valid 2024 odds CSV exists in the repository. P43 final classification remains `P43_BLOCKED_BY_DATA_GAP`. Cross-year edge validation is blocked until a verified 2024 MLB moneyline odds source is obtained.
- **Fixture cases are synthetic**: All 10 fixture batches use values derived from P43–P47 summaries. No live data was used.
- **ECE/Brier metrics use post-season CSV odds**: `mlb_odds_2025_real.csv` does not include pre-game timestamp snapshots. Edge metrics are vs closing line, not strict CLV.
- **No model deployed**: Platt calibration coefficients (a=0.435432, b=0.245464) are diagnostic-only. No runtime recommendation logic was changed.
- **No promotion proposed**: This contract does not authorize paper-trading escalation, Kelly deployment, or live monitoring.

---

## 7. Final P48 Classification

**`P48_MONITORING_CONTRACT_READY_DIAGNOSTIC`**

> This classification confirms that a paper-only monitoring loop contract has been specified and validated against offline fixtures. It does not authorize deployment, live monitoring, production usage, or any change to the champion strategy.

---

## CTO Summary

P48 specifies a deterministic offline monitoring contract derived from P47 Platt baseline. Ten fixture cases validate all alert paths: healthy, sample-limited, ECE/Brier/edge warning/critical, mixed, and data-gap-blocked. Governance flags are locked (paper_only=true, promotion_freeze=true, live_api_calls=0). The 2024 closing-line data gap remains unresolved. No live data was used. No runtime logic was changed. No production proposal is made.