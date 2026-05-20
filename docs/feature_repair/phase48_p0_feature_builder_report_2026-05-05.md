# Phase 48 — P0 Feature Builder Report

**報告日期**: 2026-05-05  
**Feature version**: `phase48_p0_v1`  
**上游 Phase**: Phase 47 (gate=`PROCEED_TO_FEATURE_PHASE`)  
**Hard rules**:
- `candidate_patch_created = False` ✅
- `production_modified = False` ✅
- alpha = 0.4（未調整）✅
- No external API / LLM calls ✅
- All features point-in-time safe ✅

---

## 一、已實作 Features

| Feature ID | 名稱 | 狀態 | 目標 Failure Segment |
|---|---|---|---|
| **F-001** | `sp_fip_delta` | ✅ 已實作（neutral fallback 模式） | `odds_bucket:heavy_favorite` |
| **F-002** | `park_run_factor` | ✅ 已實作（全量 lookup table） | `odds_bucket:heavy_favorite`, `disagreement:low` |
| **F-004** | `season_game_index` | ✅ 已實作（線性插值） | `month:2025-04` |

---

## 二、資料處理結果

| 指標 | 數值 |
|---|---|
| **input path** | `data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl` |
| **output path** | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase48_p0_v1.jsonl` |
| **rows_written** | 2,025 |
| **candidate_patch_created** | False |
| **production_modified** | False |

---

## 三、Feature 可用率 (Availability Rate)

| Feature | 可用筆數 | Fallback 筆數 | 可用率 |
|---|---|---|---|
| **park_run_factor** (F-002) | 2,025 | 0 | **100.0%** |
| **season_game_index** (F-004) | 2,025 | 0 | **100.0%** |
| **sp_fip_delta** (F-001) | 0 | 2,025 | **0.0%** |

### 說明

**F-001 sp_fip_delta — 0% 可用率（設計預期）**：

原始 `mlb_2025_per_game_predictions.jsonl` 僅儲存比賽結果與賠率，不含先發投手 FIP 資訊。F-001 設計為「context 注入」模式：
- 若 `context` 中提供 `home_sp_fip` 和 `away_sp_fip`（透過 StatsAPI 或 FanGraphs），功能完全運作。
- 若 context 為空（本次 batch run），安全回退至 `sp_fip_delta = 0.0`，`sp_fip_delta_available = False`。
- 這是 **正確行為**，非 bug。下一步需整合 pitcher FIP 資料管線（P1 任務）。

**F-002 park_run_factor — 100% 可用率**：

所有 30 支主場球隊均已建立 lookup table，無缺失。

**F-004 season_game_index — 100% 可用率**：

所有比賽日期格式 (`YYYY-MM-DD`) 均可正確解析，全部在 2025-04-27 至 2025-09-28 範圍內（均 > 0.0 且 < 1.0）。

---

## 四、Leakage Guard 摘要

| 項目 | 數值 |
|---|---|
| 觸發 leakage guard 的行數 | **2,025 / 2,025（100%）** |
| 被攔截的欄位 | `home_win`（每行皆含） |
| 攔截後對 feature 值的影響 | **無**（`home_win` 被完全剝離後再計算） |
| context 端的 forbidden 攔截 | 0 筆（無 context 注入） |

**關鍵驗證**：`home_win` 存在於每一筆輸入記錄中（Phase 39 schema 的 required field），leakage guard 正確識別並剔除，不影響三個特徵值（park_run_factor、season_game_index、sp_fip_delta 均與 home_win 無關）。

---

## 五、Feature 值分佈

### F-002 park_run_factor 分佈

| 球場環境 | 球隊數 | Factor 範圍 |
|---|---|---|
| 高得分（≥ 1.03） | 7 球隊 | 1.03–1.15 |
| 中性（0.98–1.02） | 14 球隊 | 0.98–1.02 |
| 低得分（≤ 0.97） | 9 球隊 | 0.94–0.97 |

最高：Colorado Rockies 1.15（Coors Field）  
最低：San Diego Padres 0.94（Petco Park）

### F-004 season_game_index 範圍

資料範圍 2025-04-27 → 2025-09-28，對應 index 值：

| 日期 | season_game_index |
|---|---|
| 2025-04-27（最早） | ~0.259 |
| 2025-06-15（中間） | ~0.491 |
| 2025-09-28（最晚） | ~0.981 |

---

## 六、輸出格式

每筆輸出行包含：

```json
{
  "schema_version": "phase39-v1",
  "game_date": "2025-04-27",
  "game_id": "...",
  "home_team": "New York Yankees",
  "home_win": 1,
  "model_home_prob": 0.6007,
  "market_home_prob_no_vig": 0.5991,
  "... (所有原始欄位) ...": "...",
  "p0_features": {
    "feature_version": "phase48_p0_v1",
    "candidate_patch_created": false,
    "production_modified": false,
    "sp_fip_delta": 0.0,
    "sp_fip_delta_available": false,
    "park_run_factor": 1.04,
    "park_factor_available": true,
    "season_game_index": 0.259345,
    "season_game_index_available": true,
    "feature_audit_hash": "...(64 hex chars)...",
    "audit_notes": {
      "ignored_forbidden_fields": ["home_win"],
      "sp_fip_source": "neutral_fallback",
      "park_factor_source": "lookup_table",
      "season_index_source": "computed"
    }
  },
  "feature_version": "phase48_p0_v1",
  "feature_audit_hash": "...(64 hex chars)..."
}
```

---

## 七、已知限制 (Known Limitations)

| 限制 | 影響 | 緩解措施 |
|---|---|---|
| `sp_fip_delta` 全 fallback | F-001 目前無法提供真實先發投手 FIP 差值 | 需整合 StatsAPI / FanGraphs pitcher FIP 資料管線（P1 任務） |
| `park_run_factor` 靜態 | 未反映天氣、球場臨時改建等動態因素 | 接受此限制；年度 park factor 已足夠穩定 |
| `season_game_index` 為全球時間線性插值 | 不反映各球隊實際出賽場次（強隊/弱隊賽程密度不同） | Phase 46 Blueprint F-004 原始設計即為此線性近似；更精確的「球隊層級場次計數」留作 P1 |
| Leakage guard 僅在 Phase 48 層 | 若未來資料管線繞過 `build_mlb_p0_features()`，保護失效 | 建議 Phase 49+ 加入全管線 leakage 單元測試 |

---

## 八、測試覆蓋

```
tests/test_phase48_p0_feature_builder.py::TestHardRuleInvariants      6/6   ✅
tests/test_phase48_p0_feature_builder.py::TestParkRunFactor           11/11  ✅
tests/test_phase48_p0_feature_builder.py::TestSeasonGameIndex         11/11  ✅
tests/test_phase48_p0_feature_builder.py::TestSPFipDelta               9/9   ✅
tests/test_phase48_p0_feature_builder.py::TestLeakageGuard             7/7   ✅
tests/test_phase48_p0_feature_builder.py::TestAuditHash                6/6   ✅
tests/test_phase48_p0_feature_builder.py::TestBuildMlbP0Features      10/10  ✅
tests/test_phase48_p0_feature_builder.py::TestScriptIntegration        7/7   ✅
──────────────────────────────────────────────────────────────────────────────
TOTAL: 67/67 passed in 0.09s
```

---

## 九、下一步建議

### 立即 (Phase 49)：以 phase48 JSONL 重新執行 Phase 43/44/45

```bash
# 以 phase48 enriched JSONL 重新執行 Phase 45 attribution
python -c "
import json
from wbc_backend.evaluation.prediction_persistence import PredictionRow
from orchestrator.phase45_model_value_attribution import run_phase45_attribution

rows = []
with open('data/mlb_2025/derived/mlb_2025_per_game_predictions_phase48_p0_v1.jsonl') as f:
    for line in f:
        d = json.loads(line)
        rows.append(PredictionRow(**{k: d[k] for k in PredictionRow.__dataclass_fields__}))
result = run_phase45_attribution(rows)
print('gate:', result.gate, 'bss:', result.global_bss)
"
```

**預期**: 若 `park_run_factor` 和 `season_game_index` 作為分層變量，`month:2025-04` segment 的 BSS 應從 −2.50% 改善；`odds_bucket:heavy_favorite` segment 的 ECE 應從 0.0893 下降。

### P1：整合先發投手 FIP 資料
- 目標：讓 `sp_fip_delta_available` 從 0% → 接近 100%
- 方式：從 `data/wbc_pitching_stats_2026.json` 或 `data/mlb_2025/` 下的投手資料，建立 `game_id → (home_sp_fip, away_sp_fip)` 的 lookup

### P1：F-003 Bullpen Fatigue Index
- 依 Phase 46 Blueprint，F-003 對 month:2025-06 ECE 的改善潛力最大（−30%）

---

## 十、不變量驗證

| 規則 | 狀態 |
|---|---|
| `CANDIDATE_PATCH_CREATED = False` | ✅ 模組常數 + script 返回值 + 每行輸出 |
| `PRODUCTION_MODIFIED = False` | ✅ 同上 |
| alpha = 0.4（未調整） | ✅ Phase 48 不涉及 alpha |
| 無外部 API / LLM 呼叫 | ✅ 純離線計算 |
| Point-in-time safety | ✅ park_run_factor 使用前年資料；season_game_index 只用 game_date；sp_fip_delta 設計為「開賽前已知投手 FIP」|
| Leakage guard | ✅ 2,025/2,025 行正確攔截 `home_win`，不影響任何 feature 值 |

---

## 十一、驗證標記

```
PHASE_48_P0_FEATURE_BUILDER_VERIFIED
feature_version=phase48_p0_v1
rows_written=2025
park_availability_rate=100.0%
season_idx_availability_rate=100.0%
sp_fip_availability_rate=0.0% (neutral fallback, by design — no pitcher context injected)
forbidden_fields_triggered=2025/2025 (home_win correctly intercepted, zero feature impact)
tests=67/67
candidate_patch_created=False
production_modified=False
```
