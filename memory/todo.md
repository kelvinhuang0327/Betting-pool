# LLM Research Plan: WBC 2026 Strategy Governance & Optimization

## Phase 1: Data Integrity & Consistency Check
- [x] Step 1: Verify data consistency (game_id, timestamps, scores, odds).
- [x] Step 2: Identify data gaps and define stop conditions.

## Phase 2: Strategy Performance Evaluation
- [x] Step 3: Extract registry data and rank Top 3 strategies (Single/2-game/3-game).
- [x] Step 4: Perform multi-window analysis (30/100/300/Full) for Edge, Sharpe, and Drawdown.

## Phase 3: Error Decomposition & Analysis
- [x] Step 5: Decompose misses into noise, feature gaps, and regime shifts.
- [x] Step 6: Perform consistency checks on starter info and market availability.

## Phase 4: Statistical Validation & Gating
- [x] Step 7: Run real-registry Permutation and McNemar tests for top candidates.
- [x] Step 8: Calculate final Strategy Scores and identify overfitting risks.

## Phase 5: Governance & Action
- [x] Step 9: Design automated learning scheme with gate integration.
- [x] Step 10: Counter-evidence check (Board Deliberation).
- [x] Step 11: Gate Decision (Stage 1-5) with real evidence.
- [x] Step 12: Generate Action List (P0/P1/P2) and Final Report.

## Immediate Next Iteration (Required before deploy)
- [x] P0: Expand gate coverage to all valid pregame snapshots (real registry replay).
- [x] P1: Enforce final output probability clamp in serving layer (0.15~0.85).
- [x] P2: Re-run `scripts/verify_gating_stats.py` with Stage1~Stage5 evidence regeneration.

## New Priority Loop
- [x] P0: Recover Stage2 by reducing ensemble brier below 0.22.
- [ ] P1: Recover Stage4 by statistically significant improvement vs Bayesian baseline.
- [ ] P2: Recover Stage5 by reducing rolling-10 Brier stability std below policy bound.
- [x] Evidence task: complete lambda blend search and archive results (`gate_blend_search.json`).

## Current Gate Snapshot
- [x] Stage1 Integrity: PASS
- [x] Stage2 Validation: PASS
- [x] Stage3 Risk: PASS
- [ ] Stage4 Deployment: FAIL (no significance edge)
- [ ] Stage5 Stability: FAIL (volatility too high)
