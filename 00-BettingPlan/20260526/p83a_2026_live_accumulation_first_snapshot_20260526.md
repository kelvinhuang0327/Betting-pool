# P83A — 2026 Live Accumulation First Snapshot / Awaiting Contract
**Date:** 2026-05-26  
**Phase:** P83A  
**Classification:** `P83A_AWAITING_2026_DATA`  
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## P82C Verification

- P82C classification: `P82C_STAGING_GUARD_DRYRUN_READY` ✅
- Scanner modes: 4 ✅
- Mock cases: ✅ PASS
- Repo guard state: `STAGE_CLEAN` ✅
- P82 status: `BLOCKED_NO_REAL_DATASET` ✅
- live_api_calls: 0 ✅

---

## 2026 Data Discovery

**Discovery mode:** Local paths only — no API calls. `discovery_local_only=True`

### Paths Searched

- `data/mlb_2026` ❌ not found
- `data/mlb_2026/derived` ❌ not found
- `data/mlb_2026/predictions` ❌ not found
- `data/mlb_2026/live` ❌ not found
- `outputs/online_validation` ❌ not found

**Files found:** 2
**2026 rows with required schema:** 0
**Data found:** NO

### Schema-Incompatible Files (sample)

- `outputs/recommendations/PAPER/2026-05-11/2026-05-11-AWY-HOM-824441.jsonl` — runtime_recommendation_pipeline_not_p83a_schema
- `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl` — runtime_recommendation_pipeline_not_p83a_schema

> Discovery searched local paths only. outputs/recommendations/PAPER/2026-* contains runtime pipeline outputs but uses different schema (no sp_fip_delta / predicted_side). These do not qualify as P83A prediction rows.

---

## Expected 2026 Row Schema

**Schema ID:** `P83A_2026_PREDICTION_ROW_SCHEMA_V1`

### Required Fields
- `game_id`
- `game_date`
- `season`
- `home_team`
- `away_team`
- `predicted_side`
- `model_probability`
- `sp_fip_delta`
- `abs_sp_fip_delta`
- `source_prediction_version`
- `paper_only`
- `diagnostic_only`
- `odds_used`
- `market_edge_evaluated`
- `production_ready`

### Optional Outcome Fields
- `actual_winner`
- `is_correct`
- `outcome_source`
- `outcome_available`

### Governance Required Values
- `paper_only` = `True`
- `diagnostic_only` = `True`
- `odds_used` = `False`
- `market_edge_evaluated` = `False`
- `production_ready` = `False`

**Expected canonical path:** `data/mlb_2026/predictions/mlb_2026_prediction_only_sp_fip_delta_v1.jsonl`

---

## Awaiting-Data Contract

**Status:** AWAITING

> No 2026 prediction rows with required P83A schema found in local repository. The runtime pipeline outputs (outputs/recommendations/PAPER/2026-05-11/) use a different schema (market/TSL pipeline, no sp_fip_delta field) and do not qualify as P83A prediction-only research rows.

### Snapshot Thresholds

| Threshold | Min n | Label |
|---|---:|---|
| smoke | 1 | `smoke_snapshot` |
| sample_limited | 10 | `first_sample_limited_report` |
| checkpoint_1 | 50 | `checkpoint_1` |
| checkpoint_2 | 100 | `checkpoint_2` |
| operational | 200 | `operational_checkpoint` |

### Rerun Trigger

- Condition: Any new file matching P83A schema in data/mlb_2026/ or outputs/online_validation/
- Minimum for rerun: n >= 1
- Recommended for first report: n >= 10

### Tracking Rules

- Primary: `TIER_C_HOME_PLUS_AWAY_125`
- Shadow: `TIER_C_HOME_PLUS_AWAY_100`
- Tier B: `TIER_B_ABS_DELTA_025_050`
- Tier A watchlist: `TIER_A_ABS_DELTA_BELOW_025`

**P82 market-edge:** BLOCKED — requires external legal odds dataset
**Next phase when data arrives:** P83B — 2026 Accumulation Snapshot with Outcomes

---

*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*