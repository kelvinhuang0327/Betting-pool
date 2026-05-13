# P36 Odds Approval Import Gate — Research Report

**Date**: 2026-05-13  
**Phase**: P36 — Licensed Odds Approval Import Gate  
**Branch**: `p13-clean`  
**Prior HEAD**: `cdedd24` (P35 commit)  
**PAPER_ONLY**: `True`  
**PRODUCTION_READY**: `False`  
**SEASON**: `2024`

---

## 1. Phase Objective

P36 establishes a mandatory approval gate for importing any externally-sourced odds data into the 2024 MLB research pipeline. Before any odds file can be consumed by downstream phases (P37+), the researcher must:

1. Create a signed approval record documenting the provider's license terms.
2. Confirm that internal research use is permitted.
3. Confirm the data was downloaded manually — no automated scraping.
4. Acknowledge that raw odds files must **never** be committed to the repository.

This gate is a data governance control, not a prediction logic gate.

---

## 2. Module Inventory

| File | Role |
|------|------|
| `wbc_backend/recommendation/p36_odds_approval_contract.py` | All constants, dataclasses, gate strings |
| `wbc_backend/recommendation/p36_odds_approval_record_validator.py` | Load & validate approval record JSON |
| `wbc_backend/recommendation/p36_manual_odds_import_validator.py` | Validate manual odds CSV schema |
| `wbc_backend/recommendation/p36_odds_import_gate_planner.py` | Gate decision logic + file writer |
| `scripts/run_p36_odds_approval_import_gate.py` | CLI orchestrator (14-step pipeline) |

---

## 3. Approval Record Specification (16 Required Fields)

```
provider_name, source_name, source_url_or_reference, license_terms_summary,
allowed_use, redistribution_allowed, attribution_required,
internal_research_allowed, commercial_use_allowed, approved_by, approved_at,
approval_scope, source_file_expected_path, checksum_required,
paper_only, production_ready
```

All fields must be present and non-empty. `paper_only` must be `true`; `production_ready` must be `false`.

---

## 4. Manual Odds Schema Specification (11 Required Columns)

```
game_id, game_date, home_team, away_team, p_market,
odds_decimal, sportsbook, market_type, closing_timestamp,
source_odds_ref, license_ref
```

**Forbidden columns (10)**: `y_true`, `final_score`, `home_score`, `away_score`, `winner`,
`outcome`, `result`, `run_diff`, `total_runs`, `game_result`

**Allowed market types**: `moneyline`, `ml`, `money_line`, `1x2`, `h2h`

---

## 5. Gate Priority Logic

| Priority | Condition | Gate |
|----------|-----------|------|
| 1 | `production_ready=True` or `paper_only=False` | `P36_BLOCKED_CONTRACT_VIOLATION` |
| 2 | No approval record provided | `P36_BLOCKED_APPROVAL_RECORD_MISSING` |
| 3 | Approval record has missing/invalid fields | `P36_BLOCKED_APPROVAL_RECORD_INVALID` |
| 4 | `internal_research_allowed=False` or bad `allowed_use` | `P36_BLOCKED_LICENSE_NOT_ALLOWED_FOR_RESEARCH` |
| 5 | Approval valid, but no odds source file provided | `P36_BLOCKED_ODDS_SOURCE_NOT_PROVIDED` |
| 6 | All checks pass | `P36_ODDS_APPROVAL_RECORD_READY` |

`raw_odds_commit_allowed` is always `False`, even when gate = READY.

---

## 6. Test Results

| Test File | Tests |
|-----------|-------|
| `test_p36_odds_approval_contract.py` | 20 |
| `test_p36_odds_approval_record_validator.py` | 24 |
| `test_p36_manual_odds_import_validator.py` | 22 |
| `test_p36_odds_import_gate_planner.py` | 18 |
| `test_run_p36_odds_approval_import_gate.py` | 10 |
| **Total P36** | **94** |

All 94 P36 tests pass. Combined with prior phases: **769 total** (675 prior + 94 P36).

---

## 7. Real CLI Run (No Approval Record)

```
Command:
  python scripts/run_p36_odds_approval_import_gate.py
    --p32-dir data/mlb_2024/processed
    --p35-dir data/mlb_2024/processed/p35_dual_source_import_validation
    --output-dir data/mlb_2024/processed/p36_odds_approval_import_gate
    --paper-only true

Result:
  p36_gate=P36_BLOCKED_APPROVAL_RECORD_MISSING
  approval_record_status=APPROVAL_MISSING
  odds_source_status=unknown
  internal_research_allowed=False
  raw_odds_commit_allowed=False
  paper_only=True
  production_ready=False
  EXIT_CODE=1
```

P35 prerequisite gate (`P35_BLOCKED_ODDS_LICENSE_NOT_APPROVED`) was verified successfully. P32 game identity (2429 rows) loaded successfully.

---

## 8. Output Files (data/mlb_2024/processed/p36_odds_approval_import_gate/)

| File | Contents |
|------|----------|
| `odds_approval_validation.json` | Approval record validation result |
| `manual_odds_import_schema.json` | Required schema for manual odds CSV |
| `manual_odds_import_validation.json` | Manual odds file validation result (NO_FILE) |
| `odds_import_gate_plan.json` | Full gate plan dict |
| `odds_import_gate_plan.md` | Human-readable gate summary |
| `p36_gate_result.json` | Final gate decision + recommended next action |

---

## 9. Fixture-Only Validation (READY path)

A temporary approval record and odds CSV were created in `/tmp` (not committed).

```
Result:
  p36_gate=P36_ODDS_APPROVAL_RECORD_READY
  approval_record_status=APPROVAL_READY
  odds_source_status=provided
  internal_research_allowed=True
  raw_odds_commit_allowed=False
  production_ready=False
  paper_only=True
  EXIT_CODE=0
```

The READY path confirms that valid inputs produce gate passage. Fixture files were discarded post-verification.

---

## 10. Determinism Check

Two independent runs against `/tmp/p36_det_run1` and `/tmp/p36_det_run2` with no approval record.

```
DETERMINISM_CHECK=PASSED
```

Keys excluded from comparison: `generated_at`, `output_dir`, `artifacts`.

---

## 11. Data Safety Invariants

- `raw_odds_commit_allowed=False` **always** (even when gate=READY). Redistribution risk.
- No raw odds files staged or committed at any point.
- No automated scraping. `requests.get`, `urllib`, `BeautifulSoup` absent from all P36 modules.
- `PAPER_ONLY=True` enforced at module level and re-enforced in all outputs regardless of record content.
- `PRODUCTION_READY=False` enforced at module level and re-enforced in all outputs.
- Fixture files written only to `/tmp`, never to repo.

---

## 12. Next Phase

`P37_BUILD_2024_ODDS_IMPORT_ARTIFACT` — Build the actual 2024 odds import artifact using a manually approved and licensed odds source, subject to the approval contract established in P36.

To unblock P36: provide a valid `odds_approval_record.json` at `data/mlb_2024/manual_import/` after reviewing the ToS of the chosen odds provider.

---

## 13. Gate Marker

```
P36_ODDS_APPROVAL_IMPORT_GATE_BLOCKED
```

*Current state: blocked at approval record missing. This is expected for this phase — no licensed odds source has been obtained yet. Gate logic and infrastructure are fully implemented and validated.*
