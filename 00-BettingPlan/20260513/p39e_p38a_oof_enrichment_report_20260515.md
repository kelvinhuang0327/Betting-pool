# P39E — P38A OOF Enrichment Report
**Date**: 2026-05-15
**Marker**: `P39E_P38A_OOF_ENRICHMENT_PARTIAL_20260515`
**Status**: PARTIAL

---

## Execution Summary

| Parameter | Value |
|-----------|-------|
| Script | `scripts/join_p38a_oof_with_p39b_features.py` |
| Script version | `p39c_feature_join_v1` |
| P38A path | `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv` |
| P39B path | `data/pybaseball/local_only/p39e_rolling_features_2024_04_08_04_30.csv` |
| Output path | `data/pybaseball/local_only/p39e_enriched_p38a_april_sample.csv` |
| Team code normalization | ENABLED (`--normalize-team-codes`) |
| Mode | `--execute` |

---

## Join Results

| Metric | Value | Status |
|--------|-------|--------|
| Total P38A rows | 2,187 | — |
| P39B feature rows | 690 | — |
| Joined output rows | 2,187 (left join) | ✅ |
| **Overall home match count** | **210** | — |
| **Overall home match rate** | **9.6%** | PARTIAL |
| **In-scope April home match rate** | **210 / 210 = 100.0%** | ✅ PASS |
| Away match count | 0 | — |
| Away match rate | 0.0% | See note |
| April unmatched home games | 0 | ✅ |
| Leakage violations | 0 | ✅ |
| Odds boundary | CONFIRMED | ✅ |
| Unknown team codes | 0 | ✅ |
| Deterministic hash | `9f0ad16d6b8e87f3` | — |

---

## Team Code Normalization Applied

All Retrosheet codes in P38A game_id prefixes were successfully mapped to Statcast canonical:

| Retrosheet (in game_id) | Normalized to | Example game_id |
|------------------------|---------------|-----------------|
| CHA | CWS | CHA-20240415-0 |
| OAK | ATH | OAK-20240415-0 |
| TBA | TB | TBA-20240415-0 |
| ARI | AZ | ARI-20240416-0 |

All other codes (BAL, BOS, DET, HOU, etc.) were already Statcast-canonical and passed through as identity.

**Unknown codes detected**: 0  
**Normalization status**: OK

---

## April Teams Matched (All 30 Canonical Teams)

```
ATH, ATL, AZ, BAL, BOS, CHC, CIN, CLE, COL, CWS,
DET, HOU, KC, LAA, LAD, MIA, MIL, MIN, NYM, NYY,
PHI, PIT, SD, SEA, SF, STL, TB, TEX, TOR, WSH
```

---

## Why PARTIAL (Not PASS)

The PASS criterion is "home+away complete match rate ≥80%". The overall rate is 9.6% because:

### Cause 1 — Date coverage (primary)
- P38A full-season data: Apr 15 – Sep 30, 2024 (2,187 games total)
- P39E features generated: Apr 8–30, 2024 (690 feature rows for 23 dates)
- Date coverage: April only (23 out of ~180 regular-season dates)
- Unmatched rows: 1,977 / 2,187 (May–Sep games have no features yet)

### Cause 2 — Away match rate 0% (schema limitation)
- P38A CSV schema: `game_id, fold_id, p_oof, model_version, source_prediction_ref, generated_without_y_true`
- No `away_team` column in P38A CSV
- `_enrich_p38a_with_game_meta()` extracts `home_team` from game_id prefix only
- Away join is silently skipped (`if "away_team" in joined.columns:` is False)
- Fix: Add a schedule lookup (e.g., Retrosheet game logs) to map game_id → away_team

---

## PARTIAL Classification

| Category | Result |
|----------|--------|
| In-scope April home match rate | **100%** — all 210 April P38A games matched |
| Away match rate | **0%** — P38A has no away_team column (schema limitation) |
| Overall home match rate | **9.6%** — expected, April features only |
| Team code normalization | **PASS** — all codes resolved, no unknowns |
| Leakage | **PASS** — 0 violations |
| Odds boundary | **PASS** — CONFIRMED |

**Classification**: PARTIAL — in-scope date enrichment succeeds; full-season features not yet generated.

---

## Next Steps for Full PASS

1. **Full-season Statcast fetch** (P39E Phase 2):
   - Date range: 2024-03-20 → 2024-10-01
   - Strategy: 14-day chunks (~24 chunks)
   - Expected: ~500,000 Statcast rows → ~5,400 rolling feature rows (30 teams × 180 dates)
   - Trigger: explicit authorization for long-running fetch

2. **Away team lookup** (optional):
   - Ingest Retrosheet game logs to map game_id → away_team
   - Re-run join with both home + away enrichment
   - Expected away match rate: ~100% after full-season features + normalization

---

## Data Isolation Status

- Enriched CSV written to `data/pybaseball/local_only/` — gitignored
- **NOT committed** to repo
- PAPER_ONLY = True

---

## Marker

`P39E_P38A_OOF_ENRICHMENT_PARTIAL_20260515`
