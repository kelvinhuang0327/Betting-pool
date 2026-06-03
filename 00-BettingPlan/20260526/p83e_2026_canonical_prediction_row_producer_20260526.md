# P83E — 2026 Canonical Prediction Row Producer
**Date:** 2026-05-26
**Classification:** `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA`
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## 摘要

P83E 嘗試產生 canonical 2026 預測資料列。重新確認 P83D 閘門後，
三個必要的上游檔案仍然不存在於本地檔案系統 → 不寫入 canonical rows。
Producer 邏輯已完整實作，以 in-memory mock fixture 驗證所有計算邏輯。

**最終分類：** `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA`

---

## STOP 條件觸發原因

| 必要上游檔案 | 狀態 |
|---|---|
| data/mlb_2026/schedule/mlb_2026_schedule.jsonl | ❌ 缺失 |
| data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl | ❌ 缺失 |
| data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl | ❌ 缺失 |

---

## sp_fip_delta 計算慣例（P83C 合約）

- `sp_fip_delta = home_sp_fip - away_sp_fip`
- 正值 → home 投手佔優（系統慣例）
- `predicted_side = 'home' if sp_fip_delta > 0 else 'away'`
- 平局（delta == 0）從 canonical 輸出中排除

---

## 規則旗標計算（全部通過 P83C 5 個驗證案例）

| 旗標 | 條件 |
|---|---|
| rule_primary_125_flag | home: abs >= 0.50 OR away: abs >= 1.25 |
| rule_shadow_100_flag | home: abs >= 0.50 OR away: abs >= 1.00 |
| tier_b_candidate_flag | 0.25 <= abs < 0.50 |
| tier_a_watchlist_flag | abs < 0.25 |

---

## Canonical Row Schema（P83B/P83C）

必要欄位 19 個：
game_id, game_date, season, home_team, away_team,
sp_fip_delta, abs_sp_fip_delta, model_probability,
predicted_side, source_prediction_version,
rule_primary_125_flag, rule_shadow_100_flag,
tier_b_candidate_flag, tier_a_watchlist_flag,
paper_only, diagnostic_only, odds_used,
market_edge_evaluated, production_ready

---

## 重新執行觸發條件

當以下 3 個檔案全部在本地存在時重新執行 P83E：
1. `data/mlb_2026/schedule/mlb_2026_schedule.jsonl`
2. `data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl`
3. `data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl`

---

## 治理不變量

- paper_only: True | diagnostic_only: True | live_api_calls: 0
- odds_used: False | ev_calculated: False | clv_calculated: False
- kelly_calculated: False | production_ready: False
- canonical_rows_written: False | forbidden_scan_pass: True
