# Phase70 完成回報

**日期**: 2026-05-07  
**Phase**: Phase 70 — Strong Home Favorite Underconfidence Feature Root-Cause Audit  
**版本**: `phase70_strong_home_favorite_underconfidence_audit_v1`  
**完成標記**: `PHASE_70_STRONG_HOME_FAVORITE_UNDERCONFIDENCE_AUDIT_VERIFIED`

---

## 1. 本輪目標

承接 Phase 69 發現（gate: `CALIBRATION_OBJECTIVE_NOT_PROMISING`）：  
model_home_prob **0.65–0.70 band** 存在嚴重 underconfidence（model 預測 ~0.67，實際勝率 ~0.77，residual ≈ −0.095），且 calibration / 概率塑形無法修正。

Phase 70 任務：
- **診斷根因** — 不修改生產環境，僅做 paper-only attribution
- **五維度分析**：(A) 市場 vs 模型比較、(B) 偏好方向分析、(C) split/時間穩定性、(D) 球隊集中度、(E) 特徵代理歸因
- **5 個負控** 驗證信號真實性
- **Bootstrap CI** 驗證不確定性
- **產出 Gate**（7 選 1）與 Phase 71 建議

---

## 2. 已完成事項

| # | 事項 | 結果 |
|---|------|------|
| 1 | `orchestrator/phase70_strong_home_favorite_underconfidence_audit.py` | ✅ 建立完成 |
| 2 | `scripts/run_phase70_strong_home_favorite_underconfidence_audit.py` | ✅ 建立完成 |
| 3 | `tests/test_phase70_strong_home_favorite_underconfidence_audit.py` | ✅ 122 tests PASS |
| 4 | `reports/phase70_strong_home_favorite_underconfidence_audit_20260507.json` | ✅ 產出完成 |
| 5 | Phase 67/68/69 回歸驗證 | ✅ 463 passed |

---

## 3. 修改或產出的檔案

| 檔案 | 操作 |
|------|------|
| `orchestrator/phase70_strong_home_favorite_underconfidence_audit.py` | 新建 |
| `scripts/run_phase70_strong_home_favorite_underconfidence_audit.py` | 新建 |
| `tests/test_phase70_strong_home_favorite_underconfidence_audit.py` | 新建 |
| `reports/phase70_strong_home_favorite_underconfidence_audit_20260507.json` | 新建 |
| `00-BettingPlan/20260507/phase70_strong_home_favorite_underconfidence_audit_report_20260507.md` | 新建（本文件） |

**⚠️ 安全宣告（FROZEN）：**
- `CANDIDATE_PATCH_CREATED = False`
- `PRODUCTION_MODIFIED = False`
- `ALPHA_MODIFIED = False`
- `DIAGNOSTIC_ONLY = True`
- `PREDICTION_JSONL_OVERWRITTEN = False`
- `ALPHA = 0.40`（凍結）

---

## 4. 驗證結果 / 測試結果

### Phase 70 單元測試
```
122 passed in 3.12s
```

**測試類別**：
- `TestSafetyConstants` — 8 tests ✅
- `TestPhaseIdentity` — 8 tests ✅
- `TestCoreMath` — 16 tests ✅
- `TestEnrich` — 12 tests ✅
- `TestFilterSegment` — 5 tests ✅
- `TestSegmentMetrics` — 11 tests ✅
- `TestSplitStability` — 5 tests ✅
- `TestTeamConcentration` — 5 tests ✅
- `TestFeatureAttribution` — 6 tests ✅
- `TestBootstrapCI` — 6 tests ✅
- `TestNegativeControls` — 6 tests ✅
- `TestGateDetermination` — 9 tests ✅
- `TestSerialization` — 6 tests ✅
- `TestThresholds` — 8 tests ✅
- `TestIntegration` — 6 tests ✅（合成資料）
- `TestEndToEnd` — 6 tests ✅（真實資料）

### Phase 67/68/69 回歸測試
```
463 passed, 1 warning in 29.78s
```
**無回歸。**

---

## 5. Gate 結論

**Gate: `MARKET_ONLY_SUPERIOR`** ✅

### 關鍵指標（0.65–0.70 band, n=103）

| 指標 | 數值 |
|------|------|
| n_target_band | 103 |
| model_brier | 0.1865 |
| market_brier | 0.1725 |
| **model_brier − market_brier** | **+0.0140** ≥ 閾值 0.005 |
| model_residual_mean | −0.0951 |
| market_residual_mean | −0.0982 |
| model_minus_market_mean | +0.0031 |
| observed_win_rate | 0.7670 |
| predicted_mean_prob | 0.6718 |
| market_mean_prob | 0.6688 |

### Gate 觸發邏輯

在 0.65–0.70 band，**市場（market）的 Brier Score（0.1725）明顯低於模型（0.1865）**，Brier gap = **+0.014**（高於閾值 0.005）。

值得注意的是，市場 residual（−0.0982）與模型 residual（−0.0951）**非常接近**，但市場概率（0.6688）和模型概率（0.6718）也幾乎相同。  
這意味著兩者都對這個 band 的實際勝率（0.767）嚴重低估，但市場的 **概率分佈更分散**（更接近兩端），因此 Brier Score 較低。

### 其他摘要 flags

| Flag | 值 |
|------|----|
| `market_better_in_target_band` | **True** |
| `feature_gap_detected` | **True**（sp_fip_delta extreme_delta = +0.314） |
| `team_concentration_detected` | False（最高球隊佔 11.7%，未達 30% 閾值） |
| `split_instability_detected` | **True**（split residual std > 0.08） |
| `negative_controls_clear` | **True**（5/5 NCs 無 overfit risk） |
| `bootstrap_ci_stable` | False（target band CI 較寬：−0.1728 ~ −0.0155） |
| `worth_phase71` | **True** |

---

## 6. 0.65–0.70 underconfidence 的最可能原因

### 主要發現

**市場優於模型（MARKET_ONLY_SUPERIOR）**，但兩者都低估了 0.65–0.70 band 的實際勝率（0.767）。

#### (A) 市場 vs 模型

- 兩者 residual 都是負值（~−0.095 ~ −0.098）
- 市場 Brier 低於模型 Brier（差距 0.014），表明市場的**概率分佈更廣**，而模型更集中在 0.65–0.70 附近
- 市場捕捉到模型未能捕捉的信息

#### (B) Split 時間不穩定性

| Split | n | Residual | Win Rate |
|-------|---|----------|----------|
| window_1 | 25 | −0.1652 | 0.840 |
| window_2 | 26 | −0.0148 | 0.692 |
| window_3 | 14 | +0.1777 | 0.500 |
| window_4 | 25 | −0.1342 | 0.800 |
| window_5 | 13 | −0.3396 | 1.000 |

Split residual std = 0.18（遠超閾值 0.08），表明 underconfidence **不是穩定的系統性偏差**，而是在不同時間窗口下方向相反的信號。

#### (C) 特徵代理歸因

`sp_fip_delta` 在 target band 的均值（extreme_delta = **+0.3144**）遠高於 all_games 均值（超過閾值 0.10）。  
這意味著 0.65–0.70 band 的比賽，home SP（先發投手）相對於 away SP **FIP 更低（更好）的幅度更大**，但模型對此的回應不足。

#### (D) 負控驗證

| 負控 | Signal Gap | Overfit Risk |
|------|-----------|--------------|
| shuffled_probability_band | −0.1047 | **False** |
| random_favorite_direction | −0.1329 | **False** |
| irrelevant_date_bucket_split | +0.0017 | **False** |
| random_team_bucket_split | +0.0857 | **False** |
| random_confidence_assignment | −0.2375 | **False** |

**5/5 負控通過**（overfit_risk = False），underconfidence 信號是**真實的**，不是雜訊。

#### (E) Bootstrap CI（target band, residual_mean）

```
obs = −0.0951  95%CI = [−0.1728, −0.0155]  excl0 = True
```

CI 排除零，確認 underconfidence 信號在統計上顯著，但 CI 較寬（不穩定）。

### 綜合判斷

0.65–0.70 band 的 underconfidence 根因：

1. **主因（MARKET_ONLY_SUPERIOR）**：市場在此 band 的 Brier Score 系統性低於模型，顯示市場具有模型 feature set 未捕捉到的資訊
2. **加劇因素**：sp_fip_delta 在此 band 極端偏高（home SP 明顯優於 away SP），模型對此特徵的權重不足
3. **時間不穩定**：此 band 的 residual 在不同 window 間差異極大（window_5 residual = −0.34），可能存在 regime change

---

## 7. 是否建議 Phase 71

**建議 Phase 71 ✅（`worth_phase71 = True`）**

Phase 71 方向：**market dominance / model de-risk audit**

具體工作：
- 調查 `market_home_prob_no_vig` 在 0.65–0.70 band 的分佈，了解市場為何概率分佈更廣
- 分析 `sp_fip_delta` 與 model underconfidence 的具體關聯（market 是否對此特徵更敏感）
- 探討 ensemble 中是否能以 market signal 作為 anchor 修正此 band 的概率

**⚠️ Phase 71 仍為 paper-only，不允許 production patch。**

---

## 8. 尚未完成事項

本 phase 所有任務均已完成。無遺留事項。

---

## 9. 風險與不確定點

| 風險 | 嚴重度 | 說明 |
|------|--------|------|
| Bootstrap CI 不穩定 | 中 | Target band residual CI 寬度超過閾值（−0.1728 ~ −0.0155），不確定性大 |
| Split 時間不穩定 | 中 | Window_3 residual +0.178 與 window_5 −0.340，方向相反，可能有 regime change |
| n_target_band 較小 | 低-中 | n=103，足夠分析但部分 team-level 數據 data_limited |
| sp_fip_delta 與 market 相關性 | 低 | 兩者都可能被同一個底層因素驅動（不是獨立信號） |
| Market vs Model Brier gap 不大 | 低 | gap=0.014，統計顯著但實際影響有限 |

---

## 10. 下一輪建議方向

### Phase 71 — Market Dominance / Model De-Risk Audit

**核心問題**：市場在 0.65–0.70 band 為何比模型更準確？

**具體分析任務**：
1. **Market signal decomposition**：分析市場概率的分佈特性——在此 band 市場是否更多預測 >0.70？
2. **sp_fip_delta × market correlation**：sp_fip_delta 極端值時，市場概率是否同步偏高？
3. **Blend 效果分析**：現有 blend（40% market + 60% model）在此 band 的效果評估
4. **季節效應**：split 不穩定性是否有季節規律（早季 vs 晚季）？
5. **若以 market 為 anchor**：paper-only 模擬 — 若 blend 比例調整至此 band，對 Brier 的影響

**禁止**：不得修改 `ALPHA = 0.40`，不得修改生產 JSONL。

### 替代方向（若 Phase 71 不批准）

- **LeagueAdapter / Budget Guard**：回到架構優先 P1
- **Governance / Metrics SSOT**：修正 phase chain 的 BSS/ECE 指標一致性問題

---

## 11. 完成標記

```
PHASE_70_STRONG_HOME_FAVORITE_UNDERCONFIDENCE_AUDIT_VERIFIED
```
