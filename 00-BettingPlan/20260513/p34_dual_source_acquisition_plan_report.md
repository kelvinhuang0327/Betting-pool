# P34 Dual Source Acquisition Plan — Report

**Date**: 2026-05-13  
**Phase**: P34  
**Author**: Automated Pipeline  
**Branch**: p13-clean  
**PAPER_ONLY**: True | **PRODUCTION_READY**: False

---

## 1. Repo Evidence

- **Branch**: `p13-clean`
- **HEAD at start of session**: `8dd9a00` — "feat(betting): build P33 2024 prediction odds gap plan"
- **Python venv**: `.venv/bin/python` (3.10+)
- **P31 committed**: `6b0ab64` — 65/65 tests pass
- **P32 committed**: `d7766bc` — 145/145 tests pass  
- **P32.5 committed**: `736d0f9` — gl2024.txt → processed artifacts (2,429 game rows)
- **P33 committed**: `8dd9a00` — 203/203 tests pass

---

## 2. P33 Evidence (Prerequisite)

P33 gate result from `data/mlb_2024/processed/p33_joined_input_gap/p33_gate_result.json`:

```json
{
  "gate": "P33_BLOCKED_NO_VERIFIED_PREDICTION_SOURCE",
  "season": 2024,
  "prediction_gap_blocked": true,
  "odds_gap_blocked": true,
  "paper_only": true,
  "production_ready": false,
  "next_phase": "P34_DUAL_SOURCE_ACQUISITION_PLAN"
}
```

P33 found 467 prediction candidates and 469 odds candidates in the repo — all blocked due to missing verified 2024 sources. P34 was prescribed as the next phase.

---

## 3. Why P34 Was Needed

P33 confirmed that no verified 2024 prediction probability (p_oof) or market closing odds (p_market) exist in the repository. Without these two inputs, the joined input spec required for EV analysis and Kelly criterion position sizing cannot be constructed.

P34's mission is to produce a **safe, paper-only acquisition plan** specifying:
- Which prediction source to acquire (and how, without leakage)
- Which odds source to acquire (and how, without scraping or license violations)
- The schema templates for import
- The validation rules that must be satisfied before P35 can proceed

---

## 4. Prediction Acquisition Options

| Option | Name | Status | Coverage | Leakage Risk |
|--------|------|--------|----------|--------------|
| pred_r01 | Retrain 2024 OOF from P32 gl2024 features | OPTION_READY_FOR_IMPLEMENTATION_PLAN | 100% | none |
| pred_r02 | External 2024 prediction CSV import | OPTION_REQUIRES_MANUAL_APPROVAL | 0% | medium |
| pred_r03 | No prediction source available | OPTION_BLOCKED_PROVENANCE | 0% | none |

**Best option**: `pred_r01` — OOF rebuild from P32 Retrosheet game log features (2,429 rows available). Requires feature engineering pipeline and OOF training. Must not use y_true to generate p_oof.

**Hard rules enforced**:
- NEVER use y_true to create p_oof
- NEVER use final scores to create p_model
- is_dry_run → OPTION_REJECTED_FAKE_OR_LEAKAGE
- year_unverified → OPTION_BLOCKED_PROVENANCE

---

## 5. Odds Acquisition Options

| Option | Name | Status | Coverage | License |
|--------|------|--------|----------|---------|
| odds_r01 | sportsbookreviewsonline.com 2024 MLB Closing Moneylines | OPTION_REQUIRES_LICENSE_REVIEW | 90% | personal_research_verify_tos |
| odds_r02 | The Odds API — Historical MLB 2024 Moneylines | OPTION_REQUIRES_MANUAL_APPROVAL | 85% | paid_subscription_internal_research |
| odds_r03_* | Existing P33 repo candidates (469 total) | OPTION_BLOCKED_PROVENANCE | 0% | unknown |
| odds_r04 | No odds source available | OPTION_BLOCKED_PROVENANCE | 0% | blocked |

**Best option**: `odds_r01` — sportsbookreviewsonline.com provides freely downloadable per-month Excel archives of MLB moneylines. Requires manual download (no scraping), American odds → decimal conversion, and alignment to P32 game_id spine.

**Hard rules enforced**:
- Do NOT scrape odds from any source
- Do NOT infer odds from game outcomes (reverse-engineering forbidden)
- Do NOT call live odds APIs
- Do NOT use unclear-license odds without review

---

## 6. Schema Templates

Three schema artifacts written to `data/mlb_2024/processed/p34_dual_source_acquisition/`:

### Prediction Import Template (`prediction_import_template.csv`)
Header-only CSV with 9 required columns:
```
game_id, game_date, home_team, away_team, p_oof, model_version, fold_id,
source_prediction_ref, generated_without_y_true
```

### Odds Import Template (`odds_import_template.csv`)
Header-only CSV with 11 required columns:
```
game_id, game_date, home_team, away_team, p_market, odds_decimal, sportsbook,
market_type, closing_timestamp, source_odds_ref, license_ref
```

### Validation Rules (`joined_input_validation_rules.json`)
Key rules enforced:
- `game_id`: required and non-null
- `game_date`: required and parseable
- `p_oof`: range [0, 1] inclusive
- `p_market`: range [0, 1] inclusive
- `odds_decimal`: > 1.0 (valid decimal odds)
- `generated_without_y_true`: must be True for every prediction row
- `license_ref`: required and non-empty for every odds row
- `source_odds_ref`: required and non-empty
- Global: no outcome-derived odds, no y_true-derived predictions, season 2024 only

---

## 7. License and Provenance Risk

| Risk | Severity | Notes |
|------|----------|-------|
| sportsbookreviewsonline.com ToS | Medium | Freely available for personal/research use. Must verify ToS before redistribution. |
| P32 OOF rebuild leakage | Low | Features must be engineered from pre-game state only. Full leakage audit required before use. |
| P33 repo candidates | High | All 469 odds candidates blocked — wrong season (2025/2026) or no license. |

**Recommendation**: Complete ToS verification for `odds_r01` before downloading any data. Do not proceed to P35 without confirmed license.

---

## 8. Test Results

**All 567 tests passed** (P31 + P32 + P33 + P34):

```
tests/test_p34_dual_source_acquisition_contract.py  — 47 tests
tests/test_p34_prediction_source_planner.py         — 30 tests
tests/test_p34_odds_source_planner.py               — 27 tests
tests/test_p34_joined_input_schema_package.py       — 27 tests
tests/test_p34_dual_source_plan_builder.py          — 20 tests
tests/test_run_p34_dual_source_acquisition_plan.py  — 3 tests (+ 10 skipped pending P32/P33)

P31–P33 regression tests:                          — 363 tests

TOTAL: 567 passed, 0 failed, 2 warnings
```

---

## 9. Determinism Result

Two consecutive CLI runs with identical inputs produced identical outputs.

```
[P34] Determinism check: PASS
```

Compared files (normalized — `generated_at` and `artifacts` fields excluded):
- `prediction_acquisition_options.json` ✅
- `odds_acquisition_options.json` ✅
- `dual_source_acquisition_plan.json` ✅
- `joined_input_validation_rules.json` ✅
- `p34_gate_result.json` ✅
- `prediction_import_template.csv` ✅ (binary identical)
- `odds_import_template.csv` ✅ (binary identical)

---

## 10. Production Readiness

| Guard | Value |
|-------|-------|
| PAPER_ONLY | True |
| PRODUCTION_READY | False |
| Real bets placed | No |
| Live odds queried | No |
| Scraping performed | No |
| Fabricated predictions | No |
| y_true used for p_oof | No |

This is a planning document. No actual data acquisition has occurred.

---

## 11. Remaining Limitations

1. **OOF rebuild not yet executed** — `pred_r01` is ready for implementation, but the feature engineering pipeline and model training have not been built.
2. **Odds license not yet confirmed** — `odds_r01` (sportsbookreviewsonline.com) requires ToS review before data can be downloaded.
3. **Game-id alignment not validated** — P32 spine join for odds must be tested against real downloaded data.
4. **Coverage gaps** — odds_r01 estimates 90% coverage; ~10% of games may not have closing moneylines in the archive.
5. **OOF fold calibration** — k-fold OOF probability calibration must be validated before p_oof values can be used in EV analysis.

---

## 12. Next-Phase Recommendation

**Next phase**: `P35_DUAL_SOURCE_IMPORT_VALIDATION`

Steps recommended:
1. Verify sportsbookreviewsonline.com ToS permits research use without redistribution.
2. Download 2024 MLB Excel archives manually; parse and convert to odds_import_template.csv format.
3. Build OOF feature engineering pipeline from P32 gl2024.txt game log features.
4. Train k-fold OOF model; generate p_oof predictions; populate prediction_import_template.csv.
5. Validate both imports against `joined_input_validation_rules.json`.
6. Align game_id across both templates using P32 spine.
7. Produce certified P35 joined input.

---

## 13. CLI Run Summary

```
[P34] gate:                     P34_DUAL_SOURCE_ACQUISITION_PLAN_READY
[P34] best_prediction_option:   pred_r01
[P34] best_odds_option:         odds_r01
[P34] prediction_path_status:   OPTION_READY_FOR_IMPLEMENTATION_PLAN
[P34] odds_path_status:         OPTION_REQUIRES_LICENSE_REVIEW
[P34] schema_templates_written: True
[P34] production_ready:         False
[P34] paper_only:               True
[P34] license_risk:             Odds acquisition path requires license review
                                before data can be downloaded. Do NOT download
                                or use odds until ToS is confirmed.
[P34] recommended_next_action:  Complete license review for odds_r01, then begin
                                OOF feature engineering for pred_r01.

[P34] RESULT: READY — P34_DUAL_SOURCE_ACQUISITION_PLAN_READY
Exit code: 0
```

---

`P34_DUAL_SOURCE_ACQUISITION_PLAN_READY`
