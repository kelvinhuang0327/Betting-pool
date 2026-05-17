# P31 Mission Specification
## P31 — Honest Data Reality Audit & 2024 Acquisition Decision Gate

**Date**: 2026-05-13
**Author**: Transition Agent (P30→P31)
**Status**: PLANNING — awaiting execution in next agent run
**PAPER_ONLY**: True
**production_ready**: False

---

## 1. Phase Name

**P31 — Honest Data Reality Audit & 2024 Acquisition Decision Gate**

---

## 2. Mission Statement

Distinguish raw historical sources from derived pipeline outputs in the current
data inventory. Conduct an honest classification audit to determine the true
number of raw historical records available for model training. Decide whether
2024 MLB season ingestion is feasible and safe, and issue a GO / NO-GO
acquisition decision.

**Core problem this phase solves:**
- P30 reported `n_ready_sources=348` but the majority of these are derived
  pipeline outputs in `outputs/`, not new raw historical data.
- P28 + P29 confirmed only 324 active entries exist; no policy combo reaches
  1,500 without new raw historical ingestion.
- This audit ends the "auditing the audit" loop and gives a concrete path
  forward or a hard BLOCKED signal.

---

## 3. Source Classification Taxonomy

All inventory entries must be assigned exactly one of the following four classes:

| Class | Code | Definition |
|-------|------|-----------|
| Raw Primary | `RAW_PRIMARY` | CSV / JSON from `data/` with game-day timestamps, no model-generated fields, covers ≥1 full season |
| Raw Secondary | `RAW_SECONDARY` | Retrosheet / MLB Stats API exports, externally sourced; license documented; no model fields |
| Derived Output | `DERIVED_OUTPUT` | Files under `outputs/predictions/PAPER/**`, `p15/`, `p25/`, `p27/` lineage, or any file produced by a model/pipeline step |
| Schema Partial | `SCHEMA_PARTIAL` | Raw but missing one or more canonical columns (e.g. `game_date`, `home_team`, `run_line_result`, `moneyline_result`) |

**Classification rules:**
- A file is `DERIVED_OUTPUT` if it was written by any script that calls a
  model, prediction pipeline, or aggregation function.
- A file is `RAW_PRIMARY` only if it has a verifiable external timestamp and
  contains no predicted columns.
- `SCHEMA_PARTIAL` files cannot be used for training without backfill.
- Double-counting across classes is forbidden.

---

## 4. Required External Sources for 2024

The following external sources must be evaluated for the 2024 acquisition
decision. Each requires provenance documentation and license check:

### 4.1 Retrosheet 2024 Game Logs (gl2024)
- **URL**: https://www.retrosheet.org/gamelogs/index.html
- **Format**: Fixed-width text (`.TXT`), ~161 columns per game
- **License**: Retrosheet non-commercial use; attribution required
- **Action**: Download `gl2024.zip`, validate field mapping to canonical schema
- **Schema columns needed**: `game_date`, `home_team`, `visitor_team`, `home_runs`, `visitor_runs`
- **Provenance**: Must record download date, URL, SHA256 hash in `data/provenance.json`

### 4.2 MLB Stats API 2024 Schedule + Linescore
- **Endpoint**: `https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2024`
- **Format**: JSON
- **License**: MLB Stats API — free for non-commercial research; no redistribution of raw feed
- **Action**: Evaluate if linescore data covers all 2430 regular-season games
- **Provenance**: Record API version, season param, fetch timestamp

### 4.3 Closing Moneyline Odds 2024
- **Status**: UNRESOLVED — must select provider
- **Candidate providers**:
  - The Odds API (historical tier, paid): `https://the-odds-api.com/`
  - OddsPortal (scraped, TOS risk): restricted use
  - Pinnacle historical (API, paid): commercial license
- **License check required**: Determine if any provider permits non-commercial
  model training use before downloading
- **Blocker**: P31 must document the chosen provider + license decision.
  If no provider is license-safe, issue `P31_BLOCKED_LICENSE_PROVENANCE_UNSAFE`.

---

## 5. Gate Constants

```python
# P31 gate constants — define exactly one outcome per run
P31_HONEST_DATA_AUDIT_READY = "P31_HONEST_DATA_AUDIT_READY"
P31_BLOCKED_NO_RAW_HISTORICAL_INCREMENT = "P31_BLOCKED_NO_RAW_HISTORICAL_INCREMENT"
P31_BLOCKED_LICENSE_PROVENANCE_UNSAFE = "P31_BLOCKED_LICENSE_PROVENANCE_UNSAFE"
P31_BLOCKED_NON_DETERMINISTIC_INVENTORY = "P31_BLOCKED_NON_DETERMINISTIC_INVENTORY"
P31_FAIL_INPUT_MISSING = "P31_FAIL_INPUT_MISSING"
```

| Constant | Trigger condition |
|----------|------------------|
| `P31_HONEST_DATA_AUDIT_READY` | ≥1 verifiable RAW_PRIMARY or RAW_SECONDARY 2024 source identified; license documented; GO/NO-GO issued |
| `P31_BLOCKED_NO_RAW_HISTORICAL_INCREMENT` | All candidate 2024 sources are DERIVED_OUTPUT or SCHEMA_PARTIAL; no ingestion path exists |
| `P31_BLOCKED_LICENSE_PROVENANCE_UNSAFE` | No odds provider with safe non-commercial license identified |
| `P31_BLOCKED_NON_DETERMINISTIC_INVENTORY` | Inventory counts differ across two audit runs; root cause not resolved |
| `P31_FAIL_INPUT_MISSING` | Required input files (canonical schema, existing inventory list) not found |

---

## 6. Acceptance Criteria for P31_HONEST_DATA_AUDIT_READY

All of the following must be satisfied:

- [ ] **AC-1** At least one verifiable 2024 RAW_PRIMARY or RAW_SECONDARY source path
      is identified (file path or API endpoint with confirmed data availability)
- [ ] **AC-2** Provenance + license for each candidate 2024 source is documented
      in `data/p31_provenance_audit.json`
- [ ] **AC-3** Schema gap inventory is updated with real measured counts
      (not theoretical projections like "54,675 expected")
- [ ] **AC-4** 2024 acquisition decision issued as `GO` or `NO-GO` with written reason
- [ ] **AC-5** All counters separate `RAW_PRIMARY + RAW_SECONDARY` from `DERIVED_OUTPUT`
      — no double-counting
- [ ] **AC-6** P31 audit report produced at
      `00-BettingPlan/20260513/p31_honest_data_audit_report.md`
- [ ] **AC-7** Gate constant written as final line of report

---

## 7. Hard Non-Goals

The following are explicitly OUT OF SCOPE for P31:

| Non-Goal | Rationale |
|----------|-----------|
| **Do not download any data in P31** | Downloading is P32. P31 is audit + decision only. |
| **Do not build joined input artifacts** | That was the old (deprecated) P31 goal. It was removed because it presupposed data that doesn't exist yet. |
| **Do not fabricate source counts or file paths** | Any invented path must be flagged as `THEORETICAL` not `VERIFIED`. |
| **Do not re-run P30 acquisition pipeline** | P30 ran its dry-run; results are final for this cycle. |
| **Do not scrape live TSL or place bets** | PAPER_ONLY=True at every layer. |

---

## 8. Out-of-Scope Notes for CTO

The following flags are raised from the P30 → P31 transition audit:

### 8.1 P30 "n_ready_sources=348" Misleading Nomenclature (FLAGGED FOR DOWNGRADE)
- P30 contract defines `ready_sources >= threshold` as the READY gate.
- However, of the 348 "ready" sources, the majority are `DERIVED_OUTPUT`
  entries in `outputs/` — files produced by earlier pipeline stages.
- **Recommendation**: Retroactively annotate P30 report with
  `NOTE: n_ready_sources counts derived outputs as ready; raw-only count = TBD`
- P30 SHOULD be considered `READY_WITH_CAVEAT`, not unconditional READY.

### 8.2 "expected_sample_gain=54,675" Is Theoretical (NOT DELIVERABLE)
- P30 projected 54,675 new samples from the acquisition plan.
- This number was computed from source file sizes × expected rows-per-file.
- No actual 2024 files have been downloaded or validated.
- **Recommendation**: Replace projection with `PROJECTED_UPPER_BOUND` label.
  Real deliverable count is 0 until P32 completes ingestion.

### 8.3 Sample Wall Remains Hard-Blocked
- P28 + P29 confirmed: 324 active entries, no existing policy combination
  reaches the 1,500-entry model training threshold.
- P31 audit must confirm whether 2024 ingestion can bridge this gap.
- If 2024 provides ~2,430 regular season games, that is the primary candidate
  to push active entries above 1,500.

---

## Deliverable Checklist for P31 Implementation Agent

The **next agent run** (P31 implementation) must produce:

1. `data/p31_source_classification_audit.csv`
   — Every inventory entry classified as RAW_PRIMARY / RAW_SECONDARY /
     DERIVED_OUTPUT / SCHEMA_PARTIAL
2. `data/p31_provenance_audit.json`
   — Provenance + license record for each 2024 candidate source
3. `00-BettingPlan/20260513/p31_honest_data_audit_report.md`
   — Full audit findings with gate constant as final line
4. Updated schema gap table (real counts, not theoretical)
5. 2024 acquisition decision: `GO` or `NO-GO` with justification

---

## Gate Marker

```
P31_MISSION_SPEC_READY
```

P31_MISSION_SPEC_READY
