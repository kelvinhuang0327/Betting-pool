# P28 Feature Bottleneck Audit
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 特徵覆蓋分析

| 狀態 | 特徵群組 | 說明 |
|------|---------|------|
| ✅ AVAILABLE | odds-implied baseline | Home/Away ML 隱含機率（已使用） |
| ✅ AVAILABLE | home/away split | 市場賠率隱含在內 |
| ⚠️ PARTIAL | starting pitcher | 姓名已知，品質（ERA/FIP）未載入 |
| ⚠️ PARTIAL | injury/lineup proxy | 僅 starter_known binary，無品質訊號 |
| ⚠️ PARTIAL | over/under calibration | OU 線已使用，Over/Under 賠率隱含機率未用 |
| ❌ MISSING | run-line signal | RL Home/Away 賠率在 CSV 但未使用 |
| ❌ MISSING | rolling team win rate | 可從 CSV 內部計算，但 walkforward 未實作 |
| ❌ MISSING | bullpen fatigue | 無資料來源 |
| ❌ MISSING | batting rolling form | 無資料來源 |
| ❌ MISSING | team defense metrics | 無資料來源 |
| ❌ MISSING | rest days | 無資料來源 |
| ❌ MISSING | travel/schedule fatigue | 無資料來源 |
| ❌ MISSING | weather/park factor | 無資料來源 |
| ❌ MISSING | AUC / discrimination metrics | 未在 artifacts 中計算 |

---

## 根本原因排名

| 排名 | 原因 | 影響程度 |
|------|------|---------|
| 1 | 特徵貧乏：僅用市場賠率衍生特徵 | **CRITICAL** |
| 2 | 市場映射：模型學習近恆等映射 | **CRITICAL** |
| 3 | 先發投手品質訊號缺失 | HIGH |
| 4 | 打線狀態缺失 | HIGH |
| 5 | Orchestrator 疊加引入雜訊（Brier 更差） | MEDIUM |
| 6 | 可用 CSV 欄位未充分使用（RL、Over odds） | LOW |

---

## Alpha Signals vs Walkforward 使用情況

| 項目 | 數量 |
|------|------|
| alpha_signals.py 定義特徵 | 318 |
| Walkforward 實際使用特徵 | **7** |
| 未使用特徵 | **311（97.8%）** |

**Alpha signals 完全沒有進入 MLB walkforward**。  
所有 318 特徵都依賴 `TeamSnapshot` / `BatterSnapshot` / `PitcherSnapshot` 物件，  
而這些物件在 MLB walkforward 中沒有被載入（使用市場賠率代理）。

---

## 資料缺口評估

| 缺口類型 | 是否可在 repo 內修復 | 修復成本 | 預估改善 |
|---------|-------------------|---------|---------|
| RL odds 轉為特徵 | ✅ 是（CSV 已有） | 低 | 極小（P28 測試：+0.000485 vs baseline）|
| Rolling win rate | ✅ 是（可從 CSV 計算） | 低 | 極小（P28 測試：included in CandB）|
| Pitcher ERA/FIP | ❌ 需外部資料 | 高 | 估計 -0.005 至 -0.015 |
| Batting wOBA | ❌ 需外部資料 | 高 | 估計 -0.003 至 -0.010 |
| 牛棚疲勞 | ❌ 需外部資料 | 高 | 估計 -0.002 至 -0.007 |

---

## 結論

當前 CSV 資料（市場賠率 + 球隊名稱 + 先發姓名）已達 repo 內特徵工程的天花板（Brier ≈ 0.245）。  
真正的 model quality 改善需要外部資料：Fangraphs、Baseball Reference、Statcast 等。  
下一步應規劃外部資料引入方案（paper-only research / data contract 設計）。
