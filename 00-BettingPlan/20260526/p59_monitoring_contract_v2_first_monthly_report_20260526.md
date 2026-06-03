# P59 — Monitoring Contract V2 First Monthly Report

**Report Month**: 2025-09
**Report Type**: HISTORICAL_DIAGNOSTIC_FIRST_REPORT
**Run Date**: 2026-05-25
**Template Source**: P58_MONITORING_CONTRACT_V2_MONTHLY_REPORT_TEMPLATE_V1
**Report Version**: P59_MONITORING_CONTRACT_V2_FIRST_MONTHLY_REPORT_V1

---

## 1. Global Status (P52 V2 Threshold-Driven)

| Field | Value |
|---|---|
| report_month | `2025-09` |
| batch_n | **98** |
| global_status | **MONITORING_ALERT_DIAGNOSTIC** |
| global_alert_level | **RED** |
| edge_status | EDGE_WITHIN_THRESHOLD |
| calibration_status | **CALIBRATION_ALERT** |
| sample_status | **SAMPLE_INSUFFICIENT** |
| raw_edge_mean | 0.108441 |
| raw_edge_ci_low | 0.092154 |
| raw_edge_ci_high | 0.124587 |
| platt_ece | 0.122929 |
| platt_brier | 0.235731 |

**Alert Reasons:**

- platt_ece=0.122929 exceeds ece_critical_threshold=0.12 (P52 V2)
- SAMPLE_LIMITED: batch_n=98 < 100 (P52 V2 dominance_rule: SAMPLE_LIMITED does not suppress CALIBRATION_CRITICAL)

> ⚠ Global status is controlled exclusively by P52 V2 thresholds.
> Band-level annotations (Section 2) are metadata only and have no influence on global status.

---

## 2. Band Annotations (Metadata Only)

> **Band annotations do not change global P52 status.**

Active TRACK_ONLY records: **1**

### Sep 2025 Mid-Band Carry-Forward Record

| Field | Value |
|---|---|
| band_label | `1.00 <= |sp_fip_delta| < 1.25` |
| band_n | **27** |
| sample_tier | **BAND_SAMPLE_INSUFFICIENT** |
| annotation | **SAMPLE_SENSITIVE_BAND_ANOMALY** |
| action | **TRACK_ONLY_NO_REFIT** |
| evidence_strength | INSUFFICIENT |
| platt_ece | 0.245988 |
| raw_ece | 0.165456 |
| ece_delta | 0.080532 |
| repeated_month_count | **2** |
| cumulative_band_n | 27 |
| should_change_global_status | False |
| should_trigger_refit | False |
| should_change_thresholds | False |
| carry_forward_status | **ACTIVE_TRACK_ONLY** |

_Carried forward from P57 (first observation Sep 2025). P59 is the second tracking entry (repeated_month_count=2). No new qualifying band data in this report period. FE01 not yet met (n=27 < 30). FE02 not yet met (single source month)._

---

## 3. Validation Results (VAL01–VAL10)

| Rule | Status | Evidence |
|---|---|---|
| VAL01 | ✓ PASS | global_status='MONITORING_ALERT_DIAGNOSTIC', alert_reasons_count=2 |
| VAL02 | ✓ PASS | should_change_global_status=True violations: 0 |
| VAL03 | ✓ PASS | should_trigger_refit=True violations for n<30: 0 |
| VAL04 | ✓ PASS | should_change_thresholds=True violations: 0 |
| VAL05 | ✓ PASS | ACTIVE_TRACK_ONLY records for Sep mid-band: 1 |
| VAL06 | ✓ PASS | section_header='Band annotations do not change global P52 status.' |
| VAL07 | ✓ PASS | p52_thresholds source='data/mlb_2025/derived/p52_monitoring_contract_v2_ |
| VAL08 | ✓ PASS | data_gap_status='2024 closing-line data gap (P43_BLOCKED_BY_DATA_GAP) re |
| VAL09 | ✓ PASS | sample_status='SAMPLE_INSUFFICIENT', calibration_status='CALIBRATION_ALE |
| VAL10 | ✓ PASS | paper_only=True, live_api_calls=0, promotion_freeze=True, kelly_deploy_a |

**10/10 rules passed.**

---

## 4. Data Gap Status

- **2024 Closing-Line Gap**: UNRESOLVED
- **Impact**: Cross-year band analysis is not possible until 2024 historical odds data is obtained. The Sep 2025 mid-band finding applies to 2025 data only.

---

## 5. Governance Summary

| Flag | Value |
|---|---|
| paper_only | True |
| live_api_calls | 0 |
| promotion_freeze | True |
| kelly_deploy_allowed | False |
| platt_constants | `A=0.435432, B=0.245464 (P45, locked)` |
| p52_thresholds_changed | False |

---

## 6. Limitations

- Tier C batch_n=98 < 100: all metrics are subject to elevated estimation variance.
- Sep 2025 mid-band annotation (n=27) is BAND_SAMPLE_INSUFFICIENT. No refit or threshold change warranted.
- 2024 closing-line data gap prevents cross-year market-edge validation.
- This is a single-month diagnostic report. Longitudinal trend analysis requires multiple future monthly reports.
- platt_ece=0.122929 exceeds the P52 V2 ece_critical_threshold=0.12. This is a CALIBRATION_CRITICAL signal for the Sep 2025 Tier C batch. It is a monitoring observation only; no refit is authorized.

---

## Final Classification

**`P59_FIRST_MONTHLY_REPORT_SAMPLE_LIMITED`**

> This report is diagnostic only.  No production deployment, no refit, no threshold changes.
> All findings are paper research observations under paper_only=True, promotion_freeze=True.
