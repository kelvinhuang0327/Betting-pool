# Betting-pool Canonical Roadmap

**CTO review date:** 2026-06-03 Asia/Taipei
**Canonical repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
**Observed branch:** `main`
**Mode:** `paper_only=true`, `production_ready=false`, `NO_REAL_BET=true`
**Roadmap status:** canonical roadmap maintained in-place; latest section `0K` supersedes `0J` for current execution priority.
**Active marker:** `CTO_CANONICAL_ROADMAP_P140_MERGED_PRODUCT_INTENT_DIRTY_TREE_POLICY_NEXT_20260603`

---

## 0K. Latest CTO Update - P140 Merged, Product Intent Recentered

This section supersedes section 0J for current execution priority. PR #4 merged the P122-P140 governance chain into `origin/main`, and local `main` is synchronized at `9a0ddc205b3f6b6cb4499dc214391bd4d886db2d`. The user has now restated the Betting product intent in two concrete lanes:

1. MLB pregame prediction strategy and paper-only betting-advice candidates mapped to Taiwan Sports Lottery bettable markets.
2. Backtesting, score simulation, and learning loops for existing prediction strategies, with strategy adjustment based on observed prediction success.

Because the local worktree still contains many pre-existing modified/untracked files, the next execution step should be a read-only dirty-tree cleanup policy / classification pass before opening P141 or any broader implementation.

### 0K.1 Canonical Product Intent

| Lane | Core goal | Current allowed state | Blocked until |
|---|---|---|---|
| Lane A: MLB pregame market advisory | Produce pregame strategy, prediction, and paper-only recommendation candidates for Taiwan Sports Lottery bettable markets such as moneyline, run line, totals, first-five, and other supported markets. | Paper-only market contracts, recommendation-row schemas, validation gates, provider/legal evidence gates, and diagnostic reports. | Legal provider authorization, lawful odds/source trace, market availability validation, edge validation, risk controls, and explicit approval. |
| Lane B: strategy backtest / simulation / learning | Evaluate existing strategies through outcome backtests, simulated score distributions, replay, drift checks, and learning matrices so strategy weights can adapt to prediction success. | Outcome-only diagnostics, score simulation runners, replay consistency, drift alert governance, learning backlog, and dashboard contracts. | Sufficient outcome coverage, stable prediction conventions, regression confidence, and explicit approval before any production or real-money use. |

### 0K.2 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Canonical repo `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`, git-dir `.git`. |
| HEAD | [Confirmed] Local `main` and `origin/main` are both `9a0ddc205b3f6b6cb4499dc214391bd4d886db2d`. |
| PR state | [Confirmed] PR #4 was merged after required `replay-default-validation` passed; direct push to `main` remains blocked by branch protection. |
| P122-P140 state | [Confirmed] Provider/legal evidence governance, replay/escalation governance, drift alert governance, and P140 signoff evidence packet gate are merged. |
| Product direction | [Confirmed] The user direction is two-lane: Taiwan Sports Lottery MLB pregame market advisory plus strategy backtest/simulation/learning. |
| Worktree | [Confirmed] Dirty tree remains the immediate workflow risk: current observed status count is 97 entries, with 86 modified and 11 untracked paths. |
| Tests | [Confirmed from handoff] Targeted P118-P140 chain passed; PR CI passed. [Confirmed] Full repository regression remains NOT RUN. |
| Release branch | [Confirmed] Remote/local release branch `release/p122-p140-and-reviewed-backlog` still exists and should not be deleted without explicit authorization. |
| Governance | [Confirmed] `paper_only=true`, `diagnostic_only=true`, `production_ready=false`, `NO_REAL_BET=true`; no real bet, no production recommendation, no stake/profit/Kelly deployment. |

### 0K.3 Reprioritized P0-P10 From P140 Merge

| Priority | Phase / direction | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | Dirty Tree Cleanup Policy / Classification | Workflow safety | Classify all modified/untracked files before P141 so future agents do not stage runtime, generated, or unrelated artifacts. | Read-only report maps each dirty path to keep/restore/ignore/review/unknown with risk and suggested next action; no file mutation. |
| **P0** | Product Intent Lock | Roadmap governance | Keep every future phase tied to the two canonical product lanes: Taiwan Sports Lottery MLB pregame advisory and strategy learning. | Roadmap, active task, and future prompts state the two lanes and their current blockers. |
| **P1** | Lane A Market Advisory Architecture Review | Product maturity | Re-evaluate P112-P140 against the concrete Taiwan Sports Lottery market surface and identify the smallest missing paper-only contract. | Readiness matrix covers supported markets, required odds/source fields, prediction inputs, recommendation-row gates, and blocked real-use conditions. |
| **P1** | Lane B Backtest / Simulation Learning Contract | Strategy learning | Convert existing outcome-only score/backtest/simulation artifacts into a coherent learning-loop contract. | Contract defines strategy identity, prediction record, simulated score output, success metrics, drift triggers, and learning adjustments. |
| **P1** | Agent Bootstrap / Task Template Placement | Agent governance | Resolve the current bootstrap-file location mismatch and make future workers read a stable shared entry document. | Files live in the agreed roadmap/bootstrap location, or the roadmap explicitly documents the canonical location. |
| **P2** | Full Regression Policy | QA governance | Current PR CI and targeted tests passed, but full regression was not run. | Future execution reports dedicated, targeted, and full-regression status as PASS/FAIL/NOT RUN with rationale. |
| **P2** | Release Branch Cleanup Decision | Git hygiene | PR #4 is merged but the release branch remains. | Branch cleanup is performed only after explicit authorization, or documented as intentionally retained. |
| **P3** | Legal Provider / Real Odds Evidence Gate | Data rights | Product market advisory cannot mature to real odds or real recommendations without lawful provider evidence. | Provider approval, license scope, source trace, and evidence validation pass; secrets remain outside the repo. |
| **P4** | Coverage Accumulation Watch | Data quality | Outcome learning and simulation confidence depend on enough real outcomes and stable upstream coverage. | Reruns occur only when meaningful canonical/outcome deltas exist or a scheduled review threshold is reached. |
| **P5** | Market Edge / CLV Reentry | Odds-dependent validation | EV/CLV/market-edge analysis is useful only after legal odds/source trace unlocks. | Legal odds dataset passes validation; analysis remains paper-only until further approval. |
| **P6-P10** | Production Proposal Gate | Governance | Production remains a late-stage gate, not an implied next step. | Prediction, data rights, market edge, risk control, monitoring, and explicit approval all pass before production use. |

### 0K.4 Immediate Next Task Recommendation

The next task should be **Dirty Tree Cleanup Policy / Classification Plan After PR #4 Merge**. It should be read-only and should not run tests unless needed for classification. It should not restore, delete, stash, stage, commit, push, or branch-switch. Its output should identify which paths are runtime/cache/generated artifacts, which are roadmap/governance files, which are reports/data outputs, which are probe scripts, and which require human decision.

P141 should wait until this classification exists, unless the user explicitly authorizes a narrowly whitelisted write scope.

---

## 0J. Latest CTO Update - P121 Done, Readiness Review Before More Buildout

This section supersedes section 0I for current execution priority. P94-P100 closed the high-FIP prediction lane into diagnostic-only tracking with limited coverage and production blocked. P101-P121 then realigned the product into two lanes and built a paper-only market / recommendation / provider-authorization contract chain. The next maturity step is not another placeholder; it is a readiness review that decides whether Lane A is structurally ready for a later dry-run or whether legal/provider/data blockers still dominate.

### 0J.1 Current System Truth

| Area | Status |
|---|---|
| Pre-flight | [Confirmed] Current CTO session is canonical repo `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `70623ed feat(P121): Provider Authorization Evidence Placeholder - P121_PROVIDER_AUTHORIZATION_EVIDENCE_PLACEHOLDER_READY_WITH_BLOCKERS`. |
| Roadmap drift | [Outdated] Previous latest roadmap section `0I` was post-P93 and no longer reflects HEAD. P94-P121 have since landed on `main`. |
| CEO decision state | [Outdated] `CEO-Decision.md` is post-P93/P94 and does not contain a final CEO裁決 after P101-P121. CTO cannot update that file. |
| Handoff source | [Confirmed] User-provided handoff states P101-P121 completed, P121 committed at `70623ed`, P121/P120 dedicated tests pass, push not run. |
| P94-P100 state | [Confirmed] P94 `P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY`; P95 `P95_FIP_STRATIFIED_SHADOW_TRACKER_READY_WITH_LIMITED_COVERAGE`; P96 stable but coverage limited; P97 signal pass but production blocked; P98-P100 wait/accumulate because no new outcome/coverage rows. |
| Product realignment | [Confirmed] P101 created two lanes: Lane A Taiwan Sports Lottery pregame market contract; Lane B outcome-only strategy backtest / learning / dashboard. |
| Lane B outcome-only work | [Confirmed] P102-P111 created scorecard, learning matrix, score simulation design/runner/review, strategy adjustment backlog, diagnostic tracking report, drift snapshot, dashboard contract, and dashboard fixture. |
| Lane A market-contract work | [Confirmed] P112-P121 created market-contract gap review, paper-only market schema, legal odds requirements, paper-only odds ingestion fixture, recommendation row dry-run contract, recommendation row fixture, validation gate, violation fixture, provider authorization checklist, and authorization evidence placeholder. |
| P121 blocker truth | [Confirmed] P121 explicitly says no provider is approved, no authorization evidence is present, all provider / odds / recommendation / production use remains BLOCKED. |
| Tests | [Confirmed from handoff and reports] P121 dedicated tests pass; P120 dedicated tests pass. [Unknown] P121 full repository regression status. |
| Worktree | [Confirmed] `git status --short` is dirty; count observed as 95 entries during this CTO review. Scope includes roadmap governance files plus many runtime/data/output/report files. |
| Governance | [Confirmed] Current artifacts preserve paper-only, diagnostic-only, `production_ready=false`, no real bet, no odds/EV/CLV/Kelly/stake/profit/recommendation. |
| CTO write scope | [Confirmed] This CTO review may update only `roadmap.md` and `CTO-Analysis.md`. No `active_task.md`, no `CEO-Decision.md`, no production/registry/data writes. |
| Worker prompt conflict | [Blocked] User later asks for a worker task prompt, but strict instruction also says "do not produce a new worker task prompt" and CTO may only update two files. CTO therefore records the conflict and does not emit or write a worker prompt. |

### 0J.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P94-P100 followed the P93 finding: high-FIP signal was qualified, tracked with coverage limits, and kept out of production. |
| [Aligned] | P101 correctly addressed the user's two product goals by separating Lane A market/recommendation contracts from Lane B outcome-only strategy learning. |
| [Aligned] | P112-P121 advanced Lane A without using real odds, EV, CLV, Kelly, production logic, or recommendation output. |
| [Aligned] | P118/P119 correctly make unsafe recommendation-row states BLOCKED rather than silently allowed. |
| [Aligned] | P120/P121 correctly keep provider authorization as missing and blocked instead of pretending a placeholder is evidence. |
| [Drift] | Roadmap `0I` still treated P94 as future work even though P94-P121 are now committed. |
| [Drift] | P100 said "do not run a new phase today" due outcome wait-state, but P101-P121 product-contract work proceeded; this was justified by user product direction, but should be recorded as a lane shift. |
| [Drift] | The artifact chain has grown quickly; continuing P122/P123 as more placeholder files risks process motion without product readiness. |
| [Missing] | Roadmap lacked a post-P121 readiness review to evaluate P112-P121 as one Lane A system, not isolated phase artifacts. |
| [Missing] | Roadmap lacked a compact artifact/phase catalog for P101-P121, increasing weak-worker citation and handoff risk. |
| [Missing] | Roadmap lacked a post-P121 CEO decision requirement before generating a new worker prompt or opening a new execution phase. |
| [Outdated] | P93/P94 as current next work is outdated. They remain historical foundation, not today's execution priority. |
| [Outdated] | Treating dirty-tree cleanup as an independent P0 is outdated after staged-files-only governance; dirty tree remains a P2 governance risk. |
| [Blocked] | Product recommendation, market-edge, EV/CLV, Kelly, stake, profit, and production remain blocked by missing legal provider authorization and missing real legal odds data. |
| [Blocked] | Full-season / robust learning claims remain blocked by partial 2026 coverage and no new outcome rows since the P98-P100 wait-state checks. |
| [Blocked] | A worker task prompt based on CEO final裁決 is blocked because no post-P121 CEO final decision is present and CTO prompt generation is explicitly prohibited in this request. |

### 0J.3 Reprioritized P0-P10 From P121

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P122 Paper-Only Recommendation Readiness Review | Product maturity / verification | Review P112-P121 as a single Lane A system and decide whether the chain is ready for a later paper-only dry-run gate, provider evidence gate, or should stop for legal/data blockers. | Readiness matrix covers markets, schema, odds source, recommendation row, validation gate, provider authorization, blockers, allowed next actions, prohibited actions; no new odds/recommendation/production. |
| **P0** | Legal Provider Authorization and Real Legal Odds Blocker | Data rights / product safety | No provider is approved and no authorization evidence exists; without this, market-edge and Taiwan lottery recommendation cannot mature. | Signed/legal evidence and license scope exist, provider approval is validated, source trace and audit requirements pass; until then status remains BLOCKED. |
| **P1** | P101-P121 Artifact Catalog / Phase Index | Roadmap governance | Prevent weak-worker drift across many scripts, tests, summaries, reports, commits, and classifications. | Single index maps phase -> objective -> artifact -> report -> test -> commit -> classification -> blocker; read-only over existing artifacts. |
| **P1** | Provider Evidence Validation Gate | Safety gate | Ensure the P121 placeholder can never be misread as real authorization. | Gate validates `authorization_evidence_present=false`, `provider_approved=false`, no secrets/auth URLs/contracts, and all markets remain BLOCKED until real evidence exists. |
| **P1** | Agent Entry and Staged-Files-Only Governance | Workflow orchestration | Preserve canonical repo/main entry while tolerating unrelated dirty runtime files without accidental staging. | Future tasks stop outside canonical repo/main and report staged whitelist; unrelated runtime/data/output files are not staged. |
| **P2** | P121 Targeted / Broader Regression Policy | Test governance | P121/P120 dedicated tests passed, but full regression for P121 is unknown. | P122 or next authorized QA step records dedicated, targeted P101-P121, and full-regression status as PASS/FAIL/NOT RUN with rationale. |
| **P2** | Lane B Outcome-Only Learning Cadence | Strategy learning | Keep outcome-only scorecard/dashboard useful without forcing new phases when no new rows exist. | Rerun only when new outcome/canonical rows exist or a scheduled review threshold is met; no odds or production mutation. |
| **P3** | Repo Hygiene Sweep | Repo governance | Dirty and untracked files remain a persistent commit-risk, but not today's product maturity blocker. | Separate hygiene decision classifies quarantine/gitignore/archive actions; no runtime/data artifacts committed accidentally. |
| **P4** | 2026 Coverage Accumulation Watch | Data quality | High-FIP and outcome-only claims remain limited by 828/2430 schedule coverage and March-May outcomes. | Coverage/outcome deltas trigger rerun; otherwise wait/accumulate is reported without new buildout. |
| **P5** | FIP-Stratified Shadow Tracker Maintenance | Monitoring | Maintain the high/mid/low FIP diagnostic boundary from P94-P96. | Tracker stays diagnostic-only, coverage-limited, and not a recommendation surface. |
| **P6** | Recommendation Row Dry-Run Readiness Gate | Product contract | Only after P122 says Lane A is ready should a dry-run gate be considered. | Dry-run uses fixtures/contracts only; no real odds, no EV/CLV/Kelly, no recommendation output unless legal gates unlock. |
| **P7** | Market-Edge Reentry | Odds-dependent validation | Resume P80-P82 style market-edge only after legal odds dataset exists. | Dataset passes legal/source-trace/policy validation; aggregate analysis only until further approval. |
| **P8** | Calibration / Refit Gate | Model reliability | Refit is not the current blocker and could create false maturity if run before data and market gates. | Any calibration remains OOS, diagnostic-only, and separately authorized after segment and data coverage gates. |
| **P9** | Roadmap / CEO Decision Hygiene | Governance | Roadmap, CTO analysis, CEO decision, and active task must not drift across phase bursts. | Post-P121 CEO decision is issued or marked absent; CTO/worker scopes stay explicit. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until prediction, data rights, market-edge, risk, monitoring, and explicit approval all pass. | `production_ready=false`; no champion replacement, real bet, or Taiwan lottery recommendation. |

### 0J.4 Items Upgraded, Downgraded, Merged, Paused, Retired

- [Confirmed] Upgraded to P0: P122 paper-only recommendation readiness review, because P101-P121 created enough contract surface that the next valuable step is system validation, not another placeholder.
- [Confirmed] Upgraded to P0 blocker: legal provider authorization / real legal odds evidence, because product recommendation cannot mature without lawful market data.
- [Confirmed] Upgraded to P1: P101-P121 artifact catalog / phase index, because artifact sprawl is now a weak-worker and roadmap-governance risk.
- [Confirmed] Upgraded to P1: provider evidence validation gate, because P121 is only a placeholder and must not be mistaken for authorization.
- [Confirmed] Downgraded: P94/P95/P96 high-FIP diagnostics from next-work to historical foundation; they are done and remain coverage-limited.
- [Confirmed] Downgraded: dirty-tree cleanup as standalone P0; staged-files-only governance makes it a P2/P3 risk unless staging is requested.
- [Confirmed] Downgraded: calibration/refit, market-edge reentry, production proposal, Kelly, EV/CLV, and recommendation output until legal provider/odds gates unlock.
- [Confirmed] Merged: P112-P121 should be reviewed as one Lane A readiness packet.
- [Confirmed] Merged: P102-P111 should be treated as one Lane B outcome-only learning/dashboard packet.
- [Confirmed] Merged: P118-P121 form one recommendation/provider safety suite.
- [Inferred] Paused: further placeholder/spec-only phases until P122 readiness review proves the next contract gap.
- [Confirmed] Retired: wait-only as the entire roadmap after P100; product-contract work can continue, but only when it directly reduces product maturity uncertainty.

### 0J.5 Critical Blockers

| Blocker | Impact | Why blocker | Risk if ignored | Priority | Acceptance |
|---|---|---|---|---|---|
| No legal provider authorization / no real legal odds | Product, data rights, market-edge, recommendations | P121 says no provider approved and no authorization evidence present. | System could imply betting readiness without lawful odds/source evidence. | P0 | Legal/provider evidence exists, passes validation, secrets remain outside repo, market scopes are authorized. |
| No post-P121 readiness review | Product maturity and roadmap quality | P112-P121 created many artifacts but no system-level decision about readiness. | More phases may accumulate without clarifying whether Lane A can advance. | P0 | Readiness matrix names blockers, allowed next actions, prohibited actions, and the next gate. |
| P121 full regression unknown | Test confidence | Dedicated P121/P120 tests pass, but full P121 regression was not confirmed in handoff. | Hidden cross-phase regression may be missed. | P2 | Dedicated, targeted, and full-regression status is recorded as PASS/FAIL/NOT RUN with rationale. |
| Post-P121 CEO decision absent | Governance / orchestration | Existing CEO decision is post-P93/P94, not post-P121. | A new worker prompt cannot honestly claim CEO final裁決. | P0/P9 | CEO post-P121 decision exists or roadmap explicitly marks it absent. |
| Artifact sprawl | Agent workflow and auditability | P101-P121 generated many scripts/tests/reports/summaries. | Weak workers may cite wrong artifacts, repeat phases, or bypass blockers. | P1 | Phase index maps all P101-P121 artifacts and classifications. |
| Dirty worktree | Commit safety | Current `git status --short` remains dirty across governance, runtime, data, output, and report files. | Future commits may stage unrelated artifacts. | P2/P3 | Staged-files-only governance plus optional separate hygiene sweep. |
| Partial 2026 coverage / no new outcomes | Data quality and learning validity | P98-P100 confirmed no material new row deltas; 2026 schedule coverage remains limited. | Strategy learning may overfit March-May partial coverage. | P4 | Rerun only when outcome/canonical coverage changes or review threshold is met. |

### 0J.6 Today Focus

1. Treat P121 as current HEAD and P94-P121 as completed historical phases.
2. Do not create a new worker task prompt or `active_task.md` in this CTO step; strict CTO scope forbids it.
3. Make the next CTO-recommended execution direction P122 Paper-Only Recommendation Readiness Review, pending a post-P121 CEO decision.
4. Keep Lane A blocked for all real odds, EV/CLV, Kelly, recommendation, stake/profit, and production until legal provider authorization and real legal odds pass gates.
5. Consolidate P101-P121 artifacts before any further placeholder growth.

Product direction remains two-lane:

- Lane A: Taiwan Sports Lottery pregame market/recommendation contract chain, currently paper-only and blocked by legal provider/odds evidence.
- Lane B: MLB outcome-only strategy learning and score/dashboard work, currently diagnostic-only and limited by partial 2026 coverage / no new outcome rows.

---

## 0I. Latest CTO Update - P93 Done, Dirty-Tree Decision Before P94

This section supersedes section 0H for current execution priority. P84G-P91 remain important correctness and prediction-only validation history, but HEAD has advanced through P93. The next implementation is blocked until dirty-tree policy is decided.

### 0I.1 Current System Truth

| Area | Status |
|---|---|
| Pre-flight | [Confirmed] Current CTO session is canonical repo `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`, git-dir `.git`. |
| HEAD | [Confirmed] `2221f0f feat(P93): Prediction-Only Coverage and Feature Bias Audit Gate`. |
| Handoff conflict | [Outdated] The provided handoff correctly says P92 completed and proposes P93 next. Repo evidence shows P93 is already committed on `main`; the current implementation blocker is now the dirty-tree decision gate. |
| Dirty tree | [Confirmed] Pre-flight shows 86 modified + 8 untracked files. Modified scope includes roadmap governance files, runtime/data/output artifacts, generated phase reports, and docs. Untracked scope includes repo-root diagnostic scripts and phase/report docs. |
| P91 state | [Confirmed] `P91_TRACKING_ACTIVE_SIGNAL_STABLE`; rows 828, tracked outcomes 808, hit_rate `0.569307`, AUC `0.594315`, coverage_rate `0.975845`, governance all pass. |
| P92 state | [Confirmed] `P92_SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE`; model hit_rate `0.569307`, home baseline `0.524752`, away baseline `0.475248`, predicted_home_ratio `0.509901`. |
| P93 state | [Confirmed] `P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP`; signal is concentrated in high `abs_sp_fip_delta` rows. |
| P93 high-FIP result | [Confirmed] high bucket n=287, hit_rate `0.641115`; low bucket n=178, hit_rate `0.528090`; mid bucket n=343, hit_rate `0.530612`; Q4 hit_rate `0.658416`. |
| P93 monthly evidence | [Confirmed] High-FIP hit_rate is strong in all observed months: Mar `0.7353`, Apr `0.6014`, May `0.6636`; low-FIP April collapses to `0.4868`. |
| Coverage within P93 rows | [Confirmed] 808/808 outcome rows have `sp_fip_delta`; `coverage_gap_ratio=0.0` within the analyzed prediction rows. |
| Season coverage boundary | [Confirmed] Upstream 2026 canonical coverage remains partial at 828/2430 schedule rows; no full-season claim. |
| Active task | [Drift] `active_task.md` points to P93 completion and P94 as next phase, but its historical log contains both `P93_SIGNAL_BROADLY_DISTRIBUTED` and `P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP`. CTO did not modify it. |
| CEO decision state | [Outdated] Current `CEO-Decision.md` is P84G/P84H-era, not a P93/P94 final decision; CTO may not write it. |
| Tests | [Confirmed] This CTO review reran P93 dedicated tests: 65 passed. P83A-P93 targeted regression: 1669 passed / 4 skipped / 2 pytest mark warnings. Full repo regression remains not run. |
| Governance | [Confirmed] P91/P92/P93 summaries preserve paper-only, diagnostic-only, no odds, no EV/CLV/Kelly, no production, no champion replacement, no Taiwan lottery betting recommendation. |
| Worktree governance | [Confirmed] GUI/desktop `claude/*` / `codex/*` worktree execution caused prior STOP loops per handoff. [Confirmed] Current session is not in that bad state. |

### 0I.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P92 correctly followed P91 by ruling out simple home/away baseline and side distribution confounds. |
| [Aligned] | P93 correctly followed P92 by decomposing whether the signal is broad or concentrated in FIP-delta ranges. |
| [Aligned] | P93 preserved prediction-only governance and did not open odds / EV / CLV / Kelly / production lanes. |
| [Aligned] | Active task now points to P94, matching the repo's latest committed phase. |
| [Drift] | The provided handoff is stale about phase head: it treats P92 as latest known, while repo HEAD is already P93. |
| [Drift] | Top roadmap section was still P84G/P84H oriented and did not reflect P91-P93 completion. |
| [Missing] | Roadmap lacked a current P94 decision point for high-FIP subset deeper diagnostics or FIP-stratified paper tracking. |
| [Missing] | Roadmap lacked a current dirty-tree decision gate despite 86 modified + 8 untracked files. |
| [Missing] | Roadmap lacked an explicit cross-agent entry policy: implementation tasks must start from canonical repo + `main` + `.git`, not auto-created GUI worktrees. |
| [Missing] | Roadmap lacked a segment-qualification boundary: high-FIP signal may justify diagnostic tracking, but low/mid-FIP should not be treated as equally strong. |
| [Outdated] | P84H/P92 as "next" is outdated; P94 is the current next diagnostic phase. |
| [Outdated] | Treating the P92 environment blocker as current is outdated for this repo state, though it remains a workflow risk. |
| [Blocked] | Product betting recommendations remain blocked by no real legal odds dataset and prediction-only scope. |
| [Blocked] | Full-season claims remain blocked by partial 2026 canonical coverage and March-May observed outcomes. |
| [Blocked] | Calibration/refit and production segmentation remain blocked until P94 decides how to handle high-FIP concentration. |

### 0I.3 Reprioritized P0-P10 From P93

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | Dirty-Tree Decision Gate | Workflow safety | Decide whether runtime/generated dirty files may be tolerated and how untracked diagnostics/docs should be handled before any new implementation. | Kelvin Q1/Q2/Q3 or equivalent CTO/CEO decision exists; next task can whitelist intentional changes without mixing unrelated artifacts. |
| **P1** | P94 High-FIP Subset Diagnostic / FIP-Stratified Tracking Gate | Prediction validation | Validate whether the high-FIP concentration is stable enough for diagnostic-only tracking and whether low/mid-FIP should be downgraded or excluded from signal claims. | P94 classifies high-FIP stability and low/mid-FIP risk; no odds/EV/CLV/Kelly/production claim. |
| **P1** | Agent Entry / Branch Governance Guard | Workflow orchestration | Prevent repeated STOP loops from GUI/desktop auto-created `claude/*` or `codex/*` worktrees. | Roadmap and future task headers require canonical repo, `main`, git-dir `.git`; worktree branch means STOP. |
| **P2** | Segment Qualification Contract | Model governance | Make P93's high-FIP concentration actionable as a diagnostic boundary without turning it into betting advice. | Reports distinguish high-FIP tracking, low/mid-FIP watch, and blocked product use. |
| **P3** | Targeted + Broader Regression Evidence Policy | Test governance | P93 dedicated tests and P83A-P93 targeted regression passed, but full repo regression was not run. | P94 includes P94 tests and targeted P83A-P94 regression; full repo is run only under explicit policy or marked NOT RUN. |
| **P4** | P84D / 2026 Coverage Watch | Data quality | Wait for probable pitcher coverage to improve before full-season claims or backfill work. | Coverage rerun only when it can change row count; no fabricated FIP values. |
| **P5** | FIP-Stratified Shadow Tracker | Monitoring | If P94 supports it, track high-FIP / mid-FIP / low-FIP separately in prediction-only reports. | Tracker remains diagnostic-only and does not display as recommendation. |
| **P6** | Calibration / Refit Gate | Model reliability | Consider recalibration only after segment stability is understood and not as a partial-sample patch. | Any Platt/isotonic work remains OOS, diagnostic-only, and separately authorized. |
| **P7** | Market-Edge Reentry | Odds-dependent validation | Resume P80-P82 only after real legal odds dataset exists and passes validator/policy gates. | P82 unlock status changes from `BLOCKED_NO_REAL_DATASET`; aggregate-only edge dry-run allowed, no Kelly. |
| **P8** | Paid / Raw Data Governance | Data rights | Preserve P82B/P82C raw paid data and staging guard policy. | No raw paid odds rows, secrets, or row-level proprietary odds are staged. |
| **P9** | Roadmap / Handoff Hygiene | Agent governance | Keep handoff, roadmap, active task, and CEO decision aligned without adding new repos or branches. | Stale handoffs are marked outdated; only authorized files are changed. |
| **P10** | Production Proposal Gate | Governance | Keep production blocked until prediction evidence, real odds evidence, risk controls, monitoring, and explicit approval all exist. | `production_ready=false`; no champion replacement, real bet, or Taiwan lottery recommendation. |

### 0I.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: dirty-tree decision gate, because implementation cannot safely proceed while 86 modified + 8 untracked files are unresolved.
- [Confirmed] Upgraded to P1: P94 high-FIP subset diagnostic / FIP-stratified tracking gate.
- [Confirmed] Upgraded to P1: agent entry / branch governance guard because GUI worktree execution caused repeated STOP loops.
- [Confirmed] Upgraded to P2: segment qualification contract, because P93 shows the signal is not uniformly distributed.
- [Confirmed] Downgraded: P92 execution prompt; P92 is already completed at `fdd341e`.
- [Confirmed] Downgraded: generic "coverage audit" framing; P93 already found no FIP coverage gap inside outcome rows, and the next issue is high-FIP concentration.
- [Confirmed] Paused: calibration/refit, production recommendations, champion replacement, Kelly, EV/CLV, runtime recommendation changes, TSL crawler changes, and odds-file work.
- [Confirmed] Paused: market-edge lane until real legal odds data exists.
- [Confirmed] Retired: treating simple home/away baseline as the primary explanation for P91; P92 ruled it out for current sample.
- [Confirmed] Retired: treating GUI worktree STOP as the current repo blocker; current CTO pre-flight passed, but the guard remains a workflow requirement.

### 0I.5 Critical Blockers

| Blocker | Impact | Why blocker | Risk if ignored | Priority | Acceptance |
|---|---|---|---|---|---|
| Dirty tree unresolved | Commit safety / workflow | 86 modified + 8 untracked files exist, including runtime/generated artifacts and diagnostic scripts/docs. | P94/P95 or cleanup commits may accidentally mix unrelated runtime, report, or probe files. | P0 | Kelvin or CEO/CTO decision resolves runtime dirty tolerance, untracked disposition, and next objective. |
| High-FIP concentration not yet qualified | Prediction validation | P93 shows aggregate signal is pulled mainly by high `abs_sp_fip_delta` rows. | Low/mid-FIP rows may be overclaimed as signal; tracking may overstate model breadth. | P1 | P94 classifies high-FIP stability, low/mid-FIP handling, and diagnostic-only boundary. |
| GUI worktree entry risk | Agent workflow | Prior handoff shows Claude GUI / desktop worktrees repeatedly failed governance pre-flight. | Future workers may waste cycles or produce branch artifacts off canonical main. | P1 | Future task headers enforce repo=`Betting-pool`, branch=`main`, git-dir `.git`; `claude/*`/`codex/*` worktree means STOP. |
| Regression evidence policy gap | QA | P92/P93 test files exist, but this CTO review did not rerun dedicated, targeted, or full repo regression. | Roadmap may overstate current validation confidence. | P3 | P94 reports dedicated tests and targeted regression; full repo is run only under an explicit policy or marked NOT RUN. |
| Partial 2026 season coverage | Data quality | 828 canonical rows cover only a subset of the 2430-game schedule and only March-May outcomes. | Segment results may shift as probable pitcher coverage expands. | P4 | Reports keep partial-season boundary and rerun coverage only with new data availability. |
| Real legal odds absent | Product / market edge | Prediction-only hit_rate does not prove EV, CLV, or Taiwan lottery edge. | Product recommendations could be issued without market evidence. | P7/P10 | P82 remains blocked until real legal odds dataset passes gates; no production claim. |

### 0I.6 Today Focus

1. Treat P92 as completed at `fdd341e` and P93 as completed at `2221f0f`.
2. Resolve dirty-tree policy before any implementation: runtime dirty tolerance, untracked diagnostics/docs disposition, and next objective.
3. After dirty-tree decision, make P94 the next technical focus: high-FIP subset deeper diagnostic or FIP-stratified paper tracking gate.
4. Preserve CLI/canonical-main entry governance for implementation work; GUI/desktop worktree sessions are report-review only unless governance changes.
5. Do not write `active_task.md` or emit a worker task prompt from CTO review because the strict CTO instructions prohibit worker prompts and limit writes to `roadmap.md` / `CTO-Analysis.md`.

Product direction remains two-lane:

- Lane 1: MLB prediction-only strategy validation, now focused on FIP-segment qualification after P93.
- Lane 2: Taiwan sports lottery paper-only recommendation / market-edge validation, still blocked until real legal odds data passes P81/P82 gates.

---

## 0H. Latest CTO Update - P84G Done, P84H Corrected Signal Guard Next

This section supersedes section 0G for current execution priority. P71/P82 remain important for the odds-dependent market-edge lane, but HEAD has advanced through P84G on the 2026 prediction-only lane.

### 0H.1 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Repo root `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `021a8a8 feat(P84G): Fix Predicted-Side Mapping + Regenerate Canonical Prediction Rows - P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED`. |
| P84G state | [Confirmed] `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED`; P83E `compute_predicted_side()` now maps `sp_fip_delta > 0 -> away` and `sp_fip_delta < 0 -> home`. |
| Mapping convention | [Confirmed] `sp_fip_delta = home_sp_fip - away_sp_fip`; FIP is lower-is-better, so positive delta means the home pitcher is worse and the FIP-favoured side is away. |
| Regenerated artifacts | [Confirmed] P83E canonical rows, P84E outcome-attached rows, and P84F diagnostic were regenerated after the mapping fix. |
| 2026 canonical coverage | [Confirmed] 828 canonical prediction rows out of 2430 schedule rows; schedule coverage is 34.07%, so the 2026 prediction set remains partial. |
| Outcome attachment | [Confirmed] P84E has 808 outcome-available rows and 20 outcome-pending rows. |
| Corrected metrics | [Confirmed] All-row hit_rate `0.569307`, AUC `0.594315`, Brier `0.249408`, ECE `0.069682`; primary_125 hit_rate `0.602851`, shadow_100 hit_rate `0.595149`, Tier B hit_rate `0.563830`. |
| P84F post-fix state | [Confirmed] P84F classification changed to `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK`; mapping pattern is now `PROB_GE_05_MAPS_TO_HOME`; predicted-side FIP consistency rate is 1.0. |
| P84D coverage state | [Confirmed] `P84D_PITCHER_COVERAGE_AUDIT_READY_NO_BACKFILL`; no backfill candidates were written, remaining gap is 1602 games. |
| P82 market-edge lane | [Confirmed] P82 remains `BLOCKED_NO_REAL_DATASET`; P82B raw paid data policy is ready, but no real legal odds dataset has unlocked EV / CLV / market-edge work. |
| Tests | [Confirmed from handoff] P84G dedicated tests 30/30 PASS; P83A-P84G targeted regression 502 passed / 4 skipped. [Unknown] Full repository test suite status after P84G. |
| Governance | [Confirmed] No odds, no EV, no CLV, no Kelly, no production readiness, no champion replacement, no real betting; `paper_only=true` and `diagnostic_only=true` remain active. |
| Worktree risk | [Confirmed] Worktree contains many dirty runtime/data/output files; future commits must remain whitelist-only. |
| CTO scope note | [Confirmed] CTO roadmap review may update only `roadmap.md` and `CTO-Analysis.md`; no `active_task.md` write and no new worker task prompt in this CTO step. |

### 0H.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P84G directly addressed the P84F correctness finding instead of interpreting the old 43.1% hit_rate as model failure. |
| [Aligned] | P84G correctly regenerated downstream P83E/P84E/P84F artifacts after changing canonical predicted-side semantics. |
| [Aligned] | The current lane matches the post-P72/P77 prediction-only roadmap: validate outcome prediction without odds, EV, CLV, or Kelly. |
| [Aligned] | P82/P82B market-edge governance remains intact; no real legal odds dataset means market-edge and production recommendations stay blocked. |
| [Drift] | The latest roadmap section was still P71/P72-oriented, while actual HEAD has advanced to P84G. |
| [Drift] | `active_task.md` title still references P84C even though it also records P84F/P84G completion; task-state presentation is stale but outside CTO write scope. |
| [Drift] | P84G's corrected 56.9% all-row hit_rate and 60.3% primary_125 hit_rate could be overread as production signal unless a coverage / stability guard is added. |
| [Missing] | Roadmap lacked a post-fix P84H guard to recompute metrics, split by month/time/side/rule subset, and classify coverage sufficiency. |
| [Missing] | Roadmap lacked a persistent convention invariant gate covering `sp_fip_delta`, `model_probability=P(home wins)`, `predicted_side`, and `actual_winner`. |
| [Missing] | Roadmap lacked an artifact regeneration / stale-report guard for canonical rows, outcome-attached rows, diagnostics, reports, and active task markers. |
| [Outdated] | The old `P84F_SIDE_MAPPING_INVERTED` state is no longer current after P84G; post-fix evidence must use `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK`. |
| [Outdated] | Treating the API key or market-edge lane as the next global blocker is outdated for prediction-only validation. |
| [Outdated] | Treating P84C as outcomes-pending is outdated for the 808 rows now attached by P84E, although full 2026 coverage is still partial. |
| [Blocked] | Production recommendations, betting advice, Kelly, EV, CLV, and market-edge claims remain blocked by missing real legal odds and by prediction-only partial coverage. |
| [Blocked] | Full-season 2026 claims remain blocked by 828/2430 canonical coverage and only March-May outcome evidence. |
| [Blocked] | Calibration/recalibration changes are blocked until P84H confirms whether weakness is coverage-, sample-, side-, time-, or score-transformation-driven. |

### 0H.3 Reprioritized P0-P10 From P84G

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P84H Corrected Signal Validation + Coverage Guard | Prediction validation | Validate the P84G-corrected signal across coverage, sample, calibration, monthly/time split, side split, and rule subsets. | P84H summary/report classify the corrected signal; recomputed metrics match P84E within tolerance; no odds/EV/CLV/Kelly/production claim. |
| **P1** | Prediction Convention Invariant Gate | Correctness + tests | Prevent another silent inversion across FIP sign, probability direction, predicted side, and winner label. | Tests or guard checks cover positive/negative delta, probability threshold mapping, actual winner labels, and downstream consistency. |
| **P2** | Artifact Regeneration / Dependency Contract | Workflow governance | Make canonical -> outcome -> diagnostic -> report regeneration order explicit and detect stale artifacts. | Roadmap/reporting states source-of-truth artifacts, regeneration order, and mismatch stop conditions. |
| **P3** | Targeted + Broader Regression Policy | Test governance | Extend P83A-P84G targeted regression to P84H and decide when full-repo regression is required. | P83A-P84H command is documented; full repo status is either run or explicitly marked unknown with risk. |
| **P4** | P84D Coverage Backfill Watch | Data quality | Revisit pitcher/probable coverage only when MLB probable pitcher availability improves. | Coverage audit rerun changes row count or confirms no actionable backfill; no fabricated FIP values. |
| **P5** | Calibration / Recalibration Research Gate | Model reliability | Decide whether Platt/isotonic or score transformation is warranted after P84H. | Any calibration work remains OOS/diagnostic-only and does not mutate production or recommendation logic. |
| **P6** | Prediction-Only Shadow Tracker Integration | Monitoring | Connect corrected P84G metrics to P77/P78/P79-style tracking without odds or market-edge claims. | Tracker labels P84G signal as diagnostic-only and separates primary_125, shadow_100, and Tier B. |
| **P7** | Market-Edge Reentry | Odds-dependent validation | Resume P80-P82 only after a real legal odds dataset exists and passes policy/validator gates. | P82 unlock status changes from `BLOCKED_NO_REAL_DATASET`; aggregate-only market-edge dry-run allowed, no Kelly. |
| **P8** | Paid / Raw Data Governance | Data rights | Preserve P82B/P82C raw paid data and staging guard policy. | No raw paid odds rows, API keys, or row-level proprietary odds are staged. |
| **P9** | Agent / Roadmap Hygiene | Orchestration | Keep active task, roadmap, reports, and handoff state aligned without creating new repos or foreign artifacts. | Stale markers are fixed only in authorized task scope; dirty runtime files ignored. |
| **P10** | Production Proposal Gate | Governance | Keep production blocked until prediction evidence, market-edge evidence, risk controls, monitoring, and explicit approval all exist. | `production_ready=false`; no champion replacement, profitability claim, real bet, or Taiwan lottery recommendation. |

### 0H.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: P84H corrected 2026 prediction-only signal validation + coverage guard.
- [Confirmed] Upgraded to P1: prediction convention invariant gate, because P83E/P84F tests previously encoded the wrong mapping.
- [Confirmed] Upgraded to P2: artifact regeneration / dependency contract for canonical rows and downstream diagnostics.
- [Confirmed] Downgraded: market-edge reentry from near-term global work to P7 blocked lane until real legal odds data exists.
- [Confirmed] Downgraded: calibration/refit work until P84H determines whether calibration weakness is genuine and stable.
- [Confirmed] Paused: production recommendation, champion replacement, Kelly, EV/CLV, runtime recommendation changes, TSL crawler changes, and any odds-file work.
- [Confirmed] Paused: P84D backfill until more probable pitcher data can actually increase coverage.
- [Confirmed] Retired: interpreting the pre-P84G 43.1% hit_rate as model weakness; it was an inverted side-mapping artifact.
- [Confirmed] Retired: using `P84F_SIDE_MAPPING_INVERTED` as the current diagnostic state; post-fix state is `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK`.

### 0H.5 Critical Blockers

| Blocker | Impact | Why blocker | Risk if ignored | Priority | Acceptance |
|---|---|---|---|---|---|
| Post-fix signal not yet guarded | Prediction validation | Correctness bug is fixed, but coverage/time/side/sample stability is not yet validated. | 56.9% / 60.3% hit rates may be overstated as full-season signal. | P0 | P84H emits classification and split metrics with diagnostic-only boundary. |
| Convention inversion risk | Core correctness | A core sign convention bug survived into tests and reports. | Future feature/model changes could silently invert sides again. | P1 | Invariant tests guard delta sign, probability direction, side mapping, and actual winner labels. |
| Partial 2026 coverage | Data quality | Only 828/2430 schedule rows have canonical predictions. | Coverage bias from probable pitcher availability may distort apparent accuracy. | P0/P4 | Coverage classification and bias note exist; full-season claims remain blocked. |
| Real legal odds absent | Market-edge/product | P82 cannot compute market edge, EV, CLV, or betting recommendation evidence. | Prediction accuracy could be mistaken for bettable edge. | P7 | P82 unlock requires validated real legal odds dataset; until then no edge claims. |
| Full repo regression unknown | QA | P84G targeted regression passed, but full suite was not confirmed. | Hidden non-P83/P84 regressions may remain. | P3 | Either run full suite in an authorized task or explicitly track as unknown risk. |

### 0H.6 Today Focus

1. Treat P84G as completed at `021a8a8`.
2. Focus next on P84H corrected signal validation and coverage guard.
3. Keep P84H prediction-only: no odds, no EV, no CLV, no Kelly, no production recommendation.
4. Do not write a worker task prompt or `active_task.md` from this CTO roadmap review because the strict CTO write scope only permits `roadmap.md` and `CTO-Analysis.md`.

Product direction remains two-lane:

- Lane 1: MLB prediction-only strategy validation, which can proceed with outcomes and OOS diagnostics after the P84G correctness fix.
- Lane 2: Taiwan sports lottery paper-only recommendation / market-edge validation, which remains blocked until real legal odds data passes P81/P82 policy gates.

---

## 0G. Latest CTO Update - P71 Done, Strategy Accuracy First

This section supersedes section 0F for current execution priority. P59/P60 remain important monitoring evidence, but the current HEAD has advanced through P71 on the paper recommendation / 2024 odds gap lane.

### 0G.1 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Repo root `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `1d8adb8 feat(p71): Awaiting-Key Closure - P71_PATH_A_STILL_AWAITING_API_KEY`. |
| P64 paper simulation | [Confirmed] P64 generated 535 2025-only Tier C paper rows; all 33 P62 fields present; all rows `GATE_PASS`. |
| P64/P65 edge result | [Confirmed] P64/P65 show stable negative market edge: mean edge `-0.032473`, positive edge 200/535, and all monthly/third/rolling windows negative. |
| P66 mapping audit | [Confirmed] P66 confirmed negative edge is not caused by odds join, side mapping, American odds conversion, or edge formula errors. |
| P67/P68 free source path | [Confirmed] Free 2024 odds sources did not produce usable bulk MLB moneyline data; OddsPortal is blocked by ToS / robots for automated extraction. |
| P69/P70/P71 PATH_A | [Confirmed] CEO-authorized The Odds API historical path exists, but P70/P71 are dry-run / awaiting-key only because `THE_ODDS_API_KEY` is missing. |
| API status | [Confirmed] P71 `api_key_status=API_KEY_MISSING`, `live_api_calls=0`, `paid_api_called=false`; no 2024 odds CSV has been produced. |
| Governance | [Confirmed] `paper_only=true`, `diagnostic_only=true`, `promotion_freeze=true`, `kelly_deploy_allowed=false`, `production_ready=false`, no real betting. |
| Important reframing | [Confirmed] Historical odds are required for market-edge / EV / CLV / paper betting recommendation validation. [Inferred] They are not required for pure outcome-prediction accuracy backtests. |
| Main CTO decision | [Inferred] API key should no longer be treated as the global P0 blocker. It blocks only the market-edge validation lane; the odds-free strategy accuracy lane can continue. |
| Worktree risk | [Confirmed] Worktree contains many runtime/data/output dirty files; do not stage raw feed/runtime/generated output. |

### 0G.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P64 correctly tested whether the P62 contract can produce paper-only recommendation rows from 2025 local data. |
| [Aligned] | P65/P66 correctly prevented premature product claims by proving the 2025 market-edge result is stable negative and not a mapping bug. |
| [Aligned] | P67/P68 correctly rejected governance-risky free scraping paths. |
| [Aligned] | P70/P71 correctly avoided live / paid API calls without `THE_ODDS_API_KEY`. |
| [Drift] | Earlier P60 monitoring edge evidence does not by itself support paper betting recommendations after P64-P66 market-odds simulation showed stable negative edge. |
| [Drift] | `active_task.md` frames P72 as key-readiness only; CTO roadmap now separates odds-free strategy accuracy work from odds-dependent market-edge work. |
| [Missing] | Roadmap did not clearly state which validation objectives require historical odds and which do not. |
| [Missing] | Roadmap did not yet define an odds-free strategy-accuracy backtest lane focused on predictive quality rather than money simulation. |
| [Outdated] | Treating API key absence as a global blocker is outdated. It blocks 2024 market-edge validation, not model accuracy research. |
| [Outdated] | Repeating awaiting-key closure reports is low value unless the key state changes. |
| [Blocked] | Cross-year market-edge / CLV / EV validation remains blocked by missing 2024 odds. |
| [Blocked] | Production recommendations remain blocked because 2025 paper simulation edge is negative and cross-year market-edge validation is incomplete. |

### 0G.3 Historical Odds Importance

Historical odds are important, but only for the market-facing part of the system.

| Objective | Need historical odds? | Why |
|---|---|---|
| Pure game outcome prediction accuracy | [Confirmed] No | Can evaluate against actual outcomes with AUC, Brier, log-loss, hit rate, calibration, and temporal stability. |
| Strategy selection as "most accurate predictive rule" | [Confirmed] No, if strategy means outcome prediction quality | Can compare thresholds, tiers, features, and calibration without odds. |
| Betting edge / EV / expected value | [Confirmed] Yes | Edge requires model probability minus market implied probability. |
| CLV / beating closing line | [Confirmed] Yes | CLV requires opening/pregame and closing-line odds. |
| Paper recommendation rows for Taiwan sports lottery | [Confirmed] Yes for release-quality rows | The contract requires odds, implied probability, edge, source trace, timestamp, and risk gate. |
| Profit / bankroll / Kelly simulation | [Confirmed] Yes | Stake sizing and return simulation require available odds. |

CTO conclusion:

- [Confirmed] If the immediate goal is "find the most accurate strategy," historical odds are not the top blocker.
- [Confirmed] If the goal is "prove the strategy is bettable / has market edge," historical odds remain mandatory.
- [Inferred] The roadmap should split into two lanes: P0 odds-free predictive strategy validation, and P2/P4 odds-dependent market-edge validation.

### 0G.4 Reprioritized P0-P10 From P71

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | Odds-Free Strategy Accuracy Backtest | Model validation | Evaluate strategy quality without odds using outcomes: AUC, Brier, log-loss, hit rate, calibration, threshold/tier stability, and month-by-month robustness. | Best predictive strategy is identified or rejected with outcome-only OOS evidence; no EV/profit claim. |
| **P1** | Objective Split / Metric Contract | Roadmap governance | Define separate scorecards for prediction accuracy vs market edge so future phases stop conflating them. | Roadmap states which metrics require odds and which do not; P64-P66 negative edge is not confused with predictive accuracy. |
| **P2** | P72 Key Readiness Only If Key Appears | Data gate | Avoid another awaiting-key loop; only run controlled pull if `THE_ODDS_API_KEY` is present, otherwise record blocker once and move on. | Key present -> controlled pull and schema validation; key missing -> no API call and market-edge lane remains blocked. |
| **P3** | Raw Paid Data Commit Policy | Data governance | Decide whether a paid 2024 odds CSV is raw, derived, or external-restricted before any commit. | Policy states whether `data/mlb_2025/mlb_odds_2024_real.csv` can be committed, hashed only, or kept local. |
| **P4** | Cross-Year Market-Edge Validation | Odds-dependent validation | Re-run 2024+2025 market-edge / CLV-like validation only after 2024 odds are legally obtained. | 2024 CSV schema passes; joins pass; cross-year edge result is reported without production claim. |
| **P5** | Doubleheader Join Disambiguation | Data quality | Replace or audit `(date, home_team)` last-row-wins behavior for doubleheaders before future market-edge claims. | 28 duplicate-key cases are explicitly resolved or declared non-impacting. |
| **P6** | Paper Recommendation Product Gate | Product architecture | Keep P62 rows paper-only and blocked until accuracy, calibration, odds trace, and edge gates all pass. | No release; rows retain `paper_only=true`, source trace, risk gate, and no production status. |
| **P7** | Calibration / Threshold Diagnostics | Model reliability | Improve outcome-probability quality if outcome-only backtest shows ranking signal but poor calibration. | Calibration diagnostics are OOS-only and do not mutate P45/P52 without approval. |
| **P8** | Artifact / Regression Budget | Test governance | Reduce phase sprawl and avoid repeated 6-artifact cycles for no-op blocker reports. | Targeted tests + scheduled regression policy is documented. |
| **P9** | Cross-Project Context Lock | Agent governance | Maintain Betting-only context after prior cross-project drift. | Stop on non-Betting task evidence; do not write foreign project artifacts. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until validated probabilities, market-edge evidence, risk controls, monitoring, and explicit approval exist. | `production_ready=false`; no champion replacement or profitability claim. |

### 0G.5 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: odds-free strategy accuracy backtest focused on predictive correctness, not simulated money.
- [Confirmed] Upgraded to P1: objective split / metric contract for prediction accuracy vs market edge.
- [Confirmed] Downgraded: API key from global blocker to market-edge-lane blocker.
- [Confirmed] Downgraded: repeated awaiting-key closure reports unless key state changes.
- [Confirmed] Paused: real API call, paid data pull, raw CSV commit, and 2024 cross-year market-edge validation until key and data policy are clear.
- [Confirmed] Paused: production proposal, champion replacement, optimizer promotion, real betting recommendations, Kelly deployment.
- [Confirmed] Retired: treating P60 positive monitoring edge as sufficient for paper betting product after P64-P66 found stable negative market edge.
- [Confirmed] Retired: treating P64/P65 negative edge as proof the model has no predictive value; it only proves underperformance versus available 2025 market prices.

### 0G.6 Today Focus

1. Do not spin on `THE_ODDS_API_KEY` unless the key has actually been configured.
2. Reframe the next analysis around "What strategy predicts MLB outcomes best without odds?"
3. Keep odds-free backtests honest: no EV, no CLV, no profit, no Kelly, no betting recommendation.
4. Keep market-edge validation as a separate lane that resumes only when 2024 odds are legally available.

No new repo, no new worktree, no branch switch, no production proposal, no champion replacement, no optimizer promotion, no live odds API call, no real betting recommendation, no raw/runtime commit, and no worker task prompt from CTO roadmap analysis.

Product direction remains two-lane:

- Lane 1: MLB game prediction strategy accuracy, which can proceed without historical odds using outcomes and OOS validation.
- Lane 2: Taiwan sports lottery paper-only recommendation / market-edge validation, which requires odds, source trace, edge, risk gate, and `paper_only=true`.

---

## 0F. Latest CTO Update - P59 Done, P60 Historical Monthly Pack Next

This section supersedes section 0E for current execution priority. P42/P43-P58 remain important historical evidence, but the current HEAD has advanced through P59 on the Monitoring Contract V2 lane.

### 0F.1 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Repo root `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `b1332b3 feat(p59): Monitoring Contract V2 First Monthly Report - P59_FIRST_MONTHLY_REPORT_SAMPLE_LIMITED`. |
| P59 commit scope | [Confirmed] Six whitelisted files committed: P59 script, test, summary JSON, report, BettingPlan report, and `active_task.md`. |
| P59 artifact dating | [Confirmed] P59 JSON `run_date` is `2026-05-25`; committed report paths use `20260526` labels. Treat `20260526` as artifact label, not evidence that the operating date advanced. |
| P59 report month | [Confirmed] `2025-09`, historical diagnostic fallback because no post-Sep / Oct 2025 complete monthly batch was available. |
| P59 global status | [Confirmed] `MONITORING_ALERT_DIAGNOSTIC`, alert level `RED`. |
| Alert cause | [Confirmed] Calibration + sample limitation: `batch_n=98 < 100`; `platt_ece=0.122929 > ece_critical_threshold=0.12`; edge status is healthy. |
| Edge status | [Confirmed] `EDGE_WITHIN_THRESHOLD`; raw edge mean `0.108441`, CI low `0.092154 > 0`. |
| Band annotation | [Confirmed] Sep mid-band annotation carried forward: `1.00 <= |sp_fip_delta| < 1.25`, `BAND_SAMPLE_INSUFFICIENT`, `TRACK_ONLY_NO_REFIT`, repeated count `2`. |
| Validation | [Confirmed] VAL01-VAL10 all pass; P59 tests 22/22 PASS; P40-P59 cumulative 460/460 PASS per handoff/report. CTO review did not rerun tests. |
| Governance | [Confirmed] `paper_only=true`, `promotion_freeze=true`, `kelly_deploy_allowed=false`, `live_api_calls=0`; P45 Platt constants and P52 thresholds unchanged. |
| Blocking data gap | [Confirmed] 2024 closing-line odds / Home ML / Away ML gap remains unresolved for cross-year market-edge validation. |
| External paper | [Confirmed] NTU 2016 thesis "Prediction of Postseason Appearance in MLB..." uses 1995-2015 team-season stats with factor analysis, decision tree, and SVM to predict postseason appearance. [Inferred] It is background-useful but not directly actionable for game-level betting or P59/P60 monitoring. |
| Worktree risk | [Confirmed] Worktree contains many runtime/data/output dirty files; do not stage raw feed/runtime/generated output. |

### 0F.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P59 correctly follows P58: the monthly template was exercised on real 2025 Tier C data. |
| [Aligned] | P59 correctly preserves P52 thresholds, P45 Platt constants, runtime logic, promotion freeze, and paper-only governance. |
| [Aligned] | P59 distinguishes global threshold-driven alert state from band-level annotation metadata. |
| [Drift] | Previous top roadmap priority centered on P42/P43 calibration evidence. Current HEAD has advanced to P59 monitoring-contract validation. |
| [Missing] | Roadmap did not yet encode multi-month validation of the monthly report template. |
| [Missing] | Roadmap did not yet define a reusable monthly report validator around VAL01-VAL10. |
| [Outdated] | Single-month P59 evidence is not enough to freeze monthly monitoring as stable. |
| [Outdated] | Any plan to refit Platt constants or change P52 thresholds based on Sep alone remains invalid. |
| [Blocked] | Cross-year market-edge validation remains blocked by 2024 closing-line odds gaps; production/promotion remains blocked by governance. |

### 0F.3 Reprioritized P0-P10 From P59

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P60 Historical Monthly Report Pack | Monitoring validation | Generate Apr-Sep 2025 historical monthly pack and validate whether P58/P59 contract generalizes beyond Sep. | All available months produced; VAL01-VAL10 pass per month; P52/P45/P59 artifacts preserved. |
| **P1** | Monthly Report Validator SSOT | QA architecture | Extract or formalize VAL01-VAL10 so future monthly reports use the same validation semantics. | Validator replays P59 and P60 reports with consistent pass/fail output. |
| **P2** | Sample-Limited Alert Presentation | Product / report UX | Clarify how `MONITORING_ALERT_DIAGNOSTIC` plus `SAMPLE_INSUFFICIENT` should be read. | Reports distinguish "model broken" from "sample-limited calibration alert". |
| **P3** | P52-P59 Contract Freeze Review | Governance | Freeze thresholds/constants/report semantics before adding new monitoring features. | No P45/P52 changes; no runtime recommendation logic changes; contracts documented. |
| **P4** | 2024 Closing-Line Gap Resolution Plan | Data sourcing | Plan how to acquire/validate 2024 Home ML / Away ML closing-line odds for cross-year market-edge validation. | Data requirements, source policy, and no-live-call constraints are documented. |
| **P5** | Targeted vs Full Regression Policy | Test governance | Control test sprawl as P40-P59 already reaches 460 cumulative tests. | Targeted gate and scheduled full regression policy are defined. |
| **P6** | Monthly Monitoring Artifact Hygiene | Repo governance | Prevent P52-P60 artifacts from sprawl and prevent runtime/raw files from commits. | Whitelist-only staging remains mandatory; old artifacts are not overwritten. |
| **P7** | Literature / Season-Level Context Review | Research support | Use the 2016 postseason thesis only as background for long-horizon team-strength features. | Any borrowed idea is marked background; no game-level betting conclusion is inferred. |
| **P8** | MLB Paper Recommendation Contract | Product architecture | Keep recommendation rows paper-only with probability, odds, edge, source, timestamp, risk gate, and `paper_only=true`. | Release remains blocked until calibration, monitoring, and source-trace gates clear. |
| **P9** | Cross-Project Context Lock | Agent governance | Maintain Betting-only context after prior cross-project drift. | Stop on non-Betting task evidence; do not write foreign project artifacts. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until validated probabilities, CLV/closing-line evidence, risk controls, monitoring, and explicit approval exist. | `production_ready=false`; no champion replacement or profitability claim. |

### 0F.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: P60 historical monthly report pack validation.
- [Confirmed] Upgraded to P1: monthly report validator SSOT around VAL01-VAL10.
- [Confirmed] Upgraded to P2: sample-limited alert presentation / operator interpretation.
- [Confirmed] Downgraded: single-month Sep deep dive; P59 already established Sep status.
- [Confirmed] Downgraded: new calibration/model methods until monthly monitoring stability is established.
- [Confirmed] Paused: P45 Platt refit, P52 threshold changes, runtime recommendation changes.
- [Confirmed] Paused: production proposal, champion replacement, optimizer promotion, real betting recommendations, live API calls.
- [Confirmed] Retired: interpreting Sep edge as drift; P50/P51 and P59 indicate edge is within threshold.
- [Confirmed] Retired: allowing band annotation to override global P52 status.

### 0F.5 External Paper Assessment

- [Confirmed] Source located: Wang, Yen-Chieh, NTU master's thesis, 2016, "Prediction of Postseason Appearance in Major League Baseball by Statistical Analysis and Machine Learning."
- [Confirmed] Public abstracts state it uses MLB team statistics from 1995-2015 and methods including factor analysis, decision tree, and SVM; reported prediction accuracy is at least 70%.
- [Inferred] Reference value for this system: medium for literature/background, low for immediate implementation.
- [Inferred] Useful ideas: season-level feature taxonomy, team-strength factor grouping, interpretable tree rules, and long-horizon playoff qualification framing.
- [Inferred] Not directly useful for P59/P60: it predicts season postseason appearance, not game-level betting markets, closing-line edge, calibration, or monthly monitoring alerts.
- [Inferred] Do not promote it to P0/P1; keep it as P7 background until monitoring and probability validation gates are stable.

### 0F.6 Today Focus

1. Treat P59 as completed at `b1332b3`.
2. Execute no functional development in this CTO step; next technical priority is P60 historical monthly report pack.
3. Keep P60 diagnostic-only and contract-preserving: no P45/P52 changes, no P52-P59 overwrite, no runtime recommendation logic changes.
4. Preserve `paper_only=true`, `promotion_freeze=true`, `kelly_deploy_allowed=false`, and `live_api_calls=0`.

No new repo, no new worktree, no branch switch, no production proposal, no champion replacement, no optimizer promotion, no live odds API call, no real betting recommendation, no raw/runtime commit, and no worker task prompt from CTO roadmap analysis.

Product direction remains two-lane:

- Lane 1: MLB pregame prediction and Taiwan sports lottery paper-only recommendation rows, blocked until probability calibration, monitoring, odds/source trace, and risk gates are trustworthy.
- Lane 2: strategy optimization / simulation, blocked until pregame odds, closing line, actual outcome, and source trace support statistically meaningful paper-only validation.

---

## 0E. Latest CTO Update - P42 Confirmed, P43 Calibration Gate Next

This section supersedes sections 0D/0C for current execution priority. P26K remains historically relevant to capture infrastructure, but the current HEAD has advanced through P42 on the MLB `sp_fip_delta` research lane.

### 0E.1 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Repo root `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `43cc739 feat(p42): signal-band tier framework + Kelly diagnostic - 3 tiers validated`. |
| P41 state | [Confirmed] P41 `6ee4e57` completed `CROSS_YEAR_CONFIRMED`; combined n=1490, AUC=0.5865, bootstrap CI [0.5557, 0.6170]. |
| P42 state | [Confirmed] P42 exists and is committed after the user-provided P41 handoff; P42 generated script, JSON, report, and tests. |
| P42 files | [Confirmed] `scripts/_p42_signal_band_tier_kelly_diagnostic.py`, `data/mlb_2025/derived/p42_signal_band_tier_kelly_summary.json`, `tests/test_p42_signal_band_tier_kelly.py`, `report/p42_signal_band_tier_kelly_diagnostic_20260524.md`. |
| P42 tests | [Confirmed from report] P42 78/78 PASS; P40+P41+P42 cumulative 161/161 PASS. CTO review did not rerun tests. |
| P42 tier summary | [Confirmed] Tier A n=47 AUC=0.7038 `SAMPLE_LIMITED_HIGH_AUC`; Tier B n=180 AUC=0.6476 `MEDIUM_CONFIDENCE_DIAGNOSTIC`; Tier C n=1490 AUC=0.5865 `HIGH_CONFIDENCE_DIAGNOSTIC`. |
| Governance | [Confirmed] `diagnostic_only=true`, `promotion_freeze=true`, `kelly_deploy_allowed=false`, `live_api_calls=0`, `T_LOCKED=0.50`. |
| Kelly status | [Confirmed] Kelly-equivalent analysis is theoretical diagnostic only; it is not a betting recommendation or deployment authorization. |
| Artifact consistency risk | [Confirmed] P42 markdown report and JSON summary disagree on Brier/ECE/log-loss values for tiers A/B/C. |
| P41 markdown report | [Confirmed] No `report/p41_*.md` was found in `report/`; only P41 script/test/summary JSON were observed. |
| Worktree risk | [Confirmed] Worktree contains many runtime/data/output dirty files; do not stage raw feed/runtime/generated output. |

### 0E.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P28-P30 restored observability and test baseline before feature research; this matches the data-first roadmap intent. |
| [Aligned] | P31-P41 correctly narrowed noisy candidate features down to `sp_fip_delta` with cross-year OOS evidence. |
| [Aligned] | P42 correctly kept Kelly analysis diagnostic-only and preserved promotion freeze. |
| [Drift] | The user-provided handoff says current HEAD is P41 `6ee4e57`, but repo HEAD is P42 `43cc739`; roadmap must treat P42 as current. |
| [Drift] | The handoff recommends P42 as next, but P42 has already been committed; the next phase should be P42 evidence reconciliation and P43 calibration/probability reliability. |
| [Missing] | Roadmap did not yet encode P42 artifact consistency checks between markdown and JSON. |
| [Missing] | Roadmap did not yet encode the missing P41 markdown report as an audit trail gap. |
| [Outdated] | Any plan to start P42 from scratch is outdated. |
| [Outdated] | Treating AUC-confirmed or Kelly-positive diagnostics as deployable betting strategy remains invalid. |
| [Blocked] | Production proposal, champion replacement, optimizer promotion, and real betting recommendations remain blocked by calibration / Brier / ECE reliability and governance freeze. |

### 0E.3 Reprioritized P0-P10 From P42

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P42 Evidence Consistency Reconciliation | Verification + governance | Reconcile P42 markdown vs JSON Brier/ECE/log-loss values and confirm canonical metrics before downstream decisions. | Single source of truth is declared; report/JSON discrepancies are explained or corrected in an authorized docs-only follow-up. |
| **P1** | P43 Calibration / Probability Reliability Gate | Model validation | Convert ranking signal evidence into probability reliability diagnostics before any sizing or recommendation path. | OOS-only calibration, Brier, Brier Skill, ECE, log-loss, and bucket reliability are reported without production mutation. |
| **P2** | Tier B Focused Diagnostic + Tier A Sample Plan | Signal governance | Treat Tier B as the most actionable diagnostic layer and Tier A as sample-limited. | Tier B robustness is examined; Tier A has an accumulation rule before stronger claims. |
| **P3** | P41/P42 Artifact Audit Trail Cleanup | Documentation + source governance | Fill audit gaps such as missing P41 markdown report and source/metadata notes for 2024 holdout / 2023 FIP proxy data. | Missing reports/source notes are documented without changing model conclusions. |
| **P4** | Kelly Diagnostic Guardrail | Risk governance | Keep Kelly-equivalent outputs theoretical and prevent conversion into stake sizing or recommendation logic. | Reports explicitly say `kelly_deploy_allowed=false`; no production strategy or champion mutation. |
| **P5** | CLV / Closing-Line Validation Re-entry | Data validation | Reconnect confirmed feature signal to formal pregame odds / closing line / outcome trace when capture data is ready. | CLV validation is only run with verified pregame/closing pairs and sufficient sample size. |
| **P6** | MLB Paper Recommendation Contract | Product architecture | Define paper-only rows with model probability, odds, edge, data source, generated time, risk gate, and `paper_only=true`. | Contract exists but release remains blocked until calibration and source trace gates clear. |
| **P7** | Multi-Year OOS Expansion | Research validation | Add more seasons only after source/licensing and deterministic build rules are explicit. | Additional OOS years reproduce schemas and no future leakage is introduced. |
| **P8** | Runtime / Raw Data Commit Guard | Repo governance | Keep daemon/runtime/generated output out of commits while research artifacts are reviewed. | Future commits are whitelist-only and explain ignored dirty files. |
| **P9** | Cross-Project Context Lock | Agent governance | Maintain Betting-only context after prior Stock-Prediction conversation drift. | Stop on non-Betting task evidence; do not write foreign project artifacts. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until validated probabilities, CLV evidence, risk controls, monitoring, and explicit approval exist. | `production_ready=false`; no champion replacement or profitability claim. |

### 0E.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: P42 evidence consistency reconciliation.
- [Confirmed] Upgraded to P1: P43 calibration / probability reliability gate.
- [Confirmed] Upgraded to P2: Tier B focused diagnostic and Tier A sample-size plan.
- [Confirmed] Downgraded: "execute P42" as a next task; P42 already exists at HEAD.
- [Confirmed] Downgraded: CLV/closing-line re-entry until probability reliability and capture data are ready.
- [Confirmed] Paused: Kelly deployment, champion replacement, optimizer promotion, paper recommendation release, production proposal.
- [Confirmed] Paused: live odds API calls and any real betting workflow.
- [Confirmed] Retired: treating CLV as robust signal from earlier phases; P30B marked it noise.
- [Confirmed] Retired: treating bullpen/park as current core next-step features; P35/P41 evidence favors `sp_fip_delta`.

### 0E.5 Today Focus

1. Treat P42 as completed, not pending.
2. Resolve P42 artifact consistency before using the tier/Kelly diagnostics for roadmap decisions.
3. Prepare P43 as a diagnostic-only calibration / probability reliability phase, not deployment.
4. Preserve promotion freeze, `T_LOCKED=0.50`, `kelly_deploy_allowed=false`, and `live_api_calls=0`.

No new repo, no new worktree, no branch switch, no production proposal, no champion replacement, no optimizer promotion, no live odds API call, no real betting recommendation, no raw/runtime commit, and no worker task prompt from CTO roadmap analysis.

Product direction remains two-lane:

- Lane 1: MLB pregame prediction and Taiwan sports lottery paper-only recommendation rows, blocked until probability calibration plus odds/source trace gates are trustworthy.
- Lane 2: strategy optimization / simulation, blocked until pregame odds, closing line, actual outcome, and source trace support statistically meaningful paper-only validation.

---

## 0D. Latest CTO Update - Context Hygiene Clean, Return To P26K

This section supersedes section 0C only for current execution priority. P26J remains the latest Betting evidence package; P26K remains the next technical phase.

### 0D.1 Project Context Lock

| Area | Status |
|---|---|
| Project | [Confirmed] `Betting-pool`. |
| Canonical repo | [Confirmed] `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`. |
| Canonical branch | [Confirmed] `main`. |
| Cross-project guard | [Confirmed] If P48/P49/Stock-Prediction/golden fixture/paper simulation dry-run content appears in a Betting task, stop and do not create Betting artifacts from that content. |

### 0D.2 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Repo root `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `0ccd06d verify(p26j): post-window pair verification rerun - 09:12Z`. |
| Log hygiene | [Confirmed] Recent git log is P26x Betting work; no P48/P49/Stock-Prediction/golden fixture/paper simulation dry-run entries observed. |
| Content hygiene | [Confirmed] `rg` scan over `00-Plan`, `00-BettingPlan`, `report`, and `data/paper_recommendations` found no Stock/P48/P49 contamination. |
| Context classification | [Confirmed] `BETTING_CONTEXT_CLEAN`. |
| P26K status | [Confirmed] No P26K artifacts were found in `00-Plan`, `00-BettingPlan`, `report`, `data/paper_recommendations`, `scripts`, or `tests`. |
| Dirty worktree | [Confirmed] Worktree has many Betting runtime/daemon/output modifications; do not stage raw feed/runtime/generated output files. |
| Untracked scripts | [Confirmed] Four untracked `scripts/p26j_*.py` files exist; their final disposition is [Unknown] and they must not be staged by a P26K artifact-only task unless explicitly scoped. |
| Restricted files | [Confirmed] `00-Plan/roadmap/CEO-Decision.md` and `00-Plan/roadmap/active_task.md` are modified in the worktree but are outside this CTO write scope; do not touch them in this analysis. |
| Tests | [Confirmed] No tests were run in this CTO context-hygiene review. |

### 0D.3 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | Context hygiene check aligns with the project-context-lock requirement after cross-project conversation drift. |
| [Aligned] | Returning to P26K aligns with section 0C: P26J proved daemon cycles existed but fetch did not execute in the closing window. |
| [Aligned] | P25C bootstrap remains blocked because COMPLETE_PAIR is still known as 219 from P26J and P26K has not changed that evidence. |
| [Drift] | The conversation drifted into Stock-Prediction P48/P49, but repo/log/grep checks did not show Betting repo contamination. |
| [Missing] | Roadmap did not yet encode context hygiene as a standing pre-flight for multi-project handoffs. |
| [Missing] | Roadmap did not yet explicitly call out untracked `scripts/p26j_*.py` as a commit-scope risk. |
| [Outdated] | Any task prompt or roadmap step referring to Stock/P48/P49 is not current Betting work and must not be summarized as Betting progress. |
| [Blocked] | P26K remains blocked only by execution, not by context contamination; P25C/bootstrap/product recommendation lanes remain blocked by unresolved closing fetch trigger behavior. |

### 0D.4 Reprioritized P0-P10 From Context Hygiene

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P26K Closing Fetch Trigger Root Cause Diagnostic | Runtime data QA | Resume read-only diagnosis of why P26J had 8 closing-window cycles with `fetched=false`, `api_calls_today=2`, and no closing rows. | Root cause classification exists without code/runtime mutation. |
| **P1** | Context-Lock Preflight + Commit-Scope Guard | Agent / repo governance | Ensure Betting tasks stop on Stock/P48/P49 contamination and do not stage runtime files or untracked P26J scripts accidentally. | Pre-flight reports repo/branch/log/grep hygiene and staged files are whitelist-only. |
| **P2** | Untracked P26J Script Boundary | Repo hygiene | Classify `scripts/p26j_*.py` as temporary, reusable diagnostic candidates, or unknown without staging or deleting them. | P26K report states disposition and leaves files untouched unless separately authorized. |
| **P3** | Scheduler / Quota / Next Trigger Decision Gate | Ops architecture | Decide after P26K whether the next action is scheduler patch, daemon ops fix, source monitor, quota policy fix, or continued observation. | Recommendation is evidence-backed and no patch is made in diagnostic-only scope. |
| **P4** | Heartbeat-vs-Fetch Watchdog Design | Observability | Preserve design-only alert logic for daemon alive but no fetch during closing windows. | Alert condition is defined; implementation remains deferred. |
| **P5** | COMPLETE_PAIR Recovery Gate + P25C Bootstrap | Validation | Keep bootstrap blocked until COMPLETE_PAIR >=300 and line-comparable filters pass. | Bootstrap remains blocked or runs only after threshold. |
| **P6** | Coverage Stability Audit | Data QA | Explain why COMPLETE_PAIR dropped `220 -> 219`. | Delta is tied to eligibility, source snapshot changes, line comparability, de-duplication, or documented data drift. |
| **P7** | MLB Prediction Quality Work Re-entry | Prediction | Resume P29/P30A model work only after P26K produces a stable CLV capture path or CTO explicitly reprioritizes. | Model work stays paper-only and cannot supersede data capture gates. |
| **P8** | TSL Market Paper Recommendation Contract | Product | Keep MLB/TSL paper recommendation design aligned to traceable odds, model probability, edge, source, time, risk gate, and `paper_only=true`. | Recommendation release remains blocked until data validation gates clear. |
| **P9** | Repo / PR Governance Gate | Engineering governance | Maintain canonical repo/branch discipline; no new repo/worktree/branch or protected-branch bypass. | No cross-project or raw runtime files enter Betting commits. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until validated data, evidence, live/licensed source path, fail-safe, monitoring, and approval exist. | `production_ready=false` until explicit approval. |

### 0D.5 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: P26K closing fetch trigger root-cause diagnostic, now unblocked by context hygiene.
- [Confirmed] Upgraded to P1: context-lock preflight and commit-scope guard for multi-project safety.
- [Confirmed] Upgraded to P2: untracked P26J script boundary classification.
- [Confirmed] Downgraded: repeating context hygiene as the main task; it is complete unless contamination reappears.
- [Confirmed] Downgraded: P29/P30A model quality and product recommendation work behind P26K.
- [Confirmed] Paused: P25C bootstrap until COMPLETE_PAIR >=300.
- [Confirmed] Paused: scheduler patch, daemon restart, live API calls, crawler changes, manual snapshots unless explicitly authorized.
- [Confirmed] Retired: treating conversation-level Stock drift as repo-level contamination after clean grep/log evidence.
- [Confirmed] Retired: producing new worker prompts from CTO roadmap analysis while the strict restriction forbids worker prompts.

### 0D.6 Today Focus

1. Keep `BETTING_CONTEXT_CLEAN` as the current project state.
2. Execute no functional development in this CTO step; return the next technical priority to P26K.
3. Keep P26K read-only: diagnose trigger/quota/`next_trigger_minutes`/timezone/schedule/source/governance causes without patching.
4. Protect commit scope: do not stage raw feed, runtime files, generated outputs, `CEO-Decision.md`, `active_task.md`, or untracked `scripts/p26j_*.py` unless separately authorized.

No new repo, no new worktree, no branch switch, no daemon restart, no scheduler/crawler/dedup code change, no live odds API call, no manual snapshot fabrication, no bootstrap, no promotion, no champion replacement, no production proposal, and no worker task prompt from this CTO analysis.

Product direction remains two-lane:

- Lane 1: MLB pregame prediction and TSL paper-only recommendation rows, blocked until odds/source trace and validation gates are trustworthy.
- Lane 2: strategy optimization / simulation, blocked until formal pregame odds, closing line, outcomes, and source trace support statistically meaningful validation.

---

## 0C. Latest CTO Update - P26J Post-Window Verified, P26K Root Cause Next

This section supersedes section 0B where pair formation was still pending observation.

### 0C.1 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Canonical repo `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| HEAD | [Confirmed] `0ccd06d verify(p26j): post-window pair verification rerun - 09:12Z`. |
| Prior chain | [Confirmed] P26H `d644f3f`, P26I `60a73a7`, P26J readiness `34fc118`, P26J rerun `0ccd06d`. |
| P26J timing guard | [Confirmed] PASS at `2026-05-21T09:12:47Z`, after threshold `2026-05-21T09:10:00Z`. |
| Target 3469930.1 | [Confirmed] `PREGAME_ONLY_NO_CLOSING`; 7 rows, 0 closing rows, `markets=[]`. |
| Target 3469931.1 | [Confirmed] `PREGAME_ONLY_NO_CLOSING`; 8 rows, 0 closing rows, `markets=[]`. |
| Target pair result | [Confirmed] `target_pair_delta=0`; neither expected P26G target became COMPLETE_PAIR. |
| Coverage | [Confirmed] COMPLETE_PAIR moved `220 -> 219`; P25C bootstrap remains not eligible. |
| Daemon continuity | [Confirmed] 8 daemon cycles in `07:00Z-09:00Z`; every cycle had `fetched=false`, `api_calls_today=2`, `next_trigger_minutes=null`. |
| Key diagnosis | [Confirmed] Daemon heartbeat existed, but fetch trigger did not execute during the true closing window. |
| P26J tests | [Confirmed from handoff/report] 75 PASS / 0 FAIL; CTO review did not rerun tests. |
| Commit scope | [Confirmed] P26J commit contains 5 whitelisted artifact/report files; no raw feed/runtime state staged in that commit. |
| P26J label caution | [Inferred] `P26J_TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED` may be too broad until P26K separates source availability from trigger/quota/scheduler logic. |

### 0C.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P26J correctly waited for the post-window Timing Guard before judging the two expected target pairs. |
| [Aligned] | P26J correctly blocked P25C bootstrap because COMPLETE_PAIR is 219 (<300). |
| [Aligned] | P26J preserved read-only / paper-only governance: no daemon restart, no scheduler patch, no crawler change, no manual API call, no bootstrap. |
| [Drift] | The previous P26H/P26G roadmap expected pair formation monitoring; P26J proved the selected target pairs did not form. The immediate problem is now fetch-trigger root cause, not more waiting. |
| [Missing] | Roadmap did not explicitly distinguish daemon heartbeat from actual fetch execution. |
| [Missing] | Roadmap did not explicitly capture that `status=captured` can coexist with `fetched=false` and zero new API calls. |
| [Outdated] | Waiting for `17:10` / `09:10Z` is no longer current; post-window verification is complete. |
| [Outdated] | Treating P26J's source-unavailable label as final root cause is premature until trigger/quota/timezone/scheduler gates are audited. |
| [Blocked] | CLV bootstrap, strategy simulation, MLB paper recommendation release, optimizer promotion, and production proposal remain blocked by fetch-trigger uncertainty plus COMPLETE_PAIR=219. |

### 0C.3 Reprioritized P0-P10 From P26J

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P26K Closing Fetch Trigger Root Cause Diagnostic | Runtime data QA | Read-only audit why 8 closing-window daemon cycles all had `fetched=false` and `api_calls_today=2`. | Root cause classification exists: trigger rule, quota/call limit, `next_trigger_minutes`, timezone, schedule target, source state, governance flag, or inconclusive. |
| **P1** | Scheduler / Quota / Next Trigger Decision Gate | Ops architecture | Decide whether the next step is scheduler patch, daemon ops fix, source monitor, or continued observation. | Recommendation is evidence-backed and does not mutate code/runtime without explicit authorization. |
| **P2** | Heartbeat-vs-Fetch Watchdog Design | Observability | Design a non-invasive guard for "daemon alive but no fetch during closing window". | Design-only artifact or roadmap entry defines alert conditions; no implementation until authorized. |
| **P3** | COMPLETE_PAIR Recovery Gate + P25C Bootstrap | Validation | Keep bootstrap blocked until COMPLETE_PAIR >=300 and line-comparable filters pass. | Bootstrap either remains blocked with reason or runs only after threshold. |
| **P4** | Coverage Stability Audit | Data QA | Explain why COMPLETE_PAIR dropped `220 -> 219`. | Coverage calculation inputs, eligibility, line comparability, and missingness deltas are documented. |
| **P5** | P26 Artifact SSOT Compression | Roadmap governance | Keep P26H/P26I/P26J/P26K handoffs from multiplying ambiguity. | One canonical root-cause report points to prior evidence instead of re-litigating timing guards. |
| **P6** | P26 Runtime Validation Hygiene | QA | Continue targeted tests and forbidden scans for P26 artifacts without staging raw feed/runtime files. | Validation results recorded; commit scope remains whitelist-only. |
| **P7** | MLB Prediction Quality Work Re-entry | Prediction | Resume P29/P30A Orchestrator/model work only after CLV capture root cause has a stable path. | Model work stays paper-only and cannot supersede data capture gates. |
| **P8** | TSL Market Paper Recommendation Contract | Product | Preserve the MLB/TSL paper recommendation goal with traceable odds, model probability, edge, risk gate, and `paper_only=true`. | Recommendation contract exists, but release remains blocked until data validation gates clear. |
| **P9** | Repo / PR Governance Gate | Engineering governance | Keep canonical repo/branch discipline; no new repo/worktree/branch without explicit authorization. | No raw runtime/data files staged; PR/merge actions remain explicit-YES gated. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until validated data, evidence, live/licensed source path, fail-safe, monitoring, and approval exist. | `production_ready=false` until explicit approval. |

### 0C.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: P26K closing fetch trigger root-cause diagnostic.
- [Confirmed] Upgraded to P1: scheduler/quota/next-trigger decision gate.
- [Confirmed] Upgraded to P2: heartbeat-vs-fetch watchdog design, design-only.
- [Confirmed] Downgraded: P26H pair formation monitor; P26J completed the decisive post-window check.
- [Confirmed] Downgraded: P29/P30A Orchestrator work; still useful, but not today's blocker while closing fetch does not execute.
- [Confirmed] Paused: P25C bootstrap until COMPLETE_PAIR >=300.
- [Confirmed] Paused: scheduler patch, daemon restart, live API calls, crawler changes, manual snapshots unless explicitly authorized.
- [Confirmed] Retired: waiting for 17:10 / 09:10Z for these two targets.
- [Confirmed] Retired: using heartbeat presence as proof that fetch ran.

### 0C.5 Today Focus

1. Perform P26K read-only root-cause diagnostic for `fetched=false` during the true closing window.
2. Separate source unavailability from trigger rule, quota/call limit, `next_trigger_minutes`, timezone, schedule-target, and governance-flag causes.
3. Keep P25C bootstrap, strategy simulation, paper recommendation release, promotion, and production proposal blocked.

No daemon restart, no scheduler/crawler/dedup code change, no live odds API call, no manual snapshot fabrication, no raw feed commit, no promotion, no champion replacement, and no production proposal.

Product direction remains two-lane:

- Lane 1: MLB pregame prediction and TSL paper-only recommendation rows, blocked until odds/source trace and validation gates are trustworthy.
- Lane 2: strategy optimization / simulation, blocked until formal pregame odds, closing line, outcomes, and source trace support statistically meaningful validation.

---

## 0B. Latest CTO Update - P26G Force Closing Runtime Confirmed

This section supersedes section 0 where runtime CLV coverage gates conflict with model-quality / Orchestrator work.

### 0B.1 Current System Truth

| Area | Status |
|---|---|
| Repo / branch | [Confirmed] Canonical repo `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `main`. |
| P26F | [Confirmed] Commit `8a98f52` is HEAD: `fix(p26f): force-save closing snapshots through dedup bypass`. |
| P26G artifacts | [Confirmed] JSON/MD/BettingPlan artifacts exist locally, but are currently untracked. |
| Daemon restart | [Confirmed] Old PID `1715` -> new PID `15022`; first tick reported `TSL fetch OK: 7 snapshots`. |
| Force closing runtime | [Confirmed] `force_closing_snapshot=True` rows = 10; `dedup_bypassed=True` rows = 7. |
| Closing write | [Confirmed] One row was within closing window (`gap=-0.53h`), but it had no matching pregame snapshot. |
| Coverage | [Confirmed] COMPLETE_PAIR remains 220 before/after P26G; delta = 0. |
| Bootstrap | [Confirmed] P25C bootstrap did not run and must not run while COMPLETE_PAIR < 300. |
| P26G validation | [Unknown] Handoff did not include full Phase 8 test / forbidden-scan output; CTO review did not rerun tests. |
| P26G commit | [Confirmed] No P26G commit is visible in `git log`; P26G artifacts are untracked. |
| Runtime dirty files | [Confirmed] Worktree has many daemon/runtime/data/output modifications; do not include raw feed/runtime files in roadmap-driven commits. |

### 0B.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P26G correctly verified the P26F force-closing mechanism at runtime after daemon restart. |
| [Aligned] | P25C bootstrap was correctly blocked because COMPLETE_PAIR stayed at 220 (<300). |
| [Drift] | Prior roadmap section 0 focused on P29/P30A model-quality work. Current runtime data gate shows CLV pair formation is the immediate maturity blocker. |
| [Missing] | Roadmap did not yet encode that force-closing rows alone do not imply COMPLETE_PAIR growth. |
| [Missing] | Roadmap did not yet separate P26G delivery closure from P26H pair-formation monitoring. |
| [Outdated] | Any plan to run bootstrap immediately after force-closing success is invalid until pair-level coverage reaches 300. |
| [Blocked] | Formal CLV bootstrap / downstream strategy diagnostics remain blocked by COMPLETE_PAIR=220. |

### 0B.3 Reprioritized P0-P10 From P26G

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P26G Delivery Closure + P26H Pair Formation Monitor | Data QA + runtime observation | Confirm P26G artifacts/validation state, inventory force-closing rows, and diagnose which rows have matching pregame snapshots. | P26G artifacts accounted for; force-closing rows classified by match; COMPLETE_PAIR before/after reported; no bootstrap if <300. |
| **P1** | Pregame Coverage Gap Diagnostic | Data QA | Determine why the first force-closing row lacked pregame and whether this is natural late listing or a pregame capture bug. | Missing-pregame reason categories and counts exist; no manual snapshot fabrication. |
| **P2** | Closing Cadence Impact Estimate | Ops | Estimate whether 15-minute interval is still a blocker and whether 5-minute cadence would materially improve pair formation. | Diagnostic-only estimate; no daemon/scheduler change without explicit authorization. |
| **P3** | P25C Bootstrap Gate | Validation | Run bootstrap only after COMPLETE_PAIR >=300 and line-comparable filtering is satisfied. | Bootstrap result exists or remains blocked with threshold reason. |
| **P4** | P26 Runtime Validation Hygiene | QA | Rerun targeted tests and forbidden scan for P26F/P26G/P26H artifacts. | Tests and scan results recorded; raw feed/runtime files excluded from commits. |
| **P5** | TSL CLV Data SSOT | Data governance | Keep source snapshots, history counts, daemon state, and derived pair counts distinct. | Raw feed is never committed as artifact; reports cite source trace and hash/count when needed. |
| **P6** | MLB Prediction Quality Work Re-entry | Prediction | Revisit P29/P30A model quality only after CLV data gate has a stable monitoring path. | Orchestrator work remains paper-only and cannot supersede CLV coverage gate. |
| **P7** | TSL Market Recommendation Contract | Product | Maintain paper recommendation contract for markets with traceable odds/pregame/closing evidence. | Market rows require source, timestamp, edge, risk gate, and `paper_only=true`. |
| **P8** | Daily Paper Ops / Drift Monitor | Ops | Monitor COMPLETE_PAIR, force-closing rows, missing-pregame, missing-closing, and bootstrap readiness. | Daily report explains whether bootstrap is allowed. |
| **P9** | Repo / PR Governance Gate | Engineering governance | Keep branch/repo workflow disciplined; do not create repos/worktrees or merge protected PRs without approval. | Canonical branch stays `main`; PR actions remain explicit-authorization only. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until formal evidence, licensed/live data path, fail-safe, monitoring, and approval exist. | `production_ready=false` until explicit approval. |

### 0B.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: P26H force-closing pair formation monitor and P26G delivery closure.
- [Confirmed] Upgraded to P1: missing-pregame / pair-formation root cause analysis.
- [Confirmed] Downgraded: P29/P30A Orchestrator work; still valuable, but not today's first blocker while CLV coverage is below threshold.
- [Confirmed] Paused: P25C bootstrap until COMPLETE_PAIR >=300.
- [Confirmed] Paused: daemon interval change until diagnostic-only impact estimate and explicit authorization.
- [Confirmed] Retired: assuming force-closing snapshot count equals COMPLETE_PAIR growth.

### 0B.5 Today Focus

1. Close P26G delivery uncertainty: artifacts, validation state, and commit state.
2. Run P26H pair-formation monitoring: force-closing row inventory, matching pregame lookup, COMPLETE_PAIR before/after.
3. Keep P25C bootstrap blocked unless COMPLETE_PAIR >=300.

No daemon restart, no scheduler code change, no raw data modification, no manual snapshot fabrication, no promotion, no champion replacement, and no production proposal.

---

## 0. Latest CTO Update — P29 Completed, P30A Is Next

This section supersedes the older P22/P23 priority order below where the two conflict.

### 0.1 Current System Truth

| Area | Status |
|---|---|
| P23 | [Confirmed] `P23_GATE_AND_REPRODUCIBILITY_RECONCILED`; reported P17 `69/69 PASS`, P12-P17 `323/323 PASS`. |
| P24 | [Confirmed] CLV robustness diagnostic completed; CLV signal remained not robust. |
| P25 | [Confirmed] CLV failure root cause audit completed; primary issue was a CLV construction bug from non-line-aware matching. |
| P26 | [Confirmed] Line-aware CLV repair completed; old positive CLV mean was largely artifact-driven; clean CLV remained inconclusive. |
| P27 | [Confirmed] Per-market clean CLV isolation completed; all clean CLV markets inconclusive; OE exclusion did not recover signal. |
| P28 | [Confirmed] MLB model repair attempted; `P28_MODEL_REPAIR_NO_IMPROVEMENT`; Full Orchestrator Brier `0.2487`, Simple LogReg Brier `0.2451`. |
| P29 | [Confirmed] Orchestrator proxy noise ablation and external data contract design completed. |
| P29 tests | [Confirmed from report] P26 `23/23 PASS`, P17 `64/64 PASS`, P13-P17 `296/296 PASS`, total `383/383 PASS`; not rerun in this CTO review. |
| P29 best candidate | [Confirmed] Proxy ablation best variant `MARL w_market=0.50`, Brier `0.244154`; pure market Brier `0.244354`. |
| P29 limitation | [Confirmed] P29 ablation is diagnostic/proxy, not a production Orchestrator mutation or validated real-pipeline result. |
| External data contracts | [Confirmed] SP, bullpen, batting form, lineup/injury proxy, park/weather contracts designed; no data fetched. |
| Champion / promotion | [Confirmed] `fixed_edge_5pct` preserved; promotion frozen; no production proposal. |
| Existing active task file | [Outdated] `00-Plan/roadmap/active_task.md` exists but still points to older P23 gate work; do not treat it as current unless separately authorized for update. |

### 0.2 Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P29 correctly follows P28: after CLV repair showed no usable signal and model repair failed, it investigates why Full Orchestrator is worse than simpler baselines. |
| [Aligned] | External data contracts align with the product goal of improving MLB pregame prediction quality before recommendation/promotion. |
| [Drift] | The older roadmap P0/P1 around P22/P23 is now outdated because P23-P29 artifacts exist locally. |
| [Drift] | P29 finds a candidate, but the candidate is proxy-only. The next P0 is validation in the real Orchestrator path, not immediate weight change. |
| [Missing] | Roadmap lacked an explicit timestamp/leakage audit for market probability, despite pure market Brier being the strongest baseline. |
| [Outdated] | CLV-positive interpretation from P22 is retired; P26/P27 invalidated it after line-aware repair. |
| [Blocked] | Strategy optimizer / promotion remains blocked until real Orchestrator validation and market timestamp safety clear. |

### 0.3 Reprioritized P0-P10 From P29

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P30A Real Orchestrator `w_market` Validation | Prediction architecture | Validate P29's proxy `w_market=0.50` finding in the real Orchestrator pipeline without changing production defaults. | Sweep includes at least 0.00/0.30/0.40/0.45/0.50/0.55/0.60/1.00; reports Brier/logloss/hit rate/sample size; no production mutation. |
| **P1** | Market Baseline Timestamp / Leakage Audit | Data QA | Prove market probability is pregame-safe before using pure market or higher `w_market` as evidence. | Each market probability source has timestamp lineage; closing/postgame odds are excluded or result is marked `LEAKAGE_RISK`. |
| **P2** | External Data Contract Freeze | Data architecture | Keep SP/bullpen/batting/lineup/weather contracts design-only and source-reviewed before implementation. | Contracts marked `contract_only=true`; no live crawler/API or production dependency added. |
| **P3** | Orchestrator Simplification Decision Gate | Architecture governance | Decide whether real Orchestrator should simplify, raise market weight, or keep current path after P0/P1. | Decision artifact remains paper-only; no champion replacement or production proposal. |
| **P4** | Starting Pitcher Data Prototype | Feature engineering | If P0/P1 clear and scope is approved, prototype SP season-to-date features with strict no-lookahead rules. | Historical backtest-ready SP features with `snapshot_ts < game_start` and leakage audit. |
| **P5** | Model Quality Repair Loop | Prediction | Continue Brier/ECE/logloss repair only with real-pipeline evidence and no leakage. | Improvement is out-of-sample and compared to market, LogReg, and Full Orchestrator. |
| **P6** | TSL Market Taxonomy + Recommendation Contract | Product | Map MLB predictions to TSL markets with source trace, odds, edge, risk gate, and `paper_only=true`. | Market contracts cover MNL/HDC/OU/OE/F5/team-total; unsupported markets have blocked-state semantics. |
| **P7** | Strategy Simulation Re-entry Gate | Strategy | Re-enter simulation only after P0-P5 provide reliable probabilities. | Strategy experiments remain paper-only; no optimizer promotion. |
| **P8** | Daily Paper Ops / Drift Monitor | Ops | Track Brier/ECE/logloss/CLV/no-bet/missing-data/source drift. | Daily report explains both predictions and abstentions. |
| **P9** | Repo / PR Governance Gate | Engineering governance | Keep PR #2 and consolidation PR explicit-YES gated. | No merge without `YES: merge PR #2`; no force push. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until multi-season evidence, live/licensed data, fail-safe, monitoring, and human approval exist. | `production_ready=false` until explicit approval. |

### 0.4 Items Upgraded, Downgraded, Paused, Retired

- [Confirmed] Upgraded to P0: real Orchestrator validation of P29 `w_market=0.50`.
- [Confirmed] Upgraded to P1: market timestamp/leakage audit.
- [Confirmed] Downgraded: external SP/bullpen/batting implementation; design is ready, but integration waits behind P0/P1.
- [Confirmed] Paused: optimizer promotion, champion replacement, production proposal, live API/crawler changes.
- [Confirmed] Retired: P22 positive CLV interpretation and non-line-aware CLV conclusions.
- [Confirmed] Retired: direct use of P29 proxy ablation as production evidence.

### 0.5 Today Focus

1. Validate the P29 `w_market=0.50` candidate in the real Orchestrator path.
2. Audit market probability timestamps before trusting pure market or market-heavy variants.
3. Keep external data contracts frozen as design-only.

No optimizer promotion, no champion replacement, no production proposal, no live odds API, and no TSL crawler modification.

---

## 1. Source Roadmaps Integrated

- [Confirmed] `00-Plan/roadmap/betting_roadmap_20260504.md`
- [Confirmed] `00-Plan/roadmap/betting_roadmap_20260513.md`
- [Confirmed] `00-Plan/roadmap/betting_roadmap_20260514_single_repo_consolidation.md`
- [Confirmed] `00-Plan/roadmap/betting_roadmap_20260515_mlb_product_plan.md`
- [Confirmed] `00-Plan/roadmap/betting_roadmap_20260516_p39j_odds_consolidation.md`

Date integrity note:

- [Confirmed] Current environment date is 2026-05-20.
- [Confirmed] P22 artifacts and reports exist with `20260523` labels.
- [Inferred] Treat `20260523` as artifact labels from the current handoff, not evidence that the operating date has advanced beyond 2026-05-20.

---

## 2. Current System Truth

| Area | Status |
|---|---|
| GitHub PR #2 | [Confirmed] `OPEN`, `MERGEABLE`, `CLEAN`; `replay-default-validation` PASS. Do not merge without explicit `YES: merge PR #2`. |
| P19 CLV data gate | [Confirmed] `valid_clv_pairs=233`, data threshold PASS, CEO hold was the blocker. |
| P20/P21 | [Confirmed] CEO decision deferred; no CLV validation executed in those phases. |
| P22 | [Confirmed] `P22_CLV_VALIDATION_ONLY_COMPLETED`, formal TSL data CLV validation completed. |
| P22 tests | [Confirmed from report] P17 standalone and P12-P17 governance suite report `347/347 PASS`; not rerun in this CTO review. |
| P22 CLV summary | [Confirmed] `valid_pairs_used=236`, `total_outcome_observations=2499`, mean CLV `+0.2332%`, std `8.7212%`, positive rate `32.65%`. |
| Market CLV | [Confirmed] HDC mean `+1.2103%`, MNL mean `-0.2490%`, OU `+0.1158%`, OE `+0.0083%`, TTO `+0.3281%`. |
| Promotion | [Confirmed] Frozen; no optimizer promotion, no champion replacement, no production proposal. |
| Champion | [Confirmed] `fixed_edge_5pct` preserved. |
| P23 gate | [Drift] P22-B says `p23_allowed=true` for `CLV_REPORT_REVIEW_ONLY`; P22-E/final report says `p23_allowed=false` / next owner CEO. Must reconcile before P23 execution. |
| Pair count delta | [Blocked] P19 has 233 pairs; P22 uses 236 pairs. P22 marks match OK, but root cause is not explained. |
| Data version drift | [Confirmed] P19 source reports 2,747 records; P22 report says 2,772; current `data/tsl_odds_history.jsonl` has 2,785 lines. Reproducibility must be pinned before stronger claims. |

---

## 3. Roadmap Alignment Assessment

| Tag | Assessment |
|---|---|
| [Aligned] | P22 correctly followed the approved `CLV_VALIDATION_ONLY` boundary: paper-only, no live API, no crawler modification, no production proposal, no promotion. |
| [Aligned] | P22 answers the prior P19-P21 blocker: data threshold was sufficient and CEO approval unlocked validation-only analysis. |
| [Drift] | The active historical roadmap still contains older P8/MARL, PR #2, and P22 sequencing sections; this canonical roadmap supersedes those priority orders. |
| [Missing] | A single canonical `00-Plan/roadmap/roadmap.md` was absent before this update. |
| [Missing] | Roadmap did not yet encode the P22-B vs P22-E `p23_allowed` inconsistency as a P0 blocker. |
| [Missing] | Roadmap did not yet require explaining the 236 vs 233 pair delta before further analysis. |
| [Outdated] | Repeating CEO decision follow-up phases is retired; CEO already approved P22 validation-only. |
| [Outdated] | Treating HDC positive CLV as market promotion evidence is not allowed; market diagnostics must come first. |
| [Blocked] | P23 report review cannot safely start until the P23 gate contradiction and pair-count reproducibility issue are resolved. |

---

## 4. Latest Phase Status

| Phase | Status | Roadmap call |
|---|---|---|
| P19 | [Confirmed] Completed; canonical CLV data sufficient at 233 valid pairs. | Keep as baseline evidence. |
| P20 | [Confirmed] Completed as CEO decision required / deferred. | Retired; no repeat needed. |
| P21 | [Confirmed] Completed as CEO decision required / deferred. | Retired; no repeat needed. |
| P22 | [Confirmed] Completed validation-only with formal data. | Use as input to diagnostics only. |
| P23 | [Blocked] Not approved for promotion; report-review scope conflicts across P22 artifacts. | Reconcile gate first; then diagnostic-only if explicitly allowed. |
| P24+ | [Blocked] Not allowed. | Requires separate CEO approval after P23 diagnostics. |

---

## 5. Reprioritized P0-P10

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P22/P23 Governance + Reproducibility Reconciliation | Governance + data QA | Resolve P22-B vs P22-E `p23_allowed` conflict and explain 236 vs 233 CLV pair delta with source snapshot/version evidence. | Single source of truth says whether P23 diagnostic-only is allowed; pair-count delta root cause documented; no promotion path opened. |
| **P1** | CLV Robustness Diagnostic Only | Analytics | If P0 clears, review CLV distribution, outliers, bootstrap CI, median/trimmed mean, and market-level stability. | Report classifies CLV signal as descriptive robust/weak/uncertain; no profitability or betting recommendation claim. |
| **P2** | TSL Market Taxonomy + Evidence Contract | Product architecture | Define market contracts for MNL, HDC, OU, OE, TTO, F5, and team totals with blocked-state semantics. | Roadmap/product contract says which markets are implemented, diagnostic-only, or blocked; no market release. |
| **P3** | CLV-to-Strategy Readiness Gate | Strategy governance | Decide whether CLV evidence is strong enough to justify strategy optimizer research. | `fixed_edge_5pct` remains preserved unless separate CEO approval exists; optimizer promotion remains frozen. |
| **P4** | Strategy Simulation Optimization v2 | Strategy | Run policy optimization only after P1/P3 clear; use true outcome and CLV-aware diagnostics, not EV-proxy promotion. | Bootstrap/drawdown/ROI/CLV/turnover evidence exists; champion replacement still requires explicit approval. |
| **P5** | MLB Prediction Quality Loop | Prediction | Continue Brier/ECE/calibration/model probability audits for MLB predictions behind the recommendation rows. | Quality gates explain model probability reliability before larger market expansion. |
| **P6** | Data Versioning and Artifact SSOT | Data governance | Pin source file line counts, hashes, date ranges, and derivation logic for P19/P22/P23 artifacts. | Future CLV reports are reproducible from declared input snapshots. |
| **P7** | Market-Level Coverage Expansion | Data + product | Expand market diagnostics only where source coverage and pair logic are reproducible. | Per-market sample quality and missingness are reported before modeling. |
| **P8** | Daily Paper Ops / Drift Monitor | Ops | Track CLV, Brier, ECE, no-bet rate, missing data, pair counts, and stale source drift. | Daily paper-only report explains both actions and abstentions. |
| **P9** | Repo / PR Governance Gate | Engineering governance | Keep PR #2 and consolidation PR as explicit YES-gated workflow items. | PR #2 only merges after user says `YES: merge PR #2`; no force push. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until multi-season evidence, live/licensed data path, fail-safe, monitoring, and human approval exist. | `production_ready=false` until explicit approval. |

---

## 6. Items Upgraded, Downgraded, Merged, Paused, Retired

### Upgraded to P0

- [Confirmed] P22/P23 gate inconsistency: `p23_allowed=true` in one artifact, `p23_allowed=false` in the gate refresh/final report.
- [Confirmed] 236 vs 233 pair-count delta plus source file growth from P19 to P22/current state.

### Downgraded

- [Confirmed] Optimizer promotion / champion replacement: remains below P3 and frozen.
- [Confirmed] PR #2 merge: standing governance task, not product P0, unless the user explicitly authorizes merge.
- [Confirmed] Multi-market recommendation release: after taxonomy and diagnostics, not before.

### Merged

- [Inferred] P20/P21 CEO follow-up loops are merged into one historical "CEO deferred" state; no need to repeat.
- [Inferred] CLV validation, pair sample review, and hold refresh are now one P22 evidence package.

### Paused

- [Confirmed] P23+ promotion, optimizer promotion, champion replacement, production proposal.
- [Confirmed] Live odds API and TSL crawler modification.

### Retired

- [Confirmed] Repeating the frozen Statcast batting rolling feature track.
- [Confirmed] Treating EV-proxy ROI as optimizer fitness.
- [Inferred] Generic roadmap churn without artifact/test impact.

---

## 7. Critical Blockers

| Blocker | Impact | Why it blocks | Priority | Acceptance standard |
|---|---|---|---|---|
| P23 gate contradiction | Governance, workflow safety | P22-B allows P23 review-only, while P22-E/final says P23 blocked and next owner CEO. | P0 | One canonical gate state with scope and owner; no promotion permissions. |
| Pair-count reproducibility | Data quality, CLV validity | P19=233, P22=236, current source line count grew again; no root-cause explanation. | P0 | Delta explained by source snapshot, derivation rule, duplicate handling, or reclassification. |
| CLV robustness unknown | Product correctness | Mean is small vs std and positive rate is 32.65%; HDC may be outlier-driven. | P1 | CI/trimmed/outlier/market diagnostics show signal category. |
| Market taxonomy gap | Product maturity | User goal requires TSL betting items, but evidence contract is still incomplete. | P2 | TSL market contract covers supported, diagnostic-only, and blocked markets. |
| Promotion freeze | Strategy governance | P22 was validation-only; no policy/champion change is authorized. | P3 | Any strategy research remains report-only until separate approval. |
| PR #2 open | Repo governance | Main sync still waits explicit merge approval. | P9 | Merge only after `YES: merge PR #2`; otherwise keep status visible. |

---

## 8. Today Focus

1. **P0 first:** reconcile P23 gate and pair-count reproducibility.
2. **Then P1:** diagnostic-only CLV robustness review, with no promotion.
3. **Parallel planning only:** TSL market taxonomy contract, because it directly supports MLB -> Taiwan Sports Lottery recommendation but must not release bets.

No optimizer promotion, no champion replacement, no production proposal, no live odds API, and no TSL crawler modification.

---

## 0E. P26K Update — 2026-05-23 (Root Cause Confirmed)

**P26K CLOSED**: `P26K_SOURCE_STATE_TRULY_EMPTY_CONFIRMED`

**Root causes identified**:
- **Primary** `SOURCE_STATE_TRULY_EMPTY`: TSL stopped returning NPB games 3469930.1/3469931.1 from its pre-game betting menu ~4-5.6h before game start (03:24Z/04:55Z). Daemon was executing correctly (TSL called every 15min with force_closing=True); no data to capture.
- **Secondary** `QUOTA_HARD_CAP`: OddsAPI MLB external closing hard cap=2/day hit at 02:24Z (15min after P26G restart), blocking all 8 closing-window cycles (07:10-08:56Z).

**CEO hypothesis** `STARTUP_ONLY_FETCH_ARCHITECTURE`: `PARTIALLY_REFUTED` (TSL runs every 15min, not startup-only)

**COMPLETE_PAIR**: 219→223 (recovered, no CLV sample impact)

**P26L required**: NO

**Next recommended actions**:
1. `SOURCE_AVAILABILITY_MONITOR_REQUIRED` — detect when TSL removes games from pre-game list
2. `QUOTA_POLICY_REVIEW_REQUIRED` — reserve OddsAPI quota for closing window
