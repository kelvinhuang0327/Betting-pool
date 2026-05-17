# Single Repo Dirty Inventory — Betting-pool Canonical
**Date:** 2026-05-16  
**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Branch:** `main` (ahead 38, behind 1 vs origin/main)  
**paper_only:** True | **production_ready:** False

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Modified (tracked) | 66 | review before commit |
| Deleted (tracked) | 14 | review — may be intentional |
| Untracked total | 662 | classify below |
| **KEEP** (code/docs/tests) | ~472 | safe to merge from p13-clean |
| **IGNORE** (outputs/runtime/DB/local_only) | ~140 | gitignore or leave untracked |
| **REVIEW** (data/derived, data/mlb_2025) | ~50 | needs content inspection |
| **FORBIDDEN** (.env, raw odds CSV, DB) | identified | never commit |

---

## FORBIDDEN — Never Stage / Never Commit

| File | Reason |
|------|--------|
| `.env` | Contains API keys (TELEGRAM, GITHUB, GROQ, GEMINI, ANTHROPIC, OPENROUTER — 9 keys total). **Never commit.** |
| `data/mlb_2025/mlb_odds_2025_real.csv` | Real odds CSV — forbidden by hard guard |
| `data/mlb_2025/mlb-odds.xlsx` | Raw odds spreadsheet — forbidden |
| `data/wbc_backend/bankroll_v3.db-shm` (deleted) | DB shard file — forbidden |
| `data/wbc_backend/bankroll_v3.db-wal` (deleted) | DB WAL file — forbidden |
| `runtime/agent_orchestrator/llm_audit.jsonl` | LLM call audit log with potential API context |
| `runtime/agent_orchestrator/llm_usage.jsonl` | Usage logs — local-only |
| Any `*.db`, `*.db-wal`, `*.db-shm`, `*.sqlite*` | DB binaries — forbidden |

---

## IGNORE — Outputs / Runtime / Generated Artifacts

These exist locally and are useful but must NOT be committed. Should be in `.gitignore`.

| Directory / Pattern | Contents | Recommendation |
|--------------------|---------|----------------|
| `outputs/` (untracked dir) | PAPER prediction outputs, replay reports | Add to `.gitignore` if not already |
| `runtime/agent_orchestrator/` | Orchestrator state, backlog, cto_reports, closing monitor, insights, frontend | Local runtime — gitignore |
| `runtime/agent_orchestrator/backups/` | Backup snapshots | Local-only |
| `data/wbc_backend/artifacts/` | `continuous_learning_state.json`, `retrainer_state.json` | Generated — gitignore |
| `data/wbc_backend/portfolio_risk.json` | Generated portfolio state | Local runtime |
| `data/derived/model_output_contract_validation_summary_6*` | Per-run validation summaries | Generated artifacts |
| `data/tsl_fetch_status.json` | TSL crawl state | Local runtime |
| `data/tsl_frontend_probe.json` | Frontend probe result | Local runtime |
| `data/tsl_odds_snapshot.json` | Live TSL snapshot | Local-only odds |
| `data/wbc_2026_live_scores.json` | Live game scores | Local runtime |
| `data/wbc_backend/reports/clv_activation_preview_*.json` | Generated CLV previews | Local-only |
| `data/mlb_2025/mlb_odds_2025_real.csv.metadata.json` | Metadata for forbidden odds CSV | Local-only |
| `data/mlb_2025/mlb-2025-asplayed.csv.metadata.json` | Metadata file | Local-only |

---

## REVIEW — Data Files Needing Content Inspection

| File / Directory | Reason for Review |
|-----------------|-------------------|
| `data/mlb_2025/gl2025.txt` / `gl2025.zip` | Retrosheet game logs — may be committable (public data, no license issue) |
| `data/mlb_2025/mlb-2025-asplayed.csv` | Retrosheet derived CSV — check if synthetic or real schedule |
| `data/derived/` (untracked files beyond 6q/6r/6s) | Dry-run artifacts — some may be committable as fixtures |
| `data/wbc_backend/reports/*.json` (untracked market/gate reports) | Generated reports — review if research-grade |
| `data/wbc_backend/reports/market_support_performance_summary.json` | Performance summary — check if derived or live data |

---

## KEEP — Safe Code / Docs / Tests (from p13-clean merge)

These exist in `origin/p13-clean` and are safe to bring into `Betting-pool`:

| Category | Count | Examples |
|----------|-------|---------|
| `wbc_backend/` modules | ~280 | `p38a_retrosheet_feature_adapter.py`, `p38a_oof_prediction_builder.py`, `markets/tsl_market_schema.py` |
| `scripts/` | ~30 | `run_p38a_2024_oof_prediction_rebuild.py`, `run_p39i_walkforward_feature_ablation.py` |
| `tests/` | ~50 | All P38A, P39A-I test files |
| `00-BettingPlan/` docs | ~90 | P13–P39J planning and certification docs |
| `.github/` workflows | 2 | Updated workflow files |
| `.gitignore` | 1 | Updated ignore rules |
| `data/mlb_2024/processed/` | 10 | Retrosheet-derived processed CSVs (public data) |
| `data/research_odds/fixtures/` | 3 | Synthetic fixture CSV + README (SAFE_FIXTURE_EXCEPTION) |

---

## Modified Tracked Files (66) — Spot Check

| File | Status | Notes |
|------|--------|-------|
| `data/mlb_2025/mlb_odds_2025_real.csv` | Modified | **FORBIDDEN** — real odds CSV |
| `data/convert_odds.py` | Modified | Review — odds transform script |
| `data/historical_data.py` | Modified | Review — data loader |
| `data/tsl_crawler.py` / `tsl_crawler_v2.py` | Modified | Review — live scraper |
| `data/live_updater.py` | Modified | Review — live data feed |
| `data/wbc_backend/reports/2026-03-14_*` (8 files) | Modified | WBC reports — review |
| `data/learning_state.json` | Modified | Runtime learning state |

---

## Deleted Tracked Files (14)

These were removed from the working tree but not `git rm`'d:
- `data/wbc_backend/bankroll_v3.db-shm` — DB shard (FORBIDDEN anyway)
- `data/wbc_backend/bankroll_v3.db-wal` — DB WAL (FORBIDDEN anyway)
- `data/wbc_backend/reports/2026_WBC_TPE_*` (5 files) — WBC reports deleted
- Others: review individually before staging deletions

---

## Conclusion

The canonical `Betting-pool` repo has a **large dirty working tree** (742 lines in git status). The dirty state is mostly:
1. Runtime/generated artifacts from the orchestrator system (safe to ignore)
2. A small number of FORBIDDEN files (`.env`, real odds CSV, DB files)
3. ~472 safe code/test/script files reachable from `origin/p13-clean` merge

**Consolidation is conditionally safe** if:
- Forbidden files are never staged
- Only code/docs/tests/fixtures are merged from p13-clean
- outputs/runtime/local_only remain untracked and gitignored

**Consolidation is NOT safe for a blind `git merge`** — must use selective cherry-pick or per-file copy.
