# P27 Full 2025 True-Date Backfill Expansion — 驗證報告

**閘道決策**: `P27_FULL_TRUE_DATE_BACKFILL_EXPANSION_READY`  
**執行日期**: 2026-05-12  
**分支**: `p13-clean`  
**前序承諾**: `1078f71` (P26 完成)

---

## 1. 執行摘要

P27 Full True-Date Backfill Expansion 成功完成，對 2025-05-08 → 2025-09-28 完整 144 個日期進行分段式回填重播。所有 11 個分段均通過 P26 閘道，140/144 日期有效回放（4 個日期因全明星賽休賽無可用資料），324 筆 PAPER 推薦條目完整聚合。`paper_only=True`、`production_ready=False` 全程強制執行，零資料滲透。

---

## 2. 前置條件驗證

| 前置項目 | 狀態 |
|---|---|
| P26 smoke 驗證 (7 日) | ✅ P26_TRUE_DATE_HISTORICAL_BACKFILL_READY |
| P25 全範圍分割 (2025-05-08→2025-09-28) | ✅ P25_TRUE_DATE_SOURCE_SEPARATION_READY |
| 偵測到的源資料範圍 | 2025-05-08 → 2025-09-28 (140 個日期 slice) |
| 總源資料列數 | 1,577 列 |
| Look-ahead Leakage 檢查 | ✅ 無 2026 標籤 slice |

---

## 3. 分段計劃

- **完整範圍**: 2025-05-08 → 2025-09-28
- **分段大小**: 14 天
- **分段總數**: 11 段（最末段為 4 天：2025-09-25→2025-09-28）
- **總日期數**: 144

| 分段 | 開始 | 結束 | 天數 |
|---|---|---|---|
| 0 | 2025-05-08 | 2025-05-21 | 14 |
| 1 | 2025-05-22 | 2025-06-04 | 14 |
| 2 | 2025-06-05 | 2025-06-18 | 14 |
| 3 | 2025-06-19 | 2025-07-02 | 14 |
| 4 | 2025-07-03 | 2025-07-16 | 14 |
| 5 | 2025-07-17 | 2025-07-30 | 14 |
| 6 | 2025-07-31 | 2025-08-13 | 14 |
| 7 | 2025-08-14 | 2025-08-27 | 14 |
| 8 | 2025-08-28 | 2025-09-10 | 14 |
| 9 | 2025-09-11 | 2025-09-24 | 14 |
| 10 | 2025-09-25 | 2025-09-28 | 4 |

---

## 4. P25 全範圍執行結果

| 指標 | 數值 |
|---|---|
| 閘道 | P25_TRUE_DATE_SOURCE_SEPARATION_READY |
| 請求日期數 | 144 |
| 有效 slice 日期數 | 140 |
| 空白日期數 | 0 |
| 遭封鎖日期數 | 4（全明星賽休賽 2025-07-14～07-17） |
| 偵測源資料最小日期 | 2025-05-08 |
| 偵測源資料最大日期 | 2025-09-28 |
| paper_only | True |
| production_ready | False |

---

## 5. P26 分段重播結果（逐段明細）

| 分段 | 範圍 | P26 閘道 | 活躍條目 | 勝 | 負 | 押注額 | 損益 |
|---|---|---|---|---|---|---|---|
| 0 | 05-08～05-21 | READY | 37 | 17 | 20 | 9.25 | −0.3310 |
| 1 | 05-22～06-04 | READY | 29 | 18 | 11 | 7.25 | +1.6412 |
| 2 | 06-05～06-18 | READY | 37 | 23 | 14 | 9.25 | +2.3898 |
| 3 | 06-19～07-02 | READY | 40 | 21 | 19 | 10.00 | +1.2243 |
| 4 | 07-03～07-16 | READY | 25 | 11 | 14 | 6.25 | −0.3871 |
| 5 | 07-17～07-30 | READY | 32 | 23 | 9 | 8.00 | +4.3873 |
| 6 | 07-31～08-13 | READY | 26 | 12 | 14 | 6.50 | −0.2470 |
| 7 | 08-14～08-27 | READY | 26 | 11 | 15 | 6.50 | −0.5786 |
| 8 | 08-28～09-10 | READY | 35 | 20 | 15 | 8.75 | +2.0574 |
| 9 | 09-11～09-24 | READY | 29 | 12 | 17 | 7.25 | −0.9718 |
| 10 | 09-25～09-28 | READY | 8 | 3 | 5 | 2.00 | −0.4542 |
| **合計** | | **全 READY** | **324** | **171** | **153** | **81.00** | **+8.7304** |

---

## 6. P27 全範圍聚合結果

| 指標 | 數值 |
|---|---|
| **閘道** | **P27_FULL_TRUE_DATE_BACKFILL_READY** |
| 請求日期數 | 144 |
| 有效日期數 | 140 |
| 空白日期數 | 0 |
| 封鎖日期數 | 4（2025-07-14～07-17，全明星賽休賽） |
| 封鎖分段數 | 0 |
| 活躍 PAPER 條目總數 | 324 |
| 已結算勝 | 171 |
| 已結算負 | 153 |
| 未結算 | 0 |
| 總押注額 (units) | 81.0000 |
| 總損益 (units) | +8.7304 |
| **聚合 ROI** | **+10.78%** |
| **命中率 (Hit Rate)** | **52.78%** |
| 執行時長 | 7.52 秒 |
| 運行時守衛觸發 | 否 |
| paper_only | True |
| production_ready | False |

---

## 7. 封鎖日期說明

封鎖日期：`2025-07-14`、`2025-07-15`、`2025-07-16`、`2025-07-17`（共 4 天）

原因：MLB 全明星賽休賽期間，無正規賽資料，P25 無法生成有效 slice，P26 無法進行回放。此為預期行為，非資料管線錯誤。

---

## 8. 14 天 Smoke 驗證

獨立以 P25 + P26 CLI 進行 14 天 smoke 測試（2025-05-08 → 2025-05-21）：

| 指標 | Smoke 結果 |
|---|---|
| P25 閘道 | P25_TRUE_DATE_SOURCE_SEPARATION_READY |
| P26 閘道 | P26_TRUE_DATE_HISTORICAL_BACKFILL_READY |
| 有效日期數 | 14/14 |
| 活躍條目 | 37 |
| 勝 / 負 | 17 / 20 |
| 押注額 | 9.25 |
| 損益 | −0.3310 |
| ROI | −3.58% |
| 命中率 | 45.95% |

---

## 9. 單元測試統計

| 測試集合 | 測試數 | 狀態 |
|---|---|---|
| P27 contract | — | ✅ |
| P27 range planner | — | ✅ |
| P27 P25 runner | — | ✅ |
| P27 P26 segmented runner | — | ✅ |
| P27 reconciler | — | ✅ |
| P27 CLI integration | — | ✅ |
| **P27 全部** | **94** | **✅ 全數通過** |
| P26/P25/P24 回歸 | 289 | ✅ 零回歸 |
| **總計** | **383** | **✅** |

---

## 10. 決定性驗證（Determinism）

在 14 天範圍（2025-05-08 → 2025-05-21）執行兩次獨立 P27 CLI，排除 `generated_at` 與 `actual_runtime_seconds` 後比對：

| 輸出檔案 | 比對結果 |
|---|---|
| p27_gate_result.json | ✅ IDENTICAL |
| p27_full_backfill_summary.json | ✅ IDENTICAL |
| blocked_segments.json | ✅ IDENTICAL |
| segment_results.csv | ✅ IDENTICAL |
| date_results.csv | ✅ IDENTICAL |

**5/5 IDENTICAL** — 確定性驗證通過。

---

## 11. 樣本量評估

| 指標 | 數值 | 標準 |
|---|---|---|
| 總活躍條目 | 324 | MIN_SAMPLE_SIZE_ADVISORY = 1,500 |
| 評估 | **低於諮詢門檻** | 全程僅有 PAPER 邏輯推薦，並非所有 WBC/MLB 比賽均進入 gate |

樣本量 324 < 1,500，尚未達到 MIN_SAMPLE_SIZE_ADVISORY。主因是 P16_6 閘道對低 edge 比賽進行篩選，僅保留具正 EV 預期的推薦條目。

---

## 12. 資料安全性

| 安全項目 | 狀態 |
|---|---|
| paper_only=True 全程強制 | ✅ |
| production_ready=False 全程強制 | ✅ |
| Look-ahead Leakage 檢查（無 2026 slice） | ✅ |
| 每分段 P25 slice 使用開賽前狀態 | ✅ |
| 不允許 `--paper-only false` 執行 | ✅ (exit 2) |

---

## 13. 輸出產物

**全範圍主輸出目錄**: `outputs/predictions/PAPER/backfill/p27_full_true_date_backfill_2025-05-08_2025-09-28/`

| 檔案 | 說明 |
|---|---|
| `p27_gate_result.json` | P27 閘道決策 + 聚合統計 |
| `p27_full_backfill_summary.json` | 完整摘要（含分段與日期層級）|
| `p27_full_backfill_summary.md` | Markdown 格式摘要報告 |
| `segment_results.csv` | 11 個分段結果明細 |
| `date_results.csv` | 140 個日期回放結果 |
| `blocked_segments.json` | 封鎖分段/日期清單 |
| `runtime_guard.json` | 執行時守衛日誌 |

---

## 14. 提交清單（13 個檔案）

```
wbc_backend/recommendation/p27_full_true_date_backfill_contract.py
wbc_backend/recommendation/p27_true_date_range_planner.py
wbc_backend/recommendation/p27_p25_full_range_runner.py
wbc_backend/recommendation/p27_p26_segmented_replay_runner.py
wbc_backend/recommendation/p27_full_backfill_reconciler.py
scripts/run_p27_full_true_date_backfill_expansion.py
tests/test_p27_full_true_date_backfill_contract.py
tests/test_p27_true_date_range_planner.py
tests/test_p27_p25_full_range_runner.py
tests/test_p27_p26_segmented_replay_runner.py
tests/test_p27_full_backfill_reconciler.py
tests/test_run_p27_full_true_date_backfill_expansion.py
00-BettingPlan/20260512/p27_full_true_date_backfill_expansion_report.md
```

---

## 15. 下一階段建議

**閘道**: `P27_FULL_TRUE_DATE_BACKFILL_EXPANSION_READY`  
**樣本量**: 324（< 1,500 MIN_SAMPLE_SIZE_ADVISORY）

| 路徑 | 前提條件 | 下一步 |
|---|---|---|
| 擴展資料源 | 目前只有 WBC/MLB 部分 | 加入更多源資料以提升每日可回放日期密度 |
| P28 True-Date Backfill Performance Stability Audit | n ≥ 1,500 後可執行 | 對全範圍回填結果進行跨段穩定性審計 |
| 政策樣本分析 | 現有 324 筆 | 分析 P16_6 閘道的條目密度與策略覆蓋率 |

**短期推薦行動**: 在啟動 P28 前，優先評估 2025 全年源資料覆蓋率，確認是否可擴展至 n ≥ 1,500，或以 324 作為 advisory-only 基線進行 P28 穩定性評估。
