# CTO Roadmap Alignment and System Optimization Analysis

## 1. CTO Review Date

2026-05-20 Asia/Taipei

## 2. Input Sources

Read / referenced:

- [Confirmed] `00-Plan/roadmap/roadmap.md`
- [Confirmed] `00-BettingPlan/20260520/p23_gate_and_reproducibility_reconciliation_20260520.md`
- [Confirmed] `00-BettingPlan/20260520/p24_clv_robustness_diagnostic_20260520.md`
- [Confirmed] `00-BettingPlan/20260520/p25_clv_failure_root_cause_audit_20260520.md`
- [Confirmed] `00-BettingPlan/20260520/p26_clv_line_aware_matching_repair_20260520.md`
- [Confirmed] `00-BettingPlan/20260520/p27_per_market_clean_clv_isolation_20260520.md`
- [Confirmed] `00-BettingPlan/20260520/p28_mlb_model_quality_repair_20260520.md`
- [Confirmed] `00-BettingPlan/20260520/p29_orchestrator_noise_removal_and_external_data_contract_20260520.md`
- [Confirmed] `data/paper_recommendations/p29_orchestrator_ablation_results_20260520.json`
- [Confirmed] `data/paper_recommendations/p29_orchestrator_noise_attribution_audit_20260520.json`
- [Confirmed] `data/paper_recommendations/p29_external_data_contract_20260520.json`
- [Confirmed] `data/paper_recommendations/p29_feature_readiness_matrix_20260520.json`
- [Confirmed] `data/paper_recommendations/p29_source_snapshot_drift_20260520.json`
- [Confirmed] `report/p29_final_validation_20260520.md`
- [Confirmed] Existing `00-Plan/roadmap/active_task.md` was read; it still describes older P23 work.

Not performed:

- [Confirmed] No pytest rerun in this CTO review. Test status is taken from P29 final validation report.
- [Confirmed] No development implementation, no production write, no data modification, no PR merge.
- [Confirmed] `00-Plan/roadmap/active_task.md` was not updated because the strict allowed-write list only permitted `roadmap.md` and `CTO-Analysis.md`.

## 3. Roadmap Alignment Assessment

| Tag | Finding |
|---|---|
| [Aligned] | P23-P27 correctly moved from raw CLV optimism to line-aware CLV repair and per-market isolation. |
| [Aligned] | P28 correctly shifted from CLV to model quality after clean CLV remained inconclusive. |
| [Aligned] | P29 correctly investigates Orchestrator noise after Full Orchestrator Brier `0.248703` underperformed Simple LogReg `0.245105`. |
| [Aligned] | P29 external data contracts support the product goal of improving MLB pregame predictions before recommendation expansion. |
| [Drift] | The previous canonical roadmap still placed P22/P23 reconciliation at P0, but P23-P29 artifacts now exist locally. |
| [Drift] | `active_task.md` still points to P23 gate reconciliation and is outdated relative to P29. |
| [Missing] | Roadmap lacked a real-Orchestrator validation step for the P29 proxy `w_market=0.50` finding. |
| [Missing] | Roadmap lacked a market baseline timestamp/leakage audit, despite pure market Brier `0.244354`. |
| [Outdated] | P22 positive CLV interpretation is obsolete after P25-P27 showed construction bug / clean CLV inconclusive. |
| [Outdated] | Any direct path from P29 proxy ablation to production weight change is invalid. |
| [Blocked] | Strategy optimizer, champion replacement, and production proposal remain blocked by real-pipeline validation and timestamp safety. |

## 4. Completed Work Assessment

### P23-P27

- [Confirmed] P23 gate/reproducibility reconciliation completed.
- [Confirmed] P24 CLV robustness diagnostic completed and did not establish robust CLV.
- [Confirmed] P25 identified a CLV construction bug caused by non-line-aware outcome matching.
- [Confirmed] P26 repaired CLV with line-aware matching; old positive mean was largely artifact-driven.
- [Confirmed] P27 isolated markets and OE exclusion; clean CLV remained inconclusive across markets.

### P28

- [Confirmed] `P28_MODEL_REPAIR_NO_IMPROVEMENT`.
- [Confirmed] Full Orchestrator Brier `0.2487`; Simple 7-feature LogReg Brier `0.2451`.
- [Confirmed] Target Brier `<0.24` was not reached.

### P29

- [Confirmed] P29 final classifications:
  - `P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND`
  - `P29_EXTERNAL_DATA_CONTRACT_READY`
  - `P29_EXTERNAL_FEATURES_REQUIRED_TO_BREAK_CEILING`
- [Confirmed] P29 proxy ablation tested 8 variants over 2,020 test games / 5 windows.
- [Confirmed] Best proxy variant: `V3_marl_sim_w50_sq2`, Brier `0.244154`.
- [Confirmed] Pure market Brier `0.244354`; Simple LogReg Brier `0.245105`; reported Full Orchestrator Brier `0.248703`.
- [Confirmed] P29 created two scripts:
  - `scripts/p29_orchestrator_noise_audit.py`
  - `scripts/p29_external_data_contract_builder.py`
- [Confirmed] P29 created five external-data design contracts: starting pitcher, bullpen, batting form, lineup/injury proxy, park/weather.
- [Confirmed from report] P29 validation says P26 `23/23 PASS`, P17 `64/64 PASS`, P13-P17 `296/296 PASS`, total `383/383 PASS`, JSON schema `5/5 PASS`, forbidden scan `0 hits`.

Interpretation:

- [Confirmed] P29 is diagnostic/proxy-only, not a production Orchestrator modification.
- [Inferred] The strongest next step is not SP ingestion yet; it is validating whether the real Orchestrator can reproduce the proxy improvement without leakage.

## 5. Unfinished Work Assessment

| Item | Status |
|---|---|
| Real Orchestrator `w_market` validation | [Blocked] P29 result is proxy/math simulation; real pipeline validation not yet done. |
| Market timestamp/leakage audit | [Blocked] Pure market baseline is strong, but pregame safety is not proven in P29. |
| Production-safe ablation hook | [Missing] No confirmed diagnostic hook for sweeping real Orchestrator components without default-path mutation. |
| External data implementation | [Blocked] Contracts are design-only; no SP/bullpen/batting/lineup/weather data fetched or validated. |
| Strategy optimizer re-entry | [Blocked] Should wait until probability quality improves and market baseline safety is proven. |
| TSL recommendation expansion | [Blocked] Model quality and market evidence are not strong enough for release beyond paper diagnostics. |
| Active task SSOT | [Drift] Existing `active_task.md` is stale P23; not updated due write restriction. |

## 6. P0 / P1 / P2 / P3-P10 Reprioritization

| Priority | Phase | Why now |
|---:|---|---|
| **P0** | P30A Real Orchestrator `w_market` Validation | It is the only way to turn P29's proxy finding into reliable engineering evidence. |
| **P1** | Market Baseline Timestamp / Leakage Audit | Market-heavy variants are meaningless if market probability uses closing/postgame information. |
| **P2** | External Data Contract Freeze | Contracts are valuable, but implementation would expand scope before the Orchestrator evidence is stable. |
| **P3** | Orchestrator Simplification Decision Gate | Decide simplify / raise market weight / keep full path only after P0/P1. |
| **P4** | Starting Pitcher Data Prototype | Highest-impact external feature, but waits behind P0/P1 and source approval. |
| **P5** | Model Quality Repair Loop | Continue Brier/logloss/ECE repair with real-pipeline and no-leakage evidence. |
| **P6** | TSL Market Taxonomy + Recommendation Contract | Product maturity work, but recommendation release remains blocked. |
| **P7** | Strategy Simulation Re-entry Gate | Strategy optimization resumes only after probability quality is trustworthy. |
| **P8** | Daily Paper Ops / Drift Monitor | Useful after canonical metrics and source lineage stabilize. |
| **P9** | Repo / PR Governance Gate | PR #2 remains explicit-YES gated; not product P0. |
| **P10** | Production Proposal Gate | Remains blocked until evidence, licensed/live data, fail-safe, monitoring, and approval exist. |

Upgraded to P0:

- [Confirmed] Real Orchestrator validation of `w_market=0.50`.
- [Confirmed] Diagnostic-only ablation hook / no production default mutation.

Upgraded to P1:

- [Confirmed] Market baseline timestamp/leakage audit.

Downgraded:

- [Confirmed] SP/bullpen/batting implementation. Contracts are ready, but implementation waits.
- [Confirmed] Strategy optimizer / champion replacement / promotion.
- [Confirmed] PR #2 merge, unless explicit user approval is given.

Merged:

- [Inferred] P23-P27 CLV phases become one completed CLV-cleanup evidence chain.
- [Inferred] P28-P29 become one model-quality/noise-attribution chain.

Paused / retired:

- [Confirmed] P22 positive CLV interpretation.
- [Confirmed] Non-line-aware CLV.
- [Confirmed] EV-proxy or proxy ablation as production evidence.
- [Confirmed] Live API, crawler modification, production proposal, profitability claim.

## 7. Critical Blockers

### Blocker 1: Proxy-to-Real Orchestrator Gap

- Impact: model architecture, prediction quality, recommendation validity.
- Why blocker: P29 improvement is proxy-only; real Full Orchestrator component behavior may not match.
- Risk if ignored: changing weights or planning downstream strategy from a non-reproducible proxy result.
- Priority: P0.
- Acceptance: real Orchestrator sweep reports Brier/logloss/hit rate/sample size for market weights, with no production default mutation.

### Blocker 2: Market Probability Timestamp / Leakage Risk

- Impact: data quality, model evaluation correctness.
- Why blocker: pure market Brier `0.244354` is strong, but only usable if it is pregame-safe.
- Risk if ignored: leakage can masquerade as model improvement.
- Priority: P1.
- Acceptance: each market probability has timestamp/source lineage; closing/postgame odds are excluded or result is marked `LEAKAGE_RISK`.

### Blocker 3: Orchestrator Coupling Risk

- Impact: architecture safety.
- Why blocker: MARL/Elo/market/ensemble components may be too coupled for clean ablation without side effects.
- Risk if ignored: accidental production default mutation or non-isolated research results.
- Priority: P0.
- Acceptance: diagnostic-only adapter/hook isolates weights and records no production path mutation.

### Blocker 4: Feature Ceiling Without External Data

- Impact: prediction quality.
- Why blocker: P29 suggests current repo/CSV feature ceiling is around Brier `0.244-0.245`.
- Risk if ignored: repeated internal feature/calibration experiments may burn effort without breaking ceiling.
- Priority: P2/P4.
- Acceptance: external contracts remain design-only until P0/P1 clear; starting pitcher prototype is next feature candidate after approval.

### Blocker 5: Stale Active Task SSOT

- Impact: agent orchestration and workflow safety.
- Why blocker: `active_task.md` still describes P23 while roadmap now points to P30A.
- Risk if ignored: Planner/Worker may execute stale gate work instead of current P30A focus.
- Priority: P2 governance.
- Acceptance: update is deferred until write authorization includes `active_task.md`, or the next authorized agent updates it.

## 8. Recommended System Optimization Directions

### Direction 1: Real Orchestrator Diagnostic Validation

- Roadmap phase: P0.
- Why important: Converts P29's useful but proxy-only finding into real-pipeline evidence.
- Maturity gain: Separates actual architecture improvement from simulation artifact.
- Expected benefit: Potentially reduce Brier from `0.2487` toward `0.244-0.245` if reproduced.
- Risk: Real pipeline may not reproduce P29 proxy result.
- Acceptance: sweep variants output Brier/logloss/hit rate/sample size and no production default mutation.
- Priority: P0.

### Direction 2: Market Timestamp / Leakage Safety

- Roadmap phase: P1.
- Why important: Market-heavy models require proof that market probability is pregame-safe.
- Maturity gain: Protects evaluation correctness and prevents false improvement.
- Expected benefit: Clear permission to use market baseline as comparator or fallback.
- Risk: If timestamps are missing, results must be classified as leakage-risk and not adopted.
- Acceptance: source trace and timestamp audit for every market probability field.
- Priority: P1.

### Direction 3: External Feature Contract Governance

- Roadmap phase: P2/P4.
- Why important: External features are likely required to break the Brier ceiling, but they introduce data cost and leakage risk.
- Maturity gain: Keeps sourcing, fields, freshness SLA, and anti-leakage rules explicit before implementation.
- Expected benefit: Clean path to starting pitcher / bullpen / batting upgrades after architecture validation.
- Risk: Scope explosion if SP integration starts before P0/P1.
- Acceptance: contracts remain `contract_only=true` until source approval and backtest plan exist.
- Priority: P2.

### Direction 4: Product Recommendation Contract After Model Quality

- Roadmap phase: P6.
- Why important: The core product is MLB -> TSL paper recommendation, but recommendations need reliable probability and odds lineage.
- Maturity gain: Ties markets to model probability, odds, edge, source time, risk gate, and `paper_only=true`.
- Expected benefit: Prevents unsupported market expansion and keeps product output auditable.
- Risk: Premature market expansion without model improvement.
- Acceptance: each market has supported/diagnostic/blocked status and evidence requirements.
- Priority: P3+.

### Direction 5: Roadmap / Active Task SSOT Repair

- Roadmap phase: P9.
- Why important: stale `active_task.md` can mislead the next agent.
- Maturity gain: Aligns Planner/Worker execution with current CTO priorities.
- Expected benefit: Fewer repeated or stale tasks.
- Risk: Current write constraints did not allow active task update.
- Acceptance: update `active_task.md` only after explicit authorization includes that file.
- Priority: P2 governance.

## 9. Roadmap Changes Applied

- [Confirmed] Updated `00-Plan/roadmap/roadmap.md`.
- [Confirmed] Replaced this `00-Plan/roadmap/CTO-Analysis.md` with the P29/P30A CTO assessment.
- [Confirmed] Marked P23-P27 CLV cleanup as completed/historical.
- [Confirmed] Marked P28 as model repair no improvement.
- [Confirmed] Marked P29 as completed diagnostic/proxy and external contract design.
- [Confirmed] Reprioritized P0 to P30A real Orchestrator `w_market` validation.
- [Confirmed] Reprioritized P1 to market timestamp/leakage audit.
- [Confirmed] Marked external data implementation as deferred behind P0/P1.
- [Confirmed] Did not update `active_task.md` because it is outside the strict allowed write list.

## 10. Risks / Unknowns

- [Unknown] Whether real Orchestrator pipeline reproduces P29 proxy improvement.
- [Unknown] Whether market probabilities are strictly pregame-safe.
- [Unknown] Whether Orchestrator components can be cleanly ablated without a diagnostic adapter.
- [Unknown] Whether `w_market=0.50` remains best in a wider real-pipeline sweep.
- [Unknown] Whether SP/bullpen/batting contract estimates are realistic; they are upper-bound design estimates.
- [Confirmed] P29 tests were not rerun in this CTO analysis; test status is report-based.
- [Confirmed] P29 artifacts/scripts/reports are present but untracked in the current git status.
- [Confirmed] `active_task.md` is stale relative to P29 but was not updated due write restrictions.
- [Confirmed] PR #2 remains open and must not be merged without explicit authorization.

## 11. CTO Final Recommendation

Today should focus on exactly one engineering direction: **P30A real Orchestrator `w_market` ablation validation plus market timestamp/leakage audit**. Do not start SP data integration yet, and do not launch optimizer promotion, champion replacement, production proposal, live API, or crawler changes.

The decision rule is simple:

- If real Orchestrator reproduces a Brier improvement of at least `0.002` with no leakage risk, keep it as a paper-only architecture candidate.
- If not reproduced, retire the P29 proxy result as non-actionable.
- If timestamp lineage is unsafe, block the market-heavy conclusion regardless of Brier.

Final classification: `CTO_ROADMAP_UPDATED_WITH_RISKS`

## 12. 10 行內 CTO 摘要

1. P23-P27 CLV cleanup is now historical; clean CLV remains inconclusive.
2. P28 failed to improve model quality; Full Orchestrator is worse than simple LogReg.
3. P29 found a proxy candidate: `w_market=0.50`, Brier `0.244154`.
4. P29 also shows pure market Brier `0.244354`, requiring timestamp/leakage audit.
5. P29 is diagnostic/proxy-only, not production evidence.
6. P0 is P30A real Orchestrator `w_market` validation.
7. P1 is market baseline timestamp/leakage audit.
8. External data contracts are ready but remain design-only.
9. Promotion, champion replacement, production proposal, live API, and crawler changes remain frozen.
10. Do one thing next: validate P29 in the real pipeline before any SP integration or optimizer work.
