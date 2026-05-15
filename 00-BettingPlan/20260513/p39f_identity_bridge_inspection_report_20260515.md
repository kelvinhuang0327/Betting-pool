# P39F — Identity Bridge Inspection Report
**Date**: 2026-05-15
**Marker**: `P39F_IDENTITY_BRIDGE_INSPECTION_READY_20260515`
**Status**: PASS — Bridge is valid and joinable

---

## Bridge File

| Parameter | Value |
|-----------|-------|
| Path | `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv` |
| File size | 168 KB |
| Source | Retrosheet game log |

---

## Schema

| Column | Type | Nulls | Notes |
|--------|------|-------|-------|
| `game_id` | str | 0 | Retrosheet format: `{HOME}-{YYYYMMDD}-{N}` |
| `game_date` | str (YYYY-MM-DD) | 0 | |
| `season` | int | 0 | All 2024 |
| `away_team` | str | **0** | Retrosheet code (CHA, KCA, LAN, etc.) |
| `home_team` | str | **0** | Retrosheet code |
| `source_name` | str | 0 | Always "Retrosheet" |
| `source_row_number` | int | 0 | |
| `away_score` | int | 0 | |
| `home_score` | int | 0 | |
| `y_true_home_win` | int | 0 | 0/1 |

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total rows | 2,429 |
| Date range | 2024-03-20 → 2024-09-30 |
| Duplicate game_id | **0** |
| Missing `away_team` | **0** |
| Missing `home_team` | **0** |
| Missing `game_date` | **0** |

---

## game_id Format Examples

```
SDN-20240320-0    (San Diego Padres home, March 20 opening)
LAN-20240321-0    (LA Dodgers home, March 21)
ARI-20240328-0    (Arizona home, March 28)
BAL-20240415-0    (Baltimore home, April 15)
CHA-20240415-0    (Chicago White Sox home, April 15)
OAK-20240415-0    (Oakland Athletics home, April 15)
TBA-20240415-0    (Tampa Bay Rays home, April 15)
```

**Format is identical to P38A game_id format.** Direct string join works without any transformation.

---

## Team Code Format

Bridge uses **Retrosheet** codes throughout (both home_team and away_team):

| Retrosheet | Canonical |
|-----------|-----------|
| CHA | CWS |
| KCA | KC |
| LAN | LAD |
| SDN | SD |
| TBA | TB |
| ARI | AZ |
| OAK | ATH |
| ANA | LAA |

These codes are already handled by `scripts/team_code_normalization.py` (P39E).

---

## P38A Join Test Results

| Test | Result |
|------|--------|
| P38A rows | 2,187 |
| Bridge rows | 2,429 |
| **Direct game_id join: matched** | **2187 / 2187 = 100.0%** |
| Unmatched P38A rows | 0 |
| April in-scope matched | 210 / 210 = 100.0% |
| Join deterministic hash | `a894dbca99ac1910` |

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Team code mismatch (Retrosheet → Statcast) | LOW | Already handled by P39E normalization module |
| Doubleheader game_id (suffix -0, -1) | LOW | Both P38A and bridge use same suffix convention; no collision observed |
| Missing P38A game_id in bridge | **NONE** — 100% match | |
| Bridge `home_team` conflicts with P38A extracted `home_team` | LOW | Bridge `home_team` is the authoritative source; use bridge directly |

---

## Conclusion

The bridge is **VALID** and supports complete away_team recovery for all 2,187 P38A OOF rows.

After bridge enrichment + team code normalization, the pipeline can join P39B Statcast rolling features for **both** home and away sides.

---

## Marker

`P39F_IDENTITY_BRIDGE_INSPECTION_READY_20260515`
