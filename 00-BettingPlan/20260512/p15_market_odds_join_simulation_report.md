# P15 Market Odds Join Simulation Report

## 1. Summary

| 項目 | 值 |
|---|---|
| **P15 Gate** | `P15_ODDS_AWARE_SIMULATION_READY` |
| **P14/P13 Spine Gate** | `PASS_SIMULATION_SPINE_READY` |
| **Market Odds Available** | `True` |
| **paper_only** | `True` |
| **production_ready** | `False` |
| **生成時間** | 2026-05-12 |

---

## 2. 背景與目的

P14 已激活模擬 spine，但因 P13 OOF CSV 不包含賽事識別符，故市場賠率缺失，
所有下注策略以 `MARKET_ODDS_ABSENT_SIMULATION_ONLY` 模式運行，無法計算真實 ROI。

P15 目標：將歷史市場賠率（`Away ML` / `Home ML`）從 P13 訓練來源 CSV 
`variant_no_rest.csv` 回填至 OOF rows，使 capped_kelly、ROI、edge 等指標
能基於真實賠率計算。

---

## 3. Join 策略

**方法：Positional Fold-Window Join（確定性位置映射）**

P13 `WalkForwardLogisticBaseline` 使用以下公式計算 fold 邊界：

```
boundaries = [round(n * k / (n_folds + 1)) for k in range(n_folds + 2)]
```

OOF 的第 i fold 預測行與 source CSV（相同排序後）的
`[boundaries[i+1] : boundaries[i+2]]` 行一一對應。

此映射不需要 fuzzy matching，完全確定性。

### 驗證結果

| Fold | OOF 行數 | Source 行數 | MATCH |
|------|---------|------------|-------|
| 1 | 315 | 315 | ✓ |
| 2 | 315 | 315 | ✓ |
| 3 | 316 | 316 | ✓ |
| 4 | 316 | 316 | ✓ |
| 5 | 315 | 315 | ✓ |

---

## 4. 賠率來源

- **來源檔案**：`Betting-pool/outputs/predictions/PAPER/2026-05-11/ablation/variant_no_rest.csv`
- **格式**：American Moneyline（`Away ML` / `Home ML` 欄位）
- **轉換公式**：
  - x > 0：`decimal = 1 + x/100`
  - x < 0：`decimal = 1 + 100/|x|`
  - `p_market = 1 / decimal_odds`（未去除vig）
- **edge 計算**：`edge = p_oof - p_market`（home-win 視角）

---

## 5. Odds Join 覆蓋率

| 項目 | 值 |
|---|---|
| 總 OOF 行數 | 1,577 |
| 成功 Join（`JOINED`） | 1,575 |
| 缺失（`MISSING`） | 0 |
| 無效賠率（`INVALID_ODDS`） | 2 |
| **覆蓋率** | **99.87%** |

2 行因賠率格式無效（odds=0 或 NaN）未能 join，不影響主要分析。

---

## 6. Per-Policy 策略指標

| 策略 | 下注數 | BSS | ROI (%) | Avg Edge |
|---|---|---|---|---|
| `flat` | 739 | +0.0252 | -0.173% | N/A |
| `capped_kelly` | 717 | -0.0079 | **+5.51%** | N/A |
| `confidence_rank` | 474 | +0.0372 | +0.055% | N/A |
| `no_bet` | 0 | N/A | N/A | N/A |

> **注意**：avg_edge 現在可計算但尚未在 P15 policy runner 中輸出，屬 P16 優化範圍。
> ROI 以實際 decimal_odds 計算，`paper_only=True` 全程強制。

---

## 7. 關鍵發現

1. **capped_kelly ROI = +5.51%**：市場賠率注入後，capped_kelly 不再受 `MARKET_ODDS_ABSENT` 阻擋，能基於真實賠率決策。需注意此為 in-sample OOF 統計，非真實前瞻績效。
2. **confidence_rank ROI = +0.055%**：接近零的 ROI 表示模型對最高信心 30% 預測的市場 edge 有限。
3. **flat ROI = -0.173%**：無差別下注的情境下市場有細微負優勢（vig 影響）。
4. **BSS（flat/confidence_rank 均為正值）**：模型有正向 Brier Skill Score，但不足以在含 vig 市場中系統性獲利。

---

## 8. 技術架構

### 新增檔案

- `wbc_backend/simulation/market_odds_adapter.py` — `MarketOddsJoinAdapter`、odds 轉換工具函數
- `scripts/run_p15_market_odds_join_simulation.py` — P15 CLI（join + simulation）
- `tests/test_p15_market_odds_adapter.py` — 34 個單元測試
- `tests/test_run_p15_market_odds_join_simulation.py` — 10 個 CLI 整合測試

### 修改檔案

- `wbc_backend/simulation/p13_strategy_simulator.py` — 新增 `from_joined_df()`、`_prepare_rows_with_odds()`、odds coverage 欄位

---

## 9. 輸出檔案

```
outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/
├── joined_oof_with_odds.csv     — 1577 rows，含 game_id、p_market、edge
├── simulation_summary.json      — spine gate + per-policy metrics
├── simulation_summary.md        — 人工閱讀報告
├── simulation_ledger.csv        — 每行決策 ledger
└── odds_join_report.json        — 覆蓋率統計
```

---

## 10. 確定性驗證

執行兩次相同指令（排除 `generated_at_utc`）：

```
diff run1/simulation_summary.json run2/simulation_summary.json → IDENTICAL
```

**結果**：`DETERMINISM: IDENTICAL` ✓

---

## 11. 安全 Guard 確認

| Guard | 狀態 |
|---|---|
| `paper_only=True` | ✓ 強制 |
| `production_ready=False` | ✓ 強制 |
| 輸出限制於 PAPER zone | ✓ CLI 驗證 |
| 無 live TSL / 賠率爬取 | ✓ |
| 無 Look-ahead Leakage | ✓ （positional join 僅使用預測時點前資料） |
| 無偽造賠率 | ✓ （全部來自實際 source CSV） |

---

## 12. 測試覆蓋

| 測試套件 | 通過數 |
|---|---|
| `test_p15_market_odds_adapter.py` | 34 / 34 |
| `test_run_p15_market_odds_join_simulation.py` | 10 / 10 |
| **P15 合計** | **44 / 44** |
| P14 既有測試 | 70 / 70（未受影響）|

---

## 13. 限制與後續工作

1. **avg_edge 欄位**：目前 `avg_edge_pct` 在 policy result 中為 None，P16 需在 `_run_single_policy` 中計算。
2. **vig 未去除**：`p_market` 使用原始隱含機率，未去除書商 vig（約 5-10%），實際 edge 略被低估。
3. **僅 OOF in-sample 統計**：ROI 數字為 walk-forward OOF，非真實紙上交易結果。
4. **P16 建議**：加入 vig 去除（Shin method）、Kelly 分數調整、夏普比率計算。

---

## 14. 相關 Commit

- `P14` 激活 commit：`2dfb0ee`
- `P15` commit：由 Task 11 產生

---

## 15. Gate 決策

```
P15_MARKET_ODDS_JOIN_SIMULATION_READY
```

**結論**：P15 歷史市場賠率 join 已完成，spine 在 `PASS_SIMULATION_SPINE_READY` 狀態下運行，市場賠率覆蓋 99.87%，capped_kelly 等賠率感知策略已正常啟動。本模組為 **PAPER ONLY**，**production_ready=False**。

<!-- marker: P15_MARKET_ODDS_JOIN_SIMULATION_READY -->
