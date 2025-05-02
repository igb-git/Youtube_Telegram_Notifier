import asyncio
from datetime import datetime, timedelta, timezone
import feedparser
from telegram import Bot
from pathlib import Path


CHANNELS = [
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCciQ8wFcVoIIMi-lfu8-cjQ",  # Anton Petrov
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCZ9jWH_8tJ-Nmaj8dSQdEYA",  # Stefan Milo
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC1yNl2E66ZzKApQdRuTQ4tw",  # Sabine Hossenfelder
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCMLtBahI5DMrt0NPvDSoIRQ" #Machine Learning Street Talk
]
BOT_TOKEN = "7831388539:AAEewWAe1_kla7DuSDOtEL-GFzKBFcKPkU0"
CHAT_ID = -1002619953898
videos = []
script_dir = Path(__file__).parent
file_path = script_dir / "last_date.txt"

try:
    with open(file_path, 'r') as file:
              last_date = file.read()
    last_date = last_date.strip()
    last_date = datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S%z')
except FileNotFoundError:
    last_date = datetime.now().date() - datetime.timedelta(days=1)

async def get_links(rss_url):
    d = feedparser.parse(rss_url)
    for entry in d.entries:
        try:
            published = entry.published
            published_date = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S%z')
            print(published_date)
            if published_date > last_date:
                videos.append(entry.link)
        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue

async def main():
    for channel in CHANNELS:
        await get_links(channel)

    bot = Bot(token=BOT_TOKEN)
    for link in videos:
        print(f"Sending: {link}")
        try:
            await bot.send_message(chat_id=CHAT_ID, text=link) 
        except Exception as e:
            print(f"Failed to send message: {e}")
        await asyncio.sleep(10)  # To avoid hitting Telegram rate limits

    # Update last_date.txt with the current time
    with open(file_path, 'w') as file:
        file.write(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z'))

# Run with a global timeout (optional)
asyncio.run(asyncio.wait_for(main(), timeout=120))

