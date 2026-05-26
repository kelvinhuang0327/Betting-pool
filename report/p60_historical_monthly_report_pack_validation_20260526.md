# P60 — Historical Monthly Report Pack (EDGE-FIRST Validation)
**Date:** 2026-05-26  
**Phase:** P60  
**Classification:** `P60_EDGE_STABLE_ACROSS_MONTHS`  
**Framing:** EDGE-FIRST (edge vs closing line is primary metric; calibration is secondary)

---

## 1. Pre-flight Result

| Check | Result |
|---|---|
| paper_only | PASS (True) |
| diagnostic_only | PASS (True) |
| kelly_deploy_allowed | PASS (False) |
| live_api_calls | PASS (0) |
| promotion_freeze | PASS (True) |
| runtime_recommendation_logic_changed | PASS (False) |
| P45 Platt constants | PASS (A=0.435432, B=0.245464) |
| T_LOCKED | PASS (0.50) |
| Forbidden string scan | PASS (0 violations) |

---

## 2. Source Artifacts Loaded

| Artifact | Status | SHA256 (first 16 chars) |
|---|---|---|
| P52 Monitoring Contract V2 | LOADED | `60a482a8b27348b3...` |
| P58 Monthly Report Template | LOADED | `2c234b086d8196e6...` |
| P59 First Monthly Report | LOADED | `dbb8ef6d97b457b6...` |
| P45 Platt Recalibration | LOADED | `8bd525cf6706227b...` |
| P44 Temporal Stability | LOADED | (auxiliary) |
| P53 Sep Calibration Audit | LOADED | (auxiliary) |

**P52–P59 artifacts NOT overwritten:** confirmed. All artifact_overwritten flags = False.

---

## 3. Available Months (Apr–Sep 2025)

| Month | n | Data Status |
|---|---|---|
| 2025-04 | 16 | Available (Tier C) |
| 2025-05 | 120 | Available (Tier C) |
| 2025-06 | 101 | Available (Tier C) |
| 2025-07 | 92 | Available (Tier C) |
| 2025-08 | 108 | Available (Tier C) |
| 2025-09 | 98 | Available (Tier C) |

**Total Tier C games:** 535  
**Filter:** `|sp_fip_delta| >= 0.50`, `market_home_prob_no_vig in (0,1)`, `home_win defined`

---

## 4. Per-Month Edge Metrics (EDGE-FIRST — PRIMARY)

> **EDGE-FIRST:** edge vs closing line is the primary validation. The question is: does the model consistently beat the closing line?
>
> **Edge formula:** `sigmoid(k=0.8 * |sp_fip_delta|) - market_prob_on_favored_side` (P44 canonical)  
> **CI method:** bootstrap (n_boot=5000, seed=42, percentile 95%)  
> **P52 V2 thresholds:** EDGE_WITHIN_THRESHOLD if mean ≥ 0.07 AND ci_low > 0

| Month | n | Edge Mean | CI Low | CI High | CI_low > 0? | Edge Status |
|---|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0954 | 0.0565 | 0.1331 | YES | **EDGE_WITHIN_THRESHOLD** |
| 2025-05 | 120 | 0.1050 | 0.0885 | 0.1213 | YES | **EDGE_WITHIN_THRESHOLD** |
| 2025-06 | 101 | 0.1101 | 0.0923 | 0.1287 | YES | **EDGE_WITHIN_THRESHOLD** |
| 2025-07 | 92 | 0.1083 | 0.0914 | 0.1261 | YES | **EDGE_WITHIN_THRESHOLD** |
| 2025-08 | 108 | 0.1003 | 0.0852 | 0.1153 | YES | **EDGE_WITHIN_THRESHOLD** |
| 2025-09 | 98 | 0.1084 | 0.0919 | 0.1244 | YES | **EDGE_WITHIN_THRESHOLD** |

**Result: 6/6 months EDGE_WITHIN_THRESHOLD. All CI_low > 0. Average edge = 0.1046.**

---

## 5. Per-Month Calibration & Sample Metrics (SECONDARY)

> **SECONDARY:** Calibration informs model reliability but does not override edge status.  
> **Platt formula:** `sigmoid(A * log_odds(model_home_prob) + B)`, P45-locked constants  
> **P52 V2 thresholds:** CALIBRATION_CRITICAL if platt_ece > 0.12; CALIBRATION_WARNING if > 0.10

| Month | n | Platt ECE | Platt Brier | Cal Status | Sample Status |
|---|---|---|---|---|---|
| 2025-04 | 16 | 0.0824 | 0.2527 | CALIBRATION_OK | SAMPLE_INSUFFICIENT |
| 2025-05 | 120 | 0.0595 | 0.2378 | CALIBRATION_OK | SAMPLE_ADEQUATE |
| 2025-06 | 101 | 0.0519 | 0.2401 | CALIBRATION_OK | SAMPLE_ADEQUATE |
| 2025-07 | 92 | 0.0508 | 0.2391 | CALIBRATION_OK | SAMPLE_WATCHLIST |
| 2025-08 | 108 | 0.0435 | 0.2474 | CALIBRATION_OK | SAMPLE_ADEQUATE |
| 2025-09 | 98 | **0.1229** | 0.2357 | **CALIBRATION_CRITICAL** | SAMPLE_WATCHLIST |

**Sep 2025 CALIBRATION_CRITICAL note:** platt_ece=0.1229 > threshold=0.12 (P52 V2). Edge remains healthy (mean=0.1084, ci_low=0.0919 > 0). Per P52 V2 dominance rules, SAMPLE_LIMITED does NOT suppress CALIBRATION_CRITICAL (P49 correction). Root cause under investigation (P53 audit).

---

## 6. VAL01–VAL10 Per-Month Summary

| Validation | Description | Apr | May | Jun | Jul | Aug | Sep |
|---|---|---|---|---|---|---|---|
| VAL01 | paper_only=True | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL02 | diagnostic_only=True | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL03 | kelly_deploy_allowed=False | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL04 | live_api_calls=0 | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL05 | promotion_freeze=True | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL06 | runtime_recommendation_logic_changed=False | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL07 | Platt A=0.435432, B=0.245464 | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL08 | t_locked=0.50 | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL09 | No forbidden strings | PASS | PASS | PASS | PASS | PASS | PASS |
| VAL10 | P52 thresholds unchanged | PASS | PASS | PASS | PASS | PASS | PASS |

**All 60 VAL checks (10 × 6 months): PASS**

---

## 7. Pack-Level Synthesis

| Metric | Value |
|---|---|
| Total months available | 6 |
| Months EDGE_WITHIN_THRESHOLD | **6/6** |
| Months EDGE_WARNING | 0/6 |
| Months EDGE_CRITICAL | 0/6 |
| Cross-month edge stability | **EDGE_STABLE_ACROSS_MONTHS** |
| Months CALIBRATION_OK | 5/6 |
| Months CALIBRATION_WARNING | 0/6 |
| Months CALIBRATION_CRITICAL | 1/6 (Sep 2025) |
| Average edge mean | **0.1046** |
| Average Platt ECE | 0.0685 |

---

## 8. EDGE-FIRST CONCLUSION

> **Apr–Sep 2025 模型是否穩定優於 closing line？**

**EDGE-FIRST RESULT: 是。模型穩定優於 closing line。**

具體結果：
- **6/6 月份 EDGE_WITHIN_THRESHOLD**（mean ≥ 0.07，CI_low > 0）
- 平均 edge = **0.1046**（>P52 V2 warning threshold 0.07）
- 所有月份 bootstrap 95% CI 均完全位於正值區間
- edge 訊號穩定性分類：**EDGE_STABLE_ACROSS_MONTHS**

校準注意事項（次要指標）：
- 5/6 月份 CALIBRATION_OK（platt_ece < 0.10）
- Sep 2025 CALIBRATION_CRITICAL（platt_ece=0.1229 > 0.12），但 edge 健康
- Sep 2025 校準異常根因仍在調查中（P53 audit ongoing）

**結論：** Apr–Sep 2025 模型持續優於 closing line，edge 訊號在整個賽季期間保持統計顯著性。

---

## 9. Sep 2025 Cross-Reference to P59

| Metric | P59 Reference | P60 Computed | Match |
|---|---|---|---|
| raw_edge_mean | 0.108441 | 0.108443 | YES (diff < 0.005) |
| platt_ece | 0.122929 | 0.122929 | YES (diff < 0.005) |
| batch_n | 98 | 98 | YES |
| overall_consistent | — | **True** | — |

P59 consistency check: **PASS**

---

## 10. Framing Note: 2024 Closing-Line Data Gap

**2024 closing-line data gap remains unresolved (P43_BLOCKED_BY_DATA_GAP).**

- This pack covers **2025-only** (Apr–Sep 2025, n=535 Tier C games)
- Cross-year market-edge validation (2024+2025) requires sourcing 2024 MLB moneyline closing odds
- The 2024 gap is a cross-year limitation only; it does NOT block 2025-only replay
- Resolution path: if `mlb_odds_2024_real.csv` is sourced (schema matching 2025 CSV), re-run P43

---

## 11. Files Created

| File | Purpose |
|---|---|
| `scripts/_p60_historical_monthly_report_pack_validation.py` | Main validation script |
| `tests/test_p60_historical_monthly_report_pack_validation.py` | Test suite (22 tests) |
| `data/mlb_2025/derived/p60_historical_monthly_report_pack_validation_summary.json` | JSON output artifact |
| `report/p60_historical_monthly_report_pack_validation_20260526.md` | This report |
| `00-BettingPlan/20260526/p60_historical_monthly_report_pack_validation_20260526.md` | Betting plan copy |

---

## 12. Test Results

```
tests/test_p60_historical_monthly_report_pack_validation.py — 22 passed in 0.07s
```

All 22 tests PASS including:
- VAL01–VAL10 per month (60 checks total)
- P59 Sep 2025 consistency
- Bootstrap CI deterministic (seed=42)
- Edge status classification per P52 V2
- P45 Platt constants unchanged
- P52 thresholds unchanged
- Forbidden string scan (0 violations)
- Pack classification validity

---

## 13. Forbidden String Scan

| Forbidden String | Result |
|---|---|
| "guaranteed profit" | NOT FOUND |
| "profitability claim" | NOT FOUND |
| "production proposal" | NOT FOUND |
| "live odds api call" | NOT FOUND |
| "champion replacement" | NOT FOUND |

**Forbidden scan: PASS (0 violations)**

---

## 14. Commit Hash

HEAD at time of P60: `b1332b341274eb939500a7747996ca476c406f44`

---

## 15. P52–P59 Artifacts Preservation Status

| Artifact | Overwritten | Hash Changed |
|---|---|---|
| P52 Monitoring Contract V2 | NO | NO |
| P53 Sep Calibration Audit | NO | NO |
| P54 FIP Delta Drift Audit | NO | NO |
| P55 Mid-Band Anomaly Audit | NO | NO |
| P56 Band Annotation Policy | NO | NO |
| P57 Annotation Integration | NO | NO |
| P58 Monthly Report Template | NO | NO |
| P59 First Monthly Report | NO | NO |
| P45 Platt Constants | NO | NO |

**All prior phase artifacts preserved. Zero modifications.**

---

## Governance

| Flag | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| kelly_deploy_allowed | False |
| live_api_calls | 0 |
| promotion_freeze | True |
| runtime_recommendation_logic_changed | False |
| champion_strategy_changed | False |
| tsl_crawler_modified | False |

*P60 is a paper-only, offline, diagnostic artifact. No deployment proposed. No runtime logic modified.*
