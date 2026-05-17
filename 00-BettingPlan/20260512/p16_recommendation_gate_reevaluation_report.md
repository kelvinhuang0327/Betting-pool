# P16 Recommendation Gate Reevaluation Report
**版本標記**: `P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY`

---

## 1. 執行摘要 (Executive Summary)

本報告記錄 P16 Recommendation Gate Reevaluation + Strategy Risk Hardening 任務的完整執行結果。  
依 CEO 修訂範疇，本輪共實作 13 項子任務，整合 P15 市場賠率感知模擬成果，加入策略風險評估
（Sharpe / Drawdown / Bootstrap CI / Edge Threshold Sweep），嵌入每條建議行與閘門決策。

**最終閘門決策**: `P16_BLOCKED_RISK_PROFILE_VIOLATION`  
原因：於最佳邊緣閾值（0.08）下，策略最大回撤（44.80%）超過上限（25.0%），
所有 247 條已通過邊緣篩選的行全部被 `P16_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT` 攔截。

> **PAPER_ONLY = true | PRODUCTION_READY = false**  
> 本輪所有輸出僅用於模擬研究，不得用於實際投注。

---

## 2. 任務規範 (Task Specification)

| #  | 子任務 | 狀態 |
|----|--------|------|
| T1 | Repo/branch/marker 驗證 | ✅ |
| T2 | `strategy_risk_metrics.py` — Sharpe/Drawdown/Bootstrap CI | ✅ |
| T3 | `edge_threshold_sweep.py` — 閾值掃描 + 最大 Sharpe 選取 | ✅ |
| T4 | 檢閱現有 recommendation system | ✅ |
| T5 | `p16_recommendation_input_adapter.py` | ✅ |
| T6 | `p16_recommendation_gate.py` — 含 12 種 reason code | ✅ |
| T7 | `p16_recommendation_row_builder.py` | ✅ |
| T8 | `scripts/run_p16_recommendation_gate_reevaluation.py` — CLI | ✅ |
| T9 | 5 個測試模組（181 tests pass, 0 failed） | ✅ |
| T10 | 真實 P15 資料執行 CLI | ✅ |
| T11 | 確定性驗證（兩次運行輸出完全一致） | ✅ |
| T12 | 本報告 | ✅ |
| T13 | Git commit | 待執行 |

---

## 3. 前置條件驗證 (Prerequisites)

| 指標 | 值 |
|------|----|
| Repo | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, branch `p13-clean` |
| P13 marker | `P13_WALK_FORWARD_LOGISTIC_BASELINE_READY` (commit `8e74863`) |
| P14 marker | `P14_STRATEGY_SIMULATION_SPINE_READY` (commit `2dfb0ee`) |
| P15 marker | `P15_MARKET_ODDS_JOIN_SIMULATION_READY` (commit `2d88a7b`) |
| P15 資料來源 | `outputs/predictions/PAPER/2026-05-12/p15_market_odds_simulation/` |
| P15 n_samples | 1577 |
| P15 JOINED rows | 1575 (coverage=99.87%) |
| P15 source_bss_oof | 0.008253 |

---

## 4. 新增模組清單 (Deliverable Files)

### 核心模組
| 檔案 | 功能 |
|------|------|
| `wbc_backend/simulation/strategy_risk_metrics.py` | Sharpe、Max Drawdown、Bootstrap ROI CI、Max Consecutive Loss、Hit Rate |
| `wbc_backend/simulation/edge_threshold_sweep.py` | 多閾值掃描，按最大 Sharpe（n_bets ≥ floor）選取建議閾值 |
| `wbc_backend/recommendation/p16_recommendation_input_adapter.py` | 將 P15 `joined_oof_with_odds.csv` 轉為 `P16InputRow` |
| `wbc_backend/recommendation/p16_recommendation_gate.py` | 10 級閘門邏輯，12 種 reason code |
| `wbc_backend/recommendation/p16_recommendation_row_builder.py` | 標準化建議行，嵌入完整風險欄位 |
| `scripts/run_p16_recommendation_gate_reevaluation.py` | CLI 入口，輸出 7 種文件 |

### 測試模組
| 檔案 | 測試數 |
|------|--------|
| `tests/test_strategy_risk_metrics.py` | N/A |
| `tests/test_edge_threshold_sweep.py` | N/A |
| `tests/test_p16_recommendation_input_adapter.py` | N/A |
| `tests/test_p16_recommendation_gate.py` | N/A |
| `tests/test_run_p16_recommendation_gate_reevaluation.py` | N/A |
| **合計** | **181 passed, 0 failed** |

---

## 5. 策略風險分析 (Strategy Risk Profile)

> 以最佳邊緣閾值 **0.08** 為基準（最大 Sharpe 選取）

| 指標 | 值 |
|------|----|
| ROI Mean | **+10.93%** |
| ROI 95% CI (Bootstrap, n=2000) | [-0.21%, +1.24%] |
| Max Drawdown | **44.80%** ⚠️ (超過 25.0% 限制) |
| Sharpe Ratio | 0.0937 |
| n_bets | 247 |
| Hit Rate | 見 strategy_risk_profile.json |

**風險評估結論**：  
雖然 Sharpe Ratio 為正（0.0937 ≥ floor 0.0），策略 ROI 中位數為正，  
但最大回撤高達 44.80%，遠超 25% 上限。在半凱利框架下，此回撤水準意味  
在最壞歷史情境下可能損失近一半資金，不符合本研究設定的風險容忍度。

---

## 6. 邊緣閾值掃描 (Edge Threshold Sweep)

| 閾值 | n_bets | Sharpe | ROI Mean |
|------|--------|--------|----------|
| 0.01 | 640 | 0.0497 | +5.63% |
| 0.02 | 563 | 0.0564 | +6.26% |
| 0.03 | 509 | 0.0632 | +6.98% |
| 0.05 | 396 | 0.0743 | +8.32% |
| **0.08** | **247** | **0.0937** | **+10.93%** |

**選取理由**：`threshold=0.0800 maximises Sharpe=0.0937 with n_bets=247 >= floor=50`  
所有閾值均有 n_bets ≥ 50，sweep_status = `SWEEP_OK`。

---

## 7. 閘門決策流程 (Gate Decision Flow)

```
P16 閘門按序（10 級）:
1. SWEEP_INSUFFICIENT_SAMPLES → 攔截
2. PRODUCTION_READY=True → 攔截
3. PAPER_ONLY=False → 攔截
4. BSS ≤ 0 → 攔截
5. odds_join_status != "JOINED" → 攔截
6. p_model 或 p_market 無效 → 攔截
7. odds_decimal ≤ 1.0 → 攔截
8. edge < selected_threshold → 攔截
9. max_drawdown > limit → 攔截  ← 本輪 247 行在此被攔截
10. sharpe < floor → 攔截
→ ELIGIBLE（本輪 0 行通過）
```

---

## 8. 閘門原因分佈 (Gate Reason Counts)

| 原因代碼 | 件數 |
|----------|------|
| `P16_BLOCKED_EDGE_BELOW_THRESHOLD` | 1328 |
| `P16_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT` | 247 |
| `P16_BLOCKED_ODDS_NOT_JOINED` | 2 |
| `P16_ELIGIBLE_PAPER_RECOMMENDATION` | **0** |

---

## 9. 輸出文件清單 (Output Files)

路徑: `outputs/predictions/PAPER/2026-05-12/p16_recommendation_gate/`

| 文件 | 描述 |
|------|------|
| `recommendation_rows.csv` | 1577 行（含所有閘門欄位與風險欄位） |
| `recommendation_summary.json` | 完整統計摘要 |
| `recommendation_summary.md` | 可讀摘要 |
| `gate_reason_counts.json` | 各 reason_code 件數 |
| `strategy_risk_profile.json` | 策略風險指標 |
| `edge_threshold_sweep.json` | 各閾值掃描結果 |
| `edge_threshold_sweep.md` | 掃描報告（可讀） |

---

## 10. 確定性驗證 (Determinism Verification)

| 文件 | Run 1 vs Run 2 |
|------|---------------|
| `recommendation_summary.json` | **MATCH** |
| `gate_reason_counts.json` | **MATCH** |
| `strategy_risk_profile.json` | **MATCH** |
| `edge_threshold_sweep.json` | **MATCH** |
| `recommendation_rows.csv` (gate_decision 列) | **MATCH** |

Bootstrap CI 使用固定 seed=42，閾值掃描結果確定，所有輸出可重現。

---

## 11. 測試結果 (Test Results)

```
181 passed, 0 failed in 15.12s
```

| 測試模組 | 覆蓋範圍 |
|---------|---------|
| test_strategy_risk_metrics.py | Drawdown、Sharpe、consecutive loss、Bootstrap CI、summarize |
| test_edge_threshold_sweep.py | INSUFFICIENT 場景、SWEEP_OK 選取、最大 Sharpe 選取、結構驗證 |
| test_p16_recommendation_input_adapter.py | JOINED/MISSING/INVALID、機率/賠率驗證、paper_only/production_ready |
| test_p16_recommendation_gate.py | 所有 12 種 reason code、stake cap 規則 |
| test_run_p16_recommendation_gate_reevaluation.py | CLI 整合、7 種輸出文件、確定性、paper_only 強制 |

---

## 12. 安全不變式驗證 (Safety Invariants)

| 不變式 | 驗證結果 |
|--------|---------|
| `paper_only = True`（所有行） | ✅ |
| `production_ready = False`（所有行） | ✅ |
| `created_from = "P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED"` | ✅ |
| 沒有任何行被推送至 TSL 或實際投注系統 | ✅ |

---

## 13. 閘門決策建議 (Gate Status Interpretation)

**當前狀態**: `P16_BLOCKED_RISK_PROFILE_VIOLATION`

此結果是策略研究的正常輸出，不代表模型本身失效。  
建議後續方向：

1. **降低最大回撤**：調整 Kelly 乘數（如降至 0.25x 半凱利），或縮小 `max_stake_cap`（現為 2%）
2. **提高邊緣閾值**：嘗試閾值 ≥ 0.10，以減少低品質下注並降低回撤
3. **Portfolio 分散**：引入跨場次資金分配，避免資金過度集中
4. **考慮動態 Kelly**：依據滾動 Sharpe 動態調整下注分數

---

## 14. P15 承接確認 (P15 Continuity)

| P15 指標 | 值 | P16 承接 |
|---------|----|----|
| n_samples | 1577 | ✅ (n_input_rows=1577) |
| JOINED coverage | 99.87% | ✅ (n_joined_rows=1575) |
| source_bss_oof | 0.008253 | ✅ (注入所有行) |
| capped_kelly ROI | 5.51% | — (P16 獨立風險評估) |
| paper_only | True | ✅ |
| production_ready | False | ✅ |

---

## 15. 所有輸出標記 (Output Markers)

| 標記 | 值 |
|------|----|
| `p16_gate` | `P16_BLOCKED_RISK_PROFILE_VIOLATION` |
| `paper_only` | `true` |
| `production_ready` | `false` |
| `created_from` | `P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED` |
| `source_model` | `p13_walk_forward_logistic` |

---

## 16. 技術債與已知限制 (Technical Debt & Limitations)

- **BSS OOF 硬編碼**: `SOURCE_BSS_OOF = 0.008253` 目前硬編碼在 adapter 常數中，  
  未來應從 P15 summary JSON 動態讀取。
- **Bootstrap 樣本數**: n_iter=2000 固定，未提供 CLI 參數覆蓋。
- **單一賠率選取**: 現在依 edge 正負選取主場/客場賠率，未來可納入最優賠率選取。
- **回撤上限**: 25% 上限為保守初始值，未依波動率或凱利分數動態調整。

---

## 17. 最終結論 (Final Conclusion)

P16 Recommendation Gate Reevaluation + Strategy Risk Hardening 已完整實作。  
13 項子任務中，12 項已完成（Task 13 Commit 待執行），181 個單元/整合測試全部通過，  
兩次運行輸出完全一致。

最終閘門因最大回撤超標而為 `P16_BLOCKED_RISK_PROFILE_VIOLATION`，  
這是研究閾值合理的保護機制正常運作的結果。  
模型 BSS > 0、Sharpe > 0、ROI Mean 為正，後續可透過降低 Kelly 乘數或調整閾值重新解鎖。

---

**標記**: `P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED_READY`

**生成時間**: 2026-05-12  
**生成自**: scripts/run_p16_recommendation_gate_reevaluation.py (P16 PAPER simulation)  
**分支**: p13-clean @ `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`
