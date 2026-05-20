# MLB 模型補丁驗證報告

**生成時間**: 2026-04-24T07:30:52.377664+00:00
**決策**: ⚠️  PARTIAL_KEEP

---

## 1. 補丁描述

| 欄位 | 值 |
|------|-----|
| Patch Task ID | #1354 |
| 任務名稱 | [Ensemble] MLB Calibration Patch: Platt + Isotonic + Regime Bias Correction |
| Signal State Type | `deep_research_calibration` |
| 類別 | `calibration` |
| Target Files | `wbc_backend/research/mlb_model_rebuild.py`, `wbc_backend/evaluation/mlb_decision_quality.py` |
| Expected Metric | 小 regime Brier score 改善 >= 2% |
| Insight ID | `07742efd` |
| Weakness | 各 regime 的 Brier score / LogLoss 基線未量化，校準器（Platt vs Isotonic）尚未對比 |

---

## 2. 統計說明

**樣本數**: 35 筆結算紀錄

**注意**: SNAPSHOT_COMPARISON: 35 before / 35 after predictions from calibration_patch_runner (task #1354). Method: ensemble_platt_iso_regime(alpha=0.00)

> 統計顯著門檻：樣本 ≥ 150，Brier 相對改善 ≥ 0.5%

---

## 3. BEFORE vs AFTER 指標

| 指標 | BEFORE | AFTER | 變化 |
|------|--------|-------|------|
| 樣本數 | 35 | 35 | — |
| Brier Score ↓ | 0.3022 | 0.1147 | ✅ -0.1875 ↓ |
| LogLoss ↓ | 0.8021 | 0.3685 | ✅ -0.4335 ↓ |
| Accuracy ↑ | 0.3714 | 0.8571 | ✅ +0.4857 ↑ |
| Avg ROI | 0.0000 | 0.0000 |  +0.0000 — |
| Avg CLV | N/A | N/A | — |
| CLV Records | 0 | 0 | — |

---

## 4. Regime 分解評估

| Regime | n | Brier ↓ | LogLoss ↓ | Accuracy ↑ | Avg ROI |
|--------|---|---------|-----------|------------|---------|
| Pool A | 8 | 0.2829 | 0.7603 | 0.3750 | -0.6500 |
| Pool B | 9 | 0.2883 | 0.7733 | 0.4444 | -0.2778 |
| Pool C | 9 | 0.3266 | 0.8550 | 0.3333 | -0.7567 |
| Pool D | 9 | 0.3089 | 0.8151 | 0.3333 | -0.6889 |

---

## 5. 統計顯著性評估

| 條件 | 狀態 |
|------|------|
| 樣本數 ≥ 150 | ❌ (actual: 35) |
| Brier 相對改善 ≥ 0.5% | ✅ |
| LogLoss 相對改善 ≥ 0.5% | ✅ |
| Stub Worker（未真實變更） | ✅ 無 |

---

## 6. 風險評估

_None identified_

---

## 7. 最終決策

### ⚠️  PARTIAL_KEEP

**決策理由**:

有部分改善訊號，但樣本數（35）低於推薦門檻（150）。建議累積更多數據後重新驗證。

---

## 8. 後續行動

1. Insight 狀態已更新為 `PARTIAL`
2. 建議累積 ≥ 150 筆新數據後重新執行驗證
3. 可在特定 regime 內謹慎應用

---

_此報告由 `orchestrator/patch_validator.py` 自動生成。請勿手動修改。_
