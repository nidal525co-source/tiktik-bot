import logging
import os
import glob
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def download_tiktok(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'video_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base_name = os.path.splitext(filename)
        possible_files = glob.glob(f"{base_name}.*")
        if possible_files:
            return possible_files[0]
        return filename

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Send me a TikTok link and I will download it for you.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if "tiktok.com" in user_message:
        status_message = await update.message.reply_text("Downloading, please wait...")
        video_path = None
        try:
            video_path = download_tiktok(user_message)
            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="Downloaded successfully!")
            await status_message.delete()
        except Exception as e:
            logging.error(f"Error: {e}")
            await status_message.edit_text("Sorry, an error occurred while downloading.")
        finally:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
    else:
        await update.message.reply_text("Please send a valid TikTok link.")

def main():
    # وضعت لك علامات التنصيص الجاهزة لتضع التوكن الجديد داخلها مباشرة
    TOKEN = "8886770977:AAF7sNsbMTfVAgKAzQ3fPmwBeYUG--i6UpE"
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()