# P230-A — Local Multi-Season Run Line Data Availability Audit

> **本機資料可用性盤點（read-only）。** 非模型任務、非預測任務、非 production/live/real-betting 任務；純盤點本機既有檔案是否足以將 Run Line 評估延伸至 2025（P226-A/P228-A/P229-A）既有證據之外。

## 範疇聲明
- LOCAL DATA AVAILABILITY AUDIT ONLY — not a modeling task, not a prediction task, not a production/live/real-betting task
- read-only inventory of already-present local files under data/; NO remote fetch, NO pybaseball, NO DB writes, NO data file modification, NO new dependency
- NO future prediction; NO betting recommendation; NO EV/Kelly claim; NOT a proven edge
- NO live-market claim; NOT production; NOT real betting; NO model implementation
- P226-A / P227-A / P228-A / P229-A source artifacts are read-only reference inputs and are not modified by this audit
- recommended next technical step is NOT authorized by this audit; a separate explicit Owner authorization is required before any further work begins

## 1. Season Inventory & Classification
| season | classification | final_scores | teams | date | RL spread | RL prices | metadata |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 2024 | `LABEL_ONLY_NO_ODDS` | YES | YES | YES | no | no | YES |
| 2025 | `FULL_RUNLINE_EVAL_READY` | YES | YES | YES | YES | YES | YES |
| 2026 | `MISSING_OR_UNUSABLE` | no | YES | YES | no | no | no |

### Season 2024
- **Classification**: `LABEL_ONLY_NO_ODDS`
- Files:
  - `data/mlb_2025/mlb-2024-asplayed.csv` — exists=YES, row_count=2429
  - `data/mlb_2025/mlb-2024-asplayed.csv.metadata.json` — exists=YES, row_count=—
  - `data/mlb_2025/gl2024.txt` — exists=YES, row_count=2429
  - `data/mlb_2025/gl2024.zip` — exists=YES, row_count=—
  - `data/mlb_2025/mlb_odds_2024_real.csv` — exists=no, row_count=—
- Blockers:
  - missing_run_line_spread — no local run line odds/spread file exists for 2024 (data/mlb_2025/mlb_odds_2024_real.csv does not exist)
  - missing_run_line_prices — same as above; no RL price fields locally available
  - no_local_odds_file_2024 — P70 (The Odds API historical pull) ran DRY_RUN only with 0 rows written and no API key configured (data/mlb_2025/derived/p70_path_a_the_odds_api_historical_pull_summary.json); P67 free-source search found no downloadable 2024 MLB odds source (report/p67_2024_data_gap_free_source_search_20260526.md, classification P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW); even if P70 had run, its scope was moneyline (h2h) only, not run line
- Notes: final scores + home/away + date are Retrosheet-verified (sha256-checked against gl2024.txt per metadata); this is a warm-up/label-only dataset with no locally available run line odds of any kind.

### Season 2025
- **Classification**: `FULL_RUNLINE_EVAL_READY`
- Files:
  - `data/mlb_2025/mlb-2025-asplayed.csv` — exists=YES, row_count=2430
  - `data/mlb_2025/mlb-2025-asplayed.csv.metadata.json` — exists=YES, row_count=—
  - `data/mlb_2025/mlb_odds_2025_real.csv` — exists=YES, row_count=2430
  - `data/mlb_2025/mlb_odds_2025_real.csv.metadata.json` — exists=YES, row_count=—
  - `data/mlb_2025/gl2025.txt` — exists=YES, row_count=2430
- Blockers:
  - unverified_odds_provenance — mlb_odds_2025_real.csv.metadata.json declares source_chain_verified=false and the CSV rows carry is_verified_real=False (source_type=user_supplied_xlsx from mlb-odds.xlsx); already documented as a post-game unverified snapshot in P226-A/P229-A, NOT a point-in-time pregame feed — this is the same known limitation carried into this season, not new.
- Notes: this is the existing P226-A/P228-A/P229-A evidence base itself — already fully utilized, not additional/unused local coverage.

### Season 2026
- **Classification**: `MISSING_OR_UNUSABLE`
- Files:
  - `data/mlb_2026/schedule/mlb_2026_schedule.jsonl` — exists=YES, row_count=2430
  - `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl` — exists=YES, row_count=828
- Blockers:
  - missing_final_scores — 0 of 828 local prediction rows have result_home_score populated; season 2026 is in progress as of this audit (no local asplayed/final-score file exists for 2026)
  - missing_run_line_spread — schedule/prediction jsonl schemas carry no run line spread field
  - missing_run_line_prices — schedule/prediction jsonl schemas carry no run line price field (prediction rows explicitly set odds_used=false)
  - no_metadata_provenance_file — no *.metadata.json provenance file exists for the 2026 schedule/prediction jsonl inputs
- Notes: schedule has 2430 scheduled games; predictions jsonl has 828 rows but 0 with an observed final score — current in-season data, not usable as a completed evaluation season.

## 2. Excluded / Out-of-Scope Local Data
已於 data/ 下找到但不計入本次球季盤點（原因：非 MLB 聯盟或為既有 2025 資料的重複衍生檢視）：
- `data/tsl_odds_history.jsonl` — non_mlb_league — sampled team names are NPB/KBO clubs (e.g. 羅德海洋/Chiba Lotte Marines, 西武獅/Seibu Lions, 起亞老虎/KIA Tigers, SSG登陸者/SSG Landers), not MLB; out of scope for an MLB run line audit
- `data/tsl_odds_snapshot.json` — non_mlb_league — sampled game entries are NPB clubs (e.g. 樂天金鷲/Rakuten Eagles, 西武獅/Seibu Lions); also a single-day snapshot (9 games), not season coverage
- `data/mlb_context/odds_timeline.jsonl` — derived_duplicate — moneyline-only re-projection of the same 2025 mlb_odds_2025_real.csv rows (source field cites mlb_odds_2025_real.csv); no run line field; not a new season
- `data/mlb_context_sources/odds_timeline_canonical.jsonl` — derived_duplicate — same underlying 2025 moneyline rows as odds_timeline.jsonl; carries validation_flags including missing_closing/missing_decision/missing_latest_pregame; no run line field; not a new season

## 3. Recommended Next Technical Step
- **候選（chosen）**：`stop_data_gap`
- 授權狀態：`NOT_AUTHORIZED_YET`
- Rationale: Only 1 of 3 locally discoverable candidate seasons (2025) carries both final scores AND run line spread/prices; 2024 has verified final scores but no locally available run line odds of any kind (two prior dedicated tasks, P67 free-source search and P70 paid-API dry-run, already confirmed this is a structural gap, not a missed lookup); 2026 has zero locally observed final scores (season in progress). Multi-season Run Line backtest expansion is therefore not locally supportable today — this is a genuine local data gap, not a schema or normalization problem.
- This audit recommends but does not authorize the next step; a separate explicit Owner authorization is required before any further work begins. If further work is desired despite this gap, the most locally-actionable alternative (not chosen here) would be a true-PIT odds provenance audit of the existing 2025 season odds source, since that does not require new season data.

## 免責聲明
- **NOT A MODELING TASK**：本檔不訓練、不重跑、不修改任何模型。
- **NOT A PREDICTION TASK**：無未來預測、無 upcoming game 宣稱。
- **NOT PRODUCTION / LIVE / REAL BETTING**：無 production/DB 變更、無即時市場串接、無真實下注。
- **NOT A PROVEN EDGE**：本報告不構成已證實的下注優勢宣稱，僅為本機資料可用性盤點。
- **P226-A/P227-A/P228-A/P229-A UNCHANGED**：本任務未讀寫任何上述任務的既有產出檔案。
