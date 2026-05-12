# P20 Daily PAPER MLB Orchestrator Report
**Date**: 2026-05-12  
**Branch**: `p13-clean`  
**Script**: `scripts/run_p20_daily_paper_mlb_orchestrator.py`  
**Terminal Marker**: `P20_DAILY_PAPER_MLB_ORCHESTRATOR_READY`

---

## 1. Mission

P20 builds a **deterministic daily PAPER-only MLB recommendation orchestrator** that chains all prior pipeline phases into a single daily summary artifact:

```
P16.6 (recommendation gate)
  → P19 (identity join repair)
    → P17 replay (enriched ledger)
      → P20 (daily paper summary + manifest)
```

No production bets. No real money. PAPER_ONLY=true, PRODUCTION_READY=false at all times.

---

## 2. Modules Built

| File | Purpose |
|------|---------|
| `wbc_backend/recommendation/p20_daily_paper_orchestrator_contract.py` | Frozen dataclasses, gate constants, step names |
| `wbc_backend/recommendation/p20_artifact_manifest.py` | SHA-256 artifact manifest builder & validator |
| `wbc_backend/recommendation/p20_daily_summary_aggregator.py` | Phase output loader, daily summary aggregator, output writer |
| `scripts/run_p20_daily_paper_mlb_orchestrator.py` | CLI entry point — exit 0/1/2 |

---

## 3. Gate Constants

| Constant | Value |
|----------|-------|
| Ready | `P20_DAILY_PAPER_ORCHESTRATOR_READY` |
| Blocked (P16.6) | `P20_BLOCKED_P16_6_NOT_READY` |
| Blocked (P19) | `P20_BLOCKED_P19_NOT_READY` |
| Blocked (P17 replay) | `P20_BLOCKED_P17_REPLAY_NOT_READY` |
| Blocked (contract) | `P20_BLOCKED_CONTRACT_VIOLATION` |
| Fatal (missing input) | `P20_FAIL_INPUT_MISSING` |
| Fatal (non-deterministic) | `P20_FAIL_NON_DETERMINISTIC` |

---

## 4. Real Run Results (2026-05-12)

```
Gate:                      P20_DAILY_PAPER_ORCHESTRATOR_READY
n_active_paper_entries:    324
n_settled_win:             171
n_settled_loss:            153
n_unsettled:               0
roi_units:                 0.107783  (+10.78%)
hit_rate:                  0.527778  (52.78%)
settlement_join_method:    JOIN_BY_GAME_ID
game_id_coverage:          1.0000  (100%)
paper_only:                true
production_ready:          false
```

### Upstream Gate Sources

| Phase | Gate |
|-------|------|
| P16.6 | `P16_6_PAPER_RECOMMENDATION_GATE_READY` |
| P19   | `P19_IDENTITY_JOIN_REPAIR_READY` |
| P17 Replay | `P17_PAPER_LEDGER_READY` |

### Output Artifacts

```
outputs/predictions/PAPER/2026-05-12/p20_daily_paper_orchestrator/
├── daily_paper_summary.json    ← full metrics
├── daily_paper_summary.md      ← human-readable summary
├── artifact_manifest.json      ← SHA-256 manifest of all 12 artifacts
└── p20_gate_result.json        ← gate decision
```

---

## 5. Determinism Verification

| Check | Result |
|-------|--------|
| Gate fields identical (excl `generated_at`) | ✅ DETERMINISTIC — DIFFS: NONE |
| `run1` `p20_gate_result.json` SHA-256 | `489ec21e...` |
| `run2` `p20_gate_result.json` SHA-256 | gate fields identical |

Note: `daily_paper_summary.json` SHA-256 differs between runs because it embeds `generated_at` timestamp. All business logic fields are identical.

---

## 6. Test Suite

| File | Tests | Status |
|------|-------|--------|
| `tests/test_p20_daily_paper_orchestrator_contract.py` | 14 | ✅ PASS |
| `tests/test_p20_artifact_manifest.py` | 15 | ✅ PASS |
| `tests/test_p20_daily_summary_aggregator.py` | 21 | ✅ PASS |
| `tests/test_run_p20_daily_paper_mlb_orchestrator.py` | 7 | ✅ PASS |
| **Total** | **56/56** | ✅ |

All CLI tests use `PYTHONPATH=str(REPO_ROOT)` + `cwd=str(REPO_ROOT)` in subprocess.

---

## 7. Contract Invariants

- `paper_only = True` enforced at every layer
- `production_ready = False` enforced at every layer
- `n_unsettled = 0` required for `READY` gate
- All 3 upstream gate strings must match exactly
- `--paper-only false` triggers exit code 2

---

## 8. Artifact Manifest

The manifest covers 12 artifacts across 4 phases with SHA-256 hashes:
- P16.6: `recommendation_rows.csv`, `recommendation_summary.json`
- P19: `enriched_simulation_ledger.csv`, `identity_enrichment_summary.json`, `p19_gate_result.json`
- P17 replay: `paper_recommendation_ledger.csv`, `paper_recommendation_ledger_summary.json`, `ledger_gate_result.json`
- P20: `daily_paper_summary.json`, `daily_paper_summary.md`, `artifact_manifest.json`, `p20_gate_result.json`

---

## 9. CLI Reference

```bash
PYTHONPATH=. .venv/bin/python scripts/run_p20_daily_paper_mlb_orchestrator.py \
  --run-date 2026-05-12 \
  --p16-6-dir outputs/predictions/PAPER/2026-05-12/p16_6_recommendation_gate_p18_policy \
  --p19-dir outputs/predictions/PAPER/2026-05-12/p19_odds_identity_join_repair \
  --p17-replay-dir outputs/predictions/PAPER/2026-05-12/p17_replay_with_p19_identity \
  --output-dir outputs/predictions/PAPER/2026-05-12/p20_daily_paper_orchestrator \
  --paper-only true
```

Exit codes: `0` = READY, `1` = BLOCKED, `2` = FATAL

---

## Terminal Marker

`P20_DAILY_PAPER_MLB_ORCHESTRATOR_READY`
