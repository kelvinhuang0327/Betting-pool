# Betting-pool Roadmap v8 — P39J Post-Push + Odds / Consolidation Decision

**Date:** 2026-05-16  
**Owner:** CTO agent  
**Canonical target:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Temporary source worktree:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean`, remote HEAD `origin/p13-clean = 1b50704`  
**User directive:** Do not create additional `Betting-pool*` repos. Consolidate useful work into `Betting-pool` and retire extra folders only after validation and explicit approval.  
**Operating mode:** `PAPER_ONLY=true`, `production_ready=false`, `NO_REAL_BET=true`.  
**Active marker:** `CTO_BETTING_ROADMAP_V8_P39J_ODDS_CONSOLIDATION_20260516_READY`

---

## 0C. CEO CLV Validation Decision - 2026-05-20

**Update marker:** `CEO_BETTING_ROADMAP_V8_4_APPROVE_CLV_VALIDATION_ONLY_20260520_READY`

This update supersedes sections 0B, 0A, and 0 where they conflict.

Important date correction: the current operating date is `2026-05-20` Asia/Taipei. P20/P21 artifacts are labeled `20260521` and `20260522`; treat those as existing artifact labels from the handoff, not as evidence that the system date has advanced. New P22 artifacts created from this roadmap should use `20260520` unless the operator explicitly advances the run date.

### 0C.1 CEO Decision

The CEO decision is:

> **APPROVE_CLV_VALIDATION_ONLY. Start P22 as validation-only work. Do not promote optimizer, do not replace champion, do not write a production proposal, and do not claim profitability.**

Rationale:

- P19 canonical evidence reports `valid_clv_pairs = 233`, above the 200-pair gate.
- P20 and P21 both confirmed the data layer remains sufficient.
- The only remaining blocker was CEO decision absence, not engineering readiness.
- Repeating another decision-follow-up cycle would create low-value process churn.

This approval unlocks **CLV validation only**, not strategy promotion.

### 0C.2 Current System Truth

| Area | Observed state | CEO call |
|---|---|---|
| Canonical repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `codex/main-sync-20260516`, dirty/untracked state. | Stay in this repo; no new repo/worktree. |
| P17 regression | P21 report: P17 standalone `64/64 PASS`; P12-P17 regression `347/347 PASS`. | Keep as required preflight. |
| CLV pairs | P19/P20/P21: `valid_clv_pairs = 233`. | Data threshold satisfied for validation-only. |
| P19 gate | `clv_gate_status = BLOCKED_BY_CEO_HOLD`. | CEO hold is now lifted only for CLV validation. |
| P20/P21 decision | `DEFER_DECISION`; no decision file. | Superseded by this CEO decision. |
| Champion | `fixed_edge_5pct` preserved. | Keep preserved; no replacement. |
| Promotion | Frozen. | Keep frozen. |
| Scope | paper-only, no network call, no crawler modification. | Preserve. |

### 0C.3 Roadmap Alignment Gap

The prior roadmap correctly blocked expansion while `valid_clv_pairs` were unknown or insufficient. That is now stale:

- Forward/CLV data is no longer the dominant blocker; CEO decision was.
- CEO has now approved `CLV_VALIDATION_ONLY`.
- Therefore the next task should not ask for another CEO follow-up. It should execute a tightly scoped P22 validation branch: pair integrity review, validation-only contract, CLV distribution, and final gate refresh.

### 0C.4 Reordered P0-P10 From This Point

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P22 CEO Decision Materialization | Governance | Create a paper-only CEO decision artifact for `APPROVE_CLV_VALIDATION_ONLY` using current-date naming. | Decision artifact exists; approval scope is CLV validation only; all forbidden actions remain forbidden. |
| **P1** | P22 Pair Sample Integrity Review | Data QA | Review canonical 233 CLV pairs before calculating validation metrics. | Top 20, fixed-seed random 10, and invalid/edge samples are produced with source traces and timestamp gaps. |
| **P2** | P22 CLV Validation-Only Contract | Governance + tests | Encode allowed and forbidden scope for CLV validation. | Contract permits CLV calculation/reporting only; forbids optimizer promotion, champion replacement, production proposal, live odds API, crawler modification, profitability claim. |
| **P3** | P22 CLV Distribution + Market Summary | Analytics | Compute CLV distribution and market-level summary from approved pairs. | Paper-only JSON/MD reports with mean/median CLV, buckets, market split, and uncertainty notes. |
| **P4** | P22 Hold / Ready Gate Refresh | Governance | Decide whether P23 may start and keep scope validation-only. | `p23_allowed=true` only for CLV validation continuation; promotion remains frozen. |
| **P5** | P22 Final Validation | QA | Rerun P17 + P12-P17 regression and safety grep scans. | Tests pass or exact blocker; no live odds/crawler/prod/promotion/profitability violations. |
| **P6** | P23 CLV Interpretation Gate | Analytics | Interpret whether CLV evidence is favorable, neutral, or adverse. | No strategy promotion; only evidence classification and next research recommendation. |
| **P7** | P24 Strategy Policy Review Gate | Strategy | Revisit `fixed_edge_5pct` only after CLV interpretation exists. | Baseline may remain, be narrowed, or be flagged for research; no production claim. |
| **P8** | Optimizer Re-entry Gate | Strategy | Revisit MARL/optimizer only after CLV validation and interpretation are complete. | EV-proxy remains banned; optimizer promotion requires separate CEO approval. |
| **P9** | TSL Market Taxonomy Re-entry Gate | Product | Resume multi-market taxonomy after CLV validation clarifies moneyline evidence. | Paper-only schema work; no multi-market recommendation expansion without separate gates. |
| **P10** | Production Proposal Gate | Governance | Production remains blocked until multi-season CLV, licensed/live odds path, fail-safe, and explicit approval exist. | `production_ready=false`; no production proposal write. |

### 0C.5 Highest ROI Optimization Direction

**Most worth optimizing next: P0 -> P1 -> P2 -> P3.**

The next high-value question is no longer "may we validate CLV?" The CEO answer is yes, within a strict validation-only boundary.

The next question is:

> Do the 233 canonical CLV pairs show credible positive, neutral, or negative CLV evidence for the paper strategy, after sample integrity review?

### 0C.6 Stop Rules

- No new repo, worktree, or `Betting-pool*` directory.
- Do not merge PR #2 without explicit `YES: merge PR #2`.
- Do not call live odds APIs.
- Do not modify TSL crawler or odds ingestion.
- Do not write production proposal channel.
- Do not promote optimizer.
- Do not replace `fixed_edge_5pct` champion.
- Do not claim profitability.
- All artifacts remain `paper_only=true`.
- New P22 artifacts should use current-date suffix `20260520` unless the operator explicitly changes the run date.

---

## 0B. CEO Roadmap Realignment - 2026-05-19

**Update marker:** `CEO_BETTING_ROADMAP_V8_3_P17_HOLD_AND_CLV_UNBLOCK_20260519_READY`

This update supersedes the P0-P10 ordering in sections 0A and 0 where the plans conflict.

Important date note: the latest P17 handoff artifacts are named `20260602`, but the current operating date is `2026-05-19`. Treat `2026-06-02` as the artifact label from the existing worktree handoff, not as a canonical current-date claim.

### 0B.1 CEO Decision

The CEO decision is:

> **DEFER expansion. Do not start P18. Preserve `fixed_edge_5pct`, keep promotion frozen, and focus the next execution cycle on canonicalizing P17 plus unblocking CLV / forward coverage evidence.**

The system has two product goals:

1. MLB prediction -> Taiwan Sports Lottery paper recommendation.
2. Strategy simulation / optimization.

Both goals are currently blocked by the same evidence gap: **no forward pair coverage and no closing-line CLV validation**. The best next optimization is therefore not model complexity, MARL promotion, or multi-market expansion. It is the data/evidence gate that determines whether any strategy should be trusted.

### 0B.2 Current System Truth

| Area | Observed state | CEO call |
|---|---|---|
| Canonical repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `codex/main-sync-20260516`, dirty/untracked state. | Continue inside this repo only; no new repo/worktree. |
| P17 implementation | Present under existing `.claude/worktrees/awesome-mclean-f52768/`, not canonical root. | First task is canonicalization / evidence import review. |
| P17 tests | Handoff reports P17 alone `64 passed`; P12-P17 `347 passed`. | Accept as worktree evidence until canonical rerun passes. |
| P17 classification | `P17_HOLD_ENGINEERING_EXPANSION_NO_DECISION`. | Hold state remains valid. |
| P18 allowed | `false`. | Do not start P18. |
| CEO decision state | `DEFER_DECISION`, day 3 in P17 handoff. | CEO decision now: continue HOLD / no expansion. |
| Forward pairs | `0 / 200`. | Hard blocker for CLV validation and promotion. |
| CLV status | `BLOCKED_NO_CLOSING_LINE`. | Hard blocker for strategy promotion and production proposal. |
| Champion | `fixed_edge_5pct`, preserved. | Keep as deterministic paper baseline, not a production claim. |
| Promotion | `FROZEN`. | No optimizer promotion, no production proposal, no profitability claim. |
| Safety scan | 7 checks clean in P17 handoff. | Preserve guardrails in canonicalization. |

### 0B.3 Roadmap Alignment Gap

The previous 0A plan aimed at P8 true reward optimizer training after canonicalizing P0-P7 artifacts. The P17 handoff changes priority:

- Optimizer work is useful only after CLV / forward evidence exists.
- P18 is explicitly blocked.
- The governance contract now has P12-P17 hold-state evidence that must be represented in canonical root before any further phase is trusted.
- The active roadmap must therefore prioritize **hold-state continuity, forward coverage, closing-line availability, and evidence gates** before strategy expansion.

### 0B.4 Reordered P0-P10 From This Point

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P17 Canonicalization Gate | Governance | Bring P17 code/test/artifacts/reports from existing `.claude/worktrees/awesome-mclean-f52768/` into canonical paths after diff review. | Canonical root has P17 files; P17 alone and P12-P17 suite rerun pass; no new repo; no raw/prod data. |
| **P1** | CEO Hold Decision Artifact | Governance | Materialize CEO decision as HOLD / NO P18 / no promotion while blockers remain. | `ceo_hold_decision` artifact exists; `p18_allowed=false`; forbidden actions still blocked. |
| **P2** | Forward Coverage Read-Only Inventory | Data | Count existing eligible forward pairs and identify why current count is `0/200`. | Read-only report with pair count, source paths, missing fields, and unlock requirements; no crawler/API write. |
| **P3** | Closing-Line Availability Gate | Data | Determine whether closing-line data exists anywhere approved/read-only and whether CLV can be computed. | `CLV_READY`, `CLV_BLOCKED_NO_CLOSING_LINE`, or `CLV_BLOCKED_SOURCE_UNAPPROVED`. |
| **P4** | P18 Unlock Gate Contract | Governance + tests | Encode the exact conditions for P18 start: CEO approval plus forward pairs >= 200 plus closing-line CLV readiness. | Tests prove P18 remains blocked until all gates clear. |
| **P5** | Champion Preservation Audit | Strategy | Revalidate `fixed_edge_5pct` remains baseline only, not promotion, not production, not profitability claim. | Champion artifact says preserved/frozen; no optimizer promotion. |
| **P6** | Forward Paper Monitoring Loop | Ops | Run daily read-only monitoring for CEO decision, forward pair count, CLV availability, and missing-data reasons. | Daily paper-only artifact with stable schema and no network/crawler mutation. |
| **P7** | Data Unblock Decision Packet | CEO/Data | Present options to unblock CLV: approved API key, approved local CSV, or continue HOLD. | CEO-ready packet with cost/risk/provenance; no secret/raw data committed. |
| **P8** | True Reward Optimizer Re-entry Gate | Strategy | Revisit MARL/optimizer only after P18 unlock conditions are satisfied. | Optimizer remains blocked until P4 gates clear; EV-proxy still banned as fitness. |
| **P9** | TSL Market Taxonomy Re-entry Gate | Product | Resume multi-market taxonomy only after CLV/forward evidence gate is no longer the dominant blocker. | Schema work may resume as paper-only, but no market expansion recommendation before evidence gate. |
| **P10** | Production Proposal Gate | Governance | Production remains out of scope until multi-season CLV, live/licensed odds, fail-safe, and explicit human approval exist. | `production_ready=false`; no proposal channel write. |

### 0B.5 Highest ROI Optimization Direction

**Most worth optimizing next: P0 -> P1 -> P2/P3.**

The specific question for the next engineering cycle is:

> Why are forward pairs `0/200`, and what exact approved/read-only data path can produce closing-line CLV evidence without breaking paper-only governance?

Until that is answered, P18, optimizer promotion, multi-market expansion, and production proposal all remain blocked.

### 0B.6 Stop Rules

- No new repo, worktree, or `Betting-pool*` directory.
- Do not merge PR #2 without explicit `YES: merge PR #2`.
- Do not start P18 while `p18_allowed=false`.
- Do not modify TSL crawler or odds ingestion.
- Do not call live odds APIs.
- Do not write production proposal channel.
- Do not claim profitability.
- Do not use EV-proxy ROI as optimizer fitness.
- All artifacts remain `paper_only=true`.

---

## 0A. CTO Daily Execution Update - 2026-05-19

**Update marker:** `CTO_BETTING_ROADMAP_V8_2_P8_TRUE_REWARD_EXECUTION_20260519_READY`

This update supersedes the 2026-05-18 P0-P10 ordering where the two conflict. The product goal is now fixed around two axes:

1. **MLB prediction -> Taiwan Sports Lottery paper recommendation.**
2. **Strategy simulation / optimization using true outcomes, not EV-proxy fitness.**

### 0A.1 Current System Truth

| Area | 2026-05-19 observed state | CTO call |
|---|---|---|
| Canonical repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`, branch `codex/main-sync-20260516`, large pre-existing dirty/untracked state. | Do not create another repo; do not reset or clean. |
| P0-P7 runtime work | The handoff says P0-P7 completed; matching files/artifacts are present under existing `.claude/worktrees/beautiful-carson-bd520d/`. | Treat as recoverable evidence, but not yet canonicalized into the expected repo paths. |
| Canonical P7 artifact path | `data/paper_recommendations/` is absent in canonical root. | P8 cannot assume the expected path exists until artifact reconciliation is done. |
| P7 true outcome artifact | Existing worktree artifact has 2,430 rows, 2,374 joined rows, 97.7% outcome coverage, `paper_only=true`. | True reward records are sufficient after canonical path recovery. |
| Current best deterministic policy | `fixed_edge_5pct`: true ROI `+1.8384%`, hit rate `50.11%`, true outcome bets `1,319`, EV-proxy ROI `+20.2247%`. | Baseline to beat; keep it as deterministic fallback. |
| EV-proxy gap | Fixed edge strategies show about 18pp EV-proxy overstatement vs true PnL. | EV-proxy is banned as optimizer fitness. |
| Python environment | Bare `python3` lacks numpy/scipy; repo `.venv/bin/python` has numpy and scipy, pytest 9.0.3. | P8 is not environment-blocked if `.venv/bin/python` is used. |
| `marl_optimizer.py` | Exists at `wbc_backend/strategy/marl_optimizer.py`; `optimize_strategy(records, n_generations=50, n_candidates=10, seed=42)` imports in `.venv`. | Signature callable; architecture still needs true reward adapter verification. |
| Optimizer architecture risk | Current episode logic predicts from internal `PredictorParams`, expects `market_home_prob`, and settles at hard-coded -110 payout. | Do not call this "true reward optimized" unless the adapter maps P7 records and settlement uses actual selected side / actual odds / actual outcome. |
| PR #2 | Previous report says CI passed but merge awaits explicit `YES: merge PR #2`. | Standing governance gate only; do not make it product P0 unless user asks to merge. |

### 0A.2 Roadmap Alignment Gap

The v8.1 roadmap over-weighted PR #2 and generic odds input as immediate P0/P3. That was useful for governance on 2026-05-18, but it is no longer aligned with the latest runtime handoff:

- P0-P7 product artifacts now exist, but not in canonical expected paths.
- P8 has enough true-outcome evidence to attempt optimizer integration once artifacts are reconciled.
- The highest product leverage is not another broad roadmap pass; it is closing the **true reward optimizer loop** and proving whether MARL beats `fixed_edge_5pct`.
- TSL multi-market work remains important, but expanding markets before the moneyline true reward loop is verified would multiply untrusted policy behavior.

### 0A.3 Reordered P0-P10 From This Point

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | P0-P7 Artifact Canonicalization Gate | Governance + runtime | Reconcile the existing P0-P7 modules, scripts, tests, reports, and `data/paper_recommendations` artifacts from the existing worktree evidence into canonical repo paths. | Expected P0-P7 files exist in canonical root; no new repo; no raw/prod data; path audit report lists every recovered artifact. |
| **P1** | P8 MARL True Reward Optimizer Training | Strategy | Run `wbc_backend/strategy/marl_optimizer.optimize_strategy()` against P7 with-outcomes records using TRUE_OUTCOME reward. | `p8_marl_optimized_strategy_20260518.json` and report exist, or exact blocker classification is emitted. |
| **P2** | Optimizer Reward Contract Repair | Strategy | Ensure optimizer fitness uses actual outcome, selected side, actual moneyline payout, stake, drawdown, and fold-level holdout metrics. | No EV-proxy in fitness; no hard-coded -110 settlement unless odds are truly absent and clearly labeled as blocked. |
| **P3** | Baseline Preservation + Champion Gate | Strategy | Compare optimized policy against `fixed_edge_5pct` and keep deterministic baseline unless optimizer wins out of sample. | Champion decision: optimizer ready, optimizer ready but baseline still best, env blocked, architecture blocked, or true records blocked. |
| **P4** | Outcome Join Quality Repair | Data | Fix or explicitly isolate the 56 duplicate-key / doubleheader outcome join collisions. | Join key includes doubleheader/game id disambiguation; coverage and duplicate reports pass. |
| **P5** | Moneyline Robustness Validation | Prediction | Move beyond one 2025 proxy-closing backtest: fold stability, month/team drift, bootstrap CI, 2024->2025 or 2025->2026 holdout. | ROI, hit rate, drawdown, Brier/ECE/accuracy reported with confidence bands and holdout separation. |
| **P6** | TSL Market Taxonomy + Row Contract | Product | Define Taiwan Sports Lottery market schema for moneyline, run line, totals, first five, odd/even, SP+1.5/team-total as applicable. | Schema module + tests; blocked-state semantics; only markets with evidence marked paper-implemented. |
| **P7** | Multi-Market Paper Prototype | Product | Extend paper recommendations from moneyline into run line, totals, odd/even, first five, and SP+1.5 where data contracts exist. | Separate market artifacts; no shared unvalidated edge threshold; `paper_only=true` on all rows. |
| **P8** | Pregame / Live Odds Replacement | Data | Replace POST_GAME_PROXY odds with approved pregame/live snapshots via TSL read-only bridge or approved odds source. | Timestamped odds lineage, freshness, CLV, missing-rate, and no-lookahead audits pass. |
| **P9** | Daily Paper Ops + Drift Monitor | Ops | Produce daily MLB paper advisory and postgame settlement with Brier/ECE/ROI/CLV/no-bet/missing-data drift. | Daily report explains both recommended and skipped games; no production write. |
| **P10** | Production Proposal Gate | Governance | Consider production only after multi-season evidence, live/licensed odds path, rollback/no-bet fail-safe, and human approval. | `production_ready` remains false until explicit approval; PR #2 merge remains separate YES-gated governance task. |

### 0A.4 Highest ROI Optimization Direction

**Most worth optimizing next: P0 -> P1 -> P2/P3.**

The system has crossed from proxy-only validation into true-outcome strategy evaluation. The next highest-value question is narrow and testable:

> Can a true-outcome optimizer beat `fixed_edge_5pct` out of sample without using EV-proxy fitness?

If yes, proceed with P4/P5 hardening before market expansion. If no, freeze MARL as research and promote `fixed_edge_5pct` as the deterministic paper baseline while P6 TSL taxonomy begins.

### 0A.5 Stop Rules For This Update

- No new repo, worktree, or `Betting-pool*` directory.
- No PR #2 merge without explicit `YES: merge PR #2`.
- No live odds API call and no TSL crawler / odds ingestion modification during P0-P3.
- No production proposal write.
- All artifacts remain `paper_only=true`.
- No EV-proxy ROI as optimizer fitness.
- No fake optimizer result: if `.venv` is unavailable, artifact is missing, or architecture cannot support true reward, classify the blocker.

---

## 0. CTO Daily Execution Update — 2026-05-18

**Update marker:** `CTO_BETTING_ROADMAP_V8_1_PR2_GATE_AND_MLB_EXECUTION_20260518_READY`

This update supersedes the P0-P10 ordering below where the two conflict. The user objective is now explicit:

1. **Axis A — MLB game prediction -> Taiwan Sports Lottery betting recommendation.**
   The product must support TSL-style markets, starting with auditable moneyline paper recommendations and expanding to run line, totals, first five, odd/even, and team totals only after market contracts and validation exist.
2. **Axis B — Strategy simulation / optimization.**
   Betting policy must be optimized through replay, CLV/EV evidence, Kelly caps, drawdown controls, and abstention rules before any recommendation is trusted.

### 0.1 Current System Truth

| Area | 2026-05-18 status | CTO call |
|---|---|---|
| Main sync PR | PR #2 is `OPEN`, `MERGEABLE`, `CLEAN`; `replay-default-validation` passed. | **Do not merge without explicit `YES: merge PR #2`.** |
| `origin/main` | Still based at `e765b3b` until PR #2 is merged. | Consolidation PR remains deferred. |
| Current branch | `codex/main-sync-20260516`. | Governance branch, not a feature branch. Keep edits scoped to docs unless instructed. |
| Worktree | Large pre-existing dirty/untracked state. | Protect user work; no reset, no clean, no blind checkout. |
| P38A / P39 state | 2024 OOF baseline exists; Statcast batting rolling track showed no robust uplift. | Freeze batting rolling feature repetition. |
| Odds input | `.env` has no `THE_ODDS_API_KEY`; `data/research_odds/local_only/` is absent. | P3 real odds join remains blocked. |
| TSL market schema | Concept exists in docs; no `wbc_backend/markets/tsl_market_schema.py` implementation found. | Market taxonomy must move earlier. |
| Recommendation row | `wbc_backend/recommendation/recommendation_row.py` supports paper-only moneyline/run-line/total/F5/odd-even row shape. | Good spine, but incomplete market contract and blocked real odds. |
| Strategy simulator | `wbc_backend/simulation/strategy_simulator.py` exists and tracks model/market probability sources. | Usable, but odds-aware multi-market replay is still blocked by data. |
| Decision quality | 2025 single-snapshot benchmark reports 1,493 rows but status `UNAVAILABLE_SINGLE_SNAPSHOT`. | Useful benchmark, not CLV or production evidence. |
| Optimization report | Strict eval games 1,734; Platt improves Brier/ECE, but ROI sweeps are negative. | Optimize abstention and probability quality before scaling bets. |

### 0.2 Roadmap Alignment Gap

The previous v8 ordering said "repo consolidation first, then odds." That was correct before P40D, but it is now incomplete:

- Main sync is already converted to protected-branch PR workflow.
- PR #2 CI is no longer pending; it is passed.
- The active blocker is **user merge authorization**, not engineering uncertainty.
- Consolidation PR must wait until PR #2 is merged so its diff is clean.
- Product work should not wait for another broad planning pass; it needs two focused spines: TSL market contract and odds-aware simulation readiness.

### 0.3 Reordered P0-P10 From This Point

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | PR #2 Merge Gate | Governance | Merge `codex/main-sync-20260516` only after explicit `YES: merge PR #2`. | PR #2 state `MERGED`; `origin/main` updated; no bypass / force push. |
| **P1** | Consolidation PR Readiness | Governance | Rebase/compare `codex/consolidate-p13-clean-20260516` after PR #2 merge. | PR diff contains only consolidation work, not 40+ main-sync commits. |
| **P2** | TSL Market Taxonomy + Row Contract | Product | Implement TSL market schema for moneyline, run line, totals, first five, odd/even, team totals. | Schema module + tests; only moneyline marked implemented until evidence exists. |
| **P3** | Odds Input Unblock | Data | Obtain `THE_ODDS_API_KEY` or approved local-only odds CSV; no secret/raw data committed. | `ODDS_INPUT_READY` or explicit `ODDS_INPUT_NOT_READY`; provenance rules recorded. |
| **P4** | Odds Join Certification | Data + prediction | Join approved odds to P38A/P13 predictions without lookahead. | Coverage, duplicate, unmatched, and timestamp-leakage report pass. |
| **P5** | Moneyline Paper Recommendation v2 | Product | Produce auditable TSL moneyline recommendations with `p_model`, `p_market`, edge, Kelly cap, abstention reason. | Paper ledger rows; stake remains 0 unless gate passes; no production claim. |
| **P6** | Strategy Simulation Optimization v2 | Strategy | Optimize threshold/Kelly/stake/drawdown policy on joined data. | Bootstrap CI, max drawdown, ROI, CLV, turnover, and abstention quality reported. |
| **P7** | Multi-Market Paper Prototypes | Product | Add run line, totals, first five, odd/even, team total paper prototypes. | Separate market-specific model/simulation gates and blocked-state semantics. |
| **P8** | Live Read-Only TSL Snapshot Bridge | Data | Capture read-only TSL snapshots for mapping and freshness checks only. | Snapshot artifacts with no production write and no betting execution. |
| **P9** | Daily Ops / Drift Monitor | Ops | Track Brier, ECE, CLV, ROI, no-bet rate, missing-data rate, stale odds. | Daily report can explain both recommended and skipped games. |
| **P10** | Production Proposal Gate | Governance | Consider production only after multi-season evidence, licensed/live data path, human approval. | `production_ready` review, rollback/no-bet fail-safe, monitoring, explicit CTO/user approval. |

### 0.4 Highest ROI Optimization Direction

**Most worth optimizing next:** P0 -> P1 -> P2/P3 in that order.

- P0/P1 removes PR diff pollution and lets review happen cleanly.
- P2 can proceed without odds and directly serves the user's TSL market objective.
- P3 is the highest data blocker because CLV/EV, Kelly sizing, replay realism, and strategy optimization all depend on approved odds.
- Model feature research should stay behind these gates unless odds remains blocked and a time-boxed fallback is approved.

### 0.5 Execution Stop Rules For This Update

- No new repo or worktree.
- No direct push to protected `main`.
- No PR #2 merge without `YES: merge PR #2`.
- No `.env`, API key, raw odds, local-only CSV, DB, runtime, outputs, or production ledger commit.
- No live betting, no production write, no edge claim.
- No repeating the frozen Statcast batting rolling ablation track unless new evidence changes the premise.

---

## 1. CTO Decision

P38A-P39J materially advanced the system:

- P38A produced a deterministic 2024 OOF baseline: 2,187 / 2,429 rows, Brier about 0.2487, BSS about +0.0020.
- P39A-G successfully built pybaseball / Statcast rolling batting enrichment with 100% P38A enrichment coverage.
- P39H/P39I showed no robust model uplift from Statcast batting rolling features.
- P39J pushed the accumulated p13 work to `origin/p13-clean`; `origin/main` was not touched.

The CTO decision is:

> **Freeze the Statcast batting rolling feature track. The next product blocker is P3 odds / CLV, but the next engineering execution must first protect the single-repo requirement by consolidating `p13-clean` into `Betting-pool`.**

This is the tension in the roadmap: P3 odds is the highest ROI product unblock, while repo consolidation is the highest priority governance unblock. Both should be addressed in the next task, but no runtime P3 fetch/import should proceed until the consolidation workspace is safe.

---

## 2. Roadmap Alignment Assessment

| Previous source | Status after P39J | CTO adjustment |
|---|---|---|
| v7 roadmap, 2026-05-15 | Correct on single-repo requirement and two product axes. | Update implementation state: P38A is now done, P39 batting feature track is frozen, p13 remote has 1b50704. |
| P38A report | Valid baseline. | Baseline remains operative until odds / pitcher feature pilot proves otherwise. |
| P39G report | Valid enrichment engineering success. | Engineering success did not translate into model quality improvement. |
| P39H/P39I | Valid negative result. | Stop repeating batting rolling feature ablations. |
| P39J odds assessment | Correct: P3 odds is highest ROI product blocker. | It requires operator input: `KEY_READY` or `DATA_READY`. |
| P39J push confirmation | Remote HEAD now verifies `origin/p13-clean = 1b50704`. | Treat p13 as backed up, but still not canonical. |

---

## 3. Current System Status

### 3.1 Repo state

| Path | Status | CTO classification |
|---|---|---|
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | `main...origin/main [ahead 38, behind 1]`, large dirty/untracked state | Canonical target, but unsafe for blind merge. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13` | `p13-clean`, `origin/p13-clean = 1b50704`, local/remote in sync | Temporary source only; merge back before retirement. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-preserve-2026-05-11` | Snapshot / no-git preservation folder | Keep until retirement report. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-publication` | Publication worktree | Keep until diffed. |

### 3.2 Product axis A — MLB prediction -> betting recommendation

| Capability | Current state | Next action |
|---|---|---|
| 2024 OOF baseline | Done, P38A ready | Keep baseline operative. |
| Batting Statcast enrichment | Done, no robust improvement | Freeze track. |
| Odds / market benchmark | Blocked | Need The Odds API key or local-only licensed CSV. |
| CLV / EV / Kelly recommendation | Blocked by odds | Run only after P3 input gate. |
| TSL market breadth | Moneyline-first | Add taxonomy after moneyline CLV path is validated. |

### 3.3 Product axis B — strategy simulation optimization

| Capability | Current state | Next action |
|---|---|---|
| Baseline simulation | Exists | Verify after consolidation. |
| Multi-season odds-aware replay | Blocked | Needs odds join. |
| Strategy optimization v2 | Blocked | Needs CLV / EV / multi-season joined input. |
| Pitcher feature pilot | Deferred | Only run if odds remains unavailable and CTO explicitly chooses feature research. |

---

## 4. Key Blockers

1. **Single-repo blocker:** latest useful implementation is in p13, not yet consolidated into `Betting-pool`.
2. **Dirty worktree blocker:** `Betting-pool` cannot accept a blind merge due to extensive dirty/untracked state.
3. **P3 odds blocker:** no `THE_ODDS_API_KEY` and no local-only licensed odds CSV.
4. **CLV blocker:** without odds, no CLV / EV / market benchmark can be computed.
5. **Feature ROI blocker:** batting rolling features failed P39H/P39I; repeating that track is low value.
6. **Production blocker:** no live odds source, no licensed production approval, no human approval, no edge claim.

---

## 5. Reordered P0-P10

| Priority | Phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | Single Repo Consolidation Dry Run | Governance | Bring `origin/p13-clean = 1b50704` into `Betting-pool` without creating a repo and without overwriting dirty user work. | In-repo branch created; p13 diff classified; forbidden files excluded; roadmap/docs/code/tests represented in canonical target. |
| **P1** | Dirty Worktree Safety Inventory | Governance | Produce keep / ignore / review buckets for current `Betting-pool` dirty state. | No destructive cleanup; no user data loss; merge blockers explicit. |
| **P2** | P3 Odds Input Gate | Data | Detect `KEY_READY` or `DATA_READY`; do not fetch/import if absent. | `ODDS_INPUT_READY` or `ODDS_INPUT_NOT_READY`; no secret or raw data exposure. |
| **P3** | Odds Schema Validation + Join Smoke | Data + prediction | Validate approved/local-only odds schema and join to P38A OOF. | >=100 rows if data exists; unmatched/duplicate/leakage report; raw data not committed. |
| **P4** | CLV / EV Benchmark | Recommendation | Compute no-vig implied probability, model edge buckets, CLV/EV paper metrics. | Paper-only report; no production edge claim; recommendation candidates blocked/eligible by reason. |
| **P5** | Moneyline Recommendation Gate v2 | Product | Convert P38A + odds + CLV into auditable TSL-style moneyline recommendation rows. | Rows include market, selection, odds, p_model, p_market, edge, stake, risk reason, `paper_only=true`. |
| **P6** | Strategy Optimization v2 | Strategy | Re-run policy simulation on odds-aware joined input. | Kelly cap, stake cap, drawdown, Sharpe, bootstrap CI, exposure, turnover reported. |
| **P7** | TSL Market Taxonomy Pack | Product | Define HDC, OU, F5, odd/even, team-total schema and blocked-state semantics. | Market contracts + fixture tests committed; no live market claim. |
| **P8** | Non-Moneyline Paper Prototypes | Product | Build first run line / totals / F5 paper-only models. | No-lookahead validation and separate market gates. |
| **P9** | Pitcher Feature Pilot | Research fallback | If odds remains blocked and CTO approves, test starter/bullpen features. | Walk-forward ablation; robust improvement or freeze. |
| **P10** | Production Proposal Gate | Governance | Only after multi-season paper evidence and licensed/live data path. | Human approval, rollback/no-bet fail-safe, monitoring, `production_ready` review. |

Most worth optimizing next: **P0/P1/P2 in one controlled task.** That gives us repo safety and immediately tells us whether P3 odds can begin.

---

## 6. Stop Rules

- Do not create another `Betting-pool*` repo.
- Do not delete `Betting-pool-p13`, `Betting-pool-preserve-2026-05-11`, or `Betting-pool-publication`.
- Do not run `git reset --hard`, `git clean`, or destructive checkout.
- Do not merge blindly into the dirty `Betting-pool/main`.
- Do not commit `.env`, API keys, raw odds, local-only CSV, pybaseball raw dumps, `outputs/`, `runtime/`, DB, `.db-wal`, or `.db-shm`.
- Do not repeat P39 batting rolling feature ablation.
- Do not claim edge, production readiness, live betting readiness, or `JOIN_CERT_RESEARCH_ODDS_READY`.

---

## 7. Latest Task Prompt

```text
請作為 Senior Betting CTO / P40A Single-Repo Consolidation + P3 Odds Input Gate Agent，
在既有 repo 內執行下一輪任務。

最高原則：
- 嚴禁新增 repo / worktree / Betting-pool* 目錄
- canonical target 只能是 /Users/kelvin/Kelvin-WorkSpace/Betting-pool
- /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13 只能作為 temporary source
- 不做 production write
- 不做 live betting
- 不 commit .env / API key / raw odds / local_only CSV / outputs / runtime / DB
- 不宣稱 edge
- paper-only / research-only

背景狀態：
- p13-clean 已 push：origin/p13-clean = 1b50704
- origin/main = e765b3b，未動
- P38A baseline 已完成：2187/2429 OOF rows，Brier 約 0.2487
- P39 batting Statcast rolling track 已凍結：P39I_NO_ROBUST_IMPROVEMENT
- 目前最高產品 ROI blocker 是 P3 odds，但 repo governance 先於 runtime odds fetch/import

TRACK 0 — Preflight：
cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool
git status --short --branch
git log --oneline -8
git remote -v

cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
git status --short --branch
git fetch origin
git rev-parse origin/p13-clean
git rev-parse origin/main
git log --oneline -12

TRACK 1 — Single repo safety inventory：
- 在 Betting-pool 內產出 dirty/untracked inventory
- 將檔案分為 keep / ignore / review / forbidden 四類
- 不刪檔、不 clean、不 reset
- 產出：
  00-BettingPlan/20260516/single_repo_dirty_inventory_20260516.md

TRACK 2 — p13 merge-back manifest：
- 以 origin/main..origin/p13-clean 或 main..p13-clean 盤點 p13 可併回檔案
- 明確列出：
  - code/tests/scripts/docs 可併回
  - raw/local_only/outputs/runtime/DB 禁止併回
  - fixture exception：只允許 synthetic fixture，需標示 SAFE_FIXTURE_EXCEPTION
- 產出：
  00-BettingPlan/20260516/p13_to_betting_pool_merge_manifest_20260516.md

TRACK 3 — consolidation branch only：
- 只在既有 Betting-pool repo 內建立 branch：
  codex/consolidate-p13-clean-20260516
- 不新增 repo、不新增 worktree
- 先不 merge runtime code，除非 dirty inventory 顯示安全
- 若不安全，final classification = SINGLE_REPO_CONSOLIDATION_BLOCKED_DIRTY_WORKTREE

TRACK 4 — P3 odds input gate：
- 在 Betting-pool-p13 或 Betting-pool 讀取 input 狀態，但不揭露 secrets
- 若 .env 有 THE_ODDS_API_KEY，輸出 KEY_READY_REDACTED
- 若 data/research_odds/local_only/ 有 CSV，輸出 DATA_READY_LOCAL_ONLY
- 若兩者都沒有，輸出 ODDS_INPUT_NOT_READY
- 不 fetch API、不 transform CSV、不 join odds，除非 operator 明確提供 KEY_READY 或 DATA_READY

TRACK 5 — roadmap / final report：
- 更新 roadmap 對齊狀態
- 最終報告必須包含：
  1. repo consolidation readiness
  2. P3 odds input readiness
  3. P38A/P39J current truth
  4. next execution decision
  5. forbidden-file scan result

Final classification 只能是：
- SINGLE_REPO_CONSOLIDATION_DRY_RUN_READY
- SINGLE_REPO_CONSOLIDATION_BLOCKED_DIRTY_WORKTREE
- ODDS_INPUT_READY_WAITING_FOR_JOIN
- ODDS_INPUT_NOT_READY
- BLOCKED_RAW_OR_SECRET_VISIBLE
- DOCS_ONLY_ROADMAP_UPDATED
```

---

## 8. CTO 10-Line Summary

```text
1. P38A baseline is ready, but weak; it remains operative.
2. P39 batting Statcast rolling enrichment succeeded technically but failed model uplift.
3. P39 batting rolling feature track is frozen.
4. p13-clean is backed up at origin/p13-clean = 1b50704.
5. Betting-pool remains the only canonical target; do not create repos.
6. Betting-pool main is too dirty for blind merge.
7. P3 odds is the highest ROI product blocker.
8. Odds work requires KEY_READY or DATA_READY; no forced public-data shortcut.
9. Next task should combine repo safety inventory, p13 merge-back manifest, and P3 input gate.
10. production_ready remains false; no live betting, no edge claim.
```

---

`CTO_BETTING_ROADMAP_V8_P39J_ODDS_CONSOLIDATION_20260516_READY`
