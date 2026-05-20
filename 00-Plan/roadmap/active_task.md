# Active Task — P2 Pregame Odds Timeline Feasibility Audit

> **[COMPLETE 2026-05-20]** P2_PREGAME_ODDS_TIMELINE_FEASIBILITY_AUDIT
> Status: 完成 → Final Classification: `P2_LIMITED_TIMELINE_SMOKE_ONLY`
> MLB pregame-safe games: 0 / TSL WBC pregame-safe games: 797
> P1 w_market sweep: BLOCKED (MLB pregame odds unavailable)

---

## Previous Task (Completed) — P0 Market Probability Timestamp Leakage Audit

> **[COMPLETE 2026-05-20]** P0_MARKET_PROBABILITY_TIMESTAMP_LEAKAGE_AUDIT
> Status: 完成 → Final Classification: `P0_MARKET_BASELINE_LEAKAGE_CONFIRMED`
> Leakage type: post_game_proxy (100%), pregame_safe=0%
> P1 w_market sweep: BLOCKED → P2 launched to assess pregame odds availability

---

# Previous Task (Completed) — P23 Gate & Reproducibility Reconciliation (含 Regression Rerun)

## 任務名稱

`P23_GATE_AND_REPRODUCIBILITY_RECONCILIATION_20260520`

## 背景

1. P22 已完成 `CLV_VALIDATION_ONLY`，但留下兩個 P0 級阻塞：
   - **Gate 矛盾**：`p22_ceo_decision_branch_20260523.json` 顯示 `p23_allowed=true` (REPORT_REVIEW_ONLY)，而 `p22_hold_ready_gate_refresh_20260523.json` 與 `report/p22_final_validation_20260523.md` 顯示 P23 blocked / next owner CEO。
   - **可重現性風險**：P19 canonical `valid_clv_pairs=233`，P22 derived `valid_pairs_used=236`，差 +3。`data/tsl_odds_history.jsonl` 從 P19 報告的 2,747 records → P22 報告 2,772 → 現行檔案 2,785 行，source 仍在成長。
2. P22 報告聲稱 `347/347 PASS`，但本次 CTO/CEO 審查皆未實測。CEO 要求 P0 必須親自 rerun。
3. CEO 已裁決今日唯一方向為本 P0 任務，主軸一 (paper recommendation) 與主軸二 (optimizer diagnostic) 在 P0 完成前皆不啟動。

## 目標

1. 產出單一 canonical P23 gate state artifact，明確 `p23_allowed`、scope、owner、forbidden actions、promotion freeze。
2. 解釋並文件化 236 vs 233 pair delta 的 root cause（window rule / pair derivation / duplicate handling / invalid-to-valid reclassification）。
3. 對 `data/tsl_odds_history.jsonl` 與相關 P19/P22 source artifacts 計算並 pin：line-count、sha256、時間範圍、derivation rule reference。
4. 親自 rerun 測試（**不可沿用 P22 報告數字**）：
   - P17 standalone
   - P12-P17 regression governance suite
5. 產出 final validation report 與 BettingPlan 交接。
6. 所有產出維持 `paper_only=true`。

## 允許修改範圍

- 新增以下 artifact：
  - `data/paper_recommendations/p23_gate_reconciliation_20260520.json`
  - `data/paper_recommendations/p23_pair_delta_root_cause_20260520.json`
  - `data/paper_recommendations/p23_source_snapshot_pin_20260520.json`
  - `data/paper_recommendations/p23_regression_rerun_20260520.json`
- 新增以下報告：
  - `report/p23_gate_reconciliation_20260520.md`
  - `report/p23_pair_delta_root_cause_20260520.md`
  - `report/p23_source_snapshot_pin_20260520.md`
  - `report/p23_regression_rerun_20260520.md`
  - `report/p23_final_validation_20260520.md`
  - `00-BettingPlan/20260520/p23_gate_and_reproducibility_reconciliation_20260520.md`
- 允許讀取 P19 / P22 既有 artifacts、`data/tsl_odds_history.jsonl`、`scripts/p22_pipeline.py`。

## 禁止修改範圍

- ❌ 不得修改 `data/tsl_odds_history.jsonl` 或任何 raw source data
- ❌ 不得修改 TSL crawler / odds ingestion 程式碼
- ❌ 不得呼叫 live odds API
- ❌ 不得新增 repo / worktree
- ❌ 不得 merge PR #2
- ❌ 不得執行 optimizer promotion、champion replacement、production proposal
- ❌ 不得宣稱可獲利 / profitability claim
- ❌ 不得發布 betting recommendation
- ❌ 不得啟動 P23-C/D/E (distribution / market / sanity check) — 屬於 P1 範圍
- ❌ 不得修改 `00-Plan/roadmap/CTO-Analysis.md`
- ❌ 不得修改 production registry / champion 設定

## 驗收標準

1. `p23_gate_reconciliation_20260520.json` 必含：
   - `p23_allowed: true|false`
   - `p23_scope: "GATE_AND_REPRODUCIBILITY_RECONCILIATION_ONLY"`
   - `owner`、`forbidden_actions[]`、`promotion_frozen: true`、`champion_preserved: "fixed_edge_5pct"`、`paper_only: true`
   - 明確指出採用 P22-B 還是 P22-E 為 canonical，並說明理由
2. `p23_pair_delta_root_cause_20260520.json` 必含：
   - `p19_valid_pairs: 233`、`p22_valid_pairs: 236`、`delta: 3`
   - `root_cause_category`、`evidence`、`reproducible: true|false`
   - 若無法解釋 → `classification: "PAIR_COUNT_DELTA_REQUIRES_REVIEW"`，並標記 P1 不得啟動
3. `p23_source_snapshot_pin_20260520.json` 必含：
   - `data/tsl_odds_history.jsonl` 的 `line_count`、`sha256`、`first_record_ts`、`last_record_ts`
   - P19 source baseline 與 P22 source baseline 的 hash/line-count（若可重建）
4. `p23_regression_rerun_20260520.json` 必含：
   - 親自執行的 pytest 結果（總數 / PASS / FAIL / 執行時間 / 環境）
   - 與 P22 報告 `347/347` 的比對結果
5. Final validation report 必含 grep scan 7/7 CLEAN：
   - `production proposal` / `promotion` / `champion replacement` / `profitability` / `live API` / `crawler modification` / `paper_only`
6. 全部 5 個 JSON artifact schema 含 `paper_only=true`、`network_call=false`、`crawler_modified=false`、`profitability_claim=false`

## 測試指令

```bash
cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool

# 1. P17 standalone
pytest tests/ -k "p17" -v --tb=short

# 2. P12-P17 regression governance suite
pytest tests/ -k "p12 or p13 or p14 or p15 or p16 or p17" -v --tb=short

# 3. 全套 baseline（記錄總數）
pytest tests/ --tb=short -q

# 4. grep scan（在新產出檔內容上）
grep -RniE "promotion|champion replacement|profitab|live odds api|crawler modif" \
  data/paper_recommendations/p23_*_20260520.json report/p23_*_20260520.md || echo "GREP_CLEAN_CANDIDATE"

# 5. source snapshot
wc -l data/tsl_odds_history.jsonl
shasum -a 256 data/tsl_odds_history.jsonl
```

## 輸出報告位置

- JSON artifacts: `data/paper_recommendations/p23_*_20260520.json` (4 個)
- MD reports: `report/p23_*_20260520.md` (5 個)
- BettingPlan 交接: `00-BettingPlan/20260520/p23_gate_and_reproducibility_reconciliation_20260520.md`

## Final Classification（任務結束時擇一）

- `P23_GATE_AND_REPRODUCIBILITY_RECONCILED` — 三項全部完成且 regression PASS
- `P23_PAIR_COUNT_DELTA_REQUIRES_REVIEW` — gate 解決但 pair delta 無法解釋
- `P23_BLOCKED_BY_TEST_REGRESSION` — regression rerun 出現 FAIL
- `P23_BLOCKED_BY_SCOPE_VIOLATION` — 任務過程逾越禁止範圍

## CEO Invariants（強制）

- `paper_only=true` 全程維持
- promotion / champion replacement / production proposal / live API / crawler modification 全部禁止
- PR #2 不得 merge
- `fixed_edge_5pct` champion 保留
- 主軸一 (paper recommendation) 與主軸二 (optimizer diagnostic) **今日不啟動**
