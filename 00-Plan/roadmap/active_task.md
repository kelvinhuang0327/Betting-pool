# Active Task: P202G-A-PACKAGE — Policy Evidence and Governance Six-File Packaging

## Status

`PLAN_ONLY_REQUIRES_TASK_SPECIFIC_AUTHORIZATION`

## Supersedes

This task replaces the prior active task "P202G-A Source Policy Clarification Evidence
Packet" (`AUTHORIZED_READ_ONLY_AUDIT`). P202G-A was executed and completed:

- Evidence packet: `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`
  — Final classification `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`.
- Independent adversarial review: `report/p202g_a_source_policy_clarification_independent_review_20260614.md`
  — Historical classification `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`.
- Evidence-packet narrow fix completed and independently verified:
  `P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE`.
- Governance alignment (this round): exactly four governance files updated to reflect
  the above completed policy work; HEAD / staged files / open PR count unchanged.

P202G-A is closed. This is the sole next active task.

## Background

P202F (`report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md`)
found the MLB StatsAPI source technically documented but not legally authorized for
automated/derived use. Final classification: `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`.

P202G-A gathered official policy evidence and found an explicit automated-scripts
prohibition in MLB.com Terms of Use (2025-03-11):
> "use automated scripts to collect information from or otherwise interact with the MLB
> Digital Properties"

The restriction's applicability to `statsapi.mlb.com` is `STRONGLY_SUPPORTED_INFERENCE`
(Terms §1 scope clause + official definition + openapi "Official API for Major League
Baseball." — Terms does **not** directly name that hostname; direct hostname naming =
`NOT_ESTABLISHED`).

No purpose-matched licensing path was established:

- `legaldepartment@mlb.com` = DMCA Copyright Agent / general-legal fallback (§2 "Copyright
  Agent"); **not** a data/API licensing office.
- `registrationsupport@mlb.com` = technical registration support only.
- StatsAPI self-registration (`inside.mlb.com/UserRegistrationForm/?GROUP=StatsAPI`) =
  account entry only, not a usage license.

Live transport (P202G) remains **HOLD**. The minimum allowed technical boundary is
**fixture-only**. No one-shot dry run, recurring collector, historical backfill, provider
unlock, or live implementation is authorized.

## Task Type

`COMMIT_PR_PACKAGING`

## Goal

Package exactly six files into a single commit and pull request that records the completed
P202G-A source-policy evidence work, independent review, narrow fix, and governance
alignment.

## Exact Future Package — Exactly 6 Files

1. `00-Plan/roadmap/roadmap.md`
2. `00-Plan/roadmap/CTO-Analysis.md`
3. `00-Plan/roadmap/active_task.md`
4. `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md`
5. `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`
6. `report/p202g_a_source_policy_clarification_independent_review_20260614.md`

## Hard Boundaries

- P202F report (`report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md`)
  must **not** be included in this package.
- No source/test/config/fixture files.
- No live endpoint, no MLB data collection, no DB/runtime write, no live implementation.
- No provider unlock, no credential acquisition or use.
- No production mutation, no registry mutation, no `controlled_apply`.
- No automatic branch/stage/commit/push/PR authorization from this file alone.
  A separate explicit task prompt with those authorizations is required before any of
  those git actions may proceed.

## Phase 0 Verification (for the future packaging round)

Run:

1. `git rev-parse HEAD`
2. `git rev-parse origin/main`
3. `git branch --show-current`
4. `git status --short`
5. `git diff --cached --name-only`
6. `gh pr list --state open`

Expected:

- branch `main`
- HEAD = origin/main (verify actual value at execution time)
- no staged files
- open PR count 0
- dirty/untracked files ≤ tolerated runtime list + the 6 packaging files + other
  authorized uncommitted files listed in `agent_bootstrap/CURRENT_STATE.md`

## STOP Conditions (for the future packaging round)

STOP if:

- branch is not `main` or HEAD is detached
- staged files exist from a prior session
- dirty tree includes unexpected unwhitelisted files
- any of the 6 packaging files was found to have changed unexpectedly since governance
  alignment
- any source/test/config/fixture file requires modification to complete packaging
- the task would require a seventh file or P202F inclusion

## P202G-A Policy State (for reference in the packaging commit message)

| Field | Value |
|---|---|
| Automated restriction | EXPLICITLY_PROHIBITED (official MLB.com Terms 2025-03-11) |
| StatsAPI applicability | STRONGLY_SUPPORTED_INFERENCE (Terms does not directly name `statsapi.mlb.com`) |
| Direct hostname naming | NOT_ESTABLISHED |
| Written permission obtained | NO |
| Purpose-matched licensing path | NOT_ESTABLISHED |
| `legaldepartment@mlb.com` | DMCA Copyright Agent / general-legal fallback only (§2) |
| `registrationsupport@mlb.com` | Technical registration support only |
| One-shot dry run | NOT AUTHORIZED |
| Recurring collector | NOT AUTHORIZED |
| Live transport | HOLD |
| Final packet classification | `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND` |
| Independent review historical classification | `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX` |
| Narrow fix classification | `P202G_A_EVIDENCE_PACKET_NARROW_FIX_COMPLETE` |

## Required Completion Check (for the future packaging round)

1. 是否真的完成
2. Branch / HEAD / origin/main agreement
3. Staged file whitelist = exactly 6 files (listed above), none others
4. Commit created (not amended), branch pushed to origin
5. PR opened against `main`
6. P202F excluded from package
7. Source/test/config/fixture unchanged
8. No live endpoint / DB / runtime / production mutation
9. CI status
10. Final Classification

## Final Classification (for the future packaging round)

- `P202G_A_PACKAGE_COMMIT_PR_COMPLETE`
- `P202G_A_PACKAGE_BLOCKED_BY_PREFLIGHT`
- `P202G_A_PACKAGE_BLOCKED_BY_DIRTY_TREE`
- `P202G_A_PACKAGE_BLOCKED_BY_SCOPE_EXPANSION`
- `P202G_A_PACKAGE_BLOCKED_BY_CI_FAILURE`
