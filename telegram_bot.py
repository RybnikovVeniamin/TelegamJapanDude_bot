import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from collections import defaultdict

# Try to load from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# The word to monitor (you can change this)
KEYWORD = "Japan"

# File to store mention counts
COUNTS_FILE = "mention_counts.json"

# Load existing counts from file
def load_counts():
    """Load mention counts from file"""
    if os.path.exists(COUNTS_FILE):
        try:
            with open(COUNTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return defaultdict(int)
    return defaultdict(int)

# Save counts to file
def save_counts(counts):
    """Save mention counts to file"""
    with open(COUNTS_FILE, 'w') as f:
        json.dump(dict(counts), f)

# Load counts when bot starts
mention_counts = defaultdict(int, load_counts())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    # Only process messages from channels/groups
    if not update.message or not update.message.text:
        return
    
    # Get the chat ID (unique identifier for the channel/group)
    chat_id = str(update.message.chat_id)
    
    # Get the message text
    message_text = update.message.text.lower()
    
    # Check if the keyword is mentioned (case-insensitive)
    keyword_lower = KEYWORD.lower()
    if keyword_lower in message_text:
        # Count how many times the keyword appears in this message
        count_in_message = message_text.count(keyword_lower)
        
        # Update the total count for this chat
        mention_counts[chat_id] += count_in_message
        
        # Save to file
        save_counts(mention_counts)
        
        # Get the current total count
        total_count = mention_counts[chat_id]
        
        # Send a message to the chat
        response = f"It's {total_count} mention{'s' if total_count != 1 else ''} of {KEYWORD} in this chat"
        await update.message.reply_text(response)

def main():
    """Start the bot"""
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("ERROR: Please set TELEGRAM_BOT_TOKEN environment variable")
        print("You can get your bot token from @BotFather on Telegram")
        return
    
    # Create the application
    application = Application.builder().token(bot_token).build()
    
    # Add message handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print(f"Bot is running! Monitoring for keyword: {KEYWORD}")
    print("Add this bot to your channel and give it permission to read and send messages.")
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

