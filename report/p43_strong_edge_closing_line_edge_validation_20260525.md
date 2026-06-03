# P43 Strong-Edge Closing-Line Edge Validation (2026-05-25)

## Pre-flight result
- Repo/branch/HEAD pre-flight checks were executed before artifact generation.
- diagnostic_only and promotion_freeze governance locks are enabled.

## Data inventory
- 2025 quality rows (P41-compatible filter): 1428
- 2025 rows joined with closing line: 1426
- 2024 quality rows (P39 holdout): 2158
- 2024 rows with market probability available: 0

## Edge computation methodology
- Model home probability: sigmoid(0.8 * sp_fip_delta) (locked method from P40/P41/P42).
- Market home probability: no-vig normalization from CSV Home ML / Away ML.
- Side-aware edge: compare model and market probabilities on model-favored side.
- Neutral band: |edge| < 0.005.

## Tier breakdown table
| Tier | n | mean_edge | CI95 | positive_rate | classification |
|---|---:|---:|---|---:|---|
| A | 24 | 0.1391 | [0.1149, 0.1657] | 1.0000 | SAMPLE_LIMITED |
| B | 229 | 0.1334 | [0.1218, 0.1445] | 0.9476 | EDGE_CONFIRMED |
| C | 535 | 0.1059 | [0.0989, 0.1132] | 0.8953 | EDGE_CONFIRMED |

## Year-by-year table
| Year | Tier | n | mean_edge | CI95 | classification |
|---|---|---:|---:|---|---|
| 2024 | A | 0 | N/A | N/A | SAMPLE_LIMITED |
| 2024 | B | 0 | N/A | N/A | SAMPLE_LIMITED |
| 2024 | C | 0 | N/A | N/A | SAMPLE_LIMITED |
| 2025 | A | 24 | 0.1391 | [0.1149, 0.1657] | SAMPLE_LIMITED |
| 2025 | B | 229 | 0.1334 | [0.1218, 0.1445] | EDGE_CONFIRMED |
| 2025 | C | 535 | 0.1059 | [0.0989, 0.1132] | EDGE_CONFIRMED |
| combined | A | 24 | 0.1391 | [0.1149, 0.1657] | SAMPLE_LIMITED |
| combined | B | 229 | 0.1334 | [0.1218, 0.1445] | EDGE_CONFIRMED |
| combined | C | 535 | 0.1059 | [0.0989, 0.1132] | EDGE_CONFIRMED |

## Bootstrap CI results
- Combined Tier C bootstrap: mean_boot=0.1060, 95% CI=[0.0989, 0.1132]

## Classification per tier and combined
- Tier A: SAMPLE_LIMITED
- Tier B: EDGE_CONFIRMED
- Tier C: EDGE_CONFIRMED
- Final classification: P43_BLOCKED_BY_DATA_GAP

## Framing note (edge vs closing line, not strict CLV)
- This analysis uses CSV closing-line implied probability vs model probability. CSV does not include opening/pregame snapshot trajectory, so this is edge vs closing line, not strict CLV (which requires pregame to closing comparison). P26 line-aware CLV diagnostic is separate and unchanged.

## Files created / modified
- scripts/_p43_strong_edge_closing_line_edge_validation.py
- tests/test_p43_strong_edge_closing_line_edge_validation.py
- data/mlb_2025/derived/p43_strong_edge_closing_line_edge_summary.json
- report/p43_strong_edge_closing_line_edge_validation_20260525.md
- 00-BettingPlan/20260525/p43_strong_edge_closing_line_edge_validation_20260525.md
- 00-Plan/roadmap/active_task.md

## Tests PASS / FAIL
- See pytest execution section in handoff message (outside this static report).

## Forbidden scan result
- Forbidden affirmative phrases scan executed separately in handoff.

## Commit hash or reason not committed
- Not committed in this run (workspace had pre-existing dirty files; whitelist-only artifact generation).

## CTO summary (<=10 lines)
1. P43 pipeline is implemented as paper-only diagnostic with locked threshold T=0.50.
2. 2025 strong-edge games are fully joinable to closing-line CSV and produce valid edge metrics.
3. 2024 holdout file has no closing-line implied probability fields in current frozen artifact.
4. Therefore cross-year closing-line edge cannot be fully validated in this run.
5. Tier/year/bootstrap outputs are still generated with deterministic settings (seed=42, n_boot=5000).
6. Final result is data-governance-safe: no API calls, no crawler edits, no promotion changes.
7. Classification is set from evidence: BLOCKED_BY_DATA_GAP if 2024 market probability is unavailable.
