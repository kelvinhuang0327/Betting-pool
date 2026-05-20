# Dual-Agent Orchestrator

本專案已落地一套可重用的 dual-agent orchestrator（Planner / Worker），核心在 `orchestrator/`，運行入口在 `scripts/agent_orchestrator.py`。

## 主要檔案

- `runtime/agent_orchestrator/project_profile.json`
- `runtime/agent_orchestrator/project_profile.schema.json`
- `runtime/agent_orchestrator/backlog.md`
- `orchestrator/common.py`
- `orchestrator/db.py`
- `orchestrator/planner_tick.py`
- `orchestrator/worker_tick.py`
- `orchestrator/api.py`
- `orchestrator/optional_worker_daemon.py`
- `scripts/agent_orchestrator.py`

## 快速開始

```bash
python3 scripts/agent_orchestrator.py init
python3 scripts/agent_orchestrator.py planner-tick
python3 scripts/agent_orchestrator.py worker-tick --no-provider
python3 scripts/agent_orchestrator.py summary
```

`--no-provider` 可做本地 smoke path，不呼叫外部 agent CLI，會將任務 finalize 為 `REPLAN_REQUIRED`（符合 blocked finalize 規則）。

## Provider 設定

`project_profile.json` 內的 `planner_provider` / `worker_provider` 用於排程角色分工。

Worker provider command 可透過環境變數覆寫：

- `ORCH_PROVIDER_CMD_CODEX`
- `ORCH_PROVIDER_CMD_CLAUDE`
- `ORCH_PROVIDER_CMD_COPILOT`
- `ORCH_PROVIDER_CMD_COPILOT_DAEMON`

若未覆寫，預設會嘗試：

- codex: `codex exec ...`
- claude: `claude -p ...`

## API / UI

```bash
python3 scripts/agent_orchestrator.py api --host 127.0.0.1 --port 8787
```

開啟 [http://127.0.0.1:8787](http://127.0.0.1:8787) 可看到最小 UI 與 API。

## Scheduler Daemon

```bash
python3 scripts/agent_orchestrator.py daemon
```

這會依 `scheduler_state` 的 interval 自動執行 planner/worker tick。可透過 API 切換 enable/disable。
