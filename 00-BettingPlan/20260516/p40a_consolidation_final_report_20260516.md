# P40A Single-Repo Consolidation + P3 Odds Input Gate — Final Report
**Date:** 2026-05-16  
**Canonical repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Source repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13` (temporary, read-only)  
**paper_only:** True | **production_ready:** False

---

## 1. Repo Consolidation Readiness

### Source (Betting-pool-p13)
| Item | Value |
|------|-------|
| Branch | `p13-clean` |
| Remote | `origin/p13-clean` = `1b50704` (pushed ✅) |
| Commits ahead of origin/main | 90 |
| Total files changed vs main | ~500+ |
| Safe to merge (code/tests/docs) | ~472 files |
| Forbidden in diff | 0 raw secrets; 2 synthetic fixture CSVs (SAFE_FIXTURE_EXCEPTION) |

### Canonical Target (Betting-pool)
| Item | Value |
|------|-------|
| Branch (current) | `codex/consolidate-p13-clean-20260516` ✅ created |
| Dirty state | 742 lines (66 modified, 14 deleted, 662 untracked) |
| Forbidden untracked | `.env` (9 keys), `mlb_odds_2025_real.csv`, `mlb-odds.xlsx`, `*.db-wal` |
| Safe to blind-merge? | **NO** — selective copy only |
| Consolidation strategy | Per-category file copy via `git checkout p13-source/p13-clean -- <files>` |

### Consolidation Branch
- **Branch created:** `codex/consolidate-p13-clean-20260516` off `main` (`10a08a1`)
- **Nothing staged or committed yet** — dry-run only this round
- **Status:** `SINGLE_REPO_CONSOLIDATION_DRY_RUN_READY`
  - Dirty worktree confirmed reviewed; forbidden files identified and will not be staged
  - Safe to proceed with selective file copy in next round

---

## 2. P3 Odds Input Readiness

### Gate Result: `ODDS_INPUT_NOT_READY`

| Check | Result |
|-------|--------|
| `THE_ODDS_API_KEY` in `.env` | ❌ NOT FOUND (9 keys present: TELEGRAM, GITHUB, GROQ, GEMINI, ANTHROPIC, OPENROUTER, etc.) |
| `data/research_odds/local_only/` has CSV | ❌ EMPTY / DIR MISSING |
| `data/research_odds/fixtures/` | ✅ 2 synthetic fixtures + README (SAFE_FIXTURE_EXCEPTION — not real odds) |
| `.env` has THE_ODDS_API_KEY | ❌ |
| Operator signal received | ❌ No KEY_READY / DATA_READY |

**No odds fetch, no transform, no join executed.**

### Unblock Paths (unchanged from P39J assessment)
1. Add `THE_ODDS_API_KEY=<key>` to `.env` → send `KEY_READY`
2. Drop a 2024 MLB moneyline CSV to `data/research_odds/local_only/` → send `DATA_READY`

---

## 3. P38A / P39J Current Truth

| Item | Status |
|------|--------|
| P38A OOF baseline | Brier ≈ 0.2487, 2187/2429 rows, `p38a_walk_forward_logistic_v1` |
| P39 Statcast batting track | **FROZEN** — P39I_NO_ROBUST_IMPROVEMENT (4-fold walk-forward confirmed) |
| P38A as operative model | ✅ Yes |
| TSL market schema | ✅ Defined — `MONEYLINE_HOME_AWAY` paper-implemented |
| CLV / EV calculation | ❌ Blocked — requires real pregame odds |
| Pitcher feature pilot (P39K) | ⏸️ DEFERRED — no CTO_DECISION signal |

---

## 4. Next Execution Decision

### Recommended sequence (by ROI):

| Priority | Action | Signal Required | Effort |
|----------|--------|-----------------|--------|
| 1 | **P3 odds unblock** | `KEY_READY` or `DATA_READY` | 30 min |
| 2 | **Execute consolidation** | Implicit (run next round with this branch) | 1 session |
| 3 | **P39K pitcher feature pilot** | `CTO_DECISION: run pitcher feature pilot` | 2 sessions |

### Consolidation next steps (when operator is ready):
```bash
# Already on: codex/consolidate-p13-clean-20260516
# Add p13 as remote and fetch
git remote add p13-source https://github.com/kelvinhuang0327/Betting-pool.git
git fetch p13-source p13-clean

# Selective copy: P38A core
git checkout p13-source/p13-clean -- \
  wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py \
  wbc_backend/recommendation/p38a_oof_prediction_builder.py \
  wbc_backend/markets/__init__.py \
  wbc_backend/markets/tsl_market_schema.py \
  scripts/run_p38a_2024_oof_prediction_rebuild.py \
  tests/test_p38a_retrosheet_feature_adapter.py \
  tests/test_p38a_oof_prediction_builder.py \
  tests/test_tsl_market_schema.py

# Forbidden-file check before any commit
git diff --cached --name-only | grep -E "\.env|\.db|local_only|odds_real|raw"

# Commit only if clean
git commit -m "chore(consolidation): bring P38A + market schema from p13-clean"
```

---

## 5. Forbidden-File Scan Results

| Scope | Result |
|-------|--------|
| `git diff origin/main..origin/p13-clean` contains `.env` | ❌ NOT FOUND |
| Contains `*.db` / `*.db-wal` | ❌ NOT FOUND |
| Contains `local_only/` CSV | ❌ NOT FOUND (gitignored, never committed) |
| Contains `mlb_odds_2025_real.csv` or similar | ❌ NOT FOUND |
| Contains synthetic fixture CSVs | ✅ 2 files — `SAFE_FIXTURE_EXCEPTION` declared |
| Canonical repo `.env` committed | ❌ Never (untracked, `.gitignore` must cover it) |
| Staged files on consolidation branch | ✅ ZERO (nothing staged) |

---

## Worktree Note

The canonical Betting-pool repo has **9 active Codex worktrees** at `/Users/kelvin/.codex/worktrees/*/Betting-pool` (all detached HEAD at `034f772`). These are managed by Codex and are not touched by this agent. The consolidation branch `codex/consolidate-p13-clean-20260516` was created in the main working tree only.

---

## Final Classification

```
SINGLE_REPO_CONSOLIDATION_DRY_RUN_READY
ODDS_INPUT_NOT_READY
```
