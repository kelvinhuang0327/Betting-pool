# P80 — Market-Edge Lane Re-entry Readiness Contract

> **Generated**: 2026-05-26T09:44:12.312887+00:00  
> **Classification**: `P80_MARKET_EDGE_REENTRY_CONTRACT_READY`  
> **Schema**: `p80-v1`  
> **Mode**: `paper_only=True | diagnostic_only=True | NO_REAL_BET=True`

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

**EXPLICIT STATEMENT**: This phase makes NO live API calls, computes NO EV/CLV/Kelly, produces NO production recommendation, and does NOT treat the P79B fixture result as a 2026 live conclusion.

---

## Pre-flight & Prediction Lane Status

- P79B Classification: `P79B_TIER_B_FIXTURE_RESEARCH_ONLY`
- Fixture result: `TIER_B_RESEARCH_ONLY_FIXTURE`
- Fixture is 2026 live conclusion: `False`
- Tier B research only: `True`
- Tier B n=`219` hit_rate=`0.5342` AUC=`0.5517`
- Market-edge lane (from P79B): `blocked`
- Future P79 prompt exists: `True`
- Governance clean: `True`

---

## Market-Edge Blocker Summary

**Lane state**: `BLOCKED`

**Reason**: 2025 edge stable-negative + 2024 odds gap unresolved + API key missing + production governance frozen

| Blocker | State |
|---------|-------|
| `BLOCKED_2025_EDGE_STABLE_NEGATIVE` | ACTIVE |
| `BLOCKED_NO_LEGAL_2024_ODDS` | ACTIVE |
| `BLOCKED_ODDSPORTAL_TOS_VIOLATION` | ACTIVE |
| `BLOCKED_API_KEY_MISSING` | ACTIVE |
| `BLOCKED_RAW_DATA_POLICY_MISSING` | ACTIVE |
| `BLOCKED_PRODUCTION_GOVERNANCE` | ACTIVE |

- 2025 edge result: `P65_EDGE_STABLE_NEGATIVE`
- 2024 odds gap: `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`
- API key: `API_KEY_MISSING`
- OddsPortal scraping blocked by ToS: `True`

---

## Legal Odds Data Contract

**Required fields**: 21

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `game_id` | `str` | ✅ | Unique game identifier (matchable to prediction JSONL) |
| `game_date` | `str` | ✅ | Local game date |
| `season` | `int` | ✅ | MLB season year (e.g. 2024, 2025) |
| `home_team` | `str` | ✅ | Canonical home team name/abbrev |
| `away_team` | `str` | ✅ | Canonical away team name/abbrev |
| `sportsbook_or_source` | `str` | ✅ | Named sportsbook or licensed data vendor |
| `market_type` | `str` | ✅ | Betting market type |
| `odds_timestamp_utc` | `str` | ✅ | UTC timestamp when line was captured |
| `game_start_utc` | `str` | ✅ | UTC scheduled game start time |
| `home_moneyline` | `float` | ✅ | American odds for home team (e.g. -120, +110) |
| `away_moneyline` | `float` | ✅ | American odds for away team |
| `implied_home_prob` | `float` | ✅ | Vig-removed implied probability for home team |
| `implied_away_prob` | `float` | ✅ | Vig-removed implied probability for away team |
| `line_type` | `str` | ✅ | Where in game lifecycle line was taken |
| `is_pregame` | `bool` | ✅ | True if line was captured before game start |
| `is_closing` | `bool` | ✅ | True if this is the closing line |
| `source_license_status` | `str` | ✅ | Legal license status of data source |
| `source_trace` | `str` | ✅ | URL or vendor identifier of original data source |
| `raw_data_policy` | `str` | ✅ | Whether raw data may be committed to repo |
| `checksum_hash` | `str` | ✅ | SHA256 of raw line record for tamper detection |
| `created_at_utc` | `str` | ✅ | UTC timestamp this record was created/ingested |

### Legality Requirements

- **legal_source_required**: `True`
- **scraping_prohibited_source_blocked**: `True`
- **robots_txt_violation_blocked**: `True`
- **tos_violation_blocked**: `True`
- **api_key_value_must_not_be_printed**: `True`
- **api_key_value_must_not_be_logged**: `True`
- **raw_paid_data_commit_policy_decided_before_staging**: `True`
- **timestamp_lineage_proven_before_clv**: `True`
- **side_mapping_proven_before_edge**: `True`
- **doubleheader_disambiguation_required**: `True`
- **multi_season_validation_required_before_production**: `True`
- **known_blocked_sources**: `['OddsPortal (P68: ToS violation)']`
- **known_partial_sources**: `['P67 PATH_B partial — needs review before use']`
- **authorized_path**: `PATH_A: The Odds API (P70 CEO-authorized, P71 awaiting key)`

---

## Candidate Eligibility Matrix

| Candidate | Status | Market-Edge Eligibility |
|-----------|--------|------------------------|
| `TIER_C_HOME_PLUS_AWAY_125` | `ACTIVE_SHADOW_TRACKING` | ELIGIBLE_WHEN_LEGAL_ODDS_AVAILABLE... |
| `TIER_C_HOME_PLUS_AWAY_100` | `SHADOW_ONLY` | ELIGIBLE_WHEN_LEGAL_ODDS_AVAILABLE... |
| `TIER_B_ABS_FIP_0.25_TO_0.50` | `RESEARCH_ONLY` | CONDITIONAL: eligible only if future live P79 passes operati... |
| `TIER_C_BASELINE_ABS_GTE_0.50` | `BENCHMARK_REFERENCE` | ELIGIBLE_AS_BENCHMARK_ONLY... |

---

## Validation Gates

| Gate | Name | Current State |
|------|------|---------------|
| **A** | Data Legality | BLOCKED — no legal dataset exists yet |
| **B** | Schema Validation | BLOCKED — no dataset to validate |
| **C** | Side & Game Mapping | BLOCKED — no dataset to map |
| **D** | Metric Computation Readiness | BLOCKED — Gates A-C not satisfied |
| **E** | Cross-Year Validation | BLOCKED — 2024 odds gap unresolved (P67: partial source only |
| **F** | Governance Invariants | ACTIVE — governance invariants enforced by P80 GOVERNANCE di |

**Sequential dependency**: A → B → C → D → E (all must pass in order before production claim)

---

## Future Phase Path (P81-P84)

| Phase | Name | Trigger | Gate |
|-------|------|---------|------|
| **P80** | Market-Edge Lane Re-entry Readiness Contract | P79B fixture complete and market-edge lane blocked | paper-only |
| **P81** | Legal Odds Dataset Validator | The Odds API key received AND legal data downloade | paper-only |
| **P82** | Market-Edge Recomputation Dry-Run (Paper Only) | P81 Gates A-C passing | paper-only |
| **P83** | CLV Timestamp Validation | P82 passing AND closing line dataset exists | paper-only |
| **P84** | Cross-Year Market-Edge Synthesis | P83 passing AND 2024+2025 legal odds both validate | paper-only |
| **P85_PRODUCTION_GATE** | Production Gate (Future, Out of Scope) | Requires explicit CEO authorization after P84 | PRODUCTION |

**Next phase trigger**: The Odds API key received AND legal odds dataset downloaded

---

## STOP Conditions

- `api_key_accessed_in_code`
- `ev_calculated`
- `clv_calculated`
- `kelly_calculated`
- `kelly_deployed`
- `production_ready_set_true`
- `champion_replaced`
- `real_bet_placed`
- `odds_scraped_from_blocked_source`
- `raw_paid_data_committed_without_policy`
- `timestamp_lineage_unverified`
- `side_mapping_unverified`
- `2025_fixture_treated_as_2026_conclusion`
- `p79b_research_only_overridden`
- `tsl_crawler_modified`
- `runtime_recommendation_modified`
- `profitability_claimed`

---

## Decision Summary

**P80 Classification**: `P80_MARKET_EDGE_REENTRY_CONTRACT_READY`

The prediction-only lane (P72A→P79B) is complete and clean. The market-edge lane remains BLOCKED by 4 active blockers. This contract defines the readiness gates and data contract required for re-entry. No odds data was accessed, no EV/CLV/Kelly was computed, and no production recommendation was made.

---

## CTO 10-Line Summary

1. P80 is a contract-only phase defining market-edge re-entry conditions.
2. Prediction-only lane (P72A→P79B) is complete: primary=HOME_PLUS_AWAY_125, shadow=HOME_PLUS_AWAY_100.
3. Tier B remains RESEARCH_ONLY (fixture 2025: hit_rate=0.534, AUC=0.552).
4. Market-edge lane has 4 active blockers: negative 2025 edge, 2024 odds gap, API key missing, production governance.
5. P80 defines a 21-field legal odds dataset contract with strict legality requirements.
6. 4 prediction candidates have eligibility mapped: primary/shadow eligible, Tier B conditional, baseline benchmark.
7. 6 validation gates (A-F) defined: data legality → schema → mapping → metric → cross-year → governance.
8. Future path: P81 (validator) → P82 (edge dry-run) → P83 (CLV) → P84 (cross-year synthesis).
9. EV/Kelly remain prohibited; CLV requires closing data; production gate remains out of scope.
10. Forbidden scan PASS; governance invariants enforced; 0 live API calls.
