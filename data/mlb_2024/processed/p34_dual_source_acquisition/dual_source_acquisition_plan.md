# P34 Dual Source Acquisition Plan

**Gate**: `P34_DUAL_SOURCE_ACQUISITION_PLAN_READY`
**Season**: 2024
**PAPER_ONLY**: True  |  **PRODUCTION_READY**: False

## Prediction Acquisition
- **Best option**: `pred_r01`
- **Path status**: `OPTION_READY_FOR_IMPLEMENTATION_PLAN`

### [pred_r01] Retrain 2024 OOF from P32 gl2024 features
- Status: `OPTION_READY_FOR_IMPLEMENTATION_PLAN`
- Leakage risk: none
- Coverage: 100%
- Notes: P32 game logs: 2429 rows, coverage=100.0%. Requires: feature engineering pipeline, OOF model training, leakage audit before use.

### [pred_r02] External 2024 prediction CSV import
- Status: `OPTION_REQUIRES_MANUAL_APPROVAL`
- Leakage risk: medium
- Coverage: 0%
- Notes: Requires manual provision of a verified 2024 prediction CSV with provenance, schema, and leakage documentation.

### [pred_r03] No prediction source available
- Status: `OPTION_BLOCKED_PROVENANCE`
- Leakage risk: none
- Coverage: 0%
- Notes: Explicit blocker. Must be resolved before EV analysis or Kelly position sizing can be performed.

## Odds Acquisition
- **Best option**: `odds_r01`
- **Path status**: `OPTION_REQUIRES_LICENSE_REVIEW`
- **License risk**: Odds acquisition path requires license review before data can be downloaded. Do NOT download or use odds until ToS is confirmed.

### [odds_r01] sportsbookreviewsonline.com 2024 MLB Closing Moneylines
- Status: `OPTION_REQUIRES_LICENSE_REVIEW`
- License: personal_research_verify_tos
- Coverage: 90%
- Notes: License: freely available for personal/research. Verify ToS before any redistribution. Must align to P32 game_id spine before use. Expected: American moneylines → convert to decimal.

### [odds_r02] The Odds API — Historical MLB 2024 Moneylines
- Status: `OPTION_REQUIRES_MANUAL_APPROVAL`
- License: paid_subscription_internal_research
- Coverage: 85%
- Notes: Requires API key and paid plan. Historical endpoint covers pre-game snapshots (not live). Budget ~$50–100 USD for full 2024 MLB season.

### [odds_r03_odds_466] joined_input_preview.csv
- Status: `OPTION_BLOCKED_PROVENANCE`
- License: unknown
- Coverage: 0%
- Notes: P33 candidate: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/outputs/predictions/PAPER/backfill/p30_det_run1/preview/joined_input_preview.csv. Schema: 0 present, 11 missing. License: unknown.

### [odds_r03_odds_467] joined_input_preview.csv
- Status: `OPTION_BLOCKED_PROVENANCE`
- License: unknown
- Coverage: 0%
- Notes: P33 candidate: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/outputs/predictions/PAPER/backfill/p30_det_run2/preview/joined_input_preview.csv. Schema: 0 present, 11 missing. License: unknown.

### [odds_r03_odds_468] joined_input_preview.csv
- Status: `OPTION_BLOCKED_PROVENANCE`
- License: unknown
- Coverage: 0%
- Notes: P33 candidate: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/outputs/predictions/PAPER/backfill/p30_source_acquisition_plan_2024/preview/joined_input_preview.csv. Schema: 0 present, 11 missing. License: unknown.

### [odds_r04] No odds source available
- Status: `OPTION_BLOCKED_PROVENANCE`
- License: blocked
- Coverage: 0%
- Notes: Explicit blocker. All repo-resident odds sources were blocked by P33 due to wrong season (2025/2026) or license unclear.

## Summary
Best prediction option: [pred_r01] Retrain 2024 OOF from P32 gl2024 features (status=OPTION_READY_FOR_IMPLEMENTATION_PLAN, coverage=100%). Best odds option: [odds_r01] sportsbookreviewsonline.com 2024 MLB Closing Moneylines (status=OPTION_REQUIRES_LICENSE_REVIEW, license=personal_research_verify_tos). Schema templates written (prediction + odds import templates). PAPER_ONLY=True, PRODUCTION_READY=False.

**Next phase**: `P35_DUAL_SOURCE_IMPORT_VALIDATION`
