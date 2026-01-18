import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# قراءة التوكن من الملف السري في Render
with open("/etc/secrets/bot_token.txt", "r") as f:
    TOKEN = f.read().strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖🔥 البوت شغّال بنجاح!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot started successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
