# P83C — 2026 Prediction Pipeline Stub Generator / Schema Producer Contract

**Date**: 2026-05-26  
**Classification**: `P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA`  
**Mode**: paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Pre-flight Result

| Check | Result |
|-------|--------|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✓ |
| Branch | `main` ✓ |
| HEAD | `c4e1da6` (P83B) ✓ |
| P83B classification | `P83B_INGEST_CONTRACT_READY_AWAITING_DATA` ✓ |

## Dirty File Assessment

Various modified files in working tree (runtime state, logs, PAPER outputs).
None are governance violations for P83C. No forbidden patterns in staged files.

## Files Created / Modified

**Created:**
- `scripts/_p83c_2026_prediction_schema_producer_contract.py`
- `tests/test_p83c_2026_prediction_schema_producer_contract.py`
- `data/mlb_2026/derived/p83c_2026_prediction_schema_producer_contract_summary.json`
- `report/p83c_2026_prediction_schema_producer_contract_20260526.md`
- `00-BettingPlan/20260526/p83c_2026_prediction_schema_producer_contract_20260526.md`

**Modified:**
- `00-Plan/roadmap/active_task.md`

## Source Artifacts Loaded

| Artifact | Status |
|----------|--------|
| `data/mlb_2026/derived/p83b_2026_prediction_data_ingest_contract_summary.json` | ✓ Loaded |
| `data/mlb_2026/derived/p83a_2026_live_accumulation_first_snapshot_summary.json` | ✓ Loaded |
| `data/mlb_2025/derived/p82c_staging_guard_dryrun_scanner_summary.json` | ✓ Available |
| `data/mlb_2025/derived/p82b_raw_paid_odds_data_policy_contract_summary.json` | ✓ Available |
| `data/mlb_2025/derived/p77_prediction_only_shadow_tracker_contract_summary.json` | ✓ Available |
| `data/mlb_2025/derived/p76_corrected_tier_c_final_rule_selection_summary.json` | ✓ Available |

## P83B Ingest Contract Verification

- artifact_loaded: True
- p83b_classification: `P83B_INGEST_CONTRACT_READY_AWAITING_DATA`
- classification_ok: True
- canonical_paths_count: 4 (≥4 required)
- canonical_paths_ok: True
- schema_id: `P83B_2026_PREDICTION_ROW_SCHEMA_V1`
- schema_id_ok: True
- required_fields_count: 19 (19 required)
- governance_enforced_ok: True
- runtime_paper_noncanonical: True
- live_api_calls: 0
- **verification_ok: True**

## Upstream Input Contract

**Contract ID**: `P83C_UPSTREAM_INPUT_CONTRACT_V1`  
**Status**: AWAITING  
**upstream_data_found**: False  

**Required input groups:**

### game_schedule
- Description: 2026 MLB game schedule with unique game identifiers
- Fields: `game_id, game_date, season`
- Availability: `AWAITING`

### team_identifiers
- Description: Home and away team names for each game
- Fields: `home_team, away_team`
- Availability: `AWAITING`

### starting_pitcher_features
- Description: Starting pitcher FIP data required to compute sp_fip_delta. FIP formula: (13*HR + 3*(BB+HBP) - 2*K) / IP + FIP_constant
- Fields: `home_sp_fip, away_sp_fip`
- Availability: `AWAITING`

### model_output
- Description: Ensemble model probability output for each game
- Fields: `model_probability, predicted_side, source_prediction_version`
- Availability: `AWAITING`

### governance_flags
- Description: Governance enforcement fields — all values pre-defined
- Fields: `paper_only, diagnostic_only, odds_used, market_edge_evaluated, production_ready`
- Availability: `READY`

### FIP Formula

```
FIP = (13*HR + 3*(BB+HBP) - 2*K) / IP + FIP_constant
sp_fip_delta = home_sp_fip - away_sp_fip
abs_sp_fip_delta = abs(sp_fip_delta)
```

## Producer Output Schema

**Schema ID**: `P83C_PRODUCER_OUTPUT_SCHEMA_V1`  
**Inherits From**: `P83B_2026_PREDICTION_ROW_SCHEMA_V1`  
**Output Path**: `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl`  
**Format**: jsonl  
**Required Fields**: 19 fields  
**odds_required**: False  

**Required fields (19):**

| # | Field | Derivation |
|---|-------|-----------|
| 1 | `game_id` | sourced |
| 2 | `game_date` | sourced |
| 3 | `season` | sourced |
| 4 | `home_team` | sourced |
| 5 | `away_team` | sourced |
| 6 | `predicted_side` | derived/sp_fip |
| 7 | `model_probability` | sourced |
| 8 | `sp_fip_delta` | derived/sp_fip |
| 9 | `abs_sp_fip_delta` | derived/sp_fip |
| 10 | `source_prediction_version` | sourced |
| 11 | `rule_primary_125_flag` | derived/sp_fip |
| 12 | `rule_shadow_100_flag` | derived/sp_fip |
| 13 | `tier_b_candidate_flag` | derived/sp_fip |
| 14 | `tier_a_watchlist_flag` | derived/sp_fip |
| 15 | `paper_only` | governance constant |
| 16 | `diagnostic_only` | governance constant |
| 17 | `odds_used` | governance constant |
| 18 | `market_edge_evaluated` | governance constant |
| 19 | `production_ready` | governance constant |

## Rule Flag Computation Contract

**Contract ID**: `P83C_RULE_FLAG_COMPUTATION_CONTRACT_V1`  
**Deterministic**: True  
**no_ml_required_for_flags**: True  

**Formulas:**

- `abs_sp_fip_delta`: abs_sp_fip_delta = abs(sp_fip_delta)
- `rule_primary_125_flag`: home pick: abs_sp_fip_delta >= 0.50 | away pick: abs_sp_fip_delta >= 1.25 (TIER_C_HOME_PLUS_AWAY_125 per P76/P83B)
- `rule_shadow_100_flag`: home pick: abs_sp_fip_delta >= 0.50 | away pick: abs_sp_fip_delta >= 1.00 (TIER_C_HOME_PLUS_AWAY_100 per P76/P83B)
- `tier_b_candidate_flag`: 0.25 <= abs_sp_fip_delta < 0.50
- `tier_a_watchlist_flag`: abs_sp_fip_delta < 0.25

**Verification cases: True (5 cases all pass)**

## Schema-Only Mock Validation

**Dry-Run ID**: `P83C_MOCK_SCHEMA_ONLY_DRY_RUN_V1`  
**mock_row_count**: 4  
**mock_rows_in_memory_only**: True  
**mock_row_written_to_canonical**: False  
**canonical_path_exists**: False  
**real_row_count_in_canonical**: 0  
**snapshot_unlock_blocked**: True  
**schema_pass**: True  
**governance_pass**: True  
**rule_flags_pass**: True  

| Label | schema_pass | governance_pass | rule_flags_pass |
|-------|-------------|-----------------|-----------------|
| `home_strong` | True | True | True |
| `away_strong` | True | True | True |
| `home_tier_b` | True | True | True |
| `home_tier_a` | True | True | True |

## Future P83D Prompt

**Trigger**: Upstream 2026 pitcher FIP data and game schedule are available. Use P83C_UPSTREAM_INPUT_CONTRACT_V1 to fetch required inputs.  
**Minimum rows**: 1  

```
[P83D — 2026 Prediction Row Generator]

Continue from P83C (schema producer contract). P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA is in place.

Upstream 2026 pitcher FIP data and game schedule are now available.

P83D must:
1. Load 2026 game schedule + SP FIP data.
2. Compute sp_fip_delta = home_sp_fip - away_sp_fip per game.
3. Apply ensemble model → model_probability + predicted_side.
4. Compute rule flags per P83C_RULE_FLAG_COMPUTATION_CONTRACT_V1.
5. Write governance-clean rows to canonical JSONL path.
6. Run P83B_ROW_VALIDATOR_V1 on all rows.
7. Trigger P83A snapshot flow if n>=1 valid rows.
8. Compare 2026 hit_rate to 2025 baseline (HOME+AWAY_125: hit=0.6392, AUC=0.5787).

paper_only=True | diagnostic_only=True | NO_REAL_BET=True
```

## Final Classification

**`P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA`**

| Classification | Condition |
|---------------|-----------|
| P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA | No upstream 2026 data found |
| P83C_SCHEMA_PRODUCER_READY_WITH_EXISTING_UPSTREAM_DATA | Upstream data exists |
| P83C_BLOCKED_BY_MISSING_P83B_ARTIFACT | P83B JSON not found |
| P83C_FAILED_VALIDATION | Schema/governance/rule flag validation failed |

## Tests

Run: `./.venv/bin/pytest tests/test_p83c_2026_prediction_schema_producer_contract.py -v`

Expected: 38 tests PASS

## Forbidden Scan Result

**Result**: CLEAN  
**Violations**: 0

| Check | Status |
|-------|--------|
| THE_ODDS_API_KEY | CLEAN |
| edge_pct | CLEAN |
| ev_pct | CLEAN |
| clv_pct | CLEAN |
| kelly_fraction | CLEAN |
| production_ready=true | CLEAN |

## Governance Invariants

| Invariant | Value |
|-----------|-------|
| paper_only | True |
| diagnostic_only | True |
| live_api_calls | 0 |
| kelly_deploy_allowed | False |
| production_ready | False |
| ev_calculated | False |
| clv_calculated | False |
| odds_used | False |
| market_edge_evaluated | False |
| real_bet_allowed | False |

## Commit Hash

P83B HEAD: `c4e1da6`  
P83C will be committed after tests pass.

## CTO Agent 5-Line Summary

1. P83B ingest contract verified: classification=P83B_INGEST_CONTRACT_READY_AWAITING_DATA, 19-field schema V1 confirmed.
2. Upstream input contract defined: 5 input groups (schedule, teams, pitcher FIP, model output, governance constants) — none fetched in P83C.
3. Rule flag computation contract implemented: deterministic functions for abs_sp_fip_delta, primary_125, shadow_100, Tier B, Tier A — 5-case verification all pass.
4. Schema-only dry-run: 4 mock rows validated in-memory (MOCK_SCHEMA_ONLY); schema_pass=True, governance_pass=True, rule_flags_pass=True; canonical path not written; snapshot_unlock_blocked=True.
5. P83D prompt generated; forbidden scan CLEAN; classification=P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA.

## CEO Agent 5-Line Summary

1. P83C defines the complete recipe for producing 2026 prediction rows — no guessing, no improvisation when data arrives.
2. All rule flags (primary_125 / shadow_100 / Tier B / Tier A) are now code-verified as deterministic from pitcher FIP delta alone.
3. A dry-run mock validates the full schema pipeline in-memory without fabricating real prediction evidence.
4. The pipeline stays locked at paper_only=True — no odds, no edge, no Kelly — until P83D triggers with real 2026 data.
5. P83D is ready to execute the moment upstream FIP data and schedule are available.

## Next 24h Prompt

```
[P83D — 2026 Prediction Row Generator]

Prerequisite: Upstream 2026 MLB game schedule + starting pitcher FIP data available.
Continue from P83C commit <P83C_COMMIT_HASH>.
P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA contract is in place.

P83D must execute the producer contract:
1. Fetch 2026 game schedule + SP FIP from statsapi.mlb.com (season=2026).
2. Compute sp_fip_delta = home_sp_fip - away_sp_fip per game.
3. Apply 2025 ensemble model (no retraining) → model_probability + predicted_side.
4. Compute all rule flags per P83C_RULE_FLAG_COMPUTATION_CONTRACT_V1.
5. Write governance-clean rows to: data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl
6. Run P83B_ROW_VALIDATOR_V1 on all rows.
7. Trigger P83A snapshot flow (smoke n=1 / sample_limited n=10 / ...).
8. Compare 2026 hit_rate to 2025 baseline (HOME+AWAY_125: hit=0.6392, AUC=0.5787).

paper_only=True | diagnostic_only=True | NO_REAL_BET=True
```
