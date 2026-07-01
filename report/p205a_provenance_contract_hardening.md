# P205A Provenance Contract Hardening

## Status

- Task: P205A isolated worktree provenance contract implementation.
- Worktree: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p205a`
- Branch: `task/p205a-provenance-contract-hardening`
- Base: `origin/main` at `0e52b1c1191d9adcf82a40af07707039df08e283`
- Contract version: `p205a.v1`
- Classification: `P205A_PROVENANCE_CONTRACT_PR_OPENED` pending PR creation.

## Contract Fields

`provenance_contract_version`, `prediction_input_mode`, `prediction_source`,
`prediction_source_id`, `model_version`, `feature_fingerprint`,
`prediction_as_of_utc`, `game_specific`, `selected_side_method`, `odds_source`,
`odds_is_market_observed`, `edge_is_real_evidence`, `learning_eligible`,
`learning_block_reason`.

## Implementation Summary

- Added a centralized fail-closed provenance contract builder, validator, serializer,
  and explicit strategy attribution helper.
- Path 1 paper recommendation now emits versioned `source_trace` for its neutral /
  fixed-prior paper-only path, keeps estimated odds separate from observed market
  evidence, and forces `BLOCKED_PAPER_ONLY` paper stake to zero.
- Path 2 daily advisory now emits the same versioned `source_trace` with
  `historical_no_vig` odds, `edge_is_real_evidence=False`, and
  `learning_eligible=False`.
- Scheduler paper recommendation wrapper now attributes `strategy_id` only from the
  loaded simulation object's explicit `strategy_name`.
- `MlbTslRecommendationRow` rejects legacy or missing-contract `source_trace` values
  that try to claim `learning_eligible=True`, while legacy ineligible rows remain
  backward-compatible.

## Validation Results

- Contract validation rejects string booleans, missing required fields, invalid
  learning eligibility combinations, and real-edge claims from `estimated` or
  `historical_no_vig` odds.
- Path 1 provenance: `game_specific=False`, `odds_source=estimated`,
  `odds_is_market_observed=False`, `edge_is_real_evidence=False`,
  `learning_eligible=False`, explicit paper-only block reason, `stake_units_paper=0`.
- Path 2 provenance: `prediction_input_mode=historical_replay`,
  `odds_source=historical_no_vig`, `odds_is_market_observed=False`,
  `edge_is_real_evidence=False`, `learning_eligible=False`, explicit historical
  replay/proxy block reason.
- Evaluator compatibility: read-only evaluator still treats only literal boolean
  `True` as eligible; P205A row validation prevents legacy/missing-contract rows
  from newly claiming eligibility.

## Tests

- `pytest -q tests/test_p205a_provenance_contract_hardening.py` — PASS, 14 passed.
- `pytest -q tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py` — PASS,
  35 passed.
- `pytest -q tests/test_mlb_paper_evaluator.py tests/test_p180_strategy_leaderboard.py`
  — PASS, 55 passed.
- `pytest -q tests/test_mlb_daily_advisory.py tests/test_mlb_daily_scheduler.py -k 'not phase67_72_orchestrators_importable'`
  — PASS, 77 passed, 1 deselected.
- `pytest -q tests/test_mlb_daily_advisory.py tests/test_mlb_daily_scheduler.py` —
  FAIL, 77 passed / 1 failed due missing local `sklearn` dependency while importing
  `orchestrator.phase69_calibration_objective_redesign_counterfactual`; this is not
  a P205A behavior failure and would require environment/package action outside the
  whitelist.

Full repository regression: NOT RUN.

## Explicitly Deferred

- P205B full game-id outcome join.
- Duplicate policy.
- Freshness/as-of gate.
- Evaluator semantic change.
- Leaderboard change.
- Live/current source hooks.
- DB, registry, production, publication, deployment, model promotion, and strategy
  activation.

## External Effects

- DB writes: none.
- Registry mutation: none.
- Live provider or live odds use: none.
- Production writes: none.
- Publication: none.
- Future-ticket mutation: none.
