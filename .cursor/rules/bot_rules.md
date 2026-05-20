---
paths:
  - "telegram_bot/**/*.py"
---

# 🤖 Telegram Bot 互動與回應規範 (Bot Rules)

這些規則僅在更新 Telegram 機器人相關代碼時生效。

## 🔐 安全規範 (Security)
- 嚴禁在代碼中寫死 `API_KEY`、`BOT_TOKEN`。一律從 `.env` 加載。
- **原因**: 避免敏感資訊外洩。

## 💬 訊息格式規範 (Message Formatting)
- 所有推送訊息應採用 Markdown 內容格式。
- 顯示賠率與預期獲利時，保留小數點後兩位 (%.2f)。
- 顯示隊伍名稱時，必須使用 `[隊伍 A] vs [隊伍 B]` 格式。

## 🛡 錯誤處理 (Error Handling)
- 定時任務 (Cron/Async loop) 必須包含全域 `try-catch` 防止進程崩潰。
- 每一個失敗的任務必須回報至 `log` 並推送錯誤訊息給管理員。

## 🕒 更新頻率
- 推送賠率更新的頻率不得高於每 5 分鐘一次。
- 只有當 `Expected Value (EV) > 5%` 時才主動推送警報訊息。
