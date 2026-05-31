# P114 Legal Odds Source Requirements Spec (2026-05-31)

本文件為 MLB 台灣運彩 pregame 合法賠率來源需求規格，僅供 paper-only/diagnostic-only 合約設計參考，嚴格禁止 production、推薦、賠率、EV、CLV、Kelly、下注等行為。

## Spec Metadata
- spec_version: P114.20260531
- generated_at: 2026-05-31
- source_fixture_version: P113.20260531
- final_classification: P114_LEGAL_ODDS_SOURCE_REQUIREMENTS_READY_WITH_BLOCKERS

## 來源參考
- fixture_path: data/mlb_2026/derived/p113_paper_only_market_contract_schema_fixture_summary.json
- fixture_version: P113.20260531
- final_classification: P113_MARKET_CONTRACT_SCHEMA_FIXTURE_READY_WITH_BLOCKERS

## 合法賠率來源需求 (legal_odds_source_requirements)
- provider_authorization: 必須為合法授權業者（如台灣運彩），嚴禁爬蟲、非官方 API、灰色/非法來源
- odds_schema: 必須涵蓋所有 MLB pregame 合約市場（moneyline, run line, total runs, first five innings），賠率需為正數十進位，且與官方市場定義一致
- source_trace: 每筆賠率需含 provider、fetch timestamp、market id，並可稽核
- timestamp: 必須有官方發布時間與抓取時間，且 pregame 新鮮度 <5 分鐘
- market_mapping: 市場 id 與 side 必須與 contract schema fixture 對齊，並標註所有支援/不支援市場
- data_quality: 不可有缺漏、負數、重複，必須通過 dedup/audit
- deduplication: 以 (provider, game_id, market_id, side, fetch_time) 去重
- auditability: 所有賠率紀錄必須可追溯至合法來源

## 必要欄位
- source_trace_requirements: provider, fetch_timestamp, market_id, source_trace_id
- timestamp_requirements: publish_time, fetch_time
- market_mapping_requirements: market_id, side, contract_market_id, contract_side
- data_quality_requirements: no_missing_odds, no_negative_odds, no_duplicates, deduplication_passed, audit_passed
- deduplication_requirements: provider, game_id, market_id, side, fetch_time
- auditability_requirements: provider, source_trace_id, audit_log_id

## 市場賠率需求 (market_odds_requirements)
- 詳見 data/mlb_2026/derived/p114_legal_odds_source_requirements_spec_summary.json

## Governance Locks
- paper_only: true
- diagnostic_only: true
- production_ready: false
- real_bet_allowed: false
- recommendation_allowed: false
- product_surface_allowed: false
- odds_used: false
- odds_fetched: false
- odds_stored: false
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

## Blocked Actions
- fetch_odds, store_odds, use_odds, production, recommendation, ev, clv, kelly, stake_sizing, taiwan_lottery_recommendation

## Future Integration Gates
- Legal provider API contract signed
- Schema mapping validated
- Source trace and audit pipeline ready

## Validation Rules
- 本階段嚴禁任何賠率抓取、儲存、使用、計算
- 嚴禁任何推薦、EV、CLV、Kelly、stake、production readiness
- 所有 governance locks 必須維持 true
