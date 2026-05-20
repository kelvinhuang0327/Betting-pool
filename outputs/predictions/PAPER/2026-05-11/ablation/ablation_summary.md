# P12 Feature-Family Ablation Summary

Generated: 2026-05-11T07:03:06.964400+00:00
Date range: 2025-03-01 → 2025-12-31
Input rows (total / date-filtered): 2402 / 2402

## Feature Family Classification

| Family | Columns Present |
|--------|----------------|
| recent_form | 8 |
| rest | 6 |
| bullpen | 6 |
| starter | 3 |
| weather | 3 |
| market | 8 |
| base_model | 8 |

Unknown columns (not in any family): 0

## Ablation Leaderboard

| Rank | Variant | Enabled Families | OOF BSS | OOF ECE | ROI% | Gate |
|------|---------|-----------------|---------|---------|------|------|
| 1 | no_rest | recent_form, bullpen, starter, weather, market, base_model | -0.027537 | 0.042400 | 0.75 | BLOCKED_NEGATIVE_BSS |
| 2 | all_features | recent_form, rest, bullpen, starter, weather, market, base_model | -0.027668 | 0.042928 | 0.65 | BLOCKED_NEGATIVE_BSS |
| 3 | no_bullpen | recent_form, rest, starter, weather, market, base_model | -0.027668 | 0.042928 | 0.65 | BLOCKED_NEGATIVE_BSS |
| 4 | no_weather | recent_form, rest, bullpen, starter, market, base_model | -0.027668 | 0.042928 | 0.65 | BLOCKED_NEGATIVE_BSS |
| 5 | no_context_features | base_model, market | -0.028331 | 0.035182 | 0.20 | BLOCKED_NEGATIVE_BSS |
| 6 | no_starter | recent_form, rest, bullpen, weather, market, base_model | -0.029118 | 0.032473 | 0.16 | BLOCKED_NEGATIVE_BSS |
| 7 | no_recent | rest, bullpen, starter, weather, market, base_model | -0.029878 | 0.041103 | -0.50 | BLOCKED_NEGATIVE_BSS |
| 8 | recent_only | recent_form, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 9 | rest_only | rest, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 10 | bullpen_only | bullpen, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 11 | starter_only | starter, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 12 | weather_only | weather, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 13 | recent_plus_rest | recent_form, rest, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 14 | starter_plus_bullpen | starter, bullpen, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 15 | recent_rest_starter | recent_form, rest, starter, base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |
| 16 | market_or_base_only_baseline | base_model | N/A | N/A | N/A | BLOCKED_NO_MARKET_DATA |

## Best Variant

**no_rest** — All features except rest days
- OOF BSS: -0.027537
- OOF ECE: 0.0424
- Gate: BLOCKED_NEGATIVE_BSS
- Enabled: ['recent_form', 'bullpen', 'starter', 'weather', 'market', 'base_model']

## Worst Variant

**no_recent** — All features except recent form
- OOF BSS: -0.029878
- OOF ECE: 0.041103
- Gate: BLOCKED_NEGATIVE_BSS

## P12 Conclusion

This ablation study identifies which feature families help or hurt model quality.
See ablation_results.json for full per-variant details.

paper_only: true
production_enablement_attempted: false
real_bets_placed: false