# P24 CLV Robustness Diagnostic Report

**Phase**: P24 — CLV Robustness Diagnostic-Only  
**Date**: 2026-05-20  
**Branch**: codex/main-sync-20260516  
**Tags**: `paper_only=true` | `diagnostic_only=true` | `no_production_proposal`

---

## 摘要 (Executive Summary)

WBC 2026 台灣運彩 CLV 訊號經 P24 全面 robustness 診斷後，分類為 **INCONCLUSIVE（無法確認）**。正面平均 CLV (+0.36%) 完全由極端 outlier 所驅動——前 1% 極端值貢獻了 **110.57%** 的總 CLV 總和，其餘 99% 觀測值的平均值為負。在任何 outlier 修正方法（trimming、winsorization、removal）之下，訊號均消失。

---

## 一、資料來源與隔離

| 項目 | 數值 |
|------|------|
| 使用快照 | P23 pinned (data/tsl_odds_history.jsonl) |
| 快照行數 | 2,788 lines |
| SHA-256 | `ac1320de7efa23e645ffb81f27c9825634c3d63566ed8ccf5c62ee6cf7c94118` |
| 漂移 (P24 pre-flight) | +8 lines (已排除，使用 pinned slice) |
| 有效配對 | 236 pairs |
| CLV 觀測數 | 2,284 observations (5 market codes × ≤2 outcomes) |
| 前瞻性滲漏 | 無 — pregame ≥2h / closing ±2h 窗口規則 |

---

## 二、整體 CLV 統計

| 指標 | 數值 |
|------|------|
| N | 2,284 |
| 平均 CLV | +0.3622% |
| 中位數 CLV | 0.0% |
| 標準差 | 9.62% |
| 最小 | −62.15% |
| 最大 | +158.33% |
| 正值比率 | 36.16% (826/2284) |
| 負值比率 | 36.12% (825/2284) |
| 中性 (=0) | 27.72% (633/2284) |

---

## 三、Bootstrap 信賴區間分析 (n=5000, seed=42)

| 統計量 | 估計值 | 95% CI 下界 | 95% CI 上界 | 穿越零點 |
|--------|--------|------------|------------|---------|
| 平均 CLV | +0.3622% | −0.0186% | +0.7764% | **是** |
| 正值比率 | 36.16% | 34.19% | 38.18% | N/A |

**判定**：CI 穿越零點。在 5% 顯著水準下，平均 CLV 無法與零區別。

---

## 四、Outlier 敏感性分析

| 方法 | 移除數量 | 修正後平均 | 符號翻轉 |
|------|----------|-----------|---------|
| 原始均值 | — | +0.3622% | — |
| 移除 top 1% | 22 obs | **−0.0387%** | **是** |
| 移除 top 5% | 114 obs | −0.0068% | 否 |
| Winsorized (p5/p95) | — | +0.0168% | 否 |
| 5% Trimmed Mean | — | +0.0118% | 否 |
| 10% Trimmed Mean | — | +0.0072% | 否 |

**關鍵發現**：  
- Top 1% (22 觀測值) 貢獻了總 CLV 之 **110.57%** — 意即其餘 99% 的觀測平均為負值  
- Top 5% 貢獻了 **101.79%** — 同樣的結構性問題  
- 任何 outlier 修正後，訊號完全消失

---

## 五、分類判定

```
整體 CLV 分類: INCONCLUSIVE
```

| 分類標準 | 條件 | 實際結果 |
|---------|------|---------|
| ROBUST | CI 全正 AND sign-stable after removal | ✗ CI 穿越零點 |
| WEAK_STABLE | CI 不穿越零點 AND 正值後 removal | ✗ CI 穿越零點 |
| INCONCLUSIVE | CI 穿越零點 OR 移除後符號翻轉 | ✓ **兩者皆是** |
| NEGATIVE | 均值負 AND 移除後穩定負 | ✗ 均值正 |

---

## 六、Forbidden Claims 稽核

| 項目 | 狀態 |
|------|------|
| production_proposal | ✗ 無 |
| champion_replacement | ✗ 無 |
| profitability_claim | ✗ 無 |
| guaranteed_profit | ✗ 無 |
| live_api_call | ✗ 無 |
| crawler_modification | ✗ 無 |

---

## 七、結論

WBC 2026 CLV 訊號目前分類為 **INCONCLUSIVE**。以下三項事實共同確認：

1. **95% Bootstrap CI 穿越零** — 統計不顯著
2. **去除 1% 極端值後符號翻轉** — outlier dominated
3. **Trimmed/Winsorized 均值接近零** — 無穩健正邊緣

`fixed_edge_5pct` champion 維持現狀，不受此診斷影響。

> 本報告為純學術診斷，不構成任何下注建議或盈利主張。
