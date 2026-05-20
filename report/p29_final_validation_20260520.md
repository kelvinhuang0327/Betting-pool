# P29 Final Validation Report
**Date**: 2026-05-20  
**Phase**: P29_ORCHESTRATOR_NOISE_REMOVAL + P29_EXTERNAL_DATA_CONTRACT  
**paper_only**: true | **diagnostic_only**: true

---

## 驗證矩陣

| 驗證項目 | 結果 |
|----------|------|
| P26 tests（23個） | **23/23 PASS** |
| P17 standalone | **64/64 PASS** |
| P13-P17 regression | **296/296 PASS** |
| **合計** | **383/383 PASS** |
| JSON schema（5個 P29 artifacts） | **5/5 PASS** |
| Forbidden affirmative scan | **0 hits** |
| No live API call | **PASS** |
| No TSL crawler modification | **PASS** |
| P23/P26 baseline 未被覆蓋 | **PASS** |
| fixed_edge_5pct champion 未替換 | **PASS** |
| No index fallback in CLV module | **PASS** |

---

## Source Snapshot 狀態

| 項目 | P23/P26 Pinned | Current |
|------|---------------|---------|
| TSL Lines | 2,788 | 2,815（+27） |
| Action | — | 僅記錄，P29 使用 MLB CSV |

---

## Part A: Orchestrator Noise Ablation 結果

| Variant | Brier | Δ vs Orchestrator |
|---------|-------|------------------|
| Pure market | 0.244354 | **-0.004349** |
| LogReg (P28 baseline) | 0.245105 | -0.003598 |
| **MARL w_mkt=0.50** | **0.244154** | **-0.004549（最佳）** |
| Full Orchestrator | 0.248703 | — |

**主要噪音來源**：MARL w_market=0.30 太低（最優為 0.50）

---

## Part B: External Data Contract 完整性

| Contract | 狀態 | 估計 Brier 改善 |
|---------|------|----------------|
| Starting pitcher | ✅ DESIGNED | -0.005 至 -0.015 |
| Bullpen fatigue | ✅ DESIGNED | -0.002 至 -0.007 |
| Batting form | ✅ DESIGNED | -0.003 至 -0.010 |
| Lineup/injury proxy | ✅ DESIGNED | -0.002 至 -0.006 |
| Park / Weather | ✅ DESIGNED | -0.001 至 -0.003 |

**5 個合約全部設計完成，無實際資料擷取。**

---

## 嚴格禁止確認

| 禁止事項 | 狀態 |
|---------|------|
| 合併 PR #2 | 未執行 |
| 聲稱可獲利 | 未聲稱 |
| 替換 fixed_edge_5pct champion | 未替換 |
| Strategy optimizer promotion | 未啟動 |
| 修改 TSL crawler / live odds API | 未修改 |
| 覆蓋 P23-P28 baselines | 未覆蓋 |
| 視 external data contract 為已取得資料 | 未聲稱 |
| train-only 改善宣稱模型改善 | 未作 |

---

## 最終分類

1. **`P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND`**（w_market=0.30→0.50，預期 -0.005 Brier）
2. **`P29_EXTERNAL_DATA_CONTRACT_READY`**（5 個合約設計完成）
3. **`P29_EXTERNAL_FEATURES_REQUIRED_TO_BREAK_CEILING`**（0.244 ceiling 需外部 SP/batting 資料）
