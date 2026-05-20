# P27 — Per-Market Clean CLV Isolation & OE Exclusion Study
**Date**: 2026-05-20  
**Final Classification**: P27_ALL_MARKETS_CLEAN_CLV_INCONCLUSIVE + P27_OE_EXCLUSION_NO_SIGNAL_RECOVERY  
**paper_only**: true | **diagnostic_only**: true

---

## 工程交接報告

### 1. 本輪目標

以 P26 line-aware matching 為基礎，對 MNL/HDC/OU/OE/TTO 五個市場做獨立 CLV isolation，評估 OE 是否造成 aggregate 稀釋，並輸出 market readiness decision 供後續規劃。

---

### 2. 已完成事項

| 項目 | 狀態 |
|------|------|
| Pre-flight 全面確認 | ✅ |
| Source snapshot drift 記錄（+20 records，不覆蓋 P23/P26） | ✅ |
| P23-P26 artifacts 全部存在確認 | ✅ |
| P26 module & tests 存在確認 | ✅ |
| `scripts/p27_per_market_clv_isolation.py` 實作與執行 | ✅ |
| 5 市場個別 clean CLV 計算（P26 line-aware matching） | ✅ |
| 每市場：N、mean、median、trimmed、CI、pos_rate、abs>10/25/50、top-1% | ✅ |
| 每市場 classification 輸出 | ✅ |
| OE exclusion study（9 aggregate combinations） | ✅ |
| 3 核心問題解答（Q1/Q2/Q3） | ✅ |
| Market readiness decision | ✅ |
| P26 tests 23/23 PASS | ✅ |
| P17 standalone 64/64 PASS | ✅ |
| P13-P17 regression 296/296 PASS | ✅ |
| JSON schema 4/4 PASS | ✅ |
| Forbidden affirmative scan 0 hits | ✅ |
| No index fallback 確認 | ✅ |
| 9 artifacts 產出（4 JSON + 4 MD + 1 BettingPlan） | ✅ |

---

### 3. 修改或產出的檔案

**新增腳本**:
- [`scripts/p27_per_market_clv_isolation.py`](../../scripts/p27_per_market_clv_isolation.py)

**JSON Artifacts (4個)**:
- `data/paper_recommendations/p27_per_market_clean_clv_isolation_20260520.json`
- `data/paper_recommendations/p27_oe_exclusion_study_20260520.json`
- `data/paper_recommendations/p27_market_readiness_decision_20260520.json`
- `data/paper_recommendations/p27_source_snapshot_drift_20260520.json`

**Report MDs (4個)**:
- `report/p27_per_market_clean_clv_isolation_20260520.md`
- `report/p27_oe_exclusion_study_20260520.md`
- `report/p27_market_readiness_decision_20260520.md`
- `report/p27_final_validation_20260520.md`

---

### 4. 驗證結果

| 驗證 | 結果 |
|------|------|
| P26 tests 23/23 | **PASS** |
| P17 standalone 64/64 | **PASS** |
| P13-P17 regression 296/296 | **PASS** |
| 合計 383/383 | **PASS** |
| JSON schema 4/4 | **PASS** |
| Forbidden scan | **0 hits** |
| No index fallback | **PASS** |

---

### 5. 目前結論

**Per-Market Clean CLV（P26 line-aware）**:

| Market | N | Mean% | CI (95%) | CI∋0 | 分類 |
|--------|---|-------|----------|------|------|
| MNL | 681 | +0.0449 | [-0.22, +0.30] | Yes | INCONCLUSIVE |
| HDC | 402 | -0.0027 | [-0.32, +0.32] | Yes | INCONCLUSIVE |
| OU | 418 | +0.0377 | [-0.25, +0.33] | Yes | INCONCLUSIVE |
| OE | 460 | +0.0083 | [-0.07, +0.09] | Yes | INCONCLUSIVE |
| TTO | 370 | +0.0815 | [-0.31, +0.47] | Yes | INCONCLUSIVE |

**OE Exclusion**:
- OE 輕微稀釋（+0.006pp），但排除後 CI 仍穿越 0（[-0.12, +0.20]）
- CI 反而略微變寬（OE 貢獻了穩定的 N=460 接近 0 觀測）
- **無信號恢復**

**根本原因**：樣本量不足（N=236 valid pairs，~2,300 observations）、模型品質不足（MLB Brier=0.2487）。

---

### 6. 尚未完成事項

- MNL team alias MISSING_OUTCOME 詳細調查（目前僅知 3 pairs，1.3%）
- HDC LINE_MOVED 比率隨賽季的時間序列分析
- OE 從 aggregate 的永久排除機制實作

---

### 7. 風險與不確定點

| 風險 | 說明 |
|------|------|
| MNL MISSING_OUTCOME | 若 team alias 差異比預期多，MNL N=681 可能高估有效樣本 |
| TTO 不穩定 | LINE_MOVED rate 14.7%（最高）+ CI 最寬，是最不可信的市場 |
| 樣本積累速度 | 每週約 +5-10 pairs，需要 3-6 個月才能達到 N=500 |
| 模型品質前提 | CLV 訊號依賴模型預測準確度；若 Brier 不改善，CLV 即使顯著也無法利用 |

---

### 8. 建議下一輪優先處理方向

**P28 — Model Quality Repair（Brier 從 0.2487 → 目標 < 0.24）**

理由：
1. CLV 訊號的有效利用以模型品質為前提
2. 目前所有市場 CLV CI 穿越 0，主要原因是預測能力接近隨機
3. 投資模型改善比繼續追 CLV 訊號更有前景
4. MLB walkforward 回測是目前最可靠的量化評估基礎

具體方向：
- 特徵工程：擴充 BABIP、FIP-/FIP、barrel rate、sprint speed 等 Statcast 特徵
- 校準修復：Platt Scaling 在全量 MLB 資料上的應用
- 回測框架：確保 walk-forward 無 look-ahead leakage

---

### 9. 下一輪可直接執行的 task prompt

```
請執行 P28 — MLB Model Quality Repair (Brier < 0.24 Target)：
背景：P27 確認所有市場 clean CLV CI 穿越 0，根本原因之一是模型品質不足
（MLB walkforward Brier = 0.2487，接近 random baseline 0.25）。

1. Pre-flight：確認 P23-P27 artifacts，確認 source snapshot drift 僅記錄
2. 分析現有特徵集（alpha_signals.py）找出 Brier 瓶頸
3. 設計並實作至少 3 個新特徵群組（Statcast-based proxy 可接受）
4. 重跑 MLB walkforward backtest，目標 Brier < 0.24
5. 若 Brier 改善，重跑 P26 line-aware CLV diagnostic，觀察 CI 是否收窄
6. 所有 artifacts paper_only=true / diagnostic_only=true
7. 不作 production proposal / champion replacement / optimizer promotion
8. 產出 data/paper_recommendations/p28_*.json 和 report/p28_*.md
9. P26 tests + P17 standalone + P13-P17 regression 全 PASS
```

---

### 10. CTO Agent 摘要（10 行）

P27 完成 per-market clean CLV isolation 與 OE exclusion study，使用 P26 line-aware matching（P23/P26 pinned snapshot，2,788 lines）。五個市場（MNL/HDC/OU/OE/TTO）的 clean CLV 95% bootstrap CI 均穿越 0，median 均為 0，無任何市場達到 WEAK_STABLE 程度，final classification = P27_ALL_MARKETS_CLEAN_CLV_INCONCLUSIVE。OE 確認為結構性無訊號（positive rate 僅 15.65%，|CLV|>10% = 0），排除 OE 後 CI 仍穿越 0（[-0.12,+0.20]）且略微變寬，sub-class = P27_OE_EXCLUSION_NO_SIGNAL_RECOVERY。23/23 P26 tests + 64/64 P17 + 296/296 P13-P17 = 383/383 PASS，4/4 JSON schema PASS，forbidden scan 0 hits。根本原因為樣本不足（N=236 pairs）+ 模型品質不足（Brier=0.2487）；建議 P28 先做 model quality repair（目標 Brier<0.24），champion=fixed_edge_5pct 維持，promotion frozen。
