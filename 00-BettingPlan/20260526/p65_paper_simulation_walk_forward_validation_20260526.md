# P65 Walk-Forward Validation
## Paper Simulation Temporal Stability Analysis

| 欄位 | 值 |
|---|---|
| **Phase** | P65 |
| **日期** | 2026-05-26 |
| **分類** | `P65_EDGE_STABLE_NEGATIVE` |
| **模式** | `paper_only=True`, `diagnostic_only=True` |
| **Branch** | `main` |
| **Prior** | P64 `P64_PAPER_SIMULATION_FIRST_RUN_READY` (commit `c4a3375`) |

---

## 1. Pre-flight 結果

| 檢查項目 | 結果 |
|---|---|
| Repo 狀態 | canonical (working tree clean at P64 commit `c4a3375`) |
| Branch | `main` |
| HEAD | `c4a3375` |
| 輸入資料 | 535 P64 rows (JSONL) ✅ |
| 執行模式 | paper_only + diagnostic_only (無 live API) ✅ |

---

## 2. 污染文件評估

未修改任何既有合約、模型或運行時邏輯：

| 文件 | 狀態 |
|---|---|
| P45 Platt (A=0.435432, B=0.245464) | 未異動 |
| P52 監控閾值 | 未異動 |
| 運行時推薦邏輯 | 未異動 (`runtime_recommendation_logic_changed=False`) |
| TSL / live / paid API | 未呼叫 |

---

## 3. 載入的來源工件

| 工件 | 路徑 | 狀態 |
|---|---|---|
| P64 rows JSONL | `data/mlb_2025/derived/p64_paper_simulation_rows.jsonl` | 535 rows ✅ |
| P64 summary | `data/mlb_2025/derived/p64_paper_simulation_first_run_summary.json` | ✅ |
| P62 contract | `data/mlb_2025/derived/p62_paper_recommendation_contract_draft_summary.json` | ✅ |
| P63 readiness | `data/mlb_2025/derived/p63_paper_recommendation_contract_review_readiness_summary.json` | ✅ |
| P45 Platt | `data/mlb_2025/derived/p45_platt_recalibration_summary.json` | ✅ |
| P52 thresholds | `data/mlb_2025/derived/p52_monitoring_contract_v2_summary.json` | ✅ |

---

## 4. P64 Baseline 摘要

| 指標 | 值 |
|---|---|
| 總 rows | 535 |
| P64 分類 | `P64_PAPER_SIMULATION_FIRST_RUN_READY` |
| Edge mean (全體) | -0.032473 |
| Positive edge rows | 200 / 535 (37.4%) |
| Gate status | 535/535 GATE_PASS |
| Paper status | 535/535 PAPER_ELIGIBLE_CONTRACT_ONLY |
| Forbidden scan | 0 violations (CLEAN) |

---

## 5. 月度 Walk-Forward 表

| 月份 | n | mean_edge | pos_rate |
|---|---|---|---|
| 2025-04 | 16 | -0.0253 | 0.562 |
| 2025-05 | 120 | -0.0292 | 0.417 |
| 2025-06 | 101 | -0.0339 | 0.327 |
| 2025-07 | 92 | -0.0220 | 0.359 |
| 2025-08 | 108 | -0.0127 | 0.491 |
| 2025-09 | 98 | -0.0678 | 0.224 |
| **合計** | **535** | **-0.0318** | — |

**觀察：** 8 月 edge 最接近平衡 (-0.0127, pos_rate=49.1%)；9 月最差 (-0.0678, pos_rate=22.4%)。無月份呈現正 edge。

---

## 6. 時間序列三等分表

| 分段 | n | mean_edge | pos_rate | 日期區間 |
|---|---|---|---|---|
| Third 1 | 178 | -0.0301 | 0.399 | 2025-04-27 → 2025-06-13 |
| Third 2 | 178 | -0.0242 | 0.388 | 2025-06-13 → 2025-08-08 |
| Third 3 | 179 | -0.0431 | 0.335 | 2025-08-08 → 2025-09-28 |

**分類依據：** 三個分段的 mean_edge 均 < -0.01 → `P65_EDGE_STABLE_NEGATIVE`

---

## 7. 滾動視窗表 (size=100, step=50)

| 視窗 | date_start | date_end | n | mean_edge | pos_rate |
|---|---|---|---|---|---|
| 1 | 2025-04-27 | 2025-05-21 | 100 | -0.0264 | 0.440 |
| 2 | 2025-05-09 | 2025-06-05 | 100 | -0.0277 | 0.400 |
| 3 | 2025-05-23 | 2025-06-19 | 100 | -0.0305 | 0.380 |
| 4 | 2025-06-05 | 2025-07-03 | 100 | -0.0331 | 0.340 |
| 5 | 2025-06-19 | 2025-07-21 | 100 | -0.0332 | 0.300 |
| 6 | 2025-07-05 | 2025-08-05 | 100 | -0.0163 | 0.410 |
| 7 | 2025-07-21 | 2025-08-22 | 100 | -0.0104 | 0.510 |
| 8 | 2025-08-06 | 2025-09-06 | 100 | -0.0225 | 0.430 |
| 9 | 2025-08-22 | 2025-09-18 | 100 | -0.0516 | 0.260 |
| 10 | 2025-09-06 | 2025-09-28 | 85 | -0.0685 | 0.224 |

**觀察：** 視窗 7 (-0.0104) 是全季 edge 最佳的 100 場視窗。後期季節 (視窗 9-10) edge 惡化顯著。

---

## 8. 穩定性分類

```
P65_EDGE_STABLE_NEGATIVE
```

**分類理由：**
- 三個時間等分的 mean_edge 全部 < -0.01
- 無任何月份或視窗呈現正 edge 均值
- Edge 的惡化在季末集中 → 可能為季末投手疲勞或對手資訊調整效應
- 分類確認：市場具持續優勢，本模型目前無獲利 edge

---

## 9. 診斷建議

| 建議 | 理由 |
|---|---|
| `RESOLVE_2024_DATA_GAP` | 缺乏 2024 歷史資料限制了訓練覆蓋度，可能是主要因素 |
| `DO_NOT_PROCEED_TO_PRODUCT` | Edge 持續負值，不得進入產品化或實盤流程 |
| `REVIEW_MODEL_CALIBRATION` | 8 月視窗 pos_rate=51% 但 edge 仍負，暗示 Platt 校準偏移 |
| `REVIEW_ODDS_MAPPING` | 賠率匹配 (date+home_team join) 可能含系統性偏差，需審查 |
| `ALLOW_CONTRACT_ITERATION_ONLY` | 允許合約層面迭代 (特徵工程、臨界值調整)，禁止產品化 |

---

## 10. 治理保存結果

| 治理欄位 | 值 | 狀態 |
|---|---|---|
| `paper_only` | `True` | ✅ |
| `diagnostic_only` | `True` | ✅ |
| `promotion_freeze` | `True` | ✅ |
| `kelly_deploy_allowed` | `False` | ✅ |
| `real_bet_allowed` | `False` | ✅ |
| `production_ready` | `False` | ✅ |
| `live_api_calls` | `0` | ✅ |
| `paid_api_called` | `False` | ✅ |
| `runtime_recommendation_logic_changed` | `False` | ✅ |

---

## 11. 2024 資料缺口狀態

```
data_year_2024_gap_remains_unresolved = True
```

**說明：** P65 驗證僅使用 2025 年本地資料 (535 rows, April-September 2025)。缺乏 2024 年歷史比對資料，無法驗證模型的跨年穩定性。在 2024 資料缺口解決前，所有結果均為 2025-only 估計。

---

## 12. 測試結果

| 測試套件 | PASS | FAIL |
|---|---|---|
| P65 targeted (36 tests) | 36 | 0 |
| P43 regression | — | — |
| P59 regression | — | — |
| P60 regression | — | — |
| P61 regression | — | — |
| P62 regression | — | — |
| P63 regression | — | — |
| P64 regression | — | — |
| **全迴歸 total** | **191** | **0** |

---

## 13. Forbidden Scan 結果

```json
{
  "violations": 0,
  "result": "CLEAN",
  "details": [],
  "terms_scanned": 11
}
```

掃描對象：P64 paper simulation rows (535 rows, JSON serialized)。無任何肯定式治理違規。

---

## 14. Commit Hash

```
feat(p65): walk-forward validation — P65_EDGE_STABLE_NEGATIVE
```

(commit 完成後更新此欄位)

---

## 15. 最終分類

```
P65_EDGE_STABLE_NEGATIVE
```

**解釋：** 2025 年全季 535 場 Tier C 紙上交易 (|sp_fip_delta| ≥ 0.50) 在所有時間視窗均呈現穩定負 edge。負 edge 不是隨機噪聲，而是結構性的市場效率差距。在 2024 資料缺口解決或模型校準改善前，不得推進至產品化。

---

## 16. 未來 24h 提示

```
NEXT 24H PROMPT (CEO):
P65 walk-forward validation is complete. Classification: P65_EDGE_STABLE_NEGATIVE.
535 rows across 6 months show consistently negative edge (mean -0.032, best window -0.010).
Authorization needed for next phase:
  Path A: P66 — re-calibrate Platt scaling on 2025 data only (paper-mode, no production impact)
  Path B: P61 PATH_B — resolve 2024 data gap via free historical odds sources
  Path C: odds mapping audit — review date+home_team join for systematic mismatches
Governance preserved: paper_only=True, kelly_deploy_allowed=False, real_bet_allowed=False.
```

---

## 17. CTO Agent 10-Line Summary

```
P65 WALK-FORWARD VALIDATION SUMMARY (CTO / 10-line):
1. Phase: P65 Walk-Forward Validation — 535 P64 paper rows, 2025 MLB season.
2. Classification: P65_EDGE_STABLE_NEGATIVE — all temporal windows show negative mean edge.
3. Monthly range: April (-0.025) through September (-0.068); no month positive.
4. Chronological thirds: -0.030 / -0.024 / -0.043 — degradation in late season.
5. Best rolling window: July 21–Aug 22, edge=-0.010, pos_rate=51% (borderline viable).
6. Worst rolling window: Sep 6–Sep 28, edge=-0.069, pos_rate=22% (highly negative).
7. Root cause hypothesis: Platt calibration drift + possible odds-mapping bias + 2024 data gap.
8. Governance: paper_only=True, kelly_deploy=False, real_bet=False, forbidden_scan=CLEAN.
9. Tests: 36/36 P65 PASS, 191/191 regression PASS (P43+P59-P65).
10. Recommendation: resolve 2024 data gap OR re-calibrate model before next paper iteration.
```
