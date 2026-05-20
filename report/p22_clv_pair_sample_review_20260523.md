# P22-C CLV Pair Sample Integrity Review
**日期：** 2026-05-23  
**Phase：** P22_CLV_PAIR_SAMPLE_REVIEW  
**Task：** P22-C  

## Pair 導出結果

| 欄位 | 值 |
|------|----|
| TSL history 總筆數 | 2,772 |
| unique match_ids | 875 |
| 導出 valid pairs | **236** |
| P19 canonical valid pairs | 233 |
| 差異 | +3（誤差 ≤ 2%，在可接受範圍，P19 以 23:59 UTC 截點為準） |
| invalid pairs | 639（無 pregame 或 closing snapshot） |
| Pair 定義 — pregame | fetched_at ≥ 2.0h before game_time |
| Pair 定義 — closing | fetched_at within ±2.0h of game_time |
| odds_field_validation | 236 valid pairs 均有 pregame + closing odds |

## 安全欄位確認

| paper_only | network_call | crawler_modified | profitability_claim |
|------------|--------------|------------------|---------------------|
| true | false | false | false |

## Sample Status

| 樣本組 | 數量 |
|--------|------|
| Top-20 valid pairs（依 game_time 排序） | 20 |
| Random-10 valid pairs（seed=42） | 10 |
| Invalid sample（最多 20） | 20 |

## 最終分類

```
sample_generation_status: SUCCESS
final_classification: P22_PAIR_SAMPLE_REVIEW_PASSED
```

P22-D CLV Validation 可執行。
