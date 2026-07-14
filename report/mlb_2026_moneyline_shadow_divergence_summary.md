# 2026 Moneyline Shadow Outcome-Free Divergence Baseline

**Scope:** `OUTCOME_FREE_PAPER_DIAGNOSTIC_ONLY`

This report compares the existing P84-B Moneyline baseline with the P278 corrected Moneyline shadow. It measures prediction divergence only; it is not accuracy, performance, profitability, or evidence of model superiority.

## Comparison Contract

- Alignment key: exact `game_id` (never row order).
- Probability orientation: home-win probability for both sources.
- Signed delta: `P278 - P84-B`.
- Descriptive thresholds: `0.02`, `0.05`, `0.10` absolute probability delta.
- Percentiles: R-7 linear interpolation: h=(n-1)*q, interpolate between floor(h) and ceil(h).
- Outcome fields used: `NONE`.
- Odds fields used: `NONE`.
- Evaluation denominator: `0`.

## Alignment

- Total P84-B rows: `828`
- Total P278 rows: `828`
- Shared games: `828`
- Missing P84-B / P278: `0` / `0`
- Duplicate IDs: `0`
- Identity mismatches: `0`

## Divergence Summary

- Side agreement: `481` (`58.09%`)
- Side disagreement: `347` (`41.91%`)
- Mean signed delta: `0.033631`
- Mean absolute delta: `0.136676`
- Median / p90 / p95 absolute delta: `0.123973` / `0.264083` / `0.312073`
- Maximum absolute delta: `0.501189`
- Absolute delta >= `0.02`: `763` (`92.15%`)
- Absolute delta >= `0.05`: `664` (`80.19%`)
- Absolute delta >= `0.10`: `486` (`58.70%`)
- Confidence distance increased / decreased / unchanged: `200` / `628` / `0`

## Month-Level Descriptive Breakdown

| Month | Rows | Agree | Disagree | Mean Signed | Mean Abs | >=0.02 | >=0.05 | >=0.10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03 | 73 | 42 | 31 | 0.090870 | 0.153367 | 65 | 59 | 43 |
| 2026-04 | 389 | 224 | 165 | 0.020929 | 0.141049 | 365 | 319 | 237 |
| 2026-05 | 366 | 215 | 151 | 0.035715 | 0.128700 | 333 | 286 | 206 |

## Provenance and Output Fingerprints

- P84-B comparison fingerprint: `5a7b3c9c943de81d918ee9ce5692df1517f69387cc3a25e0bab21bae5e45d59c`
- P278 comparison fingerprint: `52f72dae5f89fa537dde425bdffc5de24c080f6b75eee6e6aca43b245563cddb`
- Ledger CSV SHA-256: `9d20925fd10a2f27c8cf3ed96e7ccfa4005278c60dc6f6978783299d5cfc8f3a`
- Deterministic summary payload SHA-256: `f3607ad9984049e2eb539408736dd93310052b884adebde7b2ff6326ff8495b9`
- Summary JSON file SHA-256: `7dd12d217651eb35569e0bcee241fcd24859c472b6b0e854a65105d8877998e0`
- Generated at (runtime metadata only): `2026-07-14T13:25:32.753895Z`
- Source Git commit (runtime metadata only): `1716a2db02e4beeeedfd1ddb8776d008110c472f`

## Boundary

- Neither model is activated, selected, deployed, or declared superior.
- Divergence thresholds are descriptive, not performance thresholds.
- Future performance evaluation requires prospectively available outcomes.
- No champion selection, publication, or betting action was performed.
