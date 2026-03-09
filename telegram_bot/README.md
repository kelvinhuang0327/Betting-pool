# 🤖 Telegram Gateway 設定指南

參考 [OpenClaw](https://github.com/openclaw/openclaw) 的作法，建立專屬的自動化通知與指令機器人。

## 1. 取得 Bot Token
1. 在 Telegram 搜尋 `@BotFather`。
2. 輸入 `/newbot` 並依照指示設定名稱（例如：`Kelvin_WBC_Bot`）。
3. 取得 API Token。

## 2. 安裝相依套件
本機器人使用 `python-telegram-bot` 庫：

```bash
python -m pip install python-telegram-bot
```

## 3. 設定與執行
為了安全性，我們不將 Token 寫死在程式碼中。

### 步驟 A：取得你的 User ID
1. 執行 `python bot.py` (不帶 Token 沒關係，或者先隨便填)。
2. 在 Telegram 私訊你的 Bot `/start`。
3. 機器人會回傳你的 User ID（例如：`123456789`）。

### 步驟 B：正式運行 (配對模式)
將你的 ID 加入環境變數，這樣只有你本人可以操作機器人：

```bash
export TELEGRAM_BOT_TOKEN="你的_TOKEN"
export ALLOWED_USER_ID="你的_ID"
python bot.py
```

## 4. 指令說明
- `/predict`: 自動讀取本地 `last_report.txt` 並推送摘要。
- `/ev`: 執行 `value_detector.py` 並回傳當前最優投注選項。
- `/portfolio`: 串接資金管理模組，回傳當前水位。

## 5. 自動化整合
你可以將 `bot.py` 放在伺服器上長期執行 (使用 `screen` 或 `pm2`)，當 `wbc_backend` 執行完畢產出新報告時，可以透過 Telegram API 呼叫機器人主動發送訊息給你。
