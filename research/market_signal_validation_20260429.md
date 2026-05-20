# [VALIDATION] Market Signal — CLV Proxy Signal Validation

**Source Task ID:** 6161
**Source Lane:** market_signal
**Source Decision:** WORTH_VALIDATION
**Source Report:** `research/market_signal_hypothesis_2026-04-29.md`
**Validation Task ID:** 6168
**Validation Task Type:** validation_market_signal
**Executed By:** Copilot Research Agent (hard-off bypass, analogous to Phase 4.5)
**Timestamp:** 2026-04-29T07:45:00+00:00

---

## Validation Objective

Validate the hypothesis from source task #6161 (lane: market_signal):

> *Bets placed where CLV_proxy > 0.03 will outperform the benchmark model's overall ROI
> by at least 3 percentage points over a sample of ≥200 bets per market regime.*

**CLV proxy definition (from source report):**

```
CLV_proxy = model_probability − (1 / closing_decimal_odds)
```

Acceptance threshold: ROI delta ≥ +3pp, p-value < 0.05, N ≥ 200 per group.

---

## Dataset Used

| Source | Path | Records | Date Range |
|--------|------|---------|-----------|
| TSL Odds History | `data/tsl_odds_history.jsonl` | 1,205 records | 2026-03-13 → 2026-04-30 |
| WBC 2026 Snapshot | `data/wbc_2026_authoritative_snapshot.json` | 40 games | WBC 2026 tournament |
| Benchmark Model Predictions | N/A | 0 files | — |

---

## Data Availability Check

### 3.1 Odds Data

`data/tsl_odds_history.jsonl` contains 1,205 snapshots across 411 unique match IDs.
Of these, **282 matches have ≥2 snapshots** (earliest = opening proxy, latest = closing proxy).
All 282 have valid MNL (moneyline) markets with parseable decimal odds for both home and away.

**Source:** TSL_BLOB3RD (TSL domestic baseball odds, Taiwan Professional Baseball League).
Market codes present: TTO (4,987), MNL (3,180), OU (2,299), HDC (1,943), OE (1,074).

### 3.2 Benchmark Model Predictions

**NOT AVAILABLE.** A search of `models/`, `research/`, `data/`, and all output directories
found no files matching the pattern `*predict*.json|csv|parquet` or equivalent probability
output files for the historical match window. The benchmark model does not currently produce
persisted per-match probability outputs aligned with `match_id`.

Without `model_probability` at decision time, the primary CLV proxy cannot be computed:

```
CLV_proxy = model_probability − (1 / closing_decimal_odds)
             ↑ MISSING
```

### 3.3 Sample Sufficiency (Proxy Analysis)

Using odds-movement as a market CLV substitute
(`market_clv = closing_prob − opening_prob`, where `prob = 1/decimal_odds`):

| Group | Definition | Count | Hypothesis Threshold |
|-------|-----------|-------|---------------------|
| CLV_high | market_clv > 0.03 | **38** | ≥200 ❌ |
| CLV_mid | 0 < market_clv ≤ 0.03 | 81 | — |
| CLV_low | market_clv ≤ 0 | **163** | ≥200 ❌ |

Even with the odds-movement proxy, neither group meets the ≥200 sample minimum.

Mean market CLV: **+0.0026** (near-zero; consistent with efficient market baseline).
Median market CLV: **0.0000**.

---

## Minimal Validation Method

The validation plan (Section 4 of source report) requires:
1. Load historical match odds (opening + closing) ✅ loaded (282 matches)
2. Load benchmark model predictions ❌ **not available**
3. Compute `CLV_proxy = model_probability − (1/closing_decimal_odds)` ❌ blocked by step 2
4. Split into CLV_high / CLV_low groups ⚠️ partial (insufficient N even with proxy)
5. Compute ROI per group ❌ no outcome labels aligned to odds data
6. Run two-sample t-test ❌ blocked by steps 2 and 5
7. Report ROI delta and p-value ❌ blocked

**Alternative proxy analysis performed:**
Computed market CLV (closing − opening implied probability) for all 282 valid MNL pairs.
Distribution is near-zero (mean +0.0026), consistent with market efficiency. This is
preliminary only and does not replace the model-based CLV proxy required by the hypothesis.

---

## Walk-Forward Isolation

Walk-forward split attempted: training on 2024 (no data), validate on 2025 (no data), test on 2026.
**All available data falls within 2026-03-13 → 2026-04-30.** No historical training window exists
in the current repo. Walk-forward validation cannot be performed until historical MLB or CPBL
data is ingested via a data pipeline.

**Walk-forward isolation status: NOT APPLICABLE** — single temporal window, no multi-year split.

---

## Risk / Leakage Check

Leakage check on available methodology:

| Risk | Status |
|------|--------|
| Opening line used as pre-match proxy | ✅ confirmed (earliest snapshot per match) |
| Closing line = post-match odds | ❌ cannot confirm; TSL snapshots may be post-match for some records |
| Model predictions at decision time | N/A — predictions not available |
| Walk-forward split enforced | N/A — single time window |
| In-game stats excluded | N/A — no model predictions to inspect |

**Critical risk identified:** TSL snapshots are fetched by crawler; game_time alignment with
fetched_at is not guaranteed. Some "closing" snapshots may be post-match. A data pipeline
that aligns snapshot fetch times relative to match start time is required before any
CLV-proxy experiment is trustworthy.

---

## Statistical Test

**NOT CONDUCTED.** Prerequisites not met:
- No model predictions (required for CLV_proxy computation)
- No outcome labels aligned to odds data (required for ROI calculation)
- Sample size below minimum (38 CLV_high vs ≥200 required)

---

## Validation Decision

**NEEDS_DATA_PIPELINE**

The CLV proxy hypothesis is *theoretically sound and well-specified* (Section 6 of source
report correctly identifies it as WORTH_VALIDATION). However, execution is blocked by two
pipeline gaps:

1. **Missing benchmark model predictions** — the model does not currently persist
   per-match probability outputs that can be aligned to historical match IDs.
   Required output: a file at `data/` or `models/` mapping `match_id → model_probability`
   for the same window as the TSL odds history.

2. **Insufficient sample and temporal coverage** — 282 matches (all from 2026) provide
   only 38 CLV_high bets with the odds-movement proxy, far below the ≥200 required.
   Ingesting CPBL or MLB historical odds (2024–2025) via the existing
   `data/mlb_data_loader.py` or `data/tsl_crawler_v2.py` would resolve this.

---

## Recommended Next Step (If NEEDS_DATA_PIPELINE)

### Pipeline Task 1: Model Prediction Exporter

Create `scripts/export_model_predictions.py`:
- Load the benchmark model (from `wbc_backend/models/ensemble.py` or equivalent)
- Run inference on the historical match dataset (2024–2026)
- Output: `data/benchmark_predictions_2024_2026.csv`
  columns: `match_id, game_time, home_team, away_team, model_prob_home, decision_time`
- No production data writes; read-only model inference

### Pipeline Task 2: Historical Odds Expansion

Extend `data/tsl_crawler_v2.py` to backfill CPBL/TSL odds for 2024–2025 season:
- Target: ≥500 matches with opening and closing lines
- Required fields: `match_id`, `opening_decimal_odds`, `closing_decimal_odds`, `game_time`

### Re-Validation Trigger

After both pipelines complete, re-run validation with:
- CLV_proxy = model_prob − (1/closing_odds) per match
- Walk-forward split: train 2024, validate 2025, test 2026
- Two-sample t-test: CLV_high ROI vs CLV_low ROI
- Accept if: ROI delta ≥ +3pp AND p < 0.05 AND N_high ≥ 200

---

## Scope Constraints (Confirmed)

- ✅ No betting strategy modified
- ✅ No model weights changed
- ✅ No external betting API called
- ✅ No production data written
- ✅ No live bets placed
- ✅ No bankroll/Kelly changes
- ✅ No LotteryNew logic touched
- ✅ No git commit made

---

## Contamination Check

LotteryNew domain terms: **0 occurrences**
(Confirmed: no lottery draw logic, lottery number generators, or lottery-domain files referenced.)
