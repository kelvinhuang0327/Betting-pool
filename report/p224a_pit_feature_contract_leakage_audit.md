# P224-A PIT Feature Contract + Baseline Derivation Window Leakage Audit

Historical PIT contract and leakage audit only. Not live predictions, not betting advice.

## Summary

- Status: PASS_P223A_ARTIFACT_ONLY_PIT_FEATURE_CONTRACT_AND_DERIVATION_WINDOW_LEAKAGE_AUDIT
- Leakage conclusion: NO_DERIVATION_WINDOW_LEAKAGE_DETECTED
- P218 feature columns classified: 18
- Committed P221 split count: 2
- Committed P221 evaluated rows: 16
- Committed Baseline A overall accuracy: 0.250000
- Committed Baseline B overall accuracy: 0.312500
- Recomputed Baseline A overall accuracy: 0.250000
- Recomputed Baseline B overall accuracy: 0.312500

## Source Hash Verification

| path | expected_sha256 | actual_sha256 | match |
| --- | --- | --- | --- |
| report/p218a_historical_sample_feature_table.csv | d3d00176e3e40163c8d38a60019e204b0d37ef7efb745b638e797578f197b507 | d3d00176e3e40163c8d38a60019e204b0d37ef7efb745b638e797578f197b507 | true |
| report/p218a_historical_sample_feature_table.json | 60fde1062e935c7f5d37a693611e6433d765b905fb7e1a499c513bf728e39844 | 60fde1062e935c7f5d37a693611e6433d765b905fb7e1a499c513bf728e39844 | true |
| report/p218a_historical_sample_feature_table.md | 28aa4b4d17bade86fe9c51990cf1798640967ea3a6e7388a81e54d485efbf016 | 28aa4b4d17bade86fe9c51990cf1798640967ea3a6e7388a81e54d485efbf016 | true |
| report/p221a_historical_time_split_baseline_evaluation.csv | 2d17483e66a11069806f4b0f49bcd905f1d427ab56425edef9f24aba8844d3ae | 2d17483e66a11069806f4b0f49bcd905f1d427ab56425edef9f24aba8844d3ae | true |
| report/p221a_historical_time_split_baseline_evaluation.json | 0ccec8bc6b01c5bbdd8a3c082cbbc161d4a5fc0f39cc3cfe51948199e7528982 | 0ccec8bc6b01c5bbdd8a3c082cbbc161d4a5fc0f39cc3cfe51948199e7528982 | true |
| report/p221a_historical_time_split_baseline_evaluation.md | f31c00dbd65a86ae0224cbd147c1e2c39c45a58e13791f702266c54cb5b05617 | f31c00dbd65a86ae0224cbd147c1e2c39c45a58e13791f702266c54cb5b05617 | true |

Observed P223 index artifacts:

| path | actual_sha256 | verification_basis |
| --- | --- | --- |
| report/p223a_historical_evaluation_evidence_index.json | 33cc52b2ec8cd6cf1d564725834710f93bbd3e2360c80ed2adee6262c901ad67 | authoritative_index_json_observed_directly |
| report/p223a_historical_evaluation_evidence_index.html | 8a77f4c9a2505222620aba27bc6ddf3edc2f9569a950ebac4450f18b36d3a7fe | paired_index_html_observed_directly |

## PIT Feature Contract

| column_name | pit_category | pregame_model_feature_allowed | in_game_analysis_allowed | label_or_outcome_only | audit_only | leakage_risk_level | required_guardrail | rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_row_id | identifier_or_lineage | false | false | false | true | low | Keep for lineage and row reconciliation only; never feed it to a model or scoring rule. | 1-based lineage back to the original P216 CSV row before deterministic resorting. It is a deterministic row identifier, not baseball context.. |
| game_date | pregame_known | true | true | false | false | low | If used in modeling, restrict to PIT-safe calendar transforms and avoid raw memorization keys. | Historical game date copied from the fixed P216 sample pack. The scheduled game date is known before first pitch.. |
| game_pk | identifier_or_lineage | false | false | false | true | low | Treat as lineage only; never use a game identifier as a predictive feature. | Historical game identifier copied from the fixed P216 sample pack. It identifies the historical game instance rather than pregame state.. |
| home_team | pregame_known | true | true | false | false | low | Use only as PIT-known team context and avoid target-encoding against the same evaluation rows. | Home team code copied from the fixed P216 sample pack. Home team assignment is fixed before the game starts.. |
| away_team | pregame_known | true | true | false | false | low | Use only as PIT-known team context and avoid target-encoding against the same evaluation rows. | Away team code copied from the fixed P216 sample pack. Away team assignment is fixed before the game starts.. |
| inning | in_play_measured | false | true | false | false | low | Allow only for in-game analysis products; exclude from pregame feature sets. | Inning number copied from the fixed P216 sample pack. The inning number is only known once live game state progresses.. |
| inning_topbot | in_play_measured | false | true | false | false | low | Allow only for in-game analysis products; exclude from pregame feature sets. | Half-inning label copied from the fixed P216 sample pack. Half-inning state is determined during live play.. |
| pitcher | in_play_measured | false | true | false | false | medium | Do not reuse the realized event-row pitcher as a pregame feature without a separate PIT starter or roster contract. | Pitcher display name derived from the P216 player_name field. This artifact records the pitcher who actually threw the sampled pitch, which may depend on realized game usage.. |
| batter | in_play_measured | false | true | false | false | medium | Do not reuse the realized plate-appearance batter as a pregame feature without a separate PIT lineup contract. | Batter identifier copied from the fixed P216 batter field because batter name is not present in the source artifact. This artifact records the batter who actually appeared in the sampled pitch event.. |
| pitch_type | in_play_measured | false | true | false | false | medium | Never expose realized pitch selection to a pregame model; reserve it for post-release audit or in-game analysis. | Pitch type code copied from the fixed P216 sample pack. Pitch type is observed only after the pitch is thrown.. |
| event_category | outcome_derived | false | false | true | false | high | Use strictly as the label or evaluation outcome; never feed it back as an input feature. | Heuristic categorical label derived only from the P216 events and description fields. It is the derived target outcome for the pitch event.. |
| is_in_play | outcome_derived | false | false | true | false | high | Treat as an outcome-only flag derived from realized play; do not allow it into pregame or causal feature sets. | Boolean flag derived from event/description values that indicate contacted balls in play or resolved in-play outcomes. The flag is derived from whether the pitch event resolved into ball-in-play behavior.. |
| is_strike_like | outcome_derived | false | false | true | false | high | Treat as an outcome-only flag derived from realized pitch result; never reuse as an input feature. | Boolean flag derived from strike-like descriptions or strikeout events. The flag is derived from realized strike-like descriptions or strikeout events.. |
| is_ball_like | outcome_derived | false | false | true | false | high | Treat as an outcome-only flag derived from realized pitch result; never reuse as an input feature. | Boolean flag derived from ball-like descriptions or walk events. The flag is derived from realized ball-like descriptions or walk outcomes.. |
| release_speed | in_play_measured | false | true | false | false | medium | Keep as realized pitch telemetry only; exclude from any pregame contract. | Numeric release_speed value parsed from the P216 CSV text snapshot. Release speed is measured only when the pitch is thrown.. |
| release_speed_bucket | in_play_measured | false | true | false | false | medium | Keep as realized pitch telemetry only; exclude from any pregame contract. | Velocity bucket derived from release_speed using fixed cutoffs: <85, 85-89.9, 90-94.9, 95+. The bucket is derived from realized release speed after the pitch occurs.. |
| zone | in_play_measured | false | true | false | false | medium | Treat as post-release pitch-location telemetry only; exclude from pregame feature contracts. | Numeric zone value parsed from the P216 CSV text snapshot. Pitch zone is observed from the realized pitch location.. |
| zone_bucket | in_play_measured | false | true | false | false | medium | Treat as post-release pitch-location telemetry only; exclude from pregame feature contracts. | Zone bucket derived from Statcast-style zone numbering: 1-9 in_zone, 11+ out_of_zone, else other_zone. The bucket is derived from realized pitch location after the pitch occurs.. |

## Metrics Delta Table

| scope | split_id | eval_date | baseline | committed_accuracy | recomputed_accuracy | accuracy_delta | committed_correct_count | recomputed_correct_count | correct_count_delta | committed_row_count | recomputed_row_count | row_count_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| split_1 | 1 | 2024-04-02 | baseline_a_global_majority | 0.125000 | 0.125000 | 0.000000 | 1 | 1 | 0 | 8 | 8 | 0 |
| split_1 | 1 | 2024-04-02 | baseline_b_pitch_type_majority_with_global_fallback | 0.250000 | 0.250000 | 0.000000 | 2 | 2 | 0 | 8 | 8 | 0 |
| split_2 | 2 | 2024-04-03 | baseline_a_global_majority | 0.375000 | 0.375000 | 0.000000 | 3 | 3 | 0 | 8 | 8 | 0 |
| split_2 | 2 | 2024-04-03 | baseline_b_pitch_type_majority_with_global_fallback | 0.375000 | 0.375000 | 0.000000 | 3 | 3 | 0 | 8 | 8 | 0 |
| overall |  | overall | baseline_a_global_majority | 0.250000 | 0.250000 | 0.000000 | 4 | 4 | 0 | 16 | 16 | 0 |
| overall |  | overall | baseline_b_pitch_type_majority_with_global_fallback | 0.312500 | 0.312500 | 0.000000 | 5 | 5 | 0 | 16 | 16 | 0 |

## Row Comparison Table

| split_id | eval_date | source_row_id | pitch_type | actual_event_category | committed_baseline_a_prediction | recomputed_baseline_a_prediction | baseline_a_prediction_match | committed_baseline_b_prediction | recomputed_baseline_b_prediction | baseline_b_prediction_match | committed_baseline_b_prediction_source | recomputed_baseline_b_prediction_source | baseline_b_prediction_source_match | all_prediction_fields_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2024-04-02 | 9 | SI | strike_like | in_play_out | in_play_out | true | in_play_out | in_play_out | true | global_fallback_due_to_tie | global_fallback_due_to_tie | true | true |
| 1 | 2024-04-02 | 10 | FF | ball_like | in_play_out | in_play_out | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 1 | 2024-04-02 | 11 | FF | ball_like | in_play_out | in_play_out | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 1 | 2024-04-02 | 12 | FF | strike_like | in_play_out | in_play_out | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 1 | 2024-04-02 | 13 | FF | ball_like | in_play_out | in_play_out | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 1 | 2024-04-02 | 14 | SI | in_play_hit | in_play_out | in_play_out | true | in_play_out | in_play_out | true | global_fallback_due_to_tie | global_fallback_due_to_tie | true | true |
| 1 | 2024-04-02 | 15 | FF | strike_like | in_play_out | in_play_out | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 1 | 2024-04-02 | 16 | FF | in_play_out | in_play_out | in_play_out | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 2 | 2024-04-03 | 17 | SI | in_play_hit | strike_like | strike_like | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 2 | 2024-04-03 | 18 | SI | strike_like | strike_like | strike_like | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 2 | 2024-04-03 | 19 | FF | strike_like | strike_like | strike_like | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 2 | 2024-04-03 | 20 | FS | hit_by_pitch | strike_like | strike_like | true | strike_like | strike_like | true | global_fallback_missing_pitch_type | global_fallback_missing_pitch_type | true | true |
| 2 | 2024-04-03 | 21 | ST | ball_like | strike_like | strike_like | true | strike_like | strike_like | true | global_fallback_missing_pitch_type | global_fallback_missing_pitch_type | true | true |
| 2 | 2024-04-03 | 22 | FF | strike_like | strike_like | strike_like | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |
| 2 | 2024-04-03 | 23 | KC | ball_like | strike_like | strike_like | true | strike_like | strike_like | true | global_fallback_missing_pitch_type | global_fallback_missing_pitch_type | true | true |
| 2 | 2024-04-03 | 24 | SI | in_play_hit | strike_like | strike_like | true | strike_like | strike_like | true | pitch_type_majority | pitch_type_majority | true | true |

## Limitations

- Historical artifact audit only: all conclusions are bounded to the fixed committed P218, P221, and P223 artifacts.
- The audit verifies train-window-only derivation for the committed baseline heuristics; it does not establish production readiness or future predictive value.
- P223 can verify the P218 and P221 source artifact hashes it indexes, but its own JSON and HTML files are observed directly rather than self-hashed inside the same index.
- PIT classifications for participant identity fields remain conservative because the artifact captures realized pitch-event participants, not a separate pregame roster contract.

## Prohibited Claims

- No future prediction claim.
- No live prediction claim.
- No betting advice claim.
- No production readiness claim.
- No edge, ROI, EV, Kelly, or CLV claim.

Historical PIT contract and leakage audit only. Not live predictions, not betting advice.
