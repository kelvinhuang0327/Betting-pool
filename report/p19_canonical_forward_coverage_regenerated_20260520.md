# P19-B: Canonical Forward Coverage Regenerated

**Task**: P19-B  
**Date**: 2026-05-20  
**paper_only**: true | **network_call**: false | **crawler_modified**: false

---

## 目標

重新以 canonical root 的 `data/tsl_odds_history.jsonl` 計算 forward coverage，修正 P17 stale artifact（worktree 無此檔案故計算為 pair_count=0）。

## Stale Artifact 診斷

| 指標 | P17 artifact chain | Canonical root raw audit |
|------|--------------------|--------------------------|
| `tsl_odds_history_exists` | `false` | `true` |
| `pair_count` | `0` | `233` |
| `stale_reason` | worktree 無此檔案 | — |

## 重新計算結果

| 指標 | 值 |
|------|----|
| `total_records` | 2,747 |
| `parse_errors` | 0 |
| `unique_match_ids` | 859 |
| `pregame_candidate_count` | 796 |
| `closing_candidate_count` | 290 |
| **`valid_clv_pairs`** | **233** |
| `pair_target` | 200 |
| **`pair_coverage_pct`** | **116.5%** |
| `delta_vs_p17_artifact_chain` | +233 |
| `unique_game_dates` | 41 |
| `game_date_range` | 2026-03-13 → 2026-05-20 |
| `stale_artifact_corrected` | `true` |

## 結論

```
forward_coverage_status = CANONICAL_FORWARD_COVERAGE_SUFFICIENT
clv_gate_clear_per_data  = true
```

P17 stale artifact **已修正**。Data 層面 CLV gate **通過**。

---
*paper_only=true。無網路呼叫。無 crawler 修改。不宣稱任何策略獲利能力。*
