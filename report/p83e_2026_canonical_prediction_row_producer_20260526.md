# P83E — 2026 Canonical Prediction Row Producer
**Date:** 2026-05-26
**Classification:** `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA`
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Summary

P83E attempted to produce canonical 2026 prediction rows by loading upstream
schedule, pitcher FIP, and model output files.

**Result:** `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA`

---

## P83D Gate Recheck

| Gate | Status |
|---|---|
| SCHEDULE_GATE | ❌ FAIL |
| PITCHER_FEATURE_GATE | ❌ FAIL |
| MODEL_OUTPUT_GATE | ❌ FAIL |
| PREDICTED_SIDE_GATE | ❌ FAIL |
| GOVERNANCE_GATE | ✅ PASS |
| PRODUCER_ACTIVATION_GATE | ❌ FAIL |

---

## Upstream File Check

| File | Status |
|---|---|
| data/mlb_2026/schedule/mlb_2026_schedule.jsonl | ❌ Missing |
| data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl | ❌ Missing |
| data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl | ❌ Missing |

**Missing count:** 3

---

## Canonical Rows Status

- **Rows written:** False
- **Row count:** 0
- **Reason:** Blocked by missing upstream files: ['schedule', 'pitchers', 'model_outputs']

---

## sp_fip_delta Convention

Per P83C_UPSTREAM_INPUT_CONTRACT_V1:
- `sp_fip_delta = home_sp_fip - away_sp_fip`
- Positive → home pitcher favored (system convention)
- `predicted_side = 'home' if sp_fip_delta > 0 else 'away'`
- Ties (delta == 0) excluded from canonical output

---

## Rule Flag Thresholds (P83C)

| Flag | Condition |
|---|---|
| rule_primary_125_flag | home: abs >= 0.50 OR away: abs >= 1.25 |
| rule_shadow_100_flag | home: abs >= 0.50 OR away: abs >= 1.00 |
| tier_b_candidate_flag | 0.25 <= abs < 0.50 |
| tier_a_watchlist_flag | abs < 0.25 |

---

## Next Steps

```
[P83E Retry — Upstream Data Availability]

P83E remains blocked. Re-run when all three files exist locally:
  1. data/mlb_2026/schedule/mlb_2026_schedule.jsonl
     Fields: game_id, game_date, season, home_team, away_team
  2. data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl
     Fields: game_id, home_sp_fip, away_sp_fip
  3. data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl
     Fields: game_id, model_probability, source_prediction_version

Data sources (no API call in P83E):
  - statsapi.mlb.com/api/v1/schedule (free, public)
  - statsapi.mlb.com/api/v1/people (pitcher stats)
  - 2025-trained ensemble model applied to 2026 features

Rules: no external API calls in P83E itself | no odds | paper_only=True
```

---

## Governance Invariants

| Invariant | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| live_api_calls | 0 |
| odds_used | False |
| ev_calculated | False |
| clv_calculated | False |
| kelly_calculated | False |
| production_ready | False |
| canonical_rows_written | False |
| forbidden_scan_pass | True |

---

## Final Classification

**`P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA`**

P83E is the canonical 2026 prediction row producer. No external API calls are made. No market edge is computed. Canonical rows written only if all upstream gates pass. paper_only=True, diagnostic_only=True.
