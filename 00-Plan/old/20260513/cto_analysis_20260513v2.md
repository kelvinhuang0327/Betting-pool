已完成 CTO 重整，直接新增新版 roadmap，並把舊 roadmap 標成歷史版。

更新檔案：

- [betting_roadmap_20260513.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260513.md:1)
- [betting_roadmap_20260504.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260504.md:1)

核心判斷：現在最值得優化的方向不是再補治理文件，也不是急著做 live TSL，而是雙線並進：

1. **P0：2024 Retrosheet → pregame-safe features → OOF prediction rebuild**
   這是工程可控、可立即推進的最大槓桿，解掉 2024 prediction source 缺口。

2. **P1：Licensed 2024 closing odds approval + manual import artifact**
   P37.5 package 已 ready，但真實 `odds_approval_record.json` 和 `odds_2024_approved.csv` 尚未提供，所以 P38 仍被擋。

我也把目前實作進度寫清楚了：2025 moneyline PAPER recommendation chain 已可跑，P16.6/P18/P19/P20/P21 都已證明能產出風險修正後的 324 筆 paper recommendation、完成 settlement、daily orchestration；但 P28/P29 顯示 **324 active < 1,500**，最寬鬆政策也只有 563，所以無法做穩定性認證。真正下一階段要靠 2024 賽季資料放大樣本。

新版 P0-P10 已重排為：

- P0：2024 Retrosheet Feature Adapter + OOF Rebuild
- P1：Licensed Odds Approval + Import Artifact
- P2：2024 Joined Input Certification
- P3：Multi-Season True-Date Replay
- P4：Strategy Optimization v2
- P5：Recommendation Gate v2 + Paper Ledger Closure
- P6：TSL Market Taxonomy + Schema Pack
- P7：Run Line + Totals PAPER Prototype
- P8：Live/Approved TSL Snapshot Bridge
- P9：Daily Ops + Drift Monitoring
- P10：Production Proposal Gate

最關鍵 blocker 也已明確列入：2024 licensed odds 缺失、2024 OOF prediction source 缺失、sample wall、目前只有 moneyline、live TSL source 尚未可用、workspace drift。

驗證：已確認新 roadmap marker `CTO_MLB_BETTING_ROADMAP_V4_20260513_READY` 存在。這輪只更新文件，沒有跑測試；目前 `00-BettingPlan/roadmap/*` 在這個 worktree 仍是 untracked 狀態，我沒有 stage 或 commit。

# 版本確認 — 兩份檔案都是當前最新版

## 1. 檔案版本核對

| 檔案 | 路徑 | 最後修改 | 狀態 |
|---|---|---|---|
| 20260513v2.md | `Betting-pool/00-BettingPlan/20260513/` | 15:14（今天）| ✅ 最新工程交接 |
| cto_analysis_20260513v2.md | `Betting-pool/00-BettingPlan/20260513/` | 15:42（今天）| ✅ 最新 CTO 結論 |
| betting_roadmap_20260513.md (v4) | `Betting-pool/00-BettingPlan/roadmap/` | 15:26（今天）| ✅ 配套新 roadmap |

**我先前的 CEO 二次審查所讀取的就是這兩個 v2 檔案**（系統 reminder 也同步確認）。版本正確，分析基礎無誤。

## 2. 但發現一個之前略過的關鍵漏洞 — 需要追加調整

對照三份 CTO 產出物，**CTO 自己在同一個 24 小時內給出了互相矛盾的 P0**：

| 來源 | CTO 的 P0 | CTO 的 P1 | CTO 的 P2 |
|---|---|---|---|
| **20260513v2.md** § 8 + line 213 task prompt | **P37.6** Operator Action Packet | P38A OOF feasibility | P38 preflight |
| **cto_analysis_20260513v2.md** + roadmap v4 | **P38A** Retrosheet OOF Rebuild | Licensed Odds Approval | 2024 Joined Input |

這就是我先前指出的「**24 小時內的 roadmap drift**」實證。CTO 自己沒注意到，handoff 報告（戰術層）與 roadmap v4（策略層）相互打架。

## 3. 更嚴重的發現 — Roadmap v4 寫錯 repo 了

`cto_analysis_20260513v2.md` 第 19 行明白寫：

> 「目前 `00-BettingPlan/roadmap/*` 在這個 worktree 仍是 untracked 狀態，我沒有 stage 或 commit。」

我實際驗證的結果：
- `betting_roadmap_20260513.md` v4 寫在 **`Betting-pool`**（main 分支、stale、742 untracked）
- 它**沒有**寫在 `Betting-pool-p13`（真實工作 repo、333cf80 P37.5）
- 因此 v4 roadmap 目前完全在版本控制外，任何在 p13-clean 上工作的 agent 都看不見它

這直接強化了我 P0「Repo 治理」的判斷 — **CTO 的新 roadmap 自己就掉進了多 repo 治理的坑裡**。

## 4. 我的 CEO 分析需不需要調整？

**答案：核心結論不需要動，但要追加兩個強化點。**

### 仍然成立的部分（無需改）

| CEO P0–P10 結論 | 為何仍成立 |
|---|---|
| P0 Repo 合併計畫 + push p13-clean | ✅ 現在更急 — CTO 的 v4 寫到錯誤 repo |
| P1 Free-Source Odds Spike | ✅ 仍是拆「licensed odds 唯一路徑」的最快動作 |
| P2 P38A Retrosheet OOF | ✅ 與 CTO 策略層一致 |
| P3 TSL 多市場 schema 提前 | ✅ 用戶明示「運彩投注項目」是產品本體 |
| P7 Live TSL snapshot 提前 | ✅ read-only 不冒生產風險 |

### 需追加的強化點

1. **P0 任務 prompt 必須加一步「把 roadmap v4 從 stale repo 搬到 p13-clean」**，否則新 roadmap 會被孤立
2. **顯式 flag CTO 的內部矛盾**（P37.6 vs P38A），在 v5 roadmap 第 1 章「supersedes / reconciles」段落明確寫出
3. **P37.6 operator action packet 不應該再消耗一個 phase**；如果真的需要，應併入 P0 task 的一個小子任務（產出單一 MD 給 operator），而不是另開一個 phase 含 tests + JSON + commit

## 5. 結論

- 兩份檔案版本正確，是當前最新
- 我先前的 CEO 二次審查、P0–P10 重排、Triple-Track Task Prompt **核心都仍成立**
- 唯一需要追加的是：**P0 任務必須額外把 v4 roadmap 從錯誤 repo 搬到 p13-clean**，否則新 roadmap 永遠在版本控制外

---

## 對先前 Triple-Track Task Prompt 的最小化修訂

請在先前 prompt 的 **TRACK 1** 加入一個新子任務（其他不變）：

```text
## Task 1.4 — 救援 CTO v4 roadmap（從 stale repo 搬到 p13-clean）

CTO 在前一輪不慎將 betting_roadmap_20260513.md (v4) 寫入錯誤 repo:
  /Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260513.md

該檔案在 stale main worktree 上未追蹤，任何 p13-clean 的工作者都看不到它。
必須先在 p13-clean 建立鏡像副本，再由 v5 supersede。

執行：
  mkdir -p /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/00-BettingPlan/roadmap
  cp /Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260513.md \
     /Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13/00-BettingPlan/roadmap/betting_roadmap_20260513_v4_cto_RESCUED.md

  # 在檔頭加一行 banner（不修改原內容）
  # banner 內容：
  #   > ⚠️ RESCUED FROM STALE WORKTREE on 2026-05-13.
  #   > Original location: Betting-pool/main (untracked).
  #   > Superseded by betting_roadmap_20260513_v5_ceo.md.

驗證：
  ls 00-BettingPlan/roadmap/betting_roadmap_20260513_v4_cto_RESCUED.md
  diff <(tail -n +2 00-BettingPlan/roadmap/betting_roadmap_20260513_v4_cto_RESCUED.md) \
       /Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/roadmap/betting_roadmap_20260513.md

接著在 TRACK 5 commit 一併 stage:
  00-BettingPlan/roadmap/betting_roadmap_20260513_v4_cto_RESCUED.md
```

並在 **TRACK 4 (Roadmap v5)** 章節 1 顯式加入：

```text
## 1. CEO Decision (must include this paragraph verbatim)

This v5 supersedes betting_roadmap_20260513_v4_cto_RESCUED.md, which itself
was rescued from a stale untracked worktree. It also reconciles an internal
inconsistency in the CTO 2026-05-13 outputs: the engineering handoff doc
(20260513v2.md) named P37.6 as P0, while the CTO roadmap v4 named P38A as P0.
The CEO ruling: neither was correct in isolation.
- P37.6 was a governance loop and is downgraded to a sub-task of the
  repo-governance P0, not a full phase.
- P38A is a valid track but is dependency-ordered behind repo governance and
  the free-source feasibility spike.
- The true P0 is repo governance, because the v4 roadmap itself was lost
  to a stale worktree, proving the governance debt is now blocking
  strategic communication.
```

---

## 摘要

| 議題 | 結論 |
|---|---|
| 檔案版本 | ✅ 正確，是當天最新 v2 |
| 我先前的 CEO 分析 | ✅ 核心 P0–P10 仍成立，無需大改 |
| 需要追加 | 1) Task 1.4 救援 v4 roadmap；2) v5 第 1 章明寫 CTO 內部矛盾 |
| 最關鍵新發現 | CTO 把 v4 roadmap 寫到了 stale repo，更證明 P0=Repo 治理的必要性 |
| FINAL MARKER | 仍為 `CEO_BETTING_TRIPLE_TRACK_20260513_READY`（加上 Task 1.4 後不變）|