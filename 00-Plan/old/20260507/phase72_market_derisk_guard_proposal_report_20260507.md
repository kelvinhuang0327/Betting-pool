# Phase 72 — Paper-only Market De-risk Guard Proposal
## Compressed 0.65–0.70 Model Band

> **NO EDGE CLAIM. NO PROFIT CLAIM. PAPER-ONLY PROPOSAL. NO PRODUCTION PATCH.**

**日期**: 2026-05-07  
**版本**: `phase72_market_derisk_guard_proposal_v1`  
**安全旗標**: `DIAGNOSTIC_ONLY=True` / `CANDIDATE_PATCH_CREATED=False` / `PRODUCTION_MODIFIED=False` / `ALPHA_MODIFIED=False` / `PREDICTION_JSONL_OVERWRITTEN=False`  
**ALPHA（凍結）**: 0.40  
**Phase 70 gate anchor**: `MARKET_ONLY_SUPERIOR`  
**Phase 71 gate anchor**: `MARKET_DE_RISK_GUARD_PROMISING`

---

## 一、背景

Phase 71 完成 market dominance / model de-risk audit，發現：

| 指標 | 數值 |
|------|------|
| 目標段 n | 103（0.65–0.70 band）|
| model Brier | 0.1865 |
| market Brier | 0.1725 |
| Brier delta | **+0.0140** |
| bootstrap 95% CI | **[+0.0048, +0.0240]**（stable, excludes zero）|
| compression_ratio | **0.267**（model std 極度壓縮）|
| rank_correlation | 0.172 |
| 5 個窗口 | **5/5 市場一致優勢** |
| NC overfit_risk | 2/6（< 閾值 4）|
| sp_fip 被市場吸收 | True |

**Phase 71 gate → `MARKET_DE_RISK_GUARD_PROMISING`**

Phase 72 目標：建立 paper-only guard spec，回答以下問題：
1. guard 是否可定義得足夠清楚？
2. guard 是否 PIT-safe？
3. guard 是否只降低模型風險（不宣稱 edge）？
4. guard 是否可用 historical replay 驗證？
5. guard 是否適合進 Phase 73？
6. 或者 evidence 不足，應停止 patch path？

---

## 二、Candidate Guard Matrix

> 所有 threshold 均為提案值，Phase 73 必須驗證。不可在本輪 claim best threshold。

| guard_id | trigger_definition（摘要）| action_definition（摘要）| pit_safe | recommended |
|---------|--------------------------|--------------------------|----------|-------------|
| **G1_band_shadow** | model_home_prob ∈ [0.65, 0.70) | market_only_shadow：記錄 market-only 預測至 shadow report | ✅ | ✅ |
| **G2_band_disagreement_flag** | 同上 AND \|model-market\| ≥ 0.05 | de_risk_flag_only：附加 model_compression_risk=True flag | ✅ | ✅ |
| **G3_band_compression_abstain** | 同上 AND rolling compression_ratio ≤ 0.50 | abstain_from_model_confidence_claim：抑制 high-confidence wording | ✅ | ✅ |
| **G4_band_market_weight_cap_proposal** | model_home_prob ∈ [0.65, 0.70) | paper-only shadow_blend = 0.40\*model + 0.60\*market（不修改 alpha）| ✅ | ✅ |
| **G5_band_manual_review_route** | 同上 AND \|model-market\| ≥ 0.05 AND sp_fip 可用 | route_to_manual_review：標記 requires_human_review=True | ✅ | ✅ |
| G6_band_prior_split_evidence_only | 同上 AND ALL 前 3+ 窗口均 market_superior | market_only_shadow | ✅ | ❌ |

### 被拒絕的 Guard

**G6_band_prior_split_evidence_only** — 未被推薦（但非根本否決）：
- Rolling window 實作複雜度高，leakage risk 最高
- 需要 prior_window_segment_metrics 作為運算前置條件，Phase 73 難以驗證 PIT safety
- 建議在 G1/G2 通過 Phase 73 驗證後，再考慮 G6 作為進一步強化

### 各 Guard Action 限制事項

所有 guard action **不得**包含：
- production probability replacement（不修改 model_home_prob）
- automatic betting skip
- stake adjustment
- production market alpha patch（alpha 凍結在 0.40）
- EV / Kelly / ROI 計算

---

## 三、PIT-safe Evidence Rules（6 條，全部 REQUIRED）

| rule_id | 描述 |
|---------|------|
| PIT1_train_before_eval | train evidence 必須早於 eval window；不得 in-sample fit-and-evaluate |
| PIT2_inputs_pre_game_only | 所有 required_inputs 必須是開賽前可得資料（model_home_prob, market_home_prob_no_vig, sp_fip_delta）|
| PIT3_no_threshold_from_eval | 任何 threshold 不得由 eval 資料決定；必須在 Phase 73 多值測試 |
| PIT4_rolling_window_temporal_order | G3/G6 的 rolling window 必須嚴格按時間序排列；assert prior_window last_date < current_game_date |
| PIT5_no_production_jsonl_overwrite | PREDICTION_JSONL_OVERWRITTEN 必須保持 False；Phase 73 輸出寫入獨立 reports/ 路徑 |
| PIT6_replay_only_output_path | Phase 73 output 必須寫入 reports/phase73_*.json；不得被任何 execution module import |

---

## 四、Phase 73 成功與失敗條件

### 成功條件（所有必須達成）

| 條件 | 測量方式 |
|------|---------|
| SC1: Brier delta 改善，CI 穩定 | shadow Brier < original Brier，bootstrap 95% CI 排除 0，CI width ≤ 0.10 |
| SC2: ECE 不明顯劣化 | shadow ECE − original ECE ≤ 0.005 |
| SC3: 目標段 market risk 降低 | shadow Brier ≤ market Brier + 0.005 in 0.65–0.70 band |
| SC4: NC 不顯示 overfit | 6 個負向對照組中 overfit_risk < 4/6 |
| SC5: guard coverage 不過度擴張 | 觸發率 ≤ 15% of all games |
| SC6: 無 production mutation | CANDIDATE_PATCH_CREATED = False, PRODUCTION_MODIFIED = False |

### 失敗條件（任一觸發即 fail）

| 條件 | 測量方式 |
|------|---------|
| FC1: CI 不排除零 | shadow Brier improvement CI includes 0 → Not actionable |
| FC2: 只在單一 split 成立 | < 3/5 窗口改善 → split instability |
| FC3: NC 顯示 overfit | ≥ 4/6 NC overfit_risk → noise mining |
| FC4: coverage 過度擴張 | > 15% all games → scope too broad |
| FC5: market replacement 傷害其他段 | 非目標段 Brier 劣化 > 0.003 → negative spillover |
| FC6: PIT-safe 無法達成 | any required_input 無法確認開賽前可得 → cannot use in live setting |

---

## 五、Risk Register

| risk_name | severity | likelihood | 重要說明 |
|-----------|----------|------------|---------|
| leakage_risk | **HIGH** | MEDIUM | Rolling window 最高風險；Phase 73 必須驗證 temporal ordering |
| overfit_risk | **HIGH** | MEDIUM | n=103 borderline；不可從 eval 選 threshold |
| market_over_reliance_risk | MEDIUM | MEDIUM | G4 shadow_blend 必須標示 PAPER_SHADOW_ONLY |
| model_devaluation_risk | MEDIUM | LOW | Guard 只覆蓋 5.1% 的場次；其他段不受影響 |
| sample_concentration_risk | MEDIUM | MEDIUM | LAD+MIL = 23.4%；Phase 73 需留一隊測試 |
| threshold_mining_risk | **HIGH** | **HIGH** | 所有 threshold 未 eval-fit；Phase 73 需測多值 |
| governance_bypass_risk | **HIGH** | LOW | Guard output 不得被 execution module 消費 |
| production_mutation_risk | **HIGH** | LOW | 凍結常數保護；Phase 73 runner 必須 assert |

**4 個 HIGH severity risk**，均有對應的 Phase 73 required check。

---

## 六、Governance Rules

| rule_id | 核心規則 |
|---------|---------|
| GOV1_no_edge_claim | **不得宣稱任何投注 edge**；Brier 改善是 de-risk metric，非 ROI signal |
| GOV2_no_profit_claim | 不計算 EV / Kelly / 盈虧 |
| GOV3_no_production_patch | Phase 72/73 不產生 production patch；Phase 74+ 才能討論 |
| GOV4_no_automatic_execution | Guard output 不得連接 betting execution / stake logic |
| GOV5_replay_only | Phase 73 為 replay-only mode；不修改 live pipeline |
| GOV6_human_review_required | Phase 73 gate passage 需人工審核後才能進 Phase 74 |
| GOV7_rollback_plan | 若 Phase 74+ 實施，需提供 git rollback hash + JSONL backup |
| GOV8_audit_log_requirement | 每次執行必須寫入 JSON audit log（含 safety constants, gate, timestamp）|
| GOV9_report_path_requirement | 所有輸出寫入 `reports/phase72_*.json`；不寫入 data/ 或 live/ |

---

## 七、Phase 73 Simulation Design（設計稿，未執行）

> Phase 73 需人工 CTO 審核本報告後才得啟動。

| 項目 | 設計值 |
|------|-------|
| input JSONL | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` |
| output JSON | `reports/phase73_market_derisk_guard_replay_<date>.json` |
| output Markdown | `00-BettingPlan/<date>/phase73_market_derisk_guard_replay_report_<date>.md` |
| replay method | Historical replay；依日期排序；逐場計算 guard trigger；記錄 shadow prediction；計算 Brier/ECE |
| train/eval split | 時間切割：前 70% = train（threshold derivation）；後 30% = eval（Brier evaluation only）|
| min eval N | 0.65–0.70 band eval window 需 ≥ 20 筆 |
| trigger candidates | G1–G5（排除 G6 優先級最低）|
| action candidates | market_only_shadow / de_risk_flag_only / abstain_wording / market_weight_cap_proposal / route_to_manual_review |
| metrics | Brier, ECE, residual_mean, coverage_rate, bootstrap 95% CI, per-window Brier, per-team concentration |
| negative controls (6) | shuffled_market_assignment / shuffled_model_assignment / random_shadow_assignment / random_sp_fip_bucket / random_split_assignment / out_of_band_guard |
| bootstrap plan | 1000 samples, rng_seed=42, CI width ≤ 0.10 穩定條件 |
| gate candidates | PHASE73_GUARD_VALIDATED / PHASE73_GUARD_MARGINAL / PHASE73_GUARD_OVERFIT / PHASE73_DATA_LIMITED / PHASE73_NOT_ACTIONABLE / STOP_PATCH_SEARCH_RETURN_TO_P1 |
| completion marker | `PHASE_73_MARKET_DERISK_GUARD_REPLAY_VERIFIED` |

---

## 八、Gate 決策

### Gate Risk Notes（重要警示）

⚠️ **GOV_RISK**: governance_bypass_risk 為 HIGH severity。Phase 73 開始前必須明確設立 guard output isolation。  
⚠️ **THRESHOLD_MINING**: threshold_mining_risk 為 HIGH/HIGH。Phase 73 必須對每個 threshold 測試 3+ 個值。  
⚠️ **OVERFIT_RISK**: Phase 71 NC count = 2/6。Phase 73 必須重複 NC 測試設計。  
⚠️ **COMPRESSION**: model_std/market_std = 0.267。Shadow improvement 可能是機械性結果，非結構性優勢。  
⚠️ **SAMPLE_SIZE**: Phase 73 eval window 約 ~30 筆 target-band games；CI 會偏寬，請管理預期。

### 🎯 GATE: `MARKET_DERISK_GUARD_SPEC_READY`

**Rationale**:  
Phase 71 evidence is strong: Brier delta=+0.0140, CI=[+0.0048, +0.0240] stable and excludes 0, 5/5 windows consistent, nc_overfit_risk=2/6. Guard spec is complete: 5 recommended guards (all PIT-safe), 6 required PIT rules, 6 success + 6 failure criteria. Spec is clear and PIT-safe. Phase 73 replay is the next step.

**注意**：使用 `MARKET_DERISK_GUARD_SPEC_READY` 而非 `MARKET_DERISK_REPLAY_READY`，因為 Phase 73 simulation design 雖已完整，但尚未獨立執行並由人工 CTO 審核。Phase 73 只在本報告獲得 CTO 批准後才得啟動。

---

## 九、推薦 Guard Candidates

**推薦（5 個）**:
1. **G1_band_shadow** — 最保守，zero production risk，適合作為 Phase 73 基線
2. **G2_band_disagreement_flag** — 縮小範圍至高分歧游戲，具體可測
3. **G3_band_compression_abstain** — 抑制過度自信表述，無機率變更
4. **G4_band_market_weight_cap_proposal** — shadow blend 測試，governance risk 最高但可控
5. **G5_band_manual_review_route** — 結合 sp_fip 資訊，人工審核路徑

**建議 Phase 73 優先序**: G1 → G2 → G4 → G5 → G3

**被拒絕（1 個）**:
- **G6_band_prior_split_evidence_only** — 實作複雜度高，leakage risk 最大；暫緩至 G1/G2 驗證後再評估

---

## 十、Phase 73 建議

**Phase 73 replay simulation 建議進行**，條件如下：
1. 本報告（Phase 72）已獲 CTO 人工審核
2. Phase 73 必須嚴格按照本報告的 PIT-safe rules 實施
3. Phase 73 不得修改 production model、alpha、或 prediction JSONL
4. Phase 73 gate 若非 `PHASE73_GUARD_VALIDATED`，應回到 P1 governance

**Phase 73 結束後的決策樹**：
- `PHASE73_GUARD_VALIDATED` → 可考慮 Phase 74 production patch proposal（需另行 CTO 審核）
- 任何其他 gate → 停止 patch path，回到 P1 governance（LeagueAdapter / Budget Guard / Metrics SSOT / governance hardening）

---

## 十一、相關檔案

- 完整結果 JSON：`reports/phase72_market_derisk_guard_proposal_20260507.json`
- Orchestrator：`orchestrator/phase72_market_derisk_guard_proposal.py`
- Runner：`scripts/run_phase72_market_derisk_guard_proposal.py`
- 測試套件：`tests/test_phase72_market_derisk_guard_proposal.py` (123 tests, all pass)

---

PHASE_72_MARKET_DERISK_GUARD_PROPOSAL_VERIFIED
