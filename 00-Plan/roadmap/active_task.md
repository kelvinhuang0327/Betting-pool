# Active Task: P203-PRED-EVIDENCE — Leakage-Safe Calibration and Feature-Ablation Walk-Forward Study

## Status

`PLAN_ONLY_REQUIRES_TASK_SPECIFIC_AUTHORIZATION`

## Supersedes

This task replaces the prior active task "P202G-NEXT-DIRECTION — Fixture-Only Roadmap and
Authorization Decision Gate" (`PLAN_ONLY_REQUIRES_TASK_SPECIFIC_AUTHORIZATION`). That task
was fully completed:

- Read-only decision packet `report/p202g_next_direction_decision_packet_20260614.md`
  produced.
- Final classification: `P202G_NEXT_DIRECTION_TRACK_A_SELECTED`.
- Primary track = `TRACK_A_PRIMARY` (weighted score 4.00/5); Track B (draft
  written-permission request) = deferred / parallel human-legal action (weighted score
  2.15/5), not sent.
- Decision confidence = MEDIUM.
- Best Track A candidate = A1 (offline leakage-safe calibration + feature-ablation
  walk-forward study on the real 2025 historical dataset).
- Latest completed phase: `P202G_NEXT_DIRECTION_TRACK_A_SELECTED`.

**Since then, the Track-A decision/governance package (5 files, including the above decision
packet) was committed, pushed, and merged via PR #24** — standard merge commit
`b32dd47fe325c8dc9de64201b24d5602b53e9ebf` (head commit
`203562c6601db26e0013e63db47dc8e706e97f16`, mergedAt `2026-06-14T04:16:06Z`). HEAD /
`origin/main` advanced from `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` to
`b32dd47fe325c8dc9de64201b24d5602b53e9ebf`. Post-merge re-validation: 257 + 90 = 347 tests
passed. Release branch `release/p202g-track-a-decision-governance` retained locally and
remotely (SHA `203562c`). Latest completed phase: `P202G_TRACK_A_PR24_MERGE_COMPLETE`.

P202G-NEXT-DIRECTION and the Track-A governance package (PR #24) are both fully closed. This
is the sole next active task. The prior packaging blocker is closed; P203 still requires its
own separate task-specific authorization before any implementation, training, calibration,
or ablation run.

## Background

The P202G-NEXT-DIRECTION decision packet found that the binding constraint on MLB
prediction-accuracy improvement is data availability for game-specific, point-in-time
features (live transport, P202G, remains HOLD). The only candidate that can produce
falsifiable predictive evidence without live data is offline leakage-safe calibration and
feature-ablation on the existing real 2025 historical dataset.

- Verified historical artifact: `data/mlb_data_loader.py::load_mlb_records()` returns
  **2,430** records, `data_source="mlb_2025_retrosheet"` (independently re-verified during
  governance alignment, 2026-06-14, and unchanged by the PR #24 merge).
- Existing offline evaluation infrastructure: `wbc_backend/evaluation/full_backtest.py`,
  `wbc_backend/evaluation/institutional_backtest.py` (walk-forward, isolation boundary,
  `assert_no_synthetic`), `wbc_backend/calibration/probability_calibrator.py`
  (Temperature/Platt/Isotonic, ECE, `calibrate_walk_forward`).
- P202D (`data/mlb_probable_starter_snapshots.py`), P202E
  (`data/mlb_probable_starter_collector.py`), and P202G-B
  (`data/mlb_pitcher_game_events.py`) remain unwired capture-format skeletons with **no
  real data**. They must not be used as, or described as, populated data sources for this
  task.

## Task Type

`IMPLEMENTATION_RESEARCH`

## Goal

Determine whether the currently authorized local historical/paper data (the 2,430-game
2025 dataset) can improve out-of-sample MLB prediction quality without restricted live
data, via chronological walk-forward calibration and feature-group ablation.

## Required Questions

1. Does calibration improve OOS Brier score or log loss?
2. Which feature groups provide positive OOS value?
3. Which feature groups reduce stability or calibration?
4. Are results stable across time segments, teams, odds bands, or confidence tiers?
5. Do results outperform a frozen baseline and a simple reference model?

## Proposed Evaluation

- Chronological train/calibration/test split, no future leakage.
- Frozen baseline vs. calibrated baseline.
- Feature-group ablations.
- Metrics: Brier score, log loss, calibration error/reliability, coverage, confidence
  intervals or bootstrap, segment stability, explicit sample count.

## Proposed Success Gate

- OOS Brier-score improvement.
- No material log-loss regression.
- Zero leakage violations.
- Gains not driven by a single small segment.
- Sufficient sample size and coverage.
- Reproducible artifacts and tests.

## Proposed Falsifiable Failure Gate

- No OOS improvement found, or gains unstable / disappear under ablation or time-split.
- This is still a complete and valuable result: it documents the proxy-feature ceiling and
  reinforces that the live game-specific data axis is the binding constraint.

## Hard Boundaries

- Only local authorized historical/paper artifacts (the 2,430-game 2025 dataset and
  existing fixtures).
- No StatsAPI / MLB live endpoint of any kind.
- No live probable-starter / pitcher-event acquisition.
- No historical backfill.
- No populated-data claim for the P202D / P202E / P202G-B skeletons.
- No provider unlock.
- No production deployment.
- No model / champion / registry promotion.
- No recommendation, evaluator, or scheduler mutation.
- No production DB write.
- No registry / `controlled_apply` mutation.
- No branch / stage / commit / push / PR authorization from this file alone. A separate
  explicit task prompt with a defined file whitelist is required for implementation.

## Decision Provenance (carried forward as reference)

| Field | Value |
|---|---|
| Decision packet | `report/p202g_next_direction_decision_packet_20260614.md` (tracked, merged via PR #24) |
| PR #24 merge | merge commit `b32dd47fe325c8dc9de64201b24d5602b53e9ebf`, head `203562c6601db26e0013e63db47dc8e706e97f16`, mergedAt `2026-06-14T04:16:06Z`, 5 files, post-merge 347 tests passed |
| Final classification | `P202G_NEXT_DIRECTION_TRACK_A_SELECTED` (governance package closed: `P202G_TRACK_A_PR24_MERGE_COMPLETE`) |
| Primary track | `TRACK_A_PRIMARY` (weighted score 4.00/5) |
| Deferred track | Track B = deferred / parallel human-legal action (weighted score 2.15/5), not sent |
| Decision confidence | MEDIUM |
| Selected candidate | A1 — offline leakage-safe calibration + feature-ablation walk-forward study |
| Verified historical sample | 2,430 games, `data_source="mlb_2025_retrosheet"` |
| Live transport (P202G) | HOLD |
| Purpose-matched MLB licensing path | `NOT_ESTABLISHED` |
| Reversal trigger | Human confirms a reachable, purpose-matched MLB data/API licensing channel exists |

## Worker Guidance

- Worker model: Opus, strong thinking level (per decision packet §15).
- Same/new conversation: new round — implementation is a separately authorized action.
- Implementation requires a separate task-specific prompt defining: exact file whitelist
  (e.g., new research script such as
  `scripts/run_p203_calibration_ablation_study.py`, a results report such as
  `report/p203_calibration_ablation_evidence_<date>.md`, optional read-only pruned-feature
  config artifact, and corresponding tests such as `tests/test_p203_*.py`); Phase 0 state
  verification; STOP conditions; and required regression scope.
