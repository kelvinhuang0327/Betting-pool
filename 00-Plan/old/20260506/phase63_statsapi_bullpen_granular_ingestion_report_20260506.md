# Phase 63 — StatsAPI-based Bullpen Granular Ingestion Implementation

**日期**: 2026-05-06  
**Gate**: `GRANULAR_INGESTION_READY`  
**Module**: `wbc_backend/features/mlb_bullpen_granular_ingestion.py` (Phase 63 additions)  
**Tests**: `tests/test_phase63_statsapi_bullpen_granular_ingestion.py` — 140/140 PASS  
**Runner**: `scripts/run_phase63_statsapi_bullpen_granular_ingestion.py`  
**Audit Hash**: `4923b662e37f0ca1`

---

## 1. Phase 59–62 結論摘要

| Phase | Gate | 結論 |
|-------|------|------|
| 59-Pre+ | `BULLPEN_HYPOTHESIS_RETAINED` | local isotonic / Platt 無法修復 heavy_favorite failure；牛棚假說維持 |
| 59 | `INCONCLUSIVE` | real boxscore coverage 足夠；簡單 fatigue delta 使 ECE 惡化 |
| 60 | `DIAGNOSTIC_ONLY_SIGNAL` | fav_vs_dog_delta_3d 方向性存在，但 bootstrap / OOF / negative control 不足 |
| 61 | `SOURCE_SELECTION_REQUIRED` | 12 個顆粒化特徵 SSOT 確立；per-pitcher 資料選源待定 |
| 62 | `STATSAPI_SELECTED` | StatsAPI boxscore 足以推導 10/12 特徵；LI 特徵維持 DATA_LIMITED |

**Phase 63 任務**：將 Phase 62 fixture proof 擴展為可執行的 ingestion implementation，產出 normalized relief appearance artifact 與 SSOT feature artifact，為 Phase 64 attribution 做準備。

---

## 2. Input Source / Fixture / Artifact 說明

### Input Source
- **選定**: MLB StatsAPI `/game/{gamePk}/boxscore`
- **端點**: `https://statsapi.mlb.com/api/v1/game/{gamePk}/boxscore`
- **Phase 63 驗證**: 完全 fixture-based（無 live API 呼叫）

### Fixture
- **檔案**: `tests/fixtures/phase62_boxscore_fixtures.json`
- **內容**: 5 個 scenario（4 個正常 + 1 個 null boxscore）

| Fixture ID | 日期 | 比賽 | 特殊場景 |
|-----------|------|------|---------|
| NORMAL_GAME_1 | 2025-05-01 | NYY(home) vs BOS(away) | 正常 SP + 牛棚 |
| NORMAL_GAME_2 | 2025-05-02 | NYY vs BOS | Holmes/Weaver B2B |
| NORMAL_GAME_3 | 2025-05-03 | NYY vs BOS | Weaver 第 3 連續日 (3-in-3) |
| OPENER_GAME | 2025-05-04 | HOU(home) vs TB(away) | Pressly opener (1.1 IP < 2.0) |
| MISSING_BOXSCORE | — | — | null boxscore → postponed |

### Diagnostic Artifacts (非 Production)
| Artifact | 路徑 | 記錄數 |
|---------|------|--------|
| Relief appearances JSONL | `reports/phase63_bullpen_relief_appearances_20260506.jsonl` | 26 |
| SSOT feature artifacts JSONL | `reports/phase63_bullpen_ssot_features_20260506.jsonl` | 4 |
| Diagnostic report JSON | `reports/phase63_statsapi_bullpen_granular_ingestion_20260506.json` | 1 |

---

## 3. Normalized Relief Appearance Schema

```python
@dataclass(frozen=True)
class NormalizedReliefAppearance:
    game_id: str               # 規格化 game_id
    game_date: str             # YYYY-MM-DD (完成比賽日期)
    team: str                  # Canonical team name
    opponent: str              # 對手 canonical name（Phase 63 新增）
    pitcher_id: int            # MLB player ID
    pitcher_name: str          # 顯示名稱
    appeared_order: int        # 1-indexed; 1 = 首位投手
    starter_flag: bool         # True iff order==1 AND IP >= 2.0
    opener_flag: bool          # True iff order==1 AND IP < 2.0
    reliever_flag: bool        # True iff NOT starter_flag（含 opener）
    innings_pitched: float     # 十進制 IP (6.1 → 6.333...)
    outs_recorded: int         # int(round(ip * 3))（避免 float drift）
    pitches_thrown: int | None # from numberOfPitches; None 若欄位缺失
    source: str                # "mlb_stats_api_boxscore"
    source_game_id: str        # 原始 game_pk 或 game_id
    audit_hash: str            # sha256[:12] of (game_id, pitcher_id, ip)
```

**IP 解析規則**:
- `"6.1"` → `6 + 1/3 = 6.333...` → `outs = int(round(6.333... * 3)) = 19`
- `"6.2"` → `6 + 2/3 = 6.666...` → `outs = int(round(6.666... * 3)) = 20`
- `None` / `""` → `0.0` → `outs = 0`

**Float Drift 防護**: 使用 `int(round(ip * 3))` 而非 `int(ip * 3)`，確保 `6 + 1/3 → 19`（而非 `18.9999... → 18`）。

---

## 4. SSOT Feature Artifact Schema

```python
@dataclass
class SSOTFeatureArtifact:
    prediction_game_id: str
    game_date: str               # 預測比賽日期 (YYYY-MM-DD)
    team: str

    # AVAILABLE 特徵 (10 個, StatsAPI boxscore 可推導)
    bullpen_usage_last_1d: float | None
    bullpen_usage_last_3d: float | None
    bullpen_usage_last_5d: float | None
    reliever_back_to_back_count: int
    reliever_three_in_four_days_count: int
    closer_used_last_1d: bool
    closer_used_last_2d: bool

    # DATA_LIMITED 特徵 (2 個) — 值永遠是 None，禁止 neutral fallback
    high_leverage_reliever_used_last_1d: None   # 需要 LI from PbP
    high_leverage_reliever_workload_last_3d: None  # 需要 LI from PbP

    # Metadata
    availability_map: dict[str, str]   # feature → "AVAILABLE" | "DATA_LIMITED"
    pit_window_map: dict[str, int]     # feature → window_days
    audit_hash: str
    module_version: str   # "phase63_bullpen_granular_ingestion_v2"
    diagnostic_only: bool  # 永遠 True
```

---

## 5. Coverage 結果

| 指標 | 結果 |
|------|------|
| Games parsed | 4 |
| Games missing (null boxscore) | 1 |
| Total pitcher appearances | 26 |
| Starters | 7 |
| Openers detected | 1 |
| Relievers | 19 |
| SSOT artifacts computed | 4 (NYY / BOS / HOU / TB) |
| Errors | 0 |

### SSOT Feature Coverage (prediction_date = 2025-05-05)

| Team | 1d IP | 3d IP | 5d IP | B2B | 3in4 | CL1d | CL2d |
|------|-------|-------|-------|-----|------|------|------|
| New York Yankees | None | 5.333 | 8.333 | 0 | 1 | N | Y |
| Boston Red Sox | None | 5.0 | 7.667 | 0 | 1 | N | Y |
| Houston Astros | 9.0 | 9.0 | 9.0 | 0 | 0 | Y | Y |
| Tampa Bay Rays | 3.0 | 3.0 | 3.0 | 0 | 0 | Y | Y |

**NYY/BOS `1d=None`**: 兩隊最後一場是 May 3；D-1 from May 5 = May 4（無比賽）→ 正確回傳 None。  
**HOU/TB `1d=9.0`**: May 4 為 opener game，所有投手（含 opener）均為 reliever_flag=True。  
**NYY 3in4=1**: Weaver (700003) 連續三天出賽 (May 1, 2, 3)，在 D-1..D-4 窗口中出現 3 次。

---

## 6. 10 個 AVAILABLE 特徵 + 2 個 DATA_LIMITED 特徵

### AVAILABLE (10 個 — StatsAPI boxscore 可推導)
| 特徵 | PIT 窗口 | 計算方式 |
|------|---------|---------|
| `bullpen_usage_last_1d` | 1d | D-1 所有 reliever IP 加總 |
| `bullpen_usage_last_3d` | 3d | D-1..D-3 reliever IP 加總 |
| `bullpen_usage_last_5d` | 5d | D-1..D-5 reliever IP 加總 |
| `reliever_back_to_back_count` | 2d | D-1 ∩ D-2 出場的 unique pitcher 數 |
| `reliever_three_in_four_days_count` | 4d | D-1..D-4 中出場 ≥ 3 次的 unique pitcher 數 |
| `closer_used_last_1d` | 1d | is_closer_candidate 在 D-1 出場 |
| `closer_used_last_2d` | 2d | is_closer_candidate 在 D-1 或 D-2 出場 |
| `bullpen_fatigue_favorite_side` | 3d | 從 3d usage 派生（已有資料）|
| `bullpen_fatigue_underdog_side` | 3d | 從 3d usage 派生（已有資料）|
| `bullpen_rest_imbalance` | 3d | \|home_3d - away_3d\|（已有資料）|

### DATA_LIMITED (2 個 — 需要 PbP Leverage Index)
| 特徵 | 原因 | 推遲至 |
|------|------|-------|
| `high_leverage_reliever_used_last_1d` | Boxscore 無 LI (leverage index) 欄位 | Phase 64 (PbP optional) |
| `high_leverage_reliever_workload_last_3d` | 需要 per-appearance LI | Phase 64 (PbP optional) |

> **嚴格規定**: DATA_LIMITED 特徵值必須為 `None`。禁止輸出 `0.0` 或任何中性填補值冒充可用資料。

---

## 7. PIT Safety Validation

**核心規則**: `entry_date (snapshot_date) < game_date (prediction_date)` 嚴格成立

```python
def assert_pit_safe(prediction_date: str, snapshot_date: str) -> None:
    if snapshot_date >= prediction_date:
        raise ValueError(f"PIT VIOLATION: ...")
```

**Window 計算**:
```python
cutoff_start = prediction_date - timedelta(days=window_days)
valid_range: cutoff_start <= game_date < prediction_date  # 嚴格 <
```

**測試驗證**:
- `test_bullpen_usage_1d_none_when_no_d1_game` ✅ — NYY 在 May 4 無比賽 → 1d = None
- `test_pit_safety_excludes_same_day` ✅ — 預測 May 1 時不使用 May 1 boxscore
- `test_doubleheader_d0_excluded_by_strict_lt` ✅ — D-0 同日資料嚴格排除

---

## 8. Edge Case Policies

### 雙重賽 (Doubleheader)
同日 Game 1 的 D-0 資料不進入 Game 2 的 window。`game_date < prediction_date` 嚴格不等式保證此特性。

### 延賽 (Postponed)
null boxscore → `games_missing++`，不產生任何 appearance record。SSOT window 函數自動回退至前幾日資料。

### 暫停賽 (Suspended)
與延賽相同處理 — 視為不完整 boxscore，不進行 ingestion，直到比賽正式標記完成。

### Opener
- 檢測條件: `appearance_order == 1` AND `innings_pitched < 2.0`（`OPENER_IP_THRESHOLD`）
- `opener_flag=True`, `reliever_flag=True`
- Opener IP **計入**牛棚使用量窗口（他們是 reliever，不是 starter）

### Bulk Pitcher
- `appearance_order >= 2`，IP 可能很大（如 4.2 IP）
- `reliever_flag=True`, `starter_flag=False`, `opener_flag=False`
- Bulk pitcher IP 計入牛棚使用量，與一般牛棚投手相同處理

---

## 9. 是否產生 Production Patch

| 安全常數 | 值 | 說明 |
|---------|----|----|
| `CANDIDATE_PATCH_CREATED` | `False` | 未建立任何 production candidate patch |
| `PRODUCTION_MODIFIED` | `False` | 未修改任何 production model / dataset |
| `ALPHA_MODIFIED` | `False` | market_blend α = 0.40 未改動 |
| `DIAGNOSTIC_ONLY` | `True` | 所有 artifacts 僅寫入 `reports/` |

Artifacts **不覆蓋** production dataset (`data/mlb_context/bullpen_usage_3d.jsonl`)。

---

## 10. Gate 結論與下一步

### Gate: `GRANULAR_INGESTION_READY`

**判定條件**:
- `ingestion_result.errors == []` ✅
- `len(normalized) > 0` (26 appearances) ✅
- `len(ssot_artifacts) > 0` (4 artifacts) ✅

**理由**:
- 完整的 per-pitcher relief appearance ingestion pipeline 已驗證（fixture-based）
- 4 teams × 7 SSOT features 全部正確計算，無缺漏
- DATA_LIMITED 特徵嚴格輸出 `None`，不含 neutral fallback
- PIT safety 全窗口通過
- 140/140 tests PASS（Phase 63 專屬），407+140=547 回歸測試全部通過

### Phase 64 可否進入 Attribution？

**是**。Gate `GRANULAR_INGESTION_READY` 確認：
1. `SSOTFeatureArtifact` 可作為 Phase 64 attribution 的輸入
2. 使用 `prediction_game_id` 與 `game_date` 連接 CLV / final odds 記錄
3. 限制分析範圍至 `prediction_date` 的比賽，不跨日滲透
4. `high_leverage_*` 特徵目前標記 `DATA_LIMITED`，Phase 64 可選擇性引入 PbP

### Phase 65+ 建議

1. **滾動資料收集**: 擴展 `_bullpen_from_schedule()` 儲存 per-pitcher 出賽記錄至 `data/mlb_context/bullpen_appearances.jsonl`
2. **LI 增補 (可選)**: 引入 `/game/{pk}/playByPlay` 為 `high_leverage_*` 提供 LI，DATA_LIMITED → AVAILABLE
3. **Phase 64 Attribution**: 以 `SSOTFeatureArtifact` 計算特徵 EV delta，對比 CLV 與 market close

---

**PHASE_63_STATSAPI_BULLPEN_GRANULAR_INGESTION_VERIFIED**
