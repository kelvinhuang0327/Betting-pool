# Betting-pool Canonical Roadmap

**CTO review date:** 2026-05-20 Asia/Taipei  
**Canonical repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Observed branch:** `codex/main-sync-20260516`  
**Mode:** `paper_only=true`, `production_ready=false`, `NO_REAL_BET=true`  
**Roadmap status:** integrated from historical roadmap files because `00-Plan/roadmap/roadmap.md` was [Missing].  
**Active marker:** `CTO_CANONICAL_ROADMAP_P26H_EXPECTED_PAIRS_PREDICTION_BROKEN_20260521`

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
