# P25 CLV 失敗根因稽核 — BettingPlan

**Phase**: P25  
**Date**: 2026-05-20  
**Status**: COMPLETE  
**Classification**: `P25_CLV_FAILURE_ROOT_CAUSE_AUDIT_COMPLETED`

---

## 核心結論

P24 CLV = INCONCLUSIVE 的**主要技術根因**已確認：

> **CLV construction bug** — HDC/OU/TTO 市場在盤口移動時，CLV 公式跨盤口比較賠率，產生 +107%/+100% 等人工極端值。Top-1% outlier 貢獻 110.57% 總 CLV sum，正 CLV mean (+0.362%) 完全是 artifact。

---

## 根因排名

| # | 根因 | 嚴重度 |
|---|---|---|
| 1 | CLV Construction Bug（HDC 12.2% / TTO 14.7% / OU 9.1% name mismatch） | **CRITICAL** |
| 2 | Outlier Artifact（top-1% = 110.57% contribution） | **CRITICAL** |
| 3 | Model Quality Insufficient（Brier=0.2487，hit_rate=46.25%）| HIGH |
| 4 | Market Mapping Risk（MNL 2/3-way 混合）| HIGH |
| 5 | Policy Mismatch（CLV ≠ model edge）| MEDIUM |

---

## Champion 狀態

- `fixed_edge_5pct`：**PRESERVED / HOLD 維持**
- 推廣：**FROZEN**
- 生產提案：**NONE**

---

## 下一步

| 行動 | 性質 |
|---|---|
| 修正 CLV：name matching 非 index matching | Research only |
| 修復後重跑 CLV bootstrap 分類 | Research only |
| 模型品質提升研究（≥1500 局 backtest） | Research only |

---

## 測試

- P17: **64/64 PASS**
- P12-P17: **318/318 PASS**
- JSON Schema: **4/4 PASS**
- Forbidden scan: **0 hits**

---

**P25 COMPLETE** ✅  
*paper_only=true / diagnostic_only=true / no production proposals*
