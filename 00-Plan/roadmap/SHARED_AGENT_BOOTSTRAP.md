# Shared Agent Bootstrap

This file defines project-neutral execution rules for Planner, Worker, CTO, and CEO agents.

This file must not hardcode project-specific repo paths, DB rows, branch names, strategy names, PR numbers, or domain-specific assumptions. Project-specific state belongs in:

- 00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md
- 00-Plan/roadmap/CEO-Decision.md
- the current task-specific prompt

## Required Read Order

Before executing any task, read these files if they exist:

1. 00-Plan/roadmap/agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md
2. 00-Plan/roadmap/agent_bootstrap/TASK_TEMPLATES.md
3. 00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md
4. 00-Plan/roadmap/CEO-Decision.md
5. 00-Plan/roadmap/active_task.md, if the workflow uses it

The actual task source is the task-specific prompt provided to the agent, unless the project workflow explicitly says active_task.md is authoritative.

## Project Config

Every task-specific prompt must define:

- Project Name
- Canonical Repo
- Canonical Branch
- Expected runtime / data / artifact state
- Forbidden execution paths
- Allowed write files
- Forbidden write targets
- Required tests or guards
- Final Classification values

If Project Config is missing and the task requires file writes, DB access, git operations, or deployment, STOP.

## Conflict Priority

If rules conflict, use this priority order:

1. Explicit task-specific authorization phrase and task-specific section
2. CEO-Decision.md
3. CURRENT_STATE.md
4. SHARED_AGENT_BOOTSTRAP.md
5. TASK_TEMPLATES.md
6. active_task.md, if present

Safety rules must never be weakened. If conflict involves repo, branch, DB, production write, registry mutation, controlled apply, deployment, branch, commit, push, merge, delete, archive, or allowed files, STOP and report the conflict.

## Phase 0 Verification

Before any modification, verify actual state.

Minimum checks:

- current working directory
- git top-level
- current branch
- git-dir
- git status
- HEAD
- expected canonical repo
- expected canonical branch
- expected data / artifact / test baseline
- staged files
- unrelated dirty files

If the project has DB or critical data files, run read-only checks required by CURRENT_STATE.md or the task-specific prompt.

If actual state differs from prompt expectation, STOP. Do not repair by cd, checkout, reset, branch creation, or worktree switching unless explicitly authorized.

## STOP Conditions

STOP immediately if:

- repo is not the canonical repo
- branch is not the canonical branch
- git-dir does not match expectation
- runtime is inside an unauthorized worktree, stale clone, archive, or backup path
- staged files exist before task
- unrelated dirty files exist
- expected data / artifact / guard baseline does not match actual state
- required tests or guards fail
- task needs files outside allowed write list
- task needs DB write without explicit authorization
- task needs production write without explicit authorization
- task needs registry mutation without explicit authorization
- task needs controlled apply without explicit authorization
- task needs deployment without explicit authorization
- task needs branch creation, checkout, merge, rebase, reset, cherry-pick, commit, push, or force push without explicit authorization
- task needs destructive action without explicit authorization
- task scope is unclear or unsafe

STOP report must include:

1. prompt expected state
2. actual observed state
3. difference
4. risk
5. suggested corrected task scope

## General Forbidden Actions Unless Explicitly Authorized

- create new repo
- clone repo
- create worktree
- checkout another branch
- use detached HEAD
- DB write
- production write
- registry mutation
- controlled apply
- deployment
- git add outside whitelist
- git commit
- git push
- force push
- merge
- rebase
- reset
- cherry-pick
- delete files or folders
- archive folders
- weaken tests to pass
- bypass governance

## Allowed File Whitelist Rule

Before editing any file:

1. verify it is listed in the task-specific Allowed Write Files
2. verify the change is necessary for the task
3. verify no broader file or directory is being staged

If the file is not whitelisted, STOP and request corrected scope.

Do not use `git add .` or `git add -A` unless explicitly authorized.

## Test and Failure Handling

After a test failure:

- fix only the minimal directly related scope
- do not rewrite unrelated architecture
- do not change package, dependency, config, CI, DB, registry, or production files unless authorized
- if the failure requires scope expansion, STOP

If no tests are run, report NOT RUN. Do not claim PASS.

## Next Prompt Format

If producing the next task prompt:

- use one single text code block
- do not nest Markdown code blocks
- include Canonical Repo
- include Canonical Branch
- include Phase 0 verification
- include STOP conditions
- include Allowed Write Files
- include validation
- include Required Completion Check
- include Final Classification
- include only one main task

## Required Completion Check

Every task must end with:

1. 是否真的完成
2. 測試結果 PASS / FAIL / NOT RUN
3. 仍卡住的唯一問題
4. 修改檔案清單
5. staged / commit / push 狀態
6. 是否允許進入下一輪
7. Final Classification