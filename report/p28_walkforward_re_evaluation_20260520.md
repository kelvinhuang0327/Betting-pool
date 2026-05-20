# P28 Walkforward Re-evaluation Report
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 兩個 Baseline 的說明

| Baseline | Model | Brier | N games |
|---------|-------|-------|---------|
| Reported (P23/P24/P25 reference) | Full Orchestrator (Elo+MARL+Bayesian) | **0.2487** | 2,188 |
| Re-evaluated (P28 diagnostic) | Simple 7-feat LogReg | **0.2451** | 2,020 |

**重要**：兩者使用不同 model 架構和不同 window 配置，不可直接比較。  
P28 所有 candidates 的「improvement」必須以 **re-evaluated baseline (0.2451)** 為準。

---

## Walkforward 結果（5-fold，N=2,020 test games）

| Model | Brier | Δ vs Reported | Δ vs Re-eval | Acc | ECE | 判斷 |
|-------|-------|---------------|-------------|-----|-----|------|
| **Baseline (7-feat)** | **0.245105** | -0.003598 | 0 | 55.5% | 0.0287 | — |
| A: Temp scaling | 0.245535 | -0.003168 | **+0.000430** | 55.5% | 0.0299 | NO_IMPROVEMENT |
| B: 13-feat expand | 0.245590 | -0.003113 | **+0.000485** | 54.7% | 0.0332 | NO_IMPROVEMENT |
| C: Mkt shrinkage | 0.245299 | -0.003404 | **+0.000194** | 55.4% | 0.0345 | NO_IMPROVEMENT |

---

## 關鍵發現

### 1. Orchestrator 比 Simple LogReg 更差
簡單 7-feat LogReg (0.2451) 優於 Full Orchestrator (0.2487)。  
這代表 Elo + MARL + Bayesian ensemble 疊加 **引入雜訊**，並非提升。

### 2. 所有 candidates 均未改善 re-evaluated baseline
- 最佳：C (market shrinkage)，Δ = +0.000194（仍略差）
- 最差：B (13-feat expand)，Δ = +0.000485
- 特徵擴充完全無效：RL odds、rolling win rate、market conviction 均未提供 alpha

### 3. 目標 Brier < 0.24 未達到
- Primary target 0.24：**未達到**
- Minimum useful delta -0.002（vs re-eval baseline）：**未達到**
- All candidates within ±0.0005 of re-evaluated baseline：**已達 feature ceiling**

---

## 目標完成狀況

| 目標 | 狀態 |
|------|------|
| Primary: Brier < 0.24 | ❌ 未達到 |
| Secondary: Δ Brier ≥ -0.005 | ❌ 未達到（vs re-eval） |
| Minimum: Δ Brier ≥ -0.002 | ❌ 未達到（vs re-eval） |
| Orchestrator 問題診斷 | ✅ 完成：Orchestrator 疊加引入雜訊 |
| Feature bottleneck 識別 | ✅ 完成：需外部 pitcher/batting 資料 |

---

## CLV Recheck 資格

依據規則：「僅當 best candidate Δ Brier ≤ -0.002 時才允許做 CLV recheck」  
**→ 不符合條件，本輪不執行 CLV recheck**

---

## 最終分類

**`P28_MODEL_REPAIR_NO_IMPROVEMENT`**  
（基於 re-evaluated baseline 的正確比較）

注意：若以 Reported baseline 0.2487 為參考，所有 candidates 顯示 USEFUL_IMPROVEMENT，  
但這是 walkforward 設定差異造成的假象，不代表真實模型改善。

---

## Champion 狀態

| 項目 | 狀態 |
|------|------|
| Champion | fixed_edge_5pct |
| 狀態 | PRESERVED |
| Promotion | FROZEN |
| 本輪影響 | 無，paper-only diagnostic |
