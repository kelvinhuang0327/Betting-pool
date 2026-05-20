# Agent Orchestrator Backlog

## North Star

在不破壞 WBC/MLB/Spring 三模式穩定性的前提下，建立可持續運作的雙代理排程閉環，讓 Planner 與 Worker 以可追蹤、可驗證的方式持續交付高優先任務。

## Success Criteria

1. 每個任務都能產出 `prompt.md`、`task_contract.json`、`completed.md`、`task_result.json`。
2. Gate 會機械判斷交付品質，無效交付自動轉為 `REPLAN_REQUIRED`。
3. 禁止修改保護路徑，且所有成功宣告都附帶可追溯證據。
4. 排程可自動運行，也可手動觸發 Planner/Worker。

## Priorities

### Priority 1: Stability And Safety

- 優先處理會影響主流程穩定性的任務。
- 優先重試 `REPLAN_REQUIRED` 任務並附新策略。

### Priority 2: High-Impact Delivery

- 先推進對分析品質、可觀測性、風控最有影響的項目。

### Priority 3: Documentation And Knowledge

- 補齊 docs/wiki/memory 的關鍵缺口，降低後續任務不確定性。

### Priority 4: Tooling And Maintenance

- 進行非阻塞維護（清理、格式、內部工具）但不得影響高優先任務。

## Planner Rules

1. 產生新任務前必須讀取最新 `task_result.json`。
2. 最新任務為 `RUNNING` 時，Planner 必須跳過。
3. 最新任務為 `REPLAN_REQUIRED` 時，必須優先重規劃。
4. 每個 prompt 都必須包含 Objective / Scope / Constraints / Acceptance Criteria / Handoff Notes。
5. 不可重複提交相同失敗方案，必須明確調整範圍或驗證策略。

## Constraints

- 不可修改 `project_profile.json` 中的 `protected_paths`。
- 不可在沒有證據時宣告任務成功。
- 受權限或執行環境阻塞時必須 finalize，不可長時間停留 `RUNNING`。
- 不可建立驗收標準模糊的任務。

## References

- `README.md`
- `CLAUDE.md`
- `docs/`
- `wiki/`
- `memory/`
- `runtime/agent_orchestrator/project_profile.json`

## Auto Status Block

The orchestrator may maintain an auto-generated section below this line.
