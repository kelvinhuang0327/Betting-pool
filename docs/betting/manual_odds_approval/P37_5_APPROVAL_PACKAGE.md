# P37.5 Manual Odds Approval Package

**Phase**: P37.5 — Manual Odds Approval Package Preparation
**Status**: `P37_5_MANUAL_ODDS_APPROVAL_PACKAGE_READY`
**Prior gate**: `P37_MANUAL_ODDS_PROVISIONING_GATE_BLOCKED`
**PAPER_ONLY**: `true`
**PRODUCTION_READY**: `false`
**Season**: 2024

---

## Purpose

This package provides everything an operator needs to manually provision a valid
licensed 2024 MLB odds dataset and unblock the P38 licensed odds import artifact
build.

P37 is currently blocked at `P37_BLOCKED_APPROVAL_RECORD_MISSING`.  No automated
scraping, downloading, or fabrication of odds is permitted.  All odds data must
come from a provider whose Terms of Service explicitly allow internal research use.

---

## Package Contents

| File | Purpose |
|------|---------|
| `P37_5_APPROVAL_PACKAGE.md` | This file — overview and index |
| `P37_5_OPERATOR_CHECKLIST.md` | Step-by-step checklist for operator |
| `P37_5_PROVIDER_TOS_REVIEW_TEMPLATE.md` | Template for documenting ToS review |
| `P37_5_MANUAL_IMPORT_RUNBOOK.md` | End-to-end runbook for provisioning |
| `odds_approval_record_EXAMPLE_PLACEHOLDER.json` | Example-only approval record (PLACEHOLDER values) |
| `odds_2024_approved_EXAMPLE_TEMPLATE.csv` | Example-only odds CSV header + EXAMPLE row |

---

## Gate Architecture

```
P36  →  P37 gate  →  P37.5 package  →  [operator provisions manually]
                                            ↓
                                       P37 re-run with --approval-record + --manual-odds-file
                                            ↓
                                       P37_MANUAL_ODDS_PROVISIONING_GATE_READY
                                            ↓
                                       P38: Build 2024 Licensed Odds Import Artifact
```

---

## What Must Be Manually Reviewed Before Using Odds Data

Before any odds data may be used in this research pipeline, the operator must:

1. **Identify an odds provider** whose Terms of Service explicitly allow:
   - Internal / personal / academic research use
   - Non-commercial use
   - The specific 2024 MLB season historical odds

2. **Read the full ToS** of the chosen provider.  Confirm:
   - `internal_research_allowed = true`
   - `commercial_use_allowed = false`
   - `redistribution_allowed` may be false (acceptable)
   - No clause prohibits offline / archival research use

3. **Document the review** using `P37_5_PROVIDER_TOS_REVIEW_TEMPLATE.md`.

4. **Fill in the approval record** using `odds_approval_record_EXAMPLE_PLACEHOLDER.json` as a guide.

5. **Never commit raw odds or filled approval records** to the git repository.

---

## What This Package Does NOT Do

- Does not download odds automatically.
- Does not scrape any website.
- Does not fabricate `p_market` values.
- Does not infer odds from game outcomes.
- Does not bypass the P37 gate.
- Does not enable production betting.
- Does not connect to live TSL or any sportsbook API.

---

## Critical Invariants

| Invariant | Value |
|-----------|-------|
| `PAPER_ONLY` | `true` |
| `PRODUCTION_READY` | `false` |
| `raw_odds_commit_allowed` | `false` (always) |
| `approval_record_commit_allowed` | `false` |
| `odds_artifact_ready` | `false` (until P37 READY) |

---

## Manual Target Paths (DO NOT COMMIT)

```
data/mlb_2024/manual_import/odds_approval_record.json   ← filled by operator
data/mlb_2024/manual_import/odds_2024_approved.csv      ← provisioned by operator
```

Both paths are excluded from git staging by the P37 gate safety checks.

---

## Next Phase

Once both manual files exist and pass P37 validation:

```
./.venv/bin/python scripts/run_p37_manual_odds_provisioning_gate.py \
  --output-dir data/mlb_2024/processed/p37_manual_odds_provisioning \
  --approval-record data/mlb_2024/manual_import/odds_approval_record.json \
  --manual-odds-file data/mlb_2024/manual_import/odds_2024_approved.csv \
  --paper-only true
```

Expected on success:
```
p37_gate=P37_MANUAL_ODDS_PROVISIONING_GATE_READY
EXIT_CODE=0
```

Then proceed to: **P38 Build 2024 Licensed Odds Import Artifact**

---

*Generated: 2026-05-13 | PAPER_ONLY=True | PRODUCTION_READY=False | SEASON=2024*
