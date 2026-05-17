# P39D — P38A OOF Enrichment Smoke Report
**Date**: 2026-05-15  
**Branch**: p13-clean  
**Script**: `scripts/join_p38a_oof_with_p39b_features.py` (SCRIPT_VERSION=p39c_feature_join_v1)  
**PAPER_ONLY**: True

---

## Execution Parameters

| Parameter | Value |
|-----------|-------|
| p38a_path | `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv` |
| p39b_path | `data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv` |
| out_file | `data/pybaseball/local_only/p39d_enriched_p38a_sample_2024_04_01_04_10.csv` |
| Mode | `--execute` |

---

## Command

```bash
.venv/bin/python scripts/join_p38a_oof_with_p39b_features.py \
  --p38a-path outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv \
  --p39b-path data/pybaseball/local_only/p39d_rolling_features_2024_04_01_04_10.csv \
  --out-file data/pybaseball/local_only/p39d_enriched_p38a_sample_2024_04_01_04_10.csv \
  --execute
```

---

## Result: DEFERRED (Pipeline OK, Match Rate 0% — Expected)

The join utility executed without exceptions. Output CSV was written. All safety boundaries were enforced. However, the match rate was **0%** for both home and away teams.

### Join Metrics

| Metric | Value |
|--------|-------|
| P38A OOF rows | 2,187 |
| P39D rolling feature rows | 300 |
| Joined rows | 2,187 (all P38A rows preserved) |
| Home feature match rate | **0.0%** |
| Away feature match rate | **0.0%** |
| Leakage violations | 0 |
| Odds boundary | CONFIRMED |
| Output CSV written | ✅ |

---

## Root Cause Analysis: 0% Match Rate

### Cause 1 — Date Range Mismatch (PRIMARY)

The rolling features cover **2024-04-01 → 2024-04-10**.

However, the earliest P38A game_ids in April 2024 start from **2024-04-15**:
```
BAL-20240415-0
CHA-20240415-0
DET-20240415-0
HOU-20240415-0
OAK-20240415-0
...
```

There is **zero date overlap** between the rolling feature range and any P38A game date in April 2024. This alone accounts for 100% of the 0% match rate.

### Cause 2 — Team Code Normalization Gap (SECONDARY)

Even if dates did overlap, several team codes used in P38A game_ids (Retrosheet-style) differ from pybaseball/Statcast codes:

| Retrosheet (P38A) | Statcast (P39D) | Team |
|-------------------|-----------------|------|
| `CHA` | `CWS` | Chicago White Sox |
| `OAK` | `ATH` | Athletics |
| `TBA` | `TB` | Tampa Bay Rays |
| `ARI` | `AZ` | Arizona Diamondbacks |
| `SDN` | `SD` | San Diego Padres |

Teams with matching codes: BAL, BOS, SEA, PHI, HOU, DET, etc.

---

## Assessment

This is NOT a pipeline bug. The join utility functioned correctly. The 0% match is a documented, expected consequence of:
1. **April 1-10 rolling features cannot enrich April 15+ P38A games** (date gap)
2. **Team code normalization is not yet implemented** (P39E scope)

The enrichment is **deferred to P39E**, which will:
- Expand rolling features to the full 2024 season (`2024-03-20` → `2024-10-01`)
- Implement team code normalization map
- Re-run the join with overlapping dates and matching codes
- Target: ≥ 80% home match rate, ≥ 80% away match rate

---

## Output File

`data/pybaseball/local_only/p39d_enriched_p38a_sample_2024_04_01_04_10.csv`  
— In gitignored directory, **NOT committed**  
— Contains all 2,187 P38A rows with NaN rolling feature columns (no matches)

---

## Marker

**P39D_P38A_OOF_ENRICHMENT_SMOKE_DEFERRED_20260515**
