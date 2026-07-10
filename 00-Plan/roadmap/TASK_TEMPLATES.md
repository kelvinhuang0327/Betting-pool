# Shared Task Templates

These templates are project-neutral.

Use project-specific facts only from:

* `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`
* `00-Plan/roadmap/roadmap.md`
* `00-Plan/roadmap/CTO-Analysis.md`
* `00-Plan/roadmap/CEO-Decision.md`
* `00-Plan/roadmap/active_task.md`
* The task-specific prompt

All tasks must follow `SHARED_AGENT_BOOTSTRAP.md`.

## General Template Rules

Every instantiated task must:

* Use one main task only.
* State the task type.
* State Canonical Repo and Canonical Branch.
* State Allowed Write Files.
* State Forbidden Targets.
* State acceptance criteria.
* State required tests or evidence.
* State whether commit, push, worktree, DB write, or destructive action is explicitly authorized.
* End with the Required Completion Check.
* Use exactly one `text` fenced block when presented as a Next 24H Prompt.
* Avoid nested Markdown and inner code fences inside that prompt.

## Template 1 — Type A: Plan-Only Or Decision Support

Use for:

* Roadmap planning
* CTO analysis
* CEO review
* Decision gates
* Protocol design
* Risk review
* Scope revision
* Task planning

Required task fields:

* Project Name
* Canonical Repo
* Canonical Branch
* Task Type: Type A
* Decision Question
* Required Read Files
* Allowed Write Files: None by default
* Required Evidence
* Required Output
* Final Classification Values

Allowed actions:

* Read files, artifacts, tests, and read-only project state.
* Run read-only verification.
* Produce a report.
* Update only explicitly whitelisted roadmap, decision, analysis, or task-planning files.

Forbidden actions:

* Code implementation
* DB write
* Production write
* Registry mutation
* Controlled apply
* Deployment
* Branch operations
* Commit or push
* Destructive cleanup

Required output:

1. Problem statement
2. Confirmed findings
3. Inferred findings
4. Unknowns
5. Risks
6. Recommendation
7. Proposed next task scope, only when authorized
8. Required Completion Check

Final classification examples:

* `PLAN_ONLY_READY`
* `PLAN_ONLY_WITH_RISKS`
* `PLAN_ONLY_BLOCKED`
* `STOPPED_FOR_GOVERNANCE`

## Template 2 — Type B: Read-Only Research, Audit, Or Artifact

Use for:

* Diagnostics execution
* Read-only SQL
* Metrics extraction
* Artifact inspection
* Data-quality audit
* Replay verification
* CI or PR inspection
* Research report generation
* Design document generation

Required task fields:

* Project Name
* Canonical Repo
* Canonical Branch
* Task Type: Type B
* Objective
* Expected Baseline
* Read Scope
* Allowed Artifact Write Files: None by default
* Forbidden Targets
* Required Commands, Tests, Or Guards
* Required Output
* Final Classification Values

Allowed actions:

* Run read-only commands.
* Run tests and guards.
* Inspect DB only in read-only mode.
* Produce a report.
* Write only explicitly approved report or artifact files.

Forbidden actions:

* Source modifications
* DB write
* Production write
* Registry mutation
* Controlled apply
* Deployment
* Git staging, commit, or push
* Branch operations
* Destructive action

Required output:

1. Commands run
2. Baseline observed
3. Findings
4. Test or guard result: PASS / FAIL / NOT RUN
5. Artifact paths, if authorized
6. Risks and limitations
7. Recommended next action
8. Required Completion Check

Final classification examples:

* `READ_ONLY_READY`
* `READ_ONLY_FOUND_ISSUES`
* `READ_ONLY_WITH_RISKS`
* `READ_ONLY_BLOCKED`
* `STOPPED_FOR_GOVERNANCE`

## Template 3 — Type C: Bounded Implementation

Use for:

* Small code changes
* Test changes
* Documentation changes
* Additive scripts
* Local tooling
* Artifact generation code
* Narrow bug fixes

Required task fields:

* Project Name
* Canonical Repo
* Canonical Branch
* Task Type: Type C
* Objective
* Expected Baseline
* Allowed Write Files
* Forbidden Targets
* Explicit Special Authorization
* Acceptance Criteria
* Required Tests
* Required Evidence
* Final Classification Values

Allowed actions:

* Modify only whitelisted files.
* Run required tests.
* Stage only explicitly authorized whitelisted files.
* Commit or push only when explicitly authorized.

Forbidden actions:

* Modify files outside the whitelist.
* DB write unless explicitly authorized.
* Production write unless explicitly authorized.
* Registry mutation unless explicitly authorized.
* Controlled apply unless explicitly authorized.
* Deployment unless explicitly authorized.
* Broad staging.
* New branch, checkout, merge, rebase, reset, cherry-pick, commit, or push unless explicitly authorized.
* Worktree creation or cleanup unless explicitly authorized.
* Destructive cleanup unless explicitly authorized.

Implementation requirements:

1. Complete Phase 0 before edits.
2. Confirm every edited file is whitelisted.
3. Make the smallest change that satisfies acceptance criteria.
4. Run required tests.
5. After failure, make only the smallest directly related repair.
6. STOP if resolution requires scope expansion, configuration changes, schema/API changes, DB changes, registry changes, CI changes, or a non-whitelisted file.
7. Before staging, list all changed files and verify whitelist compliance.

Required output:

1. Implementation summary
2. Files modified
3. Tests and results
4. Diff evidence
5. Staged / commit / push status
6. Remaining blocker
7. Required Completion Check

Final classification examples:

* `IMPLEMENTATION_READY`
* `IMPLEMENTATION_READY_LOCAL_ONLY`
* `IMPLEMENTATION_TESTS_FAILED`
* `IMPLEMENTATION_SCOPE_REVISION_REQUIRED`
* `IMPLEMENTATION_BLOCKED`
* `STOPPED_FOR_GOVERNANCE`

## Template 4 — Type D: DB Write Or Destructive Operation

Use only when the task explicitly authorizes a specific DB write, ingestion, deletion, cleanup, or destructive action.

Required additional fields:

* Exact operation
* Explicit authorization phrase
* Exact target path, database, table, or resource
* Before baseline evidence
* Expected after-state
* Rollback, safe-stop, or recovery path
* Post-operation verification
* Explicit commit or push authorization, if relevant

Do not combine Type D work with unrelated code, research, or governance work.

Final classification examples:

* `CONTROLLED_WRITE_COMPLETED`
* `CONTROLLED_WRITE_VERIFY_FAILED`
* `CONTROLLED_WRITE_BLOCKED`
* `STOPPED_FOR_GOVERNANCE`

## Template 5 — Type E: Strategy, Production, Controlled Apply, Or Recommendation Change

Use only when the task explicitly authorizes:

* Strategy promotion
* Recommendation logic changes
* Registry mutation
* Production behavior changes
* Controlled apply
* Deployment

Required additional fields:

* Explicit authorization phrase
* Preconditions
* Target scope
* QA evidence
* Rollback or safe-stop plan
* Post-change verification
* Release or deployment decision owner

Do not combine Type E work with unrelated tasks.

Final classification examples:

* `HIGH_RISK_CHANGE_READY`
* `HIGH_RISK_CHANGE_VERIFY_FAILED`
* `HIGH_RISK_CHANGE_BLOCKED`
* `STOPPED_FOR_GOVERNANCE`

## Required Handoff Output For Every Template

Every completed task must include:

1. 是否真的完成：YES / NO
2. 測試結果：PASS / FAIL / NOT RUN
3. 仍卡住的唯一問題
4. 修改檔案清單
5. Diff evidence
6. staged / commit / push 狀態
7. 是否允許進入下一輪
8. Final Classification
9. Recommended Worker Profile：模型與思考強度；不適用時填 N/A
10. 是否建議下一輪延續同一對話：YES / NO + 原因
11. Owner Authorization Needed：None 或明確授權請求
12. CTO Briefing Draft：最多5句，不得寫入文件。請用白話說明本輪實際完成什麼、結果代表什麼、是否有技術或驗證風險、下一輪最合理要做什麼；不要只重複 Task ID、分類名稱或測試名稱。
13. CEO Briefing Draft：最多5句，不得寫入文件。請用非技術、容易理解的方式說明這輪研究是否真的有助於提高預測成功率、目前能做與不能做什麼、是否需要暫停或轉換研究方向，以及下一步是否需要 Owner 額外授權。


## Template 6 — Project CURRENT_STATE.md

Use this template for each project's:

`00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`

This is a project-specific operational state file.

It is not a shared file and must not be copied verbatim between projects. Only this structure is shared.

Keep it concise and current. It must describe the latest authoritative state, not become a full historical task archive.

## Current State Rules

1. One project has one canonical `CURRENT_STATE.md`.
2. It records current operational truth only.
3. Historical reports, completed task details, and long evidence belong in committed artifacts, roadmap, CTO analysis, CEO decisions, PRs, or Git history.
4. If older history is retained, it must be a short reference list only.
5. The top `State Marker` must match the latest authoritative project status.
6. `CURRENT_STATE.md` must not authorize DB writes, production changes, registry mutation, deployment, commit, push, merge, or worktree operations by itself.
7. Actual repo, code, artifacts, DB state, and tests remain the Phase 0 source of truth.
8. Update this file only when explicitly allowed by the task.

## Required Structure

# Current State — <Project Name>

Last Updated: <YYYY-MM-DD timezone and updater role>

State Marker:
<CURRENT_AUTHORITATIVE_STATUS>

Project Classification:
<READY / HOLD / BLOCKED / WAITING_FOR_USER_AUTHORIZATION / other approved value>

## 1. Canonical Execution Context

* Canonical Repo: <absolute path>

* Canonical Branch: <branch name>

* Git Requirement:
  <for example: HEAD must equal origin/main; verify in Phase 0>

* Forbidden Execution Paths:

  * <stale clone / archive / backup / unauthorized worktree paths>
  * <additional project-specific forbidden paths>

* Active Worktrees:

  * Canonical: <repo path> @ <branch>
  * Extra: None / <explicitly authorized worktree path, branch, owner, purpose>

## 2. Current Objective

* Primary Goal: <one current project goal>

* Current Approved Direction: <CEO-approved direction or HOLD state>

* Active Worker Task:
  None / <Task ID and short task title>

* Current Task Type:
  None / Type A / Type B / Type C / Type D / Type E

## 3. Current Verified Baseline

* Latest Verified Commit / Merge:
  <commit, PR, or NOT VERIFIED>

* Data / DB Baseline:
  <read-only status, dataset version, hash, row count, or N/A>

* Latest Test Evidence: <focused tests and result>

* Full Suite:
  PASS / FAIL / NOT RUN / UNKNOWN

* Latest Artifacts:

  * <path and digest, if relevant>
  * <path and digest, if relevant>

## 4. Active Constraints And Safety Gates

* DB Access:
  <for example: read-only only / no DB access / explicitly authorized write only>

* Production: <for example: NOT AUTHORIZED>

* Registry / Strategy:
  <for example: no mutation / no new strategy / research-only>

* Git Operations:
  <for example: no branch, worktree, commit, push, merge, cleanup unless explicitly authorized>

* Project-Specific Restrictions:

  * <restriction>
  * <restriction>
  * <restriction>

## 5. Current Decision Gates

| Gate   | Status                         | Evidence / Reason | Required Next Decision |
| ------ | ------------------------------ | ----------------- | ---------------------- |
| <gate> | OPEN / CLOSED / BLOCKED / HOLD | <short evidence>  | <next decision>        |
| <gate> | OPEN / CLOSED / BLOCKED / HOLD | <short evidence>  | <next decision>        |

## 6. Known Risks And Unknowns

* [Confirmed] <confirmed risk or limitation>
* [Inferred] <inference requiring later verification>
* [Unknown] <missing evidence or unresolved question>

## 7. Next Allowed Action

* Allowed Next Action: <one bounded next direction>

* Not Allowed Without New Authorization:

  * <action>
  * <action>
  * <action>

* Required Inputs For Next Task:

  * <CEO decision / clean repo / artifact / DB read authorization / other>

## 8. Short Historical References

Keep at most 5 items.

* <Task ID>: <one-line outcome>; evidence: <artifact or commit>
* <Task ID>: <one-line outcome>; evidence: <artifact or commit>
* <Task ID>: <one-line outcome>; evidence: <artifact or commit>
