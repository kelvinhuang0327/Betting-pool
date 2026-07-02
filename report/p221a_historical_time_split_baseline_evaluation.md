# P221-A Historical Time-Split Baseline Evaluation Prototype

Historical time-split baseline evaluation prototype only. Not live predictions, not betting advice.

## Summary

- Status: PASS_P218A_P219A_P220A_ARTIFACT_ONLY_HISTORICAL_TIME_SPLIT_BASELINE_EVALUATION_PROTOTYPE
- Source row count: 24
- Evaluation row count: 16
- Source column count: 18
- Evaluation column count: 11
- Split count: 2

## Source Artifacts

| Artifact | SHA256 |
| --- | --- |
| `report/p218a_historical_sample_feature_table.csv` | `d3d00176e3e40163c8d38a60019e204b0d37ef7efb745b638e797578f197b507` |
| `report/p218a_historical_sample_feature_table.json` | `60fde1062e935c7f5d37a693611e6433d765b905fb7e1a499c513bf728e39844` |
| `report/p218a_historical_sample_feature_table.md` | `28aa4b4d17bade86fe9c51990cf1798640967ea3a6e7388a81e54d485efbf016` |
| `report/p219a_historical_feature_baseline_evaluation.json` | `dc4ac6fce1e0f8f92a87a3bd3ab74d6aa60d8ea4b8205b3c8e822a1cbb370298` |
| `report/p220a_historical_baseline_error_dashboard.json` | `abd4a2540ea2109ee77f30a4a836f1800e3218cc003ed92fda0e1043c8f695f3` |

## Evaluation Method

- Read only the fixed committed P218 CSV/JSON/Markdown artifacts plus the fixed P219/P220 JSON artifacts for lineage and compatibility context.
- Sort the P218 feature-table rows by game_date and evaluate each historical date after the first observed date as a holdout split.
- For each split, train Baseline A on earlier dates only and predict the prior-date global majority event_category using deterministic alphabetical tie-break on ties.
- For each split, train Baseline B on earlier dates only and predict the prior-date pitch_type majority event_category, falling back to the prior-date global majority when the pitch_type majority is tied or absent from training history.
- Report deterministic historical-only per-split and overall holdout accuracy, confusion matrices, and baseline-B fallback coverage.

## Time Split Definitions

| split_id | train_date_range | eval_date | train_row_count | eval_row_count | baseline_a_global_majority_prediction |
| --- | --- | --- | --- | --- | --- |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 8 | 8 | in_play_out |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 16 | 8 | strike_like |

## Overall Holdout Metrics

| baseline | accuracy | correct_count | row_count | coverage_rows | coverage_fraction |
| --- | --- | --- | --- | --- | --- |
| baseline_a_global_majority | 0.250000 | 4 | 16 | 16 | 1.000000 |
| baseline_b_pitch_type_majority_with_global_fallback | 0.312500 | 5 | 16 | 16 | 1.000000 |

## Baseline B Coverage

| coverage_type | rows | fraction | correct_rows | accuracy |
| --- | --- | --- | --- | --- |
| direct_pitch_type_majority | 11 | 0.687500 | 5 | 0.454545 |
| global_fallback_due_to_tie | 2 | 0.125000 | 0 | 0.000000 |
| global_fallback_missing_pitch_type | 3 | 0.187500 | 0 | 0.000000 |
| all_global_fallback | 5 | 0.312500 | 0 | 0.000000 |

## Per-Split Metrics

| split_id | eval_date | baseline_a_accuracy | baseline_b_accuracy | direct_pitch_type_rows | fallback_rows | accuracy_delta_b_minus_a |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2024-04-02 | 0.125000 | 0.250000 | 6 | 2 | 0.125000 |
| 2 | 2024-04-03 | 0.375000 | 0.375000 | 5 | 3 | 0.000000 |

## Split 1 Pitch-Type Resolution

Eval date: `2024-04-02`

| pitch_type | support | resolved_prediction | prediction_source | fallback_to_global_majority |
| --- | --- | --- | --- | --- |
| CH | 3 | in_play_out | global_fallback_due_to_tie | true |
| FF | 3 | strike_like | pitch_type_majority | false |
| SI | 2 | in_play_out | global_fallback_due_to_tie | true |

## Split 2 Pitch-Type Resolution

Eval date: `2024-04-03`

| pitch_type | support | resolved_prediction | prediction_source | fallback_to_global_majority |
| --- | --- | --- | --- | --- |
| CH | 3 | strike_like | global_fallback_due_to_tie | true |
| FF | 9 | strike_like | pitch_type_majority | false |
| SI | 4 | strike_like | pitch_type_majority | false |

## Overall Confusion Matrices

### baseline_a_global_majority

| actual \ predicted | strike_like | ball_like | in_play_out | in_play_hit | hit_by_pitch | strikeout |
| --- | --- | --- | --- | --- | --- | --- |
| strike_like | 3 | 0 | 3 | 0 | 0 | 0 |
| ball_like | 2 | 0 | 3 | 0 | 0 | 0 |
| in_play_out | 0 | 0 | 1 | 0 | 0 | 0 |
| in_play_hit | 2 | 0 | 1 | 0 | 0 | 0 |
| hit_by_pitch | 1 | 0 | 0 | 0 | 0 | 0 |
| strikeout | 0 | 0 | 0 | 0 | 0 | 0 |

### baseline_b_pitch_type_majority_with_global_fallback

| actual \ predicted | strike_like | ball_like | in_play_out | in_play_hit | hit_by_pitch | strikeout |
| --- | --- | --- | --- | --- | --- | --- |
| strike_like | 5 | 0 | 1 | 0 | 0 | 0 |
| ball_like | 5 | 0 | 0 | 0 | 0 | 0 |
| in_play_out | 1 | 0 | 0 | 0 | 0 | 0 |
| in_play_hit | 2 | 0 | 1 | 0 | 0 | 0 |
| hit_by_pitch | 1 | 0 | 0 | 0 | 0 | 0 |
| strikeout | 0 | 0 | 0 | 0 | 0 | 0 |

## Limitations

- Evaluation reads only the fixed committed P218, P219, and P220 artifacts and does not refresh any upstream source.
- Each holdout split trains only on earlier historical game_date rows and evaluates later historical rows from the same bounded P218 sample.
- Baseline A uses the prior-date global majority event_category with deterministic alphabetical tie-break on tied counts.
- Baseline B uses the prior-date pitch_type majority event_category and falls back to the prior-date global majority when the pitch_type majority is tied or missing from training history.
- This is a historical-only evaluation prototype for pipeline shape demonstration and does not train a production model.
- Results are bounded historical holdout metrics on a 24-row artifact snapshot and must not be interpreted as future predictive ability.
- No remote data fetch, no pybaseball call, no DB write, and no production activation occur in this task.

## Prohibited Claims

- No future prediction claim.
- No live prediction claim.
- No betting advice claim.
- No production readiness claim.
- No edge, ROI, EV, Kelly, or CLV claim.

## Evaluation Rows

| split_id | train_date_range | eval_date | source_row_id | pitch_type | actual_event_category | baseline_a_prediction | baseline_a_correct | baseline_b_prediction | baseline_b_correct | baseline_b_prediction_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 9 | SI | strike_like | in_play_out | false | in_play_out | false | global_fallback_due_to_tie |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 10 | FF | ball_like | in_play_out | false | strike_like | false | pitch_type_majority |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 11 | FF | ball_like | in_play_out | false | strike_like | false | pitch_type_majority |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 12 | FF | strike_like | in_play_out | false | strike_like | true | pitch_type_majority |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 13 | FF | ball_like | in_play_out | false | strike_like | false | pitch_type_majority |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 14 | SI | in_play_hit | in_play_out | false | in_play_out | false | global_fallback_due_to_tie |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 15 | FF | strike_like | in_play_out | false | strike_like | true | pitch_type_majority |
| 1 | 2024-04-01 to 2024-04-01 | 2024-04-02 | 16 | FF | in_play_out | in_play_out | true | strike_like | false | pitch_type_majority |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 17 | SI | in_play_hit | strike_like | false | strike_like | false | pitch_type_majority |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 18 | SI | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 19 | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 20 | FS | hit_by_pitch | strike_like | false | strike_like | false | global_fallback_missing_pitch_type |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 21 | ST | ball_like | strike_like | false | strike_like | false | global_fallback_missing_pitch_type |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 22 | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 23 | KC | ball_like | strike_like | false | strike_like | false | global_fallback_missing_pitch_type |
| 2 | 2024-04-01 to 2024-04-02 | 2024-04-03 | 24 | SI | in_play_hit | strike_like | false | strike_like | false | pitch_type_majority |

Historical time-split baseline evaluation prototype only. Not live predictions, not betting advice.
