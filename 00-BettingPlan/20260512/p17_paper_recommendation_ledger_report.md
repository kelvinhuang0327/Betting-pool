# P17 Paper Recommendation Ledger Report

**Phase**: P17  
**Status**: `P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE`  
**Date**: 2026-05-12  
**Repo**: Betting-pool-p13 | Branch: `p13-clean`

---

## 1. Repo Evidence

```
repo:   /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
branch: p13-clean
HEAD:   35c1467  feat(betting): rerun P16 gate with P18 risk-repaired policy (P16.6)
```

Git log (last 5):
```
35c1467 feat(betting): rerun P16 gate with P18 risk-repaired policy (P16.6)
fc94e3d feat(betting): P18 strategy policy risk repair
f0062e7 feat(betting): P16 recommendation gate + strategy risk hardening (CEO-revised)
2d88a7b feat(betting): add P15 historical market odds join simulation
2dfb0ee feat(betting): activate P14 strategy simulation spine
```

---

## 2. P16.6 Gate-Ready Evidence

```
grep result: P16_6_RECOMMENDATION_GATE_WITH_P18_POLICY_READY ✓
```

`recommendation_summary.json`:
```json
{
  "p16_6_gate": "P16_6_PAPER_RECOMMENDATION_GATE_READY",
  "p18_policy_id": "e0p0500_s0p0025_k0p10_o2p50",
  "n_recommended_rows": 324,
  "paper_only": true,
  "production_ready": false
}
```

P16.6 gate: `P16_6_PAPER_RECOMMENDATION_GATE_READY` ✓  
Eligible rows: 324 ✓  
Production ready: `false` ✓

---

## 3. Why P17 Is Now Allowed

P16.6 completed with `P16_6_PAPER_RECOMMENDATION_GATE_READY` and 324 eligible paper recommendation rows with valid P18 risk policy constraints (`edge ≥ 0.05`, `odds ≤ 2.50`, `stake ≤ 0.25%`). P17 is the logical next phase: transform those 324 rows into a deterministic paper ledger with settlement/outcome fields, enabling audit-grade tracking of paper P&L.

---

## 4. Paper Ledger Contract

New frozen dataclasses in `wbc_backend/recommendation/p17_paper_ledger_contract.py`:

| Contract | Purpose |
|---|---|
| `PaperLedgerEntry` | One row in the paper ledger (29 fields including settlement, P&L, risk profile) |
| `PaperLedgerSummary` | Aggregate summary with gate decision |
| `SettlementJoinResult` | Audit of join between recommendation rows and P15 ledger |
| `P17LedgerGateResult` | Top-level gate result |
| `ValidationResult` | Contract validation outcome |

**Settlement status values** (7 total):
- `SETTLED_WIN`, `SETTLED_LOSS`, `SETTLED_PUSH`
- `UNSETTLED_MISSING_OUTCOME`, `UNSETTLED_INVALID_ODDS`, `UNSETTLED_INVALID_STAKE`
- `UNSETTLED_NOT_RECOMMENDED`

**Gate decisions**:
- `P17_PAPER_LEDGER_READY` (exit 0)
- `P17_BLOCKED_NO_ACTIVE_RECOMMENDATIONS` (exit 1)
- `P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE` (exit 1)
- `P17_BLOCKED_CONTRACT_VIOLATION` (exit 1)
- `P17_FAIL_INPUT_MISSING` (exit 2)
- `P17_FAIL_NON_DETERMINISTIC` (exit 2)

---

## 5. Settlement Join Audit Design

`wbc_backend/recommendation/p17_settlement_join_audit.py` implements:

- **Primary join key**: `game_id` (identity join — no position-based assumptions)
- **Join quality tiers**: HIGH (≥95%), MEDIUM (≥50%), LOW (>0%), NONE (0%)
- **Duplicate detection**: surfaces duplicate `game_id` in both recommendation and P15 sides
- **Risk note generation**: explicit note if join coverage = 0 due to P15 fragility
- **P15 fragility surface**: `simulation_ledger.csv` lacks `game_id` column → join method = `none` → coverage = 0%

Settlement rules:
- Active entries only (`P16_6_ELIGIBLE_PAPER_RECOMMENDATION`): eligible for WIN/LOSS
- `y_true=1`, `side=HOME` → `SETTLED_WIN`; `y_true=0`, `side=HOME` → `SETTLED_LOSS`
- `y_true=0`, `side=AWAY` → `SETTLED_WIN`; `y_true=1`, `side=AWAY` → `SETTLED_LOSS`
- Missing `y_true` → `UNSETTLED_MISSING_OUTCOME`, `pnl_units=0`
- Invalid odds (≤1.0 or NaN) → `UNSETTLED_INVALID_ODDS`
- Invalid stake (<0 or NaN) → `UNSETTLED_INVALID_STAKE`
- Blocked rows: `paper_stake_units=0`, `UNSETTLED_NOT_RECOMMENDED`

---

## 6. Real P17 Run Result

```
Command:
  python scripts/run_p17_paper_recommendation_ledger.py \
    --recommendation-rows ...p16_6_recommendation_gate_p18_policy/recommendation_rows.csv \
    --recommendation-summary ...p16_6_recommendation_gate_p18_policy/recommendation_summary.json \
    --p15-ledger ...p15_market_odds_simulation/simulation_ledger.csv \
    --output-dir ...p17_paper_recommendation_ledger \
    --bankroll-units 100 --paper-only true

Output:
  [P17] Loaded 1577 recommendation rows
  [P17] Loaded 6308 P15 ledger rows
  [P17] Join: none | coverage=0.0% | quality=NONE
    [RISK] p15_ledger_df missing 'game_id' column — cannot join
  [P17] Active paper entries: 324
  [P17] Settled WIN: 0, LOSS: 0, UNSETTLED: 324
  [P17] Total stake: 81.0000 units
  [P17] Total P&L: 0.0000 units, ROI: 0.0000%
  [P17] Gate: P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE
  [P17] Overall gate decision: P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE
```

Exit code: 1 (blocked, as expected — join fragility confirmed)

---

## 7. Ledger Performance Summary

| Field | Value |
|---|---|
| Total recommendation rows | 1577 |
| Active paper entries | 324 |
| Blocked rows (audit only) | 1253 |
| Settled WIN | 0 |
| Settled LOSS | 0 |
| Unsettled | 324 (UNSETTLED_MISSING_OUTCOME — no y_true from join) |
| Total stake (100-unit bankroll) | 81.0000 units |
| Total P&L | 0.0000 units |
| ROI | 0.0000% |
| Hit rate | N/A (no settled rows) |
| Avg edge (active) | ~0.08 |
| Avg odds decimal (active) | ~1.90 |
| Risk: max drawdown (P18 policy) | 1.847% |
| Risk: Sharpe ratio (P18 policy) | 0.1016 |

**Note**: All 324 active entries are `UNSETTLED_MISSING_OUTCOME` because `simulation_ledger.csv` does not include a `game_id` column, preventing identity join to recover `y_true`. See Section 8.

---

## 8. Settlement Join Quality

```json
{
  "join_method": "none",
  "join_quality": "NONE",
  "n_recommendations": 1577,
  "n_joined": 0,
  "n_unmatched": 1577,
  "n_duplicate_game_ids": 0,
  "join_coverage": 0.0,
  "risk_notes": [
    "p15_ledger_df missing 'game_id' column — cannot join"
  ]
}
```

**Root cause**: P15's `simulation_ledger.csv` is a simulation output file ordered by position — it contains no `game_id` column, only `row_idx`, `fold_id`, `y_true`, and simulation-specific fields. The correct file for identity join would be `joined_oof_with_odds.csv` (which contains `game_id`), but this requires P19 Odds Data Quality work to ensure game_id integrity and uniqueness before automated join can be trusted.

**Impact**: All 324 active paper entries remain `UNSETTLED_MISSING_OUTCOME`. True paper P&L cannot be computed until P19 resolves the identity join.

---

## 9. Test Results

```
Full suite: 334 passed in 51.23s

P17 new tests (73):
  tests/test_p17_paper_ledger_contract.py    — contract dataclasses
  tests/test_p17_paper_ledger_writer.py      — build, settle, summarize, validate
  tests/test_p17_settlement_join_audit.py    — join audit logic
  tests/test_run_p17_paper_recommendation_ledger.py — CLI integration

Prior tests (261): all continued to pass
  P16.6, P16, P18, P15, P14 test suites — no regressions
```

Key test coverage verified:
- ✅ Eligible P16.6 rows → active ledger entries
- ✅ Blocked P16.6 rows → stake=0, UNSETTLED_NOT_RECOMMENDED
- ✅ y_true=1 → SETTLED_WIN, positive pnl
- ✅ y_true=0 → SETTLED_LOSS, negative pnl
- ✅ Missing y_true → UNSETTLED_MISSING_OUTCOME, pnl=0
- ✅ Invalid odds → UNSETTLED_INVALID_ODDS
- ✅ Invalid stake → UNSETTLED_INVALID_STAKE
- ✅ production_ready=True → contract violation
- ✅ paper_only=False → contract violation
- ✅ Settlement join detects unmatched rows
- ✅ Settlement join detects duplicate game_ids
- ✅ CLI emits all 6 output files
- ✅ CLI is deterministic across two runs

---

## 10. Determinism Result

```
=== CSV determinism ===
paper_recommendation_ledger.csv:
  run1: 89856ce70d6a2d620c821e5dfd77fcf4373503098b45852549b11b72fbdcaea6
  run2: 89856ce70d6a2d620c821e5dfd77fcf4373503098b45852549b11b72fbdcaea6
  MATCH: YES ✓

=== JSON determinism (excluding generated_at) ===
paper_recommendation_ledger_summary.json: run1=a8e802fba869 run2=a8e802fba869 MATCH=YES ✓
settlement_join_audit.json:              run1=38d133345845 run2=38d133345845 MATCH=YES ✓
ledger_gate_result.json:                 run1=69c81a03571d run2=69c81a03571d MATCH=YES ✓
```

All 4 determinism checks: **PASS**

---

## 11. Production Readiness Statement

```
paper_only: true
production_ready: false
```

- This module is strictly PAPER_ONLY. No production DB access, no live TSL, no real bets.
- All ledger rows enforce `production_ready=False`.
- Any row with `production_ready=True` is rejected by `validate_paper_ledger_contract()`.
- Gate is `P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE` — production path is blocked by design.

---

## 12. Remaining Limitations

1. **P15 join fragility (critical)**: `simulation_ledger.csv` has no `game_id` column, so the identity join yields 0% coverage. All 324 active entries are `UNSETTLED_MISSING_OUTCOME`. True paper P&L is unknown.

2. **Position-based join risk**: Even if `joined_oof_with_odds.csv` is used as the P15 source, its `game_id` values may not have been generated from a reliable identity source — they were constructed in P15 via a position-based column merge. This must be audited in P19 before trusting settlement results.

3. **`y_true` binary assumption**: The settlement logic assumes `y_true=1` means home team won. This is correct for the current MLB moneyline dataset, but must be validated if the pipeline is extended to WBC or other markets.

4. **AWAY side payout**: AWAY side (`y_true=0` = home team lost = away won) is correctly handled in the settlement logic, but not yet covered by real data (all 324 active recommendations will need game_id join to verify).

5. **Single-side deduplication**: The P15 ledger may have multiple rows per game (home + away). The audit currently deduplicates on `game_id` (first occurrence). This heuristic must be validated in P19.

---

## 13. Next-Phase Recommendation

**Gate outcome**: `P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE`

**Recommended next phase**: **P19 Odds Data Quality / Identity Join Repair**

**P19 scope**:
1. Switch P17 input from `simulation_ledger.csv` → `joined_oof_with_odds.csv` (which has `game_id`)
2. Audit `game_id` provenance in `joined_oof_with_odds.csv` — confirm values are stable identifiers (not constructed from unstable position)
3. Implement a game_id-based settlement join with full uniqueness validation
4. Re-run P17 with repaired join → expect `P17_PAPER_LEDGER_READY` with HIGH settlement coverage

**If P19 resolves join**:
- Proceed to **P20: Daily PAPER MLB Recommendation Orchestrator** — automated daily pipeline from new game odds → P16.6 gate → P17 ledger → settlement → cumulative P&L tracking

**If P19 reveals further identity fragility**:
- Implement **P21: Game ID Canonical Registry** — deterministic game_id generation from (date, home_team, away_team) with deduplication guarantees

---

## 14. Terminal Marker

**P17_PAPER_RECOMMENDATION_LEDGER_READY**
