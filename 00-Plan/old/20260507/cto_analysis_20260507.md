已更新 roadmap：[betting_roadmap_20260504.md](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/00-BettingPlan/betting_roadmap_20260504.md:5)。

今日 CTO 結論：P0 改為 Phase69 calibration objective / probability shaping paper-only counterfactual；`LeagueAdapter`、Budget Guard、Metrics SSOT 下修為本週 P1；bullpen / SP fatigue / market / context feature patch 路線降為 P2。

```text
你是 Betting-pool MLB 系統的 Worker Agent。

任務名稱：
Phase 69 — Calibration Objective Redesign Counterfactual with OOF / PIT-safe Validation

日期：
2026-05-07

背景：
Phase59-68 已完成 heavy_favorite / high_confidence failure root-cause 排查。
Bullpen granular、SP fatigue、market microstructure、context feature-family patch 路線已降級。
Phase68 gate = CALIBRATION_OBJECTIVE_REDESIGN_PROMISING。
Phase68 已定位 probable causes：
- models/stacking_model.py 內 away_wp * 0.9 favorite sharpening
- models/stacking_model.py 內 logit / 0.85 confidence sharpening
- steam * 0.25 可能造成 market signal double incorporation

任務目的：
建立 paper-only counterfactual，評估 calibration objective / probability shaping / ensemble output 是否值得進入 Phase70 paper-only patch gate。不得建立 production patch。

核心要求：
1. 不修改 production model。
2. 不調整 production market_blend alpha。
3. 不覆蓋 production prediction JSONL。
4. 不用 in-sample fit-and-evaluate。
5. calibration training data 必須嚴格早於 evaluation data。
6. 至少比較 original_baseline、remove_logit_sharpening、remove_away_damping、remove_both、OOF isotonic、OOF Platt、confidence-band abstention diagnostic。
7. segmentation 至少包含 all games、heavy_favorite >= 0.70、high_confidence >= 0.75、extreme_favorite >= 0.80、model_prob bands、Phase45 failure segment。
8. metrics 至少包含 Brier、BSS、ECE、bucket-level ECE、heavy_favorite ECE、high_confidence BSS、bootstrap CI。
9. negative controls 至少包含 shuffled probability band、random confidence assignment、irrelevant bucket split。
10. report 必須明確判斷是否值得進 Phase70，或停止 patch search。

輸出檔案：
- orchestrator/phase69_calibration_objective_redesign_counterfactual.py
- scripts/run_phase69_calibration_objective_redesign_counterfactual.py
- tests/test_phase69_calibration_objective_redesign_counterfactual.py
- reports/phase69_calibration_objective_redesign_counterfactual_20260507.json
- 00-BettingPlan/20260507/phase69_calibration_objective_redesign_counterfactual_report_20260507.md

Gate 結論七選一：
- CALIBRATION_OBJECTIVE_PATCH_PROMISING
- PROBABILITY_SHAPING_REMOVAL_PROMISING
- ENSEMBLE_WEIGHTING_REPAIR_PROMISING
- ABSTENTION_GUARD_PROMISING
- OVERFIT_RISK
- DATA_LIMITED
- CALIBRATION_OBJECTIVE_NOT_PROMISING

驗收條件：
- 所有新增 tests 通過
- Phase67 / Phase68 targeted regression 不破壞
- candidate_patch_created = false
- production_modified = false
- alpha_modified = false
- report 明確說明 Phase70 是否值得進行

完成標記：
PHASE_69_CALIBRATION_OBJECTIVE_REDESIGN_COUNTERFACTUAL_VERIFIED
```
