# P118 Recommendation Row Validation Gate

- Gate version: P118.20260531
- Generated at: 2026-05-31
- Final classification: P118_RECOMMENDATION_ROW_VALIDATION_GATE_READY_WITH_BLOCKERS

## Required Row Invariants

- ROW_IS_PAPER_ONLY
- ROW_IS_DIAGNOSTIC_ONLY
- ROW_IS_BLOCKED
- NO_REAL_ODDS
- NO_RECOMMENDATION
- NO_EV_CLV_KELLY
- NO_STAKE_OR_PROFIT
- NO_PRODUCTION_READY
- NO_LIVE_API_CALLS
- NO_CANONICAL_ROW_MUTATION
- NO_OUTCOME_ROW_MUTATION
- SOURCE_TRACE_REQUIRED
- LEGAL_PROVIDER_REQUIRED_BEFORE_ACTIVATION

## Market-by-Market Validation

- moneyline_winner: blocked — moneyline_winner row must remain blocked, paper-only, diagnostic-only, and non-recommendational.
- run_line_handicap: blocked — run_line_handicap row must remain blocked, paper-only, diagnostic-only, and non-recommendational.
- total_runs_over_under: blocked — total_runs_over_under row must remain blocked, paper-only, diagnostic-only, and non-recommendational.
- first_five_innings_if_supported_later: blocked — first_five_innings_if_supported_later row must remain blocked, paper-only, diagnostic-only, and non-recommendational.
- unsupported_market_placeholder: blocked — unsupported_market_placeholder row must remain blocked, paper-only, diagnostic-only, and non-recommendational.

## Governance Validation

- paper_only: True
- diagnostic_only: True
- production_ready: False
- real_bet_allowed: False
- recommendation_allowed: False
- product_surface_allowed: False
- odds_used: False
- odds_fetched: False
- odds_stored: False
- odds_ingested: False
- live_api_calls: 0
- paid_api_calls: 0
- ev_computed: False
- clv_computed: False
- kelly_computed: False
- stake_sizing: False
- profit_computed: False
- recommendation_generated: False
- taiwan_lottery_recommendation: False
- champion_replacement: False
- production_mutation: False
- calibration_refit: False
- canonical_rows_modified: False
- outcome_rows_modified: False
- p83e_mapping_modified: False
- ui_modified: False
- branch_protection_modified: False
- force_push_used: False

## Allowed Future Actions

- May update fixture only after all blockers are cleared and governance is updated

## Prohibited Actions

- No recommendation, odds fetching, odds ingestion, EV, CLV, Kelly, stake sizing, profit, or production logic allowed

## Failure Modes

- Missing or invalid P117 fixture
- recommendation_allowed set true
- production_ready set true
- real odds, EV, CLV, Kelly, stake, or profit present
- missing source trace or legal provider

## Future Gate Requirements

- All legal, provider, ingestion, and governance blockers must be cleared before recommendation_allowed or production_ready can be set true.

## Blocked Decision Validation

- recommendation_allowed: False
- production_ready: False

## Odds Safety Validation

- real_odds_fields_forbidden: True
- ev_clv_kelly_forbidden: True
- stake_profit_forbidden: True

## Source Trace Validation

- source_trace_required: True
- legal_provider_required: True
