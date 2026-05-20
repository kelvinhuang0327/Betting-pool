# P6 任務提示 (P6 Task Prompt)

**前置條件**: P5 完成 (`P5_REAL_MODEL_PROBABILITY_INTEGRATION_READY`)  
**P5 核心發現**: 真實校準模型 BSS = -0.0188（負值），閘門阻擋推薦  

---

## P6 目標

P5 已成功整合真實模型概率，但 BSS 為負代表現有模型未能優於市場基準。  
P6 任務是**診斷 BSS 為負的根因，並嘗試修復或識別模型有優勢的子市場**。

---

## P6 任務清單

### Task 1: BSS 診斷分析

執行分析管線，回答以下問題：

1. 模型在哪些月份/球場類型/主場球隊 BSS > 0？
2. 校準曲線（Reliability Diagram）是否顯示系統性偏誤？
3. 模型概率的信賴區間分佈是否集中（過度自信）或分散（欠缺信心）？

**產出**: `00-BettingPlan/20260511/p6_bss_diagnostic_report.md`

### Task 2: 時間窗口 BSS 分析

按月計算 BSS：
```python
for month in range(4, 10):  # 2025-04 to 2025-09
    rows_in_month = filter(rows, month)
    bss_month = brier_skill_score(model_probs, outcomes)
```

若某月 BSS > 0.01 → 標記為「有效月份」，納入子策略候選。

### Task 3: ECE 校準修復嘗試

若 Reliability Diagram 顯示系統性高估/低估：
1. 對 1,476 場次的 (`model_prob`, `outcome`) 重新擬合 Platt Scaling
2. 使用 Leave-One-Out CV 驗證修復後的 ECE 是否改善
3. 若修復後 BSS > 0 → 更新 `model_outputs_2026-04-29.jsonl` 並重跑 P5 管線

**安全**: 不覆蓋原始素材，輸出至 `data/derived/model_outputs_p6_calibrated_YYYY-MM-DD.jsonl`

### Task 4: 特徵重要性審核

檢查導致模型預測偏誤的特徵：
1. 哪些特徵使模型高估主場優勢？
2. 是否存在 Look-ahead Leakage（即使 P5 已隔離）？
3. 是否有球場效應被模型忽略？

**工具**: `models/` 目錄下的特徵工程模組

### Task 5: 子市場策略搜尋

若整體 BSS < 0，嘗試找到正 BSS 子市場：
- 按投手（Starter）分組：有王牌投手出賽時 BSS 是否為正？
- 按賠率區間分組：平盤賽事（-120 to +120）vs 強弱懸殊賽事
- 按總分 O/U 分組：高分賽事 vs 低分賽事

若任一子市場 BSS > 0 且 sample_size >= 100 → 設計子策略並運行 P5 管線

### Task 6: P6 報告

產出 `00-BettingPlan/20260511/p6_model_improvement_report.md`，包含：
- BSS 診斷根因
- 校準修復嘗試結果
- 有效子市場（如有）
- 下一步行動建議

**最終標記**: `P6_MODEL_CALIBRATION_DIAGNOSTIC_READY`

---

## 重要約束 (Constraints)

- `paper_only = True` 永遠不可更改
- 不可覆蓋原始模型輸出素材
- 所有輸出限定在 `outputs/` PAPER zone
- 不得接觸 LotteryNew 或生產系統
- 樣本數 >= 30 才能計算 BSS；子市場分析需 >= 100

---

## 環境資訊

- Python: 3.13.8 in `.venv/`
- 真實模型概率素材: `data/derived/model_outputs_2026-04-29.jsonl` (1,476 場次)
- 已合併概率的賠率 CSV: `outputs/predictions/PAPER/2026-05-11/mlb_odds_with_model_probabilities.csv`
- P5 模擬結果: `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_*.jsonl`
