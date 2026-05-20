---
paths:
  - "models/**/*.py"
  - "wbc_backend/**/*.py"
---

# 📊 數據與模型統計規範 (Stats & Model Rules)

這些規則僅在編輯模型或數據分析核心時生效。

## 🎯 核心原則: Simplicity First
- 優先使用最簡單的模型（如簡單的線性回歸或規則引擎）。
- 僅在 ROI 提升顯著時（相對提升 > 2%）才使用更複雜的模型（如 XGBoost、LightGBM）。
- **原因**: 降低過擬合 (Overfitting) 的風險。

## 🧪 物理極限約束 (Physics Limits)
- 在 WBC 模型中，必須考慮投手用球數限制 (Pitch Count Limits)。
- 先發投手在預賽上限為 65 球。
- 所有的模型係數需具有可解釋性，避免單純的黑箱模型。

## 🚨 數據處理細節
- 加載數據時一律使用 `Pandas` 並明確指定 `dtype` 以節省記憶體。
- 分類特徵 (Categorical Features) 應優先使用 `LabelEncoder` 或 `OneHotEncoder`。
- 回測時樣本數必須至少覆蓋 **1500 筆** 歷史數據。
