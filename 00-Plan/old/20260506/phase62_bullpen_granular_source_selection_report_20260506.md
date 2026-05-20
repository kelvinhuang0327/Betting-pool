# Phase 62 — Bullpen Granular Source Selection and Minimal PIT-safe Ingestion Proof

**日期**: 2026-05-06  
**Gate**: `STATSAPI_SELECTED`  
**Module**: `wbc_backend/features/mlb_bullpen_granular_ingestion.py`  
**Tests**: `tests/test_phase62_bullpen_granular_source_selection.py` — 123/123 PASS  
**Audit Hash**: `1af7e7a80df3e626`

---

## 1. Phase 59–61 結論摘要

| Phase | Gate | 結論 |
|-------|------|------|
| 59-Pre+ | `BULLPEN_HYPOTHESIS_RETAINED` | 3d-window 牛棚使用量具有統計方向性，足以支撐後續深挖 |
| 59 | `INCONCLUSIVE` | 真實 boxscore 牛棚 IP 數據不足以獨立顯著，但訊號未被排除 |
| 60 | `DIAGNOSTIC_ONLY_SIGNAL` | 特徵分解顯示部份條件性訊號 (n=60 重疊投注, p>0.05)，無法驅動 production patch |
| 61 | `SOURCE_SELECTION_REQUIRED` | SSOT 架構確立：12 個顆粒化特徵已定義，10 個需要每場比賽每位投手的出賽紀錄 |

**Phase 62 任務**：選定最小可行資料源，以 fixture 驗證 PIT-safe ingestion，確認哪些特徵可從 AVAILABLE 升級。

---

## 2. 現有資料源盤點

### 現有已整合 (Phase 58/59)
| 資料集 | 路徑 | 記錄數 | 覆蓋率 |
|--------|------|--------|--------|
| `bullpen_usage_3d.jsonl` | `data/mlb_context/` | 2,430 | ~96.5% |
| `lineups.jsonl` | `data/mlb_context/` | — | — |
| `injury_rest.jsonl` | `data/mlb_context/` | — | — |

**現有格式** (`bullpen_usage_3d.jsonl`)：
```json
{
  "game_id": "MLB-2025_03_18-...",
  "bullpen_usage_last_3d_home": 11.667,
  "bullpen_usage_last_3d_away": 10.667,
  "fetched_at": "2026-03-18T17:56:56Z",
  "source": "mlb_stats_api_boxscore"
}
```

**現有格式的限制**：僅有「三日合計 IP」，無每位投手、每日的個別出賽記錄。

### 未整合來源
- **MLB StatsAPI Play-by-Play** (`/game/{pk}/playByPlay`)：有 leverage index，但未整合  
- **Statcast / Baseball Savant**：需 `pybaseball` 套件，未安裝  
- **Retrosheet GL2025** (`data/mlb_2025/gl2025.txt`)：有勝投/敗投/救援投手，但無每位牛棚投手出賽細節

---

## 3. MLB StatsAPI vs Statcast/PbP 比較表

| 特徵 | StatsAPI Boxscore | Statcast/PbP |
|------|:-----------------:|:------------:|
| `bullpen_usage_last_1d` | ✅ AVAILABLE | ✅ AVAILABLE |
| `bullpen_usage_last_3d` | ✅ AVAILABLE | ✅ AVAILABLE |
| `bullpen_usage_last_5d` | ✅ AVAILABLE | ✅ AVAILABLE |
| `reliever_back_to_back_count` | ✅ AVAILABLE | ✅ AVAILABLE |
| `reliever_three_in_four_days_count` | ✅ AVAILABLE | ✅ AVAILABLE |
| `closer_used_last_1d` | ✅ AVAILABLE (heuristic) | ✅ AVAILABLE |
| `closer_used_last_2d` | ✅ AVAILABLE (heuristic) | ✅ AVAILABLE |
| `bullpen_fatigue_favorite_side` | ✅ AVAILABLE | ✅ AVAILABLE |
| `bullpen_fatigue_underdog_side` | ✅ AVAILABLE | ✅ AVAILABLE |
| `bullpen_rest_imbalance` | ✅ AVAILABLE | ✅ AVAILABLE |
| `high_leverage_reliever_used_last_1d` | ⚠️ DATA_LIMITED (no LI) | ✅ AVAILABLE |
| `high_leverage_reliever_workload_last_3d` | ⚠️ DATA_LIMITED (no LI) | ✅ AVAILABLE |

**StatsAPI Boxscore 優勢**：
- 已整合於 `wbc_backend/mlb_data/external_sources.py`
- 費率管控已建立（Phase 58/59 生產驗證）
- 延伸 1d/5d 窗口只需調整 `timedelta` 範圍
- per-pitcher IP 資料已在 `players` dict 中 (`teams.{side}.players.ID{pid}.stats.pitching.inningsPitched`)

**Statcast/PbP 優勢**：
- 提供 leverage index (LI) → 可派生 `high_leverage_*` 特徵
- 角色確認 (closer designation)

**選擇理由**：Phase 62 的 gate 是「可行性選擇」，非「最大特徵集」。Boxscore 已覆蓋 10/12 特徵，LI 特徵維持 DATA_LIMITED 並推遲至 Phase 63。

---

## 4. 選定資料源：MLB StatsAPI Boxscore

**選定**: `mlb_stats_api_boxscore` (現有整合擴展)  
**端點**: `https://statsapi.mlb.com/api/v1/game/{gamePk}/boxscore`  
**理由**: 
1. 已整合於 `external_sources.py`，`_bullpen_from_schedule()` 已驗證解析正確性
2. 每位投手出賽紀錄完整（出場順序、IP）
3. 不需新增 API 依賴或外部套件
4. Rate limit 預算已在 Phase 58/59 實測

---

## 5. 最小 Ingestion 驗證結果

**Fixture 來源**: `tests/fixtures/phase62_boxscore_fixtures.json`  
**測試方式**: 5 個 fixture（4 個正常 + 1 個 null boxscore）

| 指標 | 結果 |
|------|------|
| Games parsed | 4 |
| Games missing (null boxscore) | 1 |
| Total pitcher appearances | 26 |
| Starters classified | 7 |
| Openers detected (IP < 2.0) | 1 |
| Relievers | 19 |
| Closer candidates | 8 |
| Errors | 0 |
| Audit hash | `1af7e7a80df3e626` |

**多日序列測試** (B2B / 3-in-4):
- Luke Weaver (ID 700003) 連續三日出賽 (May-01, May-02, May-03) → `reliever_three_in_four_days_count >= 1` ✅
- Clay Holmes (700002) + Luke Weaver (700003) 連續兩日 → `reliever_back_to_back_count >= 2` ✅

---

## 6. 標準化 Relief Appearance Schema

```python
@dataclass(frozen=True)
class ReliefAppearanceRecord:
    game_id: str               # 規格化 game_id (e.g., MLB-2025_05_01-...)
    game_date: str             # YYYY-MM-DD (完成比賽日期)
    team: str                  # Canonical team name
    side: str                  # "home" | "away"
    pitcher_id: int            # MLB player ID
    pitcher_name: str          # 顯示名稱
    appearance_order: int      # 1 = 首位投手, 2+ = 牛棚投手
    innings_pitched: float     # 十進制 IP (6.1 → 6.333)
    is_starter: bool           # appearance_order=1 且 IP >= 2.0
    is_opener: bool            # appearance_order=1 且 IP < 2.0
    is_reliever: bool          # NOT is_starter (包含 opener 場景)
    is_closer_candidate: bool  # 最後一位出場的牛棚投手
    source: str                # "mlb_stats_api_boxscore"
    pit_safe: bool             # 永遠 True (函數只接受已完成比賽)
```

**IP 解析規則**:
- `"6.1"` → `6.333` (1 out = 1/3 inning)
- `"6.2"` → `6.667` (2 outs = 2/3 inning)  
- `"6.0"` → `6.0`
- `None` / `""` → `None` → `0.0`

**Opener 規則**:
- 若首位投手 IP < 2.0 → `is_opener=True`, `is_reliever=True`, `is_starter=False`
- 後續投手（含 bulk pitcher）→ `is_reliever=True`, `appearance_order >= 2`

---

## 7. Phase 61 SSOT 特徵升級狀態

### 升為 AVAILABLE (10 個)
1. `bullpen_usage_last_1d` — sum(reliever IP on D-1)
2. `bullpen_usage_last_3d` — sum(reliever IP on D-1..D-3) [已有資料，現提升至 per-pitcher]
3. `bullpen_usage_last_5d` — sum(reliever IP on D-1..D-5)
4. `reliever_back_to_back_count` — count(unique relievers on D-1 ∩ D-2)
5. `reliever_three_in_four_days_count` — count(relievers with >= 3 appearances in D-1..D-4)
6. `closer_used_last_1d` — is_closer_candidate appeared on D-1
7. `closer_used_last_2d` — is_closer_candidate appeared on D-1 or D-2
8. `bullpen_fatigue_favorite_side` — derived from 3d usage (unchanged)
9. `bullpen_fatigue_underdog_side` — derived from 3d usage (unchanged)
10. `bullpen_rest_imbalance` — derived from 3d usage ratio (unchanged)

### 維持 DATA_LIMITED (2 個)
11. `high_leverage_reliever_used_last_1d` — 需要 LI (leverage index)，boxscore 無此欄位
12. `high_leverage_reliever_workload_last_3d` — 需要 LI，推遲至 Phase 63

> **重要**：DATA_LIMITED 特徵不輸出 0.0 作為中性填補。必須輸出 `FeatureAvailability.DATA_LIMITED` marker，由 Phase 61 SSOT 的 `_make_data_limited_slot()` 處理。

---

## 8. PIT 安全策略

**核心規則**: `entry_date (snapshot_date) < game_date (prediction_date)` 嚴格成立

**實作**:
```python
def assert_pit_safe(prediction_date: str, snapshot_date: str) -> None:
    if snapshot_date >= prediction_date:
        raise ValueError(f"PIT VIOLATION: ...")
```

**Rolling Window**:
```python
# D-1 to D-N window — 預測日 (prediction_date) 本身嚴格排除
cutoff_start = prediction_date - timedelta(days=window_days)
valid: cutoff_start <= game_date < prediction_date
```

**特殊場景**:
- **雙重賽 (Doubleheader)**: Game 1 的 D-0 資料不進入 Game 2 的 window（使用 `game_date < prediction_date` 嚴格不等式）
- **延賽 (Postponed)**: null boxscore → `games_missing++`，不產生任何 appearance record
- **Opener**: IP < 2.0 首發 → `is_opener=True`，納入牛棚 IP 統計
- **缺失資料**: missing IP → `_normalize_ip(None)` → `0.0`（偏保守估計）

---

## 9. 風險與限制

| 風險 | 嚴重性 | 緩解措施 |
|------|--------|---------|
| `is_closer_candidate` 為啟發式 (最後一位投手) | 低 | 這是定義性代理指標，非實際 closer role；Phase 63 可引入 PbP 確認 |
| IP = 0.0 for missing data | 中 | 偏保守；不過分估計牛棚疲勞。若大量缺失，改回 DATA_LIMITED |
| opener IP < 2.0 分類閾值主觀 | 低 | 2.0 IP = 6 out，業界通用標準；測試明確驗證 |
| LI 特徵缺失影響預測能力 | 中 | Phase 60 顯示 LI 特徵原本即為 DATA_LIMITED；影響已在期望值內 |
| API rate limit (若未來抓取 5d 資料) | 低 | 每次 fetch 只新增差量日期；同 Phase 58/59 運作模式 |
| `is_opener` 不排除 bulk pitcher 計入牛棚 | 低 | bulk pitcher 在 appearance_order >= 2，永遠 is_reliever=True |

---

## 10. Gate 結論與下一步

### Gate: `STATSAPI_SELECTED`

**理由**:
- MLB StatsAPI `/game/{pk}/boxscore` 提供足夠的 per-pitcher 資料，可派生 12 個 Phase 61 SSOT 特徵中的 10 個
- 2 個 LI 依賴特徵維持 DATA_LIMITED（已符合 Phase 61 SSOT 合約預期）
- Fixture-only 驗證通過：4 場正常解析 + 1 場 null boxscore 正確處理
- 無 production patch，無 alpha 修改，100% diagnostic

**Ingestion 可行性**: ✅ 已驗證 (123/123 tests PASS)  
**安全常數**: `CANDIDATE_PATCH_CREATED=False`, `PRODUCTION_MODIFIED=False`, `ALPHA_MODIFIED=False`

### 下一步 (Phase 63 建議)

1. **滾動資料收集**: 擴展 `_bullpen_from_schedule()` 以儲存 per-pitcher 出賽記錄（非僅合計 IP）到新的 `data/mlb_context/bullpen_appearances.jsonl`
2. **窗口擴展**: 從 3d → 1d / 5d（現有 timedelta 邏輯直接可擴展）
3. **LI 增補 (可選)**: 引入 `/game/{pk}/playByPlay` 為 `high_leverage_*` 特徵提供 LI，讓 DATA_LIMITED → AVAILABLE
4. **回測整合**: 將新特徵加入 Phase 60 的 segment analysis pipeline，確認統計顯著性 gate 前提

---

**PHASE_62_BULLPEN_GRANULAR_SOURCE_SELECTION_VERIFIED**
