# P39 Report — 2024 MLB Holdout Dataset Build
**Date**: 2026-05-24  
**Phase**: P39 (data acquisition & feature build)  
**Precursor**: P38 `f5a846f` (DATA_UNAVAILABLE — 0/15 paths found)  
**Status**: ✅ COMPLETE — `HOLDOUT_READY`

---

## 1. Pre-flight Check

| 項目 | 狀態 |
|------|------|
| Branch | `main` |
| HEAD | `f5a846f` |
| Governance: `diagnostic_only` | `True` |
| Governance: `promotion_freeze` | `True` |
| Governance: `T_LOCKED` | `0.50` |
| Governance: `live_api_calls` | `0` |
| Governance: `no_champion_modification` | `True` |
| Dirty files (daemon writes) | 非 P39 相關，忽略 |

---

## 2. 資料來源

| 資料集 | 來源 | 授權 |
|--------|------|------|
| `gl2024.txt` | `https://www.retrosheet.org/gamelogs/gl2024.zip` | Retrosheet — 教育/研究免費 |
| `data/mlb_2023_pitchers.py` | 2023 MLB 賽季靜態 FIP 代理表（公開統計） | 本地靜態 |

**下載方式**: `curl -s -L --connect-timeout 15 --max-time 60` (非 live API，確定性靜態資料)

---

## 3. 新建/修改檔案

| 檔案 | 操作 | 說明 |
|------|------|------|
| `data/mlb_2025/gl2024.txt` | NEW | 2024 Retrosheet game log，2429 場賽局，161 欄 |
| `data/mlb_2025/gl2024.zip` | NEW | 原始 zip (465,932 bytes) |
| `data/mlb_2023_pitchers.py` | NEW | 2023 賽季 FIP 代理表，~160 先發投手 |
| `data/mlb_2025/mlb-2024-asplayed.csv` | NEW | 2429 場 2024 MLB 賽局（含 home_win, starters） |
| `data/mlb_2025/mlb-2024-asplayed.csv.metadata.json` | NEW | 資料來源 metadata 與 SHA-256 |
| `data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl` | NEW | 2429 筆特徵記錄 |
| `data/mlb_2025/derived/p39_2024_holdout_summary.json` | NEW | 完整摘要 JSON |
| `scripts/_p39_build_2024_holdout.py` | NEW | P39 主要建構腳本（7 段落） |
| `tests/test_p39_build_2024_holdout.py` | NEW | 34 個測試（6 類別） |

---

## 4. Game Log 解析結果

| 指標 | 值 |
|------|-----|
| 來源檔 | `gl2024.txt` |
| SHA-256 (前 16 chars) | `48bae769201e0b5b` |
| 解析列數 | **2,429 場賽局** |
| 欄位數 | 161 欄（符合 Retrosheet 標準） |
| 賽季範圍 | 2024-03-20 → 2024-11-02 |
| 編碼 | `latin1` |
| 關鍵欄位 | col 0=date, col 3=away_code, col 6=home_code, col 9=away_score, col 10=home_score, col 102=away_starter, col 104=home_starter |
| 首列驗證 | date=20240320, LAN(Dodgers) @ SDN(Padres), 5-2, Glasnow vs Darvish ✅ |

---

## 5. 2023 FIP 表建構結果

| 指標 | 值 |
|------|-----|
| 模組 | `data/mlb_2023_pitchers.py` |
| 投手數量（PITCHER_FIP_2023_CLEAN） | **160 位** |
| LG_FIP_2023 | 4.14 |
| FIP 代理公式 | `0.85 × raw_fip + 0.15 × 4.14` |
| FIP 值範圍 | [2.86, 4.84]（精英 Gerrit Cole → 低檔 Alek Manoah） |
| PIT 設計 | 2023 賽季（全部早於 2024 賽局）✅ |
| 命名格式 | ASCII 無音調符號（與 Retrosheet 一致） |
| 2024 新秀缺席 | Paul Skenes, Jared Jones, Cade Povich → 正確 fallback ✅ |
| NPB 轉換投手缺席 | Yoshinobu Yamamoto, Shota Imanaga → 正確 fallback ✅ |

**分級範例**：
- Elite (< 3.25): Cole(2.86), Snell(2.90), Sonny Gray(2.94), Framber Valdez(2.98)
- Strong (3.25–3.60): Corbin Burnes(3.39), Logan Gilbert(3.27), Zack Wheeler(3.48)
- Solid (3.60–4.00): Charlie Morton(3.69), Sandy Alcantara(3.97), Lance Lynn(3.99)
- Average (4.00–4.40): Max Fried(4.22), Jack Flaherty(4.21), German Marquez(4.38)
- Below avg (> 4.40): Carlos Rodon(4.75), Patrick Corbin(4.58), Jordan Lyles(4.82)

---

## 6. SP 名稱映射覆蓋率

| 指標 | 值 |
|------|-----|
| 2024 獨特先發投手 | **370 位** |
| FIP 表覆蓋 | **160 位 (43.2%)** |
| Fallback 投手數 | 210 位 (56.8%) |
| Fallback 原因 | 2024 新秀、2023 受傷缺賽、牛棚轉先發、小聯盟緊急徵召 |

**Fallback 樣本**（部分）: `A.J. Puk`, `AJ Smith-Shawver`, `Andrew Abbott`, `Cade Povich`, `Paul Skenes`, `Jared Jones`, `Yariel Rodriguez`, `Jonathan Cannon`, `Jordan Wicks` (2024 debut), `Yilber Diaz`

> **設計說明**：43.2% 直接覆蓋率看似偏低，但因 2024 有大量一次性先發（bulk relievers, emergency callups），這些人的 fallback 行為完全符合 P37 quality filter 設計（fallback → 被排除出 strong-edge 分析）。

---

## 7. sp_fip_delta 覆蓋率分析

| 指標 | 值 | P37 基準（2025 data）|
|------|----|---------------------|
| 總賽局 | 2,429 | 2,025 |
| Quality records (非 league_avg_fallback) | **2,158 (88.8%)** | 1,409 (69.6%) |
| Strong-edge (T≥0.50) | **955 (44.3%)** | 531 (37.7%) |
| WFV viable (≥150) | ✅ YES | ✅ YES |
| Strong-edge directional accuracy | **56.4%** | 60.8% |
| Source 分布 | historical_proxy=1117, mixed=1041, fallback=271 | — |
| sp_fip_delta 範圍 | [-1.82, +1.80] | — |
| sp_fip_delta mean | 0.009 | — |
| sp_fip_delta std | 0.606 | — |

**說明**：quality_records 包含 `historical_proxy`（兩位先發均在表中）及 `mixed`（一位在表中），與 P37 的 quality filter（排除 `league_average_fallback`）一致。

---

## 8. PIT 安全性稽核

| 指標 | 值 |
|------|-----|
| 總記錄數 | 2,429 |
| PIT 安全記錄 | **2,429 (100%)** |
| PIT 違規 | **0** |
| FIP 資料年份 | 2023 |
| 賽局資料年份 | 2024 |
| FIP 早於賽局 | ✅ 2023 < 2024 |
| Snapshot 政策 | `fip_data_year < game_year` |
| 未使用 live API | ✅ 確認 |

---

## 9. Holdout Dataset 整備分類

```
分類:    HOLDOUT_READY ✅
Strong-edge count: 955  (WFV 閾值 150 → ✅ 637% 超額)
WFV viable:        True
PIT safe:          True
Total games:       2,429
Quality records:   2,158 (88.8%)
T_LOCKED:          0.50
diagnostic_only:   True
promotion_freeze:  True
```

> **P38 retry 就緒條件**：所有必要資料現已建立，P38 可直接 retry 2024 WFV 驗證。

---

## 10. 測試結果

```
pytest tests/test_p39_build_2024_holdout.py -v
34 passed in 0.11s
```

| 測試類別 | 數量 | 結果 |
|----------|------|------|
| TestGl2024Exists（gl2024.txt 格式驗證） | 5 | ✅ 全過 |
| TestFip2023Table（2023 FIP 表驗證） | 7 | ✅ 全過 |
| TestAsplayedCsv（asplayed CSV schema） | 6 | ✅ 全過 |
| TestFeatureJsonl（特徵 JSONL 驗證） | 8 | ✅ 全過 |
| TestPitSafety（PIT 安全性） | 5 | ✅ 全過 |
| TestSummaryJson（摘要 JSON） | 3 | ✅ 全過 |

---

## 11. Forbidden 掃描

P39 白名單外無修改。Staged 檔案：
```
data/mlb_2023_pitchers.py                            (NEW)
data/mlb_2025/gl2024.txt                             (NEW)
data/mlb_2025/gl2024.zip                             (NEW)
data/mlb_2025/mlb-2024-asplayed.csv                  (NEW)
data/mlb_2025/mlb-2024-asplayed.csv.metadata.json    (NEW)
data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl (NEW)
data/mlb_2025/derived/p39_2024_holdout_summary.json  (NEW)
scripts/_p39_build_2024_holdout.py                   (NEW)
tests/test_p39_build_2024_holdout.py                 (NEW)
report/p39_2024_holdout_dataset_build_20260524.md    (NEW)
```

禁止項目檢查：
- No model changes ✅
- No threshold changes ✅
- No champion replacement ✅
- No live API calls ✅
- No branch/clone/worktree ✅

---

## 12. Commit Hash

```
（本次 P39 commit — 見下）
```

前驅 P38: `f5a846f`

---

## 13. 次 24h Prompt（P40 建議）

```
P40: 2024 Holdout WFV Validation — sp_fip_delta T=0.50 OOS
=============================================================
前提：P39 COMPLETE, HOLDOUT_READY
資料：data/mlb_2025/derived/mlb_2024_sp_fip_delta_features.jsonl (2429 records)
任務：
  1. 讀取 mlb_2024_sp_fip_delta_features.jsonl
  2. 套用 quality filter (sp_context_source != 'league_average_fallback')
  3. 套用 strong-edge filter (|sp_fip_delta| >= 0.50)
  4. 70/30 Walk-Forward Validation (WFV) 按 game_date 排序
  5. Train: LR / XGBClassifier on sp_fip_delta + abs_delta
  6. Evaluate: AUC, BrierSk, monthly_stability
  7. Compare to P37 baseline: AUC_WFV=0.5665, BrierSk=+0.0123, win_rate=60.8%
  8. 分類: HOLDOUT_CONFIRMED (AUC≥0.54) / HOLDOUT_WEAK (0.50≤AUC<0.54) / FAILED
Governance: diagnostic_only=True, promotion_freeze=True, T_LOCKED=0.50
```

---

## 14. CTO 十行摘要

P39 成功建立完整 2024 MLB holdout dataset，解決 P38 DATA_UNAVAILABLE 的根本問題。從 Retrosheet 取得靜態 2024 game log（2429 場），建立 2023 FIP 代理表（160 位投手），計算每場賽局 `sp_fip_delta`（away_fip - home_fip）特徵。

關鍵成果：2429 場賽局 → 2158 quality records（88.8%）→ **955 strong-edge records（T≥0.50）**，遠超 WFV 最低需求（150）。Strong-edge 方向準確率 56.4%（高於 50% 隨機基準）。全部 2429 筆記錄通過 PIT 安全稽核（FIP year=2023 < game year=2024）。34/34 測試通過。

P40 可直接執行 2024 WFV 驗證，比對 P37 基準（AUC=0.5665, BrierSk=+0.0123）是否在 OOS 條件下得到複製。
