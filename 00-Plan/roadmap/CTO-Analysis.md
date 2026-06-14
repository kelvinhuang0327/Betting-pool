# CTO Roadmap Alignment and System Optimization Analysis

## 1. CTO Review Date

2026-06-14 Asia/Taipei

## 0F. Latest CTO Review — P202G Track-A Governance Package Merged (PR #24), P203-PRED-EVIDENCE Next

This section supersedes section `0E` (P202G-NEXT-DIRECTION decision packet, read-only) for current execution priority. **HEAD has advanced from `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` to `b32dd47fe325c8dc9de64201b24d5602b53e9ebf` via PR #24 standard merge commit** (head commit `203562c6601db26e0013e63db47dc8e706e97f16`, mergedAt `2026-06-14T04:16:06Z`).

### Completed

- [Confirmed] **PR #24 packaging complete and merged**: exactly 5 authorized files committed via standard merge commit `b32dd47fe325c8dc9de64201b24d5602b53e9ebf` (head `203562c6601db26e0013e63db47dc8e706e97f16`, mergedAt `2026-06-14T04:16:06Z`) — `00-Plan/roadmap/roadmap.md`, `00-Plan/roadmap/CTO-Analysis.md`, `00-Plan/roadmap/active_task.md`, `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`, `report/p202g_next_direction_decision_packet_20260614.md` (now tracked). P202G-A/P202F reports, source, tests, config not included. CI `replay-default-validation` = SUCCESS. Release branch `release/p202g-track-a-decision-governance` retained locally and remotely (SHA `203562c`).
- [Confirmed] **Post-merge re-validation**: 257 passed (`tests/test_mlb_pitcher_game_events.py` + `tests/test_mlb_probable_starter_collector.py` + `tests/test_mlb_probable_starter_snapshot_intake.py`) + 90 passed (`tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py` + `tests/test_mlb_paper_evaluator.py` + `tests/test_p180_strategy_leaderboard.py`) = **347 passed**, no regression. Governance tests: NOT RUN (no applicable direct tests). Workflow tests: NOT RUN. Full repository regression: NOT RUN.
- [Confirmed] **Latest completed phase**: `P202G_TRACK_A_PR24_MERGE_COMPLETE`.
- [Confirmed] **Current HEAD**: `b32dd47fe325c8dc9de64201b24d5602b53e9ebf` = `origin/main`. Open PR count: 0.
- [Confirmed] Track A primary (score 4.00), Track B deferred / parallel human-legal action (score 2.15), decision confidence MEDIUM, verified 2,430-game `mlb_2025_retrosheet` sample, and live transport HOLD all carried forward unchanged from `0E`.

### Not Completed

- [Confirmed] **P203-PRED-EVIDENCE implementation** — plan-only; requires a separate task-specific authorization round.
- [Confirmed] **Calibration result** — not produced.
- [Confirmed] **Feature-ablation result** — not produced.
- [Confirmed] **Model/champion/registry promotion** — none.
- [Confirmed] **Live MLB data acquisition** — none; live transport (P202G) remains HOLD.
- [Confirmed] **Track B submission / written-permission request** — not drafted, not sent. Purpose-matched MLB licensing channel remains `NOT_ESTABLISHED`.

### Risks

- [Confirmed] Decision confidence is **MEDIUM**, not HIGH — must not be upgraded by future tasks without new evidence.
- [Confirmed] The 2,430-row historical sample is an evaluation dataset, not proof of any prediction-quality improvement; PR #24 merge does not change this.
- [Inferred] The strongest predictive features (game-specific, point-in-time pitcher/starter data) may remain blocked by the live-data HOLD regardless of P203's outcome; A1 operates on proxy features (rolling wOBA/FIP) whose transferability to a future game-specific feature model is limited.
- [Inferred] A negative/falsifiable P203 result (no OOS Brier-skill improvement under any tested configuration) is itself valuable: it would document the current research model's ceiling under proxy features and reinforce that the live game-specific data axis is the binding constraint on prediction accuracy — this is an acceptable and complete outcome, not a failure of the task.
- [Confirmed] Live transport (P202G) remains HOLD; this merge does not change that status.

---

> **Historical (superseded by `0F`, 2026-06-14).** The section below (`0E`) reflects the state before PR #24 merged. HEAD has since advanced from `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` to `b32dd47fe325c8dc9de64201b24d5602b53e9ebf`.

## 0E. Latest CTO Review — P202G-NEXT-DIRECTION Complete (Track A Selected), P203-PRED-EVIDENCE Next

This section supersedes section `0D` (P202G-A packaging complete, PR #23 merged) for current execution priority. HEAD remains `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` (= `origin/main`); P202G-NEXT-DIRECTION was a read-only decision packet and did not change HEAD.

### Completed

- [Confirmed] P202G-NEXT-DIRECTION read-only decision packet (`report/p202g_next_direction_decision_packet_20260614.md`, untracked) produced. Final classification `P202G_NEXT_DIRECTION_TRACK_A_SELECTED`.
- [Confirmed] Technical capability mapping covering: recommendation path (P200 argmax side-selection; prediction source still `neutral_fixed_prior`), learning-eligibility gating (P201), fixture-only P202D/E/G-B skeletons (unwired, no real data), and offline evaluation capability (walk-forward backtest, calibration, paper evaluator).
- [Confirmed] Track A vs Track B weighted decision matrix produced (7 criteria, 0-5 scale, weights summing to 100%). Track A (best candidate A1) = 4.00 / 5. Track B (deferred written-permission draft) = 2.15 / 5.
- [Confirmed] Track A selected as primary; Track B classified as deferred / parallel human-legal action (not rejected).
- [Confirmed] Best Track A candidate A1 — offline leakage-safe calibration + feature-ablation walk-forward study on the real 2025 historical dataset — selected from 5 candidates (A2/A3 retained as non-predictive runner-ups; A4/A5 rejected as unwired skeleton / data-blocked).
- [Confirmed] This round independently re-verified `data/mlb_data_loader.py::load_mlb_records()` returns 2,430 records with `data_source="mlb_2025_retrosheet"`.
- [Confirmed] This round reran `tests/test_mlb_pitcher_game_events.py` + `tests/test_mlb_probable_starter_collector.py` + `tests/test_mlb_probable_starter_snapshot_intake.py` = 257 passed, and `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py` + `tests/test_mlb_paper_evaluator.py` + `tests/test_p180_strategy_leaderboard.py` = 90 passed.
- [Confirmed] Governance alignment for this decision: exactly four governance files updated (`roadmap.md`, `CTO-Analysis.md`, `active_task.md`, `agent_bootstrap/CURRENT_STATE.md`); `active_task.md` replaced with sole task `P203-PRED-EVIDENCE` (plan-only).

### Not Completed

- [Confirmed] **P203-PRED-EVIDENCE implementation** — plan-only; requires a separate task-specific authorization round.
- [Confirmed] **Calibration result** — not produced.
- [Confirmed] **Feature-ablation result** — not produced.
- [Confirmed] **Model/champion/registry promotion** — none.
- [Confirmed] **Live MLB data acquisition** — none; live transport (P202G) remains HOLD.
- [Confirmed] **Track B submission / written-permission request** — not drafted, not sent. Purpose-matched MLB licensing channel remains `NOT_ESTABLISHED`.

### Risks

- [Confirmed] Decision confidence is **MEDIUM**, not HIGH — must not be upgraded by future tasks without new evidence.
- [Inferred] The strongest predictive features (game-specific, point-in-time pitcher/starter data) may remain blocked by the live-data HOLD regardless of P203's outcome; A1 operates on proxy features (rolling wOBA/FIP) whose transferability to a future game-specific feature model is limited.
- [Inferred] A negative/falsifiable P203 result (no OOS Brier-skill improvement under any tested configuration) is itself valuable: it would document the current research model's ceiling under proxy features and reinforce that the live game-specific data axis is the binding constraint on prediction accuracy — this is an acceptable and complete outcome, not a failure of the task.

---

## 0D. Latest CTO Review — P202G-A Packaging Complete (PR #23 Merged), Direction Gate Next

> **Historical (superseded by `0E`, 2026-06-14).** P202G-NEXT-DIRECTION completed; Track A selected (`P202G_NEXT_DIRECTION_TRACK_A_SELECTED`). Next task is P203-PRED-EVIDENCE (plan-only). See section `0E` for current execution priority.

This section supersedes section `0C` (P202G-A evidence/governance alignment, 2026-06-13) for current execution priority. HEAD has advanced from `cac2a748dff5077dd3b947fbacdc01dbdeec5607` to `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` via PR #23 standard merge commit.

### Completed (verified)

- [Confirmed] **P202G-A evidence packet complete** (`report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`): official MLB.com Terms of Use (2025-03-11) contains explicit automated-scripts prohibition. Final classification: `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`. 0 MLB data endpoint calls; 0 non-official evidence sources.
- [Confirmed] **Independent adversarial review complete** (`report/p202g_a_source_policy_clarification_independent_review_20260614.md`): historical classification `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`. Identified two report-level precision defects; all decisions verified correct and conservative. Preserved as historical evidence.
- [Confirmed] **Evidence-packet narrow fix complete** (`P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE`): applicability corrected to `STRONGLY_SUPPORTED_INFERENCE`; `legaldepartment@mlb.com` reclassified as DMCA/fallback (Terms §2 "Copyright Agent"). No decisions changed.
- [Confirmed] **Governance alignment complete** (2026-06-13): exactly four governance files updated.
- [Confirmed] **PR #23 packaging complete**: exactly 6 files (4 governance + 2 reports) committed and merged via standard merge commit. Merge commit `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e`, head `840b0301c101dc6b9ffb5f49e254b96f96007e1a`, mergedAt `2026-06-13T15:52:48Z`. CI `replay-default-validation` = COMPLETED / SUCCESS. P202F excluded. No source/test/config.
- [Confirmed] **Post-merge product validation**: 257 passed. Governance tests: NOT RUN (no applicable direct tests). Workflow tests: NOT RUN. Full repository regression: NOT RUN.
- [Confirmed] **Latest completed phase**: `P202G_A_PR23_MERGE_COMPLETE`.
- [Confirmed] **Current HEAD**: `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` = `origin/main`.

### Not Completed (must not be claimed as done)

- [Confirmed] **Written permission from MLB** — not obtained; no licensing agreement established.
- [Confirmed] **Purpose-matched authorization path** — `NOT_ESTABLISHED`; `legaldepartment@mlb.com` = DMCA/fallback only (Terms §2 "Copyright Agent"), not a licensing office; `registrationsupport@mlb.com` = technical registration support only; StatsAPI self-registration = account entry, not usage license.
- [Confirmed] **StatsAPI automated-use authorization** — NOT AUTHORIZED; Terms does not directly name `statsapi.mlb.com` (direct hostname naming = `NOT_ESTABLISHED`); applicability is `STRONGLY_SUPPORTED_INFERENCE` — sufficient to maintain HOLD, not a direct contractual citation.
- [Confirmed] **Live one-shot dry run** — NOT AUTHORIZED.
- [Confirmed] **Recurring collector** — NOT AUTHORIZED.
- [Confirmed] **Real historical backfill** — NOT AUTHORIZED.
- [Confirmed] **Live provider unlock** — NOT AUTHORIZED.
- [Confirmed] **Model/feature integration based on live MLB data** — not unlocked; `diagnostic_only=true`, `production_ready=false` maintained.

### Live-Transport Blocker Status

- [Confirmed] Single remaining blocker for live-transport axis = **official written authorization from a purpose-matched MLB data/API licensing channel** (none identified as of this evidence round). Live transport (P202G) remains **HOLD**.
- [Confirmed] Minimum allowed technical boundary is **fixture-only** (consistent with P202D/P202E/P202G-B).
- [Confirmed] Public/no-auth/robots-404 facts and rate-limit information are **not** permission. Must never be read as automated-use authorization.

### Next Recommended Direction

1. **P202G-NEXT-DIRECTION**: Read-only decision memo selecting next project direction — Track A (continue fixture-only/paper prediction work without live transport) or Track B (prepare draft written-permission request without sending). Requires a separate explicit task prompt. P202G remains HOLD.
2. The prediction-provenance-axis P0 (game-specific prediction inputs / selected-side hardening) remains open and is a separate axis from the legal/live-transport axis.

---

## 0C. Latest CTO Review — P202G-A Evidence Policy Complete, Governance Alignment, Packaging Next

> **Historical (superseded by `0D`, 2026-06-14).** PR #23 packaging was completed (merge commit `96c67c1`, merged 2026-06-13T15:52:48Z). HEAD has advanced to `96c67c1`. See section `0D` for current execution priority.

This section supersedes section `0B` (P202G-B merge closeout + P202G-A-next, 2026-06-13) for current execution priority. HEAD remains `cac2a748dff5077dd3b947fbacdc01dbdeec5607`; this round is policy/report/governance only — no source, test, or runtime changes.

### Completed (verified)

- [Confirmed] **P202G-A evidence packet complete** (`report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`): official MLB.com Terms of Use (2025-03-11) contains an explicit automated-scripts prohibition: "use automated scripts to collect information from or otherwise interact with the MLB Digital Properties." Final classification: `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`. 0 MLB data endpoint calls; 0 non-official evidence sources.
- [Confirmed] **Independent adversarial review complete** (`report/p202g_a_source_policy_clarification_independent_review_20260614.md`): historical classification `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`. Identified two report-level precision defects: (1) §1 scope clause misattributed as the formal "MLB Digital Properties definition"; (2) `legaldepartment@mlb.com` overstated as a licensing entry. All decisions verified correct and conservative. Independent review preserved as historical evidence of the original defect finding.
- [Confirmed] **Evidence-packet narrow fix complete** (`P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE`): applicability updated to `STRONGLY_SUPPORTED_INFERENCE`; `legaldepartment@mlb.com` reclassified as DMCA/fallback (Terms §2 "Copyright Agent"). No decisions changed. Independent review preserved as-is.
- [Confirmed] **P202G-A governance alignment complete** (this round): exactly four governance files updated; HEAD / staged files / open PR count unchanged.

### Not Completed (must not be claimed as done)

- [Confirmed] **Written permission from MLB** — no applicable written permission obtained; no licensing agreement established.
- [Confirmed] **Purpose-matched authorization path** — `NOT_ESTABLISHED`; `legaldepartment@mlb.com` is DMCA/fallback only (Terms §2 "Copyright Agent"), not a licensing office; `registrationsupport@mlb.com` is technical registration support only; StatsAPI self-registration is account entry, not usage license.
- [Confirmed] **StatsAPI automated-use authorization** — NOT AUTHORIZED; Terms does not directly name `statsapi.mlb.com` (direct hostname naming = `NOT_ESTABLISHED`); applicability is `STRONGLY_SUPPORTED_INFERENCE` only (§1 scope clause + formal definition + openapi "Official API for MLB" identity — sufficient to maintain HOLD, not a direct contractual citation).
- [Confirmed] **Live one-shot dry run** — NOT AUTHORIZED.
- [Confirmed] **Recurring collector** — NOT AUTHORIZED.
- [Confirmed] **Real historical backfill** — NOT AUTHORIZED.
- [Confirmed] **Live provider unlock** — NOT AUTHORIZED.
- [Confirmed] **Model/feature integration based on live MLB data** — not unlocked; `diagnostic_only=true`, `production_ready=false` maintained.

### Live-Transport Blocker Status

- [Confirmed] Single remaining blocker for live-transport axis = **official written authorization from a purpose-matched MLB data/API licensing channel** (none identified as of this evidence round). Live transport (P202G) remains **HOLD**.
- [Confirmed] The minimum allowed technical boundary is **fixture-only** (consistent with P202D/P202E/P202G-B).

### Next Recommended Direction

1. **P202G-A-PACKAGE**: Package exactly 6 files (4 governance + 2 P202G-A reports) into a commit/PR. Requires a separate explicit task prompt with branch/stage/commit/push/PR authorization. P202F is excluded from this package. The 6-file list: `00-Plan/roadmap/roadmap.md`, `00-Plan/roadmap/CTO-Analysis.md`, `00-Plan/roadmap/active_task.md`, `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`, `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`, `report/p202g_a_source_policy_clarification_independent_review_20260614.md`.
2. The prediction-provenance-axis P0 (game-specific prediction inputs / selected-side hardening) remains open and is a separate axis from the legal/live-transport axis.

---

## 0B. Latest CTO Review - P202G-B Merge Closeout, Live Transport HOLD, P202G-A Next

> **Historical (superseded by `0C`, 2026-06-13).** P202G-A evidence packet, independent adversarial review, evidence-packet narrow fix, and governance alignment have since been completed. See section `0C` for current execution priority.

This section supersedes section `0A` (and the older P140/P121 analysis below it) for current execution priority. Section `0A` reflected the post-P192 state at HEAD `9a0ddc2`/`539bca2`; HEAD has since advanced through P200 (PR #18), P201 (PR #19), P202D (PR #20), P202E (PR #21), a P202F live-transport audit, and P202G-B (PR #22, merged) to `cac2a748dff5077dd3b947fbacdc01dbdeec5607`.

### Input Sources

- [Confirmed] Actual git state: local `main` = `origin/main` = `cac2a748dff5077dd3b947fbacdc01dbdeec5607`; PR #22 state = MERGED (merge commit `cac2a74...`, head `73d32c489a915a37e59c305cabb87be1ffd3d367`, base `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9`); open PR count = 0.
- [Confirmed] `report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md` (final classification `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`).
- [Confirmed] `report/p202g_b_pitcher_event_backfill_skeleton_20260614.md`, `report/p202g_b_post_implementation_review_20260614.md`, `report/p202g_b_stable_revision_identity_fix_review_20260614.md`, `report/p202g_b_cross_provider_identity_fix_review_20260614.md` (final classification `P202G_B_CROSS_PROVIDER_REREVIEW_READY_FOR_COMMIT_PACKAGING`, now packaged and merged).
- [Confirmed] `data/mlb_pitcher_game_events.py` and `tests/test_mlb_pitcher_game_events.py` (119 tests).

### Completed (verified)

- [Confirmed] **P202E merged** (PR #21, baseline `6de072b`): fixture-only probable-starter collector adapter; no live transport, no runtime path.
- [Confirmed] **P202F audit complete**: live-transport (P202G) authorization and source-policy audit finished; classification `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`; the MLB StatsAPI schedule endpoint is technically suitable but lacks written legal authorization for automated/derived use.
- [Confirmed] **P202G-B merged** (PR #22, merge commit `cac2a748dff5077dd3b947fbacdc01dbdeec5607`): fixture-only, no-network pitcher-game event backfill skeleton. Resolved two structural blockers during review iterations:
  1. Reordered-pitcher-list revision identity - fixed by making logical identity `(game_pk, pitcher_id)` and `source_record_id = "<game_pk>:pitcher:<pitcher_id>"` stable across reorder; `appearance_sequence` is observed-order metadata only and no longer splits revision history.
  2. Cross-provider/feed silent overwrite - fixed by introducing `source_lineage_key = (source_provider, source_endpoint_or_feed_id)`; any logical event observed across more than one eligible lineage fails closed as `ambiguous_cross_source_lineage` (no latest-wins/precedence/voting/silent-dedup, even for identical content).
- [Confirmed] Post-merge guardrails: P202G-B direct 119 / P202E 49 / P202D 89 / workflow 157 / combined 414 all passed; `py_compile` and `git diff --check` PASS. **Full repository regression: NOT RUN.**
- [Confirmed] Release branch `release/p202g-b-pitcher-event-backfill-skeleton` retained (local + remote).

### Not Completed (must not be claimed as done)

- [Confirmed] **Live transport authorization** - still HOLD. No written official MLB source-policy clarification exists yet.
- [Confirmed] **Actual MLB endpoint collection** - no automated collection, transport code, or runtime data write has been implemented or authorized.
- [Confirmed] **Real historical pitcher-event backfill** - P202G-B operates on local JSON fixtures only; no real historical pitcher-game event data has been collected or backfilled. Any post-hoc row is observational only and is not historical-PIT evidence before its actual `collected_at`.
- [Confirmed] **Model/feature integration** - P202G-B is not wired into the scheduler, evaluator, recommendation pipeline, or any model/feature set.
- [Confirmed] **Production recommendation use** - `diagnostic_only=true`, `production_ready=false` remain enforced; P202G-B must not be described as live-ready, production-ready, or historical-PIT-ready.

### Remaining Live-Transport Blocker

- [Confirmed] Single remaining blocker for the live-transport axis = **official written source-policy clarification** (authorization, retention, derived-use, redistribution, and contact mechanism for the MLB StatsAPI schedule source). The next step, **P202G-A**, is a **read-only evidence-gathering task** (not an implementation task) that must not call any MLB endpoint. Live transport (P202G) remains **HOLD** until P202G-A evidence is gathered and separately reviewed.

### Next Recommended Direction

1. P202G-A: Source Policy Clarification Evidence Packet - read-only, no endpoint calls, produces a future evidence report (not created in this round).
2. The prediction-provenance-axis P0 (game-specific prediction inputs / selected-side hardening, carried from prior CTO updates) remains open and is a separate axis from the legal/live-transport axis; P202G-A does not change its priority.

---

## 0A. Latest CTO Review - P192 Post-Merge Closed-Loop Realignment

> **Historical (superseded by `0B`, 2026-06-13).** HEAD has since advanced through P200/P201/P202D/P202E/P202G-B to `cac2a74`. The section below is retained as historical context only.

This section supersedes the older P140/P121 analysis below for current execution priority.

### Input Sources

- [Confirmed] User-provided P192-P198 engineering handoff.
- [Confirmed] User product direction: MLB pregame TSL-market predictions/recommendations, strategy backtesting/score simulation/learning, and one prediction + betting + result workflow.
- [Confirmed] `roadmap.md`, `active_task.md`, `CEO-Decision.md`, root bootstrap files, current git state, recent commit history, and P141/P142/P143/P180/P192 source/tests/artifacts.
- [Confirmed] `scripts/run_mlb_tsl_paper_recommendation.py`, `orchestrator/mlb_paper_evaluator.py`, `orchestrator/mlb_daily_scheduler.py`, `orchestrator/mlb_result_review.py`, and related tests.
- [Confirmed] P102/P103/P106 outcome-only backtest, learning, score-simulation, and adjustment artifacts.
- [Confirmed] Targeted guard run: 124 tests passed across recommendation, evaluator, scheduler, and strategy leaderboard suites.

### Completed Work Assessment

- [Confirmed] P141-P144 established opt-in daily paper recommendation and offline result evaluation with idempotent pending/final behavior.
- [Confirmed] P180 added explicit `strategy_id` segmentation and deterministic strategy leaderboard metrics.
- [Confirmed] P192 propagated loaded simulation `strategy_name` into recommendation `strategy_id`.
- [Confirmed] PR #16 and PR #17 merged; local `main` equals `origin/main`; open PR count is 0.
- [Confirmed] Active implementation state is idle: `NEXT_TASK_NOT_DEFINED_AFTER_P192_MERGE`.
- [Confirmed] At Phase 0 preflight, no staged or untracked files existed and the 10 dirty files exactly matched the tolerated daemon/runtime/data list. This CTO update subsequently added only the six authorized governance-file changes.

### Roadmap Alignment Assessment

| Tag | Finding |
|---|---|
| [Aligned] | Strategy attribution now supports measuring which simulation strategy produced a recommendation. |
| [Aligned] | The scheduler/evaluator spine supports the user's desired paper-only workflow shape. |
| [Drift] | Existing roadmap priority was still P140 dirty-tree policy even though the project reached P192 and the dirty list is now governed. |
| [Drift] | Attribution/governance maturity is ahead of prediction quality and market provenance. |
| [Missing] | There is no single lineage contract linking game-specific prediction inputs, selected side, observed market row, recommendation, final outcome, strategy metrics, and an adjustment proposal. |
| [Missing] | No daily learning contract consumes P180 leaderboard evidence to propose prediction-method changes under review. |
| [Outdated] | More leaderboard continuation is not the highest-value next task after P192. |
| [Blocked] | Real betting, production recommendations, and trustworthy market-edge claims remain blocked by legal provider authorization and observed odds evidence. |

### Unfinished Work Assessment

| Item | Status |
|---|---|
| Game-specific prediction provenance | [Risk] Runner may use a fixed 0.535 prior or neutral feature row and writes the inspected recommendation side as home. |
| TSL observed market provenance | [Blocked] Current sample rows use estimated odds because TSL was unavailable; team-name join is noted as incomplete. |
| End-to-end lineage | [Missing] IDs and source fingerprints across prediction, recommendation, outcome, and learning are not proven in one contract. |
| Outcome freshness | [Risk] Evaluation reads a local outcome corpus; freshness and automated pending-to-final lifecycle need explicit audit. |
| Strategy learning integration | [Missing] Leaderboard is descriptive and intentionally does not mutate weights; no human-reviewed adjustment proposal contract is connected. |
| Statistical evidence | [Data limited] Local paper recommendation corpus has two rows from one date; historical strategy attribution is absent. |
| Full regression | [Unknown] Targeted workflow tests pass; full repository regression was not run. |

### P0 / P1 / P2 / P3-P10 Reprioritization

| Priority | Direction | CTO judgment |
|---:|---|---|
| **P0** | P199 Paper Workflow Lineage and Gap Audit | Select one smallest implementation gap based on actual data lineage, not another broad phase burst. |
| **P0 blocker** | Prediction Provenance Truth | Prediction optimization cannot learn honestly if recommendation rows are generated from fallback/neutral inputs without explicit provenance. |
| **P1** | Result-to-Strategy Learning Contract | Convert evaluation evidence into reviewable adjustment proposals with sample/stability/calibration gates and no automatic mutation. |
| **P1** | TSL Market Mapping and Settlement Contract | Required to turn model outputs into valid market-specific paper decisions. |
| **P1** | Outcome Freshness and Join Integrity | Required for correct feedback and deterministic re-evaluation. |
| **P2** | Multi-strategy OOS Backtest and Score Simulation | Compare methods only after lineage and common evaluation contracts are stable. |
| **P2** | Targeted + Full Regression Policy | Broaden tests when the selected implementation crosses prediction/recommendation/outcome modules. |
| **P3** | Legal Provider / Observed Odds Evidence | True blocker for real market-edge and production use, but not for offline paper workflow design. |
| **P4-P6** | Prediction model optimization | Features/calibration/ensemble/score simulation candidates must enter through OOS gates and the feedback loop. |
| **P7-P10** | Production proposal | Remains blocked until all product, legal, risk, monitoring, and approval gates pass. |

### Critical Blockers

1. **Prediction provenance ambiguity**
   Impact: prediction correctness, strategy attribution, learning validity.
   Risk: the system could optimize strategy labels around recommendations that were not produced by game-specific model evidence.
   Acceptance: recommendation rows carry prediction/model/input identity and explicit side-selection rationale; fallback rows fail closed or remain clearly blocked.

2. **Observed market data and mapping gap**
   Impact: TSL recommendations, market comparison, settlement.
   Risk: estimated odds may be mistaken for observed market evidence.
   Acceptance: observed/estimated values are structurally distinct; supported markets and joins are deterministic; missing data blocks edge/stake.

3. **Result-to-learning disconnect**
   Impact: the user's final closed-loop goal.
   Risk: leaderboard metrics remain reporting-only and never produce a disciplined model-improvement decision.
   Acceptance: an offline proposal contract uses sample size, hit rate, Brier/ECE, temporal stability, and rollback criteria; no automatic weight changes.

4. **Sample limitation**
   Impact: strategy comparison confidence.
   Risk: two paper rows can produce impressive but meaningless leaderboard metrics.
   Acceptance: all rankings preserve `DATA_LIMITED` and promotion gates require a predefined sample/stability threshold.

### Recommended System Optimization Directions

1. **P199 workflow lineage audit (P0)**
   Build the source-to-artifact matrix and select one implementation gap. This prevents a large multi-module rewrite.

2. **Prediction provenance hardening (P0/P1 candidate)**
   Replace ambiguous fallback/neutral prediction lineage with explicit game-specific prediction evidence or a blocked fallback state.

3. **Result-to-learning proposal contract (P1)**
   Produce human-reviewable strategy adjustments without automatically changing weights or champion state.

4. **TSL market and settlement mapping (P1)**
   Separate observed odds from estimates and define supported market semantics.

5. **OOS strategy comparison cadence (P2)**
   Compare prediction methods on identical games and outcomes using calibration and temporal stability, not hit rate alone.

### Roadmap Changes Applied

- Added roadmap section `0L` for post-P192 closed-loop realignment.
- Replaced the idle active task with a single P199 audit task.
- Added canonical bootstrap files under `00-Plan/roadmap/agent_bootstrap/`.
- Made prediction optimization an explicit requirement inside the feedback workflow.
- Deferred further leaderboard enhancement until prediction/market/outcome lineage is verified.

### Risks / Unknowns

- [Unknown] Whether the daily prediction runner has another game-specific source not visible in the inspected path.
- [Unknown] Whether current daemon jobs refresh the P84E outcome corpus frequently enough for daily evaluation.
- [Risk] Existing paper recommendation rows predate P192 and remain unattributed.
- [Risk] The repository contains multiple legacy learning systems; P199 must not merge them without proving ownership and schema compatibility.
- [Confirmed] Full repository regression remains NOT RUN.

### CTO Final Recommendation

Authorize P199 as a read-only/plan-only audit. Its output must choose exactly one next implementation. Based on current evidence, prediction provenance hardening is the leading candidate because no downstream learning system can improve prediction methods reliably until each recommendation proves which game-specific prediction and side-selection logic produced it.

### CTO Summary

1. P141-P144 built the paper recommendation/evaluation spine.
2. P180/P192 completed explicit strategy attribution.
3. The main gap is now closed-loop lineage and prediction provenance, not leaderboard features.
4. Real betting remains blocked; paper-only workflow improvement can continue offline.
5. Execute P199, then implement only its single selected gap.

Final classification: `CTO_ROADMAP_UPDATED_WITH_RISKS`

## 0. Latest CTO Addendum - P140 Post-Merge Product Intent

This addendum supersedes the older P121-oriented analysis below for current execution priority while preserving the older sections as historical context.

### Current Observed State

- [Confirmed] Canonical repo is `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`.
- [Confirmed] Current branch is `main`; git-dir is `.git`.
- [Confirmed] Local `main` and `origin/main` are both `9a0ddc205b3f6b6cb4499dc214391bd4d886db2d`.
- [Confirmed] PR #4 merged P122-P140 through the protected-branch PR workflow after required CI passed.
- [Confirmed] Current user direction defines two product lanes: MLB pregame market advisory for Taiwan Sports Lottery bettable markets, and strategy backtest / score simulation / learning based on prediction success.
- [Confirmed] Worktree remains dirty with 97 status entries observed in this review: 86 modified paths and 11 untracked paths.
- [Confirmed from handoff] Targeted P118-P140 tests passed and PR CI passed.
- [Confirmed] Full repository regression remains NOT RUN.
- [Confirmed] No real betting, real recommendation, production deployment, stake/profit/Kelly deployment, live odds use, or provider unlock is authorized.

### Product Intent Assessment

| Lane | Assessment |
|---|---|
| Lane A: MLB pregame Taiwan Sports Lottery market advisory | [Aligned] This is the project-facing product lane. It should produce paper-only strategy/recommendation candidates by market, but must remain blocked for real use until legal provider authorization, lawful odds/source trace, market availability, edge validation, risk controls, and explicit approval exist. |
| Lane B: strategy backtest / simulation / learning | [Aligned] This is the model-learning lane. It should evaluate existing predictions and strategies using outcome backtests, simulated score distributions, replay/drift checks, and learning matrices; it should adjust strategy weights only inside diagnostic/paper-only governance until coverage and approvals mature. |

### Roadmap Alignment Assessment

| Tag | Finding |
|---|---|
| [Aligned] | P122-P140 strengthened governance around provider/legal evidence, replay consistency, drift alerting, escalation, and signoff evidence. |
| [Aligned] | The user's two-lane product intent matches the earlier P101 split, but it is now more concrete: Taiwan Sports Lottery bettable markets plus backtest/simulation/learning. |
| [Drift] | Existing roadmap/CTO sections still centered on P121/P122 readiness, while actual HEAD is P140 merged through PR #4. |
| [Drift] | Active task history records P140 completion, but the next actionable task is not P141 yet; dirty-tree classification should happen first. |
| [Missing] | The repo lacks a current dirty-tree classification policy after PR #4 merge. |
| [Missing] | The repo lacks a single current product-intent lock that every future task can cite. |
| [Blocked] | Real odds, EV/CLV, Kelly, real recommendations, and production remain blocked by provider/legal/data/evidence gates. |

### Recommended P0 / P1 Reprioritization

| Priority | Recommendation | Reason |
|---:|---|---|
| **P0** | Dirty Tree Cleanup Policy / Classification Plan | The repo is correctly on `main` and synced, but 97 dirty/untracked entries make the next implementation unsafe without path-by-path classification. |
| **P0** | Product Intent Lock | Future agents need the two-lane product goal stated as canonical context so they do not continue governance-only phase growth detached from the product. |
| **P1** | Lane A Market Advisory Architecture Review | The system should map Taiwan Sports Lottery bettable markets to prediction inputs, legal odds/source fields, recommendation-row contracts, and blocked/allowed states. |
| **P1** | Lane B Backtest / Simulation Learning Contract | Existing outcome-only artifacts should become a coherent learning loop with strategy identity, simulated scores, success metrics, drift triggers, and adjustment rules. |
| **P1** | Bootstrap / Task Template Location Decision | Untracked bootstrap files exist at `00-Plan/roadmap/`; the prompt template expected `00-Plan/roadmap/agent_bootstrap/`. This should be resolved before scaling worker handoffs. |

### Immediate Recommendation

Run a read-only **Dirty Tree Cleanup Policy / Classification Plan After PR #4 Merge** before P141. The task should classify every modified/untracked path into runtime/cache/generated, roadmap/governance, report/data output, probe script, candidate keep, candidate restore, candidate ignore, or requires-human-decision. It must not restore, delete, stash, stage, commit, push, switch branches, or create a PR.

Final classification for this addendum:

`CTO_ROADMAP_PRODUCT_INTENT_REALIGNED_DIRTY_TREE_POLICY_NEXT`

> ⚠️ **歷史段落界線（2026-06-03 校註）**：以下 §2–§13 為 **P121 期**撰寫的歷史分析（內文的 `HEAD=70623ed`/P121、dirty 計數、`roadmap 0I` 等均為當時狀態）。**實際 HEAD 已為 P140（`9a0ddc2`）**。當前執行優先序以上方 **§0 P140 Addendum** ＋ `roadmap.md` §0K ＋ `git HEAD` 為準；以下保留僅作歷史脈絡，請勿據此判斷現況階段。

## 2. Input Sources

Read / referenced:

- [Confirmed] User-provided handoff text at `/Users/kelvin/.codex/attachments/b07f65cb-3e8b-4c20-b38d-05a7c8b19141/pasted-text.txt`.
- [Confirmed] `00-Plan/roadmap/roadmap.md`.
- [Confirmed] Previous `00-Plan/roadmap/CTO-Analysis.md`.
- [Confirmed] `00-Plan/roadmap/active_task.md` read-only; current visible state records P120/P121 completion and "next step:待指示".
- [Confirmed] `00-Plan/roadmap/CEO-Decision.md` read-only; current decision is post-P93/P94 and does not cover P101-P121.
- [Confirmed] `git log --oneline -35`; HEAD is `70623ed feat(P121): Provider Authorization Evidence Placeholder - P121_PROVIDER_AUTHORIZATION_EVIDENCE_PLACEHOLDER_READY_WITH_BLOCKERS`.
- [Confirmed] `git status --short`; worktree is dirty, observed count 95 entries during this CTO review.
- [Confirmed] P94-P100 summary files under `data/mlb_2026/derived/`, including P94 high-FIP qualification through P100 wait-state no-op.
- [Confirmed] P101-P121 reports under `report/*_20260531.md`.
- [Confirmed] P101-P121 summaries under `data/mlb_2026/derived/*_summary.json`.
- [Confirmed] P101-P121 test file inventory under `tests/test_p10*_*.py`, `tests/test_p11*_*.py`, `tests/test_p12*_*.py`.
- [Confirmed] P121 report states P121 dedicated tests and P120 dedicated tests passed.
- [Confirmed] P121 summary states `authorization_evidence_present=false`, `provider_approved=false`, and all provider / market authorization remains `BLOCKED`.

Not performed:

- [Confirmed] No development implementation.
- [Confirmed] No pytest or full regression rerun in this CTO review.
- [Confirmed] No new repo, branch, worktree, clone, checkout, merge, commit, push, PR, daemon restart, scheduler change, crawler change, live API call, paid API call, registry write, production write, or data artifact write.
- [Confirmed] No `.env` or secret read.
- [Confirmed] No write to `active_task.md` because CTO write scope excludes it.
- [Confirmed] No write to `CEO-Decision.md` because CTO write scope excludes it.
- [Confirmed] No new worker task prompt emitted because the strict instruction forbids new worker task prompts and limits CTO writes to `roadmap.md` / `CTO-Analysis.md`.

## 3. Roadmap Alignment Assessment

| Tag | Finding |
|---|---|
| [Aligned] | P94-P100 followed P93 correctly: high-FIP signal was qualified, tracked as diagnostic-only, marked coverage-limited, and kept out of production. |
| [Aligned] | P101 correctly realigned the project into two lanes matching user product goals: Lane A Taiwan Sports Lottery pregame market/recommendation contracts; Lane B outcome-only strategy learning/backtest/simulation. |
| [Aligned] | P102-P111 advanced Lane B without odds, EV, CLV, Kelly, stake, production, or recommendation output. |
| [Aligned] | P112-P121 advanced Lane A contract safety without real odds, provider activation, recommendation generation, or production mutation. |
| [Aligned] | P118/P119 correctly validate that unsafe recommendation-row states are BLOCKED. |
| [Aligned] | P120/P121 correctly keep provider authorization as absent; placeholder is not treated as approval. |
| [Drift] | `roadmap.md` latest section was still `0I`, post-P93, even though HEAD has advanced through P121. |
| [Drift] | P100 wait-state said no new phase should run without new outcome rows; P101-P121 were nevertheless valuable because they shifted to product-contract work, but that lane shift was not yet reflected in roadmap. |
| [Drift] | P101-P121 produced many artifacts quickly; continuing with more placeholder/spec-only phases risks process motion without product readiness. |
| [Missing] | Roadmap lacked a post-P121 readiness review for P112-P121 as one Lane A system. |
| [Missing] | Roadmap lacked a P101-P121 artifact/phase index to reduce handoff and weak-worker citation risk. |
| [Missing] | Roadmap lacked an explicit post-P121 CEO decision requirement before a new worker prompt can be truthfully based on CEO final裁決. |
| [Outdated] | P94 as "next" is outdated; P94-P121 are completed historical phases. |
| [Outdated] | Treating dirty-tree cleanup as independent P0 is outdated after staged-files-only governance; dirty tree remains a commit-safety risk, not today's highest product maturity blocker. |
| [Blocked] | Taiwan lottery recommendation, market-edge, EV/CLV, Kelly, stake, profit, provider integration, and production remain blocked by missing legal provider authorization and missing real legal odds. |
| [Blocked] | Full-season learning claims remain blocked by partial 2026 coverage and P98-P100 no-new-row wait-state. |
| [Blocked] | New worker task prompt output is blocked by conflicting user instructions: later prompt asks for one, strict constraints forbid it and allow only two file writes. |

## 4. Completed Work Assessment

- [Confirmed] HEAD is `70623ed feat(P121): Provider Authorization Evidence Placeholder - P121_PROVIDER_AUTHORIZATION_EVIDENCE_PLACEHOLDER_READY_WITH_BLOCKERS`.
- [Confirmed] P94 completed with `P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY`.
- [Confirmed] P95 completed with `P95_FIP_STRATIFIED_SHADOW_TRACKER_READY_WITH_LIMITED_COVERAGE`.
- [Confirmed] P96 completed with `P96_HIGH_FIP_DRIFT_MONITOR_STABLE_COVERAGE_LIMITED`.
- [Confirmed] P97 completed with `P97_HIGH_FIP_PREFLIGHT_SIGNAL_PASS_PRODUCTION_BLOCKED`; readiness ratio reported as 2/10 and production blocked by calibration, coverage, market-edge, odds dataset, governance, recommendation contract, risk control, and season-span gates.
- [Confirmed] P98-P100 completed wait-state checks: no material new outcome/canonical row deltas; system should not rerun outcome-dependent phases without new data.
- [Confirmed] P101 created the two-lane product roadmap: Lane A market contract and Lane B outcome-only strategy learning.
- [Confirmed] P102-P111 completed the Lane B outcome-only packet: scorecard, learning matrix, score simulation design/runner/review, adjustment backlog, tracking report, drift snapshot, dashboard contract, and dashboard fixture.
- [Confirmed] P112-P121 completed the Lane A paper-only contract/safety packet: market-contract gap review, paper-only market schema, legal odds source requirements, odds ingestion fixture, recommendation row dry-run contract, recommendation row fixture, validation gate, violation fixture, provider authorization checklist, and provider authorization evidence placeholder.
- [Confirmed] P121 report states `tests/test_p121_provider_authorization_evidence_placeholder.py` passed and `tests/test_p120_legal_provider_authorization_checklist.py` passed.
- [Confirmed] P121 summary states no provider is approved, no authorization evidence is present, no real evidence is stored, and all provider / odds / recommendation / production use remains BLOCKED.
- [Confirmed] P118/P119 safety chain blocks `recommendation_allowed=true` violation fixtures.
- [Confirmed] Governance remains `paper_only=true`, `diagnostic_only=true`, `production_ready=false`, no real bet, no recommendation, no odds, no EV, no CLV, no Kelly, no stake/profit.
- [Confirmed] Push was not performed per handoff, and previous protected-branch push restrictions should not be bypassed.
- [Unknown] P121 full repository regression status.

## 5. Unfinished Work Assessment

| Item | Status |
|---|---|
| Post-P121 readiness review | [Missing] P112-P121 have not yet been evaluated as one Lane A readiness system. |
| Legal provider authorization | [Blocked] No signed/legal provider evidence exists; P121 keeps all providers BLOCKED. |
| Real legal odds dataset | [Blocked] No lawful odds source is approved or ingested; market-edge and recommendation remain blocked. |
| Provider evidence validation gate | [Missing] P121 placeholder exists, but a future gate is needed to ensure placeholders cannot be mistaken for authorization. |
| Artifact / phase catalog | [Missing] P101-P121 artifact volume is high; no compact phase index exists. |
| Post-P121 CEO decision | [Unknown] Existing `CEO-Decision.md` is post-P93/P94, not post-P121. |
| P121 broader regression | [Unknown] P121/P120 dedicated tests pass; full regression for P121 was not confirmed. |
| 2026 coverage / outcome accumulation | [Blocked] P98-P100 indicate no material new rows; outcome-dependent learning should wait for new data or a review threshold. |
| Dirty worktree | [Confirmed risk] `git status --short` remains dirty; future work must use staged-files-only governance. |
| Worker task prompt | [Blocked] Strict CTO instruction forbids producing a new worker prompt and CTO may not write `active_task.md`. |

## 6. P0 / P1 / P2 / P3-P10 Reprioritization

| Priority | Phase | Why now |
|---:|---|---|
| **P0** | P122 Paper-Only Recommendation Readiness Review | P101-P121 produced enough Lane A contract surface that the next maturity step is system-level readiness, not more placeholder accumulation. |
| **P0** | Legal Provider Authorization / Real Legal Odds Blocker | Product recommendation cannot mature without lawful provider evidence and legal odds/source trace. This is a true product and data-rights blocker. |
| **P1** | P101-P121 Artifact Catalog / Phase Index | Artifact sprawl now increases roadmap, handoff, and weak-worker risk. |
| **P1** | Provider Evidence Validation Gate | P121 placeholder must be guarded so no future agent treats placeholder fields as real authorization. |
| **P1** | Agent Entry / Staged-Files-Only Governance | Dirty worktree is persistent; governance must focus on canonical repo/main and staged whitelist rather than full-tree cleanliness. |
| **P2** | P121 Targeted / Broader Regression Policy | Dedicated tests passed; broader regression is unknown and should be reported before using P121 as a stable base. |
| **P2** | Lane B Outcome-Only Learning Cadence | Continue learning/backtest/simulation only when new outcome rows or scheduled review criteria exist. |
| **P3** | Repo Hygiene Sweep | Useful but should not preempt product readiness. Handle untracked/probe/runtime artifacts separately. |
| **P4** | 2026 Coverage Accumulation Watch | Keep full-season claims blocked until coverage/outcome rows increase. |
| **P5** | FIP-Stratified Shadow Tracker Maintenance | Maintain high/mid/low FIP diagnostic boundaries; do not expand into recommendation. |
| **P6** | Recommendation Row Dry-Run Readiness Gate | Only after P122 says Lane A is ready should any dry-run gate be considered. |
| **P7** | Market-Edge Reentry | Still blocked until real legal odds data exists and passes policy gates. |
| **P8** | Calibration / Refit Gate | Important later, but premature before legal/data/coverage gates and must remain OOS/diagnostic-only. |
| **P9** | Roadmap / CEO Decision Hygiene | Roadmap, CTO analysis, CEO decision, and active task must be synchronized after phase bursts. |
| **P10** | Production Proposal Gate | Production remains blocked until prediction, market-edge, legal/data, risk, monitoring, and explicit approval all pass. |

Upgraded:

- [Confirmed] P122 readiness review is upgraded to P0.
- [Confirmed] Legal provider authorization / real legal odds evidence is upgraded to P0 blocker.
- [Confirmed] P101-P121 artifact catalog is upgraded to P1.
- [Confirmed] Provider evidence validation gate is upgraded to P1.

Downgraded:

- [Confirmed] P94/P95/P96 high-FIP diagnostic work is downgraded from "next" to completed historical foundation.
- [Confirmed] Dirty-tree cleanup as a standalone P0 is downgraded to P2/P3 governance risk under staged-files-only policy.
- [Confirmed] Calibration/refit, market-edge, EV/CLV, Kelly, stake/profit, and production proposal remain behind legal/data/readiness gates.
- [Inferred] Continuing placeholder-only expansion should be downgraded unless P122 identifies a precise missing gate.

Merged:

- [Confirmed] P112-P121 should be reviewed as one Lane A readiness packet.
- [Confirmed] P102-P111 should be maintained as one Lane B outcome-only learning/dashboard packet.
- [Confirmed] P118-P121 should be treated as one recommendation/provider safety suite.

Paused or retired:

- [Confirmed] Retired as current priority: P94 as next task, P100 wait-only as entire roadmap, and P82 market-edge reentry without real legal odds.
- [Confirmed] Paused: all production, recommendation, odds ingestion, EV/CLV, Kelly, stake/profit, live/paid API, crawler, and provider activation work.
- [Inferred] Paused: additional placeholder/spec-only phases until readiness review proves the next missing piece.

## 7. Critical Blockers

### Blocker 1: No Legal Provider Authorization / No Real Legal Odds

- Impact: product maturity, data rights, market-edge, Taiwan lottery recommendation, EV/CLV, Kelly, and production.
- Why blocker: [Confirmed] P121 states no provider is approved and no authorization evidence is present.
- Risk if ignored: system may imply betting readiness or market validity without lawful data rights.
- Priority: P0.
- Acceptance: signed/legal provider evidence exists; license scope covers markets; provider approval passes validation; source trace and audit requirements pass; secrets remain outside repo.

### Blocker 2: No Post-P121 Readiness Review

- Impact: roadmap correctness, product direction, execution focus.
- Why blocker: [Confirmed] P112-P121 produced many contract/safety artifacts, but no system-level readiness matrix exists.
- Risk if ignored: next phases may continue producing specs/placeholders without moving toward a verified product decision.
- Priority: P0.
- Acceptance: readiness matrix covers markets, schema, legal odds, recommendation row, validation gates, provider authorization, blockers, allowed next actions, and prohibited actions.

### Blocker 3: Post-P121 CEO Decision Is Missing

- Impact: governance and task orchestration.
- Why blocker: [Confirmed] Existing CEO decision covers post-P93/P94; [Unknown] no CEO final裁決 exists for P101-P121.
- Risk if ignored: any "based on CEO final decision" worker task prompt would be unsupported.
- Priority: P0/P9.
- Acceptance: CEO post-P121 decision exists or roadmap explicitly states CEO decision is absent and prompt generation is blocked.

### Blocker 4: Provider Placeholder Could Be Misread As Authorization

- Impact: legal/compliance safety and future integration risk.
- Why blocker: [Confirmed] P121 intentionally creates a placeholder. Without a validation gate, future workers may treat placeholder fields as real authorization.
- Risk if ignored: unauthorized odds integration or recommendation flow could be unlocked accidentally.
- Priority: P1.
- Acceptance: validation gate enforces `authorization_evidence_present=false`, `provider_approved=false`, no secrets/auth URLs/contracts, and all markets BLOCKED until real evidence passes review.

### Blocker 5: P121 Full Regression Unknown

- Impact: test confidence and cross-phase correctness.
- Why blocker: [Confirmed] P121/P120 dedicated tests pass; [Unknown] full regression for P121 was not reported.
- Risk if ignored: later workers may overstate validation confidence.
- Priority: P2.
- Acceptance: dedicated, targeted P101-P121, and full-regression status is recorded as PASS/FAIL/NOT RUN with rationale.

### Blocker 6: Artifact Sprawl and Dirty Worktree

- Impact: agent workflow, auditability, commit safety.
- Why blocker: [Confirmed] P101-P121 artifact count is high and `git status --short` remains dirty.
- Risk if ignored: workers may cite wrong artifacts, repeat phases, or stage unrelated runtime/data/output files.
- Priority: P1 for catalog, P2/P3 for hygiene.
- Acceptance: phase index exists; future tasks report staged whitelist; unrelated dirty files remain unstaged or are handled by separate hygiene decision.

### Blocker 7: Partial 2026 Coverage / No New Outcomes

- Impact: data quality and learning validity.
- Why blocker: [Confirmed] P98-P100 indicate no material new rows; coverage remains partial.
- Risk if ignored: outcome-only learning may overfit March-May and overstate full-season reliability.
- Priority: P4.
- Acceptance: reruns occur only on meaningful outcome/canonical coverage deltas or scheduled review threshold; reports keep coverage-limited language.

## 8. Recommended System Optimization Directions

### Direction 1: Lane A Readiness Consolidation

- Direction name: P122 Paper-Only Recommendation Readiness Review.
- Roadmap phase: P0.
- Why important: P112-P121 are individually useful, but the system now needs one answer: is Lane A ready for a later dry-run gate, or still blocked by legal/provider/odds gaps?
- Maturity gain: Converts artifact accumulation into product-readiness evidence.
- Expected benefit: Stops placeholder drift and gives CEO/Planner a clear allowed-next-action matrix.
- Risk: Review may conclude that no further implementation is justified until legal evidence exists.
- Acceptance: readiness matrix covers P112-P121, blockers, allowed next actions, prohibited actions, and no real odds/recommendation/production.
- Suggested priority: P0.

### Direction 2: Legal Provider and Odds Evidence Gate

- Direction name: Provider authorization and legal odds unlock.
- Roadmap phase: P0 blocker / P7 reentry.
- Why important: Taiwan Sports Lottery recommendation cannot be validated without lawful odds and provider/source trace.
- Maturity gain: Separates real product unblock from contract-only progress.
- Expected benefit: Prevents unsupported EV/CLV/Kelly/recommendation claims.
- Risk: Depends on external legal/provider evidence and may remain blocked.
- Acceptance: provider evidence passes validation; no secrets in repo; authorized markets and access methods are explicit.
- Suggested priority: P0 blocker.

### Direction 3: Artifact and Roadmap Governance Index

- Direction name: P101-P121 phase catalog.
- Roadmap phase: P1.
- Why important: The repo now has many scripts, tests, reports, summaries, and classifications.
- Maturity gain: Improves auditability and reduces weak-worker drift.
- Expected benefit: Future agents can locate source-of-truth artifacts without hallucinating phase state.
- Risk: Another document could become stale if not compact and source-linked.
- Acceptance: phase -> objective -> artifact -> report -> test -> commit -> classification -> blocker table exists and is read-only over current artifacts.
- Suggested priority: P1.

### Direction 4: Verification and Regression Cadence

- Direction name: P121 broader regression policy and Lane B rerun cadence.
- Roadmap phase: P2.
- Why important: Dedicated tests are not the same as system confidence, and outcome-only learning should not rerun without new data.
- Maturity gain: Makes test status explicit and prevents meaningless reruns.
- Expected benefit: Cleaner quality gates and less compute/token waste.
- Risk: Full regression may be slow or noisy; should be marked NOT RUN when not authorized.
- Acceptance: dedicated, targeted, and full-regression status are reported; outcome-dependent reruns have data-delta criteria.
- Suggested priority: P2.

### Direction 5: Agent Workflow and Cost Guardrails

- Direction name: staged-files-only governance plus anti-sprawl discipline.
- Roadmap phase: P1/P3.
- Why important: Dirty tree and fast phase bursts are now recurring operational risks.
- Maturity gain: Improves commit provenance and reduces unnecessary phase creation.
- Expected benefit: Lower risk of accidental staging, duplicate work, and token-heavy prompt loops.
- Risk: If overdone, governance can become its own workstream.
- Acceptance: future tasks enforce canonical repo/main, staged whitelist, no new repo/worktree, no protected-branch bypass, and no placeholder-only phase unless readiness review justifies it.
- Suggested priority: P1 for workflow guard, P3 for cleanup.

## 9. Roadmap Changes Applied

- [Confirmed] Updated `00-Plan/roadmap/roadmap.md` CTO review date to `2026-05-31 Asia/Taipei`.
- [Confirmed] Updated roadmap status to state that section `0J` supersedes `0I`.
- [Confirmed] Updated active marker to `CTO_CANONICAL_ROADMAP_P121_DONE_P122_READINESS_REVIEW_NEXT_20260531`.
- [Confirmed] Added new top section `0J. Latest CTO Update - P121 Done, Readiness Review Before More Buildout`.
- [Confirmed] Marked HEAD as P121 `70623ed`.
- [Confirmed] Marked P94-P100 and P101-P121 as completed historical phases with current blockers.
- [Confirmed] Reprioritized P0-P10 around P122 readiness review, legal provider/odds blocker, artifact catalog, provider evidence validation, staged-files governance, and blocked production lane.
- [Confirmed] Preserved historical sections `0I` and earlier.
- [Confirmed] Did not write `active_task.md`.
- [Confirmed] Did not write `CEO-Decision.md`.
- [Confirmed] Did not emit or write a worker task prompt.

## 10. Risks / Unknowns

- [Confirmed] Worktree remains dirty; observed `git status --short` count was 95 entries.
- [Confirmed] P121 says no provider is approved and no authorization evidence is present.
- [Confirmed] No real odds, EV, CLV, Kelly, stake/profit, recommendation, live/paid API, provider activation, or production readiness exists.
- [Confirmed] Existing CEO decision is post-P93/P94, not post-P121.
- [Confirmed] P121/P120 dedicated tests pass per report.
- [Unknown] P121 full repository regression status.
- [Unknown] Whether CEO will approve P122 readiness review or choose provider evidence validation gate first.
- [Unknown] Whether any real legal provider evidence can be obtained soon.
- [Inferred] Continuing placeholder-only phases without readiness review will increase artifact sprawl and reduce roadmap signal.
- [Inferred] Outcome-only strategy learning should wait for new outcome rows or a defined review cadence.

## 11. CTO Final Recommendation

Do not continue adding new placeholder or contract phases until P112-P121 are reviewed as one Lane A readiness system. The highest-value next system optimization is P122 Paper-Only Recommendation Readiness Review, but this CTO step cannot emit a worker prompt because the user's strict constraints explicitly forbid new worker task prompts and limit writes to `roadmap.md` / `CTO-Analysis.md`.

The true product blocker is not model signal today. It is legal/provider/odds evidence. P121 correctly keeps every provider and market BLOCKED. Until lawful provider authorization and real legal odds data pass validation, no Taiwan lottery recommendation, EV/CLV, Kelly, stake/profit, or production lane should reopen.

For Lane B, keep outcome-only strategy learning diagnostic-only and rerun only when new outcome/canonical rows or a scheduled review threshold exists. For workflow, keep staged-files-only governance and add a P101-P121 phase catalog to reduce agent drift.

Final classification for this CTO review:

`CTO_ROADMAP_UPDATED_WITH_RISKS`

## 12. CTO Summary

1. [Confirmed] Roadmap was stale at P93; HEAD is now P121.
2. [Confirmed] P101-P121 advanced product contracts safely, but all provider/odds/recommendation paths remain BLOCKED.
3. [Inferred] Next best system move is P122 readiness review, not another placeholder.
4. [Unknown] P121 full regression and post-P121 CEO decision are absent/unknown.
5. [Blocked] CTO did not create a worker prompt because strict instructions forbid it.

## 13. CEO Summary

1. [Confirmed] Current product readiness is paper-only and diagnostic-only.
2. [Confirmed] No legal provider authorization or real odds dataset exists; recommendation and production remain blocked.
3. [Inferred] CEO should decide whether to approve P122 readiness review before any new worker execution.
4. [Inferred] P101-P121 should be consolidated into a readiness matrix and phase catalog.
5. [Blocked] A "CEO-final-decision-based" worker prompt cannot be produced until CEO post-P121 decision exists.
