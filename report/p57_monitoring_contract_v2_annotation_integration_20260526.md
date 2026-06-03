# P57 — Monitoring Contract V2 Annotation Integration

**Date**: 2026-05-25  
**Classification**: `P57_ANNOTATION_INTEGRATION_READY_DIAGNOSTIC`  
**Governance**: paper_only=True, diagnostic_only=True, live_api_calls=0

---

## 1. P56 Recap

| Item | Value |
|------|-------|
| P56 classification | `P56_BAND_ANNOTATION_POLICY_READY_DIAGNOSTIC` |
| Policy name | Sample-Sensitive Band Annotation Policy v1 |
| Policy version | 1.0 |
| Tiers defined | BAND_SAMPLE_INSUFFICIENT, BAND_SAMPLE_WATCHLIST, BAND_SAMPLE_MONITORABLE |
| Sep 2025 mid-band n | 27 |
| Sep 2025 sample_tier | BAND_SAMPLE_INSUFFICIENT |
| Sep 2025 annotation | SAMPLE_SENSITIVE_BAND_ANOMALY |
| Sep 2025 action | TRACK_ONLY_NO_REFIT |
| Sep 2025 platt_ece | 0.245988 |
| Sep 2025 ece_delta | 0.080532 |

---

## 2. Why Annotation Integration Is Needed

P53 identified a Sep 2025 global calibration anomaly. P54 isolated it to the
`sp_fip_delta` feature drift in the `1.00-1.25` band. P55 confirmed that n=27
is below the ECE reliability threshold. P56 defined a sample-sensitive band
annotation policy with three tiers (INSUFFICIENT / WATCHLIST / MONITORABLE).

Without integration into the Monitoring Contract V2 reporting layer:
1. Future reports lack a standard way to present band-level findings alongside global status.
2. Reviewers may incorrectly interpret band anomalies as global P52 alerts.
3. The Sep 2025 mid-band TRACK_ONLY finding has no formal carry-forward mechanism.
4. There is no schema defining which fields distinguish band annotations from global status.

P57 solves all four problems by adding a `BandAnnotationRecord` schema as metadata
to the P52 V2 reporting layer — without changing any P52 thresholds or runtime logic.

---

## 3. Annotation Metadata Schema

Schema: **BandAnnotationRecord v1** (v1.0)

Schema for attaching band-level diagnostic annotations to monitoring reports. These records are metadata only and do not affect P52 global monitoring status or runtime recommendation logic.

| Field | Type | Description |
|-------|------|-------------|
| `annotation_scope` | string | Scope of the annotation; BAND_LEVEL for sp_fip_delta sub-bands. |
| `metric_family` | string | Metric domain this annotation belongs to. |
| `band_label` | string | Human-readable band definition, e.g. '1.00 <= |sp_fip_delta| < 1.25'. |
| `band_n` | integer | Number of games in this band for the reporting period. |
| `sample_tier` | string | Sample size tier per P56 policy. |
| `annotation` | string | Annotation label for the band finding. |
| `action` | string | Prescribed action from P56 policy. |
| `evidence_strength` | string | Evidence strength level for this annotation. |
| `platt_ece` | float | Platt-calibrated ECE for this band in the reporting period. |
| `raw_ece` | float | Raw (uncalibrated) model ECE for this band. |
| `ece_delta` | float | platt_ece minus raw_ece. Positive = Platt worsened ECE in this band. |
| `repeated_month_count` | integer | Number of separate months this band has shown elevated ECE. |
| `cumulative_band_n` | integer | Total games in this band across all monitored months. |
| `future_evidence_required` | boolean | Whether future evidence is required before any action escalation. |
| `should_change_global_status` | boolean | Whether this annotation should change P52 global monitoring status. |
| `should_trigger_refit` | boolean | Whether this annotation should trigger a model refit. |
| `should_change_thresholds` | boolean | Whether this annotation should change P52 global thresholds. |


**Invariants**:
- should_change_global_status MUST be false when sample_tier=BAND_SAMPLE_INSUFFICIENT.
- should_trigger_refit MUST be false when n < 30.
- should_change_thresholds MUST be false for all band-level annotations.
- Band annotations are additive metadata only; they do not replace P52 status fields.
- Records must preserve trace to source phase (e.g., p55_reference, p56_reference).

---

## 4. Global vs Band Status Separation

**Principle**: P52 global monitoring status is governed by P52 V2 thresholds. Band-level annotations (P56, P57) are diagnostic metadata only. They coexist in monitoring reports without overriding global status.

| Rule | Rule Statement | Implication |
|------|---------------|-------------|
| SEP01 | Global monitoring status is controlled exclusively by P52 V2 threshold | A band anomaly cannot change global status unless P52 thresholds are t |
| SEP02 | Band annotation does not override global status unless future evidence | P55 Sep mid-band finding (n=27, SAMPLE_SENSITIVE_BAND_ANOMALY) leaves  |
| SEP03 | Band annotations appear in reports as warning metadata sections, clear | Reports must distinguish 'GLOBAL STATUS' from 'BAND ANNOTATIONS' secti |
| SEP04 | n < 30 cannot trigger model refit. | Sep 2025 1.00-1.25 band (n=27) → no refit, regardless of ECE value. |
| SEP05 | n < 30 cannot change P52 thresholds. | Even if platt_ece=0.246 in the Sep mid-band, P52 global ECE thresholds |
| SEP06 | Band-level annotation records must preserve trace to P55/P56 source ev | Each BandAnnotationRecord in a monitoring report must include p55_refe |


**Current global status**: `P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC`  
**Band annotations affect global status**: False

---

## 5. Sep 2025 Mid-Band Carry-Forward Example

This is the first active `BandAnnotationRecord` in the Monitoring Contract V2 annotation layer.

| Field | Value |
|-------|-------|
| annotation_scope | BAND_LEVEL |
| metric_family | CALIBRATION |
| band_label | 1.00 <= |sp_fip_delta| < 1.25 |
| band_n | 27 |
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
| platt_degradation_note | PLATT_BAND_DEGRADATION_NOTE |
| carry_forward_status | ACTIVE_TRACK_ONLY |

**Carry-forward reason**: n=27 < 30 (BAND_SAMPLE_INSUFFICIENT). Evidence is insufficient for any action escalation. This record is carried forward into future monitoring reports as TRACK_ONLY metadata until future evidence criteria are met.

---

## 6. Future Evidence Requirements

- **FE01** (REQUIRED): Same band (1.00 <= |sp_fip_delta| < 1.25) achieves n >= 30 in a future month.  
  *Current status: NOT_MET — n=27 in Sep 2025 only.*
- **FE02** (REQUIRED): Repeated elevated platt_ece in at least 2 separate months within the same band.  
  *Current status: NOT_MET — single month observation only.*
- **FE03** (OPTIONAL): Cumulative band n >= 100 across all months, with ECE CI lower bound > 0.08.  
  *Current status: NOT_MET — cumulative_band_n=27.*
- **FE04** (OPTIONAL): Platt worsening ece_delta > 0.05 confirmed at n >= 30.  
  *Current status: NOT_MET — n < 30 prevents reliable ece_delta attribution.*


**Refit trigger condition**: See P56 criteria

---

## 7. Future Monitoring Report Requirements

Required report sections:
1. GLOBAL STATUS — P52 V2 threshold evaluation (ECE, Brier, edge rate)
2. BAND ANNOTATIONS — Active carry-forward BandAnnotationRecord list
3. DATA GAP STATUS — 2024 closing-line gap and cross-year analysis status
4. GOVERNANCE SUMMARY — paper_only, promotion_freeze, live_api_calls

Band annotation section rules:
- Each BandAnnotationRecord must show sample_tier, annotation, action, n, platt_ece.
- Records with sample_tier=BAND_SAMPLE_INSUFFICIENT must be clearly labelled as TRACK_ONLY.
- Records must show evidence progress toward future_evidence_required criteria.
- The section must explicitly state: 'Band annotations do not change global P52 status.'
- The section must state whether should_trigger_refit and should_change_thresholds are false.

**Graduation criteria**: A BandAnnotationRecord graduates from TRACK_ONLY to FLAG_FOR_FOLLOW_UP when: band n >= 30 in a subsequent month AND repeated_month_count >= 2. A record graduates to PROMOTE_TO_DRIFT_CANDIDATE_IF_CI_ELEVATED when: cumulative_band_n >= 100 AND ECE CI lower bound > 0.08.

**Archival criteria**: A BandAnnotationRecord is archived (removed from active list) when: 6 consecutive months pass without band n >= 10, OR when an explicit senior review concludes no systematic pattern exists.

---

## 8. P52 V2 Compatibility Statement

P57 does not supersede P52 and does not change P52 thresholds.

- P57 adds a BandAnnotationRecord schema to the P52 V2 reporting metadata layer.
- P52 global monitoring thresholds (Tier C ECE, Brier score, edge rate) remain unchanged.
- P52 global status remains P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC.
- P57 annotation integration is additive; it does not replace any P52 field.
- P57 must not modify runtime recommendation logic.
- P57 must not change P45 Platt constants (A=0.435432, B=0.245464).
- P57 must not overwrite P52/P53/P54/P55/P56 artifacts.
- P57 must not change P52 thresholds.
- The Sep 2025 mid-band annotation (SAMPLE_SENSITIVE_BAND_ANOMALY, TRACK_ONLY_NO_REFIT) does not affect P52 global monitoring status.
- Future monitoring reports using P57 schema must explicitly state 'Band annotations do not change global P52 status.'


| Item | Status |
|------|--------|
| P52 thresholds | UNCHANGED |
| P52 artifact | PRESERVED |
| P53 artifact | PRESERVED |
| P54 artifact | PRESERVED |
| P55 artifact | PRESERVED |
| P56 artifact | PRESERVED |
| Platt constants | UNCHANGED — A=0.435432, B=0.245464 (P45 locked) |
| Global monitoring status | `P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC` |

---

## 9. Limitations

1. P57 annotation schema is based on 2025 Tier C data only (n=535). Cross-year validation is not yet possible.
2. The `BandAnnotationRecord` schema v1 is a first iteration; field definitions may be refined as evidence accumulates.
3. ECE is computed with 10-bin uniform-width; other binning schemes may yield different band boundaries.
4. Graduation criteria thresholds (n>=30, n>=100, CI>0.08) are heuristic and have not been validated by formal power analysis.
5. P57 is metadata only; runtime logic and monitoring thresholds are unchanged.

---

## 10. 2024 Closing-Line Data Gap

**The 2024 closing-line data gap (P43_BLOCKED_BY_DATA_GAP) remains unresolved.**

P57 annotation integration applies to 2025 Tier C data only. Cross-year band-level
analysis cannot be completed until 2024 historical odds data is obtained.

---

## 11. Final P57 Classification

```
P57_ANNOTATION_INTEGRATION_READY_DIAGNOSTIC
```

---

## 12. Next Recommended Diagnostic Task

**P58 — Monitoring Contract V2 Monthly Report Template**:
- Create a monthly report template that implements the P57 BandAnnotationRecord schema.
- Include GLOBAL STATUS and BAND ANNOTATIONS sections per P57 requirements.
- Populate the Sep 2025 mid-band carry-forward record as a live example.
- Validate that the template enforces all P57 separation rules and invariants.
- Prerequisite: 2024 closing-line data remains unavailable; report scope is 2025 only.

---

*Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True, live_api_calls=0*  
*P45 Platt constants unchanged: A=0.435432, B=0.245464*  
*P52/P53/P54/P55/P56 artifacts not overwritten. P52 thresholds not changed.*
