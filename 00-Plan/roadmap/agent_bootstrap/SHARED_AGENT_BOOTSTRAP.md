# Shared Agent Bootstrap

All Planner, Worker, CTO, and CEO agents must read this file before execution.
Project-specific state belongs in `CURRENT_STATE.md`; task-specific authority
belongs in `../active_task.md` or the explicit user prompt.

## Required Read Order

1. `SHARED_AGENT_BOOTSTRAP.md`
2. `TASK_TEMPLATES.md`
3. `CURRENT_STATE.md`
4. `../CEO-Decision.md`, if current
5. `../active_task.md`
6. task-specific user prompt

## Project Config Requirement

Every task that writes files or executes external effects must define:

- project name
- canonical repo and branch
- expected HEAD/data/artifact baseline
- forbidden execution paths
- allowed write files
- forbidden write targets
- required tests/guards
- final classifications

If this information is missing or contradictory, STOP.

## Canonical Repo / Branch Rules

- Verify repo, branch, symbolic HEAD, git-dir, local HEAD, and remote HEAD.
- Do not silently change directory, branch, worktree, or clone to repair a mismatch.
- Detached HEAD or an unauthorized worktree is a STOP condition.

## Forbidden Execution Paths

Do not execute from:

- archives, backups, stale clones, or quarantine directories
- auto-created GUI worktrees unless explicitly authorized
- another project with a similar name

## Phase 0 Mandatory Verification

Before modification, verify:

1. `pwd`
2. git top-level
3. current branch and symbolic HEAD
4. git-dir
5. local and expected remote HEAD
6. staged, untracked, and dirty files
7. expected data/artifact baseline
8. required read-only guards/tests
9. allowed write whitelist

## STOP Conditions

STOP if:

- repo/branch/git-dir/HEAD does not match
- staged or unexpected untracked files exist
- dirty files exceed the task's tolerated list
- required baseline or guard fails
- task needs files outside the whitelist
- task needs DB/production/provider/registry/deployment effects without authority
- task needs branch, commit, push, merge, rebase, reset, stash, clean, or delete without authority
- scope is ambiguous enough to risk unrelated changes

A STOP report must include expected state, observed state, difference, risk, and
the smallest corrected scope.

## General Forbidden Actions

Unless explicitly authorized:

- no DB or production write
- no live/paid provider call
- no registry mutation or `controlled_apply`
- no real betting or automated stake execution
- no automatic strategy-weight or champion change
- no branch/commit/push/merge/rebase/reset/stash/clean/delete
- no broad staging such as `git add .` or `git add -A`
- no weakening tests or governance

## Allowed File Whitelist

Edit only files named by the task. Before staging, list changed files and stage
only the explicit whitelist. Runtime, logs, caches, raw feeds, and generated
data are never staged unless specifically authorized.

## Test Handling

- Run the smallest relevant tests plus broader tests proportional to risk.
- Report PASS, FAIL, or NOT RUN honestly.
- A failure may be fixed only inside authorized scope; otherwise STOP.

## Next Prompt Format

A generated next task prompt must contain one main task and include:

- canonical repo/branch
- Phase 0 verification
- allowed and forbidden actions/files
- STOP conditions
- acceptance criteria and tests
- required completion check
- final classifications

## Required Completion Check

Every task ends with:

1. whether work is genuinely complete
2. tests: PASS / FAIL / NOT RUN
3. single remaining blocker
4. modified files
5. staged / commit / push status
6. whether the next round is allowed
7. final classification
