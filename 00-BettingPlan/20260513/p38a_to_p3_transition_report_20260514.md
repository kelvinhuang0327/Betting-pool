# P38A → P3 Transition Report — 2026-05-14

**Status:** TRANSITION_REPORT_COMPLETE  
**Author:** CTO Agent  
**Date:** 2026-05-14  
**Round:** 24H Task Cycle — P3 Free-Source Odds Spike v2 + P38A OOF Join Readiness  
**Acceptance Marker:** P38A_TO_P3_TRANSITION_REPORT_20260514_READY

---

## ⚠️ Standing Constraints

> - `P38A_RUNTIME_COMMIT_LOCAL_ONLY` — commit `3a9bec9` not pushed. No push without explicit user YES.
> - `TESTS_NOT_RUN_DOCS_ONLY` — this 24H cycle produced documentation and fixture artifacts only. No runtime code was modified.
> - All production flags remain: `PAPER_ONLY=True`, `production_ready=False`
> - No raw odds data was committed to any branch
> - No live recommendations issued

---

## 1. P38A Final State

### 1.1 Gate Status

```
Gate:              P38A_2024_OOF_PREDICTION_READY
output_hash:       7134eda90c848826e1acc97e76c984c89a811b2e5467f4e92b0e79647e26e099
paper_only:        true
production_ready:  false
deterministic:     true
```

### 1.2 Model Metrics (Frozen)

| Metric | Value |
|---|---|
| n_predictions | 2,187 |
| total_input_rows | 2,429 |
| coverage_pct | 90.04% |
| brier_score | 0.2487 |
| brier_skill_score | +0.0020 |
| log_loss | 0.6905 |
| base_rate | 52.81% |
| fold_count | 10 (walk-forward) |
| RANDOM_STATE | 42 |
| MODEL_VERSION | `p38a_walk_forward_logistic_v1` |

### 1.3 P38A Artifact Inventory (Complete)

| Artifact | Path | State |
|---|---|---|
| OOF predictions CSV | `outputs/predictions/PAPER/p38a_2024_oof/p38a_2024_oof_predictions.csv` | ✅ Frozen (2,187 rows) |
| Gate result JSON | `outputs/predictions/PAPER/p38a_2024_oof/p38a_gate_result.json` | ✅ Frozen |
| Metrics JSON | `outputs/predictions/PAPER/p38a_2024_oof/p38a_oof_metrics.json` | ✅ Frozen |
| Output contract doc | `00-BettingPlan/20260513/p38a_oof_output_contract_inventory_20260514.md` | ✅ Created |
| Join key mapping spec | `00-BettingPlan/20260513/p38a_odds_join_key_mapping_spec_20260514.md` | ✅ Created |
| Fixture smoke report | `00-BettingPlan/20260513/p38a_fixture_only_join_smoke_report_20260514.md` | ✅ Created |
| Fixture CSV | `data/research_odds/fixtures/P38A_JOIN_SMOKE_TEMPLATE_20260514.csv` | ✅ Created |
| OOF builder module | `wbc_backend/recommendation/p38a_oof_prediction_builder.py` | ✅ Unchanged |
| Feature adapter module | `wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py` | ✅ Unchanged |

### 1.4 P38A Join Readiness Assessment

**Result: JOIN_SPEC_COMPLETE — FIXTURE_VALIDATED — RUNTIME_NOT_BUILT**

The join key mapping spec is complete and validated. A 5-row fixture smoke test confirms:
- `game_id_exact` join path works 100% (5/5 match)
- Implied probability formula validated (American odds → p_implied → p_nvig)
- Leakage sentinel rule validated
- Duplicate detection rule validated
- 23-column contract schema fully specified

**What is NOT ready:**
- No real odds source has been loaded (all paid or license-blocked)
- Composite key fallback join not runtime-tested (spec only)
- Bridge join via `mlb_2024_game_identity_outcomes_joined.csv` not implemented in code
- Away_team enrichment path not runtime-tested

---

## 2. Why P3 Odds Spike Is the Next P0

### 2.1 The Odds Gap

P38A `p_oof` is a calibrated walk-forward prediction with BSS=+0.0020 vs base rate. This means the model has learned a signal. However, without odds (implied probability), we cannot:

1. Compute **Expected Value (EV)** = `p_oof - p_nvig_home`
2. Run **paper recommendation triggers** (only bet if EV > threshold)
3. Perform **Closing Line Value (CLV) benchmarking** (were bets placed at a good line?)
4. Produce a **Kelly position sizing** for paper/research tracking

All 4 of the above are required before any meaningful research output can be generated for dates where we have P38A predictions.

### 2.2 The Odds Source Gap

From the v2 candidate inventory (`research_odds_candidate_inventory_v2_20260514.md`):

| Class | Count | Status |
|---|---|---|
| ACCEPTABLE (fixture/manual import only) | 2 | ✅ Validated (fixture smoke done) |
| ACCEPTABLE (public dataset, unverified) | 4 | Needs audit (Kaggle, GitHub) |
| PAID_PROVIDER_DECISION_REQUIRED | 3 | Odds API, SportsDataIO, Sportradar |
| REJECTED_FOR_LICENSE_RISK | 2 | SBRO scrape, OddsPortal |

**P0 gap:** We have zero real MLB 2024 moneyline odds rows in any approved source. Fixture validates the join plumbing but produces no meaningful EV signal.

### 2.3 The Free-Source Hypothesis

P3 (Free-Source Odds Spike) tests whether any ACCEPTABLE public dataset (Kaggle, GitHub) contains MLB 2024 moneyline data that:
1. Has clear license (CC, MIT, or public domain)
2. Covers at minimum the 2,187 P38A game predictions
3. Has column structure mappable to the 23-column manual import contract
4. Has pre-game snapshot timestamps (or at minimum game-date only for closing-line CLV study)

If P3 succeeds → we can run a real EV + CLV benchmark for 2024 season retroactively.  
If P3 fails → decision point: pay for Odds API / SportsDataIO trial, or proceed with fixture-only paper simulation.

---

## 3. P38A Do-Not-Repeat List

Things learned from P38A that must NOT be repeated in subsequent phases:

| Issue | Rule |
|---|---|
| Away team missing from OOF CSV | Future prediction CSVs MUST include `away_team` directly. Bridge joins add fragility. |
| No timestamp in prediction output | Every prediction row must carry `generated_at` field for audit trail. |
| game_id non-standard format | Future: adopt MLB statsAPI gamePk as canonical ID alongside Retrosheet. |
| Coverage only 90% | Investigate why 10% of Retrosheet rows were dropped. Document feature-coverage failure cases. |
| BSS barely positive | +0.0020 BSS is a weak signal. Must validate with larger feature set or ensemble before paper trading. |
| No holdout test set | Walk-forward OOF is NOT a held-out test. Must designate 2025 season as true holdout before any real research claim. |
| Column misalignment in fixture CSV | Fixture CSVs must be validated column-by-column with a schema checker before being used in any smoke test. |

---

## 4. P3 Phase Definition

**P3 Goal:** Identify ≥1 free-source MLB odds dataset, import it under the manual import contract, run the first real EV join against P38A OOF predictions, and produce a CLV benchmark table for 2024 season.

### 4.1 P3 Exit Criteria

| Criterion | Measurement |
|---|---|
| Free source identified with valid license | Source audit doc with `ACCEPTABLE` classification |
| Real odds rows loaded (≥100 games) | Import CSV row count >= 100, `source_license_status != synthetic_no_license` |
| EV join executed (script not fixture) | `join_method = game_id_exact OR composite_key` in output, not `fixture` |
| CLV benchmark table produced | `ev_benchmark_report_{date}.md` with median CLV ± std |
| No leakage violation | All odds rows have `snapshot_time_optional` < game start, or clearly labeled `closing_line_research_only` |

### 4.2 P3 Candidate Priority Order

1. **Kaggle MLB Odds datasets** — search for CC-licensed MLB 2024 moneyline CSV
2. **GitHub repos** (`baseball-reference-betting-data`, `baseball-odds-archive`, similar)  
3. **Retrosheet-paired public repos** — repos that already use Retrosheet game IDs
4. **Manual research import** — if 1-3 fail, manual entry of ≤50 key games from memory/reference

### 4.3 P3 Failure Mode

If no free source with valid license is found that covers meaningful 2024 game count:
- **Decision Point A**: Subscribe to The Odds API (free tier = 500 req/month) — user must decide
- **Decision Point B**: Accept fixture-only paper simulation as permanent state and document BSS-only research claim
- **Decision Point C**: Shift focus to 2025 season where data may be more accessible

---

## 5. Acceptance Marker

```
P38A_TO_P3_TRANSITION_REPORT_20260514_READY
```
