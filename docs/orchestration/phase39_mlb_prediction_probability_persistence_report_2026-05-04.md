# Phase 39: MLB Prediction Probability Persistence Report

> 生成日期：2026-05-04  |  Run: 2026-05-04T05:01:29.689549+00:00

---

## 🎯 Phase 目標

持久化 MLB 回測的每場預測機率到 JSONL，使 BSS / Brier / ECE / 校準實驗 可從存檔行重新計算，無需重跑模型。

## 📂 預測檔案狀態

| 項目 | 值 |
|------|----|
| 檔案路徑 | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl` |
| 檔案存在 | ❌ 否 |
| 預測行數 | 0 |
| 重複 dedupe_key 數 | 0 |

## ⚠️ RAW_MODEL_PROB_MISSING

每場模型機率尚未存入磁碟。確切缺少位置：

```
wbc_backend/evaluation/full_backtest.py :: FullBacktestEngine.run() → per-game test loop → result.home_win_prob (computed but not persisted to disk in baseline version). Resolution: instantiate FullBacktestEngine(persist_predictions=True) and re-run the backtest to generate data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl
```

**解決方式**：
```python
from wbc_backend.evaluation.full_backtest import FullBacktestEngine
engine = FullBacktestEngine(persist_predictions=True)
report = engine.run(records)
# → data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl
```

## 🔒 安全閘門狀態

- **BSS Safety Gate**: 🔐 BLOCKED
- **patch_gate_unlocked**: false
- 禁止動作：production_prediction、live_bet、kelly_bet、candidate_patch_eval

## 📋 備註

- Prediction JSONL not found at: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl
- To generate: run FullBacktestEngine(persist_predictions=True).run(records)
- Missing location: wbc_backend/evaluation/full_backtest.py :: FullBacktestEngine.run() → per-game test loop → result.home_win_prob (computed but not persisted to disk in baseline version). Resolution: instantiate FullBacktestEngine(persist_predictions=True) and re-run the backtest to generate data/mlb_2025/derived/mlb_2025_per_game_predictions.jsonl

## ✅ 驗證碼

```
RAW_MODEL_PROB_MISSING
```
