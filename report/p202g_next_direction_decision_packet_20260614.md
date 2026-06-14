# P202G-NEXT-DIRECTION — Fixture-Only vs Permission-Preparation 決策報告 (Read-Only Decision Packet)

> 本報告為 **read-only 決策備忘錄**，不是法律意見，亦不授權任何實作。所有「政策/法律」性質
> 結論一律以**專案風險決策 (project risk decision)** 形式陳述。本報告為本任務 **唯一寫入檔案**；
> 未修改任何 source / test / config / fixture / 治理檔，未呼叫任何 endpoint，未做任何 git 變更。

## Report Metadata

| 欄位 | 值 |
|---|---|
| `generated_at_utc` | `2026-06-14T02:33:13Z` |
| 報告檔名日期 | `20260614`（依任務指定檔名） |
| `repository` | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` |
| `branch` | `main`（symbolic HEAD = `main`，非 detached） |
| `HEAD` | `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e`（= `origin/main`） |
| `task ID` | `P202G-NEXT-DIRECTION` |
| Task Type | `READ_ONLY_DECISION_PACKET` |
| active_task | `P202G-NEXT-DIRECTION`（`PLAN_ONLY_REQUIRES_TASK_SPECIFIC_AUTHORIZATION`） |
| Latest completed classification | `P202G_A_PR23_MERGE_COMPLETE`（CURRENT_STATE 載 post-merge governance closeout） |
| Live transport status | **HOLD** |
| Policy evidence classification | `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`（automated-access = EXPLICITLY_PROHIBITED；StatsAPI applicability = `STRONGLY_SUPPORTED_INFERENCE`；purpose-matched licensing path = `NOT_ESTABLISHED`） |
| Decision confidence | **MEDIUM** |
| Primary track selected | **TRACK_A_PRIMARY** |
| Final Classification | `P202G_NEXT_DIRECTION_TRACK_A_SELECTED` |

---

## 1. Executive Decision（執行決策）

**選定 primary track：`TRACK_A_PRIMARY`（Fixture-Only Prediction Quality）。Decision confidence：MEDIUM。**

**決定性理由（decisive reason）**：在嚴格區分「直接預測品質影響」與「間接賦能價值」後，**只有 Track A 能在不依賴受限 live 資料的前提下，產出可證偽 (falsifiable) 的預測品質證據**；Track B（書面許可請求草稿）對「提高 MLB 預測成功率」的**直接貢獻為零**，且其用途相符之官方授權「收件對象」本身為 `NOT_ESTABLISHED`（P202G-A 證實，見 §9），既不能寄送、也無法在近期解除真正的綁定約束。兩條路線**都不能**移動 live-data 軸（仍 HOLD），但只有 Track A 能立即產出新的預測/評估證據並改善推薦的證據品質。

**重要誠實限制**：本決策**不主張** Track A 能大幅提升 *live 推薦管線* 的準確率。實證顯示（§5、§6）live 推薦路徑目前以 `neutral_fixed_prior`（寫死 0.535 + 中性特徵向量）產生機率，而能餵入 game-specific 特徵的資料屬 live/HOLD。因此 Track A 的「live 準確率天花板」在資料軸解除前確實受限——但這個限制**同樣不利於** Track B（Track B 也無法解除資料軸），故仍以 Track A 為工程主軸。

| 項目 | 結論 |
|---|---|
| Primary track | **TRACK_A_PRIMARY** |
| Deferred track | **Track B = deferred / parallel HUMAN-LEGAL action**（非工程優先；非 rejected） |
| Confidence | **MEDIUM** |
| Top 3 supporting facts | (1) 三個 fixture-only 模組 P202D/E/G-B **完全未接線**、無真實資料流（§5C）；(2) 既有 offline backtest/calibration 基礎設施在 **2,430 場 2025 真實歷史資料**上可運行且 leakage-controlled（§5D）；(3) Track B 之 purpose-matched licensing 收件管道 `NOT_ESTABLISHED`（§9） |
| Top 3 uncertainties | (1) proxy 特徵（wOBA/FIP 代理）對未來真實特徵模型的轉移性有限（§6）；(2) 既有研究模型之 OOS Brier-skill 是否能經校準轉正並穩定（待 §15 任務證偽）；(3) MLB 是否存在「可達且用途相符」之 data licensing 窗口（§9，外部人類動作才能確認） |
| Reversal trigger | 人類（本任務外）確認存在**可達、用途相符之 MLB data/API licensing 管道**（解除 `NOT_ESTABLISHED`）→ Track B 成為解除綁定約束之唯一槓桿，應以**並行人類/法律行動**升級（§14） |
| Immediate next task | `P203-PRED-EVIDENCE`（Offline Leakage-Safe 校準＋特徵消融 walk-forward 證據研究；fixture/historical-only）（§15） |
| Must NOT do next | 任何 live/historical endpoint 呼叫、transport/collector 實作、provider unlock、寄送/提交許可請求、帳號/API key 申請、治理或 source/test/registry/champion 變更、把 paper/fixture 結果描述為 production live readiness |

---

## 2. Scope and Explicit Non-Actions（範圍與明確未執行動作）

本任務為唯讀決策報告。以下動作**全數未執行**：

- ❌ 未呼叫任何 MLB data endpoint（schedule / game / player / boxscore / stats / roster / probablePitcher / 任何 live 或 historical data）。`statsapi.mlb.com/api/...` 一次都未觸及。
- ❌ 未做任何官方政策網頁擷取（本任務不需要；政策結論引自既有 P202F / P202G-A 報告）。
- ❌ 未實作 transport / collector / acquisition / backfill；未產生 fixture；未寫 runtime data / DB / log payload / production / registry。
- ❌ 未修改任何 source / test / config / fixture / 模型 / 推薦 / 評估器 / scheduler。
- ❌ 未修改、stage 或提交四個治理檔（roadmap.md / CTO-Analysis.md / active_task.md / CURRENT_STATE.md）或既有報告。
- ❌ 未做任何 git add / branch / checkout / commit / push / PR / merge / rebase / reset / stash / clean / delete。
- ❌ 未寄送 email / contact form；未登入；未取得 token / API key；未接受任何契約；未申請帳號或授權。
- ❌ 未 unlock provider；未動 EV/CLV/Kelly；未自動變更 strategy weight / champion / `controlled_apply`。

**已執行（授權範圍內）**：唯讀讀取治理/政策/source/test/報告；唯讀 git/PR metadata 檢查；唯讀執行既有測試（§Phase 8）；產出本份唯一報告。

**唯一寫入檔案**：`report/p202g_next_direction_decision_packet_20260614.md`（本檔）。

---

## 3. Governance and Phase 0（治理與 Phase 0）

### 3.1 Governance Read Status

| Required file | Status | Finding |
|---|---|---|
| `agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` | READ | Phase 0、STOP、精確白名單、no-external-effects 規則適用；本任務符合 Template 1/2（plan-only/read-only + 單一報告白名單） |
| `agent_bootstrap/TASK_TEMPLATES.md` | READ | Template 1 Plan-Only：read source/artifacts/git，run read-only tests，write 唯一報告 |
| `agent_bootstrap/CURRENT_STATE.md` | READ | HEAD=`96c67c1`、`paper_only=true`/`production_ready=false`、tolerated dirty 清單、authorized uncommitted governance 清單、live HOLD、blocker 清單 |
| `active_task.md` | READ | Active Task = **P202G-NEXT-DIRECTION**，Track A/B 決策備忘，hard boundaries 與本 prompt 一致 |
| `roadmap.md` | READ | §`0O`（最新）P202G-A packaging complete、direction gate next；live HOLD；fixture-only 為最低邊界 |
| `CTO-Analysis.md` | READ | §`0D`（最新）同上；single live blocker = 官方書面授權（none identified） |
| P202F report | READ | `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`；one-shot 設計就緒但未授權；§13 警告「下一步應為更窄的法律澄清，而非又一個 implementation skeleton」；§16 已含 10 題澄清問題清單 |
| P202G-A evidence packet | READ | `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`；§13 contact-path 分析；§20 「唯一合規路徑＝先確認用途相符 licensing 管道（NOT_ESTABLISHED）」 |
| P202G-A independent review | READ | `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`（歷史）；確認 packet 所有決策正確且保守、HOLD 維持 |

> 註：`active_task.md` 列的 Final Classification 候選集（`..._DECISION_COMPLETE/...`）與本 prompt 不同。依 Governance Priority #1（本 prompt 唯讀決策報告與單檔 whitelist 優先），本報告採用**本 prompt 指定**之 Final Classification 候選集。差異已記錄，非阻斷。

### 3.2 Phase 0 — Actual State Verification 結果

| Check | Observed | Result |
|---|---|---|
| `pwd` / git toplevel | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | PASS |
| `git branch --show-current` | `main` | PASS |
| `git symbolic-ref -q --short HEAD` | `main`（非 detached） | PASS |
| `git rev-parse --git-dir` | `.git` | PASS |
| local HEAD | `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` | PASS |
| `origin/main` | `96c67c1bd3a2f4afe96c52a28109c38fabf1b05e` | PASS |
| local HEAD == origin/main == Expected HEAD | 三者相等 | PASS |
| `git diff --cached --name-only`（staged） | 空（0） | PASS |
| `gh pr list --state open` | 空（0） | PASS |
| `.venv/bin/python --version` | `Python 3.13.8`（≥ 3.11） | PASS |
| active_task = P202G-NEXT-DIRECTION | 是（title 行確認） | PASS |
| P202G-A reports tracked & present | 是（evidence packet 45,242 bytes + independent review 28,090 bytes，皆 `git ls-files` 命中） | PASS |
| 四治理檔含 post-merge closeout | 是（CURRENT_STATE updated 2026-06-14、HEAD=96c67c1、`P202G_A_PR23_MERGE_COMPLETE`） | PASS |
| dirty tree = 既知 inventory | 是（見下） | PASS |
| decision report 尚未存在 | 是（`ls` 確認 No such file，本任務新增） | PASS |
| 無 pitcher-event/probable-starter runtime data 目錄 | 是（`data/mlb_pitcher_game_events.py`、`data/mlb_probable_starter_*.py` 為 `.py` 模組，非資料目錄） | PASS |

**Phase 0 = PASS。** 無 STOP condition 觸發。

### 3.3 Dirty Inventory（Phase 0 實測完整清單）

Tracked-modified（14）：
- 治理（4）：`00-Plan/roadmap/CTO-Analysis.md`、`active_task.md`、`agent_bootstrap/CURRENT_STATE.md`、`roadmap.md`（post-merge governance closeout，authorized uncommitted）
- tolerated runtime/data（10）：`data/.live_cache/tsl_dedup_state.json`、`data/derived/tsl_market_availability_state.json`、`data/mlb_context/external_closing_state.json`、`data/mlb_context/odds_capture_schedule.json`、`data/mlb_context/odds_timeline.jsonl`、`data/tsl_fetch_status.json`、`data/tsl_odds_history.jsonl`、`data/tsl_odds_snapshot.json`、`logs/daemon_heartbeat.jsonl`、`runtime/agent_orchestrator/training_memory.json`

Untracked（7）：
- bootstrap（2）：`agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md`、`TASK_TEMPLATES.md`
- 既有排除報告（5）：`report/p199_..._20260611.md`、`report/p202_..._20260612.md`、`report/p202b_..._20260612.md`、`report/p202c_..._20260612.md`、`report/p202f_..._20260613.md`

所有 dirty 路徑皆屬 CURRENT_STATE「Tolerated Dirty Files」+「Authorized Uncommitted Governance Files」清單，**無未預期路徑**。Phase 8 執行既有測試後重新檢查，dirty tree **逐位元組與 Phase 0 相同**（pytest cache 已 gitignore）。

---

## 4. Primary Product Objective（主要產品目標）

**唯一主要目標**：提高 MLB 賽事**預測成功率**與**投注建議的證據品質**（含可學習 / paper-evaluable 的預測）。

**成本不是主要裁決因素。** 不得因某方向較易、較便宜或較快即宣稱其對預測成功率更有價值。

**Non-objectives（明確排除）**：純粹堆疊更多 infrastructure、最大化任務數、降低成本、在政策限制下開通 live access、把「許可請求草稿」當成「已取得許可」、宣稱已取得法律核准。

**Hard constraints（硬約束）**：no live transport；no automated StatsAPI collection；no historical backfill from restricted endpoint；不得以 ineligible 證據做 promotion；fixture-only / paper 工作**不得**被描述為 production live readiness。

---

## 5. Current Technical Capability Map（現況技術能力盤點）

> 每一能力主張均附實際 source/test 路徑。✅=已具備且測試覆蓋；⚠️=部分/有缺口；❌=缺。

### A. Recommendation Path（推薦產線；P200）— `scripts/run_mlb_tsl_paper_recommendation.py`

| 項目 | 狀態 | 證據 |
|---|---|---|
| 實際 prediction source | ⚠️ **永遠 `neutral_fixed_prior`** | `run_mlb_tsl_paper_recommendation.py:305`（寫死 `MODEL_HOME_PRIOR = 0.535`）；`:326`（中性特徵向量 `[[0.535,0.465,0.07,8.5,1.0,1.0,1.0]]`，與賽事無關）；game-specific 分支存在但**僅供測試覆蓋、production 路徑永不到達**（`:217`） |
| Side selection | ✅ **argmax（非寫死 home）** | `determine_selected_side()` `:170–198`，method 恆為 `"argmax_model_probability"`，`>=` tie→home；P200 取代 P199 寫死 `tsl_side="home"` |
| Edge / EV | ⚠️ **基於 estimated odds（proxy）** | `edge_pct = selected_prob - implied` `:435`；odds 來自 `_estimate_moneyline_odds()` `:144–154`（model prob + 4% vig）；即使 TSL「live available」仍為 proxy（無 team-name join，`:423` 註） |
| source_trace / provenance | ✅ 豐富 | `recommendation_row.py` source_trace 含 `prediction_input_mode`、`prediction_source`、`prediction_source_id`(None)、`prediction_model_version`、`selected_side_method`、`selected_side_reason`、`learning_eligible`(False)、`learning_block_reason`（`:412–420`） |
| 剩餘 provenance 缺口 | ❌ | **無** `input_fingerprint`（特徵向量雜湊）、**無** `odds_source_flag`（observed vs estimated）、**無** odds confidence/freshness、**無** team-name-match status；`source_trace` 為 schemaless dict、無 schema 驗證 |
| Fallback / estimated-odds 標記 | ✅ fail-closed | TSL blocked→`gate_status="BLOCKED_TSL_SOURCE"`、stake=0、kelly=0；edge≤0→`BLOCKED_EDGE_NEGATIVE`；`learning_eligible=False`（neutral 路徑）並附 `learning_block_reason` |
| 測試 | ✅ | `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`（P200 side-selection / provenance / propagation）；本輪實測通過（§Phase 8） |

### B. Learning Eligibility（P201 / P180）— `orchestrator/mlb_paper_evaluator.py`

| 項目 | 狀態 | 證據 |
|---|---|---|
| Evaluator | ✅ `p180_evaluator_v2` | `mlb_paper_evaluator.py:514`；`evaluate_paper_recommendations()` `:274–447`（hit rate/Brier/ROI/binomial p、coverage、gate/confidence/strategy 分段） |
| learning_eligible 強制 | ✅ 保守 fail-closed | `_row_learning_eligibility()` `:86–111`——**僅當 `source_trace.learning_eligible is True`** 才 eligible；缺 trace/格式錯/未宣告→ineligible + block_reason |
| eligible/ineligible 分段 | ✅ | ineligible 仍被計分（可稽核）但分開計數；block_reason histogram（`:437–441`） |
| Leaderboard | ✅ deterministic、不變更權重 | `build_strategy_leaderboard()` `:114–187`，排序 `(-hit_rate,-shadow_roi,strategy_id)`；`learning_status`∈{ELIGIBLE/DATA_LIMITED/INELIGIBLE/UNKNOWN}、`promotable_learning_evidence`（僅 ELIGIBLE 為 True）；missing→`UNATTRIBUTED` bucket |
| **下游 consumer 是否忽略 learning_status** | ⚠️ **潛在缺口（latent）** | **無任何 non-test 程式讀取 `promotable_learning_evidence` 並當 gate 強制**；`scripts/run_mlb_paper_evaluation.py` 輸出 metrics、`orchestrator/mlb_daily_scheduler.py` 僅讀 count 不據以 gate。leaderboard **只標記、未強制**。目前無任何程式消費 leaderboard，故為 latent（尚未造成 promotion 外洩） |
| 測試 | ✅ | `tests/test_mlb_paper_evaluator.py`、`tests/test_p180_strategy_leaderboard.py`；本輪實測通過（§Phase 8） |

### C. Fixture-Only Data Structures（P202D / P202E / P202G-B）

| 模組 | 規模 / 語義 | **是否接線 runtime** |
|---|---|---|
| P202D `data/mlb_probable_starter_snapshots.py` | 654 行；25-field append-only 快照；fail-closed selection；`diagnostic_only=True`/`production_ready=False` 強制；`learning_eligible` 被拒（`:253`）；`collected_at ≤ information_cutoff < scheduled_start` 閘 | **NO**（僅 P202E + tests 匯入） |
| P202E `data/mlb_probable_starter_collector.py` | 399 行；注入式 transport（無預設網路）；純 stdlib；reuse P202D normalize | **NO**（僅 tests 匯入） |
| P202G-B `data/mlb_pitcher_game_events.py` | 970 行；logical identity `(game_pk,pitcher_id)`；`source_lineage_key`；cross-source fail-closed `ambiguous_cross_source_lineage`；strict collected_at PIT 閘；`learning_eligible` 在 forbidden tokens | **NO**（僅 tests 匯入；非 test grep 無命中） |

**關鍵結論**：三模組**完全與 scheduler / orchestrator / recommendation / evaluator / feature-generation 解耦**，且**無真實資料流經**（無 live 採集授權、無真實 fixture 資料）。它們是「採集格式骨架」，定義「如何 ingest」，但目前**無資料可 ingest**。fixtures 僅 `tests/fixtures/*`（合成）。測試：本輪 257 passed（§Phase 8）。

### D. Evaluation Capability（offline，不需 live data）

| 能力 | 狀態 | 證據 |
|---|---|---|
| Walk-forward backtest | ✅ leakage-controlled | `wbc_backend/evaluation/full_backtest.py`（accuracy/Brier/logloss/ECE/ROI/Sharpe/p-value/Brier-skill/95%CI；walk-forward `:297–599`）；`institutional_backtest.py`（ISOLATION BOUNDARY `:61–67`、`assert_no_synthetic` `:150–164`、walk-forward `:207–301`） |
| Calibration | ✅ | `wbc_backend/calibration/probability_calibrator.py`（Temperature/Platt/Isotonic；ECE `:70–82`；`calibrate_walk_forward` `:349–381`） |
| Paper 評估 | ✅ | `mlb_paper_evaluator.py`（hit/Brier/ROI/binomial p、segmentation；§B） |
| Closing-line / CLV | ❌ **非真 CLV** | `wbc_backend/research/mlb_alpha_lab.py:54/69/153`；2025 為單一**賽後快照 proxy**；`strict_timeline_games=0`；`external_closing_state.json` `fetched=false` |
| Feature generation | ⚠️ **proxy 特徵** | `wbc_backend/features/alpha_signals.py`（`build_alpha_signals()` `:1386–1414`，`cutoff_date` 防洩；318 特徵自 `Matchup` 計算、無 live API）；`advanced.py`；但底層 wOBA/FIP 為**rolling 代理**（`data/mlb_data_loader.py:292–314`），非真實球員逐場數據（CLAUDE.md 待辦 Phase 8B） |
| 歷史 replay 資料 | ✅ 真實但有限 | `data/mlb_data_loader.py`（2,430 場 MLB 2025，`data_source="mlb_2025_retrosheet"`；rolling Elo K=20、賽前隔離）；paper 推薦語料**僅 2 列**（`outputs/recommendations/PAPER/2026-05-11/`），遠低於 50 場最小 / 1500 樣本門檻 |

---

## 6. Current Prediction-Quality Blockers（現況預測品質 blocker，分類）

> 分類：`DATA_BLOCKER` / `INTEGRATION_BLOCKER` / `EVALUATION_BLOCKER` / `GOVERNANCE_BLOCKER` / `AUTHORIZATION_BLOCKER` / `NOT_ACTUALLY_BLOCKING`。每項標明能否 offline 修復。綜合自 P199/P202/P202B/P202C 與本輪程式盤點。

| # | Blocker | 分類 | Offline 可修？ | 證據 |
|---|---|---|---|---|
| 1 | Prediction input = neutral fixed-prior（非 game-specific） | DATA_BLOCKER（標記面已由 P200/P201 處理） | ⚠️ 標記已修；**真正修復需 game-specific 資料**（blocker 2） | `run_..._recommendation.py:305/326`；P199 §7 |
| 2 | **無可信 game-specific 預測來源** | DATA_BLOCKER + INTEGRATION_BLOCKER | ❌ **不可 offline**（P202=NONE FOUND） | P202 `NO_TRUSTWORTHY_GAME_SPECIFIC_SOURCE`；§5（pregame fail、season-aggregate FIP leakage） |
| 3 | 無逐場投手事件 log；FIP 僅賽季彙總 / 靜態 proxy | DATA_BLOCKER | ❌ **不可 offline**（需 live boxscore） | P202B §3.2–3.3；P202C class B |
| 4 | 無真實賽前 probable-starter 快照史（2025「probable」為 as-played relabel） | DATA_BLOCKER（**irreversible**） | ❌ **不可 offline**（需 live statsapi 前向擷取，過去史無法重建） | P202B §3.1；P202C §12 class A |
| 5 | 模型 training cutoff / 機率定向未證明（on-the-fly 重訓） | GOVERNANCE_BLOCKER | ✅ **可 offline**（補 training-cutoff 契約 + 定向標記） | P202B §3.6；P202C §7 |
| 6 | Side selection 寫死 home | EVALUATION_BLOCKER | ✅ **已 offline 修復（P200 argmax）** | `determine_selected_side()`；§5A |
| 7 | 無 observed TSL odds（永遠 estimated；無 team-name join） | INTEGRATION_BLOCKER + AUTHORIZATION_BLOCKER | ❌（需 live TSL + 合法授權，獨立軸） | `_estimate_moneyline_odds` `:144`；P199 §6 |
| 8 | 樣本過小 / learning eligibility | EVALUATION_BLOCKER | ⚠️（規則已備；需前向累積 eligible 列） | 2 列 paper；§5D；P201 |
| 9 | Evaluator join 僅用 PK（碰撞風險） | GOVERNANCE_BLOCKER | ✅ **可 offline**（加 date+team 驗證） | P199 §8 |
| 10 | Outcome freshness 未逐場追蹤 | DATA_BLOCKER（評估面） | ✅ 可 offline（非預測準確率核心） | P199 §8 |
| 11 | 下游未強制 `promotable_learning_evidence` | INTEGRATION_BLOCKER（latent） | ✅ 可 offline；但目前無 consumer，屬 premature | §5B |

**Blocker 軸總結**：
- **預測準確率核心（1–4）**：binding 約束為**資料可得性**（game-specific、point-in-time、leakage-safe）。**2/3/4 皆不可 offline 修復、皆指向 live/HOLD 資料**。1 的標記面已由 P200/P201 完成，真正修復被 2 卡住。
- **已 offline 完成（6）**：P200 side-selection。
- **可 offline 但非準確率核心（5/9/10/11）**：治理 / 評估完整性 / latent 強制；改善**證據品質**而非直接準確率。
- **odds 軸（7）**：與預測軸正交，受 provider/legal 阻擋（獨立於 P202G live-transport 軸）。

> **這正是本決策的核心張力**：最能提升準確率的工作（2/3/4）資料軸 HOLD、不可 offline；而可 offline 的工作多屬證據品質或已完成。Track A 必須挑選一個**在現有真實資料上能產出可證偽預測證據**的候選，並對「live 天花板受限」誠實。

---

## 7. Track A Candidate Inventory（Fixture-Only 候選清單）

> 列 5 個具體候選。每個記錄：問題 / 現有證據 / 預測改善機制 / 所需檔案 / live 依賴 / leakage 風險 / 評估指標 / 最小證據門檻 / 可證偽時間 / 可逆性 / 治理風險 / 現有 fixture 是否足夠 / 是否能全程 fixture-only。

### Candidate A1 — Offline Leakage-Safe 校準 + 特徵消融 walk-forward 研究（2,430 場 2025）
- **問題**：現有研究模型之 OOS 預測品質與校準是否能改善？哪些特徵真正帶 OOS 訊號？（CLAUDE.md 記 Brier Skill 曾為負、Platt 後 ECE 0.035）
- **現有證據**：`full_backtest.py` / `institutional_backtest.py`（walk-forward + ISOLATION BOUNDARY）、`probability_calibrator.py`、2,430 場真實 retrosheet 資料皆已具備且 leakage-controlled（§5D）。
- **預測改善機制**：(a) 校準把 OOS Brier-skill 轉正並降 ECE→直接改善機率品質與 Kelly 定價；(b) 特徵消融找最小帶訊號特徵集（Simplicity First）→降過擬合、提升 OOS 穩定。
- **所需檔案**：新研究腳本（如 `scripts/run_p203_calibration_ablation_study.py`）+ 結果報告 + 可選 pruned-feature 設定 artifact。**不**動 champion/registry/strategy weight/recommendation/evaluator。
- **live 依賴**：**無**（全 offline，2025 歷史）。**leakage 風險**：低（rolling 賽前特徵 + walk-forward 隔離；非 P202 所指 season-aggregate FIP）。
- **評估指標**：OOS Brier Skill Score、ECE、hit-rate、各 walk-forward 視窗 95% CI、特徵移除前後 OOS Brier delta。
- **最小證據門檻**：≥1500 樣本（CLAUDE.md SOP）/ ≥50 場（backtest §02）；本資料 2,430 場滿足。
- **可證偽時間**：短（數日；引擎與資料就緒）。**可逆性**：高（純研究 + 報告 + 可選設定）。**治理風險**：極低（paper、diagnostic、無 live）。
- **現有 fixture 足夠？** 是（2,430 場真實歷史）。**能全程 fixture-only？** 是。

### Candidate A2 — Recommendation Provenance 完整化（input_fingerprint + odds_source_flag）
- **問題**：source_trace 缺 `input_fingerprint`、`odds_source_flag`、odds freshness→無法事後證明「用了哪組輸入」「odds 是觀測或估計」。
- **現有證據**：§5A 缺口；`recommendation_row.py` source_trace schemaless。
- **預測改善機制**：**間接**——提升**證據品質與可稽核性**，不直接提升準確率。
- **所需檔案**：`recommendation_row.py` + runner + 測試。
- **live 依賴**：無。**leakage 風險**：無。**評估指標**：provenance 欄位完整度、測試覆蓋（非預測指標）。
- **最小證據門檻**：N/A（非預測證據）。**可證偽時間**：短。**可逆性**：高。**治理風險**：低。
- **現有 fixture 足夠？** 是。**能全程 fixture-only？** 是。**限制**：不產出**可量測預測證據**（§Phase 3 拒絕準則的邊界）。

### Candidate A3 — 下游 `promotable_learning_evidence` 強制 gate
- **問題**：leaderboard 只標記、無 consumer 強制 promotable（§5B latent 缺口）。
- **預測改善機制**：**間接**（評估完整性/治理），不直接提升準確率；且目前無 consumer，屬 premature。
- **所需檔案**：評估/治理消費端 + 測試。**live 依賴**：無。**leakage 風險**：無。
- **評估指標**：gate 行為測試（非預測指標）。**可證偽時間**：短。**可逆性**：高。**治理風險**：低。
- **現有 fixture 足夠？** 是。**能全程 fixture-only？** 是。**限制**：非預測證據；premature（無上游 promotion 流程）。

### Candidate A4 — 把 P202D/E/G-B 接線進 feature generation
- **問題**：fixture-only 模組未接線（§5C）。
- **預測改善機制**：**無**——模組內**無真實資料**（無 live 採集授權）；接線空骨架不產生預測證據。
- **live 依賴**：實際有用需 live 採集（HOLD）。**治理風險**：中（易被誤讀為「已具備 PIT 能力」）。
- **裁定**：**REJECT**——落入 P202F §13 警告的「又一個 implementation skeleton / 空骨架」陷阱；無可量測預測證據；依賴 live 資料。

### Candidate A5 — 歷史 point-in-time 特徵 offline 重建（leakage-safe）
- **問題**：以本地資料重建任一過去 gamePk 之賽前 PIT 投手/球隊特徵。
- **預測改善機制**：理論上高（補 blocker 3/4）。
- **裁定**：**REJECT**——P202B 已判 `BLOCKED_BY_POINT_IN_TIME_STATS` + `BLOCKED_BY_PROBABLE_STARTER_HISTORY`：本地無逐場投手事件 log、FIP 僅賽季彙總（leakage）、賽前 probable 史不可重建（irreversible）。**不可 offline**。

### 候選裁定彙整

| 候選 | 可量測**預測**證據？ | live 依賴 | 裁定 |
|---|---|---|---|
| **A1** 校準+消融研究 | ✅ 是（Brier-skill/ECE/hit-rate） | 無 | **SELECT（best）** |
| A2 provenance 完整化 | ❌ 否（證據品質） | 無 | 保留為 runner-up |
| A3 下游強制 gate | ❌ 否（治理） | 無 | 保留（premature） |
| A4 接線空骨架 | ❌ 否 | 是（HOLD） | REJECT |
| A5 PIT offline 重建 | （理論是） | 是（HOLD/blocked） | REJECT |

---

## 8. Best Track A Candidate（最佳 Track A 候選）

**選定 A1 — Offline Leakage-Safe 校準 + 特徵消融 walk-forward 證據研究（fixture/historical-only）。**

**為何是 A1（依 §Phase 3 準則）**：在所有候選中，**只有 A1 能產出「可量測預測證據 (measurable predictive evidence)」**——OOS Brier Skill Score、ECE、hit-rate（含 walk-forward 95% CI）與特徵消融的 OOS Brier delta。它使用**真實**（非空骨架）2,430 場 2025 歷史資料，leakage 由 `institutional_backtest` 的 ISOLATION BOUNDARY 與 rolling 賽前特徵雙重保證，全程 fixture-only、可逆、治理風險極低。A2/A3 雖乾淨但只改善證據品質（非預測證據）；A4/A5 被 reject（空骨架 / 資料 blocked）。

**雙向可證偽（關鍵優點）**：
- 正結果：找到一組校準 + 精簡特徵集，使 OOS Brier-skill 轉正且跨視窗穩定 → 直接改善機率品質（可惠及未來真實特徵管線）。
- 負結果：無任何設定能讓 OOS Brier-skill 轉正 / 校準不穩 → **記錄當前研究模型在 proxy 特徵下的天花板，並佐證「資料軸（game-specific）才是 binding 約束」**——此本身即高價值的決策證據，且強化 §14 的 reversal 條件。

**誠實限制**：A1 在 proxy 特徵（wOBA/FIP 代理）上運作，對未來真實球員特徵模型的轉移性有限；且 **live 推薦路徑目前用 neutral fixed-prior、不吃此研究模型**，故 A1 改善**不會自動流入 live 推薦**——這正是把信心定為 MEDIUM、預測影響評 3/5 的原因。

---

## 9. Track B Permission-Preparation Feasibility（書面許可請求準備可行性）

評估「**準備但不寄送**」一份供人類/法律審查的 MLB 自動化資料存取書面許可請求草稿。

### 9.1 一份請求需涵蓋（高階大綱，僅供比較；非 send-ready）
精確請求權限 / 目標 endpoint（`statsapi.mlb.com/api/v1/schedule` 等）/ 自動化用途 / 採集頻率 / 保存 / normalized 儲存 / 歷史 backfill / 衍生統計 / 模型特徵與訓練 / 對外輸出 / redistribution / 商業使用 / 刪除與終止處理 / attribution / 安全控制 / rate-limit 接受 / 聯絡管道不確定性 / 是否需法律審查。
（P202F §16 已備 10 題澄清問題清單、P202G-A §13 已備 contact-path 表——草稿素材**大致已存在**。）

### 9.2 可行性裁定

| 判準 | 裁定 | 依據 |
|---|---|---|
| 是否解除「即時工程 blocker」 | **否** | live-data 軸 HOLD 不因「有一份草稿」而改變；草稿不是許可 |
| 是否有可信收件人 | **否（關鍵致命點）** | P202G-A：purpose-matched data/API licensing 管道 `NOT_ESTABLISHED`；`legaldepartment@mlb.com`=DMCA Copyright Agent（fallback）、`registrationsupport@mlb.com`=技術註冊支援、self-registration=帳號入口（皆非 licensing office） |
| 是否能產出可量測**預測**證據 | **否** | 草稿不含任何預測/評估指標 |
| 是否應阻擋 fixture-only 工作 | **否** | 兩軸正交；Track B 不需暫停 Track A |
| 是否應為**工程**主任務 | **否** | 本質為**人類/法律**動作，非工程；且無收件人、不可寄送 |
| 較佳處理方式 | **deferred / parallel HUMAN-LEGAL side-track** | P202G-A §20：唯一合規路徑為**人類先確認用途相符 licensing 管道**，再取得書面許可，再於新回合重審 |

### 9.3 結論
Track B **不適合作為工程 primary track**：它對主要目標（提高預測成功率）**直接貢獻為零**；其收件對象 `NOT_ESTABLISHED`（連「要寄給誰」都未知），故即便完成一份完美草稿，在人類確立管道前**不能改變任何事**；且本任務與政策均禁止寄送。Track B 真正的**第一步是人類去「建立 licensing 管道」**（解除 NOT_ESTABLISHED），而非「先寫信」。

---

## 10. Weighted Decision Matrix（加權決策矩陣）

> 0–5 計分，附證據。Track A 以 best candidate（A1）評分。權重總和 100%。

| # | 判準 | 權重 | Track A (A1) | 理由（證據） | Track B | 理由（證據） |
|---|---|---:|:---:|---|:---:|---|
| 1 | 預測品質直接影響 | 30% | **3** | 產出 OOS Brier-skill/ECE/hit-rate 證據、可找更佳校準/精簡模型；但對 live 推薦轉移受限（neutral fixed-prior + proxy 特徵） | **1** | 零直接預測證據；純未來賦能且收件人 NOT_ESTABLISHED |
| 2 | 達可證偽證據時間 | 20% | **4** | 引擎 + 2,430 場資料就緒，數日可得 falsifiable 指標 | **1** | 不產出任何可證偽**預測**證據（草稿非證據） |
| 3 | 不依賴受限 live data | 15% | **5** | 全 offline 歷史 retrosheet，零 live | **4** | 草稿本身不需 live（但其全部目的在開通 live） |
| 4 | 既有基礎設施就緒度 | 10% | **5** | full_backtest / institutional_backtest / calibrator / data_loader 皆具備且測試過 | **2** | 素材半備（P202F/G-A），但**收件管道缺失** |
| 5 | 治理/法律風險（低=高分） | 10% | **5** | paper/diagnostic/leakage-safe/無 live，風險極低 | **3** | 不寄送則低，但有「被誤當許可」與「寄錯 DMCA 管道」風險 |
| 6 | 可逆性 | 5% | **5** | 純研究+報告+可選設定，全可逆 | **5** | 未寄送之草稿全可逆 |
| 7 | 解鎖未來工作能力 | 10% | **3** | 量化哪些特徵重要、校準天花板，指引未來 game-specific 資料投入點 | **3** | 若收件人存在則為解除 binding 約束之唯一槓桿，但被 NOT_ESTABLISHED 與人類/法律歸屬上限 |

**加權計算**：
- **Track A** = 0.30×3 + 0.20×4 + 0.15×5 + 0.10×5 + 0.10×5 + 0.05×5 + 0.10×3 = 0.9+0.8+0.75+0.5+0.5+0.25+0.3 = **4.00 / 5**
- **Track B** = 0.30×1 + 0.20×1 + 0.15×4 + 0.10×2 + 0.10×3 + 0.05×5 + 0.10×3 = 0.3+0.2+0.6+0.2+0.3+0.25+0.3 = **2.15 / 5**

**結果**：Track A（4.00）> Track B（2.15）。差距主要由 30%「預測品質直接影響」與 20%「達可證偽證據時間」兩項主導——Track A 產出真實可證偽預測證據，Track B 兩項皆為零/極低。評分未為配合 default hypothesis 而操弄；Track B 的價值（真實但間接、遙遠、收件人未知、屬人類/法律）已如實反映於 1/2/4 項低分。

---

## 11. Adversarial Arguments（對抗性論證）

**Optimistic case（Track A）**：A1 找到一組校準 + 精簡特徵集使 OOS Brier-skill 顯著轉正且跨視窗穩定；feature ablation 把 318 特徵縮到帶訊號的精簡集，降過擬合；當 live game-specific 資料未來解鎖時，此校準/精簡基礎可直接套用，加速準確率提升。

**Base case（Track A）**：A1 產出一份 falsifiable 的 OOS 校準/消融證據報告，量化現有研究模型在 proxy 特徵下的能力與天花板、特徵重要度排序；不直接改變 live 推薦，但改善研究模型品質與「下一步資料投入」的決策證據。

**Failure case（Track A）**：proxy 特徵下無任何設定能讓 OOS Brier-skill 轉正 / 校準不穩 → A1 證明研究模型已達 proxy 天花板。**此非浪費**：它把 binding 約束明確釘在「資料軸（game-specific，HOLD）」，強化 reversal 條件、為人類/法律 Track B 提供決策依據。

**最強反對 Track A 的論證**：對 live 預測準確率的 binding 約束是 game-specific point-in-time 資料（HOLD）。Track A 在 proxy 特徵歷史資料上的改善**轉移性有限**，且 live 推薦路徑根本不吃研究模型（用 neutral fixed-prior），故 Track A 有「優化一個無法部署的研究模型」之風險，產出之證據現實價值有限。
→ **反駁**：(a) 它仍是**唯一可得**的可證偽預測證據來源；(b) 同時服務「證據品質」次目標；(c) 對天花板誠實，且 failure case 本身即決策證據；(d) 此反對**同樣不利 Track B**（Track B 亦無法解除資料軸、且收件人未知）——故淨效果仍偏向 Track A。

**最強反對 Track B 的論證**：收件對象 `NOT_ESTABLISHED`、不可寄送、零預測證據、本質為人類/法律而非工程；即便完美草稿，在人類確立管道前**不改變任何事**。把它當工程 primary 等於把工程資源投入一個無近期回報、且非工程歸屬的前置條件。

**會反轉決策的條件**：見 §14。

---

## 12. Primary Decision（主要決策）

| 項目 | 內容 |
|---|---|
| **Selected primary track** | **TRACK_A_PRIMARY**（Fixture-Only Prediction Quality） |
| **Deferred track status** | **Track B = deferred / parallel HUMAN-LEGAL action**（非工程優先、非 rejected；見 §13） |
| **Confidence** | **MEDIUM** |
| **Decisive reason** | 只有 Track A 能在不依賴受限 live 資料下產出可證偽預測證據；Track B 直接預測貢獻為零且收件人 NOT_ESTABLISHED、不可寄送 |
| **Top 3 supporting facts** | (1) P202D/E/G-B 完全未接線且無真實資料（§5C）；(2) offline backtest/calibration 在 2,430 場真實資料可運行且 leakage-safe（§5D）；(3) Track B licensing 收件管道 NOT_ESTABLISHED（§9，P202G-A） |
| **Top 3 uncertainties** | (1) proxy 特徵轉移性有限（§6/§8）；(2) OOS Brier-skill 能否經校準轉正並穩定（待 A1 證偽）；(3) 是否存在可達、用途相符之 MLB licensing 窗口（須人類確認） |
| **Reversal trigger** | 人類確認存在可達、用途相符之 MLB data/API licensing 管道（§14） |
| **Immediate next task** | `P203-PRED-EVIDENCE`（§15） |
| **What must NOT be done next** | live/historical endpoint 呼叫、transport/collector/backfill 實作、provider unlock、寄送/提交許可、帳號/API key 申請、治理/source/test/registry/champion 變更、把 fixture/paper 結果稱為 production live readiness |

**選定 Track A 之衍生授權狀態**：
- selected next task may start = **YES，但須另行 task-specific 授權**（本 packet 僅選方向，不自我授權實作）。
- Track B sending/submission = **NO**。
- live implementation = **NO**（仍 HOLD）。

---

## 13. Deferred Track Treatment（次要路線處置）

**Track B 處置：deferred / parallel HUMAN-LEGAL action（非工程優先級）。**

- **不是 rejected**：取得用途相符之書面許可，是未來解除 live-data binding 約束的**唯一合規路徑**；其潛在槓桿最高。
- **不是工程 primary**：它是人類/法律動作，零預測證據，且收件人 NOT_ESTABLISHED、不可寄送。
- **第一步（人類，本任務外）**：先**建立** purpose-matched 官方 data/API licensing 管道（解除 `NOT_ESTABLISHED`）——循官方法律/商務管道查詢正式 data licensing 窗口；**不**把 `legaldepartment@mlb.com`（DMCA）當 licensing 入口。
- **與 Track A 關係**：並行、不互斥；Track B 的人類/法律推進**不需暫停** Track A 的 fixture-only 研究。
- **明確界線**：本任務**未**寄送、**未**提交、**未**建立帳號、**未**撰寫 send-ready 信件；§9.1 僅為比較用之高階大綱。

---

## 14. Reversal Conditions（反轉條件）

| 條件 | 反轉效果 |
|---|---|
| **人類（本任務外）確認存在可達、用途相符之 MLB data/API licensing 管道**（解除 P202G-A `NOT_ESTABLISHED`） | Track B 升級為**並行/主要人類-法律行動**：它成為解除 binding live-data 約束之唯一槓桿，書面請求有了真實收件人，期望值大幅上升 |
| A1（Track A）證明研究模型已達 proxy 天花板、OOS Brier-skill 無法轉正 | 進一步**確認資料軸為 binding 約束**，提升人類/法律 Track B 的相對優先（但仍不改 live HOLD，亦不自我授權任何 live 動作） |
| 取得任何官方書面授權（用途相符、涵蓋自動化/保存/衍生） | 於**新授權回合**重審；即使有利，也僅使後續 P202G live 任務**有資格**接受另行明確之使用者授權，不等於可直接執行 |
| 出現新的、已授權之 fixture（人類提供合法資料） | 可重評 A4/A5（目前因無資料而 reject） |

**不會反轉的「假訊號」**（依任務規則）：技術上公開 / no-auth / robots 沉默 / rate limit 存在 / 低頻 one-shot——**皆不得**改寫為授權。

---

## 15. Recommended Next Task（建議下一任務）

> 實作仍須**獨立的 task-specific prompt**；本 packet 僅選定方向，不自我授權實作。

| 欄位 | 值 |
|---|---|
| Task ID（proposed） | `P203-PRED-EVIDENCE` |
| Task Name | Offline Leakage-Safe Calibration + Feature-Ablation Walk-Forward Evidence Study（fixture/historical-only） |
| Task Type | `IMPLEMENTATION`（research/diagnostic；產出研究腳本 + 報告，於既有 backtest 引擎上運行，無 live、無 champion/registry 變更） |
| Worker model 建議 | Opus 強 |
| Thinking level 建議 | 強 |
| Same/new conversation | **新回合**（實作為獨立受權動作） |

**可量測 success / failure 準則**：
- SUCCESS（任一即達「產出可證偽證據」）：
  - 於 2,430 場 walk-forward 報告 OOS Brier Skill Score、ECE、hit-rate（含各視窗 95% CI），且**校準方法比較**明確；
  - 產出特徵消融排序（移除哪些特徵不劣化 OOS Brier→pruned 候選集），符合 Simplicity First；
  - 三道 leakage 不變式全通過（賽前隔離、walk-forward、無 synthetic）。
- FALSIFIABLE FAILURE（仍算完成且有價值）：無任何設定使 OOS Brier-skill 轉正 / 校準跨視窗不穩 → 記錄 proxy 特徵天花板並標記資料軸為 binding 約束。
- HARD FAIL（須 STOP）：偵測到任何 look-ahead leakage / synthetic 資料 / 需 live data。

**Fixture-only 邊界**：僅用 `data/mlb_2025/*` 歷史 CSV 與既有 fixtures；**無** live MLB/TSL/endpoint 呼叫；paper/diagnostic-only；**不**變更 champion/registry/strategy weight/recommendation/evaluator/scheduler；**不** unlock provider/EV/CLV/Kelly。

**Expected allowed files（high level；實際白名單由後續 prompt 定）**：
- 新研究腳本（如 `scripts/run_p203_calibration_ablation_study.py`）
- 結果報告（如 `report/p203_calibration_ablation_evidence_<date>.md`）
- 可選：唯讀的 pruned-feature 設定 artifact（不接入 production 路徑）
- 對應測試（如 `tests/test_p203_*.py`）

**實作仍須獨立 prompt**：是。本 packet **不**授權開始 P203 實作。

---

## 16. Required Completion Check（必填完成檢查）

| Item | Result |
|---|---|
| 是否真的完成 | **是** |
| Phase 0 PASS / FAIL | **PASS** |
| Objective reconciliation | 完成（§4：主要目標=提升預測成功率+證據品質；non-objectives/hard constraints 明列） |
| Technical capability inventory completeness | 完成（§5 A–E，皆附 file:line） |
| Recommendation-path status | argmax side-selection ✅（P200）；prediction source = neutral_fixed_prior ⚠️；odds = estimated proxy ⚠️；provenance 豐富但缺 input_fingerprint/odds_source_flag ❌ |
| Learning-eligibility status | ✅ 強制（P201 `_row_learning_eligibility` 僅 True 才 eligible）；leaderboard 標記 promotable；下游強制為 latent 缺口 |
| Fixture-only data readiness | P202D/E/G-B 三模組就緒但**完全未接線、無真實資料**（capture-format skeletons） |
| Evaluation capability status | offline backtest/calibration ✅（2,430 場、leakage-safe）；CLV ❌（proxy、strict_timeline=0）；特徵 ⚠️（proxy wOBA/FIP）；paper 樣本=2 列 |
| Blocker inventory | §6：11 項分類；核心 2/3/4 為 DATA_BLOCKER 不可 offline；6 已 offline 完成；5/9/10/11 可 offline 但非準確率核心；7 為 AUTHORIZATION（odds 軸） |
| Track A candidate count / list | **5**（A1 校準+消融 / A2 provenance / A3 下游強制 / A4 接線骨架[REJECT] / A5 PIT 重建[REJECT]） |
| Best Track A candidate | **A1 — Offline Leakage-Safe 校準+特徵消融 walk-forward 研究** |
| Track B feasibility | 不適合作工程 primary：零預測證據、收件人 NOT_ESTABLISHED、不可寄送、屬人類/法律動作 |
| Weighted Track A score | **4.00 / 5** |
| Weighted Track B score | **2.15 / 5** |
| Strongest argument against Track A | binding 約束為 game-specific 資料（HOLD）；proxy 特徵改善轉移性有限、live 推薦不吃研究模型（§11） |
| Strongest argument against Track B | 收件人 NOT_ESTABLISHED、不可寄送、零預測證據、人類/法律歸屬（§11） |
| Primary track selected | **TRACK_A_PRIMARY** |
| Deferred track treatment | Track B = deferred / parallel HUMAN-LEGAL action（非工程優先、非 rejected） |
| Decision confidence | **MEDIUM** |
| Reversal trigger | 人類確認可達、用途相符之 MLB data/API licensing 管道存在（§14） |
| Recommended next task ID/name/type | `P203-PRED-EVIDENCE` / Offline Calibration+Feature-Ablation Walk-Forward Evidence Study / `IMPLEMENTATION`(research) |
| Recommended success criteria | OOS Brier-skill/ECE/hit-rate(95%CI) + 特徵消融排序 + 三 leakage 閘通過；負結果記錄天花板亦算完成（§15） |
| Live transport HOLD | **維持 HOLD** |
| Tests PASS / FAIL / NOT RUN | **PASS** |
| Test files / counts | 必跑三件 `test_mlb_pitcher_game_events.py` + `test_mlb_probable_starter_collector.py` + `test_mlb_probable_starter_snapshot_intake.py` = **257 passed**；發現之 `test_run_mlb_tsl_paper_recommendation_simulation_gate.py` + `test_mlb_paper_evaluator.py` + `test_p180_strategy_leaderboard.py` = **90 passed**（合計 347 passed） |
| Workflow / full regression status | **NOT RUN**（無實際 contract 要求；本任務未改 source/test） |
| git diff check | **PASS（DIFF_CHECK_CLEAN）** |
| Modified file count / list | **1**（新增 `report/p202g_next_direction_decision_packet_20260614.md`） |
| Governance unchanged | 是（四治理檔未動） |
| Existing reports unchanged | 是（P202F / 兩份 P202G-A / P199 / P202 / P202B / P202C 未動） |
| Source/test/config unchanged | 是 |
| Staged files | **0** |
| Current branch | `main` |
| Local HEAD / origin/main | `96c67c1...` / `96c67c1...`（相等） |
| Open PR count | **0** |
| Network / API / DB / runtime / production status | NONE（0 MLB data endpoint、0 policy-page fetch、0 DB/runtime/production 變更） |
| Single blocker or NONE | **NONE**（決策報告完成；無阻斷本任務之 blocker） |
| Whether selected next task may start | **YES，但須另行 task-specific 授權**（P203 實作須獨立 prompt） |
| Whether Track B may be sent / submitted | **NO** |
| Whether live implementation may start | **NO**（仍 HOLD） |
| Worker model recommendation | Opus 強 |
| Thinking level recommendation | 強 |
| Same / new conversation recommendation | 新回合（P203 實作為獨立受權動作） |
| Final Classification | **`P202G_NEXT_DIRECTION_TRACK_A_SELECTED`** |

---

## Final Classification

**`P202G_NEXT_DIRECTION_TRACK_A_SELECTED`**

選定 **TRACK_A_PRIMARY**（Fixture-Only Prediction Quality），confidence **MEDIUM**。決定性理由：在嚴格區分直接預測影響與間接賦能價值後，只有 Track A 能在不依賴受限 live 資料下產出可證偽的預測/評估證據（最佳候選 A1：2,430 場 2025 真實歷史的 leakage-safe 校準 + 特徵消融 walk-forward 研究，加權 4.00 vs Track B 2.15）；Track B 對提升預測成功率直接貢獻為零，且其 purpose-matched licensing 收件管道 `NOT_ESTABLISHED`、不可寄送、本質為人類/法律動作，故列為 **deferred / parallel HUMAN-LEGAL action**（非工程優先、非 rejected）。Live transport（P202G）**維持 HOLD**；建議下一任務 `P203-PRED-EVIDENCE`（須獨立 task-specific 授權）。本報告為唯一寫入檔案，HEAD=origin/main=`96c67c1bd3a2f4afe96c52a28109c38fabf1b05e`、0 staged、0 open PR、0 endpoint、四治理檔與既有報告未動、`git diff --check` PASS、必跑測試 257 passed（+ 發現 90 passed）。
