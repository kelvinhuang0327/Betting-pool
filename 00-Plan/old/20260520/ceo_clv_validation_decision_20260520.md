# CEO CLV Validation Decision - 2026-05-20

**Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Branch observed:** `codex/main-sync-20260516`  
**Mode:** `PAPER_ONLY=true`, `NO_REAL_BET=true`, `production_ready=false`  
**Roadmap updated:** `00-BettingPlan/roadmap/betting_roadmap_20260516_p39j_odds_consolidation.md`  
**Final classification:** `CEO_APPROVE_CLV_VALIDATION_ONLY_P22_READY`

---

## 1. CEO Decision

The CEO decision is:

```text
APPROVE_CLV_VALIDATION_ONLY
```

This approval means P22 may start, but only for CLV validation. It does not allow optimizer promotion, champion replacement, production proposal, live odds API calls, TSL crawler modification, or profitability claims.

Date correction: the current operating date is `2026-05-20` Asia/Taipei. Existing P20/P21 artifacts are labeled `20260521` and `20260522`; those are accepted as existing handoff labels, but new P22 files should use `20260520` unless the operator explicitly advances the run date.

---

## 2. Current System Truth

| Item | Status | CEO call |
|---|---|---|
| P19 valid CLV pairs | `233` | Threshold satisfied for validation-only. |
| P19 CLV gate | `BLOCKED_BY_CEO_HOLD` | CEO hold lifted only for CLV validation. |
| P20 classification | `P20_CEO_CLV_DECISION_REQUIRED` | Superseded by this decision. |
| P21 classification | `P21_CEO_CLV_DECISION_REQUIRED` | Superseded by this decision. |
| P17 standalone | `64/64 PASS` in P21 report | Rerun as P22 preflight. |
| P12-P17 regression | `347/347 PASS` in P21 report | Rerun as P22 preflight. |
| Champion | `fixed_edge_5pct` preserved | Keep preserved. |
| Promotion | Frozen | Keep frozen. |
| Production | Not ready | Remains blocked. |

---

## 3. Roadmap Gap

The prior roadmap correctly held P22 while CEO decision was missing. That is now stale. Continuing another decision-follow-up cycle would be process churn because the data gate is already satisfied at `valid_clv_pairs=233`.

The next meaningful work is P22 validation-only:

1. Materialize the CEO decision artifact.
2. Review pair sample integrity.
3. Encode the CLV validation-only contract.
4. Calculate CLV distribution and market summary.
5. Refresh the P23 gate without promotion.

---

## 4. Reordered P0-P10

| Priority | Phase | Objective | Done condition |
|---:|---|---|---|
| **P0** | P22 CEO Decision Materialization | Create current-date paper-only decision artifact. | `APPROVE_CLV_VALIDATION_ONLY`; forbidden actions remain blocked. |
| **P1** | P22 Pair Sample Integrity Review | Validate 233 pairs before metrics. | Top 20, random 10, invalid/edge samples with source trace. |
| **P2** | P22 CLV Validation-Only Contract | Lock allowed/forbidden scope. | CLV allowed; promotion/prod/live/crawler/profitability forbidden. |
| **P3** | P22 CLV Distribution + Market Summary | Compute CLV evidence. | Paper-only CLV JSON/MD reports. |
| **P4** | P22 Hold / Ready Gate Refresh | Decide P23 validation continuation. | `p23_allowed=true` only for validation continuation. |
| **P5** | P22 Final Validation | Rerun tests and safety scans. | Regression and grep scans pass or exact blocker. |
| **P6** | P23 CLV Interpretation Gate | Classify evidence as favorable/neutral/adverse. | No strategy promotion. |
| **P7** | P24 Strategy Policy Review Gate | Review `fixed_edge_5pct` after CLV interpretation. | Baseline preserved unless separate CEO approval. |
| **P8** | Optimizer Re-entry Gate | Revisit MARL only after CLV interpretation. | EV-proxy still banned; promotion separately approved. |
| **P9** | TSL Market Taxonomy Re-entry Gate | Resume market schema after moneyline CLV evidence. | Paper-only taxonomy, no market expansion recommendation. |
| **P10** | Production Proposal Gate | Remains blocked. | `production_ready=false`. |

---

## 5. Recommended Next Task Prompt

```text
[CEO 指令 - P22 CLV VALIDATION ONLY APPROVED]

任務代號：P22_CLV_VALIDATION_ONLY_APPROVED
主軸：MLB 運彩預測 + CLV validation-only
承接狀態：P21_CEO_CLV_DECISION_REQUIRED 已由 CEO 於 2026-05-20 supersede

CEO 決策：
APPROVE_CLV_VALIDATION_ONLY

重要日期規則：
- 目前系統日期是 2026-05-20 Asia/Taipei。
- P20/P21 既有 artifact 雖標示 20260521/20260522，視為既有 handoff label。
- 本輪 P22 新產物請使用 20260520 suffix，不要使用 20260523，除非 operator 明確改 run date。

背景：
1. P19 canonical regenerated valid_clv_pairs = 233。
2. P20/P21 連續兩輪只剩 CEO decision blocker。
3. CEO 現已批准 CLV_VALIDATION_ONLY。
4. fixed_edge_5pct champion PRESERVED。
5. promotion FROZEN。
6. P22 僅允許 CLV validation，不允許 promotion / champion replacement / production proposal。

最高原則：
- 不新增 repo / worktree / Betting-pool* 目錄
- 不 merge PR #2
- 不呼叫 live odds API
- 不修改 TSL crawler / odds ingestion
- 不寫 production proposal
- 不宣稱可獲利
- 不做 optimizer promotion
- 不做 champion replacement
- 所有 artifact 維持 paper_only=true

P22-A — Preflight:
1. 確認 canonical root：
   /Users/kelvin/Kelvin-WorkSpace/Betting-pool
2. 確認 P19/P20/P21 artifacts 存在。
3. 跑：
   - .venv/bin/python -m pytest tests/test_p17_hold_state_continuity.py
   - .venv/bin/python -m pytest tests/test_blocked_state_governance.py tests/test_blocked_state_daily_monitor_p12.py tests/test_p13_minimal_monitor.py tests/test_p14_no_expansion_guard.py tests/test_p15_no_expansion_watch.py tests/test_p16_no_expansion_hold.py tests/test_p17_hold_state_continuity.py
4. 若測試失敗，停止，Final Classification = P22_BLOCKED_BY_TEST_REGRESSION。

P22-B — CEO Decision Materialization:
1. 建立：
   data/paper_recommendations/p22_ceo_clv_validation_decision_20260520.json
2. 內容必須包含：
   - decision = APPROVE_CLV_VALIDATION_ONLY
   - clv_validation_allowed = true
   - optimizer_promotion_allowed = false
   - champion_replacement_allowed = false
   - production_proposal_allowed = false
   - paper_only = true
   - network_call = false
   - crawler_modified = false

P22-C — Pair Sample Integrity Review:
1. 讀取：
   - data/paper_recommendations/p19_closing_line_availability_recheck_20260520.json
   - data/paper_recommendations/p19_canonical_forward_coverage_regenerated_20260520.json
   - data/tsl_odds_history.jsonl
2. 產出 sample：
   - top 20 valid pairs
   - fixed-seed random 10 valid pairs
   - invalid / edge sample 最多 20 筆
3. 每筆 sample 必須包含：
   - match_id
   - game_time
   - pregame_fetched_at
   - closing_fetched_at
   - timestamp_gap
   - odds fields
   - validation_result
   - source_trace
4. 產出：
   - data/paper_recommendations/p22_clv_pair_sample_review_20260520.json
   - report/p22_clv_pair_sample_review_20260520.md

P22-D — CLV Validation-Only Contract:
1. Allowed:
   - calculate CLV
   - compare selected paper picks vs closing odds
   - produce CLV distribution
   - produce market-level summary
   - produce paper-only CLV validation report
2. Forbidden:
   - optimizer promotion
   - champion replacement
   - production proposal
   - live odds API
   - TSL crawler modification
   - profitability claim
3. 產出：
   - data/paper_recommendations/p22_clv_validation_only_contract_20260520.json
   - report/p22_clv_validation_only_contract_20260520.md

P22-E — CLV Distribution + Market Summary:
1. 使用 233 valid pairs 計算：
   - mean_clv
   - median_clv
   - positive_clv_rate
   - bucket distribution
   - market-level summary
   - sample caveats
2. 僅輸出 validation evidence，不輸出策略升級建議。
3. 產出：
   - data/paper_recommendations/p22_clv_validation_summary_20260520.json
   - report/p22_clv_validation_summary_20260520.md

P22-F — Hold / Ready Gate Refresh:
1. 若 sample review PASS 且 CLV summary 產出：
   - p23_allowed = true
   - p23_scope = CLV_INTERPRETATION_ONLY
   - promotion_frozen = true
   - champion_preserved = true
2. 否則：
   - p23_allowed = false
   - blocker 明確列出
3. 產出：
   - data/paper_recommendations/p22_hold_ready_gate_refresh_20260520.json
   - report/p22_hold_ready_gate_refresh_20260520.md

P22-G — Final Validation:
1. rerun P17 standalone
2. rerun P12-P17 regression
3. artifact schema check
4. grep scan:
   - no live odds API
   - no TSL crawler modification
   - no production proposal
   - no optimizer promotion
   - no champion replacement
   - no profitable / 可獲利 claim
   - paper_only=true
5. 產出：
   - report/p22_final_validation_20260520.md
   - 00-BettingPlan/20260520/p22_clv_validation_only_approved_20260520.md

Final Classification:
- P22_CLV_VALIDATION_ONLY_READY
- P22_BLOCKED_BY_PAIR_SAMPLE_REVIEW_FAILED
- P22_BLOCKED_BY_TEST_REGRESSION
- P22_BLOCKED_BY_SCOPE_VIOLATION
- P22_BLOCKED_BY_MISSING_CLV_EVIDENCE
```

`CEO_CLV_VALIDATION_DECISION_20260520_P22_READY`
