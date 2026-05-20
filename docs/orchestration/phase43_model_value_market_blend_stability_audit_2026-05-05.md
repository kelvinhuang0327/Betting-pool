# Phase 43: Model Value & Market Blend Stability Audit

> **生成日期**: 2026-05-05  |  Run: 2026-05-05T03:00:15.033402+00:00

---

## Executive Summary

| 項目 | 值 |
|------|----|
| Gate Recommendation | 🟡 MARKET_BLEND_PAPER_ONLY |
| Fold Stability | STABLE (4/5 folds blend_bss ≥ 0) |
| Bootstrap blend_vs_market | ⚠️ NOT_SIGNIFICANT |
| Bootstrap CI (blend) | [-0.0015, +0.0006] |
| P(blend improves) | 81.0% |
| Segment Best Value | CONDITIONAL_VALUE |
| Candidate Patch Created | ✅ NO |

## 1. Overall Metrics

| Metric | Raw Model | Market Baseline | Blend α=0.4 |
|--------|-----------|-----------------|-------------|
| Brier | 0.244706 | 0.243757 | 0.243229 |
| BSS vs market | -0.0039 (-0.39%) | — | +0.0022 (+0.22%) |
| ECE | 0.031097 | — | 0.028085 |
| Row count | 2025 | | |

## 2. Fold-Level Stability Audit

> Time-aware expanding-window splits: 5 folds.  

> Stability: **STABLE** — 4/5 folds have blend_bss ≥ 0.

| Fold | N | Date Range | Raw Brier | Market Brier | Blend Brier | Raw BSS | Blend BSS | Raw ECE | Blend ECE | Best α* |
|------|---|------------|-----------|--------------|-------------|---------|-----------|---------|-----------|----------|
| fold_1 | 337 | 2025-05-22 → 2025-06-17 | 0.2473 | 0.2437 | 0.2436 | ❌ -0.0147 | ✅ +0.0003 | 0.0807 | 0.0397 | 0.2 |
| fold_2 | 337 | 2025-06-17 → 2025-07-11 | 0.2483 | 0.2441 | 0.2446 | ❌ -0.0173 | ❌ -0.0019 | 0.0672 | 0.0435 | 0.1 |
| fold_3 | 337 | 2025-07-12 → 2025-08-09 | 0.2493 | 0.2529 | 0.2506 | ✅ +0.0141 | ✅ +0.0090 | 0.0367 | 0.0421 | 1.0 |
| fold_4 | 337 | 2025-08-09 → 2025-09-03 | 0.2453 | 0.2467 | 0.2452 | ✅ +0.0055 | ✅ +0.0060 | 0.0424 | 0.0342 | 0.7 |
| fold_5 | 337 | 2025-09-03 → 2025-09-28 | 0.2390 | 0.2382 | 0.2381 | ❌ -0.0037 | ✅ +0.0005 | 0.0385 | 0.0543 | 0.3 |

> \* Best α per fold is **DIAGNOSTIC ONLY** — not production proof.


## 3. Bootstrap CI / Significance Test

> **Rule**: if 95% CI crosses 0, classification = NOT_SIGNIFICANT.


| Comparison | N | Bootstraps | Mean ΔBrier | 95% CI | P(improve) | Significance |
|------------|---|------------|-------------|--------|------------|--------------|
| raw_vs_market | 2025 | 1000 | +0.0010 | [-0.0016, +0.0037] | 22.9% | ⚠️ NOT_SIGNIFICANT |
| blend_vs_market | 2025 | 1000 | -0.0005 | [-0.0015, +0.0006] | 81.0% | ⚠️ NOT_SIGNIFICANT |

> ⚠️ **NOT_SIGNIFICANT**: CI crosses 0. Cannot recommend PATCH_GATE_RECHECK based on bootstrap alone.

## 4. Segment-Level Model Value Analysis

| Segment Type | Best Value Classification |
|--------------|--------------------------|
| confidence_bucket | 🟠 WEAK_VALUE |
| disagreement_bucket | 🟠 WEAK_VALUE |
| month | 🟡 CONDITIONAL_VALUE |
| odds_bucket | 🟡 CONDITIONAL_VALUE |

### Segment Detail

| Type | Segment | N | Raw Brier | Market Brier | Blend Brier | Raw BSS | Blend BSS | Value |
|------|---------|---|-----------|--------------|-------------|---------|-----------|-------|
| month | 2025-04 | 53 | 0.2217 | 0.2074 | 0.2126 | -0.0688 | -0.0250 | 🔴 NO_VALUE |
| month | 2025-05 | 411 | 0.2420 | 0.2439 | 0.2425 | +0.0077 | +0.0057 | 🟡 CONDITIONAL_VALUE |
| month | 2025-06 | 397 | 0.2513 | 0.2446 | 0.2457 | -0.0277 | -0.0044 | 🔴 NO_VALUE |
| month | 2025-07 | 369 | 0.2481 | 0.2512 | 0.2491 | +0.0125 | +0.0086 | 🟡 CONDITIONAL_VALUE |
| month | 2025-08 | 421 | 0.2448 | 0.2442 | 0.2435 | -0.0022 | +0.0029 | 🟠 WEAK_VALUE |
| month | 2025-09 | 374 | 0.2405 | 0.2400 | 0.2397 | -0.0021 | +0.0011 | 🟠 WEAK_VALUE |
| odds_bucket | heavy_away_fav | 148 | 0.2325 | 0.2288 | 0.2284 | -0.0162 | +0.0018 | 🟠 WEAK_VALUE |
| odds_bucket | slight_away_fav | 470 | 0.2497 | 0.2513 | 0.2496 | +0.0065 | +0.0069 | 🟡 CONDITIONAL_VALUE |
| odds_bucket | pick_em | 262 | 0.2517 | 0.2497 | 0.2497 | -0.0082 | -0.0002 | 🔴 NO_VALUE |
| odds_bucket | slight_home_fav | 705 | 0.2540 | 0.2524 | 0.2524 | -0.0063 | +0.0001 | 🟠 WEAK_VALUE |
| odds_bucket | heavy_home_fav | 440 | 0.2245 | 0.2234 | 0.2230 | -0.0049 | +0.0019 | 🟠 WEAK_VALUE |
| confidence_bucket | low_conf | 848 | 0.2500 | 0.2507 | 0.2495 | +0.0028 | +0.0046 | 🟠 WEAK_VALUE |
| confidence_bucket | medium_conf | 982 | 0.2492 | 0.2486 | 0.2480 | -0.0023 | +0.0027 | 🟠 WEAK_VALUE |
| confidence_bucket | high_conf | 195 | 0.1991 | 0.1891 | 0.1920 | -0.0531 | -0.0155 | 🔴 NO_VALUE |
| disagreement_bucket | low_disagree | 775 | 0.2417 | 0.2420 | 0.2418 | +0.0009 | +0.0006 | 🟠 WEAK_VALUE |
| disagreement_bucket | medium_disagree | 1057 | 0.2450 | 0.2447 | 0.2439 | -0.0009 | +0.0033 | 🟠 WEAK_VALUE |
| disagreement_bucket | high_disagree | 193 | 0.2552 | 0.2456 | 0.2452 | -0.0389 | +0.0018 | 🟠 WEAK_VALUE |

## 5. Gate Recommendation

### 🟡 MARKET_BLEND_PAPER_ONLY

**Reasoning:**

- Fold stability: STABLE (4/5 folds with blend_bss >= 0)
- Bootstrap blend_vs_market: NOT_SIGNIFICANT (CI [-0.0015, +0.0006], p_improve=81.0%)
- Segment value summary: {'month': 'CONDITIONAL_VALUE', 'odds_bucket': 'CONDITIONAL_VALUE', 'confidence_bucket': 'WEAK_VALUE', 'disagreement_bucket': 'WEAK_VALUE'}
- Folds stable but bootstrap CI crosses 0 (NOT_SIGNIFICANT) → market_blend can be tracked in paper-trading only, not production.

**Hard Rules Verified:**

- CANDIDATE_PATCH created: ✅ No
- Bootstrap significant: ⚠️ No (CI crosses 0)
- Fold stable: ✅ Yes
- Has STABLE_VALUE segment: ❌ No
- Best-per-fold alpha used as proof: ✅ No (diagnostic_only=True on all folds)

---
*Generated by Phase 43 audit — read-only, no production mutations.*