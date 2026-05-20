# macOS Auto-Start (launchd / LaunchAgent / LaunchDaemon)

本專案已提供一套符合 dual-agent orchestrator 的 launchd 自啟機制，涵蓋：

- 主系統自啟（backend + frontend）
- planner / worker 每 10 分鐘 tick
- worker daemon 常駐
- health check / smoke check
- 異常退出自動重啟（KeepAlive）

支援兩種 scope：

- `user` scope
  - 安裝到 `~/Library/LaunchAgents`
  - 登入後自啟
- `system` scope
  - 安裝到 `/Library/LaunchDaemons`
  - 未登入也會自啟
  - 需要 `sudo`
  - 服務會以專案擁有者帳號執行，避免 root 直接持有工作檔案

## 檔案結構

- 主啟停：
  - `start_all.sh`
  - `stop_all.sh`
- 啟動檢查：
  - `scripts/launchd/health_check.sh`
  - `scripts/launchd/smoke_check.sh`
- Tick / Daemon 包裝器：
  - `scripts/launchd/run_planner_tick.sh`
  - `scripts/launchd/run_worker_tick.sh`
  - `scripts/launchd/run_worker_daemon.sh`
- LaunchAgent 管理：
  - `scripts/launchd/manage_launch_agents.sh`
- LaunchAgent 模板：
  - `scripts/launchd/plists/com.bettingpool.main.plist.tmpl`
  - `scripts/launchd/plists/com.bettingpool.orchestrator.planner.plist.tmpl`
  - `scripts/launchd/plists/com.bettingpool.orchestrator.worker.plist.tmpl`
  - `scripts/launchd/plists/com.bettingpool.orchestrator.worker-daemon.plist.tmpl`
- 前端頁面：
  - `runtime/agent_orchestrator/frontend/index.html`

## Label 與用途

- `com.bettingpool.main`
  - 開機登入後自啟主系統
  - 呼叫 `start_all.sh --foreground`
  - `RunAtLoad=true`, `KeepAlive=true`
- `com.bettingpool.orchestrator.planner`
  - planner tick，每 10 分鐘 (`StartInterval=600`)
- `com.bettingpool.orchestrator.worker`
  - worker tick，每 10 分鐘 (`StartInterval=600`)
- `com.bettingpool.orchestrator.worker-daemon`
  - worker daemon 常駐
  - `RunAtLoad=true`, `KeepAlive=true`

## 安裝 / 重載 / 卸載

```bash
# 使用者登入後自啟（LaunchAgent）
bash scripts/launchd/manage_launch_agents.sh install

# 未登入也要自啟（LaunchDaemon）
sudo bash scripts/launchd/manage_launch_agents.sh install --scope system

# 重載（重新 render，然後 bootout/bootstrap）
bash scripts/launchd/manage_launch_agents.sh reload

# system scope 重載
sudo bash scripts/launchd/manage_launch_agents.sh reload --scope system

# 只卸載（保留 plist 檔）
bash scripts/launchd/manage_launch_agents.sh unload

# system scope 卸載
sudo bash scripts/launchd/manage_launch_agents.sh unload --scope system

# 卸載並移除 ~/Library/LaunchAgents plist
bash scripts/launchd/manage_launch_agents.sh remove

# 卸載並移除 /Library/LaunchDaemons plist
sudo bash scripts/launchd/manage_launch_agents.sh remove --scope system
```

## 手動啟停主服務

```bash
# 背景啟動（手動）
bash ./start_all.sh

# 停止 backend/frontend 並清理 pid
bash ./stop_all.sh
```

## 驗證登入自啟

1. 依需求執行 `install`：
  - 登入後自啟：`bash scripts/launchd/manage_launch_agents.sh install`
  - 未登入也自啟：`sudo bash scripts/launchd/manage_launch_agents.sh install --scope system`
2. 視 scope 驗證：
  - `user`: 登出再登入（或重開機）
  - `system`: 直接重開機即可，不需要先登入
3. 執行：
  - `bash scripts/launchd/manage_launch_agents.sh status`
  - `sudo bash scripts/launchd/manage_launch_agents.sh status --scope system`
   - `curl -fsS http://127.0.0.1:8787/api/summary`
   - `curl -fsS http://127.0.0.1:8788/`

## 觀察與除錯

- Launchd logs:
  - `runtime/agent_orchestrator/logs/launchd/`
- 主服務 logs:
  - `runtime/agent_orchestrator/logs/service/`

可直接 tail：

```bash
bash scripts/launchd/manage_launch_agents.sh logs
```

## 設計細節

- `start_all.sh` 在啟動 backend/frontend 前會檢查 port 衝突。
- 啟動後必做 `health_check.sh` + `smoke_check.sh`。
- smoke 失敗會呼叫 `stop_all.sh` 清理，並以非 0 exit code 退出。
- `--foreground` 模式會持續監控子程序存活，讓 launchd 可進行 KeepAlive 重啟。
- plist 由模板渲染，避免硬編使用者名稱；安裝時以當前 `PROJECT_ROOT` 產生實際路徑。
- `system` scope 會在 plist 內寫入 `UserName=<專案擁有者>`，讓 LaunchDaemon 在開機後可於未登入狀態啟動，但仍以專案帳號執行。
