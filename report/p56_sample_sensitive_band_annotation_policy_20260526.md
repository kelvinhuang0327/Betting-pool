# P56 — Sample-Sensitive Band Annotation Policy for Monitoring Contract V2

**Date**: 2026-05-25  
**Classification**: `P56_BAND_ANNOTATION_POLICY_READY_DIAGNOSTIC`  
**Governance**: paper_only=True, diagnostic_only=True, live_api_calls=0

---

## 1. P55 Recap

| Item | Value |
|------|-------|
| P55 classification | `P55_INCONCLUSIVE_SAMPLE_LIMITED` |
| Tier C n | 535 |
| Sep mid-band n | 27 |
| Sep mid-band platt_ece | 0.245988 |
| Sep mid-band raw_ece | 0.165456 |
| ECE delta (platt-raw) | 0.080532 |
| Anomaly source | INCONCLUSIVE_SAMPLE_LIMITED |
| Concentration | INCONCLUSIVE_SAMPLE_LIMITED |
| Sep uniquely elevated | False |

**P55 Conclusion**: Sep 1.00-1.25 band platt_ece=0.246 with n=27 is sample-limited.
Platt worsened ECE by +0.081 in this band, but n < 30 prevents reliable attribution.
No refit warranted.

---

## 2. Why a Band Annotation Policy Is Needed

P53 identified a Sep global calibration anomaly. P54 isolated it to the `sp_fip_delta` feature drift
in the 1.00-1.25 band. P55 confirmed n=27 is below the ECE reliability threshold.

Without an explicit annotation policy, future monitoring reports risk:
1. **False positives**: Treating n<30 band ECE as confirmed drift, triggering unnecessary refits.
2. **False negatives**: Ignoring band-level patterns that could accumulate into systemic drift.
3. **Threshold conflation**: Applying P52 global thresholds to small-band sub-analyses.

P56 defines a structured tiered approach to prevent these failure modes.

---

## 3. Sample Size Tiers

| Tier | Condition | Annotation | Action |
|------|-----------|------------|--------|
| BAND_SAMPLE_INSUFFICIENT | n < 30 | SAMPLE_SENSITIVE_BAND_ANOMALY | TRACK_ONLY_NO_REFIT |
| BAND_SAMPLE_WATCHLIST | 30 ≤ n < 100 | BAND_WATCHLIST | FLAG_FOR_FOLLOW_UP |
| BAND_SAMPLE_MONITORABLE | n ≥ 100 | STABLE_BAND_EVIDENCE or BAND_DRIFT_CANDIDATE | Per ECE CI |

**Sep 2025 1.00-1.25 band (n=27)**: BAND_SAMPLE_INSUFFICIENT.

---

## 4. Interpretation Rules

| Rule | Condition | Classification | Action |
|------|-----------|----------------|--------|
| R01 | n < 30 AND platt_ece is high | SAMPLE_SENSITIVE_BAND_ANOMALY | TRACK_ONLY_NO_REFIT |
| R02 | 30 <= n < 100 AND platt_ece elevated in >= 2 months | BAND_WATCHLIST | FLAG_FOR_FOLLOW_UP |
| R03 | n >= 100 AND ECE CI lower bound > 0.08 | BAND_DRIFT_CANDIDATE | PROMOTE_TO_DRIFT_CANDIDATE_IF_CI_ELEVATED |
| R04 | Any tier, single month only | SAMPLE_SENSITIVE_BAND_ANOMALY or BAND_WATCHLIST | TRACK_ONLY_NO_REFIT |
| R05 | platt_ece > raw_ece (Platt worsened ECE in band) | PLATT_BAND_DEGRADATION_NOTE | TRACK_ONLY_NO_REFIT |
| R06 | P52 global calibration stable | NOT_APPLICABLE | MAINTAIN_P52_THRESHOLDS |


---

## 5. Application to Sep 2025 1.00-1.25 Band

| Item | Value |
|------|-------|
| Band | 1.00 <= abs(sp_fip_delta) < 1.25 |
| Month | Sep 2025 |
| n | 27 |
| raw_ece | 0.165456 |
| platt_ece | 0.245988 |
| ece_delta (platt-raw) | 0.080532 |
| Outlier driven | False |
| Sep uniquely elevated | False |
| **Sample tier** | **BAND_SAMPLE_INSUFFICIENT** |
| **Annotation** | **SAMPLE_SENSITIVE_BAND_ANOMALY** |
| **Action** | **TRACK_ONLY_NO_REFIT** |

**Annotation reasoning**: n=27 < 30, so ECE estimates are unreliable. platt_ece=0.2460 and raw_ece=0.1655 are recorded but do not confirm systematic miscalibration.

### Platt Degradation Note

**Observation**: PLATT_BAND_DEGRADATION_NOTE  
ece_delta = +0.0805 (Platt worsened ECE vs raw model)  
**Action**: TRACK_ONLY_NO_REFIT  
**Meaning**: Platt transform worsened ECE in this band vs raw model by 0.0805. This is noted but does not trigger refit without n >= 30 and multi-month confirmation.

---

## 6. Future Evidence Requirements

To re-evaluate the Sep 2025 1.00-1.25 band finding, the following evidence is required:

- **FE01** (REQUIRED): Same band n >= 30 in a future month (Sep 2026 or any month)
- **FE02** (REQUIRED): Repeat elevated platt_ece in at least 2 separate months within the same band
- **FE03** (OPTIONAL): Cumulative band n >= 100 across all months with ECE CI lower bound > 0.08
- **FE04** (OPTIONAL): Platt worsening ece_delta > 0.05 confirmed at n >= 30


**Refit trigger condition**: Model refit consideration requires: FE01 AND FE02 met, AND explicit senior review, AND paper_only constraints lifted by authorized user.

**Current status**: Sep 2025 1.00-1.25 band: FE01 not yet met (n=27 < 30). FE02 not yet met (single month only). No refit warranted.

---

## 7. P52 V2 Compatibility Statement

P56 does not supersede P52.

- P56 adds an interpretive annotation layer for band-level ECE diagnostics.
- P52 global monitoring thresholds (Tier C ECE, Brier score, edge rate) remain unchanged.
- P52 edge and calibration stream ownership remains with the P52 monitoring contract.
- P56 annotations are diagnostic metadata only; they do not trigger runtime changes.
- P56 must not modify runtime recommendation logic.
- P56 must not change P45 Platt constants (A=0.435432, B=0.245464).
- P56 must not overwrite P52/P53/P54/P55 artifacts.
- P56 must not modify P52 thresholds.
- If P52 detects a global calibration critical event, P52 governs the response, not P56.
- P56 findings feed into the interpretive layer; adoption requires explicit authorization.


| Item | Status |
|------|--------|
| P52 thresholds | UNCHANGED |
| P52 artifact | PRESERVED |
| P53 artifact | PRESERVED |
| P54 artifact | PRESERVED |
| P55 artifact | PRESERVED |
| Platt constants | UNCHANGED — A=0.435432, B=0.245464 (P45 locked) |

---

## 8. Limitations

1. P56 policy is based on 2025 Tier C data only (n=535); cross-year validation is not yet possible.
2. The n<30 / n<100 thresholds are heuristic; formal statistical power analysis has not been performed.
3. ECE is computed with 10-bin uniform-width; other binning schemes may yield different tier boundaries.
4. The Platt degradation observation (ece_delta=+0.081) may or may not represent a systematic pattern.
5. P56 is a metadata annotation layer only; runtime logic and monitoring thresholds are unchanged.

---

## 9. 2024 Closing-Line Data Gap

**The 2024 closing-line data gap (P43_BLOCKED_BY_DATA_GAP) remains unresolved.**

This analysis is based exclusively on 2025 Tier C data. Cross-year band-level analysis
cannot be completed until 2024 historical odds data is obtained. P56 policy applicability
to pre-2025 seasons is unknown.

---

## 10. Final P56 Classification

```
P56_BAND_ANNOTATION_POLICY_READY_DIAGNOSTIC
```

---

## 11. Next Recommended Diagnostic Task

**P57 — Monitoring Contract V2 Annotation Integration**:
- Integrate P56 band annotation policy into the P52 monitoring contract as an interpretive metadata layer.
- Define how future monitoring reports should reference `sample_tier` and `annotation` fields.
- Verify that P52 global thresholds remain unchanged after annotation layer addition.
- Required input: P56 policy JSON + P52 V2 contract JSON.

Prerequisite before P57: 2024 closing-line data remains unavailable.
Until then, P56 annotations apply to 2025 Tier C data only.

---

*Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True, live_api_calls=0*  
*P45 Platt constants unchanged: A=0.435432, B=0.245464*  
*P52/P53/P54/P55 artifacts not overwritten. P52 thresholds not changed.*
