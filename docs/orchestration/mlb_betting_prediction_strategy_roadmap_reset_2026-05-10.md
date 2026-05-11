# MLB Betting Prediction and Strategy Optimization Roadmap

**Original reset date:** 2026-05-10  
**CTO execution update:** 2026-05-11 P12 completion  
**Scope:** Betting-pool only  
**Repo guard:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Mission:** MLB game prediction mapped to Taiwan Sports Lottery recommendations, plus strategy simulation / optimization as the second core track.

Marker: `CTO_MLB_P12_ABLATION_ROADMAP_20260511_READY`

> **P12 UPDATE (2026-05-11):** Feature-family ablation and context safety audit are complete.
>
> Key findings:
> - Context safety: all 4 active pregame context files are PREGAME_SAFE (bullpen/rest/weather/starters). 76 files flagged POSTGAME_RISK are output artifacts, not pipeline inputs.
> - Feature ranking: recent_form > starter > bullpen ≈ 0 > weather = 0 > rest (slightly negative).
> - Best variant: `no_rest` — OOF BSS = -0.027537, OOF ECE = 0.042400.
> - All 16 ablation variants remain BLOCKED_NEGATIVE_BSS.
> - Root cause confirmed: the logit-correction base estimator cannot produce positive BSS regardless of feature combination.
> - P13 direction: **Model Architecture Repair** — replace logit-correction pipeline with trained walk-forward ML model.
> - Test baseline: 165 passed (48 P12 new + 117 P11 regression).
> - P12 artifacts: `outputs/predictions/PAPER/2026-05-11/ablation/`, `outputs/predictions/PAPER/2026-05-11/context_safety/`
> - P12 report: `00-BettingPlan/20260511/p12_feature_family_ablation_context_safety_report.md`

---

## 1. CTO Decision

The roadmap now pivots from "add more features" to an evidence chain:

```text
context coverage -> OOF evidence -> simulation gate -> recommendation gate -> ablation/promotion decision
```

P11 repaired the context coverage blocker, but it did not clear model promotion:

- Context hit count: 2402/2402.
- Context hit rate: 1.0 after metadata repair.
- OOF BSS improved but remains negative: `-0.027668`.
- OOF ECE improved: `0.042928`.
- Strategy simulation is blocked: `BLOCKED_NEGATIVE_BSS`.
- Recommendation pipeline correctly blocks issuance: `BLOCKED_SIMULATION_GATE`.
- TSL live source remains unavailable / 403, so production remains NO-GO.

The next most valuable optimization direction is **P12 feature-family ablation plus context safety audit**, not production launch and not another general roadmap document.

---

## 2. Current Implementation State

### Completed / usable

- P11 context key reconciliation works for `Date`, `Home`, `Away`, and context game keys.
- `--auto-discover-context` finds context files and the export runs successfully.
- P11 targeted tests pass:

```text
117 passed
```

- OOF calibration artifact exists:
  - `outputs/predictions/PAPER/2026-05-11/oof_calibration_evaluation.json`
- Simulation artifact exists:
  - `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl`
- Paper recommendation artifact exists:
  - `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

### Still blocked

- Model promotion remains blocked because BSS is still negative.
- Production betting remains blocked.
- TSL live source remains blocked / unavailable.
- Context provenance is not production-safe until feature-family safety is audited.
- Existing full-suite failures / dirty worktree still need separate release hygiene.

---

## 3. Roadmap Alignment Gaps

| Area | Previous assumption | Actual P11 result | CTO adjustment |
|---|---|---|---|
| Feature expansion | More context should improve model | Coverage improved, BSS still negative | Move to ablation and safety audit |
| Context hit rate | 100% headline | JSON metric previously inconsistent | Fixed metric and require tests |
| OOF validation | Missing | Completed, improved but blocked | Use as promotion gate |
| Simulation | Pending | Completed, `BLOCKED_NEGATIVE_BSS` | Keep recommendation gate blocked |
| Recommendation | Could run after simulation | It runs, but blocks stake and issuance | Correct behavior; keep paper-only |
| Production | Not ready | Still not ready | No production proposal |
| TSL | External source concern | 403/unavailable still blocks real odds | Keep as P5 blocker |

---

## 4. Updated P0-P10 Execution Roadmap

### P0 - P12 Feature Family Ablation and Context Safety ✅ COMPLETE

**Goal:** identify which P11 feature families actually help and which are unsafe/noisy.

**Result (2026-05-11):**
- Context safety: 4 pregame pipeline files are PREGAME_SAFE; 76 POSTGAME_RISK files are output artifacts (not pipeline inputs).
- Feature family BSS impact: recent_form (−0.0022 if removed), starter (−0.0015), bullpen (0.0), weather (0.0), rest (+0.0001 noise).
- Best variant `no_rest`: OOF BSS = -0.027537 — still negative.
- Conclusion: all ablation candidates remain BLOCKED_NEGATIVE_BSS. **Roadmap moves to model architecture repair (P13/P8).**
- Tests: 48 P12 + 117 P11 = 165 passed.
- Artifacts: `outputs/predictions/PAPER/2026-05-11/ablation/`, `context_safety/`

### P1 - P11 Report and Evidence Lock

**Goal:** make P11 auditable and prevent the same coverage bug from reappearing.

**Work:**
- Keep `p11_bullpen_rest_context_key_reconciliation_report.md` as source of truth.
- Preserve targeted test coverage around `p11_context_reconciled_v1`.
- Add follow-up tests if separate context key / loader tests are created later.

**Acceptance:**
- P11 final report exists.
- `context_hit_rate` is consistent with hit/miss counts.
- Targeted tests pass.

### P2 - Simulation Gate Hardening

**Goal:** ensure recommendation output is impossible to mistake for approved betting advice when simulation blocks.

**Work:**
- Make simulation gate fields explicit in recommendation rows.
- Keep `stake_units_paper = 0.0` when gate is blocked.
- Ensure blocked rows include the simulation ID and BSS reason.

**Acceptance:**
- Negative-BSS simulation always produces `BLOCKED_SIMULATION_GATE`.
- No real-bet fields appear.

### P3 - TSL Source / Market Availability Repair

**Goal:** solve the TSL 403 / unavailable odds blocker without weakening gates.

**Options:**
- session-cookie workflow,
- API key / partner source,
- operator-provided CSV bridge,
- manually approved odds snapshot ingestion,
- continued replay-paper fallback with explicit warning.

**Acceptance:**
- Recommendation rows distinguish live TSL odds from estimated odds.
- No production claim while live odds are unavailable.

### P4 - Moneyline Recommendation MVP

**Goal:** ship a conservative paper-only moneyline MVP after simulation gate behavior is stable.

**Work:**
- Use the best safe model / feature candidate from P12.
- Generate daily rows for each game with recommend/watch/pass/blocked.
- Surface model probability, market probability, edge, data tier, and abstention reason.

**Acceptance:**
- Every row is auditable and reproducible from source snapshots.
- Blocked rows are first-class output, not hidden.

### P5 - Strategy Simulation Optimization Spine

**Goal:** turn simulation into the strategy optimizer, not just a gate.

**Work:**
- Compare flat stake, fractional Kelly, capped Kelly, drawdown-adaptive Kelly, abstention-heavy policy, and market de-risk policy.
- Track BSS, ECE, ROI proxy, CLV where available, max drawdown, turnover, hit rate, and exposure.

**Acceptance:**
- No staking policy graduates without walk-forward evidence and drawdown analysis.

### P6 - Settlement / CLV / Join Reliability

**Goal:** close the loop from prediction to market to result.

**Work:**
- Stabilize game IDs across schedule, odds, prediction, closing, and settlement.
- Track prediction timestamp, market timestamp, closing timestamp, and settlement timestamp.
- Flag inferred or stale joins.

**Acceptance:**
- CLV and EV are computed only when timestamps and market identities are valid.

### P7 - Expand Beyond Moneyline

**Order:**
1. Run line (`HDC`)
2. Totals (`OU`)
3. First 5 moneyline (`FMNL`)
4. Odd/even (`OE`)
5. Team total (`TTO`)

**Acceptance:**
- Each market has label availability, no-lookahead validation, backtest, and abstention rules.
- F5/team total stay blocked until labels and TSL lines exist.

### P8 / P13 - Model Architecture Repair ← NEXT PRIORITY

**Goal:** fix probability quality now that ablations confirmed feature tuning alone cannot produce positive BSS.

**P12 confirmed trigger:** best ablation variant `no_rest` has OOF BSS = -0.027537. No variant achieves positive BSS. Context safety is clean. Feature coverage is adequate (86–99%). The logit-correction base estimator is the bottleneck.

**P13 direction:**
- Replace logit-correction pipeline with a trained walk-forward ML estimator.
- Features to retain: `indep_recent_win_rate_delta`, `indep_starter_era_delta`.
- Features to drop: `indep_rest_days_delta` (marginal noise), weather (zero contribution).
- Bullpen: reassess with real boxscore data; current proxy contributes zero marginal signal.
- Model: logistic regression or LightGBM, walk-forward CV (same protocol as `mlb_oof_calibration.py`).
- Gate: require OOF BSS > 0 before simulation promotion.
- Input: `outputs/predictions/PAPER/2026-05-11/ablation/variant_no_rest.csv` (best P12 variant).

**Focus:**
- home-bias compression,
- probability range compression,
- strong favorite / away favourite segments,
- market-relative blending,
- feature-only logistic candidate,
- model family comparison.

**Acceptance:**
- Improvements must show out-of-sample BSS or market-relative decision quality, not just in-sample ECE.

### P9 - CI / Regression Hygiene

**Goal:** reduce noise from pre-existing failures without blocking P12.

**Work:**
- Quarantine known non-P11 failures.
- Keep targeted P11/P12 suite green.
- Do not alter branch protection casually.

**Acceptance:**
- A CTO can tell whether a failure is product regression or legacy noise.

### P10 - Production Proposal Gate

**Minimum gate:**
- Positive OOF / walk-forward BSS over sufficient sample.
- Safe pregame feature provenance.
- Valid TSL live or approved odds source.
- Settlement and CLV pipeline ready.
- Drawdown/exposure rules pass.
- Human approval and rollback plan.

**Current status:** deferred.

---

## 5. Key Blockers

1. **Negative BSS:** P11 improves BSS but remains below zero.
2. **Context safety:** rest/bullpen/weather context provenance must be proven pregame-safe.
3. **TSL 403 / unavailable:** real TSL odds are not reliably available.
4. **Simulation gate:** correctly blocks recommendation issuance.
5. **Dirty worktree:** release hygiene risk remains.
6. **Pre-existing test failures:** full-suite trust still needs cleanup/quarantine.

---

## 6. Immediate Engineering Sequence

1. Run P12 ablation candidates.
2. For each candidate, run OOF calibration and strategy simulation.
3. Rank by safe-feature BSS/ECE/gate status, not ROI proxy alone.
4. Keep moneyline recommendation blocked unless simulation gate passes.
5. Solve TSL source separately; do not combine source repair with model promotion.

---

## 7. CTO Recommendation

The system is now aligned with the two product goals:

1. MLB prediction to Taiwan Sports Lottery recommendation.
2. Strategy simulation / optimization before any recommendation is trusted.

**P12 is complete. P13 direction is confirmed.**

```text
P12 = feature family ablation + context safety audit  ✅ DONE
P13 = model architecture repair (trained walk-forward ML model)
```

P12 confirmed: no feature combination produces positive BSS with the current logit-correction estimator. Context sources are safe. The path to positive BSS requires a trained model, not more feature engineering.

P13 must achieve OOF BSS > 0 before simulation promotion. Until then:
- Simulation gate: BLOCKED_NEGATIVE_BSS
- Recommendation gate: BLOCKED_SIMULATION_GATE
- Production: deferred
- Paper stake: 0.0
