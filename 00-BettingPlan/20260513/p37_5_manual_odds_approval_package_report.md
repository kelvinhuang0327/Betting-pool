# P37.5 Manual Odds Approval Package — Report

**Phase**: P37.5 — Manual Odds Approval Package Preparation
**Date**: 2026-05-13
**Branch**: `p13-clean`
**Prior commit (P37)**: `08b9d5d`
**PAPER_ONLY**: `true`
**PRODUCTION_READY**: `false`
**Season**: 2024

---

## Summary

P37.5 completes the human-operator documentation layer for the P37 manual odds
provisioning gate.  All artifacts are in place for a researcher to safely
provision licensed 2024 MLB odds data without violating data leakage, copyright,
or git staging constraints.

**Final marker**: `P37_5_MANUAL_ODDS_APPROVAL_PACKAGE_READY`

---

## Files Created

### Documentation (6 files)

| File | Purpose |
|------|---------|
| `docs/betting/manual_odds_approval/P37_5_APPROVAL_PACKAGE.md` | Overview and index |
| `docs/betting/manual_odds_approval/P37_5_OPERATOR_CHECKLIST.md` | Step-by-step operator checklist |
| `docs/betting/manual_odds_approval/P37_5_PROVIDER_TOS_REVIEW_TEMPLATE.md` | Provider ToS review template |
| `docs/betting/manual_odds_approval/P37_5_MANUAL_IMPORT_RUNBOOK.md` | End-to-end provisioning runbook |
| `docs/betting/manual_odds_approval/odds_approval_record_EXAMPLE_PLACEHOLDER.json` | 17-field example (PLACEHOLDER values) |
| `docs/betting/manual_odds_approval/odds_2024_approved_EXAMPLE_TEMPLATE.csv` | 11-column example (EXAMPLE_* values) |

### Scripts (1 file)

| File | Purpose |
|------|---------|
| `scripts/check_p37_manual_odds_package.py` | Checks presence and validity of manual files, writes output JSON |

### Tests (2 files)

| File | Tests |
|------|-------|
| `tests/test_p37_5_manual_approval_docs.py` | 43 tests — docs exist, content markers, JSON fields, CSV columns |
| `tests/test_check_p37_manual_odds_package.py` | 35 tests — script exists, exit codes, no fabrication, no staging |

### Processed Outputs (1 file)

| File | Content |
|------|---------|
| `data/mlb_2024/processed/p37_manual_odds_provisioning/p37_5_manual_package_check.json` | Check result JSON (exit=1, both files missing) |

---

## Gate / Checker Run Results

### Real Run (current state — expected exit 1)

```
MISSING: data/mlb_2024/manual_import/odds_approval_record.json
MISSING: data/mlb_2024/manual_import/odds_2024_approved.csv
STATUS: Both manual files missing.
ACTION: Provision both files per docs/betting/manual_odds_approval/P37_5_OPERATOR_CHECKLIST.md
EXIT_CODE=1
```

### Check Result JSON

```json
{
  "p37_5_status": "P37_5_MANUAL_ODDS_PACKAGE_MISSING",
  "paper_only": true,
  "production_ready": false,
  "raw_odds_commit_allowed": false,
  "season": 2024,
  "approval_record_exists": false,
  "manual_odds_exists": false,
  "exit_code": 1
}
```

---

## Test Results

| Test File | Tests | Result |
|-----------|-------|--------|
| `test_p37_5_manual_approval_docs.py` | 43 | ✅ ALL PASS |
| `test_check_p37_manual_odds_package.py` | 35 | ✅ ALL PASS |
| **P37.5 subtotal** | **78** | ✅ ALL PASS |
| P37 tests (prior) | 119 | ✅ ALL PASS (no regression) |
| **P37 + P37.5 combined** | **203** | ✅ ALL PASS |

```
============================= 203 passed in 5.34s ==============================
```

---

## Determinism Check

```
DETERMINISM_CHECK=PASSED
```

Running the checker twice produces identical `p37_5_status`, `exit_code`, `paper_only`, and `raw_odds_commit_allowed` values.  Only `generated_at` (timestamp) varies.

---

## Safety Invariants Verified

| Invariant | Status |
|-----------|--------|
| `PAPER_ONLY=True` enforced in script | ✅ |
| `PRODUCTION_READY=False` enforced in script | ✅ |
| `raw_odds_commit_allowed=False` in all outputs | ✅ |
| `data/mlb_2024/manual_import/` NOT staged | ✅ |
| `data/mlb_2024/raw/gl2024.txt` NOT staged | ✅ |
| No HTTP requests in checker script | ✅ |
| No `git add` / `git commit` in checker script | ✅ |
| Example JSON has `production_ready=false` | ✅ |
| Example JSON has `paper_only=true` | ✅ |
| Example JSON has all 17 required fields | ✅ |
| Example CSV has all 11 required columns | ✅ |

---

## Committed Files (11)

```
docs/betting/manual_odds_approval/P37_5_APPROVAL_PACKAGE.md
docs/betting/manual_odds_approval/P37_5_OPERATOR_CHECKLIST.md
docs/betting/manual_odds_approval/P37_5_PROVIDER_TOS_REVIEW_TEMPLATE.md
docs/betting/manual_odds_approval/P37_5_MANUAL_IMPORT_RUNBOOK.md
docs/betting/manual_odds_approval/odds_approval_record_EXAMPLE_PLACEHOLDER.json
docs/betting/manual_odds_approval/odds_2024_approved_EXAMPLE_TEMPLATE.csv
scripts/check_p37_manual_odds_package.py
tests/test_p37_5_manual_approval_docs.py
tests/test_check_p37_manual_odds_package.py
data/mlb_2024/processed/p37_manual_odds_provisioning/p37_5_manual_package_check.json
00-BettingPlan/20260513/p37_5_manual_odds_approval_package_report.md
```

**NOT committed** (operator-filled, private):
```
data/mlb_2024/manual_import/odds_approval_record.json
data/mlb_2024/manual_import/odds_2024_approved.csv
```

---

## Gate State After P37.5

| Gate | Status |
|------|--------|
| P37 gate | `P37_BLOCKED_APPROVAL_RECORD_MISSING` (unchanged — operator action required) |
| P37.5 package | `P37_5_MANUAL_ODDS_APPROVAL_PACKAGE_READY` |

P37 remains blocked until an operator follows the runbook and provisions the two
manual files.  When they do, re-running the P37 gate with `--approval-record` and
`--manual-odds-file` will move the state to `P37_MANUAL_ODDS_PROVISIONING_GATE_READY`.

---

## Next Phase

**P38**: Build 2024 Licensed Odds Import Artifact

Triggered when:
- `data/mlb_2024/manual_import/odds_approval_record.json` is provisioned and valid
- `data/mlb_2024/manual_import/odds_2024_approved.csv` is provisioned and valid
- P37 gate returns `P37_MANUAL_ODDS_PROVISIONING_GATE_READY` (exit=0)

---

*Generated: 2026-05-13T06:49:25Z | PAPER_ONLY=True | PRODUCTION_READY=False | SEASON=2024*
