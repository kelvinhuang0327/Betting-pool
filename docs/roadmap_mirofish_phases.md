# MiroFish 借鑑開發路線圖

> 更新日期：2026-03-12
> 目標：窮盡所有方法提高棒球賽事預測成功率，達成資產翻倍

---

## ✅ 已完成

### Phase 1 — 棒球知識圖譜特徵層
- 檔案：`wbc_backend/features/knowledge_graph.py`
- 方法：NetworkX + SQLite 本地圖譜，無外部依賴
- 輸出：Category K，17 個圖結構特徵
- 防護：截止日期機制，100% 無 Look-ahead Leakage
- 測試：7 tests 全過

### Phase 2 — NLP 賽前語義特徵層
- 檔案：`wbc_backend/features/nlp_extractor.py`
- 方法：多 Provider（Groq/Gemini/Anthropic/OpenRouter/Ollama）+ 規則引擎 fallback
- 輸出：Category L，11 個語義特徵
- Provider 設定：`.env` 填入 `GROQ_API_KEY`（免費）即可啟用
- 測試：7 tests 全過

### Phase 3 — 博彩市場代理人模擬器
- 檔案：`wbc_backend/betting/market_simulator.py`
- 方法：1000 代理人（散戶/大戶/財團）× 60 輪，純 Python，< 5 秒
- 輸出：Category M，10 個市場微結構特徵（CLV/Steam/最佳時機）
- 測試：6 tests 全過

### Phase 4 — 整合 + 測試驗證
- `alpha_signals.py` 擴充 Category K/L/M
- `build_alpha_signals()` 新增 `pregame_text`, `cutoff_date`, `enable_*` 參數
- `settings.py` 新增 `LLMConfig`（Provider 設定）
- 測試套件：`tests/test_mirofish_integration.py`（27 tests）
- **總測試：209 passed，0 failed**

---

## ✅ 已完成（Phase 5）

### Phase 5A — 統計本體自動發現（Ontology Discovery）
- 檔案：`wbc_backend/features/ontology_discovery.py`
- 方法：互信息（MI）+ Pearson/Spearman 相關性 + 條件互信息（CMI）
- 輸出：`OntologyReport`（特徵重要性排名 + 交互作用建議 + 剪枝清單）
- 測試：12 tests 全過

### Phase 5B — 階層式蒙特卡洛升級（Hierarchical Monte Carlo）
- 檔案：`wbc_backend/simulation/hierarchical_mc.py`
- 方法：4 層修正架構（基礎 MC → 市場 → 知識圖譜 → NLP 方差）
- 輸出：`HierarchicalSimResult`（含 95% CI、透明稽核日誌）
- 各層上限：Layer 2 ±15% λ，Layer 3 ±8% λ，Layer 4 variance [0.10~0.50]
- 測試：12 tests 全過

### Phase 5C — 特徵自動剪枝（Auto Feature Pruning）
- 檔案：`wbc_backend/features/feature_selector.py`
- 方法：排列重要性（LogReg）+ SHAP（可選）+ K-fold 穩定性過濾
- 輸出：`FeatureSelectorResult`（JSON 持久化，供 dynamic_ensemble 前置）
- 測試：15 tests 全過

### Phase 5 整合測試
- 測試套件：`tests/test_phase5_integration.py`（42 tests 全過）
- **總測試：251 passed，0 failed**

---

## 🔄 待辦（中期）

### ~~Phase 5A — 統計本體自動發現（Ontology Discovery）~~ ✅ 完成
- 借鑑：MiroFish `ontology_generator.py`（LLM 本體生成 → 改為統計版）
- 目標：從歷史賽事資料自動發現特徵關係與交互作用
- 方法：互信息（MI）、卡方、Pearson/Spearman 相關性、條件測試
- 輸出：
  - 特徵重要性排名（相對於勝負結果）
  - 建議新交互特徵（如「高濕度 × 右投手 → 轉速下降」）
  - 自動排除低重要性特徵（剪枝）
- 檔案：`wbc_backend/features/ontology_discovery.py`
- 整合：`alpha_signals.py` → 動態選擇最佳特徵子集

### Phase 5B — 階層式蒙特卡洛升級（Hierarchical Monte Carlo）
- 借鑑：MiroFish 多層平行模擬架構
- 目標：整合 K/L/M 三層新特徵至蒙特卡洛，提升 CLV 精度
- 方法：
  - Layer 1（現有）：逐局 Gamma-Poisson 50,000 次
  - Layer 2（新增）：市場微結構修正（market_simulator 輸出調整 λ 參數）
  - Layer 3（新增）：知識圖譜加權（歷史對決優勢 → 投打能力調整）
  - Layer 4（新增）：NLP 情境修正（傷兵/天氣 → 標準差動態擴張）
- 輸出：`HierarchicalSimResult`（含不確定性區間）
- 檔案：`wbc_backend/simulation/hierarchical_mc.py`
- 整合：向後相容，不改動現有 `monte_carlo.py`

### Phase 5C — 特徵自動剪枝（Auto Feature Pruning）
- 目標：從 277+ 特徵中自動保留最高預測力子集
- 方法：排列重要性（Permutation Importance）+ SHAP
- 輸出：穩定特徵集 JSON（每週自動更新）
- 檔案：`wbc_backend/features/feature_selector.py`
- 整合：`dynamic_ensemble.py` 訓練前置步驟

---

## ✅ 已完成（Phase 6）

### Phase 6A — 棒球世界模型（Baseball World Model） ✅
- 檔案：`wbc_backend/simulation/world_model.py`
- 方法：逐打席（PA-level）模擬，球員個性化習慣（投手 k/bb/stuff，打者 barrel/babip/sprint）
- 輸出：`WorldModelResult`（分佈型預測）
  - tail_risk_score：P(總分 ≥ 15)，blowout_prob：P(差距 ≥ 7)，shutout_prob
  - score_distribution（top 15 比分），total_runs_dist（0-25 全分佈）
  - 95% 精英投手降低對面得分 ✅ 驗證通過
- 測試：17 tests 全過

### Phase 6B — 多智能體強化學習策略（MARL） ✅
- 檔案：`wbc_backend/strategy/marl_optimizer.py`
- 三智能體：PredictorAgent（ELO+市場+wOBA+FIP）/ StrategistAgent（Kelly）/ RiskControllerAgent
- 演化策略（ES）+ 精英保留，50 代 × 10 候選 < 60 秒
- 輸出：`OptimizationResult`（最優參數 + 訓練/測試集 ROI/Brier/Sharpe）
- 測試：18 tests 全過

### Phase 6C — 實時數據管道 ✅（P0-2 同步完成）

## ✅ 已完成（Phase 7）

### Phase 7A — 統一預測管道（Prediction Orchestrator） ✅
- 檔案：`wbc_backend/pipeline/prediction_orchestrator.py`
- 方法：Logit-space 加權融合（MARL 40% + HierarchicalMC 35% + WorldModel 25%）
- 輸入彈性：僅 GameRecord → 三模型全開（依可用資料自動選擇）
- 輸出：`OrchestratorResult`（融合機率 + 95% CI + Kelly 建議 + 稽核日誌）
- 測試：54 tests 全過

### Phase 7B — MLB 2025 完整回測報告生成器 ✅
- 檔案：`wbc_backend/evaluation/full_backtest.py`
- 腳本：`scripts/run_mlb_backtest.py`
- 方法：Walk-Forward（5 視窗 × 80/20，MARL 獨立優化）
- 輸出：`report/mlb_2025_full_backtest.md`（準確率/Brier/ROI/Sharpe/calibration ECE）
- 結果：54.5% 準確率，Brier 0.2796，ROI +2.8%，p < 0.0001

---

## 🔬 待辦（長期研究）

### Phase 8A — 校準優化（Probability Calibration） ✅
- 檔案：`wbc_backend/calibration/probability_calibrator.py`
- 方法：Temperature Scaling（<20 樣本）/ Platt Scaling（20-100）/ Isotonic Regression（≥100）
- 自動選擇，Walk-Forward 整合，降低 ECE（目標 < optimizer 門檻 0.12）
- 整合：`FullBacktestEngine(use_calibration=True)`，報告含 cal_brier/cal_ece/cal_skill
- 測試：43 tests 全過

### Phase 8B — 特徵接入實時球員資料
- 目標：接入 MLB Stats API 真實球員數據（取代代理 wOBA/FIP）
- 整合：`data/mlb_live_pipeline.py` → `WorldModel` 球員快照

---

## 📊 系統現況快照

| 指標 | 現況 |
|-----|------|
| 總特徵數 | 277（含 K/L/M 三新層） |
| 測試覆蓋 | **445 tests，0 failures** |
| LLM Provider | Groq（免費）/ Gemini / Anthropic / OpenRouter / Ollama |
| 市場模擬 | 1000 代理 × 60 輪，< 5 秒 |
| 蒙特卡洛 | 50,000 次（階層式 4 層修正 ✅） |
| 回測數據 | **2,430 場**（MLB 2025 全季，P0 ✅） |
| 實時資料 | **MLB Stats API 管道**（P0 ✅，5min 快取） |
| 預測準確率 | **54.5%**（Walk-Forward，MLB 2025） |
| 統計顯著性 | **p < 0.0001**（vs 亂猜） |

---

## ✅ P0 問題已解決

1. **✅ 回測數據不足**：37 → **2,430 場**（MLB 2025 全季）
   - 檔案：`data/mlb_data_loader.py`
   - 含滾動 Elo、wOBA/FIP 代理、市場隱含機率、休息天數、RSI
   - 主隊勝率 54.3%，平均得分 8.89/場（MLB 正常範圍）

2. **✅ 無實時資料管道**：MLB Stats API 免費管道實裝
   - 檔案：`data/mlb_live_pipeline.py`
   - 抓取今日/近期比賽 → GameRecord（5 分鐘快取）
   - `merge_with_live()` 自動合併歷史 CSV + 即時 API（去重）

---

## 快速指引

```bash
# 啟用 LLM（填入 Groq 免費 Key）
echo "GROQ_API_KEY=gsk_xxx" >> .env

# 執行全套測試
python3 -m pytest tests/ -q

# 執行含三新層的特徵計算
python3 -c "
from wbc_backend.features.alpha_signals import build_alpha_signals
# ... 見 tests/test_mirofish_integration.py 範例
"
```
