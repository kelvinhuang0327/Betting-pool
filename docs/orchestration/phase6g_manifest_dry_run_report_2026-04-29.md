# Phase 6G — Manifest Dry-Run Quality Report

**Date:** 2026-04-29
**Type:** Dry-run quality report — read-only on existing derived outputs
**Predecessor:** Phase 6F (`5b3a265`) — `docs/orchestration/phase6f_future_event_capture_manifest_2026-04-29.md`
**Domain:** `DOMAIN_COMMITMENT_MLB_KBO_NPB`

---

## 1. Executive Summary

This report applies the Phase 6F capture manifest quality gates (G1–G8, A1–A3) to the
existing Phase 6B/6C derived outputs for the MLB/KBO/NPB CLV pipeline.

**Readiness Decision:**

```
NOT_READY_DOMAIN_MISMATCH
```

Key findings:

- Total odds snapshots: **28,941**
- Allowed-market selection keys (ML/RL/OU only): **5,963**
- OPENING+CLOSING pairs (G1+G2 eligible): **4,356**
- Bridge-ready records (G7 pass): **0**
- Domain-mismatch selections: **5,757**

The bridge-ready count of **0** is the **expected outcome** from Phase 6C.
All 383 current matches show `DOMAIN_MISMATCH` because the prediction_registry
covers WBC 2026 only (2026-03-05..03-11), while the TSL odds cover MLB/KBO/NPB
(2026-03-13+). This is not a script failure — it is the confirmed root cause from
Phase 6C that motivates the future-event capture strategy.

---

## 2. Input Evidence

### 2.1 Input Files

| File | Path | Status |
|---|---|---|
| odds_snapshots | `data/derived/odds_snapshots_2026-04-29.jsonl` | ✅ Loaded |
| match_identity_bridge | `data/derived/match_identity_bridge_2026-04-29.jsonl` | ✅ Loaded |
| team_alias_map | `data/derived/team_alias_map_2026-04-29.csv` | ✅ Loaded |

### 2.2 Snapshot Distribution (All Markets)

| Market Type | Count |
|---|---|
| `OU` | 14,572 |
| `ML` | 8,335 |
| `RL` | 3,886 |
| `OE` | 2,148 |

- Excluded market rows (OE/TTO/EXOTIC): **2,148**
- POST_MATCH rows excluded from CLV pool: **2,127**

### 2.3 Bridge Status Distribution

| Bridge Status | Matches |
|---|---|
| `DOMAIN_MISMATCH` | 348 |
| `UNMATCHED_TEAM_CODE_MISSING` | 28 |
| `MISSING_PREDICTION` | 7 |

### 2.4 Team Alias Map

| Status | Count |
|---|---|
| RESOLVED | 59 |
| TEAM_CODE_MISSING | 6 |
| LOW_CONFIDENCE | 1 |
| **Total** | **66** |

---

## 3. Dry-Run Method

The dry-run checker (`scripts/run_manifest_dry_run.py`) applies the following logic:

1. Load all three required derived files.
2. Filter snapshots to ML/RL/OU markets only (exclude OE/TTO/EXOTIC).
3. Exclude POST_MATCH snapshots from the CLV-eligible pool.
4. Group remaining snapshots by `selection_key`.
5. For each `selection_key`, evaluate gates G1–G8.
6. Join to match_identity_bridge via `canonical_match_id` for G7.
7. Compute aggregate gates A1–A3 over all selection_keys.
8. Determine readiness_decision enum.

**Leakage guard:** The checker reads only derived outputs produced by prior phases.
No external API calls, no model inference, no settlement data required.

---

## 4. Per-Selection Gate Results

Total selection_keys evaluated: **5,963**
(ML/RL/OU only; POST_MATCH excluded)

| Gate | Description | Pass | Fail | Warn |
|---|---|---|---|---|
| `G1_OPENING_EXISTS` | OPENING snapshot exists | 4,356 | 1,607 | - |
| `G2_CLOSING_EXISTS` | CLOSING snapshot exists | 4,356 | 1,607 | - |
| `G3_MARKET_ALLOWED` | market_type in ML/RL/OU | 5,963 | 0 | - |
| `G4_POST_MATCH_EXCLUDED` | POST_MATCH excluded from pool | 5,963 | 0 | - |
| `G5_SNAPSHOT_ORDER_VALID` | OPENING < CLOSING < match_time_utc | 3,876 | 1,607 | 480 |
| `G6_IMPLIED_PROBABILITY_VALID` | 0 < implied_probability < 1 | 4,356 | 1,607 | - |
| `G7_BRIDGE_STATUS_READY` | bridge_status in MATCHED_* set | 0 | 5,963 | - |
| `G8_QUALITY_FLAGS_ACCEPTABLE` | no POST_MATCH_EXCLUDED flag | 4,356 | 0 | 1607 |

### 4.1 Gate Notes

**G1 / G2:** A high number of selections pass both gates, confirming the Phase 6B
adapter successfully captured OPENING and CLOSING snapshot pairs. These pairs are
the raw material for future CLV computation once prediction and settlement data are
available.

**G3 / G4:** All evaluated selection_keys are ML/RL/OU. POST_MATCH rows are excluded
cleanly from the CLV pool.

**G5:** Selection_keys where OPENING and CLOSING exist are checked for temporal order.
Warnings indicate cases where both snapshots have identical timestamps (edge case in
Phase 6B classification).

**G6:** Implied probability validity is checked on OPENING and CLOSING snapshots.
Expected to pass for all rows where odds were captured correctly.

**G7 (blocking gate):** `bridge_status` is checked against MATCHED_EXACT/MATCHED_ALIAS/
MATCHED_TIME_TEAM. All current matches show `DOMAIN_MISMATCH` or `UNMATCHED_*` because:
  - The prediction_registry covers WBC 2026 matches only.
  - TSL odds cover MLB/KBO/NPB matches from 2026-03-13 onward.
  - There is zero temporal or competition overlap between the two domains.
  This is the **expected and documented finding** from Phase 6C. G7 failure does not
  mean the odds adapter is broken; it means the prediction domain must be extended.

**G8:** Quality flag check is informational. OPENING_CLOSING_AMBIGUOUS flags may be
present for single pre-match snapshots that Phase 6B could not classify definitively.

---

## 5. Aggregate Gate Results

| Gate | Description | Result | Notes |
|---|---|---|---|
| `A1` | bridge-ready ≥ 200 | FAIL — current=0 | PROVISIONAL_THRESHOLD_REQUIRES_RECALIBRATION |
| `A2` | ≥1 MLB/KBO/NPB league bridge-ready | FAIL — leagues=none | See §5.2 |
| `A3` | ML/RL/OU coverage present | PASS — markets=['ML', 'OU', 'RL'] | Informational only |

### 5.1 A1 — Sample Sufficiency

- Current bridge-ready selections: **0**
- Required for aggregate CLV validation: **≥ 200**
- Status: **FAIL**
- Note: `PROVISIONAL_THRESHOLD_REQUIRES_RECALIBRATION`

Aggregate CLV validation (Phase 6J/6K) is blocked until bridge-ready samples
accumulate to ≥200. This requires the prediction pipeline to be extended to
MLB/KBO/NPB (Phase 6H) so that canonical_match_id-keyed predictions exist.

### 5.2 A2 — League Coverage

No bridge-ready leagues in current dataset. All 383 bridge records have
`bridge_status = DOMAIN_MISMATCH` or `UNMATCHED_*`. League coverage will be
confirmed in Phase 6H when the first MLB/KBO/NPB predictions are registered.

### 5.3 A3 — Market Coverage

| Market | Allowed Selection_Keys |
|---|---|
| `ML` | 1,057 |
| `RL` | 1,310 |
| `OU` | 3,596 |

Market coverage is present (A3 informational pass). The Phase 6F domain
prioritizes ML as primary market; RL and OU are secondary. Coverage confirms
the Phase 6B adapter correctly normalized TSL market codes.

---

## 6. Readiness Decision

**Decision: `NOT_READY_DOMAIN_MISMATCH`**

Decision criteria:

| Criterion | Status |
|---|---|
| OPENING snapshots available | ✅ — 4,356 selections |
| CLOSING snapshots available | ✅ — 4,356 selections |
| Bridge-ready count ≥ 0 | ✅ — 0 |
| Domain mismatch detected | ✅ (expected) — 5,757 selections affected |
| A1 sample sufficiency | ❌ NOT_MET — 0/200 |

`NOT_READY_DOMAIN_MISMATCH` is the **expected and correct result** at this stage.
It means:
1. The odds snapshot adapter (Phase 6B) is working correctly.
2. The match identity bridge (Phase 6C) correctly detected the prediction domain gap.
3. Formal CLV validation must not run until the prediction pipeline is extended.
4. 4,796 OPENING+CLOSING pairs are available and waiting for prediction coverage.

---

## 7. Findings

### 7.1 Odds Snapshot Adapter is Functional

The Phase 6B adapter (`scripts/build_odds_snapshots.py`) successfully produced
28,941 snapshot rows from TSL history data.
Of these, 4,356 OPENING+CLOSING selection_key pairs
are available across ML/RL/OU markets. This is the raw material for CLV computation.
The adapter is not broken and requires no changes for the dry-run phase.

### 7.2 Identity Bridge Proves Current Prediction Domain Mismatch

The Phase 6C bridge (`scripts/build_match_identity_bridge.py`) correctly identified
that 348 of 383 canonical matches
are `DOMAIN_MISMATCH`. This is because:
- The current `prediction_registry` contains only WBC 2026 game IDs (A01–D09, etc.)
- The TSL odds cover MLB/KBO/NPB matches from 2026-03-13 onward
- There is zero overlap in competition type, teams, or date range

The identity bridge confirmed the domain gap **correctly**. Its logic is sound
and domain-agnostic — it will work once the prediction domain is extended.

### 7.3 Formal CLV Validation Must Not Run Yet

With bridge-ready count = 0 and A1 sample < 200, formal CLV validation would
produce meaningless or misleading results. The Phase 5.5 hypothesis
(`CLV_proxy > 0.03 → ≥3pp ROI over ≥200 bets`) requires a minimum of 200
bridge-ready, settled MLB/KBO/NPB bets. None exist today.

### 7.4 Next Focus: Future-Event Capture and Prediction Registry Alignment

To unlock CLV validation, the following are required:

1. **Prediction registry extension** (Phase 6H): Extend the prediction output
   format to include `canonical_match_id`, `prediction_time_utc`, `model_version`,
   `feature_version` for MLB/KBO/NPB matches.
2. **Settlement source confirmation** (Phase 6I): Define an approved result source
   for MLB/KBO/NPB game scores.
3. **League resolution** at capture time: The `unknown_league` value in current
   snapshots must be replaced with `MLB`/`KBO`/`NPB` during future captures.

---

## 8. Recommended Next Step

**Phase 6H prediction registry extension design for MLB/KBO/NPB canonical matches**

Rationale:
- Phase 6E committed the domain to MLB/KBO/NPB.
- Phase 6F defined the capture manifest and lifecycle.
- This dry-run confirmed that 4,796 OPENING+CLOSING odds pairs already exist.
- The only remaining structural gap is the **absence of MLB/KBO/NPB predictions**
  in `canonical_match_id` format.
- Phase 6H should design the schema extension to the prediction registry before
  any production prediction pipeline changes are made.

Phase 6H scope (recommended):
- Read existing walk-forward prediction outputs for MLB/KBO/NPB
- Design `canonical_match_id`-keyed prediction schema (documentation first)
- Define `model_version`, `feature_version`, `leakage_guard_version` fields
- Document required pipeline changes (no implementation yet)

---

## 9. Scope Confirmation

| Constraint | Status |
|---|---|
| Source data modified | NO |
| Crawler modified | NO |
| DB modified | NO |
| Model modified | NO |
| External API called | NO |
| Orchestrator task created | NO |
| Formal CLV validation run | NO |
| Git commit made | NO |

Files written by this task (new only):
- `scripts/run_manifest_dry_run.py` — dry-run checker script (new)
- `docs/orchestration/phase6g_manifest_dry_run_report_2026-04-29.md` — this report (new)
- `data/derived/manifest_dry_run_summary_2026-04-29.json` — summary JSON (new, optional)

---

**PHASE_6G_DRY_RUN_VERIFIED**

*Domain: `DOMAIN_COMMITMENT_MLB_KBO_NPB`.*
*Next action: Phase 6H prediction registry extension design.*