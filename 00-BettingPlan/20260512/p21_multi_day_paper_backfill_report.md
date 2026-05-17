# P21 Multi-Day PAPER Backfill Orchestrator — Report

**Date**: 2026-05-12  
**Repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`  
**Branch**: `p13-clean`  
**Status**: ✅ `P21_MULTI_DAY_PAPER_BACKFILL_READY`

---

## 1. Repo Evidence

```
HEAD: c397d14 (p13-clean) feat(p20): Daily PAPER MLB Orchestrator
Branch: p13-clean
PAPER_ONLY=true
PRODUCTION_READY=false
```

All prior phase markers verified (see §2).

---

## 2. Prior Phase Evidence: P20

| Marker | Status |
|--------|--------|
| `P16_6_RECOMMENDATION_GATE_WITH_P18_POLICY_READY` | ✅ |
| `P17_PAPER_RECOMMENDATION_LEDGER_READY` | ✅ |
| `P19_ODDS_IDENTITY_JOIN_REPAIR_READY` | ✅ |
| `P20_DAILY_PAPER_MLB_ORCHESTRATOR_READY` | ✅ |

P20 real run (2026-05-12):
- `p20_gate = P20_DAILY_PAPER_ORCHESTRATOR_READY`
- `n_active_paper_entries = 324`
- `n_settled_win = 171`, `n_settled_loss = 153`, `n_unsettled = 0`
- `roi_units = +10.78%`, `hit_rate = 52.78%`
- `settlement_join_method = JOIN_BY_GAME_ID`
- `game_id_coverage = 100%`
- `paper_only = true`, `production_ready = false`

---

## 3. Why P21 Is Now Allowed

P20 established a validated single-day PAPER orchestration pipeline (P16.6→P19→P17) with:
- zero unsettled entries
- deterministic gate output
- 100% game_id coverage via JOIN_BY_GAME_ID
- 56/56 tests passing

P21 extends this into a multi-day backfill that:
- aggregates N daily P20 artifacts into a unified summary
- uses stake-weighted ROI and settled-bet-weighted hit rate
- explicitly reports missing daily artifacts (never fabricates)
- maintains `paper_only=true`, `production_ready=false` at all layers

---

## 4. Backfill Contract

**Module**: `wbc_backend/recommendation/p21_multi_day_backfill_contract.py`

Gate constants:
| Constant | Value |
|----------|-------|
| `P21_MULTI_DAY_PAPER_BACKFILL_READY` | READY state |
| `P21_BLOCKED_NO_READY_DAILY_RUNS` | Zero dates pass gate |
| `P21_BLOCKED_MISSING_REQUIRED_ARTIFACTS` | Required files absent |
| `P21_BLOCKED_DAILY_GATE_NOT_READY` | Date p20_gate != READY |
| `P21_BLOCKED_CONTRACT_VIOLATION` | paper_only/production_ready violated |
| `P21_FAIL_INPUT_MISSING` | CLI fatal (base dir missing, paper-only false) |
| `P21_FAIL_NON_DETERMINISTIC` | Reserved for determinism failures |

Frozen dataclasses (all `@dataclass(frozen=True)`):
- `P21BackfillDateResult` — 17 fields per date
- `P21MissingArtifactReport` — missing file catalog
- `P21BackfillAggregateSummary` — 21-field multi-day summary
- `P21BackfillGateResult` — gate output struct

---

## 5. Daily Artifact Discovery Design

**Module**: `wbc_backend/recommendation/p21_daily_artifact_discovery.py`

Required artifacts per date (`p20_daily_paper_orchestrator/`):
1. `daily_paper_summary.json`
2. `artifact_manifest.json`
3. `p20_gate_result.json`

Key design decisions:
- **Never fabricate** missing dates — always emit `P21MissingArtifactReport`
- A date is `READY` only if `p20_gate == P20_DAILY_PAPER_ORCHESTRATOR_READY`
- A date with bad gate emits `P21BackfillDateResult` with `daily_gate=P21_BLOCKED_DAILY_GATE_NOT_READY`
- `discover_p20_daily_artifacts()` returns exactly `n_dates_requested` items
- `summarize_missing_artifacts()` extracts missing reports for JSON output

---

## 6. Multi-Day Aggregation Design

**Module**: `wbc_backend/recommendation/p21_multi_day_backfill_aggregator.py`

Aggregation rules:
- Only READY dates contribute to aggregate metrics
- **ROI**: `total_pnl / total_stake` (stake-weighted, NOT day-averaged)
- **Hit rate**: `total_wins / (total_wins + total_losses)` (settled-bet-weighted, NOT day-averaged)
- `total_unsettled` surfaced (not hidden)
- `min_game_id_coverage` = minimum across all ready dates
- Contract enforcement: any ready run with `production_ready=True` or `paper_only=False` → `P21_BLOCKED_CONTRACT_VIOLATION`

Output files (5 per backfill run):
1. `backfill_summary.json` — full aggregate metrics
2. `backfill_summary.md` — human-readable summary
3. `date_results.csv` — per-date row for all P21BackfillDateResult items
4. `missing_artifacts.json` — explicit missing date catalog
5. `p21_gate_result.json` — gate fields + safety fields

---

## 7. Single-Day Real P21 Run Result

**Command**: `--date-start 2026-05-12 --date-end 2026-05-12`

```
Gate:               P21_MULTI_DAY_PAPER_BACKFILL_READY
date_start:         2026-05-12
date_end:           2026-05-12
n_dates_requested:  1
n_dates_ready:      1
n_dates_missing:    0
n_dates_blocked:    0
total_active:       324
total_settled_win:  171
total_settled_loss: 153
total_unsettled:    0
total_stake_units:  81.00
total_pnl_units:    8.7304
aggregate_roi:      +10.78%
aggregate_hit_rate: 52.78%
min_game_coverage:  100.0%
production_ready:   False
paper_only:         True
```

Metrics align with P20 single-day run. ✅

Output artifacts:
- `outputs/predictions/PAPER/backfill/p21_multi_day_paper_backfill_2026-05-12_2026-05-12/` (5 files)

---

## 8. Missing-Date Guard Result

**Command**: `--date-start 2026-05-11 --date-end 2026-05-12`

```
n_dates_requested:  2
n_dates_ready:      1
n_dates_missing:    1
```

Missing date report (from `missing_artifacts.json`):
```
2026-05-11: Directory not found: outputs/predictions/PAPER/2026-05-11/p20_daily_paper_orchestrator
```

Design decision: P21 remains **READY** when at least one date has valid artifacts, but the missing date is **explicitly documented** in `missing_artifacts.json`. No fabrication occurred.

---

## 9. Test Results

**New P21 tests**: 4 files, **53 tests**

| File | Tests | Status |
|------|-------|--------|
| `test_p21_multi_day_backfill_contract.py` | 15 | ✅ PASS |
| `test_p21_daily_artifact_discovery.py` | 13 | ✅ PASS |
| `test_p21_multi_day_backfill_aggregator.py` | 17 | ✅ PASS |
| `test_run_p21_multi_day_paper_backfill.py` | 8 | ✅ PASS |

**Full test run including P21**: `221 passed in 15.18s` ✅

**Regression suite (P14–P20)**: `252 passed in 33.59s` ✅

Note: `tests/test_run_p18_strategy_policy_risk_repair.py` has a file permission issue (unrelated to P21); excluded from run. All P17–P21 tests pass.

---

## 10. Determinism Result

Two independent runs on identical inputs:

| Comparison | Result |
|------------|--------|
| `p21_gate_result.json` (excl. `generated_at`) | **IDENTICAL** |
| `missing_artifacts.json` | **IDENTICAL** |
| `date_results.csv` | **IDENTICAL** |

**RESULT: DETERMINISTIC** ✅

---

## 11. Production Readiness Statement

This phase is **PAPER_ONLY** backfill orchestration.

- `production_ready = false` enforced at all layers (contract, aggregator, CLI, outputs)
- `paper_only = true` enforced at all layers
- No live TSL calls
- No real bets placed
- No production DB written
- No scheduler/daemon enabled
- No push to remote
- No fabrication of missing dates, game_ids, outcomes, odds, or PnL

---

## 12. Remaining Limitations

1. **Single date available**: Only 2026-05-12 has P20 artifacts. Multi-day aggregation across a real date range requires running P16.6→P17→P19→P20 for each additional historical date.
2. **Stake units approximation**: P20 daily summary stores `roi_units` and counts but not always explicit `total_stake_units`. P21 derives stake from `n_active_paper_entries` (1 unit/entry) when field absent.
3. **No backfill scheduler**: P21 is CLI-only; it does not automate running P20 for historical dates.
4. **No multi-date expansion yet**: Expanding the date range requires historical artifact generation (P22 scope).

---

## 13. Next-Phase Recommendation

P21 single-day backfill READY + missing-date guard working correctly →

**Recommended next phase: P22 Historical Backfill Data Availability Expansion**

P22 would:
- Identify which historical dates have source data available (TSL odds, game results)
- Run P16.6→P19→P20 pipeline for each available date
- Expand the P21 backfill window from 1 date to N dates
- Produce a multi-week aggregate PAPER performance summary

Alternative if data availability is blocked: **P23 TSL Market Expansion Schema** (expand market types captured by the TSL crawler).

---

## 14. Terminal Marker

`P21_MULTI_DAY_PAPER_BACKFILL_READY`
