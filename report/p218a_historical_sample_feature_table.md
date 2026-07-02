# P218-A Historical Sample Feature Table Prototype

Historical sample feature table prototype only. Not live predictions, not betting advice.

## Summary

- Status: PASS_P216A_P217A_ARTIFACT_ONLY_HISTORICAL_SAMPLE_FEATURE_TABLE_PROTOTYPE
- Source row count: 24
- Source column count: 16
- Feature row count: 24
- Feature column count: 18

## Source Artifacts

| Artifact | SHA256 |
| --- | --- |
| `report/p216a_pybaseball_multidate_sample_pack.md` | `f3ad49921b60df67449c6c846777318b5c4e81d79db393b47a14eac0c1e800b9` |
| `report/p216a_pybaseball_multidate_sample_pack.json` | `c4f048a072097378978dbb71b1ba60749f0014157b91affd9a3438f6531e72c8` |
| `report/p216a_pybaseball_multidate_sample_pack.csv` | `e2d2eb233d4cb930ba7a886d7ca3350922aea671343ba23c6979f9dcedcac3c0` |
| `report/p217a_pybaseball_multidate_quality_dashboard.json` | `850cfc282505df70f5472133d16ec1772df5411bdddb26bf30be6b5c414ac516` |

## Feature Columns

- `source_row_id`
- `game_date`
- `game_pk`
- `home_team`
- `away_team`
- `inning`
- `inning_topbot`
- `pitcher`
- `batter`
- `pitch_type`
- `event_category`
- `is_in_play`
- `is_strike_like`
- `is_ball_like`
- `release_speed`
- `release_speed_bucket`
- `zone`
- `zone_bucket`

## Derived Feature Definitions

| Feature | Definition |
| --- | --- |
| `source_row_id` | 1-based lineage back to the original P216 CSV row before deterministic resorting. |
| `game_date` | Historical game date copied from the fixed P216 sample pack. |
| `game_pk` | Historical game identifier copied from the fixed P216 sample pack. |
| `home_team` | Home team code copied from the fixed P216 sample pack. |
| `away_team` | Away team code copied from the fixed P216 sample pack. |
| `inning` | Inning number copied from the fixed P216 sample pack. |
| `inning_topbot` | Half-inning label copied from the fixed P216 sample pack. |
| `pitcher` | Pitcher display name derived from the P216 player_name field. |
| `batter` | Batter identifier copied from the fixed P216 batter field because batter name is not present in the source artifact. |
| `pitch_type` | Pitch type code copied from the fixed P216 sample pack. |
| `event_category` | Heuristic categorical label derived only from the P216 events and description fields. |
| `is_in_play` | Boolean flag derived from event/description values that indicate contacted balls in play or resolved in-play outcomes. |
| `is_strike_like` | Boolean flag derived from strike-like descriptions or strikeout events. |
| `is_ball_like` | Boolean flag derived from ball-like descriptions or walk events. |
| `release_speed` | Numeric release_speed value parsed from the P216 CSV text snapshot. |
| `release_speed_bucket` | Velocity bucket derived from release_speed using fixed cutoffs: <85, 85-89.9, 90-94.9, 95+. |
| `zone` | Numeric zone value parsed from the P216 CSV text snapshot. |
| `zone_bucket` | Zone bucket derived from Statcast-style zone numbering: 1-9 in_zone, 11+ out_of_zone, else other_zone. |

## Limitations

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
- No betting advice claim.
- No production readiness claim.
- No ROI, EV, Kelly, CLV, or edge claim.

## Feature Table

| source_row_id | game_date | game_pk | home_team | away_team | inning | inning_topbot | pitcher | batter | pitch_type | event_category | is_in_play | is_strike_like | is_ball_like | release_speed | release_speed_bucket | zone | zone_bucket |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2024-04-01 | 745277 | SEA | CLE | 1 | Top | Hancock, Emerson | 680757 | SI | strike_like | false | true | false | 94.2 | 90_to_94_9 | 5 | in_zone |
| 2 | 2024-04-01 | 745277 | SEA | CLE | 1 | Top | Hancock, Emerson | 680757 | FF | strike_like | false | true | false | 94.5 | 90_to_94_9 | 8 | in_zone |
| 3 | 2024-04-01 | 745277 | SEA | CLE | 1 | Top | Hancock, Emerson | 680757 | CH | strikeout | false | true | false | 87.8 | 85_to_89_9 | 13 | out_of_zone |
| 4 | 2024-04-01 | 745277 | SEA | CLE | 1 | Top | Hancock, Emerson | 665926 | FF | strike_like | false | true | false | 93.7 | 90_to_94_9 | 7 | in_zone |
| 5 | 2024-04-01 | 745277 | SEA | CLE | 1 | Top | Hancock, Emerson | 665926 | FF | in_play_out | true | false | false | 94.6 | 90_to_94_9 | 1 | in_zone |
| 6 | 2024-04-01 | 745277 | SEA | CLE | 1 | Top | Hancock, Emerson | 608070 | SI | in_play_out | true | false | false | 93.4 | 90_to_94_9 | 7 | in_zone |
| 7 | 2024-04-01 | 745277 | SEA | CLE | 2 | Top | Hancock, Emerson | 647304 | CH | ball_like | false | false | true | 87.2 | 85_to_89_9 | 13 | out_of_zone |
| 8 | 2024-04-01 | 745277 | SEA | CLE | 2 | Top | Hancock, Emerson | 647304 | CH | in_play_out | true | false | false | 87.9 | 85_to_89_9 | 4 | in_zone |
| 9 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 680757 | SI | strike_like | false | true | false | 94.8 | 90_to_94_9 | 4 | in_zone |
| 10 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 680757 | FF | ball_like | false | false | true | 95.9 | 95_plus | 13 | out_of_zone |
| 11 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 680757 | FF | ball_like | false | false | true | 95.7 | 95_plus | 2 | in_zone |
| 12 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 680757 | FF | strike_like | false | true | false | 95.2 | 95_plus | 5 | in_zone |
| 13 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 680757 | FF | ball_like | false | false | true | 95.9 | 95_plus | 11 | out_of_zone |
| 14 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 680757 | SI | in_play_hit | true | false | false | 94.8 | 90_to_94_9 | 4 | in_zone |
| 15 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 665926 | FF | strike_like | false | true | false | 96.3 | 95_plus | 9 | in_zone |
| 16 | 2024-04-02 | 745273 | SEA | CLE | 1 | Top | Castillo, Luis | 665926 | FF | in_play_out | true | false | false | 93.7 | 90_to_94_9 | 3 | in_zone |
| 17 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 680757 | SI | in_play_hit | true | false | false | 95.8 | 95_plus | 7 | in_zone |
| 18 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 665926 | SI | strike_like | false | true | false | 94.9 | 90_to_94_9 | 13 | out_of_zone |
| 19 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 665926 | FF | strike_like | false | true | false | 94.8 | 90_to_94_9 | 1 | in_zone |
| 20 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 665926 | FS | hit_by_pitch | false | false | false | 84.3 | lt_85 | 14 | out_of_zone |
| 21 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 608070 | ST | ball_like | false | false | true | 88.7 | 85_to_89_9 | 14 | out_of_zone |
| 22 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 608070 | FF | strike_like | false | true | false | 95.4 | 95_plus | 1 | in_zone |
| 23 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 608070 | KC | ball_like | false | false | true | 83.3 | lt_85 | 14 | out_of_zone |
| 24 | 2024-04-03 | 745275 | SEA | CLE | 1 | Top | Kirby, George | 608070 | SI | in_play_hit | true | false | false | 95.0 | 95_plus | 4 | in_zone |

Historical sample feature table prototype only. Not live predictions, not betting advice.

