# P158 Daily Workflow Commit & Push Permission Fix

**日期**: 2026-06-05  
**任務**: P158 — Fix Daily Workflow Commit Push Permission  
**狀態**: COMMITTED (local, not pushed)

---

## 根本原因

Workflow run ID `26994316105`（`Daily WBC Data Sync`，排程觸發，headSha `dda5739442215eeb3c0cea96102083575478ebeb`）的 **Commit and Push changes** 步驟（step 7）以 `failure` 結束。

失敗訊息摘要：
```
remote: Permission to kelvinhuang0327/Betting-pool.git denied to github-actions[bot].
fatal: unable to access '...': The requested URL returned error: 403
```

根本原因：GitHub Actions 預設 `GITHUB_TOKEN` 的 `contents` 權限為 `read`，workflow 沒有宣告 `permissions: contents: write`，因此 `git push` 被拒絕（HTTP 403）。

---

## 修復內容

**修改檔案**: `.github/workflows/daily_update.yml`

**新增最上層 `permissions` 區塊**（位於 `jobs:` 之前）：

```yaml
permissions:
  contents: write
```

**最小 diff** — 僅插入兩行，其餘 workflow 內容（名稱、排程、paper step、WBC update step、Commit and Push step）完全保留不變。

---

## Workflow Run 詳情

| 欄位 | 值 |
|------|-----|
| Run ID | 26994316105 |
| Workflow Name | Daily WBC Data Sync |
| Event | schedule |
| headSha | dda5739442215eeb3c0cea96102083575478ebeb |
| 結論 | failure |
| 失敗步驟 | Commit and Push changes (step 7) |
| 成功步驟 | Run MLB Daily Scheduler (Paper Mode) (step 5), Run Data Update (step 6) |

---

## 安全不變量

- ✅ 僅修改 `.github/workflows/daily_update.yml`（Allowed File Whitelist 內）
- ✅ 未新增 `workflow_dispatch`（原本已有，未移除亦未更動）
- ✅ 未修改 cron 排程
- ✅ 未修改 paper flags（`--run-paper-recommendation true`、`--run-paper-evaluation true`）
- ✅ 未修改 WBC update 指令
- ✅ 未修改 Commit and Push 步驟邏輯
- ✅ 未 push
- ✅ 未觸發 workflow_dispatch 或 rerun
- ✅ 未執行 DB 寫入
- ✅ 未呼叫 live API
- ✅ 未解鎖 provider / production / EV / CLV / Kelly
- ✅ 未修改 registry / service.py / controlled_apply
- ✅ Tolerated daemon/runtime dirty files 未觸碰

---

## 驗證結果

```
YAML_OK
permissions: contents: write 出現於第 10–11 行
P158_WORKFLOW_TEXT_OK
```

---

## 建議下一步

1. 建立 PR（`release/p158-daily-workflow-commit-push-permission-fix` → `main`）
2. 合併 PR 後，等待下一次排程觸發（UTC 00:00 / 台灣時間 08:00）
3. 驗證 Commit and Push changes 步驟結論為 `success`
4. 確認 paper outputs 成功 commit 回 repo
