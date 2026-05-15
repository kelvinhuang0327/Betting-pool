# P39E — Enrichment Certification & Full-Season Plan
**Date**: 2026-05-15
**Marker**: `P39E_ENRICHMENT_CERTIFICATION_READY_20260515`
**Classification**: `P39E_ENRICHMENT_PARTIAL`

---

## Certification Summary

| Track | Description | Result |
|-------|-------------|--------|
| TRACK 0 | Preflight / Repo Ground Truth | ✅ PASS |
| TRACK 1 | P39E Scope Decision | ✅ PASS — EXPANDED_APRIL_SAMPLE_FIRST |
| TRACK 2 | Team code normalization module | ✅ PASS — 31 tests |
| TRACK 3 | Join utility + normalization flag | ✅ PASS — 19 tests (12 P39C + 7 new) |
| TRACK 4 | Expanded April feature generation | ✅ PASS — 90,696 rows, 690 features, 0 leakage |
| TRACK 5 | P38A OOF enrichment | ✅ PARTIAL — 100% in-scope, 9.6% overall |
| TRACK 6 | Regression tests | ✅ PASS — 70 / 70 |
| TRACK 7 | Certification (this doc) | ✅ |
| TRACK 8 | Push gate | 🔒 NOT AUTHORIZED |
| TRACK 9 | Validation (all markers) | ✅ See below |

---

## Artifact Inventory

| Artifact | Type | Status |
|----------|------|--------|
| `scripts/team_code_normalization.py` | New module | ✅ COMMITTED |
| `tests/test_team_code_normalization.py` | New tests (31) | ✅ COMMITTED |
| `scripts/join_p38a_oof_with_p39b_features.py` | Modified | ✅ COMMITTED |
| `tests/test_p39c_feature_join_contract.py` | Extended (+7 tests) | ✅ COMMITTED |
| `00-BettingPlan/20260513/p39e_execution_scope_decision_20260515.md` | Plan doc | ✅ COMMITTED |
| `00-BettingPlan/20260513/p39e_expanded_april_feature_generation_report_20260515.md` | Report | ✅ COMMITTED |
| `00-BettingPlan/20260513/p39e_p38a_oof_enrichment_report_20260515.md` | Report | ✅ COMMITTED |
| `data/pybaseball/local_only/p39e_rolling_features_2024_04_08_04_30.csv` | Raw Statcast | ❌ NOT COMMITTED (gitignored) |
| `data/pybaseball/local_only/p39e_enriched_p38a_april_sample.csv` | Enriched CSV | ❌ NOT COMMITTED (gitignored) |

---

## P39E Markers Confirmed

| Marker | Location | Status |
|--------|----------|--------|
| `P39E_EXECUTION_SCOPE_DECISION_20260515_READY` | p39e_execution_scope_decision_20260515.md | ✅ |
| `P39E_TEAM_CODE_NORMALIZATION_READY_20260515` | scripts/team_code_normalization.py | ✅ |
| `P39E_EXPANDED_APRIL_FEATURE_GENERATION_PASS_20260515` | p39e_expanded_april_feature_generation_report_20260515.md | ✅ |
| `P39E_P38A_OOF_ENRICHMENT_PARTIAL_20260515` | p39e_p38a_oof_enrichment_report_20260515.md | ✅ |
| `P39E_JOIN_UTILITY_TEAM_NORMALIZATION_READY_20260515` | scripts/join_p38a_oof_with_p39b_features.py | ✅ |
| `P39E_REGRESSION_PASS_20260515` | 70/70 tests | ✅ |
| `P39E_PUSH_NOT_AUTHORIZED_20260515` | This doc | ✅ |
| `P39E_ENRICHMENT_CERTIFICATION_READY_20260515` | This doc | ✅ |

---

## Inherited Markers (P39A–D, confirmed present)

| Marker | Status |
|--------|--------|
| `P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515` | ✅ Confirmed in 58a05d1 |
| `P39B_ROLLING_FEATURE_CORE_READY_20260515` | ✅ Confirmed in 58a05d1 |
| `P39C_JOIN_UTILITY_READY_20260515` | ✅ Confirmed (still present in join utility) |
| `P39C_FEATURE_JOIN_TESTS_PASS_20260515` | ✅ 12/12 tests still pass |
| `P39D_REAL_FEATURE_OUTPUT_RUNTIME_READY_20260515` | ✅ Confirmed in 58a05d1 |

---

## Full-Season Chunked Fetch Plan (Phase 2 — DEFERRED)

### Prerequisites (before executing)
1. Explicit authorization from CTO
2. Stable network environment (pybaseball fetches from Baseball Savant)
3. At least 2 GB free disk for cache

### Execution Strategy

```
Total date range: 2024-03-20 → 2024-10-01 (~196 days)
Chunk size: 14 days
Number of chunks: ~14 chunks
```

| Chunk | Start | End | Expected rows |
|-------|-------|-----|---------------|
| 1 | 2024-03-20 | 2024-04-02 | ~40,000 |
| 2 | 2024-04-03 | 2024-04-16 | ~50,000 |
| 3 | 2024-04-17 | 2024-04-30 | ~55,000 |
| 4 | 2024-05-01 | 2024-05-14 | ~60,000 |
| … | … | … | … |
| 14 | 2024-09-18 | 2024-10-01 | ~50,000 |
| **Total** | | | **~700,000** |

### Command Template (per chunk)

```bash
PYTHONPATH=. .venv/bin/python scripts/build_pybaseball_pregame_features_2024.py \
  --execute \
  --start-date {CHUNK_START} \
  --end-date {CHUNK_END} \
  --window-days 7 \
  --out-file data/pybaseball/local_only/p39e_chunk_{N}_features.csv \
  --cache-dir data/pybaseball/local_only/cache
```

### Merge Strategy

After all chunks complete:
1. Concatenate all chunk CSVs into `p39e_fullseason_rolling_features_2024.csv`
2. De-duplicate on `(as_of_date, team)` 
3. Run leakage validation on merged file
4. Re-run join: full P38A (2,187 rows) × full-season features (~5,400 rows)
5. Expected overall home match rate: ~95%+

### Expected Outcomes (Full-Season)

| Metric | Expected |
|--------|---------|
| Total Statcast rows | ~700,000 |
| Rolling feature rows | ~5,400 (30 teams × 180 dates) |
| Overall home match rate | ~95%+ |
| Away match rate | 0% until away_team schema fix |
| Brier improvement | Measurable (delta vs P38A baseline 0.2487) |

---

## Brier Improvement Measurement Plan

Once full-season enrichment is complete:
1. Train variant of P38A model with rolling features as additional input
2. Compare OOF Brier score: baseline (0.2487) vs enriched model
3. Report absolute and relative improvement
4. Acceptance threshold: Δ Brier ≥ 0.005 (0.5 pp improvement)

**IMPORTANT**: pybaseball ≠ odds source. Rolling features (launch speed, hard hit rate, barrel rate) are baseball statistics only. CLV / EV / Kelly sizing still require a separate licensed odds feed.

---

## Push Gate

`P39E_PUSH_NOT_AUTHORIZED_20260515`

Push to `origin/p13-clean` is **NOT AUTHORIZED** in this session. Explicit "YES" required from CTO before any remote push.

---

## Classification

```
P39E_ENRICHMENT_PARTIAL
- In-scope April: PASS (100% home match)
- Full-season: DEFERRED (Phase 2 pending)
- Away team: BLOCKED (schema limitation)
```

---

## Marker

`P39E_ENRICHMENT_CERTIFICATION_READY_20260515`
