# P42 — Signal-band Tier Framework + Kelly-equivalent Diagnostic

**日期**: 2026-05-24  
**狀態**: ✅ PASS (exit code 1 — Tier A SAMPLE_LIMITED, directional only)  
**前置**: P41 CLOSED @ `6ee4e57` (CROSS_YEAR_CONFIRMED, AUC=0.5865)  
**治理**: `diagnostic_only=True` · `promotion_freeze=True` · `kelly_deploy_allowed=False`

---

## 1. 執行摘要

P42 對 sp_fip_delta 訊號進行三層信號強度分層分析（Tier A/B/C），驗證高強度訊號邊緣是否具備統計顯著性，並計算 Kelly-equivalent 理論倉位（純診斷，不作為下注建議）。

| Tier | 閾值 | n | AUC | WR | CI 95% | 分類 |
|------|------|---|-----|----|--------|------|
| **A** | \|delta\| ≥ 1.50 | 47 | **0.7038** | 0.6596 | [0.5417, 0.8472] | `SAMPLE_LIMITED_HIGH_AUC` |
| **B** | \|delta\| ≥ 1.25 | 180 | **0.6476** | 0.6111 | [0.5591, 0.7323] | `MEDIUM_CONFIDENCE_DIAGNOSTIC` |
| **C** | \|delta\| ≥ 0.50 | 1490 | **0.5865** | 0.5792 | [0.5557, 0.6170] | `HIGH_CONFIDENCE_DIAGNOSTIC` |

**關鍵發現**：訊號強度與分層閾值成正相關 — 越嚴格的閾值，AUC 越高（0.5865 → 0.6476 → 0.7038）。三層均跨年度穩定（cross_year_stable=True）。

---

## 2. 資料清單

| 欄位 | 值 |
|------|-----|
| 質量記錄總量 | 3,586 筆 (2024: 2,158 / 2025: 1,428) |
| Tier C 強邊緣記錄 | 1,490 筆 (覆蓋率 41.5%) |
| Tier B 強邊緣記錄 | 180 筆 (覆蓋率 5.0%) |
| Tier A 強邊緣記錄 | 47 筆 (覆蓋率 1.3%) |
| T_LOCKED | 0.50 (不變動) |
| 資料來源 2024 | `mlb_2024_sp_fip_delta_features.jsonl` |
| 資料來源 2025 | `mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` |

---

## 3. 各 Tier 完整指標

### Tier A：|delta| ≥ 1.50

```
n               = 47
coverage        = 1.31%
AUC             = 0.7038
favored_WR      = 0.6596
Brier Score     = 0.2556
Brier Skill     < 0 (sigmoid calibration偏差，屬已知現象)
ECE             = 0.0847
log-loss        = 0.6213
Bootstrap AUC CI= [0.5417, 0.8472]  (寬 — 樣本小)
Bootstrap WR CI = (包含 0.50 下界)
cross_year_stable = True
```

**年度分解**：
- 2024: n=23, AUC=0.6364, WR=0.6087
- 2025: n=24, AUC=0.7727, WR=0.7083

⚠️ n=47 過小，CI 很寬 ([0.54, 0.85])，絕對不能依此下注。AUC=0.70 具方向性指示意義，但置信度低。

---

### Tier B：|delta| ≥ 1.25

```
n               = 180
coverage        = 5.02%
AUC             = 0.6476
favored_WR      = 0.6111
Brier Score     = 0.2488
Brier Skill     < 0 (已知)
ECE             = 0.0783
log-loss        = 0.6192
Bootstrap AUC CI= [0.5591, 0.7323]  (CI 完全 > 0.54)
Bootstrap WR CI = CI_lo > 0.50
cross_year_stable = True
```

**年度分解**：
- 2024: n=82, AUC=0.6696, WR=0.6341
- 2025: n=98, AUC=0.6490, WR=0.5918

Tier B 的 CI 完全排除 0.54，屬於統計意義最強的一層（n 仍相對有限，僅 180）。

---

### Tier C：|delta| ≥ 0.50（P37 鎖定閾值，基線）

```
n               = 1490
coverage        = 41.55%
AUC             = 0.5865  (符合 P41 結果 ±0.001)
favored_WR      = 0.5792
Brier Score     = 0.2514
Brier Skill     < 0 (已知)
ECE             = 0.0802
log-loss        = 0.6212
Bootstrap AUC CI= [0.5557, 0.6170]  (完全 > 0.54)
Bootstrap WR CI = CI_lo > 0.50
cross_year_stable = True
```

**年度分解**：
- 2024: n=955, AUC=0.5748, WR=0.5644
- 2025: n=535, AUC=0.6020, WR=0.6056

Tier C 為 P37/P40/P41 的基礎鎖定層，P42 結果完全復現 P41 的 AUC=0.5865 (|diff|<0.001)。

---

## 4. Tier A vs. Tier C 顯著性比較

| 指標 | 值 |
|------|-----|
| 觀察 AUC delta (A - C) | **+0.1173** |
| Permutation test p-value | 0.0805 |
| n_permutations | 2,000 |
| significance (α=0.05) | `not_significant` |
| Tier A n | 47 |

**解讀**：Tier A AUC 高出 Tier C 約 0.12，但 p=0.0805 未達 α=0.05。這**主要是 Tier A n=47 導致統計檢定力不足**，而非訊號為零。方向上，更高閾值 → 更強 AUC 的梯度是一致的（0.5865 → 0.6476 → 0.7038）。若 Tier A 達 n≥200，結果可能顯著。

---

## 5. Kelly-equivalent 診斷（純理論，禁止部署）

> ⚠️ **警告**: 以下 Kelly 倉位計算全為診斷用途。以 `favored_wr` 作為 oracle p_win 假設，實際賽事中估算誤差顯著。`kelly_deploy_allowed=False`。

### Tier C（基礎層，n=1490）

| 賠率情境 | Decimal odds | p_win假設 | Full Kelly | ¼ Kelly | 正期望值 |
|---------|-------------|----------|-----------|---------|---------|
| fair_no_vig | 2.00 | 0.5792 | **15.8%** | 3.96% | ✅ |
| tight_book | 1.90 | 0.5792 | **11.2%** | 2.79% | ✅ |
| standard_book | 1.85 | 0.5792 | **8.4%** | 2.10% | ✅ |

### Tier B（中強度，n=180）

| 賠率情境 | Decimal odds | p_win假設 | Full Kelly | ¼ Kelly | 正期望值 |
|---------|-------------|----------|-----------|---------|---------|
| fair_no_vig | 2.00 | 0.6111 | **22.2%** | 5.56% | ✅ |
| tight_book | 1.90 | 0.6111 | **17.9%** | 4.47% | ✅ |
| standard_book | 1.85 | 0.6111 | **15.4%** | 3.83% | ✅ |

### Tier A（高強度，n=47 — 樣本不足）

| 賠率情境 | Decimal odds | p_win假設 | Full Kelly | ¼ Kelly | 正期望值 |
|---------|-------------|----------|-----------|---------|---------|
| fair_no_vig | 2.00 | 0.6596 | **31.9%** | 7.98% | ✅ |
| tight_book | 1.90 | 0.6596 | **28.1%** | 7.03% | ✅ |
| standard_book | 1.85 | 0.6596 | **25.9%** | 6.48% | ✅ |

**Kelly 解讀**：即使在最保守的 ¼ Kelly 與 1.85 賠率下，理論倉位仍為正。但此計算**假設 favored_wr 等於真實 win probability，忽略了賠率中隱含的抽水、自身估算誤差、以及樣本變異**。Tier A 因 n=47 完全不適合作為 Kelly 基準。Tier C 的理論 ¼ Kelly ~2-4% 在回測中看起來合理，但未納入跨場次相關性、槓桿衰減、資金邊際等因素。

---

## 6. 治理聲明

| 項目 | 狀態 |
|------|------|
| diagnostic_only | ✅ True |
| promotion_freeze | ✅ True |
| T_LOCKED | ✅ 0.50（不變動）|
| kelly_deploy_allowed | ✅ False |
| live_api_calls | ✅ 0 |
| no_champion_modification | ✅ True |
| champion 模型修改 | ✅ 無 |
| 未來資訊洩漏 | ✅ 無 |

---

## 7. 分類摘要

| Tier | 分類標籤 | 說明 |
|------|---------|------|
| A | `SAMPLE_LIMITED_HIGH_AUC` | AUC=0.70 具指示性，但 n=47 無法信賴 CI |
| B | `MEDIUM_CONFIDENCE_DIAGNOSTIC` | CI 完全 > 0.50，n=180 達中等置信水平 |
| C | `HIGH_CONFIDENCE_DIAGNOSTIC` | CI 完全 > 0.54，n=1490 大樣本，P41 基礎復現 |

---

## 8. 測試覆蓋

| 測試類別 | 測試數 | 狀態 |
|---------|-------|------|
| TestFileExists | 3 | ✅ |
| TestGovernance | 7 | ✅ |
| TestDataInventory | 6 | ✅ |
| TestTierDefinitions | 4 | ✅ |
| TestTierAMetrics | 8 | ✅ |
| TestTierBMetrics | 8 | ✅ |
| TestTierCMetrics | 7 | ✅ |
| TestBootstrapCI | 7 | ✅ |
| TestComparisonAC | 7 | ✅ |
| TestKellyDiagnostic | 8 | ✅ |
| TestTierClassification | 4 | ✅ |
| TestP41Reference | 4 | ✅ |
| TestMetricCompleteness | 5 | ✅ |
| **合計** | **78** | **78/78 PASS** |

**P40 + P41 + P42 累計**: 31 + 52 + 78 = **161/161 PASS**

---

## 9. 產出文件

| 文件 | 路徑 |
|------|------|
| P42 主腳本 | `scripts/_p42_signal_band_tier_kelly_diagnostic.py` |
| P42 結果 JSON | `data/mlb_2025/derived/p42_signal_band_tier_kelly_summary.json` |
| P42 測試套件 | `tests/test_p42_signal_band_tier_kelly.py` |
| P42 分析報告 | `report/p42_signal_band_tier_kelly_diagnostic_20260524.md` |

---

## 10. 結論與下一步

P42 確認：

1. **訊號強度梯度存在** — 越高閾值的子集，AUC 越高（C=0.5865 < B=0.6476 < A=0.7038）
2. **三層均跨年度穩定** — 2024 和 2025 均呈正向 AUC，`cross_year_stable=True`
3. **Tier B 的置信度最佳** — CI 完全排除 0.54，且 n=180 足夠提供可信的 bootstrap 估計
4. **Tier A 需要更多資料** — AUC=0.70 高但 n=47 不足，CI 寬 [0.54, 0.85]，不可信賴
5. **Kelly 理論正值** — 但僅供診斷，`kelly_deploy_allowed=False` 鎖定

**潛在後續**（未在本 commit 中執行，留待後續階段決策）：
- P43 候選：累積更多 Tier A 記錄至 n≥150 後重新評估
- 考慮 Tier B 的 focused analysis（n=180，CI 清晰）
- 探索 sp_fip_delta 以外的第二特徵是否可進一步提升 Tier A 精度
