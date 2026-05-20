# P28 Final Validation Report
**Date**: 2026-05-20  
**Phase**: P28_MLB_MODEL_QUALITY_REPAIR  
**paper_only**: true | **diagnostic_only**: true

---

## 本輪目標

診斷 MLB model quality 瓶頸（Brier=0.2487），設計並評估修復 candidates，嘗試達成 Brier < 0.24。

---

## 驗證矩陣

| 驗證項目 | 結果 |
|----------|------|
| P26 tests（23個） | **23/23 PASS** |
| P17 standalone | **64/64 PASS** |
| P13-P17 regression | **296/296 PASS** |
| **合計** | **383/383 PASS** |
| JSON schema（5個 P28 artifacts） | **5/5 PASS** |
| Forbidden affirmative scan | **0 hits** |
| No index fallback | **PASS** |
| P23/P26 baseline 未被覆蓋 | **PASS** |
| MLB CSV 資料正確使用（無 future leakage） | **PASS** |
| fixed_edge_5pct champion 未替換 | **PASS** |
| Live API / TSL crawler 未修改 | **PASS** |

---

## Source Snapshot 狀態

| 項目 | P23/P26 Pinned | Current |
|------|---------------|---------|
| TSL Lines | 2,788 | 2,809（+21） |
| Action | — | 僅記錄，P28 使用 MLB CSV |

---

## Walkforward 結果摘要

| Model | Brier | Δ vs Re-eval | 結論 |
|-------|-------|-------------|------|
| Re-eval baseline (7-feat LogReg) | 0.245105 | — | baseline |
| A: Temperature scaling | 0.245535 | +0.000430 | NO_IMPROVEMENT |
| B: 13-feat expansion | 0.245590 | +0.000485 | NO_IMPROVEMENT |
| C: Market shrinkage | 0.245299 | +0.000194 | NO_IMPROVEMENT |
| Target | < 0.240 | — | **未達到** |

**關鍵發現：Simple 7-feat LogReg (0.2451) 優於 Full Orchestrator (0.2487)**

---

## 嚴格禁止確認

| 禁止事項 | 狀態 |
|---------|------|
| 合併 PR #2 | 未執行 |
| 聲稱可獲利 | 未聲稱 |
| 替換 fixed_edge_5pct champion | 未替換 |
| Strategy optimizer promotion | 未啟動 |
| 修改 TSL crawler / live odds API | 未修改 |
| 覆蓋 P23-P27 baselines | 未覆蓋 |
| Index fallback | 未使用 |
| Train-only 改善聲稱模型改善 | 未作 |
| 未授權外部資料 | 未使用 |

---

## 最終分類

**`P28_MODEL_REPAIR_NO_IMPROVEMENT`**

（vs re-evaluated baseline。None of A/B/C 改善 re-evaluated baseline Brier=0.2451）

---

## 額外關鍵發現

1. Orchestrator (0.2487) 比 Simple LogReg (0.2451) 差 → MARL/Elo 疊加引入雜訊
2. Feature ceiling 已達：所有 repo 內可用特徵都無法突破 0.245
3. 真正改善需要外部 pitcher/batting 資料（Fangraphs/Statcast）
4. CLV recheck 不符合資格（delta vs re-eval baseline > 0）
