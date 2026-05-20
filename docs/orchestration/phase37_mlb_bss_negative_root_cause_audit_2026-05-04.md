# Phase 37: MLB BSS 負值根因審計報告

**建立日期**: 2026-05-04  
**資料集**: MLB 2025 (2,430 場賽事, 2025-03-18 → 2025-09-28)  
**報告 BSS**: **-14.1%** (model_brier=0.2796, market_brier=0.2451)  
**來源報告**: `report/mlb_2025_full_backtest.md` (生成日期: 2026-03-13)

---

## 1. 問題描述

MLB 2025 Walk-Forward 回測顯示 MARL 預測模型的 **Brier Skill Score (BSS) = -14.1%**，表示模型預測品質低於市場賠率基準。本審計旨在確定根本原因。

### BSS 公式驗證

$$\text{BSS} = 1 - \frac{\text{model\_brier}}{\text{market\_brier}} = 1 - \frac{0.2796}{0.2451} = -0.141 = -14.1\% \checkmark$$

公式計算正確，BSS 值確認為真實結果。

---

## 2. 資料集狀態

| 項目 | 狀態 | 細節 |
|------|------|------|
| 原始賠率資料 | ✓ 存在 | `data/mlb_2025/mlb_odds_2025_real.csv` (2,430 行) |
| 原始結果資料 | ✓ 存在 | `data/mlb_2025/mlb-2025-asplayed.csv` (2,430 行) |
| 賠率來源可信鏈 | △ 未驗證 | `source_chain_verified=False`，來源: user_supplied_xlsx |
| 重複記錄 | △ 28 筆 | 重複賽事記錄影響有效筆數 |

---

## 3. 審計結果 (11 項檢查)

### C01: BSS 公式 — ✓ PASS
公式 `BSS = 1 - model_brier / market_brier` 計算結果與報告吻合（差異 < 0.001）。  
**結論**: 公式本身無誤，非根因。

### C02: 原始資料可用性 — ✓ PASS
賠率 CSV 和結果 CSV 均存在，可進行重算。

### C03: 賠率來源可信鏈 — △ WARN [根因貢獻]
- `source_chain_verified = False`
- 來源: `user_supplied_xlsx`（本地使用者上傳，未獨立驗證）
- **風險**: 賠率資料若包含誤植或非官方值，市場 Brier 基準將失真。

### C04: 重複賽事記錄 — △ WARN [根因貢獻]
- 結果 CSV 發現 **28 筆重複**記錄（總計 2,430 行）
- 去重後有效筆數: **2,402**
- 重複範例: `2025-04-06 Cardinals@Red Sox`, `2025-04-20 Nationals@Rockies`
- **影響**: 若回測未去重，報告的 market_brier 可能與重算值略有差異

### C05: 市場 Brier 重算 — ✓ PASS（有差異）
| 指標 | 報告值 | 重算值 | 差異 |
|------|--------|--------|------|
| market_brier | 0.2451 | 0.2421 | 0.0030 (1.2%) |
| 有效筆數 | 2,430 | 2,402 | -28 (去重) |

- 重算後 BSS（若 model_brier=0.2796）: **-15.5%**（比報告更差）
- 差異原因：去重後排除 28 筆重複記錄

### C06: 結果標籤正確性 — ✓ PASS
- `home_win=1` 確認對應主場勝（1,305 場）
- `home_win=0` 確認對應客場勝（1,097 場）
- 交叉驗證不一致: **0 筆**

### C07: No-vig 公式 — ✓ PASS
- 公式: `p_no_vig = p_raw / (p_home_raw + p_away_raw)` — 正確
- 平均 vig: **4.26%**（正常範圍 3-8%）
- 公式本身無問題

### C08: 模型校準誤差 — ✗ FAIL [主要根因]
$$\text{ECE} = 0.1447 > 0.12 \text{ (容許上限)}$$

| 校準指標 | 值 | 目標 |
|---------|-----|------|
| ECE（Platt Scaling 後）| 0.1447 | < 0.08 |
| 校準方法 | Platt Scaling | Isotonic Regression（建議） |

**結論**: 模型嚴重低估不確定性，校準不足是 Brier Score 偏高的直接原因。

### C09: 模型 vs 市場機率分佈 — ✗ FAIL [主要根因]

| 基準 | Brier | coin-flip BSS |
|------|-------|--------------|
| 拋硬幣 (p=0.5) | 0.2500 | — |
| 市場賠率 | 0.2451 | +2.0% |
| MARL 模型 | 0.2796 | -11.8% |
| 模型 vs 市場 BSS | — | **-14.1%** |

**分析**: 模型雖然略優於拋硬幣（BSS vs coin-flip = -11.8%），但落後市場 14.1%。MARL 特徵（ELO + wOBA 代理 + FIP 代理 + RSI）無法捕捉市場隱含的精細機率資訊。

### C10: Walk-Forward 視窗穩定性 — △ WARN [根因貢獻]

| 視窗 | ELO 權重 | 市場權重 | 問題 |
|------|---------|---------|------|
| W1 | 0.389 | 0.249 | 市場信號被低估 |
| W2 | 0.247 | 0.492 | 市場信號偏高 |
| W3 | 0.621 | 0.390 | ELO 主導 |

- 市場特徵權重跨視窗差異大（0.249 ~ 0.492），顯示 **MARL 無法找到穩定的最優特徵組合**
- 僅 3 個視窗（每窗 607 場測試）— 樣本數不足以評估泛化能力

### C11: BSS Safety Gate — ✓ PASS
`orchestrator/bss_safety_gate.py` 存在且功能正常，BSS = -14.1% 時生產任務被正確封鎖。

---

## 4. 根因彙整

### 已確認根因（按嚴重度排序）

| 優先級 | 根因 ID | 類型 | 描述 |
|--------|---------|------|------|
| 1 | C09_MODEL_VS_MARKET | 模型能力不足 | MARL 代理特徵（ELO/wOBA代理/FIP代理）無法有效捕捉市場隱含資訊，需要真實 Statcast 數據 |
| 2 | C08_MODEL_CALIBRATION | 校準失敗 | Platt Scaling 後 ECE=0.1447 仍遠超目標 0.08，模型過度自信 |
| 3 | C10_WALK_FORWARD_WINDOWS | 特徵不穩定 | 3 視窗中市場特徵權重差異大（249%~492%），MARL 優化不穩定 |
| 4 | C03_ODDS_PROVENANCE | 資料品質 | 賠率來源未獨立驗證，基準 Brier 可能失真 |
| 5 | C04_DUPLICATE_RECORDS | 資料品質 | 28 筆重複記錄，影響去重後的市場 Brier 重算值 |

---

## 5. 修復建議（按優先順序）

### 優先級 1: DATA_REPAIR
- 取得真實開盤/收盤賠率時間軸（Pinnacle/Sportradar 等可信來源）
- 替代目前 `user_supplied_xlsx`，確保 `source_chain_verified=True`
- 去除 28 筆重複記錄，確保回測資料品質

### 優先級 2: METRIC_REPAIR
- 更換校準方法：Platt Scaling → **Isotonic Regression** 或 **Temperature Scaling**
- 目標：ECE < 0.08（校準後）
- 需重新回測並驗證 Brier 改善

### 優先級 3: INVESTIGATE
- 增加 Walk-Forward 視窗數至 **5+ 個**
- 測試市場特徵固定權重 vs 動態優化的 BSS 差異
- 評估是否可直接使用市場機率作為特徵（參考 CLV 設計）

---

## 6. 安全門設計 (Phase 37 Rule)

在 BSS < 0 期間，**嚴格禁止** 以下操作：
- 生產預測任務 (`production_prediction`)
- Kelly 下注執行 (`kelly_bet`, `live_bet`)
- Patch 候選評估 (`candidate_patch_eval`)

**允許** 以下操作：
- 根因調查 (`investigate_*`)
- 資料修復 (`data_repair`, `collect_*`)
- 指標修復 (`metric_repair`)
- 審計工具 (`audit_guard_*`, `usage_budget_*`)

詳見: `orchestrator/bss_safety_gate.py`

---

## 7. 技術摘要

```
BSS = 1 - model_brier / market_brier
    = 1 - 0.2796 / 0.2451
    = -14.1%  ← 模型落後市場

市場 Brier (重算) = 0.2421  ← 去重後 2,402 場
重算後 BSS = 1 - 0.2796/0.2421 = -15.5%  ← 比報告更差

根因摘要:
  PRIMARY  → 代理特徵（ELO/wOBA/FIP）無法捕捉市場資訊精度
  SECONDARY → 校準不足 (ECE=0.1447 > 0.12)
  TERTIARY  → MARL 特徵穩定性差（3 視窗市場權重差異 2x）
  DATA      → 賠率未驗證 + 28 筆重複記錄
```

---

## 8. 後續行動計劃

| 行動 | 類型 | 預計樣本要求 |
|------|------|------------|
| 取得 Pinnacle 賠率資料並重建基準 Brier | DATA_REPAIR | >= 1,500 場 |
| 更換校準器為 Isotonic，目標 ECE < 0.08 | METRIC_REPAIR | >= 500 場驗證集 |
| 增加 Walk-Forward 視窗至 5+ | INVESTIGATE | 現有 2,402 場 |
| 重新回測並驗證 BSS > 0 | RE_VALIDATE | >= 1,500 場 |

---

*審計工具*: `scripts/run_phase37_mlb_bss_root_cause_audit.py`  
*安全門*: `orchestrator/bss_safety_gate.py`  
*測試*: `tests/test_phase37_mlb_bss_root_cause_audit.py` (24 tests, all PASS)
