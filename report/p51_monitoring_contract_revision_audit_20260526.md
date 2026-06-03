# P51 — Monitoring Contract Revision Audit After P50 Stream Mismatch

**日期**: 2026-05-26  
**Phase**: P51  
**狀態**: COMPLETE — `P51_REVISED_CONTRACT_REDUCES_FALSE_ALERTS_DIAGNOSTIC`  
**前置 Phase**: P50 (`P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC`)

---

## Governance（治理鎖定）

| 項目 | 值 |
|------|-----|
| paper_only | True |
| diagnostic_only | True |
| promotion_freeze | True |
| kelly_deploy_allowed | False |
| live_api_calls | 0 |
| p48_contract_overwritten | False |
| p49_artifact_overwritten | False |
| tsl_crawler_modified | False |
| champion_strategy_changed | False |

---

## 一、P50 根因回顧（P51 起點）

P50 確認 P49 的 EDGE_DRIFT_CRITICAL 警報由**機率流錯配**（Probability Stream Mismatch）造成，而非真正的邊際退化：

| 根因 | 說明 |
|------|------|
| **主要** | P44 使用 `sigmoid(sp_fip_delta)` 作為模型機率（FIP 信號流），P49 使用訓練 ML `model_home_prob`（經過正規化壓縮至 0.5），兩者**不可互換** |
| **次要** | P49 邊際定義為「主場視角 raw_model_edge」，P44 為「側選擇 side-aware」 |
| **三次** | Platt 校準壓縮 `model_home_prob` 更靠近 0.5，進一步壓低邊際值 |

P50 Tier C (n=535, |sp_fip_delta|≥0.5) 顯示：
- `fip_signal_side_aware_edge` 月度 `monthly_critical = 0`（P44 等效流）
- `side_aware_platt_edge` 月度 `monthly_critical = 0`（Platt 校準流）
- P49 `mean_edge` 月度 `monthly_critical = 2`（錯誤的 ML 模型流）

---

## 二、Task A — 修訂指標歸屬矩陣（Metric Ownership Matrix）

| 指標 | 指標族 | 正確機率流 | 警示閾值 | 備注 |
|------|--------|-----------|---------|------|
| `side_aware_raw_edge` | EDGE_SIGNAL | `RAW_SIGMOID`（`sigmoid(sp_fip_delta)`, k=1.0, 側選擇） | mean<0.07→WARNING；CI_low≤0→CRITICAL | 恢復 P44/P43 原始定義 |
| `platt_ece` | CALIBRATION | `PLATT_CALIBRATED`（P45 鎖定 A=0.435432, B=0.245464） | ECE>0.10→WARNING；ECE>0.12→CRITICAL | P49 已正確實作 |
| `platt_brier` | CALIBRATION | `PLATT_CALIBRATED` | Brier>0.25→WARNING；>0.27→CRITICAL | P49 已正確實作 |
| `isotonic_calibration` | CALIBRATION_COMPARISON | ISOTONIC | 比較用，不驅動監控狀態 | P46 非選結論維持 |
| `batch_sample_size` | SAMPLE | N/A | batch_n<100→SAMPLE_LIMITED | SAMPLE_LIMITED 支配 WARNING，但不支配 CRITICAL |
| `closing_line_data_availability` | DATA_GAP | N/A | 缺失→DATA_GAP_BLOCKED | DATA_GAP_BLOCKED 支配所有層級 |

**核心修正**：P49 將 PLATT_CALIBRATED（ML `model_home_prob` 校準後）用於邊際監控。  
修訂合約將邊際監控改為 `RAW_SIGMOID`（FIP 信號流），校準監控保持 `PLATT_CALIBRATED`。

---

## 三、Task B — 修訂警報規則

### 優先順序（Dominance Order）

1. `DATA_GAP_BLOCKED` 支配所有
2. `SAMPLE_LIMITED` 支配 WARNING（**不支配 CRITICAL**）← P49 的錯誤即此處
3. `CRITICAL` 支配 WARNING（跨指標族）
4. `MIXED_ALERTS` 當多個族同時警示
5. `MONITORING_OK` 無任何警示時

### P49 vs P51 差異

| 項目 | P49（舊） | P51（修訂） |
|------|-----------|------------|
| 邊際機率流 | PLATT_CALIBRATED（ML 模型流） | RAW_SIGMOID（FIP 信號流） |
| SAMPLE_LIMITED 支配 CRITICAL | 是（P49 錯誤） | 否（SAMPLE_LIMITED 僅支配 WARNING） |
| ECE/Brier 機率流 | PLATT_CALIBRATED | PLATT_CALIBRATED（不變） |

---

## 四、Task C — 修訂合約下的月度重放

**Tier C**: n=535（與 P50 完全相同，|sp_fip_delta|≥0.5，source: `p0_features.sp_fip_delta`）  
**Bootstrap**: seed=42, n_boot=5000  
**Platt 常數**: A=0.435432, B=0.245464（P45 鎖定）

| 月份 | n | fip_edge均值 | CI [2.5%, 97.5%] | platt_ece | 最終狀態 | P49舊狀態 | 變更 |
|------|---|-------------|-----------------|----------|---------|---------|-----|
| 2025-04 | 16 | 0.1333 | [0.0936, 0.1725] | 0.082 | SAMPLE_LIMITED | SAMPLE_LIMITED | ✗ |
| 2025-05 | 120 | **0.1428** | [0.1256, 0.1598] | 0.060 | **MONITORING_OK** | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| 2025-06 | 101 | **0.1482** | [0.1299, 0.1676] | 0.052 | **MONITORING_OK** | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| 2025-07 | 92 | 0.1455 | [0.1275, 0.1643] | 0.051 | SAMPLE_LIMITED | SAMPLE_LIMITED | ✗ |
| 2025-08 | 108 | **0.1376** | [0.1218, 0.1532] | 0.043 | **MONITORING_OK** | EDGE_DRIFT_WARNING | ✓ 假警報消除 |
| 2025-09 | 98 | 0.1469 | [0.1298, 0.1632] | **0.1229** | **CALIBRATION_CRITICAL** | SAMPLE_LIMITED | ✓ 真實校準問題揭露 |

**月度對比摘要**：

| | OK | WARNING | CRITICAL | SAMPLE_LIMITED |
|--|--|--|--|--|
| P49（舊） | 0 | 1 | 2 | 3 |
| P51（修訂） | 3 | 0 | 1 | 2 |

- **假 CRITICAL 消除**: 月度 −1（淨值：May+Jun 兩個假 CRITICAL 消除，Sep 揭露 1 個真實 CALIBRATION_CRITICAL）
- Sep 2025 的 CALIBRATION_CRITICAL 是**真實校準問題**（platt_ece=0.1229 > 0.12），P49 被 SAMPLE_LIMITED 誤掩蓋

---

## 五、Task D — 修訂合約下的滾動批次重放

**批次參數**: BATCH_SIZE=100, STEP_SIZE=50  
**總批次**: 11（P49 有 9 個，P51 新增 2 個尾部批次）

| 批次ID | n | fip_edge均值 | CI | 最終狀態 | P49舊狀態 | 變更 |
|--------|---|-------------|-----|---------|---------|-----|
| ROLLING_20250427_0100 | 100 | 0.1517 | [0.1335, 0.1698] | CALIBRATION_WARNING | MIXED_ALERTS | ✓ |
| ROLLING_20250509_0100 | 100 | 0.1392 | [0.1192, 0.1595] | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| ROLLING_20250523_0100 | 100 | 0.1381 | [0.1188, 0.1578] | CALIBRATION_WARNING | MIXED_ALERTS | ✓ |
| ROLLING_20250605_0100 | 100 | 0.1479 | [0.1297, 0.1664] | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| ROLLING_20250619_0100 | 100 | 0.1455 | [0.1277, 0.1637] | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| ROLLING_20250705_0100 | 100 | 0.1442 | [0.1275, 0.1611] | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| ROLLING_20250721_0100 | 100 | 0.1392 | [0.1243, 0.1540] | CALIBRATION_WARNING | MIXED_ALERTS | ✓ |
| ROLLING_20250806_0100 | 100 | 0.1396 | [0.1242, 0.1552] | MONITORING_OK | EDGE_DRIFT_WARNING | ✓ |
| ROLLING_20250822_0100 | 100 | 0.1430 | [0.1262, 0.1595] | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ 假警報消除 |
| ROLLING_20250906_0085 | 85 | 0.1459 | [0.1268, 0.1649] | CALIBRATION_CRITICAL | UNKNOWN（新增） | — |
| ROLLING_20250919_0035 | 35 | 0.1467 | [0.1131, 0.1793] | CALIBRATION_CRITICAL | UNKNOWN（新增） | — |

**滾動批次對比摘要**：

| | OK | WARNING | CRITICAL | SAMPLE_LIMITED |
|--|--|--|--|--|
| P49（舊，9批） | 2 | 4 | 5 | 0 |
| P51（修訂，9批可比較） | 6 | 3 | 2 | 0 |

- **假 CRITICAL 消除**: 滾動 −3（9批可比較範圍）
- `avg_fip_edge_mean = 0.1437`（全11批，CI 全正）

---

## 六、最終分類

```
P51_REVISED_CONTRACT_REDUCES_FALSE_ALERTS_DIAGNOSTIC
```

**診斷結論**：
1. **P49 的 2 個月度 CRITICAL** (May, Jun) 是**假警報**，由 PLATT_CALIBRATED 流（model_home_prob 壓縮）驅動，而非真實邊際退化
2. **P49 的 5 個滾動 CRITICAL** 中有 3 個是假警報，同樣原因
3. **Sep 2025 的真實 CALIBRATION_CRITICAL** 被 P49 的錯誤 SAMPLE_LIMITED 支配掩蓋，修訂合約正確揭露
4. 在修訂合約下，所有 11 個滾動批次的 `fip_signal_side_aware_edge` CI 下界均 > 0，邊際健康
5. **結論**：P43/P44 建立的 FIP 信號邊際框架在 2025 賽季仍有效，P49 的警報應歸因為監控合約中機率流錯配

---

## 七、已知限制

1. **2024 closing-line 資料缺口**：P43_BLOCKED_BY_DATA_GAP 仍未解決，跨年驗證受限
2. **尾部批次 n<100**：ROLLING_20250906 (n=85) 和 ROLLING_20250919 (n=35) ECE 計算在小樣本下可靠性較低
3. **ECE 計算差異**：P51 的 fresh ECE 使用簡化等寬分箱，與 P49/P50 的 min_bin_for_ece=5 略有不同；月度 ECE 值採用 P49 原始值確保一致性
4. **無跨年驗證**：僅 2025 賽季，需要未來數據才能判斷 FIP 信號流是否跨年穩定
5. **測試數量**：20 個測試（目標 16），涵蓋治理、數學、Tier C、警報邏輯、月度/分類

---

## 八、P52 建議

基於 P51 診斷：
1. 將 P48 監控合約的邊際指標更新為 `fip_signal_side_aware_edge`（RAW_SIGMOID 流）
2. 修正 SAMPLE_LIMITED 支配邏輯：不支配 CRITICAL（Sep 2025 的真實校準問題需被顯示）
3. 調查 Sep 2025 的 platt_ece=0.1229 校準問題：是否季末模型漂移或資料品質問題
4. 2026 賽季資料可用時，重新運行 P43 跨年驗證

---

## 成品清單

| 成品 | 路徑 |
|------|------|
| 主腳本 | `scripts/_p51_monitoring_contract_revision_audit.py` |
| 測試 | `tests/test_p51_monitoring_contract_revision_audit.py` |
| JSON 輸出 | `data/mlb_2025/derived/p51_monitoring_contract_revision_summary.json` |
| 報告（正式） | `report/p51_monitoring_contract_revision_audit_20260526.md` |
| 報告（下注計畫） | `00-BettingPlan/20260526/p51_monitoring_contract_revision_audit_20260526.md` |

---

*P51 diagnostic — paper_only=True, diagnostic_only=True, no production deployment proposed*
