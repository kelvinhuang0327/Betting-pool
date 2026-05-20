# Phase 44 — Market Blend Paper-Only Tracking
## Evidence Pack: α=0.4 Strategy (Paper-Only Gate)

**Generated at**: 2026-05-05T03:10:45.601361Z
**Run ID**: `c4cabb6d-9027-4955-b90e-2c298c058755`
**Input**: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl`
**Audit Hash**: `593b85dd0561e0a1cfe02d0216d2408229c6338a00899176c57793b921eafc60`

---

## Executive Summary

| Field | Value |
|-------|-------|
| **Gate State** | `PAPER_ONLY` |
| **Candidate Patch Created** | `False` |
| **Alpha (fixed)** | `0.4` |
| **Sample Size** | 2,025 |
| **Date Range** | 2025-04-27 → 2025-09-28 |
| **blend BSS vs Market** | `+0.0022` |
| **Bootstrap Significance** | `NOT_SIGNIFICANT` |
| **Bootstrap CI (95%)** | `[-0.0015, +0.0006]` |
| **Gate Criteria Summary** | `PARTIALLY_MET` |

> **Why not production?** The α=0.4 market_blend strategy shows a marginal BSS of `+0.0022` vs market, but the 95% bootstrap CI crosses 0 (`[-0.0015, +0.0006]`), confirming the result is statistically NOT SIGNIFICANT. Current sample (2,025 games) is below the re-evaluation threshold of 3,000. All hard rules are enforced: gate stays PAPER_ONLY, no candidate patch is created.

---

## Phase 43 Evidence Recap

Phase 43 completed on 2026-05-05 with the following findings:

| Metric | Value |
|--------|-------|
| Sample size | 2,025 |
| Date range | 2025-04-27 → 2025-09-28 |
| Overall raw BSS | `-0.0039` |
| Overall blend BSS | `+0.0022` |
| Overall blend Brier | `0.2432` |
| Overall market Brier | `0.2438` |
| Fold stability | `STABLE` |
| Folds with positive blend_bss | 4 / 5 |
| Bootstrap CI (blend vs market) | `[-0.0015, +0.0006]` |
| Bootstrap significance | `NOT_SIGNIFICANT` |
| Gate recommendation | `MARKET_BLEND_PAPER_ONLY` |

**Segment value summary (Phase 43)**:
- `month` → CONDITIONAL_VALUE
- `odds_bucket` → CONDITIONAL_VALUE
- `confidence_bucket` → WEAK_VALUE
- `disagreement_bucket` → WEAK_VALUE

---

## Paper-Only Metrics Table (This Run)

| Metric | Raw Model | Market Baseline | Blend (α=0.4) |
|--------|-----------|-----------------|---------------|
| **Brier Score** | 0.2447 | 0.2438 | 0.2432 |
| **BSS vs Market** | -0.0039 | — | +0.0022 |
| **ECE** | 0.0311 | 0.0301 | 0.0281 |
| **Brier Delta (blend−mkt)** | — | — | -0.0005 |

**Bootstrap CI (blend vs market)**: [-0.0015, +0.0006]  ·  Significance: `NOT_SIGNIFICANT`  ·  P(improve): 81.0%

---

## Segment Tracking Table

| Segment Type | Best Value Classification |
|---|---|
| confidence_bucket | WEAK_VALUE |
| disagreement_bucket | WEAK_VALUE |
| month | CONDITIONAL_VALUE |
| odds_bucket | CONDITIONAL_VALUE |

---

## Next Gate Criteria

The following criteria must ALL be met before re-evaluating the PAPER_ONLY gate:

| Criterion | Current Status |
|-----------|---------------|
| sample_size >= 3,000 | ❌ NOT MET |
| Bootstrap CI does not cross 0 (SIGNIFICANT) | ❌ NOT MET |
| blend_bss consistently > 0 | ✅ MET |
| ECE not clearly deteriorated (≤ market_ece + 0.01) | ✅ MET |
| >= 4/5 folds have positive blend_bss | ✅ MET |
| Human review approved | ❌ NOT MET |

**Summary**: `PARTIALLY_MET`

---

## Risk Notes

- α=0.4 blend shows +0.22% BSS vs market overall but CI crosses 0 — statistically NOT_SIGNIFICANT
- Best-per-fold alpha varies (0.1–1.0) — diagnostic_only; do NOT use per-fold alpha in production
- CONDITIONAL_VALUE only in month + odds_bucket segments; high_conf segment shows NO_VALUE
- Paper-only: track BSS/ECE/sample metrics for >= 3 periods before re-evaluating gate
- Do NOT deploy to production without PATCH_GATE_RECHECK from BSS Safety Gate

---

## Next Gate Criteria (Detail)

- sample_size >= 3000 OR +30 days new rolling data since Phase 43 (2026-05-05)
- bootstrap CI does not cross 0 (SIGNIFICANT at 95% level)
- blend_bss consistently > 0 across >= 3 consecutive evaluation periods
- ECE not clearly deteriorated: blend_ece <= market_ece + 0.01
- >= 4/5 folds or rolling windows have positive blend_bss
- human review approved (via review_queue system)

---

## Hard Rules (always enforced)

- `gate_state = PAPER_ONLY` — never changes until ALL gate criteria met
- `candidate_patch_created = False` — never flip
- `alpha = 0.4` — fixed from Phase 42A / Phase 43, no per-fold override
- Do NOT deploy to production without `PATCH_GATE_RECHECK` from BSS Safety Gate
- Bootstrap CI crossing 0 → NOT_SIGNIFICANT → PAPER_ONLY stays
- Best-per-fold alpha (0.1–1.0) is diagnostic only; do NOT use in production

---

*Phase 44 — Market Blend Paper-Only Tracking | Betting-pool quant research*
