# P22-D CLV Validation Result
**日期：** 2026-05-23  
**Phase：** P22_CLV_VALIDATION_ONLY  
**Task：** P22-D  

## 驗證範圍

| 欄位 | 值 |
|------|----|
| 使用 valid pairs | 236 |
| 總 outcome 觀測數 | 2,499 |
| 覆蓋市場 | MNL, OU, OE, HDC, TTO |
| parse_errors | 0 |
| 資料源 | TSL odds history（data/tsl_odds_history.jsonl, 2,772 筆） |

## CLV 計算方法

```
CLV_abs = pregame_odds - closing_odds
CLV_pct = (pregame_odds - closing_odds) / closing_odds × 100

正向 CLV（POSITIVE）：pregame_odds > closing_odds（賽前觀測到較優賠率）
負向 CLV（NEGATIVE）：pregame_odds < closing_odds
中性 CLV（NEUTRAL）  ：|diff| ≤ 0.001
```

> **免責聲明：** CLV 統計為純學術描述性數值，不代表任何實際獲利能力或投資建議。

## 整體 CLV 摘要

| 指標 | 值 |
|------|----|
| n（觀測數） | 2,499 |
| mean CLV% | **+0.2332%** |
| median CLV% | 0.0% |
| std CLV% | 8.7212% |
| min CLV% | — |
| max CLV% | — |
| Positive CLV 數 | 816（**32.65%**） |
| Negative CLV 數 | 820（32.81%） |
| Neutral CLV 數 | 863（34.53%） |

## 分市場 CLV 摘要

| 市場 | n | mean CLV% | median CLV% | Positive Rate |
|------|---|-----------|-------------|---------------|
| **MNL**（不讓分） | 687 | **-0.2490%** | — | 35.37% |
| **OU**（大小分） | 460 | **+0.1158%** | — | 38.26% |
| **OE**（單雙） | 460 | **+0.0083%** | — | 15.65% |
| **HDC**（讓分） | 458 | **+1.2103%** | — | 39.74% |
| **TTO**（特定） | 434 | **+0.3281%** | — | 32.95% |

## 觀察重點

1. **整體 mean CLV = +0.23%**：整體偏正向，但 std = 8.72% 遠大於 mean，統計不顯著。
2. **MNL 市場 mean = -0.25%**：不讓分市場賠率略向盤口移動，pregame 觀測時效率較高。
3. **HDC mean = +1.21%**：讓分市場 pregame 到 closing 有最大漂移，可能反映流動性較低。
4. **OE positive rate = 15.65%**：單雙市場幾乎無線路移動，合理（固定賠率型市場）。
5. **Positive ≈ Negative ≈ Neutral**：整體分布接近對稱，符合有效市場假設。

## 安全欄位確認

| paper_only | network_call | crawler_modified | profitability_claim | promotion_allowed |
|------------|--------------|------------------|---------------------|-------------------|
| true | false | false | false | false |

## 最終分類

```
final_classification: P22_CLV_VALIDATION_ONLY_COMPLETED
```

**不宣稱可獲利。不做 optimizer promotion。不做 champion replacement。**
