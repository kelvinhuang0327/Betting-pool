# P172 Bot-Branch Daily Workflow Persistence

- Date: 2026-06-06
- Repository: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Base local HEAD: `41e44d9838ef1f955bcb56a37eae9805d937f7f4`
- Base `origin/main`: `10c586d5764a241e165c6b37af001896164c31f2`
- Classification: bot-branch persistence implementation

## Root Cause Chain

P167 verified scheduled run `27051506120`. The Paper Mode and WBC update
steps succeeded, and the P152 path fix plus P158 `contents: write` permission
were effective. The final push failed with `GH006` because protected `main`
requires `replay-default-validation`.

P168 selected branch-based persistence to preserve branch protection. P169R
then confirmed that repository Actions settings
(`default_workflow_permissions: read`,
`can_approve_pull_request_reviews: false`) prohibit `GITHUB_TOKEN` from
creating pull requests. P171 therefore authorized P172 as an interim
bot-branch-only design.

## Chosen Solution

The Daily WBC Data Sync workflow now persists generated daily outputs only to
the deterministic branch `bot/daily-wbc-data`.

The persistence step:

1. Collects known WBC and paper-only generated paths under top-level
   `data/*.json`, P143 evaluation JSON, MLB scheduler reports, daily scheduler
   Markdown, and PAPER recommendation JSONL files.
2. Exits successfully with explicit logging when no generated changes exist.
3. Fails if an unexpected non-ignored path remains outside that persistence
   allowlist.
4. Stashes the generated changes before changing branches.
5. Checks out the existing bot branch or creates it from the workflow source
   commit.
6. Merges the current workflow source commit into an existing bot branch so
   mainline changes and unmerged bot-branch history are preserved.
7. Reapplies and commits the generated outputs.
8. Pushes only `bot/daily-wbc-data`, with explicit success or failure logging.

The update does not force-push. A concurrent or non-fast-forward update fails
visibly instead of overwriting remote history.

## Explicit Boundaries

- No generated output is pushed directly to protected `main`.
- No PR is created, updated, approved, or merged automatically.
- `pull-requests: write` was not added.
- Existing `contents: write` remains the only declared workflow permission.
- Main branch protection and `replay-default-validation` were not changed or
  bypassed.
- No GitHub Actions settings were changed.
- No PAT, GitHub App credential, or secret was added or used.
- The existing `workflow_dispatch` declaration was left unchanged; it was not
  invoked, and no workflow was rerun.
- No DB write was run manually.
- No live API call was run manually.
- No provider, production betting, EV, CLV, or Kelly capability was unlocked.
- No registry mutation or `controlled_apply` occurred.
- Existing local runtime dirty files were not modified, staged, or committed.

## Validation

Targeted validation for this implementation includes:

- PyYAML was unavailable and no package was installed. Ruby's built-in YAML
  parser successfully loaded the workflow (`YAML_OK_RUBY`).
- The extracted persistence shell block passed `bash -n`
  (`BASH_SYNTAX_OK`).
- Workflow text assertions for `contents: write`,
  `bot/daily-wbc-data`, retained paper flags, and absence of
  `pull-requests: write`, `gh pr create`, and direct `main` push passed
  (`P172_WORKFLOW_TEXT_OK` and `P172_STRUCTURE_OK`).
- Grep inspection of sensitive workflow strings.
- Workflow diff inspection.
- JSON parse validation for the P172 summary passed (`JSON_OK`).
- Staged-file verification against the three-file P172 whitelist.

No pytest is required because this task changes workflow text and governance
artifacts only.

## Next Step

Package the local P170, P171, and P172 commits in a human-created PR into
`main`. Merge only after CI passes. Then wait for the next scheduled Daily WBC
Data Sync run and verify that generated outputs are committed and pushed to
`bot/daily-wbc-data`. A separate authorized task may later decide how and
whether to open PRs from that branch.
