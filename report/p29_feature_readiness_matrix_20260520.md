# P29 Feature Readiness Matrix
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 特徵就緒狀態矩陣

| Feature Group | 狀態 | 預估 Brier 改善 | 回測可行 | 工程成本 |
|---------------|------|----------------|---------|---------|
| 市場賠率（current） | ✅ CURRENTLY_AVAILABLE | 0（已達天花板 0.244） | — | — |
| Run-line signal | ⚠️ REPO_PROXY_AVAILABLE | 0（P28 測試無效）| YES | LOW |
| Starting pitcher ERA/FIP | 🔴 EXTERNAL_REQUIRED | **-0.005 至 -0.015** | YES | LOW-MED |
| Bullpen fatigue (IP_7d) | 🔴 EXTERNAL_REQUIRED | **-0.002 至 -0.007** | YES | LOW |
| Batting form (rolling wOBA) | 🔴 EXTERNAL_REQUIRED | **-0.003 至 -0.010** | YES | MEDIUM |
| Lineup/Injury proxy | 🔴 EXTERNAL_REQUIRED | -0.002 至 -0.006 | PARTIAL | HIGH |
| Park / Weather | 🔴 EXTERNAL_REQUIRED | -0.001 至 -0.003 | PARTIAL | MEDIUM |

---

## 禁止使用的特徵

| 特徵 | 禁止原因 |
|------|---------|
| 今日賽事賽後統計 | 未來資訊 |
| Closing odds 作為賽前特徵 | Look-ahead leakage |
| 投注截止後陣容更新 | 未來資訊 |
| Result-derived fields | 循環定義 |
| 未授權爬蟲 PII | 合規 + 技術風險 |

---

## 突破天花板路線圖

```
當前 ceiling: 0.244（市場賠率 + 牌局 RL 信號）

Step 1 (Orchestrator simplification):
  w_market: 0.30 → 0.50
  Expected: 0.244 → 0.244 (minor, already at market ceiling)

Step 2 (SP stats added):
  Pitcher ERA/FIP from MLB API (free)
  Expected: 0.244 → ~0.234 (-0.010)

Step 3 (Batting form added):
  Team rolling wOBA from FanGraphs
  Expected: ~0.234 → ~0.228 (-0.006)

Step 4 (Bullpen fatigue):
  IP_7d from MLB Stats API
  Expected: ~0.228 → ~0.224 (-0.004)

Step 5 (Park + Lineup proxy):
  Park factor from FanGraphs, IL list from MLB API
  Expected: ~0.224 → ~0.221 (-0.003)

Target: < 0.22 (requires full external stack)
```

---

## P29 Decision 矩陣

| Decision | 值 |
|---------|---|
| Orchestrator noise found | ✅ YES — w_market=0.30 太低 |
| Simplification candidate | ✅ P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND |
| External data contract complete | ✅ P29_EXTERNAL_DATA_CONTRACT_READY |
| Ceiling analysis | ✅ P29_EXTERNAL_FEATURES_REQUIRED_TO_BREAK_CEILING |

**Combined final classification**:
1. `P29_ORCHESTRATOR_NOISE_REMOVAL_CANDIDATE_FOUND`
2. `P29_EXTERNAL_DATA_CONTRACT_READY`
3. `P29_EXTERNAL_FEATURES_REQUIRED_TO_BREAK_CEILING`

---

## 下一步行動建議（優先序）

| 優先度 | 行動 | 預期影響 | 工程成本 |
|--------|------|---------|---------|
| P1 | 調高 MARL w_market: 0.30 → 0.50（diagnostic only） | Brier -0.002 至 -0.005 | 極低 |
| P2 | 引入 SP ERA/FIP from MLB Stats API | Brier -0.005 至 -0.015 | 低-中 |
| P3 | 引入 bullpen IP_7d from MLB API | Brier -0.002 至 -0.007 | 低 |
| P4 | 引入 park factor from FanGraphs CSV | Brier -0.001 至 -0.003 | 低 |
| P5 | 引入 batting rolling wOBA | Brier -0.003 至 -0.010 | 中 |

**所有行動均為 paper-only diagnostic，不得 promotion，不替換 champion。**
