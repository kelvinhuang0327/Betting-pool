# P201 — Evaluator-side `learning_eligible` Enforcement

- **日期 (Date):** 2026-06-11 (Asia/Taipei)
- **任務類型:** Implementation（Template 3，paper-only / offline）
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` · **Branch:** `main`
- **Baseline HEAD:** `4f2e37ff45ed92d4749f85c040edc5df38ef3c65`（= origin/main；P200 merge commit）
- **依據:** P199 審計 + P200 provenance/selected-side 硬化（PR #18 已合併）
- **Worker:** Opus 強 · Thinking 中–強
- **狀態:** 本地實作完成、測試全通過、**未 commit / 未 push**（依授權）

---

## 1. Phase 0 — Actual State Verification

| 檢查 | 觀察值 | 預期 | 結果 |
|------|--------|------|------|
| pwd / toplevel | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | 同 | ✅ |
| branch / symbolic HEAD | `main` / `main` | `main`、非 detached | ✅ |
| git-dir | `.git` | `.git` | ✅ |
| HEAD / origin/main | `4f2e37f` / `4f2e37f` | 相等 | ✅ |
| HEAD 衍生自 P200 merge | `4f2e37f`（即 P200 merge 本身） | 等於或衍生自 `4f2e37f` | ✅ |
| PR #18 | MERGED | MERGED | ✅ |
| open PR | 0 | 0 | ✅ |
| staged | (空) | 無 | ✅ |
| P199/P200/P200-review 報告 | 皆存在 | 存在 | ✅ |
| dirty/untracked | tolerated runtime/data + 授權 CTO governance + 未提交 P199 報告 | 子集 | ✅ |
| active_task.md | `AUTHORIZED_PLAN_ONLY`（P199, plan-only） | 無衝突的 implementation task | ✅（預期 mismatch，已報告） |

`active_task.md` 仍標 P199 plan-only；本 P201 由 prompt explicit authorization（優先序第一）授權，無衝突。STOP 條件均未觸發。

---

## 2. Files Inspected

- `orchestrator/mlb_paper_evaluator.py`（row 解析、`evaluate_paper_recommendations`、`build_strategy_leaderboard`、`execute_batch_evaluation`）— **修改**
- `tests/test_p180_strategy_leaderboard.py`、`tests/test_mlb_paper_evaluator.py` — **修改（新增測試）**
- `tests/test_mlb_paper_evaluation_runner.py` — 在白名單，但**無需修改**（既有測試已涵蓋且仍通過）
- `orchestrator/mlb_daily_scheduler.py`（`run_paper_evaluation_job` 消費 evaluator metrics — **未在白名單，未修改**，僅讀取確認相容）
- `scripts/run_mlb_paper_evaluation.py`（CLI runner — **未在白名單，未修改**，由 runner 測試覆蓋）
- P200 `source_trace` 契約：`scripts/run_mlb_tsl_paper_recommendation.py`（已合併，僅讀取以對齊欄位名）

---

## 3. Implementation Summary

**設計原則（保守、加性、零破壞）：** 不改 row schema、不改既有評分/結算邏輯、不改 P180 排序規則；僅**新增**欄位與一個選邊外的學習資格分類，向後相容於無 `source_trace` 的歷史列。

`orchestrator/mlb_paper_evaluator.py` 變更：

1. **新增保守判定函式** `_row_learning_eligibility(rec) -> (is_eligible, block_reason)`：僅當 `source_trace.learning_eligible is True` 才視為 eligible；缺 `source_trace`、`source_trace` 非 dict、未宣告旗標、或旗標為 falsey（現行 `neutral_fixed_prior`/fallback 路徑）一律 **ineligible**，並回傳對應 `block_reason`（`missing_source_trace_provenance` / `learning_eligible_not_declared` / P200 的 `learning_block_reason`）。
2. **`PaperEvaluationMetrics` 新增三欄**（皆有預設值，序列化加性）：`learning_eligible_count`、`learning_ineligible_count`、`learning_eligibility_segmentation`（含 `eligible_count`/`ineligible_count`/`block_reasons` 計數）。
3. **`evaluate_paper_recommendations`**：於既有 matched-row 主迴圈中累計每列學習資格與 per-strategy `{eligible, ineligible}`，並寫入上述 metrics。
4. **`build_strategy_leaderboard`** 新增可選參數 `strategy_learning`；每個 leaderboard entry 新增 `learning_eligible_count`/`learning_ineligible_count`/`learning_status`/`promotable_learning_evidence`。新增純函式 `_classify_strategy_learning` 決定狀態：
   - `LEARNING_INELIGIBLE`：eligible_count == 0（即使 hit_rate 高、樣本足，**永不** promotable）；
   - `DATA_LIMITED`：0 < eligible_count < threshold；
   - `LEARNING_ELIGIBLE`：eligible_count ≥ threshold（唯一 `promotable_learning_evidence=True`）；
   - `UNKNOWN`：未提供 `strategy_learning`（legacy 直接呼叫）→ 保守、非 promotable。
5. **`execute_batch_evaluation`** 的 `per_date` 加性新增 `learning_eligible_count`/`learning_ineligible_count`。

既有模組常數新增四個 `LEARNING_STATUS_*` 標籤。**未變更**：`_extract_pk` join、評分/Brier/ROI/p-value 計算、`SMALL_SAMPLE_THRESHOLD`、`data_limited` 語意（仍為 `sample_count < threshold`）、`evaluator_version="p180_evaluator_v2"`、`paper_only`/offline 不變量。

---

## 4. Evaluator Behavior — Before / After

| | Before（P200 後） | After（P201） |
|--|------------------|---------------|
| 讀取 `source_trace.learning_eligible` | **否**（完全忽略） | **是**，保守判定 |
| 學習資格計數 | 無 | `learning_eligible_count` / `learning_ineligible_count` + `learning_eligibility_segmentation`（含 block reason 計數） |
| ineligible 列是否仍被評分 | — | **是**（評分/結算/hit/Brier 不變，供稽核） |
| 缺/壞 `source_trace` 列 | 照常評分、無資格概念 | 照常評分，但**保守歸為 ineligible**、不 crash |

## 5. Leaderboard / Learning-Evidence Behavior — Before / After

| | Before | After |
|--|--------|-------|
| 防止 fallback 被當學習證據 | 僅靠 `UNATTRIBUTED` + `data_limited` 間接安全網 | **顯式** `learning_status` + `promotable_learning_evidence` |
| 高 hit_rate、足樣本、但全 ineligible 的策略 | 看似 promotable（非 data_limited、attributed） | `LEARNING_INELIGIBLE` 且 `promotable_learning_evidence=False` |
| 既有 entry 欄位（rank/data_limited/…） | 保留 | 保留（純加性新增四欄） |
| 排序決定性（hit_rate→roi→id） | 是 | 不變 |

## 6. Backward Compatibility for Old Rows

- 歷史列無 P200 `source_trace` → `_row_learning_eligibility` 回 `(False, "missing_source_trace_provenance")`：照常評分、計入 `learning_ineligible_count`、**永不**被宣稱為 promotable。
- `build_strategy_leaderboard` 在無 `strategy_learning`（既有直接呼叫者，如 P180 測試）時：`learning_status="UNKNOWN"`、`promotable_learning_evidence=False`、計數欄為 `None` — 既有欄位與排序完全不變，既有測試零修改通過。
- metrics 新欄皆有預設、JSON 可序列化、決定性 → runner 冪等性與 `r1==r2` 斷言不受影響。

---

## 7. Tests Run

新增 **18** 個 P201 測試（涵蓋 D1–D6；D7/D8 為既有測試續通過）：

- `tests/test_mlb_paper_evaluator.py`：+12（`TestP201RowLearningEligibilityHelper` ×6、`TestP201EvaluatorLearningCounts` ×6）— helper 保守判定、eligible/ineligible 分別計數(D1/D3)、block reason 揭露(D2)、缺 source_trace 不崩潰且保守(D5)、eligible 維持(D6)、序列化/決定性。
- `tests/test_p180_strategy_leaderboard.py`：+6（`TestP201LeaderboardLearningStatus`）— 全 ineligible 策略不 promotable(D4)、足量 eligible 可 promotable、部分 eligible→DATA_LIMITED、省略→UNKNOWN、端到端 ineligible/eligible。

| 指令 | 結果 |
|------|------|
| `pytest tests/test_mlb_paper_evaluator.py -q` | **17 passed**（5 baseline + 12 新增） |
| `pytest tests/test_mlb_paper_evaluation_runner.py -q` | **21 passed**（無修改，續通過 — D8） |
| `pytest tests/test_p180_strategy_leaderboard.py -q` | **38 passed**（32 baseline + 6 新增 — 含 D7） |
| 三檔合計 | **76 passed**（58 baseline + 18 新增） |
| 合併工作流 5 檔 | **157 passed**（139 baseline + 18 新增） |
| `pytest tests/test_run_mlb_feature_family_ablation.py -q`（白名單外，相容性抽查） | **5 passed** |

---

## 8. Full Regression Status

**NOT RUN（全庫，346 測試檔）。** 理由：變更為純加性 evaluator 擴充（新欄位 + 新可選參數 + 新 helper），未改既有評分/排序/schema 邏輯。evaluator 之**全部直接 importer**（`mlb_daily_scheduler.py`、`scripts/run_mlb_paper_evaluation.py`、三個測試檔）皆由合併工作流 5 檔 157 tests 覆蓋並通過，另抽查唯一其他引用 leaderboard 字樣的 `test_run_mlb_feature_family_ablation.py` 亦通過。全庫回歸對此窄加性改動不成比例，且可能引入與本任務無關之既有 baseline 失敗。

---

## 9. Risks and Limitations

1. **資格不等於正確性。** `learning_eligible=true` 僅表示「逐場、非 fallback」之 provenance；目前產線仍恆為 `neutral_fixed_prior`（P200 已記載），故實務上所有現行列為 ineligible。真正逐場特徵路徑屬後續任務。
2. **賠率仍為 proxy。** P201 未引入 observed odds；`roi`/`edge` 仍為結構性量（屬 P199 候選 B，受合法 provider 授權阻擋）。
3. **`UNATTRIBUTED` 仍可能混合資格。** 多列無 strategy_id 會聚為單一 `UNATTRIBUTED` 桶；其 `learning_status` 依該桶 eligible 計數判定，符合保守原則但聚合掩蓋逐列差異（逐列計數仍見於 `learning_eligibility_segmentation`）。
4. **下游消費端未強制。** 本任務只在 evaluator/leaderboard **標記** promotability；任何「晉升」決策模組若存在，仍應自行尊重 `promotable_learning_evidence`（未來契約）。

---

## 10. Explicit Non-Actions

- 未 commit / push / branch / PR / merge / rebase / reset / stash / clean / delete。
- 未改白名單外任何 source/test（含 `mlb_daily_scheduler.py`、`run_mlb_tsl_paper_recommendation.py`、CLI runner、row schema）。
- 未碰 tolerated daemon/runtime/data dirty 檔；未編輯/暫存授權 CTO governance 檔；未動 `active_task.md`。
- 無 DB write / live or paid API / provider unlock / production betting / real recommendation。
- 無 EV/CLV/Kelly unlock、strategy-weight/champion mutation、registry mutation、`controlled_apply`、scheduler runtime 變更、schema migration。

---

## 11. Required Completion Check

| 項目 | 結果 |
|------|------|
| 是否真的完成 | ✅ 是 — evaluator 尊重 `learning_eligible`；fallback/neutral/proxy/缺 provenance 列無法成為 promotable 學習證據；歷史列保守相容；計數欄測試覆蓋；P201 報告已寫入 |
| Test result | **PASS**（三檔 76、合併工作流 157、抽查 5；新增 18） |
| Full regression | **NOT RUN**（全庫；importer 比例性回歸已做，見 §8） |
| Single remaining blocker | NONE（任務層級）；工作流層級真 P0 仍為合法 provider 授權 / observed odds + 真正逐場特徵路徑 |
| Modified files | `orchestrator/mlb_paper_evaluator.py`, `tests/test_mlb_paper_evaluator.py`, `tests/test_p180_strategy_leaderboard.py`, `report/p201_evaluator_learning_eligible_enforcement_20260611.md`（本報告） |
| Untracked files | `00-Plan/roadmap/agent_bootstrap/*`（授權）、`report/p199_…md`（未提交）、`report/p201_…md`（本報告） |
| Staged files | 無 |
| Current branch | `main` |
| Local HEAD | `4f2e37ff45ed92d4749f85c040edc5df38ef3c65` |
| origin/main HEAD | `4f2e37ff45ed92d4749f85c040edc5df38ef3c65`（相符） |
| Open PR count | 0 |
| active_task.md status | `AUTHORIZED_PLAN_ONLY`（P199；未由本任務修改） |
| DB write / live API / provider unlock | 無 / 無 / 無 |
| production / registry / controlled_apply mutation | 無 / 無 / 無 |
| strategy/champion mutation | 無 |
| commit / push status | 無 / 無 |
| 下一輪是否允許 | ✅ 允許（P202 = commit/PR packaging of P201；或下游 promotability 契約消費） |
| 下一輪 Worker 建議 | Opus 強 |
| 下一輪 Thinking 建議 | 中 |
| 是否續用同一對話 | 建議新一輪對話（重跑 Phase 0） |

---

## Final Classification

**`P201_EVALUATOR_LEARNING_ELIGIBLE_ENFORCEMENT_COMPLETE`**

> 註：實作完成且本地測試全通過，但**未 commit / 未 push**（依授權）。工作樹保留未提交狀態，供後續審閱與打包。
