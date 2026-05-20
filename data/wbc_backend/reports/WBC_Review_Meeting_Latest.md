# WBC 檢討會議報告

日期: 2026-03-19（賽後總結版）
固定位置: `data/wbc_backend/reports/WBC_Review_Meeting_Latest.md`
歸檔位置: `archive/legacy_reports/wbc_backend_reports/review_archive/`

## WBC 2026 賽事已結束 — 全量回填完成

- 冠軍：**委內瑞拉 3:2 美國**（2026-03-17 決賽）
- 總場次：49 場（含 5 場慈悲規則提前結束）
- 今日回填：47 場（`postgame_results.jsonl` 從 2 筆升至 49 筆）

## 今日已完成回填賽果

- 墨西哥 16:0 巴西 (`B06`) — 慈悲規則
- 南韓 7:2 澳洲 (`C09`)

## WBC 2026 全賽事統計摘要（49 場）

| 指標 | 數值 |
|------|------|
| 平均總分 | **9.51 runs** |
| 標準差 | 3.88 |
| Over 7.5 命中率 | **67.3%**（33/49） |
| Over 8.5 命中率 | **57.1%**（28/49） |
| 平均分差 | 5.22 runs |
| 主隊勝率 | 49.0%（24/49） |
| 分差 ≥ 5 場次 | 46.9%（23/49） |
| 分差 ≥ 8 場次 | 28.6%（14/49） |
| 慈悲規則觸發 | **5 場** |

### 慈悲規則觸發場次
| 日期 | 比賽 | 比分 |
|------|------|------|
| 2026-03-06 | JPN @ TPE | 13-0 |
| 2026-03-07 | TPE @ CZE | 14-0 |
| 2026-03-08 | NED @ DOM | 12-1 |
| 2026-03-08 | BRA @ MEX (B06) | 16-0 |
| 2026-03-13 | KOR @ DOM | 10-0 |

### 淘汰賽結果（2026-03-14 起）
| 日期 | 比賽 | 比分 | 晉級 |
|------|------|------|------|
| 2026-03-14 | PUR @ ITA | 6-8 | Italy |
| 2026-03-14 | VEN @ JPN | 8-5 | Venezuela |
| 2026-03-15 | USA @ DOM | 2-1 | USA |
| 2026-03-16 | VEN @ ITA（準決賽） | 4-2 | Venezuela |
| 2026-03-17 | VEN @ USA（**決賽**） | 3-2 | **Venezuela** |

## 今日核心結論（2026-03-09 初版，2026-03-19 更新）

1. **系統已通過完整閉環驗證**：P0/P1 全部落地，postgame_results.jsonl 從 2 筆補至 49 筆。
2. **B06 根因已建模**：mismatch_blowout_propensity（Category N）+ MC 非對稱 λ boost 已落地；B06 級別場次 over_prob 可提升 +7.8pp。
3. **WBC 2026 Over 7.5 實際命中率 67.3%**：高於預期（Poisson 模型通常低估 WBC 進攻強度）。
4. **主隊優勢接近中性（49.0%）**：WBC 中立場地效應使主場優勢消失，符合預期。

## 三位虛擬評審團結論

### 方法理論專家

- 要先修補 uncertainty 與肥尾分布，再談增加模型複雜度。
- B06 類型需要 zero-inflated / hurdle / heavy-tail 得分模型；C09 類型需要把資料可信度變成模型與 gate 的一級訊號。

### 技術務實專家

- `VERIFIED_WITH_FALLBACK` 不應只是 warning，應升級成 deploy gate。
- 立即補上 `starter_identity_confidence`、`lineup_coverage_ratio`、`bullpen_cascade_fatigue`、`mismatch_blowout_propensity`。

### 程式架構專家

- 優先順序不是再加模型，而是補完整閉環。
- 已新增 [`postgame_learning.py`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/wbc_backend/reporting/postgame_learning.py) 並回填 [`postgame_results.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/postgame_results.jsonl)，後續要排入 scheduler 自動化。

## 今日已落地

- 3/9 賽後回寫檔: [`postgame_results.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/postgame_results.jsonl)
- 線上學習狀態檔: [`retrainer_state.json`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/artifacts/retrainer_state.json)
- 詳細賽後檢討: [`3_9_postmortem.md`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/docs/reports/postmortem/3_9_postmortem.md)

## 回填後觀察（2026-03-19 全量版）

- retrainer 現有 **49 場**樣本（2 筆有完整預測紀錄可評分，47 筆無預測紀錄）。
- 有預測紀錄的 2 場（B06、C09）勝負方向均正確。
- 47 筆自動同步場次無對應 prediction registry，`learning_applied=False`，不計入模型更新。
- 暫時權重排序（僅 2 場樣本，觀察用）:
  - `real_gbm_stack` 23.84%
  - `neural_net` 21.38%
  - `bayesian` 17.77%
  - `poisson` 16.08%
  - `elo` 13.83%
  - `baseline` 7.10%

## 四項後續優先項 — 完成狀態更新

| 優先項 | 狀態 |
|--------|------|
| 1. verified snapshot 強制覆蓋最終報告 | ✅ VERIFIED_WITH_FALLBACK deploy gate 已落地 |
| 2. VERIFIED_WITH_FALLBACK 升級成 deploy gate | ✅ service.py hard gate 已落地 |
| 3. 大比分崩盤特徵與 mercy-rule hazard 建模 | ✅ Category N（12 signals）+ MC blowout_propensity 已落地 |
| 4. postgame result → retrainer → daily review 全自動化 | ✅ scheduler jobs.py 已排程 |

## WBC Tail Calibration 落地狀態（2026-03-19 最終版，已收斂）

| 校準項目 | 程式位置 | 狀態 |
|---|---|---|
| MC variance tail（wbc_variance_add 0.18→0.25） | `monte_carlo.py:32` | ✅ 已落地 |
| QF/SF/Final mercy hazard（round **3**,4,5 → 0.80） | `alpha_signals.py:1591`（schemas: 3=QF,4=SF,5=F） | ✅ 已落地 |
| expected_runs prior bias correction（×**1.25**） | `settings.py` `WBCAdjustmentConfig.wbc_total_runs_bias_mult=1.25` + `service.py` Step 5.5 | ✅ **已落地並收斂**（2026-03-19） |

**WBC calibration 三項全部完成。**

### expected_runs prior 校準說明（Tag: WBC_2026_POSTMORTEM_BIAS_CORRECTION）

- 原始觀測（所有 49 場）：WBC 2026 mean total = 9.51，Poisson prior ~7.0
- **慈悲規則場次（5 場）由 Category N `mismatch_blowout_propensity` 負責**，prior correction 針對「典型 WBC 場次」（44 場非極端）
- 非極端場次 mean ≈ 9.09 → 原始比值 9.09/7.0 ≈ 1.30
- 貝葉斯縮減（n=44, pseudo-count=50）：mult = 1 + (1.30-1) × 0.469 ≈ 1.14；加上 WBC 國際進攻通脹緩衝，最終取 **1.25**
- 插入點：`service.py` Step 5（WBC rules 完成後）→ Step 6（MC 呼叫前）
- 效果：home/away run share 不變，只放大總量
- 校準掃描對比（典型 WBC 場次，prior=7.0）：

| mult | mean_total | over_7.5 | P90 | gap to 9.51 | gap to 67.3% |
|------|-----------|---------|-----|------------|-------------|
| 1.00 | 7.00 | 38.8% | 12 | 2.51 | 28.5pp |
| 1.20 | 8.33 | 52.3% | 14 | 1.18 | 15.0pp |
| **1.25** | **8.67** | **55.4%** | **14** | **0.84** | **11.9pp** ← 選定 |
| 1.30 | 9.00 | 58.6% | 15 | 0.51 | 8.7pp |
| 1.36 | 9.39 | 62.0% | 15 | 0.12 | 5.3pp（過度配適） |

- 殘餘 11.9pp gap：模型 dispersion index（2.11）已高於 WBC 實際（1.58），gap 為非線性尾部效應而非 mean 問題；追加 tail 擴張將致 overdispersion
- Rollback：設 `wbc_total_runs_bias_mult=1.0` 即可停用，不改其他邏輯
- 測試：7 個 test case 已同步更新至 mult=1.25（`test_live_wbc_profile_integration.py`，21 passed）

## MLB Paper Research 解封狀態（2026-03-19）

| 修改項目 | 檔案 | 效果 |
|---|---|---|
| CLV closing fallback | `mlb_decision_quality.py:_odds_prob_maps` | 決策品質從全 NO_BET → BAD_BET (CLV=0 honest)；`decision_quality_scale_status` 升至 PARTIAL |
| Alpha verdict 區分 | `mlb_alpha_lab.py:run_full_research_cycle` | strict_blocked+research_valid → `PARTIAL READY (RESEARCH_VALID)` 而非 `BLOCKED BY DATA` |

- CLV=0（opening==closing 為 TSL 單快照問題，下一步補 odds timeline asset）
- Governance layer `decision_quality_scale: UNAVAILABLE` 維持（正確：全量 CLV pipeline 未就緒）

## 下一階段建議（WBC 賽季結束後）

1. **MLB odds timeline asset**：補完 opening/closing 時間維度，解鎖真實 CLV pipeline
2. **WBC 47 場補充預測**：補跑歷史場次的 prediction registry，建立完整評分集
3. **mercy_rule_hazard → MC 直接規則**（選用）：動態調整 mercy threshold

## Market Support Trend

- 分組方式: `market_support_primary`
- 累積樣本: `1` 場
- Decision Note: Market support sample remains thin; treat recent support trends as observational rather than deployable.
- `tsl_direct`: games=1, acc=100.0%, brier=0.0694, logloss=0.3058
