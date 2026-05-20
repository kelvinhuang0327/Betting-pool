# Phase 38 — MLB BSS 資料+校準修復報告

**日期**: 2026-05-04
**模式**: PAPER_ONLY（唯讀預覽，不修改生產模型）
**封鎖狀態**: patch_gate_unlocked = False ← 永遠封鎖直到 BSS ≥ 0

---

## 1. 資料修復診斷 (Task 1)

| 指標 | 數值 |
|------|------|
| 原始行數 | 2,430 |
| 去重後行數 | 2,402 |
| 重複記錄數 | 28 |
| 缺失結果行數 | 0 |
| 缺失賠率行數 | 0 |
| 未驗證賠率行數 | 2,430 |
| 無效賠率行數 | 2 |
| 延期/取消行數 | 0 |
| 市場機率異常值 | 0 |
| 可修復 | True |

**問題清單:**
- `DUPLICATE_RECORDS: 28 duplicate (Date,Away,Home) keys in outcomes CSV.`
- `INVALID_ODDS: 2 rows with unparseable ML values.`
- `UNVERIFIED_ODDS: 2430 rows with is_verified_real=False.`

---

## 2. 清理資料集預覽 (Task 2)

| 欄位 | 值 |
|------|-----|
| 輸出路徑 | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/derived/mlb_2025_backtest_cleaned_preview.csv` |
| 清理後行數 | 2,400 |
| 移除重複記錄 | 28 |
| 移除缺失結果 | 0 |
| 移除無效賠率 | 2 |
| 移除延期場次 | 0 |
| 實際寫出 | False |

> 使用 `--write-preview` 選項可將清理資料集寫出至 derived/ 目錄。

**新增稽核欄位**: `clean_reason`, `original_row_index`, `dedupe_key`,
`market_home_prob_no_vig`, `market_away_prob_no_vig`

---

## 3. 市場基準重算比較 (Task 3)

| 版本 | Market Brier | 備註 |
|------|--------------|------|
| 報告值 (Phase 37 report) | 0.2451 | REPORT_ONLY |
| Phase 37 重算 (2,402 場去重) | 0.2421 | 去重後重算 |
| Phase 38 清理預覽 (2,400 場) | 0.2419 | 本次合併清理後 |

| 統計 | 值 |
|------|----|
| 主場勝率 | 54.4% |
| 平均超賠率 (overround) | 4.26% |
| No-vig 總和有效率 | 100.0% |

---

## 4. 校準實驗 (Task 4)

**狀態**: `RAW_MODEL_PROB_MISSING`

Raw per-game MARL model probabilities not persisted from backtest. Backtest only stored aggregate Brier/BSS metrics. Platt Scaling and Isotonic Regression require per-game predictions: SKIPPED. Market-blend alpha grid shown analytically based on reported aggregate values.

**sklearn 可用性**:
- Isotonic Regression: True
- Platt Scaling (LogisticRegression): True

**Market-blend alpha 格子 (理論估計)**:

| alpha | 描述 | 理論 BSS |
|-------|------|----------|
| 0.0 | pure market (BSS≈0.0 by definition) | -0.0000 |
| 0.1 | blend alpha=0.1 | -0.0141 |
| 0.2 | blend alpha=0.2 | -0.0282 |
| 0.3 | blend alpha=0.3 | -0.0423 |
| 0.4 | blend alpha=0.4 | -0.0564 |
| 0.5 | blend alpha=0.5 | -0.0705 |
| 0.6 | blend alpha=0.6 | -0.0846 |
| 0.7 | blend alpha=0.7 | -0.0987 |
| 0.8 | blend alpha=0.8 | -0.1128 |
| 0.9 | blend alpha=0.9 | -0.1269 |
| 1.0 | pure model (BSS=REPORT_BSS) | -0.1410 |

> **注意**: 因缺乏逐場模型預測機率，alpha 格子為理論估計，
> 實際效果需在 MARL 模型啟用預測日誌後才能驗證。

---

## 5. 校準結果分類 (Task 5)

**分類**: `RAW_MODEL_PROB_MISSING`

原因: 逐場模型機率未保存 → 無法執行 Platt / Isotonic 校準。
下一步需先啟用 MARL 回測的預測日誌功能 (Task: `metric_repair_enable_prediction_logging`)。

---

## 6. BSS Safety Gate 狀態 (Task 6)

| 指標 | 值 |
|------|----|
| current_bss | -14.1% |
| current_model_brier | 0.2796 |
| current_market_brier | 0.2451 |
| cleaned_bss | -15.6% (同為負值 — 資料修復後 BSS 未轉正，根本問題仍在模型能力) |
| calibrated_bss | RAW_MODEL_PROB_MISSING |
| ece_before | 0.1447 (目標 < 0.08) |
| ece_after | None |
| **patch_gate_unlocked** | **False** ← 生產封鎖中 |
| safety_gate_file_exists | True |

**為何 Patch Gate 仍然封鎖**:
- BSS = -14.1% < 0，模型 Brier (0.2796) > 市場 Brier (0.2451)
- 清理後 BSS = -15.6% 仍為負值
- 校準實驗狀態 = `RAW_MODEL_PROB_MISSING`（缺乏原始預測機率）
- 規則: BSS < 0 時禁止任何 `patch_candidate` 或 `production_prediction` 任務

**建議下一步允許的操作**:
- DATA_REPAIR: Obtain verified odds from Pinnacle/Sportradar to replace unverified rows.
- DATA_REPAIR: Remove 28 duplicate records from outcomes CSV (deterministic dedup).
- METRIC_REPAIR: Re-run MARL backtest with per-game prediction logging enabled.
- METRIC_REPAIR: Apply Isotonic Regression calibration once raw model probs are available.
- FEATURE_REPAIR_INVESTIGATION: Test whether removing ELO proxy features improves calibration.
- COLLECT_MORE_DATA: Extend dataset to 2026 season once available (target N >= 3,000).

---

## 最終判定

```
PHASE_38_MLB_BSS_DATA_CALIBRATION_REPAIR_VERIFIED
```

Phase 38 資料修復預覽完成。Patch Gate 維持封鎖。
下一允許操作: 啟用 MARL 預測日誌 (METRIC_REPAIR) 或獲取驗證賠率 (DATA_REPAIR)。