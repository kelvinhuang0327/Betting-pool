# P205B Learning Outcome Join Guard

## Status

- Task: P205B-A learning outcome join and freshness/as-of guard.
- Worktree: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p205b`
- Branch: `task/p205b-learning-outcome-join-guard`
- Base: `origin/main` at `2e5f22ac905c663f6b855ebd92a6d649db2dbf34`
- Scope: local/replay-only learning eligibility guard.

## Implementation Summary

- Added `wbc_backend.recommendation.learning_outcome_join` as the centralized fail-closed guard.
- The guard requires a valid `p205a.v1` provenance contract before learning eligibility can pass.
- The guard requires stable game identity from explicit `game_pk`/`gamePk`/`mlb_game_pk` or a stable numeric game-id suffix; it does not fuzzy-match teams, dates, or names.
- The guard rejects missing outcomes and duplicate/ambiguous outcome identities for learning eligibility.
- The guard requires `prediction_as_of_utc` to parse and be strictly before the result timestamp.
- The guard fails closed when the result timestamp is absent.
- The evaluator uses the guard for versioned P205A rows or rows with result timestamps to reject/annotate learning-ineligible rows only; scoring, matched-count behavior, segmentation calculations, and leaderboard ranking sort are unchanged.
- Tightened the P205A provenance validator so `learning_eligible=True` also requires observed market odds and real edge evidence, and cannot use `estimated` or `historical_no_vig` odds.

## Explicit Block Reasons

- `missing_contract`
- `legacy_contract`
- `malformed_contract`
- `not_learning_eligible`
- `missing_game_id`
- `outcome_not_found`
- `ambiguous_outcome_join`
- `missing_prediction_as_of_utc`
- `stale_or_invalid_as_of`
- `result_timestamp_missing`

## Guard Contract And Field Inventory

Required provenance remains the P205A contract:

`provenance_contract_version`, `prediction_input_mode`, `prediction_source`,
`prediction_source_id`, `model_version`, `feature_fingerprint`,
`prediction_as_of_utc`, `game_specific`, `selected_side_method`, `odds_source`,
`odds_is_market_observed`, `edge_is_real_evidence`, `learning_eligible`,
`learning_block_reason`.

Additional P205B learning acceptance checks:

- stable recommendation game identity is present.
- exactly one outcome exists for that stable identity.
- result timestamp exists on the outcome.
- `prediction_as_of_utc` parses as a timestamp before the result timestamp.

## Outcome Join Behavior

- Stable identity is exact and ID-based.
- Team names, game dates, and fuzzy text joins are not used as identity.
- Duplicate outcomes for the same stable identity block learning as `ambiguous_outcome_join`.
- Missing outcomes block learning as `outcome_not_found`.

## Freshness/As-Of Behavior

- Missing `prediction_as_of_utc` blocks learning as `missing_prediction_as_of_utc`.
- Invalid or stale prediction timestamps block learning as `stale_or_invalid_as_of`.
- Missing outcome result timestamps block learning as `result_timestamp_missing`.
- A prediction timestamp equal to the result timestamp is rejected; it must be strictly earlier.

## Evaluator Compatibility

- The evaluator still scores matched rows for auditability.
- The guard is used only for learning eligibility acceptance/rejection annotation.
- Leaderboard ranking logic remains unchanged.

## Explicit Non-Claims And Deferred Work

- No prediction accuracy claim.
- No EV, ROI, payout, CLV, or Kelly claim.
- No activation or live-market claim.
- No production behavior change.
- No DB write or runtime data mutation.
- No registry mutation.
- No live odds use.
- No publication or future-ticket mutation.
- Duplicate-ticket policy is deferred.
- Strategy optimization is deferred.

## Tests

- `pytest -q tests/test_p205b_learning_outcome_join_guard.py` - PASS, 13 passed.
- `pytest -q tests/test_p205a_provenance_contract_hardening.py` - PASS, 15 passed.
- `pytest -q tests/test_mlb_paper_evaluator.py` - PASS, 17 passed.
- Full repository regression: NOT RUN.

