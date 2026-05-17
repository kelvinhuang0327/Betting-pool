# P40D Draft PR Readiness Report
**Date:** 2026-05-16  
**Branch pushed:** NO — awaiting `YES: push codex/consolidate-p13-clean-20260516 to origin`  
**paper_only:** True | **production_ready:** False

---

## Branch Summary

| Item | Value |
|------|-------|
| Source branch | `codex/consolidate-p13-clean-20260516` |
| Local HEAD | `592acaa` (P40B) + 4 staged scripts from P40C |
| Intended PR target | `main` (pending CTO confirmation) |
| `main` SHA | `10a08a1` (UNTOUCHED) |
| `origin/main` SHA | `e765b3b` |
| Branch pushed to remote | ❌ NOT YET |

---

## Test Result

| Metric | Value |
|--------|-------|
| Tests | 153 passed, 2 skipped, 0 failed |
| Test suite | 11 files (P38A + P39A-I full suite) |
| Environment | Betting-pool `.venv` |
| Verdict | ✅ READY |

2 skipped tests require `data/mlb_2024/processed/` — not present in Betting-pool, gracefully skipped.

---

## Forbidden-File Audit

| Check | Result |
|-------|--------|
| `.env`, API keys | ✅ NOT IN DIFF |
| `*.db`, `*.db-wal`, `*.db-shm` | ✅ NOT IN DIFF |
| `data/research_odds/local_only/` | ✅ NOT IN DIFF |
| `data/pybaseball/local_only/` | ✅ NOT IN DIFF |
| Raw odds CSV | ✅ NOT IN DIFF |
| Raw Statcast / pybaseball data | ✅ NOT IN DIFF |
| Synthetic fixtures | ✅ 2 CSVs — `SAFE_FIXTURE_EXCEPTION` (dummy data, `synthetic_no_license`, 5 rows each) |
| False-positive flag | `research_odds_local_only_decision_20260513.md` — pure 58-line markdown policy doc, NOT raw data |

**Verdict: NO_REAL_FORBIDDEN_DATA_FILES** ✅

---

## Copied Files Summary (P40B + P40C combined)

| Category | Count |
|----------|-------|
| Planning docs (`00-BettingPlan/2026051[1-3]/`) | ~115 |
| Core Python modules (`wbc_backend/markets/`, `recommendation/p38a_*.py`) | 7 |
| Test files | 11 |
| Dependency scripts (`scripts/build_pybaseball_*.py`, etc.) | 7 |
| Synthetic fixtures + README | 3 |
| PAPER metrics JSON | 2 |
| P40A/B/C/D docs | ~9 |
| **Total** | **~154 files** |

---

## Remaining Excluded Files (Not Yet Reviewed)

| Category | Approx. Count | Reason Not Copied |
|----------|--------------|-------------------|
| `wbc_backend/recommendation/p13_*.py` through `p37_*.py` | ~75 files | Requires separate review against Betting-pool's existing dirty recommendation pipeline |
| `wbc_backend/simulation/p18_*.py`, `p13_strategy_simulator.py` | ~5 | Potential conflict with Betting-pool's existing simulation modules |
| `data/mlb_2024/processed/` | ~15 files | Retrosheet-derived public data — safe but requires explicit decision to add to canonical repo |
| `outputs/predictions/PAPER/p38a_2024_oof/` | 3 files | Large generated OOF prediction CSV — review size before committing |
| `.github/` workflow updates | 2 | Require separate CI review |

These can be addressed in P40E / follow-on sessions.

---

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|-----------|
| `Betting-pool/main` is **38 commits ahead** of `origin/main` | Medium | PR should target local `main`, not `origin/main`; ensure orchestrator Phases 1–24 are pushed first |
| `~360` p13-clean files not yet merged | Low | These are additive; no conflict expected if merged separately |
| 9 active Codex worktrees at `~/.codex/worktrees/` | Low | Not touched; remain at `034f772` |
| 2 skipped tests (missing `mlb_2024/processed/`) | Low | Graceful skip; add data files in follow-on or accept skip |

---

## Open Questions for CTO

1. **Push this branch now?** → Send `YES: push codex/consolidate-p13-clean-20260516 to origin`
2. **PR target**: Should the PR target local `main` (which has unpushed orchestrator work) or wait until `Betting-pool/main` is pushed to `origin/main` first?
3. **Review p13–p37 pipeline**: Should the ~75 recommendation pipeline files be merged in a separate P40E task?
4. **Add `data/mlb_2024/processed/`**: Should processed Retrosheet CSVs be copied to Betting-pool?
5. **P3 odds unblock**: Still blocked — `THE_ODDS_API_KEY` missing, no local CSV.

---

## Next Signal Options

| Signal | Effect |
|--------|--------|
| `YES: push codex/consolidate-p13-clean-20260516 to origin` | Push branch, enable remote PR |
| `CTO_DECISION: merge p13-p37 pipeline` | Copy remaining ~75 recommendation files |
| `KEY_READY: The Odds API key is in .env as THE_ODDS_API_KEY` | Resume P3 odds fetch |
| `DATA_READY: I dropped a CSV to data/research_odds/local_only/` | Validate & join odds CSV |
| `CTO_DECISION: run pitcher feature pilot` | Start P39K |

---

## Acceptance Marker

`P40D_PR_READINESS_REPORT_READY_20260516`

`P40D_PUSH_NOT_AUTHORIZED_20260516`
