# P40D Main Sync Forbidden Audit
**Date:** 2026-05-16  
**Branch:** `main` (local)  
**Comparing:** `origin/main..main`  
**paper_only:** True | **production_ready:** False

---

## Ahead / Behind Summary

| Direction | Count | SHA |
|-----------|-------|-----|
| Local main ahead of origin/main | **38 commits** | newest: `10a08a1` |
| Local main **behind** origin/main | **1 commit** | `e765b3b` |
| Merge base | `034f772` | last shared ancestor |
| Topology | **DIVERGED** — not a simple ahead relationship |

> ⚠️ `git push origin main` would be **REJECTED** (non-fast-forward).  
> A `--force` push is forbidden by hard rules. See Track 2 for resolution options.

---

## Changed Files in 38 Local Commits

| Category | Count |
|----------|-------|
| Total files changed | 258 |
| `orchestrator/` | ~15 |
| `wbc_backend/` | ~60 |
| `tests/` | ~30 |
| `data/` (committed artifacts) | ~10 |
| `docs/` | ~20 |
| `outputs/replay/` | 7 |
| `scripts/` | ~8 |
| Other (`main.py`, `models/`, etc.) | ~108 |

---

## Forbidden-File Scan Results

### Strict Pattern (hard guards)

```
\.env$ | \.db$ | \.sqlite$ | \.db-wal$ | \.db-shm$ |
data/research_odds/local_only/ | data/pybaseball/local_only/ |
data/mlb_2025/mlb_odds_2025_real\.csv
```

**Result: NO_STRICT_FORBIDDEN** ✅

| File pattern | Status |
|-------------|--------|
| `.env` | ✅ NOT IN COMMITTED DIFF |
| `*.db`, `*.db-wal`, `*.db-shm` | ✅ NOT IN COMMITTED DIFF (deleted from working tree, never re-committed) |
| `data/mlb_2025/mlb_odds_2025_real.csv` | ✅ NOT IN COMMITTED DIFF (modified in working tree only — dirty but not staged/committed) |
| `data/research_odds/local_only/` | ✅ NOT IN DIFF |
| `data/pybaseball/local_only/` | ✅ NOT IN DIFF |

### Broad Pattern (flags for review)

| File | Pattern Matched | Classification |
|------|----------------|----------------|
| `tests/test_production_integration.py` | `production` in name | **SAFE** — integration test using unittest mocks, not real production write |
| `data/wbc_backend/calibration_compare.json` | `data/` | **REVIEW** — model calibration comparison artifact (research output) |
| `data/wbc_backend/walkforward_summary.json` | `data/` | **REVIEW** — walk-forward model summary (research output) |
| `data/wbc_backend/model_artifacts.json` | `data/` | **REVIEW** — model artifact metadata |
| `outputs/replay/` (7 files) | `outputs/` | **REVIEW** — replay CI validation reports (non-secret) |

### Verdict

| Level | Result |
|-------|--------|
| Hard-forbidden files (real secrets/raw data) | **0 found** ✅ |
| Suspicious (needs review before push to origin) | 4 data JSON files + 7 outputs files |
| `test_production_integration.py` | SAFE — mock-based integration test |

---

## Key Data Files Classification

| File | Content | Push-safe? |
|------|---------|-----------|
| `data/wbc_backend/calibration_compare.json` | Platt calibration results, 2188 games, model metrics | ✅ Research artifact — safe |
| `data/wbc_backend/walkforward_summary.json` | Walk-forward summary stats, 1626 ml_bets field | ✅ Research artifact — safe |
| `data/wbc_backend/model_artifacts.json` | Model artifact paths/metadata | ✅ Safe |
| `outputs/replay/*.md/.json/.html` | Replay validation CI reports | ✅ Safe — documentation |

None contain: real odds, real bets, API secrets, personal data.

---

## Push Readiness (Forbidden Only)

| Criterion | Status |
|-----------|--------|
| No `.env` / API keys | ✅ PASS |
| No raw odds CSV | ✅ PASS |
| No DB binaries | ✅ PASS |
| No local_only raw data | ✅ PASS |
| Broad-scan data files | ⚠️ REVIEW (safe research artifacts, not blocking) |
| **Forbidden files block push?** | **NO** |

**Push is NOT blocked by forbidden files.** It is blocked by the **diverged history** (see Track 2).

---

## Acceptance Marker

`P40D_MAIN_SYNC_FORBIDDEN_AUDIT_CLEAN_20260516`
