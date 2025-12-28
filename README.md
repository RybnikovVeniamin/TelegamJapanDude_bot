# Telegram Keyword Counter Bot 🤖

A Telegram bot that monitors a channel and counts how many times a specific word (like "Japan") is mentioned. Every time someone mentions the keyword, the bot posts a message showing the total count.

## What It Does

- Monitors messages in your Telegram channel
- Counts mentions of a specific keyword (default: "Japan")
- Posts a count message each time the keyword is mentioned
- Remembers counts even after restarting

## Quick Start

1. **Get a bot token** from [@BotFather](https://t.me/BotFather) on Telegram
2. **Install dependencies**: `pip3 install -r requirements.txt`
3. **Set your token**: Create a `.env` file with `TELEGRAM_BOT_TOKEN=your-token-here`
4. **Run the bot**: `python3 telegram_bot.py`
5. **Add bot to your channel** and give it permission to read and send messages

## Change the Keyword

Edit `telegram_bot.py` and change this line:
```python
KEYWORD = "Japan"
```
to whatever word you want to monitor.

## Deploy to Cloud

See `CLOUD_DEPLOYMENT.md` for instructions on running the bot 24/7 in the cloud (free options available).

## Files

- `telegram_bot.py` - The main bot code
- `requirements.txt` - Python packages needed
- `TELEGRAM_BOT_SETUP.md` - Detailed setup instructions
- `CLOUD_DEPLOYMENT.md` - Guide for cloud deployment

## How It Works

1. Bot watches all messages in the channel
2. When it sees the keyword, it counts it
3. Saves the count to a file (so it remembers)
4. Posts a message like "It's 5 mentions of Japan in this chat"

Enjoy your keyword counter bot! 🚀
