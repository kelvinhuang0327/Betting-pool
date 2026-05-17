# P39J CTO Decision Gate
**Date:** 2026-05-15  
**paper_only:** True | **production_ready:** False

---

## P39I Conclusion (Input to This Gate)

| Item | Value |
|------|-------|
| Classification | `P39I_NO_ROBUST_IMPROVEMENT` |
| Folds evaluated | 4 temporal folds (chronological walk-forward) |
| Feature groups tested | 5 (diff-only, home/away rolling, full Statcast, p_oof+Statcast) |
| Best group mean ΔBrier | +0.0016 (home_away_rolling_only — **worsening**) |
| % folds improved (best group) | 25% (threshold: ≥60%) |
| Worst fold degradation | +0.0069 (exceeds +0.005 threshold) |
| P38A baseline | Brier ≈ 0.2487 — **remains operative model** |
| Statcast batting rolling track | **FROZEN** — do not repeat this direction |

---

## Decision Options

### Option 1 — PUSH_LOCAL_COMMITS
- **What**: Push 16 local commits on `p13-clean` to `origin/p13-clean`
- **Risk**: Low — all commits are paper-only, no secrets, no raw data
- **Effort**: 15 minutes (forbidden-file check + single push command)
- **Value**: Backs up 16 sessions of work to remote; enables collaboration
- **Signal required**: `YES: push the 16 local commits on p13-clean to origin`
- **Command**: `git push origin p13-clean:p13-clean`
- **Constraint**: `origin/main` must remain untouched

### Option 2 — P3_ODDS_UNBLOCK
- **What**: Provide real pregame moneyline odds → enable CLV / EV research
- **Risk**: Medium — requires operator decision on API / data license
- **Effort**: Depends on path (API key: hours; CSV drop: 1 day; paid provider: weeks)
- **Value**: **Highest ROI** — genuine market calibration, CLV benchmark, EV calculation
- **Signal required (any one)**:
  - `KEY_READY: The Odds API key is in .env as THE_ODDS_API_KEY`
  - `DATA_READY: I dropped a CSV to data/research_odds/local_only/`
- **Unblock paths**: The Odds API / Pinnacle / local manual import (see P39J P3 assessment)

### Option 3 — PITCHER_FEATURE_PILOT
- **What**: Explore pitcher-level features (starter ERA/FIP rolling, bullpen workload)
- **Risk**: Low-medium — pybaseball data available; may yield more signal than batting features
- **Effort**: 1–2 sessions to build + validate
- **Value**: Medium — pitcher quality correlates more directly with run prevention than batting rolling averages
- **Rationale**: P39 batting rolling features failed; pitcher-level is a distinct, unexplored dimension
- **Signal required**: `CTO_DECISION: run pitcher feature pilot`
- **Next task if approved**: P39K pitcher feature feasibility spike

### Option 4 — PAUSE_FEATURE_RESEARCH
- **What**: Halt all feature research until P3 odds source is unblocked
- **Risk**: Near zero — no new code or data
- **Effort**: Zero
- **Value**: Avoids diminishing-returns feature work; focuses attention on the bottleneck (odds)
- **Rationale**: Without CLV/EV, feature improvements cannot be monetized even if found
- **Signal required**: None — this is the default if no other signal is given

---

## Recommended Priority

```
1. PUSH_LOCAL_COMMITS     → lowest risk, fastest, backs up 16 sessions (15 min)
2. P3_ODDS_UNBLOCK        → highest ROI, unlocks CLV/EV research axis
3. PITCHER_FEATURE_PILOT  → only if CTO wants to continue feature research
4. PAUSE_FEATURE_RESEARCH → default if no signal
```

**CTO recommended sequence**: Push first (Option 1), then resolve P3 odds operator decision (Option 2). Options 3 and 4 are mutually exclusive and lower priority.

---

## Explicit Operator Signals Required

| Action | Signal |
|--------|--------|
| Push 16 commits | `YES: push the 16 local commits on p13-clean to origin` |
| Unblock via API key | `KEY_READY: The Odds API key is in .env as THE_ODDS_API_KEY` |
| Unblock via CSV drop | `DATA_READY: I dropped a CSV to data/research_odds/local_only/` |
| Pitcher pilot | `CTO_DECISION: run pitcher feature pilot` |
| Pause everything | *(no signal — default)* |

---

## Hard Guards

- No repeated Statcast batting rolling ablation (P39 track frozen)
- No production edge claim
- No odds claim without verified odds source
- No push without explicit YES
- No API call without KEY_READY
- No CSV ingestion without DATA_READY

---

## Acceptance Marker

`P39J_CTO_DECISION_GATE_READY_20260515`
