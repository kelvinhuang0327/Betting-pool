# MLB Live Source Adapter Selection and Integration Plan

> **⚠️ PAPER-ONLY — PLAN DOCUMENT — NO REAL BET — NO PROFIT CLAIM**
>
> 本報告為 live source adapter 選擇與整合計畫文件。
> 不連接任何真實 API。不執行任何真實下注。不宣稱任何真實獲利。
> 所有候選 source 需人工驗證後方可用於 production 環境。

**Date:** 2026-05-07
**Generated:** 2026-05-07T09:01:48.465504+00:00
**Module:** `mlb_live_source_plan_v1`

---

## Safety Flags

- **production_modified**: `False`
- **no_real_bet**: `True`
- **paper_only**: `True`
- **no_profit_claim**: `True`
- **no_edge_claim**: `True`
- **no_auto_execution**: `True`
- **no_live_api_connected**: `True`
- **plan_only**: `True`
- **diagnostic_only**: `True`
- **fixture_not_production**: `True`

---

## Source Candidate Matrix

| Source ID | Type | Name | Method | Recommended | Needs Verification | Prod Readiness | Governance Risk |
|-----------|------|------|--------|-------------|-------------------|----------------|-----------------|
| sched_mlb_statsapi_v1 | schedule | MLB StatsAPI (statsapi.mlb.com | rest_api | ✅ YES | ⚠️ YES | needs_verification | low |
| sched_mlbdataapi_v1 | schedule | MLB Data API (via python-mlb-s | rest_api | ✅ YES | ⚠️ YES | needs_verification | low |
| sched_manual_csv_v1 | schedule | Manual CSV Import (daily sched | csv_import | ❌ NO | NO | ready | none |
| sched_fixture_v1 | schedule | Fixture Source (local JSON tes | fixture_file | ❌ NO | NO | not_ready | none |
| odds_theoddsapi_v2 | odds | The Odds API (the-odds-api.com | rest_api | ✅ YES | ⚠️ YES | needs_verification | low |
| odds_sportradar_v1 | odds | Sportradar Odds API | rest_api | ❌ NO | ⚠️ YES | needs_verification | low |
| odds_actionnetwork_scrape_v1 | odds | Action Network (web scraping) | web_scraping | ❌ NO | NO | blocked | high |
| odds_manual_csv_v1 | odds | Manual CSV Import (pre-game od | csv_import | ❌ NO | NO | ready | none |
| odds_fixture_v1 | odds | Fixture Odds Source (embedded  | fixture_file | ❌ NO | NO | not_ready | none |
| result_mlb_statsapi_v1 | result | MLB StatsAPI — Game Result (st | rest_api | ✅ YES | ⚠️ YES | needs_verification | low |
| result_manual_csv_v1 | result | Manual CSV Import (game result | csv_import | ❌ NO | NO | ready | none |
| result_replay_artifact_v1 | result | Historical Replay Artifact (pr | jsonl_artifact | ❌ NO | NO | ready | none |

**Total Candidates:** 12
- Schedule: 4
- Odds: 5
- Result: 3
- Recommended: 4
- Needs Verification: 5
- Blocked (scraping/fixture): 1

---

## Source Contract Schemas

### Schedule Source Contract (`mlb_schedule_source_contract_v1`)

**Freshness SLA:** 60 minutes

**Required Fields:**
  - `game_id`
  - `game_date`
  - `home_team`
  - `away_team`
  - `scheduled_start_time`
  - `game_status`

**Optional Fields:**
  - `probable_home_pitcher`
  - `probable_away_pitcher`
  - `venue`
  - `series_description`
  - `doubleheader_flag`
  - `broadcast_info`

**Unavailable Behavior:** If source is unavailable: set source_unavailable_flag=True, do not generate advisory, trigger fallback to DATA_LIMITED

**Fallback Behavior:** Fallback order: live current source → manual CSV import → fixture (tests/dry-run only) → DATA_LIMITED

### Odds Source Contract (`mlb_odds_source_contract_v1`)

**Freshness SLA:** 30 minutes

**Required Fields:**
  - `game_id`
  - `game_date`
  - `home_moneyline_odds`
  - `away_moneyline_odds`
  - `source_timestamp`

**Optional Fields:**
  - `runline_spread`
  - `runline_home_odds`
  - `runline_away_odds`
  - `total_line`
  - `over_odds`
  - `under_odds`
  - `bookmaker_source`
  - `closing_line_flag`
  - `market_consensus_flag`

**Unavailable Behavior:** If odds unavailable: set market_home_prob_no_vig=None, advisory must output PASS (no_model_prediction mode). Do not invent or estimate odds.

**Fallback Behavior:** Fallback: live odds API → manual CSV import → no odds (PASS advisory only) → DATA_LIMITED

### Result Source Contract (`mlb_result_source_contract_v1`)

**Freshness SLA:** 240 minutes

**Required Fields:**
  - `game_id`
  - `game_date`
  - `final_home_score`
  - `final_away_score`
  - `game_status`
  - `home_win`

**Optional Fields:**
  - `result_verified_at`
  - `innings_played`
  - `outs_recorded`
  - `postponed_rescheduled_date`

**Unavailable Behavior:** If result unavailable: ledger entries remain PENDING_REVIEW. Do not fabricate results. Do not mark as WON/LOST without confirmed data.

**Fallback Behavior:** Fallback: live result API → manual CSV import → manual override (human-entered) → remain PENDING

---

## Odds Normalization Contract

**Contract ID:** `mlb_odds_normalization_contract_v1`

**Existing Functions (reused — not re-implemented):**
- `american_odds_to_implied_prob` (orchestrator.mlb_current_sources): Converts American odds to raw implied probability. Positive (underdog): 100/(odds+100). Negative (favorite): |odds|/(|odds|+100).
- `normalize_two_way_no_vig` (orchestrator.mlb_current_sources): Removes bookmaker vig from two-way market. Divides each raw implied prob by total overround. Returns (no_vig_home_prob, no_vig_away_prob).

**Governance:**
- **no_stake_sizing**: `True`
- **no_vig_removal_does_not_imply_edge**: `True`
- **derived_probs_are_estimates_not_true_probabilities**: `True`
- **closing_line_value_not_computed_in_current_phase**: `True`

---

## Fallback Strategy

### Today Mode Fallback Priority

| Priority | Source | Condition |
|----------|--------|-----------|
| 1 | live_current_source | source reachable, schema valid, freshness OK |
| 2 | manual_csv_import | live source unavailable; human operator provides CSV |
| 3 | fixture_source | ONLY if explicitly allowed (dry-run / schema-test / demo); NEVER for production |
| 4 | replay_source | historical data only; date must be in historical range |
| 5 | DATA_LIMITED | all sources exhausted or unavailable |

### Replay Mode Fallback Priority

| Priority | Source | Condition |
|----------|--------|-----------|
| 1 | historical_prediction_artifact | date in JSONL, home_win available |
| 2 | historical_ledger_review_snapshot | ledger JSONL exists; reviewed_snapshot available |
| 3 | DATA_LIMITED | date not in historical data |

### Fixture Governance Rules

**Allowed Uses:**
- unit tests
- local dry-run
- schema contract validation
- demo / documentation
- adapter integration testing

**Forbidden Uses:**
- ⛔ production advisory (real advisory treated as live)
- ⛔ real-money recommendation
- ⛔ live source readiness claim
- ⛔ override of live source in production pipeline
- ⛔ bankroll / stake sizing calculation

---

## Integration Plan

### Phase Live-1: Schedule Source Adapter

**Goal:** Implement a live schedule source adapter that fetches today's MLB schedule from MLB StatsAPI (or manual CSV fallback). Validates schema contract. No odds dependency.

**Files to Create:**
- `orchestrator/mlb_schedule_source_adapter.py`
- `tests/test_mlb_schedule_source_adapter.py`
- `data/fixtures/mlb_schedule_source_test.json`

**Acceptance Criteria:**
- Adapter returns list of schedule rows matching MLBScheduleSourceContract
- All required fields present or explicit unavailable flags set
- Source health gate evaluates correctly (OK / STALE / UNAVAILABLE)
- Fixture source returns FIXTURE_NOT_PRODUCTION flag
- Postponed/cancelled games handled without exception
- All 6 new tests pass
- No regression in existing 1086+ tests

**Rollback Plan:** Revert orchestrator/mlb_schedule_source_adapter.py to previous version or delete if newly created. Fixture source remains available for testing. mlb_daily_scheduler.py already handles fixture fallback.

**Governance Guard:** PRODUCTION_MODIFIED=False throughout. Fixture source must not bypass production pipeline. Any live API fetch must be read-only.

### Phase Live-2: Odds Source Adapter

**Goal:** Implement an odds source adapter that normalizes moneyline/runline/total from a verified API (e.g. The Odds API). Applies american_odds_to_implied_prob + normalize_two_way_no_vig. Produces source health report per MLBOddsSourceContract.

**Files to Create:**
- `orchestrator/mlb_odds_source_adapter.py`
- `tests/test_mlb_odds_source_adapter.py`
- `data/fixtures/mlb_odds_source_test.json`

**Acceptance Criteria:**
- Adapter normalizes moneyline to no-vig probability using existing functions
- market_home_prob_no_vig in (0.0, 1.0) for all valid inputs
- Missing runline/total fields handled without exception
- Source health gate triggers correctly on >50% missing moneyline
- No stake_sizing field in any output
- All 8 new tests pass
- No regression in existing tests

**Rollback Plan:** Delete orchestrator/mlb_odds_source_adapter.py if newly created. Advisory falls back to market_home_prob_no_vig=None → PASS advisory.

**Governance Guard:** No stake sizing. No closing line value calculation. odds_normalization_contract_v1 enforced. API key must be stored in .env — never hardcoded. Scraping (ACTION_NETWORK) is blocked — must not be implemented.

### Phase Live-3: Result Source Adapter + Auto Post-game Review

**Goal:** Implement a result source adapter that fetches final scores from MLB StatsAPI and triggers automatic post-game ledger review. Handles postponed/cancelled/suspended per MLBResultSourceContract. Writes reviewed snapshot.

**Files to Create:**
- `orchestrator/mlb_result_source_adapter.py`
- `tests/test_mlb_result_source_adapter.py`
- `data/fixtures/mlb_result_source_test.json`

**Acceptance Criteria:**
- Adapter returns final scores matching MLBResultSourceContract
- home_win correctly derived from final scores
- Postponed games: home_win=None, ledger entries remain PENDING
- Cancelled games: ledger entries marked CANCELLED
- Auto post-game review triggers for FINAL games
- All 8 new tests pass
- No regression in existing tests

**Rollback Plan:** Delete orchestrator/mlb_result_source_adapter.py if newly created. Scheduler falls back to manual result ingestion path. Ledger entries remain PENDING — no data loss.

**Governance Guard:** No result fabrication. no_auto_result_fabrication=True enforced. human_review_required for suspended/cancelled games. LEDGER_OVERWRITE_BLOCKED=True must remain throughout.

### Phase Live-4: Daily Scheduler Integration + API Status + Source Freshness Dashboard

**Goal:** Integrate live schedule/odds/result adapters into mlb_daily_scheduler.py. Add API status endpoint for source freshness. Build source health dashboard (JSON + markdown). Full pipeline: live schedule → live odds → advisory → ledger → live result → post-game review → failure notes → manifest.

**Files to Create:**
- `orchestrator/mlb_source_health_dashboard.py`
- `tests/test_mlb_source_health_dashboard.py`

**Acceptance Criteria:**
- Scheduler gate reaches MLB_DAILY_SCHEDULER_READY with live sources
- API status endpoint returns source_health per source type
- Source freshness dashboard JSON + markdown generated
- Fallback to DATA_LIMITED when all live sources unavailable
- Completion marker MLB_DAILY_SCHEDULER_API_MVP_VERIFIED preserved
- All 6 new tests pass
- No regression in existing tests

**Rollback Plan:** Revert orchestrator/mlb_daily_scheduler.py to current version (scheduler v1). Fixture-based and replay-based pipelines remain operational. Gate reverts to MLB_SCHEDULER_DATA_LIMITED / MLB_SCHEDULER_API_MVP_READY.

**Governance Guard:** NO_REAL_BET=True throughout. PRODUCTION_MODIFIED=False throughout. No stake sizing in any new API endpoint. Live source freshness checks must not bypass DATA_LIMITED gate. MLB_LIVE_SOURCE_PLAN_VERIFIED must be in Phase Live-4 report.

---

## Gate Conclusion

**Gate: `MLB_LIVE_SOURCE_NEEDS_API_VERIFICATION`**

> Contracts and plan complete; 1 recommended odds source(s) require human API verification: The Odds API (the-odds-api.com)

---

## 人工決策事項

以下項目需人工確認後才可進入 production 環境：

1. **The Odds API** — 確認 API key 取得流程、費用方案、rate limit
2. **MLB StatsAPI** — 確認 ToS 對商業使用的限制
3. **Sportradar** — 成本評估（目前標記為 high cost / not recommended）
4. **Action Network scraping** — 已標記 BLOCKED，確認不會被誤用
5. **Fixture source** — 確認 FIXTURE_NOT_PRODUCTION guard 在所有 pipeline 路徑有效

---

## No Profit Claim

本系統不宣稱已找到任何可盈利的投注 edge。本計畫文件僅為 live source adapter 選擇與整合規劃。所有 paper advisory 均為研究目的，不代表任何真實獲利預期。

**NO_PROFIT_CLAIM = True**
**NO_EDGE_CLAIM = True**
**PAPER_ONLY = True**
**NO_REAL_BET = True**
**NO_LIVE_API_CONNECTED = True**
**PLAN_ONLY = True**

---

## Completion Marker

`MLB_LIVE_SOURCE_PLAN_VERIFIED`

