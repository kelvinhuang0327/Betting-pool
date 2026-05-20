# P25 最終驗證報告

**Phase**: P25 — CLV Inconclusive Root-Cause Audit & Model Quality Repair Plan  
**Date**: 2026-05-20  
**Final Classification**: `P25_CLV_FAILURE_ROOT_CAUSE_AUDIT_COMPLETED`  
**Constraints**: `paper_only=true` / `diagnostic_only=true`

---

## 一、測試套件結果

| 測試套件 | 結果 | 通過數 |
|---|---|---|
| P17 獨立 | ✅ PASS | **64/64** |
| P12-P17 全回歸 | ✅ PASS | **318/318** |

---

## 二、Artifact 清單與 Schema 驗證

| Artifact | 類型 | paper_only | diagnostic_only | 狀態 |
|---|---|---|---|---|
| `p25_clv_failure_root_cause_audit_20260520.json` | JSON | ✅ true | ✅ true | ✅ OK |
| `p25_market_mapping_audit_20260520.json` | JSON | ✅ true | ✅ true | ✅ OK |
| `p25_outlier_case_review_20260520.json` | JSON | ✅ true | ✅ true | ✅ OK |
| `p25_model_quality_gap_audit_20260520.json` | JSON | ✅ true | ✅ true | ✅ OK |
| `report/p25_clv_failure_root_cause_audit_20260520.md` | MD | — | — | ✅ 存在 |
| `report/p25_market_mapping_audit_20260520.md` | MD | — | — | ✅ 存在 |
| `report/p25_model_quality_gap_audit_20260520.md` | MD | — | — | ✅ 存在 |
| `report/p25_final_validation_20260520.md` | MD | — | — | ✅ 本文件 |
| `00-BettingPlan/20260520/p25_clv_failure_root_cause_audit_20260520.md` | BettingPlan | — | — | ✅ 存在 |

**總計**：4 JSON + 4 MD + 1 BettingPlan = **9 artifacts** ✅

---

## 三、Forbidden Scan 結果

| 禁止項目 | 掃描結果 |
|---|---|
| 生產提案 (`production_proposal`) | ✅ 0 hits |
| 盈利聲明 (`profitability_claim`) | ✅ 0 hits |
| Champion 替換 (`champion_replacement_allowed`) | ✅ false on all |
| 推廣允許 (`promotion_allowed`) | ✅ false on all |
| 直播 API 呼叫 (`network_call`) | ✅ false on all |
| Crawler 修改 (`crawler_modified`) | ✅ false on all |

---

## 四、P25 根因稽核摘要

### 最終分類：`P25_CLV_FAILURE_ROOT_CAUSE_AUDIT_COMPLETED`

**主根因（CRITICAL）**：

1. **CLV_CONSTRUCTION_RISK** — HDC/OU/TTO 市場的 outcome name 包含盤口線（line）。當 pregame 到 closing 之間盤口移動，CLV 公式以 index 位置比較不同盤口的賠率，產生人工極端值。HDC: 12.2% pairs affected，17 個 |CLV|>50% 觀測值。

2. **OUTLIER_DRIVEN** — 因上述 construction bug，top-1% outlier 貢獻 CLV sum 的 110.57%，正的 CLV mean (+0.362%) 完全是 artifact，不反映真實市場效率優勢。

**次根因（HIGH）**：

3. **MODEL_QUALITY_INSUFFICIENT** — MLB walkforward Brier=0.2487（近乎隨機），ML hit rate=46.25%（低於 50% break-even），ML ROI=-1.11%。

4. **MARKET_MAPPING_RISK** — MNL 混合 2/3-way 市場（index-1 語意不一致）；HDC/OU/TTO line-name cross-comparison（見主根因）。

**輔根因（MEDIUM）**：

5. **POLICY_MISMATCH** — CLV 衡量市場效率移動，不是模型 edge；兩者需獨立評估。

---

## 五、修復優先序

| 優先級 | 行動 | 預期效果 |
|---|---|---|
| P1 立即 | 修正 CLV：使用 name matching，丟棄 name mismatch pairs | 消除人工極端值；CLV mean 預計趨近 0 |
| P2 高 | 修復後重跑 CLV bootstrap，重新分類 | 確認 CLV 是否仍 INCONCLUSIVE 或轉為 NEUTRAL |
| P3 中 | Model quality：重新設計特徵，WBC 專屬訓練（≥1500 局）| 提升 Brier 至 ≤0.22，hit rate > 50% |
| P4 低 | 補齊 7 個 model contract 時間戳欄位 | 使 Data Leakage 審計可執行 |

> ⚠️ P2-P4 均為 paper_only 研究方向，不允許推進至生產部署

---

## 六、資料源確認

- **P23 pinned snapshot**: 2788 行，sha256=`ac1320de7efa23e645ffb81f27c9825634c3d63566ed8ccf5c62ee6cf7c94118`
- **當前 tsl_odds_history.jsonl**: 2796 行（+8 drift，已記錄於 P24）
- **P25 分析**: 僅使用前 2788 行

---

## 七、Champion 狀態確認

- `fixed_edge_5pct` 狀態：**PRESERVED**
- 推廣：**FROZEN**
- HOLD 維持：**YES**
- P25 不修改任何策略或生產邏輯

---

**P25 COMPLETE** ✅
