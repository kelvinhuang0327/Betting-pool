# MLB 2025 Historical Odds Timeline Asset Spec

## Purpose
Provide a production-grade historical odds timeline for MLB 2025 so CLV and per-game decision quality can be evaluated at scale under strict governance.

## Scope
- League: MLB
- Season: 2025 regular season (primary)
- Market: moneyline (phase 1)
- Target coverage: >= 80% of `data/mlb_2025/mlb_odds_2025_real.csv` games

## Required Fields (Per Game)
- `game_id` (`MLB-{date}-{start_time}-{away}-AT-{home}`)
- `source` (provider name)
- `book` (bookmaker identifier)
- `market_type` (`moneyline`)
- `opening_home_ml`, `opening_away_ml`
- `decision_home_ml`, `decision_away_ml`
- `latest_pregame_home_ml`, `latest_pregame_away_ml`
- `closing_home_ml`, `closing_away_ml`
- `opening_ts`, `decision_ts`, `latest_pregame_ts`, `closing_ts`
- `fetched_at`
- `odds_history[]` snapshot list
- `unavailable_fields[]` explicit missing markers

## Timestamp Requirements
- Preserve raw provider timestamps; no synthetic timestamps.
- All timestamps normalized to UTC for storage.
- Time ordering must satisfy:
  - `opening_ts <= decision_ts <= latest_pregame_ts <= closing_ts`
  - no post-start leakage into `decision_*`
- If ordering fails, mark record invalid for strict CLV use.

## Mapping Rules
- Team normalization table must map provider team names to canonical MLB names.
- Timezone normalization must convert provider game time to ET before `game_id` construction.
- `game_id` generation must use `make_mlb_game_id` only.
- No fuzzy auto-merge when multiple candidates exist; unresolved mappings remain explicit unmatched records.

## Acceptable Sources
- The Odds API historical snapshots (book-level timestamps).
- SportsDataIO odds history feed.
- Equivalent source only if it provides timestamped pregame snapshots and bookmaker IDs.

## QA Requirements
- Coverage:
  - `mapped_games_to_csv / total_csv_games >= 0.80`
- Timepoint availability rates:
  - opening/decision/latest/closing each reported separately
- Timestamp monotonicity violations count
- Duplicate snapshot resolution count
- Unmatched game mapping count
- Per-source contribution and freshness diagnostics

## Governance Gates
- MLB remains `PAPER_ONLY` until:
  - coverage gate pass (`>=80%`)
  - timestamp integrity gate pass
  - CLV availability gate pass on strict universe
- No live recommendation/sizing/execution while gate is red.

## Output Artifacts
- Canonical timeline file:
  - `data/mlb_context_sources/odds_timeline_canonical.jsonl`
- QA report:
  - `data/wbc_backend/reports/mlb_odds_timeline_qa_report.json`
- Source audit:
  - `data/wbc_backend/reports/mlb_odds_source_audit.json`
