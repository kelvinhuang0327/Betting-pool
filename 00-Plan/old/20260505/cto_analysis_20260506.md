# CTO Agent — 系統下一階段優化方向分析

**Document ID:** `cto_analysis_2026-05-06`
**Date:** 2026-05-06
**Author:** CTO Agent (deterministic, no external AI invoked)
**Inputs:**
1. `00-Plan/betting_roadmap_20260504.md`（180-day MLB Optimization Plan v1, 含 Phase 36 Budget Guard 補充）
2. `00-Plan/20260505.md`（昨日工作報告：Phase 35 / 42A / 43–58）
3. `CLAUDE.md`（專案規範）

**Scope:** Plan-only。本文件不觸發任何 patch、不繞過 review、不調整 production model。

---

## 0. TL;DR (給三分鐘讀者)

1. **方向判斷**：昨日方向「正確但偏科」。研究紀律與治理底線守住了，但**整個團隊把 roadmap 的 Workstream B（模型 / 特徵）一次衝到 Phase 58，卻完全跳過了 Workstream E（Budget Guard）和 Workstream A（架構基石）**。架構債正在快速累積。
2. **不建議直接做 Phase 59**：在投入 2–3 天去抓真實 boxscore 之前，**先用 1 天做一個便宜的反事實實驗**（heavy_favorite bucket 的 isotonic re-calibration），確認「真的是 bullpen 缺特徵」這個假設。否則我們有可能把工程資源砸在錯方向上。
3. **下一階段的 P0 應該是「架構與治理補課 sprint」**，把 Budget Guard、LeagueAdapter 骨架、Metrics SSOT、no-lookahead test gate、Feature Registry 補上 — 然後才接 Phase 59（真實 bullpen 資料）。
4. **Roadmap 需要修訂**：在現有 Phase 0 與 Phase 1 之間，插入 **「Phase 0.5 — Architecture & Governance Catch-up（10–14 天）」**，把已偏離的順序拉回來。北極星 KPI、180 天總時程不變。

---

## 1. Roadmap 對齊度 Audit

### 1.1 Roadmap 原本期望的執行順序（First 10 Tasks）

| Order | Task | Workstream | Status (2026-05-05) |
|---|---|---|---|
| T1 | Glossary `league_codes.md` | A | ❌ 未做 |
| T2 | Budget Guard | E | ❌ 未做（Phase 36 還沒啟動）|
| T3 | Planner external-AI invariant assert | E | ❌ 未做 |
| T4 | UI Budget panel | E | ❌ 未做 |
| T5 | `LeagueAdapter` + `MLBAdapter` 包覆 | A | ❌ 未做 |
| T6 | Metrics SSOT (`evaluation/metrics.py`) | A/B | ❌ 未做 |
| T7 | `test_no_lookahead.py` | B | ⚠️ 部分（Phase 48 自製 leakage_guard，但非統一框架）|
| T8 | MLB Data Inventory doc | B | ❌ 未做 |
| T9 | `PredictionState` state machine | A | ❌ 未做 |
| T10 | `LearningMemoryRepository` | A/C | ❌ 未做 |

### 1.2 實際昨日做了什麼 → 對應到哪個 Workstream

昨日完成 19 個 Phases，幾乎全部落在 **Workstream B（Phase 6.x — MLB Prediction Accuracy）** 的 Phase A/B 段：

| Phase | 對應 Roadmap 位置 | 重要性 |
|---|---|---|
| 35 | Workstream D 邊角（CLV ops runbook） | M |
| 42A | §6.3 Phase A — Baseline Calibration 已基本達成 | **H** |
| 43 / 44 | §6.4 Validation Methodology 局部落地（fold stability、bootstrap CI、paper-only gate） | **H** |
| 45 | §6.2 attribution（segment-level）— **新增**，原 roadmap 未明列 | **H** |
| 46–50 | §6.2 Feature engineering — `park_run_factor`、`season_game_index`、`sp_fip_delta` | M |
| 51–54 | §6.2 Feature 第一名訊號 SP 完整閉環 | **H** |
| 55 | 假設驗證：「SP 不夠 → bullpen 缺口」 | M |
| 56–58 | Bullpen pipeline 架構（proxy fallback） | M |

### 1.3 對齊度結論

| 維度 | 評估 |
|---|---|
| Workstream B（模型/特徵）進度 | **超前**（已做到 Phase 1 末段、部分跨入 Phase 2）|
| Workstream E（Budget Guard） | **完全落後**（Phase 36 prompt 已寫好但未執行）|
| Workstream A（架構基石）| **完全落後**（無 LeagueAdapter、無 PredictionState、無 Metrics SSOT、無 LearningMemoryRepository）|
| Workstream C（Simulation framework）| 局部（Phase 43 fold + bootstrap、Phase 45 attribution 算雛形） |
| Workstream D（Scheduler priority-score） | 未開始 |
| 治理與紀律（governance discipline） | **持續高**（不 patch、不調 alpha 騙、不用小樣本宣稱、PIT safe）|

→ **整體**：方向沒錯，但**「研究進度」遠領先「架構與治理基礎建設」**。這是典型的科研 sprint 完成後出現的失衡，需要立即補課，否則接下來每加一個 Phase（如 59、60）都會在臨時架構上疊加新債。

---

## 2. 關鍵阻塞與風險（CTO 視角）

### 2.1 阻塞 #1：模型「heavy_favorite / high_confidence 失敗」根因尚未鎖定（**最關鍵**）

**現象**：
- Phase 45：`gate = FEATURE_REPAIR_INVESTIGATION`，主要問題 = structural ECE failure / overconfidence
- Phase 52A：SP 注入後 heavy_favorite ECE **輕微惡化**
- Phase 54：6 個 failure segments 仍存在
- Phase 55：6 種 SP functional form 都沒明顯改善 → 直接跳到 `BULLPEN_FEATURE_INVESTIGATION`

**CTO 質疑**：從 Phase 55 「6 種 SP form 沒效 → 一定是 bullpen」這個推論是 **過早收斂**。可能的另一條根因：
1. **Calibration layer 本身缺局部 isotonic**：global ECE 良好不代表 bucket-level 良好；prob ≥ 0.7 的區段如果 over-confidence，是個典型的「Pinnacle/sharp 市場本身已經 squeeze 掉 favorite-bias，但我們的 model 沒有」的 calibration 問題，不一定要新特徵才能修。
2. **Market blend α=0.4 在 favorite 區可能反而放大 over-confidence**：因為大盤對 heavy favorite 通常 sharp，但 model 對 heavy favorite 不準 → blend 後反而拉錯方向。
3. **真的是 bullpen 缺口**：Phase 55 的 `bullpen_missing_score=0.6` 是個 heuristic，不是統計證據。

**風險**：
- 若直接做 Phase 59（boxscore acquisition），需要 2–3 天工程 + 真實 boxscore 抓取（可能 rate limit / cache 設計成本高）
- 一旦真實 bullpen data 接上，Phase 60 重跑後**仍是 NOT_SIGNIFICANT**，那等於這 5–7 天的最大產出只是「驗證了 bullpen 不是答案」

### 2.2 阻塞 #2：架構債在快速累積

昨日新增 / 修改的 pipeline 檔案（從 Phase 58 描述提取）：
- `mlb_bullpen_usage_loader.py`
- `mlb_relief_appearance_parser.py`
- `mlb_bullpen_usage_snapshot.py`
- `mlb_bullpen_pit_validator.py`
- `run_phase58_bullpen_usage_backfill.py`
- `run_phase58_inject_bullpen_usage_to_phase56.py`
- `run_phase58_bullpen_feature_injection.py`
- `phase58_bullpen_usage_evaluation.py`
- `run_phase58_bullpen_usage_pipeline.py`
- `test_phase58_bullpen_usage_pipeline.py`

加上 Phase 48 / 50 / 52 / 53 的 P0 feature builders、SP backfill 等，**這幾天已產生 20+ 個新模組**，但全部不在 `LeagueAdapter` / `Feature Registry` 抽象之下。

**風險**：
- 等 T5 LeagueAdapter 真的開始做時，要一次搬 20+ 個檔案的 import（典型「import 風暴」），cost 是現在搬的 5–10 倍。
- 這些 Phase 5x 的 feature builders **沒有統一 schema**（每個 Phase 自寫一份），導致未來 walk-forward 與 ensemble 整併時資料對齊成本飆升。

### 2.3 阻塞 #3：Budget Guard 仍然空缺（governance 紅線）

Roadmap 補充段（Phase 36）已明確：
> 我會把 Phase 36 放在所有模型優化之前，因為這是你目前實際遇到的痛點：Copilot / Claude 用量可見，但尚未被治理。

**昨日 19 個 Phases 全程沒做 Budget Guard**。在 Worker 端 Copilot / Claude 重度使用的情況下：
- 沒有 hard cap → 一個 worker bug loop 可能在一晚燒掉整個月額度
- 沒有 Planner external-AI invariant assertion → governance hard rule 仍只靠紀律不靠程式

### 2.4 阻塞 #4：Metrics SSOT 缺失，BSS 數字可能在打架

- Phase 42A：Best calibrated BSS ≈ +0.28%
- Phase 43：fold-level blend_bss
- Phase 49 / 50 / 52A / 54：各自算 delta_bss
- Phase 45：segment delta_bss

這些 BSS 是不是**用同一個函數、同一個 baseline、同一個 sample weight** 算出來的？沒有 `wbc_backend/evaluation/metrics.py` SSOT 之前，**這些數字之間能不能直接比較是有疑問的**。

### 2.5 阻塞 #5：No-lookahead test 是個別檔案的 leakage_guard，不是統一 gate

Phase 48 寫了「leakage guard 成功攔截 home_win」— 這是好事，但這只是 Phase 48 builder 內部的檢查。**roadmap T7 要求的 `tests/feature_validation/test_no_lookahead.py` 統一框架仍未存在**。隨著新特徵越來越多（park、season、SP、bullpen workload、bullpen leverage、b2b…），洩漏只會越來越難肉眼抓到。

---

## 3. 重排 P0 / P1 / P2

### 3.1 P0（最優先，建議下個 sprint，2 週內完成）

| Rank | 項目 | Workstream | 為何此刻必須做 | Effort |
|---|---|---|---|---|
| **P0-1** | **Phase 59 前置：Heavy-favorite Isotonic Counterfactual Experiment** | B | 在投入 boxscore acquisition 之前，**用 1 天驗證假設**：「heavy_favorite ECE 惡化是否能用 isotonic / monotonic local re-calibration 修好」。若能修 → bullpen 不是唯一根因，Phase 59 投入順序要重排 | S (1 day) |
| **P0-2** | **Phase 36 — Usage Budget Guard**（roadmap T2/T3/T4 合一）| E | Worker Copilot/Claude 用量已是現實痛點；Planner external-AI invariant 是 hard rule。governance 不能再延 | M (3–4 day) |
| **P0-3** | **T5 — `LeagueAdapter` 骨架 + 把 Phase 56–58 bullpen pipeline 折進 `MLBAdapter`** | A | 阻止架構債繼續滾雪球；昨日新增 10+ pipeline 檔案如果這週不收編，下週 Phase 59 又會多 5–10 個 | M (3 day) |
| **P0-4** | **T6 — `wbc_backend/evaluation/metrics.py` SSOT** | A/B | Phase 42A/43/45/49/50/52/54 的 BSS / ECE / delta 數字必須統一基準，否則後續 Phase 60 比較 Phase 54 的 baseline 時等於用兩把尺 | M (2 day) |
| **P0-5** | **T7 — `tests/feature_validation/test_no_lookahead.py` 統一框架** | B | Phase 50–58 的 features 全部要回填這層 gate；越晚做、回填工作量越大 | M (2 day) |
| **P0-6** | **Phase 59 — Real Bullpen Boxscore Acquisition & Cache Builder** | B | **僅在 P0-1 結果不能單靠 calibration 修好時才做**；做的話需建在 P0-3 的 `MLBAdapter` 上 | L (3–5 day) |

### 3.2 P1（重要，4–6 週內完成）

| Rank | 項目 | 為何 P1 |
|---|---|---|
| P1-1 | **Feature Registry**（feature name / version / source / PIT rule / availability / lineage / audit hash） | 昨日新增 ≥ 5 個 features (park_run_factor, season_game_index, sp_fip_delta, bullpen_workload_proxy, etc.)；無 registry 就無法 walk-forward / ensemble |
| P1-2 | **Phase 60 — Bullpen Real Backfill Evaluation**（重跑 Phase 45 / 49 / 54）| 在 P0-6 完成後立即做 |
| P1-3 | **CLV + BSS joint gate** | 目前 BSS 與 CLV 是兩條線；patch gate 必須同時看 |
| P1-4 | **T9 — `PredictionState` state machine** | 散落 if/else 在 Phase 5x 又繼續長，狀態爆炸前要收斂 |
| P1-5 | **T10 — `LearningMemoryRepository`** | 昨日 Phase 4x/5x 寫了多個 evidence pack JSON；統一 repo 再做 retention |
| P1-6 | **Walk-forward / rolling monthly evaluation harness** | 目前是固定 2025 JSONL，無法做 OOS rolling |
| P1-7 | **T8 — MLB Data Inventory doc** | 在 Phase 59 boxscore / Statcast / FanGraphs 接入前必須有 SLA / rate limit 表 |

### 3.3 P2（架構完善，2–3 個月內）

| Rank | 項目 |
|---|---|
| P2-1 | T1 — Glossary `league_codes.md`（XS effort，何時做都行，建議捎帶完成） |
| P2-2 | Decision Card 整合 Phase 58/59/60 區塊（feature availability / PIT / gate / failure segments） |
| P2-3 | Audit Dashboard frontend |
| P2-4 | Scheduler priority-score v1（Workstream D） |
| P2-5 | Bullpen functional form / coefficient calibration（前提：P0-6 + P1-2 顯示 bullpen 真有 value） |
| P2-6 | Persistence JSONL → SQLite 評估（90 天後） |

---

## 4. Roadmap 落差與調整建議

### 4.1 落差總結

1. **執行順序顯著偏離**：Roadmap 的 T1–T10 順序是 governance → 架構 → 模型；實際執行是直接跳到模型（Phase 42–58），governance 與架構**全部欠帳**。
2. **新增 phases 未進入 roadmap**：Phase 35 / 42A / 43 / 44 / 45 / 46 / 47 / 48 / 49 / 50 / 51 / 52 / 52A / 53 / 54 / 55 / 56 / 57 / 58 — 這 19 個 phase 全部是 roadmap 撰寫後才出現。Roadmap 的 §10 Phase Plan 表只列了 Phase 0–4，**缺乏 phase number 對應**，造成 prompt 端與 plan 端各自成章。
3. **Bullpen 議題未入原 roadmap §6.2**：原 feature backlog 表把 bullpen state 放在 row #3（pri 4），但沒有列出「需要真實 boxscore acquisition」的子任務 → Phase 57–58 是邊做邊發現的。
4. **「CONDITIONAL_VALUE / FEATURE_REPAIR_INVESTIGATION」這類細粒度 gate**沒在原 roadmap §11.4 Acceptance Gates 列出，建議加進 gate vocabulary。

### 4.2 建議的 Roadmap 修訂（最小變更）

#### 變更 1：在 Phase 0 與 Phase 1 之間插入 Phase 0.5

```
Phase 0   ──── Phase 0.5 ──── Phase 1 ──── Phase 2 ──── Phase 3 ──── Phase 4
Stabilize    Catch-up        Foundation    Validation    Self-Learn   Production-Proposal
(Day 0–14)   (Day 15–28)     (Day 29–60)   (Day 61–90)   (Day 91–150) (Day 151–180)
```

**Phase 0.5 — Architecture & Governance Catch-up（10–14 天）**
- Goal：把 Budget Guard、LeagueAdapter、Metrics SSOT、no-lookahead gate、Feature Registry 一次補上
- 對應上面的 P0-2 / P0-3 / P0-4 / P0-5 + P1-1
- Success criteria：
  - Budget Guard hard cap 可阻擋 Worker subprocess
  - Phase 56–58 bullpen pipeline 已折入 `MLBAdapter`
  - Phase 42A/43/45/49/50/52/54 之 BSS / ECE 全部用 SSOT 重算一次，數字一致
  - 所有 Phase 5x 的 features 通過 `test_no_lookahead.py`
  - Feature Registry 至少寫入 5 個 feature 的 lineage

#### 變更 2：Phase 1 起增加「Phase Number 對應表」

把 Phase 35 / 42A / 43–58 都掛到 Workstream B / D，明確標註「此 Phase 屬於 Phase 1 第 X 段」。避免 prompt 端的 PhaseNN 與 plan 端的 Phase 0–4 失聯。

#### 變更 3：§6.2 Feature Backlog 補列「資料取得難度」欄位

例如 bullpen state 這列要明確：
```
Bullpen state | data acquisition: HIGH (需 boxscore + relief appearance parser + cache + PIT)
```
避免下次出現「pipeline 蓋好但資料 0%」的循環。

#### 變更 4：§11.4 Acceptance Gates 擴充 gate 詞彙表

現有：`LEARNING_READY` / `PATCH_GATE_RECHECK` / `PROPOSAL_DRAFTED` / `HUMAN_REVIEW_APPROVED` / `DEPLOYED`
建議加入：
- `MARKET_BLEND_PAPER_ONLY`
- `FEATURE_REPAIR_INVESTIGATION`
- `FEATURE_REPAIR_NOT_EFFECTIVE`
- `FEATURE_INJECTION_REQUIRED`
- `FEATURE_COEFFICIENT_PAPER_ONLY`
- `FEATURE_REPAIR_STILL_WEAK`
- `BULLPEN_FEATURE_INVESTIGATION`
- `DATA_GAP_REMAINS`

並把每個 gate 的「下一步建議動作」表格化。

#### 變更 5：明確「便宜實驗優先」原則

寫入 §15 Final Recommendation：
> 在投入 ≥ 2 天工程到資料取得 / 新 pipeline 前，**先用 ≤ 1 天的 calibration / re-bucketing 反事實實驗**驗證假設。

### 4.3 不建議的調整

- ❌ 不要因為昨日進度快就把 180 天時程縮短 — 樣本累積與 walk-forward 仍需要時間
- ❌ 不要把「Phase 59 真實 bullpen」直接升到 P0 第一順位 — 還沒做 P0-1 calibration 反事實實驗之前不應該動
- ❌ 不要 retro 改 Phase 35–58 的標號 — 維持歷史可追溯比規範化重要

---

## 5. 兩週行動計畫（建議下個 sprint）

| Day | Action | Owner | 對應 P0 | Output |
|---|---|---|---|---|
| D1 | Heavy-favorite isotonic counterfactual experiment（用既有 Phase 42A JSONL，bucket prob ≥ 0.7 做 isotonic / Platt 局部校正） | Worker | P0-1 | `report/phase59_pre_isotonic_counterfactual.md`，輸出 ECE / BSS delta |
| D1 (晚) | CTO review counterfactual 結果，決定 Phase 59 是否仍為必要 | CTO | — | go / no-go 決策 |
| D2–D4 | Budget Guard schema + evaluator + scheduler integration + UI | Worker | P0-2 | `orchestrator/usage_budget_guard.py`、tests、UI |
| D5 | Planner external-AI invariant assertion + alert path | Worker | P0-2 | tests pass，misconfig 觸發 critical |
| D6–D7 | `wbc_backend/league/base.py` + `MLBAdapter` skeleton + 把 Phase 56–58 bullpen 模組導入 | Worker | P0-3 | adapter, behavior unchanged, import test 通過 |
| D8–D9 | `wbc_backend/evaluation/metrics.py` SSOT，重算 Phase 42A/43/45/49/50/52/54 BSS / ECE | Worker | P0-4 | metrics.py + 一次 cross-check report |
| D10–D11 | `tests/feature_validation/test_no_lookahead.py` 框架 + 把 Phase 48/50/52/56–58 的 features 都塞進去 | Worker | P0-5 | test 全綠，含一個故意 leak 的 negative test |
| D12 | Feature Registry skeleton（YAML/JSON 都可）+ 寫入 5 個 feature lineage | Worker | P1-1 | `wbc_backend/features/registry.py` + `features/registry.yaml` |
| D13 | (條件啟動) Phase 59 — Real Bullpen Boxscore Acquisition kick-off | Worker | P0-6 | Phase 59 day 1 progress |
| D14 | Sprint retrospective + Roadmap v1.1 update（含 Phase 0.5、phase mapping 表、gate vocabulary）| CTO | — | `betting_roadmap_20260520.md` |

---

## 6. 給下個 Agent 的 Prompt 指引（建議標題）

如果今日要立即派出 agent 行動，建議**第一順位 prompt 不是 Phase 59**，而是：

```
Phase 59-Pre — Heavy-Favorite Isotonic Counterfactual Experiment
```

**目的**：在投入真實 bullpen boxscore acquisition 之前，**用 1 天驗證**「heavy_favorite ECE 失敗是否能單靠 local probability calibration 修好」，避免錯把 5–7 天工程資源砸在錯方向。

**SOP**：
1. 讀取 Phase 42A 的 `mlb_2025_per_game_predictions_phase48_p0_v1.jsonl`
2. 切 prob bucket（如 0.5–0.6 / 0.6–0.7 / 0.7–0.8 / 0.8–0.9 / 0.9+）
3. 對 prob ≥ 0.7 子集分別跑 isotonic regression / Platt scaling
4. 比較 segment-level ECE / BSS（Phase 45 attribution segments）
5. 輸出 gate：
   - `LOCAL_CALIBRATION_SUFFICIENT` → 暫緩 Phase 59，先做 calibration patch
   - `BULLPEN_HYPOTHESIS_RETAINED` → 進 Phase 59
   - `MIXED` → 兩條路並行
6. 嚴禁：production patch / 改 alpha / sample 切到 < 1500

第二順位 prompt 才是 **Phase 36 — Usage Budget Guard**（roadmap 補充段已有完整 prompt）。

---

## 7. CTO 結論（一句話）

> 昨日的研究方向是對的、紀律是強的，但**「研究跑太快、架構跟治理沒跟上」**這個失衡狀態，必須在這個 sprint 用「先做便宜反事實實驗 + 同步補 Budget Guard / LeagueAdapter / Metrics SSOT / no-lookahead gate」來校正。**P0 不是 Phase 59，而是 P0-1 ~ P0-5；Phase 59 的優先級應在 calibration 反事實實驗結果出來之後，根據證據再排。**

---

**CTO_ANALYSIS_2026-05-06_VERIFIED**
