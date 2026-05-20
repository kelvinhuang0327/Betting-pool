# Phase 46 — Feature Repair Blueprint

**Document type**: Spec-first design (no code changes in this phase)  
**Status**: `FEATURE_REPAIR_INVESTIGATION`  
**Generated**: 2026-05-05  
**Phase 45 audit_hash**: `b605313ff4c0cdbc…`  
**Hard rules**: ❌ 直接改模型 ❌ ensemble ❌ tuning alpha ❌ production patch

---

## Executive Summary

Phase 45 對 2,025 筆 MLB 2025 預測資料進行 segment-level value attribution，結論：

| 指標 | 數值 |
|---|---|
| global_conclusion | `CONDITIONAL_VALUE` |
| gate | `FEATURE_REPAIR_INVESTIGATION` |
| VALUE_POSITIVE segments | 2 (month:2025-05, month:2025-07) |
| VALUE_NEGATIVE segments | 1 (month:2025-04) |
| Failure segments (ECE/BSS) | 6 |
| Top positive | 2025-07 (blend_bss=+0.86%), 2025-05 (blend_bss=+0.57%) |
| Top negative | 2025-04 (blend_bss=−2.50%), 2025-06 (blend_bss=−0.44%) |

**根本問題**：模型 ECE（校準誤差）在多數 segment 系統性高於市場，尤其在：
- 強勝率球隊（heavy_favorite, ECE=0.0893 vs market 0.0330）
- 開季（2025-04, ECE=0.1992 vs market 0.1274）
- 夏季（2025-06, ECE=0.0815 vs market 0.0317）

**這不是 alpha 問題，而是 feature quality 問題。**

---

## Phase 45 完整 Segment 結果

### 所有 segment 一覽

| Dimension | Bucket | n | blend_bss | model_ece | market_ece | value |
|---|---|---|---|---|---|---|
| odds_bucket | heavy_favorite | 211 | −0.17% | 0.0893 | 0.0330 | NO_SIGNAL ⚠️ |
| odds_bucket | mid | 1,407 | +0.23% | 0.0446 | 0.0336 | NO_SIGNAL ⚠️ |
| odds_bucket | underdog | 407 | +0.32% | 0.0301 | 0.0248 | NO_SIGNAL |
| disagreement | high | 193 | +0.18% | 0.0759 | 0.0679 | NO_SIGNAL |
| disagreement | low | 1,176 | +0.08% | 0.0323 | 0.0181 | NO_SIGNAL ⚠️ |
| disagreement | medium | 656 | +0.46% | 0.0421 | 0.0488 | NO_SIGNAL ✅ |
| confidence | high_confidence | 531 | −0.27% | 0.0173 | 0.0228 | NO_SIGNAL |
| confidence | low_confidence | 848 | +0.46% | 0.0210 | 0.0263 | NO_SIGNAL |
| confidence | mid_confidence | 646 | +0.24% | 0.0557 | 0.0521 | NO_SIGNAL ⚠️ |
| month | 2025-04 | 53 | **−2.50%** | **0.1992** | 0.1274 | **VALUE_NEGATIVE** ❌ |
| month | 2025-05 | 411 | **+0.57%** | 0.0422 | 0.0545 | **VALUE_POSITIVE** ✅ |
| month | 2025-06 | 397 | −0.44% | **0.0815** | 0.0317 | NO_SIGNAL ⚠️ |
| month | 2025-07 | 369 | **+0.86%** | 0.0322 | 0.0543 | **VALUE_POSITIVE** ✅ |
| month | 2025-08 | 421 | +0.29% | 0.0418 | 0.0192 | NO_SIGNAL ⚠️ |
| month | 2025-09 | 374 | +0.11% | 0.0477 | 0.0505 | NO_SIGNAL |

> ⚠️ = ECE failure (model_ece > market_ece + 0.01), ❌ = BSS failure, ✅ = positive signal

### 確認的 Failure Segments（6 個）

| Segment | n | blend_bss | failure_type | 關鍵觀察 |
|---|---|---|---|---|
| odds_bucket:heavy_favorite | 211 | −0.17% | ECE_DETERIORATION | model_ece 2.7× market_ece |
| odds_bucket:mid | 1,407 | +0.23% | ECE_DETERIORATION | 最大樣本群，ECE 仍劣化 |
| disagreement:low | 1,176 | +0.08% | ECE_DETERIORATION | 模型市場一致時校準反而差 |
| month:2025-04 | 53 | **−2.50%** | **BOTH** | 開季校準崩潰 |
| month:2025-06 | 397 | −0.44% | ECE_DETERIORATION | 夏初 ECE 2.6× market |
| month:2025-08 | 421 | +0.29% | ECE_DETERIORATION | 換季前 ECE 劣化 |

---

## Feature Gap Analysis

### Gap 1 — 開季冷啟動（season-start cold start）

**Failure segment**: `month:2025-04` (BOTH: BSS −2.50%, ECE 0.1992)  
**問題型態**: `OVERCONFIDENCE` + `MARKET_OUTPERFORM`  
**觀察**:
- 樣本最小（n=53），但校準誤差最高（ECE 0.1992 vs market 0.1274）
- 開季時，球隊戰力評估依賴上季末數據，但陣容已大幅變動
- 市場透過 spring training 資訊調整賠率；模型沿用 ELO/WOBA/FIP 但缺乏休賽期更新

**推測缺失 feature 類型**:
- `lineup_strength`：春訓先發名單與開季陣容一致性
- `starting_pitcher`：開季投手輪換確認（春訓未出賽者）
- `recent_form`：春訓成績（有限但有信號）

---

### Gap 2 — 強勝率球隊校準（heavy_favorite calibration）

**Failure segment**: `odds_bucket:heavy_favorite` (ECE_DETERIORATION: model_ece=0.0893 vs 0.0330)  
**問題型態**: `OVERCONFIDENCE`  
**觀察**:
- 市場 ECE=0.0330（校準良好），模型 ECE=0.0893（嚴重失準）
- 主場大幅優勢時（market_prob ≥ 0.65），模型無法準確反映差距
- 正確率（wr=0.725）確認重度主場優勢確實存在，但模型概率分布過於分散
- 模型 BSS=−1.59%（明顯輸給市場），blend 稍微改善至−0.17%

**推測缺失 feature 類型**:
- `park_factor`：主場優勢球場（Fenway, Coors Field, Great American, etc.）未充分編碼
- `starting_pitcher`：王牌先發（Ace pitcher）對比弱輪流先發的差距
- `lineup_strength`：比賽當日實際出賽名單 vs 理論最佳陣容

---

### Gap 3 — 夏季 ECE 崩潰（summer ECE collapse）

**Failure segments**: `month:2025-06` (ECE 0.0815 vs 0.0317), `month:2025-08` (ECE 0.0418 vs 0.0192)  
**問題型態**: `MARKET_OUTPERFORM`  
**觀察**:
- 2025-06 model_ece 高達 0.0815（市場 0.0317），ECE 差距最大月份
- 六月：傷兵名單（IL placements）高峰期、中繼投手負荷累積、交易謠言影響陣容
- 八月：trade deadline（7/31）後新球員整合期、球隊放棄/衝刺分歧
- 模型使用靜態賽季特徵，未追蹤陣容即時變動

**推測缺失 feature 類型**:
- `bullpen_state`：中繼牛棚前 7 天投球局數、疲勞指數
- `recent_form`：前 10 場勝率、打擊率滾動窗口
- `lineup_strength`：IL 名單中的明星球員數量

---

### Gap 4 — 低分歧校準劣勢（disagreement-low ECE failure）

**Failure segment**: `disagreement:low` (n=1,176, ECE_DETERIORATION: 0.0323 vs 0.0181)  
**問題型態**: `UNDERCONFIDENCE` / 系統性偏差  
**觀察**:
- 當 |model − market| < 0.05 時，模型與市場方向一致，但 ECE 仍比市場差
- 這表示模型的**輸出分布形狀**與市場不同，即使方向正確
- 最可能原因：模型對「中立概率」（0.45–0.55）的預測群集化，而市場在同一區間更分散
- 此段佔樣本 58%（1,176 筆），是最關鍵的修復目標

**推測缺失 feature 類型**:
- `park_factor`：中性球場特徵，正確識別「真正平衡對戰」
- `starting_pitcher`：「同等先發」的定量評估，而非二元 ace/journeyman

---

### Gap 5 — 高信心方向誤差（high_confidence directional failure）

**Failure segment**: `confidence:high_confidence` (n=531, blend_bss=−0.27%)  
**問題型態**: `OVERCONFIDENCE`（方向性）  
**觀察**:
- 模型 ECE=0.0173（優於市場 0.0228），校準反而正確
- 但 blend_bss=−0.27%：加入 40% 模型後反而比純市場差
- 代表：當模型遠離 0.5 時，其方向選擇偶爾與市場衝突，但市場才是正確的
- wr=0.593 遠高於基準（0.53），說明此 bucket 存在強主場效應

**推測缺失 feature 類型**:
- `starting_pitcher`：主客場對比先發 FIP 差距
- `recent_form`：近 5 場形勢（momentum 指標）

---

## Feature 設計規格（核心）

### F-001 — Starting Pitcher Quality Delta

| 欄位 | 內容 |
|---|---|
| **feature_name** | `sp_fip_delta` |
| **描述** | 主場先發 FIP − 客場先發 FIP（本賽季滾動 60 天）。正值代表主場投手較優。 |
| **資料來源** | FanGraphs Leaderboards / MLB StatsAPI `gameFeed.liveData.boxscore` |
| **計算方式** | `sp_fip_delta = home_sp_fip_60d - away_sp_fip_60d`（比賽日**開賽前**最後已知值） |
| **時間點安全** | ✅ 只使用開賽前已公告先發（`probablePitcher`），不使用比賽中換投資訊 |
| **預期改善 segment** | `odds_bucket:heavy_favorite`（ECE -30%）、`confidence:high_confidence`（BSS +0.3%） |

**Hypothesis**: 加入 `sp_fip_delta` 後，heavy_favorite segment 的 model_ece 應從 0.0893 下降至 0.055 以下，因為模型將能區分「整體強隊」與「今日先發強隊」的差異。

---

### F-002 — Park Run Factor

| 欄位 | 內容 |
|---|---|
| **feature_name** | `park_run_factor` |
| **描述** | 比賽地點球場的得分因子（100 = 聯盟平均），基於三年滾動 park factor 資料。 |
| **資料來源** | Baseball Reference Park Factors / ESPN Park Factor tables（年度更新） |
| **計算方式** | 直接查表，以 `home_team` + `season` 為鍵。正規化至 [0.8, 1.2]。 |
| **時間點安全** | ✅ 使用**前一整年**的 park factor，無未來資訊 |
| **預期改善 segment** | `odds_bucket:heavy_favorite`（ECE −25%）、`disagreement:low`（ECE −15%） |

**Hypothesis**: 加入 `park_run_factor` 後，heavy_favorite segment 的校準誤差將縮小，因為高得分球場（Coors, Great American）主場優勢被正確量化，而非由 ELO 模糊吸收。

---

### F-003 — Bullpen Fatigue Index

| 欄位 | 內容 |
|---|---|
| **feature_name** | `bullpen_fatigue_7d` |
| **描述** | 主客場各自中繼投手前 7 天累積投球局數。差值 = home - away。 |
| **資料來源** | MLB StatsAPI `game/v1/pitchers` 或 `stats/game` API（逐場記錄） |
| **計算方式** | `fatigue = Σ IP(bullpen, last 7 calendar days)`，以比賽日前一天為截止點 |
| **時間點安全** | ✅ 只累積比賽日前已完成的比賽投球局數 |
| **預期改善 segment** | `month:2025-06`（ECE −30%）、`month:2025-08`（ECE −15%） |

**Hypothesis**: 加入 `bullpen_fatigue_7d` 後，2025-06 的 model_ece 應從 0.0815 下降，因為六月牛棚疲勞是導致後段比賽強隊失手的主要未被捕捉因素。

---

### F-004 — Season-Start ELO Warm-up Dampener

| 欄位 | 內容 |
|---|---|
| **feature_name** | `season_game_index` |
| **描述** | 球隊本賽季已出賽場次（0 = 開季第一場）。用於降低開季 ELO 特徵的權重。 |
| **資料來源** | 由歷史比賽記錄計算，無需外部 API |
| **計算方式** | `game_index = count(games_played_by_team_in_season, before=game_date)`。可做為 ELO 信心係數：`elo_confidence = min(1.0, game_index / 30)` |
| **時間點安全** | ✅ 只計算比賽日之前的已完成場次 |
| **預期改善 segment** | `month:2025-04`（BSS +1.5%，ECE −30%） |

**Hypothesis**: 加入 `season_game_index` 作為 ELO 調節器後，開季（2025-04）的校準誤差應從 0.1992 大幅下降，因為 ELO 在低場次時的不確定性將被明確建模。

---

### F-005 — Recent Team Form（10-Game Rolling）

| 欄位 | 內容 |
|---|---|
| **feature_name** | `form_10g_delta` |
| **描述** | 主客場各自前 10 場勝率差值。用於捕捉短期動能。 |
| **資料來源** | 由歷史比賽記錄滾動計算 |
| **計算方式** | `form_delta = home_win_rate_10g - away_win_rate_10g`。若場次 < 10，使用所有可用場次。 |
| **時間點安全** | ✅ 只使用比賽日前已完成場次 |
| **預期改善 segment** | `confidence:high_confidence`（BSS +0.2%）、`month:2025-06`（ECE −10%） |

**Hypothesis**: 加入 `form_10g_delta` 後，high_confidence segment 的方向誤差應縮小，因為當模型概率遠離 0.5 但近期 form 逆向時，模型將有機制自我修正。

---

### F-006 — Active Roster Strength Index（IL 調整）

| 欄位 | 內容 |
|---|---|
| **feature_name** | `active_roster_strength` |
| **描述** | 主客場當前 40 人名單中，在 IL（Injured List）的明星球員 WAR 損失。 |
| **資料來源** | MLB StatsAPI `transactions` endpoint（每日異動記錄） |
| **計算方式** | `il_war_loss = Σ WAR(players on IL, current roster)`（使用前一賽季 WAR 作為代理） |
| **時間點安全** | ✅ 只使用比賽日前已公告的 IL transaction |
| **預期改善 segment** | `month:2025-06`（ECE −20%）、`month:2025-08`（ECE −10%） |

**Hypothesis**: 加入 `active_roster_strength` 後，夏季月份的 ECE 劣化應減緩，因為主力球員傷退是市場與模型最大的資訊不對稱點。

---

## 優先順序

### P0 — 立即執行（直接對應 Failure Segments）

| Feature | Target Failure Segment | 預期效益 | 實作複雜度 |
|---|---|---|---|
| **F-004** `season_game_index` | month:2025-04 (BOTH failure) | ECE −30%, BSS +1.5% | **低**（只需計算場次）|
| **F-001** `sp_fip_delta` | odds_bucket:heavy_favorite (ECE ×2.7) | ECE −30% | **中**（需對接 StatsAPI probablePitcher）|
| **F-002** `park_run_factor` | odds_bucket:heavy_favorite, disagreement:low | ECE −25% (heavy), −15% (low) | **低**（靜態查表）|

**理由**: 這三個 feature 對應最嚴重的兩個 failure patterns（開季崩潰 + heavy_favorite ECE），且實作複雜度低，可快速驗證。

---

### P1 — 重要（強化 Positive Segments + 修補夏季 ECE）

| Feature | Target Segment | 預期效益 | 實作複雜度 |
|---|---|---|---|
| **F-003** `bullpen_fatigue_7d` | month:2025-06, 2025-08 | ECE −30%, −15% | **中**（需滾動計算 IP）|
| **F-005** `form_10g_delta` | confidence:high_confidence, 2025-06 | BSS +0.2%, ECE −10% | **低**（滾動勝率）|

**理由**: 牛棚疲勞是六月 ECE 崩潰的主要嫌疑因素；近期 form 對 high_confidence 方向誤差有修正潛力。

---

### P2 — 延後/探索性

| Feature | Target Segment | 說明 |
|---|---|---|
| **F-006** `active_roster_strength` | month:2025-06, 2025-08 | IL API 整合複雜，WAR 代理指標可信度低 |
| 天氣特徵（weather API） | odds_bucket 各段 | 資料來源不穩定，與 park_factor 高度共線 |
| 主審特徵（umpire strike zone） | disagreement:low | 效果存疑，樣本驗證困難 |
| Trade deadline 衝擊指標 | month:2025-08 | 難以定量化，且 2025 資料量不足做統計驗證 |

---

## 嚴格限制（Invariants）

本 Blueprint 的所有 feature 設計必須遵守：

```
❌ 禁止直接改模型架構（新 feature 只能加入 feature vector）
❌ 禁止建立 ensemble（只能在現有 XGBoost/ELO 框架內添加特徵）
❌ 禁止調整 alpha（alpha 固定 = 0.4，per Phase 42A/43/44）
❌ 禁止建立 production patch（任何改動必須先通過 Phase 43/44/45 回測）
✅ 所有 feature 必須通過 point-in-time safety review 再進入 backtest
✅ 每個 feature 引入後必須重跑 Phase 43/44/45 全流程驗證
```

---

## Phase 47 任務清單（自動生成）

### 任務 47.1 — Feature Builder Implementation

**目標**: 實作 P0 feature 計算管線  
**檔案**:
- `models/features/sp_fip_delta.py` — F-001 先發投手 FIP 差值
- `models/features/park_run_factor.py` — F-002 球場得分因子
- `models/features/season_game_index.py` — F-004 賽季場次索引

**驗收條件**:
- [ ] 每個 feature 有 unit test，覆蓋邊界值（開季第一場、缺少先發資料）
- [ ] 所有 feature 均通過 point-in-time safety test（不洩露未來資訊）
- [ ] feature 值域合理：`sp_fip_delta` ∈ [-3, 3]，`park_run_factor` ∈ [0.8, 1.2]

---

### 任務 47.2 — Feature Integration Backtest

**目標**: 將 P0 feature 加入現有 backtest pipeline，重跑 2025 回測  
**前置條件**: 47.1 全部通過  
**流程**:
1. 在 `models/` 的 feature vector 中加入 F-001, F-002, F-004
2. 重跑 `examples/optimize_and_backtest.py`（或等效腳本）
3. 產出新版 `mlb_2025_per_game_predictions_v2.jsonl`

**驗收條件**:
- [ ] 新 JSONL schema_version = `phase47-v1`
- [ ] 總樣本數 ≥ 2,025（不得縮水）
- [ ] overall Brier score 不惡化（vs phase39-v1 baseline）

---

### 任務 47.3 — Phase 43/44/45 Re-run

**目標**: 用 v2 預測重跑完整評估流程  
**流程**:
1. `python -m orchestrator.phase43_model_value_market_blend_stability` on v2 data
2. `python -m orchestrator.phase44_market_blend_paper_tracking` on v2 data
3. `python -m orchestrator.phase45_model_value_attribution` on v2 data

**成功門檻（比較 v1 vs v2）**:
- [ ] month:2025-04 blend_bss > −1.0%（v1 = −2.50%，目標改善 ≥ 60%）
- [ ] odds_bucket:heavy_favorite model_ece < 0.060（v1 = 0.0893）
- [ ] overall blend_bss 不惡化（v1 = +0.22%）
- [ ] bootstrap CI 仍在 [SIGNIFICANT] 或維持 NOT_SIGNIFICANT 不惡化

**若未達門檻**: 將 F-001/F-002 分別控制變數重測，確認各自貢獻。

---

### 任務 47.4 — P1 Feature 決策

**觸發條件**: 47.3 成功通過  
**動作**:
- 若 month:2025-06 ECE 仍 > 0.05 → 推進 F-003 `bullpen_fatigue_7d`
- 若 confidence:high_confidence BSS 仍 < 0 → 推進 F-005 `form_10g_delta`
- 否則 → 回到 Phase 44 paper-only tracking 繼續累積樣本

---

## Gate 決策樹（Phase 47 後）

```
Phase 47 完成後
│
├── 若 month:2025-04 改善 ≥ 60% AND heavy_favorite ECE < 0.060
│   └── 繼續 P1 features → Phase 48 P1 Feature Implementation
│
├── 若改善 < 30%（P0 feature 無效）
│   └── 回 Phase 45 重新 segment analysis → 換方向
│
└── 若 overall blend_bss 惡化
    └── 回退 P0 changes → MARKET_BLEND_PAPER_ONLY
```

---

## 附錄 A — Phase 45 完整 audit trail

```
phase45_run_id        : (uuid, 每次執行不同)
phase45_audit_hash    : b605313ff4c0cdbc...
input_data            : data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl
sample_size           : 2025
date_range            : 2025-04-27 ~ 2025-09-28
alpha                 : 0.4 (fixed)
gate                  : FEATURE_REPAIR_INVESTIGATION
candidate_patch_created: False
```

---

*Phase 46 為 spec-only phase。本文件通過 review 後，方可啟動 Phase 47 實作。*
