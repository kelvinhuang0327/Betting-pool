# P3.1 CLV Benchmark Table Specification — 2026-05-15

**Status:** SPEC COMPLETE — AWAITING REAL DATA TO COMPUTE  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Purpose:** Define the Closing Line Value (CLV) benchmark output schema, computation formulas, interpretation guards, and decision threshold policy for P38A model evaluation.  
**References:**
- `p38a_oof_output_contract_inventory_20260514.md` (P38A schema: Brier=0.2487, BSS=+0.0020)
- `p38a_odds_join_key_mapping_spec_20260514.md` (implied probability formulas)
- `p31_real_odds_join_smoke_plan_20260515.md` (join pipeline)

---

## ⚠️ Interpretation Guard (Non-Negotiable)

> **BSS = +0.0020 ≠ production edge.**
>
> The P38A Walk-Forward OOF Logistic model has a Brier Skill Score of +0.0020 above climatology.
> This is STATISTICALLY MARGINAL — within noise for a 2,187-row dataset.
>
> A positive CLV average in the benchmark table DOES NOT mean:
> - The model will generate positive expected value in production.
> - The model beats the market consistently.
> - Any real money should be wagered based on these results.
>
> CLV analysis is a DIAGNOSTIC TOOL ONLY. It measures whether the model's predictions
> correlate with line movement — not whether the model is profitable.
>
> **This system is PAPER_ONLY=True, production_ready=False until further notice.**

---

## 1. CLV Benchmark Table — Output Schema

### 1.1 Per-Game Row

| Column | Type | Formula / Source | Description |
|---|---|---|---|
| `game_id` | str | join key | e.g., `BAL-20240403-0` |
| `game_date` | str | bridge table | YYYY-MM-DD |
| `season` | int | bridge table | 2024 |
| `away_team` | str | bridge table | Retrosheet 3-letter |
| `home_team` | str | bridge table | Retrosheet 3-letter |
| `fold_id` | int | P38A OOF | 0–9 (WF fold) |
| `p_oof` | float | P38A OOF | Model's predicted P(home win) |
| `home_ml_american` | int | odds | e.g., -145 |
| `away_ml_american` | int | odds | e.g., +122 |
| `home_implied_prob_raw` | float | formula below | Raw market prob (includes vig) |
| `away_implied_prob_raw` | float | formula below | Raw market prob (includes vig) |
| `vig_total` | float | formula below | Vig / overround (sum − 1) |
| `home_no_vig_prob` | float | formula below | Market-implied P(home win), no vig |
| `away_no_vig_prob` | float | formula below | Market-implied P(away win), no vig |
| `clv_edge_home` | float | formula below | Model edge vs closing no-vig line |
| `clv_edge_abs` | float | `abs(clv_edge_home)` | Unsigned edge magnitude |
| `clv_direction` | str | see below | `POSITIVE`, `NEGATIVE`, `NEUTRAL` |
| `clv_edge_bucket` | str | see below | Discretized edge band |
| `y_true_home_win` | int | bridge table | 1=home win, 0=away win |
| `p_oof_correct` | int | computed | 1 if `p_oof > 0.5` == `y_true_home_win` |
| `bookmaker_key` | str | odds | e.g., `draftkings` |
| `odds_timestamp_utc` | str | odds | ISO 8601 UTC |
| `snapshot_type` | str | odds | `closing` or `pregame` |
| `source_license_status` | str | odds | license classification |
| `model_version` | str | P38A OOF | `p38a_walk_forward_logistic_v1` |

### 1.2 Summary Aggregation Row

| Column | Type | Description |
|---|---|---|
| `n_games` | int | Total joined game count |
| `mean_clv_edge_home` | float | Average CLV edge across all games |
| `std_clv_edge_home` | float | Standard deviation of CLV edge |
| `mean_p_oof` | float | Average predicted probability |
| `mean_home_no_vig_prob` | float | Average market-implied probability |
| `base_rate_home_win` | float | Actual home-win rate in sample |
| `model_accuracy` | float | Fraction where `p_oof > 0.5` was correct |
| `mean_brier_score` | float | Brier score for this sample |
| `brier_skill_score` | float | BSS vs climatology (`base_rate_home_win`) |
| `pct_positive_clv` | float | Fraction of games with `clv_edge_home > 0` |
| `pct_negative_clv` | float | Fraction of games with `clv_edge_home < 0` |
| `pct_neutral_clv` | float | Fraction within `±0.005` threshold |

---

## 2. Formulas

### 2.1 American Moneyline → Implied Probability (Raw)

For **favorite** (negative line, e.g., -145):
$$p_{raw} = \frac{|line|}{|line| + 100}$$

For **underdog** (positive line, e.g., +122):
$$p_{raw} = \frac{100}{100 + line}$$

```python
def american_to_implied_prob(line: int) -> float:
    if line < 0:
        return abs(line) / (abs(line) + 100)
    else:
        return 100 / (100 + line)
```

### 2.2 Vig (Overround) Calculation

$$vig = p_{raw,home} + p_{raw,away} - 1.0$$

```python
vig = home_implied_prob_raw + away_implied_prob_raw - 1.0
```

### 2.3 No-Vig Implied Probability (Market Consensus)

$$p_{no\text{-}vig,home} = \frac{p_{raw,home}}{p_{raw,home} + p_{raw,away}}$$

$$p_{no\text{-}vig,away} = \frac{p_{raw,away}}{p_{raw,home} + p_{raw,away}}$$

```python
total_raw = home_implied_prob_raw + away_implied_prob_raw
home_no_vig_prob = home_implied_prob_raw / total_raw
away_no_vig_prob = away_implied_prob_raw / total_raw
```

### 2.4 CLV Edge (Primary Signal)

$$clv\_edge\_home = p_{oof} - p_{no\text{-}vig,home}$$

- **Positive CLV edge:** model predicted higher probability of home win than market consensus → model was ahead of market (in theory)
- **Negative CLV edge:** model predicted lower probability than market → model was behind market
- **Near-zero CLV edge:** model and market in agreement

```python
clv_edge_home = p_oof - home_no_vig_prob
```

### 2.5 CLV Direction Classification

```python
def clv_direction(clv_edge: float, threshold: float = 0.005) -> str:
    if clv_edge > threshold:
        return "POSITIVE"
    elif clv_edge < -threshold:
        return "NEGATIVE"
    else:
        return "NEUTRAL"
```

### 2.6 CLV Edge Buckets

| Bucket Label | Condition |
|---|---|
| `STRONG_POSITIVE` | `clv_edge_home > 0.05` |
| `MODERATE_POSITIVE` | `0.02 < clv_edge_home ≤ 0.05` |
| `WEAK_POSITIVE` | `0.005 < clv_edge_home ≤ 0.02` |
| `NEUTRAL` | `-0.005 ≤ clv_edge_home ≤ 0.005` |
| `WEAK_NEGATIVE` | `-0.02 ≤ clv_edge_home < -0.005` |
| `MODERATE_NEGATIVE` | `-0.05 ≤ clv_edge_home < -0.02` |
| `STRONG_NEGATIVE` | `clv_edge_home < -0.05` |

### 2.7 Brier Score and Brier Skill Score

$$BS = \frac{1}{n} \sum_{i=1}^{n} (p_{oof,i} - y_{true,i})^2$$

$$BSS = 1 - \frac{BS}{BS_{ref}}$$

where:
$$BS_{ref} = base\_rate \times (1 - base\_rate)$$

(Climatological reference — always predicting the observed base rate.)

```python
import numpy as np
base_rate = y_true.mean()
bs = np.mean((p_oof - y_true) ** 2)
bs_ref = base_rate * (1 - base_rate)
bss = 1 - (bs / bs_ref)
```

**Interpretation:** BSS = +0.0020 (P38A current result) means the model is 0.20% better than always predicting the base rate. This is marginally above zero — NOT a reliable production signal.

---

## 3. Decision Threshold Policy

### 3.1 CLV Gate Thresholds

These are RESEARCH ONLY — not production trading signals:

| Metric | Research Threshold | Action if Met |
|---|---|---|
| `mean_clv_edge_home` > 0.02 | Preliminary positive signal | Flag for further investigation; do NOT trade |
| `mean_clv_edge_home` > 0.05 | Strong positive signal | Escalate to P4 research agenda |
| `pct_positive_clv` > 55% | Model beats market majority | Note but do NOT conclude profitability |
| `brier_skill_score` > 0.01 | Meaningful calibration improvement | Flag as meaningful; still PAPER_ONLY |
| `n_games` < 500 | Insufficient sample | DO NOT DRAW CONCLUSIONS — mark as INSUFFICIENT_SAMPLE |

### 3.2 Interpretation Constraints

```
FORBIDDEN interpretations (do not make these claims):
  ❌ "The model generates X% ROI."
  ❌ "The model beats the market."
  ❌ "This is a profitable betting strategy."
  ❌ "A positive CLV edge means we should bet on home teams."

PERMITTED interpretations:
  ✅ "The model's P(home win) correlates [weakly/moderately/strongly] with market closing odds."
  ✅ "The average CLV edge of [X] suggests [positive/negative/neutral] market alignment."
  ✅ "Brier Skill Score of [X] indicates [marginal/meaningful/strong] calibration improvement."
  ✅ "This result requires validation on a larger out-of-sample dataset before conclusions can be drawn."
```

---

## 4. Output File Specification

### 4.1 Per-Game CSV

```
outputs/predictions/PAPER/p38a_2024_oof/p38a_oof_clv_benchmark_per_game.csv
```

Columns: all 23 per-game columns listed in Section 1.1  
Format: CSV, UTF-8, comma-separated  
Index: sequential integer

### 4.2 Summary JSON

```
outputs/predictions/PAPER/p38a_2024_oof/p38a_oof_clv_benchmark_summary.json
```

Contains all summary aggregation fields from Section 1.2 plus:
```json
{
  "generated_at": "<ISO 8601 timestamp>",
  "model_version": "p38a_walk_forward_logistic_v1",
  "paper_only": true,
  "production_ready": false,
  "interpretation_guard": "BSS=+0.0020 is marginal. This is not a production edge signal.",
  "n_games": ...,
  "mean_clv_edge_home": ...,
  ...
}
```

### 4.3 Report Markdown

```
00-BettingPlan/20260513/p31_clv_benchmark_results_<DATE>.md
```

Generated AFTER real data is obtained and joined. Contains:
- Summary table
- CLV distribution histogram (text-based)
- Interpretation guard prominently displayed
- Per-fold breakdown (fold_id 0–9)

---

## 5. Acceptance Marker

```
P31_CLV_BENCHMARK_TABLE_SPEC_20260515_READY
```
