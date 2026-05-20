# CEO Roadmap Realignment - 2026-05-19

**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Branch observed:** `codex/main-sync-20260516`  
**Mode:** `PAPER_ONLY=true`, `NO_REAL_BET=true`, `production_ready=false`  
**Roadmap updated:** `00-BettingPlan/roadmap/betting_roadmap_20260516_p39j_odds_consolidation.md`  
**Final classification:** `CEO_HOLD_P18_BLOCKED_PRIORITIZE_CLV_FORWARD_UNBLOCK`

---

## 1. CEO Decision

The CEO decision is:

> Continue HOLD. Do not start P18. Preserve `fixed_edge_5pct`; keep promotion frozen; focus the next cycle on P17 canonicalization, forward coverage, and closing-line CLV evidence.

The P17 handoff is internally consistent: 64 P17 tests passed, 347 P12-P17 regression tests passed, 7 safety scans were clean, and all artifacts stayed `paper_only=true`. But those files are currently in `.claude/worktrees/awesome-mclean-f52768/`, not canonical root.

Date note: the P17 artifacts are labeled `20260602`, while the current operating date is `2026-05-19`. Treat `2026-06-02` as a handoff artifact label until the operator confirms otherwise.

---

## 2. Current System Truth

| Item | Status | CEO call |
|---|---|---|
| P17 classification | `P17_HOLD_ENGINEERING_EXPANSION_NO_DECISION` | Accept hold state. |
| P18 allowed | `false` | P18 must not start. |
| CEO decision in handoff | `DEFER_DECISION` | Update to CEO HOLD / no expansion. |
| Forward pairs | `0 / 200` | Hard blocker. |
| CLV status | `BLOCKED_NO_CLOSING_LINE` | Hard blocker. |
| Champion | `fixed_edge_5pct`, preserved | Baseline only, not promotion. |
| Promotion | `FROZEN` | Keep frozen. |
| Safety scan | CLEAN | Preserve in canonicalization. |
| Canonical root | P17 files absent | P0 must canonicalize or explicitly block. |

---

## 3. Roadmap Gap

The previous roadmap still pointed toward true reward optimizer work. That was a reasonable P8 direction before P17, but P17 shows a stricter blocker: no forward coverage and no closing-line CLV. That makes optimizer promotion and market expansion premature.

The next highest-value optimization is the evidence gate: figure out how to get from `0/200` forward pairs and `BLOCKED_NO_CLOSING_LINE` to an approved, read-only CLV validation path.

---

## 4. Reordered P0-P10

| Priority | Phase | Objective | Done condition |
|---:|---|---|---|
| **P0** | P17 Canonicalization Gate | Review and bring P17 code/test/artifacts/reports from existing worktree into canonical root. | P17 and P12-P17 rerun pass in canonical root. |
| **P1** | CEO Hold Decision Artifact | Record CEO HOLD / no P18 / no promotion. | `p18_allowed=false`; forbidden actions still blocked. |
| **P2** | Forward Coverage Read-Only Inventory | Explain why forward pairs are `0/200`. | Read-only artifact lists source paths, missing fields, and unlock requirement. |
| **P3** | Closing-Line Availability Gate | Determine if approved closing-line data exists. | `CLV_READY` or exact blocked reason. |
| **P4** | P18 Unlock Gate Contract | Encode CEO approval + 200 forward pairs + CLV readiness. | Tests prove P18 stays blocked until all gates clear. |
| **P5** | Champion Preservation Audit | Keep `fixed_edge_5pct` as frozen baseline only. | No optimizer promotion, no profitability claim. |
| **P6** | Forward Paper Monitoring Loop | Daily read-only monitor for CEO decision, forward pairs, CLV. | Stable paper-only artifact. |
| **P7** | Data Unblock Decision Packet | Present API key / local CSV / continue HOLD options. | CEO-ready packet with provenance and risk. |
| **P8** | True Reward Optimizer Re-entry Gate | Resume optimizer only after gates clear. | EV-proxy remains banned; promotion remains blocked. |
| **P9** | TSL Market Taxonomy Re-entry Gate | Resume market expansion only after evidence blocker is no longer dominant. | Paper-only schema path, no recommendation expansion. |
| **P10** | Production Proposal Gate | Remains blocked. | `production_ready=false`; no production proposal write. |

---

## 5. Recommended Next Task Prompt

```text
[CEO 指令 - P18_BLOCKED / P17 CANONICALIZATION + CLV UNBLOCK]

任務代號：P18_BLOCKED_P17_CANONICALIZE_AND_CLV_FORWARD_GATE

目標：
在 /Users/kelvin/Kelvin-WorkSpace/Betting-pool 內，不新增 repo/worktree，
將既有 .claude/worktrees/awesome-mclean-f52768 的 P17 成果做 canonicalization preflight，
並建立下一步 CLV / forward coverage 解鎖報告。

最高原則：
- 嚴禁新增 repo / worktree / Betting-pool* 目錄
- 不 merge PR #2，除非 CEO 明確說 YES: merge PR #2
- 不啟動 P18，因 p18_allowed=false
- 不呼叫 live odds API
- 不修改 TSL crawler / odds ingestion
- 不寫 production proposal channel
- 不宣稱可獲利
- 不做 optimizer promotion
- 所有 artifact 維持 paper_only=true

必做：
1. 比對 canonical root 與 .claude/worktrees/awesome-mclean-f52768 的 P17 差異：
   - wbc_backend/recommendation/blocked_state_governance.py
   - tests/test_p17_hold_state_continuity.py
   - data/paper_recommendations/p17_*.json
   - report/p17_*.md
2. 若差異安全，將 P17 必要檔案收斂到 canonical root；若不安全，輸出 P17_CANONICALIZATION_BLOCKED_DIFF_RISK。
3. 用 .venv/bin/python rerun：
   - tests/test_p17_hold_state_continuity.py
   - P12-P17 regression suite
4. 新增或更新 CEO hold artifact：
   - p18_allowed=false
   - ceo_decision=HOLD_NO_EXPANSION
   - champion=fixed_edge_5pct PRESERVED
   - promotion=FROZEN
5. 做 forward coverage read-only inventory：
   - 找出 forward_pairs 為何是 0/200
   - 不呼叫 API、不改 crawler
   - 列出缺少的欄位、source path、最小解鎖條件
6. 做 closing-line availability gate：
   - 若無 approved closing line，輸出 CLV_BLOCKED_NO_CLOSING_LINE
   - 若有資料但未核准，輸出 CLV_BLOCKED_SOURCE_UNAPPROVED
   - 若可用，僅產出 readiness，不做 promotion
7. 新增報告：
   - 00-BettingPlan/20260519/p18_blocked_p17_canonicalization_and_clv_gate_20260519.md

驗收標準：
- 不新增 repo/worktree
- P17 canonical files present or explicit blocker
- P17 alone tests pass in canonical root
- P12-P17 regression pass or exact dependency blocker
- p18_allowed remains false
- forward pair count and CLV blocked reason documented
- no production proposal, no live odds write, no crawler modification

Final classification:
- P17_CANONICALIZED_P18_STILL_BLOCKED_CLV_FORWARD_GATE_READY
- P17_CANONICALIZATION_BLOCKED_DIFF_RISK
- P17_CANONICALIZATION_BLOCKED_TESTS
- CLV_BLOCKED_NO_CLOSING_LINE
- CLV_BLOCKED_SOURCE_UNAPPROVED
```

`CEO_ROADMAP_REALIGNMENT_20260519_P18_BLOCKED_CLV_FORWARD_READY`
