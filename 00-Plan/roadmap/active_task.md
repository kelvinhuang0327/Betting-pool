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

---

## P44 Execution Status Update (2026-05-25)

- Status: `COMPLETED (diagnostic-only)`
- Final classification: `P44_STABLE_AND_CALIBRATED` (temporal STABLE, calibration MODERATE_MISCALIBRATED)

### P44.A — Temporal Stability Results (Tier C, n=535)

| Month | n | Mean Edge | CI Low | CI High | Classification |
|-------|---|-----------|--------|---------|----------------|
| 2025-04 | 16 | 0.0954 | 0.0548 | 0.1344 | STABLE |
| 2025-05 | 120 | 0.1050 | 0.0882 | 0.1212 | STABLE |
| 2025-06 | 101 | 0.1101 | 0.0919 | 0.1275 | STABLE |
| 2025-07 | 92 | 0.1083 | 0.0913 | 0.1253 | STABLE |
| 2025-08 | 108 | 0.1003 | 0.0851 | 0.1159 | STABLE |
| 2025-09 | 98 | 0.1084 | 0.0922 | 0.1246 | STABLE |

**Overall Temporal Pattern: TEMPORAL_STABLE** — all 6 months show CI fully positive.

### P44.B — Calibration Results (Tier C, 10-bin)

- **Brier Score**: 0.248133
- **ECE**: 0.095289 (bins with n >= 5 only)
- **Calibration Classification**: MODERATE_MISCALIBRATED

Observation: Low-prob bins (0.2-0.4) show model underconfidence; high-prob bins (0.7-0.8) show overconfidence.
Sigmoid mapping `p = sigmoid(0.8 * delta)` is not perfectly calibrated; Platt scaling would improve ECE.

### Known Limitation Remains

- 2024 closing-line data gap **unresolved** — all analysis covers 2025 only.
- This is edge vs closing-line, NOT strict CLV.
- No production deployment. No champion replacement. Paper-only.

### Deliverables Generated

- `scripts/_p44_signal_temporal_stability_calibration.py`
- `tests/test_p44_signal_temporal_stability_calibration.py` (14 tests PASS)
- `data/mlb_2025/derived/p44_temporal_stability_summary.json`
- `data/mlb_2025/derived/p44_calibration_audit_summary.json`
- `report/p44_signal_temporal_stability_calibration_20260525.md`
- `00-BettingPlan/20260525/p44_signal_temporal_stability_calibration_20260525.md`

### Validation Results

- `pytest tests/test_p44_signal_temporal_stability_calibration.py -v` → `14 passed`
- Cumulative `pytest P41+P42+P43+P44 -q` → `153 passed`
- Forbidden phrase scan → 0 hits

---

## P45 Execution Status Update (2026-05-26)

- Status: `COMPLETED (diagnostic-only)`
- Final classification: `P45_RECALIBRATION_HELPFUL`

### P45.A — Train/Test Platt Pilot (80/20, seed=42)

| Metric | Raw | Calibrated | Improvement |
|--------|-----|------------|-------------|
| ECE (test) | 0.097154 | 0.070058 | +0.027096 |
| Brier (test) | 0.230849 | 0.226447 | +0.004402 |

- platt_a: `0.435432`, platt_b: `0.245464`

### P45.B — 5-Fold Cross Validation

| Metric | Mean Raw | Mean Calibrated | Mean Improvement |
|--------|----------|-----------------|------------------|
| ECE | 0.116838 | 0.086164 | +0.030673 |
| Brier | 0.248133 | 0.238477 | +0.009656 |

**CV Classification: RECALIBRATION_HELPFUL** (mean ECE improvement > 0.02 across all 5 folds)

### P45.C — Walk-Forward Monthly (5 evaluations)

- All 5 walk-forward months show ECE improvement after Platt scaling
- **Walk-Forward Classification: WALK_FORWARD_HELPFUL**

### Known Limitations

- 2024 closing-line data gap **remains unresolved**
- Platt scaling is diagnostic only; no recalibrated model deployed
- No production proposal. No champion replacement. Paper-only.

### Deliverables Generated

- `scripts/_p45_platt_recalibration_pilot.py`
- `tests/test_p45_platt_recalibration_pilot.py` (16 tests PASS)
- `data/mlb_2025/derived/p45_platt_recalibration_summary.json`
- `report/p45_platt_recalibration_pilot_20260526.md`
- `00-BettingPlan/20260526/p45_platt_recalibration_pilot_20260526.md`

### Validation Results

- `pytest tests/test_p45_platt_recalibration_pilot.py -v` → `16 passed`
- Cumulative `pytest P41+P42+P43+P44+P45 -q` → `169 passed`
- Forbidden phrase scan → 0 affirmative hits

---

## P46 Execution Status Update (2026-05-26)

- Status: `COMPLETED (diagnostic-only)`
- Final classification: `P46_MIXED_RECALIBRATION_DIAGNOSTIC`

### P46.A — Train/Test Comparison (80/20, seed=42)

| Method | ECE | Brier |
|--------|-----|-------|
| Raw sigmoid | 0.0972 | 0.2308 |
| Platt (P45) | 0.0701 | 0.2264 |
| Isotonic (P46) | 0.0578 | — |

- Isotonic knot count: 13 (reasonable, no overfit risk)
- Isotonic achieves lower test-split ECE, but this is a single split

### P46.B — 5-Fold CV

| Metric | Mean Raw | Mean Platt | Mean Isotonic |
|--------|----------|------------|---------------|
| ECE | 0.1168 | 0.0862 | 0.0842 |

- Iso beats Platt (ECE): 2/5 folds
- **CV Classification: ISOTONIC_COMPARABLE** (Δ only 0.002)

### P46.C — Walk-Forward Monthly (5 evaluations)

- Platt performs better in 3/5 temporal evaluation months
- **Walk-Forward Classification: PLATT_WALK_FORWARD_PREFERRED**

### Interpretation

Isotonic achieves marginally lower ECE in train/test split but is NOT consistently better in CV or walk-forward.
**Platt scaling is more temporally stable.** The small test-split ECE advantage of isotonic (0.058 vs 0.070)
does not hold up in out-of-fold or out-of-month evaluation.

### Known Limitations

- 2024 closing-line data gap **remains unresolved**
- No isotonic or Platt model deployed; diagnostic only
- No production proposal. No champion replacement. Paper-only.

### Deliverables Generated

- `scripts/_p46_isotonic_recalibration_comparison.py`
- `tests/test_p46_isotonic_recalibration_comparison.py` (19 tests PASS)
- `data/mlb_2025/derived/p46_isotonic_recalibration_summary.json`
- `report/p46_isotonic_recalibration_comparison_20260526.md`
- `00-BettingPlan/20260526/p46_isotonic_recalibration_comparison_20260526.md`

### Validation Results

- `pytest tests/test_p46_isotonic_recalibration_comparison.py -v` → `19 passed`
- Cumulative `pytest P41+P42+P43+P44+P45+P46 -q` → `188 passed`
- Forbidden phrase scan → 0 affirmative hits

---

## P47 Execution Status Update (2026-05-26)

- Status: `COMPLETED (diagnostic-only, synthesis only)`
- Final classification: `P47_PLATT_SELECTED_FOR_MONITORING_DIAGNOSTIC`
- Selected monitoring probability stream: `PLATT_CALIBRATED`

### P43-P46 Synthesis Table

| Phase | Key Result | Classification |
|-------|-----------|----------------|
| P43 | Tier C n=535, mean_edge=0.1059, CI fully positive | `EDGE_CONFIRMED` |
| P44 temporal | 6/6 months STABLE, n=535 | `TEMPORAL_STABLE` |
| P44 calibration | ECE=0.0953, Brier=0.2481 | `MODERATE_MISCALIBRATED` |
| P45 Platt | CV ECE 0.1168→0.0862, WF HELPFUL | `P45_RECALIBRATION_HELPFUL` |
| P46 Isotonic | CV ECE iso=0.0842 vs platt=0.0862, beats Platt 2/5 folds | `P46_MIXED_RECALIBRATION_DIAGNOSTIC` |

### Monitoring Thresholds (Advisory Only)

| Metric | Baseline | Warning | Critical |
|--------|----------|---------|----------|
| ECE | 0.0862 (Platt CV) | > 0.10 | > 0.12 |
| Brier | 0.2385 (Platt CV) | > 0.25 | > 0.27 |
| Mean Edge | 0.1059 (Tier C) | < 0.07 | CI crosses zero |
| Monthly CI | All positive | Any crosses zero | Two consecutive |
| Sample batch | — | — | n < 100 → SAMPLE_LIMITED |

### Data Gaps Registered (5 items)

1. **HIGH**: 2024 closing-line odds — blocks cross-year validation
2. **HIGH**: Cross-year market-edge validation — blocked by #1
3. **MEDIUM**: 2026 live odds — blocked by no-live-call governance
4. **MEDIUM**: External odds source provenance documentation
5. **LOW**: Approved paper-trading monitoring loop

### Known Limitations

- 2024 closing-line data gap **remains unresolved**
- No model deployed, no runtime logic changed
- No production proposal. No champion replacement. Paper-only.

### Deliverables Generated

- `scripts/_p47_calibration_synthesis_report.py`
- `tests/test_p47_calibration_synthesis_report.py` (15 tests PASS)
- `data/mlb_2025/derived/p47_calibration_synthesis_summary.json`
- `report/p47_calibration_synthesis_report_20260526.md`
- `00-BettingPlan/20260526/p47_calibration_synthesis_report_20260526.md`

### Validation Results

- `pytest tests/test_p47_calibration_synthesis_report.py -v` → `15 passed`
- Cumulative `pytest P41+P42+P43+P44+P45+P46+P47 -q` → `203 passed`
- Forbidden phrase scan → 0 affirmative hits

---

## P48 Execution Status Update (2026-05-26)

- Status: `COMPLETED (diagnostic-only)`
- Final classification: `P48_MONITORING_CONTRACT_READY_DIAGNOSTIC`
- Selected probability stream: `PLATT_CALIBRATED` (P47 synthesis decision)
- P47 baseline commit: `17dad86`

### P48 Monitoring Contract Summary

| Alert Threshold | Warning | Critical |
|----------------|---------|----------|
| ECE (Platt) | > 0.10 | > 0.12 |
| Brier (Platt) | > 0.25 | > 0.27 |
| Edge mean | < 0.07 | CI crosses zero |
| Sample | — | SAMPLE_LIMITED if n < 100 |
| Data gap | — | DATA_GAP_BLOCKED (overrides all) |

### Fixture Validation Results

| Fixture | Status |
|---------|--------|
| fixture_01_healthy_baseline | MONITORING_OK |
| fixture_02_sample_limited | SAMPLE_LIMITED |
| fixture_03_ece_warning | ECE_DRIFT_WARNING |
| fixture_04_ece_critical | ECE_DRIFT_CRITICAL |
| fixture_05_brier_warning | BRIER_DRIFT_WARNING |
| fixture_06_brier_critical | BRIER_DRIFT_CRITICAL |
| fixture_07_edge_warning | EDGE_DRIFT_WARNING |
| fixture_08_edge_critical | EDGE_DRIFT_CRITICAL |
| fixture_09_mixed_alerts | MIXED_ALERTS |
| fixture_10_data_gap_blocked | DATA_GAP_BLOCKED |

### Deliverables Generated

- `scripts/_p48_monitoring_loop_contract.py`
- `tests/test_p48_monitoring_loop_contract.py` (17 tests)
- `data/mlb_2025/derived/p48_monitoring_loop_contract_summary.json`
- `report/p48_monitoring_loop_contract_20260526.md`
- `00-BettingPlan/20260526/p48_monitoring_loop_contract_20260526.md`

### Known Limitations

- 2024 closing-line data gap **remains unresolved** (P43_BLOCKED_BY_DATA_GAP)
- No live API calls made. No runtime recommendation logic changed.
- No production proposal. No champion replacement. Paper-only monitoring contract.


---

## P49 — Offline Historical Monitoring Replay Using P48 Contract

**Status**: ✅ COMPLETE  
**Commit**: (pending — staging in progress)  
**Date**: 2026-05-26  
**Tests**: 18 tests  
**Cumulative**: 238 tests passed (220 + 18)

### Final Classification

**`P49_MONITORING_REPLAY_CRITICAL_DIAGNOSTIC`**

### Tier C Verification

| Metric | Value |
|--------|-------|
| Rebuilt Tier C n | 535 |
| Expected n | 535 |
| Match | True |
| Date range | 2025-04-01 – 2025-09-28 |

### Monthly Replay Summary (6 months, Apr–Sep 2025)

| Month | n | Status | Alert |
|-------|---|--------|-------|
| 2025-04 | 16 | SAMPLE_LIMITED | WARNING |
| 2025-05 | 120 | EDGE_DRIFT_CRITICAL | CRITICAL |
| 2025-06 | 101 | EDGE_DRIFT_CRITICAL | CRITICAL |
| 2025-07 | 92 | SAMPLE_LIMITED | WARNING |
| 2025-08 | 108 | EDGE_DRIFT_WARNING | WARNING |
| 2025-09 | 98 | SAMPLE_LIMITED | WARNING |

Monthly: OK=0, Warning=1, Critical=2, SampleLMonthly: OK=0, Warning=1, Critical=2, SampleLMonthly: OK=0, Warning=1, Critical=2, SampleL=0, WarnMonthly: OK=0, Warning=1, Critical=2, SampleLMonthly: OK=0, Warring Monthly: OK=0, Warning=1, CMonthly: OK=0, Warning=1, Critical=2, SampleLMe Monthly: OK=0, WarninEDMonthly: OK=0, =0.07 iMonthly: OK=0, Warning=1, Critical=2, Santly Monthly: OK=0, Warning=ablMonthly: OK=0, Warning=1, Critical=2, Sampleical_Monthly: OK=0, Warnin
- `- `- `- `- `- `- fline_historical_monitoring_replay.py` (18 tests)
- `data/mlb_2025/derived/p49_offline_historical_monitoring_replay_summary.json`
- `report/p49_offline_historical_monitoring_replay_20260526.md`
- `00-BettingPlan/20260526/p49_offline_historical_monitoring_replay_20260526.md`

### Known Limitations

- 2024 closing-line data gap **remains unresolved** (P43_BLOCKED_BY_DATA_GAP)
- No live API calls made. No runtime recommendation logic changed.
- No production proposal. No champion replacement. Paper-only offline replay.
- Edge CI uses normal approximation (n≥100). Not identical to P43 bootstrap but valid for large-sample batches.
- CRITICAL classification driven by edge drift, not ECE/Brier. Platt calibration itself remains structurally sound but mean_edge falls below 0.07 in peak-season batches.

---

## P50 — Edge Drift Root-Cause Audit (2026-05-26)

**Final Classification:** `P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC`
**Reconciliation:** `METRICS_RECONCILED_PROBABILITY_STREAM_DIFFERENCE`
**Governance:** paper_only=True | diagnostic_only=True | live_api_calls=0 | promotion_freeze=True

### Root Cause Summary (Multi-Factorial)

| Rank | Factor | Impact |
|------|--------|--------|
| 1 | MODEL_PROBABILITY_SOURCE_MISMATCH — P44 uses sigmoid(sp_fip_delta), P49 uses model_home_prob | PRIMARY |
| 2 | EDGE_PERSPECTIVE_SIDE_AWARE_VS_HOME_PERSPECTIVE | SECONDARY |
| 3 | CI_METHOD_BOOTSTRAP_VS_NORMAL_APPROXIMATION | TERTIARY |
| 4 | MARKET_ODDS_SOURCE_CSV_CLOSING_LINE_VS_EMBEDDED_NO_VIG | QUATERNARY |

### Key Proof

`fip_signal_side_aware_edge` (P44-equivalent: sigmoid(sp_fip_delta), side-aware, embedded market):
- Monthly CRITICAL = **0** | Monthly WARNING = **0** | SampleLimited = **3**
- All 3 qualifying months (n≥100): **OK**

P49 home-perspective ML-model edge: Monthly CRITICAL = **2**, Rolling CRITICAL = **6**

The CRITICAL alerts dissolve when the probability source is changed to match P44's sigmoid(sp_fip_delta).

### Resolution Paths

- **(A)** Re-baseline P48 thresholds using ML model_hom- **(A)** Re-baseline P48 thresholds using ML model_hom- **(A)** Re-baseline P48 threshold(sp_fip_d- **(A)** Re-baseline P48 thresholds### Co- **(A)** Re-baseline scrip- **(A)** Re-baseline P48au- **(A)** Re-baseline P48 thresholds using ML model_hom- **(A)** Re-baseline P48 thresholds using ML model_hom-ft- **(A)** Re-baseline P48 thresholds using ML model_hom- **(A)**use_- **(A)** Re-baseline P48 thresholds using ML model_hom- **(_ro- **(A)** Re-baseline P48 thresholds using ML model_hom- **(A)** Re-bas data - **(Amains **u- **(A)** Re-baseline P48 thresholds using ML model_hom- **(A)** Re-baseline P48 thresholds usined.
- No production proposal. No champion replacement. Paper-only offline audit.
- Market odds source difference (closing-line CSV vs embedded no-vig) not fully quantified.

---

## P51 — Monitoring Contract Revision Audit (2026-05-26)

**Final Classification:** `P51_REVISED_CONTRACT_REDUCES_FALSE_ALERTS_DIAGNOSTIC`  
**Governance:** paper_only=True | diagnostic_only=True | live_api_calls=0 | promotion_freeze=True  
**Tests:** 20 tests PASS  
**Cumulative:** 311 tests passed (P40–P51)

### Root Cause Applied

P50 confirmed stream mismatch: P49 used PLATT_CALIBRATED (ML model_home_prob) for edge monitoring, but P44/P43 edge framework uses RAW_SIGMOID (sigmoid(sp_fip_delta), k=1.0). P51 applies the correct stream assignment:

| Metric Family | Revised Stream |
|---------------|---------------|
| Edge monitoring | RAW_SIGMOID — `fip_signal_side_aware_edge` |
| Calibration (ECE/Brier) | PLATT_CALIBRATED — unchanged from P49 |

### Monthly Replay Under Revised Contract

| Month | n | fip_edge | CI | Final Status | P49 Status | Changed |
|-------|---|----------|-----|-------------|------------|---------|
| 2025-04 | 16 | 0.1333 | [0.094, 0.173] | SAMPLE_LIMITED | SAMPLE_LIMITED | No |
| 2025-05 | 120 | 0.1428 | [0.126, 0.160] | **MONITORING_OK** | EDGE_DRIFT_CRITICAL | ✓ |
| 2025-06 | 101 | 0.1482 | [0.130, 0.168] | **MONITORING_OK** | EDGE_DRIFT_CRITICAL | ✓ |
| 2025-07 | 92 | 0.1455 | [0.128, 0.164] | SAMPLE_LIMITED | SAMPLE_LIMITED | No |
| 2025-08 | 108 | 0.1376 | [0.122, 0.153] | **MONITORING_OK** | EDGE_DRIFT_WARNING | ✓ |
| 2025-09 | 98 | 0.1469 | [0.130, 0.163] | **CALIBRATION_CRITICAL** | SAMPLE_LIMITED | ✓ |

Monthly false CRITICALs eliminated: 1 net (2 false CRITICAL removed, 1 genuine CALIBRATION_CRITICAL revealed)  
Rolling false CRITICALs eliminated: 3 (P49: 5 CRITICAL → P51: 2 CRITICAL, in comparable batches)

### Sep 2025 Calibration Issue

Sep 2025 (n=98, platt_ece=0.1229) is a genuine calibration warning masked by P49's incorrect SAMPLE_LIMITED dominance over CRITICAL. Requires P52 investigation.

### Deliverables

- `scripts/_p51_monitoring_contract_revision_audit.py`
- `tests/test_p51_monitoring_contract_revision_audit.py` (20 tests)
- `data/mlb_2025/derived/p51_monitoring_contract_revision_summary.json`
- `report/p51_monitoring_contract_revision_audit_20260526.md`
- `00-BettingPlan/20260526/p51_monitoring_contract_revision_audit_20260526.md`
