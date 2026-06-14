# Active Task: P204-PREDICTION-PROVENANCE-HARDENING — Read-Only Pipeline Inventory (Plan-Only)

## Status

`PLAN_ONLY_REQUIRES_TASK_SPECIFIC_AUTHORIZATION`

## Supersedes

This task replaces the prior active task "P203-PACKAGE — P203 Prediction Evidence Study
Eight-File Packaging" (`IN_PROGRESS_GOVERNANCE_COMMIT_TO_PR26`). That task is now fully
complete:

- PR #26 (`release/p203-prediction-evidence-study` → `main`) is **MERGED** at merge
  commit `e7ac8f7d0672a9501aefca1dd73ad623a2941e38` (mergedAt `2026-06-14T13:45:24Z`);
  2 commits, 8 files (4 P203 evidence artifacts + 4 governance files); CI
  `replay-default-validation` = SUCCESS.
- `origin/main` confirmed to contain the merge commit; source branch
  `release/p203-prediction-evidence-study` retained (local + remote).
- P203 final classification: `P203_PRED_EVIDENCE_INCONCLUSIVE`. `calibrated_baseline`
  (frozen Elo + Platt) Brier 0.248346 is the best point estimate (CI vs frozen includes
  zero); `candidate_full` Brier 0.252568, improved 2/5 folds, **NOT promoted**.
- `tests/test_p203_prediction_evidence_study.py`: 34 passed (prior round). Regression /
  workflow / full-repository regression: NOT RUN.
- Live transport (P202G) remains HOLD; Track B unsent; purpose-matched MLB licensing
  channel = `NOT_ESTABLISHED`.
- P203 cannot, on its own, separate model limitation from data limitation; the
  point-in-time (PIT) game-specific pitcher/lineup data-availability limitation remains
  `[Inferred]`.
- This closeout round (governance-only): exactly 4 governance files
  (`roadmap.md`, `CTO-Analysis.md`, `active_task.md`,
  `agent_bootstrap/CURRENT_STATE.md`) updated to record PR #26 merge and define this
  next task. No model/source/test/data/runtime/registry/production mutation.

## Background

The P202G-NEXT-DIRECTION decision packet selected Track A (offline leakage-safe
calibration + feature-ablation walk-forward study), executed as P203
(`P203_PRED_EVIDENCE_INCONCLUSIVE`). The post-P203 CTO strategic review (`roadmap.md`
§0S / `CTO-Analysis.md` §0H) elevated **Prediction Provenance Hardening** to the lead
substantive P0: it is unblocked by the live/legal HOLD and directly serves user goal #3
(one end-to-end prediction → bet → result → learning workflow). From P199, the daily
prediction runner may use a fixed prior (~0.535), a neutral feature row, and/or a
hard-coded `home`-side fallback in the inspected path — provenance is not yet proven.

## Task Type

`PLAN_ONLY` (read-only inventory; no implementation)

## Goal

Produce a read-only inventory of the daily prediction/recommendation pipeline's
provenance, covering at minimum:

1. **Prediction producer** — which module(s) generate the per-game prediction actually
   used by the daily recommendation; whether each prediction can be traced to a
   verifiable model/version/input fingerprint, or falls back to a fixed prior / neutral
   feature row.
2. **Scheduler / runner** — how and when the prediction producer is invoked; whether
   game-specific inputs (lineups, starters, etc.) are available at that point in time.
3. **Recommendation builder** — how the prediction is mapped to a side
   (home/away/over/under) and a recommendation row; whether any hard-coded-side
   fallback exists and under what conditions it triggers.
4. **`source_trace`** — what provenance metadata (if any) is currently recorded per
   recommendation row, and whether it is sufficient to distinguish
   "verified game-specific" from "fallback/neutral/fixed-prior".
5. **`learning_eligible`** — how this flag is currently set, and whether fallback rows
   are correctly excluded from learning per P200/P201.
6. **Fixed-prior / neutral-feature / hard-coded-side-fallback usage** — enumerate every
   code path where these occur, with file/line references.

Output: a single read-only audit report (file path and naming to be defined in the
next task-specific authorization) describing current state, gaps, and a **proposed**
fail-closed / learning-ineligible contract for rows lacking verifiable game-specific
provenance. No implementation in this round.

## Hard Boundaries (this plan-only round)

- Read-only inventory and report-writing only; this `active_task.md` entry itself does
  not authorize any source/test/data/runtime/registry/production write.
- No model/champion/registry/evaluator/leaderboard/recommendation mutation.
- No MLB/StatsAPI endpoint call; no live/historical data acquisition; no provider
  unlock; live transport (P202G) remains HOLD.
- No production DB write; no deployment; no production promotion.
- No Track B written-permission request.
- Implementation of provenance hardening (code changes to the prediction producer,
  runner, recommendation builder, or `source_trace`/`learning_eligible` logic) requires
  a **separate, explicit, task-specific authorization** with its own file whitelist,
  Phase 0 state verification, STOP conditions, and required regression scope.

## Decision Provenance (carried forward as reference)

| Field | Value |
|---|---|
| P203 final classification | `P203_PRED_EVIDENCE_INCONCLUSIVE` |
| Raw/eligible sample | 2,430 games, `data_source="mlb_2025_retrosheet"` |
| Pooled OOS n | 2,010 (5 folds) |
| Brier improvement | −0.002757 (95% CI [−0.007517, 0.001864]) |
| ci95_lower_above_zero | False |
| Folds improved (candidate_full) | 2/5 improved; 3/5 did not improve |
| ECE frozen → calibrated_baseline | 0.053463 → 0.035953 (Platt calibration; NOT Brier gate) |
| ECE candidate_full | 0.035802 (separate from calibrated_baseline ECE) |
| calibrated_baseline Brier | 0.248346 (best point estimate; CI [−0.00197, 0.004735] includes zero) |
| candidate_full promotion | NOT authorized |
| PR #26 | MERGED, merge commit `e7ac8f7d0672a9501aefca1dd73ad623a2941e38` |
| Live transport (P202G) | HOLD |
| Track B | Not sent, not drafted |
| HEAD / origin/main | `e7ac8f7d0672a9501aefca1dd73ad623a2941e38` |

## Worker Guidance

- Worker model: Sonnet, standard thinking level (read-only inventory does not require
  Opus).
- This task is plan-only: no branch/stage/commit/push/PR should be created for the
  provenance inventory itself unless a separate authorization defines a report-writing
  scope.
- After the inventory/report is produced and reviewed, a separate authorization round
  will define the implementation scope, file whitelist, and regression requirements for
  actual provenance hardening.
