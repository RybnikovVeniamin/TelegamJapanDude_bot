import os
import json
import re
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from collections import defaultdict

# Try to load from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# Default keyword to start with
DEFAULT_KEYWORD = "Япония"
DEFAULT_KEYWORD_ROOT = "Япони"  # Root that matches all forms: Япония, Японию, Японии, Японией, etc.

# ALLOWED_CHANNEL_ID: Set this to your channel ID to restrict the bot to only one channel
# Leave as None to allow the bot to work in any channel
# To find your channel ID: add the bot, send a message, and check the console output
ALLOWED_CHANNEL_ID = None  # Change this to your channel ID (as a string, e.g., "-1001234567890")

# Files to store data
# Use /var/data/ on Render (persistent disk), otherwise use current directory
DATA_DIR = "/var/data" if os.path.exists("/var/data") else "."
COUNTS_FILE = os.path.join(DATA_DIR, "mention_counts.json")
KEYWORDS_FILE = os.path.join(DATA_DIR, "tracked_keywords.json")

if DATA_DIR == "/var/data":
    print("✅ Using persistent disk at /var/data - data will be saved!")
else:
    print("📁 Using local directory for data storage")

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

# Load tracked keywords from file
def load_keywords():
    """Load tracked keywords from file"""
    if os.path.exists(KEYWORDS_FILE):
        try:
            with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert old format (single keyword) to new format (list)
                if isinstance(data, str):
                    return [{"word": data, "root": data[:len(data)-1] if len(data) > 1 else data}]
                elif isinstance(data, list):
                    return data
                else:
                    return [{"word": DEFAULT_KEYWORD, "root": DEFAULT_KEYWORD_ROOT}]
        except:
            return [{"word": DEFAULT_KEYWORD, "root": DEFAULT_KEYWORD_ROOT}]
    return [{"word": DEFAULT_KEYWORD, "root": DEFAULT_KEYWORD_ROOT}]

# Save keywords to file
def save_keywords(keywords):
    """Save tracked keywords to file"""
    with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)

# Load data when bot starts
mention_counts = defaultdict(int, load_counts())
tracked_keywords = load_keywords()

async def what_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /what command - tells user what keywords the bot is tracking"""
    try:
        # Handle both regular messages and channel posts
        message = update.message
        if not message:
            message = update.channel_post
        
        if not message:
            return
        
        # Get the chat ID
        chat_id = str(message.chat_id)
        
        # If ALLOWED_CHANNEL_ID is set, only respond to that channel
        if ALLOWED_CHANNEL_ID is not None and chat_id != ALLOWED_CHANNEL_ID:
            return
        
        # Build response with all tracked keywords
        global tracked_keywords
        if len(tracked_keywords) == 1:
            response = f"Я отслеживаю упоминания слова: {tracked_keywords[0]['word']}"
        else:
            words_list = ", ".join([kw['word'] for kw in tracked_keywords])
            response = f"Я отслеживаю упоминания слов: {words_list}"
        
        try:
            await message.reply_text(response)
        except:
            # If reply fails (e.g., in channels), send as a new message
            await context.bot.send_message(chat_id=chat_id, text=response)
    except Exception as e:
        print(f"Error in what_command: {e}")
        import traceback
        traceback.print_exc()

async def setcount_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setcount command - manually set the counter value"""
    try:
        message = update.message
        if not message:
            message = update.channel_post
        
        if not message:
            return
        
        chat_id = str(message.chat_id)
        
        if ALLOWED_CHANNEL_ID is not None and chat_id != ALLOWED_CHANNEL_ID:
            return
        
        # Get the number from command arguments
        if not context.args or len(context.args) == 0:
            response = "Укажите число. Например: /setcount 58"
            try:
                await message.reply_text(response)
            except:
                await context.bot.send_message(chat_id=chat_id, text=response)
            return
        
        try:
            new_count = int(context.args[0])
        except ValueError:
            response = "Пожалуйста, укажите число. Например: /setcount 58"
            try:
                await message.reply_text(response)
            except:
                await context.bot.send_message(chat_id=chat_id, text=response)
            return
        
        global mention_counts
        mention_counts[chat_id] = new_count
        save_counts(mention_counts)
        
        response = f"✅ Счётчик установлен на {new_count}"
        try:
            await message.reply_text(response)
        except:
            await context.bot.send_message(chat_id=chat_id, text=response)
            
    except Exception as e:
        print(f"Error in setcount_command: {e}")
        import traceback
        traceback.print_exc()

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /add command - adds a new keyword to track"""
    try:
        # Handle both regular messages and channel posts
        message = update.message
        if not message:
            message = update.channel_post
        
        if not message:
            return
        
        # Get the chat ID
        chat_id = str(message.chat_id)
        
        # If ALLOWED_CHANNEL_ID is set, only respond to that channel
        if ALLOWED_CHANNEL_ID is not None and chat_id != ALLOWED_CHANNEL_ID:
            return
        
        # Get the word from command arguments
        if not context.args or len(context.args) == 0:
            response = "Пожалуйста, укажите слово для отслеживания. Например: /add Токио"
            try:
                await message.reply_text(response)
            except:
                await context.bot.send_message(chat_id=chat_id, text=response)
            return
        
        new_word = " ".join(context.args)  # Join in case word has spaces
        new_word = new_word.strip()
        
        if not new_word:
            response = "Пожалуйста, укажите слово для отслеживания."
            try:
                await message.reply_text(response)
            except:
                await context.bot.send_message(chat_id=chat_id, text=response)
            return
        
        global tracked_keywords
        
        # Check if word already exists
        for kw in tracked_keywords:
            if kw['word'].lower() == new_word.lower():
                response = f"Слово '{new_word}' уже отслеживается."
                try:
                    await message.reply_text(response)
                except:
                    await context.bot.send_message(chat_id=chat_id, text=response)
                return
        
        # Extract root (for Russian words, use first few letters)
        # Simple approach: use the word itself as root, or remove last 1-2 characters
        root = new_word
        if len(new_word) > 3:
            # For Russian, try to get root by removing last 1-2 characters
            root = new_word[:-1] if len(new_word) > 4 else new_word
        
        # Add new keyword
        tracked_keywords.append({"word": new_word, "root": root})
        save_keywords(tracked_keywords)
        
        response = f"Добавлено слово для отслеживания: {new_word}"
        try:
            await message.reply_text(response)
        except:
            await context.bot.send_message(chat_id=chat_id, text=response)
            
    except Exception as e:
        print(f"Error in add_command: {e}")
        import traceback
        traceback.print_exc()

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /list command - shows all tracked keywords"""
    try:
        # Handle both regular messages and channel posts
        message = update.message
        if not message:
            message = update.channel_post
        
        if not message:
            return
        
        # Get the chat ID
        chat_id = str(message.chat_id)
        
        # If ALLOWED_CHANNEL_ID is set, only respond to that channel
        if ALLOWED_CHANNEL_ID is not None and chat_id != ALLOWED_CHANNEL_ID:
            return
        
        global tracked_keywords
        
        if len(tracked_keywords) == 0:
            response = "Нет отслеживаемых слов."
        else:
            words_list = "\n".join([f"• {kw['word']}" for kw in tracked_keywords])
            response = f"Отслеживаемые слова:\n{words_list}"
        
        try:
            await message.reply_text(response)
        except:
            await context.bot.send_message(chat_id=chat_id, text=response)
    except Exception as e:
        print(f"Error in list_command: {e}")
        import traceback
        traceback.print_exc()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    try:
        # Handle both regular messages and channel posts
        message = update.message
        if not message:
            # Try channel post instead
            message = update.channel_post
        
        if not message or not message.text:
            return
        
        # Get the chat ID (unique identifier for the channel/group)
        chat_id = str(message.chat_id)
        
        # Print chat ID to help user find their channel ID (remove this after setting ALLOWED_CHANNEL_ID)
        print(f"Message from chat ID: {chat_id}, text: {message.text[:50]}...")
        
        # If ALLOWED_CHANNEL_ID is set, only respond to that channel
        if ALLOWED_CHANNEL_ID is not None and chat_id != ALLOWED_CHANNEL_ID:
            print(f"Ignoring message from chat {chat_id} (not allowed)")
            return  # Ignore messages from other channels
        
        # Get the message text (keep original case for Russian)
        message_text = message.text
        
        # Check if any tracked keyword is mentioned
        # Extract all words (Russian and other characters)
        words = re.findall(r'[а-яёА-ЯЁa-zA-Z]+', message_text)
        
        # Check all tracked keywords - all contribute to ONE shared counter
        global tracked_keywords
        all_matches = []
        matched_keywords = []
        
        for keyword_info in tracked_keywords:
            keyword_root = keyword_info['root']
            keyword_word = keyword_info['word']
            # Find matches for this keyword (check both exact match and root match)
            # This allows matching "Japan" and "Япония" even though they're different words
            matches = []
            for word in words:
                word_lower = word.lower()
                keyword_lower = keyword_word.lower()
                root_lower = keyword_root.lower()
                # Check if word matches the keyword exactly or starts with the root
                if word_lower == keyword_lower or word_lower.startswith(root_lower):
                    matches.append(word)
            
            if matches:
                all_matches.extend(matches)
                # Only add keyword to matched_keywords list if not already there
                if keyword_word not in matched_keywords:
                    matched_keywords.append(keyword_word)
        
        if all_matches:
            # Count how many times ANY tracked word appears in this message
            # All tracked words contribute to the SAME counter
            count_in_message = len(all_matches)
            
            # If this is the first mention for this chat, start from 55
            if chat_id not in mention_counts or mention_counts[chat_id] == 0:
                mention_counts[chat_id] = 55 - count_in_message
            
            # Update the total count for this chat
            mention_counts[chat_id] += count_in_message
            
            # Save to file
            save_counts(mention_counts)
            
            # Get the current total count
            total_count = mention_counts[chat_id]
            
            # Send a message to the chat (in Russian)
            try:
                # Create response - all tracked words share ONE counter
                # Show which words were mentioned, but emphasize it's one shared count
                if len(matched_keywords) == 1:
                    keyword = matched_keywords[0]
                    messages = [
                        f"Красавчики опять заговорили про {keyword.lower()}, это уже {total_count} раз",
                        f"Так, ещё одно упомянутие {keyword} ({total_count}) и мы покупаем билеты",
                        f"{keyword} в этом чате упомянули уже {total_count} раз"
                    ]
                else:
                    keywords_str = ", ".join(matched_keywords)
                    messages = [
                        f"Красавчики опять заговорили про {keywords_str.lower()}, это уже {total_count} раз (всего)",
                        f"Так, ещё одно упомянутие ({keywords_str}) - всего {total_count}",
                        f"В этом чате упомянули уже {total_count} раз (все отслеживаемые слова)"
                    ]
                
                response = random.choice(messages)
                # Try to reply, if that fails, send a new message
                try:
                    await message.reply_text(response)
                except:
                    # If reply fails (e.g., in channels), send as a new message
                    await context.bot.send_message(chat_id=chat_id, text=response)
            except Exception as e:
                print(f"Error sending message: {e}")
                import traceback
                traceback.print_exc()
                # Don't crash if we can't send a message
    except Exception as e:
        print(f"Error in handle_message: {e}")
        import traceback
        traceback.print_exc()

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
    
    # Add command handlers
    application.add_handler(CommandHandler("what", what_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("setcount", setcount_command))
    
    # Add message handler for all text messages (both regular messages and channel posts)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Also handle channel posts separately (in case they're not caught by the above)
    application.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POSTS & filters.TEXT, handle_message))
    
    # Show tracked keywords on startup
    keywords_list = ", ".join([kw['word'] for kw in tracked_keywords])
    print(f"Bot is running! Monitoring for keywords: {keywords_list}")
    print("Add this bot to your channel and give it permission to read and send messages.")
    print("Commands: /what, /add <word>, /list, /setcount <number>")
    
    # Start the bot with error handling
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Exception as e:
        print(f"Error running bot: {e}")
        raise

if __name__ == '__main__':
    main()

