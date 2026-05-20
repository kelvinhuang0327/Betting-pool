# P29 Orchestrator Noise Attribution Audit
**Date**: 2026-05-20  
**Phase**: P29_ORCHESTRATOR_NOISE_REMOVAL  
**paper_only**: true | **diagnostic_only**: true

---

## 背景

P28 發現：Full Orchestrator (Brier=0.2487) 比 Simple 7-feat LogReg (0.2451) 差 +0.0036。  
本報告識別造成此差距的具體 noise component。

---

## Orchestrator Pipeline 組件

```
PredictionOrchestrator.predict(record)
├── MARL PredictorParams.predict(record)      [always activated]
│   ├── elo_diff = (home_elo - away_elo) / 400  [默認 0]
│   ├── market = market_home_prob
│   ├── woba_diff, fip_diff, rsi_diff           [默認 0]
│   ├── score = w_elo(0.40)×elo_diff + w_market(0.30)×(market-0.5)×2 + ...
│   └── prob = sigmoid(score × 2)              ← score×2 squeeze
├── mlb_regime_paper.predict_record(record)   [activated ~20% of games]
│   ├── regime detection (4 regimes)
│   └── paper_prob + confidence adjustment
└── weighted_ensemble(marl:0.70, regime:0.30) → fused_prob
```

---

## 5-fold Walkforward 消融結果（N=2,020 test games）

| Variant | Brier | Δ vs LogReg | Δ vs Orch | Acc |
|---------|-------|-------------|-----------|-----|
| V0: 純市場賠率 | **0.244354** | -0.000751 | **-0.004349** | 55.5% |
| V1: LogReg (P28 baseline) | 0.245105 | 0 | -0.003598 | 55.5% |
| V2: MARL sim (w_mkt=0.30, sq=2) | 0.245736 | +0.000631 | -0.002967 | 55.5% |
| **V3: MARL sim (w_mkt=0.50, sq=2)** | **0.244154** | **-0.000951** | **-0.004549** | 55.5% |
| V4: MARL V2 + regime noise | 0.245786 | +0.000681 | -0.002917 | 55.4% |
| V5: Ensemble LR(60%)+MARL(40%) | 0.244604 | -0.000501 | -0.004099 | 55.8% |
| V6: Ensemble LR(80%)+MARL(20%) | 0.244729 | -0.000376 | -0.003974 | 55.9% |
| V7: MARL no-squeeze | 0.247584 | +0.002480 | -0.001119 | 55.5% |

---

## Noise Hypotheses 驗證

### H1：MARL score×2 壓縮（CONFIRMED）
- V0（純市場）= 0.244354 優於 V2（MARL w_mkt=0.30）= 0.245736
- MARL w_market=0.30 不足：市場訊號被低估
- **Brier cost = +0.001382 vs pure market**

### H2：squeeze vs no-squeeze（MINOR）
- V2（with squeeze）= 0.245736 vs V7（no squeeze）= 0.247584
- 有 squeeze 比無 squeeze **更好**！squeeze 實際上有幫助（拉離 0.5）
- 真正問題是 w_market=0.30 太低，不是 squeeze 本身

### H3：Ensemble 平均（CONFIRMED_BUT_MINOR）
- V5（LR+MARL）= 0.244604 < V1（LogReg alone）= 0.245105 → ensemble 幫助
- **Ensemble 本身不是問題；問題是 MARL 的 w_market 太低**

### H4：Regime 偵測噪音（CONFIRMED）
- V4（MARL + regime noise）= 0.245786 vs V2 = 0.245736
- Regime 偵測在 ~20% 遊戲上增加 Brier +0.00005（輕微但存在）

---

## 根本原因識別

**主要問題：MARL 的 w_market = 0.30 太低**

| 設定 | Brier |
|------|-------|
| 純市場（w_mkt=1.0 等效） | 0.244354 |
| MARL w_mkt=0.50 | 0.244154（最佳）|
| MARL w_mkt=0.30（現有） | 0.245736 |
| Full Orchestrator（reported） | 0.248703 |

市場賠率已是最佳單一預測器。MARL 的非市場特徵（Elo/wOBA/FIP）在 MLB walkforward 中全為默認值（差值≈0），因此只有 w_market 項有實際貢獻，且 0.30 的權重不足。

**次要問題：Full Orchestrator 的額外疊加**

Full Orchestrator (0.2487) 比 MARL proxy (0.2457) 還要差 +0.003，差距來自：
- ES 優化（每 window 重新優化 MARL 權重，可能過擬合）
- mlb_regime_paper 整合帶來的額外 variance
- Log-probability 空間融合引入的非線性

---

## Simplification Candidate

**P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND**

| 候選方案 | 預期 Brier | 改善 |
|---------|-----------|------|
| 調高 w_market 至 0.50 | ~0.244 | -0.005 |
| 使用純市場賠率 | 0.244 | -0.005 |
| Ensemble(LogReg 60% + MARL_w50 40%) | ~0.243 | -0.006 |

**這些都是 diagnostic-only candidates，不得 promotion，不替換 champion。**
