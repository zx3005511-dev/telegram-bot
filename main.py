# bot.py
import os
import sys
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- Helpers ---
def get_token():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("ERROR: BOT_TOKEN not set in environment variables.")
        sys.exit(1)
    # إزالة أي سطور جديدة أو مسافات زائدة
    token = token.strip()
    if not token:
        print("ERROR: BOT_TOKEN is empty after stripping whitespace/newlines.")
        sys.exit(1)
    return token

def verify_token(token: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.InvalidURL:
        print("ERROR: InvalidURL — يبدو أن التوكِن يحتوي على محارف غير صحيحة (تحقق من وجود سطر جديد أو مسافات).")
        return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR: اتصال الشبكة فشل: {e}")
        return False

    try:
        data = r.json()
    except ValueError:
        print("ERROR: لم يتم استقبال JSON صالح من Telegram.")
        return False

    if data.get("ok"):
        me = data.get("result", {})
        print(f"Token valid. Bot username: @{me.get('username')} (id: {me.get('id')})")
        return True
    else:
        print(f"ERROR: التوكن غير صحيح. استجابة Telegram: {data}")
        return False

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! البوت شغّال ✅")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or "<no text>"
    await update.message.reply_text(f"أرسلت: {text}")

# --- Main ---
def main():
    token = get_token()
    if not verify_token(token):
        print("أوقف التنفيذ بسبب مشكلة في التوكن.")
        sys.exit(1)

    try:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

        print("Starting bot (polling)... Press Ctrl+C to stop.")
        app.run_polling()
    except Exception as e:
        print("ERROR: فشل تشغيل البوت:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
