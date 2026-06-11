# P200 — Post-Implementation Review & Commit-Readiness Audit

- **日期 (Date):** 2026-06-11 (Asia/Taipei)
- **任務類型:** Read-only post-implementation review（唯一授權寫入本報告）
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` · **Branch:** `main`
- **HEAD:** `2a7aa134470dac578b5bedf08c40d80b94c56fea`（= origin/main，未提交）
- **被審對象:** P200 本地實作（未 commit / 未 push）
- **Reviewer:** Opus 強 · Thinking 中–強

---

## 1. Governance Files Read Status

| # | 檔案 | 狀態 |
|---|------|------|
| 1 | `00-Plan/roadmap/agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` | ✅ READ |
| 2 | `00-Plan/roadmap/agent_bootstrap/TASK_TEMPLATES.md` | ✅ READ（套用 Template 2: Read-Only Execution） |
| 3 | `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md` | ✅ READ（tolerated + 授權 governance list 已核對） |
| 4 | `00-Plan/roadmap/active_task.md` | ✅ READ（Status=`AUTHORIZED_PLAN_ONLY`, P199） |
| 5 | `00-Plan/roadmap/roadmap.md` | ⏸ 未逐行（凍結舊版；治理以 CURRENT_STATE/active_task 為準） |
| 6 | `00-Plan/roadmap/CTO-Analysis.md` | ⏸ 未逐行（授權未提交 governance；僅確認 dirty，未編輯） |
| 7 | `report/p199_paper_workflow_lineage_gap_audit_20260611.md` | ✅ READ（全文） |
| 8 | `report/p200_prediction_provenance_selected_side_hardening_20260611.md` | ✅ READ（全文） |

---

## 2. Phase 0 — Actual State Verification

| 檢查 | 觀察值 | 預期 | 結果 |
|------|--------|------|------|
| pwd / toplevel | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | 同 | ✅ |
| branch / symbolic HEAD | `main` / `main` | `main`、非 detached | ✅ |
| git-dir | `.git` | `.git` | ✅ |
| HEAD / origin/main | `2a7aa13…c56fea` / `2a7aa13…c56fea` | 相等 | ✅ |
| staged | (空) | 無 | ✅ |
| open PR | 0 | 0 | ✅ |
| P199 report | 存在 | 存在 | ✅ |
| P200 report | 存在 | 存在 | ✅ |
| 審計後工作樹 | 與 Phase 0 逐字相同 | 無副作用 | ✅ |

**Dirty/Untracked 全帳目對齊（無未預期檔）：**

- **Tolerated runtime/data（CURRENT_STATE §Tolerated Dirty Files）：** `data/.live_cache/tsl_dedup_state.json`, `data/derived/tsl_market_availability_state.json`, `data/mlb_context/external_closing_state.json`, `data/mlb_context/odds_capture_schedule.json`, `data/mlb_context/odds_timeline.jsonl`, `data/tsl_fetch_status.json`, `data/tsl_odds_history.jsonl`, `data/tsl_odds_snapshot.json`, `logs/daemon_heartbeat.jsonl`, `runtime/agent_orchestrator/training_memory.json`。
- **授權 CTO governance（CURRENT_STATE §Authorized Uncommitted）：** `00-Plan/roadmap/{roadmap,CTO-Analysis,active_task}.md` + `00-Plan/roadmap/agent_bootstrap/{SHARED_AGENT_BOOTSTRAP,TASK_TEMPLATES,CURRENT_STATE}.md`。
- **Prompt 顯式授權之 P199/P200 檔：** `report/p199_…md`, `report/p200_…md`, `scripts/run_mlb_tsl_paper_recommendation.py`, `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`, `tests/test_mlb_daily_scheduler.py`, `tests/test_p180_strategy_leaderboard.py`。

無 STOP 觸發。`active_task.md` 仍標 P199（plan-only）；P200 由 prompt explicit authorization（優先序第一）授權。此為**已知且預期之 mismatch**，非失敗——無任何「不同的 active implementation task」被授權。

---

## 3. P200 Diff Review（13 點審查）

| # | 審查項 | 判定 | 依據 |
|---|--------|------|------|
| 1 | `determine_selected_side()` 決定性 argmax | ✅ | `home if model_prob_home >= model_prob_away else away`；純函式，無副作用 |
| 2 | 逐場機率 ≥ 0.5 選 home | ✅ | 機率和為 1 時 `home>=0.5` ⇔ `home>=away` |
| 3 | 逐場機率 < 0.5 選 away | ✅ | 同上對稱 |
| 4 | `selected_side_method` 絕不靜默回報 `hardcoded_home` | ✅ | 恆回 `argmax_model_probability`；`hardcoded_home` 僅存於 `_VALID_…` 常數，永不輸出。`TestP200…test_method_is_never_hardcoded_home` 覆蓋 |
| 5 | `classify_prediction_provenance()` 正確標 `neutral_fixed_prior` | ✅ | `game_specific=False`（預設）→ `neutral_fixed_prior`；`build_recommendation` 以無 `game_specific` 參數呼叫 |
| 6 | fallback/neutral 列 `learning_eligible=false` | ✅ | neutral 分支 `learning_eligible=False` |
| 7 | `learning_eligible=false` 時 `learning_block_reason` 必填 | ✅ | neutral 分支填入原因字串；game_specific 分支為 `None`（因 eligible=True） |
| 8 | edge/odds 用選定側機率而非恆 home | ✅ | `tsl_decimal_odds=_estimate_moneyline_odds(selected_prob)`、`edge_pct=selected_prob-implied`，`tsl_live` True/False 兩分支一致 |
| 9 | `source_trace` schema 相容，免改 `recommendation_row.py` | ✅ | 八欄寫入既有 `source_trace: dict`；`git status` 確認 row schema 未改 |
| 10 | scheduler 路徑傳遞 provenance | ✅ | `mlb_daily_scheduler.py:475` 呼叫 `script.build_recommendation`（共用路徑）；`test_27b` 驗證 |
| 11 | leaderboard/evaluator 測試未過度宣稱 | ✅ | `TestP200LearningIneligibleRowsNotPromoted` docstring 明載 evaluator 尚未強制 `learning_eligible`，僅測既有 `UNATTRIBUTED`+`data_limited` 安全網 |
| 12 | 未觸 DB/live/provider/production/registry/controlled_apply | ✅ | diff 僅含選邊/provenance 邏輯與 source_trace 寫入 |
| 13 | 無無關 refactor / 格式 churn | ✅ | 變更集中、命名一致、無大範圍重排 |

### 次要觀察（非 blocker，毋須改碼）

1. **`_estimate_moneyline_odds(model_prob_home)` 參數名未更新。** 現接收 `selected_prob`（可能為 away 機率）。函式體將其當泛用機率處理，**功能正確**；僅參數名語意略誤導。P200 刻意不改賠率估計邏輯（避免越界），屬可接受之化妝性瑕疵，可留待 commit-packaging 或 P201 順手更名。
2. **`test_27b` scheduler 斷言為條件式**（`if result.status==SUCCESS and output_paths:`）。若 job 未成功則斷言被略過，對「傳遞回歸」偵測力較弱。但 **propagation 契約已由 sim-gate 檔 `TestP200RowProvenancePropagation` 非條件式直測 `build_recommendation` 覆蓋**，故整體覆蓋充分；scheduler 測試為輔助，且其防禦式寫法是因 TSL 403 環境下 job 可能 BLOCK。
3. **`test_row_side_is_consistent_with_argmax` 含回歸錨點 `tsl_side=="home"`**，依賴 fixture 中性 prior 經 adapter 後 home_prob≥0.5。P200 報告 §10 風險 #4 已明列此假設。目前通過；若日後 adapter 使主隊機率 <0.5 需更新錨點（argmax 一致性主斷言仍正確）。

以上三點皆 cosmetic / 文件化已知假設，**無一需要 source/test 修改才能 commit**。

---

## 4. Test Result Summary（重跑驗證）

| 指令 | 本次重跑 | P200 報告聲稱 | 一致 |
|------|---------|--------------|------|
| `pytest tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py -q` | **35 passed** | 35 passed | ✅ |
| `pytest tests/test_mlb_daily_scheduler.py -q` | **46 passed** | 46 passed | ✅ |
| `pytest tests/test_mlb_paper_evaluator.py tests/test_mlb_paper_evaluation_runner.py tests/test_p180_strategy_leaderboard.py -q` | **58 passed** | 58 passed | ✅ |
| 合併工作流 5 檔 | **139 passed** | 139 passed | ✅ |
| `pytest tests/test_run_mlb_tsl_paper_recommendation_smoke.py -q`（白名單外，僅驗證） | **13 passed** | 13 passed | ✅ |

**合計 152 個相關測試通過，與 P200 報告聲稱完全一致。** 無任何測試失敗。

---

## 5. Full Regression Status

**NOT RUN（全庫）。** 與 read-only 審計之比例性原則一致：變更僅及單一 script 的選邊/provenance 邏輯與三測試檔；已對該 script 全部 importer（含白名單外 smoke）做比例性回歸並全通過。全庫回歸對此窄改動不成比例，且可能引入與本任務無關之既有 baseline 失敗（記憶記載 `test_portfolio_metrics_are_hardened_when_tsl_feed_blocked` 為獨立 baseline）。

---

## 6. Scope & Governance Compliance

| 檢查 | 結果 |
|------|------|
| 僅改 P199 prompt 之白名單檔 | ✅（script + 3 測試 + P200 報告） |
| `recommendation_row.py` 未改（P199 允許「僅必要時」，P200 以 source_trace 規避） | ✅ |
| evaluator / scheduler / simulation 原始碼未改 | ✅ |
| DB write / live API / provider unlock / production betting | 無 |
| EV/CLV/Kelly unlock / strategy-weight / champion mutation | 無 |
| registry mutation / `controlled_apply` | 無 |
| branch / commit / push / merge / rebase / reset / stash / clean / delete | 無 |
| tolerated dirty 檔被觸碰 | 無 |

---

## 7. Commit-Readiness Classification

**`READY_FOR_COMMIT_PACKAGING`**

P200 本地實作**正確、窄範圍、測試覆蓋充分、治理合規、向後相容**（既有無 `strategy_id` 列仍可評估），可進入後續 commit/PR 打包任務。次要觀察（§3）皆為 cosmetic 或已文件化之已知假設，不阻擋提交。

**Single blocker: NONE.**

---

## 8. Next Action Recommendation

- **下一任務：P200 Commit and PR Packaging**（本任務不執行打包）。打包任務須：
  1. 僅暫存白名單：`scripts/run_mlb_tsl_paper_recommendation.py`, `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`, `tests/test_mlb_daily_scheduler.py`, `tests/test_p180_strategy_leaderboard.py`, `report/p200_…md`（+ 本審查報告，視需要）。**絕不** `git add .`／`git add -A`，**絕不**暫存 tolerated runtime/data 或授權 CTO governance 檔。
  2. 同步更新 `active_task.md`（由 P199 plan-only 推進為 P200 已實作/待提交，或 P201 規劃）——此為打包任務之白名單事項，非本審查可改。
  3. Conventional Commits + 繁中說明（CLAUDE.md 規範）。
- **P201 現在不允許執行**（本 prompt 明令 do not implement P201）。P201（讓 evaluator 直接強制 `learning_eligible`，需將 evaluator 原始碼納入白名單）僅作為後續候選，不在本輪。

---

## 9. Required Completion Check

| 項目 | 結果 |
|------|------|
| 是否真的完成 | ✅ 是 — read-only 審計完成，diff/test/governance 全數覆核 |
| Test result | **PASS**（重跑 139 合併 + 13 smoke = 152，與 P200 報告一致） |
| Full regression | **NOT RUN**（全庫；比例性 importer 回歸已做） |
| Commit readiness classification | `READY_FOR_COMMIT_PACKAGING` |
| Single remaining blocker | **NONE** |
| Modified files | `scripts/run_mlb_tsl_paper_recommendation.py`, `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`, `tests/test_mlb_daily_scheduler.py`, `tests/test_p180_strategy_leaderboard.py`（+ tolerated runtime/data + 授權 governance，均非 P200 產物） |
| Untracked files | `00-Plan/roadmap/agent_bootstrap/*`（授權）、`report/p199_…md`、`report/p200_…md`、`report/p200_post_implementation_review_20260611.md`（本報告） |
| Staged files | 無 |
| Current branch | `main` |
| Local HEAD | `2a7aa134470dac578b5bedf08c40d80b94c56fea` |
| origin/main HEAD | `2a7aa134470dac578b5bedf08c40d80b94c56fea`（相符） |
| Open PR count | 0 |
| active_task.md status | `AUTHORIZED_PLAN_ONLY`（P199）— 預期內 mismatch，已報告 |
| DB write status | 無 |
| live API status | 無 |
| provider unlock status | 無 |
| production mutation status | 無 |
| registry mutation status | 無 |
| controlled_apply status | 無 |
| strategy/champion mutation status | 無 |
| commit status | 無 |
| push status | 無 |
| 下一輪是否允許 | ✅ 允許（P200 Commit and PR Packaging） |
| 下一輪 Worker 建議 | Opus 強 |
| 下一輪 Thinking 建議 | 中（打包屬機械性，但須嚴守暫存白名單） |
| 是否續用同一對話 | 建議**新一輪對話**（打包任務自含，重跑 Phase 0） |

---

## Final Classification

**`P200_POST_IMPLEMENTATION_REVIEW_READY_FOR_COMMIT_PACKAGING`**
