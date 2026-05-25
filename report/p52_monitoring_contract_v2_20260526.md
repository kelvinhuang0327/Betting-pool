# P52 — Formal Monitoring Contract V2

**日期**: 2026-05-26  
**Phase**: P52  
**狀態**: COMPLETE — `P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC`  
**前置 Phase**: P51 (`P51_REVISED_CONTRACT_REDUCES_FALSE_ALERTS_DIAGNOSTIC`)

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
| p48_artifact_overwritten | False |
| p49_artifact_overwritten | False |
| p51_artifact_preserved | True |

---

## 一、為何需要 V2 合約

P50 確認 P49 的邊際漂移警報由**機率流錯配**引起：P49 使用 PLATT_CALIBRATED（ML `model_home_prob`）
驅動邊際監控，而 P43/P44 原始框架使用 RAW_SIGMOID（`sigmoid(sp_fip_delta)`, k=1.0）。

P51 修訂重放驗證此修正消除了假警報。P52 **正式確立** V2 合約文件，無需刪除或覆蓋 P48/P49 成品。

---

## 二、V2 合約 — 超越政策（Supersession Policy）

### 已超越（Superseded）

- P48 edge-monitoring stream rule (P48 assigned edge monitoring to PLATT_CALIBRATED; V2 assigns it to RAW_SIGMOID fip_signal_side_aware_edge)
- P49 SAMPLE_LIMITED dominance over CRITICAL (P49 let SAMPLE_LIMITED suppress genuine CALIBRATION_CRITICAL; V2 prohibits this suppression)
- P49 Platt-edge drift interpretation (P49 classified May/Jun/Aug 2025 Platt-edge alerts as genuine drift; P50 confirmed stream mismatch; V2 uses correct stream)

### 已保留（Preserved）

- P48 fixture schema concept — monitoring_row_schema fields retained as V2 base
- P48 ECE/Brier thresholds — ece_warning=0.10, ece_critical=0.12, brier_warning=0.25, brier_critical=0.27 unchanged
- P48 edge thresholds — mean_edge_warning=0.07, critical=CI_crosses_zero unchanged
- P48 DATA_GAP_BLOCKED dominance rule — retained in V2
- P49 offline replay concept — batch replay against historical records retained
- P47 Platt selection for calibration monitoring — PLATT_CALIBRATED remains canonical for ECE/Brier

### 不覆蓋（Does Not Overwrite）

- `P48 artifact: data/mlb_2025/derived/p48_monitoring_loop_contract_summary.json`
- `P49 artifact: data/mlb_2025/derived/p49_offline_historical_monitoring_replay_summary.json`
- `P51 artifact: data/mlb_2025/derived/p51_monitoring_contract_revision_summary.json`
- `runtime recommendation logic`
- `champion strategy`
- `TSL crawler`

---

## 三、指標歸屬矩陣 V2（Metric Ownership Matrix）

| 指標族 | 機率流 | 驅動告警 | 備注 |
|--------|--------|---------|------|
| EDGE_SIGNAL | RAW_SIGMOID | EDGE_SIGNAL_ALERT | — |
| CALIBRATION | PLATT_CALIBRATED | CALIBRATION_ALERT | — |
| SAMPLE | NONE | SAMPLE_ALERT | P49 incorrectly let SAMPLE_LIMITED mask CALIBRATION_CRITI... |
| DATA_GAP | NONE | DATA_GAP_ALERT | — |

---

## 四、V2 警報規則

### 邊際警報（Edge — RAW_SIGMOID）

| 等級 | 條件 |
|------|------|
| WARNING | `mean_edge < 0.07` |
| CRITICAL | `edge_ci_low <= 0`（CI 穿越零） |

### 校準警報（Calibration — PLATT_CALIBRATED）

| 指標 | WARNING | CRITICAL |
|------|---------|---------|
| platt_ece | > 0.10 | > 0.12 |
| platt_brier | > 0.25 | > 0.27 |

### 樣本警報

- `batch_n < 100` → SAMPLE_LIMITED
- **SAMPLE_LIMITED 支配 WARNING，不支配 CRITICAL**（P49 錯誤已修正）

### 優先順序

1. DATA_GAP_BLOCKED: dominates all if required current-scope data absent
2. CRITICAL: EDGE_DRIFT_CRITICAL or CALIBRATION_CRITICAL take priority
3. SAMPLE_LIMITED: dominates WARNING but must NOT hide CRITICAL
4. WARNING: EDGE_DRIFT_WARNING or CALIBRATION_WARNING
5. MIXED_ALERTS: when alerts span multiple metric families at same severity
6. MONITORING_OK: no alert fires

---

## 五、P48/P49 規則：保留 vs 廢棄

### 保留規則

| Rule ID | 描述 | 狀態 |
|---------|------|------|
| P48_THRESHOLD_ECE_WARNING | ECE warning threshold: platt_ece > 0.10... | RETAINED |
| P48_THRESHOLD_ECE_CRITICAL | ECE critical threshold: platt_ece > 0.12... | RETAINED |
| P48_THRESHOLD_BRIER_WARNING | Brier warning: platt_brier > 0.25... | RETAINED |
| P48_THRESHOLD_BRIER_CRITICAL | Brier critical: platt_brier > 0.27... | RETAINED |
| P48_EDGE_WARNING_MEAN | Edge warning: mean_edge < 0.07... | RETAINED |
| P48_EDGE_CRITICAL_CI_CROSSES_ZERO | Edge critical: CI_low <= 0... | RETAINED |
| P48_SAMPLE_LIMITED_THRESHOLD | SAMPLE_LIMITED if batch_n < 100... | RETAINED |
| P48_DATA_GAP_DOMINANCE | DATA_GAP_BLOCKED dominates all alerts... | RETAINED |
| P48_MONITORING_ROW_SCHEMA_CONCEPT | Monitoring row schema with identity, metrics, status, trace ... | RETAINED_EXTENDED |
| P49_OFFLINE_REPLAY_CONCEPT | Offline batch replay against historical JSONL records... | RETAINED |

### 廢棄規則

| Rule ID | 描述 | 超越依據 |
|---------|------|---------|
| P48_P49_EDGE_USES_PLATT_CALIBRATED | P48/P49 implicitly used PLATT_CALIBRATED (model_home_pr... | V2 edge monitoring uses RAW_SIGMOID (fip_signal_si... |
| P49_SAMPLE_LIMITED_DOMINATES_CRITICAL | P49 let SAMPLE_LIMITED mask CALIBRATION_CRITICAL. Sep 2... | V2 rule: SAMPLE_LIMITED dominates WARNING only. CR... |
| P49_SINGLE_PROBABILITY_STREAM_FIELD | P49 schema had a single 'probability_stream' field used... | V2 schema has separate 'edge_probability_stream' a... |

---

## 六、P51 重放證據摘要

**Tier C**: n=535（`|sp_fip_delta|>=0.5`, source: `p0_features.sp_fip_delta`）

| 月份 | n | fip_edge均值 | CI低 | CI高 | platt_ece | 最終狀態 | P49舊狀態 | 變更 |
|------|---|-------------|------|------|----------|---------|---------|-----|
| 2025-04 | 16 | 0.1333 | 0.0936 | 0.1725 | 0.0824 | SAMPLE_LIMITED | SAMPLE_LIMITED | — |
| 2025-05 | 120 | 0.1428 | 0.1256 | 0.1598 | 0.0595 | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ |
| 2025-06 | 101 | 0.1482 | 0.1299 | 0.1676 | 0.0519 | MONITORING_OK | EDGE_DRIFT_CRITICAL | ✓ |
| 2025-07 | 92 | 0.1455 | 0.1275 | 0.1643 | 0.0508 | SAMPLE_LIMITED | SAMPLE_LIMITED | — |
| 2025-08 | 108 | 0.1376 | 0.1218 | 0.1532 | 0.0435 | MONITORING_OK | EDGE_DRIFT_WARNING | ✓ |
| 2025-09 | 98 | 0.1469 | 0.1298 | 0.1632 | 0.1229 | CALIBRATION_CRITICAL | SAMPLE_LIMITED | ✓ |

月度假 CRITICAL 消除（淨值）：1
滾動假 CRITICAL 消除：3（9批可比較範圍）

---

## 七、Sep 2025 校準問題追蹤

| 欄位 | 值 |
|------|-----|
| 月份 | 2025-09 |
| n | 98 |
| platt_ece | 0.122929 |
| 臨界閾值 | 0.12 |
| 超出量 | +0.002929 |
| P49 狀態（錯誤） | SAMPLE_LIMITED (platt_ece was masked by n=98 < 100) |
| P51 修正狀態 | CALIBRATION_CRITICAL |

> **邊際狀態**: Edge healthy (fip_edge ~0.147, CI_low > 0). Issue is calibration only.

> **P53 建議**: P53 should investigate Sep 2025 calibration degradation. Possible causes: late-season pitcher-FIP regression, market adaptation, or Platt constants drifting. Platt constants are locked from P45 and cannot be updated without explicit authorization.

---

## 八、未解決資料缺口

### GAP_2024_MLB_CLOSING_LINE_ODDS

- **描述**: 2024 MLB moneyline closing-line odds are not available in the repository. data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl does not contain Home ML / Away ML columns (all null). data/mlb_2025/mlb-2024-asplayed.csv is Retrosheet gamelog only — no odds.
- **影響範圍**: CROSS_YEAR_ONLY — does not block 2025-only offline replay
- **P43 分類**: `P43_BLOCKED_BY_DATA_GAP`
- **解決路徑**: If mlb_odds_2024_real.csv is sourced with schema matching mlb_odds_2025_real.csv (Date, Away, Home, scores, Away ML, Home ML), re-run P43 script — load_2024_unified() stub already exists.
- **狀態**: UNRESOLVED

---

## 九、最終分類

```
P52_MONITORING_CONTRACT_V2_READY_DIAGNOSTIC
```

---

## 十、未來建議

- **P53**: Investigate Sep 2025 CALIBRATION_CRITICAL (platt_ece=0.1229). Determine if late-season calibration drift is real or a regime change.
- **P54**: If/when 2024 closing-line odds are sourced, re-run P43 cross-year validation.
- **P55**: When ≥2 full seasons of data available under V2 contract, evaluate whether Platt constants require recalibration.

---

## 成品清單

| 成品 | 路徑 |
|------|------|
| 主腳本 | `scripts/_p52_monitoring_contract_v2_builder.py` |
| 測試 | `tests/test_p52_monitoring_contract_v2_builder.py` |
| JSON 輸出 | `data/mlb_2025/derived/p52_monitoring_contract_v2_summary.json` |
| 報告（正式） | `report/p52_monitoring_contract_v2_20260526.md` |
| 報告（下注計畫） | `00-BettingPlan/20260526/p52_monitoring_contract_v2_20260526.md` |

*P52 diagnostic — paper_only=True, diagnostic_only=True, no production deployment proposed*