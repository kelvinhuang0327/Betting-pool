# Data Sources


Purpose

Canonical list of data feeds, ingestion owners, schema rules and QA requirements.

Key Concepts

- Sources: MLB/NPB/KBO historical feeds, WBC official live roster/schedule, odds providers (Odds API, SportsDataIO), TSL snapshots.
- Local artifacts: `data/wbc_backend/reports/`, `data/mlb_2025/`, `data/tsl_*`.

Rules / Constraints (schema & timestamps)

- Required timeline fields (MLB timeline spec): `game_id`, `source`, `book`, `market_type`, `opening_*`, `decision_*`, `latest_pregame_*`, `closing_*`, timestamp fields and `fetched_at`.
- Timestamp monotonicity: `opening_ts <= decision_ts <= latest_pregame_ts <= closing_ts`. Violations mark record invalid for strict CLV use.
- Preserve provider raw timestamps; normalize to UTC only for storage.
- Team normalization: use canonical mapping table; unresolved mappings remain explicit (no fuzzy auto-merge).

QA Requirements

- Coverage gate: mapped_games / total_csv_games >= 0.80 for canonical timeline.
- Timestamp integrity: separate availability metrics per timepoint.
- Output artifacts: `data/mlb_context_sources/odds_timeline_canonical.jsonl`, QA reports under `data/wbc_backend/reports/`.

Known Duplications & Notes

- `data/tsl_crawler.py` vs `data/tsl_crawler_v2.py`: confirm which module is the active integration and update importers accordingly (risk: v1 still imported by some loaders).

Source

docs/mlb_2025_historical_odds_timeline_asset_spec.md, docs/wbc_backend_architecture.md

