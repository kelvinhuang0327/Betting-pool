# P38A + TSL Market Schema — Execution Report
**Date:** 2026-05-15  
**Agent:** CEO-Mandated Execution Agent  
**paper_only:** True | **production_ready:** False

---

## 1. What Shipped Today

### P38A — 2024 OOF Prediction Rebuild (v1)
- `wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py` — pregame-only feature adapter (7 features, no leakage)
- `wbc_backend/recommendation/p38a_oof_prediction_builder.py` — walk-forward logistic OOF builder (10 folds, L2, seed=42)
- `scripts/run_p38a_2024_oof_prediction_rebuild.py` — CLI with 5 gate constants, determinism check, forbidden-flag guard

### TSL Market Taxonomy + Schema Pack (v1)
- `wbc_backend/markets/__init__.py` — package init
- `wbc_backend/markets/tsl_market_schema.py` — 8 market enums, frozen dataclasses, audit-serializable

---

## 2. P38A Metrics (Real Run — 2429 MLB 2024 Games)

| Metric | Value |
|--------|-------|
| Input rows | 2,429 |
| Rows with p_oof | 2,187 |
| Coverage | **90.04%** (gate: ≥90%) |
| Brier score | 0.2487 |
| Log-loss | 0.6905 |
| Brier Skill Score vs base-rate | +0.0020 |
| Base rate | 0.5281 (home win %) |
| Folds | 10 (walk-forward, time-ordered) |
| Model version | `p38a_walk_forward_logistic_v1` |
| Deterministic | **YES** (hash match: `7134eda90c848826`) |
| ECE | Not computed in v1 (Platt calibration deferred to P38B) |

**Interpretation:** BSS of +0.002 indicates marginal predictive value above naïve base-rate with 7 simple rolling features. This is expected at v1 — richer features and calibration are P38B scope.

---

## 3. Market Schema — Implemented Markets

| Market | is_paper_implemented | paper_only | production_ready |
|--------|---------------------|------------|-----------------|
| `MONEYLINE_HOME_AWAY` | **True** | True | False |
| `RUN_LINE_HANDICAP` | False | True | False |
| `TOTALS_OVER_UNDER` | False | True | False |
| `FIRST_FIVE_INNINGS_MONEYLINE` | False | True | False |
| `FIRST_FIVE_INNINGS_TOTALS` | False | True | False |
| `ODD_EVEN_TOTAL_RUNS` | False | True | False |
| `TEAM_TOTAL_HOME` | False | True | False |
| `TEAM_TOTAL_AWAY` | False | True | False |

v1 implements paper moneyline only. Expansion to run-line and totals is P7 scope (per roadmap).

---

## 4. Test Count

| Test file | Tests | Status |
|-----------|-------|--------|
| `test_p38a_retrosheet_feature_adapter.py` | 7 | ✅ ALL PASS |
| `test_p38a_oof_prediction_builder.py` | 8 | ✅ ALL PASS |
| `test_run_p38a_2024_oof_prediction_rebuild.py` | 5 | ✅ ALL PASS |
| `test_tsl_market_schema.py` | 11 | ✅ ALL PASS |
| **Total** | **31** | ✅ **31/31** |

---

## 5. Gate Result

```
P38A_2024_OOF_PREDICTION_READY
```

All acceptance criteria met:
- Coverage: 90.04% ≥ 90% ✅
- Leakage suite: PASS ✅
- Brier: reported (0.2487) ✅
- Determinism: PASS (identical hash on 2 runs) ✅
- Forbidden files: NONE staged ✅

---

## 6. Marker

```
P38A_RUNTIME_AND_TSL_SCHEMA_EXECUTION_READY
```
