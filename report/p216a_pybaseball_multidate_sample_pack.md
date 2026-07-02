# P216-A pybaseball Multi-Date Historical Sample Pack

Historical pybaseball multi-date sample pack only. Not live predictions, not betting advice.

## Summary

- Status: PASS_FIXED_MULTIDATE_HISTORICAL_SAMPLE_PACK
- Source library: pybaseball 2.2.7
- Source function: pybaseball.statcast
- Requested date range: 2024-04-01..2024-04-03
- Team filter: SEA
- Row count: 24
- Column count: 16
- Fetched row count: 383
- Fetched column count: 119

## Sample Size Limits

- Per-date row limit: 8
- Total row limit: 24
- Preview row limit: 5
- Requested date count: 3

## Observed Dates

- Observed dates: 2024-04-01, 2024-04-02, 2024-04-03

## Artifact Hashes

- CSV SHA256: e2d2eb233d4cb930ba7a886d7ca3350922aea671343ba23c6979f9dcedcac3c0

## Guardrails

- Historical pybaseball multi-date sample pack only. Not live predictions, not betting advice.
- Read-only historical sample pack only; no live odds, no paid provider, and no production endpoint calls were made by this adapter.
- No database writes, model integration, or future-ticket mutation were performed.
- No custom MLB scraper or parser was implemented; data access is delegated to pybaseball.

## Limitations

- One fixed three-day historical date range and one team filter only; this is a bounded sample pack, not a season-wide study.
- Output depends on the public historical pybaseball/statcast upstream response remaining available and schema-compatible for the fixed request.
- Sample rows are normalized into a deterministic, bounded CSV artifact for inspection only and are not production-ready data contracts.

## Prohibited Claims

- No future prediction claim.
- No betting advice claim.
- No production readiness claim.
- No ROI, EV, Kelly, CLV, or edge claim.

## Sample Pack

| game_date | game_pk | home_team | away_team | inning | inning_topbot | at_bat_number | pitch_number | player_name | batter | pitcher | pitch_type | events | description | release_speed | zone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 1 | 1 | Hancock, Emerson | 680757 | 676106 | SI |  | called_strike | 94.2 | 5 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 1 | 2 | Hancock, Emerson | 680757 | 676106 | FF |  | called_strike | 94.5 | 8 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 1 | 3 | Hancock, Emerson | 680757 | 676106 | CH | strikeout | swinging_strike | 87.8 | 13 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 2 | 1 | Hancock, Emerson | 665926 | 676106 | FF |  | called_strike | 93.7 | 7 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 2 | 2 | Hancock, Emerson | 665926 | 676106 | FF | field_out | hit_into_play | 94.6 | 1 |
| 2024-04-01 | 745277 | SEA | CLE | 1 | Top | 3 | 1 | Hancock, Emerson | 608070 | 676106 | SI | field_out | hit_into_play | 93.4 | 7 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 7 | 1 | Hancock, Emerson | 647304 | 676106 | CH |  | ball | 87.2 | 13 |
| 2024-04-01 | 745277 | SEA | CLE | 2 | Top | 7 | 2 | Hancock, Emerson | 647304 | 676106 | CH | field_out | hit_into_play | 87.9 | 4 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 1 | 1 | Castillo, Luis | 680757 | 622491 | SI |  | called_strike | 94.8 | 4 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 1 | 2 | Castillo, Luis | 680757 | 622491 | FF |  | ball | 95.9 | 13 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 1 | 3 | Castillo, Luis | 680757 | 622491 | FF |  | ball | 95.7 | 2 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 1 | 4 | Castillo, Luis | 680757 | 622491 | FF |  | foul | 95.2 | 5 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 1 | 5 | Castillo, Luis | 680757 | 622491 | FF |  | ball | 95.9 | 11 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 1 | 6 | Castillo, Luis | 680757 | 622491 | SI | single | hit_into_play | 94.8 | 4 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 2 | 1 | Castillo, Luis | 665926 | 622491 | FF |  | called_strike | 96.3 | 9 |
| 2024-04-02 | 745273 | SEA | CLE | 1 | Top | 2 | 2 | Castillo, Luis | 665926 | 622491 | FF | field_out | hit_into_play | 93.7 | 3 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 1 | 1 | Kirby, George | 680757 | 669923 | SI | single | hit_into_play | 95.8 | 7 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 2 | 1 | Kirby, George | 665926 | 669923 | SI |  | called_strike | 94.9 | 13 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 2 | 2 | Kirby, George | 665926 | 669923 | FF |  | swinging_strike | 94.8 | 1 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 2 | 3 | Kirby, George | 665926 | 669923 | FS | hit_by_pitch | hit_by_pitch | 84.3 | 14 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 3 | 1 | Kirby, George | 608070 | 669923 | ST |  | blocked_ball | 88.7 | 14 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 3 | 2 | Kirby, George | 608070 | 669923 | FF |  | called_strike | 95.4 | 1 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 3 | 3 | Kirby, George | 608070 | 669923 | KC |  | ball | 83.3 | 14 |
| 2024-04-03 | 745275 | SEA | CLE | 1 | Top | 3 | 4 | Kirby, George | 608070 | 669923 | SI | double | hit_into_play | 95.0 | 4 |

Historical pybaseball multi-date sample pack only. Not live predictions, not betting advice.

