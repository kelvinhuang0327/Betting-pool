已確認指定 repo/branch 正確：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`、`p13-clean`，P13/P14/P15 markers 都存在。現有 roadmap 確實落後在 P12 視角，我已直接更新。

更新檔案：

- [正式 roadmap](/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/docs/orchestration/mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md:1)
- [2026-05-12 CTO realignment report](/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/00-BettingPlan/20260512/cto_roadmap_realignment_20260512.md:1)

核心調整：下一階段 P0 不再是模型修復，也不是 live TSL 修復，而是 **P16 Recommendation Gate Re-evaluation**。原因是 P13 已有正 OOF BSS、P15 已有 historical odds-aware simulation；目前最大缺口是推薦層還沒有直接消費 P15 的 `p_model / p_market / edge / odds` artifact。

新版 P0-P10：

| Priority | Phase | Focus |
|---|---|---|
| P0 | P16 | P15 odds-aware artifact -> PAPER recommendation rows |
| P1 | P17 | Paper recommendation ledger / settlement join |
| P2 | P18 | Strategy optimization hardening：avg edge、Kelly、drawdown、threshold sweeps |
| P3 | P19 | Odds data quality / invalid odds / identity audit |
| P4 | P20 | Daily PAPER MLB recommendation orchestrator |
| P5 | P21 | Live TSL / approved odds source repair |
| P6 | P22 | Model improvement and calibration |
| P7 | P23 | TSL market expansion：讓分、大小、F5、單雙、隊伍總分 |
| P8 | P24 | CI / regression / worktree hygiene |
| P9 | P25 | Daily ops monitoring |
| P10 | P26 | Production proposal gate |

關鍵 blocker 也已明確寫入：P16 adapter/gate/row builder 尚未存在、live TSL 仍是 production blocker、2 筆 invalid odds 待 audit、P15 strategy summary 還缺 avg edge / avg Kelly / drawdown 等風險指標。

沒有跑測試，因為這輪只更新 roadmap/report 文件。現有 worktree 仍有先前就存在的 dirty `data/`、`outputs/`、`runtime/` 變更；我沒有碰它們。

最值得聚焦的系統優化方向：**先做 P16，把 P13 + P15 的 evidence 變成可稽核 PAPER recommendation rows；如果 P16 ready，再進 P17 settlement ledger。**

`production_ready=false` 仍維持。  
`CTO_MLB_P15_P16_ROADMAP_REALIGNMENT_20260512_READY`

# CEO 二次審查報告 — 2026-05-12

## 1. 昨天 (P15) 是否真的推進系統成熟度？

**結論：部分推進，但有被高估的風險。**

| 項目 | CTO 宣稱 | CEO 審查 |
|---|---|---|
| odds join coverage 99.87% | ✅ 成功 | ⚠️ 但用 **deterministic 位置映射**，非 game_id 對齊；上游資料順序一變就靜默崩 |
| capped_kelly ROI +5.51% | ✅ 啟動 | ⚠️ **單一 Kelly 設定 / 單一 edge 閾值 / 無 bootstrap CI / 無 Sharpe / 無 drawdown**，這不叫「策略優化」，只是「策略可跑」 |
| confidence_rank ROI +0.055% | ✅ 揭露 | ⚠️ 與 capped_kelly 差距 100x — 強烈暗示 ROI 集中在少數高賠率 outlier，未做敏感度分析 |
| 2 rows invalid odds | ⚠️ 已揭露 | ❌ 沒有分析這 2 筆是隨機還是系統性偏誤（例：postponed game / extra inning） |
| 114/114 PASS | ✅ | ✅ 真實推進，但測試多是 contract 測試，**不是 ROI 統計顯著性測試** |
| `production_ready=false` 維持 | ✅ | ✅ 紀律維持得很好 |

**真實推進**：P13 → P15 把 model probability 與 historical odds 接通，這是必要的一步。
**被高估的部分**：+5.51% ROI 在沒有 drawdown / Sharpe / bootstrap CI 之前，**不能作為下一階段決策的證據**。

---

## 2. CTO P0 判斷（P16 Recommendation Gate）是否合理？

**結論：方向對，但時機太早，順序錯。**

CTO 把 P16 (Recommendation Gate) 放 P0，把 P18 (Strategy Hardening) 放 P2。
這違反一個重要原則：**你不能在不知道策略風險側寫的情況下，就把策略結論翻譯成推薦列。**

如果今天直接做 P16，會發生：
- 推薦列裡的 `paper_stake_fraction` 由 capped_kelly 推導
- 但我們不知道 capped_kelly 的 max drawdown / 95% CI
- 一旦 recommendation row 落地，下游就會把 +5.51% 當作「策略表現」引用
- production gate 之前的所有 audit 都會繼承這個未驗證的數字

**CTO 的盲點：把「資料管線 ready」誤認為「策略 ready」。**

P15 完成的是「odds-aware simulation 能跑」，不是「策略表現可信」。

---

## 3. 對應用戶兩大主軸的進度評估

| 主軸 | 現況 | 缺口 |
|---|---|---|
| **A. MLB 預測 → 運彩投注項目預測建議** | 只有 **ML（獨贏）** 市場，且為歷史 OOF，無 live odds、無讓分/大小/F5/單雙 | 缺 (1) 推薦層消費 P15 artifact (2) 多市場擴展 (3) live odds source |
| **B. 策略優化模擬** | 只跑了 **1 個策略 × 1 組參數**（capped_kelly 預設），無 sweep、無風險指標 | 缺 (1) edge / Kelly fraction sweep (2) Sharpe / drawdown / bootstrap CI (3) 策略比較矩陣 |

**主軸 B 的進度遠落後於主軸 A**，但 CTO 卻把 B 放到 P2。這是誤判。

---

## 4. CEO 修正版 P0–P10

| 優先 | Phase | Focus | 對應主軸 |
|---|---|---|---|
| **P0** | **P16** | **Recommendation Gate Re-evaluation + Strategy Risk Metrics 強制綁定**（必須一起做：gate 的 edge_threshold 必須來自 sweep 證據，stake 必須附帶 drawdown / Sharpe） | A + B |
| P1 | P17 | Paper Recommendation Ledger / Settlement Join（推薦落地稽核） | A |
| P2 | P18 | Strategy Threshold Sweep（edge / kelly_fraction / confidence 三維 grid + bootstrap CI） | B |
| P3 | P19 | Odds Data Quality Audit（2 rows invalid 根因 + game_id-based join 取代位置映射） | A |
| P4 | P20 | TSL Market Expansion 設計：讓分、大小、F5、單雙、隊伍總分（先做 schema + paper-only，不接 live） | A |
| P5 | P21 | Daily PAPER MLB Recommendation Orchestrator（每日跑通 P13→P15→P16→P17） | A |
| P6 | P22 | Model Calibration Refresh（Brier/ECE 校準 + walk-forward 重跑） | A |
| P7 | P23 | Live TSL / Approved Odds Source 修復（403 / cookie / CSV bridge） | A |
| P8 | P24 | CI / Regression / Worktree Hygiene（消除 dirty data/、outputs/、runtime/） | 基建 |
| P9 | P25 | Daily Ops Monitoring（gate 漂移 / coverage 退化 / ROI 衰減告警） | 基建 |
| P10 | P26 | Production Proposal Gate（人工審批 + 多輪 live shadow 後才考慮） | A |

**關鍵差異 vs CTO**：
- P0 把 P16 與「風險指標綁定」合併，避免推薦列繼承未驗證 ROI
- P18 (Threshold Sweep) 從 P2 提到 P2（保持），但**列為 P0 的前置強制依賴**
- 把 Odds Quality Audit 提到 P3（CTO 是 P3，一致）
- TSL Market Expansion 提到 P4（CTO 是 P7）— 因為用戶明確指主軸 A 是「運彩投注項目」，不只 ML

---

## 5. 今天最應聚焦方向

**P0 = P16 Recommendation Gate + 強制嵌入策略風險指標。**

不是純 gate 翻譯，而是：
1. 在 gate 決策前，先對 P15 simulation ledger 跑 **edge_threshold sweep（0.01 / 0.02 / 0.03 / 0.05）**
2. 對每個 threshold 計算 **avg edge / capped_kelly ROI / max drawdown / Sharpe / bootstrap 95% CI**
3. Gate 必須引用 sweep 結果選 threshold，而不是寫死 `--edge-threshold 0.02`
4. Recommendation row 必須包含 `strategy_risk_profile`（drawdown_pct, sharpe, ci_low, ci_high）
5. 仍維持 `production_ready=false`、`paper_only=true`

---

## 6. 今天可直接執行的任務 Prompt

```text
# ROLE
You are Betting-pool's P16 Recommendation Gate + Strategy Risk Hardening Agent
(CEO-revised scope, supersedes CTO P16-only scope).

# MISSION
Re-evaluate the MLB PAPER recommendation gate using P13 + P14 + P15 artifacts,
AND simultaneously harden the strategy evidence with risk metrics and threshold sweep.

Two deliverables in ONE phase (non-negotiable bundling, per CEO review):
  (1) Recommendation rows that consume P15 odds-aware artifacts.
  (2) Strategy risk profile (Sharpe / drawdown / bootstrap CI / threshold sweep)
      embedded into the gate decision AND into every recommendation row.

This phase is NOT production betting.
This phase is NOT live TSL repair.
This phase is NOT model improvement.
This phase is strictly PAPER_ONLY gate re-evaluation WITH risk-hardened evidence.

# WHY THIS BUNDLING (CEO RATIONALE)
P15 produced +5.51% capped_kelly ROI with NO drawdown, NO Sharpe, NO bootstrap CI,
NO edge threshold sweep. A recommendation gate that consumes this evidence without
risk hardening will propagate an unverified ROI number into every downstream
audit. CEO blocks any P16 scope that does not include risk metrics.

# PROJECT LOCK
- Required repo: /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
- Required branch: p13-clean
- Required prior commits:
  - P13: 8e74863 or later
  - P14: 2dfb0ee or later
  - P15: 2d88a7b or later

Forbidden repos:
- /Users/kelvin/Kelvin-WorkSpace/Betting-pool
- /Users/kelvin/Kelvin-WorkSpace/LotteryNew
- /Users/kelvin/app-workspace/novel
- /Users/kelvin/SCB/workspace-AI/MobileBank_Middleware

If repo/branch does not match, STOP and report context drift.

# HARD GUARD
DO NOT:
- touch /Users/kelvin/Kelvin-WorkSpace/Betting-pool
- push, open PR, or modify branch protection / workflows
- write production DB
- place real bets / call live TSL / scrape live odds
- claim production readiness
- bypass MLB PAPER_ONLY gate
- alter P13/P15 metrics
- fabricate odds or fabricate risk metrics
- run pull / reset / stash / clean
- commit DB binaries, runtime/, .venv/, or large generated outputs
- write a recommendation gate that ignores risk metrics (CEO veto)

# PRIMARY INPUTS
P13:
  outputs/predictions/PAPER/2026-05-12/p13_walk_forward_logistic/oof_predictions.csv
  outputs/predictions/PAPER/2026-05-12/p13_walk_forward_logistic/oof_report.json

P15:
  outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/joined_oof_with_odds.csv
  outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/simulation_summary.json
  outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/simulation_ledger.csv
  outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/odds_join_report.json

# TASKS

## Task 1 — Repo / marker / evidence check
Run:
  cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
  pwd && git rev-parse --show-toplevel
  git branch --show-current
  git log --oneline -8
  git status --short --branch | head -100

Verify markers:
  grep "P13_WALK_FORWARD_LOGISTIC_BASELINE_READY" 00-BettingPlan/20260512/p13_walk_forward_logistic_baseline_report.md
  grep "P14_STRATEGY_SIMULATION_SPINE_READY"      00-BettingPlan/20260512/p14_strategy_simulation_spine_activation_report.md
  grep "P15_MARKET_ODDS_JOIN_SIMULATION_READY"    00-BettingPlan/20260512/p15_market_odds_join_simulation_report.md

If any marker missing → STOP and report blocker.

## Task 2 — Strategy Risk Metrics Module (NEW, CEO-mandated)
Create:
  wbc_backend/simulation/strategy_risk_metrics.py

Required functions:
- compute_max_drawdown(equity_curve: list[float]) -> float
- compute_sharpe(returns: list[float], rf: float = 0.0) -> float
- compute_max_consecutive_loss(pnl_series: list[float]) -> int
- bootstrap_roi_ci(pnl_series: list[float], n_iter: int = 2000, seed: int = 42) -> tuple[float, float]
- summarize_strategy_risk(ledger_df) -> StrategyRiskProfile

StrategyRiskProfile fields:
- roi_mean
- roi_ci_low_95
- roi_ci_high_95
- max_drawdown_pct
- sharpe_ratio
- max_consecutive_loss
- n_bets
- n_winning_bets
- hit_rate

Deterministic: fixed seed for bootstrap.

## Task 3 — Edge Threshold Sweep (NEW, CEO-mandated)
Create:
  wbc_backend/simulation/edge_threshold_sweep.py

Required:
- sweep_edge_thresholds(ledger_df, thresholds=[0.01, 0.02, 0.03, 0.05, 0.08]) -> SweepReport
- For each threshold, compute StrategyRiskProfile + n_eligible_rows
- Produce a recommended threshold based on: max Sharpe subject to n_bets >= 50
- If no threshold satisfies n_bets >= 50, mark SWEEP_INSUFFICIENT_SAMPLES

SweepReport must include:
- per_threshold_rows
- recommended_threshold
- recommended_reason
- fallback_threshold (if recommended fails)

## Task 4 — Inspect existing recommendation system
Read & document:
  wbc_backend/recommendation/
  scripts/run_mlb_tsl_paper_recommendation.py
  tests/test_recommendation_gate_policy.py
  tests/test_recommendation_row_contract.py

Capture: existing row contract, required fields, current gate reasons,
PAPER_ONLY enforcement path, stake policy.

## Task 5 — P16 Recommendation Input Adapter
Create/update:
  wbc_backend/recommendation/p16_recommendation_input_adapter.py

Input: P15 joined_oof_with_odds.csv
Output fields (must include all):
- game_id / date / p_model / p_market / edge / odds_decimal
- odds_join_status / y_true (if available)
- source_model = "p13_walk_forward_logistic"
- source_bss_oof = 0.008253
- odds_join_coverage = 0.9987
- paper_only = true / production_ready = false

Rules:
- Only odds_join_status == JOINED is eligible
- Invalid / missing odds preserved but marked ineligible

## Task 6 — P16 Gate (must consume sweep + risk profile)
Create/update:
  wbc_backend/recommendation/p16_recommendation_gate.py

Required gate logic:
- production_ready must be false
- paper_only must be true
- source_bss_oof > 0
- odds_join_status == JOINED
- p_model / p_market valid probabilities
- edge >= recommended_threshold (from Task 3 sweep, NOT hardcoded)
- odds_decimal valid
- stake is paper stake only
- If sweep returned SWEEP_INSUFFICIENT_SAMPLES → gate must emit
  P16_BLOCKED_SWEEP_INSUFFICIENT_SAMPLES and refuse to recommend

Reason codes (extended):
- P16_ELIGIBLE_PAPER_RECOMMENDATION
- P16_BLOCKED_NOT_PAPER_ONLY
- P16_BLOCKED_PRODUCTION_NOT_ALLOWED
- P16_BLOCKED_NEGATIVE_OR_ZERO_BSS
- P16_BLOCKED_ODDS_NOT_JOINED
- P16_BLOCKED_INVALID_PROBABILITY
- P16_BLOCKED_INVALID_ODDS
- P16_BLOCKED_EDGE_BELOW_THRESHOLD
- P16_BLOCKED_INVALID_STAKE
- P16_BLOCKED_SWEEP_INSUFFICIENT_SAMPLES   (NEW)
- P16_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT       (NEW, drawdown_pct > 25)
- P16_BLOCKED_SHARPE_BELOW_FLOOR           (NEW, sharpe < 0.0)
- P16_BLOCKED_UNKNOWN

## Task 7 — Recommendation Row Builder (must carry risk profile)
Create/update:
  wbc_backend/recommendation/p16_recommendation_row_builder.py

Row fields (extended):
- recommendation_id / game_id / date / side
- p_model / p_market / edge / odds_decimal
- paper_stake_fraction / strategy_policy
- gate_decision / gate_reason
- source_model / source_bss_oof / odds_join_status
- paper_only / production_ready
- created_from = "P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED"
- strategy_risk_profile_roi_ci_low_95   (NEW)
- strategy_risk_profile_roi_ci_high_95  (NEW)
- strategy_risk_profile_max_drawdown    (NEW)
- strategy_risk_profile_sharpe          (NEW)
- strategy_risk_profile_n_bets          (NEW)
- selected_edge_threshold               (NEW)

Stake rules:
- Gate fail → stake = 0
- Gate pass → paper stake per capped_kelly, but capped at
  min(kelly_stake, 0.02) AND must respect strategy_risk_profile

## Task 8 — CLI
Create:
  scripts/run_p16_recommendation_gate_reevaluation.py

Args:
  --joined-oof <P15 joined CSV>
  --p15-summary <P15 summary JSON>
  --p15-ledger <P15 ledger CSV>          (NEW, for sweep)
  --output-dir outputs/predictions/PAPER/2026-05-12/p16_recommendation_gate
  --paper-only true
  --edge-threshold-grid 0.01,0.02,0.03,0.05,0.08
  --min-bets-floor 50
  --max-drawdown-limit 0.25
  --sharpe-floor 0.0

Outputs:
- recommendation_rows.csv
- recommendation_summary.json
- recommendation_summary.md
- gate_reason_counts.json
- strategy_risk_profile.json            (NEW)
- edge_threshold_sweep.json             (NEW)
- edge_threshold_sweep.md               (NEW)

Summary fields (extended):
- p16_gate
- n_input_rows / n_joined_rows / n_eligible_rows
- n_recommended_rows / n_blocked_rows
- selected_edge_threshold / sweep_recommended_reason
- strategy_roi_mean / strategy_roi_ci_low_95 / strategy_roi_ci_high_95
- strategy_max_drawdown / strategy_sharpe / strategy_n_bets
- source_bss_oof / odds_join_coverage
- production_ready = false / paper_only = true
- top_gate_reasons / generated_from_p15_gate

Gate decisions:
- P16_PAPER_RECOMMENDATION_GATE_READY
- P16_BLOCKED_NO_ELIGIBLE_ROWS
- P16_BLOCKED_INPUT_MISSING
- P16_BLOCKED_SWEEP_INSUFFICIENT_SAMPLES
- P16_BLOCKED_RISK_PROFILE_VIOLATION
- P16_FAIL_CONTRACT_VIOLATION
- P16_FAIL_NON_DETERMINISTIC

## Task 9 — Tests
Create:
  tests/test_strategy_risk_metrics.py
  tests/test_edge_threshold_sweep.py
  tests/test_p16_recommendation_input_adapter.py
  tests/test_p16_recommendation_gate.py
  tests/test_run_p16_recommendation_gate_reevaluation.py

Required cases:
- drawdown math correct on synthetic curve
- Sharpe matches reference on synthetic returns
- bootstrap CI deterministic with fixed seed
- sweep returns SWEEP_INSUFFICIENT_SAMPLES when n_bets < 50 everywhere
- sweep picks max-Sharpe threshold subject to floor
- joined rows eligible; missing/invalid blocked
- invalid probability / invalid odds / zero BSS blocked
- edge below selected threshold blocked
- paper_only=false / production_ready=true ALWAYS blocked
- drawdown > limit → P16_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT
- sharpe < floor → P16_BLOCKED_SHARPE_BELOW_FLOOR
- passed rows carry strategy_risk_profile_* fields
- failed rows have stake 0
- CLI emits all 7 outputs
- CLI is deterministic across two runs

Run:
  ./.venv/bin/pytest -q \
    tests/test_strategy_risk_metrics.py \
    tests/test_edge_threshold_sweep.py \
    tests/test_p16_recommendation_input_adapter.py \
    tests/test_p16_recommendation_gate.py \
    tests/test_run_p16_recommendation_gate_reevaluation.py \
    tests/test_p15_market_odds_adapter.py \
    tests/test_run_p15_market_odds_join_simulation.py \
    tests/test_p14_strategy_policies.py \
    tests/test_p14_strategy_simulator.py

## Task 10 — Real P16 run
Run CLI with the args above.
Print:
- p16_gate / selected_edge_threshold / sweep_recommended_reason
- n_input_rows / n_joined_rows / n_eligible_rows
- n_recommended_rows / n_blocked_rows
- top gate reasons
- strategy_roi_mean / ci_low / ci_high
- strategy_max_drawdown / strategy_sharpe
- production_ready / paper_only

## Task 11 — Determinism check
Run CLI twice into:
  outputs/predictions/PAPER/2026-05-12/p16_recommendation_gate
  outputs/predictions/PAPER/2026-05-12/p16_recommendation_gate_run2

Compare (excluding generated_at if present):
- recommendation_summary.json
- recommendation_rows.csv
- gate_reason_counts.json
- strategy_risk_profile.json
- edge_threshold_sweep.json

## Task 12 — Final report
Create:
  00-BettingPlan/20260512/p16_recommendation_gate_reevaluation_report.md

Required sections:
1. Repo evidence
2. P13/P14/P15 prior evidence
3. CEO scope expansion rationale (why risk metrics bundled)
4. Strategy risk metrics design
5. Edge threshold sweep result table (per-threshold ROI / Sharpe / drawdown / n_bets)
6. Selected threshold + reason
7. Recommendation input adapter summary
8. Gate policy summary (with new reason codes)
9. Recommendation row contract (with risk profile fields)
10. Test results
11. Real P16 run result
12. Gate reason distribution
13. Determinism result
14. Production readiness statement (must remain false)
15. Risk and limitations (explicitly call out: historical-only, no live TSL,
    single market ML only, 2 rows invalid odds still unresolved, position-based
    join still fragile)
16. Next-phase recommendation (P17 ledger / settlement)
17. Marker line

Marker:
  P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY

## Task 13 — Commit
Stage only:
  wbc_backend/simulation/strategy_risk_metrics.py
  wbc_backend/simulation/edge_threshold_sweep.py
  wbc_backend/recommendation/p16_recommendation_input_adapter.py
  wbc_backend/recommendation/p16_recommendation_gate.py
  wbc_backend/recommendation/p16_recommendation_row_builder.py
  scripts/run_p16_recommendation_gate_reevaluation.py
  tests/test_strategy_risk_metrics.py
  tests/test_edge_threshold_sweep.py
  tests/test_p16_recommendation_input_adapter.py
  tests/test_p16_recommendation_gate.py
  tests/test_run_p16_recommendation_gate_reevaluation.py
  00-BettingPlan/20260512/p16_recommendation_gate_reevaluation_report.md

Before commit:
  git diff --cached --name-only
  git diff --cached --name-only | grep -E "\.(db|db-wal|db-shm|sqlite|sqlite3)$|^runtime/|^outputs/|^\.venv/" || echo "NO_FORBIDDEN_FILES"

Commit:
  git commit -m "feat(betting): P16 recommendation gate + strategy risk hardening (CEO-revised)"
  git rev-parse HEAD

Do NOT push.

# ACCEPTANCE CRITERIA
- P13/P14/P15 markers verified
- Strategy risk metrics module exists and tested
- Edge threshold sweep exists and tested
- Selected edge_threshold comes from sweep, NOT hardcoded
- Gate enforces drawdown ceiling and Sharpe floor
- Recommendation rows carry strategy_risk_profile_* fields
- Failed rows → stake 0; passed rows → paper stake capped
- All tests PASS
- Real run completes with explicit risk numbers printed
- Determinism check PASS
- No production DB write / no live TSL / no real bets
- Report includes marker:
  P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY
- production_ready remains false

# FINAL OUTPUT
Return:
1. P16 commit hash
2. P16 gate decision
3. selected_edge_threshold and reason
4. n_recommended_rows / n_blocked_rows
5. strategy_roi_mean + 95% CI + max_drawdown + Sharpe
6. top gate reasons
7. test result summary
8. production_ready=false confirmation
9. next recommended phase:
   - GATE_READY → P17 Paper Recommendation Ledger / Settlement Join
   - SWEEP_INSUFFICIENT_SAMPLES → revisit P15 ledger / lower n_bets floor / expand data
   - RISK_PROFILE_VIOLATION → tune strategy policy before P17
   - FAIL_* → repair contract before P17

# FINAL MARKER
P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY
```

---

## CEO 10 行摘要

1. P15 推進了「資料管線」，但沒推進「策略可信度」。
2. CTO 把 P16 放 P0、P18 放 P2 是順序錯誤 — 不能在沒有 drawdown/Sharpe 之前翻譯成推薦列。
3. 用戶兩大主軸：A 預測投注建議、B 策略優化模擬 — B 嚴重落後且被 CTO 低估。
4. +5.51% capped_kelly ROI 沒有 bootstrap CI、沒有 Sharpe、沒有 drawdown — 不能直接餵 gate。
5. 今天 P0 = P16 + 強制嵌入風險指標 + edge threshold sweep（三件綁定，CEO 否決純 gate 翻譯）。
6. 新增閘門：drawdown > 25% 阻擋、Sharpe < 0 阻擋、n_bets < 50 觸發 SWEEP_INSUFFICIENT_SAMPLES。
7. Recommendation row 必須攜帶 strategy_risk_profile 5 個欄位，供下游稽核。
8. TSL 多市場（讓分/大小/F5）從 CTO 的 P7 提到 P4，因為用戶明確說「運彩投注項目」≠ 只有 ML。
9. Live TSL 修復降到 P7 — 沒有 paper 證據前不該碰 live。
10. Marker：`P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY`，`production_ready=false` 不變。