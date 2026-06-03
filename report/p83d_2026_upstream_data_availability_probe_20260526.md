# P83D — 2026 Upstream Data Availability Probe
**Date:** 2026-05-26
**Classification:** `P83D_AWAITING_UPSTREAM_DATA`
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Summary

P83D probes all local filesystem paths for upstream 2026 data required by
P83C's upstream input contract. No external API calls are made.

**Result:** `P83D_AWAITING_UPSTREAM_DATA`

---

## P83C State Verification

| Field | Value |
|---|---|
| Classification | `P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA` |
| Classification OK | True |
| live_api_calls | 0 |
| Canonical prediction path | `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl` |
| Upstream contract ID | `P83C_UPSTREAM_INPUT_CONTRACT_V1` |
| Snapshot unlock blocked | True |
| Mock rows noncanonical | True |

---

## Upstream Probe Results

### Directories Probed
- `data/mlb_2026`
- `data/mlb_2026/derived`
- `outputs/recommendations/PAPER`
- `outputs/predictions/PAPER`

### Directories Missing
- `data/mlb_2026/schedule`
- `data/mlb_2026/pitchers`
- `data/mlb_2026/features`
- `data/mlb_2026/model_outputs`
- `data/mlb_2026/predictions`
- `outputs/online_validation`

### File Classification

| Category | File Count |
|---|---|
| schedule_candidate | 0 |
| pitcher_feature_candidate | 0 |
| model_probability_candidate | 0 |
| canonical_prediction_candidate | 0 |
| runtime_paper_candidate | 103 |
| contract_artifact | 6 |
| noncanonical | 0 |

### Runtime PAPER Files (2026)
- **File count:** 2
- **Noncanonical:** True (per P83B contract)
- **Files:** ['outputs/recommendations/PAPER/2026-05-11/2026-05-11-AWY-HOM-824441.jsonl', 'outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl']

### Canonical Prediction File
- **Path:** `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl`
- **Exists:** False
- **Row count:** 0

---

## Readiness Gate Table

| Gate | Status | Note |
|---|---|---|
| SCHEDULE_GATE | ❌ FAIL | Runtime PAPER files have game_id only (in filename pattern). No canonical data/m |
| PITCHER_FEATURE_GATE | ❌ FAIL | No data/mlb_2026/pitchers/ directory or file with home_sp_fip / away_sp_fip. 202 |
| MODEL_OUTPUT_GATE | ❌ FAIL | Runtime PAPER files have model_prob_home/away in recommendation schema. Canonica |
| PREDICTED_SIDE_GATE | ❌ FAIL | Deterministic logic defined in P83C. Blocked because pitcher FIP inputs unavaila |
| GOVERNANCE_GATE | ✅ PASS | Governance flags are pre-defined constants. No upstream data needed. |
| PRODUCER_ACTIVATION_GATE | ❌ FAIL | Blocked by 4 failing prerequisite gate(s). |

**Passing gates:** 1 / 6

---

## Producer Activation Status

| Field | Value |
|---|---|
| activation_allowed | False |
| canonical_rows_written | False |
| canonical_prediction_exists | False |
| Reason | Blocked by failing gates: ['SCHEDULE_GATE', 'PITCHER_FEATURE_GATE', 'MODEL_OUTPUT_GATE', 'PREDICTED_SIDE_GATE', 'PRODUCER_ACTIVATION_GATE'] |

---

## Missing Data Checklist

- **SCHEDULE_GATE** [HIGH]: 2026 MLB game schedule with game_id, game_date, home_team, away_team
  - Expected path: `data/mlb_2026/schedule/mlb_2026_schedule.jsonl`
  - Source hint: statsapi.mlb.com schedule endpoint OR manual fixture for testing
- **PITCHER_FEATURE_GATE** [HIGH]: 2026 starting pitcher FIP stats: home_sp_fip, away_sp_fip per game
  - Expected path: `data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl`
  - Source hint: statsapi.mlb.com pitcher stats OR 2026 FIP lookup table
- **MODEL_OUTPUT_GATE** [HIGH]: Canonical model_probability + source_prediction_version per game (P83B schema)
  - Expected path: `data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl`
  - Source hint: Apply 2025-trained ensemble model to 2026 features. Runtime PAPER files have model_prob_home/away but not in P83B format.
- **PREDICTED_SIDE_GATE** [DEPENDENT]: sp_fip_delta (computed from home_sp_fip - away_sp_fip)
  - Expected path: `derived from PITCHER_FEATURE_GATE data`
  - Source hint: Unblocked automatically once PITCHER_FEATURE_GATE passes

### Rerun Triggers
- When data/mlb_2026/schedule/ contains canonical game schedule file
- When data/mlb_2026/pitchers/ contains 2026 SP FIP features
- When data/mlb_2026/model_outputs/ contains canonical model output file
- When all 3 HIGH priority items above are resolved

---

## Future P83E Prompt

```
[P83E — 2026 Canonical Prediction Row Producer]

# Prerequisites
- P83D classification must be P83D_PRODUCER_ACTIVATION_READY
- P83D commit must be present on main branch

# Trigger conditions
Run P83E only when ALL of the following files exist locally:
  1. data/mlb_2026/schedule/mlb_2026_schedule.jsonl    (game_id, game_date, home_team, away_team)
  2. data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl    (game_id, home_sp_fip, away_sp_fip)
  3. data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl    (game_id, model_probability, source_prediction_version)

# Goal
P83E must:
  1. Re-run P83D probe to confirm all gates now pass.
  2. Join schedule + pitcher features + model outputs by game_id.
  3. Compute sp_fip_delta, abs_sp_fip_delta, predicted_side, rule flags.
  4. Enforce governance: paper_only=True, diagnostic_only=True, odds_used=False.
  5. Write canonical rows to: data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl
  6. Update P83A snapshot unlock gate.
  7. Update P83D summary with producer_activated=True.

# Rules
- No external API calls
- No odds data
- No edge / EV / CLV / Kelly calculation
- Keep paper_only=True, diagnostic_only=True
- Do NOT fabricate pitcher FIP values

```

---

## Governance Invariants

| Invariant | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| live_api_calls | 0 |
| odds_used | False |
| ev_calculated | False |
| clv_calculated | False |
| kelly_calculated | False |
| kelly_deploy_allowed | False |
| production_ready | False |
| real_bet_allowed | False |
| profitability_claim | False |
| canonical_rows_written_in_p83d | False |
| forbidden_scan_pass | True |

---

## Final Classification

**`P83D_AWAITING_UPSTREAM_DATA`**

P83D is a local-only upstream data availability probe. No external API calls are made. No market edge is computed. No canonical 2026 prediction rows are written unless upstream is complete and task explicitly authorizes activation. paper_only=True, diagnostic_only=True.
