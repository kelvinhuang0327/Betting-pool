# P58 — Monitoring Contract V2 Monthly Report Template

**Date**: 2026-05-25  
**Classification**: `P58_MONTHLY_REPORT_TEMPLATE_READY_DIAGNOSTIC`  
**Template Version**: `P58_MONITORING_CONTRACT_V2_MONTHLY_REPORT_TEMPLATE_V1`  
**Governance**: paper_only=True, diagnostic_only=True, live_api_calls=0

---

## 1. P57 Recap

P57 completed at commit `616448e` with classification `P57_ANNOTATION_INTEGRATION_READY_DIAGNOSTIC`.

Key P57 outputs incorporated here:
- **BandAnnotationRecord schema v1**: 17 fields, 5 invariants, 6 SEP separation rules.
- **Sep 2025 1.00–1.25 band carry-forward**: n=27, BAND_SAMPLE_INSUFFICIENT, TRACK_ONLY_NO_REFIT.
- **P57 key principle**: Global monitoring status is controlled exclusively by P52 V2 thresholds.  
  Band annotations are metadata-only and must not override global status, trigger refit, or change thresholds.

---

## 2. Why Monthly Report Template Is Needed

Without a standard template:
1. Future agents have no schema defining how global status and band annotations coexist in a single report.
2. Reviewers may incorrectly conflate band-level findings (TRACK_ONLY, n=27) with P52 global alerts.
3. The Sep 2025 mid-band carry-forward has no mechanism to persist across reporting cycles.
4. There is no validation layer preventing an agent from incorrectly setting should_trigger_refit=true.

P58 provides a **reusable template** with schema, validation rules, and a concrete Sep 2025 example.

---

## 3. Monthly JSON Schema

Schema: **MonitoringContractV2MonthlyReport** (v1.0)

Schema for a Monitoring Contract V2 monthly report. Separates global P52 status (threshold-driven) from band-level annotations (P57 BandAnnotationRecord, metadata only). Does not modify runtime logic or thresholds.

**Required top-level fields**:
- `report_type`
- `template_version`
- `report_month`
- `generated_date`
- `global_status`
- `band_annotations`
- `data_gap_status`
- `governance_summary`
- `report_limitations`
- `next_review_date`

**Section order**:
1. GLOBAL STATUS — P52 V2 threshold evaluation
2. BAND ANNOTATIONS — Active carry-forward BandAnnotationRecord list
3. DATA GAP STATUS — 2024 closing-line gap and cross-year analysis status
4. GOVERNANCE SUMMARY — paper_only, promotion_freeze, live_api_calls
5. LIMITATIONS — sample sizes, data gaps, schema caveats

---

## 4. Global Status Section Schema

Global monitoring status driven exclusively by P52 V2 thresholds. Must never be modified by band-level annotations.

| Field | Type | Description |
|-------|------|-------------|
| `report_month` | string | Month covered by this report, e.g. '2025-09'. |
| `batch_n` | integer | Number of games in the Tier C batch for this month. |
| `global_status` | string | Overall monitoring status. Controlled only by P52 V2 thresholds. Must no |
| `global_alert_level` | string | Traffic-light alert level based on P52 thresholds. |
| `global_alert_reasons` | list[string] | List of reasons the current alert level was assigned. |
| `edge_status` | string | Edge rate status against P52 V2 thresholds. |
| `calibration_status` | string | Calibration (ECE) status against P52 V2 thresholds. |
| `sample_status` | string | Sample size status for the monthly Tier C batch. Shown separately from c |
| `data_gap_status` | string | 2024 closing-line data gap. Must be shown as a cross-year limitation, no |
| `raw_edge_mean` | float | Mean raw edge across Tier C games for this month. |
| `raw_edge_ci_low` | float | Lower bound of 95% CI on raw edge mean. |
| `raw_edge_ci_high` | float | Upper bound of 95% CI on raw edge mean. |
| `platt_ece` | float | Platt-calibrated ECE for all Tier C games this month. |
| `platt_brier` | float | Platt-calibrated Brier score for Tier C games this month. |
| `p52_thresholds_used` | object | Snapshot of the P52 V2 thresholds applied in this report. |
| `source_trace` | object | Traceability to source JSON artifacts used to populate this section. |


**Rules**:
- global_status is controlled only by P52 V2 thresholds.
- global_status must not be modified by band annotations.
- sample_status must be displayed separately from calibration_status and edge_status.
- data_gap_status must describe the 2024 cross-year limitation, not a 2025-only blocker.
- p52_thresholds_used must reflect locked P52 V2 thresholds; not changed by P57 or P58.
- platt_ece and platt_brier reflect Platt-calibrated values using locked P45 constants.

---

## 5. Band Annotations Section Schema

Band-level diagnostic annotations using P57 BandAnnotationRecord schema. These records are metadata only. They do not affect global_status, trigger refit, or change P52 thresholds.

**Record schema**: BandAnnotationRecord v1 (see P57)

**Required fields per record**:
- `annotation_scope`
- `metric_family`
- `band_label`
- `band_n`
- `sample_tier`
- `annotation`
- `action`
- `evidence_strength`
- `platt_ece`
- `raw_ece`
- `ece_delta`
- `repeated_month_count`
- `cumulative_band_n`
- `future_evidence_required`
- `should_change_global_status`
- `should_trigger_refit`
- `should_change_thresholds`
- `carry_forward_status`
- `source_trace`

**Sample tier mapping**:
| n range | sample_tier |
|---------|-------------|
| n < 30 | `BAND_SAMPLE_INSUFFICIENT` |
| 30 ≤ n < 100 | `BAND_SAMPLE_WATCHLIST` |
| n ≥ 100 | `BAND_SAMPLE_MONITORABLE` |

**Section rules**:
- Band annotations are metadata-only; they do not replace or override global_status.
- n < 30 must map to sample_tier=BAND_SAMPLE_INSUFFICIENT.
- TRACK_ONLY_NO_REFIT must remain the action for BAND_SAMPLE_INSUFFICIENT records.
- should_change_global_status must be false for all band annotations.
- should_trigger_refit must be false for all BAND_SAMPLE_INSUFFICIENT records.
- should_change_thresholds must be false for all band annotations.
- Each record must include source_trace with p55_reference and p56_reference.
- Section header must explicitly state: 'Band annotations do not change global P52 status.'
- Section must state whether any record has should_trigger_refit=true (expected: none).
- Section must state the current count of active TRACK_ONLY records.

---

## 6. Sep 2025 Example Monthly Report

**Example type**: `HISTORICAL_DIAGNOSTIC_EXAMPLE`  
**Report month**: `2025-09`

> This is a diagnostic example only and does not modify runtime behavior. Values are sourced from P55/P56/P57 artifacts. A real monthly report would populate raw_edge_mean, platt_ece, platt_brier from the actual batch data for that month.

### 6a. Global Status (Sep 2025)

| Field | Value |
|-------|-------|
| report_month | 2025-09 |
| batch_n | 535 (535 is the full 2025 Tier C count. Sep-s...) |
| global_status | `MONITORING_ACTIVE_DIAGNOSTIC` |
| global_alert_level | **GREEN** |
| edge_status | EDGE_WITHIN_THRESHOLD |
| calibration_status | CALIBRATION_WITHIN_THRESHOLD |
| sample_status | SAMPLE_ADEQUATE |
| data_gap_status | 2024 closing-line data gap (P43_BLOCKED_BY_DATA_GAP) remains... |

### 6b. Band Annotations (Sep 2025)

> **Band annotations do not change global P52 status.**  
> Active TRACK_ONLY records: 1

| Field | Value |
|-------|-------|
| annotation_scope | BAND_LEVEL |
| metric_family | CALIBRATION |
| band_label | `1.00 <= |sp_fip_delta| < 1.25` |
| band_n | **27** |
| sample_tier | **BAND_SAMPLE_INSUFFICIENT** |
| annotation | **SAMPLE_SENSITIVE_BAND_ANOMALY** |
| action | **TRACK_ONLY_NO_REFIT** |
| evidence_strength | INSUFFICIENT |
| platt_ece | 0.245988 |
| raw_ece | 0.165456 |
| ece_delta | 0.080532 |
| repeated_month_count | 1 |
| cumulative_band_n | 27 |
| future_evidence_required | True |
| should_change_global_status | **False** |
| should_trigger_refit | **False** |
| should_change_thresholds | **False** |
| carry_forward_status | ACTIVE_TRACK_ONLY |

---

## 7. Validation Rules

| Rule ID | Rule |
|---------|------|
| VAL01 | global_status must not be MONITORING_ALERT_DIAGNOSTIC unless a P52 V2 threshold  |
| VAL02 | No band annotation may set should_change_global_status=true. |
| VAL03 | No band annotation with n < 30 may set should_trigger_refit=true. |
| VAL04 | No band annotation may set should_change_thresholds=true. |
| VAL05 | ACTIVE_TRACK_ONLY records from prior months must appear in the current report un |
| VAL06 | band_annotations section header must explicitly state 'Band annotations do not c |
| VAL07 | p52_thresholds_used must match the locked P52 V2 thresholds; not changed by any  |
| VAL08 | data_gap_status must describe the 2024 cross-year limitation (not a 2025-only bl |
| VAL09 | sample_status must be a separate field from calibration_status and edge_status. |
| VAL10 | governance_summary must include paper_only=true, live_api_calls=0, promotion_fre |


---

## 8. Invariants

- Band annotations are additive metadata; they never replace or override global_status.
- n < 30 → sample_tier=BAND_SAMPLE_INSUFFICIENT; should_trigger_refit=False; should_change_thresholds=False.
- P52 thresholds are never changed by a band annotation (should_change_thresholds must always be False).
- An ACTIVE_TRACK_ONLY record carries forward to every subsequent monthly report until archived.
- data_gap_status must always reflect the 2024 cross-year limitation.
- Governance flags (paper_only, live_api_calls=0, promotion_freeze) must be present in every report.
- platt_ece and platt_brier are computed using locked P45 Platt constants (A=0.435432, B=0.245464).
- The Sep 2025 1.00-1.25 band annotation (n=27) must remain TRACK_ONLY_NO_REFIT until FE01+FE02 are met.

---

## 9. Future Agent Usage Notes

1. **Load the P58 template (this JSON) and the current P52 V2 artifact.**  
   _Do not modify P52/P55/P56/P57 artifacts._
2. **Populate global_status from the current month's Tier C batch data.**  
   _Compute global_status using P52 V2 thresholds only. Do not let band annotations influence this field._
3. **Carry forward all ACTIVE_TRACK_ONLY BandAnnotationRecords from the previous report.**  
   _Update repeated_month_count and cumulative_band_n for each record._
4. **Add new BandAnnotationRecords if new band anomalies are detected this month.**  
   _Apply P56 sample tier policy to assign sample_tier, annotation, and action._
5. **Run VAL01-VAL10 validation rules on the generated report JSON.**  
   _A report that fails any VAL rule must not be committed as a final artifact._
6. **Generate the Markdown report from the JSON (GLOBAL STATUS + BAND ANNOTATIONS sections).**  
   _The Markdown must explicitly separate the two sections and label band annotations as metadata._
7. **Confirm governance flags in the generated report match required values.**  
   _paper_only=True, live_api_calls=0, promotion_freeze=True, kelly_deploy_allowed=False._


**Forbidden agent actions**:
- Setting should_change_global_status=true in any band annotation.
- Setting should_trigger_refit=true for a record with n < 30.
- Setting should_change_thresholds=true in any band annotation.
- Modifying P52 V2 thresholds based on band-level evidence alone.
- Triggering Platt refit from monthly report without explicit authorization.
- Removing the 2024 data gap note from data_gap_status.
- Staging P52/P53/P54/P55/P56/P57 artifact files.
- Setting live_api_calls above zero.
- Enabling kelly_deploy_allowed (must remain False at all times).

**Graduation reminder**: A BAND_SAMPLE_INSUFFICIENT record (n < 30) graduates to FLAG_FOR_FOLLOW_UP when n >= 30 in a subsequent month AND repeated_month_count >= 2. See P57 for full graduation and archival criteria.

---

## 10. Limitations

1. The Sep 2025 example uses total 2025 Tier C n=535 for global status; a real monthly report uses only that month's batch.
2. raw_edge_mean, platt_ece, platt_brier are not populated in the example (2025 monthly batch data not segmented by month in current artifacts).
3. BandAnnotationRecord schema v1 is a first iteration; field definitions may be refined.
4. Graduation thresholds (n≥30, n≥100) are heuristic and have not been validated by formal power analysis.
5. P58 is metadata / schema only; runtime logic and monitoring thresholds are unchanged.

---

## 11. 2024 Closing-Line Data Gap

**The 2024 closing-line data gap (P43_BLOCKED_BY_DATA_GAP) remains unresolved.**

Cross-year band analysis cannot be completed until 2024 historical odds data is obtained.
This is a cross-year limitation and does not block 2025-only analysis.

---

## 12. Final P58 Classification

```
P58_MONTHLY_REPORT_TEMPLATE_READY_DIAGNOSTIC
```

---

## 13. Next Recommended Diagnostic Task

**P59 — Monitoring Contract V2 First Monthly Report (Oct 2025 or rolling)**:
- Use P58 template to generate the first real monthly report for the next available month.
- Populate global_status from actual Tier C batch data for that month.
- Carry forward the Sep 2025 mid-band ACTIVE_TRACK_ONLY record.
- Run VAL01-VAL10 validation rules.
- Check whether FE01 (n >= 30 in the 1.00-1.25 band) is met for the new month.
- Prerequisite: 2024 closing-line data gap remains unresolved; report scope is 2025 only.

---

*Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True, live_api_calls=0*  
*P45 Platt constants unchanged: A=0.435432, B=0.245464*  
*P52/P53/P54/P55/P56/P57 artifacts not overwritten. P52 thresholds not changed.*
