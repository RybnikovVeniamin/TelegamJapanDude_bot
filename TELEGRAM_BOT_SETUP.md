# Telegram Keyword Counter Bot 🤖

This bot can be added to your Telegram channel and will count how many times a specific word (like "Japan") is mentioned. Every time someone mentions the word, the bot will post a message showing the total count.

## Step 1: Create Your Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat with BotFather and send the command: `/newbot`
3. BotFather will ask you to choose a name for your bot (e.g., "Japan Counter Bot")
4. Then choose a username for your bot (must end with "bot", e.g., "japan_counter_bot")
5. BotFather will give you a **token** that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. **Copy this token** - you'll need it in the next step!

## Step 2: Install Required Software

Open your terminal (command line) and run:

```bash
pip install -r requirements.txt
```

This will install the Telegram bot library.

## Step 3: Set Up Your Bot Token

You need to tell the bot what its token is. There are two ways:

### Option A: Set it temporarily (for testing)
In your terminal, run:
```bash
export TELEGRAM_BOT_TOKEN="8562930250:AAEeCXhc0ivFippDdai1jejVENAx88g8s7g"
```
Replace `your-token-here` with the actual token from BotFather.

### Option B: Set it permanently (recommended)
Create a file called `.env` in this folder and add:
```
TELEGRAM_BOT_TOKEN=your-token-here
```

## Step 4: Change the Keyword (Optional)

If you want to monitor a different word instead of "Japan", open `telegram_bot.py` and change this line:
```python
KEYWORD = "Japan"
```
to whatever word you want, for example:
```python
KEYWORD = "Tokyo"
```

## Step 5: Run the Bot

In your terminal, run:
```bash
python telegram_bot.py
```

You should see a message saying "Bot is running! Monitoring for keyword: Japan"

## Step 6: Add Bot to Your Channel

1. Go to your Telegram channel
2. Click on the channel name at the top
3. Go to "Administrators" or "Members"
4. Click "Add Administrator" or "Add Members"
5. Search for your bot by its username (the one you created with BotFather)
6. **Important**: Make sure to give the bot permission to:
   - Read messages
   - Send messages
   - Post messages (if it's a channel)

## Step 7: Test It!

Try sending a message in your channel that contains the word "Japan" (or whatever keyword you chose). The bot should reply with a count message!

## How It Works

- The bot watches all messages in the channel
- When it sees the keyword, it counts it
- It saves the count so it remembers even if you restart the bot
- Each time the keyword is mentioned, it posts a message like "It's 5 mentions of Japan in this chat"

## Troubleshooting

**Problem**: Bot doesn't respond
- Make sure the bot is running (you should see "Bot is running!" in your terminal)
- Check that the bot has permission to read and send messages in the channel
- Make sure you set the TELEGRAM_BOT_TOKEN correctly

**Problem**: "Please set TELEGRAM_BOT_TOKEN"
- You forgot to set the token. Go back to Step 3.

**Problem**: Bot responds to every message
- The bot only responds when it finds the keyword. If it's responding to everything, check that the KEYWORD is set correctly.

## Stopping the Bot

Press `Ctrl+C` in your terminal to stop the bot. The counts will be saved, so when you start it again, it will remember the previous counts.

