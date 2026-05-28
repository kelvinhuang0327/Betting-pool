# Active Task — P99 Wait-State Coverage Snapshot

> **[P0 Active — Issued by CEO 2026-05-28 Asia/Taipei]**
> **Predecessor**: P98 committed at `61063ba` (`P98_WAIT_ACCUMULATE_COVERAGE_UNCHANGED`)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
> **CEO Decision reference**: `00-Plan/roadmap/CEO-Decision.md` (2026-05-28, `CEO_DECISION_PARTIALLY_APPROVED`)
> **Roadmap reference**: `00-Plan/roadmap/roadmap.md` Section 0K

## Current Task
P99 — COMPLETED（2026-05-28）

## Final Classification
✅ `P99_WAIT_STATE_CONFIRMED_NO_RERUN`

**rationale**: No material change since P98 (delta_outcome_rows=0, delta_canonical_rows=0). schedule_coverage_pct=34.0741% (threshold: 60%). observed_months=3 (threshold: 4). Coverage unchanged — wait-state confirmed. Ingestion readiness: READY_FOR_FUTURE_OUTCOME_APPEND. All 5 recheck thresholds: WAIT. p96_rerun_ready=False.

## Blocker Summary (Primary: DATA_COVERAGE_BLOCKER)
- `DATA_COVERAGE_BLOCKER` — 34.07% coverage, 3 months only (need >=60%, >=4 months) → WAIT
- `ingestion_readiness=READY_FOR_FUTURE_OUTCOME_APPEND` — schema and governance checks pass for future appends
- delta_canonical_rows=0, delta_outcome_rows=0, delta_high_fip_rows=0 (no new data since P98)
- Recheck trigger: rerun P99 when new 2026 outcomes arrive; rerun P96 only when coverage>=60% AND months>=4

## Committed Artifacts
- `scripts/_p99_wait_state_coverage_snapshot.py`
- `tests/test_p99_wait_state_coverage_snapshot.py` (20/20 PASSED)
- `data/mlb_2026/derived/p99_wait_state_coverage_snapshot_summary.json`
- `report/p99_wait_state_coverage_snapshot_20260528.md`

---

## Previous Task
P98 — COMPLETED（2026-05-28）

## Final Classification (P98)
✅ `P98_WAIT_ACCUMULATE_COVERAGE_UNCHANGED`

**rationale**: No new rows since P97 baseline (delta_outcome_rows=0). schedule_coverage_pct=34.0741% (threshold: 60.0%). observed_months=3 (threshold: 4). Coverage unchanged — system must remain in wait/accumulate mode. No P96/P97 rerun justified. All 5 recheck thresholds: WAIT. p96_rerun_ready=False.

## Committed Artifacts (P98)
- `scripts/_p98_data_coverage_accumulation_gate.py`
- `tests/test_p98_data_coverage_accumulation_gate.py` (20/20 PASSED)
- `data/mlb_2026/derived/p98_data_coverage_accumulation_gate_summary.json`
- `report/p98_data_coverage_accumulation_gate_20260528.md`

---

## Previous Task
P97 — COMPLETED（2026-05-28）

## Final Classification (P97)
✅ `P97_HIGH_FIP_PREFLIGHT_SIGNAL_PASS_PRODUCTION_BLOCKED`

**rationale**: Signal gate PASS (P94/P95/P96 all stable, HIGH_FIP hit_rate=0.641115). Segment gate PASS (HIGH_FIP diagnostic-only, MID/LOW watch-only). Production BLOCKED by 8 failing gates: calibration_gate, coverage_gate, market_edge_gate, odds_dataset_gate, production_governance_gate, recommendation_contract_gate, risk_control_gate, season_span_gate. readiness_ratio=0.2000 (2/10). No production promotion. No EV/CLV/Kelly/recommendation/odds.

## Committed Artifacts (P97)
- `scripts/_p97_high_fip_production_gate_preflight.py`
- `tests/test_p97_high_fip_production_gate_preflight.py` (20/20 PASSED)
- `data/mlb_2026/derived/p97_high_fip_production_gate_preflight_summary.json`
- `report/p97_high_fip_production_gate_preflight_20260528.md`

---

## Previous Task
P96 — COMPLETED（2026-05-28）

## Final Classification (P96)
✅ `P96_HIGH_FIP_DRIFT_MONITOR_STABLE_COVERAGE_LIMITED`

**rationale**: All tolerance checks passed（high/mid/low FIP segment metrics match P93/P94 within 1e-4）. Partial coverage 828/2430=34.07% (March–May only) → READY_WITH_LIMITED_COVERAGE. High-FIP diagnostic tracking allowed; mid/low FIP watch-only. No EV/CLV/Kelly/recommendation/production.

---

## 任務名稱

P94 — High-FIP Subset Diagnostic / FIP-Stratified Tracking Gate

## 背景

P91 確認 prediction-only tracking 訊號穩定（828 rows，808 outcome，hit_rate `0.569307`，AUC `0.594315`）。
P92 排除簡單 side baseline 解釋（model `0.569307` vs home `0.524752` vs away `0.475248`，predicted_home_ratio `0.509901`）。
P93 進一步證實：**aggregate 56.9% 訊號主要由 high `|abs_sp_fip_delta|` 子集驅動**：

- **High bucket (|delta|≥1.5)**：n=287，hit_rate `0.641115`，model_vs_home_delta `+0.114983`
- **Mid bucket (0.5≤|delta|<1.5)**：n=343，hit_rate `0.530612`，model_vs_home_delta `−0.008746`
- **Low bucket (|delta|<0.5)**：n=178，hit_rate `0.528090`，model_vs_home_delta `+0.033708`
- **Q4 quartile**（|delta| 1.85–7.17）：n=202，hit_rate `0.658416`
- **Monthly high-FIP**：Mar `0.7353` (n=34)、Apr `0.6014` (n=143)、May `0.6636` (n=110)
- **Monthly low-FIP April collapse**：`0.4868` (n=76)
- P93 final classification: `P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP`，rationale `High-FIP hit_rate exceeds low-FIP by 0.1130 > threshold 0.08; Q4 dominates`。

下一步必須：(a) 嚴格驗證 high-FIP 子集 stability（bootstrap CI、temporal split、side split）；(b) 明確 low/mid-FIP 是否須排除或 watch-only；(c) 在 partial 2026 coverage（828/2430）與 March–May only 範圍內，給出五分類 GO/NO-GO classification。

**不得**做：calibration refit、market-edge claim、Taiwan 運彩 paper recommendation、champion replacement、Kelly/EV/CLV 計算、production_ready 提升。

## 目標

驗證 P93 發現的 high-FIP 子集（n=287，hit_rate `0.641115`）在 stability / temporal / side / sample-sufficiency / segment-qualification 各切面是否足以作為 diagnostic-only tracking signal；明確輸出五分類之一的 final classification。

---

## 第一階段：Pre-Flight Gates（必須在實作前通過，否則 STOP）

### Gate 1 — Canonical Agent Entry
- `pwd` 必須含 `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`（不得是 `.claude/worktrees/*`、`claude/*`、`codex/*`、`.git/worktrees/*`）
- `git rev-parse --show-toplevel` 必須 = `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- `git branch --show-current` 必須 = `main`
- `git rev-parse --git-dir` 必須 = `.git`（不得是 `.git/worktrees/*`）
- HEAD 必須 = `2221f0f`（P93）
- 任一不符 → STOP，不進入實作。

### Gate 2 — Dirty-Tree Inventory（CEO Dirty-Tree Policy 第 4 節）
- 紀錄 `git status --short` 全量到 P94 summary 的 `step1_preflight.dirty_tree_inventory`。
- **不修改、不 stage、不 commit** 任何下列 8 類檔案：
  - A. Roadmap governance（CEO 已動，本任務不可動）
  - B. Runtime / live state（`data/.live_cache/*`、`data/tsl_*`、`data/learning_state.json`、`data/derived/tsl_*`、`data/mlb_context/*`、`logs/daemon_*`、`data/wbc_backend/*`）
  - C. P50–P82 derived artifacts（`data/mlb_2025/derived/p63_*`、`p77_*`、`p81_*`、`p82b_*`、`outputs/predictions/PAPER/*`）
  - D. P84–P86 derived summaries（`data/mlb_2026/derived/p84[c-h]_*`、`p85_*`、`p86_*`）— P94 read-only
  - E. 舊 phase plan reports（`00-BettingPlan/20260510/*`、`20260526/*`）
  - F. 舊診斷 markdown（`docs/orchestration/phase28_*`）
  - G. Untracked repo-root probe scripts（`_p50_extract.py`、`_p50_extract3.py`、`_p51_probe3.py`、`scripts/_p30b_analysis.py`）— quarantine，不 import、不執行、不 stage
  - H. Untracked 舊 phase report（`report/p30b_feature_candidate_summary_20260524.md`、`docs/orchestration/phase28_*_2026-05-{24,25,27}.md`）

### Gate 3 — Upstream Artifact Consistency（read-only）
- 驗證以下檔案存在且 final_classification 正確：
  - `data/mlb_2026/derived/p93_prediction_only_coverage_feature_bias_audit_summary.json` → `P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP`
  - `data/mlb_2026/derived/p91_prediction_only_tracking_gate_summary.json` → `P91_TRACKING_ACTIVE_SIGNAL_STABLE`
  - `data/mlb_2026/derived/p92_prediction_only_side_bias_baseline_gate_summary.json` → `P92_SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE`
  - `data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl` 與 `p84e_2026_outcome_attachment_summary.json`
- 任一缺失或 mismatch → STOP，回報 `P94_FAILED_VALIDATION`。

---

## 第二階段：必做分析內容

### 1. Row inventory（從 `p84e_2026_outcome_attached_prediction_rows.jsonl` 重讀）
- 計算 outcome-available rows（預期 808）、有 `sp_fip_delta` 的 rows（預期 808）。
- 與 P93 step3 對齊，tolerance 1e-9。

### 2. High-FIP subset 重算（**主要分析**）
- 子集定義：`abs(sp_fip_delta) >= 1.5`（保持與 P93 一致）。
- 計算：n、hit_rate、AUC（若可）、Brier、ECE、predicted_home_ratio、actual_home_ratio。
- 與 P93 step6 high_bucket metrics 在 tolerance 1e-4 內比對，否則 STOP。

### 3. High-FIP stability tests
- **Bootstrap 95% CI** for high-FIP hit_rate（≥1000 resamples，固定 seed）。
  - 報告 `(ci_low, ci_high)`，並標註 baseline（home prior = `0.524752`，aggregate model = `0.569307`）。
  - **判定 stability**：若 `ci_low > 0.55` 視為 strong stability；`0.50 < ci_low ≤ 0.55` 視為 marginal；`ci_low ≤ 0.50` 視為 unstable。
- **Temporal split within high-FIP**：依比賽日期排序均分三段（thirds），分別計算 hit_rate / n。
  - 判定：三 third hit_rate 全部 > `0.55` 視為 temporal stable；否則 unstable。
- **Side split within high-FIP**：predicted_side = home vs away 分別計算 n、hit_rate。
  - 判定：兩側 hit_rate 差距 < 0.10 視為 side-balanced；否則 side-biased。

### 4. Mid-FIP / Low-FIP segment qualification
- 重算 mid bucket (0.5 ≤ |delta| < 1.5) 與 low bucket (|delta| < 0.5) 的 hit_rate、Brier、ECE。
- 對每個 bucket：以 binomial test 對 home_baseline 做檢定，回報 p-value（無需 odds）。
- **明確判定**：
  - mid_bucket 是否 ≥ home_baseline + 0.03（degree of confidence）
  - low_bucket 是否 ≥ home_baseline + 0.03
  - 若皆 NO → segment qualification = `LOW_MID_FIP_NOT_TRACKABLE`
  - 若任一 YES → segment qualification = `LOW_MID_FIP_PARTIALLY_TRACKABLE`

### 5. Sample sufficiency
- 高 FIP n=287 在 monthly 切面：Mar n=34、Apr n=143、May n=110。
- 判定：若任一 month n < 30 → 標 `MONTHLY_SAMPLE_LIMITED`（即便 Mar 34 邊際足夠，仍須註記三個月加總是季初樣本）。
- 計算 partial coverage indicator：`canonical_rows / schedule_rows = 828 / 2430 = 0.3407`，明確寫入 summary。

### 6. Final five-class classification（必填）
依 stability + segment + sample 三向度決定：

| 條件 | classification |
|---|---|
| Bootstrap `ci_low > 0.55` AND temporal stable AND side-balanced AND mid/low qualification 明確 | `P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY` |
| Bootstrap `0.50 < ci_low ≤ 0.55` OR temporal one third < `0.55` OR sample 邊際足夠但 monthly_sample_limited | `P94_HIGH_FIP_PROMISING_BUT_SAMPLE_LIMITED` |
| Temporal 兩段以上 < `0.55` 或 side-biased > 0.10 | `P94_HIGH_FIP_UNSTABLE_REQUIRES_REVIEW` |
| Bootstrap `ci_low ≤ 0.50` 或 high-FIP hit_rate − home_baseline < 0.05 | `P94_HIGH_FIP_NOT_SEPARABLE_FROM_NOISE` |
| Upstream consistency 失敗 / artifact mismatch / metric recomputation tolerance 超界 | `P94_FAILED_VALIDATION` |

### 7. Governance scan（必含於 summary）
- `odds_used=false`、`ev_computed=false`、`clv_computed=false`、`kelly_computed=false`
- `production_ready=false`、`paper_only=true`、`diagnostic_only=true`
- 未呼叫任何 live / paid API（`live_api_calls=0`、`paid_api_called=false`）
- 未修改 canonical / outcome rows、未修改 P83E mapping、未替換 champion、未動 P84–P86 derived summaries
- 未 stage Dirty-Tree Policy A–H 類任何檔案

### 8. Tests（`tests/test_p94_high_fip_subset_diagnostic.py`）
- Pre-flight gates 三項全有 test
- Upstream artifact existence + final_classification 一致性
- Row inventory recount vs P93 tolerance
- High-FIP metrics recount vs P93 step6 tolerance
- Bootstrap CI 結果落在合理範圍
- Temporal / side split metrics 結構正確
- Segment qualification 邏輯正確（含 LOW_MID_FIP_NOT_TRACKABLE 與 PARTIALLY_TRACKABLE 兩條 path）
- Final classification 在五分類列表內
- Governance flags 全部正確

### 9. Anti-Drift Enforcement（CEO 強制條款，違者 task fail）
- **禁止**衍生 P94A / P94B / P95+ monitoring meta-layer。
- **禁止**執行或建議任何 Platt / isotonic / score-transform calibration refit。
- **禁止**輸出 odds-implied probability / EV / CLV / Kelly / stake-sizing / champion replacement / recommended bet / Taiwan 運彩建議。
- **禁止**走 P86–P90 式「contract → recovery → authorization → executor → closure」5-phase 拆解；P94 結束就是結束。
- **禁止** import / 執行 quarantine 類 untracked probe scripts（Gate 2 G 類）。
- 即使 final classification = `NOT_SEPARABLE_FROM_NOISE` 或 `FAILED_VALIDATION`，**禁止**為了補救而提議新 phase；誠實寫入結論。

---

## 允許修改範圍（嚴格白名單）

僅允許新增以下檔案：

- `scripts/_p94_high_fip_subset_diagnostic.py`
- `tests/test_p94_high_fip_subset_diagnostic.py`
- `data/mlb_2026/derived/p94_high_fip_subset_diagnostic_summary.json`
- `report/p94_high_fip_subset_diagnostic_20260528.md`
- `00-Plan/roadmap/active_task.md`（任務完成時更新「Current Task / Final Classification / Historical log」三段）
- Optional: `00-BettingPlan/20260528/p94_high_fip_subset_diagnostic_20260528.md`

## 禁止修改範圍

- `.env` 與任何 secrets
- 任何 odds 檔 / paid odds CSV
- `scripts/_p83e_2026_canonical_prediction_row_producer.py`（P83E mapping 凍結）
- `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl`（canonical rows 凍結）
- `data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl`（outcome rows 凍結）
- `data/mlb_2026/derived/p8[1-9]*`、`p9[0-3]*`（read-only，禁止覆蓋）
- `00-Plan/roadmap/CEO-Decision.md`（CEO 已寫）
- `00-Plan/roadmap/CTO-Analysis.md`（CTO 已寫）
- `00-Plan/roadmap/roadmap.md`（CTO 已寫）
- 任何 runtime recommendation / champion strategy 檔
- 任何 production / registry / live API 設定
- TSL crawler 與相關 schedule
- Dirty-Tree Policy A–H 類所有檔案（不 stage、不 commit）
- 任何 EV / CLV / Kelly / market-edge / production_ready 旗標變更

## 驗收標準

1. Pre-flight gates 全部通過（canonical entry + dirty-tree inventory recorded + upstream consistency）。
2. `scripts/_p94_high_fip_subset_diagnostic.py` 可獨立執行並產出 JSON summary + report。
3. `data/mlb_2026/derived/p94_high_fip_subset_diagnostic_summary.json` 包含：dirty_tree_inventory、row_inventory、high_fip_metrics、bootstrap_ci、temporal_split、side_split、mid_low_segment_qualification、sample_sufficiency、final_classification（五擇一）、governance flags。
4. `report/p94_high_fip_subset_diagnostic_20260528.md` 人類可讀，明確標：partial coverage（828/2430）、March–May only、diagnostic_only=true、production_ready=false、no odds、no EV/CLV/Kelly。
5. `tests/test_p94_high_fip_subset_diagnostic.py` 全部 PASS。
6. P83A–P94 targeted regression 全部 PASS（容許 skipped）。
7. `git status --short` 在 commit 後僅多出白名單檔；Dirty-Tree Policy A–H 類無新動。
8. Final classification 明確為五分類之一。

## 測試指令

```bash
# Pre-flight 自檢（先跑）
pwd
git rev-parse --show-toplevel
git branch --show-current
git rev-parse --git-dir
git log -1 --oneline

# P94 專屬測試
./.venv/bin/pytest tests/test_p94_high_fip_subset_diagnostic.py -v

# 目標回歸（P83A–P94）
./.venv/bin/pytest \
  tests/test_p83a_*.py tests/test_p83b_*.py tests/test_p83c_*.py tests/test_p83d_*.py tests/test_p83e_*.py \
  tests/test_p84a_*.py tests/test_p84b_*.py tests/test_p84c_*.py tests/test_p84d_*.py tests/test_p84e_*.py \
  tests/test_p84f_*.py tests/test_p84g_*.py tests/test_p84h_*.py \
  tests/test_p85_*.py tests/test_p86_*.py tests/test_p87_*.py tests/test_p88_*.py tests/test_p89_*.py \
  tests/test_p90_*.py tests/test_p91_*.py tests/test_p92_*.py tests/test_p93_*.py tests/test_p94_*.py -q
```

## 輸出報告位置

- `data/mlb_2026/derived/p94_high_fip_subset_diagnostic_summary.json`
- `report/p94_high_fip_subset_diagnostic_20260528.md`
- Optional：`00-BettingPlan/20260528/p94_high_fip_subset_diagnostic_20260528.md`

## Commit 規範

- 只允許白名單檔；單一 commit；message 格式：
  ```
  feat(P94): High-FIP Subset Diagnostic / FIP-Stratified Tracking Gate — <final_classification>
  ```
- **嚴禁** `git add -A` / `git add .`，僅允許明確列檔。
- 若 final classification ∈ {`UNSTABLE_REQUIRES_REVIEW`, `NOT_SEPARABLE_FROM_NOISE`, `FAILED_VALIDATION`}，仍須 commit 證據；禁止為了避免該結論而擴展 phase。

---

## Historical Classification Log

<!-- P82: P82 completed -->
<!-- P83A: P83A_LIVE_ACCUMULATION_FIRST_SNAPSHOT_READY -->
<!-- P83C: P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA -->
<!-- P83E: P83E_CANONICAL_ROWS_READY -->
<!-- P84A: P84A_UPSTREAM_COLLECTOR_CONTRACT_READY -->
<!-- P84B: P84B_SCHEDULE_READY_PITCHER_MODEL_BLOCKED -->
<!-- P84C: P84C_PARTIAL_SNAPSHOT_READY_OUTCOMES_PENDING -->
<!-- P84D: P84D_PITCHER_COVERAGE_AUDIT_READY_NO_BACKFILL -->
<!-- P84E: P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS -->
<!-- P84F: P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK (post-P84G rerun) -->
<!-- P84G: P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED -->
<!-- P84H: P84H_CORRECTED_SIGNAL_PROMISING_BUT_COVERAGE_LIMITED -->
<!-- P85: P85_PREDICTION_CONVENTION_INVARIANT_GATE_READY -->
<!-- P86: P86_ARTIFACT_REGENERATION_DEPENDENCY_CONTRACT_READY (recovered) -->
<!-- P87: P87_REGENERATION_REQUIRED_AWAITING_EXPLICIT_YES -->
<!-- P88: P88_AWAITING_EXPLICIT_REGENERATION_AUTHORIZATION -->
<!-- P89: P89_RECOVERY_COMPLETE_CONTRACT_RESTORED -->
<!-- P90: P90_POST_RECOVERY_CLOSURE_READY -->
<!-- P91: P91_TRACKING_ACTIVE_SIGNAL_STABLE -->
<!-- P92: P92_SIGNAL_NOT_EXPLAINED_BY_SIMPLE_SIDE_BASELINE -->
<!-- P93: P93_SIGNAL_CONCENTRATED_IN_HIGH_FIP -->
<!-- P94: P94_HIGH_FIP_QUALIFIED_DIAGNOSTIC_ONLY —— Bootstrap ci_low=0.582 (STRONG), temporal 3/3 > 0.55, side_balanced, monthly_limited=False -->
<!-- P95: P95_FIP_STRATIFIED_SHADOW_TRACKER_READY_WITH_LIMITED_COVERAGE —— HIGH_FIP diagnostic tracking allowed; mid/low watch-only; partial coverage 34.07% (March–May 2026) -->
