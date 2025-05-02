import asyncio
from datetime import datetime, timedelta, timezone
import feedparser
from telegram import Bot
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Set, Optional
import os
import sys

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("Error: API_KEY and/or CHAT_ID not set in environment variables.")
    sys.exit(1)

def load_channels(filename: str) -> List[str]:
    """Load channel RSS URLs from a file, ignoring comments and blank lines."""
    path = Path(filename)
    if not path.exists():
        print(f"Error: {filename} does not exist.")
        sys.exit(1)
    with path.open("r", encoding="utf-8") as file:
        return [line.split('#', 1)[0].strip() for line in file if line.strip() and not line.strip().startswith("#")]

def load_last_date(path: Path) -> datetime:
    """Load the last checked date from a file, or return 1 day ago if not found."""
    try:
        with open(path, 'r') as file:
            last_date_str = file.read().strip()
            return datetime.strptime(last_date_str, '%Y-%m-%dT%H:%M:%S%z')
    except FileNotFoundError:
        return datetime.now(timezone.utc) - timedelta(days=1)
    except Exception as e:
        print(f"Error reading last_date: {e}")
        return datetime.now(timezone.utc) - timedelta(days=1)

def save_last_date(path: Path, dt: datetime):
    """Save the current date as the last checked date."""
    with open(path, 'w') as file:
        file.write(dt.strftime('%Y-%m-%dT%H:%M:%S%z'))

async def fetch_new_video_links(rss_url: str, since: datetime) -> Set[str]:
    """Fetch new video links from a YouTube RSS feed published after 'since'."""
    d = feedparser.parse(rss_url)
    links = set()
    for entry in d.entries:
        try:
            published = entry.published
            published_date = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S%z')
            if published_date > since:
                links.add(entry.link)
        except Exception as e:
            print(f"Error parsing entry: {e}")
    return links

async def send_telegram_messages(bot: Bot, chat_id: int, links: List[str]):
    """Send messages with video links to the specified Telegram chat."""
    for link in links:
        print(f"Sending: {link}")
        try:
            await bot.send_message(chat_id=chat_id, text=link)
        except Exception as e:
            print(f"Failed to send message: {e}")
        await asyncio.sleep(10)  # To avoid Telegram rate limits

async def main():
    script_dir = Path(__file__).parent
    file_path = script_dir / "last_date.txt"
    channels_file = script_dir / "channels.txt"

    channels = load_channels(str(channels_file))
    last_date = load_last_date(file_path)
    print(f"Last checked date: {last_date}")

    # Fetch all new video links concurrently
    tasks = [fetch_new_video_links(url, last_date) for url in channels]
    results = await asyncio.gather(*tasks)
    new_links = sorted(set().union(*results))

    if new_links:
        bot = Bot(token=BOT_TOKEN)
        await send_telegram_messages(bot, int(CHAT_ID), new_links)
        save_last_date(file_path, datetime.now(timezone.utc))
        print(f"Sent {len(new_links)} new video(s).")
    else:
        print("No new videos found.")

if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=120))

