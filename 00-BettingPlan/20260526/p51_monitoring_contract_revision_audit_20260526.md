# P51 監控合約修訂審計 — 投注計畫備案

**日期**: 2026-05-26  
**Phase**: P51  
**前置 Phase**: P50 — `P50_PROBABILITY_STREAM_MISMATCH_CONFIRMED_DIAGNOSTIC`  
**最終分類**: `P51_REVISED_CONTRACT_REDUCES_FALSE_ALERTS_DIAGNOSTIC`

---

## 投注計畫相關性

**本報告為診斷性研究**，不產生任何投注訊號或實際下注建議。  
所有 governance 旗標確認：`paper_only=True`, `kelly_deploy_allowed=False`, `live_api_calls=0`

P51 的意義在於**確認 P43/P44 建立的 FIP 信號邊際框架在 2025 賽季仍然有效**，過去的監控警報（P49）是監控系統本身的設計問題，而非策略退化。

---

## 核心發現摘要

### P49 假警報已確認消除

| 月份/批次 | P49 狀態 | P51 修訂狀態 | 說明 |
|-----------|---------|------------|------|
| 2025-05（月度, n=120） | EDGE_DRIFT_CRITICAL ❌ | MONITORING_OK ✅ | fip_edge=0.1428, CI=[0.1256,0.1598] |
| 2025-06（月度, n=101） | EDGE_DRIFT_CRITICAL ❌ | MONITORING_OK ✅ | fip_edge=0.1482, CI=[0.1299,0.1676] |
| 2025-08（月度, n=108） | EDGE_DRIFT_WARNING ⚠️ | MONITORING_OK ✅ | fip_edge=0.1376, CI=[0.1218,0.1532] |
| 5 個滾動批次 | EDGE_DRIFT_CRITICAL ❌ | OK/WARNING ✅ | 平均 fip_edge=0.1437 |

### 真實校準問題已揭露

| 月份 | 狀態 | platt_ece | 說明 |
|------|------|-----------|------|
| 2025-09（n=98） | CALIBRATION_CRITICAL ⚠️ | 0.1229 > 0.12 | P49 被 SAMPLE_LIMITED 誤掩蓋 |

### 2025 賽季 FIP 信號邊際健康

- **所有 11 個滾動批次** CI 下界 > 0（無邊際崩潰）
- **平均 fip_signal_side_aware_edge = 0.1437**（遠高於 0.07 警示線）
- P43/P44 建立的 n=535 Tier C 資料集邊際框架：`均值 ≈ 0.14`, `CI_low ≈ 0.12`

---

## 監控合約修訂要點

| 變更項目 | 舊（P49） | 新（P51 修訂） |
|---------|---------|--------------|
| 邊際監控機率流 | PLATT_CALIBRATED（ML model_home_prob 壓縮） | RAW_SIGMOID（sigmoid(sp_fip_delta), k=1.0, 側選擇） |
| SAMPLE_LIMITED 支配邏輯 | 支配 CRITICAL（錯誤） | 僅支配 WARNING，不支配 CRITICAL（修正） |
| 校準監控機率流 | PLATT_CALIBRATED | PLATT_CALIBRATED（不變） |
| ECE 警示/臨界閾值 | 0.10/0.12 | 0.10/0.12（不變） |

---

## 對未來下注策略的意義

1. **FIP 差值信號（sp_fip_delta）仍有效**：2025 賽季 n=535 批次，fip_edge 均值 ~0.14，CI 全部正向
2. **P48 監控合約需在 P52 中更新**：確保未來監控使用正確機率流，避免假警報再次出現
3. **Sep 2025 校準問題需追蹤**：ECE=0.1229，需確認是否為季末模型漂移或資料問題
4. **投注決策前提**：任何 Kelly 部位或實際下注必須等到 P48 合約正式更新且 P52 批准後才可執行

---

## 研究鏈完整性確認

```
P40 (holdout) → P41 (cross-year WFV) → P42 (signal bands) → P43 (strong edge)
→ P44 (temporal stability) → P45 (Platt calibration) → P46 (isotonic comparison)
→ P47 (calibration synthesis) → P48 (monitoring contract) → P49 (replay)
→ P50 (stream mismatch confirmed) → P51 (contract revision) ← 當前
→ P52 (contract update) ← 下一步
```

**累積測試**: P40–P51 共 311 個測試，311/311 通過

---

*診斷報告 — 不構成投注建議 — paper_only=True*
