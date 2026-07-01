# P214-A pybaseball Historical Sample Smoke

Historical pybaseball read-only sample smoke only. Not live predictions, not betting advice.

## Summary

- Status: PASS_FIXED_HISTORICAL_READ_ONLY_SAMPLE
- Source library: pybaseball 2.2.7
- Source function: pybaseball.statcast
- Fixed request: 2024-04-01..2024-04-01 team=SEA
- Fetched row count: 121
- Snapshot row count: 12
- Snapshot columns: game_date, game_pk, home_team, away_team, inning, inning_topbot, at_bat_number, pitch_number, batter, pitcher, pitch_type, events, description, release_speed, zone

## Observed Date Range

- Start: 2024-04-01
- End: 2024-04-01

## Guardrails

- Historical pybaseball read-only sample smoke only. Not live predictions, not betting advice.
- Read-only historical sample only; no live odds, no paid provider, and no production endpoint calls were made by this adapter.
- No database writes, model integration, or future-ticket mutation were performed.
- No custom MLB scraper or parser was implemented; data access is delegated to pybaseball.

## Limitations

- One fixed historical date and one team filter only; this is a bounded smoke sample, not a season-wide study.
- Output depends on the public historical pybaseball/statcast upstream response remaining available for the fixed request.
- Snapshot records are normalized to a small deterministic subset for inspection and are not production-ready data contracts.

## Snapshot

| game_date | game_pk | home_team | away_team | inning | inning_topbot | at_bat_number | pitch_number | batter | pitcher | pitch_type | events | description | release_speed | zone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 1 | 1 | 680757 | 676106 | SI |  | called_strike | 94.2 | 5 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 1 | 2 | 680757 | 676106 | FF |  | called_strike | 94.5 | 8 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 1 | 3 | 680757 | 676106 | CH | strikeout | swinging_strike | 87.8 | 13 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 2 | 1 | 665926 | 676106 | FF |  | called_strike | 93.7 | 7 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 2 | 2 | 665926 | 676106 | FF | field_out | hit_into_play | 94.6 | 1 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 3 | 1 | 608070 | 676106 | SI | field_out | hit_into_play | 93.4 | 7 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 7 | 1 | 647304 | 676106 | CH |  | ball | 87.2 | 13 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 7 | 2 | 647304 | 676106 | CH | field_out | hit_into_play | 87.9 | 4 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 8 | 1 | 671289 | 676106 | SI |  | foul | 94.2 | 13 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 8 | 2 | 671289 | 676106 | SI |  | called_strike | 94.0 | 8 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 8 | 3 | 671289 | 676106 | CH |  | ball | 89.7 | 14 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 8 | 4 | 671289 | 676106 | CH | field_out | hit_into_play | 85.1 | 5 |

Historical pybaseball read-only sample smoke only. Not live predictions, not betting advice.

