# P82B — Raw Paid Odds Data Storage / Commit Policy Contract

**Snapshot**: raw_paid_odds_data_policy_contract_20260526  
**Schema version**: p82b-v1  
**Classification**: `P82B_RAW_PAID_DATA_POLICY_READY`  
**Generated**: 2026-05-26T10:24:39.630345+00:00

---

## Step 1 — P82A State Verification

| Check | Result |
|---|---|
| classification_correct | ✅ PASS |
| p82_unlock_status_blocked | ✅ PASS |
| p82_unlocked_false | ✅ PASS |
| live_api_calls_zero | ✅ PASS |
| raw_data_policy_field_present | ✅ PASS |
| contains_api_key_must_be_false | ✅ PASS |
| forbidden_scan_passed | ✅ PASS |
| production_ready_false | ✅ PASS |
| intake_gate_defined | ✅ PASS |

- **P82A classification**: `P82A_REAL_LEGAL_ODDS_INTAKE_GATE_READY`
- **P82 unlock status**: `BLOCKED_NO_REAL_DATASET`
- **Manifest fields**: 23
- **raw_data_policy field present**: True
- **contains_api_key must be False**: True
- **Total blockers**: 12
- **Only real legal dataset unlocks P82**: True

---

## Step 2 — Artifact Classes

**9 artifact classes defined**

| Class ID | can_commit | Default Policy |
|---|---|---|
| `RAW_PAID_ODDS_DATA` | ❌ No | LOCAL_ONLY_DO_NOT_COMMIT |
| `RAW_FREE_LEGAL_ODDS_DATA` | ⚠️ Conditional | COMMIT_ALLOWED_ONLY_IF_LICENSE_ALLOWS |
| `VALIDATION_MANIFEST` | ✅ Yes | COMMIT_ALLOWED |
| `CHECKSUM_ONLY_RECORD` | ✅ Yes | COMMIT_ALLOWED |
| `DERIVED_VALIDATION_SUMMARY` | ✅ Yes | COMMIT_ALLOWED |
| `DERIVED_MARKET_EDGE_SUMMARY` | ✅ Yes | COMMIT_ALLOWED_AGGREGATE_ONLY |
| `LOCAL_REPRODUCIBILITY_NOTE` | ✅ Yes | COMMIT_ALLOWED |
| `SECRET_OR_API_KEY` | ❌ No | HARD_FORBIDDEN |
| `MOCK_FIXTURE` | ✅ Yes | COMMIT_ALLOWED_IF_EXPLICITLY_LABELED_MOCK |

- **Hard-forbidden classes**: SECRET_OR_API_KEY
- **Local-only classes**: RAW_PAID_ODDS_DATA
- **Conditional commit**: RAW_FREE_LEGAL_ODDS_DATA

---

## Step 3 — Commit Policy Matrix

| Class ID | can_commit | can_stage | storage_location |
|---|---|---|---|
| `RAW_PAID_ODDS_DATA` | ❌ | ❌ | local_external_only — not inside repo di... |
| `RAW_FREE_LEGAL_ODDS_DATA` | ⚠️ | ⚠️ | data/mlb_2025/derived/ (if license confi... |
| `VALIDATION_MANIFEST` | ✅ | ✅ | data/mlb_2025/derived/... |
| `CHECKSUM_ONLY_RECORD` | ✅ | ✅ | data/mlb_2025/derived/... |
| `DERIVED_VALIDATION_SUMMARY` | ✅ | ✅ | data/mlb_2025/derived/... |
| `DERIVED_MARKET_EDGE_SUMMARY` | ✅ | ✅ | data/mlb_2025/derived/... |
| `LOCAL_REPRODUCIBILITY_NOTE` | ✅ | ✅ | docs/ or report/... |
| `SECRET_OR_API_KEY` | ❌ | ❌ | NEVER — must not exist anywhere in git h... |
| `MOCK_FIXTURE` | ✅ | ✅ | data/fixtures/ or tests/fixtures/... |

- **Matrix valid**: True
- **Validation errors**: []

---

## Step 4 — Staging Guard Contract

**Guard ID**: `p82b_staging_guard_v1`

| Rule ID | Guard State |
|---|---|
| `BLOCK_ENV_FILE` | `BLOCK_SECRET` |
| `BLOCK_API_KEY_PATTERN` | `BLOCK_SECRET` |
| `BLOCK_RAW_PAID_CSV` | `BLOCK_RAW_PAID_DATA` |
| `BLOCK_REAL_ODDS_FILENAME` | `BLOCK_UNPOLICIED_ODDS` |
| `BLOCK_CONTAINS_API_KEY_FLAG` | `BLOCK_SECRET` |
| `BLOCK_ROW_LEVEL_ODDS` | `BLOCK_ROW_LEVEL_LEAKAGE` |

**Guard states**: STAGE_CLEAN, BLOCK_RAW_PAID_DATA, BLOCK_SECRET, BLOCK_UNPOLICIED_ODDS, BLOCK_ROW_LEVEL_LEAKAGE, REVIEW_REQUIRED

**Hard-blocked classes**: SECRET_OR_API_KEY, RAW_PAID_ODDS_DATA

---

## Step 5 — Manifest Integration Policy

### raw_data_policy allowed values

- ✅ `LOCAL_ONLY_HASH_COMMITTED`
- ✅ `DERIVED_ONLY_COMMIT`
- ✅ `COMMIT_ALLOWED_LICENSE_VERIFIED`
- ✅ `MOCK_ONLY`

### raw_data_policy forbidden values

- ❌ `UNKNOWN`
- ❌ `COMMIT_RAW_PAID_DATA`
- ❌ `EMBED_SECRET`
- ❌ `UNLICENSED_SOURCE`

- **Default**: `LOCAL_ONLY_HASH_COMMITTED`
- **Checksum requirement**: SHA-256 checksum must be computed from the raw file before staging the manifest; checksum_hash is a mandatory non-nullable field
- **License evidence requirement**: source_license_evidence_ref must point to a stored license document; cannot be empty or a placeholder like TBD

---

## Step 6 — Future Real Data Workflow

### Step 1: Acquire legal odds data outside git

- **Where**: External acquisition — never inside repo directory
- **Gate**: Source must have a verifiable legal license; LEGAL_OR_LICENSED required

### Step 2: Store raw paid data in local external path

- **Where**: Local filesystem path outside repo (e.g. ~/odds-data/2025/raw/)
- **Gate**: Raw data path must not appear in any committed file

### Step 3: Generate manifest with checksum, row count, and schema version

- **Where**: data/mlb_2025/derived/intake_manifest_<season>.json
- **Gate**: _validate_manifest() from P82A script must return valid=True with zero errors

### Step 4: Run P81 validator locally against raw file

- **Where**: Local execution; validation summary written to data/mlb_2025/derived/
- **Gate**: Validator must return LEGAL_ODDS_DATASET_VALIDATED_FOR_P82 before advancing

### Step 5: Commit only manifest, checksum record, and derived validation summary

- **Where**: data/mlb_2025/derived/ — no raw data rows in diff
- **Gate**: Staging guard STAGE_CLEAN required; diff must contain zero raw paid odds values

### Step 6: Run P82 dry-run edge diagnostics only after P82A unlock criteria pass

- **Where**: Local execution; aggregate summary to data/mlb_2025/derived/
- **Gate**: _run_unlock_decision(manifest) must return can_unlock_p82=True

### Step 7: Never commit API key values, raw paid odds rows, or proprietary row-level values

- **Where**: Entire repo lifetime — no time limit, no exception path without authorization
- **Gate**: HARD_FORBIDDEN — no override without explicit governance authorization record

- **P82 remains blocked**: True
- **Block reason**: BLOCKED_NO_REAL_DATASET — workflow steps 1-4 must complete before P82 unlock

---

## Step 7 — Source Artifacts

- **Total**: 14 | **All present**: True
- **Missing**: []

---

## Step 8 — Forbidden Scan

- **Scan passed**: True
- **Violations**: 0
- **Patterns checked**: 10
- **Lines scanned**: 1037

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
| `p82b_storage_policy_defined` | `True` |

---

## Current P82 Status

- **P82 unlock status**: `BLOCKED_NO_REAL_DATASET`
- **P82B current status**: RAW_PAID_DATA_POLICY_DEFINED — awaiting real legal odds dataset
- **live_api_calls**: 0
- **ev_clv_kelly_computed**: False

---
*Generated by P82B — paper_only=True | diagnostic_only=True | no_real_bet_enforced*