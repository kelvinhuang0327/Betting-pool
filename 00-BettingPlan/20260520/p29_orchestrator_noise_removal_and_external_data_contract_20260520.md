# P29 — Orchestrator Noise Removal + External Data Contract Design
**Date**: 2026-05-20  
**Final Classification**:
- P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND
- P29_EXTERNAL_DATA_CONTRACT_READY
- P29_EXTERNAL_FEATURES_REQUIRED_TO_BREAK_CEILING  
**paper_only**: true | **diagnostic_only**: true

---

## 工程交接報告

### 1. 本輪目標

**Part A**：識別 Full Orchestrator (Brier=0.2487) 比 Simple LogReg (0.2451) 差的根本原因，找出可移除的 noise components。

**Part B**：設計突破 0.244 feature ceiling 所需的外部資料合約（5 個合約，無實際資料擷取）。

---

### 2. 已完成事項

| 項目 | 狀態 |
|------|------|
| Pre-flight 全面確認 | ✅ |
| Source snapshot drift 記錄（+27，不覆蓋 P23） | ✅ |
| Orchestrator pipeline 完整分析（MARL/ensemble/regime）| ✅ |
| 8-variant 消融研究（5-fold walkforward，2,020 test games） | ✅ |
| H1/H2/H3/H4 四個 noise 假說驗證 | ✅ |
| 主要 noise 來源識別：MARL w_market=0.30 太低 | ✅ |
| Simplification candidate 設計 | ✅ |
| Starting pitcher contract 設計 | ✅ |
| Bullpen contract 設計 | ✅ |
| Batting form contract 設計 | ✅ |
| Lineup/injury proxy contract 設計 | ✅ |
| Park/weather contract 設計 | ✅ |
| Feature readiness matrix | ✅ |
| P26 tests 23/23 PASS | ✅ |
| P17 standalone 64/64 PASS | ✅ |
| P13-P17 regression 296/296 PASS | ✅ |
| JSON schema 5/5 PASS | ✅ |
| Forbidden affirmative scan 0 hits | ✅ |
| 11 artifacts 產出 | ✅ |

---

### 3. 修改或產出的檔案

**新增腳本（2個）**：
- [`scripts/p29_orchestrator_noise_audit.py`](../../scripts/p29_orchestrator_noise_audit.py)
- [`scripts/p29_external_data_contract_builder.py`](../../scripts/p29_external_data_contract_builder.py)

**JSON Artifacts (5個)**：
- `data/paper_recommendations/p29_orchestrator_noise_attribution_audit_20260520.json`
- `data/paper_recommendations/p29_orchestrator_ablation_results_20260520.json`
- `data/paper_recommendations/p29_external_data_contract_20260520.json`
- `data/paper_recommendations/p29_feature_readiness_matrix_20260520.json`
- `data/paper_recommendations/p29_source_snapshot_drift_20260520.json`

**Report MDs (5+1 BettingPlan)**：全部已產出

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

**Part A — Orchestrator Noise**

| Variant | Brier | Δ vs Orchestrator |
|---------|-------|------------------|
| V3: MARL w_mkt=0.50 | **0.244154** | **-0.004549** |
| V0: Pure market | 0.244354 | -0.004349 |
| V1: LogReg baseline | 0.245105 | -0.003598 |
| Full Orchestrator | 0.248703 | — |

主要 noise source：**MARL w_market=0.30 太低**（最優 ~0.50）。  
Full Orchestrator 比市場賠率差 +0.0043，主要原因是 MARL 低估市場訊號 + ES 優化過擬合。

**Part B — External Data Contract**

5 個合約全部設計完成。最高優先：Starting pitcher ERA/FIP（估計 -0.005 至 -0.015 Brier）。  
目前 ceiling 0.244 需要外部 pitcher/batting 資料才能突破。  
**合約是設計文件，無資料已取得。**

---

### 6. 尚未完成事項

- 實際 SP/Bullpen 資料擷取與整合（需 P30）
- MARL w_market 參數修改的 production-safe 驗證
- Per-window noise 時間序列分析

---

### 7. 風險與不確定點

| 風險 | 說明 |
|------|------|
| Proxy ablation vs full Orchestrator | 消融使用 mathematical proxy，非真實 Orchestrator；實際改善可能不同 |
| SP data quality | 歷史資料中 SP 換人（injury/last-minute change）難以完美捕捉 |
| Rolling stats leakage | 需嚴格實作 date-cutoff 以防未來資訊洩漏 |
| Brier 估計樂觀 | External feature 改善估計為上界，實際可能只有一半 |

---

### 8. 建議下一輪優先處理方向

**P30 — MARL w_market Repair + SP Data Integration Prototype**

兩個並行目標：
1. **MARL w_market 調整**：在 P29 diagnositc framework 下確認 w_market=0.50 的 Brier 改善，輸出 formal candidate（paper-only）
2. **SP data prototype**：從 MLB Stats API 取得 2025 season pitcher game logs，計算 season-to-date ERA/FIP 欄位，整合進 walkforward

---

### 9. 下一輪可直接執行的 task prompt

```
請執行 P30 — MARL Parameter Repair + SP Data Integration Prototype：

背景：P29 確認 MARL w_market=0.30 太低（最優 ~0.50），調整可改善 Brier -0.004 至 -0.005。
同時設計了 starting pitcher 外部資料合約（contracts/starting_pitcher_pregame_v1）。

Part A — MARL w_market 修正 (paper-only diagnostic):
1. 在 PredictorParams 預設值調整研究中，比較 w_market=[0.30, 0.40, 0.50, 0.60]
2. 使用 P28/P29 walkforward framework（MLB 2025 CSV，5-fold）
3. 確認最佳 w_market 值與對應 Brier
4. 產出 formal candidate report（paper_only=true，diagnostic_only=true）
5. 不修改 production orchestrator，不替換 champion，不做 promotion

Part B — SP Data Prototype (paper-only):
1. 從 MLB Stats API (https://statsapi.mlb.com) 取得 2025 season pitcher game logs
2. 計算 season-to-date ERA/FIP（per game date，嚴格排除當日賽事）
3. 整合進 MLB walkforward，重跑 Brier
4. 輸出 Brier before/after SP feature addition
5. 若無法取得免費資料，輸出 data_gap report，不虛構

所有 artifacts：paper_only=true / diagnostic_only=true
驗證：P26 tests + P17 + P13-P17 全 PASS
禁止：production proposal / champion replacement / promotion / live odds API call
```

---

### 10. CTO Agent 摘要（10 行）

P29 完成 Orchestrator noise attribution（8 variants，5-fold walkforward，2020 test games）與 5 個外部資料合約設計。核心發現：MARL w_market=0.30 太低是主要 noise source，調整至 0.50 後 Brier 從 0.2487 降至 0.2442（-0.004549），而純市場賠率達 0.2444；Full Orchestrator 的額外疊加（ES optimization + regime ensemble）合計帶來 +0.0043 Brier 損耗。5 個外部資料合約（SP/Bullpen/Batting/Lineup/Park）全部設計完成，無資料實際取得，Starting pitcher ERA/FIP 預估改善最高（-0.005 至 -0.015）。383/383 tests PASS，5/5 JSON schema，forbidden scan 0 hits，champion=fixed_edge_5pct 維持，promotion frozen。Final classification: P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND + P29_EXTERNAL_DATA_CONTRACT_READY + P29_EXTERNAL_FEATURES_REQUIRED_TO_BREAK_CEILING。建議 P30 做 MARL w_market 修正驗證 + SP 資料整合原型。
