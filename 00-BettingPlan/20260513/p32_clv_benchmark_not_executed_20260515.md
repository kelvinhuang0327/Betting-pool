# P3.2 CLV Benchmark — Not Executed — 2026-05-15

**Status:** NOT_EXECUTED  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Acceptance Marker:** `P32_CLV_BENCHMARK_NOT_EXECUTED_20260515`

---

## 1. Execution Status

```
CLV Benchmark NOT EXECUTED.
Reason: ODDS_DATA_NOT_READY (TRACK 1 gate)
Upstream blocker: Join smoke not executed → no merged dataset available
```

---

## 2. What the CLV Benchmark Would Produce

CLV (Closing Line Value) measures whether P38A OOF predictions beat the market's no-vig implied probabilities. A positive CLV edge suggests the model is identifying mispriced games.

**Core metric:**

$$\text{clv\_edge\_home} = p\_oof - home\_no\_vig\_prob$$

| Metric | Definition |
|---|---|
| `mean_clv_edge_home` | Mean of clv_edge_home across all matched games |
| `clv_positive_rate` | % of games where clv_edge_home > 0 |
| `clv_edge_by_bookmaker` | Mean CLV broken out per bookmaker key |
| `clv_edge_by_fold` | Mean CLV per walk-forward fold (folds 0–9) |
| `n_matched` | Rows successfully joined |
| `n_no_odds` | P38A rows with no matching odds (join miss) |

---

## 3. Pass Criteria (For Next Session)

| Criterion | Threshold |
|---|---|
| `n_matched` | ≥ 100 |
| No division-by-zero errors | 0 |
| `clv_edge_home` values in range | All values in [-0.5, +0.5] |
| `source_license_status` on all rows | `local_only_paid_provider_no_redistribution` |

---

## 4. Interpretation Guard (Non-Negotiable)

```
⚠ BSS +0.0020 DOES NOT EQUAL PRODUCTION EDGE

Even if CLV shows positive mean edge:
  - P38A is PAPER_ONLY, production_ready=False
  - Walk-forward OOF is backtested — not live-traded
  - Closing line value does not account for liquidity / line movement
  - No real money should be wagered based on this analysis
  - CLV is a research metric only
```

---

## 5. Expected Table Format (When Executed)

```
CLV Benchmark Summary (P38A OOF vs The Odds API, 2024 MLB Season)
===================================================================
Bookmaker: draftkings / fanduel / [all]

n_predictions      : 2,187  (P38A OOF total)
n_matched          : X      (≥100 required for smoke pass)
n_no_odds          : Y      (P38A rows without odds match)
match_rate         : Z%     (n_matched / n_predictions)

mean_clv_edge_home : +/-N.NNNN
clv_positive_rate  : NN.NN%
std_clv_edge_home  : N.NNNN

CLV by Fold:
  fold_0: mean=+/-N.NNNN, n=NNN
  fold_1: mean=+/-N.NNNN, n=NNN
  ...

CLV by Bookmaker:
  draftkings : mean=+/-N.NNNN, n=NNN
  fanduel    : mean=+/-N.NNNN, n=NNN
  ...

Interpretation:
  ⚠ Research only. Not production signal.
  ⚠ PAPER_ONLY=True. Do not wager.
```

---

## 6. Resume Instructions

```
Once join smoke passes (≥100 matched rows), CLV benchmark runs automatically.
Tell agent: "Join smoke passed. Run CLV benchmark."
```

---

## 7. Acceptance Marker

```
P32_CLV_BENCHMARK_NOT_EXECUTED_20260515
```
