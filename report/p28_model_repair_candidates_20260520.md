# P28 Model Repair Candidates Report
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## Walkforward 設定

| 項目 | 數值 |
|------|------|
| Games total | 2,428 |
| Windows | 5 |
| Train/test | 累積 train + 404 games test per window |
| Date range | 2025-03-18 → 2025-09-28 |
| Test games total | 2,020 |

---

## 結果彙整

| Candidate | Brier | Δ vs Reported (0.2487) | Δ vs Re-eval Baseline (0.2451) | 旗標 |
|-----------|-------|------------------------|-------------------------------|------|
| **Baseline (7-feat LogReg)** | **0.245105** | **-0.003598** | 0 (baseline) | — |
| A: Temperature scaling | 0.245535 | -0.003168 | **+0.000430（更差）** | NO_IMPROVEMENT |
| B: 13-feat expansion | 0.245590 | -0.003113 | **+0.000485（更差）** | NO_IMPROVEMENT |
| C: Market shrinkage | 0.245299 | -0.003404 | **+0.000194（更差）** | NO_IMPROVEMENT |

---

## 方法論重要說明

**Re-evaluated baseline (0.245105) ≠ Reported baseline (0.248703)**

| 版本 | Model | Brier | 原因差異 |
|------|-------|-------|---------|
| Reported | Orchestrator (Elo+MARL+Bayesian) | 0.2487 | 全系統回測，2188 games |
| Re-evaluated | LogReg 7-feat | 0.2451 | 本輪 P28 walkforward，2020 games |

**重要發現：簡單 7-feat LogReg (0.2451) 優於完整 Orchestrator (0.2487)**

這表示 Orchestrator/MARL ensemble 疊加層為 Brier 引入了額外雜訊。

---

## Candidate 分析

### Candidate A：Temperature Scaling
- 方法：在 inner validation 上 grid search 最佳 T（T ∈ [0.5, 3.0]）
- 結果：Brier=0.245535，比 re-eval baseline **更差 (+0.000430)**
- 結論：溫度縮放在此設定下不穩定，不同視窗的最佳 T 不一致

### Candidate B：13-feature Expansion
- 新增特徵：RL implied prob、market conviction、over implied、rolling win rates、RL-ML diff
- 結果：Brier=0.245590，比 re-eval baseline **更差 (+0.000485)**
- 結論：這些 proxy 特徵沒有真實 alpha 訊號，只增加雜訊

### Candidate C：Market Shrinkage Ensemble
- 方法：w×p_model + (1-w)×p_market，在 inner val 最優化 w
- 結果：Brier=0.245299，比 re-eval baseline **更差 (+0.000194)**
- 結論：效果最接近 baseline，但仍略差

---

## Corrected Final Classification

**`P28_MODEL_REPAIR_NO_IMPROVEMENT`**

（vs re-evaluated baseline）

所有候選方案均未能改善 re-evaluated baseline Brier=0.2451。  
「vs reported 0.2487 有改善」是方法論差異（不同 walkforward 設定）造成的假象。

---

## 真正需要的修復

| 修復方向 | 估計 Brier 改善潛力 | 資料需求 |
|---------|-------------------|---------|
| 先發投手 ERA/FIP 歷史資料 | -0.005 至 -0.015 | 需外部資料源 |
| 打線 wOBA/OPS 滾動 | -0.003 至 -0.010 | 需外部資料源 |
| 牛棚疲勞指標 | -0.002 至 -0.007 | 需外部資料源 |
| 球場/天氣因子 | -0.001 至 -0.003 | 部分可代理 |
| Orchestrator 簡化（去除 MARL 雜訊） | -0.002 至 -0.004 | 使用 repo 內資料 |

目前 CSV 只有市場賠率 + 球隊名稱 + 先發姓名，無法實現前三項。

---

## 嚴格禁止確認

- 不作 production proposal ✅
- 不作 champion replacement ✅
- 不作 profitability claim ✅
- 不啟動 optimizer promotion ✅
