# Active Task: P172 Bot-Branch Daily Workflow Persistence

## Governance Status

P169R automatic PR creation is blocked by the repository's actual GitHub
Actions settings:

- `default_workflow_permissions`: `read`
- `can_approve_pull_request_reviews`: `false`

Under the current repository policy, GitHub Actions is not allowed to create
pull requests with the workflow `GITHUB_TOKEN`. Automatic PR creation with
`GITHUB_TOKEN` is not authorized and must not be implemented.

The previous P169 requirement to create or update a pull request automatically
is superseded. P172 is the active next implementation task and is limited to
bot-branch persistence only. This governance update does not authorize any
later GitHub settings, PAT, GitHub App, secret, or automatic PR task.

## Purpose

Implement interim persistence for the Daily WBC Data Sync workflow:

1. Stop direct pushes from the daily workflow to protected `main`.
2. Persist generated changes to the deterministic branch
   `bot/daily-wbc-data`.
3. Push only `bot/daily-wbc-data`.
4. Perform no automatic PR creation.
5. Leave manual PR creation, or a future GitHub App, PAT, or repository-setting
   decision, to a separately authorized task.

When a human later opens or updates a PR from `bot/daily-wbc-data` into `main`,
the existing `replay-default-validation` required check must run normally
before merge.

## Allowed File Whitelist

P172 may modify, stage, and commit only:

- `.github/workflows/daily_update.yml`
- `report/p172_bot_branch_daily_workflow_persistence_20260606.md`
- `data/mlb_2026/derived/p172_bot_branch_daily_workflow_persistence_summary.json`

Any required change outside this whitelist must stop the task.

## Required Workflow Behavior

- Preserve the workflow name and existing cron schedule.
- Preserve the existing Paper Mode step and paper flags.
- Preserve the existing WBC fetch and update commands.
- Keep `contents: write`.
- Do not add `pull-requests: write`; P172 performs no automatic PR operation.
- Exit successfully with explicit logging when there are no generated changes.
- When generated changes exist, commit them to `bot/daily-wbc-data`.
- Push only `bot/daily-wbc-data`, with clear success and failure logging.
- Reuse the single deterministic bot branch and preserve any unmerged daily
  data already present on that branch.
- Never push generated changes directly to `main`.
- Do not create, update, approve, or merge a pull request automatically.

## Safety Invariants

- No branch protection weakening, required-check bypass, or bot bypass.
- No `workflow_dispatch`, manual workflow trigger, or workflow rerun.
- No branch creation or deletion manually during local P172 implementation.
- No GitHub Actions repository settings changes.
- Do not enable Actions-created pull requests.
- No PAT creation or usage.
- No GitHub App provisioning or credentials.
- No secret creation or usage beyond the existing workflow `GITHUB_TOKEN`.
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
- No modifications outside the P172 Allowed File Whitelist.

## Expected P172 Phase 0

Before P172 edits begin, verify:

- Canonical repo:
  `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Current branch: `main`
- HEAD is attached.
- Local HEAD equals the new P171 commit produced by this governance task. The
  next P172 prompt must use that exact commit SHA.
- `origin/main` remains
  `10c586d5764a241e165c6b37af001896164c31f2` unless a separate task explicitly
  authorizes a push.
- Local `main` contains the P170 and P171 governance commits above
  `origin/main`.
- PR #12 remains merged.
- Workflow run `27051506120` exists with head SHA
  `10c586d5764a241e165c6b37af001896164c31f2`.
- No files are staged.
- No untracked files exist.
- The dirty tree is clean or contains only the tolerated runtime files below.
- `.github/workflows/daily_update.yml` exists.
- `.github/workflows/replay_default_validation.yml` exists.
- Repository Actions settings remain compatible with branch push via explicit
  `contents: write`; no automatic PR capability is assumed.

## Tolerated Runtime Dirty Files

These pre-existing files may be modified but must not be staged, committed,
restored, cleaned, deleted, moved, reset, or changed by P172:

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

Stop P172 immediately if:

- The repo is not the canonical repo.
- The current branch is not `main`.
- HEAD is detached.
- Local HEAD does not equal the P171 commit specified by the next task.
- `origin/main` differs from the expected SHA without separate authorization.
- Any files are staged before implementation.
- Any untracked files exist before implementation.
- The dirty tree contains files outside the tolerated runtime list.
- Either required workflow file is missing.
- Implementation requires modifying or staging a file outside the P172
  whitelist.
- Implementation requires weakening branch protection or bypassing
  `replay-default-validation`.
- Implementation requires automatic PR creation, `pull-requests: write`,
  `workflow_dispatch`, a manual trigger, or a rerun.
- Implementation requires changing GitHub settings, creating or using a PAT,
  provisioning a GitHub App, or adding a secret.
- Implementation requires a direct push to `main`, a local push during the
  implementation task, or manual branch creation or deletion.
- Implementation requires DB writes beyond existing workflow outputs, manual
  API calls, provider or production unlock, EV/CLV/Kelly unlock,
  `controlled_apply`, or registry mutation.

## Commit Authorization

After P172 validation passes, staging and one local commit are authorized only
for the three whitelisted P172 files. P172 must not push the local commit,
create a branch manually, trigger or rerun a workflow, create a PR, or modify
GitHub settings, tokens, apps, or secrets.

## Expected P172 Outcome

- Direct protected-main push behavior is removed.
- Daily generated changes persist on `bot/daily-wbc-data`.
- No automatic PR is created.
- Main branch protection and `replay-default-validation` remain unchanged.
- P172 report and JSON summary artifacts are committed with the workflow
  change.
- Runtime dirty files remain untouched.
