# Active Task — P43 sp_fip_delta Strong-Edge Closing-Line Edge Validation

> **[ACTIVE 2026-05-25]** `P43_STRONG_EDGE_CLOSING_LINE_EDGE_VALIDATION`
> **Issued by**: CEO Second-Level Review 2026-05-25
> **CEO classification**: `CEO_DECISION_PARTIALLY_APPROVED`
> **CTO P0 override**: P42 reconciliation 降為 P1；本任務為新 P0
> **HEAD**: `43cc739` | **Branch**: `main` | **Mode**: `paper_only=true`

---

## Task Prompt（直接交給 Planner / Worker）

```md
[P43 — sp_fip_delta Strong-Edge Closing-Line Edge Validation]

# Branch Governance
## Canonical Repo
/Users/kelvin/Kelvin-WorkSpace/Betting-pool
## Canonical Branch
main
## Rules
- Do NOT create a new branch
- Do NOT create a new worktree
- Do NOT checkout another branch
- Do NOT clone another repo
- Do NOT use detached HEAD
- Worktree dirty files MUST NOT be staged; commit whitelist-only.

# Required Pre-flight
git rev-parse --show-toplevel        # 預期: /Users/kelvin/Kelvin-WorkSpace/Betting-pool
git branch --show-current             # 預期: main
git rev-parse HEAD                    # 預期: 43cc739
git status --short                    # 紀錄但不依此 stage 全部
git log --oneline -8

# STOP Conditions
- Wrong repo / wrong branch / detached HEAD → STOP
- HEAD ≠ 43cc739 且未經 CEO authorization → STOP
- 偵測 live odds API call、TSL crawler 修改、champion replacement → STOP

---

## 1. Task Name
P43 — sp_fip_delta Strong-Edge Closing-Line Edge Validation (Paper-Only Diagnostic)

## 2. Background
P41 已 confirm `sp_fip_delta` strong-edge T=0.50 為 cross-year robust ranking signal
（n=1490, AUC=0.5865, bootstrap CI [0.5557, 0.6170]）。
但 AUC 只證明 **ranking ability**，**不等於 beat the closing line**。
P42 進一步建立 Tier A/B/C framework，但 JSON brier 欄位為 None（與 markdown 顯示的數字不一致）。

CEO directive: 回到資料驗證主線——確認模型是否穩定優於 closing line。

## 3. Goal
量化 sp_fip_delta strong-edge (|delta| >= 0.50) 篩選的賽事中，
模型機率相對於 closing line 隱含機率的 edge 是否有統計顯著正值。

## 4. Allowed Modification Scope (whitelist)
- `scripts/_p43_strong_edge_closing_line_edge_validation.py` (NEW)
- `tests/test_p43_strong_edge_closing_line_edge_validation.py` (NEW)
- `report/p43_strong_edge_closing_line_edge_validation_20260525.md` (NEW)
- `data/mlb_2025/derived/p43_strong_edge_closing_line_edge_summary.json` (NEW)
- `00-BettingPlan/20260525/p43_strong_edge_closing_line_edge_validation_20260525.md` (NEW)
- `00-Plan/roadmap/active_task.md` (本檔，最終狀態更新)

## 5. Forbidden Modification Scope (hard blocks)
- 禁止修改 `wbc_backend/clv/outcome_matching.py` (P26 contract frozen)
- 禁止修改 `wbc_backend/pipeline/prediction_orchestrator.py`
- 禁止修改 `wbc_backend/strategy/marl_optimizer.py`
- 禁止修改 `data/mlb_2025/mlb_odds_2025_real.csv` (source data immutable)
- 禁止修改 `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl` (P39 frozen)
- 禁止修改 `data/tsl_odds_history.jsonl` 或任何 TSL crawler 檔案
- 禁止替換 champion `fixed_edge_5pct`
- 禁止呼叫 live odds API
- 禁止 promotion / champion replacement / optimizer promotion
- 禁止覆蓋 P23/P24/P25/P26/P40/P41/P42 baselines
- 禁止 stage runtime/raw feed/daemon output
- 禁止輸出任何 "guaranteed profit" / "profitability claim" / "production proposal" / "live odds api call"

## 6. Required Work

### Step 1 — Data inventory (from existing files, no new fetch)
1. Load 2025 dataset: `data/mlb_2025/mlb_odds_2025_real.csv`
   - Use `Home ML` / `Away ML` 作為 closing line (CSV 內為 closing odds)
   - `Home Score` / `Away Score` 作為 outcome
2. Load 2024 holdout: `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl`
   - 包含 sp_fip_delta、closing line implied probabilities、actual outcome
3. Apply P41 cross-year join logic to get unified records (use P41 / P40 scripts as reference, no rewrite)

### Step 2 — Compute model probability
1. 以 P41/P42 validated method 計算 model home win probability for each game
2. 不重新訓練；僅引用已 confirmed 的 sp_fip_delta-based logistic mapping at T=0.50
3. 若需 baseline model，使用 simple LogReg on closing implied prob (no MARL, no Orchestrator stack)
4. 記錄每筆 record: game_id, year, sp_fip_delta, model_prob, market_prob (closing), actual_outcome

### Step 3 — Compute edge vs closing line
1. For each game with |sp_fip_delta| >= 0.50:
   - `edge = model_prob - market_prob` (側別自動：以 model 偏向方向計算)
   - 若 |edge| < 0.005 視為 NEUTRAL
2. Compute strong-edge subset filter
3. 報告以下統計:
   - n
   - mean edge
   - median edge
   - std
   - positive_rate
   - bootstrap 95% CI (n_boot=5000)
   - top-1% contribution

### Step 4 — Tier breakdown
1. Tier C: |sp_fip_delta| >= 0.50
2. Tier B: |sp_fip_delta| >= 1.00 (調整 P42 thresholds 以對齊 0.5/1.0/1.5)
3. Tier A: |sp_fip_delta| >= 1.50
4. 每個 tier 輸出: n, mean_edge, CI, positive_rate, classification

### Step 5 — Year-by-year breakdown
1. 2024 only
2. 2025 only
3. 2024+2025 combined
4. 每年每 tier: n, mean_edge, CI

### Step 6 — Bootstrap significance
1. Bootstrap CI for combined mean edge
2. CI 全正 → `EDGE_CONFIRMED`
3. CI 上界 > 0 但 mean 小 → `WEAK_STABLE`
4. CI 穿越 0 → `INCONCLUSIVE`
5. CI 全負 → `NEGATIVE`
6. n < 30 → `SAMPLE_LIMITED`

### Step 7 — Important framing note in report
- **必須明確記載**: 「This analysis uses CSV closing-line implied probability vs model probability.
  CSV 不含 opening / pregame snapshot, 因此這是 'edge vs closing line', not strict CLV (which requires
  pregame → closing comparison). P26 line-aware CLV diagnostic is separate and unchanged.」

### Step 8 — Tests
- 至少 8 個 deterministic tests:
  - Test 1: data load shape match
  - Test 2: |delta| >= 0.50 filter correct
  - Test 3: edge computation correctness
  - Test 4: bootstrap CI is deterministic given seed
  - Test 5: tier breakdown counts match expected
  - Test 6: year split correctness
  - Test 7: classification logic (EDGE_CONFIRMED / WEAK_STABLE / etc.)
  - Test 8: paper_only / promotion_freeze flags in JSON output

### Step 9 — Artifacts
1. JSON: `data/mlb_2025/derived/p43_strong_edge_closing_line_edge_summary.json`
   - 含 paper_only=true, diagnostic_only=true, promotion_freeze=true, kelly_deploy_allowed=false
   - 含 framing_note (edge vs closing line, not strict CLV)
   - 含 tier_metrics, year_metrics, combined_metrics, classification
2. Report MD: `report/p43_strong_edge_closing_line_edge_validation_20260525.md`
3. BettingPlan: `00-BettingPlan/20260525/p43_strong_edge_closing_line_edge_validation_20260525.md`
4. Script + tests

## 7. Constraints
- `paper_only=true`
- `diagnostic_only=true`
- `promotion_freeze=true`
- `kelly_deploy_allowed=false`
- `T_LOCKED=0.50` (must NOT re-optimize)
- No live API call
- No TSL crawler modification
- No champion replacement
- No production proposal
- No branch / worktree / clone
- 不可在報告中聲稱 profitability / guaranteed profit / production ready
- 不依賴 P42 brier=None 的 JSON 欄位（若需 Brier，自行重算並標示為 P43-computed）

## 8. Validation / Test Commands
- `/opt/homebrew/bin/pytest tests/test_p43_strong_edge_closing_line_edge_validation.py -v`
- `/opt/homebrew/bin/pytest tests/test_p41_cross_year_combined_wfv.py tests/test_p42_signal_band_tier_kelly.py tests/test_p43_strong_edge_closing_line_edge_validation.py -q`
- 期望: P43 ≥ 8 tests PASS, P41+P42+P43 cumulative PASS
- Forbidden affirmative scan: 0 hits

## 9. Output Report Locations
- `data/mlb_2025/derived/p43_strong_edge_closing_line_edge_summary.json`
- `report/p43_strong_edge_closing_line_edge_validation_20260525.md`
- `00-BettingPlan/20260525/p43_strong_edge_closing_line_edge_validation_20260525.md`

## 10. Final Classification (預期)
依結果擇一:
- `P43_EDGE_CONFIRMED` (Tier C combined CI 全正)
- `P43_EDGE_WEAK_STABLE` (mean > 0 但 CI 接近 0)
- `P43_EDGE_INCONCLUSIVE` (CI 穿越 0) — 合理結果
- `P43_EDGE_NEGATIVE` (CI 全負) — 表示 model 未能 beat closing line
- `P43_EDGE_SAMPLE_LIMITED` (n 不足)
- `P43_BLOCKED_BY_DATA_GAP` (若 join 失敗)

## 11. Handoff Report Required Sections
- Pre-flight result
- Data inventory (which files used, row counts)
- Edge computation methodology
- Tier breakdown table
- Year-by-year table
- Bootstrap CI results
- Classification per tier and combined
- Framing note (edge vs closing line, not strict CLV)
- Files created / modified
- Tests PASS / FAIL
- Forbidden scan result
- Commit hash or reason not committed
- 10 行內 CTO summary

---

# Strict Reminder

- 本任務由 CEO 指派，**override CTO 原 P0 (P42 reconciliation)**
- P42 reconciliation 降為 P1，可在 P43 引用 metrics 時順帶處理
- 本任務嚴格 diagnostic-only，不得轉為 production / promotion / champion replacement
- 若任何 step 觸發 STOP condition → 停止並回報，不嘗試 workaround
```

---

## Execution Status Update (2026-05-25)

- Status: `COMPLETED (diagnostic-only)`
- Final classification: `P43_BLOCKED_BY_DATA_GAP`
- Combined Tier C rule classification (available data): `EDGE_CONFIRMED`
- Data gap evidence: `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl` does not contain closing-line market implied probabilities; 2024 market-joinable rows = `0`.

### Deliverables Generated

- `scripts/_p43_strong_edge_closing_line_edge_validation.py`
- `tests/test_p43_strong_edge_closing_line_edge_validation.py`
- `data/mlb_2025/derived/p43_strong_edge_closing_line_edge_summary.json`
- `report/p43_strong_edge_closing_line_edge_validation_20260525.md`
- `00-BettingPlan/20260525/p43_strong_edge_closing_line_edge_validation_20260525.md`

### Validation Results

- `pytest tests/test_p43_strong_edge_closing_line_edge_validation.py -v` → `9 passed`
- `pytest tests/test_p41_cross_year_combined_wfv.py tests/test_p42_signal_band_tier_kelly.py tests/test_p43_strong_edge_closing_line_edge_validation.py -q` → `139 passed`
- Forbidden phrase scan (`guaranteed profit|profitability claim|production proposal|live odds api call`) on P43 artifacts → `0 hits`

### Known Limitation — 2024 Closing-Line Data Gap (P43.1 Confirmed)

> **Confirmed 2026-05-25 via P43.1 repo-wide search.**

- `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl` (P39 frozen artifact): does **not** contain `Home ML`, `Away ML`, `home_implied_prob`, `away_implied_prob`, or `market_home_prob` columns. All 2429 rows have `null` market probability.
- `data/mlb_2025/mlb-2024-asplayed.csv`: Retrosheet gamelog only (scores + starters). No odds columns.
- No other 2024 closing-line odds CSV exists in the repository.
- `data/mlb_context/odds_timeline.jsonl` and related files: 2025-season entries only.
- **Implication**: Cross-year (2024+2025) closing-line edge validation cannot be completed without an external 2024 MLB moneyline odds CSV. The P43 final classification remains `P43_BLOCKED_BY_DATA_GAP`. The 2025-only result (Tier B/C `EDGE_CONFIRMED`) stands as a valid partial finding.
- **Resolution path**: If `data/mlb_2025/mlb_odds_2024_real.csv` is ever sourced with matching schema (`Date, Away, Home, Away Score, Home Score, Away ML, Home ML`), re-run P43 script — `load_2024_unified()` already has the join logic stub.

---

## P44 Proposal — sp_fip_delta 2025 Signal Temporal Stability + Calibration Audit

> **[PROPOSED 2026-05-25]** `P44_SIGNAL_TEMPORAL_STABILITY_CALIBRATION`
> **Prerequisite**: P43 complete (committed `1e09997`).
> **Classification**: `paper_only=true`, `diagnostic_only=true`, `promotion_freeze=true`, `kelly_deploy_allowed=false`

### Rationale

P43 confirmed a positive closing-line edge for 2025 (Tier B/C), but two critical questions remain unanswered before any paper-trading escalation:

1. **Temporal stability**: Is the edge uniform across the 2025 season, or does it degrade in later months (signal decay, pitcher FIP regression, market adaptation)?
2. **Calibration**: Does the sigmoid model probability (`p = 1/(1+exp(-0.8·delta))`) accurately reflect actual win rates, or is it systematically over/under-confident?

### Proposed Scope

#### P44.A — Monthly Temporal Edge Breakdown (2025 Tier C)
- Split Tier C games (`|sp_fip_delta| >= 0.50`) by calendar month (Apr–Sep 2025).
- Compute per-month: `n`, `mean_edge`, `positive_rate`, bootstrap 95% CI.
- Classification: stable (all months CI overlap), degrading (late-season CI crosses 0), or improving.
- Output: `data/mlb_2025/derived/p44_temporal_stability_summary.json`

#### P44.B — Calibration Audit (2025 Tier C)
- 10-bin reliability diagram: bin model_prob [0.0, 1.0], compute actual win rate per bin.
- Brier score decomposition: reliability + resolution + uncertainty.
- Expected Calibration Error (ECE).
- Overconfidence / underconfidence diagnosis.
- Output: `data/mlb_2025/derived/p44_calibration_audit_summary.json`

### Tests Required
- ≥ 8 deterministic tests covering both modules.
- Re-run P41+P42+P43+P44 cumulative suite.

### Whitelist for P44 Commit
- `scripts/_p44_signal_temporal_stability_calibration.py` (NEW)
- `tests/test_p44_signal_temporal_stability_calibration.py` (NEW)
- `data/mlb_2025/derived/p44_temporal_stability_summary.json` (NEW)
- `data/mlb_2025/derived/p44_calibration_audit_summary.json` (NEW)
- `report/p44_signal_temporal_stability_calibration_20260525.md` (NEW)
- `00-BettingPlan/20260525/p44_signal_temporal_stability_calibration_20260525.md` (NEW)
- `00-Plan/roadmap/active_task.md` (this file, status update)

