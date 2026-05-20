# P28 — MLB Model Quality Repair Diagnostic
**Date**: 2026-05-20  
**Final Classification**: P28_MODEL_REPAIR_NO_IMPROVEMENT  
**paper_only**: true | **diagnostic_only**: true

---

## 工程交接報告

### 1. 本輪目標

診斷 MLB model quality 瓶頸（Brier=0.2487）、設計修復 candidates（calibration / feature expansion / ensemble shrinkage），執行 5-fold walkforward re-evaluation，嘗試達成 Brier < 0.24。

---

### 2. 已完成事項

| 項目 | 狀態 |
|------|------|
| Pre-flight 全面確認（branch/artifacts/drift） | ✅ |
| 既有 MLB walkforward artifacts 讀取與分析 | ✅ |
| Prediction probability distribution 分析 | ✅ |
| Calibration audit（Platt/Isotonic/baseline ECE） | ✅ |
| Feature bottleneck audit（7 vs 318 defined）| ✅ |
| Candidate A：Temperature scaling | ✅ |
| Candidate B：13-feature expansion（RL + rolling + conviction）| ✅ |
| Candidate C：Market shrinkage ensemble | ✅ |
| 5-fold walkforward re-evaluation（2,020 test games）| ✅ |
| Re-evaluated baseline vs Reported baseline 分析 | ✅ |
| Orchestrator noise 發現（critical insight）| ✅ |
| P26 tests 23/23 PASS | ✅ |
| P17 standalone 64/64 PASS | ✅ |
| P13-P17 regression 296/296 PASS | ✅ |
| JSON schema 5/5 PASS | ✅ |
| Forbidden affirmative scan 0 hits | ✅ |
| 11 artifacts 產出 | ✅ |

---

### 3. 修改或產出的檔案

**新增腳本**：
- [`scripts/p28_model_quality_repair.py`](../../scripts/p28_model_quality_repair.py)

**JSON Artifacts (5個)**：
- `data/paper_recommendations/p28_model_quality_baseline_audit_20260520.json`
- `data/paper_recommendations/p28_feature_bottleneck_audit_20260520.json`
- `data/paper_recommendations/p28_model_repair_candidates_20260520.json`
- `data/paper_recommendations/p28_walkforward_re_evaluation_20260520.json`
- `data/paper_recommendations/p28_source_snapshot_drift_20260520.json`

**Report MDs (5個)**：
- `report/p28_model_quality_baseline_audit_20260520.md`
- `report/p28_feature_bottleneck_audit_20260520.md`
- `report/p28_model_repair_candidates_20260520.md`
- `report/p28_walkforward_re_evaluation_20260520.md`
- `report/p28_final_validation_20260520.md`

---

### 4. 驗證結果

| 驗證 | 結果 |
|------|------|
| P26 tests 23/23 | **PASS** |
| P17 standalone 64/64 | **PASS** |
| P13-P17 regression 296/296 | **PASS** |
| 合計 383/383 | **PASS** |
| JSON schema 5/5 | **PASS** |
| Forbidden scan | **0 hits** |

---

### 5. 目前結論

**兩個關鍵發現**：

**F1：Orchestrator 比 Simple LogReg 更差**
- Simple 7-feat LogReg：Brier = 0.2451
- Full Orchestrator (Elo+MARL+Bayesian)：Brier = 0.2487
- MARL/Elo 疊加引入雜訊（Δ = +0.0036），不是改善

**F2：Feature ceiling 已達 ~0.245 with current data**

| Candidate | Brier | Δ vs 7-feat LogReg |
|-----------|-------|-------------------|
| Re-eval baseline (7-feat) | 0.245105 | — |
| C: Market shrinkage | 0.245299 | +0.000194 |
| A: Temperature scaling | 0.245535 | +0.000430 |
| B: 13-feat expansion | 0.245590 | +0.000485 |

**No candidate improves over simple LogReg. Feature ceiling = ~0.2451 with current data.**

**Target Brier < 0.24 未達到。CLV recheck 不符合資格。**

---

### 6. 尚未完成事項

- AUC / discrimination metrics 計算
- Per-window Brier 時間序列分析（早季 vs 晚季）
- Orchestrator simplification prototype（移除 MARL/Elo 層）

---

### 7. 風險與不確定點

| 風險 | 說明 |
|------|------|
| Walkforward 設定差異 | P28 re-eval (LogReg, 5-fold) ≠ Original (Orchestrator, 5-fold)，比較需謹慎 |
| Rolling win rate look-ahead | 確認 in-window 計算正確，但 rolling stats 會隨視窗增長而改善 |
| Feature ceiling 估計 | 0.245 是估計值，可能還有 0.001-0.003 的提升空間 |

---

### 8. 建議下一輪優先處理方向

**P29 — External Data Contract Design（Pitcher/Batting 外部資料需求規格）**

理由：
1. Feature ceiling ~0.245（with current data）已確認
2. Pitcher ERA/FIP 預估可帶來 Brier -0.005 至 -0.015 的改善
3. 需先設計資料合約（來源、格式、anti-leakage 規範）再實作

具體工作：
- 設計 pitcher stats data contract（Fangraphs/Baseball Reference）
- 設計 team rolling stats schema
- 定義 look-ahead leakage prevention rules
- 產出 P29 data gap requirements report

**備選：P29 — Orchestrator Noise Removal Diagnostic**

若資料引入不在 P29 範圍內，可先做：
- 移除 MARL/Elo 疊加層，簡化為 LogReg + Platt
- 確認 Brier 從 0.2487 降至 ~0.2451
- 這是 paper-only 的架構簡化，不需外部資料

---

### 9. 下一輪可直接執行的 task prompt

```
請執行 P29 — Orchestrator Noise Removal + External Data Contract Design：

背景：P28 確認 Full Orchestrator (0.2487) 比 Simple LogReg (0.2451) 更差；
feature ceiling ~0.245 with current data。

Part A — Orchestrator Simplification (paper-only):
1. 在 mlb_moneyline.py 框架下，移除 MARL/Elo 疊加
2. 使用 5-fold walkforward 確認 Brier 從 0.2487 降至 ~0.2451
3. 產出 paper_only=true / diagnostic_only=true 比較報告

Part B — External Data Contract Design:
1. 設計 pitcher stats data contract schema（ERA/FIP/WHIP，per game，pre-game only）
2. 設計 team rolling batting stats schema（wOBA/OPS，rolling 15-game window）
3. 定義 look-ahead leakage prevention rules
4. 評估 free data sources（Baseball Reference / FanGraphs public APIs）
5. 產出 P29 data requirements report（只做設計，不抓資料，不做 live call）

驗證：P26 tests + P17 + P13-P17 全 PASS
禁止：production proposal / champion replacement / promotion / live data API call
所有 artifacts：paper_only=true / diagnostic_only=true
```

---

### 10. CTO Agent 摘要（10 行）

P28 完成 MLB model quality repair diagnostic（3 candidates，5-fold walkforward，2020 test games）。關鍵發現 1：Simple 7-feat LogReg (Brier=0.2451) 優於 Full Orchestrator (0.2487)，差距 +0.0036，MARL/Elo 疊加引入雜訊。關鍵發現 2：三個修復 candidates（temperature scaling / 13-feat expansion / market shrinkage）均無法改善 re-evaluated baseline，差距 +0.000194 至 +0.000485，當前 CSV 資料已達特徵天花板 ≈ 0.245。Target Brier < 0.24 未達到，CLV recheck 不符合資格，final class = P28_MODEL_REPAIR_NO_IMPROVEMENT。383/383 tests PASS，5/5 JSON schema PASS，forbidden scan 0 hits。champion=fixed_edge_5pct 維持，promotion frozen。建議 P29 做 Orchestrator noise removal（預估 -0.004 Brier）+ 外部 pitcher/batting 資料合約設計，以突破 0.245 天花板。
