# Strategy Replay Strategy Identity Source Recovery Audit

Date: 2026-05-10
Status: Read-only recovery audit completed
Marker: P25A_STRATEGY_REPLAY_STRATEGY_IDENTITY_SOURCE_RECOVERY_AUDIT_READY

## 1. Executive Summary

The historical Strategy Replay rows do **not** expose a trustworthy source for `strategy_id` or `strategy_name` in the current workspace.

Current conclusion:
- `strategy_id` = `SOURCE_NOT_FOUND`
- `strategy_name` = `SOURCE_NOT_FOUND`
- readiness remains `BACKFILL_REQUIRED`
- UI can start = false
- production migration can start = false

The only trustworthy historical backfill proven in prior phases is `actual_result`. Strategy identity is still blocked for all 66 historical rows.

## 2. Data Sources Inspected

Read-only sources inspected for this audit:
- `00-BettingPlan/20260510/strategy_replay_gate_reconciliation_after_p23.md`
- `00-BettingPlan/20260510/strategy_replay_source_by_source_repair_plan.md`
- `00-BettingPlan/20260510/strategy_replay_historical_data_coverage_audit.md`
- `data/wbc_backend/reports/prediction_registry.jsonl`
- `data/wbc_backend/reports/postgame_results.jsonl`
- `wbc_backend/domain/schemas.py`
- `wbc_backend/reporting/prediction_registry.py`
- `wbc_backend/reporting/strategy_replay_instrumentation.py`
- `wbc_backend/reporting/strategy_replay_backfill_plan.py`
- `wbc_backend/reporting/strategy_replay_readiness.py`
- `wbc_backend/reporting/strategy_replay_history.py`
- `wbc_backend/reporting/strategy_replay_adapter.py`
- `wbc_backend/reporting/strategy_replay_backfill_review.py`
- `wbc_backend/reporting/strategy_replay_post_staging_readiness.py`

## 3. Repository Search Results

The repository contains explicit read-time strategy identity handling, but no trustworthy historical source for the 66 replay rows:

- `AnalyzeRequest` defines `strategy_id`, `strategy_name`, `lifecycle_state_at_prediction_time`, and `current_lifecycle_state` in [wbc_backend/domain/schemas.py](../../wbc_backend/domain/schemas.py).
- `prediction_registry.py` writes the request payload and decision output as-is, but the current historical registry rows do not carry strategy identity fields.
- `strategy_replay_instrumentation.py` resolves strategy identity only from explicit fields. It does not invent missing values.
- `strategy_replay_history.py`, `strategy_replay_readiness.py`, and `strategy_replay_backfill_plan.py` all treat missing `strategy_id` and missing `lifecycle_state_at_prediction_time` as blockers.
- No authoritative strategy catalog, strategy registry, or historical strategy-to-row mapping table was found.

Weak strategy-related hints were found, but they are not identity:
- `decision_report.execution_strategy` is always `SINGLE_BOOK` across the 66 rows.
- `game_output.best_bet_strategy` is empty across the 66 rows.
- `prediction.sub_model_results[].model_name` contains ensemble component names, not strategy identity.

These are not safe sources for `strategy_id` or `strategy_name`.

## 4. Historical Row Field Inventory

Live registry coverage for the 66 historical rows:

Fields present in every row:
- `recorded_at_utc`
- `game_id`
- `request`
- `teams`
- `verification`
- `deployment_gate`
- `game_output`
- `prediction`
- `simulation`
- `top_bets`
- `decision_report`
- `calibration_metrics`
- `portfolio_metrics`

Identity-related exact key counts in the registry:
- `strategy_id`: `0`
- `strategy_name`: `0`
- `lifecycle_state_at_prediction_time`: `0`
- `current_lifecycle_state`: `0`
- `source_refs`: `0`

Identity-related container fields present in every row:
- `request`: `66`
- `decision_report`: `66`
- `prediction`: `66`
- `simulation`: `66`
- `game_output`: `66`
- `deployment_gate`: `66`

Weak-hint coverage:
- `decision_report.execution_strategy`: `66` (`SINGLE_BOOK` in every row)
- `game_output.best_bet_strategy`: `66` (blank in every row)

## 5. Candidate Strategy Identity Sources

### Source-by-source repairability table

| Source | Coverage | Classification | Failure mode | Approval manifest needed |
|---|---:|---|---|---|
| `AnalyzeRequest.strategy_id` / `AnalyzeRequest.strategy_name` in `wbc_backend/domain/schemas.py` | 0/66 historical rows | `SOURCE_NOT_FOUND` | Schema exists for future writes, but historical rows do not contain these fields. | No, not for current history because there are no target values. |
| `prediction_registry.request.strategy_id` / `request.strategy_name` | 0/66 | `SOURCE_NOT_FOUND` | Request payloads in the current historical registry do not carry strategy identity. | No. |
| `prediction_registry.decision_report.strategy_id` / `decision_report.strategy_name` | 0/66 | `SOURCE_NOT_FOUND` | Decision report does not contain identity fields for the historical rows. | No. |
| `prediction_registry.prediction.strategy_id` | 0/66 | `SOURCE_NOT_FOUND` | Prediction payload does not carry strategy identity in the historical rows. | No. |
| `strategy_replay_instrumentation.resolve_strategy_identity()` | 0/66 historical recoveries | `SOURCE_NOT_FOUND` | Safe resolver exists, but it only reads explicit fields and returns missing values here. | No. |
| `decision_report.execution_strategy` | 66/66 | `UNSAFE_TO_INFER` | Always `SINGLE_BOOK`; this is execution mode, not strategy identity. | No. |
| `game_output.best_bet_strategy` | 66/66 | `UNSAFE_TO_INFER` | Blank in all rows; not identity. | No. |
| Strategy catalog / strategy registry | 0 found | `SOURCE_NOT_FOUND` | No authoritative mapping table or catalog exists in the current workspace. | No. |

### Required conclusion

`strategy_id` is `SOURCE_NOT_FOUND` for the 66 historical rows.
`strategy_name` is `SOURCE_NOT_FOUND` for the 66 historical rows.

## 6. Row-Level Candidate Summary

There is no safe per-row strategy identity candidate for any of the 66 rows.

Row group distribution in the historical registry:
- `A05`: 14 rows
- `A06`: 7 rows
- `B05`: 6 rows
- `B06`: 10 rows
- `C07`: 1 row
- `C08`: 1 row
- `C09`: 7 rows
- `D05`: 10 rows
- `D06`: 10 rows

For every row group above:
- candidate_strategy_id: none
- candidate_strategy_name: none
- source path: none
- evidence type: negative field coverage scan
- confidence: high
- repairability: `SOURCE_NOT_FOUND`
- reason: no explicit historical source exposes strategy identity

Because the same missing-field pattern applies to all 66 rows, no row-level approval manifest is meaningful at this stage.

## 7. Safe-to-Repair / Review / Unsafe Summary

- Safe to repair: `0`
- Review required: `0`
- Unsafe to infer: `0` for identity fields, because no candidate source even reaches review quality
- Source not found: `66`

Interpretation:
- Strategy identity cannot be repaired from current historical sources.
- The correct state is not “review the inferred strategy”; the correct state is “no trustworthy source exists in the workspace.”

## 8. Impact on Readiness

This audit does not change readiness.

Current readiness remains:
- `BACKFILL_REQUIRED`

Why:
- `strategy_id` remains missing for all 66 historical rows.
- `lifecycle_state_at_prediction_time` remains missing for all 66 historical rows.
- `actual_result` backfill is already proven separately, but it does not resolve the identity blockers.

## 9. UI / Production Verdict

- UI can start = false
- production migration can start = false

Reason:
- The strategy-based page cannot group or filter historical rows without `strategy_id`.
- The historical lifecycle snapshot is also still absent.
- The repository does not contain a trustworthy strategy identity source for these rows.

## 10. Recommended Next Phase

Recommended next phase: `P25E Stop Historical Repair and Instrument Future Rows Only`

Why:
- `strategy_id` is `SOURCE_NOT_FOUND` for the historical set.
- There is no trustworthy catalog or mapping table to recover it retroactively.
- Continuing historical repair work would require inventing identity, which is unsafe.
- The next useful work is to instrument future rows so `strategy_id` and `lifecycle_state_at_prediction_time` are captured at write time.

## 11. Next Worker Agent Prompt

Audit the live prediction write path and add read-only instrumentation checks that confirm future rows persist `strategy_id`, `strategy_name`, and `lifecycle_state_at_prediction_time` at prediction time, without changing historical registry files or attempting any retroactive repair.

## 12. Required Conclusions

- `strategy_id` = `SOURCE_NOT_FOUND`
- `strategy_name` = `SOURCE_NOT_FOUND`
- readiness remains `BACKFILL_REQUIRED`
- UI can start = false
- production migration can start = false

## Validation Marker

P25A_STRATEGY_REPLAY_STRATEGY_IDENTITY_SOURCE_RECOVERY_AUDIT_READY
