# Phase 6C: Match Identity Bridge Report
*Generated: 2026-04-29T13:26:28Z*
*Run ID: phase6c_build_2026-04-29*

---

## 1. Executive Summary

Phase 6C built a deterministic team/match identity bridge between TSL odds
snapshots (Phase 6B output) and WBC 2026 prediction records.

**Critical Finding — Domain Mismatch:**
The TSL odds data covers **MLB, KBO, and NPB professional league games**
(date range: 2026-03-13 to 2026-04-30). The `prediction_registry` covers
**WBC 2026 pool games only** (date range: 2026-03-05 to 2026-03-11). These
are entirely different competitions with zero temporal and zero competition
overlap.

**CLV join readiness: 0.0%**

| Metric | Value |
|---|---|
| TSL odds snapshot rows (input) | 28,941 |
| TSL canonical matches | 383 |
| prediction_registry records (input) | 9 |
| postgame_results records (input) | 49 |
| Team alias entries | 66 |
| Bridge records written | 383 |
| MATCHED_PREDICTION | 0 |
| DOMAIN_MISMATCH | 348 |
| MISSING_PREDICTION | 7 |
| UNMATCHED_TEAM_CODE_MISSING | 28 |
| CLV join readiness | **0.0%** |

---

## 2. Input Evidence

### 2.1 TSL Odds Snapshots (`data/derived/odds_snapshots_2026-04-29.jsonl`)
- **28,941 rows** (Phase 6B output)
- **383 unique canonical matches**
- **Game date range: 2026-03-13 to 2026-04-30**
- **Team name language**: Traditional Chinese (e.g. `密爾瓦基釀酒人`, `起亞老虎`, `西武獅`)
- **`league` field**: `unknown_league` for all records (inferred by Phase 6B)
- **Leagues represented**: MLB (30 teams), KBO (10 teams), NPB (10+ teams)

### 2.2 prediction_registry (`data/wbc_backend/reports/prediction_registry.jsonl`)
- **9 rows**
- **game_id format**: WBC pool codes (A01–B10, C01–C10, D01–D10)
- **team format**: 3-letter WBC national team codes (COL, CUB, KOR, JPN, TPE, etc.)
- **coverage**: WBC 2026 pool phase only; dates ~2026-03-05 to ~2026-03-12

### 2.3 postgame_results (`data/wbc_backend/reports/postgame_results.jsonl`)
- **49 rows** (2 WBC-code rows + 47 numeric auto-synced rows)
- WBC-code rows: B06, C09 (recorded 2026-03-09)
- Numeric rows: 788xxx IDs, auto-synced from `wbc_2026_live_scores.json`
- Teams in numeric rows: full English names (Australia, Chinese Taipei, Korea, etc.)
- **Zero overlap** with TSL raw match IDs confirmed by probe

### 2.4 WBC Authoritative Snapshot (`data/wbc_2026_authoritative_snapshot.json`)
- **40 WBC games**: C01–C10, A01–A10, D01–D10, B01–B10
- `home`/`away` = 3-letter WBC national team codes at top level
- `game_time_utc` range: 2026-03-05T03:00:00Z to 2026-03-11T23:00:00Z

---

## 3. Team Alias Map Analysis

**Total unique team names: 66**

| Quality Flag | Count |
|---|---|
| RESOLVED (exact match) | 59 |
| LOW_CONFIDENCE (partial match) | 1 |
| TEAM_CODE_MISSING (no mapping found) | 6 |

**League distribution of resolved teams:**

| League | Unique Team Names |
|---|---|
| MLB | 30 |
| NPB | 12 |
| KBO | 10 |
| WBC | 8 |
| UNKNOWN | 6 |

**Key mapping sources used (hardcoded from `data/tsl_snapshot.py`):**
- `TEAM_NAME_TO_CODE`: 21 WBC national team Chinese names → 3-letter codes
- `MLB_ZH_TO_CODE`: 34 MLB Chinese team names → 3-letter codes
- `KBO_ZH_TO_CODE`: 10 KBO Chinese team names → league codes (Phase 6C additions)
- `NPB_ZH_TO_CODE`: 13 NPB Chinese team names → league codes (Phase 6C additions)

---

## 4. Match Identity Bridge Analysis

**Total bridge records: 383**

| Bridge Status | Count | % |
|---|---|---|
| MATCHED_PREDICTION | 0 | 0% |
| DOMAIN_MISMATCH | 348 | 90% |
| MISSING_PREDICTION | 7 | 1% |
| UNMATCHED_TEAM_CODE_MISSING | 28 | 7% |

### 4.1 Root Cause: Domain Mismatch

The zero-match outcome is **expected and correct** — not a data error:

| Attribute | TSL Odds | prediction_registry |
|---|---|---|
| **Competition** | MLB / KBO / NPB regular season | WBC 2026 national tournament |
| **Date range** | 2026-03-13 to 2026-04-30 | 2026-03-05 to ~2026-03-12 |
| **Team codes** | MLB (ARI, ATL…), KBO (KIA, LOT…), NPB (HAM, YKL…) | WBC (COL, CUB, KOR, JPN, TPE…) |
| **Temporal overlap** | **0 days** | — |
| **Competition overlap** | **0 games** | — |

The WBC 2026 pool phase ended on 2026-03-11. TSL began tracking
MLB/KBO/NPB regular season odds from 2026-03-13. These are separate
competitions. No valid prediction-to-odds join is possible from the
current prediction_registry.

---

## 5. Leakage / CLV Readiness

| Check | Result |
|---|---|
| L1: No future data in odds snapshot timestamps | PASS (Phase 6B verified) |
| L2: No future data in team alias map | PASS (static lookup table) |
| L3: Bridge match keys use match_time_utc only | PASS |
| L4: No model output in bridge records | PASS |
| CLV join readiness | **0.0%** — DOMAIN_MISMATCH blocking |
| Root cause | prediction_registry covers WBC; TSL covers MLB/KBO/NPB |

---

## 6. Phase 6D Recommendation (DOMAIN_DESIGN_REQUIRED)

To enable CLV validation for the TSL odds dataset, one of the following
must be implemented:

### Option A: Extend prediction_registry to cover MLB/KBO/NPB
- Build separate prediction models for MLB, KBO, and NPB regular season
- Align team codes to the resolved codes in `team_alias_map_2026-04-29.csv`
- Required team code schemas: MLB 3-letter (ARI, ATL…), KBO (KIA, LOT…), NPB (HAM, YKL…)

### Option B: Limit CLV analysis to WBC games only
- Filter TSL odds to WBC national team names (identified in `TEAM_NAME_TO_CODE`)
- Re-run bridge against WBC date range (2026-03-05 to 2026-03-11)
- Note: TSL data does NOT appear to contain WBC game odds in current dataset

### Recommended: Option A + seed KBO/NPB team code standards
- The `team_alias_map_2026-04-29.csv` provides the Chinese→code seed for this
- A CSV with authoritative KBO + NPB team codes should be committed as
  `data/derived/kbo_team_codes.csv` and `data/derived/npb_team_codes.csv`

---

## 7. Backward Compatibility

- Phase 6B `odds_snapshots_2026-04-29.jsonl` is **unchanged**
- Phase 6A CLV data contract is **unchanged**
- No source files were modified
- Bridge output is additive only

---

## 8. Scope Confirmation

| Constraint | Status |
|---|---|
| No external API calls | ✅ PASS |
| No source file modifications | ✅ PASS |
| No crawler / DB / model changes | ✅ PASS |
| No orchestrator tasks created | ✅ PASS |
| No commit performed | ✅ PASS (script only generates files) |
| Deterministic output (UUID5 IDs) | ✅ PASS |

---

## 9. Final Status

**PHASE_6C_BRIDGE_DOMAIN_MISMATCH_DOCUMENTED**

The bridge script ran successfully and produced valid, schema-compliant
output files. No prediction join is possible from current inputs due to
fundamental domain mismatch (TSL = MLB/KBO/NPB; predictions = WBC only).

This finding is the correct outcome of Phase 6C evidence-driven analysis.
Phase 6D must decide which direction to extend the prediction system before
CLV validation can proceed.

**Output files:**
- `data/derived/team_alias_map_2026-04-29.csv` — 66 team alias entries
- `data/derived/match_identity_bridge_2026-04-29.jsonl` — 383 bridge records
- `docs/orchestration/phase6c_match_identity_bridge_report_2026-04-29.md` — this report
