# P37.5 Operator Checklist — Manual Odds Approval Provisioning

**Phase**: P37.5
**Gate to unblock**: `P37_MANUAL_ODDS_PROVISIONING_GATE_BLOCKED`
**PAPER_ONLY**: `true`
**PRODUCTION_READY**: `false`

---

## Pre-Flight Checks

- [ ] Confirmed repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`
- [ ] Confirmed branch: `p13-clean`
- [ ] Confirmed P37 gate: `P37_BLOCKED_APPROVAL_RECORD_MISSING`
- [ ] Confirmed `data/mlb_2024/manual_import/` directory exists (or create it)
- [ ] Confirmed no raw odds files are staged in git

---

## Phase A: Identify and Review Odds Provider

- [ ] **A1** — Choose an odds provider that allows internal/research use for MLB 2024
- [ ] **A2** — Navigate to the provider's Terms of Service page
- [ ] **A3** — Read the full ToS document
- [ ] **A4** — Confirm: `internal_research_allowed = true`
- [ ] **A5** — Confirm: `commercial_use_allowed = false`
- [ ] **A6** — Confirm: no prohibition on offline archival use
- [ ] **A7** — Document findings in `P37_5_PROVIDER_TOS_REVIEW_TEMPLATE.md`
- [ ] **A8** — Obtain provider name, source URL, and license reference string

---

## Phase B: Prepare Approval Record

- [ ] **B1** — Copy `odds_approval_record_EXAMPLE_PLACEHOLDER.json` to a working location
- [ ] **B2** — Replace ALL `PLACEHOLDER_*` values with real content
- [ ] **B3** — Set `allowed_use` to one of: `internal_research`, `research`, `personal_research`, `academic_research`
- [ ] **B4** — Set `internal_research_allowed = true`
- [ ] **B5** — Set `commercial_use_allowed = false`
- [ ] **B6** — Set `redistribution_allowed = false` (standard)
- [ ] **B7** — Set `paper_only = true` (MUST be true)
- [ ] **B8** — Set `production_ready = false` (MUST be false)
- [ ] **B9** — Set `approved_by` to your full name or role
- [ ] **B10** — Set `approved_at` to current ISO 8601 datetime
- [ ] **B11** — Set `approval_scope = "mlb_2024_season"`
- [ ] **B12** — Set `source_file_expected_path = "data/mlb_2024/manual_import/odds_2024_approved.csv"`
- [ ] **B13** — Place completed record at: `data/mlb_2024/manual_import/odds_approval_record.json`
- [ ] **B14** — Do NOT commit this file to git

---

## Phase C: Prepare Odds CSV

- [ ] **C1** — Obtain 2024 MLB historical closing odds from approved provider
- [ ] **C2** — Ensure odds reflect pre-game closing prices only (no post-game data)
- [ ] **C3** — Verify file has all required columns:
  - `game_id`, `game_date`, `home_team`, `away_team`
  - `p_market`, `odds_decimal`, `sportsbook`, `market_type`
  - `closing_timestamp`, `source_odds_ref`, `license_ref`
- [ ] **C4** — Verify file has NO forbidden columns:
  - `y_true`, `final_score`, `home_score`, `away_score`, `winner`
  - `outcome`, `result`, `run_diff`, `total_runs`, `game_result`
- [ ] **C5** — Verify `p_market` is in range (0, 1) — vig-adjusted probability
- [ ] **C6** — Verify `odds_decimal >= 1.0` for all rows
- [ ] **C7** — Verify `market_type` is one of: `moneyline`, `ml`, `money_line`, `1x2`, `h2h`
- [ ] **C8** — If `checksum_required = true` in approval record, compute:
  ```bash
  shasum -a 256 data/mlb_2024/manual_import/odds_2024_approved.csv
  ```
  Update `checksum_sha256` in approval record accordingly.
- [ ] **C9** — Place completed CSV at: `data/mlb_2024/manual_import/odds_2024_approved.csv`
- [ ] **C10** — Do NOT commit this file to git

---

## Phase D: Validate with P37 Gate

- [ ] **D1** — Run the manual package checker:
  ```bash
  PYTHONPATH=. ./.venv/bin/python scripts/check_p37_manual_odds_package.py
  ```
  Expected: both files found, validation proceeds.

- [ ] **D2** — Run the full P37 gate:
  ```bash
  PYTHONPATH=. ./.venv/bin/python scripts/run_p37_manual_odds_provisioning_gate.py \
    --output-dir data/mlb_2024/processed/p37_manual_odds_provisioning \
    --approval-record data/mlb_2024/manual_import/odds_approval_record.json \
    --manual-odds-file data/mlb_2024/manual_import/odds_2024_approved.csv \
    --paper-only true
  ```

- [ ] **D3** — Verify output:
  ```
  p37_gate=P37_MANUAL_ODDS_PROVISIONING_GATE_READY
  approval_record_status=APPROVAL_VALID
  manual_odds_file_status=MANUAL_ODDS_VALID
  EXIT_CODE=0
  ```

- [ ] **D4** — If gate is still BLOCKED, review the blocker_reason and fix the issue.

---

## Phase E: Safety Verification Before Any Commit

- [ ] **E1** — Confirm manual import files are NOT staged:
  ```bash
  git diff --cached --name-only | grep "manual_import" && echo "ERROR" || echo "OK"
  ```
- [ ] **E2** — Confirm raw odds file is NOT staged:
  ```bash
  git diff --cached --name-only | grep "raw/gl2024" && echo "ERROR" || echo "OK"
  ```
- [ ] **E3** — Do NOT stage `data/mlb_2024/manual_import/odds_approval_record.json`
- [ ] **E4** — Do NOT stage `data/mlb_2024/manual_import/odds_2024_approved.csv`

---

## Phase F: Proceed to P38

- [ ] **F1** — P37 gate confirmed READY
- [ ] **F2** — Proceed to P38: Build 2024 Licensed Odds Import Artifact
- [ ] **F3** — P38 will join the approved odds CSV with P32 game identity
- [ ] **F4** — P38 will produce `data/mlb_2024/processed/p38_odds_import_artifact/`

---

## Abort Conditions

Stop and report if any of these occur:
- Provider ToS does not allow internal research use
- Odds data appears to contain game outcomes (leakage detected)
- Approval record has `paper_only = false` or `production_ready = true`
- Any manual_import file gets staged in git
- Raw `gl2024.txt` gets staged

---

*PAPER_ONLY=True | PRODUCTION_READY=False | SEASON=2024 | DO NOT PUSH*
