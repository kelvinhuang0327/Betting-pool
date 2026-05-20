# CTO Daily Review - 2026-05-19

**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Branch observed:** `codex/main-sync-20260516`  
**Mode:** `PAPER_ONLY=true`, `NO_REAL_BET=true`, `production_ready=false`  
**Roadmap updated:** `00-BettingPlan/roadmap/betting_roadmap_20260516_p39j_odds_consolidation.md`  
**Final classification:** `ROADMAP_REALIGNED_TO_P8_TRUE_REWARD_WITH_CANONICAL_ARTIFACT_GATE`

---

## 1. CTO Decision

The system should now be managed around two product axes:

1. **MLB prediction -> Taiwan Sports Lottery paper recommendation.**
2. **Strategy simulation / optimization using true outcomes.**

The next stage should not start with PR merge work, generic roadmap work, or new data-source exploration. The highest-leverage execution path is:

1. Recover/canonicalize P0-P7 runtime files and artifacts into the expected repo paths.
2. Run P8 true reward optimizer training from the P7 with-outcomes artifact.
3. Keep `fixed_edge_5pct` as champion unless the optimizer beats it out of sample.

---

## 2. Current System Status

| Area | Observed state | CTO interpretation |
|---|---|---|
| Canonical `data/paper_recommendations/` | Missing from repo root. | P8 cannot use the expected handoff path yet. |
| Existing P0-P7 evidence | Present under `.claude/worktrees/beautiful-carson-bd520d/`. | Recoverable, but must be reconciled before being treated as canonical. |
| P7 rows | 2,430 rows, 2,374 joined, 97.7% coverage, all `paper_only=true`. | True reward records are sufficient after path recovery. |
| Best baseline | `fixed_edge_5pct` true ROI `+1.8384%`, hit rate `50.11%`, true bets `1,319`. | Baseline to beat. |
| EV-proxy gap | `fixed_edge_5pct` EV-proxy ROI `+20.2247%` vs true ROI `+1.8384%`. | EV-proxy is not valid optimizer fitness. |
| Bare Python | `/opt/homebrew/opt/python@3.14/bin/python3.14`, numpy/scipy missing. | Bare interpreter is not the correct runtime. |
| Repo venv | `.venv/bin/python`, numpy/scipy available, pytest 9.0.3. | P8 environment is usable if `.venv` is enforced. |
| Optimizer signature | `optimize_strategy(records, n_generations=50, n_candidates=10, seed=42)`. | Callable in `.venv`. |
| Optimizer architecture | Current settlement path assumes internal prediction and hard-coded -110 payout. | Needs true reward adapter / contract repair before claiming success. |

---

## 3. Roadmap Alignment Assessment

The 2026-05-18 roadmap was correct for PR #2 governance, but now underweights the new runtime evidence from P0-P7. The most important mismatch is:

| Previous roadmap emphasis | Actual current need | Adjustment |
|---|---|---|
| PR #2 merge gate as P0 | User did not authorize merge; product path has moved to P8 planning. | Keep PR #2 as standing YES-gated governance, not product P0. |
| Odds input as main blocker | P7 with true outcomes exists, but canonical path is missing. | P0 becomes artifact canonicalization. |
| Generic strategy optimization v2 | P8 must specifically optimize TRUE_OUTCOME reward. | P1 becomes true reward optimizer integration. |
| TSL taxonomy later | Market breadth matters, but moneyline strategy loop is not closed. | TSL taxonomy moves after P8/P3 champion gate. |

---

## 4. Reordered P0-P10

| Priority | Phase | Goal | Done condition |
|---:|---|---|---|
| **P0** | P0-P7 Artifact Canonicalization Gate | Bring P0-P7 modules, scripts, tests, reports, and paper artifacts into canonical paths without new repo/worktree. | Expected files exist; path audit complete; no production/raw data. |
| **P1** | P8 MARL True Reward Optimizer Training | Run `optimize_strategy()` from `.venv` on P7 with-outcomes records. | Optimized artifact/report exists or exact blocker classification. |
| **P2** | Optimizer Reward Contract Repair | Ensure reward uses actual side, actual odds payout, stake, true outcome, fold metrics. | No EV-proxy fitness; no unlabelled hard-coded -110 settlement. |
| **P3** | Baseline Preservation + Champion Gate | Compare optimizer vs `fixed_edge_5pct`. | Champion decision documented. |
| **P4** | Outcome Join Quality Repair | Resolve 56 doubleheader/duplicate join-key collisions. | Duplicate-safe key and coverage report pass. |
| **P5** | Moneyline Robustness Validation | Add fold/month/team stability and multi-season or holdout evidence. | ROI/Brier/ECE/drawdown confidence bands reported. |
| **P6** | TSL Market Taxonomy + Row Contract | Define moneyline, run line, totals, F5, odd/even, SP+1.5/team-total contracts. | Schema/tests and blocked-state semantics. |
| **P7** | Multi-Market Paper Prototype | Extend paper recommendation beyond moneyline where data exists. | Separate paper-only artifacts and market gates. |
| **P8** | Pregame / Live Odds Replacement | Replace POST_GAME_PROXY with approved pregame/live read-only odds. | Timestamp/no-lookahead/CLV/freshness audits pass. |
| **P9** | Daily Paper Ops + Drift Monitor | Daily advisory and postgame settlement reporting. | Recommended and skipped games are explainable. |
| **P10** | Production Proposal Gate | Only after evidence, live/licensed data, human approval, rollback/no-bet fail-safe. | `production_ready` remains false until explicit approval. |

---

## 5. Key Blockers

1. **Canonical artifact blocker:** P7 artifact exists in an existing worktree path, not expected canonical path.
2. **Optimizer contract blocker:** current MARL optimizer can import in `.venv`, but its episode settlement is not yet proven compatible with P7 true reward rows.
3. **Doubleheader blocker:** P7 has 56 duplicate-key / doubleheader rows that should be fixed before precision ROI claims.
4. **Evidence blocker:** `+1.84%` is a 2025 proxy-closing backtest, not live CLV or real betting evidence.
5. **Market breadth blocker:** product target requires TSL markets beyond moneyline, but those should follow the true reward champion gate.
6. **Governance blocker:** PR #2 remains unmerged unless the user explicitly says `YES: merge PR #2`.

---

## 6. Next Execution Prompt

```text
任務代號：P0_P1_CANONICALIZE_AND_P8_TRUE_REWARD_PREFLIGHT

目標：
在 /Users/kelvin/Kelvin-WorkSpace/Betting-pool 內，不新增 repo/worktree，
先把 P0-P7 artifact/code/test/report 收斂到 canonical path，
再用 .venv 執行 P8 true reward optimizer preflight。

硬性約束：
- 不新增 repo / worktree / Betting-pool* 目錄
- 不 merge PR #2，除非 CEO 明確說 YES: merge PR #2
- 不呼叫 live odds API
- 不修改 TSL crawler / odds ingestion
- 不寫 production proposal channel
- 所有 artifact 維持 paper_only=true
- optimizer fitness 必須來自 TRUE_OUTCOME
- 不得使用 EV-proxy ROI 作為 fitness

必做：
1. 盤點 canonical root 缺少哪些 P0-P7 檔案。
2. 從既有 `.claude/worktrees/beautiful-carson-bd520d/` 只回收 P0-P7 必要 code/test/script/report/artifact。
3. 使用 `.venv/bin/python` 做 numpy/scipy/pytest/optimizer signature preflight。
4. 建立 P8 true reward adapter 或明確回報 architecture blocked。
5. 比較 optimized strategy vs fixed_edge_5pct true ROI +1.8384%。

Final classification:
- P8_MARL_TRUE_REWARD_OPTIMIZER_READY
- P8_MARL_TRUE_REWARD_OPTIMIZER_READY_BASELINE_STILL_BEST
- P8_OPTIMIZER_ENV_BLOCKED
- P8_OPTIMIZER_ARCHITECTURE_BLOCKED
- P8_BLOCKED_BY_TRUE_REWARD_RECORDS
```

`CTO_DAILY_REVIEW_20260519_P8_TRUE_REWARD_ROADMAP_READY`
