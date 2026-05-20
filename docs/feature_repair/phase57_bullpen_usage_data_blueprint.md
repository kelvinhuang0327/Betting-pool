# Phase 57 — Bullpen Usage Data Acquisition & PIT Backfill Blueprint

**生成日期**: 2026-05-05  
**版本**: `phase57_bullpen_usage_blueprint_v1`  
**狀態**: Blueprint Only — Paper / Offline  
**前置 Phase**: Phase 56 (`DATA_GAP_REMAINS`)  
**後繼 Phase**: Phase 58 (`Bullpen Usage Backfill Implementation`)

---

## Hard Rules (NEVER Violate)

| 規則 | 值 |
|------|----|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |
| 調整 alpha | ❌ 禁止 |
| Ensemble | ❌ 禁止 |
| 串接 Production API | ❌ 禁止（本 Phase 僅 blueprint） |
| 宣稱 performance improvement | ❌ 禁止（未有實際資料驗證） |

---

## 1. Executive Summary

Phase 56 成功建立了完整的牛棚特徵工程管線（feature builder → PIT validator → backfill → context injection → adjustment → evaluation），並通過 1012/1012 全回歸測試。然而，最終 Gate 為 `DATA_GAP_REMAINS`，原因是：

**bullpen_feature_available_rate = 0.0%（0/2025 場）**

這表示牛棚假說（bullpen fatigue/workload 影響勝負機率）在理論設計上合理，但**缺乏實際 MLB 2025 牛棚使用資料**，無法進行有效的統計評估。目前所有 bullpen features 均使用中性回退值（neutral fallback），導致：

- `bullpen_adjustment = 0.0` for all 2025 rows
- `delta_BSS = 0.000000`
- `delta_ECE = 0.000000`
- Phase 56 injected JSONL = Phase 52 JSONL（機率完全相同）

本 Phase 57 Blueprint 的目標是：

1. 明確定義 Phase 58 所需的牛棚使用資料欄位
2. 評估候選資料來源（不串接 production API）
3. 設計 point-in-time safe 的 schema 與 backfill 策略
4. 定義驗收標準
5. 產出 Phase 58 實作任務清單

---

## 2. Why Phase 56 Ended with DATA_GAP_REMAINS

### Phase 56 Gate 決策邏輯

```
if bullpen_feature_available_rate < 0.80:
    gate = DATA_GAP_REMAINS
```

### 根本原因分析

| 層面 | 說明 |
|------|------|
| **Feature Design** | ✅ 正確：5 個 proxy features 設計合理，已通過 PIT 驗證 |
| **PIT Safety** | ✅ 通過：所有特徵嚴格使用 `game_date` 之前資料 |
| **Code Quality** | ✅ 通過：111 個 Phase56 測試、1012 全回歸測試全過 |
| **Data Availability** | ❌ 失敗：`bullpen_feature_available = False` for ALL 2025 rows |
| **Context** | MLB 2025 牛棚出賽記錄（`bullpen_outs`, `appearances`, `leverage_idx`）未被收集 |

### 目前 Neutral Fallback 值

| 欄位 | Fallback 值 | 說明 |
|------|-------------|------|
| `home_bullpen_fatigue_3d` | `0.0` | 中性：無資料假設無疲勞 |
| `home_bullpen_recent_era_proxy` | `4.10` | 聯盟平均 ERA |
| `home_late_game_leverage_usage_proxy` | `0.0` | 中性：無槓桿使用資料 |
| `home_reliever_b2b_count` | `0` | 中性：無 B2B 資料 |
| `bullpen_fatigue_delta_3d` | `0.0` | 無差異 |

### 結論

**Bullpen hypothesis 尚未被驗證，原因是資料不可用，不是 feature 無效。** 本設計架構正確，需要在 Phase 58 填補資料空缺。

---

## 3. Required Bullpen Usage Fields

### 3.1 Game Identity

| 欄位 | 型別 | 說明 |
|------|------|------|
| `game_id` | `str` | 唯一比賽識別碼，e.g. `"MLB_2025_20250415_NYY_BOS"` |
| `game_date` | `str` | 比賽日期 `YYYY-MM-DD` |
| `home_team` | `str` | 主場球隊全名 |
| `away_team` | `str` | 客場球隊全名 |
| `doubleheader_game_num` | `int` | 0 = 非雙重賽; 1 = DH 第一場; 2 = DH 第二場 |
| `is_bullpen_game` | `bool` | 是否為牛棚賽 (opener) |

### 3.2 Bullpen Workload (Cumulative Outs)

| 欄位 | 型別 | 說明 |
|------|------|------|
| `home_bullpen_outs_1d` | `float` | 主場牛棚前 1 天出局數總計 |
| `away_bullpen_outs_1d` | `float` | 客場牛棚前 1 天出局數總計 |
| `home_bullpen_outs_3d` | `float` | 主場牛棚前 3 天出局數總計 |
| `away_bullpen_outs_3d` | `float` | 客場牛棚前 3 天出局數總計 |
| `home_bullpen_outs_7d` | `float` | 主場牛棚前 7 天出局數總計 |
| `away_bullpen_outs_7d` | `float` | 客場牛棚前 7 天出局數總計 |
| `home_bullpen_outs_1d_available` | `bool` | 1d 資料是否可用 |
| `away_bullpen_outs_1d_available` | `bool` | |
| `home_bullpen_outs_3d_available` | `bool` | 3d 資料是否可用 |
| `away_bullpen_outs_3d_available` | `bool` | |
| `home_bullpen_outs_7d_available` | `bool` | 7d 資料是否可用 |
| `away_bullpen_outs_7d_available` | `bool` | |

### 3.3 Back-to-Back & High-Frequency Usage

| 欄位 | 型別 | 說明 |
|------|------|------|
| `home_reliever_b2b_count` | `int` | 主場連 2 天出賽的中繼投手人數（2d 內） |
| `away_reliever_b2b_count` | `int` | 客場連 2 天出賽的中繼投手人數 |
| `home_reliever_3in4_count` | `int` | 主場 4 天內出賽 3 次以上的中繼投手人數 |
| `away_reliever_3in4_count` | `int` | 客場 4 天內出賽 3 次以上的中繼投手人數 |
| `home_b2b_available` | `bool` | B2B 資料是否可用 |
| `away_b2b_available` | `bool` | |
| `home_3in4_available` | `bool` | 3in4 資料是否可用 |
| `away_3in4_available` | `bool` | |

### 3.4 Performance Proxy

| 欄位 | 型別 | 說明 |
|------|------|------|
| `home_bullpen_recent_era_proxy` | `float` | 主場牛棚近 14 天 ERA proxy（0–15，cap at 15） |
| `away_bullpen_recent_era_proxy` | `float` | 客場牛棚近 14 天 ERA proxy |
| `home_bullpen_recent_fip_proxy` | `float` | 主場牛棚近 14 天 FIP proxy（FIP = (13×HR + 3×BB - 2×K) / IP + 3.2） |
| `away_bullpen_recent_fip_proxy` | `float` | 客場牛棚近 14 天 FIP proxy |
| `home_era_available` | `bool` | ERA proxy 是否可用 |
| `away_era_available` | `bool` | |
| `home_fip_available` | `bool` | FIP proxy 是否可用 |
| `away_fip_available` | `bool` | |

> **FIP proxy 說明**: 標準 FIP 公式需要個別投手 K/BB/HR 資料。若只有 box score aggregates，FIP proxy 可用 `(3×ER + adjusted_bb_factor) / IP`。若資料不足，fallback 到 ERA proxy。

### 3.5 Leverage Proxy

| 欄位 | 型別 | 說明 |
|------|------|------|
| `home_late_game_leverage_usage_proxy` | `float` | 主場 7 天內 high-leverage 出賽比例（0–1） |
| `away_late_game_leverage_usage_proxy` | `float` | 客場 7 天內 high-leverage 出賽比例 |
| `home_high_leverage_reliever_usage_3d` | `float` | 主場 3 天內 high-leverage 出賽次數（raw count） |
| `away_high_leverage_reliever_usage_3d` | `float` | 客場 3 天內 high-leverage 出賽次數 |
| `home_leverage_available` | `bool` | Leverage 資料是否可用 |
| `away_leverage_available` | `bool` | |

> **High-Leverage 定義**: `leverage_index >= 1.5`，或 `inning >= 7 AND run_diff <= 2`。若無 LI 欄位，使用後者 proxy。

### 3.6 Derived Deltas

| 欄位 | 公式 | 說明 |
|------|------|------|
| `bullpen_fatigue_delta_3d` | `away_bullpen_outs_3d - home_bullpen_outs_3d` | 正值 = 客場更疲勞 = 主場有利 |
| `bullpen_fatigue_delta_7d` | `away_bullpen_outs_7d - home_bullpen_outs_7d` | |
| `reliever_b2b_delta` | `away_reliever_b2b_count - home_reliever_b2b_count` | 正值 = 客場 B2B 更多 |
| `bullpen_recent_era_delta` | `away_bullpen_recent_era_proxy - home_bullpen_recent_era_proxy` | 正值 = 客場 ERA 較高 = 主場有利 |
| `bullpen_recent_fip_delta` | `away_bullpen_recent_fip_proxy - home_bullpen_recent_fip_proxy` | |
| `leverage_delta_3d` | `away_high_leverage_reliever_usage_3d - home_high_leverage_reliever_usage_3d` | |

### 3.7 Availability Summary

| 欄位 | 型別 | 說明 |
|------|------|------|
| `bullpen_feature_available` | `bool` | `True` 若 home + away 雙方均有 3d workload 資料 |
| `bullpen_partial_available` | `bool` | `True` 若只有單邊資料 |
| `availability_components` | `dict` | 各子特徵可用性字典 |

### 3.8 Audit

| 欄位 | 型別 | 說明 |
|------|------|------|
| `data_timestamp` | `str` | 資料抓取時間戳 ISO8601 UTC |
| `snapshot_date` | `str` | 快照日期（必須 < `game_date`） |
| `source` | `str` | 資料來源標籤（見 §4） |
| `source_detail` | `str` | 來源 URL / endpoint 細節 |
| `point_in_time_safe` | `bool` | PIT 驗證通過標記 |
| `fallback_reason` | `str` | 若 fallback，說明原因 |
| `feature_version` | `str` | `"phase58_bullpen_usage_v1"` |
| `audit_hash` | `str` | `sha256:{hash}` 覆蓋 game_id + source + snapshot_date + key feature values |

---

## 4. Candidate Data Sources

### 4.1 MLB StatsAPI (官方)

**端點**: `https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore`

| 評估項目 | 結果 |
|----------|------|
| 可取得欄位 | 每場比賽 box score；包含每個投手 IP、ER、H、BB、SO；有 inning 時序 |
| 免費 | ✅ 是（公開 API，無需 API Key） |
| 穩定性 | ⭐⭐⭐（官方，但有 rate limit；偶有 downtime） |
| 批次 backfill | ✅ 可；需要先取得 `game_pk` 列表（`/schedule` endpoint） |
| Point-in-time | ✅ 可；box score 結束後即鎖定；可用 `abstractGameState=Final` 過濾 |
| Research 適合度 | ✅ 高（資料完整、有球員 ID、有 inning-level stats） |
| Production 適合度 | ⚠️ 中（rate limit、需要維護 game_pk 映射） |
| Rate Limit | 推測 ~15–20 req/s；需加 `time.sleep(0.1)` |
| Cache Strategy | 以 `game_pk` 為 key 存入本地 JSON；永久 cache（結果不變） |
| **Leverage 資料** | ⚠️ 無直接 LI；需由 `inning >= 7 AND close game` proxy |
| **B2B 計算** | ✅ 需跨賽程計算；用前 n 天 appearances 聚合 |
| **建議優先度** | 🥇 **第一優先** |

**所需 endpoints**:
```
GET /api/v1/schedule?sportId=1&season=2025&gameTypes=R
    → 取得所有 game_pk 列表

GET /api/v1/game/{game_pk}/boxscore
    → 取得每場比賽 pitcher-level 詳情

GET /api/v1/game/{game_pk}/linescore
    → 取得逐局比分（輔助 high-leverage proxy）
```

**資料映射**:
```python
# box score pitcher entry (relief pitcher):
{
  "person": {"id": 592789, "fullName": "..."},
  "stats": {
    "pitching": {
      "inningsPitched": "2.0",
      "earnedRuns": 1,
      "strikeOuts": 2,
      "baseOnBalls": 1,
      "homeRuns": 0,
    }
  },
  "gameStatus": {"isCurrentPitcher": false},
  "pitchOrder": 2   # 1 = starter, 2+ = reliever
}
```

---

### 4.2 Baseball Savant / Statcast

**端點**: `https://baseballsavant.mlb.com/statcast_search/csv?...`  
或 `pybaseball.statcast()` wrapper

| 評估項目 | 結果 |
|----------|------|
| 可取得欄位 | Pitch-level 資料：`events`, `inning`, `at_bat_number`, `leverage_index`, `pitcher`, `game_date` |
| 免費 | ✅ 是（公開）|
| 穩定性 | ⭐⭐（時常有流量限制；搜尋介面不穩） |
| 批次 backfill | ✅ 可；但每次查詢有 row 上限（~40,000 rows / request） |
| Point-in-time | ✅ 是（賽後資料） |
| Research 適合度 | ✅ 非常高（有真實 `leverage_index`） |
| Production 適合度 | ⚠️ 低（不穩定、需大量請求） |
| Rate Limit | 嚴格；建議每 2–3 秒一請求，並完整 cache |
| Cache Strategy | 按 `game_date` + `game_pk` 存成本地 CSV / Parquet |
| **Leverage 資料** | ✅ 直接 `leverage_index` 欄位 |
| **B2B 計算** | ✅ 可；需 player-level 跨日聚合 |
| **建議優先度** | 🥈 **第二優先（leverage 最佳來源）** |

**pybaseball 用法**:
```python
from pybaseball import statcast
df = statcast("2025-04-01", "2025-04-30")
# columns: game_date, game_pk, pitcher, leverage_index, inning, events, ...
```

---

### 4.3 Retrosheet Game Logs

**來源**: `https://www.retrosheet.org/gamelogs/`

| 評估項目 | 結果 |
|----------|------|
| 可取得欄位 | Game-level aggregates；各隊投手人數、IP、ER、H、BB、SO；無個別投手資料 |
| 免費 | ✅ 是 |
| 穩定性 | ⭐⭐⭐⭐（靜態文件；非常穩定） |
| 批次 backfill | ✅ 最快；整個賽季一個文件 |
| Point-in-time | ✅ 固定歷史記錄 |
| Research 適合度 | ⭐⭐（team-level only；無法計算 B2B / 個別投手疲勞） |
| Production 適合度 | ❌ 低（無即時更新；用於歷史回溯） |
| Rate Limit | 無（靜態文件下載） |
| Cache Strategy | 整年文件 download 後本地存放 |
| **Leverage 資料** | ❌ 無 |
| **B2B 計算** | ❌ 無個別投手資料 |
| **建議優先度** | 🥉 **第三優先（輔助驗證用）** |

---

### 4.4 FanGraphs Bullpen / Reliever Stats

**URL**: `https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&...`  
或 `pybaseball.pitching_stats()` wrapper

| 評估項目 | 結果 |
|----------|------|
| 可取得欄位 | Pitcher-level 賽季累計：ERA、FIP、xFIP、K%、BB%、IP；無 game-level 時序 |
| 免費 | ⚠️ 基本資料免費；advanced metrics 需 FanGraphs+ 訂閱 |
| 穩定性 | ⭐⭐⭐（穩定但非即時） |
| 批次 backfill | ⚠️ 可抓賽季累計；但無每日快照 |
| Point-in-time | ❌ 困難：FanGraphs 提供賽季累計，無每日 rolling snapshot |
| Research 適合度 | ⭐⭐（適合確認聯盟水準；不適合 rolling window） |
| Production 適合度 | ❌ 低 |
| **建議優先度** | 4️⃣ **輔助用（ERA/FIP 聯盟平均校正用）** |

---

### 4.5 pybaseball (Open Source Wrapper)

**GitHub**: `https://github.com/jldbc/pybaseball`

| 評估項目 | 結果 |
|----------|------|
| 可取得欄位 | 整合 Baseball Savant, FanGraphs, Baseball Reference |
| 免費 | ✅ 是 |
| 穩定性 | ⭐⭐（依賴上游網站；偶有爬蟲問題） |
| 批次 backfill | ✅ `statcast()`, `pitching_stats()`, `team_game_logs()` |
| Point-in-time | ✅ 需自行控制查詢日期 |
| Research 適合度 | ✅ 高（最方便的 Python 入口） |
| Production 適合度 | ⚠️ 中（有 rate limit、版本更新風險） |
| 關鍵函數 | `statcast()`, `team_pitching_bref()`, `pitching_stats()` |
| **建議優先度** | 🥇 **整合優先（作為 MLB StatsAPI + Savant 的 Python 橋接層）** |

---

### 4.6 Local as-played / Schedule Files（專案內）

**現有文件**:
- `data/wbc_2026_authoritative_snapshot.json`
- `data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl`（2025 rows）
- `data/mlb_context_sources/`（待確認）

| 評估項目 | 結果 |
|----------|------|
| 可取得欄位 | game_id, game_date, home_team, away_team（已有）；無牛棚使用記錄 |
| 免費 | ✅ 自有 |
| 點位時序 | ✅ 固定 |
| 缺少項目 | 投手 IP / ER / appearances / leverage |
| **用途** | 作為 backfill 的 game_id 列表骨架；不含牛棚資料 |
| **建議優先度** | ✅ 必用（確定 2025 賽程清單） |

---

### 4.7 資料來源優先組合建議

```
Phase 58 建議採用策略：

主要來源（Tier 1）:
  MLB StatsAPI boxscore → bullpen workload (IP, ER, appearances per game)
  pybaseball.statcast   → leverage_index per plate appearance

輔助來源（Tier 2）:
  Retrosheet game logs  → team-level ER/IP 驗證
  FanGraphs             → 聯盟 ERA/FIP 標準化基準

本地文件（Scaffolding）:
  mlb_2025 baseline JSONL → game_id / team 骨架
```

---

## 5. Point-in-Time Safety Rules

### 5.1 核心原則

對 `game_date = D` 的比賽，bullpen features 只能使用 **D-1（含）以前** 完成的比賽資料。

```python
# PIT 安全性判斷（必須嚴格 <，不可 <=）
def is_pit_safe(entry_game_date: str, target_game_date: str) -> bool:
    return entry_game_date < target_game_date  # strict less than
```

### 5.2 同日賽事

| 情況 | 處理方式 |
|------|----------|
| 同日先後賽 (doubleheader) | 第二場**不可**使用第一場的牛棚資料（同日） |
| 同日其他球隊 | **不可**使用（無法確保賽事順序） |
| 安全方案 | 只使用 `entry_date < game_date`（strict <），完全排除當天 |

### 5.3 Doubleheader 特殊處理

```python
def get_pit_safe_schedule(schedule: list[dict], game_date: str) -> list[dict]:
    """
    返回 PIT 安全的過去賽程記錄。
    
    Doubleheader 規則：
    - game_date = D, DH game_num = 1 → 使用 game_date < D
    - game_date = D, DH game_num = 2 → 使用 game_date < D 
      (DH game 1 同日，不可用)
    """
    return [
        entry for entry in schedule
        if entry["game_date"] < game_date  # strict less than
    ]
```

> **雙重賽注意**：即使第一場比賽已完成，第二場的 bullpen features 也**不可**使用第一場的結果。這是因為無法保證資料管線的 snapshot 時序。建議在 schema 中記錄 `doubleheader_game_num` 並在驗證時特別標記。

### 5.4 Bullpen Game / Opener 標記

```python
GAME_TYPE_NORMAL = "normal"
GAME_TYPE_BULLPEN_GAME = "bullpen_game"     # 無傳統先發，牛棚全場
GAME_TYPE_OPENER = "opener"                  # 先發投 1-2 局後牛棚接管
```

- Bullpen game / opener 場次中，「先發投手」實為中繼投手
- 這些場次的 B2B / workload 計算應將 opener 納入 **bullpen** 計算，不入 SP 計算
- Schema 需標記 `is_bullpen_game = True` 以便後續分析

### 5.5 Scratched Starter 處理

| 情況 | 處理方式 |
|------|----------|
| 先發投手在開賽當日 scratch | 對該場比賽：`sp_feature_available = False`；以 bullpen workload 補償 |
| 臨時換人（in-game） | 不影響本場 bullpen features 計算（使用賽前 snapshot） |
| 如何偵測 | 若 `starter_ip < 1.0` → 視為 `short_outing`；可標記 `starter_role_normal = False` |

### 5.6 禁止欄位清單

以下欄位**絕對禁止**出現在 bullpen features 中：

```python
_FORBIDDEN_LEAKAGE_FIELDS: frozenset[str] = frozenset({
    "home_win",
    "final_score",
    "home_score",
    "away_score",
    "result",
    "box_score",
    "post_game_stats",
    "closing_odds_after_game",
    "innings_pitched_today",        # 當場
    "era_after_game",
    "game_score",
    "actual_starter_ip_today",
    "whip_after_game",
    "fip_after_game",
    "win_probability_after_game",
    "wpa_after_game",               # Win Probability Added (需賽後)
    "re24_after_game",              # Run Expectancy (需賽後)
})
```

### 5.7 Snapshot Date 驗證

```python
def validate_snapshot_date(record: dict) -> bool:
    """
    確保 snapshot_date < game_date。
    """
    snapshot = record.get("snapshot_date", "")
    game_date = record.get("game_date", "")
    if not snapshot or not game_date:
        return False
    return snapshot < game_date  # strict less than
```

### 5.8 Audit Hash 覆蓋範圍

```python
import hashlib

def compute_bullpen_audit_hash(
    game_id: str,
    snapshot_date: str,
    source: str,
    home_outs_3d: float,
    away_outs_3d: float,
    feature_version: str,
) -> str:
    payload = (
        f"{game_id}|{snapshot_date}|{source}|"
        f"{home_outs_3d:.2f}|{away_outs_3d:.2f}|{feature_version}"
    )
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()[:32]
```

---

## 6. Schema 設計

### 6.1 目標文件

```
data/mlb_2025/derived/mlb_2025_bullpen_usage_phase58.jsonl
```

### 6.2 完整 Schema（每筆記錄）

```jsonc
{
  // === Game Identity ===
  "game_id": "MLB_2025_20250415_NYY_BOS",
  "game_date": "2025-04-15",
  "home_team": "New York Yankees",
  "away_team": "Boston Red Sox",
  "season": 2025,
  "doubleheader_game_num": 0,
  "is_bullpen_game": false,

  // === Bullpen Workload — Home ===
  "home_bullpen_outs_1d": 3.0,
  "home_bullpen_outs_3d": 18.0,
  "home_bullpen_outs_7d": 42.0,
  "home_bullpen_outs_1d_available": true,
  "home_bullpen_outs_3d_available": true,
  "home_bullpen_outs_7d_available": true,

  // === Bullpen Workload — Away ===
  "away_bullpen_outs_1d": 9.0,
  "away_bullpen_outs_3d": 24.0,
  "away_bullpen_outs_7d": 51.0,
  "away_bullpen_outs_1d_available": true,
  "away_bullpen_outs_3d_available": true,
  "away_bullpen_outs_7d_available": true,

  // === B2B & High-Frequency Usage ===
  "home_reliever_b2b_count": 1,
  "away_reliever_b2b_count": 2,
  "home_reliever_3in4_count": 0,
  "away_reliever_3in4_count": 1,
  "home_b2b_available": true,
  "away_b2b_available": true,

  // === Performance Proxy ===
  "home_bullpen_recent_era_proxy": 3.75,
  "away_bullpen_recent_era_proxy": 4.80,
  "home_bullpen_recent_fip_proxy": 3.60,
  "away_bullpen_recent_fip_proxy": 4.50,
  "home_era_available": true,
  "away_era_available": true,
  "home_fip_available": false,   // 需要 K/BB/HR 個別資料
  "away_fip_available": false,

  // === Leverage Proxy ===
  "home_late_game_leverage_usage_proxy": 0.45,
  "away_late_game_leverage_usage_proxy": 0.38,
  "home_high_leverage_reliever_usage_3d": 3.0,
  "away_high_leverage_reliever_usage_3d": 2.0,
  "home_leverage_available": true,
  "away_leverage_available": true,

  // === Derived Deltas ===
  "bullpen_fatigue_delta_3d": 6.0,          // away - home (正 = 客場更疲勞)
  "bullpen_fatigue_delta_7d": 9.0,
  "reliever_b2b_delta": 1,                  // away - home
  "bullpen_recent_era_delta": 1.05,         // away - home (正 = 客場 ERA 較高)
  "bullpen_recent_fip_delta": 0.90,
  "leverage_delta_3d": -1.0,

  // === Availability Summary ===
  "bullpen_feature_available": true,        // home AND away 均有 3d workload
  "bullpen_partial_available": false,
  "availability_components": {
    "home_3d": true,
    "away_3d": true,
    "home_b2b": true,
    "away_b2b": true,
    "home_era": true,
    "away_era": true,
    "home_leverage": true,
    "away_leverage": true
  },

  // === Audit ===
  "snapshot_date": "2025-04-14",            // MUST be < game_date
  "data_timestamp": "2026-05-05T00:00:00Z", // 資料抓取時間
  "source": "mlb_statsapi_boxscore",
  "source_detail": "https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore",
  "point_in_time_safe": true,
  "fallback_reason": "",
  "feature_version": "phase58_bullpen_usage_v1",
  "audit_hash": "sha256:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
}
```

### 6.3 Schema 版本控制

| 欄位 | 說明 |
|------|------|
| `feature_version` | 格式：`phase{N}_bullpen_usage_v{M}`，版本更新時遞增 M |
| `audit_hash` | 每次 backfill 重跑應產生相同 hash（冪等性） |
| 不變欄位 | `game_id`, `game_date`, `home_team`, `away_team`, `season` |

---

## 7. Backfill Strategy

### 7.1 Overview

```
Input:  data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl  (2,025 rows)
Output: data/mlb_2025/derived/mlb_2025_bullpen_usage_phase58.jsonl (2,025 rows)
```

### 7.2 步驟流程

```
Step 1: 讀取 baseline predictions JSONL
        → 取得 game_id, game_date, home_team, away_team 清單
        → 按 game_date 升序排序

Step 2: 下載 / 載入 pitcher-level relief appearance history
        → 來源：MLB StatsAPI boxscore（每個 game_pk）
        → 轉換為 team-level relief appearance records:
          [{
            "game_id": ..., "game_date": ...,
            "team": ...,
            "bullpen_outs": ...,    # 所有 relief pitcher IP * 3
            "bullpen_earned_runs": ...,
            "bullpen_appearances": ...,  # 中繼投手人數
            "relief_pitcher_ids": [...],  # 用於 B2B 計算
            "high_leverage_appearances": ...  # from Statcast
          }]

Step 3: 建立 team rolling schedule
        → team_schedule[team] = list of appearance records sorted by game_date
        → 確保 game_date 欄位為 YYYY-MM-DD string

Step 4: 對每場比賽，依 game_date = D：
        → D-1 snapshot：過濾 entry_date < D（strict <）
        → 計算 1d / 3d / 7d workload（sum of bullpen_outs）
        → 計算 b2b count（2天內有記錄的投手人數）
        → 計算 3in4 count（4天內出賽3+次的投手人數）
        → 計算 ERA proxy（window=14d）：(ER * 9) / max(IP, 0.33)
        → 計算 FIP proxy（若有 K/BB/HR）
        → 計算 leverage proxy（高槓桿出賽比例，window=7d）

Step 5: 計算 derived deltas（away - home）

Step 6: 計算 bullpen_feature_available
        → True if AND(home_3d_available, away_3d_available)

Step 7: 輸出 JSONL（one row per game, in game_date order）

Step 8: 執行 PIT validation（phase58_pit_validator）
        → 確認 snapshot_date < game_date for all rows
        → 確認無 forbidden 欄位
        → 確認 audit_hash 存在

Step 9: 輸出驗證報告
```

### 7.3 Edge Cases

| 情況 | 處理策略 |
|------|----------|
| 賽季開幕第一週（無歷史） | `window_days` 資料不足 → 使用可用資料計算，標記 `partial_window = True` |
| All-Star Break | 空白期間 → 7d window 跨越 break → 照常計算（只使用實際有資料的日期） |
| Doubleheader | DH game 2 不使用 DH game 1 資料（strict <，同日排除） |
| Rainout / PPD | 補賽場次：使用補賽日期作為 game_date |
| Injury list（IL） | 投手在 IL 期間出賽記錄為 0；不特別標記（資料自然為 0）|
| Bullpen game | 先發 < 2 IP → 首位投手計入 bullpen；標記 `is_bullpen_game = True` |
| 重複 game_id | 以 game_id 為主鍵，重複時保留最後寫入版本並記錄 warning |

### 7.4 效能考量

| 項目 | 估計 |
|------|------|
| Total games | 2,025 |
| API calls（MLB StatsAPI）| 2,025 × 1 box score call + schedule call |
| Estimated time（含 rate limit）| ~6–8 分鐘（@10 req/s） |
| Cache strategy | `{game_pk}.json` 本地 cache；cache hit → 無需 API call |
| Statcast download | 按月下載（12 個月）；約 50–200 MB |

### 7.5 幂等性（Idempotency）

- 若 `data/mlb_2025/derived/mlb_2025_bullpen_usage_phase58.jsonl` 已存在，且 `audit_hash` 一致，則 skip 重新計算
- 只有明確加 `--force` 參數才允許重新計算
- `audit_hash` 覆蓋 `game_id + snapshot_date + source + key_values` → 確保冪等

---

## 8. Validation Plan

Phase 58 完成後，`tests/test_phase58_bullpen_usage_validation.py` 必須驗證：

### 8.1 資料完整性

| 驗證項目 | 標準 | 說明 |
|----------|------|------|
| `row_count` | `== 2,025` | 必須與 baseline JSONL 完全對應 |
| `game_id` 唯一性 | 0 duplicates | 不允許重複記錄 |
| `game_id` 對應率 | `100%` | 每個 baseline game_id 必須有對應 bullpen record |
| Schema 完整性 | 所有必要欄位存在 | 見 §6.2 |

### 8.2 Point-in-Time Safety

| 驗證項目 | 標準 |
|----------|------|
| `point_in_time_safe_rate` | `== 100%` (2025/2025) |
| `snapshot_date < game_date` | ALL rows |
| 無禁止欄位洩漏 | 0 violations |
| `audit_hash_present_rate` | `== 100%` |

### 8.3 Feature Availability

| 驗證項目 | 目標標準 |
|----------|----------|
| `bullpen_feature_available_rate` | `>= 80%` |
| `home_bullpen_outs_3d_available_rate` | `>= 85%` |
| `away_bullpen_outs_3d_available_rate` | `>= 85%` |
| `home_b2b_available_rate` | `>= 80%` |
| `away_b2b_available_rate` | `>= 80%` |
| `fallback_rate` | `<= 20%` |

> 若 `bullpen_feature_available_rate < 80%`，Phase 58 Gate 應為 `DATA_GAP_REMAINS`（與 Phase 56 相同）。

### 8.4 Feature Value Sanity

| 驗證項目 | 標準 |
|----------|------|
| `home_bullpen_outs_3d` | `>= 0`, `<= 100` (合理範圍) |
| `home_bullpen_recent_era_proxy` | `>= 0`, `<= 15` |
| `home_late_game_leverage_usage_proxy` | `>= 0`, `<= 1` |
| `bullpen_fatigue_delta_3d` | `[-100, 100]` |
| `home_reliever_b2b_count` | `>= 0`, `<= 15` |

### 8.5 Model 指標驗證（Phase 56 Gate 重跑）

在 `bullpen_feature_available_rate >= 80%` 的前提下，重跑 Phase 56 evaluation：

| 驗證項目 | 目標 |
|----------|------|
| Heavy-Favorite ECE | `delta_ece <= 0` (改善) |
| High-Confidence BSS | `delta_bss >= -0.001` (不惡化) |
| Overall BSS | `delta_bss >= -0.001` (不惡化) |
| Phase55 Failure Segment Count | `delta <= 0` (不增加) |

### 8.6 測試架構

```
tests/
  test_phase58_bullpen_usage_validation.py
    class TestDataIntegrity
    class TestPITSafety
    class TestFeatureAvailability
    class TestFeatureValueSanity
    class TestModelMetrics (requires real JSONL)
```

---

## 9. Phase 58 Implementation Tasks

### 58.1 — Bullpen Usage Data Loader

**目的**: 下載並 cache MLB StatsAPI boxscore 資料  
**輸出**: `data/mlb_2025/raw/mlb_statsapi_boxscores/` (per-game JSON cache)  
**關鍵函數**: `load_bullpen_game_log(game_pk: int) -> dict`  
**注意**: 必須遵守 rate limit；cache-first 策略

```python
# 介面設計
def load_bullpen_game_log(
    game_pk: int,
    cache_dir: Path,
    rate_limit_sec: float = 0.1,
) -> dict: ...
```

### 58.2 — Relief Appearance Parser

**目的**: 從 boxscore JSON 解析每個中繼投手的出賽記錄  
**輸出**: `list[ReliefAppearanceRecord]`  
**關鍵邏輯**:
- 先發 = `pitchOrder == 1`；中繼 = `pitchOrder >= 2`
- 計算 bullpen_outs = sum(IP * 3 for all relievers)
- Bullpen game 特殊處理（先發 < 2 IP → 視為中繼）

```python
@dataclass
class ReliefAppearanceRecord:
    game_id: str
    game_date: str
    team: str
    pitcher_id: int
    pitcher_name: str
    innings_pitched: float
    earned_runs: int
    appearances: int  # always 1 per record
    is_high_leverage: bool  # from Statcast leverage_index
```

### 58.3 — Team Rolling Workload Snapshot Builder

**目的**: 對每個球隊建立滾動 workload 快照  
**輸入**: list of `ReliefAppearanceRecord`  
**輸出**: 每個 (team, game_date) 的 rolling stats  
**視窗**: 1d / 3d / 7d / 14d

```python
def build_team_workload_snapshot(
    team: str,
    game_date: str,
    appearance_history: list[ReliefAppearanceRecord],
    windows: list[int] = [1, 3, 7, 14],
) -> dict: ...
```

### 58.4 — Bullpen Point-in-Time Validator（更新版）

**目的**: 驗證 phase58_bullpen_usage schema 的 PIT 安全性  
**基於**: Phase 56 的 `mlb_bullpen_pit_validator.py`（需更新欄位清單）  
**新增驗證**:
- `snapshot_date < game_date`
- `doubleheader_game_num` 合法值 (0, 1, 2)
- `availability_components` 各子項目 bool 類型

### 58.5 — 產出 MLB 2025 Bullpen Usage JSONL

**目的**: 執行完整 backfill，產出 `mlb_2025_bullpen_usage_phase58.jsonl`  
**Script**: `scripts/run_phase58_bullpen_backfill.py`  
**參數**: `--dry-run`, `--force`, `--print`, `--json`  
**預期行數**: 2,025

### 58.6 — 注入 Phase56 Bullpen Context（更新版）

**目的**: 用 Phase58 真實資料替換 Phase56 的 neutral fallback  
**Script**: `scripts/run_phase58_inject_bullpen_usage.py`  
**輸入**: `mlb_2025_bullpen_usage_phase58.jsonl` + Phase52 context JSONL  
**輸出**: `mlb_2025_per_game_predictions_phase58_sp_bullpen_context_v1.jsonl`

### 58.7 — 重跑 Phase49 / Phase45 / Phase54 Audit

**目的**: 確認 bullpen 資料注入後不影響既有 SP feature 穩定性  
**必跑**:
- Phase 45: Model Value Attribution
- Phase 49: Feature Repair Evaluation
- Phase 54: Safe SP Stability Audit

### 58.8 — Gate Decision

**目的**: 重跑 Phase56 evaluation orchestrator，決定最終 gate  
**輸入**: baseline JSONL + phase58 injected JSONL  
**Gate 選項（ONLY these 4）**:

| Gate | 觸發條件 |
|------|----------|
| `BULLPEN_FEATURE_EFFECTIVE_PAPER_ONLY` | availability >= 80% AND ECE/BSS 均改善 |
| `BULLPEN_FEATURE_NOT_EFFECTIVE` | availability >= 80% 但無改善 |
| `DATA_GAP_REMAINS` | availability < 80% |
| `COLLECT_MORE_DATA` | 樣本不足 (<100) |

---

## 10. 禁止事項清單（本 Phase 57）

| 禁止行為 | 原因 |
|----------|------|
| 串接 production API | Blueprint only |
| 建立 candidate patch | `CANDIDATE_PATCH_CREATED = False` |
| 修改 betting model | `PRODUCTION_MODIFIED = False` |
| 調整 alpha / ensemble | 超出本 Phase 範圍 |
| 宣稱 performance improvement | 無實際資料驗證 |
| 使用當場 box score / home_win | Leakage violation |
| 使用同日更早比賽結果 | PIT violation（doubleheader） |
| 使用 closing odds after game | Post-game data leakage |

---

## 11. 完成標準

Phase 57 (Blueprint) 完成標準：

| 項目 | 標準 |
|------|------|
| Blueprint 文件產出 | ✅ 本文件 |
| 資料來源評估 | ✅ 4+ 個來源，含優先度評分 |
| Schema 設計 | ✅ 完整 JSON schema，含所有 required fields |
| PIT safety rules | ✅ 明確定義，含 edge cases |
| Backfill strategy | ✅ 9 步驟流程，含 edge case 處理 |
| Validation plan | ✅ 含目標 availability >= 80% |
| Phase 58 tasks | ✅ 8 個任務，含介面設計 |
| `CANDIDATE_PATCH_CREATED` | `False` ✅ |
| `PRODUCTION_MODIFIED` | `False` ✅ |

---

```
PHASE_57_BULLPEN_USAGE_DATA_BLUEPRINT_VERIFIED
```
