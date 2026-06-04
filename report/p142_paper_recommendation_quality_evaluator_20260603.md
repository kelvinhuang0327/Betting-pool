# P142 Paper Recommendation Quality Evaluator Report

**日期**: 2026-06-03
**任務**: P142_PAPER_RECOMMENDATION_QUALITY_EVALUATOR
**最終分類**: `P142_PAPER_RECOMMENDATION_QUALITY_EVALUATOR_READY_FOR_COMMIT`

---

## 摘要

P142 實作完成。本任務成功建立了一個離線、Paper-only 的推薦品質評估器（`orchestrator/mlb_paper_evaluator.py`），能夠將 `outputs/recommendations/PAPER/` 中產生的每日推薦 row 對應到歷史比賽結果（如 `data/mlb_2026/derived/p84e_2026_outcome_attached_prediction_rows.jsonl`），並計算包括 Hit Rate、Brier Score、ROI 及統計顯著性（Binomial p-value）在內的核心指標。

全套 107 個測試（包含 5 個新增的評估器測試）全部通過，無任何 staged 變更。

---

## Phase 0 驗證

| 項目 | 狀態 |
|---|---|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` ✅ |
| Branch | `main` ✅ |
| HEAD | `d2a6f4ee56f0a292331acab0ec6db4d08e786c9b` ✅ |
| local HEAD = origin/main | ✅ |
| 工作樹（source code） | 乾淨（僅含 P142 新增檔案與預期的 runtime 噪音） |
| Staged files | 0 ✅ |

---

## 實作與對應合約 (Mapping Contract)

對應合約基於 **Game PK**。
- **Paper Row (推薦檔)**: `game_id`（例如 `2026-05-11-LAA-CLE-824441`），透過 `game_id.split("-")[-1]` 提取 Game PK `824441`。
- **Outcome Record (結果檔)**: `game_id`（例如 `mlb_2026_824441`），透過 `game_id.split("_")[-1]` 提取 Game PK `824441`。
- 比對兩者 PK 進行對應，若 Game PK 一致且結果中 `outcome_available` 為 True 且 `actual_winner` 為 "home" 或 "away"，則列入評估集。

---

## 支援的指標 (Metrics Supported)

1. **evaluated_count**: 讀取的推薦總數。
2. **matched_outcome_count**: 成功對應且結果有效的數量。
3. **missing_outcome_count**: 未對應或結果無效的數量。
4. **coverage_rate**: 對應成功率 (`matched / evaluated`)。
5. **hit_rate**: 預測邊（`tsl_side`）與實際勝隊（`actual_winner`）一致的比例。
6. **brier_score**: 模型預測機率（`model_prob_home`）與真實結果（home_win 為 1 或 0）的均方誤差。
7. **binomial_p_value**: 基於 H0 假設（p=0.5）的單尾二項式顯著性 p 檢定值。
8. **actual_paper_pnl & roi**: 基於 `stake_units_paper` 限制的模擬損益與回報率。
9. **shadow_unit_pnl & roi**: 假設全部投注一單位（忽略 gate 阻擋）的影子損益與回報率。
10. **細分市場**:
    - **gate_segmentation**: 依 `gate_status` 劃分的計數、準確率與 ROI。
    - **confidence_segmentation**: 依模型最大機率區間（0.50-0.55、0.55-0.65、0.65-1.00）劃分的表現。

---

## Paper-Only 安全閘與聲明

- ✅ **No DB Writes**: 評估器完全在記憶體中運作，不對資料庫進行任何寫入操作。
- ✅ **No Live API Calls**: 完全使用本地 JSONL 快照，不呼叫 live 體育博彩 API。
- ✅ **No Provider Unlock**: 不涉及任何賠率提供商憑證或解鎖。
- ✅ **No EV/CLV/Kelly production unlock**: 所有 ROI 與 Kelly 均保持為 paper 狀態，stake 僅作回測診斷。
- ✅ **Unstaged Changes**: 變更保持在未 stage 狀態，無 commit 與 push。

---

## 測試結果

| 測試指令 | 結果 | 測試數 |
|---|---|---|
| `.venv/bin/python -m pytest tests/test_mlb_paper_evaluator.py -v` | **PASS** | 5 |
| `.venv/bin/python -m pytest tests/test_run_mlb_tsl_paper_recommendation_smoke.py -v` | **PASS** | 6 |
| `.venv/bin/python -m pytest tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py -v` | **PASS** | 10 |
| `.venv/bin/python -m pytest tests/test_mlb_daily_scheduler.py -v` | **PASS** | 27 |
| `.venv/bin/python -m pytest tests/test_mlb_advisory_api.py -v` | **PASS** | 59 |
| **合計** | **PASS** | **107** |

---

## 剩餘阻擋與下一步建議

| Blocker | 影響 | 建議 |
|---|---|---|
| 背景 daemon 噪音 | 導致 git 狀態持續 modified 影響 Preflight | 建議在 P143 統一處理 `.gitignore` 或隔離 runtime 目錄。 |
| TSL 403 API Block | Paper 投注推薦的 actual ROI 暫時為 0.0 | 持續追蹤 TSL API 權限或研究備用賠率擷取管道。 |

---

## 修改/建立檔案清單

```
orchestrator/mlb_paper_evaluator.py                        (建立 - 評估器核心邏輯)
tests/test_mlb_paper_evaluator.py                          (建立 - 評估器單元測試)
data/mlb_2026/derived/p142_paper_recommendation_quality_evaluator_summary.json  (建立 - 真實數據運行輸出)
report/p142_paper_recommendation_quality_evaluator_20260603.md (建立 - 本報告說明檔)
```
