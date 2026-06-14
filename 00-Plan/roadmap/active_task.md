# Active Task: P203-PACKAGE — P203 Prediction Evidence Study Eight-File Packaging

## Status

`IN_PROGRESS_GOVERNANCE_COMMIT_TO_PR26`

PR #26 OPEN (`release/p203-prediction-evidence-study` → `main`). Evidence commit
`e3416f6` (4 P203 evidence files) pushed to branch. Governance files (4 allowed files)
being added as second commit. PR final target: 2 commits, 8 files.

## Supersedes

This task replaces the prior active task "P203-PRED-EVIDENCE — Leakage-Safe Calibration and
Feature-Ablation Walk-Forward Study" (`PLAN_ONLY_REQUIRES_TASK_SPECIFIC_AUTHORIZATION`). That task
was fully completed via a separate task-specific authorization round:

- P203 prediction evidence study executed on the 2,430-game 2025 historical dataset
  (`data_source="mlb_2025_retrosheet"`); pooled OOS n=2,010 across 5 chronological folds.
- Final classification: `P203_PRED_EVIDENCE_INCONCLUSIVE`.
- Primary Brier improvement (baseline − candidate) point estimate: −0.002757; frozen Elo
  baseline Brier 0.249811; candidate_full Brier 0.252568. 95% CI: [−0.007517, 0.001864].
  CI includes zero; ci95_lower_above_zero = False. candidate_full improved 2/5 folds;
  did not improve 3/5 folds.
- Platt calibration ECE: 0.053463 (frozen_baseline) → 0.035953 (calibrated_baseline);
  candidate_full ECE: 0.035802 (separate from calibrated_baseline ECE). Calibration
  reliability improved (frozen → calibrated_baseline). Neither satisfies the Brier positive
  gate nor constitutes overall prediction quality improvement.
- No comparison passed the positive gate: ci95_lower_above_zero = False for all comparisons.
- candidate_full is **NOT** promoted; no model/champion/registry/recommendation mutation
  authorized or performed.
- Live transport (P202G) remains HOLD. Track B not sent. Purpose-matched MLB licensing
  channel = NOT_ESTABLISHED.
- Reproducibility: PASS (random seed 20260614, data fingerprints locked in JSON report).
- P203 evidence artifacts (script, test, JSON report, Markdown report) committed at
  `e3416f6` (branch `release/p203-prediction-evidence-study`, PR #26 OPEN).
- P203 governance alignment complete (prior round): exactly four governance files updated.
  Governance files being added as second commit to PR #26 (this round).
  Latest completed phase in progress: `P203_GOVERNANCE_PACKAGE_ADDED_TO_PR26` (pending).

## Background

The P202G-NEXT-DIRECTION decision packet selected Track A (offline leakage-safe calibration
+ feature-ablation walk-forward study) as primary candidate A1 (weighted score 4.00/5 vs
Track B 2.15/5, confidence MEDIUM). The P203-PRED-EVIDENCE round executed the study. The
INCONCLUSIVE result documents the proxy-feature ceiling (rolling wOBA/FIP/RSI as crude
proxies for game-specific point-in-time pitcher/lineup data). This reinforces that the live
game-specific data axis is the binding constraint on prediction accuracy.

## Task Type

`COMMIT_PR_PACKAGING`

## Goal

Package exactly 8 files — 4 updated governance files (already completed this round) plus the
4 P203 evidence artifacts (script, test, JSON report, Markdown report) — into a single
commit/PR.

## Expected Package (Exactly 8 Files)

Commit 1 — evidence (`e3416f6`, **DONE**):
5. `scripts/p203_prediction_evidence_study.py`
6. `tests/test_p203_prediction_evidence_study.py`
7. `report/p203_prediction_evidence_study_20260614.json`
8. `report/p203_prediction_evidence_study_20260614.md`

Commit 2 — governance (this round, pending):
1. `00-Plan/roadmap/roadmap.md`
2. `00-Plan/roadmap/CTO-Analysis.md`
3. `00-Plan/roadmap/active_task.md`
4. `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`

## Hard Boundaries

- Only the above 8 files; no other source, config, data, report, or governance changes.
- No model/champion/registry/evaluator/leaderboard/recommendation mutation.
- No MLB/StatsAPI endpoint call; no live/historical data acquisition; no provider unlock.
- No production DB write; no deployment; no production promotion.
- No Track B written-permission request.
- No branch/stage/commit/push/PR authorization from this file alone; a separate explicit
  task prompt with defined file whitelist, Phase 0 state verification, STOP conditions, and
  required regression scope is required.

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
| Live transport (P202G) | HOLD |
| Track B | Not sent, not drafted |
| HEAD | `122ba7895958157fc650b7d108676c13324fa91d` |

## Worker Guidance

- Worker model: Sonnet, standard thinking level.
- In progress: evidence commit e3416f6 pushed to PR #26; governance commit pending.
- After governance commit and PR body update, verify: 2 commits, 8 files in PR #26, CI
  SUCCESS, no merge. Next authorized action after this round: PR #26 merge (separate
  authorization). Then pivot to Prediction Provenance Hardening (P0 substantive).
