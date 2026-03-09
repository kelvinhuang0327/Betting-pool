import logging
import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ── Configuration ────────────────────────────────────────────────────────
# 建議將 TOKEN 放在環境變數中，不要直接寫在程式碼裡
# 執行方式: TELEGRAM_BOT_TOKEN="your_token" python bot.py
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID") # Pairing 機制：僅開放給你本人

# 設定日誌
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ── Handlers ─────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /start 指令。"""
    user_id = str(update.effective_user.id)
    
    # 簡單的身份驗證 (借鏡 OpenClaw Pairing)
    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text(f"🚫 存取拒絕。你的 User ID 是 {user_id}\n請在伺服器端將此 ID 加入 ALLOWED_USER_ID 環境變數中以進行配對。")
        return

    welcome_text = (
        "🦞 **WBC Betting Pool Gateway** 已啟動\n\n"
        "你可以使用以下指令：\n"
        "🎯 /predict - 查詢今日關鍵對戰預測\n"
        "💰 /ev - 查詢市場上高預期價值的盤口\n"
        "📊 /portfolio - 查詢當前資金與回撤狀態\n"
        "🔔 /alerts - 開啟/關閉即時賠率異動提醒"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """模擬查詢預測結果。"""
    # 這裡未來會串接你的 wbc_backend/api/app.py 或直接讀取報告檔案
    try:
        with open("../last_report.txt", "r") as f:
            report = f.read()[:2000] # Telegram 訊息上限約 4096 字
            await update.message.reply_text(f"📈 **最新預測報告摘要**：\n\n{report}", parse_mode='Markdown')
    except FileNotFoundError:
        await update.message.reply_text("目前還沒有產出報告。請先執行模型分析。")

async def ev_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查詢 EV+ 的投注建議。"""
    # 這裡未來會串接 strategy/value_detector.py
    await update.message.reply_text("🔍 正在掃描 TSL 盤口與模型勝率差異...\n\n✅ 建議：[台灣 vs 澳洲] 不讓分 (主勝) - EV: +7.2%")

# ── Main ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if not TOKEN:
        print("❌ 錯誤: 請設定 TELEGRAM_BOT_TOKEN 環境變數")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # 註冊指令
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("predict", predict))
        app.add_handler(CommandHandler("ev", ev_check))
        
        print("🚀 Telegram Bot 正在運行中...")
        app.run_polling()
