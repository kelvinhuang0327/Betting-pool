# Betting-pool Current State

**Updated:** 2026-06-14 Asia/Taipei

## Canonical Project Config

- Project: Betting-pool
- Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Branch: `main`
- Git dir: `.git`
- HEAD / `origin/main`: `122ba7895958157fc650b7d108676c13324fa91d` (advanced from `b32dd47fe325c8dc9de64201b24d5602b53e9ebf` via PR #25 P202G Track-A post-merge governance closeout)
- Mode: `paper_only=true`, `production_ready=false`, `NO_REAL_BET=true`
- Forbidden paths: other clones, archives, backups, quarantine, unauthorized worktrees
- Forbidden writes for governance tasks: `data/`, `runtime/`, `logs/`, `outputs/`, production/registry/DB state

## Latest Product Intent

1. Produce MLB pregame prediction strategies and paper-only recommendations mapped to Taiwan Sports Lottery bettable markets.
2. Backtest existing prediction strategies, simulate win/loss and score outcomes, and learn from prediction success.
3. Connect prediction, paper betting decision, final result, evaluation, and strategy/model improvement into one workflow.
4. Prediction-method optimization is a core priority, but only through attributable, out-of-sample, leakage-safe evidence.

## Completed Milestones

- P141-P144: daily paper recommendation and offline evaluation spine.
- P180: strategy attribution and deterministic leaderboard.
- P192: simulation strategy name propagated to recommendation `strategy_id`.
- P199: paper workflow lineage/gap audit complete (`report/p199_paper_workflow_lineage_gap_audit_20260611.md`).
- P200 (PR #18) / P201 (PR #19, merge `539bca2`): argmax side-selection + provenance; evaluator respects `learning_eligible`.
- P202 / P202B / P202C: read-only audits (`NO_TRUSTWORTHY_GAME_SPECIFIC_SOURCE`, `NO_GO_MULTIPLE_BLOCKERS`, point-in-time pitcher-data gap evidence contract).
- P202D (PR #20) / P202E (PR #21, baseline `6de072b`): fixture-only probable-starter snapshot intake + collector adapter skeletons; no live transport.
- P202F: live-transport authorization/source-policy audit complete; final classification `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`; live transport (P202G) HOLD.
- **P202G-B (PR #22)** merged at `cac2a748dff5077dd3b947fbacdc01dbdeec5607` (head implementation commit `73d32c489a915a37e59c305cabb87be1ffd3d367`): fixture-only, no-network, append-only pitcher-game event backfill skeleton; `diagnostic_only=true`, `production_ready=false`.
- **P202G-A evidence packet complete** (`report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`): official MLB.com Terms of Use (2025-03-11) contains explicit automated-scripts prohibition; final classification `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`; 0 MLB data endpoint calls; 0 non-official evidence sources; StatsAPI applicability = `STRONGLY_SUPPORTED_INFERENCE` (Terms does not directly name `statsapi.mlb.com`; direct hostname naming = `NOT_ESTABLISHED`); written permission = NOT OBTAINED; purpose-matched licensing path = `NOT_ESTABLISHED`.
- **P202G-A independent adversarial review complete** (`report/p202g_a_source_policy_clarification_independent_review_20260614.md`): historical classification `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`; identified two report-level precision defects; all decisions verified correct and conservative.
- **P202G-A evidence-packet narrow fix complete**: classification `P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE`; applicability corrected to `STRONGLY_SUPPORTED_INFERENCE`; `legaldepartment@mlb.com` reclassified as DMCA/fallback; all decisions unchanged.
- **P202G-A governance alignment complete** (2026-06-13): exactly four governance files updated.
- **P202G-A packaging complete** — **PR #23 merged** at merge commit `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` (head commit `840b0301c101dc6b9ffb5f49e254b96f96007e1a`, mergedAt `2026-06-13T15:52:48Z`). Exactly 6 authorized files (4 governance + 2 reports). P202F excluded. Source/test/config unchanged. CI `replay-default-validation` = SUCCESS.
- **Post-merge product validation**: 257 passed (`tests/test_mlb_pitcher_game_events.py` + `tests/test_mlb_probable_starter_collector.py` + `tests/test_mlb_probable_starter_snapshot_intake.py`). Governance tests: NOT RUN (no applicable direct tests). Workflow tests: NOT RUN. Full repository regression: NOT RUN.
- **Latest completed phase (superseded)**: `P202G_A_PR23_MERGE_COMPLETE`.
- **P202G-NEXT-DIRECTION complete** — read-only decision packet `report/p202g_next_direction_decision_packet_20260614.md` (now tracked, merged via PR #24). Final classification `P202G_NEXT_DIRECTION_TRACK_A_SELECTED`. Primary track = TRACK_A_PRIMARY (weighted score 4.00/5); Track B (draft written-permission request) = deferred / parallel human-legal action (weighted score 2.15/5), not sent. Decision confidence = MEDIUM. Selected candidate = A1 (offline leakage-safe calibration + feature-ablation walk-forward on the 2,430-game 2025 historical dataset, `data_source="mlb_2025_retrosheet"`, independently re-verified via `data/mlb_data_loader.py::load_mlb_records()`). P202D/E/G-B remain unwired capture-format skeletons with no real data — must not be described as populated sources. Reversal trigger = human confirms a reachable, purpose-matched MLB data/API licensing channel exists (currently `NOT_ESTABLISHED`).
- **P202G Track-A governance package merged — PR #24** at merge commit `b32dd47fe325c8dc9de64201b24d5602b53e9ebf` (head commit `203562c6601db26e0013e63db47dc8e706e97f16`, mergedAt `2026-06-14T04:16:06Z`). Exactly 5 authorized files (4 governance + 1 decision-packet report). P202G-A/P202F excluded. Source/test/config unchanged. CI `replay-default-validation` = SUCCESS. Release branch `release/p202g-track-a-decision-governance` retained locally and remotely (SHA `203562c`).
- **Post-merge product validation**: 257 passed (fixture-only subset: `tests/test_mlb_pitcher_game_events.py` + `tests/test_mlb_probable_starter_collector.py` + `tests/test_mlb_probable_starter_snapshot_intake.py`) + 90 passed (P200/P201/leaderboard subset: `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py` + `tests/test_mlb_paper_evaluator.py` + `tests/test_p180_strategy_leaderboard.py`) = **347 passed**. Governance tests: NOT RUN (no applicable direct tests). Workflow tests: NOT RUN. Full repository regression: NOT RUN.
- **P202G Track-A post-merge governance closeout — PR #25** merged at merge commit `122ba7895958157fc650b7d108676c13324fa91d` (head commit `268f846b9a76df7568c35499d932f5ef6bf3f500`). Exactly 4 governance files. CI SUCCESS.
- **P203-PRED-EVIDENCE study complete** (2026-06-14): raw/eligible sample 2,430 games (`data_source="mlb_2025_retrosheet"`); pooled OOS n=2,010; 5 chronological folds; leakage_free=True. Frozen Elo baseline Brier 0.249811; candidate_full Brier 0.252568. Primary Brier improvement (baseline − candidate) = −0.002757 (95% CI [−0.007517, 0.001864]); ci95_lower_above_zero=False; folds improved 2/5. ECE 0.053463 → 0.035802 (calibration reliability improved; NOT Brier gate). No comparison passed positive gate. Final classification `P203_PRED_EVIDENCE_INCONCLUSIVE`. candidate_full NOT promoted. Live transport HOLD unchanged. Track B unsent.
- **P203 governance alignment complete** (2026-06-14): exactly four governance files updated (roadmap.md, CTO-Analysis.md, active_task.md, CURRENT_STATE.md).
- **P203 evidence files committed** (2026-06-14): 4 P203 evidence artifacts committed at `e3416f6b4716d0ce98ff3298330bac1536becc2c` on branch `release/p203-prediction-evidence-study`; PR #26 OPEN (`release/p203-prediction-evidence-study` → `main`; 1 commit, 4 files; CI `replay-default-validation` = SUCCESS).
- **Latest completed phase**: `P203_PACKAGE_EVIDENCE_COMMITTED`; governance commit pending as second commit to PR #26.
- Open PR count: 1 (PR #26 `release/p203-prediction-evidence-study` → `main`, OPEN; evidence commit `e3416f6`; governance commit this round).

## Current Artifact Baseline

- Paper recommendation rows: 2 local rows under `outputs/recommendations/PAPER/2026-05-11/`.
- Outcome corpus: `data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl`.
- Evaluator: `orchestrator/mlb_paper_evaluator.py`, version `p180_evaluator_v2`.
- Strategy leaderboard: explicit `strategy_id`; missing IDs become `UNATTRIBUTED`.
- Historical paper rows predate P192 and do not contain `strategy_id`.
- P202G-B (`data/mlb_pitcher_game_events.py`, fixture-only, no-network) is **not** wired into any runtime/scheduler/evaluator/recommendation path; no real pitcher-game event data has been collected.
- No probable-starter runtime path. No live MLB endpoint call anywhere in the repo.
- Release branches retained: `release/p202g-a-policy-evidence-governance` (local + remote, SHA `840b030`); `release/p202g-b-pitcher-event-backfill-skeleton` (local + remote, SHA `73d32c4`); `release/p202g-track-a-decision-governance` (local + remote, SHA `203562c`).
- Full repository regression: NOT RUN.

## Tolerated Dirty Files

These background-generated files may be dirty. Do not edit, restore, clean,
stage, commit, move, or delete them without explicit authorization:

- `data/.live_cache/tsl_dedup_state.json`
- `data/derived/tsl_market_availability_state.json`
- `data/mlb_context/external_closing_state.json`
- `data/mlb_context/odds_capture_schedule.json`
- `data/mlb_context/odds_timeline.jsonl`
- `data/tsl_fetch_status.json`
- `data/tsl_odds_history.jsonl`
- `data/tsl_odds_snapshot.json`
- `logs/daemon_heartbeat.jsonl`
- `runtime/agent_orchestrator/training_memory.json`

Any dirty file outside this list is a STOP condition unless the active task
explicitly authorizes it.

## Authorized Uncommitted Governance Files

This task (P203-GOVERNANCE-PACKAGE, 2026-06-14) modifies exactly the four governance
files below as the second commit to PR #26. The remaining untracked/dirty items are
prior-superseded read-only reports/governance docs (must not be edited or staged without
explicit authorization):

- `00-Plan/roadmap/roadmap.md`
- `00-Plan/roadmap/CTO-Analysis.md`
- `00-Plan/roadmap/active_task.md`
- `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`
- `00-Plan/roadmap/agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` (untracked)
- `00-Plan/roadmap/agent_bootstrap/TASK_TEMPLATES.md` (untracked)
- `report/p199_paper_workflow_lineage_gap_audit_20260611.md`
- `report/p202_game_specific_prediction_source_integration_audit_20260612.md`
- `report/p202b_pregame_point_in_time_prediction_feasibility_audit_20260612.md`
- `report/p202c_point_in_time_pitcher_data_gap_evidence_contract_20260612.md`
- `report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md`

Note (now committed/tracked):
- `scripts/p203_prediction_evidence_study.py` — committed at `e3416f6` (PR #26 commit 1)
- `tests/test_p203_prediction_evidence_study.py` — committed at `e3416f6` (PR #26 commit 1)
- `report/p203_prediction_evidence_study_20260614.json` — committed at `e3416f6` (PR #26 commit 1)
- `report/p203_prediction_evidence_study_20260614.md` — committed at `e3416f6` (PR #26 commit 1)
- `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`,
  `report/p202g_a_source_policy_clarification_independent_review_20260614.md` (merged via PR
  #23), and `report/p202g_next_direction_decision_packet_20260614.md` (merged via PR #24) are
  **tracked and committed**.

Any other dirty/untracked file is a STOP condition unless explicitly authorized.

## Current Blockers and Risks

- Prediction runner may use fixed-prior/neutral inputs and inspected path selects home; game-specific prediction provenance is not yet proven (separate axis from the legal/live-transport axis below).
- Estimated odds are used when TSL is unavailable; they are not observed market evidence.
- Team-name/market join is incomplete in the inspected recommendation path.
- Outcome-only learning and leaderboard artifacts are not connected to an approved daily adjustment-proposal contract.
- Paper sample is too small for strategy promotion.
- Legal provider authorization and observed odds remain blockers for real use.
- P203 evidence artifacts (script, test, JSON, Markdown) committed at `e3416f6` in PR #26; governance files being added as second commit this round.
- candidate_full is INCONCLUSIVE; it is NOT promoted; ECE improvement alone does not satisfy the positive gate.
- Live MLB-data transport (P202G) is HOLD (P202F + P202G-A confirmed, PR #23 packaged; P202G-NEXT-DIRECTION Track A selected and packaged via PR #24): P202G-A found explicit automated-scripts prohibition in official MLB.com Terms of Use (2025-03-11); StatsAPI applicability = `STRONGLY_SUPPORTED_INFERENCE`; direct hostname naming = `NOT_ESTABLISHED`; no purpose-matched licensing path established (`legaldepartment@mlb.com` = DMCA/fallback only; `registrationsupport@mlb.com` = technical registration support only); one-shot and recurring both NOT AUTHORIZED. Public/no-auth/robots/rate-limit facts must not be read as automated-use permission. P203 INCONCLUSIVE result does not change this status.

## Current Roadmap Phase

PR #25 merged (merge commit `122ba7895958157fc650b7d108676c13324fa91d`). P203-PRED-EVIDENCE complete — `P203_PRED_EVIDENCE_INCONCLUSIVE`. P203 governance alignment complete. P203 evidence files committed to PR #26 at `e3416f6` (branch `release/p203-prediction-evidence-study`; CI SUCCESS). Governance files being added as second commit to PR #26 (this round). Latest completed phase: `P203_PACKAGE_EVIDENCE_COMMITTED`. After PR #26 merges (separate authorization): `P203_GOVERNANCE_PACKAGE_ADDED_TO_PR26`.

## Recommended Next Direction

**P203-GOVERNANCE-PACKAGE (this round, in progress)** — Add 4 governance files as second
commit to PR #26 (branch `release/p203-prediction-evidence-study`). candidate_full is NOT
promoted (INCONCLUSIVE). PR #26 merge requires separate authorization.

**After PR #26 merged**: pivot to **Prediction Provenance Hardening (P0 substantive)** —
replace fixed-prior / neutral / hard-coded-side fallback with verifiable game-specific
provenance or fail-closed rows. Serves user goal #3; not blocked by live data.

Track B remains deferred / parallel human-legal action; not sent, not submitted. Live
transport (P202G) remains HOLD; no live endpoint, no data collection, no provider unlock.

## Persistent Governance

- no DB write
- no live/paid provider call
- no production betting
- no EV/CLV/Kelly unlock
- no strategy-weight/champion auto-mutation
- no registry mutation or `controlled_apply`
- no branch/commit/push unless separately authorized
