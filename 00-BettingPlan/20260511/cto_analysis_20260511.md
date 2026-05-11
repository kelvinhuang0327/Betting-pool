> **CTO 2026-05-11 P12 evidence update:** P12 feature-family ablation and context safety audit are complete. Full report: `00-BettingPlan/20260511/p12_feature_family_ablation_context_safety_report.md`.
>
> **P12 key findings:**
> - Context safety: CLEAN. All 4 active pregame pipeline context files (bullpen/rest/weather/starters in `data/mlb_context/`) are PREGAME_SAFE. 76 POSTGAME_RISK files are output artifacts, not pipeline inputs.
> - Feature family ranking: recent_form is most valuable (BSS drops 0.0022 if removed); starter ERA is second (−0.0015); bullpen and weather have zero marginal contribution; rest days add slight noise (+0.0001 better BSS when removed).
> - Best ablation variant: `no_rest` — OOF BSS = −0.027537 (still negative).
> - All 16 ablation variants: BLOCKED_NEGATIVE_BSS.
> - Root cause confirmed: the logit-correction base estimator (P9 bias removal + feature adjustments) cannot produce positive BSS regardless of feature combination. This is not a feature selection problem.
> - Next P0 is now **P13 Model Architecture Repair**: train a walk-forward ML model (logistic regression / LightGBM) on the feature matrix. Features to retain: `indep_recent_win_rate_delta`, `indep_starter_era_delta`. Features to drop: rest days, weather.
> - Test baseline: 165 passed (48 P12 new + 117 P11 regression).
> - Production: still blocked. TSL 403 still active. Paper stake = 0.0.

已完成 CTO 每日檢討與 roadmap 重排，並直接更新：

- [正式 roadmap](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/docs/orchestration/mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md)
- [20260511 CTO 分析](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/20260511/cto_analysis_20260511md.md)
- [20260511 交接檔 addendum](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/20260511/20260511.md)

核心結論我已改掉：下一階段不要再把 Strategy Replay 文件 / UI mock spec 當主線。P41 mock-only artifact 其實已經存在，所以現在最值得推的是實作。

新版優先級：

- **P0**：Live MLB / TSL source readiness，解決 `today/current` 目前會 fallback replay 的問題
- **P1**：code-level MLB → TSL recommendation row contract
- **P2**：Phase 73 market de-risk replay
- **P3**：strategy simulation spine，walk-forward 驗證策略與倉位
- **P4**：只補 strategy replay 必要 backfill/coverage，不再加文件層
- **P5**：moneyline recommendation MVP
- **P6-P10**：settlement/CLV、擴展玩法、feature repair、daily ops、production gate

我也實際跑了 no-write scheduler。結果是 dry-run 可跑，但 current source 不可達，會 fallback replay；所以目前真正 blocker 是 **live MLB / TSL source**，不是 roadmap 不夠完整。

測試方面，本機 `python3` 沒有 `pytest`，所以 targeted pytest 無法跑，這點已記入 CTO 分析作為實作前環境 blocker。

# CEO 每日行動 — 二次審查（2026-05-11）

我把昨天的 P27D–P40（governance chain）、CTO 今天的 pivot（live source readiness 為 P0），跟你補充的兩大主軸（**MLB 賽事預測 → 運彩投注建議** / **策略模擬優化**）擺在一起對照後，結論直接講：

---

## 1. 昨天成果是否真的推進系統成熟度？

**工程上有沉澱，但與你兩大主軸的距離沒有縮短。**

| 維度 | 結果 |
|------|------|
| Metadata source contract / runtime injection / acceptance gate / dashboard | ✅ 完整 |
| Mock-only UI spec + 19 個測試 | ✅ 完成 |
| 14 個 phase 全部 PASS / artifact 齊全 | ✅ 紀律好 |
| 但是…production UI / runtime / migration | ❌ 全部 blocked |
| **MLB → 運彩投注建議**端到端可運行 | ❌ 零推進 |
| **策略模擬優化** spine | ❌ 零推進 |
| Live MLB / TSL source today/current 可用性 | ❌ 仍 fallback replay |

簡單講：昨天**用 14 個 phase 證明「production 還不能啟動」**，但你今天指定的兩大主軸（預測、模擬）一個 commit 都沒前進。這是典型的 **over-engineered governance**——治理鏈完備，產品價值未交付。

---

## 2. CTO 判斷是否合理？盲點在哪？

CTO 今天 pivot 的方向**對**：從 governance / mock spec 轉向 live source + code-level implementation。但仍有三個盲點：

### 盲點 A：CTO 沒把「策略模擬優化」當主軸提出
CTO 把 strategy simulation spine 放 P3，但你今天明確說「**策略優化可以進行模擬優化**」就是兩大主軸之一。它不該排在 P3，更不該被 Phase 73 market de-risk replay（P2）擋在前面。

### 盲點 B：Phase 73 market de-risk replay 放 P2 是錨點殘留
這仍是 **replay 系統的延伸**，是昨天 governance chain 的慣性產物。對你的主軸 MLB→運彩 / 策略模擬都不是必要前提，可以延後或併入 P3 模擬骨架。

### 盲點 C：「moneyline recommendation MVP」放 P5 太後面
你說「能根據運彩投注項目進行預測建議投注」就是主軸 A。**端到端能跑出一筆 MLB→TSL 建議**這件事，不該在 P5。它和 live source readiness 是同一條主線，必須緊鄰排在 P0/P1 後面。

### 盲點 D（小但要點出）：環境問題被當記事，沒當 blocker
CTO 提到「本機 `python3` 沒有 `pytest`」。這是讓今天就要開始實作的人**寫了測試也跑不了**，等於前期工作會白做。這要當 P0 sub-task 處理，不是備註。

---

## 3. 今天應聚焦的系統優化方向（P0–P10 重排）

對齊你的兩大主軸：
- **主軸 A**：MLB 預測 → 運彩投注建議（端到端能跑出來）
- **主軸 B**：策略模擬優化（walk-forward 能驗證策略）

| 優先級 | 任務 | 對應主軸 |
|-------|------|---------|
| **P0** | **Live MLB / TSL source readiness + 本機環境修復（pytest 可用）** — 解決 today/current fallback replay；確認 MLB Stats API、TSL crawler v2 在今日可拉到當日資料 | A、B 共同前置 |
| **P1** | **MLB → TSL recommendation row contract（code-level）** — 一個明確的 schema：game → prediction → kelly → TSL market / line / stake → 寫到哪個輸出 | A |
| **P2** | **今日 MLB → TSL recommendation 端到端 smoke run（MVP）** — 跑一筆真實 game，產出一筆 paper recommendation，落地到報表 | A |
| **P3** | **Strategy simulation spine（walk-forward 骨架）** — `institutional_backtest.py` + `full_backtest.py` 收斂成單一可呼叫 API：輸入策略 + 區間 → Brier / ROI / Sharpe / ECE | B |
| **P4** | **模擬 → 推薦回饋鏈** — simulation 結果直接驅動 P2 的 recommendation gate（Brier > 0.285 拒絕、ECE > 0.12 拒絕） | A × B 連接 |
| **P5** | **MLB 玩法橫向擴展**（run line / total / F5 / team total）的 contract 對齊 | A |
| **P6** | **校準持續改善**（Platt / Isotonic auto-select、Brier Skill Score 修正） | A、B 共同 |
| **P7** | **賽後閉環自動化整合**（postgame_sync 結果回流 simulation spine） | A × B 連接 |
| **P8** | **replay-default-validation false-blocking / quarantine policy** — 收斂昨天的 14 個 governance phase，避免治理鏈持續吃工 | 收尾 |
| **P9** | **Daily ops monitoring**（TSL feed health、recommendation throughput、ECE drift） | 維運 |
| **P10** | **Production proposal gate**（人類審批 + rollout 切換），用真實 simulation evidence 取代昨天的 simulation-only approval | 上線 |

**關鍵調整理由**：CTO 的 P0 留下（live source 確實是 blocker），但我把 P1/P2 改成「實際跑得出 recommendation」而不是「再寫一份 contract 文件」。**今天的衡量標準應該是「跑出一筆 paper MLB→TSL 建議」與「能用 simulation spine 驗一個策略」，而不是再產一份報告**。

---

## 4. 今日可直接執行的任務 prompt

```text
# ROLE
You are Betting-pool's P0+P1+P2 MLB→TSL Live Source Readiness and Recommendation
Smoke-Run Agent, reporting to the CEO agent.

# MISSION
Today's mission has THREE chained outcomes, in order:

1. P0 - Make the live MLB and TSL data path actually work for "today/current"
   (no fallback to replay).
2. P1 - Land a code-level MLB → TSL recommendation row contract
   (game → model prob → kelly → TSL market/line/stake → output path).
3. P2 - Produce ONE end-to-end paper recommendation for a real MLB game today,
   written to a clearly labelled PAPER-ONLY output artifact.

This is implementation, not documentation. Yesterday's governance chain
(P27D–P40) is already complete. Do NOT add more mock specs, gate reports,
acceptance contexts, or production-enablement preview lifecycles.

# PRODUCT NORTH STAR (do not drift)
Betting-pool has exactly TWO product axes:
  A) MLB game prediction → Taiwan Sports Lottery (TSL / 運彩) betting recommendation
  B) Strategy simulation optimization (walk-forward backtest spine)

Today's task is axis A end-to-end smoke. Axis B (strategy simulation spine)
is the NEXT task and must not be started in this round.

# PROJECT / REPO GUARD
This task is for Betting-pool only.
- repo path must be: /Users/kelvin/Kelvin-WorkSpace/Betting-pool
- repository must be Betting-pool
- do NOT use LotteryNew / number-pattern-research / Stock / Novel
- do NOT touch PR #9 / H6 / dedicated DB lane work
- replay-default-validation required check on main: do NOT modify
- branch protection: do NOT modify
If repo/path does not match Betting-pool, STOP and report context drift.

# ENVIRONMENT PREP (blocker - do this first)
Yesterday's CTO note: `python3` lacks `pytest`. Fix BEFORE any task work:
1. Locate the project venv (likely `.venv/`). If missing, create one.
2. Ensure: pytest, pandas, requests, numpy installed.
3. Print `python -V` and `pytest --version` for evidence.
If venv cannot be created, STOP and report.

# HARD SCOPE
DO:
- Read existing live pipeline files (do not rewrite from scratch).
- Diagnose the "today/current fallback to replay" root cause.
- Implement the minimal patch to make today's path return real data
  OR honestly report PAPER_ONLY=BLOCKED with explicit reason.
- Define a small, typed recommendation row contract.
- Run ONE real game through the pipeline as paper-only.
- Write outputs to clearly PAPER-labelled paths.

DO NOT:
- write to production DB
- commit DB binaries
- send real bets
- enable production runtime (P38 boundary still NO_GO)
- migrate historical registry
- modify replay-default-validation script / workflow
- modify branch protection
- write more mock UI specs
- write more governance gate documents
- fake real human approval
- claim MLB has left PAPER_ONLY status

# TASKS

## Task 1 — Repo + environment confirmation
- `pwd`, `git branch --show-current`, `git status --short --branch`
- venv prep (see ENVIRONMENT PREP)
- print pytest version
- do NOT clean dirty working tree

## Task 2 — Live source readiness diagnostic
Inspect these files and trace the "today/current → fallback replay" path:
- data/mlb_live_pipeline.py
- data/tsl_crawler_v2.py
- wbc_backend/api/app.py
- wbc_backend/run.py
- scripts/replay_build_registry.py (only to understand fallback trigger)
- wbc_backend/league_adapters/mlb_adapter.py

Produce a short diagnostic note (inline in final report) covering:
- where the fallback decision is made
- what condition causes it
- whether MLB Stats API reachable today (a single HEAD/GET probe is OK)
- whether TSL crawler v2 returns non-empty data today
- which env vars / config flags / cache TTLs are involved

## Task 3 — Minimal live-source patch (if needed)
If the fallback is caused by a small, safe fix (e.g. wrong date window,
stale cache key, missing env flag), apply it. Otherwise, DO NOT force a fix.

Constraints:
- patch must be < 50 LoC net
- patch must not change replay-default-validation behavior
- patch must not write to production DB
- if a real fix is not safe in <50 LoC, STOP patching and document the blocker

## Task 4 — Recommendation row contract (code-level)
Create or update:
- wbc_backend/recommendation/recommendation_row.py

Define a dataclass `MlbTslRecommendationRow` with at minimum:
- game_id: str
- game_start_utc: datetime
- model_prob_home: float
- model_prob_away: float
- model_ensemble_version: str
- tsl_market: Literal["moneyline", "run_line", "total", "f5", ...]
- tsl_line: Optional[float]
- tsl_side: Literal["home", "away", "over", "under"]
- tsl_decimal_odds: float
- edge_pct: float
- kelly_fraction: float
- stake_units_paper: float    # paper-only stake
- gate_status: Literal["PASS", "BLOCKED_BRIER", "BLOCKED_ECE", "BLOCKED_PAPER_ONLY", ...]
- gate_reasons: list[str]
- paper_only: bool = True
- generated_at_utc: datetime
- source_trace: dict          # which data sources fed this row

Add a `to_dict()` and `to_jsonl_line()` method.

## Task 5 — Add a thin orchestrator entrypoint
Create or update:
- scripts/run_mlb_tsl_paper_recommendation.py

Behavior:
- pick today's first available MLB game (or the closest available game)
- call existing prediction orchestrator
- compute one recommendation row
- write to: outputs/recommendations/PAPER/YYYY-MM-DD/<game_id>.jsonl
- print a one-line summary to stdout

The script MUST refuse to run if:
- live source still falls back to replay AND the user did not pass `--allow-replay-paper`
- output dir cannot be created
- MLB PAPER_ONLY hard gate is removed (it must remain enabled)

## Task 6 — Tests (read-only + 1 smoke)
Add:
- tests/test_recommendation_row_contract.py
  - dataclass field presence
  - to_dict round-trip
  - paper_only default True
  - gate_status enum validity
- tests/test_run_mlb_tsl_paper_recommendation_smoke.py
  - monkeypatch live source to a fixture
  - assert one row produced
  - assert output file written under PAPER/ path
  - assert paper_only is True

Run:
- `.venv/bin/pytest tests/test_recommendation_row_contract.py tests/test_run_mlb_tsl_paper_recommendation_smoke.py -q`

If pytest is unavailable, STOP and report env blocker.

## Task 7 — Actually run the smoke (real or fixture)
- Run `scripts/run_mlb_tsl_paper_recommendation.py` once.
- If live source works → produce a real paper row.
- If live source still falls back → run with `--allow-replay-paper` and label
  the output file with suffix `.replay_fallback.jsonl`.
- Capture stdout into the final report.

## Task 8 — Final report
Create:
- 00-BettingPlan/20260511/p0_p1_p2_mlb_tsl_paper_smoke_report.md

Must include:
1. Repo + branch + env evidence
2. Live source diagnostic (root cause of today/current fallback)
3. Patch summary (or "no patch applied, blocker is X")
4. Recommendation row contract summary (paste field list)
5. Smoke run result (real live vs replay-fallback, with file path)
6. Test results (counts + names)
7. Explicit status flags:
   - live MLB source ready today: true/false
   - live TSL source ready today: true/false
   - recommendation row contract landed: true/false
   - paper smoke produced: true/false
   - production enablement attempted: must be false
   - replay-default-validation modified: must be false
   - branch protection modified: must be false
   - LotteryNew touched: must be false
8. Blockers for tomorrow's P3 (strategy simulation spine)
9. One-line CEO-readable summary

# ACCEPTANCE CRITERIA
- env: pytest runs, version printed
- diagnostic: explains today/current fallback cause
- contract: MlbTslRecommendationRow exists and tests pass
- smoke: at least one row written under outputs/recommendations/PAPER/
- no production DB writes
- no DB binaries committed
- no real bets placed
- MLB PAPER_ONLY hard gate untouched (still enforced)
- replay-default-validation untouched
- branch protection untouched
- no new governance/mock-spec documents created
- final report exists and contains all required sections

# FINAL MARKER
P0_P1_P2_MLB_TSL_LIVE_SOURCE_AND_PAPER_SMOKE_READY
```

---

## CEO 一句話總結

CTO 已經修正方向（從 governance pivot 到 live source），方向**對**，但**錨點仍偏**：今天衡量標準不能再是「又產一份報告/合約文件」，必須是「**真的跑出一筆 MLB→運彩 paper 建議**」+「**本機環境能跑測試**」。當這兩件事今天落地，明天才有資格進策略模擬骨架（主軸 B）。在那之前，governance 鏈先放著，不要再加 phase。
