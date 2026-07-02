# P219-A Historical Feature Baseline Evaluation Prototype

Historical feature baseline evaluation prototype only. Not live predictions, not betting advice.

## Summary

- Status: PASS_P218A_ARTIFACT_ONLY_HISTORICAL_FEATURE_BASELINE_EVALUATION_PROTOTYPE
- Evaluated historical rows: 24
- Output column count: 11
- Target: `event_category`
- Baseline A accuracy: 0.375
- Baseline B accuracy: 0.5
- Baseline B coverage: 14 / 24 (0.583333)

## Source Artifacts

| Artifact | SHA256 |
| --- | --- |
| `report/p218a_historical_sample_feature_table.csv` | `d3d00176e3e40163c8d38a60019e204b0d37ef7efb745b638e797578f197b507` |
| `report/p218a_historical_sample_feature_table.json` | `60fde1062e935c7f5d37a693611e6433d765b905fb7e1a499c513bf728e39844` |
| `report/p218a_historical_sample_feature_table.md` | `28aa4b4d17bade86fe9c51990cf1798640967ea3a6e7388a81e54d485efbf016` |

## Evaluation Method

- Read the fixed P218 CSV/JSON/Markdown artifacts only.
- Evaluate the same 24 historical rows already present in the P218 feature table.
- Baseline A predicts the global majority event_category for every row.
- Baseline B predicts the within-pitch_type majority event_category only when that majority is unique; otherwise it falls back to the global majority event_category.
- Report deterministic in-sample accuracy, per-class support, confusion matrices, and pitch-type baseline coverage.

## Target Definition

- Target column: `event_category`
- Description: Historical categorical label copied from the fixed P218 feature table event_category column.

| Class | Support | Fraction |
| --- | --- | --- |
| `strike_like` | 9 | 0.375 |
| `ball_like` | 6 | 0.25 |
| `in_play_out` | 4 | 0.166667 |
| `in_play_hit` | 3 | 0.125 |
| `hit_by_pitch` | 1 | 0.041667 |
| `strikeout` | 1 | 0.041667 |

## Baseline Definitions

- Baseline A: Predict the most frequent event_category across all P218 rows for every row.
- Baseline A resolved prediction: `strike_like`
- Baseline B: Predict the most frequent event_category within each pitch_type when the pitch_type has a unique majority; otherwise predict the global majority event_category.
- Baseline B global fallback prediction: `strike_like`

### Pitch-Type Resolution Table

| Pitch Type | Support | Resolved Prediction | Prediction Source | Fallback |
| --- | --- | --- | --- | --- |
| `CH` | 3 | `strike_like` | `global_fallback_due_to_tie` | true |
| `FF` | 11 | `strike_like` | `pitch_type_majority` | false |
| `FS` | 1 | `hit_by_pitch` | `pitch_type_majority` | false |
| `KC` | 1 | `ball_like` | `pitch_type_majority` | false |
| `SI` | 7 | `strike_like` | `global_fallback_due_to_tie` | true |
| `ST` | 1 | `ball_like` | `pitch_type_majority` | false |

## Metric Summary

### Baseline A

- Accuracy: 0.375
- Correct rows: 9 / 24
- Coverage: 24 / 24 (1.0)

| Predicted Class | Count | Fraction |
| --- | --- | --- |
| `strike_like` | 24 | 1.0 |

#### Baseline A Confusion Matrix

| actual \ predicted | ball_like | hit_by_pitch | in_play_hit | in_play_out | strike_like | strikeout |
| --- | --- | --- | --- | --- | --- | --- |
| ball_like | 0 | 0 | 0 | 0 | 6 | 0 |
| hit_by_pitch | 0 | 0 | 0 | 0 | 1 | 0 |
| in_play_hit | 0 | 0 | 0 | 0 | 3 | 0 |
| in_play_out | 0 | 0 | 0 | 0 | 4 | 0 |
| strike_like | 0 | 0 | 0 | 0 | 9 | 0 |
| strikeout | 0 | 0 | 0 | 0 | 1 | 0 |

### Baseline B

- Accuracy: 0.5
- Correct rows: 12 / 24
- Coverage: 14 / 24 (0.583333)

| Predicted Class | Count | Fraction |
| --- | --- | --- |
| `strike_like` | 21 | 0.875 |
| `ball_like` | 2 | 0.083333 |
| `hit_by_pitch` | 1 | 0.041667 |

#### Baseline B Confusion Matrix

| actual \ predicted | ball_like | hit_by_pitch | in_play_hit | in_play_out | strike_like | strikeout |
| --- | --- | --- | --- | --- | --- | --- |
| ball_like | 2 | 0 | 0 | 0 | 4 | 0 |
| hit_by_pitch | 0 | 1 | 0 | 0 | 0 | 0 |
| in_play_hit | 0 | 0 | 0 | 0 | 3 | 0 |
| in_play_out | 0 | 0 | 0 | 0 | 4 | 0 |
| strike_like | 0 | 0 | 0 | 0 | 9 | 0 |
| strikeout | 0 | 0 | 0 | 0 | 1 | 0 |

## Per-Row Historical Baseline Output

| source_row_id | game_date | game_pk | pitcher | pitch_type | actual_event_category | baseline_a_global_prediction | baseline_a_correct | baseline_b_pitch_type_prediction | baseline_b_correct | baseline_b_prediction_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2024-04-01 | 745277 | Hancock, Emerson | SI | strike_like | strike_like | true | strike_like | true | global_fallback_due_to_tie |
| 2 | 2024-04-01 | 745277 | Hancock, Emerson | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 3 | 2024-04-01 | 745277 | Hancock, Emerson | CH | strikeout | strike_like | false | strike_like | false | global_fallback_due_to_tie |
| 4 | 2024-04-01 | 745277 | Hancock, Emerson | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 5 | 2024-04-01 | 745277 | Hancock, Emerson | FF | in_play_out | strike_like | false | strike_like | false | pitch_type_majority |
| 6 | 2024-04-01 | 745277 | Hancock, Emerson | SI | in_play_out | strike_like | false | strike_like | false | global_fallback_due_to_tie |
| 7 | 2024-04-01 | 745277 | Hancock, Emerson | CH | ball_like | strike_like | false | strike_like | false | global_fallback_due_to_tie |
| 8 | 2024-04-01 | 745277 | Hancock, Emerson | CH | in_play_out | strike_like | false | strike_like | false | global_fallback_due_to_tie |
| 9 | 2024-04-02 | 745273 | Castillo, Luis | SI | strike_like | strike_like | true | strike_like | true | global_fallback_due_to_tie |
| 10 | 2024-04-02 | 745273 | Castillo, Luis | FF | ball_like | strike_like | false | strike_like | false | pitch_type_majority |
| 11 | 2024-04-02 | 745273 | Castillo, Luis | FF | ball_like | strike_like | false | strike_like | false | pitch_type_majority |
| 12 | 2024-04-02 | 745273 | Castillo, Luis | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 13 | 2024-04-02 | 745273 | Castillo, Luis | FF | ball_like | strike_like | false | strike_like | false | pitch_type_majority |
| 14 | 2024-04-02 | 745273 | Castillo, Luis | SI | in_play_hit | strike_like | false | strike_like | false | global_fallback_due_to_tie |
| 15 | 2024-04-02 | 745273 | Castillo, Luis | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 16 | 2024-04-02 | 745273 | Castillo, Luis | FF | in_play_out | strike_like | false | strike_like | false | pitch_type_majority |
| 17 | 2024-04-03 | 745275 | Kirby, George | SI | in_play_hit | strike_like | false | strike_like | false | global_fallback_due_to_tie |
| 18 | 2024-04-03 | 745275 | Kirby, George | SI | strike_like | strike_like | true | strike_like | true | global_fallback_due_to_tie |
| 19 | 2024-04-03 | 745275 | Kirby, George | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 20 | 2024-04-03 | 745275 | Kirby, George | FS | hit_by_pitch | strike_like | false | hit_by_pitch | true | pitch_type_majority |
| 21 | 2024-04-03 | 745275 | Kirby, George | ST | ball_like | strike_like | false | ball_like | true | pitch_type_majority |
| 22 | 2024-04-03 | 745275 | Kirby, George | FF | strike_like | strike_like | true | strike_like | true | pitch_type_majority |
| 23 | 2024-04-03 | 745275 | Kirby, George | KC | ball_like | strike_like | false | ball_like | true | pitch_type_majority |
| 24 | 2024-04-03 | 745275 | Kirby, George | SI | in_play_hit | strike_like | false | strike_like | false | global_fallback_due_to_tie |

## Limitations

- This evaluation reuses the fixed 24-row P218 historical feature table only and does not refresh any upstream source.
- Baselines are deterministic heuristics for pipeline demonstration only and do not train or score a production model.
- Pitch-type baseline falls back to the global majority class whenever a pitch type has no unique within-pitch majority class.
- Results are in-sample on a bounded historical snapshot and must not be interpreted as future predictive ability.
- Feature rows are derived only from the fixed P216/P217 artifact snapshots and do not refresh upstream data.
- This prototype is a bounded preprocessing example for one small historical sample and is not a production feature contract.
- Several fields remain heuristic because the source artifacts do not include full context such as batter names, count state, or full plate appearance outcomes.
- One fixed three-day historical date range and one team filter only; this is a bounded sample pack, not a season-wide study.
- Output depends on the public historical pybaseball/statcast upstream response remaining available and schema-compatible for the fixed request.
- Sample rows are normalized into a deterministic, bounded CSV artifact for inspection only and are not production-ready data contracts.
- Dashboard metrics are computed from the fixed P216-A CSV snapshot only, not from a refreshed upstream pull.
- This dashboard reflects a small bounded multi-date historical sample and should not be generalized beyond the fixed date range and team filter.
- CSV typing is preserved as artifact text for determinism, so numeric-looking fields are summarized as stored snapshot values.

## Prohibited Claims

- No future prediction claim.
- No live prediction claim.
- No betting advice claim.
- No production readiness claim.
- No ROI, EV, Kelly, CLV, or edge claim.

Historical feature baseline evaluation prototype only. Not live predictions, not betting advice.

