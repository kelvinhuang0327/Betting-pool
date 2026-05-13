# P32 Raw Game Log Artifact Report

**Date**: 2026-05-13T03:44:01Z
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

## 4. Source File Availability
- Source path: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt`
- Status: **MISSING**

> **Manual action required**: Download Retrosheet 2024 game logs from https://www.retrosheet.org/gamelogs/index.html and place the file at `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt`. Attribution is required per Retrosheet license.

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
**BLOCKER**: P32_BLOCKED_SOURCE_FILE_MISSING

Reason: Source file not found: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt. Manually download from https://www.retrosheet.org/gamelogs/index.html and place at data/mlb_2024/raw/gl2024.txt.

No processed artifacts written. Re-run after resolving the blocker.

## 7. Provenance / Attribution
```
Source: Retrosheet (season=2024)
  License: ATTRIBUTION_REQUIRED
  Attribution required: True
  URL: https://www.retrosheet.org/gamelogs/index.html
  Source file: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt [MISSING]
  No odds: True
  No predictions: True
  paper_only: True
  production_ready: False
```

**Attribution text** (Retrosheet requirement):
> The information used here was obtained free of charge from and is copyrighted by Retrosheet. Interested parties may contact Retrosheet at www.retrosheet.org.

## 8. Test Results
Run: `./.venv/bin/pytest tests/test_p32_*.py -q`

## 9. Determinism Result
Determinism: BLOCKER DETERMINISTIC — the `P32_BLOCKED_SOURCE_FILE_MISSING` gate is always emitted when the source file is absent. Blocker output is reproducible.

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
- **gl2024.txt requires manual download**: Source file not in repo. Must be obtained from Retrosheet.org with attribution.
- **Retrosheet game logs exclude odds and starter stats by default**: Additional join with pitcher data (MLB Stats API) needed for full feature set.

## 12. Next-Phase Recommendation
**Next recommended phase**: Manually provision Retrosheet gl2024.txt, then rerun P32.
  - Download from: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/data/mlb_2024/raw/gl2024.txt
    https://www.retrosheet.org/gamelogs/index.html
  - Place at: `data/mlb_2024/raw/gl2024.txt`
  - Attribution required (Retrosheet license).
  - Rerun: `./.venv/bin/python scripts/run_p32_build_2024_raw_game_logs.py`

---

```
P32_RAW_GAME_LOG_ARTIFACT_BLOCKED_SOURCE_MISSING
```

P32_RAW_GAME_LOG_ARTIFACT_BLOCKED_SOURCE_MISSING