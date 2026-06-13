# Betting-pool Current State

**Updated:** 2026-06-13 Asia/Taipei

## Canonical Project Config

- Project: Betting-pool
- Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Branch: `main`
- Git dir: `.git`
- HEAD / `origin/main`: `cac2a748dff5077dd3b947fbacdc01dbdeec5607`
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
- **P202G-B (PR #22) merged** at `cac2a748dff5077dd3b947fbacdc01dbdeec5607` (head implementation commit `73d32c489a915a37e59c305cabb87be1ffd3d367`): fixture-only, no-network, append-only pitcher-game event backfill skeleton; `diagnostic_only=true`, `production_ready=false`.
- **P202G-A evidence packet complete** (`report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`): official MLB.com Terms of Use (2025-03-11) contains explicit automated-scripts prohibition; final classification `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`; 0 MLB data endpoint calls; 0 non-official evidence sources; StatsAPI applicability = `STRONGLY_SUPPORTED_INFERENCE` (Terms does not directly name `statsapi.mlb.com`; direct hostname naming = `NOT_ESTABLISHED`); written permission = NOT OBTAINED; purpose-matched licensing path = `NOT_ESTABLISHED`.
- **P202G-A independent adversarial review complete** (`report/p202g_a_source_policy_clarification_independent_review_20260614.md`): historical classification `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`; identified two report-level precision defects (§1 scope clause misattributed as "definition"; `legaldepartment@mlb.com` overstated as licensing entry). All decisions verified correct and conservative. Preserved as historical evidence.
- **P202G-A evidence-packet narrow fix complete**: classification `P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE`; applicability corrected to `STRONGLY_SUPPORTED_INFERENCE`; `legaldepartment@mlb.com` reclassified as DMCA/fallback; all decisions unchanged; independent review preserved as-is.
- **P202G-A governance alignment complete** (2026-06-13): exactly four governance files updated to reflect completed policy work; HEAD / staged files / open PR count unchanged.
- Latest completed phase: `P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE` (governance alignment this round).
- Open PR count: 0.
- P202G-B post-merge guardrails: P202G-B direct 119 / P202E 49 / P202D 89 / workflow 157 / combined 414 - all passed. `py_compile` + `git diff --check` PASS.
- **Full repository regression: NOT RUN.**

## Current Artifact Baseline

- Paper recommendation rows: 2 local rows under `outputs/recommendations/PAPER/2026-05-11/`.
- Outcome corpus: `data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl`.
- Evaluator: `orchestrator/mlb_paper_evaluator.py`, version `p180_evaluator_v2`.
- Strategy leaderboard: explicit `strategy_id`; missing IDs become `UNATTRIBUTED`.
- Historical paper rows predate P192 and do not contain `strategy_id`.
- P202G-B (`data/mlb_pitcher_game_events.py`, fixture-only, no-network) is **not** wired into any runtime/scheduler/evaluator/recommendation path; no real pitcher-game event data has been collected. There is no probable-starter runtime path and no live MLB endpoint call anywhere in the repo.
- Release branch `release/p202g-b-pitcher-event-backfill-skeleton` retained (local + remote, SHA `73d32c4`); not deleted.
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

## Authorized Uncommitted CTO Governance Files

The 2026-06-13 CTO update may remain uncommitted. Future read-only tasks may
proceed when the following, plus the prior-superseded read-only reports below,
are the only additional dirty/untracked files, but they must not edit or stage
them:

- `00-Plan/roadmap/roadmap.md`
- `00-Plan/roadmap/CTO-Analysis.md`
- `00-Plan/roadmap/active_task.md`
- `00-Plan/roadmap/agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md`
- `00-Plan/roadmap/agent_bootstrap/TASK_TEMPLATES.md`
- `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`
- `report/p199_paper_workflow_lineage_gap_audit_20260611.md`
- `report/p202_game_specific_prediction_source_integration_audit_20260612.md`
- `report/p202b_pregame_point_in_time_prediction_feasibility_audit_20260612.md`
- `report/p202c_point_in_time_pitcher_data_gap_evidence_contract_20260612.md`
- `report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md`
- `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`
- `report/p202g_a_source_policy_clarification_independent_review_20260614.md`

Any other dirty/untracked file is a STOP condition unless explicitly
authorized.

## Current Blockers and Risks

- Prediction runner may use fixed-prior/neutral inputs and inspected path selects home; game-specific prediction provenance is not yet proven (separate axis from the legal/live-transport axis below).
- Estimated odds are used when TSL is unavailable; they are not observed market evidence.
- Team-name/market join is incomplete in the inspected recommendation path.
- Outcome-only learning and leaderboard artifacts are not connected to an approved daily adjustment-proposal contract.
- Paper sample is too small for strategy promotion.
- Legal provider authorization and observed odds remain blockers for real use.
- Live MLB-data transport (P202G) is HOLD (P202F + P202G-A confirmed): P202G-A found an explicit automated-scripts prohibition in official MLB.com Terms of Use (2025-03-11); StatsAPI applicability = `STRONGLY_SUPPORTED_INFERENCE`; direct hostname naming = `NOT_ESTABLISHED`; no purpose-matched licensing path established (`legaldepartment@mlb.com` = DMCA/fallback only; `registrationsupport@mlb.com` = technical registration support only); one-shot and recurring both NOT AUTHORIZED. Rate-limit/no-auth/public-accessibility facts must not be read as automated-use permission.

## Current Roadmap Phase

P202G-B merged (PR #22, merge commit `cac2a748dff5077dd3b947fbacdc01dbdeec5607`). P202G-A evidence packet + independent review + narrow fix + governance alignment complete. Latest completed phase: `P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE`.

## Recommended Next Direction

Live-transport axis: **P202G-A-PACKAGE** — commit/PR packaging of exactly 6 files (4
governance files + 2 P202G-A reports). P202F is excluded. Requires a separate explicit
task prompt with branch/stage/commit/push/PR authorization. Live transport (P202G)
remains HOLD; no live endpoint, no data collection, no provider unlock is authorized.

Prediction-provenance axis (unaffected by P202G-A, separate from the above):
prediction provenance and selected-side hardening remains the leading
candidate carried from the P199 audit.

## Persistent Governance

- no DB write
- no live/paid provider call
- no production betting
- no EV/CLV/Kelly unlock
- no strategy-weight/champion auto-mutation
- no registry mutation or `controlled_apply`
- no branch/commit/push unless separately authorized
