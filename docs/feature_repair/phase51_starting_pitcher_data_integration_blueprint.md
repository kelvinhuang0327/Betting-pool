# Phase 51 — Starting Pitcher Data Integration Blueprint

**報告日期**: 2026-05-05  
**版本**: v1.0  
**狀態**: BLUEPRINT（規劃文件，不含 production patch）  
**作者**: Betting-pool Research System  

---

## 1. Executive Summary

Phase 50 的 P0 Feature Injection 結果顯示 `feature_effect_mode = MODEL_AFFECTING`，但
`gate = FEATURE_REPAIR_NOT_EFFECTIVE`，核心原因是：

- **sp_fip_delta availability = 0%**（所有 2,025 行均為 neutral fallback）
- park_run_factor / season_game_index 有效但影響幅度極小（mean_abs_adjustment = 0.000003）
- adjusted_rate 僅 0.9%，代表注入的特徵幾乎未發揮作用

本 Phase 51 Blueprint 定義「如何補齊先發投手資料」，使 Phase 52 能讓
sp_fip_delta availability ≥ 80%，實質性地提升 P0 feature injection 的影響力。

**本文件為純規劃 Blueprint，禁止：**

- 串接 production API
- 建立 production patch
- 修改 betting model 或 alpha 值
- 宣稱 performance improvement
- 進行 ensemble 或重新訓練

---

## 2. Why Phase 50 Was Not Effective

### 2.1 Root Cause 分析

| 症狀 | 根因 |
|---|---|
| `sp_fip_delta_available = False` for all 2,025 rows | mlb_p0_feature_builder.py 的 sp_fip source 永遠回傳 `neutral_fallback` |
| adjusted_rate = 0.9% | 只有 park_run_factor > 1.05 且 prob > 0.60 的 18 行被調整 |
| mean_abs_adjustment ≈ 0 | FIP 貢獻 = 0，park/season 調整量極微 |
| delta_bss = -0.000003 | 幾乎沒有差異 |

### 2.2 sp_fip_delta 在 Phase 48 的狀態

```
# 每行 p0_features.audit_notes 顯示：
"sp_fip_source": "neutral_fallback"

# 代表：
sp_fip_delta = 0.0
sp_fip_delta_available = False
```

Phase 48 的 feature builder (`mlb_p0_feature_builder.py`) 在計算 `sp_fip_delta` 時，
找不到對應 pitcher 的 FIP 統計數據，全部退回 neutral_fallback (0.0)。

### 2.3 現有資料庫的覆蓋差距

| 資料來源 | 覆蓋範圍 | 缺失 |
|---|---|---|
| `data/mlb_2024_pitchers.py` | ~40 位頂級先發投手，僅含 ERA/WHIP/K9 | 無 FIP/xFIP/BB9/HR9，無 pitcher_id |
| `data/mlb_2025_preview.py` | 球隊層級 ELO/RPG/ERA，無個人投手 | 完全無先發投手個人 stats |
| `data/mlb_2025/mlb-2025-asplayed.csv` | 2,430 行，含 home_starter/away_starter **姓名** | 有先發投手姓名但無 FIP stats |
| `data/mlb_context_sources/confirmed_lineups.jsonl` | 2,370 行，含 confirmed_home/away_starter | 有先發投手姓名但無 FIP stats |
| `data/mlb_player_stats.py` | 有 `fetch_probable_starters(date)` API | 需即時 API 呼叫，非 backfill 模式 |

**關鍵發現**：
- `mlb-2025-asplayed.csv` 與 baseline JSONL 匹配率 = **100%** (2,025/2,025 on game_date × home_team)
- 369 個唯一先發投手姓名已存在於 asplayed CSV
- 缺的是每位投手在 **賽前截止日期的 FIP 統計**

---

## 3. Why Starting Pitcher Data Is the Next Bottleneck

### 3.1 先發投手的預測力文獻依據

學術研究與業界共識表明，先發投手品質是預測單場勝率的最強個體變數：

- Tango / MGL 研究：SP FIP 對單場結果的影響幅度 = 3-5 個百分點 win probability
- ZiPS / Steamer 預測系統：SP 是最主要的 game-level adjustor
- 台灣運彩開盤算法：讓分盤通常最先反映先發投手變動

### 3.2 Phase 50 injection 調整規則的理論上限

```
# F-001 sp_fip_delta 調整規則（Phase 50 定義）：
# sp_fip_delta = away_sp_fip - home_sp_fip
# adjustment = tanh(delta * 0.5) * 0.003
# 單方向上限：~0.003（小於 total cap 0.025）

# 若 sp_fip_delta availability = 80%：
# 預期 adjusted_rate = 80%+ (vs. 現在 0.9%)
# 預期 mean_abs_adjustment = 0.001-0.003 (vs. 現在 0.000003)
```

### 3.3 機會成本

若 Phase 52 能補齊 sp_fip_delta，Phase 49 re-evaluation 可望：
- `feature_effect_mode` 維持 `MODEL_AFFECTING`
- `gate` 從 `FEATURE_REPAIR_NOT_EFFECTIVE` 升至 `FEATURE_REPAIR_EFFECTIVE_PAPER_ONLY`
- `sp_fip_triggered` 從 0 升至 ~1,600 rows

---

## 4. Data Source Options

### 4.1 候選資料來源評估

#### Option A: MLB Stats API（強烈推薦）

| 屬性 | 評估 |
|---|---|
| **可取得欄位** | ERA, WHIP, K, BB, HR, IP, K9, BB9, H9, ERA+（需自行計算 FIP） |
| **免費** | ✅ 完全免費，無需 API Key |
| **穩定性** | ✅ 官方 API，穩定性高 |
| **Rate Limit** | 建議 1 req/sec，無官方上限但請勿濫用 |
| **Point-in-time** | ✅ 可指定 season + hydrate=stats，用 `asOfDate` param 截點 |
| **Production 適用** | ✅ 已有 `fetch_probable_starters()` 在 `mlb_player_stats.py` |
| **Research 適用** | ✅ 可批次抓取歷史賽季數據 |
| **Base URL** | `https://statsapi.mlb.com/api/v1` |
| **關鍵 Endpoint** | `/people/{playerId}/stats?stats=season&season=2025&sportId=1` |
| **FIP 計算** | 需用 `(13×HR + 3×(BB+HBP) - 2×K) / IP + FIP_const` 自行計算（已在 mlb_player_stats.py 實作） |
| **缺點** | 需將投手姓名轉換為 player_id（需額外 lookup step） |

**推薦等級：⭐⭐⭐⭐⭐（首選）**

---

#### Option B: Pybaseball（FanGraphs 爬取）

| 屬性 | 評估 |
|---|---|
| **可取得欄位** | FIP, xFIP, K9, BB9, HR9, BABIP, LOB%, GB%, K%, BB%, ERA, WHIP |
| **免費** | ✅ 開源套件，爬 FanGraphs |
| **穩定性** | ⚠️ 依賴 FanGraphs 網站結構，有時 break |
| **Rate Limit** | ⚠️ 無官方 limit，但 FanGraphs 不歡迎高頻爬取 |
| **Point-in-time** | ⚠️ 只有 season-level，無法指定截止日 |
| **Production 適用** | ⚠️ 不建議（穩定性、point-in-time 問題） |
| **Research 適用** | ✅ 適合 offline backfill 和研究 |
| **安裝** | `pip install pybaseball` |
| **用法** | `from pybaseball import pitching_stats; df = pitching_stats(2025)` |
| **優點** | 直接提供 FIP/xFIP，省去自行計算 |
| **缺點** | 非 point-in-time；中途 break；依賴外部網站 |

**推薦等級：⭐⭐⭐（Backfill 研究用可接受）**

---

#### Option C: Baseball Savant / Statcast

| 屬性 | 評估 |
|---|---|
| **可取得欄位** | xFIP, xERA, EV, LA, Spin Rate, Barrel%, Stuff+, Location+ |
| **免費** | ✅ 免費 |
| **穩定性** | ✅ MLB 官方 Statcast，穩定性高 |
| **Rate Limit** | ⚠️ 需控制頻率，建議 2-3 req/sec |
| **Point-in-time** | ✅ 可指定 start_dt / end_dt |
| **Production 適用** | ✅ 穩定，但資料量大 |
| **Research 適用** | ✅ 最佳資料品質 |
| **Base URL** | `https://baseballsavant.mlb.com/statcast_search/csv` |
| **pybaseball 整合** | `statcast_pitcher(start_dt, end_dt, player_id)` |
| **缺點** | Pitch-level 資料非常大，需聚合到 season-level |

**推薦等級：⭐⭐⭐⭐（Phase 53+ 深度研究）**

---

#### Option D: FanGraphs API（直接）

| 屬性 | 評估 |
|---|---|
| **可取得欄位** | FIP, xFIP, SIERA, K/9, BB/9, HR/9, Stuff+ |
| **免費** | ✅ 基本查詢免費 |
| **穩定性** | ⚠️ 非官方 API，可能 break |
| **Rate Limit** | ⚠️ 需自行節流 |
| **Point-in-time** | ⚠️ 較困難，season stats 為累積值 |
| **推薦等級** | ⭐⭐（備用） |

---

### 4.2 Phase 52 推薦資料來源組合

```
Primary:   MLB Stats API       → pitcher_id lookup + season stats (FIP 自行計算)
Fallback:  pybaseball           → FanGraphs FIP 補充 (offline research only)
Future:    Baseball Savant      → Phase 53+ xFIP / Stuff+ 進階特徵
```

---

## 5. Schema Design

### 5.1 Starting Pitcher Feature Record Schema

```json
{
  "game_id": "MLB2025_0405_2025-04-27_TOR_NEW",
  "game_date": "2025-04-27",
  "home_team": "New York Yankees",
  "away_team": "Toronto Blue Jays",
  
  "home_probable_pitcher_id": 670770,
  "away_probable_pitcher_id": 666201,
  "home_probable_pitcher_name": "Gerrit Cole",
  "away_probable_pitcher_name": "Kevin Gausman",
  
  "home_sp_fip":  3.41,
  "away_sp_fip":  3.28,
  "home_sp_xfip": 3.55,
  "away_sp_xfip": 3.35,
  "home_sp_k9":   9.40,
  "away_sp_k9":   9.80,
  "home_sp_bb9":  2.10,
  "away_sp_bb9":  1.90,
  "home_sp_hr9":  1.20,
  "away_sp_hr9":  0.90,
  "home_sp_era":  3.41,
  "away_sp_era":  3.28,
  "home_sp_whip": 1.13,
  "away_sp_whip": 1.05,
  "home_sp_ip":   45.2,
  "away_sp_ip":   52.0,
  
  "sp_fip_delta": -0.13,
  "sp_fip_delta_available": true,
  
  "stats_cutoff_date": "2025-04-26",
  "data_timestamp": "2025-04-27T08:30:00Z",
  "probable_pitcher_confirmed_at": "2025-04-27T06:00:00Z",
  "first_pitch_time_utc": "2025-04-27T17:05:00Z",
  
  "source": "mlb_stats_api",
  "point_in_time_safe": true,
  "point_in_time_validation": {
    "stats_cutoff_before_game": true,
    "pitcher_confirmed_before_first_pitch": true,
    "no_post_game_fields": true,
    "scratched_pitcher_handled": false
  },
  
  "fallback_reason": null,
  "scratched_pitcher_event": null,
  
  "audit_hash": "sha256_of_game_id_plus_pitcher_ids_plus_fip_values"
}
```

### 5.2 Nullable 欄位規則

| 欄位 | Nullable | 原因 |
|---|---|---|
| `home_probable_pitcher_id` | No（若 available） | Key identifier |
| `home_sp_fip` | Yes | 若 IP < 5 則資料不穩定 |
| `home_sp_xfip` | Yes | xFIP 需額外計算 |
| `sp_fip_delta` | No | 缺資料時 = 0.0 且 available = false |
| `probable_pitcher_confirmed_at` | Yes | 部分資料來源無此欄位 |
| `scratched_pitcher_event` | Yes | 正常情況為 null |

### 5.3 sp_fip_delta 計算定義

```python
# sp_fip_delta = away_sp_fip - home_sp_fip
#
# 正值：away SP FIP 較高 → away 投手較差 → home 優勢 → 輕微加強 home prob
# 負值：home SP FIP 較高 → home 投手較差 → away 優勢 → 輕微降低 home prob
# 零值：持平或無資料

sp_fip_delta = away_sp_fip - home_sp_fip  # if both available
sp_fip_delta = 0.0                          # fallback
sp_fip_delta_available = both_fips_available
```

### 5.4 FIP 計算公式

```python
FIP_CONSTANT = 3.10  # 2024 MLB league average

def compute_fip(hr: int, bb: int, hbp: int, k: int, ip: float) -> float | None:
    if ip < 5.0:
        return None  # insufficient sample
    return (13 * hr + 3 * (bb + hbp) - 2 * k) / ip + FIP_CONSTANT
```

---

## 6. Point-in-Time Safety Design

### 6.1 核心原則

**任何用於預測的數據，都必須是「比賽開始前可以合法獲得的資訊」。**

違反此原則即為 **Look-ahead Leakage**，會導致回測結果虛高、無法在真實環境中複製。

### 6.2 允許使用的資料

| 類型 | 說明 | 截止條件 |
|---|---|---|
| 先發投手 FIP | 截至 `game_date - 1` 的賽季累積 FIP | `stats_cutoff_date < game_date` |
| 先發投手名單 | 比賽前公布的 probable pitcher | `confirmed_at < first_pitch_time` |
| 球場因子 | 靜態年度 park factor（無時間性問題） | N/A（靜態） |
| 先發投手 IP | 截至 `game_date - 1` 的賽季累積 IP | `stats_cutoff_date < game_date` |

### 6.3 禁止使用的資料（Forbidden Fields）

```python
_FORBIDDEN_FIELDS = frozenset({
    "home_win",          # 比賽結果
    "final_score",       # 比賽結果
    "home_score",        # 比賽結果
    "away_score",        # 比賽結果
    "result",            # 比賽結果
    "closing_odds_after_game",  # 收盤後賠率
    "post_game_stats",   # 比賽後統計
    "actual_starter",    # 實際出賽先發（vs. probable）
    "innings_pitched_today",  # 當場 IP
    "game_score",        # 當場分數
})
```

### 6.4 Probable Pitcher 處理規則

```
情境 1：Probable pitcher 賽前確認，比賽正常進行
  → 使用 confirmed probable pitcher 的截止日 FIP
  → point_in_time_safe = True

情境 2：Probable pitcher 在賽前 scratched（臨時換投）
  → 若在 first_pitch 前收到更新：使用新投手 FIP（若有）
  → 若無新投手 FIP：使用 neutral fallback，sp_fip_delta_available = False
  → scratched_pitcher_event = {"original": name, "replacement": name, "event_time": UTC}
  → point_in_time_safe = True（因為使用了最新可用資訊）

情境 3：回測時無法確認 scratch 時間點
  → 使用 asplayed 資料中的 actual_starter 姓名，但標記為 point_in_time_safe = False
  → 此類行在 Phase 52 backfill 中需特別處理

情境 4：Probable pitcher 資料完全缺失
  → sp_fip_delta = 0.0, sp_fip_delta_available = False
  → fallback_reason = "no_probable_pitcher_data"
```

### 6.5 Stats Cutoff 驗證邏輯

```python
def validate_point_in_time(record: dict) -> bool:
    """
    驗證先發投手統計是否為 point-in-time safe。
    
    規則：
    - stats_cutoff_date < game_date（嚴格小於）
    - probable_pitcher_confirmed_at < first_pitch_time_utc
    - 不含任何 forbidden fields
    """
    cutoff = date.fromisoformat(record["stats_cutoff_date"])
    game_date = date.fromisoformat(record["game_date"])
    
    if cutoff >= game_date:
        return False  # 使用了當日或賽後統計
    
    if record.get("probable_pitcher_confirmed_at") and record.get("first_pitch_time_utc"):
        confirmed = datetime.fromisoformat(record["probable_pitcher_confirmed_at"])
        first_pitch = datetime.fromisoformat(record["first_pitch_time_utc"])
        if confirmed >= first_pitch:
            return False  # 先發投手名單在開球後才確認
    
    for field in _FORBIDDEN_FIELDS:
        if field in record and record[field] is not None:
            return False
    
    return True
```

---

## 7. Backfill 計畫

### 7.1 目標

對 2,025 baseline JSONL rows 建立對應的 starting pitcher feature 檔案：

```
data/mlb_2025/derived/mlb_2025_starting_pitcher_features_phase52.jsonl
```

### 7.2 現有資料優勢

**關鍵發現**（Phase 51 探勘結果）：

- `data/mlb_2025/mlb-2025-asplayed.csv` 包含 2,430 行，含 `home_starter` / `away_starter` 姓名
- baseline JSONL 2,025 行 **100% 可對齊** asplayed（game_date × home_team 聯合鍵）
- 369 個唯一先發投手已識別

### 7.3 Backfill 流程設計

```
Step 1: 建立 Pitcher Name → MLB StatsAPI pitcher_id lookup table
  Input:  369 unique pitcher names from asplayed CSV
  Output: name_to_id.json (姓名 → player_id 對照表)
  方法:   MLB StatsAPI /people?search=name 或 /teams/{team}/roster
  注意:   同名球員需用球隊/年份區分

Step 2: 批次抓取截止日 FIP 統計
  For each game (2,025 rows):
    cutoff_date = game_date - 1 day
    pitcher_ids = [home_pitcher_id, away_pitcher_id]
    For each pitcher_id:
      stats = mlb_stats_api.pitcher_season_stats(
          player_id=pitcher_id,
          season=2025,
          as_of_date=cutoff_date  # point-in-time safe
      )
      fip = compute_fip(stats)
  Rate: 1 req/sec, 估計耗時 ~15 分鐘

Step 3: 計算 sp_fip_delta
  sp_fip_delta = away_sp_fip - home_sp_fip
  sp_fip_delta_available = both fips are not None

Step 4: Point-in-time validation
  validate_point_in_time(record) → True/False

Step 5: 寫出 JSONL
  每行對應一個 game_id
  含完整 schema（見 §5.1）

Step 6: 產出匹配報告
  match_rate, missing_rate, duplicate_handling_summary
  fip_coverage_rate
  point_in_time_safe_rate
  audit_hash_coverage
```

### 7.4 Join 鍵策略

```python
# Primary join key（已確認 100% 覆蓋）
join_key = (game_date, home_team_full_name)

# Dedup strategy（同一場次多行時）
# baseline 存在重複 game_id（如 MLB2025_0405/0406 同 date+team）
# 使用 game_id 做最終區分，若多個 asplayed 行符合，取第一個
dedup_policy = "first_match_per_game_id"

# Missing handler
missing_policy = {
    "no_pitcher_id": "fallback_to_name_search",
    "no_fip_data": "use_neutral_fallback_sp_fip_delta_0.0",
    "ip_lt_5": "use_neutral_fallback",
    "scratched_pitcher": "use_replacement_if_available_else_fallback",
}
```

### 7.5 Duplicate Handling

```python
# 若同 (game_date, home_team) 有多筆 asplayed 記錄（雙重頭）
duplicate_strategy:
  1. 若 game_id 可區分 → 分別對應
  2. 若 game_id 無法區分 → 取 innings_pitched 最高者（確認為當日真實先發）
  3. 所有 duplicates 記錄於 backfill_audit_log.jsonl
```

### 7.6 預期輸出檔案

```
data/mlb_2025/derived/
  mlb_2025_starting_pitcher_features_phase52.jsonl   # 主要輸出 (2,025 行)
  mlb_2025_pitcher_name_to_id.json                   # 姓名 → player_id 對照表
  mlb_2025_backfill_audit_log.jsonl                  # backfill 過程稽核紀錄
```

---

## 8. Validation Plan

Phase 52 完成後需通過以下所有驗證 gate：

### 8.1 覆蓋率 Gates

| 指標 | 目標 | 說明 |
|---|---|---|
| `sp_fip_delta availability` | **≥ 80%** | Phase 50 目前為 0%，此為最關鍵 gate |
| `pitcher_id match rate` | **≥ 80%** | 姓名對 player_id 轉換成功率 |
| `fip_computed_rate` | **≥ 70%** | 有足夠 IP 可計算 FIP 的比率 |
| `backfilled_rows` | **= 2,025** | 必須涵蓋所有 baseline rows |
| `audit_hash_present_rate` | **= 100%** | 每行必須有 audit hash |
| `point_in_time_safe_rate` | **≥ 95%** | 必要的品質下限 |

### 8.2 Leakage 防護驗證

```python
# Phase 52 leakage guard test
def test_no_leakage_in_sp_features():
    """先發投手 feature 文件不應含任何 forbidden fields."""
    forbidden = {"home_win", "final_score", "home_score", "away_score",
                 "result", "closing_odds_after_game", "actual_starter_ip_today"}
    with open("data/mlb_2025/derived/mlb_2025_starting_pitcher_features_phase52.jsonl") as f:
        for line in f:
            row = json.loads(line)
            for field in forbidden:
                assert field not in row or row[field] is None, f"Leakage: {field}"
```

### 8.3 End-to-End Re-evaluation Gates

完成 Phase 52 backfill 後，重新執行 Phase 48 → Phase 49 → Phase 50 管線：

| 管線步驟 | 預期結果 | 當前結果（對照） |
|---|---|---|
| Phase 48 rebuild | sp_fip_delta_available ≥ 80% | 0% |
| Phase 49 evaluation | `feature_effect_mode = MODEL_AFFECTING` | `REPORT_ONLY` → 此為正確 |
| Phase 50 injection | adjusted_rate ≥ 60% | 0.9% |
| Phase 50 gate | `FEATURE_REPAIR_EFFECTIVE_PAPER_ONLY` | `FEATURE_REPAIR_NOT_EFFECTIVE` |
| Phase 45 attribution | sp_fip_delta attribution ≥ 0.001 | 未計算 |

### 8.4 Phase 45 Model Value Attribution 重新執行

Phase 52 完成後需更新 Phase 45 attribution 報告：
- sp_fip_delta 應顯示非零 attribution
- 特徵重要性排名應更新

---

## 9. Phase 52 Implementation Tasks

### 52.1 Starting Pitcher Data Loader

**檔案**: `data/mlb_sp_data_loader.py`

```python
# 功能：
# - load_asplayed_starters(csv_path) → DataFrame
# - fetch_pitcher_season_stats_as_of(player_id, season, cutoff_date) → dict
# - compute_fip(stats) → float | None
# - build_sp_feature_record(game_record, home_stats, away_stats) → dict
```

**注意**：繼承 `mlb_player_stats.py` 的 FIP 計算邏輯，避免重複實作。

---

### 52.2 Pitcher Stat Snapshot Builder

**檔案**: `wbc_backend/features/mlb_sp_stat_snapshot.py`

```python
# 功能：
# - build_snapshot(pitcher_id, season, cutoff_date) → PitcherStatSnapshot
# - PitcherStatSnapshot: fip, xfip, k9, bb9, hr9, era, whip, ip, sample_size_ok
# - Cache: TTL=6h for live, permanent for historical backfill
```

---

### 52.3 Point-in-Time Safety Validator

**檔案**: `wbc_backend/features/mlb_pit_validator.py`

```python
# 功能：
# - validate_pit_safety(sp_record) → ValidationResult
# - ValidationResult: is_safe, violations, warnings
# - 實作 §6.5 validate_point_in_time() 邏輯
```

---

### 52.4 Backfill 2025 Rows

**Script**: `scripts/run_phase52_sp_backfill.py`

```
流程：
  1. 讀取 baseline JSONL (2,025 rows)
  2. Join asplayed CSV → 取得 home/away starter 姓名
  3. 呼叫 mlb_stats_api → 取得 pitcher_id
  4. 批次抓取截止日 FIP (rate_limit=1/s)
  5. 計算 sp_fip_delta
  6. 執行 point-in-time validation
  7. 寫出 starting_pitcher_features_phase52.jsonl
  8. 產出匹配率 / 覆蓋率報告
```

---

### 52.5 注入 Phase 48 Context

**Script**: `scripts/run_phase52_inject_to_phase48.py`

```
流程：
  1. 讀取 phase48 JSONL
  2. 讀取 sp_features_phase52.jsonl
  3. Join on game_id
  4. 更新 p0_features.sp_fip_delta 和 sp_fip_delta_available
  5. 重新計算 feature_audit_hash
  6. 寫出新的 phase48_with_sp_v2.jsonl
```

---

### 52.6 Rerun Phase 49 / Phase 50 / Phase 45

```bash
# Step 1: Phase 49 re-evaluation (baseline vs phase48_with_sp_v2)
python scripts/run_phase49_feature_repair_evaluation.py \
  --phase48-path data/mlb_2025/derived/mlb_2025_per_game_predictions_phase48_with_sp_v2.jsonl

# Step 2: Phase 50 re-injection
python scripts/run_phase50_p0_feature_injection.py --print --json --report

# Step 3: Phase 45 attribution update
python scripts/run_phase45_model_value_attribution.py
```

**預期 gate 變化**：
- Phase 49：`FEATURE_INJECTION_REQUIRED` 維持（MODEL_AFFECTING 模式）
- Phase 50：`FEATURE_REPAIR_EFFECTIVE_PAPER_ONLY`（若 BSS 改善）
- Phase 45：sp_fip_delta attribution 非零

---

## 10. 禁止事項（Phase 51 Hard Rules）

本 Phase 為純 Blueprint，以下操作**嚴格禁止**：

| 禁止事項 | 原因 |
|---|---|
| ❌ 串接 production API 進行即時預測 | Phase 51 為規劃，不修改 production |
| ❌ 修改 betting model / alpha 值 | alpha = 0.4 不可調整 |
| ❌ ensemble 或重新訓練模型 | 無重新訓練規則 |
| ❌ 宣稱 performance improvement | 尚未有實驗數據 |
| ❌ 建立 production patch | `CANDIDATE_PATCH_CREATED = False` |
| ❌ 修改 production 任何檔案 | `PRODUCTION_MODIFIED = False` |
| ❌ 使用賽後數據 | leakage guard 嚴格執行 |

---

## 11. 附錄：現有資料盤點結果

### 11.1 asplayed CSV 先發投手覆蓋率

```
data/mlb_2025/mlb-2025-asplayed.csv:
  total_rows = 2,430
  rows_with_home_starter = 2,430 (100%)
  rows_with_away_starter = 2,430 (100%)
  unique_starters = 369

baseline JSONL match rate:
  total_baseline_rows = 2,025
  matched_to_asplayed = 2,025 (100%)
  join_key = (game_date, home_team)
```

### 11.2 mlb_player_stats.py 現有功能

已實作（Phase 8B）：
- `fetch_pitcher_season_stats(player_id)` → MLB StatsAPI
- `fetch_probable_starters(date)` → date 當日先發投手
- `compute_fip()` 計算邏輯
- TTL cache（pitcher stats = 6h，schedule = 1h）

**Phase 52 需要新增**：
- `fetch_pitcher_season_stats_as_of(player_id, season, cutoff_date)` — 截止日 FIP
- `pitcher_name_to_id_batch(names)` — 批次姓名轉 ID
- `build_backfill_snapshot(game_date, home_pitcher, away_pitcher)` — 批次回填快照

### 11.3 confirmed_lineups.jsonl 覆蓋率

```
data/mlb_context_sources/confirmed_lineups.jsonl:
  total_rows = 2,370
  rows_with_confirmed_home_starter = 2,370 (100%)
  rows_with_confirmed_away_starter = 2,370 (100%)
```

此資料可作為 probable pitcher 的另一個來源，尤其適合 point-in-time 確認。

---

## 12. 驗證標記

```
PHASE_51_STARTING_PITCHER_DATA_INTEGRATION_BLUEPRINT_VERIFIED
blueprint_version=v1.0
phase=51
type=BLUEPRINT_ONLY
candidate_patch_created=False
production_modified=False
asplayed_match_rate=100%
unique_starters=369
primary_data_source=mlb_stats_api
fallback_data_source=pybaseball_fangraphs
phase52_tasks_defined=6
sp_fip_delta_availability_target>=80%
pitcher_id_match_rate_target>=80%
backfill_target_rows=2025
```
