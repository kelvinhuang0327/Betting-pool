# P104 Outcome-Only Score Simulation Design — 2026-05-31

## Final Classification
P104_SCORE_SIMULATION_DESIGN_READY_DIAGNOSTIC_ONLY

## 設計目標
- 僅允許 win/loss/score/accuracy/diagnostic 分析
- 明確阻擋所有 betting/EV/CLV/Kelly/台灣運彩相關模組
- 合約 schema 必須包含 strategy_id、eligible_rows、predicted_side、actual_winner、win_loss_result、home_score、away_score、score_margin、score_margin_bucket、accuracy_metrics、sample_limitations
- 支援 win_loss_simulation_by_strategy、side_accuracy_by_strategy、monthly_win_loss_simulation、score_margin_descriptive_analysis
- HIGH_FIP 僅 diagnostic-only，MID/LOW 僅 watch-only
- 下一步：P105 Outcome-Only Win/Loss and Score Simulation Runner

## Schema
- strategy_id
- eligible_rows
- predicted_side
- actual_winner
- win_loss_result
- home_score
- away_score
- score_margin
- score_margin_bucket
- accuracy_metrics
- sample_limitations

## Supported Simulations
- win_loss_simulation_by_strategy
- side_accuracy_by_strategy
- monthly_win_loss_simulation
- score_margin_descriptive_analysis

## Blocked Simulations
- profit_simulation_blocked
- ev_simulation_blocked
- clv_simulation_blocked
- kelly_or_stake_simulation_blocked
- taiwan_lottery_recommendation_blocked

## Governance
- paper_only: true
- diagnostic_only: true
- production_ready: false
- real_bet_allowed: false
- recommendation_allowed: false
- odds_used: false
- ev_computed: false
- clv_computed: false
- kelly_computed: false
- stake_sizing: false
- taiwan_lottery_recommendation: false
- champion_replacement: false
- production_mutation: false
- calibration_refit: false
- live_api_calls: 0
- paid_api_calls: 0
- canonical_rows_modified: false
- outcome_rows_modified: false
- p83e_mapping_modified: false

## Next Implementation Target
P105 Outcome-Only Win/Loss and Score Simulation Runner

---

本設計僅為診斷/合約階段，未包含任何投注、EV、CLV、Kelly、台灣運彩或 production 相關邏輯。
