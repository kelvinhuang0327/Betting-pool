# P88 — Regeneration Authorization Gate

## Classification

`P88_AWAITING_EXPLICIT_REGENERATION_AUTHORIZATION`

## Authorization Status

**NOT GRANTED**

Required phrase: `YES regenerate stale downstream artifacts for P87 recovery`

## Gate Check Results

- P87 classification confirmed: `P87_REGENERATION_REQUIRED_AWAITING_EXPLICIT_YES`
- P86 classification confirmed: `P86_ARTIFACT_CONTRACT_FAILED_STALE_DOWNSTREAM_RISK`
- count_match: True
- game_id_full_coverage: True
- content_drift_likely: False
- stale_by_mtime_only: True
- safe_without_explicit_yes: False
- all_preconditions_met: True

## What P88 Did NOT Do

- P88 did not regenerate artifacts
- P88 did not overwrite frozen outputs
- P88 did not run P84E / P84F / P84G / P84H / P85 / P86 recovery
- P88 only prepared the authorization gate and readiness plan

## Governance

- paper_only = true
- diagnostic_only = true
- production_ready = false
- ev_computed = false
- clv_computed = false
- kelly_computed = false
- odds_used = false
- live_api_calls = 0
- paid_api_called = false
- no_canonical_row_rewrite = true
- no_outcome_row_rewrite = true
- no_historical_artifact_overwrite = true
- no_calibration_refit = true
- no_production_betting_recommendation = true
- no real bet instruction issued
- no stake calculation
- no EV / CLV / Kelly computation
- no Taiwan lottery betting recommendation

## Regeneration Order (After Future Authorization Only)

- **Step 1 [P84E]**: Rerun outcome attachment against current canonical_rows (828 rows)
- **Step 2 [P84F]**: Rerun predicted-side calibration diagnostic
- **Step 3 [P84G]**: Rerun side mapping fix and metrics regeneration
- **Step 4 [P84H]**: Rerun corrected signal validation and coverage guard
- **Step 5 [P85]**: Rerun prediction convention invariant gate
- **Step 6 [P86]**: Rerun artifact regeneration dependency contract
- **Step 7 [VERIFY]**: Verify P86 classification upgraded to READY
- **Step 8 [TEST]**: Run P83A–P88 targeted regression
- **Step 9 [COMMIT]**: Commit whitelist-only regenerated artifacts

## Allowed Classifications

- `P88_AWAITING_EXPLICIT_REGENERATION_AUTHORIZATION`
- `P88_REGENERATION_AUTHORIZED_READY_TO_EXECUTE`
- `P88_AUTHORIZATION_GATE_FAILED_P87_STATE_MISMATCH`
- `P88_AUTHORIZATION_GATE_FAILED_P86_STATE_MISMATCH`
- `P88_AUTHORIZATION_GATE_BLOCKED_BY_PREFLIGHT`
- `P88_AUTHORIZATION_GATE_BLOCKED_BY_SCOPE_DRIFT`

---

*Generated at 2026-05-27T08:10:01.219175+00:00 UTC*