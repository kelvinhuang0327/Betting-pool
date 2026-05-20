# P19-C: Closing-Line Availability Recheck

**Task**: P19-C  
**Date**: 2026-05-20  
**paper_only**: true | **network_call**: false | **crawler_modified**: false

---

## Pair 定義

| 角色 | 時間窗口條件 |
|------|-------------|
| **Pregame** | `fetched_at >= 2.0 小時 before game_time` |
| **Closing** | `fetched_at within ±2.0 小時 of game_time` |
| **有效 pair** | 同一 `match_id` 同時有 pregame + closing，且兩者均有 odds 欄位 |

## Recheck 結果

| 指標 | 值 |
|------|----|
| `valid_pair_count` | **233** |
| `invalid_pair_count` | 620 |
| `missing_closing_count` | 563 |
| `missing_pregame_count` | 57 |
| `timestamp_parse_error_count` | **0** |
| `odds_field_validation` | PASS（233 pairs 均有 odds） |
| `source_trace_field` | TSL_BLOB3RD |

## Sample Valid Pairs

| mid | Pregame fetched_at | Closing fetched_at | game_time |
|-----|--------------------|--------------------|-----------|
| 3468398.1 | 2026-05-13T16:14:37Z | 2026-05-14T03:41:06Z | 2026-05-14T12:00+08 |
| 3461584.1 | 2026-04-17T04:22:00Z | 2026-04-17T23:09:49Z | 2026-04-18T07:10+08 |
| 3467361.1 | 2026-05-09T02:27:25Z | 2026-05-09T23:07:06Z | 2026-05-10T07:15+08 |
| 3462246.1 | 2026-04-18T18:19:19Z | 2026-04-19T16:09:19Z | 2026-04-20T01:35+08 |
| 3464719.1 | 2026-04-28T17:16:38Z | 2026-04-29T04:48:19Z | 2026-04-29T13:00+08 |

## 結論

```
closing_line_available   = true
recheck_result           = CLOSING_LINE_CONFIRMED_233_PAIRS
timestamp_parse_errors   = 0
```

Closing line **確認可用**。233 pairs 均有清晰的 pregame + closing timestamps 與 odds。

---
*paper_only=true。無網路呼叫。無 crawler 修改。不宣稱任何策略獲利能力。*
