# Betting-pool Roadmap v5 — CEO Canonical Edition

**Date:** 2026-05-13  
**Version:** v5  
**Owner:** CEO Agent  
**Acceptance Marker:** CEO_BETTING_ROADMAP_V5_20260513_READY  
**Supersedes:** `betting_roadmap_20260513_v4_cto_RESCUED.md`

---

## Chapter 1 — CEO Reconciliation Statement

This v5 supersedes betting_roadmap_20260513_v4_cto_RESCUED.md, which itself
was rescued from a stale untracked worktree. It also reconciles an internal
inconsistency in the CTO 2026-05-13 outputs: the engineering handoff doc
(20260513v2.md) named P37.6 as P0, while the CTO roadmap v4 named P38A as P0.
The CEO ruling: neither was correct in isolation.
- P37.6 was a governance loop and is downgraded to a sub-task of the
  repo-governance P0, not a full phase.
- P38A is a valid track but is dependency-ordered behind repo governance and
  the free-source feasibility spike.
- The true P0 is repo governance, because the v4 roadmap itself was lost
  to a stale worktree, proving the governance debt is now blocking
  strategic communication.

---

## Chapter 2 — Active Risks (Must Preserve Across All Versions)

These risks must be acknowledged in every roadmap revision and agent handoff:

| Risk ID | Risk Description                        | Severity | Mitigation Path              |
|---------|-----------------------------------------|----------|------------------------------|
| R1      | 2024 licensed odds unavailable          | HIGH     | P37.5 approval + P1 feasibility spike |
| R2      | 2024 OOF prediction source missing      | HIGH     | P38A Retrosheet rebuild      |
| R3      | Sample wall (insufficient game count)   | MEDIUM   | P38A + P5 multi-season       |
| R4      | Moneyline-only limitation               | MEDIUM   | P8 run line/totals (later)   |
| R5      | Live TSL source not available           | HIGH     | No current mitigation        |
| R6      | Multi-worktree drift                    | HIGH     | P0 repo governance closure   |
| R7      | No verified edge claim                  | HIGH     | Governance rule: no claims   |

---

## Chapter 3 — Canonical Priority Ordering

### P0 — Repo Governance Closure + Roadmap Canonicalization

**Status:** IN PROGRESS (this roadmap is the output)  
**Owner:** CEO/CTO Agent  
**Evidence:** `00-BettingPlan/20260513/repo_governance_closure_plan_20260513.md`

**Why P0:**
The v4 roadmap was produced in a stale untracked worktree and was never
committed to the canonical repo. This governance failure blocked all strategic
communication for at least one full agent cycle. Until the governance debt
is resolved, no subsequent phases can be reliably handed off.

**Deliverables:**
- [x] `repo_governance_closure_plan_20260513.md` — stale repo policy, rescue evidence, merge rules
- [x] `betting_roadmap_20260513_v4_cto_RESCUED.md` — rescue artifact, diff clean
- [x] `betting_roadmap_20260513_v5_ceo.md` — this document
- [x] Canonical repo confirmed: `Betting-pool-p13 / p13-clean`

**P0 Sub-Task: P37.6 Operator Action Packet**
- Previously named P0 in engineering handoff (incorrect per CEO ruling)
- Downgraded to sub-task of P0 governance closure
- No standalone phase
- Deliverable: Operator runbook section appended to governance closure plan

---

### P1 — Free-Source Odds Feasibility Spike

**Status:** PLANNING COMPLETE  
**Owner:** CTO Agent  
**Evidence:** `00-BettingPlan/20260513/free_source_odds_feasibility_spike_20260513.md`

**Objective:**  
Unblock the P38/P39 replay pipeline without requiring P37.5 licensed odds
approval. Identify research-grade, non-production, non-wagering odds proxy
paths.

**Key Ruling:**
- Community datasets: ACCEPTABLE_FOR_RESEARCH (with join-cert)
- Manual-import CSV: ACCEPTABLE_FOR_RESEARCH (safest path)
- Synthetic fixtures: ACCEPTABLE_FOR_RESEARCH (smoke tests only)
- Sportsbook snapshot archives: REJECTED_FOR_LICENSE_RISK

**Deliverables:**
- [x] Feasibility assessment document
- [ ] 1-2 candidate community datasets identified and license-verified
- [ ] Join certification test run

---

### P2 — P38A Retrosheet Feature Adapter + OOF Rebuild

**Status:** PLANNING COMPLETE  
**Owner:** CTO Agent  
**Evidence:** `00-BettingPlan/20260513/p38a_retrosheet_oof_rebuild_plan_20260513.md`  
**Dependency:** P1 must have at least one ACCEPTABLE_FOR_RESEARCH odds source

**Objective:**  
Rebuild the 2024 OOF prediction pipeline using Retrosheet public game logs,
with a formally audited pregame-safe feature subset.

**Artifact Contract (Summary):**
- Input: Retrosheet 2024 game logs + schedule + team mapping
- Output: prediction JSONL with `is_research: true`, `leakage_audit_passed: false`
- Required: 4 smoke tests (fixture, date-range, leakage sentinel, determinism)

**Non-Goals (confirmed):**
- No production bet
- No live TSL
- No edge claim
- No odds approval bypass

---

### P3 — Licensed Odds Approval / Manual Import Artifact

**Status:** BLOCKED (pending P37.5 approval)  
**Owner:** CTO Agent  
**Evidence:** `00-BettingPlan/20260513/p37_5_manual_odds_approval_package_report.md`

**Objective:**  
Obtain or construct a formally approved 2024 odds artifact that satisfies the
P37.5 approval gate. This is the production-grade odds path.

**Approval Gate Conditions:**
- Licensed source identified and contracted, OR
- Manual import CSV provided and validated by user

---

### P4 — 2024 Joined Input Certification

**Status:** NOT STARTED  
**Dependency:** P2 (OOF artifact) + P3 (approved odds) OR P1 research proxy

**Objective:**  
Join the 2024 OOF prediction artifact against the 2024 odds artifact on
`game_date + home_team_id + away_team_id`. Certify join rate ≥ 90%.

**Deliverables:**
- `reports/joined_input_certification_2024.md`
- Join rate metric
- Unjoined game analysis

---

### P5 — Multi-Season True-Date Replay

**Status:** NOT STARTED  
**Dependency:** P4 (joined input certified)

**Objective:**  
Run date-ordered, leakage-free replay across 2022-2024 MLB seasons using
certified joined input artifacts. Establish baseline hit-rate and EV metrics
for research purposes.

**Constraints:**
- No edge claims from replay results
- Replay output flagged `is_research: true`
- No production wagering decisions derived from replay

---

### P6 — Strategy Optimization v2

**Status:** NOT STARTED  
**Dependency:** P5 (multi-season replay baseline)

**Objective:**  
Optimize the Kelly criterion sizing and market selection strategy using
replay-validated distribution data. Focus on variance reduction, not
edge maximization.

---

### P7 — TSL Market Taxonomy + Schema Pack

**Status:** NOT STARTED  
**Dependency:** P6 (strategy optimization)

**Objective:**  
Define the canonical TSL market taxonomy (moneyline, run line, totals,
1H/5-inning variants) with formal JSON schema for artifact compatibility.

---

### P8 — Run Line + Totals PAPER Prototype

**Status:** NOT STARTED  
**Dependency:** P7 (market taxonomy)

**Objective:**  
Build a paper (non-wagering) prototype for run line and totals prediction.
No production integration. Validate model architecture against moneyline baseline.

---

### P9 — Daily Ops + Drift Monitoring

**Status:** NOT STARTED  
**Dependency:** P5 (replay baseline established)

**Objective:**  
Implement daily operations pipeline: model drift monitoring, data freshness
alerts, prediction confidence tracking. Supports operational readiness for P10.

---

### P10 — Production Proposal Gate

**Status:** NOT STARTED  
**Dependency:** P9 (daily ops in place)

**Decision Gate:**  
Before any production use, a formal production proposal must pass:
- [ ] Licensed odds source in place (P3 complete)
- [ ] Multi-season replay certified (P5 complete)
- [ ] No active governance debt
- [ ] Risk register reviewed
- [ ] Explicit user authorization

**Until P10 gate passes:** No production bet. No live wagering. No edge claims.

---

## Chapter 4 — Roadmap Succession Chain

| Version  | File                                              | Status                    |
|----------|---------------------------------------------------|---------------------------|
| v1-v3    | (legacy, not tracked)                             | SUPERSEDED                |
| v4 (CTO) | `betting_roadmap_20260513_v4_cto_RESCUED.md`      | RESCUED / SUPERSEDED      |
| v5 (CEO) | `betting_roadmap_20260513_v5_ceo.md`              | CANONICAL (this document) |

Future versions must:
- Reference this document as parent
- Increment version number
- Document what changed from v5

---

## Chapter 5 — Agent Governance Checklist

Any agent working on this repo must confirm before any write:

- [ ] CWD is `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`
- [ ] `git branch --show-current` → `p13-clean`
- [ ] No writes to `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- [ ] All new artifacts in `00-BettingPlan/YYYYMMDD/` namespace
- [ ] No production write or live betting interface touched
- [ ] No edge claim made
- [ ] Reference roadmap version is this document (v5)

---

## Chapter 6 — Glossary

| Term         | Definition                                                     |
|--------------|----------------------------------------------------------------|
| OOF          | Out-of-favor prediction: model probability differs from closing market |
| Pregame-safe | Feature knowable before first pitch; no postgame data         |
| Leakage      | Any use of future/postgame data in a pregame prediction       |
| P0           | Highest priority phase; must complete before all others       |
| RESCUED      | File copied from stale repo with banner, body diff-verified   |
| CANONICAL    | The authoritative version of a document in the tracked repo   |
| Research     | Non-production, non-wagering, flagged `is_research: true`     |

---

**CEO_BETTING_ROADMAP_V5_20260513_READY**
