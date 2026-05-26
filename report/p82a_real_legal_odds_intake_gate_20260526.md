# P82A — Real Legal Odds Dataset Intake Gate + P82 Blocker Closure Plan

**Snapshot**: real_legal_odds_intake_gate_20260526  
**Schema version**: p82a-v1  
**Classification**: `P82A_REAL_LEGAL_ODDS_INTAKE_GATE_READY`  
**Generated**: 2026-05-26T10:04:03.372403+00:00

---

## Step 1 — P81 State Verification

| Check | Result |
|---|---|
| classification | ✅ PASS |
| p82_unlock_status | ✅ PASS |
| live_api_calls | ✅ PASS |
| ev_clv_kelly | ✅ PASS |
| forbidden_scan_passed | ✅ PASS |
| production_ready | ✅ PASS |
| real_legal_dataset_available | ✅ PASS |
| mock_cannot_unlock_p82 | ✅ PASS |

- **P81 classification**: `P81_VALIDATOR_CONTRACT_READY_MOCK_ONLY`
- **P82 unlock status**: `BLOCKED_NO_REAL_DATASET`
- **live_api_calls**: 0
- **Validator script exists**: True
- **Input types**: REAL_LEGAL_ODDS_DATASET, MOCK_ODDS_FIXTURE, UNKNOWN_SOURCE_DATASET, SCRAPING_PROHIBITED_SOURCE, RAW_PAID_DATA_UNPOLICIED
- **Validator gates**: LEGALITY_GATE, RAW_DATA_POLICY_GATE, TIMESTAMP_GATE, MONEYLINE_GATE, IDENTITY_GATE

---

## Step 2 — Intake Manifest Schema

**23 required fields**

| Field | Type | Required Value / Rule |
|---|---|---|
| `manifest_id` | str | Unique ID for this intake manifest |
| `dataset_path` | str | Relative path to the dataset file |
| `dataset_type` | str | Must be `REAL_LEGAL_ODDS_DATASET` |
| `season` | int | Season year (e.g. 2025) |
| `source_name` | str | Name of originating sportsbook or data provider |
| `source_license_status` | str | Must be `LEGAL_OR_LICENSED` |
| `source_license_evidence_ref` | str | Path or URL to license evidence document |
| `acquisition_method` | str | How data was acquired (e.g. PAID_API, LICENSED_FEED) |
| `acquired_at_utc` | str | ISO-8601 UTC timestamp of acquisition |
| `acquired_by` | str | Person or system that acquired the data |
| `raw_data_policy` | str | Forbidden: `UNKNOWN`; allowed: ['COMMIT_ALLOWED', 'LOCAL_ONLY_HASH_COMMITTED', 'DERIVED_ONLY_COMMIT'] |
| `checksum_hash` | str | SHA-256 checksum of dataset file |
| `row_count` | int | Number of rows in the dataset |
| `expected_schema_version` | str | Must be `p81-v1` |
| `validator_script` | str | Path to P81 validator script |
| `validator_command` | str | Command to invoke the validator |
| `p81_validator_version` | str | Version string of the validator |
| `storage_policy` | str | Where dataset is stored (LOCAL_ONLY, CLOUD_PRIVATE, etc.) |
| `commit_policy` | str | Whether dataset is committed to git |
| `contains_api_key` | bool | Must be `False` |
| `contains_personal_data` | bool | Whether dataset contains PII |
| `allowed_next_phase` | str | P82 only after validator passes; null if blocked |
| `blocked_next_phase_reason` | str | Reason P82 is blocked if allowed_next_phase is null |

**Allowed raw_data_policy values**: COMMIT_ALLOWED, LOCAL_ONLY_HASH_COMMITTED, DERIVED_ONLY_COMMIT

---

## Step 3 — Blocker Closure Checklist

**12 blockers** (10 real-data, 2 governance)

| Blocker ID | Current Status | Unlock Effect |
|---|---|---|
| `REAL_DATASET_PRESENT` | `BLOCKED_PENDING_REAL_DATASET` | Permits validator invocation |
| `SOURCE_LEGALITY_PROVEN` | `BLOCKED_PENDING_REAL_DATASET` | Permits LEGALITY_GATE pass |
| `LICENSE_EVIDENCE_RECORDED` | `BLOCKED_PENDING_REAL_DATASET` | Required for audit trail |
| `RAW_DATA_POLICY_DECIDED` | `BLOCKED_PENDING_REAL_DATASET` | Permits RAW_DATA_POLICY_GATE pass |
| `CHECKSUM_RECORDED` | `BLOCKED_PENDING_REAL_DATASET` | Enables integrity verification before validator run |
| `SCHEMA_VALIDATED` | `BLOCKED_PENDING_REAL_DATASET` | Permits full 5-gate validation |
| `TIMESTAMP_LINEAGE_VALIDATED` | `BLOCKED_PENDING_REAL_DATASET` | Enables pregame edge diagnostics; closing pairs required for CLV |
| `MONEYLINE_VALIDATED` | `BLOCKED_PENDING_REAL_DATASET` | Enables implied probability computation |
| `IDENTITY_MAPPING_VALIDATED` | `BLOCKED_PENDING_REAL_DATASET` | Enables join to prediction candidates |
| `MOCK_DATA_EXCLUDED` | `BLOCKED_PENDING_REAL_DATASET` | Ensures real-data integrity; mock rows would invalidate edge diagnostics |
| `API_KEY_NOT_STORED` | `ACTIVE_GUARDRAIL` | Permanent guardrail — must be False at all times |
| `PRODUCTION_REMAINS_BLOCKED` | `ACTIVE_GUARDRAIL` | Permanent guardrail — P82 is dry-run only |

**P82 can open**: False  
**Requires**: All 10 real-data blockers CLOSED + 2 governance guardrails ACTIVE

---

## Step 4 — P82 Unlock Decision Function

**Function**: `_run_unlock_decision(manifest)`

**Required conditions to unlock P82**:

- manifest.dataset_type == REAL_LEGAL_ODDS_DATASET
- manifest.source_license_status == LEGAL_OR_LICENSED
- manifest.contains_api_key == False
- manifest.raw_data_policy in allowed policies
- manifest._validator_output_state == LEGAL_ODDS_DATASET_VALIDATED_FOR_P82
- GOVERNANCE.production_ready == False
- GOVERNANCE.kelly_deploy_allowed == False

**Scenario test results**:

| Scenario | can_unlock_p82 | Blocks |
|---|---|---|
| HYPOTHETICAL_REAL_LEGAL | `True` | — |
| MOCK_FIXTURE | `False` | WRONG_DATASET_TYPE:MOCK_ODDS_FIXTURE; VALIDATOR_NOT_PASSED:MOCK_FIXTURE_VALIDATOR_PASS_NOT_MARKET_READY |
| UNKNOWN_SOURCE | `False` | BAD_LICENSE_STATUS:UNKNOWN; VALIDATOR_NOT_PASSED:None |
| SCRAPING_PROHIBITED | `False` | BAD_LICENSE_STATUS:SCRAPING_TOS_VIOLATION |
| MISSING_DATASET | `False` | WRONG_DATASET_TYPE:None; VALIDATOR_NOT_PASSED:None |
| API_KEY_IN_DATA | `False` | API_KEY_PRESENT_IN_DATA |
| BAD_RAW_DATA_POLICY | `False` | BAD_RAW_DATA_POLICY:UNKNOWN |
| VALIDATOR_NOT_PASSED | `False` | VALIDATOR_NOT_PASSED:BLOCKED_SOURCE_LEGALITY |

**Only REAL_LEGAL_ODDS_DATASET unlocks P82**: True
**Current P82 status**: `BLOCKED_NO_REAL_DATASET`

---

## Step 5 — Future P82 Dry-Run Scope

**Allowed in P82**:

- load validated odds dataset
- join prediction candidates to odds rows via game_id
- compute market implied probabilities from home/away moneylines
- compute paper-only edge diagnostics (model prob vs implied prob)
- compare primary 125 vs shadow 100 vs baseline Tier C
- generate dry-run diagnostic report

**Prohibited in P82**:

- calculate Kelly criterion or position sizing
- recommend bets or wagering amounts
- change champion strategy or Tier C thresholds
- promote production readiness
- claim profitability from historical edge
- use unvalidated or partially-validated odds rows
- use mock odds or fixture data as real market evidence
- access the live odds api key env var
- compute CLV (reserved for P83 pending closing data and timestamp lineage)

**CLV status**: BLOCKED_UNTIL_P83 — closing-line pairs not yet confirmed in dataset; timestamp lineage must pass before CLV scope activates
**Production status**: BLOCKED — P82 is diagnostic dry-run only; paper_only=True remains

---

## Step 6 — Source Artifacts

| Artifact | Present |
|---|---|
| p81_legal_odds_dataset_validator_contract_summary.json | ✅ |
| p80_market_edge_reentry_readiness_contract_summary.json | ✅ |
| p79b_tier_b_vs_tier_c_comparison_harness_summary.json | ✅ |
| p79a_tier_b_trigger_readiness_contract_summary.json | ✅ |
| p78_monthly_shadow_tracker_report_template_summary.json | ✅ |
| p77_prediction_only_shadow_tracker_contract_summary.json | ✅ |
| p76_corrected_tier_c_final_rule_selection_summary.json | ✅ |
| p75b_calibration_diagnostics_corrected_tier_c_summary.json | ✅ |
| p75a_tier_c_corrected_rule_validator_summary.json | ✅ |
| p74_tier_c_home_away_bias_correction_summary.json | ✅ |
| p73_tier_stability_and_sample_expansion_summary.json | ✅ |
| p72b_objective_metric_contract_summary.json | ✅ |
| p72a_odds_free_strategy_accuracy_backtest_summary.json | ✅ |

---

## Step 7 — Forbidden Phrase Scan

- **Scan passed**: True
- **Violations**: 0
- **Patterns checked**: 10
- **Lines scanned**: 919

---

## Governance Invariants

| Key | Value |
|---|---|
| `paper_only` | `True` |
| `live_api_calls` | `0` |
| `ev_calculated` | `False` |
| `clv_calculated` | `False` |
| `market_edge_evaluated` | `False` |
| `kelly_calculated` | `False` |
| `kelly_deploy_allowed` | `False` |
| `production_ready` | `False` |
| `real_bet_allowed` | `False` |
| `champion_replacement_allowed` | `False` |
| `profitability_claim` | `False` |
| `promotion_freeze` | `True` |
| `tsl_crawler_modified` | `False` |
| `runtime_recommendation_modified` | `False` |
| `the_odds_api_key_required` | `False` |
| `the_odds_api_key_accessed` | `False` |
| `uses_historical_odds` | `False` |
| `odds_used` | `False` |
| `diagnostic_only` | `True` |
| `real_odds_dataset_present` | `False` |
| `p82_unlocked` | `False` |

---

## STOP Conditions

P82 **remains blocked** until all of the following are satisfied:

1. A real legal odds dataset file is present at manifest.dataset_path
2. source_license_status == LEGAL_OR_LICENSED (evidence documented)
3. raw_data_policy in allowed values
4. P81 validator returns LEGAL_ODDS_DATASET_VALIDATED_FOR_P82
5. All 10 real-data blockers are CLOSED
6. contains_api_key == False
7. GOVERNANCE.production_ready == False
8. GOVERNANCE.kelly_deploy_allowed == False

Mock data, fixture data, scraping-sourced data, or unknown-source data can **never** unlock P82.

---

*paper_only=True | diagnostic_only=True | live_api_calls=0 | ev_calculated=False | kelly_deploy_allowed=False*