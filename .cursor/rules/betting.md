# ⚾️ 2026 WBC 經典賽：棒球領域規則與分析報告 (WBC Domain Rules)

此規則定義了 2026 WBC 賽事特性、投手限制與分析報告範式。

## 1. WBC 賽事特殊規則 (Mandatory)

### 用球數限制 (Pitch Count Limits)
| 賽程階段 | 單場上限 | 隔場限制 |
| :--- | :--- | :--- |
| 預賽 (Pool) | 65 球 | ≥30球 → 休1天; ≥50球 → 休4天 |
| 複賽 (2nd Round) | 80 球 | ≥30球 → 休1天; ≥50球 → 休4天 |
| 準決賽/決賽 | 95 球 | ≥30球 → 休1天; ≥50球 → 休4天 |

### 對模型開發的具體影響
- **先發局數**: 預賽先發投手通常僅能負擔 **3~4 局**，牛棚佔比 > 60%。
- **第二先發**: 某些球隊會採取 Piggyback Starter 調度，第二位投手的品質是隱藏關鍵。
- **投手調度**: 需要偵測教練團的調度風格與近三日牛棚用量。

## 2. 棒球核心預測指標
- **打者**: wOBA, OPS+, SwStr% vs Fastballs, High-leverage OPS.
- **投手**: FIP, WHIP, Stuff+, K/9, Platoon Splits (左右打對決).
- **球隊**: 防守效率 (DER), BaseRuns (預期勝率), Bullpen Depth Index.

## 3. 數據權重建議
| 數據來源周期 | 權重 | 說明 |
| :--- | :--- | :--- |
| 2025 世界 12 強賽 | 30% | 最近的國際大賽數據 |
| 2025 MLB/NPB/KBO 球季 | 35% | 過去一年的常規能力 |
| 2026 春訓 & 熱身賽 | 25% | **當前狀態 (Current Form)** |
| 歷屆 WBC 表現 | 10% | 國際賽經驗值 |

## 4. 預測報告輸出格式 (Report Template)
每一份生成的分析報告必須包含：
1. **核心指標對比**: 雷達圖數據。
2. **投捕對決分析**: 先發投手對陣打線。
3. **用球數與調度**: 預計換投時間點。
4. **下注建議 (TSL/運彩)**: 計算 EV% 與勝率。
    - 不讓分 (ML)、讓分 (RL)、大小分 (OU)、前五局 (F5)。
5. **關鍵變數 (X-Factors)**: 球星狀態、球場維度。

## 📍 參考更多詳細規則
- [platform_core.md](file:///Users/kelvin/Kelvin-WorkSpace/Betting-pool/.cursor/rules/platform_core.md) - 關於統計標準與策略 lifecycle。
- [.cursorrules](file:///Users/kelvin/Kelvin-WorkSpace/Betting-pool/.cursorrules) - 關於代碼風格與開發 SOP。
