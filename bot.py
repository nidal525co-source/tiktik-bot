import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحباً بك! أرسل لي رابط مقطع تيك توك وسأقوم بتحميله فوراً 🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    if "tiktok.com" not in url:
        await update.message.reply_text("يرجى إرسال رابط تيك توك صحيح.")
        return

    status_message = await update.message.reply_text("جاري تحميل المقطع، انتظر قليلاً... ⏳")
    
    try:
        api_url = f"https://tikwm.com{url}"
        response = requests.get(api_url).json()
        video_url = response["data"]["play"]
        await update.message.reply_video(video=video_url, caption="تم التحميل بنجاح عبر بوتك الخاص! 🚀")
        await status_message.delete()
    except Exception as e:
        logging.error(f"Error: {e}")
        await status_message.edit_text("حدث خطأ أثناء معالجة الرابط أو أن المقطع خاص.")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    application.run_polling()

if _name_ == '_main_':
    main()
