# P25 CLV 失敗根因稽核報告

**Phase**: P25 — CLV Inconclusive Root-Cause Audit & Model Quality Repair Plan  
**Date**: 2026-05-20  
**Classification**: `P25_CLV_FAILURE_ROOT_CAUSE_AUDIT_COMPLETED`  
**Constraints**: `paper_only=true` / `diagnostic_only=true` / 無生產提案

---

## 執行摘要

P24 已確認 CLV 為 **INCONCLUSIVE**（bootstrap 95% CI [-0.019%, +0.776%] 跨越零，top-1% outlier 貢獻 110.57% 總 CLV sum）。本報告對 7 個根因候選項進行深度稽核，確定 **主因為 CLV Construction Bug（HDC/OU/TTO 跨 line 比較）**，次因為 **Outlier Artifact**，輔因為 **Model Quality Insufficient**。

---

## 一、根因稽核架構

調查 7 個候選根因：

| ID | 候選根因 | 調查方法 | 最終嚴重度 |
|---|---|---|---|
| A | 模型品質不足 | walkforward_summary + calibration_compare + gate_validation | **HIGH** |
| B | 市場賠率對齊 | Outcome name matching audit (pre vs close) | **CRITICAL** |
| C | CLV Construction | Gap analysis, formula review, look-ahead check | **HIGH** |
| D | Outlier Artifact | Top-25 case analysis, contribution decomposition | **CRITICAL** |
| E | Market Taxonomy / Side Mapping | All 5 markets outcome name analysis | **MEDIUM** |
| F | 樣本數量不足 | Per-market pair count, CI width analysis | **LOW** |
| G | 推薦政策錯位 | CLV vs model edge conceptual review | **MEDIUM** |

---

## 二、主要發現

### 根因 B+D（CRITICAL）：HDC/OU/TTO 跨 Line CLV 比較

**這是 CLV INCONCLUSIVE 的主要技術根因。**

TSL odds history 中，HDC（讓分）、OU（大小分）、TTO（球隊總分）的 outcome name 包含 **盤口線（line）**：

- HDC 範例：`底特律老虎 -2.5` / `密爾瓦基釀酒人 +2.5`
- OU 範例：`大 7.5` / `小 7.5`
- TTO 範例：`大 4.5` / `小 4.5`

當 pregame 和 closing 之間 **盤口線改變**（line shift），outcome name 也跟著改變（例如 pregame=`-1.5` → closing=`-2.5`）。但現有 CLV 公式以 **index 位置**（index 0 = side A，index 1 = side B）比較賠率，而非以 outcome name 比較。

**結果**：CLV = `(pregame_odds_on_-1.5 - closing_odds_on_-2.5) / closing_odds_on_-2.5`，這是在比較**不同盤口的賠率**，數學上沒有意義。

**量化影響**：
- HDC: 28/229 pairs (12.2%) 發生 name mismatch，產生 17 個 |CLV| > 50% 的極端值
- TTO: 32/217 pairs (14.7%) name mismatch，最高比例
- OU: 21/230 pairs (9.1%) name mismatch

**Top outlier 模式**：
```
match 3468261.1 | HDC | 底特律老虎 -2.5 | pre=2.9 → clo=1.4 | CLV = +107.14%
match 3467671.1 | HDC | 匹茲堡海盜 -2.5 | pre=2.9 → clo=1.45 | CLV = +100.00%
```

這些數字反映的是「pregame 某一 handicap line 的賠率」與「closing 不同 handicap line 的賠率」之比，不是真實的市場效率訊號。

---

### 根因 A（HIGH）：模型品質不足

| 指標 | 數值 | 基準 / 意涵 |
|---|---|---|
| MLB Walkforward Brier | 0.2487 | 隨機基準 = 0.25；delta = -0.0013（近乎隨機）|
| ML Hit Rate | 46.25% | 低於 50% break-even — 比擲硬幣更差 |
| ML ROI (Platt) | -1.1% | 負收益 |
| OU ROI | -12.2% | 強烈負值 |
| WBC Ensemble Brier | 0.1415 | N=40（太小，CI 不可靠）|
| Platt ECE | 3.52% | 校準本身可接受 |
| Isotonic ECE | 4.40% | 校準本身可接受 |

**結論**：即使 CLV construction bug 修復後，現有模型的辨別能力（discriminative ability）不足以持續打敗市場效率。校準（calibration）品質可接受，但底層預測準確率不夠。

---

### 根因 C（HIGH）：CLV Construction 已知問題

1. **53% closing window < 30 分鐘前**：技術上合法，但若 TSL 在開賽後仍更新賠率，存在微小 in-play 風險（本次 `same_timestamp_pre_clo=0`，無 look-ahead）
2. **OE 市場無資訊含量**：std=0.84%，68.7% 觀測值接近 0 CLV，稀釋整體統計

---

### 根因 G（MEDIUM）：政策錯位

CLV 衡量的是「市場賠率如何移動」，而非「模型預測是否優於市場」。CLV = 0 不代表模型沒有價值；CLV > 0 也不代表模型有 edge。兩者需要分離評估。

---

## 三、根因排名

| 排名 | 根因 | 嚴重度 | 驅動因素 |
|---|---|---|---|
| 1 | CLV_CONSTRUCTION_RISK | **CRITICAL** | HDC/OU/TTO 跨 line 比較產生人工極端值 |
| 2 | OUTLIER_DRIVEN | **CRITICAL** | Top-1% outlier 貢獻 110.57%，正 CLV mean 完全是 artifact |
| 3 | MODEL_QUALITY_INSUFFICIENT | **HIGH** | Brier≈random，hit rate < 50% |
| 4 | MARKET_MAPPING_RISK | **HIGH** | MNL 混合 2/3 路市場；HDC/OU/TTO line-name 不一致 |
| 5 | POLICY_MISMATCH_CONFIRMED | **MEDIUM** | CLV 不是模型 edge 的有效代理指標 |

---

## 四、修復優先序

| 優先級 | 行動 | 預期結果 |
|---|---|---|
| P1 立即 | 修正 CLV 計算：使用 name matching 非 index matching | 消除 top-1% outlier artifact；CLV mean 預計趨近 0 |
| P2 高 | 修復後重跑 CLV 分析，重新分類 | 確認 INCONCLUSIVE 是否仍成立（預期仍成立，但更乾淨） |
| P3 中 | 模型品質提升：重新設計特徵 + WBC 專屬訓練 | 需 ≥1500 局歷史，backtest 驗證 |
| P4 低 | OE 市場排除 | 提升統計清晰度 |

> **所有修復均為 paper_only / research_only，不得提案生產部署**

---

## 五、約束確認

- ✅ `paper_only=true`
- ✅ `diagnostic_only=true`
- ✅ 無生產提案 / 無盈利聲明
- ✅ 未修改 TSL crawler 或 live odds API
- ✅ `fixed_edge_5pct` champion 未受影響
- ✅ 使用 P23-pinned slice（2788 行）

---

*Artifact*: `data/paper_recommendations/p25_clv_failure_root_cause_audit_20260520.json`
