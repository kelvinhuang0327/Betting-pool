# Phase 61 — Bullpen Granular Data Acquisition Blueprint & SSOT Guard

**日期**: 2026-05-06  
**版本**: `phase61_bullpen_granular_ssot_v1`  
**Gate 結論**: `SOURCE_SELECTION_REQUIRED`  
**Safety**: `CANDIDATE_PATCH_CREATED=False` | `PRODUCTION_MODIFIED=False` | `ALPHA_MODIFIED=False` | `DIAGNOSTIC_ONLY=True`

---

## Section 1 — Phase 59 / Phase 60 結論摘要

### Phase 59 (Real Bullpen Boxscore Acquisition)
- **Gate**: `INCONCLUSIVE`
- **核心發現**: 從 MLB StatsAPI boxscore 取得的 3 日滾動牛棚 IP 資料 (coverage ≈ 96.5%)，統計上未能拒絕虛無假說。樣本量與信號強度均不足以進入生產。

### Phase 60 (Bullpen Feature Decomposition)
- **Gate**: `DIAGNOSTIC_ONLY_SIGNAL`
- **資料規模**: n_predictions=2,025、n_bullpen_rows=2,430、n_aligned=1,890 (alignment_rate=93.3%)
- **Available 特徵**: 7 個（全屬 3 日 aggregate 衍生）
- **DATA_LIMITED 特徵**: 4 個（1d、5d、B2B proxy、closer/high-leverage）
- **重型最愛 (heavy_fav) 區段**: n=60；fav_vs_dog_delta_3d bootstrap 未達顯著 (null_rejected=False)
- **OOF 驗證**: oof_mean_delta=−0.2075，跨 3 fold 符號不一致（n_fold_sizes=[24, 8, 2]）→ 訓練集上方向性信號存在，但 OOF 過小，判斷為雜訊
- **負控制**: real_delta=+0.0264、shuffled_mean=−0.0122、null_rejected=False
- **整體結論**: 3 日 aggregate 資料已達研究性上限；需要粒度更細的資料（1d、5d、逐投手）才能進一步驗證假說

---

## Section 2 — 現有 Bullpen Artifacts 盤點

### 資料檔案
| 路徑 | 說明 | 狀態 |
|------|------|------|
| `data/mlb_context/bullpen_usage_3d.jsonl` | 主要牛棚資料，2,430 筆，3 日 aggregate IP | ✅ 存在 |
| `data/mlb_context/injury_rest.jsonl` | 球員休息資料 | ✅ 存在 |

### Python 模組
| 路徑 | 功能 | Phase |
|------|------|-------|
| `data/mlb_bullpen_usage_loader.py` | Schedule proxy fallback loader | Phase 58 |
| `wbc_backend/features/mlb_bullpen_feature_builder.py` | 5 種牛棚 proxy 特徵建構 | Phase 56 |
| `wbc_backend/features/mlb_bullpen_feature_injection.py` | 特徵注入管線 | Phase 56 |
| `wbc_backend/features/mlb_bullpen_pit_validator.py` | PIT 安全驗證器 | Phase 56 |
| `wbc_backend/features/mlb_bullpen_usage_snapshot.py` | 滾動快照建構 | Phase 58 |
| `wbc_backend/features/mlb_relief_appearance_parser.py` | Relief appearance 解析 (Tier2 schedule proxy) | Phase 58 |
| `wbc_backend/mlb_data/external_sources.py` | MLB StatsAPI boxscore 3d 聚合擷取 | Phase 58 |
| `wbc_backend/features/mlb_bullpen_granular_ssot.py` | **SSOT (本 Phase 新增)** — 所有粒度特徵的唯一來源 | Phase 61 |

### Orchestrator 模組
| 路徑 | Gate |
|------|------|
| `orchestrator/phase55_sp_vs_bullpen_diagnosis.py` | — |
| `orchestrator/phase56_bullpen_feature_evaluation.py` | — |
| `orchestrator/phase58_bullpen_usage_evaluation.py` | — |
| `orchestrator/phase59_real_bullpen_boxscore_acquisition.py` | `INCONCLUSIVE` |
| `orchestrator/phase60_bullpen_feature_decomposition.py` | `DIAGNOSTIC_ONLY_SIGNAL` |

---

## Section 3 — 現有資料缺口

### 缺口 A — 時間粒度不足

| 所需特徵 | 現況 | 缺口說明 |
|----------|------|----------|
| `bullpen_usage_last_1d` | DATA_LIMITED | `bullpen_usage_3d.jsonl` 只儲存 3 日 aggregate，無法還原單日 |
| `bullpen_usage_last_5d` | DATA_LIMITED | 現有 API 呼叫只拉取 D-1、D-2、D-3，未拉取 D-4、D-5 |

### 缺口 B — 投手粒度不足（僅有球隊層級）

| 所需特徵 | 現況 | 缺口說明 |
|----------|------|----------|
| `reliever_back_to_back_count` | DATA_LIMITED | 需要 per-pitcher per-game 出賽記錄；現有來源只有球隊 IP 總和 |
| `reliever_three_in_four_days_count` | DATA_LIMITED | 同上；需要 4 天滾動窗口的投手出賽頻次 |
| `closer_used_last_1d` | DATA_LIMITED | 需要 Closer role 分類；現有 boxscore 不提供 role/leverage 標籤 |
| `closer_used_last_2d` | DATA_LIMITED | 同上 |

### 缺口 C — 槓桿指數 (Leverage Index) 不足

| 所需特徵 | 現況 | 缺口說明 |
|----------|------|----------|
| `high_leverage_reliever_used_last_1d` | DATA_LIMITED | 需要 play-by-play LI 資料，boxscore summary 無 LI 欄位 |
| `high_leverage_reliever_workload_last_3d` | DATA_LIMITED | 同上；LI > 1.5 的投手 IP 累計需 PbP 層級資料 |

### 現有 API 來源侷限
`mlb_stats_api_boxscore` (`/game/{gamePk}/boxscore`) 在目前呼叫邏輯中：
- 排除 pitchers[0]（推定先發）以估算牛棚 IP
- 只計算 D-1、D-2、D-3 三天加總
- 無 role/leverage 欄位
- 無每投手跨日歷史

---

## Section 4 — Granular Bullpen SSOT Schema

所有特徵的唯一來源：`wbc_backend.features.mlb_bullpen_granular_ssot`

```
SSOT_SCHEMA_VERSION = "phase61_bullpen_granular_ssot_v1"
```

### 12 個核心特徵定義

| 特徵名稱 | 視窗 | 當前可用性 | 資料來源 |
|----------|------|------------|----------|
| `bullpen_usage_last_1d` | D-1 | DATA_LIMITED | mlb_stats_api_boxscore (per-day) |
| `bullpen_usage_last_3d` | D-1~D-3 | **AVAILABLE** | mlb_stats_api_boxscore ✅ |
| `bullpen_usage_last_5d` | D-1~D-5 | DATA_LIMITED | mlb_stats_api_boxscore (extended) |
| `reliever_back_to_back_count` | D-1~D-2 | DATA_LIMITED | mlb_stats_api per-pitcher log |
| `reliever_three_in_four_days_count` | D-1~D-4 | DATA_LIMITED | mlb_stats_api per-pitcher log |
| `closer_used_last_1d` | D-1 | DATA_LIMITED | boxscore + closer role table |
| `closer_used_last_2d` | D-1~D-2 | DATA_LIMITED | boxscore + closer role table |
| `high_leverage_reliever_used_last_1d` | D-1 | DATA_LIMITED | play-by-play + LI |
| `high_leverage_reliever_workload_last_3d` | D-1~D-3 | DATA_LIMITED | play-by-play + LI |
| `bullpen_fatigue_favorite_side` | D-1~D-3 | **AVAILABLE** (derived) | bullpen_usage_last_3d + blend_prob |
| `bullpen_fatigue_underdog_side` | D-1~D-3 | **AVAILABLE** (derived) | bullpen_usage_last_3d + blend_prob |
| `bullpen_rest_imbalance` | D-1~D-3 | **AVAILABLE** (derived) | \|home_3d − away_3d\| |

### BullpenGranularRecord 結構

```python
@dataclass
class GranularFeatureSlot:
    feature_name: str
    value: float | None          # None if DATA_LIMITED or MISSING
    availability: FeatureAvailability  # AVAILABLE / DATA_LIMITED / MISSING / PIT_VIOLATION
    data_limited_reason: str | None
    pit_window_days: int
    pit_snapshot_date: str | None  # YYYY-MM-DD, must be < game_date

@dataclass
class BullpenGranularRecord:
    ssot_schema_version: str
    game_id: str
    game_date: str
    team: str
    side: str   # "home" or "away"
    candidate_patch_created: bool   # always False
    production_modified: bool       # always False
    diagnostic_only: bool           # always True
    bullpen_usage_last_3d: GranularFeatureSlot        # AVAILABLE
    bullpen_usage_last_1d: GranularFeatureSlot        # DATA_LIMITED
    bullpen_usage_last_5d: GranularFeatureSlot        # DATA_LIMITED
    reliever_back_to_back_count: GranularFeatureSlot  # DATA_LIMITED
    reliever_three_in_four_days_count: GranularFeatureSlot  # DATA_LIMITED
    closer_used_last_1d: GranularFeatureSlot          # DATA_LIMITED
    closer_used_last_2d: GranularFeatureSlot          # DATA_LIMITED
    high_leverage_reliever_used_last_1d: GranularFeatureSlot   # DATA_LIMITED
    high_leverage_reliever_workload_last_3d: GranularFeatureSlot  # DATA_LIMITED
    bullpen_fatigue_favorite_side: GranularFeatureSlot   # AVAILABLE (derived)
    bullpen_fatigue_underdog_side: GranularFeatureSlot   # AVAILABLE (derived)
    bullpen_rest_imbalance: GranularFeatureSlot          # AVAILABLE (derived)
    source: str
    pit_safe: bool
    audit_hash: str
```

---

## Section 5 — 每個特徵的 PIT-safe 定義

核心規則：`snapshot_date 必須嚴格 < game_date`。game_date = D 當天的比賽只能使用 D-1 或更早的歷史資料。

| 特徵 | PIT 視窗 | Snapshot 最晚日期 | 違規範例 |
|------|----------|-------------------|---------|
| `bullpen_usage_last_1d` | D-1 | D-1 | 使用 D 當日 boxscore |
| `bullpen_usage_last_3d` | D-1, D-2, D-3 | D-1 | 加入 D 當日任何 IP |
| `bullpen_usage_last_5d` | D-1~D-5 | D-1 | 加入 D 當日任何 IP |
| `reliever_back_to_back_count` | D-1, D-2 | D-1 | 使用 D 當日出賽記錄 |
| `reliever_three_in_four_days_count` | D-1~D-4 | D-1 | 使用 D 當日出賽記錄 |
| `closer_used_last_1d` | D-1 | D-1 | 使用 D 當日 closer 出賽 |
| `closer_used_last_2d` | D-1, D-2 | D-1 | 使用 D 當日 closer 出賽 |
| `high_leverage_reliever_used_last_1d` | D-1 | D-1 | 使用 D 當日 LI 事件 |
| `high_leverage_reliever_workload_last_3d` | D-1~D-3 | D-1 | 使用 D 當日 LI 事件 |
| `bullpen_fatigue_favorite_side` | D-1~D-3 (derived) | D-1 | 同 bullpen_usage_last_3d |
| `bullpen_fatigue_underdog_side` | D-1~D-3 (derived) | D-1 | 同 bullpen_usage_last_3d |
| `bullpen_rest_imbalance` | D-1~D-3 (derived) | D-1 | 同 bullpen_usage_last_3d |

### 雙重賽特殊規定
雙重賽同日期 Game 1 的結果，對 Game 2 而言屬於**當日資料 (D-0)**，不得作為 D-1 特徵使用。
詳見 Section 7。

---

## Section 6 — 採集 / 擷取 Blueprint

### Tier 1 — 擴展現有 3d 視窗（建議首先執行）

**目標**：取得 1d 和 5d 兩個滾動窗口

**實作路徑**：
修改 `wbc_backend/mlb_data/external_sources.py` 中的 `_bullpen_from_schedule()` 函數：
```python
# 目前：
recent = [(d - timedelta(days=i)).isoformat() for i in (1, 2, 3)]

# 擴展為：
recent_1d = [(d - timedelta(days=i)).isoformat() for i in (1,)]
recent_3d = [(d - timedelta(days=i)).isoformat() for i in (1, 2, 3)]
recent_5d = [(d - timedelta(days=i)).isoformat() for i in (1, 2, 3, 4, 5)]
```

輸出欄位新增到 `bullpen_usage_3d.jsonl`（或另存 `bullpen_usage_granular.jsonl`）：
```json
{
  "bullpen_usage_last_1d_home": 2.333,
  "bullpen_usage_last_1d_away": 1.0,
  "bullpen_usage_last_3d_home": 6.667,
  "bullpen_usage_last_3d_away": 4.333,
  "bullpen_usage_last_5d_home": 9.0,
  "bullpen_usage_last_5d_away": 7.333
}
```

**前提條件**：MLB StatsAPI 需能取得 D-4、D-5 的 boxscore（通常可用，但需驗證 API 速率限制）

### Tier 2 — 逐投手出賽記錄（需確認資料來源）

**目標**：取得 `reliever_back_to_back_count`、`reliever_three_in_four_days_count`

**候選來源**：
| 來源 | API | 覆蓋率 | 成本 |
|------|-----|--------|------|
| MLB StatsAPI `/game/{pk}/boxscore` | pitchers 陣列（現有） | 高 | 低 |
| MLB StatsAPI `/game/{pk}/pitchingLines` | 更細粒度但需驗證 | 未知 | 低 |
| Baseball Reference Play Index | 歷史資料完整 | 高 | 中（需爬蟲） |
| Statcast (Baseball Savant) | 最細粒度，含 LI | 高 | 中 |
| FanGraphs Splits | 含出賽紀錄 | 高 | 中（需爬蟲） |

**Phase 62 必須執行來源評估**（見 Section 10）

### Tier 3 — Leverage Index（需 play-by-play）

**目標**：取得 `closer_used_last_Nd`、`high_leverage_reliever_*`

**所需資料**：play-by-play 事件流，含 `leverageIndex` 欄位

**候選來源**：
- MLB StatsAPI `/game/{pk}/playByPlay`（現有 API，已知可用）
- Statcast Baseball Savant（含 LI，但需 Python 擷取套件如 `pybaseball`）

**PIT 注意事項**：play-by-play 資料只能使用完整比賽（非當日進行中的比賽）

---

## Section 7 — 特殊比賽處理規則

### 7.1 雙重賽 (Doubleheader)

```
策略：PIT 視窗錨定於 game_date，不論場次順序

Game 1 (D)：可使用 D-1 及更早的牛棚歷史
Game 2 (D)：同樣只能使用 D-1 及更早的牛棚歷史
             → Game 1 在 D 的牛棚使用屬「同日資料 (D-0)」，禁止用於 Game 2 的特徵計算

實作：
  - bullpen_usage_last_1d 計算時，若 boxscore 日期 = game_date，則排除
  - 即使 Game 1 已完成，也不得將 Game 1 的 IP 納入 Game 2 的 bullpen_usage_last_1d
```

### 7.2 延賽 / 停賽補賽 (Postponed / Suspended)

```
策略：PIT 視窗以實際開賽日期為準

補賽日期 = D_reschedule：
  - 使用 D_reschedule - 1 及更早的牛棚歷史
  - 原定日期的任何資料均不適用（原定日期的比賽未實際開始）
```

### 7.3 開場投手 / 大量投手 (Opener / Bulk Pitcher)

```
策略：依 IP 閾值判斷 reliever vs starter

Opener 定義：
  - pitchers[0] 的 IP < 2.0 → 視為 reliever，IP 計入牛棚負荷
  - 通常情況：pitchers[0] IP >= 5.0 → 視為先發，從牛棚 IP 排除

Bulk Pitcher 定義：
  - 在 opener 之後登場
  - 若在第 3 局結束前進場 → 視為 reliever（IP 計入牛棚）
  - 若在第 4 局或之後進場 → 視為先發替代（IP 排除）

實作注意：
  - 現有 _bullpen_from_schedule() 中的 pitchers[0] 排除邏輯，
    在 opener 格式比賽中可能導致 opener 的 IP 被誤排除
  - Phase 62 擷取器必須根據 IP 閾值動態判斷，而非固定排除 pitchers[0]
```

### 7.4 雨延 / 中途停賽後復賽 (Suspension)

```
策略：IP 依實際投球日期分配

原始日期 D_original：記錄 D_original 投球的所有 IP
復賽日期 D_resume：記錄 D_resume 投球的所有 IP

使用 D_after_resume 日期比賽的特徵：
  - 兩段投球記錄均在各自日期的歷史中
  - 只要各段日期 < D_after_resume，均可安全使用
```

### 7.5 缺少 Boxscore 的比賽

```
策略：輸出 MISSING，不使用 neutral fallback

若某比賽日期的 boxscore 無法取得：
  - bullpen_usage_last_Nd 輸出 availability=MISSING，value=None
  - 下游消費者必須顯式處理 MISSING（不可假定為 0 IP）

禁止：以 0.0 或聯盟平均 (4.10 ERA proxy) 填充 MISSING 記錄
```

---

## Section 8 — DATA_LIMITED 處理政策

### 核心原則：禁止中性值偽裝 (No Neutral Fallback Masquerade)

當特徵無法從當前資料來源計算時：

```
✅ 正確處理：
  availability = FeatureAvailability.DATA_LIMITED
  value = None
  data_limited_reason = "..."（必須填寫）

❌ 禁止：
  value = 0.0    → 偽裝成「沒有疲勞」
  value = 0.5    → 偽裝成「中性機率」
  value = 1.0    → 偽裝成「假設某個水準」
```

### 驗證機制

`BullpenGranularRecord.validate()` 在建構時自動執行：
- 若 `availability in (DATA_LIMITED, MISSING)` 且 `value is not None` → 拋出 ValueError
- 訊息包含 `SSOT-MASQUERADE` 標識

### 下游消費政策

任何使用 bullpen 特徵的下游模型（Phase 62+）必須：
1. 先讀取 `availability` 欄位，再讀取 `value`
2. 若 availability = DATA_LIMITED → 跳過該特徵，不填入模型
3. 若 availability = MISSING → 視為有效缺失，可考慮 imputation（需記錄）

---

## Section 9 — SSOT Guard 政策

### 單一來源規則

所有 bullpen 特徵**必須且只能**從 `wbc_backend.features.mlb_bullpen_granular_ssot` 產生。

```python
# SSOT 所有權登錄表 (_SSOT_REGISTERED_MODULES)
{
    "bullpen_usage_last_3d": "wbc_backend.features.mlb_bullpen_granular_ssot",
    "bullpen_usage_last_1d": "wbc_backend.features.mlb_bullpen_granular_ssot",
    "bullpen_usage_last_5d": "wbc_backend.features.mlb_bullpen_granular_ssot",
    "reliever_back_to_back_count": "wbc_backend.features.mlb_bullpen_granular_ssot",
    ...（共 14 項）
}
```

### Guard 使用方式

```python
from wbc_backend.features.mlb_bullpen_granular_ssot import assert_ssot_ownership

# 在任何試圖計算 bullpen 特徵的模組頂部呼叫：
assert_ssot_ownership("bullpen_usage_last_3d", __name__)
# → 若 __name__ 不是 SSOT 模組，立即拋出 ValueError
```

### Legacy 特徵遷移清單

以下 Phase 56/58 特徵已登錄到 SSOT，Phase 62 起必須從 SSOT 讀取，不得在各自 Phase 的 orchestrator 中獨立計算：

| Legacy 特徵 | 來源模組 | 遷移狀態 |
|------------|---------|---------|
| `bullpen_fatigue_3d` | `mlb_bullpen_feature_builder` | ⚠️ 需遷移 |
| `bullpen_fatigue_7d` | `mlb_bullpen_feature_builder` | ⚠️ 需遷移 |
| `reliever_back_to_back_count` | `mlb_bullpen_feature_builder` (proxy) | ⚠️ 需遷移 |
| `bullpen_recent_era_proxy` | `mlb_bullpen_feature_builder` | 不在 SSOT 範圍（ERA 非本期目標） |
| `late_game_leverage_usage_proxy` | `mlb_bullpen_feature_builder` | ⚠️ 需遷移（high_leverage 系列） |

---

## Section 10 — 下一步建議

### Gate 結論：`SOURCE_SELECTION_REQUIRED`

理由：
1. **1d、5d 特徵**：mlb_stats_api_boxscore 已有 per-day IP，只需擴展現有 API 呼叫的日期視窗（D-4、D-5）即可取得，不需要新來源
2. **per-pitcher 出賽記錄**：需確認 MLB StatsAPI `/game/{pk}/boxscore` 的 `pitchers` 陣列是否足以計算 B2B，或需要 `/pitchingLines` endpoint
3. **Leverage Index**：需確認 `/game/{pk}/playByPlay` 的可用性，或採用 Statcast pybaseball 套件
4. **在決定來源之前，不應開始實作擷取器**

### Phase 62 任務清單（前提：完成來源評估）

**選項 A — 僅擴展 3d 視窗（最低風險）**：
- 修改 `_bullpen_from_schedule()` 納入 D-4、D-5
- 輸出 `bullpen_usage_1d / 5d` 到 `bullpen_usage_granular.jsonl`
- 預期 gate：`GRANULAR_ACQUISITION_PARTIAL_SUCCESS`

**選項 B — 加入 per-pitcher 出賽記錄（中風險）**：
- 確認 `pitchers` 陣列含跨日 ID 一致性
- 建立 per-pitcher 歷史記錄 store（JSONL 或 SQLite）
- 計算 B2B、3-in-4 計數
- 預期 gate：`GRANULAR_ACQUISITION_RELIEVER_LEVEL`

**選項 C — 加入 Leverage Index（高風險）**：
- 評估 MLB StatsAPI play-by-play 的 `leverageIndex` 欄位品質
- 備選：使用 `pybaseball` Statcast 資料
- 計算 closer 使用 / high-leverage workload
- 預期 gate：`GRANULAR_ACQUISITION_LEVERAGE_LEVEL`

### 建議執行順序

```
Phase 62A → 擴展 1d/5d 視窗（Tier 1，最快可驗證）
Phase 62B → 評估 per-pitcher B2B（Tier 2，需 API 驗證）
Phase 62C → 評估 LI 來源（Tier 3，最高成本）
```

每個 Phase 62 子任務均需：
- 通過 103 項 Phase 61 SSOT 測試（無回歸）
- 自身測試 >= 40 項
- 更新 SSOT 的 `available_in_current_data` 標記
- 輸出獨立 gate 報告

---

<!-- PHASE_61_BULLPEN_GRANULAR_DATA_SSOT_BLUEPRINT_VERIFIED -->
