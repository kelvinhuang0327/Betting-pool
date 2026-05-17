# P39E — Execution Scope Decision
**Date**: 2026-05-15
**Marker**: `P39E_EXECUTION_SCOPE_DECISION_20260515_READY`
**Status**: EXPANDED_APRIL_SAMPLE_FIRST

---

## Decision: EXPANDED_APRIL_SAMPLE_FIRST

### Rationale

Root cause analysis from P39D revealed two blockers for the join:

| Blocker | Detail | Fix |
|---------|--------|-----|
| **Date gap (PRIMARY)** | P39D rolling features covered Apr 1–10 only. P38A April OOF games start Apr 15. Zero date overlap → 0% match rate. | Expand Statcast fetch to Apr 8–30 |
| **Team code mismatch (SECONDARY)** | P38A uses Retrosheet codes (CHA, TBA, ARI, OAK…). Statcast uses different canonical codes (CWS, TB, AZ, ATH…). | Build normalization map + pre-join normalization |

Full-season fetch (2024-03-20 → 2024-10-01) is **deferred** until the April sample join achieves ≥80% in-scope home match rate. This avoids expensive full-season pybaseball fetches (~150K+ rows) against a broken join.

---

## Execution Parameters

### Phase 1 — April Sample (THIS RUN)

| Parameter | Value |
|-----------|-------|
| Date range | 2024-04-08 → 2024-04-30 |
| Reason for start | 7-day window requires Apr 8 lookback to cover Apr 15 games |
| Reason for end | P38A April coverage ends ~Apr 30 |
| Window days | 7 |
| Expected P38A rows in range | ~210 (Apr 15–30 subset) |
| Expected Statcast rows | ~150,000+ |
| Expected team-daily rows | ~690 (30 teams × 23 dates) |
| Expected rolling feature rows | ~690 |
| Leakage guard | feature_window_end < as_of_date (strict D-1) |
| Output path | data/pybaseball/local_only/p39e_rolling_features_2024_04_08_04_30.csv |

### Phase 2 — Full-Season (DEFERRED, post Phase 1 PASS)

| Parameter | Value |
|-----------|-------|
| Date range | 2024-03-20 → 2024-10-01 |
| Strategy | Chunked fetch: 14-day windows |
| Chunks | ~24 chunks × ~20,000 rows each |
| Total estimated rows | ~500,000 |
| Trigger condition | Phase 1 in-scope home match rate ≥80% |

---

## Success Criteria

| Criterion | Pass Threshold | Status |
|-----------|---------------|--------|
| Rolling features generated | leakage_violations=0, odds_columns=0 | TBD |
| Team code normalization | All MLB aliases map to canonical codes | TBD |
| In-scope home match rate | ≥80% (Apr 15–30 subset of P38A) | TBD |
| Overall home match rate | Expected ~10% (April features vs full 2,187-row P38A) | TBD |
| Away match rate | 0% expected (P38A CSV has no away_team column) | TBD |
| Regression tests | 32+ PASS | TBD |

### Note on Away Match Rate

The real P38A CSV schema (`game_id, fold_id, p_oof, model_version, source_prediction_ref, generated_without_y_true`) does **not** include `away_team`. The `_enrich_p38a_with_game_meta()` function only extracts `home_team` from the `game_id` prefix. Therefore:
- Away match rate = 0% (no away_team column to join on)
- This is a schema limitation, not a data quality failure
- Full bidirectional enrichment requires a game schedule lookup that maps game_id → away_team

---

## Mode Decision

```
MODE = EXPANDED_APRIL_SAMPLE_FIRST
FULL_SEASON = DEFERRED
PAPER_ONLY = True
```

---

## Marker

`P39E_EXECUTION_SCOPE_DECISION_20260515_READY`
