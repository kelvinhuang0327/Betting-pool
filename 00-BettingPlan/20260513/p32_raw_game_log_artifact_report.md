# P32 Raw Game Log Artifact Report

**Date**: 2026-05-13T03:57:45Z
**Phase**: P32 — 2024 Raw Game Log Artifact Layer (PAPER_ONLY)
**PAPER_ONLY**: True
**production_ready**: False

---

## 1. Repo Evidence
- Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`
- Branch: `p13-clean`
- P31 commit: `6b0ab64`
- P31 gate: `P31_HONEST_DATA_AUDIT_READY`

## 2. Prior Phase Evidence (P31)
| Metric | Value |
| --- | --- |
| Total classified sources | 1,397 |
| RAW_PRIMARY | 1 (2025 only) |
| RAW_SECONDARY | 0 |
| DERIVED_OUTPUT | 1,372 |
| SCHEMA_PARTIAL | 24 |
| usable_2024_raw | 0 |
| P32 recommendation | GO_PARTIAL_GAME_LOGS_ONLY |

## 3. Why P32 Is Partial Only
P31 confirmed that 2024 closing moneyline odds have no confirmed license-safe provider. P32 therefore builds ONLY the game identity/outcome artifact from Retrosheet game logs. **No odds artifact is built. No prediction artifact is built.**

## 3b. Prior P32 BLOCKED State
- Prior gate (commit `d7766bc`): `P32_BLOCKED_SOURCE_FILE_MISSING`
- Reason: `data/mlb_2024/raw/gl2024.txt` was absent at build time
- Prior report marker: `P32_RAW_GAME_LOG_ARTIFACT_BLOCKED_SOURCE_MISSING`
- P32 implementation and 145 tests were committed while blocked

## 3c. Manual Source Provisioning Evidence (P32.5)
- Source downloaded from: `https://www.retrosheet.org/gamelogs/gl2024.zip`
- Extracted to: `data/mlb_2024/raw/gl2024.txt`
- File size: 2.5 MB (2,650,378 bytes)
- Line count: 2,429 rows
- First game: `2024-03-20` (Seoul Series, LAN @ SDN)
- Raw file NOT staged / NOT committed (per Hard Guard)
- Git status: `?? data/mlb_2024/raw/gl2024.txt` (untracked only)

## 4. Source File Availability
- Source path: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt`
- Status: **AVAILABLE** (2,650,378 bytes)

## 5. Retrosheet Schema Parser Design
- File format: CSV with no header, 161+ positional columns.
- Column 0: date (YYYYMMDD)
- Column 1: game number in doubleheader (0/1/2)
- Column 3: visiting (away) team 3-letter ID
- Column 6: home team 3-letter ID
- Column 9: visiting score
- Column 10: home score
- game_id: `<HOME>-<YYYYMMDD>-<game_number>` (deterministic)
- y_true_home_win: 1 if home_score > away_score, 0 if away wins, None if tied/missing.
- Missing scores → None (not fabricated).

## 6. Processed Artifact Outputs
| Metric | Value |
| --- | --- |
| row_count_raw | 2,429 |
| row_count_processed | 2,429 |
| unique_game_id_count | 2,429 |
| date_start | 2024-03-20 |
| date_end | 2024-09-30 |
| teams_detected_count | 60 |
| outcome_coverage_pct | 100.00% |
| contains_odds | False |
| contains_predictions | False |

Artifacts written to `data/mlb_2024/processed/`:
  - `mlb_2024_game_identity.csv` (153 KB, 2,429 rows — game_id, game_date, teams only, no scores)
  - `mlb_2024_game_outcomes.csv` (168 KB, 2,429 rows — includes scores and y_true_home_win)
  - `mlb_2024_game_identity_outcomes_joined.csv` (168 KB, 2,429 rows — full join)
  - `mlb_2024_game_log_summary.json`
  - `mlb_2024_retrosheet_provenance.json`
  - `mlb_2024_game_log_manifest.json`
  - `p32_gate_result.json` (gate=P32_RAW_GAME_LOG_ARTIFACT_READY)

## 7. Provenance / Attribution
```
Source: Retrosheet (season=2024)
  License: ATTRIBUTION_REQUIRED
  Attribution required: True
  URL: https://www.retrosheet.org/gamelogs/index.html
  Source file: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt [AVAILABLE]
  No odds: True
  No predictions: True
  paper_only: True
  production_ready: False
```

**Attribution text** (Retrosheet requirement):
> The information used here was obtained free of charge from and is copyrighted by Retrosheet. Interested parties may contact Retrosheet at www.retrosheet.org.

## 8. Test Results
Run: `./.venv/bin/pytest tests/test_p32_*.py tests/test_p31_*.py tests/test_p30_*.py -q`

| Suite | Tests | Result |
| --- | --- | --- |
| P32 (contract, parser, writer, provenance, CLI) | 145 | ✅ PASS |
| P31 regression (audit, provenance, CLI) | 71 | ✅ PASS |
| P30 regression (contract, inventory, CLI) | 72 | ✅ PASS |
| **Total** | **288** | **✅ ALL PASS** |

## 9. Determinism Result
`DETERMINISM_OK` — Verified by running P32 twice into `/tmp/p32_det_ready_run1` and `/tmp/p32_det_ready_run2`:

| File | Result |
| --- | --- |
| `p32_gate_result.json` (excl. generated_at/paths) | ✅ MATCH |
| `mlb_2024_game_log_summary.json` | ✅ MATCH |
| `mlb_2024_game_identity.csv` | ✅ EXACT byte-for-byte match |
| `mlb_2024_game_outcomes.csv` | ✅ EXACT byte-for-byte match |
| `mlb_2024_game_identity_outcomes_joined.csv` | ✅ EXACT byte-for-byte match |

game_id is deterministic: `<HOME_TEAM>-<YYYYMMDD>-<game_number>` — no random components.

## 10. Production Readiness Statement
| Control | Value |
| --- | --- |
| PAPER_ONLY | True |
| production_ready | False |
| Live TSL called | False |
| Real bets placed | False |
| Odds artifact built | False |
| Prediction artifact built | False |
| Scheduler/daemon enabled | False |

## 11. Remaining Limitations
- **No 2024 closing odds**: Moneyline model training blocked until a license-safe odds source is confirmed.
- **Sample wall not solved**: Raw game logs increase game-identity coverage but full model training rows require joined odds data.
- **gl2024.txt is local only**: Source file not committed. Must be re-downloaded from Retrosheet.org on new machines.
- **Retrosheet game logs exclude odds and starter stats by default**: Additional join with pitcher data (MLB Stats API) needed for full feature set.
- **Ties excluded from y_true_home_win**: 2024 regular season had no ties; field is `None` for tied games.

## 12. Next-Phase Recommendation
**Next recommended phase**: P33 — 2024 Prediction / Odds Source Gap Builder.
- Confirm license-safe odds provider (The Odds API paid tier or approved alternative).
- Join gl2024 game logs with closing moneyline odds.
- Validate complete training row schema.

---

```
P32_RAW_GAME_LOG_ARTIFACT_READY
```

P32_RAW_GAME_LOG_ARTIFACT_READY