import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing")

GOLD_API = "https://api.metals.live/v1/spot/gold"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖🔥 بوت رعد جاهز! اكتب /gold لمعرفة سعر الذهب الآن")

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(GOLD_API, timeout=10)
        data = response.json()

        price = data[0][1]
await update.message.reply_text(f"📊 سعر الذهب الآن: {price}$")

    except Exception:
        await update.message.reply_text("⚠️ حدث خطأ أثناء جلب سعر الذهب")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))

    print("Bot started successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
