import os
import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from bs4 import BeautifulSoup
from linkvertise_bypasser import Bypasser

# Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
PASTELINK_API_KEY = os.getenv("PASTELINK_API_KEY")
GPLINKS_API = os.getenv("GPLINKS_API")

bot = Bot(token=BOT_TOKEN)
bypasser = Bypasser()

def bypass_link(url):
    try:
        return bypasser.bypass(url)
    except:
        return None

def extract_and_clean_paste(paste_url):
    try:
        r = requests.get(paste_url)
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", {"id": "content"}).get_text(separator="\n")
        lines = content.splitlines()
        cleaned = []
        for line in lines:
            if "mega.nz" in line:
                cleaned.append(line.strip())
            elif "t.me/" in line:
                cleaned.append("https://t.me/fansdeposit")
        return "\n".join(cleaned)
    except Exception as e:
        print("Paste extract error:", e)
        return None

def create_pastelink(text):
    payload = {
        "api": PASTELINK_API_KEY,
        "title": "Content Drop",
        "description": "Auto-posted",
        "content": text,
        "visibility": 1
    }
    try:
        r = requests.post("https://pastelink.net/api/create", data=payload)
        return r.json().get("url")
    except Exception as e:
        print("Paste create error:", e)
        return None

def shorten_with_gplinks(link):
    api_url = f"https://api.gplinks.com/api?api={GPLINKS_API}&url={link}"
    try:
        r = requests.get(api_url)
        result = r.json()
        return result["shortenedUrl"] if result["status"] == "success" else None
    except Exception as e:
        print("GPLinks error:", e)
        return None

def process_message(update: Update, context):
    if not update.message or not update.message.caption:
        return

    caption = update.message.caption
    download_link = None

    for line in caption.splitlines():
        if "http" in line:
            download_link = line.strip()
            break

    if not download_link:
        return

    bypassed = bypass_link(download_link)
    if not bypassed:
        return

    cleaned_text = extract_and_clean_paste(bypassed)
    if not cleaned_text:
        return

    new_paste_url = create_pastelink(cleaned_text)
    if not new_paste_url:
        return

    final_short_url = shorten_with_gplinks(new_paste_url)
    if not final_short_url:
        return

    photo_file_id = update.message.photo[-1].file_id if update.message.photo else None
    if photo_file_id:
        bot.send_photo(
            chat_id=CHANNEL_USERNAME,
            photo=photo_file_id,
            caption=final_short_url
        )

def start(update, context):
    update.message.reply_text("Bot is running.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.chat(username="@OnlyFansFile") & Filters.photo, process_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
      
