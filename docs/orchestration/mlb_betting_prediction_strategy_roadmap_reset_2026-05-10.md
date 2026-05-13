# MLB Betting Prediction and Strategy Optimization Roadmap

**Original reset date:** 2026-05-10  
**CTO realignment date:** 2026-05-12  
**Current repo guard:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`  
**Current branch guard:** `p13-clean`  
**Scope:** MLB prediction mapped to Taiwan Sports Lottery PAPER recommendations, plus strategy simulation / optimization.  
**Current gate:** `P15_ODDS_AWARE_SIMULATION_READY`  
**Production status:** `paper_only=True`, `production_ready=False`

Marker: `CTO_MLB_P15_P16_ROADMAP_REALIGNMENT_20260512_READY`

---

## 1. CTO Decision

The system has moved past the 2026-05-11 P12 blocker. The earlier roadmap said the next priority was model architecture repair because all P12 feature ablations had negative BSS. That is now stale.

Current evidence:

| Phase | Result | Product meaning |
|---|---|---|
| P13 | `P13_WALK_FORWARD_LOGISTIC_BASELINE_READY`; OOF BSS `+0.008253` | Model probability quality is now positive enough for PAPER simulation promotion. |
| P14 | `P14_STRATEGY_SIMULATION_SPINE_READY`; simulation spine activated | Strategy policies can consume P13 OOF probabilities deterministically. |
| P15 | `P15_ODDS_AWARE_SIMULATION_READY`; odds coverage `1575/1577 = 99.87%` | Historical market odds are joined, enabling edge / ROI / capped Kelly PAPER evidence. |

Therefore the next most valuable optimization direction is:

```text
P16 Recommendation Gate Re-evaluation
```

P16 should consume the completed P13 + P15 artifacts and determine whether the MLB PAPER recommendation layer can issue auditable PAPER_ONLY recommendation rows. It must not repair live TSL, place bets, or claim production readiness.

---

## 2. Product North Star

Betting-pool has two product axes:

1. **MLB prediction -> Taiwan Sports Lottery recommendation**
   - Convert model probability, market probability, edge, and odds into auditable recommendation rows.
   - Support TSL-style markets over time: moneyline, run line, totals, first-five, odd/even, team totals.
   - Keep all current output PAPER_ONLY.

2. **Strategy simulation optimization**
   - Validate policies through walk-forward / OOF evidence before any recommendation is trusted.
   - Optimize staking and abstention rules with ROI, BSS, ECE, drawdown, exposure, and settlement evidence.
   - Treat positive ROI as research evidence only until live-source and production gates are separately cleared.

The roadmap must keep these axes connected:

```text
model probabilities -> historical odds join -> strategy simulation -> recommendation gate -> paper ledger -> settlement/optimization
```

---

## 3. Current Implementation State

### Completed / usable

- P13 walk-forward logistic baseline:
  - `source_model = p13_walk_forward_logistic`
  - OOF BSS `+0.008253`
  - OOF rows `1577`
  - Marker: `P13_WALK_FORWARD_LOGISTIC_BASELINE_READY`

- P14 strategy simulation spine:
  - Deterministic PAPER simulation runner exists.
  - Policies include `flat`, `capped_kelly`, `confidence_rank`, `no_bet`.
  - P14 market-absent mode correctly blocked odds-dependent Kelly until P15.
  - Marker: `P14_STRATEGY_SIMULATION_SPINE_READY`

- P15 historical market odds adapter:
  - `joined_oof_with_odds.csv` contains `p_oof`, `p_market`, `edge`, `odds_decimal_home`, `odds_decimal_away`, `odds_join_status`.
  - Odds join coverage `99.87%`.
  - Invalid odds rows `2`.
  - `capped_kelly` PAPER ROI `+5.51%`.
  - `confidence_rank` PAPER ROI `+0.055%`.
  - Marker: `P15_MARKET_ODDS_JOIN_SIMULATION_READY`

- Existing recommendation smoke layer:
  - `wbc_backend/recommendation/recommendation_row.py`
  - `wbc_backend/recommendation/recommendation_gate_policy.py`
  - `scripts/run_mlb_tsl_paper_recommendation.py`
  - It enforces PAPER_ONLY, writes under `outputs/recommendations/PAPER/`, and blocks when TSL/simulation gates block.

### Still blocked / incomplete

- The recommendation layer does not yet consume P15 joined odds artifacts directly.
- Existing recommendation smoke script may use estimated odds and TSL availability checks; it is not the P15 odds-aware recommendation path.
- No P16 adapter exists yet to transform `joined_oof_with_odds.csv` into recommendation candidates.
- No P16 gate exists yet with explicit P13/P15 reason codes.
- No recommendation summary exists with `n_recommended_rows`, `n_blocked_rows`, and gate reason distribution.
- Live TSL remains unresolved and must stay out of P16.
- Production remains blocked.

---

## 4. Roadmap Alignment Gaps

| Area | Previous roadmap assumption | Actual 2026-05-12 state | CTO adjustment |
|---|---|---|---|
| Model quality | P13 still needed to repair negative BSS | P13 is complete with OOF BSS `+0.008253` | Move model repair from immediate P0 to later improvement track. |
| Simulation | Market odds absent, Kelly blocked | P15 joined historical odds; capped Kelly can run | Promote odds-aware simulation evidence into recommendation gate. |
| Recommendation | Smoke path exists but simulation/TSL still block | Existing script is not P15-aware and can use estimated odds | Build P16 P15-artifact recommendation gate, not live smoke. |
| Live TSL | Treated as early blocker | Still unresolved, but not required for historical PAPER P16 | Keep live TSL as production blocker, not P16 blocker. |
| Strategy optimization | Could wait after recommendation | P15 now exposes ROI/edge/stake evidence | Put strategy hardening immediately after P16/P17 ledger. |
| Production | Could be confused by positive ROI | `production_ready=False` remains correct | Every phase must preserve PAPER_ONLY until live-source + human approval. |

---

## 5. Reordered P0-P10 Execution Roadmap

### P0 - P16 Recommendation Gate Re-evaluation

**Goal:** connect P13 probabilities and P15 joined historical odds to the PAPER recommendation gate.

**Why now:** This is the first step that converts research/simulation evidence into the product-facing recommendation contract while staying PAPER_ONLY.

**Work:**
- Create `p16_recommendation_input_adapter.py` to consume `joined_oof_with_odds.csv`.
- Create `p16_recommendation_gate.py` with explicit reason codes.
- Create `p16_recommendation_row_builder.py`.
- Create `scripts/run_p16_recommendation_gate_reevaluation.py`.
- Emit `recommendation_rows.csv`, `recommendation_summary.json`, `recommendation_summary.md`, and `gate_reason_counts.json`.

**Acceptance:**
- P13/P14/P15 markers verified.
- All invalid/missing odds rows are preserved and blocked.
- Passed rows may have `paper_stake_fraction > 0`.
- Failed rows always have stake `0`.
- `paper_only=True`, `production_ready=False`.
- Determinism check passes.
- Final marker: `P16_RECOMMENDATION_GATE_REEVALUATION_READY`.

### P1 - P17 Paper Recommendation Ledger / Settlement Join

**Goal:** turn P16 recommendation rows into an auditable PAPER ledger that can be settled against known outcomes.

**Work:**
- Join P16 rows with `y_true` / final game result where available.
- Record paper P/L, stake, odds, side, gate decision, and no-bet reasons.
- Produce daily/season ledger summaries.
- Preserve blocked rows as first-class rows.

**Acceptance:**
- Ledger reconciles recommendation rows to settlement labels.
- No production DB write.
- No live TSL call.
- Summary exposes ROI, hit rate, average edge, average stake, and reason-code distribution.

### P2 - P18 Strategy Optimization Hardening

**Goal:** make strategy simulation a real optimization engine, not just a proof that the spine can run.

**Work:**
- Add `avg_edge_pct` and `avg_kelly_fraction` to P15/P18 policy summaries.
- Run threshold sweeps for edge threshold, Kelly cap, confidence rank cutoff, and no-bet abstention.
- Add drawdown, turnover, exposure, and bankroll trajectory.
- Separate raw implied probability from no-vig market probability.
- Compare flat, capped Kelly, fractional Kelly, confidence-rank, and abstention-heavy policies.

**Acceptance:**
- Strategy ranking is based on walk-forward/OOF evidence plus drawdown and exposure, not ROI alone.
- Positive ROI is reported as PAPER evidence only.
- Capped Kelly promotion requires stable risk metrics, not just one headline ROI.

### P3 - P19 Market Odds Data Quality and Identity Audit

**Goal:** improve audit quality of the historical market odds join before expanding markets.

**Work:**
- Investigate the 2 invalid odds rows.
- Keep deterministic fold/position alignment tests.
- Add row-level join audit output with source row index, fold id, and invalid reason.
- Normalize American/decimal odds conversion contracts.
- Add optional vig-removal method for moneyline pairs.

**Acceptance:**
- Invalid odds are explained, not merely counted.
- Join coverage and identity mapping are reproducible.
- Market probability semantics are explicit: raw implied vs no-vig.

### P4 - P20 Daily PAPER MLB Recommendation Orchestrator

**Goal:** run daily PAPER recommendation output using the P16 row contract, not the older smoke-only estimate path.

**Work:**
- Build a daily runner that consumes approved PAPER artifacts or approved source snapshots.
- Emit all eligible games, not one smoke row.
- Keep TSL live disabled unless explicitly sourced through an approved bridge.
- Surface recommended/watch/pass/blocked rows.

**Acceptance:**
- Daily PAPER output can be regenerated deterministically.
- Recommendation rows include model source, odds source, edge, stake, gate reason, and production flags.
- No estimated odds are represented as real TSL odds.

### P5 - P21 Live TSL / Market Source Repair

**Goal:** solve real market data availability without weakening historical PAPER gates.

**Options:**
- TSL session/cookie workflow.
- Approved API / partner source.
- Operator-provided CSV bridge.
- Manual odds snapshot ingestion with provenance and timestamp.

**Acceptance:**
- Live/pre-game odds have source timestamp, market identity, and replayable snapshot.
- Recommendation rows distinguish historical odds, approved snapshot odds, and live TSL odds.
- Production remains blocked until live-source validation passes.

### P6 - P22 Model Improvement and Calibration

**Goal:** improve model quality after the product contract is stable.

**Work:**
- Segment P13 by home/away, favorite/underdog, high/low odds, month, and park/starter buckets.
- Compare logistic regression with regularized variants and tree/boosted models.
- Add calibration selection only with walk-forward or OOF evidence.
- Evaluate BSS, ECE, log-loss, ROI proxy, and decision quality.

**Acceptance:**
- No model replaces P13 unless it improves OOF/walk-forward evidence.
- No in-sample calibration is allowed into recommendation decisions.

### P7 - P23 TSL Market Expansion Beyond Moneyline

**Goal:** expand to Taiwan Sports Lottery betting items after moneyline contracts are reliable.

**Order:**
1. Run line.
2. Totals.
3. First-five moneyline / spread / total.
4. Odd/even.
5. Team totals.

**Acceptance:**
- Each market has labels, odds schema, settlement semantics, and no-lookahead validation.
- Markets without reliable labels or odds remain blocked with explicit reason codes.

### P8 - P24 CI, Regression, and Worktree Hygiene

**Goal:** keep the research branch trustworthy as new P16/P17/P18 outputs accumulate.

**Work:**
- Maintain focused P13-P18 regression suites.
- Quarantine unrelated legacy failures without hiding product regressions.
- Avoid staging `outputs/`, `runtime/`, `.venv/`, DB binaries, or large generated files.
- Document dirty-worktree context before commits.

**Acceptance:**
- A CTO can tell whether a failing test blocks MLB recommendation work or belongs to legacy debt.
- Source/report/test commits stay clean.

### P9 - P25 Daily Ops and Monitoring

**Goal:** make the PAPER system observable enough to run every day.

**Work:**
- Track source availability, artifact freshness, recommendation count, blocked count, stake exposure, and drift.
- Add alerts for missing P13/P15/P16 inputs.
- Add daily summaries for model metrics, market metrics, gate reasons, and settlement performance.

**Acceptance:**
- A daily operator can tell whether the system produced no recommendations because there was no edge, no odds, no data, or a gate failure.

### P10 - P26 Production Proposal Gate

**Goal:** define the minimum bar for any future production request.

**Minimum gate:**
- Positive and stable walk-forward evidence.
- Auditable pre-game features.
- Approved live or snapshot market source.
- Recommendation ledger and settlement join ready.
- Strategy drawdown/exposure within approved limits.
- Human approval, rollback plan, and clear no-bet fail-safe.

**Current status:** deferred. P15/P16 evidence is necessary but not sufficient.

---

## 6. Key Blockers

1. **Recommendation layer not P15-aware yet.** This is the immediate P0 blocker.
2. **Live TSL unresolved.** This blocks production and true live recommendations, but not P16 historical PAPER rows.
3. **Historical odds source is not live TSL.** P15 proves replay/historical odds-aware behavior only.
4. **2 invalid odds rows remain unexplained.** Low volume, but should be audited in P19.
5. **Strategy summary lacks avg edge / avg Kelly.** P18 should fix this before optimizing stake policies.
6. **Existing smoke recommendation path can use estimated odds.** It must not be confused with P16 P15-backed recommendation rows.
7. **Production readiness confusion risk.** Positive capped Kelly ROI must remain labeled PAPER evidence.

---

## 7. Immediate Engineering Sequence

1. Run P16 Recommendation Gate Re-evaluation.
2. If P16 emits eligible rows, proceed to P17 Paper Recommendation Ledger / Settlement Join.
3. If P16 emits no eligible rows, inspect gate reason distribution and edge threshold.
4. After ledger exists, run P18 strategy hardening with drawdown/exposure.
5. Only after P16-P18 are stable, reopen live TSL / approved odds-source repair as P21.

Do not start with live TSL repair unless the explicit task is production-source readiness. The current product value bottleneck is the PAPER recommendation contract, not live execution.

---

## 8. CTO Recommendation

Proceed with P16 now.

The system is no longer blocked by negative BSS or absent historical market odds. It is blocked by the missing adapter between odds-aware simulation evidence and recommendation rows.

P16 should answer one concrete question:

```text
Can Betting-pool produce deterministic, auditable, PAPER_ONLY MLB recommendation rows
from P13 walk-forward probabilities and P15 historical market odds?
```

Until that answer is available:

- Do not tune the model first.
- Do not repair live TSL first.
- Do not expand to additional markets first.
- Do not claim production readiness.

Current production readiness remains:

```text
production_ready = false
paper_only = true
```

CTO_MLB_P15_P16_ROADMAP_REALIGNMENT_20260512_READY

---

## Roadmap v3 Update — 2026-05-13

**Superseded by**: `00-BettingPlan/20260513/cto_roadmap_realignment_20260513.md`

Key changes in v3:
- P30 "READY" acknowledged as misleading (derived outputs ≠ raw historical)
- P31 re-scoped from "build joined artifacts" → "honest data reality audit"
- Blocker chain corrected: P32 acquisition is the single highest-leverage move
- Sample wall (324 < 1,500) explicitly acknowledged as hard blocker

```
CTO_MLB_P30_P31_ROADMAP_REALIGNMENT_20260513_READY
```
