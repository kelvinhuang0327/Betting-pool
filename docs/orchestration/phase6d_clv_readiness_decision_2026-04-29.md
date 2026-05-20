# Phase 6D — CLV Readiness Decision After Domain Mismatch

**Date:** 2026-04-29
**Type:** Decision document — NOT an implementation
**Predecessor:** Phase 6C (`379b596`) — `docs/orchestration/phase6c_match_identity_bridge_report_2026-04-29.md`
**Author:** Betting-pool Orchestrator Research Agent

---

## 1. Executive Summary

Phase 6C confirmed that the CLV join readiness is **0.0%** due to a fundamental data
domain mismatch: TSL odds data covers MLB/KBO/NPB professional league regular-season games
(2026-03-13 onward), while the `prediction_registry` covers WBC 2026 national tournament
pool games only (2026-03-05 to 2026-03-11).

This is **not a code failure**. The Phase 6B/6C adapters (snapshot type classifier,
team alias resolver, match identity bridge) are structurally correct and reusable.
The mismatch is a data-domain design decision that must be resolved at the system level.

**This document evaluates four strategic paths forward and recommends one primary path
and one fallback path.**

**Recommended Primary Path:** Option C — Build CLV Validation Only for Future Events
(aligned, prospective data collection from a single decided domain).

**Recommended Fallback Path:** Option A — Expand Prediction Registry to MLB/KBO/NPB
(if the project confirms regular-season betting is the strategic goal).

**CLV formal validation should NOT proceed yet.**

---

## 2. Evidence Recap

### 2.1 Files Read

| File | Status | Key Finding |
|---|---|---|
| `docs/orchestration/phase6_market_signal_data_pipeline_design_2026-04-29.md` | ✅ Read | Full pipeline design; CLV hypothesis; 14-item data gap table; Phase 6A–6F plan |
| `docs/orchestration/phase6a_clv_data_contract_2026-04-29.md` | ✅ Read | Canonical schema contract; 6 blockers enumerated; snapshot_type rules; leakage guards |
| `docs/orchestration/phase6b_odds_snapshot_adapter_report_2026-04-29.md` | ✅ Read | Phase 6B resolved snapshot_type blocker; 28,941 snapshot records; league=unknown_league for all |
| `docs/orchestration/phase6c_match_identity_bridge_report_2026-04-29.md` | ✅ Read | Phase 6C result: MATCHED_PREDICTION=0, DOMAIN_MISMATCH=348, CLV readiness=0.0% |
| `data/derived/match_identity_bridge_2026-04-29.jsonl` | ✅ Read | 383 bridge records; all DOMAIN_MISMATCH or unresolved |
| `data/derived/team_alias_map_2026-04-29.csv` | ✅ Read | 66 team alias rows; 59 RESOLVED, 6 TEAM_CODE_MISSING, 1 LOW_CONFIDENCE |
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ✅ Sampled | 28,941 rows; covers MLB/KBO/NPB; date range 2026-03-13 to 2026-04-30 |
| `data/wbc_backend/reports/prediction_registry.jsonl` | ✅ Read | 66 rows; 9 unique WBC game_ids (A05, A06, B05, B06, C07, C08, C09, D05, D06); ALL decision=NO_BET; expected_clv=0.0 |
| `data/wbc_backend/reports/postgame_results.jsonl` | ✅ Read | 49 rows; 2 WBC codes (B06, C09) and 47 numeric IDs; WBC∩prediction overlap = 2/9 |

### 2.2 Key Quantitative Facts

| Metric | Value |
|---|---|
| TSL odds snapshot rows | 28,941 |
| TSL canonical matches | 383 |
| TSL date range | 2026-03-13 to 2026-04-30 |
| TSL leagues | MLB (30 teams), KBO (10), NPB (12), WBC (8) |
| prediction_registry rows | 66 |
| prediction_registry game_ids (unique) | 9 |
| prediction_registry date range | 2026-03-05 to ~2026-03-12 |
| prediction_registry decisions | ALL = NO_BET |
| prediction_registry expected_clv | ALL = 0.0 |
| postgame_results rows | 49 |
| WBC code overlap (prediction ∩ postgame) | 2 games (B06, C09) |
| CLV join readiness | **0.0%** |
| Walk-forward sample (Phase 5.5) | 2,188 MLB games (internal, not in repo) |
| CLV_high bucket sample (Phase 5.5) | 38 (need ≥200) |

---

## 3. Domain Mismatch Diagnosis

### 3.1 Root Cause

The domain mismatch has two independent dimensions:

**Dimension 1 — Competition:**
| System | Competition |
|---|---|
| TSL odds data | MLB / KBO / NPB professional regular season |
| prediction_registry | WBC 2026 national tournament |

These are entirely different competitions. No team in an MLB regular-season game
will also appear in the WBC prediction_registry for the same date.

**Dimension 2 — Time:**
| System | Date Range |
|---|---|
| TSL odds data | 2026-03-13 to 2026-04-30 |
| prediction_registry | 2026-03-05 to ~2026-03-12 |

The WBC 2026 pool phase ended on 2026-03-11. TSL began capturing MLB/KBO/NPB odds
from 2026-03-13. The two datasets do not share a single game day.

### 3.2 Impact Assessment

The mismatch blocks the following operations:

- Bet-level CLV computation (requires prediction ↔ odds join on same match)
- ROI per CLV bucket analysis (requires settled bets with matched odds)
- Walk-forward CLV validation (requires prediction time < closing odds time)

The mismatch does NOT affect:

- Phase 6B output reusability (`snapshot_type` classifier is domain-agnostic)
- Phase 6C output reusability (team alias map, bridge schema, UUID5 ID strategy)
- Calibration / Brier / hit-rate analysis (uses prediction_registry + postgame directly)
- Non-CLV model performance metrics

### 3.3 Is This a Blocker?

**Yes, for formal CLV validation. No, for the broader system.**

The Phase 6C domain mismatch is the **expected output of a correctly executed
evidence-driven pipeline**: the bridge script probed available data honestly and
reported 0.0% CLV join readiness rather than producing a spurious join. This is
the correct outcome. The system is working as designed.

---

## 4. Decision Options

### Option A — Expand Prediction Registry to MLB/KBO/NPB

**Goal:** Make model predictions for the same leagues as the TSL odds data.

| Dimension | Assessment |
|---|---|
| Aligns with | Project goal = regular-season betting engine |
| Reuses | Phase 6B snapshot adapter (domain-agnostic), Phase 6C team alias map |
| New requirements | MLB/KBO/NPB prediction pipeline; league feature sets; settlement coverage per league; sample sufficiency rules per league |
| Data gap | No MLB/KBO/NPB per-match prediction history in repo (walk-forward used 2,188 MLB games internally but per-match outputs not persisted) |
| Leakage risk | MEDIUM — need prediction_time_utc < closing_odds_time guard, same as WBC |
| Strategic scope change | HIGH — expands beyond current WBC model scope |

**Evidence:** The walk-forward summary (`data/wbc_backend/walkforward_summary.json`) shows
2,188 MLB games used for training but individual prediction outputs were not persisted to
`prediction_registry`. Rebuilding MLB prediction coverage is non-trivial.

### Option B — Acquire / Reconstruct WBC Odds Snapshots

**Goal:** Keep WBC prediction scope and obtain matching WBC market odds.

| Dimension | Assessment |
|---|---|
| Aligns with | Project goal = WBC-only tournament betting |
| Historical WBC odds | Likely unavailable from TSL as TSL stopped/started by 2026-03-13 |
| Reconstruction risk | Historical backfill introduces unknown snapshot timing quality |
| Leakage risk | HIGH — historical reconstruction may not preserve pre-match snapshot integrity |
| Sample | WBC 2026 had ≤40 games; CLV_high ≥200 threshold not achievable from WBC 2026 alone |
| Strategic value | LOW — WBC 2026 is over; WBC 2029 is 3 years away |

**Evidence:** Phase 6C bridge confirmed TSL has no WBC records. Phase 5.5 already found
CLV_high sample = 38 from WBC, far below the ≥200 required. Even if historical WBC odds
were reconstructed, the sample would not support formal CLV validation.

### Option C — Build CLV Validation Only for Future Events

**Goal:** From today forward, collect odds + predictions + settlement from the same
decided domain, with aligned ingestion discipline.

| Dimension | Assessment |
|---|---|
| Aligns with | Any project goal — the cleanest forward path |
| Leakage control | HIGHEST — no historical reconstruction; all data is prospective |
| Time to evidence | LONGEST — requires ≥200 matched, settled bets to test the CLV hypothesis |
| Reuses | Phase 6B adapter and Phase 6C bridge schema as permanent infrastructure |
| New requirements | Domain decision first (WBC or MLB?), then aligned crawler schedule, prediction registry enhancements, settlement join, daily quality monitor |
| Strategic value | HIGHEST — produces audit-proof CLV evidence without backfill risk |

**Note:** Option C depends on the domain decision (WBC vs MLB/KBO/NPB) being made first.
It does not resolve the decision — it defers implementation until alignment exists.

### Option D — Defer CLV and Validate Non-CLV Signals First

**Goal:** Use existing WBC prediction + postgame data for non-market model validation
(calibration, Brier score, hit rate) before addressing CLV.

| Dimension | Assessment |
|---|---|
| Aligns with | Parallel validation track while waiting for CLV data |
| Available data | 9 WBC predictions (all NO_BET) + 2 postgame overlaps (B06, C09) |
| Sample concern | 2 matched results is statistically insufficient for any metric |
| CLV readiness impact | None — does not advance CLV readiness |
| Strategic value | LOW in isolation; MEDIUM if done alongside Option A or C |

**Evidence:** prediction_registry has 9 game_ids but ALL decisions = NO_BET and
ALL expected_clv = 0.0. Postgame overlap = 2 games. This is not sufficient for
meaningful calibration validation. Option D alone does not unblock CLV.

---

## 5. Decision Matrix

Scores: HIGH = 3, MEDIUM = 2, LOW = 1 (higher = more favorable for that dimension)

| Option | Data Availability | Engineering Cost* | Time to Evidence | Leakage Risk† | CLV Validity | Strategic Value | Recommendation |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **A** — Expand to MLB/KBO/NPB | LOW (2) | LOW (1) | MEDIUM (2) | MEDIUM (2) | HIGH (3) | HIGH (3) | Secondary / Fallback |
| **B** — Acquire WBC Odds | LOW (1) | LOW (1) | LOW (1) | LOW (1) | LOW (1) | LOW (1) | Not Recommended |
| **C** — Future-Only CLV | HIGH (3) | HIGH (3) | LOW (1) | HIGH (3) | HIGH (3) | HIGH (3) | **Primary** |
| **D** — Non-CLV Validation | MEDIUM (2) | HIGH (3) | HIGH (3) | HIGH (3) | LOW (1) | LOW (1) | Parallel / Optional |

*Engineering Cost: HIGH = low cost, LOW = high cost (inverted for readability)
†Leakage Risk: HIGH = low risk, LOW = high risk (inverted for readability)

**Composite scores (sum):** C=16, A=13, D=13, B=6

**Option C** scores highest overall. **Option A** is the preferred fallback if the
project decides to expand to regular-season betting. **Option D** can be executed in
parallel as a baseline check but does not advance CLV readiness.

---

## 6. Recommended Path

### Primary: Option C — Build CLV Validation Only for Future Events

**Rationale:**

1. **Cleanest leakage posture.** All prediction-to-odds timing relationships are
   prospective and auditable. No backfill inference.

2. **Phase 6B/6C adapters are already built.** The snapshot type classifier, team alias
   resolver, and bridge schema are domain-agnostic. They will be reused without
   modification once the domain decision (WBC vs regular-season) is locked.

3. **Forces a domain commitment.** Option C requires deciding which league to bet
   before implementation begins, surfacing the strategic question that Phase 6D
   was designed to answer.

4. **Correct response to 0.0% CLV readiness.** The Phase 6C evidence shows the current
   dataset cannot support CLV validation. Building prospective infrastructure is the
   honest engineering path.

**Preconditions before Phase 6E implementation can start:**

- [ ] Project decision: is the target betting domain MLB/KBO/NPB or WBC?
- [ ] Confirmed data source for odds + settlement for that domain
- [ ] Prediction pipeline that writes `game_id` in canonical form aligned with TSL `match_id`

**Implementation scope for Phase 6E (Option C):**

1. Aligned prediction registry schema — add `canonical_match_id` as FK alongside `game_id`
2. Crawler scheduling policy — ensure odds snapshots are fetched pre-match for decided domain
3. Settlement join logic — link postgame results to prediction_registry via canonical_match_id
4. Sample accumulation monitor — daily check: current matched-and-settled count vs ≥200 threshold
5. Leakage guard re-run — validate prediction_time_utc < CLOSING snapshot_time_utc for every new record

---

### Fallback: Option A — Expand Prediction Registry to MLB/KBO/NPB

**Rationale:**

If the project confirms that **regular-season betting is the strategic goal** (and not
WBC), Option A is the most direct path to CLV validation with the existing TSL odds data.

The Phase 6B/6C adapters already cover MLB/KBO/NPB:
- Team alias map: 30 MLB + 12 NPB + 10 KBO teams resolved
- Bridge schema: domain-agnostic, accepts any league code
- Snapshot adapter: processes any TSL game regardless of league

What is missing for Option A:
- MLB/KBO/NPB per-match prediction outputs (walk-forward generated 2,188 MLB games
  internally but did not persist per-match probabilities to prediction_registry)
- Settlement data for MLB/KBO/NPB regular season games (not in repo)
- Feature availability check for KBO/NPB (current model features are WBC/MLB-focused)

**Option A becomes Phase 6E if the domain decision resolves to regular-season.**

---

## 7. Non-Goals / Do Not Do Next

The following actions must NOT be taken as Phase 6D follow-up:

1. **Do not run formal CLV validation** — CLV join readiness = 0.0% makes this invalid.
2. **Do not reconstruct historical WBC odds** (Option B) — sample is insufficient (max 40 WBC games); backfill quality is unverifiable; WBC 2026 is over.
3. **Do not modify the TSL crawler** — crawler produces correct output; domain mismatch is not a crawler bug.
4. **Do not modify the bridge script** — Phase 6C bridge is structurally correct; any update belongs in Phase 6E.
5. **Do not modify the DB or orchestrator** — no behavioral change is needed at the runtime layer.
6. **Do not begin Option A or C implementation without a domain commitment** — starting a prediction pipeline without knowing the target league creates wasted infrastructure.
7. **Do not treat Option D alone as sufficient** — 2 matched postgame results cannot validate any model metric.

---

## 8. Next Implementation Prompt

The following prompt is ready to be used as the Phase 6E task specification once the
domain decision is made.

---

```text
# TASK: BETTING-POOL ORCHESTRATION PHASE 6E — ALIGNED CLV CAPTURE DESIGN

Follow AI system rules.

GOAL:
Design the aligned CLV capture pipeline for [CHOSEN DOMAIN: MLB / KBO / NPB / WBC].

This task is design-only. Do not modify code, data, DB, crawler, or model.
Do not commit.

CONTEXT:
- Phase 6C confirmed CLV join readiness = 0.0% (domain mismatch).
- Phase 6D recommended Option C (future-only CLV) as primary path.
- Domain decision: [INSERT DECISION: regular-season MLB/KBO/NPB OR future WBC].
- Phase 6B/6C adapters are reusable (domain-agnostic).

REQUIRED INPUTS:
- docs/orchestration/phase6d_clv_readiness_decision_2026-04-29.md
- docs/orchestration/phase6c_match_identity_bridge_report_2026-04-29.md
- docs/orchestration/phase6a_clv_data_contract_2026-04-29.md
- data/derived/odds_snapshots_2026-04-29.jsonl
- data/wbc_backend/reports/prediction_registry.jsonl

REQUIRED OUTPUT:
Create: docs/orchestration/phase6e_aligned_clv_capture_design_YYYY-MM-DD.md

Required sections:
1. Domain Commitment
2. Prediction Registry Schema Extension (add canonical_match_id FK)
3. Crawler Scheduling Policy (pre-match capture window, OPENING/CLOSING rules)
4. Settlement Join Design
5. Sample Accumulation Policy (path to ≥200 matched, settled bets)
6. Leakage Guard Specification
7. Phase 6F Implementation Readiness Gate
8. Scope Confirmation

FORBIDDEN:
- Do not modify code, data, DB, crawler, model.
- Do not run CLV validation.
- Do not copy LotteryNew logic or terms.
- Do not commit.

ACCEPTANCE:
File created, contamination = 0, scope constraints confirmed.
```

---

### If Option A (Regular-Season Expansion) is chosen instead:

```text
# TASK: BETTING-POOL ORCHESTRATION PHASE 6E — MLB/KBO/NPB PREDICTION REGISTRY EXTENSION

Follow AI system rules.

GOAL:
Design the prediction registry extension to cover MLB/KBO/NPB regular-season games,
enabling CLV validation with existing TSL odds snapshots.

This task is design-only. Do not modify code, data, DB, crawler, or model.
Do not commit.

CONTEXT:
- Phase 6D recommended Option A (expand prediction registry) as fallback path.
- TSL odds cover MLB (30 teams), KBO (10), NPB (12) from 2026-03-13 onward.
- Phase 6B/6C adapters are domain-agnostic and reusable.
- Walk-forward used 2,188 MLB games internally (not persisted per-match).

REQUIRED INPUTS:
- docs/orchestration/phase6d_clv_readiness_decision_2026-04-29.md
- docs/orchestration/phase6b_odds_snapshot_adapter_report_2026-04-29.md
- docs/orchestration/phase6a_clv_data_contract_2026-04-29.md
- data/derived/team_alias_map_2026-04-29.csv
- data/wbc_backend/model_artifacts.json

REQUIRED OUTPUT:
Create: docs/orchestration/phase6e_mlb_kbo_npb_prediction_extension_design_YYYY-MM-DD.md

Required sections:
1. League Coverage Plan (MLB priority, KBO, NPB rollout sequence)
2. Prediction Registry Schema Extension
3. Feature Availability Assessment per League
4. Settlement Coverage Sources per League
5. Sample Sufficiency Rules per League
6. Model Scope Gate (walk-forward validation required before production bets)
7. Phase 6F CLV Validation Readiness Gate
8. Scope Confirmation

FORBIDDEN:
- Do not modify code, data, DB, crawler, model.
- Do not run CLV validation.
- Do not copy LotteryNew logic or terms.
- Do not commit.

ACCEPTANCE:
File created, contamination = 0, scope constraints confirmed.
```

---

## 9. Scope Confirmation

This document is a decision analysis and design document only.

| Constraint | Status |
|---|---|
| Code modified | NO |
| Data files modified | NO |
| DB modified | NO |
| Crawler modified | NO |
| Model modified | NO |
| External API called | NO |
| Orchestrator task created | NO |
| Git commit made | NO |
| CLV validation run | NO |
| Phase 6E implementation started | NO |

All Phase 6 predecessor outputs (`odds_snapshots_2026-04-29.jsonl`, `team_alias_map_2026-04-29.csv`,
`match_identity_bridge_2026-04-29.jsonl`) remain unchanged and are confirmed reusable.

---

**PHASE_6D_DECISION_COMPLETE**

*Next action: Obtain project domain commitment (WBC vs regular-season), then proceed to Phase 6E using the appropriate prompt from §8 above.*
