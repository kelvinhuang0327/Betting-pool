# Active Task: P169 PR-Based Daily Workflow Persistence

## Governance Status

The previous Dirty Tree Cleanup Policy / Classification task is stale and
superseded. Its file whitelist and prohibition on staging and committing no
longer govern the next task.

P169 is the active next task. P169 implementation is authorized after this
governance update is committed. This authorization applies only to P169 and
does not authorize P170+ implementation tasks.

## Purpose

Implement PR-based persistence for the Daily WBC Data Sync workflow:

1. Stop direct pushes from the daily workflow to protected `main`.
2. Persist generated changes to the deterministic branch
   `bot/daily-wbc-data`.
3. Create or update one pull request from `bot/daily-wbc-data` into `main`.
4. Preserve main branch protection and the required
   `replay-default-validation` check on the pull request.
5. Do not auto-merge the pull request.

## Allowed File Whitelist

P169 may modify, stage, and commit only:

- `.github/workflows/daily_update.yml`
- `report/p169_pr_based_daily_workflow_persistence_20260606.md`
- `data/mlb_2026/derived/p169_pr_based_daily_workflow_persistence_summary.json`

Any required change outside this whitelist must stop the task.

## Required Workflow Behavior

- Preserve the workflow name and existing cron schedule.
- Preserve the existing Paper Mode step and paper flags.
- Preserve the existing WBC fetch and update commands.
- Keep `contents: write` and add or confirm `pull-requests: write`.
- Exit successfully with explicit logging when there are no generated changes.
- When changes exist, commit them to `bot/daily-wbc-data` and push only that
  branch.
- Create a pull request into `main` when none exists.
- Update the existing bot branch without creating another pull request when an
  open PR already exists.
- Never push generated changes directly to `main`.
- Allow `replay-default-validation` to run normally on the pull request.

## Safety Invariants

- No branch protection weakening, required-check bypass, or bot bypass.
- No `workflow_dispatch`, manual workflow trigger, or workflow rerun.
- No branch creation or deletion manually during P169 implementation.
- No auto-merge.
- No DB writes outside existing workflow-generated outputs.
- No manual live or paid API calls.
- No provider access unlock.
- No production betting unlock.
- No EV, CLV, or Kelly recommendation unlock.
- No registry mutation.
- No `controlled_apply`.
- No modification, cleanup, restore, reset, move, deletion, staging, or commit
  of tolerated runtime files.
- No modifications outside the P169 Allowed File Whitelist.

## Phase 0 Expectations

Before P169 edits begin, verify:

- Canonical repo:
  `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Current branch: `main`
- HEAD is attached.
- Local HEAD:
  `10c586d5764a241e165c6b37af001896164c31f2`
- `origin/main`:
  `10c586d5764a241e165c6b37af001896164c31f2`
- PR #12 is merged with merge commit
  `10c586d5764a241e165c6b37af001896164c31f2`.
- Workflow run `27051506120` exists with head SHA
  `10c586d5764a241e165c6b37af001896164c31f2`.
- No files are staged.
- No untracked files exist.
- The dirty tree is clean or contains only the tolerated runtime files below.
- `.github/workflows/daily_update.yml` exists.
- `.github/workflows/replay_default_validation.yml` exists.

## Tolerated Runtime Dirty Files

These pre-existing files may be modified but must not be staged, committed,
restored, cleaned, deleted, moved, reset, or changed by P169:

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

Stop P169 immediately if:

- The repo is not the canonical repo.
- The current branch is not `main`.
- HEAD is detached.
- Local HEAD or `origin/main` differs from the expected SHA.
- Any files are staged before implementation.
- Any untracked files exist before implementation.
- The dirty tree contains files outside the tolerated runtime list.
- Either required workflow file is missing.
- Implementation requires modifying or staging a file outside the P169
  whitelist.
- Implementation requires weakening branch protection or bypassing
  `replay-default-validation`.
- Implementation requires `workflow_dispatch`, a manual trigger, or a rerun.
- Implementation requires branch creation or deletion manually, a push during
  the local implementation task, or GitHub settings mutation.
- Implementation requires DB writes beyond existing workflow outputs, manual
  API calls, provider or production unlock, EV/CLV/Kelly unlock,
  `controlled_apply`, or registry mutation.

## Commit Authorization

After P169 validation passes, staging and one local commit are authorized only
for the three whitelisted P169 files. P169 must not push the commit, create a
branch manually, trigger or rerun a workflow, or modify GitHub settings.

## Expected P169 Outcome

- Direct protected-main push behavior is removed.
- Daily generated changes use `bot/daily-wbc-data`.
- The workflow creates or updates a PR into `main`.
- `replay-default-validation` remains required and is not bypassed.
- P169 report and JSON summary artifacts are committed with the workflow
  change.
- Runtime dirty files remain untouched.
