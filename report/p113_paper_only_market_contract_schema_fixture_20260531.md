# P113 Paper-Only Market Contract Schema Fixture (2026-05-31)

本文件為 MLB 台灣運彩風格 pregame 市場 schema fixture，僅供 paper-only/diagnostic-only 合約設計參考，嚴格禁止 production、推薦、賠率、EV、CLV、Kelly、下注等行為。

## Fixture Metadata
- fixture_version: P113.20260531
- generated_at: 2026-05-31
- source_gap_review_version: P112.20260531
- final_classification: P113_MARKET_CONTRACT_SCHEMA_FIXTURE_READY_WITH_BLOCKERS

## 來源參考
- gap_review_path: data/mlb_2026/derived/p112_lane_a_market_contract_gap_review_summary.json
- gap_review_version: P112.20260531
- final_classification: P112_LANE_A_MARKET_CONTRACT_GAP_REVIEW_READY_DIAGNOSTIC_ONLY

## 市場合約 (market_contracts)
- moneyline_winner: 支援，缺 legal odds，BLOCKED (LEGAL_ODDS_SOURCE_BLOCKER, GOVERNANCE_PRODUCTION_BLOCKER, EV_CLV_NOT_ALLOWED_BLOCKER)
- run_line_handicap: 不支援，BLOCKED (MARKET_SCHEMA_BLOCKER)
- total_runs_over_under: 不支援，BLOCKED (MARKET_SCHEMA_BLOCKER)
- first_five_innings_if_supported_later: 不支援，BLOCKED (MARKET_SCHEMA_BLOCKER)
- unsupported_market_placeholder: 不支援，BLOCKED (MARKET_SCHEMA_BLOCKER)

## 必要欄位
- required_prediction_fields: game_id, predicted_side
- required_odds_fields: odds (僅 schema，不 fetch)
- required_source_trace_fields: source_trace, source_prediction_version
- required_timestamp_fields: game_date, outcome_finalized_at
- required_outcome_fields: actual_winner, is_correct, result_home_score, result_away_score
- blocked_fields: ev, clv, kelly, stake, recommendation

## Governance Locks
- paper_only: true
- diagnostic_only: true
- production_ready: false
- real_bet_allowed: false
- recommendation_allowed: false
- odds_used: false
- odds_fetched: false
- live_api_calls: 0
- paid_api_calls: 0
- ev_computed: false
- clv_computed: false
- kelly_computed: false
- stake_sizing: false
- taiwan_lottery_recommendation: false
- champion_replacement: false
- production_mutation: false
- calibration_refit: false
- canonical_rows_modified: false
- outcome_rows_modified: false
- p83e_mapping_modified: false
- ui_modified: false

## Blocker Categories
- LEGAL_ODDS_SOURCE_BLOCKER
- MARKET_SCHEMA_BLOCKER
- SOURCE_TRACE_BLOCKER (如有)
- EV_CLV_NOT_ALLOWED_BLOCKER
- GOVERNANCE_PRODUCTION_BLOCKER
- DATA_COVERAGE_BLOCKER (如有)

## Allowed Next Actions
- diagnostic_tracking_only

## Prohibited Actions
- production
- recommendation
- betting
- odds
- ev
- clv
- kelly
- stake_sizing
- taiwan_lottery_recommendation

## Validation Rules
- 不可產生推薦
- 不可計算 EV/CLV/Kelly/stake/production readiness
- moneyline 僅 schema-ready，仍因 legal odds 缺失被 BLOCKED
- run line/total runs/first five innings 皆 BLOCKED
- 台灣運彩推薦必須為 false
- production readiness 必須為 false

---

本 fixture 僅供 schema/合約設計參考，嚴格禁止任何 production、推薦、賠率、EV、CLV、Kelly、下注等行為。
