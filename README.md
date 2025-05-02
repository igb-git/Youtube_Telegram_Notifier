# YouTube Telegram Notifier

This Python script monitors a list of YouTube channel RSS feeds and sends new video links to a Telegram channel. Obviously, you need a channel and a bot with administrator rights and authorization to add messages. You get the BOT_TOKEN when you create the bot using Telegram's @BotFather,then you add your bot to your channel, make him admin, and allow it to manage messages. You can get your channel id using Telegram bots such as @IDBot.

## Features

- Reads channel RSS URLs from `channels.txt`
- Remembers the last checked date to avoid duplicate notifications
- Sends new video links to a Telegram chat via a bot

## Setup

1. **Clone the repository** and install requirements:
git clone https://github.com/yourusername/yt-telegram-notifier.git
cd yt-telegram-notifier
pip install -r requirements.txt


2. **Create a `.env` file** in the project directory:
API_KEY=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id

3. **Create `channels.txt`** in the project directory, listing one YouTube RSS URL per line.
You can comment lines with `#`:


3. **Create `channels.txt`** in the project directory, listing one YouTube RSS URL per line.
You can comment lines with `#`:

https://www.youtube.com/feeds/videos.xml?channel_id=UCciQ8wFcVoIIMi-lfu8-cjQ # Anton Petrov
https://www.youtube.com/feeds/videos.xml?channel_id=UCZ9jWH_8tJ-Nmaj8dSQdEYA # Stefan Milov

*You can get the channel_id from the channel description > Share channel*
