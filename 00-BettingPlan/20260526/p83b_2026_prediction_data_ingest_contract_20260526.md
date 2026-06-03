# P83B — 2026 Prediction Data Ingest Contract / Awaiting Stub
**Date:** 2026-05-26  
**Phase:** P83B  
**Classification:** `P83B_INGEST_CONTRACT_READY_AWAITING_DATA`  
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## P83A Awaiting-State Verification

- P83A classification: `P83A_AWAITING_2026_DATA` ✅
- Schema rows (2026 research): 0 ✅
- Runtime PAPER file excluded: ✅
- Snapshot thresholds: 5 ✅
- P82 status: `BLOCKED_NO_REAL_DATASET` ✅
- live_api_calls: 0 ✅

---

## Canonical 2026 Paths

- `prediction_rows_jsonl`: `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl`
- `derived_accumulation_rows_jsonl`: `data/mlb_2026/derived/p83_live_accumulation_rows.jsonl`
- `derived_accumulation_latest_summary_json`: `data/mlb_2026/derived/p83_live_accumulation_latest_summary.json`
- `live_report_md`: `report/p83_live_accumulation_latest.md`

**Runtime PAPER output:** NON_CANONICAL
> Runtime PAPER recommendation outputs use market-pipeline schema (contains edge_pct, kelly_fraction) and lack sp_fip_delta / predicted_side. These files must not be treated as canonical P83 research rows.
> Adapter: Future task: P83_RUNTIME_ADAPTER — transform PAPER output to P83A schema if needed.

---

## 2026 Row Schema (v1)

**Schema ID:** `P83B_2026_PREDICTION_ROW_SCHEMA_V1`

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
- `rule_primary_125_flag`
- `rule_shadow_100_flag`
- `tier_b_candidate_flag`
- `tier_a_watchlist_flag`
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
- `outcome_finalized_at`

### Governance Enforced Values
- `season` = `2026`
- `paper_only` = `True`
- `diagnostic_only` = `True`
- `odds_used` = `False`
- `market_edge_evaluated` = `False`
- `production_ready` = `False`

---

## 2025→2026 Extension Contract

**Source 2025:** `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
**Target 2026:** `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl`
**Version:** `mlb_2026_prediction_rows_v1`
**No retraining required:** ✅
**No live API required:** ✅

### Preserved Semantics
- **sp_fip_delta**: home_sp_fip - away_sp_fip, using same FIP calculation as 2025 pipeline. FIP = (13*HR + 3*(BB+HBP) - 2*K) / IP + FIP_constant.
- **model_probability**: P(home wins) from ensemble; convert to P(predicted_side wins) the same way as 2025 pipeline.
- **predicted_side**: Same logic: 'home' if sp_fip_delta > 0 else 'away'. Ties (sp_fip_delta == 0) excluded.
- **rule_primary_125**: Home: abs_sp_fip_delta >= 0.50 AND predicted_side='home'. Away: abs_sp_fip_delta >= 1.25 AND predicted_side='away'.
- **rule_shadow_100**: Home: abs_sp_fip_delta >= 0.50 AND predicted_side='home'. Away: abs_sp_fip_delta >= 1.00 AND predicted_side='away'.
- **tier_b**: 0.25 <= abs_sp_fip_delta < 0.50 (research only, n>=200 needed).
- **tier_a_watchlist**: abs_sp_fip_delta < 0.25 (monitoring only).
- **governance_fields**: paper_only=True, diagnostic_only=True, odds_used=False, market_edge_evaluated=False, production_ready=False. Same as 2025 pipeline.

---

## Validator Contract

**Validator ID:** `P83B_ROW_VALIDATOR_V1`
**abs_sp_fip_delta tolerance:** 1e-06

### Snapshot Triggers

| Level | Min n | Label | Classification |
|---|---:|---|---|
| smoke | 1 | `smoke_snapshot` | `P83C_SMOKE_SNAPSHOT_READY` |
| sample_limited | 10 | `first_sample_limited` | `P83C_SAMPLE_LIMITED_SNAPSHOT_READY` |
| checkpoint_1 | 50 | `checkpoint_1` | `P83C_CHECKPOINT_1_READY` |
| checkpoint_2 | 100 | `checkpoint_2` | `P83C_CHECKPOINT_2_READY` |
| operational | 200 | `operational_checkpoint` | `P83C_OPERATIONAL_SNAPSHOT_READY` |

---

## Future P83C Prompt

**Trigger:** When data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl exists with n>=1 rows
**Minimum n:** 1
**Preferred n:** 10

**2025 Baseline Reference:**
- Rule: `TIER_C_HOME_PLUS_AWAY_125` | hit=`0.6392` | AUC=`0.5787` | n=`316`

```
[P83C — 2026 Live Accumulation First Real Snapshot]

Continue from P83B (commit <P83B_COMMIT_HASH>). P83B_INGEST_CONTRACT_READY_AWAITING_DATA contract is in place.

2026 prediction rows are now available at:
  data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl

P83C must:
1. Load canonical 2026 prediction rows from canonical path.
2. Run P83B_ROW_VALIDATOR_V1 on each row.
3. Count: total rows / governance-clean / primary_125 / shadow_100 / tier_b / tier_a.
4. Determine snapshot level (smoke/sample_limited/checkpoint_1/checkpoint_2/operational).
5. If outcomes available: compute hit_rate / AUC / Brier / ECE.
   If not: classify as OUTCOMES_PENDING.
6. Compare 2026 hit_rate to 2025 baseline (HOME_PLUS_AWAY_125: hit=0.6392, AUC=0.5787).
7. Generate snapshot report.
8. Keep P82 market-edge blocked — no odds, no EV, no CLV, no Kelly.

paper_only=True | diagnostic_only=True | NO_REAL_BET=True
```

---

*paper_only=True | diagnostic_only=True | NO_REAL_BET=True*