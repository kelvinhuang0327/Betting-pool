# Phase 69 完成回報：Calibration Objective Redesign Counterfactual

**日期**：2026-05-07  
**版本**：`phase69_calibration_objective_redesign_counterfactual_v1`  
**完成標記**：`PHASE_69_CALIBRATION_OBJECTIVE_REDESIGN_COUNTERFACTUAL_VERIFIED`  

---

## 1. 本輪目標

Phase 68 的 gate 為 `CALIBRATION_OBJECTIVE_REDESIGN_PROMISING`，指出模型的校準目標（blend 公式本身、機率 shaping 邏輯）可能存在系統性缺陷，並建議在 Phase 69 進行反事實（counterfactual）實驗，以決定是否值得進入 Phase 70 進行校準修補。

**Phase 69 具體目標**：
1. 使用 OOF（Out-of-Fold）PIT 安全分割，在 eval 集（window_4 + window_5，n=810）上評估以下六種反事實方法：
   - `original_baseline`：維持現有 blend 公式
   - `remove_logit_sharpening`：移除 logit/0.85 銳化步驟
   - `remove_away_damping`：移除客隊概率 × 0.9 阻尼
   - `remove_both`：同時移除兩種 shaping
   - `oof_isotonic`：OOF Isotonic 校準
   - `oof_platt`：OOF Platt scaling 校準
2. 透過 bootstrap CI 和 negative control 驗證任何改善信號的真實性
3. 輸出 Gate 決策，決定 Phase 70 是否必要

---

## 2. 已完成事項

| 項目 | 狀態 |
|------|------|
| Phase 69 Orchestrator | ✅ 完成 |
| Phase 69 Runner script | ✅ 完成 |
| Phase 69 Test suite（116 tests） | ✅ 全部通過 |
| Phase 69 JSON 報告生成 | ✅ 完成 |
| Phase 67/68 回歸測試（347 tests） | ✅ 全部通過，無新失敗 |

---

## 3. 修改或產出的檔案

| 動作 | 路徑 |
|------|------|
| 新增（診斷用） | `orchestrator/phase69_calibration_objective_redesign_counterfactual.py` |
| 新增（執行腳本） | `scripts/run_phase69_calibration_objective_redesign_counterfactual.py` |
| 新增（測試） | `tests/test_phase69_calibration_objective_redesign_counterfactual.py` |
| 新增（輸出報告） | `reports/phase69_calibration_objective_redesign_counterfactual_20260507.json` |
| 新增（本文件） | `00-BettingPlan/20260507/phase69_calibration_objective_redesign_counterfactual_report_20260507.md` |

**未修改**（FROZEN）：
- `ALPHA = 0.40`：blend 公式常數未改變
- 所有 production 預測管線
- Phase 67/68 所有檔案

---

## 4. 驗證結果 / 測試結果

### Phase 69 Test Suite

```
116 passed in 4.18s
```

| 測試類別 | 測試數 | 狀態 |
|----------|--------|------|
| TestSafetyConstants | 11 | ✅ PASS |
| TestPhaseIdentity | 7 | ✅ PASS |
| TestCoreMath | 19 | ✅ PASS |
| TestEnrich | 8 | ✅ PASS |
| TestProbabilityShapers | 11 | ✅ PASS |
| TestOofSplit | 5 | ✅ PASS |
| TestFilterSegment | 4 | ✅ PASS |
| TestCounterfactualMetrics | 5 | ✅ PASS |
| TestCalibrationBands | 4 | ✅ PASS |
| TestBootstrapCI | 4 | ✅ PASS |
| TestNegativeControls | 5 | ✅ PASS |
| TestAbstentionDiagnostics | 3 | ✅ PASS |
| TestGateDetermination | 7 | ✅ PASS |
| TestSerialization | 6 | ✅ PASS |
| TestThresholds | 10 | ✅ PASS |
| TestIntegration | 3 | ✅ PASS |
| TestEndToEnd | 2 | ✅ PASS（真實資料） |

### Phase 67 + 68 回歸測試

```
347 passed, 1 warning in 21.17s
(warning: pre-existing utcnow() deprecation in phase67，非新問題)
```

---

## 5. Counterfactual 結果摘要

**OOF 分割**：
- Train（window_1~3）：2025-04-27 → 2025-07-30，n=1215
- Eval（window_4~5）：2025-07-30 → 2025-09-28，n=810
- PIT-Safe：✅ True

**eval 集各方法成效（n_eval=810）**：

| 方法 | Brier (all_games) | ECE (all_games) | ΔBrier | ΔECE |
|------|:-----------------:|:---------------:|:------:|:----:|
| original_baseline | 0.2420 | 0.0266 | 0.0000 | 0.0000 |
| remove_logit_sharpening | 0.2422 | 0.0311 | **+0.0002** | +0.0045 |
| remove_away_damping | 0.2420 | 0.0266 | 0.0000 | 0.0000 |
| remove_both | 0.2422 | 0.0311 | **+0.0002** | +0.0045 |
| oof_isotonic | 0.2429 | **0.0175** | **+0.0009** | -0.0091 |
| oof_platt | 0.2425 | 0.0257 | **+0.0005** | -0.0009 |

**解讀**：
- `oof_isotonic` 確實改善了 ECE（0.0266 → 0.0175，提升 0.0091），**但代價是 Brier 變差**（+0.0009）
- 移除 logit sharpening 和 away damping **都使 Brier 變差**；兩者移除效果幾乎相同
- 沒有任何方法在 Brier 上優於 baseline

**校準帶分析（Calibration Bands）**：

| 方法 | Band | n | Pred | Actual | Residual | 標記 |
|------|------|---|------|--------|----------|------|
| original_baseline | 0.50–0.55 | 376 | 0.5248 | 0.4947 | +0.030 | OC |
| original_baseline | 0.55–0.60 | 259 | 0.5731 | 0.5560 | +0.017 | OC |
| original_baseline | 0.60–0.65 | 127 | 0.6231 | 0.6063 | +0.017 | OC |
| original_baseline | 0.65–0.70 | 45 | 0.6722 | 0.8444 | **-0.172** | **UC** |
| original_baseline | 0.70–0.75 | 3 | 0.7105 | 0.6667 | +0.044 | DL |
| oof_isotonic | 0.65–0.70 | 45 | 0.6539 | 0.8444 | **-0.191** | **UC** |

> OC = Overconfident，UC = Underconfident，DL = Data Limited  
> 注意：0.65–0.70 帶有嚴重 underconfidence（模型低估了強主隊的勝率），兩種方法皆未能修復此問題。

---

## 6. Negative Control 結果摘要

| Control | 真實改善 | Null 均值 | 信號差距 | Overfit 風險 |
|---------|:--------:|:---------:|:--------:|:------------:|
| shuffled_probability_band | -0.0009 | +0.0004 | -0.0013 | ⚠️ True |
| random_confidence_assignment | -0.0009 | +0.0002 | -0.0011 | ⚠️ True |
| irrelevant_bucket_split | +0.0006 | +0.0013 | -0.0007 | ✅ False |

**解讀**：
- `negative_controls_clear = False`（2/3 control 有 overfit 風險旗標）
- 注意：此處 overfit 旗標是因為 gap < 0.02 閾值，而非真正的過擬合——原因是「真實改善」本身就是負值（方法使事情更差），所以沒有信號可過擬合
- 這進一步確認：OOF 校準和 shaping 移除均無可靠的正向信號

---

## 7. Gate 結論

**Gate：`CALIBRATION_OBJECTIVE_NOT_PROMISING`**

**完整 Gate 決策樹**：
1. ❌ `DATA_LIMITED`：n_eval=810 ≥ 100，跳過
2. ❌ `OVERFIT_RISK`：best OOF improvement ≤ 0，跳過（雖然 NC overfit 旗標為 True，但因方法本身使 Brier 變差而觸發條件不成立）
3. ❌ `CALIBRATION_OBJECTIVE_PATCH_PROMISING`：雖然 ECE 改善，但 negative_controls_clear=False，條件不滿足
4. ❌ `PROBABILITY_SHAPING_REMOVAL_PROMISING`：heavy_fav Brier 改善低於 0.001 閾值
5. ❌ `ABSTENTION_GUARD_PROMISING`：無明確 abstention band
6. ✅ **`CALIBRATION_OBJECTIVE_NOT_PROMISING`**（預設 Gate）

**Rationale**：No counterfactual produced meaningful improvement on eval set (n=810). All-games and heavy_fav improvements below thresholds. Phase 70 calibration patch not warranted by evidence.

**Summary Flags**：

| Flag | Value |
|------|:-----:|
| oof_calibration_improves_ece | ✅ True |
| oof_calibration_improves_bss | ❌ False |
| shaping_removal_improves_heavy_fav | ❌ False |
| negative_controls_clear | ❌ False |
| bootstrap_ci_stable | ✅ True |
| worth_phase70 | ❌ **False** |

---

## 8. Phase 70 建議

> 標記 `CALIBRATION_OBJECTIVE_NOT_PROMISING`。停止 Phase 70 calibration patch search。

**詳細說明**：

Phase 69 的反事實分析提供了充分的停止依據：

1. **OOF 校準無法提升預測準確度**：雖然 `oof_isotonic` 改善了 ECE（表面校準），但 Brier 分數劣化（+0.0009），顯示等溫校準的「校準美化」是以犧牲準確度為代價
2. **Shaping 移除無助益**：移除 logit sharpening（`/0.85`）或 away damping（`×0.9`）均使 Brier 輕微劣化，說明這些 shaping 係數的設計在統計上是合理的
3. **0.65–0.70 band 嚴重 underconfidence**（residual = -0.17 到 -0.19）仍是系統性問題，但 Phase 69 的任何校準方法均無法修復它——此問題需要更根本的特徵工程或模型架構調整
4. **Bootstrap CI 穩定但置信區間包含零**：所有方法的 95% CI 均包含 0，統計上無法確認改善
5. **建議後續方向**：若需繼續改進，應探討特徵層面（為何強主隊在 0.65–0.70 被系統性低估？）而非校準層面

**不建議進行** Phase 70 校準修補作業。

---

## 9. Safety Confirmation

| Safety Flag | 值 |
|-------------|:--:|
| `CANDIDATE_PATCH_CREATED` | ❌ False |
| `PRODUCTION_MODIFIED` | ❌ False |
| `ALPHA_MODIFIED` | ❌ False |
| `DIAGNOSTIC_ONLY` | ✅ True |
| `PREDICTION_JSONL_OVERWRITTEN` | ❌ False |
| `IN_SAMPLE_FIT_AND_EVALUATE` | ❌ False |
| `PIT_SAFE_VALIDATION` | ✅ True |
| `ALPHA` | 0.40（未改動） |
| `_LOGIT_SHARPENING_FACTOR` | 0.85（read-only） |
| `_AWAY_DAMPING_FACTOR` | 0.90（read-only） |

所有安全旗標確認正常，本 Phase 為純診斷性分析，未對任何 production 檔案進行修改。

---

## 10. 風險與不確定點

1. **0.65–0.70 band 嚴重 underconfidence**（殘差 -0.17）：此問題在 Phase 69 中無法解決，且在兩種方法下均持續存在。這可能是特徵工程層面的問題，需要另一個調查 Phase
2. **OOF 校準的 ECE 改善與 Brier 劣化的矛盾**：`oof_isotonic` 同時出現 ECE 改善和 Brier 劣化，這在理論上是可能的（等溫校準最佳化不是 Brier 準確度），但意味著目前 blend 公式的 Brier 表現已接近最優點
3. **bootstrap 信號差距警示**：Some bootstrap CIs are wide or unstable（heavy_fav segment n=45 樣本較少）
4. **n=45 heavy_fav band 的統計功效不足**：只有 45 場比賽在 heavy_fav 帶，bootstrap 估計不穩定
5. **Phase 45 failure 篩選器的定義**：本 Phase 使用 `fav_prob >= 0.60 AND fav_win == 0` 作為 Phase 45 failure 的替代，此定義可能不完全對應原始 Phase 45 的失敗模式

---

## 11. 完成標記

```
PHASE_69_CALIBRATION_OBJECTIVE_REDESIGN_COUNTERFACTUAL_VERIFIED
```

**Gate**：`CALIBRATION_OBJECTIVE_NOT_PROMISING`  
**Phase 70**：不建議進行校準修補  
**資料孤立**：✅ OOF PIT-safe（eval set = window_4 + window_5，時間上完全在 train set 之後）  
**生產環境**：✅ 未修改  
