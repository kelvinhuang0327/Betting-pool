# Worker Provider 設定報告 — GitHub Copilot Daemon + gpt-5-mini

**產出日期**: 2026-05-04  
**任務**: 將 Worker 預設設定為 `copilot-daemon`，模型指定為 `gpt-5-mini`  
**狀態**: ✅ 設定已寫入 SQLite DB 並驗證通過

---

## 1. 設定來源

| 項目 | 儲存位置 |
|------|---------|
| 設定方式 | SQLite `settings` 表（key-value）|
| DB 路徑 | `runtime/agent_orchestrator/orchestrator.db` |
| 讀取函數 | `db.get_worker_provider()` / `db.get_worker_copilot_model()` |
| 寫入函數 | `db.set_worker_provider(v)` / `db.set_worker_copilot_model(v)` |
| 預設值位置 | `orchestrator/db.py` — `DEFAULT_SETTINGS` dict |

> ⚠️ **注意**: 設定 **不在** `.env`、`scheduler_state.json` 或 `launchd.env` 中 — 完全由 SQLite DB 管控。

---

## 2. 修改內容

### 2a. `orchestrator/db.py` — DEFAULT_SETTINGS

```diff
-    "worker_provider": "codex",
-    "worker_copilot_model": "",
+    "worker_provider": "copilot-daemon",
+    "worker_copilot_model": "gpt-5-mini",
```

### 2b. 即時 DB 更新（Python setter）

```python
db.set_worker_copilot_model("gpt-5-mini")
# worker_provider 已為 "copilot-daemon"（前次手動設定），無需再次寫入
```

---

## 3. 驗證結果

```
worker_provider:      copilot-daemon   ✅
worker_copilot_model: gpt-5-mini       ✅
planner_provider:     codex            （DB 值，受 role guard 封鎖，實際不執行外部 LLM）
cto_planner_provider: claude           （DB 值，受 role guard 封鎖，實際不執行外部 LLM）
ext_llm_role_planner: 0               ✅ Planner 外部 LLM 呼叫封鎖
ext_llm_role_worker:  1               ✅ Worker 允許外部 LLM（受 execution_policy 管控）
ext_llm_role_cto:     0               ✅ CTO 外部 LLM 呼叫封鎖
```

---

## 4. Planner / CTO 隔離確認

**雙重防護機制**：

1. **Role Guard**（`orchestrator/provider_factory.py`）：
   - `ROLE_BLOCKED_PROVIDERS["planner"] = EXTERNAL_PROVIDERS`
   - `ROLE_BLOCKED_PROVIDERS["cto"] = EXTERNAL_PROVIDERS`
   - `copilot-daemon` 屬於 `EXTERNAL_PROVIDERS` → Planner / CTO 完全無法使用

2. **DB 開關**（`ext_llm_role_planner: "0"`, `ext_llm_role_cto: "0"`）：
   - `execution_policy.evaluate_execution()` 會在執行前確認
   - 即使 role guard 被繞過，DB 開關仍封鎖

**結論**: Planner 與 CTO 即便 DB 的 `planner_provider` / `cto_planner_provider` 指向外部 provider，也**不會**觸發任何外部 LLM 呼叫。

---

## 5. LLM 執行驗證

- `llm_usage.jsonl` 最後記錄時間: `2026-05-01T13:05:33Z`（本次操作前）
- 總筆數: 30 筆（本次操作後未新增任何記錄）
- 結論: **本次設定操作未觸發任何 LLM 呼叫** ✅

---

## 6. UI / API 狀態

- `GET /api/providers` 回傳 `_build_provider_config_payload()` → 讀取 DB，無需手動重啟
- `WORKER_PROVIDER_LABELS["copilot-daemon"]` = `"GitHub Copilot Daemon"` ✅（已在 `common.py`）
- `COPILOT_MODEL_PRESETS` 包含 `{"value": "gpt-5-mini", "label": "gpt-5-mini"}` ✅
- `validate_copilot_model("gpt-5-mini")` = `True` ✅

---

## 7. ⚠️ 相容性警告 — `gh copilot suggest` 指令格式

**問題**: `copilot_daemon.py` 目前使用舊版指令格式：

```python
# 目前程式碼（copilot_daemon.py line 198）：
cmd = [gh_bin, "copilot", "suggest", "--target", "shell"]
if copilot_model:
    cmd += ["--model", copilot_model]
```

**現況**:
- `gh` 版本: 2.87.3（2026-02-23）
- `copilot` binary 版本: 1.0.40（新版 Agent-based CLI）
- 新版 `copilot` CLI **已移除** `suggest --target shell` 子命令
- 新版使用格式: `copilot -p "..." --allow-all-tools --model gpt-5-mini`

**影響**:
- `copilot-daemon` Worker 在呼叫 `gh copilot suggest --target shell` 時會因子命令不存在而失敗
- **設定已正確寫入**，但實際執行時 Daemon 執行層需更新指令格式才能正常工作

**建議修正（不在本次任務範疇）**:

```python
# 建議更新為新版格式（需另行評估）：
cmd = [gh_bin, "copilot", "--", "-p", prompt_content, "--allow-all-tools"]
if copilot_model:
    cmd = [gh_bin, "copilot", "--", "--model", copilot_model, "-p", prompt_content, "--allow-all-tools"]
```

> 此問題屬於 `copilot_daemon.py` 執行邏輯層，與本次「設定 provider/model」任務無關，但需在啟用 Daemon 前修復。

---

## 8. 摘要

| 項目 | 結果 |
|------|------|
| Worker Provider | `copilot-daemon` ✅ |
| Worker Model | `gpt-5-mini` ✅ |
| DEFAULT_SETTINGS 更新 | `orchestrator/db.py` ✅ |
| 即時 DB 寫入 | 成功 ✅ |
| Planner 隔離 | 維持 role guard（ext_llm_role_planner=0）✅ |
| CTO 隔離 | 維持 role guard（ext_llm_role_cto=0）✅ |
| LLM 呼叫驗證 | 無新增記錄 ✅ |
| UI 顯示 | 標籤與 preset 已就位 ✅ |
| CLI 相容性警告 | `suggest --target shell` 指令格式已過時 ⚠️ |
