# P200 — Prediction Provenance and Selected-Side Hardening

- **日期 (Date):** 2026-06-11 (Asia/Taipei)
- **任務類型:** Implementation（Template 3，paper-only）
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` · **Branch:** `main`
- **HEAD:** `2a7aa134470dac578b5bedf08c40d80b94c56fea`（= origin/main，未提交）
- **依據:** P199 審計報告 `report/p199_paper_workflow_lineage_gap_audit_20260611.md`
- **Worker:** Opus 強 · Thinking 強

---

## 1. Phase 0 — Actual State Verification

| 檢查 | 觀察值 | 預期 | 結果 |
|------|--------|------|------|
| pwd / toplevel | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | 同 | ✅ |
| branch / symbolic HEAD | `main` / `main` | `main`，非 detached | ✅ |
| git-dir | `.git` | `.git` | ✅ |
| HEAD / origin/main | `2a7aa13…c56fea` / `2a7aa13…c56fea` | 相等 | ✅ |
| staged | (空) | 無 | ✅ |
| open PR | 0 | 0 | ✅ |
| P199 report | 存在 | 存在 | ✅ |
| dirty/untracked | tolerated runtime/data + 授權 CTO governance + P199 report | 子集 | ✅ |
| active_task.md | `AUTHORIZED_PLAN_ONLY`(P199, plan-only) | 無衝突的 implementation task | ✅ |

Phase 0 全數通過。`active_task.md` 僅授權 P199（plan-only，已完成）；本 P200 由 prompt 之 explicit authorization 授權（優先序第一），無衝突。STOP 條件均未觸發。

---

## 2. Files Inspected

- `scripts/run_mlb_tsl_paper_recommendation.py`（`build_recommendation`、`_estimate_moneyline_odds`、main）
- `wbc_backend/recommendation/recommendation_row.py`（schema — **不在白名單，未修改**）
- `orchestrator/mlb_paper_evaluator.py`（evaluator/leaderboard — **不在白名單，未修改**；僅讀取）
- `orchestrator/mlb_daily_scheduler.py`（`run_paper_recommendation_job` 共用同一 `build_recommendation`/`_pick_game`）
- 測試：`tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`, `tests/test_mlb_daily_scheduler.py`, `tests/test_p180_strategy_leaderboard.py`, `tests/test_mlb_paper_evaluator.py`, `tests/test_mlb_paper_evaluation_runner.py`, `tests/test_run_mlb_tsl_paper_recommendation_smoke.py`（smoke 非白名單，僅執行驗證）
- 既有 artifacts：`outputs/recommendations/PAPER/2026-05-11/*.jsonl`

---

## 3. Implementation Summary

**Schema 決策：** `recommendation_row.py` 不在白名單，故 P200 **不修改 row schema**，改以既有自由格式欄位 `source_trace: dict` 承載 provenance（P200 prompt 部分 A 明確允許此做法）。selected-side 直接使用 row 既有的 `tsl_side` 欄位（其 `Literal` 已含 `home`/`away`），無需 schema 變更。

**`scripts/run_mlb_tsl_paper_recommendation.py` 變更（共 6 處，全在白名單）：**

1. 新增純函式 `determine_selected_side(model_prob_home, model_prob_away=None) -> (side, method, reason)` — 以 argmax 選邊，`method` 恆為 `argmax_model_probability`，永不輸出 `hardcoded_home`。
2. 新增純函式 `classify_prediction_provenance(model_version, *, game_specific=False, prediction_source_id=None) -> dict` — 回傳 `prediction_input_mode` / `prediction_source` / `prediction_source_id` / `prediction_model_version` / `learning_eligible` / `learning_block_reason`。
3. 新增模組常數 `_VALID_PREDICTION_INPUT_MODES`、`_VALID_SELECTED_SIDE_METHODS`。
4. `build_recommendation`：於模型機率定案後計算 `provenance` 與 `selected_side`/`selected_prob`。
5. 將 provenance 八個欄位寫入 `source_trace`；賠率與 edge 改以**選定側** `selected_prob` 計算（`tsl_live` True/False 兩分支一致）。
6. row 建構由 `tsl_side="home"` 改為 `tsl_side=selected_side`。

CLI 與 daemon（`run_paper_recommendation_job`）共用同一 `build_recommendation`，故硬化在兩條路徑同時生效。

**未變更：** 模型訓練、特徵工程數值、`_estimate_moneyline_odds` 賠率估計邏輯、gate 門檻、Kelly/stake 政策、`paper_only` 與 `VALID_GATE_STATUSES` 不變量、evaluator/scheduler runtime 行為。

---

## 4. Provenance Fields Added（寫入 `source_trace`）

| 欄位 | 值域 / 範例 | 語意 |
|------|------------|------|
| `prediction_input_mode` | `game_specific` / `neutral_fixed_prior` / `unknown` | 預測輸入是否逐場 |
| `prediction_source` | `neutral_feature_fallback` / `fixed_prior_fallback` / `game_specific_features` / `unknown` | 預測來源分類 |
| `prediction_source_id` | 穩定識別碼或 `null` | 可用時的來源鍵 |
| `prediction_model_version` | 如 `v1-mlb-moneyline-trained` | 模型/契約版本 |
| `selected_side_method` | `argmax_model_probability`（恆）；永不 `hardcoded_home` | 選邊機制 |
| `selected_side_reason` | 如 `model_prob_home=0.5403 >= model_prob_away=0.4597` | 決定性說明 |
| `learning_eligible` | `true` 僅當逐場非 fallback | 是否可作學習證據 |
| `learning_block_reason` | `learning_eligible=false` 時必填 | 不可學習之原因 |

> 目前產線路徑恆為硬編碼中性特徵 → `prediction_input_mode=neutral_fixed_prior`、`learning_eligible=false`。`game_specific=True` 分支供未來逐場特徵路徑使用，已由測試覆蓋，現行路徑不會到達。

---

## 5. Selected-Side Behavior — Before / After

| | Before（P199 發現） | After（P200） |
|--|--------------------|---------------|
| 選邊 | `tsl_side="home"` 寫死（L395） | `tsl_side = argmax(model_prob_home, model_prob_away)` |
| 賠率 / edge 基準 | 一律以 `model_prob_home` | 以**選定側** `selected_prob` |
| 方法揭露 | 無 | `selected_side_method=argmax_model_probability`（+ reason） |
| `hardcoded_home` | 隱性存在 | 永不輸出 |
| 現行 FIXTURE（CLE，中性 prior 0.5403） | home | home（行為保留，回歸錨點） |
| 逐場 home_prob < 0.5 | 仍會錯選 home | 正確選 away（`determine_selected_side` 測試證實） |

---

## 6. Fallback Behavior — Before / After

| | Before | After |
|--|--------|-------|
| 中性特徵預測 | 靜默呈現，外觀如逐場 model edge | 明確標記 `prediction_input_mode=neutral_fixed_prior`、`learning_eligible=false`、`learning_block_reason` |
| `v1-mlb-moneyline-trained`（中性輸入） | 看似已訓練模型 | `prediction_source=neutral_feature_fallback`、不可學習 |
| `v1-home-prior-baseline`（0.535） | 看似預測 | `prediction_source=fixed_prior_fallback`、不可學習 |

未改變 fallback 是否「產生 row」的契約（仍寫出 row 供稽核）；P200 僅讓 row **誠實揭露**其為 fallback 且 `learning_eligible=false`。

---

## 7. Evaluator / Leaderboard Learning-Eligibility Behavior

- **範圍限制：** `orchestrator/mlb_paper_evaluator.py`（evaluator 原始碼）**不在 P200 白名單**，故未修改；evaluator 目前不讀取 `source_trace.learning_eligible`。
- **現行安全網（已足以避免過度宣稱）：** learning-ineligible 的中性 row 不帶 `strategy_id` → 歸入 `UNATTRIBUTED`；樣本 < `SMALL_SAMPLE_THRESHOLD(10)` → `data_limited=True`。兩者皆使其**無法**成為「可晉升（attributed 且非 data_limited）」的 leaderboard 項目。
- 新增測試（`tests/test_p180_strategy_leaderboard.py`）證明：帶 `learning_eligible=false` 的中性 row 經 `evaluate_paper_recommendations` 後 → `UNATTRIBUTED` + `data_limited`；且一批此類 row 不產生任何可晉升項目。
- **後續（out of P200 scope）：** 讓 evaluator 直接讀取 `learning_eligible` 並於 metrics 明確分類，需納入 evaluator 原始碼白名單，建議列為 P201。

---

## 8. Tests Run

新增 P200 測試共 **15** 個：
- `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`：+12（`TestP200SelectedSide` ×5、`TestP200Provenance` ×4、`TestP200RowProvenancePropagation` ×3）
- `tests/test_mlb_daily_scheduler.py`：+1（`test_27b_paper_recommendation_job_propagates_p200_provenance` — scheduler 傳遞驗證）
- `tests/test_p180_strategy_leaderboard.py`：+2（`TestP200LearningIneligibleRowsNotPromoted`）

| 指令 | 結果 |
|------|------|
| `pytest tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py -q` | **35 passed** |
| `pytest tests/test_mlb_daily_scheduler.py -q` | **46 passed** |
| `pytest tests/test_mlb_paper_evaluator.py tests/test_mlb_paper_evaluation_runner.py tests/test_p180_strategy_leaderboard.py -q` | **58 passed** |
| 合併工作流 5 檔 | **139 passed**（124 baseline + 15 新增） |
| `pytest tests/test_run_mlb_tsl_paper_recommendation_smoke.py -q`（白名單外，僅驗證未破壞） | **13 passed** |

合計 152 個相關測試通過，涵蓋被改檔的所有 importer。

---

## 9. Full Regression Status

**NOT RUN（全庫）。** 理由：變更僅限單一 script 的選邊/provenance 邏輯與三個測試檔；已對該 script 的**全部** importer（含白名單外 smoke 測試）做比例性回歸並全通過。全庫回歸對此窄範圍改動不成比例，且可能引入與本任務無關之既有失敗（記憶中曾記錄 `test_portfolio_metrics_are_hardened_when_tsl_feed_blocked` 等獨立 baseline），其屬白名單外、無法在 P200 範圍內處理。

---

## 10. Risks and Limitations

1. **賠率仍為 proxy。** P200 未引入 observed TSL odds，`edge_pct` 仍為以選定側機率推導之循環/結構性量（屬 P199 候選 B，受合法 provider 授權阻擋，刻意不在本任務）。
2. **目前無 `game_specific` 路徑。** 產線恆為 `neutral_fixed_prior`；`game_specific=True` 分支僅供未來逐場特徵接入並由測試覆蓋。引入真實逐場特徵屬後續任務。
3. **Evaluator 未強制 `learning_eligible`。** 受白名單限制，僅以既有 `UNATTRIBUTED`/`data_limited` 安全網防止過度宣稱；直接強制留待 P201。
4. **回歸錨點。** `test_row_side_is_consistent_with_argmax` 含 `tsl_side=="home"` 斷言，假設中性 prior 經 adapter 調整後仍 ≥ 0.5；若日後 adapter 行為使主隊機率 < 0.5，需更新該錨點（argmax 一致性主斷言仍正確）。

---

## 11. Required Completion Check

| 項目 | 結果 |
|------|------|
| 是否真的完成 | ✅ 是 — provenance 欄位、argmax 選邊、fallback 誠實標記、scheduler 傳遞、leaderboard 安全網測試皆完成並通過；P200 報告已寫入 |
| Test result | **PASS**（合併工作流 139 passed；含 smoke 共 152 passed） |
| Full regression | **NOT RUN**（全庫；已做比例性 importer 回歸，見 §9） |
| Single remaining blocker | NONE（任務層級）；工作流層級真 P0 仍為合法 provider 授權 / observed odds（屬未來 B） |
| Modified files | `scripts/run_mlb_tsl_paper_recommendation.py`, `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`, `tests/test_mlb_daily_scheduler.py`, `tests/test_p180_strategy_leaderboard.py`, `report/p200_prediction_provenance_selected_side_hardening_20260611.md`（本報告） |
| Untracked files | `00-Plan/roadmap/agent_bootstrap/*`（授權）、`report/p199_…md`（授權）、`report/p200_…md`（本報告） |
| Staged files | 無 |
| Current branch | `main` |
| Local HEAD | `2a7aa134470dac578b5bedf08c40d80b94c56fea` |
| origin/main HEAD | `2a7aa134470dac578b5bedf08c40d80b94c56fea`（相符） |
| Open PR count | 0 |
| active_task.md status | `AUTHORIZED_PLAN_ONLY`（P199；未由本任務修改） |
| DB write status | 無 |
| live API status | 無 |
| provider unlock status | 無 |
| production mutation status | 無 |
| registry mutation status | 無 |
| controlled_apply status | 無 |
| strategy/champion mutation status | 無 |
| commit status | 無 |
| push status | 無 |
| 下一輪是否允許 | ✅ 允許 |
| 下一輪 Worker 建議 | Opus 強（若做 P201 evaluator-side `learning_eligible` 強制，需將 evaluator 原始碼納入白名單） |
| 下一輪 Thinking 建議 | 強 |
| 是否續用同一對話 | 建議**新一輪對話**（重跑 Phase 0；本任務未 commit，下一輪需先確認工作樹狀態） |

---

## Final Classification

**`P200_PREDICTION_PROVENANCE_SELECTED_SIDE_HARDENING_COMPLETE`**

> 註：實作完成且本地測試全通過，但**未 commit / 未 push**（依授權，無 git 變更）。工作樹保留未提交狀態，供使用者後續審閱與提交。
