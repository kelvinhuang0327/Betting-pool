# P53 Sep 2025 校準根因審計 — 投注計畫備案

**日期**: 2026-05-26  
**Phase**: P53  
**最終分類**: `SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC`

---

## 投注計畫相關性

**本報告為診斷性研究**，不產生任何投注訊號或實際下注建議。
所有 governance 旗標確認：`paper_only=True`, `kelly_deploy_allowed=False`, `live_api_calls=0`

P53 調查 Sep 2025 CALIBRATION_CRITICAL 根因，是 P52 V2 合約遺留問題的直接跟進。

---

## 核心發現

| 項目 | 值 |
|------|-----|
| Sep n | 98 |
| platt_ece | **0.122929** (臨界值 0.12) |
| 超出 | +0.002929 |
| 5-bin ECE | 0.122929 |
| adaptive ECE | 0.134578 |
| Bootstrap 95% CI | [0.06229, 0.215319] |
| Bootstrap > 0.12 佔比 | 53.88% |
| 最終分類 | `SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC` |

---

## 晚賽季比較概覽

| 期間 | platt_ece | V2 狀態 |
|------|----------|---------|
| May | 0.0595 | MONITORING_OK |
| Jun | 0.0519 | MONITORING_OK |
| Aug | 0.0435 | MONITORING_OK |
| Sep | 0.1229 | CALIBRATION_CRITICAL+SAMPLE_LIMITED |
| LateAug+Sep | 0.0635 | MONITORING_OK |

---

## 2025 賽季 FIP 信號狀態

- Tier C n=535，整賽季 platt_ece=0.02924
- Sep 2025 邊際健康：`fip_edge ≈ 0.147`，`CI_low > 0.130`（P52 V2 合約確認）
- 校準問題限於 Sep 2025（可能為晚賽季效應）

---

## 2024 資料缺口狀態

- 2024 closing-line odds 缺失，`P43_BLOCKED_BY_DATA_GAP` 未解決
- 影響範圍：cross-year only，**不影響 2025-only 分析**

---

## 研究鏈狀態

```
P43→P44→P45→P46→P47→P48→P49→P50→P51→P52→P53 (當前) → P54 (下一步)
```

---

*診斷報告 — 不構成投注建議 — paper_only=True*