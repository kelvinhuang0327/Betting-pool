# P117 Paper-Only Recommendation Row Fixture

- 產出日期：2026-05-31
- 來源合約：P116 paper-only recommendation row dry-run contract
- 上游依賴：P115, P114, P113, P112, P101, P84e
- 最終分類：P117_RECOMMENDATION_ROW_FIXTURE_READY_WITH_BLOCKERS

## 主要內容
- 本 fixture 僅供 schema/contract 驗證，無任何推薦、賠率、EV、CLV、Kelly、stake、profit、production output。
- 所有 market row fixture 均為 dry_run_status=blocked，governance_locks 全部為 diagnostic-only/paper-only/production_ready=false。
- 不產生任何推薦，不允許任何 production/mutation/odds/EV/CLV/Kelly/stake/profit。

## 主要欄位
- fixture_metadata
- source_p116_contract_reference
- paper_only_recommendation_rows
- market_row_fixtures
- prediction_field_fixtures
- market_field_fixtures
- odds_reference_fixtures
- source_trace_fixtures
- blocked_decision_fields
- governance_locks
- validation_rules
- future_integration_gates
- prohibited_actions

## Market Row Fixtures
- moneyline_winner
- run_line_handicap
- total_runs_over_under
- first_five_innings_if_supported_later
- unsupported_market_placeholder

## Blocker Categories
- LEGAL_ODDS_SOURCE_BLOCKER
- LEGAL_PROVIDER_AUTHORIZATION_BLOCKER
- ODDS_INGESTION_NOT_IMPLEMENTED_BLOCKER
- ODDS_SCHEMA_BLOCKER
- MARKET_MAPPING_BLOCKER
- SOURCE_TRACE_BLOCKER
- TIMESTAMP_FRESHNESS_BLOCKER
- DATA_QUALITY_BLOCKER
- EV_CLV_NOT_ALLOWED_BLOCKER
- KELLY_STAKE_NOT_ALLOWED_BLOCKER
- GOVERNANCE_PRODUCTION_BLOCKER
- RECOMMENDATION_NOT_ALLOWED_BLOCKER

## Governance Locks
- paper_only: true
- diagnostic_only: true
- production_ready: false
- recommendation_allowed: false
- odds_used: false
- ev_computed: false
- kelly_computed: false
- taiwan_lottery_recommendation: false

## 測試結果
- P117 專屬測試：PASS
- P116 專屬測試：PASS
- P115 專屬測試：PASS

---

本 fixture 僅供驗證與未來整合，所有推薦與 production 行為均被封鎖。