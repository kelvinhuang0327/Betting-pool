# P55 — Sep 2025 Mid-Band Calibration Anomaly Audit

**Date**: 2026-05-25  
**Classification**: `P55_INCONCLUSIVE_SAMPLE_LIMITED`  
**Governance**: paper_only=True, diagnostic_only=True, live_api_calls=0

---

## 1. P54 Recap

| Item | Value |
|------|-------|
| P54 classification | `P54_NO_FEATURE_DRIFT_FOUND_DIAGNOSTIC` |
| Tier C n | 535 |
| Sep n | 98 |
| Sep platt_ece (overall) | 0.122929 |
| Sep 1.00-1.25 band platt_ece (P54) | 0.245988 |
| Sep 1.00-1.25 band n (P54) | 27 |
| P53 classification | `SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC` |

**P55 Goal**: Investigate whether the Sep 1.00-1.25 band platt_ece=0.246 (n=27) anomaly is
outlier-driven, broad-based, or caused by Platt transformation issues.

---

## 2. Sep Mid-Band Dataset Verification

- **Tier C n**: 535 (consistent with P54: True)
- **Sep mid-band n**: 27 (consistent with P54: True)
- **Band definition**: 1.00 ≤ |sp_fip_delta| < 1.25

All 27 Sep games in the 1.00-1.25 band are included in per-game analysis.

---

## 3. Outlier Concentration Audit

| Metric | Value |
|--------|-------|
| n | 27 |
| platt_ece | 0.2460 |
| raw_ece | 0.1655 |
| platt_brier | 0.2315 |
| raw_brier | 0.2139 |
| mean_platt_prob | 0.5754 |
| actual_win_rate | 0.5556 |
| calibration_gap | 0.0199 |
| top1 contribution share | 0.0460 |
| top3 contribution share | 0.1350 |
| top5 contribution share | 0.2230 |
| LOO ECE min | 0.2328 |
| LOO ECE max | 0.2731 |
| LOO ECE swing | 0.0403 |
| LOO ECE std | 0.0159 |
| **Concentration** | **INCONCLUSIVE_SAMPLE_LIMITED** |

### Top 5 Games by Absolute Platt Error

| Date | Home | Away | sp_fip_delta | platt_prob | Outcome | abs_error |
|------|------|------|-------------|-----------|---------|-----------|
| 2025-09-01 | San Diego Padres | Baltimore Orioles | 1.1000 | 0.5890 | 0 | 0.5890 |
| 2025-09-25 | Athletics | Houston Astros | -1.2000 | 0.5713 | 0 | 0.5713 |
| 2025-09-12 | Boston Red Sox | New York Yankees | -1.0500 | 0.5699 | 0 | 0.5699 |
| 2025-09-24 | San Diego Padres | Milwaukee Brewers | 1.1000 | 0.5667 | 0 | 0.5667 |
| 2025-09-24 | Arizona Diamondbacks | Los Angeles Dodgers | -1.2000 | 0.5608 | 0 | 0.5608 |

---

## 4. Month / Band Comparison (1.00-1.25 band)

| Month | n | raw_ece | platt_ece | raw_brier | platt_brier | actual_wr | mean_platt_prob |
|-------|---|---------|-----------|-----------|-------------|-----------|----------------|
| Apr | 6 | 0.2702 | 0.1050 | 0.1913 | 0.2091 | 0.6667 | 0.6005 |
| May | 29 | 0.1149 | 0.0373 | 0.2418 | 0.2355 | 0.6207 | 0.5834 |
| Jun | 22 | 0.1732 | 0.1789 | 0.2491 | 0.2333 | 0.6364 | 0.5631 |
| Jul | 21 | 0.2162 | 0.2490 | 0.2635 | 0.2808 | 0.3333 | 0.5824 |
| Aug | 26 | 0.1631 | 0.1261 | 0.2570 | 0.2630 | 0.4615 | 0.5877 |
| Sep | 27 | 0.1655 | 0.2460 | 0.2139 | 0.2315 | 0.5556 | 0.5754 |


- **Sep rank by platt_ece**: 2 / 6 months with data
- **Avg non-Sep platt_ece**: 0.1393
- **Sep vs avg non-Sep**: 0.1067
- **Sep uniquely elevated**: False

---

## 5. Platt vs Raw Transformation Check

| Metric | Raw | Platt | Market |
|--------|-----|-------|--------|
| ECE | 0.1655 | 0.2460 | 0.2220 |
| Brier | 0.2139 | 0.2315 | 0.1953 |
| calibration_gap | 0.0221 | 0.0199 | 0.0242 |
| ECE delta (platt-raw) | 0.0805 | | |
| Platt improved ECE | False | | |

**Anomaly source**: `INCONCLUSIVE_SAMPLE_LIMITED`  
**Reasoning**: n=27 is below 30, making ECE estimates unreliable regardless of pattern.

---

## 6. Root-Cause Conclusion

The Sep 1.00-1.25 mid-band platt_ece=0.246 (n=27) is classified as:

**`P55_INCONCLUSIVE_SAMPLE_LIMITED`**

Key factors:
- Concentration: INCONCLUSIVE_SAMPLE_LIMITED (top3 share=0.1350, LOO swing=0.0403)
- Platt vs raw: anomaly source = INCONCLUSIVE_SAMPLE_LIMITED
- Sep rank among months: 2 (Sep uniquely elevated: False)
- With n=27, ECE estimates carry high variance; the anomaly cannot be reliably attributed to a systemic cause.

---

## 7. P52 V2 Contract Annotation Recommendation

P52 V2 monitoring contract should receive a **sample-sensitive band-level annotation** noting:
- The 1.00-1.25 band ECE should be interpreted cautiously when monthly n < 30.
- Sep 2025 mid-band n=27 is below the P48 SAMPLE_LIMITED threshold of 100.
- No contract threshold change is recommended; annotation only.

---

## 8. Limitations

1. Sep mid-band n=27 is small; ECE estimates have high variance.
2. Leave-one-out ECE measures raw individual error proxy, not exact ECE contribution.
3. Platt transformation was fit on a different dataset; its performance in sub-bands may degrade with small n.
4. No Jul data in P54 band comparison; Jul 1.00-1.25 band is now included if JSONL data exists.
5. This is a diagnostic report only; results do not affect runtime, deployment, or betting strategy.

---

## 9. 2024 Data Gap Status

**The 2024 closing-line data gap (P43_BLOCKED_BY_DATA_GAP) remains unresolved.**  
This analysis is based exclusively on 2025 Tier C data.  
Cross-year closing-line edge validation cannot be completed until 2024 historical odds are obtained.

---

## 10. Final P55 Classification

```
P55_INCONCLUSIVE_SAMPLE_LIMITED
```

---

## 11. Next Recommended Diagnostic Task

Given `P55_INCONCLUSIVE_SAMPLE_LIMITED`:
- If classification is `P55_INCONCLUSIVE_SAMPLE_LIMITED`: P56 should focus on expanding the mid-band sample across 2024 (when data available) or monitoring Sep 2026 mid-band as additional data accumulates.
- If classification is `P55_OUTLIER_DRIVEN_MID_BAND_ANOMALY_DIAGNOSTIC`: P56 should investigate whether the top-3 outlier games share a common context (park, opponent, bullpen usage).
- If classification is `P55_PLATT_WORSENED_MID_BAND_DIAGNOSTIC`: P56 should investigate Platt behavior in mid-band probability range; consider whether a band-specific correction is warranted (paper analysis only).

---

*Governance: paper_only=True, diagnostic_only=True, promotion_freeze=True, live_api_calls=0*  
*P45 Platt constants unchanged: A=0.435432, B=0.245464*  
*P52/P53/P54 artifacts not overwritten.*
