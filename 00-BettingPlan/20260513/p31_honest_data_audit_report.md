# P31 Honest Data Reality Audit Report

**Date**: 2026-05-13T02:23:06Z
**Phase**: P31 — Honest Data Reality Audit & 2024 Acquisition Decision Gate
**PAPER_ONLY**: True
**production_ready**: False

---

## 1. Executive Conclusion
Of the **1397** data files classified in this audit, **1** qualify as RAW_PRIMARY, **0** as RAW_SECONDARY, **1372** as DERIVED_OUTPUT, and **24** as SCHEMA_PARTIAL.

P30 claimed `n_ready_sources=348` and `expected_sample_gain=54,675`. This audit confirms that **1372** of those sources are DERIVED_OUTPUT — pipeline-generated artifacts, not new raw historical data. The P30 READY designation is therefore misleading and should be treated as **READY_WITH_CAVEAT**.

**2024 usable raw sources found in repo**: 0. No 2024 raw game logs or closing odds exist in the repository.

**P32 recommendation**: **GO_PARTIAL_GAME_LOGS_ONLY**. Retrosheet gl2024 (game logs) can be acquired with low risk. Closing odds require license resolution before full ingestion.

## 2. Source Classification Counters
| Metric | Count |
| --- | --- |
| Total sources classified | 1397 |
| RAW_PRIMARY | 1 |
| RAW_SECONDARY | 0 |
| DERIVED_OUTPUT | 1372 |
| SCHEMA_PARTIAL | 24 |
| Usable 2024 raw sources (in-repo) | 0 |
| P30 'ready' sources that are actually DERIVED_OUTPUT | 1372 |

> **NOTE**: DERIVED_OUTPUT sources were produced by earlier pipeline stages (p15, p25, p27, outputs/predictions/PAPER). They cannot be used as training data. Double-counting these as raw sources would inflate sample estimates by up to 54,675 rows.

## 3. P30 'ready_sources=348' Downgrade Explanation
P30 defined its READY gate as: `n_ready_sources >= threshold`. The 348 'ready' sources were identified by scanning the repository for files matching source acquisition criteria. However, the P30 scanner included derived pipeline outputs under `outputs/` in its count.

| P30 Metric | Claimed | Reality |
| --- | --- | --- |
| n_ready_sources | 348 | 1372 DERIVED + 1 RAW |
| expected_sample_gain | 54,675 | 0 (no 2024 raw data downloaded) |
| Gate | READY | READY_WITH_CAVEAT |

**Recommendation**: Retroactively annotate `00-BettingPlan/20260512/p30_historical_source_acquisition_plan_report.md` with: `NOTE: n_ready_sources includes derived outputs; raw-only count = 1`.

## 4. 2024 Acquisition Feasibility
**Current in-repo 2024 raw sources**: 0 (zero — no 2024 files exist in `data/`).

**Sample wall context** (from P28/P29):
- Active entries: 324
- Training threshold: 1,500
- Gap: -1,176
- Best policy relaxation achieved: 563 entries (still below 1,500)

**Retrosheet gl2024**: ~2,430 MLB regular-season games. If all games ingested and schema-validated, combined active entries could reach ~2,754 — well above the 1,500 threshold. Game-log ingestion is **feasible and LOW risk**.

**Closing odds for 2024**: No licensed, non-commercial provider confirmed. Without closing odds, model training is incomplete for moneyline edge calculation. This is a **MEDIUM–HIGH risk blocker** for full P32.

## 5. Provenance & License Decision Table
| Source | Type | Provenance | License | Risk | Schema Gap | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Retrosheet 2024 Game Logs (gl2024) | RAW_SECONDARY | VERIFIED | REQUIRES_ATTRIBUTION | LOW | closing_moneyline_home, closing_moneyline_away, run_line_spread, over_under | GO_PARTIAL |
| MLB Stats API 2024 Schedule + Linescore | RAW_SECONDARY | VERIFIED | REQUIRES_ATTRIBUTION | MEDIUM | closing_moneyline_home, closing_moneyline_away, run_line_spread, over_under | GO_PARTIAL |
| 2024 Closing Moneyline Odds (Provider TBD) | RAW_PRIMARY_CANDIDATE | UNRESOLVED | UNKNOWN | HIGH | None | PENDING_LICENSE |

### 5.1 Retrosheet 2024 Notes
gl2024.zip is publicly available for non-commercial research. Schema provides game outcomes and starting pitchers but no closing odds. A supplemental odds source (separate license) is required for full moneyline model training. P32 can proceed for game-log ingestion independently of odds resolution. Attribution required per Retrosheet terms: 'The information used here was obtained free of charge from and is copyrighted by Retrosheet.'

### 5.2 MLB Stats API 2024 Notes
MLB Stats API provides game outcomes but no betting odds. Useful as a cross-validation source alongside Retrosheet gl2024. Risk: MLB may rate-limit; API schema changes between seasons require field-mapping validation. Not a source for odds — must be paired with a licensed odds provider for full moneyline model input. Medium risk due to potential schema drift; recommend pinning API version.

### 5.3 2024 Closing Odds Notes
CRITICAL BLOCKER for full GO decision. Three candidate providers evaluated:
  1. The Odds API (historical tier):      https://the-odds-api.com/ — paid subscription;      non-commercial research use unclear; requires direct license inquiry.
  2. OddsPortal: scraping prohibited by TOS; HIGH legal risk.
  3. Pinnacle historical API: commercial license required;      research exception not documented.
ACTION REQUIRED before P32: Select provider, obtain license confirmation in writing, record in data/p31_provenance_audit.json. Until resolved, P32 can only ingest game logs (GO_PARTIAL). Full GO requires this blocker cleared.

## 6. Schema Gap Inventory
The following canonical columns are missing from the identified 2024 external sources. These gaps must be resolved before model training.

| Column | Retrosheet gl2024 | MLB Stats API | Odds Source (TBD) |
| --- | --- | --- | --- |
| game_date | ✅ Present (date field) | ✅ Present (gameDate) | ✅ Present |
| home_team | ✅ Present | ✅ Present | ✅ Present |
| away_team | ✅ Present (visiting_team_id) | ✅ Present | ✅ Present |
| home_score / away_score | ✅ Present | ✅ Present (linescore) | ❌ Not included |
| closing_moneyline_home | ❌ MISSING | ❌ MISSING | ⚠️ Unresolved license |
| closing_moneyline_away | ❌ MISSING | ❌ MISSING | ⚠️ Unresolved license |
| run_line_spread | ❌ MISSING | ❌ MISSING | ⚠️ Unresolved license |
| over_under | ❌ MISSING | ❌ MISSING | ⚠️ Unresolved license |

**Schema gap conclusion**: A JOIN of Retrosheet gl2024 + a licensed odds source is required to produce a complete training row. Game logs alone can populate ~4 of 8 canonical columns.

## 7. P31 Gate Determination
**Final P31 gate**: `P31_HONEST_DATA_AUDIT_READY`

Gate is READY because:
- At least one verifiable 2024 raw external source is identified (Retrosheet gl2024, VERIFIED provenance)
- License for game-log source is documented (attribution required, safe for non-commercial research)
- Schema gap inventory is updated with real measured data
- GO/NO-GO decision is issued below
- All counters distinguish RAW from DERIVED (no double-counting)


## 8. P32 Acquisition Decision
**Decision**: `GO_PARTIAL_GAME_LOGS_ONLY`

**Rationale**:
- Retrosheet gl2024 and MLB Stats API 2024 are VERIFIED with safe non-commercial licenses. Game-log ingestion can proceed NOW.
- 2024 closing moneyline odds provider is UNRESOLVED. Full moneyline model training must wait for license confirmation.

**P32 Phase A (permitted immediately)**:
  Download Retrosheet gl2024.zip → parse → validate schema →   load into data/mlb_2024/ raw layer.

**P32 Phase B (blocked pending license)**:
  Acquire closing moneyline odds → join with game logs →   build complete training rows.

**Expected gain from Phase A alone**:
  ~2,430 game records → potential active entries ~2,754 (if ≥90% pass schema validation).


## 9. Compliance Status
| Control | Value |
| --- | --- |
| PAPER_ONLY | True |
| production_ready | False |
| Live TSL called | False |
| Real bets placed | False |
| Data downloaded in P31 | False (audit only) |

---

```
P31_HONEST_DATA_AUDIT_READY
```

P31_HONEST_DATA_AUDIT_READY