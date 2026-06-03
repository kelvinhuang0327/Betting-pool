# P52 監控合約 V2 — 投注計畫備案

**日期**: 2026-05-26  
**Phase**: P52  
**最終分類**: `P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC`

---

## 投注計畫相關性

**本報告為診斷性研究**，不產生任何投注訊號或實際下注建議。
所有 governance 旗標確認：`paper_only=True`, `kelly_deploy_allowed=False`, `live_api_calls=0`

P52 正式確立監控合約 V2，為未來離線監控提供標準化框架。

---

## V2 合約核心要點

| 指標族 | 機率流 | 關鍵規則 |
|--------|--------|---------|
| 邊際（Edge） | RAW_SIGMOID — `sigmoid(sp_fip_delta)`, k=1.0 | CI_low≤0→CRITICAL；mean<0.07→WARNING |
| 校準（Calibration） | PLATT_CALIBRATED — P45 鎖定 | ECE>0.12→CRITICAL；Brier>0.27→CRITICAL |
| 樣本（Sample） | N/A | n<100→SAMPLE_LIMITED（不支配 CRITICAL） |
| 資料缺口（Data Gap） | N/A | 2024缺口為跨年限制，不阻擋 2025-only 重放 |

---

## P51 修訂成果確認

| 月份 | P49 舊狀態 | V2 修訂狀態 | 說明 |
|------|-----------|-----------|------|
| 2025-05 (n=120) | EDGE_DRIFT_CRITICAL ❌ | MONITORING_OK ✅ | 假警報消除，fip_edge=0.1428 |
| 2025-06 (n=101) | EDGE_DRIFT_CRITICAL ❌ | MONITORING_OK ✅ | 假警報消除，fip_edge=0.1482 |
| 2025-08 (n=108) | EDGE_DRIFT_WARNING ⚠️ | MONITORING_OK ✅ | 假警報消除，fip_edge=0.1376 |
| 2025-09 (n=98) | SAMPLE_LIMITED (掩蓋) | CALIBRATION_CRITICAL ⚠️ | 真實校準問題揭露 |

---

## Sep 2025 校準問題

- **platt_ece = 0.1229** > 臨界閾值 0.12（超出 +0.0029）
- n=98 < 100 但在 V2 規則下 CALIBRATION_CRITICAL 不被 SAMPLE_LIMITED 壓制
- **邊際仍健康**：fip_edge=0.1469，CI_low=0.130 > 0
- 校準問題原因待查（P53 任務）

---

## 2025 賽季 FIP 信號邊際健康確認

- Tier C n=535，全 11 個滾動批次 CI_low > 0
- 平均 fip_signal_side_aware_edge = 0.1437（遠高於 0.07 警示線）
- P43/P44 建立的 FIP 信號邊際框架在 2025 賽季有效

---

## 研究鏈狀態

```
P43 → P44 → P45 → P46 → P47 → P48 → P49 → P50 → P51 → P52 (當前) → P53 (下一步)
```

**累積測試**: P40–P52 共 328 個測試，328/328 通過（預期含 P52 的 17 個測試）

---

*診斷報告 — 不構成投注建議 — paper_only=True*