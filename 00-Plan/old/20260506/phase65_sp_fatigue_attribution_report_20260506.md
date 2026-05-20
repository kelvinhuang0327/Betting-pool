# Phase 65 — SP Fatigue Attribution Report

**日期**: 2026-05-06  
**版本**: `phase65_sp_fatigue_attribution_v1`  
**Phase 64-B 錨點**: `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING`  
**Gate 結果**: 🔴 `OVERFIT_RISK`  
**Completion Marker**: `PHASE_65_SP_FATIGUE_ATTRIBUTION_VERIFIED`

---

## 1. 執行摘要

Phase 65 對 2025 MLB 賽季 2,025 場預測比賽進行先發投手 (SP) 疲勞特徵歸因分析。  
分析資料來源為 `mlb-2025-asplayed.csv`（實際先發投手）與 Phase 56 模型預測檔。  
核心問題：**先發投手休息天數是否對重寶盤（blend ≥ 0.70）的勝率有可利用的預測力？**

**結論：Gate = `OVERFIT_RISK`，不建議進入 Phase 66。**

---

## 2. 安全常數快照 (Frozen)

| 常數 | 值 |
|---|---|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `ALPHA_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |
| `ALPHA` | `0.40` |

---

## 3. 資料基礎

### SP 先發歷史

| 指標 | 值 |
|---|---|
| asplayed 行數 | 2,430 |
| 不重複投手 | 369 |
| 多次先發投手 | 308 |
| 日期區間 | 2025-03-18 → 2025-09-28 |

### Alignment（預測 ↔ asplayed）

| 指標 | 值 |
|---|---|
| 總預測數 | 2,025 |
| 主隊先發 rest_days 覆蓋 | 1,930 / 95.3% |
| 客隊先發 rest_days 覆蓋 | 1,936 / 95.6% |
| 雙邊皆覆蓋 | 1,846 / 91.2% |
| `coverage_sufficient` | ✅ True |

---

## 4. 特徵登錄表

### AVAILABLE (11 個特徵，來自 asplayed 先發名單)

| 特徵名稱 | 覆蓋率 |
|---|---|
| `home_sp_rest_days` | 95.3% |
| `away_sp_rest_days` | 95.6% |
| `home_sp_short_rest` | 95.3% |
| `away_sp_short_rest` | 95.6% |
| `home_sp_long_rest` | 95.3% |
| `away_sp_long_rest` | 95.6% |
| `sp_rest_imbalance` | 91.2% |
| `fav_sp_rest_days` | 96.4% |
| `dog_sp_rest_days` | 94.6% |
| `fav_sp_short_rest` | 96.4% |
| `sp_rest_advantage` | 91.2% |

### DATA_LIMITED (5 個特徵，asplayed.csv 無 IP/投球數欄位)

| 特徵名稱 | 原因 |
|---|---|
| `starter_previous_start_ip` | asplayed 無 IP 欄位 |
| `starter_last_7d_ip` | asplayed 無 IP 欄位 |
| `starter_last_14d_ip` | asplayed 無 IP 欄位 |
| `starter_previous_start_pitch_count` | asplayed 無投球數欄位 |
| `opener_or_bulk_pitcher_flag` | 無法由姓名推斷 |

---

## 5. 分段大小

| 分段 | 樣本數 | 說明 |
|---|---|---|
| `all` | 2,025 | 全預測集 |
| `heavy_favorite` | 60 | blend ≥ 0.70 |
| `high_confidence` | 10 | blend ≥ 0.75 |

> ⚠️ `heavy_favorite` 僅 60 場，`high_confidence` 僅 10 場，分段樣本極小，統計功效受限。

---

## 6. 重寶盤 (heavy_favorite) 歸因結果

### Bucket Attribution (median split)

| 特徵 | Δ 勝率 | 95% Bootstrap CI | n_high | n_low | 顯著? |
|---|---|---|---|---|---|
| `home_sp_rest_days` | +0.0617 | [-0.2447, +0.3532] | 10 | 47 | ❌ |
| `away_sp_rest_days` | +0.0196 | [-0.3529, +0.3922] | 6 | 51 | ❌ |
| `home_sp_short_rest` | — | (n 不足) | — | — | — |
| `away_sp_short_rest` | — | (n 不足) | — | — | — |
| **`home_sp_long_rest`** | **+0.3846** | **[+0.2692, +0.5192]** | **5** | **52** | **✅** |
| **`away_sp_long_rest`** | **+0.3636** | **[+0.2364, +0.4909]** | **2** | **55** | **✅** |
| `sp_rest_imbalance` | -0.0632 | [-0.2912, +0.1978] | 26 | 28 | ❌ |
| `fav_sp_rest_days` | +0.0252 | [-0.3648, +0.3962] | 6 | 53 | ❌ |
| `dog_sp_rest_days` | +0.0556 | [-0.2778, +0.3444] | 10 | 45 | ❌ |
| `fav_sp_short_rest` | — | (n 不足) | — | — | — |
| `sp_rest_advantage` | -0.1590 | [-0.4615, +0.1282] | 15 | 39 | ❌ |

> `home_sp_long_rest` 與 `away_sp_long_rest` 的 bootstrap CI 不含零，表面顯著。

### OOF 驗證 (rolling monthly, heavy_fav)

| 特徵 | 平均 Δ | Folds | 一致符號 | OOF 顯著? |
|---|---|---|---|---|
| `home_sp_long_rest` | +0.3464 | 2 | ✅ | ✅ |
| `away_sp_long_rest` | +0.3333 | 2 | ✅ | ✅ |
| 其他特徵 | ±0.07 | 2 | ❌ | ❌ |

> ⚠️ Fold 數僅 2（heavy_fav 樣本不足，月份分布稀疏），OOF 可靠性極低。

---

## 7. 負控制 (Negative Control)

| 特徵 | 真實 Δ | 洗牌平均 | 洗牌標準差 | null_rejected | overfit_risk |
|---|---|---|---|---|---|
| `home_sp_rest_days` | +0.0617 | -0.0001 | 0.1736 | ❌ | ❌ |
| `away_sp_rest_days` | +0.0196 | -0.0046 | 0.2068 | ❌ | ❌ |
| **`home_sp_long_rest`** | **+0.3846** | **-0.0056** | **0.2161** | **✅** | **✅ ⚠️** |
| `away_sp_long_rest` | +0.3636 | -0.0095 | 0.3596 | ✅ | ❌ (std≥0.36，含零) |
| `sp_rest_imbalance` | -0.0632 | +0.0162 | 0.1401 | ❌ | ❌ |
| `fav_sp_rest_days` | +0.0252 | +0.0029 | 0.2231 | ❌ | ❌ |
| `sp_rest_advantage` | -0.1590 | +0.0201 | 0.1510 | ❌ | ❌ |
| `fav_sp_short_rest` | 0.0000 | 0.0000 | 0.0000 | ❌ | ❌ |
| `home/away_sp_short_rest` | 0.0000 | 0.0000 | 0.0000 | ❌ | ❌ |
| `dog_sp_rest_days` | +0.0556 | -0.0166 | 0.1789 | ❌ | ❌ |

**`home_sp_long_rest` 觸發 `OVERFIT_RISK`**：  
- `null_rejected = True`（真實 Δ 超過洗牌分佈）  
- `shuffled_std = 0.2161 > 0.10`（洗牌分佈極不穩定）  
→ 信號很可能是小樣本（n_high=5）下的隨機偶發，而非真實可利用的規律。

---

## 8. Gate 決策

**Gate: `OVERFIT_RISK`**

```
rationale: Negative control indicates overfit risk: null rejected AND 
shuffled_std > 0.10. No production patch produced. SP fatigue signal 
may be spurious.

next_step: Disable fitted adjustment. Re-validate with fresh hold-out 
segment (n >= 200 heavy_fav games). Consider Bonferroni correction.

worth_phase66: False
```

### 決策邏輯說明

```
任何 nc.overfit_risk → OVERFIT_RISK  (優先級高於 PROMISING)
```

`home_sp_long_rest` 在 heavy_fav 分段中 n_high=5，本質上為小樣本噪音：
- 5 場「投手長休」賽事中全贏，並不代表可靠規律
- 洗牌標準差 0.2161 說明在這個分段大小下，隨機洗牌就能輕易產生類似 Δ
- Bonferroni 修正後（11 特徵 × 3 分段），顯著水準需 < 0.0015，更難通過

---

## 9. 統計工程評估

### 根本原因
1. **Heavy_fav 分段過小**（n=60，其中 long_rest 子組 n=5）
2. **Fold 數不足**（僅 2 fold，OOF 可靠性低）
3. **多重比較未修正**（11 特徵 × 3 分段 = 33 次測試，Type I 錯誤率高）
4. **asplayed 先發投手 ≠ 開賽前預測投手**（Phase 56 特徵用 probable pitcher，非實際先發）

### 特徵固有限制
- Long_rest (DL 復出) 在整個賽季只有極少樣本落在 heavy_fav 分段
- IP 特徵（最佳 SP 疲勞指標）因 asplayed.csv 缺乏欄位而 DATA_LIMITED
- 知道「某投手長休」在開賽前不一定是可即時取得的資訊

---

## 10. 回歸測試結果

| 測試套件 | 測試數 | 結果 |
|---|---|---|
| Phase 63 (`test_phase63*.py`) | 140 | ✅ PASS |
| Phase 64 (`test_phase64_*.py`) | 137 | ✅ PASS |
| Phase 64-B (`test_phase64b*.py`) | 109 | ✅ PASS |
| Phase 65 (`test_phase65*.py`) | 113 | ✅ PASS |
| **總計** | **499** | **✅ 499/499 PASS** |

---

## 11. 產出檔案

| 檔案 | 說明 |
|---|---|
| `orchestrator/phase65_sp_fatigue_attribution.py` | 核心歸因模組 |
| `scripts/run_phase65_sp_fatigue_attribution.py` | 執行腳本 |
| `tests/test_phase65_sp_fatigue_attribution.py` | 113 個測試 |
| `reports/phase65_sp_fatigue_attribution_20260506.json` | 完整診斷 JSON |
| `00-BettingPlan/phase65_sp_fatigue_attribution_report_20260506.md` | 本報告 |

---

## 12. 結論與下一步

### 結論
Phase 65 SP 疲勞特徵歸因分析完成，gate 為 **`OVERFIT_RISK`**。

`home_sp_long_rest` 顯示表面顯著的勝率差異（Δ≈+38%），但這是在 n_high=5 的極小樣本上，負控制確認此為小樣本過擬合偽信號，**不具可利用性**。

### 不進入 Phase 66 的理由
- `worth_phase66 = False`
- 在 n=60 的 heavy_fav 分段中，任何 long_rest 信號均缺乏統計效力
- 若要有效驗證，需要 n ≥ 200 的 heavy_fav 分段（估計需要 5-6 年資料）
- 數據來源（asplayed.csv）缺乏 IP/投球數等更可靠的疲勞代理指標

### 建議的備選方向
- **棄置 SP 疲勞線路**：在 heavy_fav 小分段中無可靠 SP 疲勞信號
- **探索其他維度**：球場效應（主場優勢異質性）、比賽月份效應、對戰歷史
- **提升 heavy_fav 樣本**：分析 2023-2025 多年資料，增加分段樣本至 ≥ 200

---

**Phase 64-B Gate**: `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING`  
**Phase 65 Gate**: `OVERFIT_RISK`  
**Phase 66**: ⛔ 不建議（`worth_phase66 = False`）  
**Completion Marker**: `PHASE_65_SP_FATIGUE_ATTRIBUTION_VERIFIED`
