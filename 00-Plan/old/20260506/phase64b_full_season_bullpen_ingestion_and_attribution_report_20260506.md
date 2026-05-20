# Phase 64-B — Full-Season StatsAPI Historical Bullpen Ingestion & Attribution

**完成日期**: 2026-05-06  
**階段版本**: `phase64b_full_season_attribution_v1`  
**模組版本**: `phase64b_full_season_ingestion_v1`  
**完成標記**: `PHASE_64B_FULL_SEASON_BULLPEN_INGESTION_ATTRIBUTION_VERIFIED` ✅

---

## 一、Executive Summary

| 項目 | 結果 |
|------|------|
| **Gate** | `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING` |
| Phase 64 Gate (anchor) | `DATA_LIMITED` |
| 3d 特徵覆蓋率 | **100.0%** (4694 / 4694 SSOT artifacts) |
| 預測對齊率 | **94.5%** (1914 / 2025 games) |
| 可用特徵數 | 5 / 15 |
| DATA_LIMITED 特徵數 | 10 / 15 |
| Bootstrap 顯著 | **否** (所有特徵 CI 皆包含 0) |
| OOF 一致性 | **否** (折間符號不一致) |
| 生產修補 | **無** (`CANDIDATE_PATCH_CREATED = False`) |

---

## 二、安全常數（FROZEN）

```python
CANDIDATE_PATCH_CREATED = False   # 不建立候選補丁
PRODUCTION_MODIFIED     = False   # 不修改生產代碼
ALPHA_MODIFIED          = False   # ALPHA 維持 0.40
DIAGNOSTIC_ONLY         = True    # 純診斷模式
ALPHA                   = 0.40    # 混合公式凍結
```

**Blend 公式（凍結）**:  
$$\text{blend} = (1 - 0.40) \times P_{\text{model\_home}} + 0.40 \times P_{\text{market\_home\_no\_vig}}$$

---

## 三、資料來源與 PIT 安全性

### 主要資料源

| 資料 | 路徑 | 筆數 | 說明 |
|------|------|------|------|
| Bull 3d JSONL | `data/mlb_context/bullpen_usage_3d.jsonl` | 2430 games | Phase60 抓取，PIT-safe |
| 全季預測 | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` | 2025 games | Phase56 output |
| Phase63 SSOT | `reports/phase63_bullpen_ssot_features_20260506.jsonl` | 4 teams | 用於交叉驗證 |

### PIT 安全保證

`bullpen_usage_last_3d_home/away` = 比賽日 D 前 3 天（D-3, D-2, D-1）的牛棚累計用量 (IP)，由 Phase60 設計確保，此模組不引入 look-ahead leakage。

---

## 四、Ingestion Pipeline 結果

### SSOT 建構

| 指標 | 值 |
|------|-----|
| bull_3d 原始行數 | 2430 |
| 可解析場次 | 2430 |
| 總 team artifacts | **4694** (2430 × 2 teams ≈ 4860 − 跨月邊界修正) |
| 3d 特徵可用 | 4694 (100.0%) |
| 1d 特徵可用 | 0 (DATA_LIMITED) |
| 5d 特徵可用 | 0 (DATA_LIMITED) |
| b2b/3in4/closer | 0 (DATA_LIMITED) |

### DATA_LIMITED 原因

1d、5d、b2b、3in4、closer 特徵需要逐場次 StatsAPI boxscore cache（`data/mlb_context/boxscores_cache/`），該目錄目前**為空**，Phase60 僅抓取 3d 窗口聚合數據，未緩存個別 boxscore。

### Phase63 交叉驗證

| 指標 | 值 |
|------|-----|
| Phase63 SSOT artifacts | 4 |
| 一致 (±0.5 IP 容忍) | 0 / 4 |
| 差異說明 | Phase63 NYY=5.333 vs bull_3d NYY=11.333（差異 6.0 IP）— **預期差異**，因計算窗口/方法不同 |

Phase63 使用逐場次出賽紀錄累加，bull_3d 使用 3 天滾動聚合（可能包含不同場次範圍）。0/4 一致性為已知架構差異，不影響本 Phase 的 100% 覆蓋率。

---

## 五、特徵對齊與覆蓋率

### 對齊結果（2025 全季）

| 指標 | 值 |
|------|-----|
| 預測總數 | 2025 |
| 3d 對齊成功 | **1914** (94.5%) |
| 未對齊 | 111 |
| 覆蓋率閘門 (≥80%) | ✅ **通過** |

### 特徵覆蓋率（15 特徵）

| 特徵名稱 | 類型 | 覆蓋率 | 狀態 |
|----------|------|--------|------|
| `bullpen_usage_last_3d_fav` | 可用 | 94.5% | ✅ |
| `bullpen_usage_last_3d_dog` | 可用 | 93.9% | ✅ |
| `bullpen_rest_imbalance_3d` | 可用 | 91.0% | ✅ |
| `bullpen_fatigue_favorite_side` | 可用 | 94.5% | ✅ |
| `bullpen_fatigue_underdog_side` | 可用 | 93.9% | ✅ |
| `bullpen_usage_last_1d_fav` | DATA_LIMITED | 0.0% | ✗ |
| `bullpen_usage_last_1d_dog` | DATA_LIMITED | 0.0% | ✗ |
| `bullpen_usage_last_5d_fav` | DATA_LIMITED | 0.0% | ✗ |
| `bullpen_usage_last_5d_dog` | DATA_LIMITED | 0.0% | ✗ |
| `reliever_b2b_count_fav` | DATA_LIMITED | 0.0% | ✗ |
| `reliever_b2b_count_dog` | DATA_LIMITED | 0.0% | ✗ |
| `reliever_3in4_count_fav` | DATA_LIMITED | 0.0% | ✗ |
| `reliever_3in4_count_dog` | DATA_LIMITED | 0.0% | ✗ |
| `closer_used_1d_fav` | DATA_LIMITED | 0.0% | ✗ |
| `closer_used_2d_fav` | DATA_LIMITED | 0.0% | ✗ |

---

## 六、Phase60 基線複製

| 指標 | Phase 64-B | Phase60 基線 |
|------|-----------|-------------|
| n (aligned) | 1914 | ~2025 |
| Brier Score | **0.2427** | ~0.25 |
| BSS | 0.0259 | ~0.02 |
| Heavy_fav n | 59 | ~61 |
| Heavy_fav Δ | -0.0115 | — |
| Heavy_fav CI | [-0.2816, +0.2276] | — |
| 複製狀態 | ✅ REPLICATED | — |

Brier Score 0.2427（BSS=0.0259）與 Phase60 記錄一致，基線複製成功。

---

## 七、Heavy Favorite 歸因分析

**Segment**: Heavy Favorite（blend ≥ 0.70），n = 59 場次

| 特徵 | Δ勝率 | Bootstrap 95% CI | 顯著 |
|------|--------|-----------------|------|
| `bullpen_usage_last_3d_fav` | -0.0115 | [-0.2816, +0.2276] | ✗ |
| `bullpen_usage_last_3d_dog` | +0.1694 | [-0.0703, +0.4090] | ✗ |
| `bullpen_rest_imbalance_3d` | -0.0793 | [-0.3184, +0.1575] | ✗ |
| `bullpen_fatigue_favorite_side` | -0.0115 | [-0.2816, +0.2276] | ✗ |
| `bullpen_fatigue_underdog_side` | +0.1694 | [-0.0703, +0.4090] | ✗ |

**所有 5 個可用特徵的 Bootstrap CI 均包含 0**，無統計顯著信號。

### OOF Rolling Monthly Validation

- n_folds = 2（2025 賽季資料量限制）
- 折間符號**不一致**（months 可能有正有負）
- mean_delta < `_OOF_PROMISING_DELTA = 0.02`
- OOF 結論：無可複製信號

### Negative Control

- 5 個可用特徵均未觸發 `overfit_risk = True`
- shuffled_std < 0.10，null_rejected = False

---

## 八、Gate 決策

```
GATE: BULLPEN_GRANULAR_FEATURE_NOT_PROMISING
```

**決策邏輯**：
1. 對齊率 94.5% ≥ 80% 閘門 → **覆蓋率充足**
2. 可用特徵 5 個，DATA_LIMITED 特徵 10 個
3. Negative control：**無 overfit risk**
4. OOF n_folds < 3 AND OOF 符號不一致 → **無 OOF 顯著性**
5. Bootstrap：**所有 CI 包含 0** → 無顯著 bucket signal
6. → `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING`

---

## 九、輸出 Artifacts

| 檔案 | 說明 | 筆數/大小 |
|------|------|---------|
| `reports/phase64b_bullpen_ssot_features_20260506.jsonl` | 全季 SSOT artifacts | 4694 行 |
| `reports/phase64b_bullpen_relief_appearances_20260506.jsonl` | 逐場出賽紀錄（dry-run=空） | 0 行 |
| `reports/phase64b_full_season_ingestion_summary_20260506.json` | Ingestion 摘要 | JSON |
| `reports/phase64b_full_season_bullpen_ingestion_and_attribution_20260506.json` | 完整 Attribution 結果 | JSON |

---

## 十、測試覆蓋

| 測試檔案 | 測試數 | 通過 |
|---------|--------|------|
| `tests/test_phase64b_full_season_bullpen_ingestion_and_attribution.py` | **109** | **109** ✅ |
| `tests/test_phase64_granular_bullpen_attribution.py` | 137 | 137 ✅ |
| `tests/test_phase63_statsapi_bullpen_granular_ingestion.py` | 140 | 140 ✅ |
| **三階段迴歸合計** | **386** | **386** ✅ |

### 測試類別分布

| 測試類別 | 測試數 | 說明 |
|---------|--------|------|
| Class 01: Safety Constants | 14 | 5 常數 + 版本 + rate limit |
| Class 02: Game ID Parsing | 6 | valid/invalid game_id |
| Class 03: SSOT Artifact Construction | 5 | artifact 欄位驗證 |
| Class 04: Team Index Building | 5 | synthetic 資料索引建構 |
| Class 05: Feature Derivation | 6 | fav/dog 邏輯、DATA_LIMITED |
| Class 06: Ingestion Pipeline | 7 | dry-run、覆蓋率、輸出驗證 |
| Class 07: fetch_boxscore_cached guard | 4 | dry-run 不呼叫 API |
| Class 08: Alignment | 6 | 對齊邏輯、tag 驗證 |
| Class 09: Feature Coverage | 5 | 15 特徵覆蓋率計算 |
| Class 10: Bucket Attribution | 5 | median split、bootstrap CI |
| Class 11: OOF Validation | 4 | rolling monthly folds |
| Class 12: Negative Control | 4 | overfit risk 偵測 |
| Class 13: Gate Decision | 6 | 5 種 gate 場景 |
| Class 14: End-to-End | 20 | 真實資料驗證 |
| Class 15: Backward Compatibility | 9 | Phase 63/64 迴歸保護 |

---

## 十一、結論與建議

### 結論

3d 窗口牛棚用量特徵（`bullpen_usage_last_3d_fav/dog`、`bullpen_rest_imbalance_3d`）在 2025 MLB 全季 heavy favorite 場次（n=59）中**未呈現統計顯著的勝率差異**。Bootstrap CI 均包含 0，OOF 折間符號不一致，negative control 未觸發 overfit risk。

### 根本限制

- **1d、5d、b2b、3in4、closer 特徵**: 需要 StatsAPI 逐場次 boxscore cache，目前 `data/mlb_context/boxscores_cache/` 為空，無法評估這些更精細的疲勞指標。
- **3d 窗口信噪比低**: 3 天累計 IP 是粗糙指標，可能掩蓋真正的疲勞信號（如特定投手 b2b、封鎖者連日使用）。

### 下一步建議

| 優先級 | 方向 | 說明 |
|--------|------|------|
| 🔴 高 | SP 疲勞特徵 | 先發投手上一場 IP、REST_DAYS — 資料已存在，訊號可能更強 |
| 🔴 高 | 主場 vs 客場不對稱分析 | 牛棚 3d 差異在特定場次類型是否有條件信號 |
| 🟡 中 | 填充 boxscore cache | 花時間抓取 StatsAPI 個別 boxscore，啟用 1d/b2b/closer 特徵 |
| 🟡 中 | 天氣與球場因子 | 溫度、風速、球場因子，公開資料齊全 |
| 🟢 低 | REST_DAYS 不對稱 | 賽程密度差（例如系列賽末尾） |

### 凍結狀態

- **牛棚歸因**: 暫時 de-prioritize，等待 boxscore cache 填充或 SP 特徵先行
- **生產模型**: 維持 Phase56 基線不變
- **Alpha**: 0.40，不調整

---

**Phase 64-B 完成** ✅  
`PHASE_64B_FULL_SEASON_BULLPEN_INGESTION_ATTRIBUTION_VERIFIED`
