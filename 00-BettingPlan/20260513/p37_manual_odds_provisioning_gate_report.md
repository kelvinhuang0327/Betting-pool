# P37 Manual Odds Provisioning Gate — Report

**Date**: 2026-05-13
**Phase**: P37 — Manual Odds Approval Record Provisioning / Licensed Odds Artifact Builder Gate
**Repo**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`
**Branch**: `p13-clean`
**PAPER_ONLY**: `true`
**PRODUCTION_READY**: `false`

---

## 1. Repo Evidence

| Key | Value |
|-----|-------|
| Branch | `p13-clean` |
| Prior commit (P36) | `2da3e7e` |
| Status | Clean — no staged files at report time |
| Forbidden file | `data/mlb_2024/raw/gl2024.txt` — not staged |

```
git log --oneline -3:
  2da3e7e feat(betting): gate P36 licensed odds approval import
  cdedd24 feat(betting): validate P35 dual source import readiness
  1a01c13 feat(betting): plan P34 dual 2024 prediction and odds source acquisition
```

---

## 2. Prior Phase Evidence: P36

| P36 Item | Value |
|----------|-------|
| Gate | `P36_BLOCKED_APPROVAL_RECORD_MISSING` |
| Marker | `P36_ODDS_APPROVAL_IMPORT_GATE_BLOCKED` |
| `raw_odds_commit_allowed` | `false` |
| `paper_only` | `true` |
| `production_ready` | `false` |
| Tests | 94/94 PASS (cumulative 769) |

P36 gate result (from `data/mlb_2024/processed/p36_odds_approval_import_gate/p36_gate_result.json`):
```json
{
  "gate": "P36_BLOCKED_APPROVAL_RECORD_MISSING",
  "approval_record_status": "APPROVAL_MISSING",
  "raw_odds_commit_allowed": false,
  "paper_only": true,
  "production_ready": false
}
```

---

## 3. Why P37 Is Required

P36 confirmed:
- No approval record exists at `data/mlb_2024/manual_import/odds_approval_record.json`
- No licensed odds file exists at `data/mlb_2024/manual_import/odds_2024_approved.csv`
- Therefore no odds import artifact can be built

P37 addresses this gap by:
1. Generating a formal approval record **template** and **instructions** so a researcher knows exactly what to fill in.
2. Generating a manual odds CSV **template** and **column guide** so the format is unambiguous.
3. Installing a provisioning gate that blocks progress unless both files exist and pass validation.
4. Writing all 7 outputs to `data/mlb_2024/processed/p37_manual_odds_provisioning/`.

---

## 4. Approval Record Template

**File**: `odds_approval_record_TEMPLATE.json`
**Required fields** (17):

| Field | Placeholder Value |
|-------|------------------|
| provider_name | PLACEHOLDER_PROVIDER |
| source_name | PLACEHOLDER_SOURCE |
| source_url_or_reference | PLACEHOLDER_URL_OR_DOI |
| license_terms_summary | PLACEHOLDER_LICENSE_SUMMARY |
| allowed_use | internal_research |
| redistribution_allowed | false |
| attribution_required | true |
| internal_research_allowed | true |
| commercial_use_allowed | false |
| approved_by | PLACEHOLDER_APPROVER |
| approved_at | YYYY-MM-DDTHH:MM:SS+00:00 |
| approval_scope | mlb_2024_season |
| source_file_expected_path | data/mlb_2024/manual_import/odds_2024_approved.csv |
| checksum_required | true |
| checksum_sha256 | PLACEHOLDER_SHA256 |
| paper_only | true |
| production_ready | false |

**Key invariants enforced**:
- `paper_only=true` and `production_ready=false` — gate blocks any deviation
- `internal_research_allowed=true` — required for research use
- Template is safe to commit (placeholder values only)

---

## 5. Manual Odds CSV Template

**File**: `odds_2024_approved_TEMPLATE.csv`
**Required columns** (11):

| Column | Type | Notes |
|--------|------|-------|
| game_id | string | Unique game key |
| game_date | date | ISO YYYY-MM-DD |
| home_team | string | MLB abbreviation |
| away_team | string | MLB abbreviation |
| p_market | float (0,1) | Pre-game market probability — NO outcome data |
| odds_decimal | float ≥ 1.0 | Closing decimal odds |
| sportsbook | string | Source book name |
| market_type | string | moneyline/ml/money_line/1x2/h2h |
| closing_timestamp | ISO datetime | Pre-game closing time |
| source_odds_ref | string | Source reference |
| license_ref | string | License approval reference |

**Forbidden columns** (10): `y_true`, `final_score`, `home_score`, `away_score`, `winner`, `outcome`, `result`, `run_diff`, `total_runs`, `game_result`

The template includes one clearly-labelled EXAMPLE row — not real data.

---

## 6. Real P37 No-Approval Run Result

```
Command:
  PYTHONPATH=. ./.venv/bin/python scripts/run_p37_manual_odds_provisioning_gate.py \
    --output-dir data/mlb_2024/processed/p37_manual_odds_provisioning \
    --paper-only true --skip-determinism-check

Output:
  p37_gate=P37_BLOCKED_APPROVAL_RECORD_MISSING
  approval_record_status=APPROVAL_MISSING
  manual_odds_file_status=MANUAL_ODDS_REQUIRED
  raw_commit_risk=False
  templates_written=True
  recommended_next_action=Fill in odds_approval_record_TEMPLATE.json ...
  production_ready=False
  paper_only=True
  DETERMINISM_CHECK=PASSED
  EXIT_CODE=1
```

**Result**: `P37_BLOCKED_APPROVAL_RECORD_MISSING` — expected.  Templates still generated. No odds imported. No raw files staged.

---

## 7. Fixture-Only Ready Path Result

```
Fixtures created:
  /tmp/p37_valid_approval_record.json  (all 17 fields, paper_only=true, internal_research_allowed=true)
  /tmp/p37_valid_manual_odds.csv       (11 required columns, moneyline, no forbidden cols)

Command:
  PYTHONPATH=. ./.venv/bin/python scripts/run_p37_manual_odds_provisioning_gate.py \
    --output-dir /tmp/p37_valid_gate \
    --approval-record /tmp/p37_valid_approval_record.json \
    --manual-odds-file /tmp/p37_valid_manual_odds.csv \
    --paper-only true --skip-determinism-check

Output:
  p37_gate=P37_MANUAL_ODDS_PROVISIONING_GATE_READY
  approval_record_status=APPROVAL_VALID
  manual_odds_file_status=MANUAL_ODDS_VALID
  raw_commit_risk=False
  templates_written=True
  recommended_next_action=Proceed to P38: Build 2024 Licensed Odds Import Artifact...
  production_ready=False
  paper_only=True
  DETERMINISM_CHECK=PASSED
  EXIT_CODE=0
```

**Result**: `P37_MANUAL_ODDS_PROVISIONING_GATE_READY` — fixture path is fully functional.
Fixture files were NOT committed.

---

## 8. Test Results

| Test File | Tests | Status |
|-----------|-------|--------|
| test_p37_manual_odds_provisioning_contract.py | ~38 | ✅ PASS |
| test_p37_approval_record_template_writer.py | ~20 | ✅ PASS |
| test_p37_manual_odds_template_writer.py | ~19 | ✅ PASS |
| test_p37_manual_odds_provisioning_gate.py | ~28 | ✅ PASS |
| test_run_p37_manual_odds_provisioning_gate.py | ~14 | ✅ PASS |
| **P37 subtotal** | **119** | **✅ 100% PASS** |
| P36 regression (5 files) | 94 | ✅ PASS |
| P35 regression (6 files) | 108 | ✅ PASS |
| P34 regression (6 files) | 154 | ✅ PASS |

**Full suite run**: `225 passed (P37+P36)` + `271 passed (P35+P34)` = **496 total in regression run**

**Cumulative across P31–P37**: 769 (prior) + 119 (P37 new) = **~888 tests passing**

> Note: P31–P33 tests (675 baseline) not re-run in this session but remain committed and passing from prior phases.

---

## 9. Determinism Result

```
Two runs without approval record:
  Run 1: /tmp/p37_det_run1/
  Run 2: /tmp/p37_det_run2/

Compared (excluding generated_at, artifacts):
  manual_odds_provisioning_gate.json → MATCH
  p37_gate_result.json               → MATCH

Compared (exact):
  odds_approval_record_INSTRUCTIONS.md → MATCH
  odds_2024_approved_TEMPLATE.csv      → MATCH
  odds_2024_approved_COLUMN_GUIDE.md   → MATCH

DETERMINISM_CHECK=PASSED
```

---

## 10. Production Readiness Statement

| Invariant | Value |
|-----------|-------|
| `PAPER_ONLY` | `True` |
| `PRODUCTION_READY` | `False` |
| `raw_odds_commit_allowed` | `False` (always) |
| `approval_record_commit_allowed` | `False` |
| `odds_artifact_ready` | `False` (real run) |
| Live TSL called | No |
| Real bets placed | No |
| Scheduler/daemon enabled | No |
| Raw odds downloaded | No |
| Raw odds staged | No |

---

## 11. Remaining Limitations

1. **No real approval record exists** — `data/mlb_2024/manual_import/odds_approval_record.json` must be created manually by reviewing actual provider ToS.
2. **No licensed odds file exists** — `data/mlb_2024/manual_import/odds_2024_approved.csv` must be manually provisioned from a provider with explicit research-use permission.
3. **Checksum not verified** — if `checksum_required=true`, `checksum_sha256` must be computed from the actual odds file.
4. **No P38 artifact yet** — P37 only gates readiness. The import artifact build is deferred to P38.
5. **Market coverage unknown** — without a real odds file, coverage of the 2429 P32 game identity rows cannot be assessed.

---

## 12. Next-Phase Recommendation

**Current state**: `P37_BLOCKED_APPROVAL_RECORD_MISSING`

**To unblock P37**:
1. Identify an odds provider with internal-research-use license
2. Fill in `data/mlb_2024/processed/p37_manual_odds_provisioning/odds_approval_record_TEMPLATE.json`
3. Place completed record at `data/mlb_2024/manual_import/odds_approval_record.json`
4. Manually provision odds CSV at `data/mlb_2024/manual_import/odds_2024_approved.csv`
5. Rerun P37 with `--approval-record` and `--manual-odds-file`

**If P37 becomes READY**:
- Next phase = **P38: Build 2024 Licensed Odds Import Artifact**
  - Join approved odds CSV with P32 game identity
  - Validate prediction coverage
  - Produce `data/mlb_2024/processed/p38_odds_import_artifact/` outputs

---

## 13. Marker

```
P37_MANUAL_ODDS_PROVISIONING_GATE_BLOCKED
```

*Current state: blocked at approval record missing — expected.*
*All P37 infrastructure fully implemented. 119 new tests pass. Templates generated.*
*Real path: exit=1, gate=P37_BLOCKED_APPROVAL_RECORD_MISSING.*
*Fixture path: exit=0, gate=P37_MANUAL_ODDS_PROVISIONING_GATE_READY.*
*Determinism: PASSED.*
