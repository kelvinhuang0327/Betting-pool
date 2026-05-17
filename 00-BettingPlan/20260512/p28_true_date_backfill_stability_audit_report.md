# P28 True-Date Backfill 穩定性審計報告

**報告日期**: 2026-05-12  
**審計階段**: P28 True-Date Backfill Stability Audit  
**前置階段**: P27 Full True-Date Backfill Expansion (`4f5866e`)  
**最終閘門**: `P28_BLOCKED_SAMPLE_SIZE_INSUFFICIENT`  
**paper_only**: `True` | **production_ready**: `False`

---

## 1. 執行摘要

P28 審計已針對 P27 完整回填資料集（324 筆有效 paper entries，2025-05-08 至 2025-09-28）執行樣本密度、績效變異數、風險/回撤三大分析模組。

**核心發現：樣本量不足。** 324 < 最低建議樣本量 1,500，觸發 `P28_BLOCKED_SAMPLE_SIZE_INSUFFICIENT` 閘門。現有資料規模尚不足以進行統計顯著的穩定性認證。此為研究就緒信號，非工程失敗。

| 指標 | 數值 |
|------|------|
| 最終閘門 | `P28_BLOCKED_SAMPLE_SIZE_INSUFFICIENT` |
| 審計狀態 | `STABILITY_SAMPLE_SIZE_INSUFFICIENT` |
| 有效 Paper Entries | 324 |
| 最低樣本建議值 | 1,500 |
| 樣本量通過 | ❌ False |
| 決策優先序 | 樣本量不足（優先觸發）|

---

## 2. 審計範圍與配置

| 項目 | 值 |
|------|-----|
| 資料區間 | 2025-05-08 → 2025-09-28 |
| 總請求日數 | 144 天 |
| 就緒日數 | 140 天 |
| 封鎖日數 | 4 天（全明星賽休息：2025-07-14 至 07-17）|
| 分段數 | 11 個 |
| 最低樣本建議 (`MIN_SAMPLE_SIZE_ADVISORY`) | 1,500 |
| Bootstrap 迭代次數 | 2,000（seed=42，可重現）|
| 最大回撤限制 (`MAX_DRAWDOWN_PCT_LIMIT`) | 25.0% |
| 分段 ROI Std 不穩定閾值 | 0.50 |
| 執行時間 | 2026-05-12T07:38:41+00:00 |
| CLI 退出碼 | 1（BLOCKED）|

---

## 3. 閘門判定邏輯

閘門按以下優先順序評估（依序觸發，先命中即停）：

1. **樣本量不足** → `P28_BLOCKED_SAMPLE_SIZE_INSUFFICIENT` ← **本次觸發**
2. 回撤超限（> 25%）→ `P28_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT`
3. 分段 ROI Std 不穩定（> 0.50）→ `P28_BLOCKED_SEGMENT_VARIANCE_UNSTABLE`
4. 全部通過 → `P28_TRUE_DATE_STABILITY_AUDIT_READY`

**封鎖理由**: `total_active_entries=324 < min_sample_size_advisory=1500`

---

## 4. 樣本密度分析

### 4.1 整體密度

| 指標 | 值 |
|------|-----|
| 總有效 Entries | 324 |
| 每日平均活躍 | 2.25 |
| 每日最低活躍 | 0 |
| 每日最高活躍 | 9 |
| 每日活躍 Std | 1.637 |
| 稀疏日數（< 1 筆）| 21 天 |
| 稀疏分段數（< 50 筆）| 11 段（全部）|
| 樣本量通過 | ❌ False（324 / 1500）|

### 4.2 稀疏日期（21 天）

```
2025-05-15, 2025-05-16, 2025-05-30, 2025-06-01, 2025-06-02,
2025-06-11, 2025-06-12, 2025-06-16, 2025-07-06, 2025-07-08,
2025-07-14, 2025-07-15, 2025-07-16, 2025-07-17,
2025-07-24, 2025-08-18, 2025-08-25, 2025-08-26, 2025-08-28,
2025-09-11, 2025-09-22
```

（注：07-14 至 07-17 為全明星賽封鎖日，已納入稀疏清單）

### 4.3 分段活躍分佈

| Segment | 區間 | 活躍 Entries | 稀疏 |
|---------|------|-------------|------|
| seg0 | 2025-05-08 – 2025-05-21 | 37 | ⚠️ |
| seg1 | 2025-05-22 – 2025-06-04 | 29 | ⚠️ |
| seg2 | 2025-06-05 – 2025-06-18 | 37 | ⚠️ |
| seg3 | 2025-06-19 – 2025-07-02 | 40 | ⚠️ |
| seg4 | 2025-07-03 – 2025-07-16 | 25 | ⚠️ |
| seg5 | 2025-07-17 – 2025-07-30 | 32 | ⚠️ |
| seg6 | 2025-07-31 – 2025-08-13 | 26 | ⚠️ |
| seg7 | 2025-08-14 – 2025-08-27 | 26 | ⚠️ |
| seg8 | 2025-08-28 – 2025-09-10 | 35 | ⚠️ |
| seg9 | 2025-09-11 – 2025-09-24 | 29 | ⚠️ |
| seg10 | 2025-09-25 – 2025-09-28 | 8 | ⚠️ |

所有 11 個分段均低於每段 50 筆的稀疏閾值。

---

## 5. 績效變異數分析

> ⚠️ 以下統計數據為研究觀察，**不代表任何盈利邊際（edge）的統計顯著性證明**。

### 5.1 分段 ROI 變異

| 指標 | 值 |
|------|-----|
| 分段 ROI 最小值 | -0.2271 |
| 分段 ROI 最大值 | +0.5484 |
| 分段 ROI 均值 | +0.0732 |
| 分段 ROI Std | 0.2268（閾值 0.50，未觸發）|
| 正 ROI 分段數 | 5 / 11 |
| 負 ROI 分段數 | 6 / 11 |
| 分段命中率最低 | 37.5% |
| 分段命中率最高 | 71.9% |
| 分段命中率 Std | 0.1082 |

### 5.2 每日 ROI 變異

| 指標 | 值 |
|------|-----|
| 每日 ROI 均值 | +0.1306 |
| 每日 ROI Std | 0.7032 |
| 每日 ROI 範圍 | [-1.0, +1.5] |
| 每日命中率 Std | 0.382 |

### 5.3 Bootstrap ROI 95% CI（n=2,000, seed=42）

| 指標 | 值 |
|------|-----|
| CI 下界 95% | -0.0044 |
| CI 上界 95% | +0.2215 |
| CI 跨零 | ✅ 是（下界為負）|
| 總體 ROI（P27）| +0.1078 |

**解讀**：信賴區間跨越零，表示在現有樣本規模下，無法以統計方式確認正 ROI。需要更多資料。

---

## 6. 風險與回撤分析

| 指標 | 值 |
|------|-----|
| 最大回撤（units）| 2.192 |
| 最大回撤（%）| 275.9% |
| 回撤超限（> 25%）| ✅ 是（次要風險，被樣本量閘門覆蓋）|
| 最大連續虧損天數 | 4 天 |
| 高虧損連續天數警示（> 7 天）| ❌ 否 |
| 總虧損天數 | 47 天 |
| 總獲利天數 | 72 天 |
| 中性天數（PnL=0）| 25 天 |
| 虧損群集（連續 ≥ 2 天）| 9 個群集 |

**注釋**：275.9% 回撤率反映了股票曲線在峰值極低（首日累積 0.147 units）後進入負值區域的數學特性。在單位 stake 量少、淨值接近零的早期累積曲線中，百分比回撤容易超過 100%。此指標在樣本量充足後應重新評估。

回撤雖然超過 25% 限制，但因樣本量閘門優先觸發，`P28_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT` 未被獨立輸出。

---

## 7. 可重現性驗證（決定論檢查）

執行兩次相同參數的 P28 審計，對比所有 7 個輸出檔案（排除 `generated_at`）：

| 檔案 | 結果 |
|------|------|
| `p28_gate_result.json` | ✅ PASS |
| `p28_stability_audit_summary.json` | ✅ PASS |
| `sample_density_profile.json` | ✅ PASS |
| `performance_variance_profile.json` | ✅ PASS |
| `risk_drawdown_profile.json` | ✅ PASS |
| `sparse_dates.csv` | ✅ PASS |
| `sparse_segments.csv` | ✅ PASS |

**結論**：`ALL_DETERMINISM_PASSED` — Bootstrap CI 使用 `np.random.RandomState(seed=42)` 確保完全可重現。

---

## 8. 測試驗證

P28 測試覆蓋（6 個測試檔案）：

| 測試檔案 | 測試數 | 結果 |
|----------|--------|------|
| `test_p28_true_date_stability_contract.py` | 合約、常數、dataclass 凍結 | ✅ |
| `test_p28_sample_density_analyzer.py` | 密度計算、稀疏識別、載入器 | ✅ |
| `test_p28_performance_variance_analyzer.py` | ROI 變異、Bootstrap 確定性 | ✅ |
| `test_p28_risk_drawdown_analyzer.py` | 股票曲線、回撤、虧損群集 | ✅ |
| `test_p28_true_date_stability_auditor.py` | 閘門優先序、整合審計、8 檔輸出 | ✅ |
| `test_run_p28_true_date_backfill_stability_audit.py` | CLI 退出碼、決定論、輸出驗證 | ✅ |

**P28 + P27 總計: 198 / 198 通過**

---

## 9. 輸出檔案清單

路徑：`outputs/predictions/PAPER/backfill/p28_true_date_stability_audit_2025-05-08_2025-09-28/`

| 檔案 | 說明 |
|------|------|
| `p28_gate_result.json` | 最終閘門與封鎖原因 |
| `p28_stability_audit_summary.json` | 完整稽核摘要（JSON）|
| `p28_stability_audit_summary.md` | 完整稽核摘要（Markdown）|
| `sample_density_profile.json` | 樣本密度分析結果 |
| `performance_variance_profile.json` | 績效變異數分析結果（含 Bootstrap CI）|
| `risk_drawdown_profile.json` | 風險回撤分析結果 |
| `sparse_dates.csv` | 稀疏日期清單（21 天）|
| `sparse_segments.csv` | 稀疏分段清單（11 段）|

---

## 10. 系統架構摘要

P28 由以下模組組成：

| 模組 | 職責 |
|------|------|
| `p28_true_date_stability_contract.py` | 凍結 dataclasses、閘門常數、閾值 |
| `p28_sample_density_analyzer.py` | 樣本密度計算與稀疏識別 |
| `p28_performance_variance_analyzer.py` | ROI 變異分析、Bootstrap CI |
| `p28_risk_drawdown_analyzer.py` | 股票曲線、最大回撤、虧損群集 |
| `p28_true_date_stability_auditor.py` | 模組整合、閘門決策、8 檔輸出 |
| `scripts/run_p28_true_date_backfill_stability_audit.py` | CLI 入口（`--paper-only true` 強制）|

---

## 11. 安全控制驗證

| 控制項 | 狀態 |
|--------|------|
| `paper_only=True` 全程強制 | ✅ |
| `production_ready=False` 全程強制 | ✅ |
| Dataclass 凍結（FrozenInstanceError）| ✅ |
| `--paper-only false` → exit 2 | ✅ |
| 無未來資訊滲透（Look-ahead Leakage）| ✅（僅使用 P27 歷史回填資料）|
| 無盈利宣稱 | ✅（Bootstrap CI 跨零，無法確認 edge）|

---

## 12. 限制說明

1. **樣本量**: 324 遠低於 1,500 的建議最低值，所有統計數字的信賴度有限。
2. **Bootstrap CI 跨零**: 無法在統計上確認存在正 ROI。此為預期結果，非異常。
3. **回撤指標**: 275.9% 的百分比回撤反映了初期累積金額極小的數學特性，並非實際資本損失規模。
4. **資料來源**: 僅涵蓋 WBC 相關賽事的 paper entries，不代表任何真實資金損益。
5. **所有結果僅供研究參考，不構成任何投資或下注建議。**

---

## 13. 失敗分析

**問題**: 為何 324 entries 遠低於 1,500？

- P27 回填區間（144 天）中每日僅平均 2.25 筆 entries，主要受限於：
  1. WBC 賽程本身密度（並非每天均有符合條件的賽事）
  2. 篩選條件嚴格（僅計 `n_active_paper_entries > 0` 的日期）
  3. 全明星賽休息期（4 天封鎖）

**解決方向**: 見第 14 節「下一步建議」。

---

## 14. 下一步建議（P29 規劃）

**P29 建議方向：來源覆蓋率擴展（Source Coverage Expansion）**

目標：將有效 paper entries 密度從每日 ~2.25 提升至 ~12+，達到 1,500 筆樣本閾值。

建議措施：

1. **擴展聯盟覆蓋**: 納入 MLB、NPB、KBO、CPBL 等聯盟的歷史資料，增加每日可參考賽事數量。
2. **放寬賽事篩選條件**: 在數據品質可保證的前提下，審查並微調現有 paper entry 產生閾值。
3. **延長回填區間**: 在可取得歷史資料的條件下，將區間向前延伸至 2024 年或更早。
4. **增加每日 Entries 來源多樣性**: 納入讓分、大小分、前五局等多種玩法的 entries，提升密度。

**樣本充足後，P29 完成時應能解鎖 P28 所有被封鎖的閘門（含回撤分析重新評估）。**

---

## 15. 結論

P28 True-Date Backfill 穩定性審計已依規格完整執行：

- ✅ 5 個分析模組均已建立並通過測試
- ✅ 6 個測試檔案，198/198 測試通過
- ✅ 真實 P27 資料審計完成，退出碼 1（預期封鎖）
- ✅ 決定論驗證通過（7 檔全部一致）
- ✅ `paper_only=True`、`production_ready=False` 全程強制
- ⛔ 閘門結論：`P28_BLOCKED_SAMPLE_SIZE_INSUFFICIENT`（324 < 1,500）

此為有效的研究就緒信號。當樣本量充足後，P28 審計管線可直接重新執行，無需修改。

---

`P28_TRUE_DATE_BACKFILL_STABILITY_AUDIT_SAMPLE_SIZE_BLOCKED`
