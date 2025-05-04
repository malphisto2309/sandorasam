import asyncio
import re
import requests
from pastelink import Paste
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from linkvertise_bypasser import bypass_url

# Telegram API credentials
api_id = 11752289
api_hash = "1c67aaab57aa95bf84145e199c69f500"
phone_number = "+5521984561253"

# GPLinks API
gplinks_api = "eb820552d0f95f920542577393c3d88d6dbf6386"

# Pastelink API
pastelink_api = "bwecc2dqac9k9jk3vejjeqpfjnkwybpx7pwshccoqf5huuct9ud3w3awfqdbh7ryb763yjuqkbb"

# Telegram channels
source_channel = "OnlyFansFile"
target_channel = "fansdeposit"

client = TelegramClient("session", api_id, api_hash)

def extract_pastelink(text):
    match = re.search(r"(https:\/\/pastelink\.net\/\S+)", text)
    return match.group(1) if match else None

def extract_mega_link(text):
    match = re.search(r"https:\/\/mega\.nz\/[^\s]+", text)
    return match.group(0) if match else None

def replace_tme_links(text):
    return re.sub(r"https?:\/\/t\.me\/\S+", "https://t.me/fansdeposit", text)

def shorten_with_gplinks(destination_url):
    api = f"https://api.gplinks.com/api?api={gplinks_api}&url={destination_url}"
    try:
        res = requests.get(api).json()
        return res.get("shortenedUrl", "Failed to shorten")
    except:
        return "Error with GPLinks"

def create_pastelink(content):
    paste = Paste(api_key=pastelink_api)
    try:
        return paste.create(content=content)
    except Exception as e:
        print("Pastelink error:", e)
        return None

async def process_messages():
    await client.start(phone=phone_number)

    history = await client(GetHistoryRequest(
        peer=source_channel,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    messages = history.messages
    for message in reversed(messages):
        if message.message and "pastelink" in message.message:
            pastelink_url = extract_pastelink(message.message)
            if not pastelink_url:
                continue

            print("Bypassing:", pastelink_url)
            try:
                final_page = bypass_url(pastelink_url)
            except Exception as e:
                print("Bypass failed:", e)
                continue

            mega_link = extract_mega_link(final_page)
            if not mega_link:
                print("No Mega link found")
                continue

            clean_content = replace_tme_links(final_page)
            pastelink_result = create_pastelink(clean_content)
            if not pastelink_result:
                print("Pastelink creation failed")
                continue

            shortened = shorten_with_gplinks(pastelink_result)
            if message.photo:
                await client.send_file(target_channel, file=message.photo, caption=shortened)
            else:
                await client.send_message(target_channel, shortened)

if __name__ == "__main__":
    asyncio.run(process_messages())
    
