# Shared Task Templates

This file provides project-neutral task templates. Project-specific details must come from CURRENT_STATE.md, CEO-Decision.md, and the task-specific prompt.

## Template 1 — Plan-only Task

Use for:

- discussion
- roadmap planning
- decision gate
- protocol design
- risk review
- task planning

Allowed actions:

- read files
- read artifacts
- run read-only verification
- produce final report
- optionally update allowed roadmap / decision files if the task explicitly permits it

Forbidden actions:

- code implementation
- DB write
- production write
- registry mutation
- controlled apply
- deployment
- git commit
- git push
- branch creation
- destructive cleanup

Required Phase 0:

- verify repo
- verify branch
- verify git-dir
- verify no staged files
- verify project state from CURRENT_STATE.md or task-specific prompt

Allowed write scope:

- none by default
- only roadmap / decision / analysis files if explicitly listed

Validation:

- file existence checks if files are written
- read-only guard checks if available
- mark tests NOT RUN if not applicable

Required output:

1. problem statement
2. findings
3. risks
4. recommendation
5. next task scope
6. Required Completion Check

Final Classification examples:

- PLAN_ONLY_TASK_READY
- PLAN_ONLY_TASK_WITH_RISKS
- PLAN_ONLY_TASK_BLOCKED

---

## Template 2 — Read-only Execution Task

Use for:

- diagnostic script execution
- read-only SQL
- audit
- metrics extraction
- artifact inspection
- CI / PR monitoring

Allowed actions:

- run read-only commands
- run tests
- inspect DB in read-only mode
- inspect git / PR / CI state
- produce report

Forbidden actions:

- DB write
- source modification
- production write
- registry mutation
- controlled apply
- deployment
- git add
- git commit
- git push
- branch change
- destructive action

Required Phase 0:

- verify repo
- verify branch
- verify git-dir
- verify no staged files
- verify data / artifact baseline
- verify required read-only guards

Allowed write scope:

- none unless the task explicitly allows writing report artifacts

Validation:

- targeted tests
- relevant read-only guards
- DB integrity / artifact consistency checks when applicable

Required output:

1. commands run
2. observations
3. PASS / FAIL / NOT RUN test status
4. risk notes
5. next recommended action
6. Required Completion Check

Final Classification examples:

- READ_ONLY_EXECUTION_READY
- READ_ONLY_EXECUTION_FOUND_ISSUES
- READ_ONLY_EXECUTION_BLOCKED

---

## Template 3 — Implementation Task

Use for:

- code change
- test change
- docs change
- artifact creation
- migration script creation
- local commit / PR workflow when explicitly authorized

Allowed actions:

- modify files listed in Allowed Write Files
- run tests
- stage whitelisted files if authorized
- commit / push only if explicitly authorized

Forbidden actions:

- modify files outside whitelist
- DB write unless explicitly authorized
- production write unless explicitly authorized
- registry mutation unless explicitly authorized
- controlled apply unless explicitly authorized
- deployment unless explicitly authorized
- broad git add
- force push
- branch / merge operations unless explicitly authorized
- destructive cleanup unless explicitly authorized

Required Phase 0:

- verify repo
- verify branch
- verify git-dir
- verify no unrelated dirty files
- verify no staged files
- verify current baseline
- verify allowed write list
- verify expected tests

Implementation rules:

- make minimal changes
- do not expand scope
- after each failure, fix only directly related issue
- if scope must expand, STOP
- before staging, list changed files
- stage only whitelisted files
- never stage DB / binary / runtime / logs unless explicitly authorized

Validation:

- targeted tests
- relevant regression tests
- guard checks
- staged file scan if staging occurs
- DB integrity checks if DB is relevant and read-only checks are allowed

Required output:

1. implementation summary
2. files modified
3. tests run
4. staged / commit / push status
5. remaining blocker
6. Required Completion Check

Final Classification examples:

- IMPLEMENTATION_READY
- IMPLEMENTATION_READY_LOCAL_ONLY
- IMPLEMENTATION_BLOCKED
- IMPLEMENTATION_TESTS_FAILED
- IMPLEMENTATION_SCOPE_REVISION_REQUIRED