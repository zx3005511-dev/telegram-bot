import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing")

GOLD_API = "https://api.metals.live/v1/spot/gold"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖🔥 البوت جاهز!\n"
        "لمعرفة سعر الذهب الآن اكتب:\n"
        "/gold"
    )


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(GOLD_API, timeout=10)
        data = response.json()

        # يدعم أكثر من شكل للـ API
        price = data.get("gold") or data.get("price") or data[0][1]

        await update.message.reply_text(f"📊 سعر الذهب الآن: {price}$")

    except Exception as e:
        await update.message.reply_text("⚠️ حدث خطأ أثناء جلب سعر الذهب")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))

    print("Bot started successfully...")
    app.run_polling()


if __name__ == "__main__":
    main()
