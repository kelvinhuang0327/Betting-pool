# P25 市場對映稽核報告

**Phase**: P25 — Market Mapping Audit  
**Date**: 2026-05-20  
**Constraints**: `paper_only=true` / `diagnostic_only=true`

---

## 稽核摘要

| 市場 | 狀態 | Pairs | CLV Obs | Name Mismatch | |CLV|>50% 數 | 結論 |
|---|---|---|---|---|---|---|
| MNL | ⚠️ RISK | 236 | 472 | 3 (1.3%) | 3 | 混合 2/3 路市場，index-1 語意不一致 |
| HDC | 🔴 CRITICAL | 229 | 458 | **28 (12.2%)** | **17** | Handicap line shift → 跨 line 比較 |
| OU | ⚠️ RISK | 230 | 460 | 21 (9.1%) | 0 | Total line shift，同 HDC 問題 |
| OE | ✅ PASS | 230 | 460 | 0 | 0 | 無構造風險，但市場無資訊含量 |
| TTO | ⚠️ HIGH | 217 | 434 | **32 (14.7%)** | 0 | Line shift 比例最高，max |CLV|=40.4% |

---

## HDC（讓分）— CRITICAL

### 問題

HDC outcome name 格式：`{TeamName} {+/-spread}`（例如 `底特律老虎 -2.5`）

當 pregame 到 closing 之間莊家移線（line shift），例如從 `-1.5` 變為 `-2.5`：

```
pregame record:  outcomes[0] = {"outcomeName": "底特律老虎 -1.5", "odds": 2.90}
closing record:  outcomes[0] = {"outcomeName": "底特律老虎 -2.5", "odds": 1.40}
```

CLV 公式：`(2.90 - 1.40) / 1.40 * 100 = 107.14%`

這 **不是** 真實的市場移動，而是在比較**不同盤口**的賠率差異。`-1.5` 的 2.90 和 `-2.5` 的 1.40 本來就是不同的盤，是正常的盤口定價關係，不是 CLV 訊號。

### 量化影響

- 28/229 pairs（12.2%）發生 name mismatch
- 其中產生 17 個 |CLV| > 50% 的極端觀測值
- 這 17 個觀測值約等於 34 個 CLV 資料點（每 pair 2 sides）
- 這些人工極端值支撐了 top-1% outlier 的 110.57% 貢獻率

### 修復方案

```python
# 修復前：by index
clv = (pre_outcomes[i]["odds"] - clo_outcomes[i]["odds"]) / clo_outcomes[i]["odds"] * 100

# 修復後：by name matching
pre_by_name = {o["outcomeName"]: float(o["odds"]) for o in pre_outcomes}
clo_by_name = {o["outcomeName"]: float(o["odds"]) for o in clo_outcomes}
for name in pre_by_name:
    if name in clo_by_name:  # only compute CLV if same line
        clv = (pre_by_name[name] - clo_by_name[name]) / clo_by_name[name] * 100
```

---

## MNL（獨贏）— RISK

### 問題

MNL 市場有兩種變體：
- **3-way**（棒球有和局，如 WBC 延長制）：HomeTeam / Draw / AwayTeam
- **2-way**（MLB/NPB 正規賽無和局）：HomeTeam / AwayTeam

資料集中：215 個 3-way + 21 個 2-way

CLV 公式使用 index 0（side A）和 index 1（side B）：
- 3-way 市場：index 1 = **Draw（和局）**
- 2-way 市場：index 1 = **Away team**

**index-1 在不同市場類型代表不同含義**，混合計算會引入語意噪音。

### 嚴重度

相對 HDC 較低：name mismatch 只有 3 對（1.3%），無構造性 bug，但 3-way/2-way 混合是方法論瑕疵。

---

## OU（大小分）— RISK

OU outcome 格式：`大 X.X` / `小 X.X`（X.X = 總分盤口）

21/230 pairs（9.1%）在 pregame/closing 之間總分盤口改變（例如 7.5 → 8.5）。

CLV 計算的是「7.5 盤口的 pregame 賠率」與「8.5 盤口的 closing 賠率」之差 → 無意義。

最大 |CLV| = 22.34%，比 HDC 溫和，但原理相同。

---

## OE（單雙）— PASS（但無資訊含量）

Outcome names 固定為 `單` / `雙`，永不改變。零 name mismatch。

但 OE 市場賠率幾乎不移動（std=0.84%，68.7% 觀測值 CLV ≈ 0），包含在彙總統計中稀釋整體 CLV mean。

---

## TTO（球隊總分）— HIGH RISK

TTO 是各別球隊的 Over/Under，格式同 OU（`大 X.X`）。

32/217 pairs（14.7%）— 五個市場中**最高的 name mismatch 比例**。

最大 |CLV| = 40.4%，雖低於 50% 臨界值，但積累影響顯著。

---

## 綜合修復建議

| 行動 | 優先級 | 預期效果 |
|---|---|---|
| HDC/OU/TTO：改用 name matching 計算 CLV | P1 立即 | 消除 ~20 個 |CLV|>50% 人工極端值 |
| MNL：分離 2-way / 3-way 分析 | P2 | 提升語意一致性 |
| OE：從彙總 CLV 統計中排除 | P3 | 減少非資訊性噪音 |
| 修復後重跑 bootstrap CI | P2 | 重新分類 INCONCLUSIVE vs NEUTRAL |

> **所有建議均為 paper_only，不允許生產部署**

---

*Artifact*: `data/paper_recommendations/p25_market_mapping_audit_20260520.json`
