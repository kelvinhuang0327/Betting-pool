# Active Task — P84H Corrected 2026 Prediction-Only Signal Validation + Coverage Guard

> **[P0 Active — Issued by CEO 2026-05-27 Asia/Taipei]**
> **Predecessor**: P84G committed at `021a8a8` (`P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED`)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
> **CEO Decision reference**: `00-Plan/roadmap/CEO-Decision.md` (2026-05-27, `CEO_DECISION_PARTIALLY_APPROVED`)
> **Roadmap reference**: `00-Plan/roadmap/roadmap.md` Section 0H
>
> **Required final classification (one of five)**:
> - `P84H_CORRECTED_SIGNAL_VALIDATED_DIAGNOSTIC_ONLY`
> - `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED`
> - `P84H_CALIBRATION_WEAK_REQUIRES_REVIEW`
> - `P84H_COVERAGE_TOO_LOW_FOR_SIGNAL_CLAIM`
> - `P84H_FAILED_VALIDATION`

---

## 任務名稱

P84H — Corrected 2026 Prediction-Only Signal Validation + Coverage Guard

## 背景

P84F 確認 `predicted_side` 在 P83E 中與 FIP 訊號方向反轉（`P84F_SIDE_MAPPING_INVERTED`）。
P84G 修正 P83E `compute_predicted_side()`，使其遵循 FIP lower-is-better 慣例：
- `sp_fip_delta = home_sp_fip - away_sp_fip`
- `delta > 0 → away`（home pitcher 較差）
- `delta < 0 → home`
並重新產生 P83E canonical rows / P84E outcome-attached rows / P84F diagnostic summary。

P84G commit `021a8a8`、classification `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED`。

修正後 metrics（partial coverage）：
- canonical rows = 828（schedule 2430，coverage 34.07%）
- outcome-available rows = 808
- hit_rate = `0.569307`
- AUC = `0.594315`
- Brier = `0.249408`
- ECE = `0.069682`
- primary_125 hit_rate = `0.602851`
- shadow_100 hit_rate = `0.595149`
- Tier B hit_rate = `0.563830`
- P84F post-fix classification = `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK`

但這些 metrics 仍是 March–May 2026 partial sample，**不足以宣告 full-season 或 production 訊號**。

## 目標

驗證 P84G 修正後的 2026 prediction-only signal，在 coverage / monthly / chronological / side / rule-subset / calibration 各切面下是否穩定、可作為 diagnostic-only tracking signal。

明確輸出五分類之一的 final classification（見上）。

## 允許修改範圍

僅允許新增或修改以下檔案：

- `scripts/_p84h_corrected_signal_validation_coverage_guard.py`（新增）
- `tests/test_p84h_corrected_signal_validation_coverage_guard.py`（新增）
- `data/mlb_2026/derived/p84h_corrected_signal_validation_coverage_guard_summary.json`（新增）
- `report/p84h_corrected_signal_validation_coverage_guard_20260527.md`（新增）
- `00-Plan/roadmap/active_task.md`（任務完成後更新狀態欄）
- Optional: `00-BettingPlan/20260527/p84h_corrected_signal_validation_coverage_guard_20260527.md`（新增）

## 禁止修改範圍（嚴格）

- `.env` 與任何 secrets 檔
- 任何 odds 檔案 / 任何 paid odds CSV
- `scripts/_p83e_2026_canonical_prediction_row_producer.py`（P83E mapping 已凍結）
- `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl`（canonical rows 凍結）
- `data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl`（outcome rows 凍結）
- 任何 runtime recommendation logic / champion strategy 檔
- 任何 production / registry / live API 設定
- TSL crawler 與相關 schedule
- `data/learning_state.json` / `data/tsl_*` / `data/.live_cache/*`（runtime dirty 不准 stage）
- 任何 EV / CLV / Kelly / market-edge / production_ready 旗標變更
- CTO-Analysis.md（CEO 已寫，本任務不再動）

## 必做內容

1. **Artifact consistency check**
   - 驗證 P84G summary、P83E summary、P84E summary、P84F summary 皆存在且 classification 與 CEO 背景一致；任一缺失或 mismatch 立即 STOP 並回報。
   - 驗證 P83E canonical rows = 828、P84E outcome-available rows = 808。

2. **Recomputed metrics from outcome-attached rows**
   - 從 `p84e_2026_outcome_attached_prediction_rows.jsonl` 重新計算 all-row hit_rate / AUC / Brier / ECE。
   - 與 `p84e_2026_outcome_attachment_summary.json` 中既有 metrics 在 tolerance 內比對；若超過 tolerance（建議 1e-4）則 STOP 並回報 `P84H_FAILED_VALIDATION`（artifact 不一致）。

3. **Split metrics**（必做，且須報告 n、hit_rate、AUC、Brier、ECE）：
   - **Monthly split**：依比賽日期分月（至少 2026-03, 2026-04, 2026-05）
   - **Chronological thirds split**：依比賽日期排序後均分三段
   - **Side split**：predicted_side=home vs predicted_side=away
   - **Rule subset split**：primary_125, shadow_100, Tier B

4. **Calibration analysis**
   - 重算 reliability curve（建議 10 bins，依 sample 量可彈性 5–10 bins）
   - 標出 ECE、bin-wise mean predicted prob vs empirical hit rate
   - 評估 P84F post-fix `CALIBRATION_WEAK` 是否來自：sample size、coverage bias、side bias、score transformation（純診斷，**禁止做 Platt/isotonic refit**）

5. **Coverage classification**
   - canonical_coverage_ratio = canonical_rows / schedule_rows
   - outcome_coverage_ratio = outcome_available_rows / canonical_rows
   - 明確分類：`COVERAGE_SUFFICIENT_FOR_DIAGNOSTIC` / `COVERAGE_LIMITED` / `COVERAGE_TOO_LOW`
   - 紀錄 coverage 偏差來源（probable pitcher availability 為主）

6. **Subset 比較**
   - primary_125 vs shadow_100 vs Tier B 的 hit_rate / AUC / Brier 對照表
   - 標註是否 primary_125 顯著優於 baseline（用 binomial test 或 bootstrap CI，無 odds，僅針對命中率本身）

7. **Final classification（必須是五分類之一）**：
   - `P84H_CORRECTED_SIGNAL_VALIDATED_DIAGNOSTIC_ONLY`
   - `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED`
   - `P84H_CALIBRATION_WEAK_REQUIRES_REVIEW`
   - `P84H_COVERAGE_TOO_LOW_FOR_SIGNAL_CLAIM`
   - `P84H_FAILED_VALIDATION`

8. **Governance scan**（測試與報告中必含）：
   - `odds_used=false`、`ev_computed=false`、`clv_computed=false`、`kelly_computed=false`
   - `production_ready=false`、`paper_only=true`、`diagnostic_only=true`
   - 未呼叫任何 live / paid API（`live_api_calls=0`、`paid_api_called=false`）
   - 未修改 canonical / outcome rows、未修改 P83E mapping、未替換 champion

9. **Tests**
   - `tests/test_p84h_corrected_signal_validation_coverage_guard.py` 至少涵蓋：
     - artifact consistency 檢查（含 STOP 條件）
     - recomputed metrics vs P84E summary tolerance
     - 每個 split 都至少有一個 hit_rate / AUC bound assertion
     - coverage classification 邊界
     - final classification 為五分類之一
     - governance flags 全部 false / true 正確
   - 全部 PASS。

10. **Anti-drift 強制條款（CEO 規則）**
    - 本任務**不得**衍生「P84I / P84J / P85+ monitoring meta-layer」task。
    - **不得**在報告或 summary 中建議或執行 Platt / isotonic / score-transform calibration refit。
    - **不得**輸出任何 odds-implied probability、EV、CLV、Kelly、stake-sizing、champion replacement、recommended bet。
    - 若 classification 為 `COVERAGE_TOO_LOW_FOR_SIGNAL_CLAIM` 或 `FAILED_VALIDATION`，必須誠實寫入；禁止為了避免該結論而額外推導新 phase。

## 驗收標準

- `scripts/_p84h_corrected_signal_validation_coverage_guard.py` 可獨立執行，產出 JSON summary 與 report。
- `data/mlb_2026/derived/p84h_corrected_signal_validation_coverage_guard_summary.json` 包含：recomputed metrics、split metrics（monthly / thirds / side / rule subset）、calibration metrics、coverage classification、final classification、governance flags。
- `report/p84h_corrected_signal_validation_coverage_guard_20260527.md` 用人類可讀格式呈現上述內容並明確標記 `diagnostic_only=true, production_ready=false`。
- `tests/test_p84h_corrected_signal_validation_coverage_guard.py` 全部 PASS。
- P83A–P84H 目標回歸全部 PASS（容許 skipped）。
- 未修改 canonical prediction rows / outcome-attached rows / P83E mapping / champion / runtime recommendation。
- 未做任何 odds / EV / CLV / Kelly 計算。
- 未呼叫 live / paid API。
- 無 secret / `.env` 讀寫。
- commit 為 whitelist-only：僅允許上述「允許修改範圍」列出之檔案。
- 報告明確標註：partial 2026 coverage（828/2430）、March–May only、no full-season claim、no production claim。

## 測試指令

```bash
# 任務專屬測試
./.venv/bin/pytest tests/test_p84h_corrected_signal_validation_coverage_guard.py -v

# 目標回歸（P83A–P84H）
./.venv/bin/pytest \
  tests/test_p83a_*.py tests/test_p83b_*.py tests/test_p83c_*.py tests/test_p83d_*.py tests/test_p83e_*.py \
  tests/test_p84a_*.py tests/test_p84b_*.py tests/test_p84c_*.py tests/test_p84d_*.py tests/test_p84e_*.py \
  tests/test_p84f_*.py tests/test_p84g_*.py tests/test_p84h_*.py -q
```

## 輸出報告位置

- `data/mlb_2026/derived/p84h_corrected_signal_validation_coverage_guard_summary.json`
- `report/p84h_corrected_signal_validation_coverage_guard_20260527.md`
- Optional：`00-BettingPlan/20260527/p84h_corrected_signal_validation_coverage_guard_20260527.md`

## Final Classification（任務完成時填寫）

五擇一：
- `P84H_CORRECTED_SIGNAL_VALIDATED_DIAGNOSTIC_ONLY`
- `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED`
- `P84H_CALIBRATION_WEAK_REQUIRES_REVIEW`
- `P84H_COVERAGE_TOO_LOW_FOR_SIGNAL_CLAIM`
- `P84H_FAILED_VALIDATION`

---

<!-- Prior phase completion markers (required by regression tests) -->
<!-- P47: P47_PLATT_SELECTED_FOR_MONITORING_DIAGNOSTIC -->
<!-- P48: P48_MONITORING_CONTRACT_READY_DIAGNOSTIC -->
<!-- P49: P49_MONITORING_REPLAY_CRITICAL_DIAGNOSTIC -->
<!-- P50: P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC -->
<!-- P52: P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC -->
<!-- P53: SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC -->
<!-- P54: P54_NO_FEATURE_DRIFT_FOUND_DIAGNOSTIC -->
<!-- P55: P55_INCONCLUSIVE_SAMPLE_LIMITED -->
<!-- P56: P56_BAND_ANNOTATION_POLICY_READY_DIAGNOSTIC -->
<!-- P57: P57_ANNOTATION_INTEGRATION_READY_DIAGNOSTIC -->
<!-- P58: P58_MONTHLY_REPORT_TEMPLATE_READY_DIAGNOSTIC -->
<!-- P61: P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT -->
<!-- P62: P62_CONTRACT_DRAFT_READY_FOR_CEO_REVIEW -->
<!-- P64: P64_PAPER_SIMULATION_FIRST_RUN_READY -->
<!-- P65: P65_EDGE_STABLE_NEGATIVE -->
<!-- P66: P66_ODDS_MAPPING_INTEGRITY_CONFIRMED -->
<!-- P67: P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW -->
<!-- P68: P68_ODDSPORTAL_BLOCKED_BY_TOS -->
<!-- P69: P69_CEO_DECISION_MEMO_READY -->
<!-- P70: P70_PATH_A_AUTHORIZED_AWAITING_API_KEY -->
<!-- P71: P71_PATH_A_STILL_AWAITING_API_KEY -->
<!-- P72A: P72A_ODDS_FREE_STRATEGY_ACCURACY_BACKTEST_READY -->
<!-- P72B: P72B_OBJECTIVE_METRIC_CONTRACT_READY -->
<!-- P73: P73_TIER_STABILITY_AND_SAMPLE_EXPANSION_READY -->
<!-- P74: P74_TIER_C_HOME_AWAY_BIAS_CORRECTION_READY -->
<!-- P75A: P75A_TIER_C_CORRECTED_RULE_VALIDATOR_READY -->
<!-- P77: P77_PREDICTION_ONLY_SHADOW_TRACKER_CONTRACT_READY -->
<!-- P78: P78_MONTHLY_SHADOW_TRACKER_REPORT_TEMPLATE_READY -->
<!-- P79A: P79A_TIER_B_TRIGGER_READINESS_CONTRACT_READY -->
<!-- P79B: P79B_TIER_B_VS_TIER_C_COMPARISON_HARNESS_READY -->
<!-- P80: P80_MARKET_EDGE_REENTRY_READINESS_CONTRACT_READY -->
<!-- P81: P81_LEGAL_ODDS_DATASET_VALIDATOR_CONTRACT_READY -->
<!-- P82: P82B_RAW_PAID_DATA_POLICY_READY / P82C_STAGING_GUARD_DRYRUN_READY -->
<!-- P82B: P82B_RAW_PAID_DATA_POLICY_READY -->
<!-- P82C: P82C_STAGING_GUARD_DRYRUN_READY -->
<!-- P83A: P83A_AWAITING_2026_DATA -->
<!-- P83C: P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA -->
<!-- P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA confirmed -->
<!-- P83E: P83E_CANONICAL_ROWS_READY -->
<!-- P84A: P84A_UPSTREAM_COLLECTOR_CONTRACT_READY -->
<!-- P84B: P84B_SCHEDULE_READY_PITCHER_MODEL_BLOCKED -->
<!-- P84C: P84C_PARTIAL_SNAPSHOT_READY_OUTCOMES_PENDING -->
<!-- P84D: P84D_PITCHER_COVERAGE_AUDIT_READY_NO_BACKFILL -->
<!-- P84E: P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS -->
<!-- P84F: P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK (post-P84G rerun) -->
<!-- P84G: P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED -->
<!-- P84H: (pending — to be set on completion) -->


## P84H — Corrected 2026 Signal Validation + Coverage Guard
- **Status**: COMPLETE
- **Classification**: `P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED`
- **Date**: 2026-05-27
- **Script**: scripts/_p84h_corrected_signal_validation_coverage_guard.py
- **Summary**: data/mlb_2026/derived/p84h_corrected_signal_validation_coverage_guard_summary.json
- **Report**: report/p84h_corrected_signal_validation_coverage_guard_20260527.md
- **Governance**: paper_only=True, diagnostic_only=True, production_ready=False

## P85 — Prediction Convention Invariant Gate
- **Status**: COMPLETED
- **Classification**: `P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY`
- **Generated**: 2026-05-27T07:20:29.172331+00:00
- **Invariants checked**: 9 steps (FIP+/-, zero-delta policy, prob semantics, actual_winner derivation, is_correct consistency, AUC/hit_rate guard, governance)
- **Violations**: 0
- **Note**: Paper-only diagnostic gate. Not a production recommendation.
