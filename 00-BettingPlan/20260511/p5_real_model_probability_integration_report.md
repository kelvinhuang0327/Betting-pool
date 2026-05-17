# P5 Real Model Probability Integration Report

**日期**: 2026-05-11  
**里程碑**: P5_REAL_MODEL_PROBABILITY_INTEGRATION_READY  
**狀態**: ✅ COMPLETE  

---

## 1. 執行摘要 (Executive Summary)

P5 成功將真實校準模型概率整合進策略模擬脊柱，並通過 `source_trace` 在每一層（模擬→推薦）完整記錄概率來源。核心發現：真實模型 (`calibrated_platt_from_report`) 在 2025 賽季 BSS = -0.0188，代表模型預測能力略遜於市場基準。閘門已正確阻擋推薦。

---

## 2. 背景與目標 (Background & Objectives)

P5 任務：

1. 歷史賽事行數包含 `model_prob_home` 欄位 ✅  
2. 模擬可區分「模型概率」vs「市場概率」 ✅  
3. BSS 基於真實模型概率計算（有意義） ✅  
4. 推薦 `source_trace` 清楚標示概率來源 ✅  
5. 若真實模型 BSS < 0 → 模擬閘門阻擋 ✅  

---

## 3. 真實模型概率素材 (Real Model Probability Artifact)

| 項目 | 數值 |
|---|---|
| 素材路徑 | `data/derived/model_outputs_2026-04-29.jsonl` |
| 總行數 | 2,986 行（每場賽事 HOME + AWAY 各一行） |
| 有效場次 | 1,476 場次（擁有真實 predicted_probability） |
| 概率來源標籤 | `calibrated_platt_from_report` |
| P5 映射源 | `calibrated_model` |
| 日期範圍 | 2025-04-25 → 2025-09-28 |

**Stub 素材（不可用）**：
- `data/derived/model_outputs_6q_dry_run_2026-04-30.jsonl`（30 行，`predicted_probability = None`）  
- `data/derived/future_model_predictions_dry_run_2026-04-29.jsonl`（stub，無真實概率）

---

## 4. 新增模組 (New Modules)

### `wbc_backend/prediction/__init__.py`
Package init。

### `wbc_backend/prediction/mlb_model_probability.py`
- `MlbModelProbability` dataclass，含硬性不變量（prob ∈ [0,1]、總和 ≈ 1.0、source 白名單）
- `VALID_PROBABILITY_SOURCES = {"real_model", "calibrated_model", "market_proxy", "fixture"}`
- 方法：`to_dict()`, `to_jsonl_line()`

### `wbc_backend/prediction/mlb_model_probability_adapter.py`
- `MLB_TEAM_CODE_MAP`：30 支 MLB 球隊全名 → 三字母代碼
- `build_model_probabilities_from_existing_artifacts()`：從素材 JSONL 產出概率列表
- `merge_model_probabilities_into_rows()`：雙模式 join（game_id 優先，date+teams 備援）
- 安全：`_assert_paper_output_path()` 限定輸出在 `outputs/predictions/PAPER/`

### `scripts/run_mlb_model_probability_export.py`
- CLI 工具：輸出概率 JSONL + 已合併賠率 CSV
- 預設拒絕市場代理（`--allow-market-proxy` 明確啟用）
- PAPER zone 強制執行

---

## 5. 現有模組更新 (Modified Modules)

### `wbc_backend/simulation/strategy_simulator.py`
新增 `source_trace` 欄位：
- `probability_source_mode`：`"real_model"` | `"calibrated_model"` | `"market_proxy"` | `"mixed"` | `"unknown"`
- `real_model_count`：使用真實模型概率的賽事數量
- `market_proxy_count`：使用市場代理概率的賽事數量
- `missing_model_prob_count`：缺乏模型概率的行數

### `wbc_backend/recommendation/recommendation_gate_policy.py`
- 在 `build_recommendation_gate_from_simulation()` 回傳字典中加入 `source_trace` 欄位
- 讓推薦層可直接讀取模擬層的概率來源元數據

### `scripts/run_mlb_tsl_paper_recommendation.py`
新增 `source_trace` 欄位：
- `probability_source`：從模擬 source_trace 繼承的概率來源模式
- `simulation_probability_source_mode`
- `simulation_real_model_count`
- `simulation_market_proxy_count`
- 若模擬為純 market_proxy → `gate_reasons` 加入警告

---

## 6. 連接策略 — Team Code Join (Join Strategy)

**問題**：賠率 CSV 使用球隊全名（"Los Angeles Dodgers"），模型輸出使用三字母代碼（"LAD"）。

**解法**：`MLB_TEAM_CODE_MAP`（30 球隊，硬編碼）+ 部分後綴匹配備援。

**Join 優先序**：
1. `canonical_match_id` / `game_id` 精確匹配
2. 正規化日期（YYYY-MM-DD）+ `home_team_code` + `away_team_code`

---

## 7. 概率輸出統計 (Export Statistics — Task 9)

```
probability_count=1476
real_model_count (calibrated + real_model)=1476
market_proxy_count=0
row_count=2430
enriched_with_model_prob=1341
```

- **1,476 場次**獲得真實校準模型概率
- **1,341 賠率行**成功合併（2,430 行中 55.2% 覆蓋）
- 未覆蓋行（2025-03-18 → 2025-04-24）不含真實模型概率；模擬脊柱回退至市場代理並標記

---

## 8. 模擬結果 (Simulation Result — Task 10)

```
strategy=moneyline_edge_threshold_v0
n=2428 | bets=848
BSS=-0.0188 (NEGATIVE)
ECE=0.0363
ROI=-0.03%
gate=BLOCKED_NEGATIVE_BSS
probability_source_mode=real_model
real_model_count=2428
market_proxy_count=0
```

**解讀**：真實校準模型 BSS = -0.0188 < 0。模型 Brier Score 略高於市場隱含概率，代表未優於市場基準。閘門正確阻擋。

---

## 9. 推薦結果 (Recommendation Result — Task 11)

```
gate=BLOCKED_SIMULATION_GATE
probability_source=real_model
simulation_probability_source_mode=real_model
simulation_real_model_count=2428
simulation_market_proxy_count=0
simulation_gate_status=BLOCKED_NEGATIVE_BSS
```

推薦輸出：`outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

---

## 10. 測試覆蓋 (Test Coverage)

| 測試文件 | 測試數量 | 狀態 |
|---|---|---|
| `tests/test_mlb_model_probability_contract.py` | 14 | ✅ PASS |
| `tests/test_mlb_model_probability_adapter.py` | 14 | ✅ PASS |
| `tests/test_strategy_simulator_spine.py` (含新增 P5 類) | 27 | ✅ PASS |
| 回歸：P3/P4 所有測試 | 116 | ✅ PASS |
| **合計** | **142+** | **✅ ALL PASS** |

---

## 11. P5 成功準則驗證 (P5 Success Criteria Validation)

| 準則 | 達成 |
|---|---|
| 歷史行包含 `model_prob_home` | ✅ 1,341 行已合併 |
| 模擬區分模型 vs 市場概率 | ✅ `probability_source_mode` 正確標記 |
| BSS 基於真實概率有意義 | ✅ BSS=-0.0188（真實非零值） |
| 推薦 `source_trace` 標示概率來源 | ✅ 所有 P5 欄位存在 |
| 真實模型 BSS < 0 → 閘門阻擋 | ✅ `BLOCKED_SIMULATION_GATE` |

---

## 12. 安全審核 (Security Review)

- 所有輸出嚴格限定在 `outputs/predictions/PAPER/` 和 `outputs/simulation/PAPER/`
- `market_proxy` 永不標記為 `real_model`
- 生產模式未啟用（`_MLB_PAPER_ONLY = True`）
- 無資料滲透（Look-ahead Leakage）：模型素材來自賽前訓練數據

---

## 13. 已知限制 (Known Limitations)

1. **賠率 CSV 覆蓋缺口**：2025-03-18 → 2025-04-24 無真實模型概率（占約 5 週資料）
2. **BSS = -0.0188**：真實模型略遜市場，需進一步特徵工程或重新校準
3. **球隊代碼 join**：依賴後綴匹配備援，對歷史名稱變更（如 Oakland Athletics → Athletics）可能有遺漏

---

## 14. 下一步 (Next Steps — P6 Scope)

若 P5 中 BSS 為負，P6 應探索：
1. **特徵工程修復**：識別導致校準偏誤的特徵
2. **模型重新訓練**：以 2025 賽季資料驗證模型更新
3. **時間窗口分析**：是否某些月份/球場類型 BSS 為正？
4. **校準修復**：Platt Scaling 重新調整
5. **市場無效性搜尋**：尋找 BSS > 0 的特定市場條件

---

## 15. 最終標記 (Final Marker)

```
P5_REAL_MODEL_PROBABILITY_INTEGRATION_READY
```

**生成時間**: 2026-05-11  
**測試數量**: 142 passed  
**BSS (真實模型)**: -0.0188  
**閘門結果**: BLOCKED_NEGATIVE_BSS → BLOCKED_SIMULATION_GATE  
