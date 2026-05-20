已完成 CTO roadmap reset，並新增文件：

[mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/docs/orchestration/mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md)

我確認了：

- repo/path 是 Betting-pool：`/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- 已 fetch `origin/main`
- `main` branch protection 仍要求 `replay-default-validation`
- strict mode enabled
- admin enforcement enabled
- 沒有把 LotteryNew / number-pattern-research / PR #9 / H6 帶進 Betting roadmap

**CTO 結論**
目前最值得優化的方向不是再加 replay / CI infra，而是把 Betting-pool 拉回兩條主線：

1. MLB 賽事預測 → 台灣運彩玩法投注建議
2. 策略模擬 / 回放 / 倉位優化 → 驗證哪些投注策略值得信任

**新版 P0-P10 排序**
- P0：repo / scope hygiene，先處理目前 `main ahead 38, behind 1` 與大量 dirty state
- P1：建立 MLB → TSL recommendation contract
- P2：執行 Phase 73 market de-risk replay
- P3：盤點 MLB 歷史資料與 TSL odds timeline readiness
- P4：先做 moneyline recommendation MVP
- P5：把 strategy simulation / bankroll policy 變成主驗證骨架
- P6：再擴充 run line、total、F5、odd/even、team total
- P7：針對模型弱點做 feature repair
- P8：replay required check false-blocking / quarantine policy
- P9：每日 MLB ops / recommendation / TSL feed monitoring
- P10：production proposal gate

**關鍵調整**
舊 README / roadmap 仍把 MLB 定位成 paper-only，這和你現在的產品目標有落差。新版 roadmap 改成：MLB 不是永遠 paper-only，而是「投注建議必須經過資料、模型、replay simulation、CLV、風控 gate 後才可升級」。

**目前最大阻塞**
第一個不是模型，而是工作區狀態：本機 `main` 已經 `ahead 38, behind 1`，且有大量既有修改。正式進 P1/P2 前，應先做 P0 清理與分支隔離，避免把 DB/runtime noise 或其他歷史 artifact 混進真正的 Betting roadmap 實作。

本輪只新增 roadmap 文件，沒有改程式、CI、branch protection、DB，也沒有新增測試。

Marker: `CTO_MLB_BETTING_ROADMAP_RESET_20260510_READY`


# CEO 每日行動 — 二次審查（2026-05-10）

我先把昨天工作、CTO 分析、和你剛剛補充的「策略歷史回放功能」三者擺在一起對照，把我認為的盲點與誤判點直接講白。

---

## 1. 昨天成果是否真的推進系統成熟度？

**部分是、部分不是。**

| 項目 | 真實價值 | CEO 評估 |
|------|---------|---------|
| `replay-default-validation` CLI / workflow 完成 | 有 | ✅ 是基礎設施沉澱 |
| Required check enactment + 短期 stability | 有 | ⚠️ 有，但邊際效益遞減 |
| mismatch/aligned/multi-state fixture 驗證 | 有 | ✅ 算工程護欄 |
| **跟「使用者看得到的回放頁面」距離** | **零** | ❌ 商業價值未落地 |

換句話說：昨天交付的是**「替未來的 replay 功能加上 CI 防護網」**，而不是「replay 功能本身」。對你今天補充的「策略歷史回放功能上線」這個目標，幾乎沒有直接推進。

---

## 2. CTO 判斷是否合理？盲點在哪？

CTO 寫的 roadmap reset（`cto_analysis_20260510.md`）整體方向不算錯（要從 CI 治理回到 MLB 預測 + 策略模擬主線），但**有三個明確盲點**：

### 盲點 A：把「replay」當成後端驗證工具，沒看到它是「產品頁面」
- CTO 的 P0–P10 完全沒有 **UI / 歷史回放頁面** 這條任務。
- 但你補充的需求很清楚：你要的是**畫面**——「顯示同歷史預測清單即可」、「對所有策略（上線/下線/拒絕/觀察）的每一期預測 vs 開獎結果做比對清單」。
- 這是 product feature，不是 backend gate。CTO 把它跟 replay-default-validation 混為一談了。

### 盲點 B：CTO 把 P0 設為「repo / scope hygiene（main ahead 38, behind 1）」
- 這是工程衛生，不是用戶價值。
- 在你已經明確指定產品目標（回放頁面上線）的情況下，把 P0 留給 git housekeeping 是錯位優先級。
- Hygiene 該做，但不該佔 P0。

### 盲點 C：策略生命週期沒有被當作回放頁面的一級維度
- 你明確點出：「**包含上線、下線、拒絕、觀察等等所有系統上有開發過的策略**」。
- CTO 的 P5–P7 都圍繞 strategy simulation / model calibration，但沒有交付：「**任何狀態的策略，都能查到它每一期預測 vs 實際結果**」這個能力。
- 這代表資料層必須先支援「跨 lifecycle state 的 prediction history 查詢」，否則畫面做不出來。

---

## 3. 今天最該聚焦的系統優化方向（P0–P10 重排）

我把優先級重新對齊到你補充的目標。Betting-pool 主線今天起明確分兩條：**(a) 策略歷史回放頁面落地**、**(b) 預測核心研究**。前者比後者優先，因為前者是你剛指定的產品目標。

| 優先級 | 任務 | 為什麼放這 |
|-------|------|----------|
| **P0** | **盤點現有「歷史預測清單」頁面與後端資料來源**（schema、API、欄位、是否已涵蓋多策略狀態） | 不知道現況就規劃不出回放頁，也避免重造輪子 |
| **P1** | **設計「策略歷史回放頁」資料契約**：predictions × actuals × strategy_lifecycle_state 的 join 規格 | 這是頁面能不能呈現的根本前提 |
| **P2** | **確認資料完整性**：上線/下線/拒絕/觀察四種狀態的策略，歷史 prediction 是否都有保存 | 若任一狀態的歷史被丟棄，需先補回追蹤紀錄 |
| **P3** | **回放頁 MVP 規格**：欄位、篩選、分頁、與既有歷史預測清單一致的 UI/格式 | 你明說「顯示畫面同歷史預測清單即可」，這是錨點 |
| **P4** | **repo / scope hygiene**：處理 main ahead 38 / behind 1，避免在後續開發中把 dirty state 帶進 PR | CTO 原本的 P0，降為 P4：必要但不擋路 |
| **P5** | replay-default-validation 的 false-blocking / quarantine policy（避免 required check 卡到回放頁開發 PR） | 防止昨天的 CI 治理變成今日開發絆腳石 |
| **P6** | 策略 lifecycle state 寫入規範化（單一 source of truth，不要散在多檔） | 回放頁正確性的前提 |
| **P7** | MLB → TSL recommendation contract（CTO 原 P1） | 預測核心研究主線，仍重要但不擋產品上線 |
| **P8** | strategy simulation / bankroll policy 主驗證骨架（CTO 原 P5） | 等回放頁有了再講策略可信度 |
| **P9** | 預測模型弱點（calibration / Brier / ECE）feature repair | 模型側持續優化，非阻塞回放頁 |
| **P10** | production proposal gate / 上線審批機制 | 等前面都齊了再制度化 |

**關鍵調整理由**：CTO 把 P1 給了「MLB → TSL contract」，但你今天要的是「**先讓使用者看到歷史回放畫面**」。產品 SoP 必須讓 P0–P3 全部圍繞這個目標，等頁面 MVP 出來，再把 CTO 原本 P1–P10 接回去。

---

## 4. 今日可直接執行的任務 prompt

```text
# ROLE
You are Betting-pool's P0 Strategy Historical Replay Page Discovery & Contract Agent,
reporting to the CEO agent.

# MISSION
Stage 1 (discovery only, no code changes): figure out exactly what's needed
to deliver the user-facing "strategy historical replay page" for Betting-pool.

The page goal (verbatim from CEO/user):
- Show ALL strategies regardless of lifecycle state:
  online / offline / rejected / observation / any other state ever introduced.
- For each strategy, list every period's prediction vs actual outcome.
- Display format must match the existing "歷史預測清單" (historical prediction list).
- This is a product feature page, NOT backend CI infrastructure.

# PROJECT / REPO GUARD
This task is for Betting-pool only.
- repo path must be: /Users/kelvin/Kelvin-WorkSpace/Betting-pool
- repository must be Betting-pool
- do not use LotteryNew
- do not use number-pattern-research
- do not touch PR #9 / H6 / dedicated DB lane work from LotteryNew
If repo/path does not match Betting-pool, STOP and report context drift.

# CONTEXT
- replay-default-validation CI infra is already enacted as required check on main
  (strict + admin enforcement). DO NOT modify.
- Yesterday's "replay" work was BACKEND VALIDATION, not the user-facing page.
- The user wants the actual product page now.
- Local main is ahead 38 / behind 1 with dirty state — do NOT clean up in this round,
  just note it for P4.

# HARD SCOPE (this round = discovery + contract design ONLY)
Do NOT:
- write production code for the page
- modify replay-default-validation script or workflow
- change branch protection
- add or remove required checks
- modify DB schema
- commit DB binaries
- run replay generation or strategy mining
- touch LotteryNew / number-pattern-research files
- claim long-term stability or feature completeness

# TASKS
1. Confirm repo/path is Betting-pool. Print git status snapshot.
2. Inventory the EXISTING "歷史預測清單" surface:
   - frontend file(s) / route(s) / component(s)
   - backend API endpoint(s) feeding it
   - data model / schema for stored predictions
   - what fields are currently displayed
3. Inventory STRATEGY LIFECYCLE STATE storage:
   - where "online / offline / rejected / observation" status is recorded
   - is it a single field, multiple tables, or scattered configs?
   - is historical state transition preserved (audit log) or only current state?
4. Inventory PREDICTION HISTORY storage:
   - per strategy, per period: are predictions persisted regardless of lifecycle state?
   - identify any state where predictions were NOT being saved (gap risk).
5. Inventory ACTUAL OUTCOME storage:
   - how is real game/draw result joined to predictions today?
   - any mismatch / lookup-key risk (cross-ref tests/test_phase29_clv_lookup_key_mismatch_fix.py)?
6. Identify GAPS between current data and what the replay page needs:
   - missing fields
   - missing strategy states in history
   - missing join keys
   - missing API endpoints
7. Draft a DATA CONTRACT proposal (markdown, no code):
   - request shape (filters: strategy_id, lifecycle_state, date range, market type)
   - response row shape (period, strategy, lifecycle_state_at_time, prediction, actual, hit/miss, notes)
   - explicit decision: should the page show lifecycle_state at the time of prediction,
     or current lifecycle_state? Recommend one with reasoning.
8. Produce a discovery report at:
   00-BettingPlan/20260510/strategy_replay_page_discovery_and_contract.md

# REPORT MUST INCLUDE
- Section A: existing 歷史預測清單 surface map (with file paths and line refs).
- Section B: lifecycle state storage map.
- Section C: prediction history storage map + gap analysis.
- Section D: actual outcome / join key map.
- Section E: gap list ranked by severity (blocker / important / nice-to-have).
- Section F: proposed data contract (request + response).
- Section G: open questions for CEO before MVP build starts.
- Section H: explicit "what NOT to build yet" list (avoid over-scoping the MVP).
- Section I: confirmation that LotteryNew / number-pattern-research were excluded.

# ACCEPTANCE CRITERIA
- Discovery report file is created at the path above.
- No production code changed.
- No CI changed.
- No branch protection changed.
- No DB writes / no DB binaries committed.
- No new tests added.
- Report distinguishes "current state" from "proposed contract".
- Recommendations are conservative and evidence-based.
- Betting-only scope preserved.
- Report explicitly answers: can we build the replay page MVP using current data,
  or must we backfill / re-instrument first? If backfill is needed, list the
  minimum backfill set in priority order.

# FINAL MARKER
P0_STRATEGY_REPLAY_PAGE_DISCOVERY_READY
```

---

## CEO 一句話總結

CTO 寫得有理，但**遺漏了你今天指定的最重要事**：策略歷史回放是**頁面**，不是 CI。今天 P0 不是 git hygiene，也不是 MLB contract，而是**先把現有「歷史預測清單」與策略狀態資料盤清楚**，否則回放頁規格寫了也是空中樓閣。先做 discovery + contract，再進 MVP。