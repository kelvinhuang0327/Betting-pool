# Active Task: P180 Offline Paper Strategy Attribution and Performance Leaderboard

## Governance Status

P172 bot-branch daily workflow persistence is merged and is no longer the
active implementation task.

- PR #13 is merged.
- P172 bot-branch persistence is on `main`.
- P176/P177 are `WAITING` for the first post-P172 scheduled run.
- Do not start more Git polling or Git architecture work unless scheduled
  persistence later fails.

P179 supersedes the stale P172 active-task authorization and authorizes P180
only after the P179 governance update is committed locally. P180 is limited to
an offline, paper-only, diagnostic-only strategy attribution and performance
leaderboard implementation.

## Purpose

Implement one offline vertical slice that connects MLB paper recommendations
to strategy-level performance evaluation:

1. Add an explicit, backward-compatible `strategy_id` to MLB paper
   recommendation rows.
2. Populate `strategy_id` only from the loaded simulation `strategy_name`.
3. Classify legacy or missing strategy identities as `UNATTRIBUTED`.
4. Extend `mlb_paper_evaluator` with strategy segmentation and a deterministic
   performance leaderboard.
5. Include sample count, hit rate, Brier score, shadow-unit ROI, and binomial
   p-value for each attributed strategy.
6. Mark strategies below the existing small-sample threshold as
   `DATA_LIMITED`.
7. Add fixture-only tests for attribution, legacy rows, deterministic ranking,
   and safety invariants.

P180 must not infer a missing `strategy_id` from filenames, model versions, or
other indirect metadata.

## Allowed File Categories

P180 may modify only files in these offline categories, with exact paths
adapted to the repository's actual code structure:

- Recommendation row and paper recommendation producer files required to add
  and populate `strategy_id`.
- `mlb_paper_evaluator` files required to implement strategy segmentation and
  the deterministic leaderboard.
- Fixture-only tests for the P180 behavior and safety invariants.
- P180 report and summary artifacts.

P180 must not modify workflow files, DB migrations, registries, provider
integrations, production betting code, deployment files, or
`controlled_apply` files.

## Required Behavior

### Strategy Attribution

- The recommendation row contract remains backward-compatible.
- New paper rows use the loaded simulation's exact `strategy_name` as
  `strategy_id`.
- Rows without an explicit strategy identity evaluate as `UNATTRIBUTED`.
- Legacy rows remain readable without migration or backfill.
- Missing identities are never guessed from filenames,
  `model_ensemble_version`, simulation IDs, or other indirect fields.

### Strategy Performance Leaderboard

- Evaluation remains deterministic for identical recommendation and outcome
  fixtures.
- Results are segmented by explicit `strategy_id`, including
  `UNATTRIBUTED`.
- Each leaderboard entry includes:
  - sample count
  - hit rate
  - Brier score
  - shadow-unit ROI
  - binomial p-value
- Strategies below the existing small-sample threshold are marked
  `DATA_LIMITED`.
- Ranking rules and tie-breakers are explicit and covered by fixture-only
  tests.
- The leaderboard is diagnostic evidence only and must not mutate strategy
  weights or select a production champion.

## Safety Invariants

- Offline only.
- `paper_only=true`.
- `diagnostic_only=true`.
- No live API calls.
- No DB writes.
- No provider access unlock.
- No production betting unlock.
- No EV, CLV, or Kelly unlock.
- No strategy weight changes.
- No production champion replacement.
- No workflow trigger, workflow rerun, or `workflow_dispatch`.
- No GitHub Actions settings or branch-protection changes.
- No registry mutation.
- No `controlled_apply`.
- No branch creation or deletion unless separately authorized.
- No push unless separately authorized.
- No modification, cleanup, restore, reset, move, deletion, staging, or commit
  of tolerated runtime files.

## Expected P180 Phase 0

Before P180 edits begin, verify:

- Canonical repo:
  `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Current branch is `main`.
- HEAD is attached.
- Local HEAD contains the committed P179 governance update.
- No files are staged.
- No untracked files exist.
- The dirty tree is clean or contains only the tolerated runtime files below.
- P179 is the immediately preceding authorization for P180.
- P172 remains merged and Git polling remains paused while P176/P177 wait for
  the first post-P172 scheduled run.

## Tolerated Runtime Dirty Files

These pre-existing files may be modified but must not be staged, committed,
restored, cleaned, deleted, moved, reset, or changed by P180:

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

## STOP Conditions

Stop P180 immediately if:

- The repo is not the canonical repo.
- The current branch is not `main`.
- HEAD is detached.
- The P179 governance update is not committed.
- Any files are staged before implementation.
- Any untracked files exist before implementation.
- The dirty tree contains files outside the tolerated runtime list.
- Implementation requires live API calls or DB writes.
- Implementation requires provider access, production betting, or EV/CLV/Kelly
  unlock.
- Implementation requires a workflow trigger, workflow rerun, GitHub settings
  change, or Git architecture change.
- Implementation requires strategy weight mutation or production champion
  replacement.
- Implementation requires inferring a missing `strategy_id` from filenames,
  model versions, simulation IDs, or indirect metadata.
- Implementation requires modifying files outside the offline recommendation,
  evaluator, fixture-only tests, and P180 artifact scope.
- Implementation requires registry mutation, deployment changes, or
  `controlled_apply`.

## Commit Authorization

P180 implementation, validation, staging, and commit are authorized only after
the P179 governance update commit exists. P180 may stage and commit only the
exact offline recommendation, evaluator, fixture-only test, and P180 artifact
files authorized by its task prompt. P180 is not authorized to push, trigger
or rerun workflows, change GitHub settings, or modify tolerated runtime files.

## Expected P180 Outcome

- New MLB paper recommendation rows carry an explicit simulation-derived
  `strategy_id`.
- Legacy and missing identities are safely represented as `UNATTRIBUTED`.
- The offline evaluator emits deterministic strategy segmentation and a
  performance leaderboard.
- Each strategy reports sample count, hit rate, Brier score, shadow-unit ROI,
  binomial p-value, and `DATA_LIMITED` status when applicable.
- Fixture-only tests prove attribution, legacy compatibility, ranking
  determinism, and safety invariants.
- No live, DB, provider, production, betting, EV/CLV/Kelly, strategy-weight,
  workflow, or GitHub-settings behavior is changed.
