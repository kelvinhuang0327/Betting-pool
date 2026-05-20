# Strategy Historical Replay Page Discovery and Contract

Date: 2026-05-10
Repo: Betting-pool
Status: Discovery only, no production code changes

## Scope Note

This report distinguishes the current data surface from the proposed page contract. The goal is a user-facing strategy historical replay page that shows all strategies regardless of lifecycle state, and that mirrors the existing historical prediction list presentation style.

## Section A. Existing 歷史預測清單 Surface Map

I did not find a dedicated frontend page or route named history replay list in the current discovery pass. The closest existing surface is the markdown/report generation path that renders reviewed prediction rows from the replay/result review pipeline.

| Surface | Evidence | What it currently does |
|---|---|---|
| Prediction registry write path | [wbc_backend/reporting/prediction_registry.py](wbc_backend/reporting/prediction_registry.py#L49-L94) | Appends one JSONL record per prediction run. The stored shape includes recorded_at_utc, game_id, request, teams, verification, deployment_gate, game_output, prediction, simulation, top_bets, market_support, decision_report, calibration_metrics, and portfolio_metrics. |
| Prediction registry file paths | [wbc_backend/config/settings.py](wbc_backend/config/settings.py#L28-L32) | Central source of truth for prediction_registry_jsonl and postgame_results_jsonl file locations. |
| Latest prediction lookup | [wbc_backend/reporting/postgame_learning.py](wbc_backend/reporting/postgame_learning.py#L28-L37) | Loads the registry JSONL and returns the latest row by game_id. |
| Prediction summary fields | [wbc_backend/reporting/postgame_learning.py](wbc_backend/reporting/postgame_learning.py#L102-L120) | Derives a compact summary with predicted_home_win_prob, predicted_away_win_prob, predicted_home_score, predicted_away_score, confidence_index, verification_status, used_fallback_lineup, decision, decision_reasoning, market_support_primary, market_support_tilt, and best_bet_support_state. |
| Result review join logic | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L360-L391) | Matches ledger entries to outcomes by exact game_id first, then attempts a date/team fallback, but the fallback path is not actually resolved beyond a placeholder pass. |
| Review row schema | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L145-L159) | Review rows carry game_id, game_date, market_type, recommendation, paper_selection, model_prob, market_prob, result_status, realized_outcome, review_status, review_reason, paper_profit_loss_units, brier_component, failure_tags, paper_only, and no_real_bet. |
| Reviewed entry table output | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L1127-L1140) | The rendered historical list uses a table with columns game_id, date, mkt, rec, selection, result, review_status, and P&L. |
| Reviewed snapshot JSONL fields | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L933-L952) | Writes reviewed snapshot rows with ledger_id, advisory_id, game_id, game_date, market_type, recommendation, paper_selection, model_prob, market_prob, result_status, realized_outcome, review_status, review_reason, paper_profit_loss_units, brier_component, failure_tags, paper_only, and no_real_bet. |

### Current display fields

The current user-visible list format is essentially row-based review output with these display fields:

- game_id
- date
- market_type
- recommendation
- paper_selection
- result_status
- review_status
- paper_profit_loss_units

That is the best existing style match for the new replay page.

## Section B. Lifecycle State Storage Map

Current finding: there is no canonical strategy lifecycle store in the current WBC backend surface that I could identify during this pass. I found scattered status-like fields, but not a single source of truth for strategy lifecycle state or historical transitions.

| Evidence | What it means |
|---|---|
| [wbc_backend/optimization/continuous_learning.py](wbc_backend/optimization/continuous_learning.py#L73-L87) | FeatureExperiment has a status field with values testing, promoted, rejected. This is operational experiment state, not a replay strategy lifecycle store. |
| [wbc_backend/data/wbc_verification.py](wbc_backend/data/wbc_verification.py#L98-L105) | VerificationResult defaults status to REJECTED. This is a verification result, not a persisted strategy lifecycle ledger. |
| [wbc_backend/models/mlb_f5_moneyline.py](wbc_backend/models/mlb_f5_moneyline.py#L6-L26) | A model validation helper returns status values such as rejected and ready. This is model readiness state, not strategy lifecycle history. |
| wbc_backend search result | No canonical strategy_lifecycle or lifecycle_state store surfaced in wbc_backend during discovery. |

Conclusion: current lifecycle state is scattered and mostly current-state only. Historical lifecycle transitions are not preserved in a dedicated audit log that would support a replay page showing all lifecycle states over time.

## Section C. Prediction History Storage Map and Gap Analysis

### Current storage path

- The pipeline appends prediction records through [wbc_backend/pipeline/service.py](wbc_backend/pipeline/service.py#L73-L80).
- The append function writes a single JSONL record per run to [wbc_backend/reporting/prediction_registry.py](wbc_backend/reporting/prediction_registry.py#L49-L94).
- Retrieval in the current postgame learning flow is keyed by game_id only, not by strategy_id or lifecycle state, via [wbc_backend/reporting/postgame_learning.py](wbc_backend/reporting/postgame_learning.py#L28-L37).

### Current prediction record shape

The registry record stores a rich game-level summary, but it does not include a strategy_id field or any lifecycle state fields. It stores the request, teams, verification, deployment_gate, game_output, prediction, simulation, top_bets, market_support, decision_report, calibration_metrics, and portfolio_metrics.

### Gap analysis

| Gap | Severity | Why it matters |
|---|---|---|
| No strategy_id in the prediction registry record | Blocker | The requested page is strategy-based. Without strategy_id, the page cannot group or filter per strategy. |
| No lifecycle_state_at_time in stored prediction rows | Blocker | The page must show all strategies regardless of lifecycle state, and the historical lifecycle state at the time of prediction is required to avoid semantic drift. |
| No historical lifecycle transition log | Blocker | Current state alone is not enough when a strategy later moves from online to offline, rejected, or observation. |
| Storage is game-level, not per strategy per period | Blocker | The requested replay page needs one row per strategy-period outcome. The current registry is one row per game run. |
| Latest lookup is by game_id only | Important | The current retrieval model cannot safely reconstruct a full strategy replay timeline without a stable per-strategy period key. |
| No evidence that offline / rejected / observation strategies are preserved as historical prediction rows | Important | The discovery pass did not surface a storage path that guarantees those states retain their predictions. |

### Gap risk summary

Current data is enough to support a limited review page for current prediction runs, but not enough to support the verbatim product goal of all strategies across all lifecycle states.

## Section D. Actual Outcome and Join Key Map

### Outcome storage

- Actual outcomes are read from [wbc_backend/config/settings.py](wbc_backend/config/settings.py#L31-L32) via postgame_results_jsonl.
- The postgame learning path reads the latest prediction record by game_id from the prediction registry in [wbc_backend/reporting/postgame_learning.py](wbc_backend/reporting/postgame_learning.py#L14-L37).

### Join logic in use today

| Join path | Evidence | Risk |
|---|---|---|
| game_id exact match | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L360-L379) | Safe only when identifiers are perfectly aligned. |
| date and team fallback | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L379-L391) | Placeholder fallback is effectively not implemented, so real-world alias drift can still stay unmatched. |
| rendered review table | [orchestrator/mlb_result_review.py](orchestrator/mlb_result_review.py#L1127-L1140) | The current list view is built from review status and payout, not from strategy lifecycle state. |

### Lookup-key mismatch risk

The repo already contains a direct example of lookup-key fragility in [tests/test_phase29_clv_lookup_key_mismatch_fix.py](tests/test_phase29_clv_lookup_key_mismatch_fix.py#L125-L205). That test shows:

- canonical lookup can fail when identifiers differ,
- snapshot_ref fallback may be needed,
- same-snapshot guards still need to reject stale matches.

This is not the same pipeline as the replay page, but it is strong evidence that join keys and alias handling need to be explicit in the replay contract.

## Section E. Gap List Ranked by Severity

### Blocker

1. No canonical per-strategy replay history store exists in the current surface.
2. No strategy lifecycle history at time of prediction is persisted.
3. No stable replay row contract exists that can be used to render all strategies across all lifecycle states.

### Important

1. Existing prediction registry records are game-level, not strategy-level.
2. Outcome joins rely on game_id exact matching and a weak fallback that does not fully resolve alias drift.
3. There is no evidence of a preserved audit trail for lifecycle transitions.

### Nice-to-have

1. Reuse the existing table style from the historical review output so the new page feels familiar.
2. Preserve the current review_reason / failure_tags style for explainability.

## Section F. Proposed Data Contract

### Recommendation on lifecycle state

Show lifecycle_state_at_time as the primary historical truth.

Why:

- The page is historical replay, so the state that existed when the prediction was made is the correct record of intent.
- Current lifecycle state can change later and would misrepresent the row if used as the primary label.
- Current state can still be exposed as secondary metadata for filtering or admin debugging.

### Request shape

Proposed query filters:

| Field | Type | Required | Notes |
|---|---|---|---|
| strategy_id | string | no | Optional exact strategy filter. |
| lifecycle_state | string | no | Filter by lifecycle state at the time of prediction. Values should include online, offline, rejected, observation, and any future states. |
| market_type | string | no | Optional market or product family filter. |
| date_from | string (ISO date) | no | Inclusive lower bound on period date. |
| date_to | string (ISO date) | no | Inclusive upper bound on period date. |
| page | integer | no | Pagination. |
| page_size | integer | no | Pagination. |

### Response shape

Proposed response envelope:

| Field | Type | Notes |
|---|---|---|
| items | array | Page rows. |
| total | integer | Total matched rows. |
| page | integer | Current page. |
| page_size | integer | Page size. |
| filters | object | Echoed filters. |

Proposed row shape:

| Field | Type | Notes |
|---|---|---|
| period | string | The replay period identifier, such as game_id or draw key. |
| strategy_id | string | Stable strategy identifier. |
| strategy_name | string | Human-readable strategy name. |
| lifecycle_state_at_time | string | Primary historical lifecycle state. |
| current_lifecycle_state | string | Secondary metadata only. |
| market_type | string | Product or market family. |
| prediction | object | Prediction payload, ideally matching the existing historical list density. |
| actual | object | Joined actual outcome payload. |
| hit_miss | string | hit, miss, pending, or not_applicable. |
| notes | string | Join warnings, fallback notes, or validation notes. |
| source_keys | object | Optional debug metadata for join traceability. |

### Display contract recommendation

The page should visually mirror the current historical review list format, but it should be strategy-centered instead of game-centered. The minimum row should answer:

- which strategy,
- which lifecycle state it was in at prediction time,
- what it predicted,
- what actually happened,
- whether the row hit or missed,
- and what key was used to join the actual outcome.

## Section G. Open Questions for CEO Before MVP Build Starts

1. Do you want the page to show one row per strategy-period, or to group rows by strategy with expandable periods?
2. Should lifecycle_state filter use the state at prediction time only, or also allow filtering by current state?
3. Should unresolved actual outcomes appear as pending rows, or be hidden by default?
4. Is the first MVP limited to WBC, or should MLB / other products share the same contract immediately?
5. What is the canonical replay period key for this page: game_id, draw_id, or a separate replay_period_id?
6. Do you want the page to retain review_reason / notes style from the current historical review output, or keep the UI cleaner for MVP?

## Section H. What Not to Build Yet

Do not build any of the following in the MVP discovery phase:

- lifecycle editing or state transition admin UI,
- branch protection or CI changes,
- DB schema changes before contract approval,
- automatic backfill tooling without an approved backfill plan,
- replay generation or strategy mining,
- promotion or governance automation,
- multi-product expansion beyond the agreed MVP scope,
- export/download features,
- or any long-term retention / archiving policy changes.

## Section I. Exclusion Confirmation

This discovery pass stayed inside Betting-pool and did not use LotteryNew or number-pattern-research as sources.

## Can We Build the MVP With Current Data?

Short answer: not fully.

The current data surface is sufficient for a limited review-style page, but not for the stated product requirement of showing all strategies across all lifecycle states with historical prediction vs actual rows.

### Minimum backfill / reinstrument set, in priority order

1. Add a canonical per-strategy replay history record with strategy_id, strategy_name, lifecycle_state_at_time, and replay period key.
2. Persist actual outcome joins against the same replay period key, plus a stable alias / normalization table for identifier drift.
3. Preserve lifecycle transition history so rows can be rendered against the state that existed when the prediction was produced.
4. Backfill existing historical rows into the new contract only after the canonical keys are defined.

Without those steps, the page would either drop strategies, mislabel lifecycle state, or fail to join actual outcomes reliably.
