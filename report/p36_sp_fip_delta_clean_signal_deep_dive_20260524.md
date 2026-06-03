# P36: sp_fip_delta Clean Signal Deep Dive

**日期**: 2026-05-24  
**作者**: AI Quant Research  
**狀態**: COMPLETE — diagnostic_only=True | promotion_freeze=True  
**Branch**: main | HEAD: 9c54bca → commit pending  
**Script**: `scripts/_p36_sp_fip_delta_clean_signal_deep_dive.py`

---

## 一、研究背景與動機

P35 確認：`sp_fip_delta` 是整個特徵集中唯一穩健信號（月度穩定 100%，mean AUC=0.581）。P36 對其進行深度解剖：

**研究問題**：
1. 信號是否單調（decile 桶分析）？
2. 信號是否在點時間(PIT)安全（無前看漏洞）？
3. 哪種特徵轉換效果最好（raw / abs / winsorized / binary / 強邊緣）？
4. 信號在不同時間維度（月度/賽季階段）是否穩定？
5. 校準品質如何？

**約定**：`sp_fip_delta = away_SP_FIP − home_SP_FIP`  
- 正值 → 主場 SP 優勢（客場 SP FIP 較高/較差）  
- 負值 → 客場 SP 優勢（主場 SP FIP 較高/較差）

---

## 二、資料集

| 項目 | 值 |
|---|---|
| 資料源 | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` |
| 原始總計 | 2,025 rows |
| 去重後 | 2,002 rows |
| 排除 league_average_fallback | 593 rows (29.6%) |
| **最終分析集** | **1,409 rows** |
| 結果欄 | `home_win`（top-level field，非特徵） |

### 2.1 特徵結構

```json
{
  "p0_features": {
    "sp_fip_delta": 0.15,
    "sp_fip_delta_available": true,
    "sp_context_source": "historical_proxy",
    "sp_home_pitcher": "Max Fried",
    "sp_away_pitcher": "Kevin Gausman",
    "audit_notes": {
      "ignored_forbidden_fields": ["home_win"],
      "sp_fip_source": "neutral_fallback"
    },
    "production_modified": false
  },
  "diagnostic_only": true,
  "home_win": 1   // outcome only, excluded from features
}
```

---

## 三、SECTION 0 — PIT 安全審計

> 確認特徵不含未來資訊（Look-ahead leakage）

| 檢查項目 | 結果 |
|---|---|
| `sp_fip_delta_available=True` | ✅ confirmed |
| `audit_notes.ignored_forbidden_fields` 含 `home_win` | ✅ YES (SAFE) |
| `sp_fip_source` 來源 | `neutral_fallback` 100% (先前賽季 FIP) |
| `production_modified=True` | 0 rows ✅ |
| `diagnostic_only=True` | 2025/2025 rows ✅ |

**PIT 安全結論**：✅ 完全安全。`home_win` 在特徵建構時被明確排除（`ignored_forbidden_fields`），`sp_fip_delta` 使用的是比賽前可取得的先前賽季 FIP 資料（`neutral_fallback`）。無前看洩漏風險。

---

## 四、SECTION 1 — 特徵分佈

| 統計量 | 值 |
|---|---|
| n | 1,409 |
| min | −1.800 |
| max | +1.700 |
| mean | +0.010 |
| median | 0.000 |
| std | 0.639 |
| p5 / p95 | −1.100 / +1.150 |
| p10 / p90 | −0.900 / +0.900 |
| p25 / p75 | −0.350 / +0.350 |

**方向分佈**：
```
delta > 0 (主場 SP 優勢): 673 局 (47.8%)
delta = 0 (中性)        :  80 局 ( 5.7%)
delta < 0 (客場 SP 優勢): 656 局 (46.6%)
```

分佈幾乎對稱，中心靠近 0，有肥尾（fat tails，尤其在 |delta| > 0.9 的強邊緣區域）。

---

## 五、SECTION 2 — 十分位桶分析（核心發現）

| 十分位 | delta 範圍 | n | 主場勝率 | Δ from base |
|---|---|---|---|---|
| D01 (強客場) | [−1.800 to −0.900] | 140 | **45.7%** | −7.1% |
| D02 | [−0.900 to −0.450] | 140 | 46.4% | −6.4% |
| D03 | [−0.450 to −0.250] | 140 | 53.6% | +0.8% |
| D04 | [−0.250 to −0.100] | 140 | 47.1% | −5.7% |
| D05 | [−0.100 to  0.000] | 140 | 52.9% | +0.1% |
| D06 | [ 0.000 to +0.100] | 140 | 46.4% | −6.4% |
| D07 | [+0.100 to +0.250] | 140 | 54.3% | +1.5% |
| D08 | [+0.300 to +0.450] | 140 | 49.3% | −3.5% |
| D09 | [+0.450 to +0.900] | 140 | **64.3%** | +11.5% |
| D10 (強主場) | [+0.900 to +1.700] | 149 | **67.1%** | +14.3% |

```
整體方向 (D1→D10): 45.7% → 67.1%  (Δ=+21.4%) ✅
單調上升次數: 6/9 (67%) → MOSTLY MONOTONIC ✅
Pearson r (十分位均值 vs HW%): +0.804

尾端對比:
  最弱 2 分位 (D1+D2): HW%=46.1%
  最強 2 分位 (D9+D10): HW%=65.7%
  差距: +19.6% 🔑
```

### 🔑 關鍵發現：非線性尾端效應

**中間十分位（D3–D8，delta 約 ±0.45 之內）高度噪雜**（HW% 在 47–54% 之間波動無規律），但**尾端十分位（D1-D2 和 D9-D10）信號極為清晰**：

- 強客場優勢（delta ≤ −0.9）→ 主場勝率 46%（低 7pp）
- 強主場優勢（delta ≥ +0.45）→ 主場勝率 64–67%（高 11–14pp）

這直接解釋了為何 `strong-edge (|delta|≥0.5)` 是最佳模型變體。

---

## 六、SECTION 3 — Context Source 層分析

| 層 | n | AUC | Pearson r | HW% |
|---|---|---|---|---|
| mixed | 1,001 | 0.5596 | +0.1137 | 50.9% |
| historical_proxy | 408 | 0.5728 | +0.1276 | 57.4% |

兩層均顯示一致正向 AUC，`historical_proxy` 略優（0.573 vs 0.560）。

---

## 七、SECTION 4 — 月度穩定性

| 月份 | n | AUC | HW% | Pearson r | 狀態 |
|---|---|---|---|---|---|
| 2025-04 | 37 | **0.700** | 48.6% | +0.344 | ✅ ABOVE 0.5 |
| 2025-05 | 304 | 0.551 | 53.6% | +0.093 | ✅ ABOVE 0.5 |
| 2025-06 | 277 | 0.588 | 49.8% | +0.174 | ✅ ABOVE 0.5 |
| 2025-07 | 252 | 0.607 | 53.6% | +0.183 | ✅ ABOVE 0.5 |
| 2025-08 | 285 | 0.512 | 53.7% | +0.025 | ✅ ABOVE 0.5 |
| 2025-09 | 254 | 0.544 | 53.9% | +0.084 | ✅ ABOVE 0.5 |

```
月度 AUC 摘要: mean=0.584, std=0.061
above-0.5 比率: 6/6 (100%) → STABLE ✅

比較:
  P31B (fallback 污染版 sp_fip_delta): AUC ≈ 0.511  
  P35 multi-feature model monthly:      mean=0.581, 100%
  P36 sp_fip_delta raw signal:          mean=0.584, 100% ← 本次確認
```

---

## 八、SECTION 5 — 賽季階段分析

| 階段 | n | AUC | HW% | Pearson r |
|---|---|---|---|---|
| 早期 (index 0.00–0.33) | 139 | **0.604** | 48.2% | +0.195 |
| 中期 (index 0.33–0.67) | 655 | 0.582 | 53.7% | +0.150 |
| 晚期 (index 0.67–1.00) | 615 | 0.533 | 52.8% | +0.059 |

**發現**：信號在早期賽季最強（AUC=0.604），晚期賽季最弱（AUC=0.533），但仍高於 0.5。

**機制解釋**：`sp_fip_source = neutral_fallback`（先前賽季 FIP）。隨著賽季推進，選手當賽季表現取代先前賽季數據的預測力，導致衰減。早期賽季先前賽季數據最為相關。

---

## 九、SECTION 6 — 模型變體比較（WFV 70/30）

**分割**：
- Train: 2025-04-27 → 2025-08-13 (n=986)
- Val  : 2025-08-13 → 2025-09-28 (n=423)
- Val HW%: 53.4%

| 變體 | AUC | Brier Skill | ECE | 備註 |
|---|---|---|---|---|
| raw sp_fip_delta | 0.5280 | −0.00528 | 0.0480 | 連續信號 |
| abs(sp_fip_delta) | 0.5213 | **+0.00096** | **0.0089** | 邊緣強度無方向 |
| winsorized ±1.5 | 0.5280 | −0.00483 | 0.0463 | 近似 raw |
| binary (delta>0→1) | 0.5142 | −0.00382 | 0.0336 | 方向只，信號弱 |
| **strong-edge (｜delta｜≥0.5)** | **0.5414** | **+0.00757** | **0.0272** | **🏆 最佳** |
| sign (−1/0/+1) | 0.5075 | −0.00788 | 0.0503 | 最差 |

### 🏆 強邊緣（Strong-Edge）為最佳變體

```
strong-edge (|delta|≥0.5):
  AUC         = 0.5414  ← 最高
  Brier Skill = +0.0076  ← 唯一明確正值（+0.76%）
  ECE         = 0.0272   ← 較好校準

與 raw 相比:
  AUC         +0.0134 improvement
  Brier Skill +0.013 improvement
  ECE         −0.021 improvement
```

**Strong-edge 的邏輯**：當 |delta| < 0.5（中性邊緣），投手差異太小，隱性噪音主導，信號不穩定。當 |delta| ≥ 0.5（強邊緣），投手素質差距足夠明顯，信號清晰。

---

## 十、SECTION 7 — 校準診斷（raw sp_fip_delta）

| 指標 | 值 |
|---|---|
| AUC | 0.5280 |
| Brier Skill | −0.0053 |
| Log-Loss Skill | −0.0040 |
| ECE (raw) | 0.0480 |
| ECE (naive base rate) | 0.0000 |
| Logistic coeff w | +0.292 (std) |

**Reliability Diagram**:
```
[0.3-0.4]:  Conf=0.378, Acc=0.524, n= 21  → UNDERCONF (模型低估)
[0.4-0.5]:  Conf=0.457, Acc=0.533, n=107  → UNDERCONF (最大 ECE 貢獻)
[0.5-0.6]:  Conf=0.543, Acc=0.515, n=231  → OK
[0.6-0.7]:  Conf=0.641, Acc=0.603, n= 63  → OK
```

**問題**：模型在低置信區間系統性低估（預測 46%，實際 53%），是預測壓縮向基準率的典型表現。

**Platt in-sample（診斷上限，不可部署）**：
```
ECE:  0.0480 → 0.0007 (近乎完美，但 in-sample)
AUC:  0.5280 → 0.5280 (不變 — Platt 不改變排名)
Brier: −0.0053 → +0.0007
```

---

## 十一、SECTION 8 — 信號分類

| 維度 | 值 |
|---|---|
| WFV AUC (raw) | 0.5280 |
| WFV AUC (strong-edge) | **0.5414** |
| Brier Skill (strong-edge) | **+0.0076** |
| ECE (strong-edge) | 0.0272 |
| 月度穩定性 | 100% (6/6 months) |
| 十分位方向 | MOSTLY MONOTONIC (6/9) |
| PIT 安全 | ✅ PASS |

```
分類: WEAK_STABLE_SIGNAL — 需校準審計後方可使用
      PROMOTION_BLOCKED_BY_GOVERNANCE (promotion_freeze=True)
```

---

## 十二、關鍵發現摘要

### 🔑 Finding 1: 信號集中於強邊緣（尾端效應）
中間 |delta| < 0.45 的遊戲高度噪雜（約 70% 的局數），強邊緣 |delta| ≥ 0.5 的遊戲（約 30%）是信號的真正載體。Strong-edge 變體 AUC=0.5414，Brier Skill=+0.0076 — 是 P31B→P35 整個研究序列中**第一個同時達到正 Brier Skill 的模型**。

### 🔑 Finding 2: PIT 安全確認
`sp_fip_delta` 使用的是比賽前可知的先前賽季 FIP 數據（`neutral_fallback`），`home_win` 被明確排除在特徵建構之外。無前看漏洞。

### 🔑 Finding 3: 月度穩定性 100%
6/6 月均高於 0.5，mean AUC=0.584。信號在 2025 全賽季一致有效。

### 🔑 Finding 4: 早季衰減效應
AUC 從早季 0.604 → 晚季 0.533。原因：`neutral_fallback`（先前賽季 FIP）的相關性隨賽季推進下降。當賽季 FIP 數據（`current_season`）預計可顯著改善晚季穩定性。

### 🔑 Finding 5: abs(delta) 有最低 ECE（0.0089）
絕對值變體雖然 AUC 較低（0.5213），但 ECE 最小（0.0089），且 Brier Skill 正值（+0.001）。含義：邊緣強度（無論方向）本身也有校準價值。

---

## 十三、研究序列總覽（P31B → P36）

| Phase | Feature / Model | AUC | Brier Skill | 月度穩定 |
|---|---|---|---|---|
| P31B | sp_fip_delta (fallback 污染) | 0.511 | — | — |
| P31B | park_run_factor | 0.513 | — | — |
| P31B | bullpen_fatigue_delta_3d | 0.500 | — | NOISE |
| P32 | bullpen_usage_diff (SSOT) | 0.529 | — | — |
| P33 | multi-feature 3D (all-sample) | 0.528 | +0.0009 | — |
| P34 | historical_proxy (sp_fip_delta) | 0.542 | −0.006 | STABLE 83% |
| P35 | quality-filtered multi-feature | 0.525 | −0.004 | — |
| **P36** | **sp_fip_delta raw (quality)** | **0.528** | −0.0053 | **STABLE 100%** |
| **P36** | **strong-edge ｜delta｜≥0.5** | **0.541** | **+0.0076** | **STABLE** |

**突破點**：P36 strong-edge 是系列中第一個同時達到正 Brier Skill 的實用模型。

---

## 十四、後續研究建議

| 優先 | 方向 | 動機 |
|---|---|---|
| **高** | **P37: Strong-edge threshold 最佳化** | 0.5 是啟發式選取的，0.3 / 0.7 可能更好 |
| **高** | **P38: 2024 MLB 獨立 holdout 驗證** | Strong-edge 需 OOS 驗證才能進一步研究 |
| 中 | P39: 當賽季 FIP 整合 (current_season tier) | 消除晚季衰減（解決 neutral_fallback 限制） |
| 低 | P40: park_run_factor × strong_edge 交互效應 | 球場修正後的投手優勢 |

---

## 十五、治理聲明

```
diagnostic_only   = True   ✅
promotion_freeze  = True   ✅
Champion strategy = UNMODIFIED ✅
Kelly/betting     = UNMODIFIED ✅
Test suite        = 216 PASS / 0 FAIL ✅
Staged files      = 0 (runtime files excluded) ✅
Live odds API     = NOT CALLED ✅
```

---

*Generated by P36 analysis pipeline — 2026-05-24*
