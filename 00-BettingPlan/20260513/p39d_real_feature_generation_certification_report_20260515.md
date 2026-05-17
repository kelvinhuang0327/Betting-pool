# P39D — Real Feature Generation Certification Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Author**: CTO Agent  
**PAPER_ONLY**: True — Research only. No production write, no live betting.

---

## Summary

P39D successfully demonstrated real Statcast rolling feature generation using pybaseball. The core pipeline (fetch → aggregate → roll → write) operates correctly with real Baseball Savant data. A minor script bug discovered during TRACK 2 review was immediately fixed. All regression tests pass. The P38A enrichment is deferred pending full-season expansion and team code normalization (P39E).

---

## Execution Scope

**Mode selected**: APRIL_SAMPLE_EXECUTION  
**Date range**: 2024-04-01 → 2024-04-10  
**Window days**: 7 (strict D-1 pregame-safe)

Full documentation: [p39d_execution_scope_decision_20260515.md](p39d_execution_scope_decision_20260515.md)

---

## Track-by-Track Results

### TRACK 0 — Preflight ✅
- Branch: `p13-clean`, HEAD: `9be3823`
- 10 local commits ahead of `origin/p13-clean`
- P39C artifacts: all 6 present, all 5 markers confirmed
- RAW_AND_SECRET_NOT_VISIBLE confirmed
- pybaseball 2.2.7 installed, both scripts CLI-complete

### TRACK 1 — Execution Scope Decision ✅
- Created: `00-BettingPlan/20260513/p39d_execution_scope_decision_20260515.md`
- Marker: `P39D_EXECUTION_SCOPE_DECISION_20260515_READY`

### TRACK 2 — Runtime Script Enhancement ✅
- Script: `scripts/build_pybaseball_pregame_features_2024.py`
- Change: Added `P39D_REAL_FEATURE_OUTPUT_RUNTIME_READY_20260515` marker to both summary-only and execute mode print paths
- **Bug fixed**: `sys.exit(0)` was missing from summary-only block due to incorrect indentation from prior edit; fixed immediately
- Script now exits cleanly in summary-only mode and runs real execute correctly
- Marker: `P39D_REAL_FEATURE_OUTPUT_RUNTIME_READY_20260515`

### TRACK 3 — Real Pybaseball Execute Smoke ✅ PASS
- Real Baseball Savant data fetched via pybaseball
- 38,331 raw Statcast rows (April 1-10, 2024)
- 258 team-daily aggregate rows
- 300 rolling feature rows (30 teams × 10 dates)
- 300/300 pregame-safe (leakage violations = 0)
- Odds boundary: CONFIRMED
- CSV written to `data/pybaseball/local_only/` (gitignored, not committed)
- Marker: `P39D_REAL_PYBASEBALL_EXECUTE_SMOKE_PASS_20260515`

Full report: [p39d_real_pybaseball_execute_smoke_report_20260515.md](p39d_real_pybaseball_execute_smoke_report_20260515.md)

### TRACK 4 — P38A OOF Enrichment Smoke ⚠️ DEFERRED
- Join utility executed without exception
- Output CSV written to `data/pybaseball/local_only/` (gitignored, not committed)
- Match rate: 0% (expected — see root cause)
- **Root Cause 1 (PRIMARY)**: Rolling features cover Apr 1-10; P38A April games start Apr 15+. Zero date overlap.
- **Root Cause 2 (SECONDARY)**: Team code normalization gap (CHA≠CWS, OAK/ATH, TBA≠TB, ARI≠AZ)
- Leakage violations: 0 | Odds boundary: CONFIRMED
- Enrichment deferred to P39E (full season + normalization)
- Marker: `P39D_P38A_OOF_ENRICHMENT_SMOKE_DEFERRED_20260515`

Full report: [p39d_p38a_oof_enrichment_smoke_report_20260515.md](p39d_p38a_oof_enrichment_smoke_report_20260515.md)

### TRACK 5 — Regression Tests ✅ 32/32 PASS
```
tests/test_p39b_pybaseball_leakage_policy.py     11/11 PASS
tests/test_p39b_pybaseball_feature_aggregation.py 9/9  PASS
tests/test_p39c_feature_join_contract.py          12/12 PASS
──────────────────────────────────────────────────────────
TOTAL                                             32/32 PASS (1.16s)
```
Marker: `P39D_P39B_P39C_REGRESSION_PASS_20260515`

---

## Script Change Summary

### `scripts/build_pybaseball_pregame_features_2024.py`

| Change | Justification |
|--------|---------------|
| Added `P39D_REAL_FEATURE_OUTPUT_RUNTIME_READY_20260515` marker to summary-only print path | TRACK 2 acceptance marker |
| Added `P39D_REAL_FEATURE_OUTPUT_RUNTIME_READY_20260515` marker to execute-mode print path | TRACK 2 acceptance marker |
| Fixed `sys.exit(0)` placement (indentation bug) in summary-only block | Bugfix — summary-only was falling through to execute mode |

**No other files were modified.**  
**SCRIPT_VERSION remains `p39b_pybaseball_rolling_v1`** — no semantic version bump required for marker/bugfix changes.

---

## Local-Only Artifacts (NOT Committed)

| File | Description |
|------|-------------|
| `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv` | 300 rolling feature rows |
| `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.summary.json` | Summary metadata |
| `data/pybaseball/local_only/p39d_enriched_p38a_sample_2024_04_01_04_10.csv` | P38A + features (0% match) |
| `data/pybaseball/local_only/cache/` | pybaseball Statcast cache |

All in `data/pybaseball/local_only/` — gitignored at `.gitignore` line 86.  
**Raw Statcast data not committed. Confirmed.**

---

## Boundaries

| Boundary | Status |
|----------|--------|
| PAPER_ONLY=True | ✅ CONFIRMED (all artifacts) |
| No odds columns in any output | ✅ CONFIRMED |
| No look-ahead leakage | ✅ CONFIRMED (300/300 pregame-safe, 0 leakage violations) |
| pybaseball ≠ odds source | ✅ CONFIRMED (baseball statistics only) |
| CLV / EV / Kelly | ⚠️ NOT COMPUTED — requires separate licensed odds API |
| Raw data not committed | ✅ CONFIRMED |

---

## Known Limitations

1. **Team code normalization gap**: Retrosheet codes in P38A (CHA, TBA, OAK/ATH, ARI) differ from Statcast codes (CWS, TB, ATH, AZ). Must be resolved in P39E.
2. **Date range mismatch**: April 1-10 rolling features do not overlap with P38A April 15+ games. Full season expansion required.
3. **Early-season window gap**: Apr 1-7 rolling features have `sample_size=0` (no prior-week data at season start). This is correct behavior.
4. **No full-season CLV enrichment**: P39E will need to expand to full 2024 season (March 20 → October 1) to enable meaningful Brier improvement measurement.

---

## Next Step: P39E

| P39E Scope Item | Priority |
|-----------------|----------|
| Implement chunked monthly Statcast fetch (30-day chunks) | HIGH |
| Full 2024 season rolling features (Mar 20 → Oct 1) | HIGH |
| Team code normalization map (Retrosheet → Statcast) | HIGH |
| Re-run P38A OOF enrichment with overlapping dates | HIGH |
| Target: ≥ 80% home match rate, ≥ 80% away match rate | HIGH |
| Measure Brier improvement vs P38A baseline (0.2487) | MEDIUM |

---

## Push Gate

**NOT AUTHORIZED** — No explicit YES given by user.  
Current state: 11 local commits ahead of `origin/p13-clean` (10 P39C + 1 P39D script change).  
Push requires explicit user confirmation.

Marker: `P39D_PUSH_NOT_AUTHORIZED_20260515`

---

## Acceptance Marker

**P39D_REAL_FEATURE_GENERATION_CERTIFICATION_READY_20260515**
