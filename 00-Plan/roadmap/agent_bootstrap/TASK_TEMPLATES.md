# Shared Task Templates

Project-specific values must come from `CURRENT_STATE.md` and the active task.

## Template 1: Plan-Only Task

Use for roadmap, architecture, scope selection, and decision audits.

Allowed:

- read source/artifacts/git state
- run read-only guards/tests
- write only explicitly allowed planning/report files

Forbidden:

- source/data/runtime mutation
- DB/provider/production/registry effects
- branch/commit/push/destructive git actions

Whitelist pattern:

- exact roadmap/report files named by the task

Required output:

- findings, candidate comparison, risks, one recommendation, next task prompt

Completion check:

- report written or final response delivered
- tests/guards reported
- no unauthorized files changed

Classifications:

- `PLAN_ONLY_TASK_READY`
- `PLAN_ONLY_TASK_WITH_RISKS`
- `PLAN_ONLY_TASK_BLOCKED`

## Template 2: Read-Only Execution Task

Use for diagnostics, metrics extraction, artifact inspection, and CI/PR checks.

Allowed:

- read-only commands and tests
- read-only DB access only when explicitly authorized
- optional exact report output

Forbidden:

- source/data mutation
- live provider calls
- DB/production/registry writes
- staging/commit/push/branch/destructive actions

Whitelist pattern:

- none by default; optionally one exact report path

Required output:

- commands, observations, test status, risks, next action

Completion check:

- baseline verified
- no side effects
- report/response complete

Classifications:

- `READ_ONLY_EXECUTION_READY`
- `READ_ONLY_EXECUTION_FOUND_ISSUES`
- `READ_ONLY_EXECUTION_BLOCKED`

## Template 3: Implementation Task

Use for a narrowly authorized code/test/docs change.

Allowed:

- edit exact whitelisted files
- run targeted and proportional regression tests
- stage/commit/push only when separately authorized

Forbidden:

- scope expansion
- unrelated refactor
- runtime/raw/generated staging
- DB/provider/production/registry/deployment effects unless explicit
- branch/merge/destructive operations unless explicit

Whitelist pattern:

- exact source/test/report files, not broad directories

Required output:

- implementation summary, files, tests, git status, blocker

Completion check:

- acceptance criteria met
- test results reported
- changed/staged files match whitelist
- external effects reported

Classifications:

- `IMPLEMENTATION_READY`
- `IMPLEMENTATION_READY_LOCAL_ONLY`
- `IMPLEMENTATION_TESTS_FAILED`
- `IMPLEMENTATION_SCOPE_REVISION_REQUIRED`
- `IMPLEMENTATION_BLOCKED`
