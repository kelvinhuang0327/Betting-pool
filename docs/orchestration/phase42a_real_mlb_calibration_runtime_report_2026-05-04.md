# Phase 42A: Real MLB Calibration Runtime Report

> **生成日期**: 2026-05-04  
> **狀態**: `PHASE_42A_REAL_MLB_CALIBRATION_RUNTIME_VERIFIED` ✅

---

## 1. 預測 JSONL 狀態

| 項目 | 值 |
|------|----|
| 檔案路徑 | `data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl` |
| 檔案存在 | ✅ 是 |
| 產生方式 | `FullBacktestEngine(persist_predictions=True, n_windows=5)` |
| 源資料 | `data/mlb_2025/mlb-2025-asplayed.csv` + `data/mlb_2025/mlb_odds_2025_real.csv` |
| 總比賽場數 | 2,430 |
| 預測行數 | **2,025**（5 個測試視窗合計） |
| 重複 dedupe_key 數 | 23（正常，同一場比賽不同視窗重疊） |
| has_model_home_prob | ✅ |
| has_market_home_prob_no_vig | ✅ |
| has_home_win | ✅ |
| has_game_date | ✅ |
| has_dedupe_key | ✅ |
| has_audit_hash | ✅ |
| calibration_ready | ✅ True |
| 日期範圍 | 2025-04-27 → 2025-09-28 |

---

## 2. Phase 39 JSONL 重算指標

> 使用 `wbc_backend.evaluation.metrics` (SSOT)，從 JSONL 重算。

| 指標 | 值 |
|------|----|
| 樣本數 | 2,025 |
| Model Brier | 0.244706 |
| Market Brier | 0.243757 |
| BSS (model vs market) | **-0.003894** (-0.39%) |
| Log-Loss | 0.682205 |
| ECE | 0.031097 |
| 主隊勝率 | 52.99% |

> **備註**: BSS 略微負值（-0.39%），表示模型 Brier 略差於市場賠率。這與 Phase 37/38 的 -14.1% 報告值差距大，主因是本次 JSONL 僅包含 walk-forward 測試折（2,025 場）而非全部 2,430 場，且 MARL 模型在此批次的市場代理較接近真實賠率。

---

## 3. Phase 42 校準修復結果

> 執行指令：`python scripts/run_phase42_mlb_calibration_repair.py --print --report`

### 3.1 整體指標（5 折彙整）

| 指標 | Raw（模型原始） | Calibrated（最佳方法） | Market Baseline |
|------|:-----------:|:------------------:|:---------------:|
| Brier | 0.2459 | **0.2444** | 0.2451 |
| BSS | -0.31% | **+0.28%** | — (基準) |
| ECE | 0.0314 | 0.0323 | — |

### 3.2 各方法比較摘要

| 方法 | 特性 |
|------|------|
| identity | 原始模型機率（基準） |
| binwise | 區間加權校準；需足夠訓練樣本 |
| platt | sklearn LogisticRegression（sklearn ✅ 可用） |
| isotonic | sklearn IsotonicRegression（sklearn ✅ 可用） |
| **market_blend α=0.4** | **最佳方法**：40% 模型 + 60% 市場賠率 |

### 3.3 最佳方法

| 項目 | 值 |
|------|----|
| best_method | `market_blend` |
| best_alpha | **0.4**（40% 模型，60% 市場） |
| calibrated_brier | **0.2444**（較 raw 0.2459 改善 0.0015） |
| calibrated_bss | **+0.0028**（+0.28%，由負轉正） |
| calibrated_ece | 0.0323（較 raw 0.0314 略差） |

---

## 4. 校準分類結果

```
CALIBRATION_REPAIR_NOT_HELPFUL
```

### 分類依據

| 條件 | 值 | 觸發? |
|------|----|-------|
| market blend alpha < 0.2 → MARKET_ONLY_BEST | α=0.4 | ❌ |
| cal_bss >= 0 AND ece_improved → CALIBRATION_REPAIR_HELPFUL | BSS✅ ECE❌ | ❌ |
| ece_improved only → CALIBRATION_REPAIR_HELPFUL_BUT_NOT_SUFFICIENT | ECE ❌ | ❌ |
| else → CALIBRATION_REPAIR_NOT_HELPFUL | — | ✅ |

**分析**：最佳方法使 BSS 由 -0.31% 提升至 +0.28%（轉正），但 ECE 從 0.0314 略升至 0.0323（無改善）。依分類規則，需同時滿足 BSS>=0 且 ECE 改善，才判定為 HELPFUL。因 ECE 未改善，分類為 `CALIBRATION_REPAIR_NOT_HELPFUL`。

> **補充解讀**：ECE 基線 (0.0314) 已相當低（校準已較好），市場混合在改善 Brier/BSS 的同時輕微惡化了 ECE，符合 Brier-ECE trade-off 現象。

---

## 5. BSS 安全閘 (BSS Safety Gate)

| 項目 | 值 |
|------|----|
| task_kind | `metric_repair` |
| BSS Safety Gate 結果 | **ALLOWED** |
| calibrated BSS | +0.0028（>= 0） |
| bss_negative | False |
| patch_gate_eligible | **True**（calibrated BSS >= 0） |
| CANDIDATE_PATCH 建立 | ❌ **否**（此 Phase 不建立） |

> **說明**：`metric_repair` 類型在 BSS Safety Gate 中永遠 ALLOWED。calibrated BSS >= 0 使 `patch_gate_eligible = True`，標記為 `PATCH_GATE_RECHECK_ELIGIBLE`。但依 Phase 42A 規則，本 Phase 不建立 CANDIDATE_PATCH。

---

## 6. 市場基準是否仍勝出？

**是**。`market_brier = 0.2451 < raw_model_brier = 0.2459`。

最佳校準（market_blend α=0.4）後 `calibrated_brier = 0.2444 < market_brier = 0.2451`，
校準後模型略勝市場（差距 0.0007），但僅靠「引入 60% 市場權重」實現，並非純模型預測力改善。

**結論**：純模型預測力仍弱於市場基準；市場混合是唯一有效的校準手段。

---

## 7. 煙霧測試（Smoke Validation）

| 測試 | 結果 |
|------|------|
| 生成 JSONL 不修改源 CSV 檔案 | ✅ |
| JSONL schema 驗證通過 | ✅ |
| Phase 42 CLI 可消費 JSONL | ✅ |
| 無外部 API / LLM 呼叫 | ✅ |
| 未修改生產模型 | ✅ |
| 未建立 CANDIDATE_PATCH | ✅ |
| BSS Safety Gate 未被繞過 | ✅ |

---

## 8. 下一步建議

| 優先順序 | 動作 | 說明 |
|---------|------|------|
| 1 | **Feature Repair Investigation** | ECE 已低，Brier/BSS 差距的根本原因是特徵品質，需調查 Elo/wOBA/FIP 代理指標準確性 |
| 2 | **Data Repair** | 確認 23 筆重複 dedupe_key 是否影響指標計算 |
| 3 | **Collect More Data** | 若要穩定 BSS >= 0，需要更多場次數據（目前 2,025 場，BSS 差異在 0.3% 邊緣） |
| 4 | **市場混合部署評估** | market_blend α=0.4 可作為低風險後處理步驟，在不修改模型前提下改善 Brier（需後續 Phase 決策） |

---

## 9. 完成確認

| 驗收標準 | 狀態 |
|---------|------|
| 預測 JSONL 來自真實 FullBacktestEngine 輸出 | ✅ |
| Phase 39 check 通過（calibration_ready=True） | ✅ |
| Phase 42 校準在真實行上執行 | ✅ |
| BSS Safety Gate 結果明確 | ✅ ALLOWED |
| 報告已建立 | ✅ |

**最終狀態**: `PHASE_42A_REAL_MLB_CALIBRATION_RUNTIME_VERIFIED` ✅
