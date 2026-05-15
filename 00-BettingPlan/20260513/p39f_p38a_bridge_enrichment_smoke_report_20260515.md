# P39F — P38A Bridge Enrichment Smoke Report
**Date**: 2026-05-15
**Marker**: `P39F_P38A_BRIDGE_ENRICHMENT_SMOKE_PASS_20260515`
**Status**: PASS

---

## Command

```bash
PYTHONPATH=. .venv/bin/python scripts/enrich_p38a_with_identity_bridge.py \
  --p38a-path outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv \
  --bridge-path data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv \
  --out-file data/pybaseball/local_only/p39f_p38a_oof_with_identity_bridge.csv \
  --execute
```

---

## Results

| Metric | Value |
|--------|-------|
| Script version | `p39f_p38a_bridge_enrichment_v1` |
| PAPER_ONLY | True |
| P38A rows | 2,187 |
| Bridge rows | 2,429 |
| **Bridge match: MATCHED** | **2187 / 2187 = 100.0%** |
| Unmatched rows | 0 |
| Missing away_team | 0 |
| Odds columns found | NONE |
| Output rows | 2,187 |
| Deterministic hash | `82540eba8d8933ec` |

---

## Output Schema

```
game_id, fold_id, p_oof, model_version, source_prediction_ref,
generated_without_y_true, game_date, home_team, away_team, bridge_match_status
```

Added by enrichment: `game_date`, `home_team`, `away_team`, `bridge_match_status`

**p_oof values unchanged** — p_oof integrity hash verified in-script.

---

## Output File

`data/pybaseball/local_only/p39f_p38a_oof_with_identity_bridge.csv`

- **gitignored** (under `data/pybaseball/local_only/`)
- Not committed

---

## Key Insight

The bridge provides complete `away_team` recovery for all 2,187 P38A OOF rows. Both `home_team` and `away_team` are returned in Retrosheet codes (CHA, KCA, TBA, etc.) and must be normalized to Statcast canonical before joining with P39B rolling features.

---

## Status

`P39F_P38A_BRIDGE_ENRICHMENT_SMOKE_PASS_20260515`

PAPER_ONLY=True | pybaseball ≠ odds source
