# P206A Duplicate-Ticket Reduction Dry Run

This is a local historical/replay dry run only. It is not a future prediction, betting recommendation, EV/ROI/payout/Kelly claim, activation claim, live-market claim, production change, DB mutation, real publication, or future-ticket mutation.

## Summary

- Dry-run input rows: 2
- Duplicate/overlap groups: 1
- Kept rows: 1
- Suppressed rows: 1
- Suppression rate: 50.00%
- Missing stable identity rows: 0
- Missing selected side rows: 0
- Missing market/bet type rows: 0

## Observed Duplicate Patterns

- `game=824441|side=home|market=moneyline`: 2 rows, 1 suppressed, 1 strategy attribution set(s).

## Policy Inventory

- Grouping uses stable game identity, selected side, and market/bet type only.
- Exact duplicate suppression additionally requires materially equivalent strategy attribution.
- Stable identity is ID-based; team names, dates, and text labels are not fuzzy-matched.
- Missing stable identity, selected side, or market/bet type is fail-closed and kept as ungroupable.
- P205A/P205B learning boundaries are preserved; this dry run only reports provenance contract version and learning guard status.

## Row Decisions

| row | status | group_key | keep_reason | suppress_reason | learning_guard_status | provenance_contract_version |
|---:|---|---|---|---|---|---|
| 0 | kept | `game=824441|side=home|market=moneyline` | keep_first_in_duplicate_set |  | legacy_contract |  |
| 1 | suppressed | `game=824441|side=home|market=moneyline` |  | suppress_exact_duplicate_same_identity_side_market_strategy | legacy_contract |  |
