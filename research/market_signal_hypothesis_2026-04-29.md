# [EXPLORE] Market Signal Research: Odds Movement & CLV Proxy

**Task ID:** 6161
**Lane:** market_signal
**Task Type:** forced_exploration_market_signal
**Worker Type:** research
**Status:** COMPLETED
**Timestamp:** 2026-04-29T07:09:39.769146+00:00

---

### 1. New Hypothesis

**Hypothesis:** The closing-line value (CLV) proxy — defined as the difference between our model's implied probability and the closing market odds — is a statistically significant positive predictor of long-run ROI. Specifically, bets placed where CLV_proxy > 0.03 will outperform the benchmark model's overall ROI by at least 3 percentage points over a sample of ≥200 bets per market regime.

---

### 2. Why It May Improve Betting Decision Quality

The mechanism: if our model assigns probability p(A) = 0.55 to an outcome whose closing market odds imply 0.50, we hold a CLV_proxy = +0.05 advantage at decision time. Closing market odds are widely considered the sharpest available signal in sports betting markets. A systematic positive CLV proxy indicates our model identifies edges that the broader market confirms by line movement. This would improve:

- **Hit rate**: CLV-positive bets should win more often than CLV-flat bets
- **ROI**: positive expected value from CLV_proxy > 0 by definition
- **Drawdown control**: filtering to CLV-positive bets reduces variance
- **No-bet rule improvement**: CLV_proxy ≤ 0 becomes a no-bet signal

Betting-pool domain context: active betting strategy currently selects bets via the benchmark model confidence threshold. Adding CLV proxy as a secondary filter — confirmed by walk-forward backtest — would refine the no-bet rule for low-CLV regimes.

---

### 3. Required Data

| Source | Content | Window | Min Sample |
|--------|---------|--------|------------|
| `data/tsl_odds_history.jsonl` | Opening + closing line odds per match | 2024–2026 | ≥500 matches |
| `data/wbc_2026_authoritative_snapshot.json` | WBC 2026 match results | Full tournament | ≥50 matches |
| Benchmark model outputs | Predicted probabilities per match at decision time | Same window | ≥500 predictions |

**Minimum sample:** 200 bets with CLV_proxy > 0.03 AND 200 bets with CLV_proxy ≤ 0
(to compare ROI at the group level with adequate statistical power).

**Time window constraint:** Only pre-match odds may be used (no in-play data — leakage risk). Opening line = odds at market open (≥24h before match start). Closing line = odds at decision time (within 30 min of match start).

---

### 4. Minimal Validation Plan

**Metric:** ROI delta = ROI(CLV_proxy > 0.03) − ROI(CLV_proxy ≤ 0)

**Baseline:** Benchmark model's overall ROI on the same match sample.

**Acceptance threshold:** ROI delta ≥ +3pp (percentage points) over ≥200 bets per group, with p-value < 0.05 on a two-sample t-test.

**Experiment steps:**
1. Load historical match odds (opening + closing) from `data/tsl_odds_history.jsonl`
2. Load model predictions for the same matches
3. Compute CLV_proxy = model_probability − (1 / closing_decimal_odds) for each bet
4. Split bets into CLV_high (>0.03) and CLV_low (≤0)
5. Compute ROI per group
6. Run two-sample t-test on bet outcomes
7. Report ROI delta and p-value

---

### 5. Risk / Leakage Check

**Look-ahead leakage risks:**
- Closing line must be captured at or before decision time — using post-match odds is a hard leakage
- Model predictions must use only pre-match features (no in-game stats)
- Walk-forward split required: model must be re-calibrated on training window only

**Data availability risks:**
- `tsl_odds_history.jsonl` may have incomplete closing lines for low-volume markets
- WBC 2026 sample is small (≈50 matches); MLB data needed for sufficient power
- Missing opening odds may occur for markets added late

**Market regime sensitivity:**
- CLV proxy magnitude varies by market type (moneyline vs. run-line vs. totals)
- Validate separately per market type to avoid Simpson's paradox
- High-steam (sharp action) vs. low-steam regimes may show different CLV reliability

---

### 6. Decision

**WORTH_VALIDATION**

Rationale: The CLV proxy is a well-established edge signal in sports betting research literature. The data sources exist in this repo. The validation is achievable with the existing backtest infrastructure. ROI improvement ≥3pp would meaningfully improve the active betting strategy's long-run performance. Leakage risks are manageable with the walk-forward constraint already in the codebase.

---

### 7. Next Task If Worth Validation

**Title:** [VALIDATE] CLV Proxy Signal: Walk-Forward Backtest

**Objective:** Validate that CLV_proxy > 0.03 bets outperform CLV_proxy ≤ 0 bets by ≥3pp ROI over a walk-forward window (no look-ahead leakage).

**Dataset paths:**
- `data/tsl_odds_history.jsonl` — historical odds with opening/closing lines
- benchmark model prediction outputs (to be located in `models/` or `research/`)
- `data/wbc_2026_authoritative_snapshot.json` — match results for outcome labels

**Steps:**
1. Load and clean odds history; filter to matches with both opening and closing lines
2. Load benchmark model predictions; align by match_id
3. Compute CLV_proxy per bet; split into CLV_high / CLV_low groups
4. Walk-forward split: train on 2024, validate on 2025, test on 2026
5. Compute ROI and hit rate per group per year
6. Run two-sample t-test on bet outcomes (CLV_high vs CLV_low)
7. Output: ROI delta, p-value, sample sizes, regime breakdown

**Validation checks:**
- No look-ahead leakage (opening line always < decision time)
- Sample sufficiency: ≥200 bets per group
- p-value < 0.05 on t-test
- ROI delta ≥ +3pp

**Expected output:** `research/clv_proxy_validation_20260429.md`

---

## Scope Constraints

- No betting strategy changes
- No model weight modifications
- No external betting API calls
- No production betting data writes
- Research only; do not place bets
- Source: forced_exploration
