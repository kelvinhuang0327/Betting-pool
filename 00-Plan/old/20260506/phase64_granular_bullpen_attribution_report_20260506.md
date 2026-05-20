# Phase 64 — Granular Bullpen Attribution with OOF / PIT-safe Validation
**報告日期**: 2026-05-06  
**模組版本**: `phase64_granular_bullpen_attribution_v1`  
**Gate 結果**: `DATA_LIMITED`  
**作者**: 自動化量化研究管線 (Diagnostic-only, no production patch)

---

## 1. 執行摘要 (Executive Summary)

Phase 64 旨在利用 Phase 63 產出的顆粒化 Bullpen SSOT artifacts（1d/5d/b2b/3in4/closer 等特徵），對 2025 MLB 預測資料集進行 PIT-safe attribution 分析，並透過 OOF rolling monthly 驗證評估訊號的穩健性。

**核心發現**：Phase 63 fixture-based artifacts 僅覆蓋 4 支球隊（NYY、BOS、HOU、TB）的 2025-05-05 場次，與 2025 預測標記資料集（2,025 場、2025-04-27 至 2025-09-28）的比對率僅為 **2/2025 (0.1%)**，遠低於 10% 的最低覆蓋率門檻。

**Gate 結論**：**`DATA_LIMITED`** — 顆粒化特徵（1d、5d、b2b、3in4、closer）無法在現有標記資料集上進行有意義的 attribution。必須先對完整 2025 歷史逐場資料執行 Phase 63 ingestion pipeline，再重新執行 Phase 64。

**安全確認**：
- `CANDIDATE_PATCH_CREATED = False` ✓
- `PRODUCTION_MODIFIED = False` ✓  
- `ALPHA_MODIFIED = False` ✓
- `DIAGNOSTIC_ONLY = True` ✓

---

## 2. Phase 63 承接與資料串聯 (Phase 63 Handoff)

| 項目 | 值 |
|:-----|:---|
| Phase 63 Gate | `GRANULAR_INGESTION_READY` |
| Phase 63 Audit Hash | `4923b662e37f0ca1` |
| Phase 63 SSOT artifacts | 4 teams × 1 prediction date (2025-05-05) |
| Phase 63 appearances | 26 NormalizedReliefAppearance records |
| Phase 64 anchor hash | Derived from predictions + bullpen_3d + Phase63 SSOT |

Phase 63 已確認 MLB StatsAPI boxscore 為最佳 granular bullpen ingestion 資料源，並產出了涵蓋 10 個 AVAILABLE 特徵（2 個 DATA_LIMITED）的 SSOT schema。Phase 64 的任務是驗證這些特徵是否具備預測訊號。

---

## 3. 資料載入與對齊摘要 (Data Loading & Alignment)

### 3.1 預測資料集
| 項目 | 值 |
|:-----|:---|
| 來源 | `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` |
| 場次數 | 2,025 |
| 日期範圍 | 2025-04-27 to 2025-09-28 |
| Home win 率 | 52.99% (1,073/2,025) |

### 3.2 Phase 60 3d Baseline 對齊
| 項目 | 值 |
|:-----|:---|
| 來源 | `data/mlb_context/bullpen_usage_3d.jsonl` |
| 總筆數 | 2,430 |
| 對齊場次 | 1,890 (93.3%) |
| 有效 bull_home_3d | 1,843 |

### 3.3 Phase 63 SSOT 顆粒化對齊 ⚠️

| 項目 | 值 |
|:-----|:---|
| SSOT artifacts 筆數 | 4 |
| Partial 對齊場次 | **2** (NYY vs SDP、HOU vs MIL on 2025-05-05) |
| 完整對齊場次（雙隊） | **0** |
| 覆蓋率 | **0.1%** |
| 覆蓋率門檻 | 10% |
| **Coverage insufficient** | **True** |

**已對齊的 2 個場次**：
- `MLB2025_0515_2025-05-05_SAN_NEW` → NYY (home, fav) SSOT available
- `MLB2025_0519_2025-05-05_HOU_MIL` → HOU (away, dog) SSOT available

**說明**：Phase 63 以 fixture 方式驗證 schema，僅生產 2025-05-05 的 SSOT artifacts。2025 標記資料集中 2025-05-05 有 9 場比賽，但其中只有 NYY 和 HOU 在 SSOT 中，且兩隊均來自不同比賽（一主一客），無任何場次能同時匹配兩隊。

---

## 4. 顆粒化特徵覆蓋率分析 (Granular Feature Coverage)

Phase 64 定義了 **15 個** granular features：

| 特徵名稱 | 窗口 | 覆蓋筆數 | 覆蓋率 | 狀態 |
|:---------|:----:|:--------:|:------:|:----:|
| `bullpen_usage_last_1d_fav` | 1d | 0 | 0.0% | DATA_LIMITED |
| `bullpen_usage_last_1d_dog` | 1d | 1 | 0.05% | DATA_LIMITED |
| `bullpen_usage_last_3d_fav` | 3d | 1 | 0.05% | DATA_LIMITED |
| `bullpen_usage_last_3d_dog` | 3d | 1 | 0.05% | DATA_LIMITED |
| `bullpen_usage_last_5d_fav` | 5d | 1 | 0.05% | DATA_LIMITED |
| `bullpen_usage_last_5d_dog` | 5d | 1 | 0.05% | DATA_LIMITED |
| `reliever_b2b_count_fav` | 2d | 1 | 0.05% | DATA_LIMITED |
| `reliever_b2b_count_dog` | 2d | 1 | 0.05% | DATA_LIMITED |
| `reliever_3in4_count_fav` | 4d | 1 | 0.05% | DATA_LIMITED |
| `reliever_3in4_count_dog` | 4d | 1 | 0.05% | DATA_LIMITED |
| `closer_used_1d_fav` | 1d | 1 | 0.05% | DATA_LIMITED |
| `closer_used_2d_fav` | 2d | 1 | 0.05% | DATA_LIMITED |
| `bullpen_rest_imbalance_3d` | 3d | 0 | 0.0% | DATA_LIMITED |
| `high_leverage_used_1d_fav` | 1d | 0 | 0.0% | DATA_LIMITED (LI) |
| `high_leverage_workload_3d_fav` | 3d | 0 | 0.0% | DATA_LIMITED (LI) |

**全部 15 個特徵 DATA_LIMITED**（0 個 AVAILABLE）

**覆蓋率不足的主因**：
1. Phase 63 fixture 僅涵蓋 5 場比賽（2025-05-01 至 2025-05-04）
2. SSOT artifacts 日期（2025-05-05）在 prediction 資料集中只有 9 場
3. 在這 9 場中，SSOT 僅覆蓋 NYY 和 HOU（各為其中一方球隊）
4. 沒有任何場次同時擁有雙方 SSOT → 聯合特徵（rest_imbalance）全部 None

---

## 5. Phase 60 Baseline 複製 (Phase 60 Baseline Replication)

使用 `bullpen_usage_3d.jsonl` 複製 Phase 60 的 3d attribution 基線：

| 指標 | 值 |
|:-----|:---|
| n (有效 3d 資料) | 1,843 |
| n (heavy_fav 子集) | 59 |
| Brier Score | 0.2423 |
| Brier Skill Score (BSS) | 0.0271 |
| Heavy Fav bucket_delta | +0.1247 (high-3d wins more?) |
| Bootstrap CI (95%) | [-0.1119, +0.3613] |
| Bootstrap significant | **False** |
| Phase 60 signal label | `DIAGNOSTIC_ONLY_SIGNAL` |

**結論**：Phase 60 的 3d baseline 訊號在 Phase 64 得到完整複製——bootstrap CI 橫跨零，無法排除統計雜訊。此為 Phase 60 Gate 結果（`DIAGNOSTIC_ONLY_SIGNAL`）的再確認。

---

## 6. 顆粒化 Attribution 分析 (Granular Attribution)

由於所有 15 個特徵均為 DATA_LIMITED（覆蓋率 < 0.05%），無法執行有意義的 bucket attribution、bootstrap CI 或 OOF 驗證。

**Attribution 計算結果摘要**：
- 共計 60 筆 attribution entries（15 features × 4 segments）
- 所有 entries 的 `data_limited = True`
- 所有 entries 的 `bucket_attribution = None`（有效樣本數 < MIN_SEGMENT_N=20）
- 13 個 negative controls（非 inherently-limited 特徵）均未達 null rejection

---

## 7. Segment 分析 (Segment Analysis)

| Segment | n | 說明 |
|:--------|:-:|:-----|
| all | 2,025 | 全部預測場次 |
| heavy_favorite | 60 | fav_prob ≥ 0.70 |
| high_confidence | 10 | fav_prob ≥ 0.75 |
| phase45_failure | 14 | heavy_fav 且輸球 |

> **注意**：Segment 定義與 Phase 60 一致。Heavy_favorite n=60 為顆粒化 attribution 可用的最大 segment，但因 Phase 63 SSOT 覆蓋率為 0.1%，有效樣本數僅 0~1，無法計算統計量。

---

## 8. 負控制與 Overfit 風險 (Negative Control)

| 項目 | 結果 |
|:-----|:-----|
| 負控制執行筆數 | 13（非 inherent DATA_LIMITED 特徵）|
| null_rejected 筆數 | 0 |
| overfit_risk 筆數 | 0 |
| 結論 | 無 overfit 風險（因樣本數不足，負控制無意義）|

---

## 9. OOF Rolling Monthly 驗證 (Out-of-Fold Validation)

| 項目 | 結果 |
|:-----|:-----|
| OOF 執行筆數 | 13 |
| 有效 fold 數 | 0（所有特徵均因樣本量不足無法計算月度 fold）|
| oof_significant | False（全部）|
| oof_consistent_sign | False（全部）|

> **說明**：OOF 以 heavy_favorite segment 為基礎（n=60 in all, 0~1 with Phase63 SSOT），在 1% 覆蓋下無法產生月度 fold。此為 DATA_LIMITED 狀態下的預期結果。

---

## 10. PIT 安全性驗證 (PIT Safety Audit)

| 驗證項目 | 結果 |
|:---------|:-----|
| Phase 63 SSOT diagnostic_only 標記 | True (全部 4 artifacts) ✓ |
| Phase 63 game_date 格式 | YYYY-MM-DD (全部合法) ✓ |
| game_date 嚴格早於 boxscore 資料 | entry_date < game_date (Phase 63 保證) ✓ |
| Forbidden feature 名稱檢查 | 全部 15 個特徵通過 ✓ |
| home_win 僅作為 label 使用 | 確認 — 不作為 feature ✓ |

---

## 11. Gate 決策邏輯 (Gate Decision)

```
Gate = DATA_LIMITED

判斷條件：
  Phase63 alignment_rate = 0.1% < MIN_COVERAGE_RATE = 10%  →  coverage_insufficient = True
  ALL 15 features: coverage < threshold                    →  all data_limited = True
  → Gate = DATA_LIMITED
```

**Gate 排除條件**（均未觸發）：
- `OVERFIT_RISK`：需 null_rejected=True 且 shuffled_std > 0.10 → 未觸發
- `BULLPEN_GRANULAR_FEATURE_PROMISING`：需 OOF consistent + bootstrap sig → 未觸發
- `DIAGNOSTIC_ONLY_SIGNAL`：需 bootstrap_significant → 未觸發  
- `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING`：需 coverage ≥ threshold → 未觸發（DATA_LIMITED 優先）

**Gate Rationale**（節錄）：
> "Phase63 granular SSOT artifact coverage = 2/2025 games (0.1%) < 10% threshold. New granular features (1d, 5d, b2b, 3in4, closer) cannot be meaningfully attributed on current prediction dataset. Phase63 fixture-only artifacts do not overlap with labeled 2025 prediction history at sufficient scale. 3d replication from Phase60 confirms DIAGNOSTIC_ONLY_SIGNAL. No production patch produced."

---

## 12. 已驗證的 Gate Chain (Phase 60 → 63 → 64)

```
Phase 60: DIAGNOSTIC_ONLY_SIGNAL (3d bullpen, n=1890 aligned)
    └─▶ Phase 62: STATSAPI_SELECTED (407 tests)
         └─▶ Phase 63: GRANULAR_INGESTION_READY (140 tests, 4 SSOT artifacts)
              └─▶ Phase 64: DATA_LIMITED ← 當前
                   └─▶ Next: 需要全量 2025 歷史 ingestion → Phase 64-B 重跑
```

---

## 13. 後續行動計畫 (Next Steps)

### 立即行動 (Phase 64-B 前提)
1. **執行全量 Phase 63 ingestion**：對 `bullpen_usage_3d.jsonl` 所覆蓋的 2,430 場比賽逐一呼叫 MLB StatsAPI boxscore endpoint，產出每場比賽的 NormalizedReliefAppearance 及 SSOTFeatureArtifact。預計產出：
   - ~2,430 game-level appearances JSONL
   - ~2,430 × 2 team-level SSOT artifacts （主客各一）
   - 對齊後可覆蓋 ~1,890 預測場次（93.3% 覆蓋率，遠超 10% 門檻）

2. **重新計算 Phase 63 SSOT → prediction 對齊**：使用完整 SSOT dataset，預期覆蓋率提升至 ~90%+。

3. **重跑 Phase 64 attribution**：以新的完整 SSOT artifacts 計算所有 15 個特徵的：
   - bucket attribution（各 segment，n ≥ 20）
   - bootstrap CI（1,000 samples，95% CI）
   - negative control（shuffled distribution）
   - OOF rolling monthly（每月至少 20 samples）

### Gate 預測
基於 Phase 60 的 `DIAGNOSTIC_ONLY_SIGNAL` 結果，重跑 Phase 64 後預期 Gate 為：
- 若 OOF 月度一致 + CI 排除 0：`BULLPEN_GRANULAR_FEATURE_PROMISING` → Phase 65 paper-trade gate
- 若 OOF 不一致但方向存在：`DIAGNOSTIC_ONLY_SIGNAL`（升級版）
- 若無顆粒化額外訊號：`BULLPEN_GRANULAR_FEATURE_NOT_PROMISING` → 放棄 bullpen attribution

### 工程前提
- 需要 MLB StatsAPI rate limit 處理（約 2,430 次 API 呼叫）
- 建議使用 exponential backoff + 每批 50 場次暫停
- 歷史 boxscore 資料應快取至 `data/mlb_context/boxscores_2025/`

---

## Appendix A: 技術常數快照

| 常數 | 值 |
|:-----|:---|
| `PHASE_VERSION` | `phase64_granular_bullpen_attribution_v1` |
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `ALPHA_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |
| `ALPHA` | `0.40` |
| `_MIN_COVERAGE_RATE` | `0.10` |
| `_HEAVY_FAV_THRESHOLD` | `0.70` |
| `_HIGH_CONF_THRESHOLD` | `0.75` |
| `_MIN_SEGMENT_N` | `20` |
| `_BOOTSTRAP_N` | `1000` |
| `_OOF_PROMISING_DELTA` | `0.02` |
| `_OVERFIT_SIGMA` | `1.5` |
| `_PHASE63_AUDIT_HASH` | `4923b662e37f0ca1` |

## Appendix B: 測試覆蓋摘要

| 測試類別 | 測試數 | 說明 |
|:---------|:------:|:-----|
| TestPhase64SafetyConstants | 13 | 安全常數、Gate 常數、版本 |
| TestGranularFeatureRegistry | 10 | Registry 結構驗證 |
| TestPhase64DataclassSchemas | 6 | Dataclass 欄位驗證 |
| TestUtilityFunctions | 18 | 工具函式正確性 |
| TestPITSafety | 8 | PIT 安全性驗證 |
| TestPhase63SSOTLoading | 5 | SSOT 載入與索引 |
| TestGranularFeatureDerivation | 11 | 顆粒化特徵推導 |
| TestPhase63Alignment | 8 | Phase63 → prediction 對齊 |
| TestFeatureCoverageComputation | 6 | 特徵覆蓋率計算 |
| TestBucketAttributionAndNegativeControl | 6 | Bucket attribution 與負控制 |
| TestOOFValidation | 5 | OOF 驗證 |
| TestGateDecisionLogic | 6 | Gate 決策邏輯 |
| TestPhase60BaselineReplication | 3 | Phase60 基線複製 |
| TestPhase64EndToEnd | 18 | 端對端整合測試 |
| TestPhase6263BackwardCompatibility | 9 | 向後相容性回歸 |
| **Total** | **137** | **137/137 PASS** |

## Appendix C: Diagnostic Artifacts

| Artifact | 路徑 | 說明 |
|:---------|:-----|:-----|
| JSON 報告 | `reports/phase64_granular_bullpen_attribution_20260506.json` | 完整 attribution 結果 |
| Markdown 報告 | `00-BettingPlan/phase64_granular_bullpen_attribution_report_20260506.md` | 本報告 |
| Phase 63 SSOT | `reports/phase63_bullpen_ssot_features_20260506.jsonl` | 4 team SSOT artifacts |
| Phase 63 appearances | `reports/phase63_bullpen_relief_appearances_20260506.jsonl` | 26 NormalizedReliefAppearance |

---

*PHASE_64_GRANULAR_BULLPEN_ATTRIBUTION_VERIFIED — Gate: DATA_LIMITED*
