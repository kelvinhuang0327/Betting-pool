我來作為 CTO agent 進行分析。先檢查目前系統實際狀態與最近進度。

我看到真正的開發在 `Betting-pool-p13` 上的 `p13-clean` 分支，且 P30 的 staged files 正待 commit。讓我檢查最新的 CTO realignment 與關鍵 phase 報告以理解全貌。

讓我繼續檢查 P29 阻塞狀態與最新 roadmap 文件，並查看 MLB 預測與策略模擬的目前狀態。

讓我快速看一下 P16-P28 進度與更晚期 phase 的關鍵阻塞，並掌握目前 staged commit 的內容。

我已完整檢視 Betting-pool-p13 上 P13→P30 全部 18 個 phase 的實際狀態。現在進行 CTO 分析。

---

# CTO 分析報告 — 2026-05-13

## 1. 現實狀態核對（vs roadmap）

| 軸線 | Roadmap 假設 | 實際狀態 | 落差 |
|---|---|---|---|
| MLB 預測管道 | P16/P20 完成即可日常輸出 | ✅ P16.6→P19→P17→P20 已成鏈 | 對齊 |
| 樣本密度 | 至 P28 達 1,500 active entries 完成穩定性認證 | ⛔ 324 active / 1,577 total，最寬政策 563 | **嚴重落差** |
| 來源擴充 | P29→P30 透過政策放寬解封 | ⛔ P29 BLOCKED；P30「READY」但實際 348 個 ready sources 是 derived outputs，非新原始資料 | **roadmap 偏移** |
| 策略最佳化 | P18 完成後即可 | 🟡 P18 修復風險，但缺乏 walk-forward + drawdown/exposure 真正掃描 | 半對齊 |
| 賽事結算 | P17 ledger | ⛔ `P17_BLOCKED_SETTLEMENT_JOIN_INCOMPLETE`（後續被 P19 局部修復但未閉環） | 落差 |
| 模型品質 | P13 OOF BSS +0.008253 已足夠 | 🟡 邊際正值但 edge 分布過薄：57.5% 樣本 edge < 5% | 半對齊 |

## 2. Roadmap 根本性偏移（必須調整）

連續四個 phase（P28→P29→P30）都在「審計樣本密度不足」這件事繞圈：
- **P28**：324 < 1500，BLOCKED
- **P29**：政策格 64 組合都跑了，最佳 563 < 1500，BLOCKED
- **P30**：給出「source acquisition plan READY」但實際**沒有取得任何新的 raw data**（348 個 ready 都是 `outputs/` 下的派生檔）

**真正瓶頸不是政策、不是審計，是兩件事：**
1. **資料來源沒擴**：`data/mlb_2024/` 不存在；只有 2025-05-08→2025-09-28 一段
2. **模型 edge 太薄**：P13 OOF BSS 僅 +0.008，導致 57.5% 樣本 edge < 5% 直接被閘擋

繼續 P31「建構 joined input artifacts」是**架構 plumbing**，不會新增任何 active entry。必須**直接面對資料取得與模型品質**。

## 3. 重新排序 P0–P10（兩大主軸交織）

| 優先序 | Phase | 主軸 | 目標 | 為何擺這裡 |
|---|---|---|---|---|
| **P0** | **P30 Commit Recovery** | 工程衛生 | 切回 `Betting-pool-p13` 完成 13 檔 commit | T13 未完成，後續 commit 都會污染 |
| **P1** | **P31 Honest Data Reality Audit + 2024 Acquisition Gate** | 預測 | 區分 raw vs derived，明確 2024 取得路徑（Retrosheet/MLB Stats API/odds CSV） | P30 的 348 ready 是假樂觀；必須 honest gate |
| **P2** | **P32 2024 Historical Game Logs + Closing Odds Ingestion** | 預測 | 真正取得 2024 全季 game logs + 收盤 ML odds，至少 +2,400 candidates | 唯一能突破 1,500 sample wall 的實質動作 |
| **P3** | **P33 Model Quality Improvement (原 P22)** | 預測 | 用 P13+P32 合併資料重訓 walk-forward；目標 OOF BSS +0.020 / ECE < 0.05 | edge 分布過薄是 P28/P29 BLOCK 的真因 |
| **P4** | **P34 Strategy Optimization Hardening (深化 P18)** | 策略 | 真正 walk-forward 掃描 edge_threshold × kelly_cap × abstention，回報 drawdown/exposure/turnover | 策略主軸首次具備可比較證據 |
| **P5** | **P35 P28 Re-audit Pass** | 策略 | 用 P33+P34 結果重跑 P28；目標 active entries ≥ 1,500，drawdown ≤ 25% | 把 sample wall 拆掉 |
| **P6** | **P36 P17 Ledger Settlement Closure** | 策略 | 真正關閉 P17 settlement join；輸出 PAPER P/L、hit rate、CLV proxy | P17 BLOCKED 未閉環是策略主軸技術債 |
| **P7** | **P37 TSL Market Expansion (Run Line + Totals)** | 預測 | moneyline 穩定後新增跑線/大小分；用 Phase 5C MC + blowout_propensity | 用戶明示「運彩投注項目」需擴出 ML 之外 |
| **P8** | **P38 Live TSL Snapshot Bridge** | 預測 | 啟用 2026 球季 TSL 真實 odds snapshot 收集（不寫 prod DB、不下單） | 為後續 CLV 與真實推薦做基礎，仍 PAPER_ONLY |
| **P9** | **P39 Daily Ops & Drift Monitoring** | 共用 | 來源新鮮度、recommendation count、blocked reasons、Brier/ECE drift | 多日多市場後監控才有意義 |
| **P10** | **P40 Production Proposal Gate** | 共用 | 人工核可 + rollback + no-bet fail-safe | 嚴格 deferred 到所有上游 gate PASS |

## 4. 關鍵阻塞

1. **P30 commit 未完成**：工作區還在錯誤 repo（`Betting-pool`），13 個 P30 檔案處於 staged 但未 commit
2. **2024 raw data 不存在**：`data/mlb_2024/` 缺席是 P28/P29 BLOCK 的根因
3. **模型 edge 分布過薄**：P13 OOF BSS = +0.008，不足以撐起 1,500 active entries
4. **P17 settlement join 從未真正閉環**：策略主軸缺最終 P/L 證據
5. **TSL 春訓 2026 資料與 2025 歷史宇宙零重疊**（memory 已記）：CLV 研究現階段只能用 post-game proxy

## 5. 最該聚焦的系統優化方向

**不是 P31「build joined artifacts」這種 plumbing。**

最高槓桿的單一動作是 **P32 — 真實取得 2024 MLB 全季 game logs + 收盤 odds**，理由：

- 直接把 1,577 → ~4,000 candidates（>2× scale）
- 拆掉 P28 sample wall 的硬性卡點
- 為 P33 model improvement 提供 cross-season walk-forward
- 不需動既有產品契約（P16/P19/P20 已成鏈，新資料直接灌入）
- 完全 PAPER，無 live TSL 風險

第二槓桿是 **P33 模型品質**：若 OOF BSS 從 +0.008 → +0.020，57.5% 邊際 edge < 5% 的樣本會大幅縮減 → active entries 自然成長。

---

# 下一個立即執行任務 Prompt

```text
# ROLE
You are Betting-pool's P30→P31 Transition Agent.

# MISSION
Two-step transition:
(A) finish the interrupted P30 commit recovery in the correct repo,
(B) then plan + open P31 as an HONEST Data Reality Audit
    (NOT a "build joined artifacts" architecture step).

This task is a TRANSITION + PLANNING task, not full P31 implementation.
P31 implementation happens in the FOLLOWING agent run after this prompt commits the gate.

# PROJECT LOCK
Required repo:
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
Required branch:
  p13-clean
Forbidden repo:
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool
Required prior marker:
  P30_HISTORICAL_SOURCE_ACQUISITION_PLAN_READY

# HARD GUARD
DO NOT: push, open PR, modify workflows, write production DB,
call live TSL, scrape live odds, place real bets,
claim production readiness, enable cron / daemon,
fabricate source artifacts, run pull / reset / stash / clean,
commit DB binaries, runtime/, .venv/, outputs/, or large generated files,
commit from /Users/kelvin/Kelvin-WorkSpace/Betting-pool.
PAPER_ONLY=True, production_ready=False at every layer.

# ============================================================
# PART A — P30 COMMIT RECOVERY (must finish first)
# ============================================================

## Task A1 — Workspace verification
  cd /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
  pwd
  git rev-parse --show-toplevel
  git branch --show-current
  git log --oneline -5
  git status --short --branch | head -100

Acceptance:
  pwd = /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13
  branch = p13-clean
Otherwise STOP and report context drift.

## Task A2 — Confirm P29 / P30 markers exist
  grep "P29_SOURCE_COVERAGE_DENSITY_EXPANSION_BLOCKED" \
    00-BettingPlan/20260512/p29_source_coverage_density_expansion_report.md
  grep -E "P30_HISTORICAL_SOURCE_ACQUISITION_PLAN_READY|P30_HISTORICAL_SOURCE_ACQUISITION_PLAN_BLOCKED" \
    00-BettingPlan/20260512/p30_historical_source_acquisition_plan_report.md

If missing, STOP.

## Task A3 — Verify 13 P30 files exist
  ls \
    wbc_backend/recommendation/p30_source_acquisition_contract.py \
    wbc_backend/recommendation/p30_historical_season_source_inventory.py \
    wbc_backend/recommendation/p30_required_artifact_spec_generator.py \
    wbc_backend/recommendation/p30_source_acquisition_plan_builder.py \
    wbc_backend/recommendation/p30_dry_run_artifact_builder_skeleton.py \
    scripts/run_p30_historical_source_acquisition_plan.py \
    tests/test_p30_source_acquisition_contract.py \
    tests/test_p30_historical_season_source_inventory.py \
    tests/test_p30_required_artifact_spec_generator.py \
    tests/test_p30_source_acquisition_plan_builder.py \
    tests/test_p30_dry_run_artifact_builder_skeleton.py \
    tests/test_run_p30_historical_source_acquisition_plan.py \
    00-BettingPlan/20260512/p30_historical_source_acquisition_plan_report.md

If any missing → STOP, do NOT partial-commit.

## Task A4 — Stage exactly 13 files & verify count
  git add <above 13 paths>
  git diff --cached --name-only | wc -l    # expect 13
  git diff --cached --name-only

If != 13, STOP.

## Task A5 — Forbidden-file check
  git diff --cached --name-only \
    | grep -E "\.(db|db-wal|db-shm|sqlite|sqlite3)$|^runtime/|^outputs/|^\.venv/" \
    || echo "NO_FORBIDDEN_FILES"
Expected: NO_FORBIDDEN_FILES

## Task A6 — Commit (do NOT push)
  git commit -m "feat(betting): plan P30 historical season source acquisition"

## Task A7 — Post-commit verify
  git log --oneline -3
  git status --short --branch | head -100
  git diff --cached --name-only

# ============================================================
# PART B — P31 HONEST DATA REALITY AUDIT (PLANNING ONLY)
# ============================================================

CONTEXT: P30 marked "READY" because the contract permits any inventory plan
where ready_sources >= threshold. But of the 348 ready sources, the majority
are derived pipeline outputs in outputs/, NOT new raw historical data.
P28 + P29 confirmed: 324 active entries, no policy combo reaches 1,500.
The roadmap has drifted into auditing-the-audit. P31 must HONEST-audit
the real raw-data deficit and decide the 2024 acquisition path.

## Task B1 — Draft P31 mission spec
Produce 00-BettingPlan/20260513/p31_mission_spec.md containing:

1. Phase name:
   P31 — Honest Data Reality Audit & 2024 Acquisition Decision Gate
2. Mission statement:
   Distinguish raw historical sources from derived pipeline outputs.
   Decide whether 2024 MLB season ingestion is feasible & safe.
3. Source classification taxonomy:
   - RAW_PRIMARY  (CSV from data/, with game-day timestamps, no model fields)
   - RAW_SECONDARY (Retrosheet / MLB Stats API exports, externally sourced)
   - DERIVED_OUTPUT (outputs/predictions/PAPER/**, p15/p25/p27 children)
   - SCHEMA_PARTIAL (raw but missing canonical columns)
4. Required external sources for 2024:
   - Retrosheet 2024 game logs (gl2024)
   - MLB Stats API 2024 schedule + linescore
   - Closing moneyline odds 2024 (which provider? license check needed)
5. Gate constants (draft):
   P31_HONEST_DATA_AUDIT_READY
   P31_BLOCKED_NO_RAW_HISTORICAL_INCREMENT
   P31_BLOCKED_LICENSE_PROVENANCE_UNSAFE
   P31_BLOCKED_NON_DETERMINISTIC_INVENTORY
   P31_FAIL_INPUT_MISSING
6. Acceptance criteria for P31 READY:
   - At least one verifiable 2024 raw primary source path identified
   - Provenance + license documented
   - Schema gap inventory updated (real, not theoretical 54,675)
   - 2024 acquisition decision: GO / NO-GO with reason
   - All counters distinguish raw vs derived (no double-counting)
7. Hard non-goals:
   - Do not download data in P31 (that is P32)
   - Do not build joined input artifacts (was old P31, deprecated)
   - Do not fabricate
8. Out-of-scope notes for CTO:
   - Original P30 "n_ready_sources=348" is misleading — flag for downgrade
   - "expected_sample_gain=54,675" is theoretical, not deliverable

## Task B2 — Draft CTO Roadmap v3 update
Produce 00-BettingPlan/20260513/cto_roadmap_realignment_20260513.md containing:

- Acknowledge P28/P29 sample wall (324 < 1500)
- Acknowledge P30 "READY" misleading nomenclature (derived ≠ raw)
- Adopt new P0–P10 ordering:
  P0  P30 Commit Recovery
  P1  P31 Honest Data Reality Audit & 2024 Acquisition Gate
  P2  P32 2024 Historical Game Logs + Closing Odds Ingestion
  P3  P33 Model Quality Improvement (OOF BSS +0.020 target)
  P4  P34 Strategy Optimization Hardening (deep P18 sweeps)
  P5  P35 P28 Re-audit Pass (1500 active entries unlock)
  P6  P36 P17 Ledger Settlement Closure
  P7  P37 TSL Market Expansion (run line + totals)
  P8  P38 Live TSL Snapshot Bridge (PAPER snapshot, no orders)
  P9  P39 Daily Ops & Drift Monitoring
  P10 P40 Production Proposal Gate
- Explicit critical-blocker list
- Highest-leverage next action statement: P32 acquisition is the single
  highest-leverage move; P33 second; everything else gated

Marker at end of file:
  CTO_MLB_P30_P31_ROADMAP_REALIGNMENT_20260513_READY

## Task B3 — Commit B-part deliverables
Stage exactly:
  00-BettingPlan/20260513/p31_mission_spec.md
  00-BettingPlan/20260513/cto_roadmap_realignment_20260513.md
  docs/orchestration/mlb_betting_prediction_strategy_roadmap_reset_2026-05-10.md   (IF updated to point at v3)

Forbidden-file check again → NO_FORBIDDEN_FILES.

  git commit -m "docs(betting): P31 mission spec + CTO roadmap v3 realignment"

# ============================================================
# PART C — FINAL OUTPUT
# ============================================================
Return:
1. Repo path verified
2. Branch verified
3. Part A commit hash + 13-file confirmation
4. Part B commit hash + spec/roadmap file paths
5. Forbidden-file check results
6. P30 marker found
7. Whether any P30 tests were re-run (or skipped because identical state)
8. Final git log --oneline -5
9. Confirmation: NOT PUSHED
10. Next agent run target: P31 implementation (audit execution, not planning)

# FINAL MARKER
P30_COMMIT_RECOVERY_AND_P31_PLANNING_READY
```

---

## 摘要

- **發現**：P28→P29→P30 三 phase 都在審計同一個樣本量不足問題，roadmap 已偏移成「審計-審計-審計」循環
- **真正瓶頸**：2024 raw data 不存在 + 模型 edge 太薄（BSS +0.008）
- **重排 P0–P10**：commit recovery → 誠實資料審計 → **2024 季實際取得** → 模型品質 → 策略硬化 → 樣本牆解封 → ledger 閉環 → 市場擴張 → 真實 odds bridge → ops 監控 → 生產閘
- **單一最高槓桿**：P32 — 取得 2024 MLB 全季 raw data
- **下一步任務 prompt**：P30 commit recovery + P31 mission spec + CTO roadmap v3 撰寫（合併一次 agent run）