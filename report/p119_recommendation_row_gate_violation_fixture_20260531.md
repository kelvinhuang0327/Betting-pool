# P119 Recommendation Row Gate Violation Fixture — 報告 (2026-05-31)

## 版本與產出
- Fixture Version: P119.20260531
- 產出時間: 2026-05-31
- Final Classification: P119_GATE_VIOLATION_FIXTURE_READY_WITH_BLOCKERS

## 上游參考
- P118 Gate: data/mlb_2026/derived/p118_recommendation_row_validation_gate_summary.json
- P117 Fixture: data/mlb_2026/derived/p117_paper_only_recommendation_row_fixture_summary.json
- P116 Contract: data/mlb_2026/derived/p116_paper_only_recommendation_row_dry_run_contract_summary.json

## 負面測試範圍
本 fixture 專為驗證 recommendation row validation gate（P118）能正確阻擋所有違規推薦行為。所有案例皆為合成負面測試，預期全部被 gate block。

## 覆蓋市場
- moneyline_winner
- run_line_handicap
- total_runs_over_under
- first_five_innings_if_supported_later
- unsupported_market_placeholder

## 覆蓋違規案例
- recommendation_allowed_true_violation
- production_ready_true_violation
- real_odds_present_violation
- ev_field_present_violation
- clv_field_present_violation
- kelly_field_present_violation
- stake_field_present_violation
- profit_field_present_violation
- missing_source_trace_violation
- missing_legal_provider_violation
- canonical_row_mutation_violation
- outcome_row_mutation_violation
- taiwan_lottery_recommendation_true_violation

## Gate 預期行為
- 所有違規案例 expected_gate_status = BLOCKED
- governance_expected_result = BLOCKED
- 無任何案例被視為 valid recommendation row
- governance flags: recommendation_allowed=false, recommendation_generated=false, production_ready=false, taiwan_lottery_recommendation=false

## Invariant 覆蓋
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

## 允許與禁止行為
- Allowed Future Actions: None
- Prohibited Actions: Production, Recommendation, Real Odds

## 測試結果
- P119 專屬測試: 9/9 PASS
- P118 專屬測試: 5/5 PASS
- P117 專屬測試: 14/14 PASS

## 結論
本 fixture 已完整驗證 recommendation row gate 能正確阻擋所有違規推薦行為，符合所有治理與合約規範，允許進入下一階段。
