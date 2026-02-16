
import os
import requests
import logging
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configuration with Validation
def get_env_or_fail(key, default=None):
    value = os.getenv(key, default)
    if not value:
        raise ValueError(f"Environment variable {key} is missing")
    return value

try:
    TELEGRAM_BOT_TOKEN = get_env_or_fail("TELEGRAM_BOT_TOKEN")
    PAPERLESS_API_URL = get_env_or_fail("PAPERLESS_API_URL", "http://webserver:8000/api")
    PAPERLESS_API_TOKEN = get_env_or_fail("PAPERLESS_API_TOKEN")
except ValueError as e:
    print(f"Startup Error: {e}")
    exit(1)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Rate Limiting (Simple Token Bucket)
class RateLimiter:
    def __init__(self, rate_limit=5, time_window=60):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.user_requests = {}

    def is_allowed(self, user_id):
        current_time = time.time()
        # Clean old requests
        if user_id in self.user_requests:
             self.user_requests[user_id] = [t for t in self.user_requests[user_id] if current_time - t < self.time_window]
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = []
            
        if len(self.user_requests[user_id]) < self.rate_limit:
            self.user_requests[user_id].append(current_time)
            return True
        return False

rate_limiter = RateLimiter()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="MedicalVault Bot Online! Use /search <query> to find documents.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not rate_limiter.is_allowed(user_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Slow down! You are sending too many requests.")
        return

    query = " ".join(context.args)
    if not query:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a search query. Example: /search x-quang")
        return

    # safe encoding handled by requests params
    headers = {
        "Authorization": f"Token {PAPERLESS_API_TOKEN}"
    }
    
    try:
        response = requests.get(f"{PAPERLESS_API_URL}/documents/", params={'query': query}, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        if not results:
             await context.bot.send_message(chat_id=update.effective_chat.id, text="No documents found.")
             return

        message = f"Found {data.get('count', 0)} documents:\n"
        for i, doc in enumerate(results[:5]): # Limit to 5 results
            message += f"{i+1}. {doc['title']} (ID: {doc['id']})\n"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error searching documents: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Connection error to Document Server.")
    except Exception as e:
        logging.error(f"Error searching documents: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ An error occurred while searching.")

async def recent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not rate_limiter.is_allowed(user_id):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Slow down! You are sending too many requests.")
        return

    headers = {
        "Authorization": f"Token {PAPERLESS_API_TOKEN}"
    }
    
    try:
        response = requests.get(f"{PAPERLESS_API_URL}/documents/", params={'ordering': '-created'}, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        if not results:
             await context.bot.send_message(chat_id=update.effective_chat.id, text="No documents found.")
             return

        message = f"Recent 5 documents:\n"
        for i, doc in enumerate(results[:5]):
            message += f"{i+1}. {doc['title']} (ID: {doc['id']})\n"
        
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error getting recent documents: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Connection error to Document Server.")
    except Exception as e:
        logging.error(f"Error getting recent documents: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ An error occurred.")

if __name__ == '__main__':
    # Validation happened at top level
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    search_handler = CommandHandler('search', search)
    recent_handler = CommandHandler('recent', recent)
    
    application.add_handler(start_handler)
    application.add_handler(search_handler)
    application.add_handler(recent_handler)
    
    print("Bot is polling...")
    application.run_polling()
