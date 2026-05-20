# P29 Orchestrator Ablation Results
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 方法論

- **數據**：MLB 2025 CSV，2,428 遊戲（同 P28）
- **驗證**：5-fold walkforward，2,020 test games
- **Proxy 消融**：以數學公式模擬 Orchestrator components，不修改 production 路徑

---

## 完整結果表

| Variant | Brier | Δ vs Market | Δ vs LogReg | Δ vs Orch |
|---------|-------|-------------|------------|-----------|
| V0 市場賠率（pure market） | 0.244354 | — | -0.000751 | -0.004349 |
| V1 LogReg 7-feat（P28 baseline） | 0.245105 | +0.000751 | — | -0.003598 |
| V2 MARL w=0.30 sq×2 | 0.245736 | +0.001382 | +0.000631 | -0.002967 |
| **V3 MARL w=0.50 sq×2** | **0.244154** | **-0.000200** | **-0.000951** | **-0.004549** |
| V4 MARL V2 + regime noise | 0.245786 | +0.001432 | +0.000681 | -0.002917 |
| V5 LR(60%)+MARL_V2(40%) | 0.244604 | +0.000250 | -0.000501 | -0.004099 |
| V6 LR(80%)+MARL_V2(20%) | 0.244729 | +0.000375 | -0.000376 | -0.003974 |
| V7 MARL no-squeeze | 0.247584 | +0.003230 | +0.002480 | -0.001119 |
| **Full Orchestrator (reported)** | **0.248703** | +0.004349 | +0.003598 | — |

---

## 關鍵洞察

### 1. 純市場賠率 (V0) 是最佳 baseline（0.2444）
市場本身已是最準確的單一信號。LogReg 加了 OU / starter_known，反而輕微增加 Brier。

### 2. V3 (MARL w_market=0.50) 是最佳 MARL 設定（0.2442）
- 市場訊號權重從 0.30 提升至 0.50，Brier 改善 -0.001582 vs V2
- 說明 MARL 對市場權重的預設值 (0.30) 太低

### 3. Squeeze 有幫助（V2 < V7）
- no-squeeze (V7 = 0.2476) 比 with-squeeze (V2 = 0.2457) 更差
- Squeeze (×2) 拉大機率分布，實際上對 Brier 有益

### 4. Full Orchestrator 的超額損耗（+0.0043 vs market）
Full Orchestrator 比純市場賠率差 +0.0043，原因：
1. MARL w_market=0.30 太低（主要）
2. ES optimization 每 window 可能 overfit（次要）
3. mlb_regime_paper 額外 variance（次要）

---

## 推薦 Simplification Path

| 步驟 | 改動 | 預期 Brier |
|------|------|-----------|
| Step 1 | 提高 MARL w_market: 0.30 → 0.50 | ~0.244 |
| Step 2 | 移除 mlb_regime_paper ensemble | ~0.244 |
| Step 3 | 移除 ES optimization（固定 MARL 權重）| ~0.244 |

**預期總改善：0.2487 → ~0.244 (Δ ≈ -0.005)**

**全部為 diagnostic-only。不得 promotion，不替換 champion，不修改 production 預設路徑。**
