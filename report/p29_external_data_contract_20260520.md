# P29 External Data Contract Design
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true  
**no_data_fetched**: true（設計文件，無實際 API 呼叫）

---

## 背景

當前 Brier ceiling ≈ 0.244（使用 CSV 市場賠率資料）。  
突破此天花板需要外部 pitcher/batting/bullpen 資料。  
本文件為資料合約設計規格，**不含任何實際資料擷取**。

---

## Contract 1：Starting Pitcher

**目的**：提供先發投手品質與近況信號  
**估計 Brier 改善**：-0.005 至 -0.015  
**Priority**：HIGHEST

| Field | Type | Nullable | Fallback | Leakage Risk |
|-------|------|----------|----------|-------------|
| pitcher_name | str | No | UNKNOWN | MEDIUM |
| pitcher_hand | str | Yes | UNKNOWN | LOW |
| season_era | float | Yes | 4.20（聯盟平均） | **HIGH** |
| season_fip | float | Yes | 4.20 | **HIGH** |
| last3_era | float | Yes | season_era | **HIGH** |
| days_rest | int | Yes | 5 | LOW |
| pitch_count_last | int | Yes | 90 | LOW |
| injury_flag | bool | No | False | MEDIUM |
| snapshot_ts | str | No | N/A | NONE |

**反 Leakage 規則**：
- `season_era`/`season_fip` 必須用 date < game_date 的賽事計算
- `last3_era` 必須排除今日賽事
- `injury_flag` 必須在 bet 截止時間前確認

**免費資料來源**：
- MLB Stats API (https://statsapi.mlb.com) — 官方，免費
- FanGraphs season stats (CSV download，研究用)
- Baseball Reference

---

## Contract 2：Bullpen

**目的**：捕捉牛棚疲勞與可用性  
**估計 Brier 改善**：-0.002 至 -0.007

| Field | Type | Nullable | Fallback | Leakage Risk |
|-------|------|----------|----------|-------------|
| bullpen_ip_1d | float | No | 0.0 | LOW |
| bullpen_ip_3d | float | No | 3.0 | LOW |
| bullpen_ip_7d | float | No | 7.0 | LOW |
| closer_available | bool | No | True | MEDIUM |
| fatigue_score | float | Yes | 0.5 | LOW |
| season_bullpen_era | float | Yes | 4.10 | **HIGH** |
| snapshot_ts | str | No | N/A | NONE |

**反 Leakage 規則**：
- IP counts 必須排除今日賽事
- `closer_available` 是即時信號，回測困難

---

## Contract 3：Batting Form

**目的**：滾動打擊狀態補充季度平均值  
**估計 Brier 改善**：-0.003 至 -0.010

| Field | Type | Nullable | Fallback | Leakage Risk |
|-------|------|----------|----------|-------------|
| team_woba_season | float | Yes | 0.317 | **HIGH** |
| team_woba_7d | float | Yes | team_woba_season | **HIGH** |
| team_woba_14d | float | Yes | team_woba_season | **HIGH** |
| team_k_pct | float | Yes | 0.228 | **HIGH** |
| team_bb_pct | float | Yes | 0.085 | **HIGH** |
| vs_hand_split | str | Yes | null | HIGH |
| snapshot_ts | str | No | N/A | NONE |

**反 Leakage 規則**：
- 所有滾動窗口必須排除今日賽事
- `vs_hand_split` 需要 SP 手性已知（賽前）

---

## Contract 4：Lineup / Injury Proxy

**目的**：捕捉陣容完整性與傷兵不確定性  
**估計 Brier 改善**：-0.002 至 -0.006（高不確定性）

| Field | Type | Nullable | Fallback | Leakage Risk |
|-------|------|----------|----------|-------------|
| confirmed_lineup_flag | bool | No | False | MEDIUM |
| missing_key_bats | int | No | 0 | **HIGH** |
| injury_uncertainty | float | No | 0.0 | **HIGH** |
| stale_lineup_flag | bool | No | True | LOW |
| snapshot_ts | str | No | N/A | NONE |

**反 Leakage 規則**：
- 絕不使用賽後傷兵更新
- `confirmed_lineup_flag` 只有在官方名單提交後才設 True

---

## Contract 5：Park / Weather

**目的**：球場與天氣對得分環境的調整  
**估計 Brier 改善**：-0.001 至 -0.003

| Field | Type | Nullable | Fallback | Leakage Risk |
|-------|------|----------|----------|-------------|
| park_factor_runs | float | No | 100.0 | LOW |
| wind_mph | float | Yes | 0.0 | LOW |
| wind_direction | str | Yes | CALM | LOW |
| temperature_f | float | Yes | 72.0 | LOW |
| roof_status | str | Yes | OUTDOOR | LOW |
| snapshot_ts | str | No | N/A | NONE |

**反 Leakage 規則**：
- `park_factor` 只用歷史賽季（前 5 年平均）
- Weather 必須是預報值（非實際值）

---

## 資料取得方案評估

| 資料 | 免費來源 | 歷史回測可行 | 工程複雜度 |
|------|---------|------------|----------|
| SP stats | MLB API / FanGraphs | ✅ YES | LOW-MEDIUM |
| Bullpen IP | MLB Stats API | ✅ YES | LOW |
| Batting form | FanGraphs / BRef | ✅ YES | MEDIUM |
| Lineup/Injury | MLB API / Rotoworld | ⚠️ PARTIAL | HIGH |
| Park factor | FanGraphs (stable) | ✅ YES | LOW |
| Weather | NWS API / OWM | ❌ Historical costly | MEDIUM |

---

## 絕對禁止使用的資料

1. 今日賽事的賽後統計（ERA/H/ER）
2. 作為賽前特徵的 closing odds（未來資訊）
3. 投注截止後的陣容更新
4. 結果衍生欄位（勝率、得分差）
5. 未授權爬蟲的個人可識別資訊

---

## 結論

**資料合約完整性：P29_EXTERNAL_DATA_CONTRACT_READY**

優先實作順序：
1. **起始投手 ERA/FIP**（最高影響 -0.005 到 -0.015，免費資料，歷史可回測）
2. **牛棚疲勞 IP_7d**（容易計算，MLB API 免費）
3. **Park factor**（穩定，FanGraphs CSV，最低工程成本）
4. **Batting rolling wOBA**（需仔細處理滾動窗口）
5. **Lineup/Injury**（即時信號，回測困難，最後考慮）
