# P81 — Legal Odds Dataset Validator Contract

**Classification**: `P81_VALIDATOR_CONTRACT_READY_MOCK_ONLY`  
**Date**: 2026-05-26  
**Mode**: `paper_only=True | diagnostic_only=True | NO_REAL_BET=True`  
**Commit**: P81 (follows P80 `ecbcc37`)  

---

## Pre-flight

- Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Branch: `main`
- P80 classification: `P80_MARKET_EDGE_REENTRY_CONTRACT_READY`
- P80 required_field_count: 21 (expected 21)
- Gates defined: 6 (A-F)
- live_api_calls: 0
- API key accessed: False
- P80 readiness: **PASS**

---

## Step 1 — P80 Readiness Verification

| Item | Value |
|------|-------|
| P80 classification | `P80_MARKET_EDGE_REENTRY_CONTRACT_READY` |
| required_field_count | 21 |
| gates_open | ['gate_f_governance'] |
| gates_blocked | ['gate_a_data_legality', 'gate_b_schema', 'gate_c_mapping', 'gate_d_metric_readiness', 'gate_e_cross_year_validation'] |
| live_api_calls | 0 |
| api_key_accessed | False |
| status | **PASS** |

---

## Step 2 — Validator Input Types

| Input Type | Can Unlock P82 | Notes |
|------------|---------------|-------|
| `REAL_LEGAL_ODDS_DATASET` | YES | Must pass all 5 validator gates before P82 unlock |
| `MOCK_ODDS_FIXTURE` | NO | Passes schema gate; fails real-market readiness permanently |
| `UNKNOWN_SOURCE_DATASET` | NO | Blocked until source/license resolved |
| `SCRAPING_PROHIBITED_SOURCE` | NO | Hard blocked — OddsPortal TOS / robots.txt violation |
| `RAW_PAID_DATA_UNPOLICIED` | NO | Blocked until COMMIT_ALLOWED / LOCAL_ONLY_HASH_COMMITTED / DERIVED_ONLY_COMMIT declared |

> **Currently available**: `MOCK_ODDS_FIXTURE` only — P82 unlock: **BLOCKED**

---

## Step 3 — Required Schema Fields (21 fields from P80 contract)

| # | Field | Type Rule |
|---|-------|-----------|
| 1 | `game_id` | non-empty string |
| 2 | `game_date` | ISO-8601 UTC datetime string |
| 3 | `season` | numeric >= 2000 |
| 4 | `home_team` | non-empty string |
| 5 | `away_team` | non-empty string |
| 6 | `sportsbook_or_source` | non-empty string |
| 7 | `market_type` | non-empty string |
| 8 | `odds_timestamp_utc` | ISO-8601 UTC datetime string |
| 9 | `game_start_utc` | ISO-8601 UTC datetime string |
| 10 | `home_moneyline` | numeric (American odds) |
| 11 | `away_moneyline` | numeric (American odds) |
| 12 | `implied_home_prob` | float in (0, 1) |
| 13 | `implied_away_prob` | float in (0, 1) |
| 14 | `line_type` | one of ['moneyline', 'spread', 'total', 'runline'] |
| 15 | `is_pregame` | boolean |
| 16 | `is_closing` | boolean |
| 17 | `source_license_status` | one of ['LEGAL_OR_LICENSED', 'MOCK_VALIDATOR_ONLY'] |
| 18 | `source_trace` | non-empty string |
| 19 | `raw_data_policy` | one of ['COMMIT_ALLOWED', 'LOCAL_ONLY_HASH_COMMITTED', 'DERIVED_ONLY_COMMIT'] |
| 20 | `checksum_hash` | non-empty string |
| 21 | `created_at_utc` | ISO-8601 UTC datetime string |

---

## Step 4 — Validator Gates

| Gate | Description | Edge/EV/CLV Computed |
|------|-------------|---------------------|
| `LEGALITY_GATE` | source_license_status must be in allowed values; OddsPortal scrape = hard block | False |
| `RAW_DATA_POLICY_GATE` | raw_data_policy must declare storage/commit policy | False |
| `TIMESTAMP_GATE` | pregame odds_timestamp_utc < game_start_utc; closing flag required for CLV | False |
| `MONEYLINE_GATE` | moneylines numeric and convertible to implied probabilities; edge NOT computed | False |
| `IDENTITY_GATE` | game/team identity fields present and internally consistent | False |

---

## Step 5 — Mock Fixture Validation

### Valid Mock Fixture

- Schema valid: `True`
- All gates pass: `True`
- Can unlock P82: `False`
- Outcome: `MOCK_FIXTURE_VALIDATOR_PASS_NOT_MARKET_READY`
- Note: **MOCK_VALIDATOR_ONLY — not evidence of real legal odds**

### Invalid Mock Fixture (Expected Failures)

- Schema valid: `False`
- All gates pass: `False`
- Outcome: `BLOCKED_SOURCE_LEGALITY`
- Note: Expected to fail LEGALITY_GATE and RAW_DATA_POLICY_GATE

> Mock fixtures are NOT evidence of real legal odds. `can_unlock_p82 = False` for all mock types.

---

## Step 6 — Output Decision States

| State | Condition |
|-------|-----------|
| `LEGAL_ODDS_DATASET_VALIDATED_FOR_P82` | Only possible for REAL_LEGAL_ODDS_DATASET passing all 5 gates |
| `MOCK_FIXTURE_VALIDATOR_PASS_NOT_MARKET_READY` | Mock fixture passes schema; cannot unlock P82 |
| `BLOCKED_SOURCE_LEGALITY` | source_license_status prohibited or missing |
| `BLOCKED_SCHEMA_INVALID` | One or more required fields missing or invalid type |
| `BLOCKED_RAW_DATA_POLICY` | raw_data_policy not declared or UNKNOWN |
| `BLOCKED_TIMESTAMP_LINEAGE` | Timestamp ordering violation or unparseable |
| `BLOCKED_MONEYLINE_INVALID` | Moneyline values non-numeric or not convertible |
| `BLOCKED_IDENTITY_MAPPING` | Game/team identity fields missing or conflicting |
| `BLOCKED_NO_REAL_DATASET` | No real legal dataset provided; mock-only mode active |

**Current state**: `BLOCKED_NO_REAL_DATASET`  
**P82 unlock status**: BLOCKED — no real legal dataset present  

---

## Governance Invariants

| Flag | Value |
|------|-------|
| `paper_only` | `True` |
| `diagnostic_only` | `True` |
| `uses_historical_odds` | `False` |
| `live_api_calls` | `0` |
| `the_odds_api_key_required` | `False` |
| `the_odds_api_key_accessed` | `False` |
| `odds_used` | `False` |
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

---

## Forbidden Scan

- Scan passed: **True**
- Violations: 0
- Patterns checked: 10
- Lines scanned: 1012

---

## CTO Agent 10-Line Summary

1. P81 implements the legal odds dataset validator contract — no real odds pulled.
2. P80 readiness verified: classification=P80_MARKET_EDGE_REENTRY_CONTRACT_READY, 21-field contract, 6 gates.
3. 5 validator input types defined; only REAL_LEGAL_ODDS_DATASET can unlock P82.
4. 5 validator gates: LEGALITY, RAW_DATA_POLICY, TIMESTAMP, MONEYLINE, IDENTITY.
5. Schema validator checks all 21 P80 contract fields with type and range rules.
6. Valid mock fixture: schema PASS, gates PASS, market_readiness=False, P82 unlock=False.
7. Invalid mock fixture: LEGALITY_GATE and RAW_DATA_POLICY_GATE both FAIL as expected.
8. No EV, CLV, or Kelly computed; live_api_calls=0; API key not accessed.
9. Forbidden scan: PASS (0 violations).
10. Classification: P81_VALIDATOR_CONTRACT_READY_MOCK_ONLY — validator ready, awaiting real legal dataset.

---

## Next 24h Prompt

```
P82 — Market-Edge Recomputation Dry-Run
Prerequisite: P81_VALIDATOR_CONTRACT_READY_MOCK_ONLY (this task)
Trigger: Only when a REAL_LEGAL_ODDS_DATASET passes all 5 P81 validator gates.
Until then: dry-run only on mock fixture to validate P82 pipeline plumbing.
No EV/CLV/Kelly in production. paper_only=True. diagnostic_only=True.
```
