# P53 — Sep 2025 校準 CRITICAL 根因審計

**日期**: 2026-05-26  
**Phase**: P53  
**前置 Phase**: P52 (`P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC`)  
**狀態**: COMPLETE — `SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC`

---

## Governance（治理鎖定）

| 項目 | 值 |
|------|-----|
| paper_only | True |
| diagnostic_only | True |
| promotion_freeze | True |
| kelly_deploy_allowed | False |
| live_api_calls | 0 |
| tsl_crawler_modified | False |
| champion_strategy_changed | False |
| production_usage_proposed | False |
| runtime_recommendation_logic_changed | False |
| p52_contract_overwritten | False |

---

## 一、P52 背景回顧

P52 正式確立 V2 監控合約：
- 邊際監控：RAW_SIGMOID (`fip_signal_side_aware_edge`, k=1.0)
- 校準監控：PLATT_CALIBRATED (A=0.435432, B=0.245464)
- SAMPLE_LIMITED 不支配 CRITICAL（P49 錯誤修正）

**P52 遺留問題**：Sep 2025 (n=98, platt_ece=0.1229 > 0.12) 被分類為 CALIBRATION_CRITICAL。
P49 曾以 SAMPLE_LIMITED 掩蓋此問題。P53 調查根因。

---

## 二、Tier C 資料驗證

| 項目 | 值 |
|------|-----|
| 總 Tier C n | 535 |
| 預期 n | 535 |
| 符合預期 | True |
| Sep 2025 n | 98 |
| Platt A | 0.435432 (P45 鎖定) |
| Platt B | 0.245464 (P45 鎖定) |

---

## 三、Sep 2025 校準指標

| 指標 | 值 |
|------|-----|
| n | 98 |
| platt_ece | **0.122929** |
| raw_ece | 0.06302 |
| platt_brier | 0.235731 |
| raw_brier | 0.230901 |
| mean_platt_prob | 0.571682 |
| mean_raw_prob | 0.524761 |
| actual_win_rate | 0.581633 |
| calibration_gap_platt | 0.00995 |
| V2 Contract 狀態 | `CALIBRATION_CRITICAL+SAMPLE_LIMITED` |

> Platt ECE 臨界閾值 = 0.12；Sep platt_ece = 0.122929 → 超出 0.002929

---

## 四、可靠性 Bin 根因分析（10 個 Bin）

**主要模式**: MIXED  
**錯誤是否集中**: True  
（最大 ECE bin 佔比: 54.05%）

| Bin | n | 預測均值(P) | 實際勝率 | Platt Gap | ECE 貢獻 | 解讀 |
|-----|---|------------|---------|----------|---------|------|
| [0.50,0.60] | 81 | 0.5622 | 0.4938 | -0.0683 | 0.0565 | OVERCONFIDENT |
| [0.60,0.70] | 17 | 0.6170 | 1.0000 | +0.3830 | 0.0664 | UNDERCONFIDENT |

**最大 ECE 貢獻 Bin**: [0.6, 0.7] ECE 貢獻=0.0664, 解讀=UNDERCONFIDENT

---

## 五、晚賽季比較

| 期間 | n | raw_ece | platt_ece | platt_brier | 實際勝率 | 平均預測(P) | V2 狀態 |
|------|---|---------|----------|------------|---------|-----------|---------|
| May | 120 | 0.0669 | 0.0595 | 0.2378 | 0.5750 | 0.5825 | MONITORING_OK |
| Jun | 101 | 0.0694 | 0.0519 | 0.2401 | 0.5545 | 0.5628 | MONITORING_OK |
| Aug | 108 | 0.0204 | 0.0435 | 0.2474 | 0.5463 | 0.5898 | MONITORING_OK |
| Sep | 98 | 0.0630 | 0.1229 | 0.2357 | 0.5816 | 0.5717 | CALIBRATION_CRITICAL+SAMPLE_LIMITED |
| LateAug+Sep | 206 | 0.0328 | 0.0635 | 0.2418 | 0.5631 | 0.5812 | MONITORING_OK |

---

## 六、樣本敏感性分析（P53.D）

### Bootstrap (n_boot=5000, seed=42, 10-bin ECE)

| 指標 | 值 |
|------|-----|
| 觀測 platt_ece | 0.122929 |
| Bootstrap 均值 | 0.128446 |
| Bootstrap 標準差 | 0.041027 |
| 95% CI | [0.06229, 0.215319] |
| 90% CI | [0.067849, 0.202466] |
| CI_low_95 > 0.12 | False |
| Bootstrap > 0.12 佔比 | 53.88% |
| Bootstrap > 0.10 佔比 | 72.80% |

### Bin 數量敏感性

| 方法 | n_bins | platt_ece | > 0.12 |
|------|--------|----------|-------|
| 5-bin | 5 | 0.122929 | True |
| 10-bin | 10 | 0.122929 | True |
| adaptive (min_n=10) | 9 | 0.134578 | True |

### 方法一致性

- 5_bin: `CRITICAL`
- 10_bin: `CRITICAL`
- adaptive: `CRITICAL`
- bootstrap_observed: `CRITICAL`
- bootstrap_ci_low_95: `not_critical`

**所有方法均超 CRITICAL**: False  
**任一方法超 CRITICAL**: True

---

## 七、Platt 過/欠信心診斷

校準缺口（platt）= 實際勝率 - 平均 Platt 預測 = 0.5816 - 0.5717 = +0.0100

**診斷**: 整體 Platt 校準接近中性，偏差不顯著（< 2%）

Bin 主要模式: **MIXED**

---

## 八、限制

- Sep 2025 n=98 is below the n=100 SAMPLE_LIMITED threshold — all sensitivity analyses account for this.
- Platt constants locked from P45. Recalibration requires explicit authorization.
- 2024 closing-line data gap remains unresolved (P43_BLOCKED_BY_DATA_GAP — cross-year market-edge validation blocked).
- No live odds data used. Analysis is entirely offline.
- Root cause of Sep 2025 degradation (late-season regression, market adaptation, regime change) not yet determined.
- P53 does not modify runtime recommendation logic.
- P52 artifact not overwritten.

---

## 九、最終分類

```
SEP_CALIBRATION_SAMPLE_SENSITIVE_DIAGNOSTIC
```

**2024 closing-line 資料缺口**: 仍未解決 (`P43_BLOCKED_BY_DATA_GAP`)，
為 cross-year blocker only，不影響 2025-only 分析。

---

## 十、建議下一步

- **P54**（如需要）：若確認為真實校準漂移，調查 Sep 2025 SP FIP delta 分布變化
  是否反映晚賽季投手 FIP 回歸，或者比賽特性改變
- **P55**：若 2+ 個完整賽季數據可用，評估是否需要 Platt 常數重新校準
  （需要 CEO 授權）
- **P54 或 P55**：若 2024 closing-line odds 補齊，重新執行 P43 跨年驗證

---

## 成品清單

| 成品 | 路徑 |
|------|------|
| 主腳本 | `scripts/_p53_sep_calibration_critical_audit.py` |
| 測試 | `tests/test_p53_sep_calibration_critical_audit.py` |
| JSON 輸出 | `data/mlb_2025/derived/p53_sep_calibration_critical_audit_summary.json` |
| 報告（正式） | `report/p53_sep_calibration_critical_audit_20260526.md` |
| 報告（下注計畫） | `00-BettingPlan/20260526/p53_sep_calibration_critical_audit_20260526.md` |

*P53 diagnostic — paper_only=True, diagnostic_only=True, no production deployment proposed*