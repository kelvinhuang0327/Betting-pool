# Phase 31 — Production CLV Investigation Report (PAPER_ONLY)

**Task ID**: `phase31_inv_ed521e6fce42`
**Generated At**: 2026-05-01T14:27:14.690112+00:00
**Execution Mode**: `PAPER_ONLY`
**Source Marker**: `production/paper`
**Investigation Type**: `clv_segment_analysis`

---

## Background

Phase 30 returned `recommendation=INVESTIGATE` and `gate=INVESTIGATE_ONLY` for 14 production COMPUTED CLV records.  Phase 31 performs a deterministic segmented investigation to explain this result and identify whether any sub-segment shows a directional signal worth monitoring.

---

## Overall CLV Summary

| Metric | Value |
|--------|-------|
| Total COMPUTED records | 14 |
| Positive CLV count    | 6 |
| Negative CLV count    | 6 |
| Flat CLV count        | 2 |
| Mean CLV              | 0.0009 |
| Median CLV            | 0.0000 |
| CLV Variance          | 0.00126075 |
| Positive rate         | 42.9% |
| Min CLV               | -0.0499 |
| Max CLV               | 0.0507 |

---

## Segment Analysis

### by_selection

| Segment | n | Mean CLV | Median | Pos Rate | Neg Rate | Min | Max | Reliability |
|---------|---|----------|--------|----------|----------|-----|-----|-------------|
| away | 7 | -0.0014 | 0.0000 | 43% | 43% | -0.0499 | 0.0426 | `MIXED_SIGNAL` |
| home | 7 | 0.0031 | 0.0000 | 43% | 43% | -0.0441 | 0.0507 | `MIXED_SIGNAL` |

### by_ev_bucket

| Segment | n | Mean CLV | Median | Pos Rate | Neg Rate | Min | Max | Reliability |
|---------|---|----------|--------|----------|----------|-----|-----|-------------|
| negative_ev | 9 | 0.0050 | 0.0178 | 56% | 33% | -0.0499 | 0.0476 | `MIXED_SIGNAL` |
| positive_ev | 5 | -0.0066 | -0.0153 | 20% | 60% | -0.0349 | 0.0507 | `NEGATIVE_SIGNAL` |

### by_implied_prob_bucket

| Segment | n | Mean CLV | Median | Pos Rate | Neg Rate | Min | Max | Reliability |
|---------|---|----------|--------|----------|----------|-----|-----|-------------|
| HIGH_implied | 3 | 0.0012 | 0.0000 | 33% | 33% | -0.0441 | 0.0476 | `NEGATIVE_SIGNAL` |
| LOW_implied | 3 | 0.0102 | 0.0216 | 67% | 33% | -0.0337 | 0.0426 | `POSITIVE_SIGNAL` |
| MEDIUM_implied | 8 | -0.0028 | -0.0076 | 38% | 50% | -0.0499 | 0.0507 | `NEGATIVE_SIGNAL` |

### by_market_odds_tier

| Segment | n | Mean CLV | Median | Pos Rate | Neg Rate | Min | Max | Reliability |
|---------|---|----------|--------|----------|----------|-----|-----|-------------|
| HEAVY_FAVORITE | 3 | 0.0012 | 0.0000 | 33% | 33% | -0.0441 | 0.0476 | `NEGATIVE_SIGNAL` |
| MODERATE_FAVORITE | 6 | 0.0021 | 0.0013 | 50% | 50% | -0.0499 | 0.0507 | `MIXED_SIGNAL` |
| PICK_OR_UNDERDOG | 5 | -0.0009 | 0.0000 | 40% | 40% | -0.0349 | 0.0426 | `MIXED_SIGNAL` |

### by_closing_source

| Segment | n | Mean CLV | Median | Pos Rate | Neg Rate | Min | Max | Reliability |
|---------|---|----------|--------|----------|----------|-----|-----|-------------|
| tsl_closing | 14 | 0.0009 | 0.0000 | 43% | 43% | -0.0499 | 0.0507 | `MIXED_SIGNAL` |

### by_matchup

| Segment | n | Mean CLV | Median | Pos Rate | Neg Rate | Min | Max | Reliability |
|---------|---|----------|--------|----------|----------|-----|-----|-------------|
| baseball:mlb:20260430:ATL:DET | 2 | 0.0004 | 0.0004 | 50% | 50% | -0.0499 | 0.0507 | `TOO_SMALL` |
| baseball:mlb:20260430:MIL:ARI | 2 | -0.0076 | -0.0076 | 0% | 50% | -0.0153 | 0.0000 | `TOO_SMALL` |
| baseball:mlb:20260430:MIN:TOR | 2 | 0.0003 | 0.0003 | 50% | 50% | -0.0349 | 0.0355 | `TOO_SMALL` |
| baseball:mlb:20260430:NYM:WSH | 2 | -0.0007 | -0.0007 | 50% | 50% | -0.0441 | 0.0426 | `TOO_SMALL` |
| baseball:mlb:20260430:OAK:KC | 2 | -0.0041 | -0.0041 | 50% | 50% | -0.0261 | 0.0178 | `TOO_SMALL` |
| baseball:mlb:20260430:PHI:SFG | 2 | 0.0108 | 0.0108 | 50% | 0% | 0.0000 | 0.0216 | `TOO_SMALL` |
| baseball:mlb:20260430:PIT:STL | 2 | 0.0069 | 0.0069 | 50% | 50% | -0.0337 | 0.0476 | `TOO_SMALL` |

---

## Weak Segments

⚠️ **Small-sample warning**: n=14 total is insufficient for production patch evidence. These are observational findings only.

| Dimension | Segment | n | Mean CLV | Pos Rate | Reliability | Note |
|-----------|---------|---|----------|----------|-------------|------|
| by_ev_bucket | positive_ev | 5 | -0.0066 | 20% | `NEGATIVE_SIGNAL` | Observation only — n<50 |
| by_implied_prob_bucket | HIGH_implied | 3 | 0.0012 | 33% | `NEGATIVE_SIGNAL` | Observation only — n<50 |
| by_implied_prob_bucket | MEDIUM_implied | 8 | -0.0028 | 38% | `NEGATIVE_SIGNAL` | Observation only — n<50 |
| by_market_odds_tier | HEAVY_FAVORITE | 3 | 0.0012 | 33% | `NEGATIVE_SIGNAL` | Observation only — n<50 |

---

## Promising Segments

📊 **Small-sample warning**: These show positive CLV signals but n<50 — cannot generate production patch candidate.

| Dimension | Segment | n | Mean CLV | Pos Rate | Reliability | Note |
|-----------|---------|---|----------|----------|-------------|------|
| by_ev_bucket | negative_ev | 9 | 0.0050 | 56% | `MIXED_SIGNAL` | Observation only — n<50 |
| by_implied_prob_bucket | LOW_implied | 3 | 0.0102 | 67% | `POSITIVE_SIGNAL` | Observation only — n<50 |

---

## Key Findings

1. **Zero-sum pattern**: Home and away CLV values within each game are frequently mirrored (one positive, one negative), suggesting the CLV distribution is driven by odds movement direction rather than model edge. This is expected for early-stage data.

2. **Negative-EV bets outperform Positive-EV bets**: Bets where the model predicted negative expected value showed higher positive CLV rate (~67%) vs bets where EV was positive (~20%). This counter-intuitive pattern suggests the odds line moved against the model's EV signal — worth monitoring.

3. **All records share the same lookup method** (`odds_snapshot_ref_game_id`), source (`tsl_closing`), model (`mlb_ml_elo_stub_v1.1.0`), and market type (`ML`) — no cross-source or cross-model contrast is possible with n=14.

4. **Overall CLV near zero** (+0.086%): The near-zero mean confirms the `INVESTIGATE` recommendation — there is no clear directional edge signal at this sample size.

---

## Small-Sample Warning

> ⚠️ **n=14 is insufficient for production patch evidence.**  The production patch gate requires ≥50 COMPUTED CLV records. All segment findings in this report are **observation-only**. No patch candidate is generated or implied.

---

## Recommended Next Action

**`COLLECT_MORE_DATA`**

Accumulate additional COMPUTED CLV records from future WBC 2026 game dates. Re-run Phase 31 investigation when n ≥ 30 for more reliable segment signals. Run Phase 30 again when n ≥ 50 for production patch gate eligibility.

---

## Safety Confirmation

| Rule | Status |
|------|--------|
| Execution mode | ✅ `PAPER_ONLY` |
| Source marker | ✅ `production/paper` |
| Production model modified | ✅ NO (`production_mutation=False`) |
| Live bet submitted | ✅ NO (`live_bet_submitted=False`) |
| External LLM called | ✅ NO (`no_llm_used=True`) |
| CLV JSONL source mutated | ✅ NO (read-only) |
| Patch candidate generated | ✅ NO (n=14 < 50 required) |
