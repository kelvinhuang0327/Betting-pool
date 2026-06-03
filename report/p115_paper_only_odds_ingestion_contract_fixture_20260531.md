# P115 Paper-Only Odds Ingestion Contract Fixture (2026-05-31)

本文件為 MLB 台灣運彩 pregame paper-only odds ingestion contract fixture，僅供合約/驗證/治理設計參考，嚴格禁止 production、推薦、賠率、EV、CLV、Kelly、下注等行為。

## Fixture Metadata
- fixture_version: P115.20260531
- generated_at: 2026-05-31
- source_requirements_version: P114.20260531
- final_classification: P115_PAPER_ONLY_ODDS_INGESTION_CONTRACT_READY_WITH_BLOCKERS

## 來源參考
- requirements_path: data/mlb_2026/derived/p114_legal_odds_source_requirements_spec_summary.json
- requirements_version: P114.20260531
- final_classification: P114_LEGAL_ODDS_SOURCE_REQUIREMENTS_READY_WITH_BLOCKERS

## Paper-Only Ingestion Payload Contract
- 必要欄位: provider_id, provider_name, game_id, market_id, side, line, odds, publish_time, fetch_time, source_trace_id, audit_log_id
- 禁止欄位: real_odds, ev, clv, kelly, stake, profit, recommendation, production_ready
- 治理鎖: paper_only, diagnostic_only, production_ready=false, odds_used=false, odds_fetched=false, odds_stored=false, odds_ingested=false, recommendation_allowed=false, product_surface_allowed=false, live_api_calls=0, paid_api_calls=0, ev_computed=false, clv_computed=false, kelly_computed=false, stake_sizing=false, profit_computed=false, taiwan_lottery_recommendation=false, champion_replacement=false, production_mutation=false, calibration_refit=false, canonical_rows_modified=false, outcome_rows_modified=false, p83e_mapping_modified=false, ui_modified=false

## 市場 Payload 合約 (market_payload_contracts)
- moneyline_winner
- run_line_handicap
- total_runs_over_under
- first_five_innings_if_supported_later
- unsupported_market_placeholder

每個市場皆定義 payload_version, 必要 provider/game/market/side/line/odds/timestamp/source_trace/audit/dedupe/freshness/quality 欄位、blocker_type、prohibited_action、allowed_future_action。

## Dedupe Contract
- dedupe_key_fields: provider, game_id, market_id, side, fetch_time
- 不可有重複 odds 記錄

## Source Trace Contract
- 必要欄位: provider, fetch_timestamp, market_id, source_trace_id
- 必須可追溯至合法來源

## Timestamp Freshness Contract
- 必要欄位: publish_time, fetch_time
- pregame odds 必須 <5 分鐘

## Provider Metadata Contract
- 必要欄位: provider_id, provider_name
- 必須為合法授權業者

## Data Quality Validation Contract
- 必要欄位: odds
- 不可有缺漏、負數、重複，必須通過 dedup/audit

## Audit Log Contract
- 必要欄位: audit_log_id
- 必須可稽核

## Blocked Actions
- fetch_odds, store_odds, use_odds, ingest_odds, production, recommendation, ev, clv, kelly, stake_sizing, profit, taiwan_lottery_recommendation

## Governance Locks
- paper_only: true
- diagnostic_only: true
- production_ready: false
- odds_used: false
- odds_fetched: false
- odds_stored: false
- odds_ingested: false
- recommendation_allowed: false
- product_surface_allowed: false
- live_api_calls: 0
- paid_api_calls: 0
- ev_computed: false
- clv_computed: false
- kelly_computed: false
- stake_sizing: false
- profit_computed: false
- taiwan_lottery_recommendation: false
- champion_replacement: false
- production_mutation: false
- calibration_refit: false
- canonical_rows_modified: false
- outcome_rows_modified: false
- p83e_mapping_modified: false
- ui_modified: false

## Future Integration Gates
- Legal provider API contract signed
- Schema mapping validated
- Source trace and audit pipeline ready
- Ingestion implementation complete

## Validation Rules
- 本階段嚴禁任何賠率抓取、儲存、使用、ingest、計算
- 嚴禁任何推薦、EV、CLV、Kelly、stake、profit、production readiness
- 所有治理鎖必須維持 true
