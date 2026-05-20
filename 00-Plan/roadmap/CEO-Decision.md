# CEO Decision — P22 後置二次審查與今日方向裁決

## P0 完成 & P2 啟動原因（2026-05-20 補記）

- **P0 Final Classification**: `P0_MARKET_BASELINE_LEAKAGE_CONFIRMED`
  - `mlb_odds_2025_real.csv` 無 `snapshot_timestamp`，`pregame_safe=0%`
  - P29 pure market Brier=0.244354 不可作為 P1 sweep 基準
  - P1 w_market ablation sweep **暫停**
- **P2 啟動原因**: P0 blocking P1 → 需先盤點系統是否有 pregame-safe odds
- **P2 Final Classification**: `P2_LIMITED_TIMELINE_SMOKE_ONLY`
  - MLB pregame-safe=0，TSL WBC pregame-safe=797
  - P1 持續暫停，需另行建立 MLB live odds pipeline

---

## 1. CEO Review Date

2026-05-20 Asia/Taipei

備註：
- [Confirmed] 環境日期為 2026-05-20。
- [Inferred] 工件標籤 `20260523` 為交接 artifact label，非作業日期已推進的證據。

## 2. Reviewed Inputs

- [Confirmed] `00-Plan/roadmap/roadmap.md`
- [Confirmed] `00-Plan/roadmap/CTO-Analysis.md`
- [Confirmed] `00-Plan/roadmap/current_state.md`（昨日工程交接報告）
- [Confirmed] P22 系列 JSON / MD artifacts（透過 CTO 報告引用）

未執行：
- [Confirmed] CEO 本輪未直接重跑 pytest 或修改 CTO-Analysis.md。

## 3. Yesterday Work Value Assessment

| 項目 | 評估 | 標記 |
|---|---|---|
| P22 CLV validation-only 完成 | 治理成熟度推進，非產品成熟度推進 | [Confirmed] |
| `APPROVE_CLV_VALIDATION_ONLY` CEO decision artifact 建立 | 解開 P19-P21 的 CEO 阻塞 | [Confirmed] |
| `347/347 PASS`、grep 7/7 CLEAN | 來自 P22 報告，未在本輪 rerun | [Inferred][Risk] |
| 236 valid pairs / mean CLV +0.2332% / std 8.7212% / positive rate 32.65% | 描述性數據，**不構成可獲利或可促升證據** | [Confirmed] |
| HDC +1.2103% / MNL -0.2490% | 描述性差異，未經 outlier sensitivity / CI 驗證 | [Risk] |
| `fixed_edge_5pct` champion preserved、promotion frozen | 治理狀態正確 | [Confirmed] |
| 236 vs 233 pair delta 與 source 檔成長 (2747 → 2772 → 2785) | **可重現性風險，未解釋** | [Risk] |
| P23 gate 在 P22-B vs P22-E 不一致 | **治理一致性風險，未解決** | [Risk] |

結論：昨日成果只達「驗證型完成」，未達「系統成熟度推進」，且引入兩個 P0 級阻塞 (gate contradiction + reproducibility)。

## 4. CTO Judgment Review

採納項：
- [Confirmed] P0 = P23 gate + pair-count reconciliation
- [Confirmed] P1 = CLV robustness diagnostic-only
- [Confirmed] promotion / champion replacement / production proposal 全部 frozen
- [Confirmed] P20/P21 retired
- [Confirmed] PR #2 不得在無 `YES: merge PR #2` 下合併

修正項：
- [Inferred] CTO P2 為「TSL market taxonomy」，未顯式掛勾**主軸一 MLB 對台彩 paper recommendation**，CEO 改寫 P2。
- [Risk] CTO 直接採信 `347/347 PASS`，CEO 要求 P0 任務必須 rerun。
- [Inferred] PR #2 在 CTO 排 P9，CEO 上拉至 P6。
- [Inferred] CTO P4 (strategy optimizer v2) 未設條件門檻，CEO 加入「必須在 P1 結論為 robust 或 weak-stable 才能啟動」。

最終判定：**CEO_DECISION_PARTIALLY_APPROVED**。

## 5. Roadmap Gap Assessment

| Gap | 處理方式 |
|---|---|
| P2 未對齊主軸一 | 改寫為「MLB → 台彩多市場 paper recommendation 證據契約」 |
| P3 未對齊主軸二前置 | 改寫為「CLV-to-Strategy Readiness Gate」 |
| P4 未設條件啟動 | 加入硬條件「依 P1 結論啟動」 |
| PR #2 governance 太低 | 上拉到 P6 |
| 缺乏 source snapshot pin 規範 | 併入 P0 acceptance |
| 缺乏 regression rerun 規範 | 併入 P0 acceptance |

## 6. CEO Priority Decision

| Priority | Phase | Done condition |
|---:|---|---|
| **P0** | P23 Gate Reconciliation + Pair-Count / Source Snapshot Reproducibility + Regression Rerun | 單一 canonical gate state；236 vs 233 root cause 文件化；source line-count + sha256 pin；P17 standalone + P12-P17 rerun 親自執行非沿用報告 |
| **P1** | CLV Robustness Diagnostic-Only | bootstrap CI / trimmed mean / outlier sensitivity / per-market CI；訊號分類 robust / weak-stable / inconclusive；無 promotion |
| **P2** | MLB → 台彩多市場 Paper Recommendation 證據契約（主軸一） | moneyline / 讓分 / 大小分 / 單雙 / 局數 每筆需含 model_prob、odds、edge、source、timestamp、gate、`paper_only=true` |
| **P3** | CLV-to-Strategy Readiness Gate（主軸二前置） | 由 P1 結論決定是否允許策略 diagnostic；champion 不替換 |
| **P4** | Strategy Simulation / Optimizer Diagnostic（條件性） | 僅在 P1 = robust 或 weak-stable 啟動；輸出 report-only |
| **P5** | MLB Prediction Quality Loop (Brier / ECE / calibration) | 模型可靠度持續監測 |
| **P6** | PR #2 / main branch governance 收斂 | PR #2 僅在 `YES: merge PR #2` 後合併；分支策略文件化 |
| **P7** | Data Versioning & Artifact SSOT | hash / line-count / 時間範圍 / derivation rule 全部 pin |
| **P8** | Market-Level Coverage Expansion | 在 P2 taxonomy + P1 diagnostic 後 |
| **P9** | Daily Paper Ops / Drift Monitor | CLV / Brier / no-bet / missing data |
| **P10** | Production Proposal Gate | 永久 blocked，直到多季 evidence + live licensed data + CEO 批准 |

## 7. Today Focus Direction

唯一方向：**P0 — Gate & Reproducibility Reconciliation（含 regression rerun）**

- 對應 phase：P0
- 重要性：P23 gate 矛盾 + 236 vs 233 pair delta + source 檔案 line-count 漂移，三者任一未解，下游 P1 / P2 / P3 全部會被污染。
- 系統成熟度推進：交接歧義轉為可稽核 gate 狀態；建立 source snapshot pinning baseline；測試狀態回到當下實測值。
- 預期收益：P1 / P2 可安全啟動；未來 CLV 報告可重現；governance audit trail 完整。
- 風險：純治理動作，無模型/收益改變；不做才是更大風險。
- 驗收標準：
  1. 單一 canonical `p23_allowed` 值 + scope + owner + forbidden actions
  2. 236 vs 233 root cause 文件化
  3. `data/tsl_odds_history.jsonl` line-count + sha256 pinned
  4. P17 standalone + P12-P17 regression rerun（**不沿用報告值**）
  5. 所有產出 `paper_only=true`，無 promotion / champion replacement / production / live API / crawler modification 字樣
- 是否採納 CTO：採納並加強。

## 8. Risks / Blind Spots

- [Risk] `347/347 PASS` 為報告值，本輪未實測。
- [Risk] `data/tsl_odds_history.jsonl` 仍在成長，未 pin snapshot 將導致 P1 diagnostic 不可重現。
- [Risk] HDC +1.21% 可能 outlier-driven，跳過 sensitivity 直接做 market 結論會誤導。
- [Unknown] P22-B (`p23_allowed=true`) vs P22-E (`p23_allowed=false`) 最終 authority。
- [Risk] `codex/main-sync-20260516` 與 main 分歧愈久整合成本愈高。
- [Risk] 主軸一 (paper recommendation) 易被治理議題遮蔽，CEO 顯式保留為 P2。
- [Inferred] 主軸二 (策略優化) 若在 P1 未通過前啟動，將造成 champion drift 風險。

## 9. CEO Final Decision

**CEO_DECISION_PARTIALLY_APPROVED**

- 採納 CTO 的 P0/P1 排序與全面 promotion freeze。
- 修正 P2/P3/P4/P6 對齊**主軸一 (MLB paper recommendation)** 與**主軸二 (策略優化條件啟動)**。
- 今日唯一執行方向為 P0 Reconciliation + Regression Rerun。
- 明令禁止：optimizer promotion、champion replacement、production proposal、live odds API、TSL crawler modification、profitability claim、PR #2 merge（除非顯式批准）。
- `paper_only=true` 為所有產出強制 invariant。

## 10. 10 行內 CEO 摘要

1. P22 完成屬治理成熟度，非產品成熟度。
2. CLV mean +0.2332%、std 8.7212%，訊號弱於波動，不可解讀為可獲利。
3. 採納 CTO P0/P1 排序，但部分修正。
4. P2 改為主軸一「MLB → 台彩 paper recommendation 證據契約」。
5. P3 改為主軸二前置「CLV-to-Strategy Readiness Gate」。
6. P4 optimizer 必須在 P1 結論為 robust/weak-stable 才能啟動。
7. PR #2 governance 上拉到 P6。
8. 今日唯一方向 = P0 reconciliation，且必須 rerun regression 不沿用報告值。
9. promotion / champion / production / live API / crawler 全部維持 frozen。
10. Final classification = `CEO_DECISION_PARTIALLY_APPROVED`。
