# P0 Market Probability Timestamp Leakage Audit

**日期**: 2026-05-20
**任務**: P0_MARKET_PROBABILITY_TIMESTAMP_LEAKAGE_AUDIT
**類型**: paper_only=true / diagnostic_only=true
**結論**: `P0_MARKET_BASELINE_LEAKAGE_CONFIRMED`

---

## 1. 背景

P29 proxy ablation 產出以下關鍵數字：

| 變體 | Brier |
|------|-------|
| V0 Market-only | 0.244354 |
| V3 MARL w_market=0.50 | **0.244154** |
| V1 LogReg baseline | 0.245105 |
| Full Orchestrator (reported) | 0.248703 |

CEO 二次審查指出：若 P29 ablation 的 `market_prob` 來自 `data/mlb_2025/mlb_odds_2025_real.csv`（已知為 post-season 單次快照），則上述所有數字可能建立在 closing/post-game leakage 之上，不可作為工程依據。

本報告完整稽核 P29 ablation 使用的 market probability 資料來源，輸出 pregame_safe 覆蓋率與 leakage 風險分類。

---

## 2. Pre-flight — P29 Market Prob 欄位追蹤

### 2.1 Source 檔案

```
data/mlb_2025/mlb_odds_2025_real.csv
```

### 2.2 P29 使用欄位

```python
# scripts/p29_orchestrator_noise_audit.py
h = american_to_prob(r.get("Home ML", ""))
games.append({
    "home_ml_p": h,   # ← 這就是所有 V0/V3 market_prob 的來源
    ...
})
```

`Home ML` 欄位透過 `american_to_prob()` 轉換為機率，即 V0 (pure market) 與 V3 (MARL w_market=0.50) 的 `market_prob`。

### 2.3 CSV 欄位清單

```
Date, Start Time (EDT), Away, Away Score, Home, Home Score, Status,
Away Starter, Home Starter, O/U, Over, Under, Away ML, Home ML,
Home RL Spread, RL Away, RL Home, source_file, source_type, is_verified_real
```

**關鍵缺失**: `snapshot_timestamp` 欄位**不存在**於 CSV（驗證結果：0/2430 rows 有 snapshot_timestamp）。

---

## 3. 逐行 Leakage 標註

**稽核方法**: 對 2,430 筆 CSV 行每筆標註以下欄位：

| 欄位 | 說明 |
|------|------|
| `source_file` | data/mlb_2025/mlb_odds_2025_real.csv |
| `source_row_id` | CSV 行號 (0-indexed) |
| `snapshot_timestamp` | None (欄位不存在) |
| `game_start_utc` | 由 Date + Start Time (EDT) 重建 |
| `pregame_safe` | false (全部) |
| `leakage_type` | post_game_proxy (全部) |

### 3.1 分類依據（四層證據）

**層 1 — CSV 結構**:
- `snapshot_timestamp` 欄位不存在 → 無法驗證任何 odds 為 pregame 快照
- `Status` 全部為 `"Final"` → 所有場次已完賽
- `is_verified_real` 全部為 `"False"` → 真實性未驗證

**層 2 — source_type 追蹤**:
- `source_type` 全部為 `"user_supplied_xlsx"` → 來自 `mlb-odds.xlsx` 單次人工上傳
- 無任何 API 時間戳或爬蟲捕捉記錄

**層 3 — MEMORY 2026-03-20 外部確認**:
> "mlb_odds_2025_real.csv 是 post-season 單次抓取（2026-03-18/19），全部 2430 場只有 1 個 snapshot，所有快照時間戳在賽後，沒有任何 pregame 時間點。"

**層 4 — historical_odds_ingestion.py QA 報告**:
```
genuine_decision_odds : 0
closing_fallback       : 1,493
post_game_proxy_count  : 2,396
```

---

## 4. 統計結果

### 4.1 pregame_safe 覆蓋率

| 指標 | 數值 |
|------|------|
| 總行數 | 2,430 |
| pregame_safe=true | **0 (0.0%)** |
| pregame_safe=false | 2,430 (100.0%) |
| 有效 market_prob 行數 | 2,428 |
| pregame_safe 門檻 | 80% |
| **通過門檻？** | **否** |

### 4.2 leakage_type 分布

| leakage_type | 行數 | 佔比 |
|--------------|------|------|
| `post_game_proxy` | **2,430** | **100.0%** |
| `none` | 0 | 0.0% |
| `closing_odds` | 0 | 0.0% |
| `missing_timestamp` | 0 | 0.0% |
| `unknown` | 0 | 0.0% |

*分類說明*: 所有行被標記為 `post_game_proxy` 而非 `missing_timestamp`，因為 MEMORY 2026-03-20 提供了確鑿的外部證據（post-season 單次快照），而非單純 timestamp 缺失的模糊情況。

### 4.3 MEMORY Timeline Tier 交叉比對

| MEMORY 分類 | 值 | 本審計一致性 |
|------------|-----|------------|
| `strict_4point` | 0 | ✅ |
| `3plus` | 0 | ✅ |
| `closing_only_pregame` | 0 | ✅ |
| `post_game_proxy_only` | 2,396 | ✅ (審計：2,430*) |
| `genuine_decision_odds` | 0 | ✅ (審計：0) |

*\*差異 34 筆：MEMORY 的 `no_data=34` 行在本審計中仍歸類為 post_game_proxy（無 snapshot_timestamp 且 MEMORY 確認為 post-season），保守計算一致。*

---

## 5. 對 P29 Brier 數字的影響估計

### 5.1 受污染的測試集規模

P29 walkforward 5-fold，測試集共 **2,020 場**（2,430 × 5/6 ≈ 2,025，實際 2,020）。

這 2,020 場的 `market_prob`（即 `home_ml_p`）**100% 來自 post_game_proxy 源**。

### 5.2 若移除 leakage 行後的 Brier

```
可用 pregame-safe 行 : 0
移除 leakage 後剩餘  : 0
可計算 Brier          : 不可能（0 行）
```

### 5.3 Leakage 對 P29 結論的影響

| P29 聲稱 | 實際含義 | 可信度 |
|----------|---------|--------|
| V0 市場基準 Brier=0.244354 | 「市場勝過簡單 LogReg」 | ❌ 基於 post-game proxy，可能反映 odds 在賽後被修正為最終走勢 |
| V3 w_market=0.50 Brier=0.244154 | 「更強市場信號改善 MARL」 | ❌ Δ=-0.0002 差異在 contaminated 輸入下不具統計意義 |
| MARL squeeze 為主要噪音源 | 合理假設 | ⚠️ 結構分析可能正確，但 Brier 量化無效 |
| 建議 w_market sweep | P1 可啟動 | ❌ 不可啟動，基準污染 |

### 5.4 Leakage 機制說明

Post-season 單次快照的 odds 問題：
1. **非 closing odds**：betting platform 在賽後可能顯示賽前最終賠率，但也可能已被覆寫
2. **確認偏誤風險**：若 odds 在賽後被回填（back-filled）或調整，則市場信號將帶有 outcome 方向的污染
3. **時間點不可驗證**：無 snapshot_timestamp → 無法排除 odds 為 post-game 調整值

---

## 6. 稽核腳本驗證

```
scripts/p0_market_probability_leakage_audit.py
```

**單元測試結果 (3/3 PASS)**:
- TEST1: 無 snapshot_timestamp → pregame_safe=False, leakage=post_game_proxy ✅
- TEST2: american_to_prob() 邊界值處理 ✅
- TEST3: brier() 計算正確性 ✅

---

## 7. Forbidden Affirmative Scan

針對本報告執行關鍵詞掃描，確認無生產提案、晉升聲明或獲利宣稱。

**結果: 0 hits** ✅

---

## 8. 決策輸出

### Final Classification

```
P0_MARKET_BASELINE_LEAKAGE_CONFIRMED
```

### 決策依據

1. **pregame_safe 覆蓋率 = 0.0%**（門檻 80%）
2. **leakage_type = post_game_proxy，2,430/2,430 行（100%）**
3. **MEMORY 2026-03-20 確認**：post-season 單次快照，無 pregame 時間點
4. **CSV 無 snapshot_timestamp 欄位**：物理上無法驗證任何 odds 為 pregame
5. **historical_odds_ingestion.py QA**：genuine_decision_odds=0

### P1 狀態

```
P1 w_market sweep → 暫停 (BLOCKED)
```

### 重新啟動 P1 的條件

需滿足以下任一條件：
1. 取得帶有 pregame snapshot_timestamp 的 MLB 歷史 odds 資料（external API，如 The Odds API / OddsJam historical）
2. 從 2026 regular season TSL 實時收集累積足夠 pregame snapshot（預計 2026 年 4 月起）
3. 以 TSL 現有 233 closing pairs（data/tsl_odds_history.jsonl）為基礎重做 P29，但樣本數需 ≥ 300 場以支撐統計推論

---

## 9. Champion 狀態

本報告不影響 champion。
- **Champion**: `fixed_edge_5pct`（維持不變）
- **Production path**: 未修改

---

## 10. 輸出 Artifact 清單

| 檔案 | 狀態 |
|------|------|
| `scripts/p0_market_probability_leakage_audit.py` | ✅ 已產出 |
| `data/paper_recommendations/p0_market_probability_leakage_audit_20260520.json` | ✅ 已產出（含 2,430 筆 per-row flag） |
| `report/p0_market_probability_leakage_audit_20260520.md` | ✅ 本文件 |
| `00-BettingPlan/20260520/p0_market_probability_leakage_audit_20260520.md` | ✅ 已產出 |

---

*paper_only=true | diagnostic_only=true | no_production_proposal | no_champion_swap | no_gain_claim | live_api_call=false*
