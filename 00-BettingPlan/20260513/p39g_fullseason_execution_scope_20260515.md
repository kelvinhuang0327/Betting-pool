# P39G Full-Season Execution Scope
**Date**: 2026-05-15
**Author**: P39G Full-Season Statcast Rolling Feature Agent
**Prev round**: P39F (d14b17c) — away_team recovery 100% CERTIFIED

---

## Selected Mode

**FULL_SEASON_CHUNKED_EXECUTION**

Full 2024 MLB regular season Statcast data fetched in 14-day chunks,
assembled into a single rolling feature table, then joined with
bridge-enriched P38A OOF predictions.

---

## Date Range

| Parameter | Value | Reason |
|-----------|-------|--------|
| start_date | 2024-03-20 | Pre-season start (7-day rolling lookback for Apr 01 games) |
| end_date | 2024-10-01 | End of 2024 regular season |
| n_days | ~196 | Covers all 2024 P38A OOF game dates |
| chunk_size | 14 days | Balanced: avoids single large Statcast call (~30K rows/chunk) |
| n_chunks | ~14 | 196 / 14 = 14 chunks |

**Why 2024-03-20 start**: P38A earliest game is near April 01. Rolling
7-day window needs data from 2024-03-25 minimum (game_date - 7).
2024-03-20 provides safe pre-season lookback margin.

**Why 14-day chunks**: pybaseball `statcast()` is stable for date ranges
≤30 days. A 14-day chunk averages ~20,000–40,000 pitch-level rows, well
within safe API limits. Resume manifest tracks per-chunk status for
reliable retry.

---

## Chunked Resume Manifest Design

Location: `data/pybaseball/local_only/p39g_statcast_manifest_2024.json` (NOT committed)

Per-chunk entry:
```json
{
  "chunk_id": 0,
  "start_date": "2024-03-20",
  "end_date": "2024-04-02",
  "status": "SUCCESS | FAILED | PENDING",
  "rows": 23451,
  "error": null,
  "hash": "abc123...",
  "fetched_at": "2026-05-15T10:00:00Z"
}
```

Resume policy:
- Only PENDING or FAILED chunks are re-fetched on resume
- SUCCESS chunks are loaded from local CSV cache
- No duplicate rows: dedup by `(game_date, game_pk, batter)` before aggregation

---

## Expected Outputs (All local-only, NOT committed)

| Output | Path | Committed? |
|--------|------|------------|
| Raw chunk CSVs | `data/pybaseball/local_only/cache/chunk_*.csv` | NO |
| Chunk manifest JSON | `data/pybaseball/local_only/p39g_statcast_manifest_2024.json` | NO |
| Full-season rolling features | `data/pybaseball/local_only/p39g_rolling_features_2024_fullseason.csv` | NO |
| Bridge-enriched P38A OOF | `data/pybaseball/local_only/p39g_p38a_oof_with_identity_bridge.csv` | NO |
| Full enriched P38A OOF | `data/pybaseball/local_only/p39g_enriched_p38a_oof_fullseason.csv` | NO |
| Summary JSON (metadata only) | `data/pybaseball/local_only/p39g_rolling_features_2024_fullseason.summary.json` | NO |

Gitignore boundary: `data/pybaseball/local_only/` is already gitignored.

---

## Success Criteria

| Criterion | Threshold | Priority |
|-----------|-----------|----------|
| Full rolling feature generation | PASS | Required |
| P38A complete home+away match rate | ≥80% | Required |
| Ideal P38A match rate | ≥90% | Preferred |
| Leakage violations | 0 | Required |
| Odds columns in output | 0 | Required |
| Unknown team codes | 0 | Required |
| Duplicate rows in aggregated output | 0 | Required |

---

## Retry / Resume Policy

1. Manifest written after EACH chunk completes (success or fail)
2. On resume: read manifest, skip SUCCESS chunks, re-fetch FAILED/PENDING
3. Partial manifest allowed: first run may produce 10/14 chunks PASS
4. Final assembly only runs when all chunks SUCCESS
5. Failed chunk → status=FAILED, error field populated
6. `--force-refresh` flag clears all chunk status → full re-fetch

---

## Key Constraints

- PAPER_ONLY = True
- pybaseball ≠ odds source
- No odds columns in any output
- No look-ahead leakage (window_end = game_date - 1)
- All raw Statcast / generated features / enriched CSVs → local_only
- No commit of any CSV / manifest / raw data
- Bridge team codes are Retrosheet → `--normalize-team-codes` handles mapping
- No production edge claim
- No CLV without odds source

---

## P39G Task Sequence

```
TRACK 0  Preflight
TRACK 1  Execution Scope (this doc)
TRACK 2  Enhance runtime: --chunk-days, --resume-manifest, --force-refresh
TRACK 3  Full-season feature generation (14-day chunks)
TRACK 4  Full P38A bridge enrichment (P39F utility, all 2187 rows)
TRACK 5  Full P38A OOF feature join (home+away features, target ≥80%)
TRACK 6  Regression (86+ tests PASS)
TRACK 7  Enriched feature quality check
TRACK 8  Certification + P39H modeling plan
TRACK 9  Push gate (no push without explicit YES)
TRACK 10 Validation / marker check
TRACK 11 Optional commit (scripts + docs only)
TRACK 12 Final handoff report
```

---

## P39H Preview (Research-Only)

After P39G enrichment certified:
- Compare P38A baseline Brier vs enriched-feature model
- Time-aware train/test split only (no future-bleed)
- No production edge claim
- No odds / CLV unless licensed odds source is integrated
- Baseline P38A Brier: 0.2487

---

## Acceptance Marker

**P39G_FULLSEASON_EXECUTION_SCOPE_READY_20260515**
