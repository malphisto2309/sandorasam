import logging
import requests
from bs4 import BeautifulSoup
from telegram import Bot, InputMediaPhoto, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from linkvertise_bypasser import Bypasser

# Credentials (HARD-CODED)
BOT_TOKEN = "8067339211:AAE-yvNtTRv7-O09YoIMi3qbYD23aw7v_vY"
CHANNEL_USERNAME = "@fansdeposit"
GPLINKS_API = "eb820552d0f95f920542577393c3d88d6dbf6386"
PASTELINK_API_KEY = "bwecc2dqac9k9jk3vejjeqpfjnkwybpx7pwshccoqf5huuct9ud3w3awfqdbh7ryb763yjuqkbb"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def bypass_and_extract(url: str) -> str:
    try:
        bypassed = Bypasser().bypass(url)
        print("Bypassed link:", bypassed)
        return bypassed
    except Exception as e:
        logger.error(f"Bypass failed: {e}")
        return None

def extract_mega_link(paste_url: str) -> str:
    try:
        res = requests.get(paste_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()
        lines = text.strip().split("\n")
        mega_links = [line.strip() for line in lines if "mega.nz" in line]
        cleaned = []
        for line in lines:
            if "t.me" in line:
                line = line.replace("t.me", "https://t.me/fansdeposit")
            if "mega.nz" in line or "t.me" in line:
                cleaned.append(line)
        return "\n".join(cleaned)
    except Exception as e:
        logger.error(f"Error extracting from pastelink: {e}")
        return None

def create_pastelink(content: str) -> str:
    try:
        response = requests.post("https://api.pastelink.net/v1/paste", data={
            "api_key": PASTELINK_API_KEY,
            "title": "Download Link",
            "content": content,
            "visibility": 1
        })
        data = response.json()
        return "https://pastelink.net/" + data["id"]
    except Exception as e:
        logger.error(f"Pastelink error: {e}")
        return None

def shorten_with_gplinks(url: str) -> str:
    try:
        api = f"https://api.gplinks.com/api?api={GPLINKS_API}&url={url}"
        res = requests.get(api).json()
        return res["shortenedUrl"] if "shortenedUrl" in res else None
    except Exception as e:
        logger.error(f"GPLinks error: {e}")
        return None

def handle_message(update: Update, context: CallbackContext):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    photo = update.message.photo[-1].file_id if update.message.photo else None

    if "linkvertise" not in text and "pastelink.net" not in text:
        return

    try:
        link = None
        for word in text.split():
            if "linkvertise" in word or "pastelink.net" in word:
                link = word
                break

        if not link:
            return

        bypassed = bypass_and_extract(link)
        if not bypassed:
            return

        mega_content = extract_mega_link(bypassed)
        if not mega_content:
            return

        new_paste = create_pastelink(mega_content)
        if not new_paste:
            return

        gplink = shorten_with_gplinks(new_paste)
        if not gplink:
            return

        if photo:
            context.bot.send_photo(chat_id=CHANNEL_USERNAME, photo=photo, caption=gplink)
        else:
            context.bot.send_message(chat_id=CHANNEL_USERNAME, text=gplink)

    except Exception as e:
        logger.error(f"Processing failed: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    logger.info("Bot started")
    updater.idle()

if __name__ == "__main__":
    main()
    
