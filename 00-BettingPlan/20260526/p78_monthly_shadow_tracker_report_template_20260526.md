# P78 — Monthly Rule Monitoring Template + Shadow Tracker Report Pack

**Date:** 2026-05-26  
**Classification:** `P78_MONTHLY_SHADOW_TRACKER_TEMPLATE_READY`  
**Mode:** `prediction_only | paper_only=true | diagnostic_only=true | production_ready=false`  
**Source:** P77 commit `ffd2bc9` — P77_SHADOW_TRACKER_CONTRACT_READY  

---

## 1. Pre-flight & P77 Contract Verification

| Field | Value |
|-------|-------|
| P77 Classification | `P77_SHADOW_TRACKER_CONTRACT_READY` |
| Primary Rule | `TIER_C_HOME_PLUS_AWAY_125` |
| Shadow Rule | `TIER_C_HOME_PLUS_AWAY_100` |
| Semantics Status | `PASS` |
| paper_only | `True` |
| production_ready | `False` |
| Tier B Trigger N | `200` |
| Market Edge Status | `DEFERRED` |
| Verification | `PASS` |

---

## 2. Monthly Report Schema (vp78-v1)

The schema defines 7 required sections per monthly report:

**Section 1_metadata:** `report_month`, `generated_at`, `source_prediction_version`, `data_cutoff`, `mode`

**Section 2_governance:** `paper_only`, `diagnostic_only`, `odds_used`, `ev_calculated`, `clv_calculated`, `kelly_calculated`, `production_ready`, `live_api_calls`

**Section 3_rule_summary:** `primary_rule_name`, `shadow_rule_name`, `primary_n`, `shadow_n`, `primary_hit_rate`, `shadow_hit_rate`, `primary_auc`, `shadow_auc`, `primary_brier`, `shadow_brier`, `primary_ece`, `shadow_ece`

**Section 4_tier_b:** `tier_b_n`, `tier_b_hit_rate`, `tier_b_auc`, `tier_b_status`, `n_to_200`

**Section 5_tier_a:** `tier_a_n`, `tier_a_hit_rate`, `tier_a_auc`, `tier_a_status`

**Section 6_alerts:** `rolling_100_hit_rate`, `two_consecutive_months_below_50`, `ece_worsened`, `sample_status`, `alert_level`

**Section 7_decision:** `continue_primary_rule`, `keep_shadow_rule`, `tier_b_re_evaluation_triggered`, `market_edge_lane_status`, `next_action`

---

## 3. Fixture Monthly Reports (2025-04 → 2025-09)

Generated using 2025 historical data as fixture validation. No scientific claim — template validation only.

### 3.1 Monthly Summary Table

| Month | Primary N | Primary Hit% | Shadow N | Shadow Hit% | Tier B (cum) | Alert |
|-------|-----------|--------------|----------|-------------|--------------|-------|
| 2025-04 | 14 | 0.5000 | 15 | 0.5333 | 9 | **RED** |
| 2025-05 | 100 | 0.5900 | 107 | 0.5701 | 85 | **GREEN** |
| 2025-06 | 61 | 0.5738 | 70 | 0.5429 | 154 | **GREEN** |
| 2025-07 | 72 | 0.5972 | 77 | 0.5974 | 219 | **RED** |
| 2025-08 | 97 | 0.5567 | 100 | 0.5500 | 295 | **GREEN** |
| 2025-09 | 63 | 0.6508 | 76 | 0.6447 | 363 | **GREEN** |

### 3.2 Monthly Detail

#### 2025-04

**Primary Rule** (TIER_C_HOME_PLUS_AWAY_125): n=14, hit_rate=0.5, AUC=0.4583, Brier=0.2555, ECE=0.2339  
**Shadow Rule** (TIER_C_HOME_PLUS_AWAY_100): n=15, hit_rate=0.5333, AUC=0.5179, Brier=0.2524, ECE=0.2488  
**Tier B** (cumulative): n=9, hit=0.5556, status=accumulating, n_to_200=191  
**Tier A** (watchlist): n=1, hit=0.0, status=watchlist_only  
**Alerts**: rolling_100=None, two_consec=False, ece_worsened=True, sample=limited, **level=RED**  
**Decision**: continue_primary=True, tier_b_triggered=False, market_edge=blocked, next=urgent_review_required|continue_monthly_accumulation  

#### 2025-05

**Primary Rule** (TIER_C_HOME_PLUS_AWAY_125): n=100, hit_rate=0.59, AUC=0.642, Brier=0.2338, ECE=0.0576  
**Shadow Rule** (TIER_C_HOME_PLUS_AWAY_100): n=107, hit_rate=0.5701, AUC=0.6104, Brier=0.2363, ECE=0.0659  
**Tier B** (cumulative): n=85, hit=0.5658, status=accumulating, n_to_200=115  
**Tier A** (watchlist): n=10, hit=0.4444, status=watchlist_only  
**Alerts**: rolling_100=0.59, two_consec=False, ece_worsened=False, sample=sufficient, **level=GREEN**  
**Decision**: continue_primary=True, tier_b_triggered=False, market_edge=blocked, next=review_at_n200  

#### 2025-06

**Primary Rule** (TIER_C_HOME_PLUS_AWAY_125): n=61, hit_rate=0.5738, AUC=0.5808, Brier=0.2378, ECE=0.0333  
**Shadow Rule** (TIER_C_HOME_PLUS_AWAY_100): n=70, hit_rate=0.5429, AUC=0.5614, Brier=0.2396, ECE=0.0686  
**Tier B** (cumulative): n=154, hit=0.4928, status=accumulating_halfway, n_to_200=46  
**Tier A** (watchlist): n=18, hit=0.625, status=watchlist_only  
**Alerts**: rolling_100=0.6, two_consec=False, ece_worsened=False, sample=sufficient, **level=GREEN**  
**Decision**: continue_primary=True, tier_b_triggered=False, market_edge=blocked, next=review_at_n100  

#### 2025-07

**Primary Rule** (TIER_C_HOME_PLUS_AWAY_125): n=72, hit_rate=0.5972, AUC=0.4728, Brier=0.2426, ECE=0.1164  
**Shadow Rule** (TIER_C_HOME_PLUS_AWAY_100): n=77, hit_rate=0.5974, AUC=0.504, Brier=0.2423, ECE=0.1048  
**Tier B** (cumulative): n=219, hit=0.5385, status=TRIGGER_FIRED, n_to_200=0  
**Tier A** (watchlist): n=20, hit=0.5, status=watchlist_only  
**Alerts**: rolling_100=0.6, two_consec=False, ece_worsened=True, sample=sufficient, **level=RED**  
**Decision**: continue_primary=True, tier_b_triggered=True, market_edge=blocked, next=urgent_review_required|initiate_p79_tier_b_review|review_at_n100  

#### 2025-08

**Primary Rule** (TIER_C_HOME_PLUS_AWAY_125): n=97, hit_rate=0.5567, AUC=0.5366, Brier=0.2445, ECE=0.0242  
**Shadow Rule** (TIER_C_HOME_PLUS_AWAY_100): n=100, hit_rate=0.55, AUC=0.5282, Brier=0.2454, ECE=0.0295  
**Tier B** (cumulative): n=295, hit=0.5789, status=TRIGGER_FIRED, n_to_200=0  
**Tier A** (watchlist): n=21, hit=1.0, status=watchlist_only  
**Alerts**: rolling_100=0.55, two_consec=False, ece_worsened=False, sample=sufficient, **level=GREEN**  
**Decision**: continue_primary=True, tier_b_triggered=True, market_edge=blocked, next=initiate_p79_tier_b_review|review_at_n100  

#### 2025-09

**Primary Rule** (TIER_C_HOME_PLUS_AWAY_125): n=63, hit_rate=0.6508, AUC=0.6857, Brier=0.2219, ECE=0.0956  
**Shadow Rule** (TIER_C_HOME_PLUS_AWAY_100): n=76, hit_rate=0.6447, AUC=0.6967, Brier=0.2253, ECE=0.0902  
**Tier B** (cumulative): n=363, hit=0.4706, status=TRIGGER_FIRED, n_to_200=0  
**Tier A** (watchlist): n=24, hit=0.6667, status=watchlist_only  
**Alerts**: rolling_100=0.61, two_consec=False, ece_worsened=False, sample=sufficient, **level=GREEN**  
**Decision**: continue_primary=True, tier_b_triggered=True, market_edge=blocked, next=initiate_p79_tier_b_review|review_at_n100  

---

## 4. Alert Level Definitions

**GREEN**: Sample sufficient and no downgrade criteria triggered
- rolling_100_hit_rate >= 0.55 (or insufficient n for rolling)
- not two_consecutive_months_below_50
- not ece_worsened
- governance clean
- primary_n >= 50

**YELLOW**: Sample limited or one warning criterion triggered
- primary_n < 50 (insufficient sample for alert)
- rolling_100 not computable due to small n
  > *Sample limitation alone does NOT imply model failure*

**RED**: Downgrade criteria triggered; requires urgent review
- rolling_100_hit_rate < 0.55
- 2 consecutive eligible months hit_rate < 0.5
- ECE materially worsened (delta >= 0.03 from baseline)
- governance violation

---

## 5. Pack Synthesis

| Metric | Value |
|--------|-------|
| Months Generated | 6 (2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09) |
| All Schema Valid | `True` |
| All Governance Clean | `True` |
| Months with Alerts | ['2025-04', '2025-07'] |
| Primary Total N | 407 |
| Shadow Total N | 445 |
| Primary Avg Monthly Hit% | 0.5781 |
| Shadow Avg Monthly Hit% | 0.5731 |
| Tier B Accumulated N (end) | 363 |
| Tier B n≥200 Trigger Fires | `True` |
| Template Readiness | `P78_MONTHLY_SHADOW_TRACKER_TEMPLATE_READY` |

---

## 6. Governance Invariants & Forbidden Scan

**Method:** Direct GOVERNANCE dict value check (no text scanning).  
**Scan Result:** `PASS`  
**Violations:** 0  

| Invariant | Required | Actual |
|-----------|----------|--------|
| paper_only | True | True |
| diagnostic_only | True | True |
| ev_calculated | False | False |
| clv_calculated | False | False |
| kelly_calculated | False | False |
| production_ready | False | False |
| live_api_calls | 0 | 0 |

---

## 7. Market-Edge Separation

Market-edge (CLV / EV / Kelly) lane is **BLOCKED** in P78.  
This is a prediction-only shadow tracker. No odds data required.  
Market-edge remains deferred until P80 (requires The Odds API key).  

---

## 8. Tier B Accumulation Status

Tier B definition: `abs_sp_fip_delta` in [0.25, 0.50)  
Trigger: cumulative n ≥ 200 → initiates P79 Tier B review  
Tier B cumulative at end of fixture period (2025-09): **363**  
Trigger fires in fixture period: `True`  

---

## 9. P79 Recommendation

**P79 conditions:**
- Tier B cumulative n ≥ 200 (predicted ~2026-09 for live 2026 tracking)
- No governance violations
- No RED alert on primary rule

**P79 scope:** Full Tier B sample expansion analysis vs Tier C finalists on 2026 live data.  
**P80 scope:** Market-edge (CLV/EV/Kelly) lane — requires odds API key.  

---

## 10. Final Classification

> **`P78_MONTHLY_SHADOW_TRACKER_TEMPLATE_READY`**

---

*Generated by P78 Monthly Rule Monitoring Template | paper_only=True | NO_REAL_BET*