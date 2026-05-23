# CTO Roadmap Alignment and System Optimization Analysis

## 1. CTO Review Date

2026-05-23 Asia/Taipei

## 2. Input Sources

Read / referenced:

- [Confirmed] `00-Plan/roadmap/roadmap.md`
- [Confirmed] `00-Plan/roadmap/CTO-Analysis.md`
- [Confirmed] `data/paper_recommendations/p26j_post_window_pair_verification_rerun_20260521.json`
- [Confirmed] `data/paper_recommendations/p26j_daemon_continuity_verification_rerun_20260521.json`
- [Confirmed] `report/p26j_post_window_pair_verification_rerun_20260521.md`
- [Confirmed] `report/p26j_daemon_continuity_verification_rerun_20260521.md`
- [Confirmed] `00-BettingPlan/20260521/p26j_post_window_pair_verification_rerun_20260521.md`
- [Confirmed] `git rev-parse --show-toplevel`
- [Confirmed] `git branch --show-current`
- [Confirmed] `git status --short --branch`
- [Confirmed] `git log --oneline --decorate -12`
- [Confirmed] `rg` context contamination scan for `P48|P49|Stock-Prediction|golden fixture|paper simulation dry-run`
- [Confirmed] User-provided Betting-pool context hygiene handoff report in this conversation.

Not performed:

- [Confirmed] No pytest rerun in this CTO review.
- [Confirmed] No P26K execution.
- [Confirmed] No daemon restart, scheduler change, crawler change, manual API call, raw data modification, production write, PR merge, branch creation, or worktree creation.
- [Confirmed] No `active_task.md` write because the strict allowed-write list only permits `roadmap.md` and `CTO-Analysis.md`.
- [Confirmed] No new worker task prompt emitted because the strict restriction says not to produce a new worker task prompt.
- [Confirmed] No changes made to `00-Plan/roadmap/CEO-Decision.md` even though it is currently modified in the worktree.

## 3. Roadmap Alignment Assessment

| Tag | Finding |
|---|---|
| [Aligned] | Betting project identity is clean: repo root is `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` and branch is `main`. |
| [Aligned] | Recent git log is P26x Betting work ending at `0ccd06d`; no Stock/P48/P49 entries were observed. |
| [Aligned] | `rg` scan across `00-Plan`, `00-BettingPlan`, `report`, and `data/paper_recommendations` found no Stock-Prediction / P48 / P49 contamination. |
| [Aligned] | Returning to P26K matches the previous CTO roadmap: P26J proved daemon cycles existed but fetch did not execute in the closing window. |
| [Aligned] | P25C bootstrap remains correctly blocked because the latest known COMPLETE_PAIR is 219 (<300). |
| [Drift] | Conversation context drifted into Stock-Prediction-System, but repo evidence does not show Betting code/artifact contamination. |
| [Drift] | `active_task.md` and `CEO-Decision.md` are modified in the worktree, but they are outside this CTO scope and were not touched. |
| [Missing] | Roadmap did not yet encode context hygiene as a standing pre-flight for multi-project handoffs. |
| [Missing] | Roadmap did not yet call out the four untracked `scripts/p26j_*.py` files as a commit-scope risk. |
| [Outdated] | Any Stock/P48/P49 content must be ignored for Betting roadmap purposes unless a future scan proves actual contamination. |
| [Blocked] | P26K is not blocked by context hygiene anymore; it is blocked only by execution. P25C, product release, strategy simulation, promotion, and production remain blocked. |

## 4. Completed Work Assessment

### Context Hygiene

- [Confirmed] Repo root check passed: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`.
- [Confirmed] Branch check passed: `main`.
- [Confirmed] Recent log check passed: latest commits are P26x Betting work, ending at `0ccd06d verify(p26j): post-window pair verification rerun - 09:12Z`.
- [Confirmed] Content scan passed: no P48/P49/Stock-Prediction/golden fixture/paper simulation dry-run content found in the checked Betting directories.
- [Confirmed] Current context classification: `BETTING_CONTEXT_CLEAN`.
- [Confirmed] No repo cleanup or contamination repair is needed before returning to Betting P26K.

### P26J Evidence Still Current

- [Confirmed] P26J full post-window verification completed at commit `0ccd06d`.
- [Confirmed] `3469930.1` is `PREGAME_ONLY_NO_CLOSING`: 7 rows, 0 closing rows, `markets=[]`.
- [Confirmed] `3469931.1` is `PREGAME_ONLY_NO_CLOSING`: 8 rows, 0 closing rows, `markets=[]`.
- [Confirmed] `target_pair_delta=0`.
- [Confirmed] COMPLETE_PAIR changed `220 -> 219`, delta `-1`.
- [Confirmed] P25C bootstrap did not run and remains not eligible.
- [Confirmed] Daemon had 8 heartbeat cycles during `07:00Z-09:00Z`.
- [Confirmed] Every closing-window cycle had `fetched=false`.
- [Confirmed] `api_calls_today` stayed at 2 throughout the window.
- [Confirmed] `next_trigger_minutes=null`.

### Worktree State

- [Confirmed] Worktree contains many Betting runtime/daemon/data/output modified files.
- [Confirmed] `00-Plan/roadmap/CEO-Decision.md` is modified but outside this CTO write scope.
- [Confirmed] `00-Plan/roadmap/active_task.md` is modified but outside this CTO write scope.
- [Confirmed] Four untracked P26J scripts exist:
  - `scripts/p26j_phase2_analysis.py`
  - `scripts/p26j_phase3_daemon.py`
  - `scripts/p26j_phase3b_heartbeat.py`
  - `scripts/p26j_phase4_coverage.py`
- [Unknown] Whether the untracked P26J scripts are temporary analysis files or reusable diagnostic tools.

## 5. Unfinished Work Assessment

| Item | Status |
|---|---|
| P26K closing fetch trigger root cause | [Blocked] Not executed. P26J proves `fetched=false`; root cause remains unknown. |
| Source vs trigger separation | [Missing] Need to separate source-side `markets=[]` from fetch-trigger failure. |
| Quota / call limit gate | [Unknown] `api_calls_today=2` was stable; whether this is a hard cap, policy gate, or incidental state is not confirmed. |
| `next_trigger_minutes=null` | [Unknown] Need to know whether null means no scheduled fetch, a scheduler bug, or expected idle state. |
| COMPLETE_PAIR decrease | [Blocked] COMPLETE_PAIR dropped from 220 to 219; reason remains unexplained. |
| P25C bootstrap | [Blocked] Needs COMPLETE_PAIR >=300; latest known value is 219. |
| Untracked P26J script boundary | [Missing] Must be classified during P26K pre-flight and not staged accidentally. |
| Context-lock pre-flight | [Missing] Should become standard for Betting / Stock / Lottery cross-project handoffs. |
| Product recommendation release | [Blocked] MLB/TSL paper recommendations need traceable odds, model probability, edge, source time, risk gate, and validation evidence before release. |
| Strategy optimization / simulation | [Blocked] Requires formal pregame odds, closing line, actual outcome, source trace, and sufficient validation data; no promotion path is open. |

## 6. P0 / P1 / P2 / P3-P10 Reprioritization

| Priority | Phase | Why now |
|---:|---|---|
| **P0** | P26K Closing Fetch Trigger Root Cause Diagnostic | Context hygiene is clean; the direct blocker is still closing-window cycles with `fetched=false` and no closing rows. |
| **P1** | Context-Lock Preflight + Commit-Scope Guard | Cross-project conversation drift happened; future Betting work must stop on Stock/P48/P49 contamination and must not stage runtime files. |
| **P2** | Untracked P26J Script Boundary | Four untracked P26J scripts can pollute commit scope if not explicitly classified. |
| **P3** | Scheduler / Quota / Next Trigger Decision Gate | Only after P26K should the team decide whether to patch scheduler, adjust quota/ops, monitor source, or no-op. |
| **P4** | Heartbeat-vs-Fetch Watchdog Design | Prevents false confidence from daemon heartbeat when fetch does not execute. Design-only until authorized. |
| **P5** | COMPLETE_PAIR Recovery Gate + P25C Bootstrap | Bootstrap remains blocked until COMPLETE_PAIR >=300 and line-comparable filters pass. |
| **P6** | Coverage Stability Audit | COMPLETE_PAIR dropping `220 -> 219` must be explained before trusting coverage trend. |
| **P7** | MLB Prediction Quality Work Re-entry | P29/P30A model work remains useful but should not preempt P26K data-capture root cause. |
| **P8** | TSL Market Paper Recommendation Contract | Keep product design aligned to MLB/TSL paper recommendations; release remains blocked. |
| **P9** | Repo / PR Governance Gate | No new repo/worktree/branch; no protected-branch bypass; keep raw feed/runtime files out of commits. |
| **P10** | Production Proposal Gate | Production remains blocked until formal evidence, live/licensed data path, fail-safe, monitoring, and explicit approval exist. |

Upgraded to P0:

- [Confirmed] P26K closing fetch trigger root-cause diagnostic.

Upgraded to P1:

- [Confirmed] Context-lock preflight and commit-scope guard.

Upgraded to P2:

- [Confirmed] Untracked P26J script boundary classification.

Downgraded:

- [Confirmed] Repeating context hygiene as a standalone task; it is complete unless contamination reappears.
- [Confirmed] P29/P30A Orchestrator validation; useful later, but not today's direct blocker.
- [Confirmed] External SP/bullpen/batting implementation; contract/design only until data gates are healthier.

Paused:

- [Confirmed] P25C bootstrap until COMPLETE_PAIR >=300.
- [Confirmed] Scheduler patch, daemon restart, crawler modification, live API call, manual snapshot fabrication unless explicitly authorized.
- [Confirmed] Optimizer promotion, champion replacement, production proposal, paper recommendation release, and profitability claims.

Retired:

- [Confirmed] Treating Stock-Prediction conversation drift as Betting repo contamination after clean grep/log evidence.
- [Confirmed] Including P48/P49/Stock summaries in Betting handoffs.
- [Confirmed] Producing worker prompts from CTO roadmap analysis while the strict restriction forbids worker prompts.

## 7. Critical Blockers

### Blocker 1: Closing Fetch Did Not Execute During True Window

- Impact: CLV pair formation, closing-line evidence, P25C bootstrap, strategy validation, and paper recommendation credibility.
- Why blocker: P26J observed 8 daemon cycles in `07:00Z-09:00Z`, but all had `fetched=false`; `api_calls_today=2` did not change.
- Risk if ignored: The system may appear operational while collecting no closing evidence.
- Priority: P0.
- Acceptance: P26K classifies the cause as trigger rule, quota/call limit, `next_trigger_minutes`, timezone computation, schedule target, source state, governance flag, or inconclusive.

### Blocker 2: Commit-Scope Risk From Dirty Runtime Files

- Impact: repo governance and review safety.
- Why blocker: Worktree includes many runtime/daemon/data/output modifications plus modified roadmap governance files outside this CTO scope.
- Risk if ignored: raw feed, generated output, `CEO-Decision.md`, or `active_task.md` could be committed unintentionally.
- Priority: P1.
- Acceptance: Future task stages only whitelisted artifacts and explicitly reports ignored dirty files.

### Blocker 3: Untracked P26J Scripts

- Impact: repo hygiene and future artifact scope.
- Why blocker: Four untracked `scripts/p26j_*.py` files may be temporary scratch scripts or reusable diagnostic tools.
- Risk if ignored: They may be accidentally committed or deleted without a policy decision.
- Priority: P2.
- Acceptance: P26K classifies them as temporary, reusable diagnostic candidates, or unknown without staging/deleting unless authorized.

### Blocker 4: COMPLETE_PAIR Is 219, Below Bootstrap Threshold

- Impact: P25C bootstrap, CLV significance checks, strategy simulation, and any model-to-bet validation.
- Why blocker: Required threshold is 300; latest known value is 219.
- Risk if ignored: Bootstrap or strategy conclusions would be underpowered and misleading.
- Priority: P5.
- Acceptance: Bootstrap remains blocked until COMPLETE_PAIR >=300 and line-comparable filters pass.

### Blocker 5: Context Drift Risk

- Impact: roadmap reliability across Betting / Stock / Lottery projects.
- Why blocker: Conversation-level cross-project drift already occurred.
- Risk if ignored: Wrong project summaries or artifacts may be written into Betting.
- Priority: P1.
- Acceptance: Project context lock and contamination grep are part of future pre-flight when project switching risk exists.

## 8. Recommended System Optimization Directions

### Direction 1: Context-Locked P26K Root-Cause Isolation

- Roadmap phase: P0/P1.
- Why important: It resumes the correct Betting technical path after context hygiene clears.
- Maturity gain: Converts "daemon alive but no fetch" into a concrete operational classification.
- Expected benefit: Enables correct next action: scheduler patch, quota fix, source monitor, or no-op.
- Risk: Root cause may remain inconclusive without deeper logs.
- Acceptance: P26K produces one primary classification and keeps Stock/P48/P49 content out of Betting artifacts.
- Priority: P0.

### Direction 2: Commit-Scope and Untracked Script Hygiene

- Roadmap phase: P1/P2.
- Why important: Dirty runtime files and untracked scripts are the easiest path to accidental repo pollution.
- Maturity gain: Makes artifact-only work auditable.
- Expected benefit: Cleaner commits and less handoff ambiguity.
- Risk: Overly strict staging may delay useful diagnostic script preservation.
- Acceptance: Future P26K commit is whitelist-only; `scripts/p26j_*.py` are classified but not staged unless explicitly scoped.
- Priority: P1.

### Direction 3: Heartbeat-vs-Fetch Observability

- Roadmap phase: P4.
- Why important: P26J proves daemon health is not equivalent to fetch execution.
- Maturity gain: Adds a future detection layer for closing-window silent failures.
- Expected benefit: Reduces delayed discovery after windows close.
- Risk: If implemented too soon, it may add alert noise; keep design-only until P26K classifies root cause.
- Acceptance: Defined alert condition for "closing window active + heartbeat present + fetched=false + no API-call increment".
- Priority: P2/P4.

### Direction 4: Bootstrap Gate Discipline and Coverage Stability

- Roadmap phase: P5/P6.
- Why important: Strategy validation needs sufficient, stable, line-comparable data.
- Maturity gain: Prevents underpowered CLV conclusions and explains pair-count drift.
- Expected benefit: Cleaner evidence before simulation/optimizer work.
- Risk: Slows product-facing output, but correctly protects validity.
- Acceptance: COMPLETE_PAIR threshold and coverage deltas are machine-readable in reports.
- Priority: P3.

### Direction 5: Product / Strategy Lane Gating

- Roadmap phase: P7/P8/P10.
- Why important: The project has two clear product lanes: MLB prediction/paper recommendations and strategy simulation. Both require reliable formal data.
- Maturity gain: Keeps roadmap pointed at product value without jumping over validation.
- Expected benefit: Paper recommendation rows eventually include model probability, odds, edge, source, generated time, risk gate, and `paper_only=true`.
- Risk: Product release remains delayed until capture reliability improves.
- Acceptance: No recommendation release, promotion, or production proposal until data source trace and validation gates clear.
- Priority: P3+.

## 9. Roadmap Changes Applied

- [Confirmed] Updated `00-Plan/roadmap/roadmap.md` with a new top section `0D. Latest CTO Update - Context Hygiene Clean, Return To P26K`.
- [Confirmed] Updated active marker to `CTO_CANONICAL_ROADMAP_CONTEXT_CLEAN_RETURN_TO_P26K_20260523`.
- [Confirmed] Updated CTO review date to 2026-05-23.
- [Confirmed] Marked `BETTING_CONTEXT_CLEAN` as the current context state.
- [Confirmed] Marked P26K as still not executed and still P0.
- [Confirmed] Added context-lock preflight and untracked P26J script boundary as P1/P2 governance priorities.
- [Confirmed] Kept P25C bootstrap blocked at latest known COMPLETE_PAIR=219.
- [Confirmed] Did not write `active_task.md` because it is outside the strict allowed-write list.
- [Confirmed] Did not emit a worker task prompt because the strict instruction forbids producing a new worker task prompt.
- [Confirmed] Did not modify `CEO-Decision.md`.

## 10. Risks / Unknowns

- [Unknown] Whether `api_calls_today=2` is a hard quota, a daily policy cap, or incidental.
- [Unknown] Whether `next_trigger_minutes=null` is expected idle behavior or a scheduler bug.
- [Unknown] Whether source-side `markets=[]` would have persisted if the API fetch had actually run in the closing window.
- [Unknown] Why COMPLETE_PAIR decreased from 220 to 219.
- [Unknown] Whether the four untracked `scripts/p26j_*.py` files should be committed later, ignored, or removed.
- [Confirmed] Betting context hygiene is clean as of this review.
- [Confirmed] P25C bootstrap remains invalid at latest known COMPLETE_PAIR=219.
- [Confirmed] Tests were not rerun by this CTO analysis.
- [Confirmed] Current worktree contains many runtime/data/output dirty files plus modified files outside this CTO scope; future commits must be whitelist-only.

## 11. CTO Final Recommendation

The Betting repo is context-clean. Do not spend the next cycle on more Stock/P48/P49 contamination handling unless a new scan finds evidence.

Today should not run P25C bootstrap, P29/P30A model repair, strategy optimizer, paper recommendation release, scheduler patch, daemon restart, live API call, crawler modification, champion replacement, production proposal, or worker-prompt generation from CTO analysis.

The next highest-value system direction is still **P26K Closing Fetch Trigger Root Cause Diagnostic**, read-only and context-locked:

- Verify Betting context at pre-flight.
- Verify P26J commit and artifacts.
- List but do not stage `scripts/p26j_*.py`.
- Reconstruct the `07:00Z-09:00Z` closing-window timeline.
- Determine why every cycle had `fetched=false`.
- Separate source unavailability from trigger/quota/scheduler/timezone/governance causes.
- Keep COMPLETE_PAIR and bootstrap gates explicit.

Final classification: `CTO_ROADMAP_UPDATED_WITH_RISKS`

## 12. 10 行內 CTO 摘要

1. Betting context hygiene is clean: repo=`Betting-pool`, branch=`main`.
2. Recent git log is P26x Betting work; no Stock/P48/P49 contamination found.
3. P26K has not executed; no P26K artifacts were found.
4. P26J remains latest technical evidence at commit `0ccd06d`.
5. P26J showed both targets are `PREGAME_ONLY_NO_CLOSING`.
6. COMPLETE_PAIR latest known value is 219, so P25C bootstrap is blocked.
7. P0 remains P26K read-only closing fetch trigger root-cause diagnostic.
8. P1 is context-lock preflight and whitelist-only commit scope.
9. P2 is untracked `scripts/p26j_*.py` boundary classification.
10. No active_task write, no worker prompt, no daemon restart, no scheduler patch, no production proposal.
